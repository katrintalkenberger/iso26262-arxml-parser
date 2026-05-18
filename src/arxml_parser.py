import lxml.etree as ET
import os
from typing import Dict, List, Any, Optional

class ARXMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.root = None
        self.ns = {}

    def load(self) -> bool:
        """Loads and parses the ARXML file safely."""
        try:
            # Parse ARXML file
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            # Extract namespace
            if "}" in self.root.tag:
                auto_ns = self.root.tag.split("}")[0].strip("{")
                self.ns = {'ns': auto_ns}
            return True        
        except Exception as e:
            print(f"Error loading ARXML: {e}")
            return False

    def get_elements(self, element: ET._Element, tag_name: str, direct_only: bool=True) -> List[ET._Element]:
        """Find all child elements matching the given local name.

        Input-Arguments:
            - element: ARXML element starting point
            - tag_name: Local name of the target XML tag (e.g. 'RUNNABLE-ENTITY').
            - direct_only: If True, only search next level (./). 
                           If False, search complete subtree (.//).
        Returns:
            - List of lxml elements (empty list if no elements match).
        """
        xpath_prefix = "./" if direct_only else ".//"
        return element.xpath(f"{xpath_prefix}*[local-name()='{tag_name}']")
    
    def get_single_element(self, element: ET._Element, tag_name: str, direct_only: bool=True, default: Any=None) -> Any:
        """Find the first child element matching the given local name.

        Input-Arguments:
            - element: ARXML element starting point
            - tag_name: Local name of the target XML tag (e.g. 'INTERNAL-BEHAVIORS').
            - direct_only: If True, only search next level (./). 
                           If False, search complete subtree (.//).
            - default: Return value, if element does not exist.
        Returns:
            - Single ARXML element or default value.
        """
        elements = self.get_elements(element, tag_name, direct_only)
        return elements[0] if elements else default


    def get_element_text(self, element: ET._Element, tag_name: str, direct_only: bool = True, default: Any = None) -> Optional[str]:
        """Extract text value of an ARXML element given its local name.

        Input-Arguments:
            - element: ARXML element starting point
            - tag_name: Local name of XML tag (e.g. 'SHORT-NAME').
            - direct_only: If True, only search next level (./). 
                           If False, search complete subtree (.//).
            - default: return value, if element does not exist.
        Returns:
            - Text of ARXML element (None if element does not exist).            
        """
        xpath_prefix = "./" if direct_only else ".//"
        element_text_list = element.xpath(f"{xpath_prefix}*[local-name()='{tag_name}']/text()")
        
        return element_text_list[0] if element_text_list else default

    def get_all_composition_swcs(self):
        """Get all composition software components."""

        return self.get_elements(self.root,"COMPOSITION-SW-COMPONENT-TYPE",direct_only=False)
    
    def get_composition_swc_ref(self, composition: ET._Element) -> Dict[str, List[str]]:
        """Get all SWC references of a composition."""
        data: Dict[str, List[str]] = {"swc_names": [], "swc_refs": []}
        all_swc = self.get_elements(composition,"SW-COMPONENT-PROTOTYPE",direct_only=False)
        for swc in all_swc:
            data["swc_names"].append(self.get_element_text(swc,"SHORT-NAME"))
            data["swc_refs"].append(self.get_element_text(swc,"TYPE-TREF"))
        return data

    def get_all_atomic_swcs(self) -> List[ET._Element]:
        """Get all atomic software components.
        
        An ARXML can contain one or more of the following atomic software components:
        - APPLICATION-SW-COMPONENT-TYPE
        - COMPLEX-DEVICE-DRIVER-SW-COMPONENT-TYPE
        - SERVICE-SW-COMPONENT-TYPE
        """
        if self.root is None:
            return []
        return self.root.xpath(
            "//*[contains(local-name(), 'SW-COMPONENT-TYPE') and " \
            "local-name() != 'COMPOSITION-SW-COMPONENT-TYPE']"
        )
    
    def get_swc_internal_behavior(self, swc_element: ET._Element) -> tuple[dict, list]:
        """Parse the internal behavior and validates ISO 26262 integrity.
        
        Returns:
            - dict: Cleaned architecture metadata (events, runnables, pims, parameters)
            - list: Found architectural and safety compliance issues
        """        
        internal_behavior = {
            "events": [],
            "runnables": [],
            "pims": [],
            "parameters": []
        }
        issues = []

        swc_name = self.get_element_text(swc_element, "SHORT-NAME", default="Unknown_SWC")

        # 1. Get all events
        events_element = self.get_elements(swc_element,"EVENTS",direct_only=False)
        events_references = []

        if events_element:
            all_events = list(events_element[0])
            for event in all_events:
                event_type = str(event.xpath("local-name()"))
                event_name = self.get_element_text(event,"SHORT-NAME")
                event_ref = self.get_element_text(event,"START-ON-EVENT-REF")

                # ISO 26262 Check: Orphaned event without a Runnable reference
                if not event_ref:
                    issues.append({
                        "severity": "ERROR",
                        "type": "Orphaned Event",
                        "description": f"Event '{event_name}' in SWC '{swc_name}' is missing the runnable reference (`START-ON-EVENT-REF`)."
                    })
                    continue  # Without a reference, the mapping doesn't make sense

                # Additional information:
                extra_info = "N/A"
                if event_type == "TIMING-EVENT":
                    # Get period time (e.g. 0.01s)
                    period = self.get_element_text(event,"PERIOD")
                    # ISO 26262 Check: Invalid or missing timing compromises determinism
                    if not period or float(period) <= 0:
                        issues.append({
                            "severity": "CRITICAL",
                            "type": "Invalid Timing",
                            "description": f"Timing-Event '{event_name}' in SWC '{swc_name}' has invalid period ({period}s)."
                        })
                    extra_info = f"Period: {period}s"
                elif event_type == "OPERATION-INVOKED-EVENT":
                    # Get referenced server operation name
                    op_ref = event.xpath(".//*[@DEST='CLIENT-SERVER-OPERATION']")
                    if op_ref:
                        extra_info = f"Operation Ref: {op_ref[0].text}"
                # TODO: Any other event types with additional information?
                
                internal_behavior["events"].append([event_type, event_name, event_ref, extra_info])
                events_references.append(event_ref)

        # 2. get all runnables
        all_runnables = self.get_elements(swc_element,"RUNNABLE-ENTITY",direct_only=False)
        for runnable in all_runnables:
            runnable_name = self.get_element_text(runnable,"SHORT-NAME",1)
            if not runnable_name:
                continue

            # Get corresponding event(s)
            found_any_event = False
            for idx, ref in enumerate(events_references):
                if ref and (ref.endswith(f"/{runnable_name}") or ref == runnable_name):
                    found_any_event = True

                    # Get event data from reference list
                    evt = internal_behavior["events"][idx]
                    internal_behavior["runnables"].append({
                        "name": runnable_name,
                        "trigger_type": evt[0],
                        "event_name": evt[1],
                        "extra_info": evt[3]
                    })
            
            # ISO 26262 Check: Untriggered, passive runnable
            if not found_any_event:
                internal_behavior["runnables"].append({
                    "name": runnable_name,
                    "trigger_type": "NO-EVENT (Passive / Call-Return)",
                    "event_name": "N/A",
                    "extra_info": "N/A"
                })
                issues.append({
                    "severity": "WARNING",
                    "type": "Untriggered Runnable",
                    "description": f"Runnable '{runnable_name}' in SWC '{swc_name}' is not being actively triggered by any event."
                })                

        # 3. Get all per-instance-memorys (PIMs)
        pims_element = self.get_elements(swc_element,"AR-TYPED-PER-INSTANCE-MEMORYS",direct_only=False)
        if pims_element:
            all_pims = list(pims_element[0])
            for pim in all_pims:
                internal_behavior["pims"].append(self.get_element_text(pim,"SHORT-NAME"))

        # 4. Get all parameters
        params_element = self.get_elements(swc_element,"SHARED-PARAMETERS",direct_only=False)
        if params_element:
            all_params = list(params_element[0])
            for param in all_params:
                internal_behavior["parameters"].append(self.get_element_text(param,"SHORT-NAME"))        
        
        return internal_behavior, issues
    

    def export_to_markdown(self, all_swc_details: list, all_architecture_issues: list, filename: str) -> None:
        """Generates a comprehensive architecture and ISO 26262 compliance report. 
        
        Writes all collected SWC data and architecture errors to a single file."""
        # Ensure that destination directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            # 1. HEADLINE AND INTRODUCTION
            f.write("# AUTOSAR Architecture & ISO 26262 Safety Report\n\n")
            f.write("This document contains the static architectural analysis and the  ")
            f.write("compliance check in accordance with the requirements of **ISO 26262-6** ")
            f.write("completeness and consistency). \n\n")
            
            # 2. ISO 26262 COMPLIANCE DASHBOARD
            f.write("## ⚠️ ISO 26262 Architectural Integrity Check\n\n")
            if all_architecture_issues:
                # Count error classes for quick overview
                criticals = sum(1 for i in all_architecture_issues if i["severity"] == "CRITICAL")
                errors = sum(1 for i in all_architecture_issues if i["severity"] == "ERROR")
                warnings = sum(1 for i in all_architecture_issues if i["severity"] == "WARNING")
                f.write("**Status:** 🛑 Architektur-Verletzungen gefunden! ")
                f.write(f"{criticals} Critical, {errors} Error, {warnings} Warning)\n\n")
                
                # Markdown table for the discrepancies
                f.write("| Schweregrad | Fehlertyp | Beschreibung |\n")
                f.write("| :--- | :--- | :--- |\n")
                for issue in all_architecture_issues:
                    if issue["severity"] == "CRITICAL":
                        sev_emoji = "🚨"
                    elif issue["severity"] == "ERROR":
                        sev_emoji = "❌"
                    else:
                        sev_emoji = "⚠️"
                    f.write(f"| {sev_emoji} {issue['severity']} | {issue['type']} | {issue['description']} |\n")
                f.write("\n")
            else:
                f.write("**Status:** ✅ Pass (No structural violations or orphaned elements found).\n\n")
            
            f.write("---\n\n")
            
            # 3. SOFTWARE COMPONENT DETAILS
            f.write("## 🧩 Software Component Details\n\n")
            for swc in all_swc_details:
                swc_name = swc["name"]
                details = swc["details"]
                
                # Add SWC headline
                f.write(f"### Software Component: {swc_name}\n\n")
                
                # Add runnable information
                f.write("#### Runnables\n")
                if details["runnables"]:
                    f.write("| Runnable name | Event type | Event name | Additional info |\n")
                    f.write("| :--- | :--- | :--- | :--- |\n")            
                    for row in details["runnables"]:
                        f.write(f"| {row['name']} | {row['trigger_type']} | {row['event_name']} | {row['extra_info']} |\n")
                else:
                    f.write("N/A")
                f.write("\n\n")
                
                # Add per-instance-memory (PIM) information
                f.write("#### Per-Instance Memories (PIMs)\n")
                if details["pims"]:
                    for pim in details["pims"]:
                        f.write(f"- `{pim}`\n")
                else:
                    f.write("N/A\n")
                f.write("\n")
                
                # Add shared-parameters information
                f.write("#### Shared Parameters\n")
                if details["parameters"]:
                    for param in details["parameters"]:
                        f.write(f"- `{param}`\n")
                else:
                    f.write("N/A\n")
                f.write("\n---\n\n")             