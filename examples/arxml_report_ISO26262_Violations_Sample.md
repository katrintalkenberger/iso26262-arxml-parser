# AUTOSAR Architecture & ISO 26262 Safety Report

This document contains the static architectural analysis and the  compliance check in accordance with the requirements of **ISO 26262-6** completeness and consistency). 

## ⚠️ ISO 26262 Architectural Integrity Check

**Status:** 🛑 Architektur-Verletzungen gefunden! 1 Critical, 3 Error, 1 Warning)

| Schweregrad | Fehlertyp | Beschreibung |
| :--- | :--- | :--- |
| ❌ ERROR | Orphaned Event | Event 'None' in SWC 'NonCompliant_Service_SWC' is missing the runnable reference (`START-ON-EVENT-REF`). |
| ❌ ERROR | Orphaned Event | Event 'Orphaned_Timer_Event' in SWC 'NonCompliant_Service_SWC' is missing the runnable reference (`START-ON-EVENT-REF`). |
| ❌ ERROR | Orphaned Event | Event 'None' in SWC 'NonCompliant_Service_SWC' is missing the runnable reference (`START-ON-EVENT-REF`). |
| 🚨 CRITICAL | Invalid Timing | Timing-Event 'Critical_ZeroTiming_Event' in SWC 'NonCompliant_Service_SWC' has invalid period (0.0s). |
| ⚠️ WARNING | Untriggered Runnable | Runnable 'Passive_Unused_Runnable' in SWC 'NonCompliant_Service_SWC' is not being actively triggered by any event. |

---

## 🧩 Software Component Details

### Software Component: NonCompliant_Service_SWC

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| Standard_Runnable | TIMING-EVENT | Critical_ZeroTiming_Event | Period: 0.0s |
| Passive_Unused_Runnable | NO-EVENT (Passive / Call-Return) | N/A | N/A |


#### Per-Instance Memories (PIMs)
- `Fault_Logger_History_PIM`

#### Shared Parameters
- `Max_Allowed_Retries_Param`

---

