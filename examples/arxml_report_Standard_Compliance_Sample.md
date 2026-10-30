# AUTOSAR Architecture & ISO 26262 Safety Report

This report contains a static analysis of the software architecture with consistency checks to support the verification of the software architectural design according to **ISO 26262-6**.

## ⚠️ ISO 26262 Architectural Integrity Check

**Status:** ✅ Pass (No structural violations or orphaned elements found).

---

## 🧩 Software Component Details

### Software Component: ValidApp_SWC

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| Cyclic_Runnable | TIMING-EVENT | Timer_10ms_Event | Period: 0.01s |


#### Per-Instance Memories (PIMs)
- `Velocity_Filtered_PIM`
- `Acceleration_State_PIM`

#### Shared Parameters
- `Filter_Gain_Param`

---

### Software Component: ValidCdd_SWC

#### Runnables
| Runnable name | Event type | Event name | Additional info |
| :--- | :--- | :--- | :--- |
| Hardware_Runnable | OPERATION-INVOKED-EVENT | ClientRequest_Event | N/A |


#### Per-Instance Memories (PIMs)
- `Hardware_Register_Buffer_PIM`

#### Shared Parameters
- `Sensor_Calibration_Offset_Param`
- `SPI_Baudrate_Config_Param`

---

