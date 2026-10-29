import os
from pathlib import Path

import pytest

from src.arxml_parser import ARXMLParser

# =====================================================================
# PYTEST FIXTURE (Generates the minimal XML test data)
# =====================================================================

@pytest.fixture
def parser_env(tmp_path: Path) -> dict[str, str]:
    """Create temporary ARXML content for testing the parser."""
    # 1. Valid AUTOSAR document containing components, events, and runnables
    valid_content = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<AUTOSAR xmlns="http://autosar.org">\n'
        '  <AR-PACKAGES>\n'
        '    <COMPOSITION-SW-COMPONENT-TYPE>\n'
        '      <SHORT-NAME>Main_Composition</SHORT-NAME>\n'
        '      <SW-COMPONENT-PROTOTYPE>\n'
        '        <SHORT-NAME>EngineCtrl_Prototype</SHORT-NAME>\n'
        '        <TYPE-TREF>/Components/EngineCtrl</TYPE-TREF>\n'
        '      </SW-COMPONENT-PROTOTYPE>\n'
        '    </COMPOSITION-SW-COMPONENT-TYPE>\n'
        '    <APPLICATION-SW-COMPONENT-TYPE>\n'
        '      <SHORT-NAME>EngineCtrl</SHORT-NAME>\n'
        '      <EVENTS>\n'
        '        <TIMING-EVENT>\n'
        '          <SHORT-NAME>T_10ms_Event</SHORT-NAME>\n'
        '          <START-ON-EVENT-REF>/Components/EngineCtrl/Run_Engine_10ms</START-ON-EVENT-REF>\n'
        '          <PERIOD>0.01</PERIOD>\n'
        '        </TIMING-EVENT>\n'
        '        <TIMING-EVENT>\n'
        '          <SHORT-NAME>Orphaned_Event</SHORT-NAME>\n'
        '          <PERIOD>0.02</PERIOD>\n' # Missing START-ON-EVENT-REF -> ISO error!
        '        </TIMING-EVENT>\n'
        '      </EVENTS>\n'
        '      <RUNNABLE-ENTITY>\n'
        '        <SHORT-NAME>Run_Engine_10ms</SHORT-NAME>\n'
        '      </RUNNABLE-ENTITY>\n'
        '      <RUNNABLE-ENTITY>\n'
        '        <SHORT-NAME>Passive_Runnable</SHORT-NAME>\n' # No event -> ISO warning!
        '      </RUNNABLE-ENTITY>\n'
        '    </APPLICATION-SW-COMPONENT-TYPE>\n'
        '  </AR-PACKAGES>\n'
        '</AUTOSAR>'
    )
    
    # 2. Corrupt XML that is not valid AUTOSAR
    invalid_content = '<NOT-AUTOSAR><SHORT-NAME>Fake</SHORT-NAME></NOT-AUTOSAR>'

    valid_file = tmp_path / "valid_test.arxml"
    valid_file.write_text(valid_content, encoding="utf-8")

    invalid_file = tmp_path / "invalid_test.arxml"
    invalid_file.write_text(invalid_content, encoding="utf-8")

    return {
        "valid_path": str(valid_file),
        "invalid_path": str(invalid_file)
    }

# =====================================================================
# PARSER UNIT TESTS
# =====================================================================

def test_parser_load_success(parser_env):
    """Check if valid ARXML file is loaded without errors."""
    parser = ARXMLParser(parser_env["valid_path"])
    assert parser.load() is True
    assert parser.root is not None
    assert parser.root.tag.endswith("AUTOSAR")


def test_parser_load_invalid_autosar_structure(parser_env) -> None:
    """Check if parser terminates if the XML does not have an <AUTOSAR> root tag."""
    parser = ARXMLParser(parser_env["invalid_path"])
    assert parser.load() is False


def test_get_all_composition_swcs(parser_env) -> None:
    """Check if composition components are extracted correctly."""
    parser = ARXMLParser(parser_env["valid_path"])
    parser.load()
    
    compositions = parser.get_all_composition_swcs()
    assert len(compositions) == 1
    assert parser.get_element_text(compositions[0], "SHORT-NAME") == "Main_Composition"


def test_get_composition_swc_ref(parser_env) -> None:
    """Check if prototype references are resolved correctly within a composition."""
    parser = ARXMLParser(parser_env["valid_path"])
    parser.load()
    
    comp = parser.get_all_composition_swcs()[0]
    ref_data = parser.get_composition_swc_ref(comp)
    
    assert "EngineCtrl_Prototype" in ref_data["swc_names"]
    assert "/Components/EngineCtrl" in ref_data["swc_refs"]


def test_get_all_atomic_swcs(parser_env) -> None:
    """Check if atomic components are are extracted correctly."""
    parser = ARXMLParser(parser_env["valid_path"])
    parser.load()
    
    atomic_swcs = parser.get_all_atomic_swcs()
    assert len(atomic_swcs) == 1
    assert parser.get_element_text(atomic_swcs[0], "SHORT-NAME") == "EngineCtrl"


def test_iso26262_internal_behavior_validation(parser_env) -> None:
    """Check if parser detects orphaned events and untriggered runnables."""
    parser = ARXMLParser(parser_env["valid_path"])
    parser.load()
    
    swc = parser.get_all_atomic_swcs()[0]
    internal_behavior, issues = parser.get_swc_internal_behavior(swc)
    
    # 1. Check data integrity
    # The active Runnable ‘Run_Engine_10ms’ must be mapped correctly
    active_runnable = next(r for r in internal_behavior["runnables"] if r["name"] == "Run_Engine_10ms")
    assert active_runnable["trigger_type"] == "TIMING-EVENT"
    assert active_runnable["event_name"] == "T_10ms_Event"
    assert active_runnable["extra_info"] == "Period: 0.01s"

    # 2. Check for ISO 26262 compliance errors
    # Exactly two issues must have been found (1 error due to an orphaned event, 1 warning due to a passive runnable)
    assert len(issues) == 2
    
    severities = [i["severity"] for i in issues]
    types = [i["type"] for i in issues]
    
    assert "ERROR" in severities
    assert "WARNING" in severities
    assert "Orphaned Event" in types
    assert "Untriggered Runnable" in types


def test_export_to_markdown_generation(parser_env, tmp_path) -> None:
    """Check if Markdown report is generated."""
    parser = ARXMLParser(parser_env["valid_path"])
    parser.load()
    
    swc = parser.get_all_atomic_swcs()[0]
    details, issues = parser.get_swc_internal_behavior(swc)
    
    swc_data = [{"name": "EngineCtrl", "details": details}]
    output_report = tmp_path / "reports" / "compliance_report.md"
    
    # Trigger export
    parser.export_to_markdown(swc_data, issues, str(output_report))
    
    # Test: Does file physically exists and contains data?
    assert os.path.exists(output_report)
    with open(output_report, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# AUTOSAR Architecture & ISO 26262 Safety Report" in content
        assert "EngineCtrl" in content


@pytest.mark.parametrize(
    "period_xml",
    [
        "<PERIOD>abc</PERIOD>",
        "<PERIOD>0</PERIOD>",
        "<PERIOD>-0.01</PERIOD>",
        "<PERIOD>nan</PERIOD>",
        "<PERIOD>inf</PERIOD>",
        "<PERIOD></PERIOD>",
        "",
    ],
    ids=["non-numeric", "zero", "negative", "nan", "inf", "empty", "missing"],
)
def test_invalid_timing_period_is_reported(parser_env, tmp_path, period_xml) -> None:
    """Check if an invalid PERIOD is reported as CRITICAL instead of crashing."""
    # Reuse the valid fixture file and replace the period of 'T_10ms_Event'
    content = Path(parser_env["valid_path"]).read_text(encoding="utf-8")
    content = content.replace("<PERIOD>0.01</PERIOD>", period_xml, 1)
    test_file = tmp_path / "invalid_period_test.arxml"
    test_file.write_text(content, encoding="utf-8")

    parser = ARXMLParser(str(test_file))
    assert parser.load() is True

    swc = parser.get_all_atomic_swcs()[0]
    _, issues = parser.get_swc_internal_behavior(swc)

    timing_issues = [i for i in issues if i["type"] == "Invalid Timing"]
    assert len(timing_issues) == 1
    assert timing_issues[0]["severity"] == "CRITICAL"
    assert "T_10ms_Event" in timing_issues[0]["description"]
