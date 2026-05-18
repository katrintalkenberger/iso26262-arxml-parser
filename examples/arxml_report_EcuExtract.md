# AUTOSAR Architecture & ISO 26262 Safety Report

This document contains the static architectural analysis and the  compliance check in accordance with the requirements of **ISO 26262-6** completeness and consistency). 

## ⚠️ ISO 26262 Architectural Integrity Check

**Status:** ✅ Pass (No structural violations or orphaned elements found).

---

## 🧩 Software Component Details

### Software Component: Door

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| DoorMain | TIMING-EVENT | timingEvent_0_1 | Period: 0.1s |
| SetLocked | OPERATION-INVOKED-EVENT | Command_SetLock | Operation Ref: /Demo/Interfaces/DoorCommands/SetLock |


#### Per-Instance Memories (PIMs)
*N/A*

#### Shared Parameters
*N/A*

---

### Software Component: IoHwAb

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| DigitalWrite | OPERATION-INVOKED-EVENT | Digital_Led_Write | Operation Ref: /Demo/Services/IoHwAb/DigitalServiceWrite/Write |


#### Per-Instance Memories (PIMs)
*N/A*

#### Shared Parameters
*N/A*

---

### Software Component: DoorControl

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| Main | TIMING-EVENT | timingEvent_0_1 | Period: 0.1s |


#### Per-Instance Memories (PIMs)
*N/A*

#### Shared Parameters
*N/A*

---

