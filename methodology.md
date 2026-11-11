# Methodology

This project is an **AI-assisted independent replication and extension** of published Block Blast reverse-engineering findings. The purpose is to establish what the examined files actually demonstrate, without generalizing every code path to every player.

## 1. Preserve primary artifacts

Keep the original downloaded IPA/APK archives read-only and compute SHA-256 before processing. Record file size, retrieval date (when known), app version, build, bundle/package identifier, and the exact origin of each remote module.

Local artifacts inspected for this report include:

- com.blockpuzzle.us.ios_7.5.1_und3fined.ipa
- ios751.tar.gz
- android1081.tar.gz
- android10.tar(1).gz
- 15.tar.gz (supplementary Codex session history)

The archives are not uploaded publicly. Their hashes and selected internal object hashes are published under evidence/.

## 2. Distinguish evidence classes

Use four labels throughout:

- **Embedded:** A file actually present in the installed application package.
- **Referenced:** A module name and content ID listed in embedded app settings or a manifest.
- **Retrieved remotely:** A response obtained from the game's CDN after package acquisition.
- **Runtime captured:** A buffer obtained from a running application loader/decryption boundary.

A file may qualify for multiple labels, but one does not imply another. In particular, a remote module reference in a signed IPA is not evidence the same module contents were historically served during that IPA's original release.

## 3. Decode and check integrity

The investigated HEK asset formats were identified as:

- Type 03: an eight-byte HEK header, repeating XOR transform, with optional gzip.
- Type 01: the same header, 16-byte-key XXTEA transform over little-endian words, and a validated trailing plaintext-length word. Decoded data beginning with `af fa` has a four-byte big-endian decompressed size followed by Brotli data; other decoded data is returned directly.

The approach was checked by comparing independently decoded bytes with known runtime plaintext and with the separately recovered source archive.

A later review of the supplied `analysis/decrypt_hek.py` made those format details explicit and produced a [public research decoder with synthetic tests](tools/hek/README.md). It accepts a locally supplied key and includes no application key, protected bundled assets, or decrypted commercial source. Header bytes five through seven are skipped; their meaning is not established by that implementation.

The public adaptation was initially checked against fixed synthetic XXTEA fixtures generated with a separate C encoder, optional Brotli/gzip inputs, malformed inputs, and CLI file handling. The Brotli fixture was also checked with Node's implementation.

With the later-supplied Android archive, decoding was also repeated on actual retained assets. Three APK-embedded settings files match their corresponding evaluator captures exactly. The encrypted 700f5 standard reward-harvest module matches the retained decoded source and identical captures from four labeled runs. The Type 03 bundle configuration decodes to the same JSON object as its retained decoded counterpart. These checks, package-manifest identities, and version-provenance limits are documented in [the Android verification](findings/android-multiversion.md). The original iOS IPA and separate Android 10.8.1 archive were not re-examined in that update.

Retained SQLite state was inspected through a read-only connection to a working copy with its WAL present. The relevant cached feature entry was reported as **stored configuration**, not an authenticated server response or proof that a gameplay branch completed. Raw account/device data and server/request identifiers remain private.

Do not run unknown game JavaScript while inspecting it. Treat decompiled source and downloaded configuration as untrusted input.

## 4. Map behavior, not just names

For each candidate mechanism:

1. Identify the trait and any referenced module hash.
2. Locate event handlers and initiation conditions.
3. Trace relevant stored variables and configuration properties.
4. Identify the exact selection mutation (e.g. replacing a bottom-algorithm list versus prepending a priority list).
5. Determine whether a later module can override the proposed selection.
6. Separate code-level capability from observed runtime effects.

The basic rewarded-ad death path is recorded in findings/rewarded-ad-death.md; the alternative variants are in findings/variants-and-difficulty.md.

## 5. Verify the final board

To prove that an ordinary player actually received an induced impossible hand, capture a trace with the initial board, all three pieces, the accepted algorithm selection, all later overrides, the active trait configuration, and the subsequent revive events.

Evaluate all possible legal placement orders, accounting for row/column clearing. This investigation does not claim to have run a population-level randomized trial or to have measured the prevalence of every code path.

## 6. Report uncertainties

Do not report "every player", "always", "fraud", or "criminal" based solely on a named trait or a recoverable branch. Record both enabled and disabled defaults, server-side cohorting possibilities, missing timestamps, alternate algorithms, and platform/version mismatches.

## Responsible handling

- Keep complete copyrighted game packages, decrypted modules, raw player logs and CDN payload dumps in private storage.
- Publish limited excerpts, source references, hashes, pseudocode, and independent verification tooling instead.
- Avoid disclosing credentials, device/account IDs or private advertising identifiers.
- Link to and credit the original investigation explicitly.
- Document changes to the public report by commits, not silent replacement of published claims.

## Tooling and authorship

Reverse engineering was performed with AI assistance (ChatGPT/Daybreak and Codex), static code inspection, runtime captures and checksum comparison. The [supplied Codex session](evidence/session-review.md) records earlier recovery/comparison work; Codex also assisted the supplementary-tool review, decoder validation, and documentation updates. Selected recorded tool results were checked against the supplied artifact bytes. AI-generated narrative and unverified transcript timestamps are not themselves evidence of application behavior or historical distribution. Findings remain open to correction.

## Supplemental Ghidra scripts

The [exploratory Ghidra Java scripts](tools/ghidra/README.md) document an early, build-specific investigation of the Cocos native loader and HEK-adjacent callbacks. These scripts are **not** the decoder used to validate the recovered JavaScript and do not independently establish any gameplay-related finding. They are included to document the analysis approach and are not claimed to have been compatibility-tested for public release.

## Supplementary capture-script review

The [review of 36 supplied analysis source files](evidence/analysis-tooling.md) records native loader/evaluator hooks, capture filters and size limits, process-modifying probes, and an intended Android version-testing loop. These were inspected as source, not newly executed against a device. A version named in a test script is not a successfully tested version, and the script's native-code comparison does not establish compatibility at the different evaluator-hook location. The later [retained-capture verification](findings/android-multiversion.md) supplies additional evidence separately from the script's intended coverage.
