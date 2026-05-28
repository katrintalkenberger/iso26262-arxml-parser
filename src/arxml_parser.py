"""AUTOSAR ARXML core parsing and ISO 26262 compliance engine.

This module provides the central ARXMLParser class, which leverages lxml 
to safely load XML structures, extract architectural metadata, and execute 
structural functional safety checks for automotive software components.
"""

import lxml.etree as ET
import os
from typing import Dict, List, Tuple, Any, Optional
from src.exceptions import ARXMLValidationError

class ARXMLParser:
    """Parses and validates functional safety attributes from AUTOSAR files.

    This class serves as the core compliance engine, utilizing lxml to load 
    ARXML files, map namespaces dynamically, and evaluate architectural 
    elements against structural automotive safety criteria.
    """

    def __init__(self, file_path):
        """Initializes the parser instance with a target file path.

        Args:
            file_path (str): The physical file system path to the input 
                AUTOSAR ARXML configuration file.
        """        
        self.file_path = file_path
        self.tree = None
        self.root = None
        self.ns = {}

    def load(self) -> bool:
        """Safely loads and parses the ARXML file into an in-memory tree.

        Reads the physical file using lxml, extracts the root element, 
        validates the global AUTOSAR schema definition, and registers 
        the dynamic XML namespace dictionary for downstream parsing.

        Returns:
            bool: True if the file was loaded and validated as a valid 
                AUTOSAR structure. False if any parsing, validation, or 
                I/O error occurred.
        """
        try:
            # Parse ARXML file
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()

              # Check if file is AUTOSAR xml
            if "}" in self.root.tag:
                local_tag = self.root.tag.split("}")[-1]
            else:
                local_tag = self.root.tag

            if local_tag != "AUTOSAR":
                raise ARXMLValidationError(
                    "The file is valid XML, but not a valid AUTOSAR "
                    "structure."
                )  
                       
            # Extract namespace
            if "}" in self.root.tag:
                auto_ns = self.root.tag.split("}")[0].strip("{")
                self.ns = {'ns': auto_ns}
            return True        
        except Exception as e:
            print(f"Error loading ARXML: {e}")
            return False

    def get_elements(self, element: ET._Element, tag_name: str, direct_only: bool=True) -> List[ET._Element]:
        """Finds all child elements matching the given local XML tag name.

        Uses localized XPath queries to bypass strict namespace prefixes,
        allowing robust extraction of specific AUTOSAR architectural elements.

        Args:
            element (ET._Element): The starting XML node for the search.
            tag_name (str): Local name of the target XML tag 
                (e.g., 'RUNNABLE-ENTITY').
            direct_only (bool): If True, only searches immediate children 
                ('./'). If False, searches the full subtree recursively 
                ('.//').

        Returns:
            List[ET._Element]: A list of matching lxml element nodes. 
                Returns an empty list if no elements match the criteria.
        """
        xpath_prefix = "./" if direct_only else ".//"
        return element.xpath(f"{xpath_prefix}*[local-name()='{tag_name}']")
    
    def get_single_element(self, element: ET._Element, tag_name: str, direct_only: bool=True, default: Any=None) -> Any:
        """Finds the first child element matching the given local tag name.

        Queries the underlying tree and extracts the first matching node.
        If no matching element is found, a customizable fallback value 
        is returned.

        Args:
            element (ET._Element): The starting XML node for the search.
            tag_name (str): Local name of the target XML tag 
                (e.g., 'INTERNAL-BEHAVIORS').
            direct_only (bool): If True, only searches immediate children. 
                If False, searches the full subtree recursively.
            default (Any): The fallback value to return if the element 
                does not exist. Defaults to None.

        Returns:
            Any: The first matching ET._Element node if found; otherwise, 
                the specified default value.
        """
        elements = self.get_elements(element, tag_name, direct_only)
        return elements[0] if elements else default


    def get_element_text(self, element: ET._Element, tag_name: str, direct_only: bool = True, default: Any = None) -> Optional[str]:
        """Extracts the stripped text content of an ARXML element.

        Queries the node for a specific child tag and extracts its text
        payload. Commonly used to parse identifiers like 'SHORT-NAME'.

        Args:
            element (ET._Element): The starting XML node for the search.
            tag_name (str): Local name of the target XML tag 
                (e.g., 'SHORT-NAME').
            direct_only (bool): If True, only searches immediate children.
                If False, searches the full subtree recursively.
            default (Any): The fallback value to return if the element 
                does not exist or contains no text. Defaults to None.

        Returns:
            Optional[str]: The stripped text value of the element if found; 
                otherwise, the specified default value.
        """
        xpath_prefix = "./" if direct_only else ".//"
        element_text_list = element.xpath(f"{xpath_prefix}*[local-name()='{tag_name}']/text()")
        
        return element_text_list[0] if element_text_list else default

    def get_all_composition_swcs(self):
        """Extracts all top-level Composition Software Components from the tree.

        Scans the entire XML document for composition types that define 
        the high-level software component architecture mapping.

        Returns:
            List[ET._Element]: A list of matching lxml elements representing
                COMPOSITION-SW-COMPONENT-TYPE structures.
        """
        return self.get_elements(self.root,"COMPOSITION-SW-COMPONENT-TYPE",direct_only=False)
    
    def get_composition_swc_ref(self, composition: ET._Element) -> Dict[str, List[str]]:
        """Maps all internal software component prototype references.

        Iterates through the structural prototypes of a composition component
        and extracts their local names and type definitions.

        Args:
            composition (ET._Element): The composition component XML node 
                to analyze.

        Returns:
            Dict[str, List[str]]: A dictionary containing architecture maps:
                - "swc_names": List of prototype short-names.
                - "swc_refs": List of corresponding type references (TREF).
        """
        data: Dict[str, List[str]] = {"swc_names": [], "swc_refs": []}
        all_swc = self.get_elements(composition,"SW-COMPONENT-PROTOTYPE",direct_only=False)
        for swc in all_swc:
            data["swc_names"].append(self.get_element_text(swc,"SHORT-NAME"))
            data["swc_refs"].append(self.get_element_text(swc,"TYPE-TREF"))
        return data

    def get_all_atomic_swcs(self) -> List[ET._Element]:
        """Scans the structure for all standard Atomic Software Component Types.

        Queries the XML tree for component definitions while filtering out 
        high-level composition containers. Covers Application, Complex Device 
        Driver (CDD), and Service software component types.

        Returns:
            List[ET._Element]: A filtered list of lxml element nodes matching 
                the atomic component criteria. Returns an empty list if the 
                tree root is uninitialized.
        """
        if self.root is None:
            return []
        xpath_query = (
            "//*[contains(local-name(), 'SW-COMPONENT-TYPE') and "
            "local-name() != 'COMPOSITION-SW-COMPONENT-TYPE']"
        )
        return self.root.xpath(xpath_query)
    
    def get_swc_internal_behavior(self, swc_element: ET._Element) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
        """Parses internal behaviors and runs structural ISO 26262 safety checks.

        Extracts runtime attributes (Events, Runnables, Per-Instance Memory, 
        and Parameters) and checks them against deterministic ASIL-B design rules 
        to capture orphaned events, invalid timing periods, or passive runnables.

        Args:
            swc_element (ET._Element): The atomic software component XML node 
                to evaluate.

        Returns:
            Tuple[Dict[str, Any], List[Dict[str, str]]]: A compound tuple:
                - Dict[str, Any]: Extracted metadata maps for events, 
                  runnables, pims, and parameters.
                - List[Dict[str, str]]: A list of structural safety issues, 
                  where each issue contains 'severity', 'type', and 
                  'description' keys.
        """       
        internal_behavior = {
            "events": [],
            "runnables": [],
            "pims": [],
            "parameters": []
        }
        issues = []

        swc_name = self.get_element_text(swc_element, "SHORT-NAME", default="Unknown_SWC")

        # 1. Process and validate AUTOSAR Events
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
                        "description": (
                            f"Event '{event_name}' in SWC '{swc_name}' is "
                            f"missing the runnable reference "
                            f"(`START-ON-EVENT-REF`)."
                        )
                    })
                    continue  # Without a reference, the mapping doesn't make sense

                # Additional information:
                extra_info = "N/A"
                if event_type == "TIMING-EVENT":
                    # ISO 26262 Check: Invalid or missing timing compromises determinism
                    period = self.get_element_text(event,"PERIOD")
                    if not period or float(period) <= 0:
                        issues.append({
                            "severity": "CRITICAL",
                            "type": "Invalid Timing",
                            "description": (
                                f"Timing-Event '{event_name}' in SWC "
                                f"'{swc_name}' has invalid period "
                                f"({period}s)."
                            )                        })
                    extra_info = f"Period: {period}s"

                elif event_type == "OPERATION-INVOKED-EVENT":
                    # Get referenced server operation name
                    xpath_op = ".//*[@DEST='CLIENT-SERVER-OPERATION']"
                    op_ref = event.xpath(xpath_op)
                    if op_ref:
                        extra_info = f"Operation Ref: {op_ref[0].text}"
                
                # TODO: Identify and integrate additional AUTOSAR event types 
                # requiring specialized architectural metadata extraction.
                
                internal_behavior["events"].append([event_type, event_name, event_ref, extra_info])
                events_references.append(event_ref)

        # 2. Process and validate AUTOSAR Runnable Entities
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
                    "description": (
                        f"Runnable '{runnable_name}' in SWC '{swc_name}' "
                        f"is not being actively triggered by any event."
                    )
                })                

        # 3. Extract AUTOSAR Per-Instance Memory (PIM) definitions
        pims_element = self.get_elements(swc_element,"AR-TYPED-PER-INSTANCE-MEMORYS",direct_only=False)
        if pims_element:
            all_pims = list(pims_element[0])
            for pim in all_pims:
                pim_name = self.get_element_text(pim, "SHORT-NAME")
                internal_behavior["pims"].append(pim_name)

        # 4. Extract AUTSOAR Shared Parameter definitions
        params_element = self.get_elements(swc_element,"SHARED-PARAMETERS",direct_only=False)
        if params_element:
            all_params = list(params_element[0])
            for param in all_params:
                param_name = self.get_element_text(param, "SHORT-NAME")
                internal_behavior["parameters"].append(param_name)        
        
        return internal_behavior, issues
    

    def export_to_markdown(self, all_swc_details: list, all_architecture_issues: list, filename: str) -> None:
        """Generates a comprehensive architecture and ISO 26262 safety report.

        Compiles all collected software component metadata and captured 
        architectural discrepancies into a standardized, human-readable 
        Markdown compliance document.

        Args:
            all_swc_details (List[Dict[str, Any]]): Extracted configuration 
                and behavior metadata from all processed atomic components.
            all_architecture_issues (List[Dict[str, str]]): List of collected 
                safety and integrity discrepancies found during analysis.
            filename (str): Target file system path where the report file 
                will be written.
        """
        # Ensure that destination directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            # 1. Headline and Introduction
            f.write("# AUTOSAR Architecture & ISO 26262 Safety Report\n\n")
            f.write("This document contains the static architectural analysis and the  ")
            f.write("compliance check in accordance with the requirements of **ISO 26262-6** ")
            f.write("completeness and consistency). \n\n")
            
            # 2. ISO 26262 Compliance Dashboard
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
                    f.write(
                        f"| {sev_emoji} {issue['severity']} | "
                        f"{issue['type']} | {issue['description']} |\n"
                    )
                f.write("\n")
            else:
                f.write(
                    "**Status:** ✅ Pass (No structural violations or "
                    "orphaned elements found).\n\n"
                )
            
            f.write("---\n\n")
            
            # 3. Software Component Details
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
                        f.write(
                            f"| {row['name']} | {row['trigger_type']} | "
                            f"{row['event_name']} | {row['extra_info']} |\n"
                        )
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