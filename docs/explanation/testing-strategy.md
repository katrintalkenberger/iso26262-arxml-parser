# Testing strategy

This document explains how the parser is tested, why the tests are structured this way, and which parts of the code are not covered yet. For the commands to run the tests and the coverage report, see [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Scope

The tests verify the behavior of the parser: loading files, extracting software components, running the consistency checks and writing the report. They do not qualify the parser as a software tool according to ISO 26262-8. If the parser is used to support safety-related work, its results still need to be reviewed.

## Test data in temporary folders

The tests do not use files from the repository working directory. Each test creates its ARXML input in a temporary folder provided by pytest (`tmp_path`). Pytest creates a new, empty folder for every test and removes old folders automatically.

This has two effects. The tests produce the same result on every machine and in CI, because they do not depend on files that exist only locally. And a test that deletes or overwrites a file, for example an old report, cannot touch real project files.

Some tests reuse the valid test file from the fixture and change one detail, such as the value of `<PERIOD>` or an added XML comment. This keeps the test data small and makes clear which detail a test is about.

## Faulty input

Real ARXML files can be incomplete or contain unexpected values. The tests therefore include faulty input on purpose:

- An event without `START-ON-EVENT-REF`. The parser reports it as an orphaned event and continues with the next event.
- A timing event with a period that is missing, empty, not a number, zero, negative, infinite or `nan`. The parser reports it as a critical timing issue instead of stopping with a Python exception.
- A runnable that is not referenced by any event. The parser reports it as an untriggered runnable.
- XML comments between elements. They must not be treated as events.
- A file that is valid XML but not an AUTOSAR document. `load()` returns `False`.

Each case checks the reported severity and issue type, not only that no exception occurs.

## What is not covered

The entry point `if __name__ == "__main__":` in `src/main.py` is excluded from the coverage measurement. The functions it calls, `resolve_paths()` and `process_arxml_architecture()`, are tested directly. Running the module as a script in an additional test would test the same logic a second time.

In `src/arxml_parser.py`, the following parts are not covered by tests yet:

- `get_single_element()`, which is currently not used by any check.
- The extraction of per-instance memories and shared parameters.
- The handling of `OPERATION-INVOKED-EVENT`.
- Report sections for components without runnables, per-instance memories or shared parameters.

These are gaps, not intentional exclusions. They should be closed before further checks build on them.