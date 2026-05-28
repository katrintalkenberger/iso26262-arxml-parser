# How-To Guides

This document provides practical, recipe-style instructions for advanced operations, including executing quality assurance suites and performing manual fault-injection testing.

---

## Table of Contents
* [How to Run Code Quality and Test Coverage Reports](#how-to-run-code-quality-and-test-coverage-reports)
* [How to Test Custom ISO 26262 Violations](#how-to-test-custom-iso-26262-violations)

---

## How-To Guide: Verify Code Quality and Test Coverage

This guide provides step-by-step instructions on how to execute the automated test suite and analyze the verification coverage reports for the ARXML Parser.

### Prerequisites

Ensure you have installed the testing dependencies listed in the requirements file:

```bash
pip install -r requirements.txt
```

### Step 1: Run the Full Test Suite

To execute all unit tests and verify the structural integrity of the parser components, run `pytest` from the root directory of the project:

```bash
pytest
```

You should see an output indicating that all test cases passed successfully.

### Step 2: Generate the Test Coverage Report

To measure exactly which lines of code are covered by the test suite, use the `pytest-cov` plugin. Execute the following command to run the tests and calculate the coverage for the source files:

```bash
pytest --cov=src tests/
```

This will print a summary table directly in your terminal, displaying the coverage metrics for individual modules.

### Step 3: Export the Detailed HTML Coverage Report

For a deep-dive visual analysis of the testing boundaries—showing exactly which code paths are verified—you can generate an interactive HTML report:

```bash
pytest --cov=src --cov-report=html tests/
```

#### Accessing the Report:
1. Locate the newly created `htmlcov/` directory in your project root.
2. Open the `index.html` file inside any standard web browser.
3. Click on individual files (such as `arxml_parser.py`) to review the line-by-line execution analysis.

### Technical Verification Metrics
* src/main.py: 100% Coverage
* src/arxml_parser.py: 85% Coverage

---

## How to Test Custom ISO 26262 Violations

This guide explains how to inject faults into an ARXML file to test the parser's validation rules, and where to source advanced industry examples.

### Sourcing Industry ARXML Examples
If you want to test the parser with large-scale, third-party AUTOSAR files, you can use open-source repository extracts such as:
* [tests/samples/EcuExtract.arxml](tests/samples/EcuExtract.arxml) from the [patrikja autosar](https://github.com/patrikja/autosar) repository (BSD 3-Clause License).
* [tests/samples/TestApp.arxml](tests/samples/TestApp.arxml) from the [mahmut-aksakalli arxml-viewer](https://github.com/mahmut-aksakalli/arxml-viewer) repository (MIT License).

### Injecting Structural Faults for Validation Testing

You can manually manipulate any standard ARXML structure using a text editor to test the three functional safety check layers.

#### Option 1. Simulating an Orphaned Event (ASIL-B Violation)
Locate any event structure and completely delete or comment out the `<START-ON-EVENT-REF>` child tag:
```xml
<!-- Non-Compliant Modification -->
<TIMING-EVENT>
  <SHORT-NAME>Timer_Event</SHORT-NAME>
  <!-- Missing reference triggers an ERROR in the report -->
</TIMING-EVENT>
```

#### Option 2. Simulating an Invalid Timing Period (Determinism Failure)
Locate a `<TIMING-EVENT>` that contains a `<PERIOD>` tag. Change the value to `0.0` or a negative number:
```xml
<!-- Non-Compliant Modification -->
<TIMING-EVENT>
  <SHORT-NAME>Timer_Event</SHORT-NAME>
  <START-ON-EVENT-REF DEST="RUNNABLE-ENTITY">/Path/To/Runnable</START-ON-EVENT-REF>
  <PERIOD>0.0</PERIOD> <!-- Zero-value triggers a CRITICAL fault -->
</TIMING-EVENT>
```

#### Option 3. Simulating an Untriggered Runnable (Passive Code)
Add a new `<RUNNABLE-ENTITY>` inside the `<RUNNABLE-ENTITIES>` container, but do not create any corresponding event that references this runnable's short-name. The compliance engine will catch this as an unmapped, passive entity and issue a `WARNING`.

---

## Next Steps
* To understand the technical parameters and return types of specific methods, see the [API Reference](reference.md).
* To explore the architectural background of the AUTOSAR schema, check out the [Explanations](explanations/explanation-for-specialists.md).