# Command-Line Interface (CLI)

This reference manual provides a detailed technical specification of the ARXML parser Command-Line Interface (CLI).

---

The tool is executed via the command line using standard Python arguments.

## Syntax
```bash
python -m src.main <path_to_arxml>
```

## Arguments

| Argument | Type | Required | Description | Fallback Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `<arxml_path>` | `str` | No | Path to the target AUTOSAR `.arxml` file. | Automatically loads the system default path: `tests/samples/Standard_Compliance_Sample.arxml`. |
