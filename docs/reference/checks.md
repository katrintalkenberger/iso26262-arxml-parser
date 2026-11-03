# Check catalog

This catalog lists the consistency checks that the parser runs on atomic software components, the condition that triggers each finding, its severity and its relation to ISO 26262-6.

The checks support the verification of the software architectural design. They detect structural inconsistencies in the ARXML configuration. They do not assess whether the design is safe, and they do not replace a review or a safety assessment. The parser is not qualified as a software tool according to ISO 26262-8.

To trigger each finding with a modified ARXML file, see [Inject architecture faults](../how-to/inject-architecture-faults.md).

---

## Severity levels

| Severity | Report symbol | Meaning |
| :--- | :--- | :--- |
| CRITICAL | 🚨 | The configuration specifies behavior that cannot be executed as defined. |
| ERROR | ❌ | An element is incomplete, so its behavior cannot be determined from the configuration. |
| WARNING | ⚠️ | The configuration is consistent but possibly unintended. Review required. |

---

## Checks

| ID | Check | Element | Condition | Severity | Rationale | Notes | ISO 26262-6 | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ARX-001 | Orphaned event | Any event in `EVENTS` | `START-ON-EVENT-REF` missing or empty | ERROR | The event activates no runnable, so the configuration does not show which function runs. | The event is excluded from further checks. | *to be verified* | implemented |
| ARX-002 | Invalid timing period | `TIMING-EVENT` with runnable reference | `PERIOD` missing, empty, not a number, not finite, or ≤ 0 | CRITICAL | The activation rate cannot be scheduled, so the timing behavior is undefined. | Only values > 0 are valid. | *to be verified* | implemented |
| ARX-003 | Untriggered runnable | `RUNNABLE-ENTITY` | Not referenced by any event of the same component | WARNING | The runnable is never activated. This can be intended, for example during integration. | Only the first `EVENTS` container is evaluated. Runnables without `SHORT-NAME` are skipped. | *to be verified* | implemented |
| ARX-004 | Dangling runnable reference | Any event in `EVENTS` | `START-ON-EVENT-REF` points to no existing runnable | *tbd* | The event refers to a runnable that does not exist. | | *to be verified* | planned |

Check IDs are stable. An ID is never renumbered or reused, also if a check is removed.

---

## Not checked

The following is outside the scope of the current checks:

- Mandatory content of event types other than `TIMING-EVENT`, apart from the runnable reference.
- References across components. Runnables are matched by the end of the reference path, not by resolving the full path.
- Validation against the AUTOSAR XML schema (XSD). Misspelled or misplaced elements are not reported, they are not found.