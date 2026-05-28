import pytest
import os
import runpy
import sys
from typing import Dict
from unittest.mock import patch, MagicMock
from src import main
from src.exceptions import ARXMLFileNotFoundError

# =====================================================================
# PYTEST FIXTURES (Gemeinsames Setup für alle Tests)
# =====================================================================

@pytest.fixture
def setup_repo_structure(tmp_path) -> Dict[str, str]:
    """Creates a virtual repository structure in the temporary folder."""
    # Create the folder structure for the default ARXML file starting from the temp_path
    fake_default_dir = tmp_path / "tests" / "samples"
    fake_default_dir.mkdir(parents=True, exist_ok=True)
    fake_default = fake_default_dir / "SampleFile.arxml"
    fake_default.write_text("<AUTOSAR></AUTOSAR>")

     # Create the folder structure for the output report starting from the temp_path
    examples_dir = tmp_path / "examples"
    examples_dir.mkdir(exist_ok=True)

    # Set the folder path of main.py
    simulated_main_path = str(tmp_path / "src" / "main.py")

    # Wir geben die Pfade als Dictionary an die Tests weiter
    return {
        "fake_default": str(fake_default),
        "examples_dir": str(examples_dir),
        "simulated_main_path": simulated_main_path,
        "tmp_path": str(tmp_path)
    }

# =====================================================================
# TESTS FOR THE CLI ARGUMENTS (resolve_paths)
# =====================================================================

def test_resolve_paths_missing_arguments(capsys, setup_repo_structure):
    """Prüft, ob bei komplett fehlenden Argumenten auf die Default-Datei gewechselt wird."""
    env = setup_repo_structure

    # Wir simulieren: Nur der Skriptname ist in sys.argv (keine Zusatzargumente)
    with patch('os.path.abspath', return_value=env["simulated_main_path"]), \
         patch.object(sys, 'argv', ['main.py']), \
         patch('os.getcwd', return_value=env["tmp_path"]):
        
        input_file, _ = main.resolve_paths()
        
        # Test 1: Correct setup of the default path?
        assert input_file == env["fake_default"]
        
        # Test 2: Correct warning issued?
        captured = capsys.readouterr()
        assert "INFO: Missing input argument. Switching to default sample file." in captured.out


def test_resolve_paths_too_many_arguments(capsys, setup_repo_structure):
    """Check if default ARXML file is used if there are too many input arguments."""
    env = setup_repo_structure

    # Mock the base and current directory, and overwrite the input arguments
    with patch('os.path.abspath', return_value=env["simulated_main_path"]), \
         patch.object(sys, 'argv', ['main.py', 'datei1.arxml', 'datei2.arxml']), \
         patch('os.getcwd', return_value=env["tmp_path"]):
        
        input_file, output_report = main.resolve_paths()
        
        # Test 1: Correct setup of the default path?
        assert input_file == env["fake_default"]
        assert "arxml_report_SampleFile.md" in output_report
        
        # Test 2: Correct warning issued?
        captured = capsys.readouterr()
        assert "WARNING: Too many arguments. Switching to default sample file." in captured.out

def test_resolve_paths_invalid_extension(capsys, setup_repo_structure):
    """Check if default ARXML file is used if input file format is invalid."""
    env = setup_repo_structure

    with patch('os.path.abspath', return_value=env["simulated_main_path"]), \
         patch.object(sys, 'argv', ['main.py', 'wrong_file.txt']), \
         patch('os.getcwd', return_value=env["tmp_path"]):
        
        input_file, _ = main.resolve_paths()
        
        # Test 1: Correct setup of the default path?
        assert input_file == env["fake_default"]
        
        # Test 2: Correct warning issued?
        captured = capsys.readouterr()
        assert "WARNING: Invalid file extension. Switching to default sample file." in captured.out


def test_resolve_paths_file_not_found():
    """Check if custom exception is thrown if file is missing."""
    with patch.object(sys, 'argv', ['main.py', 'non-exsisting-file.arxml']), \
         patch('os.path.exists', return_value=False):
        
        # Test: Correct warning issued?
        with pytest.raises(ARXMLFileNotFoundError, match="File not found: non-exsisting-file.arxml"):
            main.resolve_paths()


def test_resolve_paths_happy_path(setup_repo_structure):
    """Check if valid input argument is handled correctly."""
    env = setup_repo_structure
    
    # Create valid input argument in the tmp_path directory
    valid_file = os.path.join(env["tmp_path"], "valid_input.arxml")
    with open(valid_file, "w") as f:
        f.write("<AUTOSAR></AUTOSAR>")
    
    with patch.object(sys, 'argv', ['main.py', valid_file]), \
         patch('os.getcwd', return_value=env["tmp_path"]):
        
        input_file, output_report = main.resolve_paths()
        
        # Test 1: Correct setup of the default path?
        assert input_file == valid_file

        # Test 2: Report created?
        assert "arxml_report_valid_input.md" in output_report


def test_resolve_paths_removes_existing_report(setup_repo_structure):
    """Check if existing report file is removed correctly."""
    env = setup_repo_structure
    
    # Use the temporary examples directory from Fixture to create a report file
    existing_report = os.path.join(env["examples_dir"], "arxml_report_SampleFile.md")

    # Write report file
    with open(existing_report, "w") as f:
        f.write("# Old Protocol")
        
    # Test 1: 
    assert os.path.exists(existing_report)

    # Call main.py with default fallback (no input argument)
    with patch('os.path.abspath', return_value=env["simulated_main_path"]), \
         patch.object(sys, 'argv', ['main.py']), \
         patch('os.getcwd', return_value=env["tmp_path"]), \
         patch('os.remove') as mock_remove:
        
        _, output_report = main.resolve_paths()
        
        # Test 2: Report path correct?
        assert output_report == existing_report

        # Test 3: Is os.remove() called with existing report?
        mock_remove.assert_called_once_with(existing_report)


def test_process_arxml_architecture_failed_load(capsys):
    """Check if function terminates correctly if the ARXML fails to load."""
    with patch('src.main.ARXMLParser') as mock_parser_class:
        mock_instance = MagicMock()
        mock_instance.load.return_value = False
        mock_parser_class.return_value = mock_instance
        
        main.process_arxml_architecture("dummy.arxml", "report.md")
        
        # Test 1: Correct error issued?
        captured = capsys.readouterr()
        assert "ERROR: Failed to load or parse the ARXML file." in captured.out
        
        # Test 2: No further calls after?
        mock_instance.get_all_composition_swcs.assert_not_called()


def test_process_arxml_architecture_happy_path(capsys):
    """Check that the main function runs completely and successfully."""
    with patch('src.main.ARXMLParser') as mock_parser_class:
        mock_instance = MagicMock()
        mock_instance.load.return_value = True
        mock_instance.get_all_composition_swcs.return_value = ["Mock_Comp_Element"]
        mock_instance.get_element_text.return_value = "TopLevel_Composition"
        mock_instance.get_all_atomic_swcs.return_value = ["Mock_Atomic_Element"]
        fake_details = {"type": "ApplicationSWC", "runnables": "RUNNABLE1"}
        fake_issues = [{"issue": "Runnable RUNNABLE1 is not triggered by an event."}]
        mock_instance.get_swc_internal_behavior.return_value = (fake_details, fake_issues)
        mock_parser_class.return_value = mock_instance
        
        main.process_arxml_architecture("dummy.arxml", "report.md")
        
        # Test 1: Was the data collected and exported correctly?
        mock_instance.export_to_markdown.assert_called_once_with(
            [{"name": "TopLevel_Composition", "details": fake_details}],
            fake_issues,
            "report.md"
        )
        
        # Test 2: Terminal output correct?
        captured = capsys.readouterr()
        assert "Found 1 Composition Software Components:" in captured.out
        assert "Processing 1 Atomic Software Components..." in captured.out
        assert "Analysis complete. Report generated at: report.md" in captured.out