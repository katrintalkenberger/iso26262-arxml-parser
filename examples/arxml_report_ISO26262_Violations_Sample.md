# AUTOSAR Architecture & ISO 26262 Safety Report

This report contains a static analysis of the software architecture with consistency checks to support the verification of the software architectural design according to **ISO 26262-6**.

## ⚠️ ISO 26262 Architectural Integrity Check

**Status:** 🛑 Architectural violations found! 1 Critical, 1 Error, 1 Warning

| Severity | Issue type | Description |
| :--- | :--- | :--- |
| ❌ ERROR | Orphaned Event | Event 'Orphaned_Timer_Event' in SWC 'NonCompliant_Service_SWC' is missing the runnable reference (`START-ON-EVENT-REF`). |
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

