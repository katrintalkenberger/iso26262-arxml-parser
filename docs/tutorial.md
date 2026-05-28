# Getting started: Run ARXML parser

This tutorial guides you through setting up the ARXML Parser and running your first architectural analysis. You will clone the repository, install the required dependencies, and convert a sample AUTOSAR ARXML file into a human-readable Markdown documentation.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
* Python 3.8 or higher
* Git

## Step 1: Clone the Repository

Open your terminal and run the following commands to clone the project and navigate into the root directory:

```bash
git clone https://github.com/katrintalkenberger/iso26262-arxml-parser
cd iso26262-arxml-parser
```

## Step 2: Install Dependencies

Install the required Python packages using `pip`. It is recommended to use a virtual environment, but for this quick start, you can install them directly:

```bash
pip install -r requirements.txt
```

## Step 3: Run the Compliant Architecture Verification

The repository contains a fully compliant software architecture file inside the `tests/samples` directory. Run the following command from the repository root directory:

```bash
python -m src.main tests/samples/Standard_Compliance_Sample.arxml
```

### Expected Output
The system logs the discovery of the software components. The generated report is saved to:
`examples/arxml_report_Standard_Compliance_Sample.md`

Open this file to verify that the ISO 26262 Architectural Integrity Check section displays a Pass status with zero criticals, errors, or warnings.


## Step 4: Run the Non-Compliant Architecture Verification

To observe how the compliance engine captures functional safety violations, run the parser against the non-compliant sample file:

```bash
python -m src.main tests/samples/ISO26262_Violations_Sample.arxml
```

### Expected Output
The system detects structural deficiencies and logs them. Open the newly generated report at:
`examples/arxml_report_ISO26262_Violations_Sample.md`

The compliance dashboard will display an architectural violation status, highlighting the captured critical timing faults, orphaned events, and untriggered runnables.

---

## Next Steps
* To learn how to verify code quality and generate test coverage reports, see the [How-To Guide](how-to-guide.md).
* For a detailed technical breakdown of all parser functions, look at the [API Reference](reference.md).
* To understand the underlying AUTOSAR concepts and safety architecture, explore the [Explanations](explanations/explanation-for-specialists.md).