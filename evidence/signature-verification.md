# IPA resource integrity checks

This page describes a reproducible check against the supplied repackaged/decrypted IPA. It does not assert that the modified IPA retains a valid installable Apple App Store signature.

## Identification

- Package: com.blockpuzzle.us.ios_7.5.1_und3fined.ipa.
- SHA-256: ee8a26cab77c783e398f4a5777b2a9a6534900fa25091aeb19f927804facb101.
- Bundle metadata: Block Blast!, com.blockpuzzle.us.ios, version 7.5.1, build 7512.
- ARM64 Mach-O executable: fangkuaipintu-mobile, encryption-info command present with **cryptid = 0**.

The executable is marked as decrypted. This is expected for a FairPlay-removed copy; it does not alone prove a particular distribution history.

## SHA-256 resource-manifest consistency

Using Python's **zipfile**, **plistlib** and **hashlib**, the following comparison was made:

1. Read Payload/fangkuaipintu-mobile.app/_CodeSignature/CodeResources.
2. Parse its files2 dictionary.
3. For each entry with a hash2 value, read the corresponding ZIP member.
4. Compute its SHA-256 and compare the raw digest bytes with hash2.

Result for the uploaded IPA:

| Check | Count |
| --- | ---: |
| Matching files2/hash2 entries | 5,357 |
| Differing files2/hash2 entries | 17 |
| Missing referenced entries | 0 |

All 17 differences were native executables located in embedded frameworks or the push extension. Ordinary gameplay resources included in the signed resource manifest matched their recorded SHA-256 values.

This pattern is consistent with an originally signed package whose executable regions were subsequently decrypted, but a repacker could in principle produce new resource manifests. Integrity against the **present resource manifest** is not a substitute for validating that manifest against an independent trusted Apple-distributed original.

## Meaning for the research

The embedded registry and encrypted assets in this package have much stronger integrity support than an unproven plaintext text dump. However:

- No full independent Apple trust-chain validation is claimed here.
- Decoded **remote CDN modules** are not covered by the IPA's signed resource hashes merely because a module name appears in the embedded settings.
- The dates on remote payloads require separate evidence.
- The corresponding source archive's independently decoded files should be compared using the published checksums, not inferred from filenames alone.
