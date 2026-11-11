# Cross-platform comparison

## Examined artifacts

| Platform | Local artifact | Identification | Evidence class |
| --- | --- | --- | --- |
| iOS | com.blockpuzzle.us.ios_7.5.1_und3fined.ipa | Bundle com.blockpuzzle.us.ios; version 7.5.1; build 7512; decrypted Mach-O (cryptid = 0) | Repackaged app package |
| iOS | ios751.tar.gz | Embedded HEK-decoded resources plus separately downloaded remote bundles | Recovered evidence set |
| Android | android1081.tar.gz | Android 10.8.1 base/split APKs and runtime captures | Runtime/recovery evidence set |
| Android | android10.tar(1).gz | Runs labeled 10.7.2, 10.7.3, 10.7.4 and 10.8.0; APK manifests verify the latter three | Additional runtime/recovery evidence set |

See the checksum and source-map files for exact references.

## iOS package compared with decoded archive

The IPA contains HEK-protected embedded gameplay resources. Earlier spot-checks successfully reproduced their decoding and matched seven outputs in the iOS recovery archive, including the settings registry, main traits, modelFeature, and selected difficulty/MAB modules.

The decoded settings file contains module mappings including:

- RewardHighValueAdHarvestTrait -> ff35e
- ZX294_RewardHighValueAdHarvestTrait -> 9aa15
- CTRefactorRewardHighValueAdHarvestTrait -> db110

**These are embedded references to remote bundles, not proof that the corresponding JavaScript was packaged inside the IPA.**

The separate iOS recovery archive contains plaintext from later retrieved CDN modules, including ff35e and 9aa15. It is important not to assign the CDN plaintext the same historical release date as the IPA solely on the basis of the version label.

## Android observations

The Android 10.8.1 runtime capture includes a settings registry mapping RewardHighValueAdHarvestTrait to **700f5** and loader activity targeting that module. The standard reward-harvest implementation was independently captured and hashed in an earlier Android session (SHA-256 f94a5d54d7f6ab0af097f408bda09b091e7767b17749f8ba828b41b638b330ad); **that plaintext file is not among the Android 10.8.1 archive's captured return payloads**.

The 10.8.1 archive itself provides direct code evidence of interstitial-eCPM-based ADPushBackModel variants and revive-control logic.

The later-supplied multi-version archive now supplies the previously mentioned Android standard source directly: four retained evaluator captures are byte-identical, each 15,616 bytes with SHA-256 f94a5d54d7f6ab0af097f408bda09b091e7767b17749f8ba828b41b638b330ad. Independent HEK decoding of its encrypted 700f5 resource reproduces those bytes. Three APK-embedded settings files also decode exactly to their early runtime captures. The report distinguishes those embedded settings from common later settings loaded in all four runs; it does not date the remote implementation to each APK's release. See [Android verification](android-multiversion.md).

The supplied session records a one-expression Android/iOS source difference in `normalizeGpAdEcpm`. Replacing Android's multiplication of valid positive inputs by 1,000 with an unchanged return reproduces exactly the previously published 15,610-byte iOS plaintext hash, 179bf50ae3c0c4a9bd5457281e4876faae728778f6181dbb0d3799b42ec70d61. This is a newly checked relationship between the actual Android bytes and the earlier iOS hash, not a new acquisition of the iOS response.

## Relationship to the original investigation

[Ayo Omolewa's original report (15 October 2026)](https://ayoships.com/breakdowns/block-blast) documented Android **10.8.2** and iOS **7.4.9** and published code-level evidence of the rewarded-ad harvest mechanism. This project was prompted by that investigation and independently followed the decryption, code inspection and cross-platform analysis path using its own artifacts. It should be called an **independent replication of specified technical findings**, not an independent first discovery.

The SHA-256 of the recovered iOS standard reward-harvest plaintext in our archive is 179bf50ae3c0c4a9bd5457281e4876faae728778f6181dbb0d3799b42ec70d61, which also appears in the original report. This agreement supports code identity but is not sufficient evidence of independent CDN historical timing.

## What is and is not cross-platform verified

**Verified from the examined files:** common feature/trait architecture, iOS remote module references, iOS recovered reward-harvest implementation, identical standard Android captures across four labeled runs, exact Android asset-to-capture decoding matches, a retained client feature configuration, and Android 10.8.1 registry/advertisement/revive/difficulty components. The 10.7.2 package version remains less strongly established because its APK is absent from the new archive.

**Not established:** that the same remote cohort settings were active for both platforms, that the implementations ran for the same fraction of users, or that remote bundles retrieved during this investigation were already being delivered when iOS 7.5.1 originally shipped.
