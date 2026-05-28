"""Execution entry point and CLI orchestration for the ISO 26262 ARXML Verifier.

This module resolves file paths from command-line arguments, triggers the 
core AUTOSAR parsing sequence, and coordinates the functional safety 
validation and reporting pipeline.
"""

import sys
import os
from typing import List, Dict, Any, Tuple
from src.arxml_parser import ARXMLParser
from src.exceptions import ARXMLToolError, ARXMLFileNotFoundError

def process_arxml_architecture(arxml_file: str, arxml_report_file: str) -> None:
    """Executes the full parsing, validation, and reporting pipeline for an ARXML file.

    This function orchestrates the lifecycle of the verification process: it
    initializes the parser, extracts software component compositions, validates
    atomic components against structural ISO 26262 requirements, and generates
    the final evaluation report in Markdown format.

    Args:
        arxml_file (str): The physical file system path to the input AUTOSAR
            ARXML configuration file.
        arxml_report_file (str): The target file system path where the validated
            Markdown report will be written.

    Returns:
        None

    Note:
        Future iterations are planned to support automatic visual architecture
        exports via Mermaid.js diagrams directly embedded inside the report.
    """
    parser = ARXMLParser(arxml_file)

    if not parser.load():
        print("ERROR: Failed to load or parse the ARXML file.")
        return

    # 1. Process Composition Software Components
    all_compositions = parser.get_all_composition_swcs()
    print(f"Found {len(all_compositions)} Composition Software Components:")
    for composition in all_compositions:
        name = parser.get_element_text(composition,"SHORT-NAME")
        print(name)

    # 2. Process Atomic Software Components and evaluate ISO 26262 compliance
    atomic_swcs = parser.get_all_atomic_swcs()
    all_swc_details: List[Dict[str, Any]] = []
    all_architecture_issues: List[Dict[str, str]] = []

    print(f"\nProcessing {len(atomic_swcs)} Atomic Software Components...")
    for swc in atomic_swcs:
        swc_name = parser.get_element_text(swc, "SHORT-NAME", default="Unknown_SWC")
        
        # Extract internal behavior and perform structural safety checks
        details, issues = parser.get_swc_internal_behavior(swc)
               
        # Compile metadata for reporting
        swc_data = {
            "name": swc_name,
            "details": details
        }
        all_swc_details.append(swc_data)
        all_architecture_issues.extend(issues)

    # 3. Generate human-readable architectural compliance report
    parser.export_to_markdown(all_swc_details, all_architecture_issues, arxml_report_file)
    print(f"\nAnalysis complete. Report generated at: {arxml_report_file}")


def resolve_paths() -> Tuple[str, str]:
    """Validates CLI inputs, applies fallbacks, and derives output targets.

    Evaluates the command-line arguments provided via sys.argv. If valid,
    the specified ARXML path is extracted. If arguments are missing,
    malformed, or invalid, the system automatically falls back to a 
    predefined test sample file.

    Returns:
        Tuple[str, str]: A tuple containing two strings:
            - The absolute validated path to the input ARXML file.
            - The calculated target path for the Markdown report.

    Raises:
        ARXMLFileNotFoundError: If the resolved input ARXML file does not
            exist on the physical file system.
    """
    arxml_file = ""

    print(f"----- Länge der Input Parameter: {len(sys.argv)}")

    # Check CLI argument(s)
    if len(sys.argv) < 2:
        print("INFO: Missing input argument. Switching to default sample file.") 
    elif len(sys.argv) > 2:
        print("WARNING: Too many arguments. Switching to default sample file.")      
    else:
        if not sys.argv[1].endswith('.arxml'):            
            print("WARNING: Invalid file extension. Switching to default sample file.")
        else:
            arxml_file = sys.argv[1]
    
    # Fallback to default ARXML file if input argument is missing or invalid
    if not arxml_file:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_path = os.path.join(base_dir, 'tests', 'samples')
        default_file = "Standard_Compliance_Sample.arxml"
        arxml_file =  os.path.join(default_path, default_file)
        print(f"Use default ARXML sample file: {arxml_file}")   

    # Check existence of ARXML file
    if not os.path.exists(arxml_file):
        raise ARXMLFileNotFoundError(f"File not found: {arxml_file}")

    # Set ARXML report file path
    arxml_file_name = os.path.splitext(os.path.basename(arxml_file))[0]
    arxml_report_path = os.path.join(os.getcwd(), 'examples')
    arxml_report_file = os.path.join(arxml_report_path, f"arxml_report_{arxml_file_name}.md")

    # Remove old report file to ensure a clean evaluation state
    if os.path.exists(arxml_report_file):
        os.remove(arxml_report_file)

    return arxml_file, arxml_report_file


if __name__ == "__main__":
    try:
        # Resolve path configurations using CLI arguments or dynamic fallbacks
        input_file, output_report = resolve_paths()

        # Execute the main parsing, validation, and export chain
        process_arxml_architecture(input_file, output_report)

    except ARXMLToolError as e:
        # Standardize error output to stderr for seamless CI/CD pipeline integration
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)