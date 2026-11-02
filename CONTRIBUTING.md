# Contributing

## Code Contributions: Verify Code Quality and Test Coverage

Code contributions are welcome. Before pushing code changes, ensure that the automated test suite runs through without errors and check the verification report for the ARXML parser.

### Prerequisites

Ensure you have installed the testing dependencies listed in the requirements file:

```bash
pip install -r requirements.txt
```

### Step 1: Run the full test suite

To execute all unit tests and verify the structural integrity of the parser components, run `pytest` from the root directory of the project:

```bash
pytest
```

You should see an output indicating that all test cases passed successfully.

### Step 2: Generate the test coverage report

To measure exactly which lines of code are covered by the test suite, use the `pytest-cov` plugin. Execute the following command to run the tests and calculate the coverage for the source files:

```bash
pytest --cov=src tests/
```

This will print a summary table directly in your terminal, displaying the coverage metrics for individual modules.

### Step 3: Export the detailed HTML coverage report

For a deep-dive visual analysis of the testing boundaries—showing exactly which code paths are verified—you can generate an interactive HTML report:

```bash
pytest --cov=src --cov-report=html tests/
```

#### Accessing the report:
1. Locate the newly created `htmlcov/` directory in your project root.
2. Open the `index.html` file inside any standard web browser.
3. Click on individual files (such as `arxml_parser.py`) to review the line-by-line execution analysis.