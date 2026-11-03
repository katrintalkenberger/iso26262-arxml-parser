# Injecting architecture faults

This guide explains how to inject faults into an ARXML file to test the parser's validation rules, and where to source advanced industry examples.

## Sourcing Industry ARXML Examples
If you want to test the parser with large-scale, third-party AUTOSAR files, you can use open-source repository extracts such as:
* `EcuExtract.arxml` from the [patrikja autosar](https://github.com/patrikja/autosar) repository (BSD 3-Clause License).
* `TestApp.arxml` from the [mahmut-aksakalli arxml-viewer](https://github.com/mahmut-aksakalli/arxml-viewer) repository (MIT License).

Download the files and place them in `tests/samples/` to run the parser against them.

## Injecting Structural Faults for Validation Testing

You can manually manipulate any standard ARXML structure using a text editor to trigger each of the three checks.

### Option 1. Orphaned event (ARX-001)
Locate any event structure and completely delete or comment out the `<START-ON-EVENT-REF>` child tag:
```xml
<!-- Non-Compliant Modification -->
<TIMING-EVENT>
  <SHORT-NAME>Timer_Event</SHORT-NAME>
  <!-- Missing reference triggers an ERROR in the report -->
</TIMING-EVENT>
```

### Option 2. Invalid timing period (ARX-002)
Locate a `<TIMING-EVENT>` that contains a `<PERIOD>` tag. Change the value to `0.0` or a negative number:
```xml
<!-- Non-Compliant Modification -->
<TIMING-EVENT>
  <SHORT-NAME>Timer_Event</SHORT-NAME>
  <START-ON-EVENT-REF DEST="RUNNABLE-ENTITY">/Path/To/Runnable</START-ON-EVENT-REF>
  <PERIOD>0.0</PERIOD> <!-- Zero-value triggers a CRITICAL fault -->
</TIMING-EVENT>
```

### Option 3. Untriggered runnable (ARX-003)
Add a new `<RUNNABLE-ENTITY>` inside the `<RUNNABLE-ENTITIES>` container, but do not create any corresponding event that references this runnable's short-name. The parser reports it as an untriggered runnable with severity WARNING

---

## Next Steps
* To understand the technical parameters and return types of specific methods, see the [API Reference](../reference/api.md).
* To explore the architectural background of the AUTOSAR schema, check out the [Explanations](../explanation/autosar-arxml-structure.md).