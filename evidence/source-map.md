# Evidence map and source classification

All paths below are **paths inside privately retained evidence archives**, not repository downloads. Files are identified by SHA-256 in internal-hashes.tsv.

| Artifact | Classification | Relevant findings |
| --- | --- | --- |
| com.blockpuzzle.us.ios_7.5.1_und3fined.ipa | Original-to-this-analysis repackaged/decrypted IPA | App metadata, embedded protected assets, signed resource manifest and remote module registry |
| ios751/type01-decoded/src/settings.7f91d.js | Decoded **embedded** IPA asset | Maps RewardHighValueAdHarvestTrait to ff35e, ZX294 to 9aa15, refactored version to db110 |
| ios751/remote-decoded/RewardHighValueAdHarvestTrait/index.ff35e.js | Decoded **later-retrieved remote CDN** module | High-value rewarded-ad classification, score threshold, death-algorithm selection and revive counter |
| ios751/remote-decoded/RewardHighValueAdHarvestV2Trait/index.677f6.js | Decoded **later-retrieved remote CDN** module | Install-age price tiers, optional recent completion requirement, death-algorithm condition |
| ios751/remote-decoded/ZX294_RewardHighValueAdHarvestTrait/index.9aa15.js | Decoded **later-retrieved remote CDN** module | 80%-to-record intervention, prioritized lethal algorithm and game-count interval |
| ios751/type01-decoded/assets/modelFeature/index.cc817.js | Decoded **embedded** IPA asset | Player/device/ad-revenue/gameplay feature calculations and supporting infrastructure |
| ios751/type01-decoded/assets/CTRefactorModelControlDieBoardTrait/index.b7dd1.js | Decoded **embedded** IPA asset | Board/death-control mechanism; not by itself proof of reward-value linkage |
| android1081/install/com.block.juggle.apk | **Embedded APK** in Android runtime archive | Android 10.8.1 application package |
| android1081/type01-capture/loader-return-0005-src_settings.cc5f1.js.bin | **Runtime loader-return capture** | Remote trait registration and content IDs |
| android1081/type01-capture/loader-return-0022-assets_class_index.ba28a.js.bin | **Runtime loader-return capture** | ADPushBackModelTrait / ADPushBackModelModifyTrait and other core classes |
| android1081/type01-capture/loader-return-0045-_data_user_0_com.block.juggle_files_gamecaches_AdPlusMinusStrategyTrait_179209600343333.js.bin | **Runtime loader-return capture** | Revive-rule changes and adjacent gameplay/advertising logic |

### Remote module caution

An embedded mapping, a CDN URL, a successful later download, and an instrumented execution are distinct facts. The ff35e and 9aa15 *plaintext implementations* were **not embedded directly** in the examined IPA. The currently examined iOS archive contains later retrieved modules; their byte hashes cannot, on their own, prove exact historical server responses at the IPA's original distribution date.

### Earlier Android 10.7.x captures

Earlier in the investigation, a separate Android runtime capture recovered RewardHighValueAdHarvestTrait as 15,616 bytes with SHA-256 **f94a5d54d7f6ab0af097f408bda09b091e7767b17749f8ba828b41b638b330ad**. The current Android 10.8.1 archive includes the 700f5 registry reference and runtime read evidence, but does **not** contain the 700f5 plaintext among its retained loader-return captures. Therefore the source map does not falsely label that earlier plaintext as a file in the 10.8.1 archive.

### Supplementary research tooling

The separately supplied `analysis.tar(1).gz` contains research scripts rather than application payloads. Its identity, review scope, capture assumptions, and Android version-loop limitations are recorded in [analysis-tooling.md](analysis-tooling.md). A [key-parameterized HEK decoder](../tools/hek/README.md) adapts its decoder implementation. Synthetic decoder tests do not add application captures or change the evidence classifications above.

### Integrity verification

Run the independent SHA-256 script described in tools/verify_hashes.py against private copies of the same three top-level artifacts. The reported checksums were recalculated from the uploaded archives before publication; matching them establishes file identity, **not** chain-of-custody beyond the investigator's possession.
