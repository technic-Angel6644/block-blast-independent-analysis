# Provenance, chronology and signature limitations

## Primary files

- **iOS IPA:** com.blockpuzzle.us.ios_7.5.1_und3fined.ipa, 91,043,837 bytes; SHA-256 ee8a26cab77c783e398f4a5777b2a9a6534900fa25091aeb19f927804facb101.
- **iOS recovery:** ios751.tar.gz, 27,418,326 bytes; SHA-256 3533a6c43e0ec99167740af9cd64a4a77046aef833f615ce4eb79691e3ddd2c1.
- **Android recovery:** android1081.tar.gz, 140,061,193 bytes; SHA-256 892f65b1c296fd061f674f32ec1022b04815b34ed61c34963d1e6df8ca21b040.

These are the researcher's received artifacts, **not** a guarantee that the files are the exact byte-for-byte store downloads. No original store-downloaded IPA hash is asserted.

## iOS application identity

The examined bundle's metadata identifies com.blockpuzzle.us.ios, version 7.5.1, build 7512. Its ARM64 Mach-O executable has cryptid = 0, consistent with removal of FairPlay encryption. The package also contains a marker associated with a decryption/repackaging workflow.

A prior inspection reported consistency between the IPA's embedded resource manifest and most package resources, with differences concentrated in decrypted executable/framework regions. This supports an original signed-package lineage, but **is not a standalone proof of Apple trust-chain validation or of remote CDN availability in the original release**.

## Remote versus local evidence

The iOS IPA's **settings registry** references ff35e, db110 and 9aa15. The separate iOS recovery archive supplies decrypted implementations for these and other remote trait variants.

The presence of a named remote resource in an app's catalog does not show when the associated URL first served a particular response, whether that response later changed, or which production cohort received it. CDN fetch timestamps, response headers, manifest assignment and cached object hashes would materially improve historical attribution.

The Android recovery file supplies contemporaneous runtime loader-return buffers and install APKs from an instrumented session. A runtime file read establishes loading activity but not necessarily activation of that trait's final death-selection behavior for all users.

## Supplementary tooling source

A later-supplied `analysis.tar(1).gz` archive contains 36 source scripts plus a compiled Python cache. Its SHA-256 and the original decoder's hash are recorded in [analysis-tooling.md](analysis-tooling.md). It is a supplementary methodology source, separate from the three primary application/recovery artifacts above. No per-version Android result captures or original application packages accompanied it, and the presence of script source does not demonstrate successful execution.

## Publication boundaries

This repository omits complete proprietary software packages and decompiled bundles. Privately retained originals should be preserved as read-only files and ideally duplicated securely. If an independently obtained package or app-store record is later supplied, document it as a **new source artifact** with its own checksums and acquisition record, rather than retroactively treating it as proof about an earlier file.
