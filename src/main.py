import sys
import os
from typing import List, Dict, Any, Tuple
from arxml_parser import ARXMLParser

def process_arxml_architecture(arxml_file: str, arxml_report_file: str) -> None:
    """Core logic for parsing the ARXML structure, validation according to ISO 26262, 
    and control of the Markdown export.
    """
    parser = ARXMLParser(arxml_file)

    if not parser.load():
        print("ERROR: Failed to load or parse the ARXML file.")
        return

    # 1. COMPOSITION SOFTWARE COMPONENTS
    all_compositions = parser.get_all_composition_swcs()
    print(f"Found {len(all_compositions)} Composition Software Components:")
    for composition in all_compositions:
        name = parser.get_element_text(composition,"SHORT-NAME")
        # TODO: Visual Architecture Export: Mermaid.js diagrams directly within the 
        # Markdown report to visualize Composition-to-SWC mapping.
        #composition_swcs = parser.get_composition_swc_ref(composition)
        print(name)

    # 2. ATOMIC SOFTWARE COMPONENTS
    atomic_swcs = parser.get_all_atomic_swcs()
    all_swc_details: List[Dict[str, Any]] = []
    all_architecture_issues: List[Dict[str, str]] = []

    print(f"\nProcessing {len(atomic_swcs)} Atomic Software Components...")
    for swc in atomic_swcs:
        swc_name = parser.get_element_text(swc, "SHORT-NAME", default="Unknown_SWC")
        
        # Get architecture details and perform ISO 26262 check
        details, issues = parser.get_swc_internal_behavior(swc)
               
        # Collect information
        swc_data = {
            "name": swc_name,
            "details": details
        }
        all_swc_details.append(swc_data)
        all_architecture_issues.extend(issues)

    # 3. GENERATE REPORT (SWC details and ISO 26262 validation)
    parser.export_to_markdown(all_swc_details, all_architecture_issues, arxml_report_file)
    print(f"\nAnalysis complete. Report generated at: {arxml_report_file}")


def resolve_paths() -> Tuple[str, str]:
    """Validate CLI argument(s), set fallbacks and generate report path."""
    arxml_file = ""

    # Check CLI argument(s)
    if len(sys.argv) < 2:
        print("Missing input argument") 
    elif len(sys.argv) > 2:
        print("Invalid number of input arguments")        
    else:
        if not sys.argv[1].endswith('.arxml'):            
            print("Invalid file extension.")  
        else:
            arxml_file = sys.argv[1]
    
    # Fallback to default ARXML file if input argument is missing
    if not arxml_file:
        default_path = os.path.join(os.getcwd(), 'tests','samples')
        default_file = "SampleFile.arxml"
        arxml_file =  os.path.join(default_path, default_file)
        print(f"Use default ARXML sample file: {arxml_file}")   

    # Check existence of ARXML file
    if not os.path.exists(arxml_file):
        print("ERROR: File not found: "+arxml_file)
        sys.exit(1)


    # Set ARXML report file path
    arxml_file_name = os.path.splitext(os.path.basename(arxml_file))[0]
    arxml_report_path = os.path.join(os.getcwd(), 'examples')
    arxml_report_file = os.path.join(arxml_report_path, f"arxml_report_{arxml_file_name}.md")

    # Remove old report file
    if os.path.exists(arxml_report_file):
        os.remove(arxml_report_file)

    return arxml_file, arxml_report_file


if __name__ == "__main__":
    input_file, output_report = resolve_paths()
    process_arxml_architecture(input_file, output_report)