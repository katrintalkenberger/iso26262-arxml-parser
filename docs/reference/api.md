# API

Classes, functions and exceptions of the ARXML parser. For the command-line usage, see [CLI](cli.md).

---

## 1. `src/arxml_parser.py`

### 1.1 Class `ARXMLParser`

Loads an ARXML file, provides helper methods to query the XML tree, and runs the consistency checks for atomic software components.

#### 1.1.1 `__init__`

```python
def __init__(self, file_path: str)
```

Stores the file path. The file is not read until `load()` is called.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `file_path` | `str` | Path to the ARXML file. |

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `file_path` | `str` | Path passed to the constructor. |
| `tree` | `ET._ElementTree \| None` | Parsed document. `None` before `load()`. |
| `root` | `ET._Element \| None` | Root element. `None` before `load()`. |
| `ns` | `dict[str, str]` | Namespace of the root element as `{"ns": <uri>}`. Not used by the queries. |

#### 1.1.2 `load`

```python
def load(self) -> bool
```

Parses the file with `lxml` and checks that the local name of the root element is `AUTOSAR`.

| Return value | Condition |
| :--- | :--- |
| `True` | The file was parsed and the root element is `AUTOSAR`. |
| `False` | The file cannot be read (`OSError`), is not well-formed XML (`XMLSyntaxError`), or the root element is not `AUTOSAR`. A message is printed to standard output. |

The method does not raise exceptions for these cases. It does not validate the file against the AUTOSAR XML schema.

#### 1.1.3 `get_elements`

```python
def get_elements(self, element: ET._Element, tag_name: str, direct_only: bool = True) -> list[ET._Element]
```

Returns all elements below `element` with the given local name. The namespace is ignored.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `element` | `ET._Element` | required | Start node of the search. |
| `tag_name` | `str` | required | Local name, for example `"RUNNABLE-ENTITY"`. |
| `direct_only` | `bool` | `True` | `True`: direct children only. `False`: all descendants. |

| Return value | Description |
| :--- | :--- |
| `list[ET._Element]` | Matching elements in document order. Empty if none match. |

#### 1.1.4 `get_child_elements`

```python
def get_child_elements(self, element: ET._Element) -> list[ET._Element]
```

Returns all direct child elements of `element`. Comments and processing instructions are not included.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `element` | `ET._Element` | Parent node. |

| Return value | Description |
| :--- | :--- |
| `list[ET._Element]` | Child elements in document order. |

#### 1.1.5 `get_single_element`

```python
def get_single_element(self, element: ET._Element, tag_name: str, direct_only: bool = True, default: Any = None) -> Any
```

Returns the first element that `get_elements()` would return, or `default`. Currently not used by the checks.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `element` | `ET._Element` | required | Start node of the search. |
| `tag_name` | `str` | required | Local name, for example `"INTERNAL-BEHAVIORS"`. |
| `direct_only` | `bool` | `True` | `True`: direct children only. `False`: all descendants. |
| `default` | `Any` | `None` | Returned if no element matches. |

| Return value | Description |
| :--- | :--- |
| `ET._Element \| Any` | First matching element, or `default`. |

#### 1.1.6 `get_element_text`

```python
def get_element_text(self, element: ET._Element, tag_name: str, direct_only: bool = True, default: Any = None) -> str | None
```

Returns the text of the first element with the given local name. Whitespace is not removed.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `element` | `ET._Element` | required | Start node of the search. |
| `tag_name` | `str` | required | Local name, for example `"SHORT-NAME"`. |
| `direct_only` | `bool` | `True` | `True`: direct children only. `False`: all descendants. |
| `default` | `Any` | `None` | Returned if no element matches or the element has no text. |

| Return value | Description |
| :--- | :--- |
| `str \| None` | Text of the element, or `default`. |

#### 1.1.7 `get_all_composition_swcs`

```python
def get_all_composition_swcs(self) -> list[ET._Element]
```

Returns all `COMPOSITION-SW-COMPONENT-TYPE` elements in the document, at any depth.

| Return value | Description |
| :--- | :--- |
| `list[ET._Element]` | Composition elements in document order. |

#### 1.1.8 `get_composition_swc_ref`

```python
def get_composition_swc_ref(self, composition: ET._Element) -> dict[str, list[str]]
```

Reads all `SW-COMPONENT-PROTOTYPE` elements of a composition.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `composition` | `ET._Element` | A `COMPOSITION-SW-COMPONENT-TYPE` element. |

| Return value | Description |
| :--- | :--- |
| `dict[str, list[str]]` | Two lists of equal length: `"swc_names"` with the `SHORT-NAME` of each prototype and `"swc_refs"` with its `TYPE-TREF`. The entries at the same index belong to the same prototype. |

#### 1.1.9 `get_all_atomic_swcs`

```python
def get_all_atomic_swcs(self) -> list[ET._Element]
```

Returns all elements whose local name contains `SW-COMPONENT-TYPE`, except `COMPOSITION-SW-COMPONENT-TYPE`. This includes, for example, `APPLICATION-SW-COMPONENT-TYPE`, `SERVICE-SW-COMPONENT-TYPE` and `COMPLEX-DEVICE-DRIVER-SW-COMPONENT-TYPE`.

| Return value | Description |
| :--- | :--- |
| `list[ET._Element]` | Atomic component elements in document order. Empty if `load()` was not successful. |

#### 1.1.10 `get_swc_internal_behavior`

```python
def get_swc_internal_behavior(self, swc_element: ET._Element) -> tuple[dict[str, Any], list[dict[str, str]]]
```

Extracts events, runnables, per-instance memories and shared parameters of one atomic component and runs the consistency checks. Only the first `EVENTS` container found in the component is evaluated.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `swc_element` | `ET._Element` | An atomic software component element. |

The return value is a tuple of two elements.

**1. Extracted data** (`dict[str, Any]`):

| Key | Type | Content |
| :--- | :--- | :--- |
| `"events"` | `list[list[str]]` | One entry per event with a runnable reference: `[event_type, event_name, runnable_ref, extra_info]`. Orphaned events are not included. |
| `"runnables"` | `list[dict[str, str]]` | One entry per runnable and triggering event with the keys `name`, `trigger_type`, `event_name`, `extra_info`. Runnables without an event have `trigger_type` `"NO-EVENT (Passive / Call-Return)"`. |
| `"pims"` | `list[str]` | `SHORT-NAME` of each per-instance memory. |
| `"parameters"` | `list[str]` | `SHORT-NAME` of each shared parameter. |

**2. Issues** (`list[dict[str, str]]`): one dictionary per finding with the keys `severity`, `type` and `description`.

| `type` | `severity` | Condition |
| :--- | :--- | :--- |
| `Orphaned Event` | `ERROR` | Event without `START-ON-EVENT-REF`. |
| `Invalid Timing` | `CRITICAL` | `TIMING-EVENT` whose `PERIOD` is missing, empty, not a number, not finite, zero or negative. |
| `Untriggered Runnable` | `WARNING` | Runnable that is not referenced by any event. |

See the [check catalog](checks.md) for the rationale of each check.

#### 1.1.11 `export_to_markdown`

```python
def export_to_markdown(self, all_swc_details: list[dict[str, Any]], all_architecture_issues: list[dict[str, str]], filename: str) -> None
```

Writes the Markdown report. The target folder is created if it does not exist. An existing file is overwritten.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `all_swc_details` | `list[dict[str, Any]]` | One entry per component with the keys `name` and `details` (the extracted data from `get_swc_internal_behavior()`). |
| `all_architecture_issues` | `list[dict[str, str]]` | All issues of all components. |
| `filename` | `str` | Path of the report file. |

---

## 2. `src/main.py`

### 2.1 `process_arxml_architecture`

```python
def process_arxml_architecture(arxml_file: str, arxml_report_file: str) -> None
```

Runs the complete process: load the file, list the compositions, evaluate all atomic components and write the report. Progress is printed to standard output. If `load()` returns `False`, an error message is printed and no report is written.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `arxml_file` | `str` | Path of the ARXML file. |
| `arxml_report_file` | `str` | Path of the report file. |

### 2.2 `resolve_paths`

```python
def resolve_paths() -> tuple[str, str]
```

Determines the input file from `sys.argv` and derives the report path.

| Command-line input | Input file used |
| :--- | :--- |
| One argument ending in `.arxml` | The given path. |
| No argument | `tests/samples/Standard_Compliance_Sample.arxml` |
| More than one argument | Default sample file, with a warning. |
| Argument without `.arxml` extension | Default sample file, with a warning. |

The report path is `examples/arxml_report_<input file name>.md`, relative to the current working directory. An existing report at this path is deleted.

| Return value | Description |
| :--- | :--- |
| `tuple[str, str]` | Input file path and report path. |

| Exception | Condition |
| :--- | :--- |
| `ARXMLFileNotFoundError` | The input file does not exist. |

### 2.3 Command-line entry point

When `src/main.py` is run as a module, `resolve_paths()` and `process_arxml_architecture()` are called. An `ARXMLToolError` is printed to standard error and the process exits with code `1`.

---

## 3. `src/exceptions.py`

| Exception | Parent class | Raised by |
| :--- | :--- | :--- |
| `ARXMLToolError` | `Exception` | Not raised directly. Base class for all exceptions of the tool. |
| `ARXMLValidationError` | `ARXMLToolError` | `load()`, if the root element is not `AUTOSAR`. Caught inside `load()`, which then returns `False`. |
| `ARXMLFileNotFoundError` | `ARXMLValidationError` | `resolve_paths()`, if the input file does not exist. |
| `ARXMLParserError` | `ARXMLToolError` | Currently not raised. |