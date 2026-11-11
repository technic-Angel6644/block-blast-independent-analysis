# Review of the supplied Codex session record

The supplementary `15.tar.gz` archive is **6,221,427 bytes**, SHA-256 **1ad132f58f5830f9292da724bb81d99cc11ed18fcbcf9e1182c0c51c2e4c63ea**. It contains one uncompressed JSONL session and two compressed session files. The review focused on relevant command/result records in the uncompressed file; the other sessions are not used to substantiate the findings here.

The relevant uncompressed JSONL is **11,712,667 bytes**, SHA-256 **04d094eb4bc388a68801765bef8364151be9eef065b9d6bf5c32c8c6234ff195**. This identifies it without publishing session/account identifiers or the raw transcript. Record numbers below are one-based physical line numbers in that file.

## Useful recorded checks

| Record | Recorded timestamp, UTC | Command-result observation | Verification in this update |
| ---: | --- | --- | --- |
| 1100 | 2026-10-15 20:56:52.358 | Four Android standard-trait captures have the same `f94a5d54…` SHA-256 and 15,616-byte metadata lengths | Recomputed from all four files in the newly supplied Android archive |
| 2099 | 2026-10-15 21:40:03.967 | HEK decoding of `index.700f5.js` produces 15,616 bytes matching the retained Android source hash | Reproduced using the public decoder and privately supplied key |
| 2247 | 2026-10-15 21:43:17.924 | Android/iOS standard-source diff changes one eCPM normalization expression | Applying that change to the supplied Android source reproduces the previously published iOS SHA-256 |

See [the Android verification report](../findings/android-multiversion.md) for complete source paths, hashes, and scope qualifications.

These are records of tool commands and their returned results, rather than treating an assistant's narrative as evidence. They document Codex participation in the earlier recovery/comparison work, in addition to the later repository and tooling review.

## Evidentiary weight

The session is a workflow record from the same investigation, not another independent researcher or a separate application acquisition. The stronger corroboration comes from independently recomputing the retained bytes and reproducing decoding during this update.

Session timestamps and filenames are not trusted timestamping, proof of public availability on those dates, or proof that historical CDN responses were distributed to ordinary users. The transcript also cannot authenticate artifacts that were not supplied here, or establish that an earlier attempted tool command succeeded unless a corresponding result supports it.

The record does not supply a complete capture of a monetization-conditioned decision followed through to the final three pieces. It therefore does not remove the report's runtime-outcome or rollout limitations.

Raw sessions contain local paths, configuration/key material, and potentially identifying metadata. Only these source identifiers and narrowly described observations are published; the transcript is retained privately.
