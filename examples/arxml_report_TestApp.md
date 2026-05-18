# AUTOSAR Architecture & ISO 26262 Safety Report

This document contains the static architectural analysis and the  compliance check in accordance with the requirements of **ISO 26262-6** completeness and consistency). 

## ⚠️ ISO 26262 Architectural Integrity Check

**Status:** ✅ Pass (No structural violations or orphaned elements found).

---

## 🧩 Software Component Details

### Software Component: HMI

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| HMI_MainFunction | TIMING-EVENT | TE_HMI_MainFunction_100ms | Period: 0.1s |


#### Per-Instance Memories (PIMs)
N/A

#### Shared Parameters
N/A

---

### Software Component: SeatManger

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| SeatManger_SetHeight | DATA-RECEIVED-EVENT | DRE_rpSeatCtrlBtn_DE_HeightBtnState | N/A |
| SeatManger_SetIncline | DATA-RECEIVED-EVENT | DRE_rpSeatCtrlBtn_DE_InclinceBtnState | N/A |
| SeatManger_SetSlide | DATA-RECEIVED-EVENT | DRE_rpSeatCtrlBtn_DE_SlideBtnState | N/A |


#### Per-Instance Memories (PIMs)
N/A

#### Shared Parameters
N/A

---

