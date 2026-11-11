# Exploratory Ghidra scripts for the iOS HEK investigation

These three Java files were produced during the initial **static analysis** of the examined iOS ARM64 Mach-O (the IPA identified as Block Blast! 7.5.1 / build 7512). They are supplemental research tooling, **not** the final HEK decoder and **not** evidence by themselves that the game selected any particular puzzle pieces.

| Script | Purpose | Important limitation |
| --- | --- | --- |
| [FindHekLoader.java](FindHekLoader.java) | Searches names and bytes associated with Cocos script loading (`jsb_init_file_operation_delegate`, `ScriptEngine::runScript`, `HEK:`, etc.), follows references, and explores possible C++ RTTI references | Full-memory string/pointer scanning and recursive decompilation can be slow and produce large logs; heuristic targets are not verified decryptors |
| [InspectHekFunctions.java](InspectHekFunctions.java) | Creates/disassembles and decompiles selected native candidate functions at specified addresses | Addresses are build- and image-base-specific; it can modify the **Ghidra analysis database** by defining code/functions |
| [InspectHekVtables.java](InspectHekVtables.java) | Treats selected regions as possible C++ function-pointer tables and decompiles recognizable targets | Not every eight-byte value is a valid function pointer; candidate table regions are heuristic |

## How to inspect

1. Import the **same** decrypted Mach-O into a Ghidra project, then allow normal analysis to complete.
2. Configure Ghidra's Script Manager to include this directory, or copy the three `.java` files into an existing Ghidra script directory.
3. Verify the target's image base and mapped address ranges **before** running scripts that reference hard-coded addresses.
4. Run selectively. Avoid running the broad `FindHekLoader` scan on a large program unless substantial output and runtime are acceptable.
5. Interpret findings alongside the actual decompiler output and debugger/runtime observations; a string reference or possible vtable does not prove a decoder's behavior.

The scripts were reviewed as source before inclusion, but **have not been executed or compatibility-tested in a Ghidra environment as part of this publication update**. They should be treated as historical exploratory tools rather than a supported end-to-end workflow.

## Relationship to the final findings

The decisive JavaScript recovery was accomplished by reconstructing the HEK formats and validating output against known runtime-captured plaintext; the final Android/iOS gameplay conclusions are documented in [../../findings/](../../findings/), based on recovered trait implementations and source-level conditions.

These scripts were originally used to investigate possible native Cocos loader/decryption paths. They did not independently establish the final HEK Type 01 format, and this repository makes no claim otherwise.

**Not included here:** the commercial executable, proprietary decrypted JS assets, Ghidra program databases, and raw decompilation dumps.

Reference: [Ghidra Script Manager documentation](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/Base/src/main/help/help/topics/GhidraScriptMgrPlugin/GhidraScriptMgrPlugin.htm).
