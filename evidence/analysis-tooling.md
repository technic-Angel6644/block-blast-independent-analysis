# Review of the supplementary Daybreak analysis scripts

The supplied `analysis.tar(1).gz` contains 36 source files and one compiled Python cache file. It is a collection of analysis tools, not a written findings report or a set of application captures. It contributes reproducibility details but no additional observed gameplay outcome.

## Source identity

| Private source | Size in bytes | SHA-256 |
| --- | ---: | --- |
| `analysis.tar(1).gz`, as received | 23,649 | `c4f845910839100ae119e0e0d8d85a6e75eb6b61c06a6feb6cdee919be3335b8` |
| `analysis/decrypt_hek.py`, inside that archive | 3,472 | `0eacc51c3f1caa1d46cc0042d6d1bc032fb28d0bb36a631aeaf6d3a6c9b43308` |

These hashes identify the supplied research scripts. They do not authenticate application binaries, prove that any script ran successfully, or establish the chronology of earlier research. This supplementary archive is separate from the three primary artifacts in `hashes.sha256`.

## What was reviewed

| Script group | Source files | Contribution and publication decision |
| --- | ---: | --- |
| HEK decoder | 1 | Precise Type 01/03 layout and checks; a key-parameterized adaptation is published under [tools/hek](../tools/hek/README.md) |
| Frida capture hosts | 3 | Save metadata and binary messages from injected scripts; source review only |
| Native loader and file-read tracing | 6 | Locate HEK reads, copies, delegates and transform boundaries; build-specific probes, not demonstrated results |
| Evaluator tracing and fingerprint capture | 4 | Inspect a native boundary and capture candidate source buffers; coverage is filtered |
| Memory scans and native-region dumps | 6 | Exploratory string/context searches and memory dumps; omitted from public tooling as unnecessary to reproduce the documented byte format |
| Runtime modification probes | 3 | Inject JavaScript or alter exception/crash-handler behavior; kept separate from observational evidence |
| Private app-file extraction | 1 | Can collect preferences and databases; outputs may identify a player and are not public evidence here |
| Android version loop | 1 | Lists intended test versions and collection steps; contains no results |
| Ghidra scripts | 10 | Additional native-reference, decompiler and analysis-configuration helpers; build-specific exploration, not compatibility-tested here |
| Candidate-key search | 1 | Exploratory XXTEA candidate testing; unnecessary for the public decoder with an independently supplied key |

All 36 source files were inspected as text. The compiled cache was excluded. Apart from adapting and testing the decoder, this review did not run the supplied scripts against a device or native executable. The existing [three Ghidra scripts](../tools/ghidra/README.md) remain separate supplemental tools.

## Decoder details added to the methodology

`decrypt_hek.py` specifies an eight-byte header and a variant byte at offset four. Type 01 uses little-endian XXTEA words with a trailing plaintext-length word; optional compression is marked by `af fa`, followed by a four-byte big-endian decompressed size and Brotli data. Type 03 uses repeating XOR and optional gzip. The meanings of header bytes five through seven are not established by the script.

The [public adaptation and synthetic tests](../tools/hek/README.md) document these operations without distributing the embedded application key. Synthetic tests are new validation of the tool, not another application-source recovery or a replication of final gameplay outcomes.

## Android version loop: planned coverage, not verified coverage

`test_remaining_android_versions.sh` lists **10.7.4, 10.8.0, 10.8.1, 10.8.2 and 10.8.5**, using a local Android 10.7.2 capture as a comparison reference. It intends to install APK splits, record hashes and package metadata, clear app data, capture a 256-byte native-code window, compare it with the reference, and then collect evaluator buffers.

The script includes `adb shell pm clear com.block.juggle`, so rerunning it would erase that installed package's local data. It is not published as a ready-to-run collection workflow.

The fingerprint guard compares a window around module offset `0xa0b374`; the subsequent evaluator hook targets `0xa0a87c`. An unchanged window at the former location does **not** prove that the latter hook or its assumed register layout is compatible. The script's source therefore establishes intended precautions, not validated cross-version instrumentation.

No per-version result logs, package files, or captured payloads accompany this archive. The version list and the reference path must not expand the report's verified version coverage. The separately mentioned multi-version Android archive was not included in this update.

## Capture and intervention limits

`trace_type01_native.js` assumes ARM64 registers and a particular libc++ string layout, uses fixed native offsets, and limits dumps to 8 MiB. A declared loader length can consequently exceed the saved bytes. `capture_evaluator_sources.js` filters short/nonprintable candidates and normally saves buffers under 1 MiB or those containing the target trait name; larger nonmatching candidates can produce metadata only. Neither collector provides an exhaustive module inventory.

The presence of a trait name in a captured buffer or file-read trace is weaker evidence than observing that trait's decision and the resulting pieces. A memory match can also refer to a registry rather than the implementation.

`inject_js_introspection.js`, `bypass_bugsnag.js` and `patch_bugsnag_native.js` change the instrumented process. Any future result obtained with them should record those changes and be compared with an unmodified session where possible. Their presence here does not show that they were used for an earlier capture.

The report's existing gameplay findings remain unchanged. This archive improves the description of the recovery workflow and its limitations.
