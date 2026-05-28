# Technical Reference

This reference manual provides a detailed technical specification of the ISO 26262 ARXML Parser API and Command-Line Interface (CLI). It serves as a strict technical lookup guide.

---

## 1. Command-Line Interface (CLI)

The tool is executed via the command line using standard Python arguments.

### 1.1 Syntax
```bash
python -m src.main <path_to_arxml>
```

### 1.2 Arguments

| Argument | Type | Required | Description | Fallback Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `<arxml_path>` | `str` | No | Path to the target AUTOSAR `.arxml` file. | Automatically loads the system default path: `tests/samples/Standard_Compliance_Sample.arxml`. |

---

## 2. Core API Reference (src/arxml_parser.py)

### 2.1 Class: ARXMLParser
The central class responsible for safely loading, navigating, filtering, and validating AUTOSAR ARXML structures.

#### 2.1.1 init
```python
def __init__(self, file_path: str)
```
Initializes the parser instance with the target file.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `file_path` | `str` | The physical path to the target ARXML file. |

#### 2.1.2 load
```python
def load(self) -> bool
```
Safely parses the XML structure into memory using `lxml`.

| Return Type | Description |
| :--- | :--- |
| `bool` | `True` if parsing and namespace registration succeeded. |

| Raised Exception | Trigger Condition |
| :--- | :--- |
| `ARXMLParserError` | If the XML structure is physically corrupt or cannot be parsed. |

#### 2.1.3 get_elements
```python
def get_elements(self, element: ET._Element, tag_name: str, direct_only: bool = True) -> List[ET._Element]
```
Finds all child elements matching a specific AUTOSAR XML tag.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `element` | `ET._Element` | *Required* | The starting XML node for the search. |
| `tag_name` | `str` | *Required* | Local name of the target XML tag (e.g., `'RUNNABLE-ENTITY'`). |
| `direct_only` | `bool` | `True` | `True`: search immediate children only (`./`). <br>`False`: search full subtree recursively (`.//`). |

| Return Type | Description |
| :--- | :--- |
| `List[ET._Element]` | A list of matching lxml elements (empty list if no elements match). |

#### 2.1.4 get_single_element
```python
def get_single_element(self, element: ET._Element, tag_name: str, direct_only: bool = True, default: Any = None) -> Any
```
Retrieves the first child element matching the local name.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `element` | `ET._Element` | *Required* | The starting XML node for the search. |
| `tag_name` | `str` | *Required* | Local name of the target XML tag (e.g., `'INTERNAL-BEHAVIORS'`). |
| `direct_only` | `bool` | `True` | `True`: search immediate children only (`./`). <br>`False`: search full subtree recursively (`.//`). |
| `default` | `Any` | `None` | Fallback value if the element does not exist. |

| Return Type | Description |
| :--- | :--- |
| `ET._Element \| Any` | The found XML element node, or the specified default value. |

#### 2.1.5 get_element_text
```python
def get_element_text(self, element: ET._Element, tag_name: str, direct_only: bool = True, default: Any = None) -> Optional[str]
```
Extracts the stripped text content of an ARXML element.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `element` | `ET._Element` | *Required* | The starting XML node. |
| `tag_name` | `str` | *Required* | Local name of the XML tag to read (e.g., `'SHORT-NAME'`). |
| `direct_only` | `bool` | `True` | `True`: check immediate level only. <br>`False`: check full subtree. |
| `default` | `Any` | `None` | Fallback value if the element contains no text. |

| Return Type | Description |
| :--- | :--- |
| `Optional[str]` | Stripped text value of the element, or the default value. |

#### 2.1.6 get_all_composition_swcs
```python
def get_all_composition_swcs(self) -> List[ET._Element]
```
Extracts all top-level Composition Software Components from the XML tree.

| Return Type | Description |
| :--- | :--- |
| `List[ET._Element]` | A list of matching `COMPOSITION-SW-COMPONENT-TYPE` elements. |

#### 2.1.7 get_composition_swc_ref
```python
def get_composition_swc_ref(self, composition: ET._Element) -> Dict[str, List[str]]
```
Maps internal prototype references for a specific composition component.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `composition` | `ET._Element` | A composition component XML node. |

| Return Type | Description |
| :--- | :--- |
| `Dict[str, List[str]]` | A dictionary mapping the component's short-name to its child references. |

#### 2.1.8 get_all_atomic_swcs
```python
def get_all_atomic_swcs(self) -> List[ET._Element]
```
Scans the structure for all standard AUTOSAR Atomic Software Component Types.

| Covers XML Tags |
| :--- |
| `APPLICATION-SW-COMPONENT-TYPE` <br> `COMPLEX-DEVICE-DRIVER-SW-COMPONENT-TYPE` <br> `SERVICE-SW-COMPONENT-TYPE` |

| Return Type | Description |
| :--- | :--- |
| `List[ET._Element]` | A merged list of all atomic component nodes found in the XML tree. |

#### 2.1.9 get_swc_internal_behavior
```python
def get_swc_internal_behavior(self, swc_element: ET._Element) -> Tuple[Dict[str, Any], List[Dict[str, str]]]
```
Parses internal definitions and runs structural safety checks for ISO 26262 / ASIL-B compliance.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `swc_element` | `ET._Element` | The atomic software component node to evaluate. |

| Return Type | Description |
| :--- | :--- |
| `Tuple[Dict[str, Any], List[Dict[str, str]]]` | A compound tuple containing:<br>1. A dictionary of processed architecture metadata (runnables, events, parameters).<br>2. A list of structural safety issue dictionaries (each containing `severity`, `type`, and `description`). |

#### 2.1.10 export_to_markdown
```python
def export_to_markdown(self, all_swc_details: List[Dict[str, Any]], all_architecture_issues: List[Dict[str, str]], filename: str) -> None
```
Compiles all gathered component data and validation issues into a human-readable Markdown report.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `all_swc_details` | `List[Dict[str, Any]]` | Extracted metadata from all components. |
| `all_architecture_issues` | `List[Dict[str, str]]` | List of collected ISO 26262 violation dictionaries. |
| `filename` | `str` | Targeted path for the output `.md` file. |

---

## 3. Application Entry Point (src/main.py)

### 3.1 process_arxml_architecture
```python
def process_arxml_architecture(arxml_file: str, arxml_report_file: str) -> None
```
Orchestrates the operational loop: triggers the loading sequence, starts validation rules against ISO 26262 requirements, and hands over data to the Markdown export layer.

### 3.2 resolve_paths
```python
def resolve_paths() -> Tuple[str, str]
```
Evaluates CLI inputs (`sys.argv`), checks physical file existence, handles dynamic fallbacks for missing arguments, and calculates path definitions.

| Return Type | Description |
| :--- | :--- |
| `Tuple[str, str]` | Validated input ARXML path and target output report path. |

| Raised Exception | Trigger Condition |
| :--- | :--- |
| `ARXMLFileNotFoundError` | If no valid input file can be resolved in the default directories. |

---

## 4. Error & Exception Catalog (src/exceptions.py)

The tool utilizes a strict exception hierarchy to ensure safe automation inside execution chains (e.g., CI/CD pipelines).

| Exception Class | Parent Class | Trigger Condition |
| :--- | :--- | :--- |
| `ARXMLToolError` | `Exception` | Global catch-all base class for tool runtime issues. |
| `ARXMLParserError` | `ARXMLToolError` | Raised when `lxml` fails to read or parse corrupted XML files. |
| `ARXMLValidationError` | `ARXMLToolError` | Raised if structural boundaries or AUTOSAR safety schemas are breached. |
| `ARXMLFileNotFoundError`| `ARXMLValidationError`| Raised instantly if the provided input file path does not exist. |