# Getting started: Run ARXML parser

This tutorial guides you through setting up the ARXML Parser and running your first architectural analysis. You will clone the repository, install the required dependencies, and convert a sample AUTOSAR ARXML file into a human-readable Markdown documentation.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
* Python 3.11 or higher
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

## Step 3: Run the parser on a consistent file

The `tests/samples` directory contains a file without findings. Run the following command from the repository root directory:

```bash
python -m src.main tests/samples/Standard_Compliance_Sample.arxml
```

### Expected Output
The system logs the discovery of the software components. The generated report is saved to:
`examples/arxml_report_Standard_Compliance_Sample.md`

Open this file. The section "Consistency Check Results" shows the status "✅ Pass (No findings detected).".

## Step 4: Run the parser on a file with findings

Run the parser against the sample file that contains configuration faults:

```bash
python -m src.main tests/samples/ISO26262_Violations_Sample.arxml
```

### Expected Output
The system detects structural deficiencies and logs them. Open the newly generated report at:
`examples/arxml_report_ISO26262_Violations_Sample.md`

The section "Consistency Check Results" lists one finding per severity: an invalid timing period (CRITICAL), an orphaned event (ERROR) and an untriggered runnable (WARNING). The [check catalog](../reference/checks.md) explains each finding.

---

## Next Steps
* To learn how to modify an ARXML file to trigger each check, see [Inject architecture faults](../how-to/inject-architecture-faults.md).
* For the API and CLI specification, see the [API](../reference/api.md) and [CLI](../reference/cli.md) reference.
* For the conditions and severity of each check, see the [check catalog](../reference/checks.md).
* To understand the structure of AUTOSAR XML files, see [AUTOSAR ARXML structure](../explanation/autosar-arxml-structure.md).