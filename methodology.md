# Methodology

This project is an **AI-assisted independent replication and extension** of published Block Blast reverse-engineering findings. The purpose is to establish what the examined files actually demonstrate, without generalizing every code path to every player.

## 1. Preserve primary artifacts

Keep the original downloaded IPA/APK archives read-only and compute SHA-256 before processing. Record file size, retrieval date (when known), app version, build, bundle/package identifier, and the exact origin of each remote module.

Local artifacts inspected for this report include:

- com.blockpuzzle.us.ios_7.5.1_und3fined.ipa
- ios751.tar.gz
- android1081.tar.gz

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

- Type 03: a short HEK header, repeating XOR transform, with optional gzip.
- Type 01: HEK header, 16-byte-key XXTEA transform, a recognized compression wrapper and Brotli decompression.

The approach was checked by comparing independently decoded bytes with known runtime plaintext and with the separately recovered source archive.

This repository does not include the game's decryption key, full proprietary decoder, protected bundled assets, or decrypted commercial source. Method descriptions are provided to explain validation and support appropriate independent review without redistributing a large copyrighted codebase.

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

Reverse engineering was performed with AI assistance (ChatGPT/Daybreak), static code inspection, runtime captures and checksum comparison. AI-generated analysis is not itself evidence. Findings are attributed to specific files, code paths and corroboration checks, and must remain open to correction.
