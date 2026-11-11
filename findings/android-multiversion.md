# Android multi-version capture verification

The additional private archive, `android10.tar(1).gz`, supplies direct evidence for an Android reward-harvest implementation that was previously represented in this report by an earlier-session hash. It contains four labeled runs, three sets of installation APKs, retained evaluator buffers, encrypted remote/cache resources, and local application state.

This update inspects retained artifacts. It does not rerun the application on a device or observe a new gameplay outcome.

## Source identity and coverage

The archive is **526,314,784 bytes**, SHA-256 **21dbb20735d0ff5abd00827cc2d44efaad4cff5c313703d070f1c1d3ab9de94f**. Its 1,311 regular files include a nested application-data backup. Selected member hashes are in [internal-hashes.tsv](../evidence/internal-hashes.tsv).

| Labeled run | Version evidence retained here | Evaluator buffers | Standard trait capture, relative to run directory |
| --- | --- | ---: | --- |
| 10.7.2 | Directory/session labeling; no installation APK or package-version dump retained in this archive | 143 | `evaluator-sources/capture-104.bin` |
| 10.7.3 | Base APK manifest: `com.block.juggle`, version 10.7.3, versionCode **10732** | 142 | `evaluator-sources/capture-100.bin` |
| 10.7.4 | Base APK manifest and retained package dump: version 10.7.4, versionCode **10740** | 165 | `evaluator-sources/capture-113.bin` |
| 10.8.0 | Base APK manifest and retained package dump: version 10.8.0, versionCode **10800** | 165 | `evaluator-sources-retry/capture-126.bin` |

All 15 retained APK splits match their supplied installation checksums. All 14 files listed in the 10.7.2 first-run checksum manifest also match. These are internal consistency checks, not independent Google Play distribution or signing-certificate verification. The 10.7.2 label has weaker version provenance than the three retained base APKs.

All **615** retained binary evaluator buffers have accompanying metadata whose declared length matches the saved byte count. These remain filtered snapshots, with duplicate payloads; they are not exhaustive inventories or proof that every captured trait executed its gameplay branch.

Researchers with private copies can verify both new top-level archives and the selected Android members without executing application code:

```bash
python3 tools/verify_hashes.py --root /path/to/private/evidence \
  --archive 'android10.tar(1).gz' --archive 15.tar.gz
```

The 10.7.3 logs retain an initial spawn timeout followed by an attach capture; the 10.8.0 logs similarly retain an unsuccessful initial attempt and a later retry. The successful retained buffers, rather than an assumption that every attempt succeeded, support the comparisons here.

## Identical standard reward-harvest source in four runs

The four captures listed above are each **15,616 bytes** and are byte-identical:

`f94a5d54d7f6ab0af097f408bda09b091e7767b17749f8ba828b41b638b330ad`

They contain the standard `RewardHighValueAdHarvestTrait` implementation, including the rewarded-ad eCPM comparison, recent completion requirement, personalized score threshold, bottom-offer mutation to `ZHI_SI_TI`, and revive-trigger counter described in [the main finding](rewarded-ad-death.md).

The source is consequently available as retained evaluator input in multiple labeled runs, rather than only as a module name in a registry. A capture at the evaluator boundary still does not establish that `shouldTriggerDeath()` later returned true or that a lethal hand reached the player.

## Independent decoding against the retained bytes

The [public HEK decoder](../tools/hek/README.md), using a privately supplied key, was applied to the actual retained assets:

| Source | Decoded result | Independent comparison |
| --- | ---: | --- |
| 10.7.3 APK: `assets/src/settings.e15ff.js` | 276,600 bytes | Exact match to `android1073/evaluator-sources/capture-004.bin` |
| 10.7.4 APK: `assets/src/settings.f54ce.js` | 280,633 bytes | Exact match to `android1074/evaluator-sources/capture-004.bin` |
| 10.8.0 APK: `assets/src/settings.ff4eb.js` | 291,653 bytes | Exact match to `android1080/evaluator-sources-retry/capture-004.bin` |
| `android1072/remote/RewardHighValueAdHarvestTrait/index.700f5.js` | 15,616 bytes | Exact match to the retained decoded source and all four standard-trait captures |
| `android1072/remote/RewardHighValueAdHarvestTrait/config.700f5.json` | 247 bytes | Same parsed JSON object as the retained decoded configuration |

The three embedded settings files all reference `RewardHighValueAdHarvestTrait` as **700f5**. The encrypted remote JavaScript is 3,544 bytes, SHA-256 **dec91aa4001f651a74bf101d512587b9a364cb71ea2a81a9cc9dbbcd2444b477**. It also matches the separately retained encrypted device-cache copy byte-for-byte.

The bundle's Type 03 `config.700f5.json` describes Cocos resource metadata. It is **not** the player-specific feature configuration discussed below and does not by itself show that the trait was enabled.

## Embedded settings versus later runtime content

Each of the three APKs has different embedded settings bytes, independently matched to its early capture. Later settings captures in all four runs are instead **298,465 bytes**, with SHA-256 **95c4ca5c2ec1f4b40ff843cc79706e1a03908911df42ca699124984da7f83658**. That is also the settings hash previously reported for the separate Android 10.8.1 archive.

This distinction matters: different client packages can reach common later runtime resources. Finding the same trait payload during sessions using different APK versions does not date that remote payload to each APK's original release, or show that the plaintext was embedded in those APKs.

The 10.7.2 first-run files also retain a patch manifest labeled `1.5.16.0.0` and a `baseV` value of `1.4.6.0.0`. These are patch-system values, not independently verified Android package versions.

## A retained client configuration names the feature

The 10.7.2 first-run snapshot includes `databases/jsb.sqlite` and its WAL/SHM files. A read-only connection to a working copy, with the WAL present, passed SQLite's integrity check. The following three local-storage entries contain the same relevant feature entry:

- `__loginDataDefault__`
- `block-blast-server_experiment_config`
- `block-blast-pure_server_experiment_config`

At `experimentDataMap.defaultLayer.configData.features[208]`, the retained entry specifies:

| Field | Retained value |
| --- | --- |
| `feature_key` | `RewardHighValueAdHarvest` |
| `scoreDeltaStep` | **1,000** |
| `minGameDurationSeconds` | **420** |

This is evidence of a named feature configuration in retained client state, beyond a downloadable module alone. It is not a separately authenticated network response, a record of trait instantiation, or a trace of the final algorithm decision. The snapshot is not known to be atomic with the evaluator captures.

The 1,000-point setting differs from the source's 500-point default, illustrating why the default must not be presented as a universal live value. The 420-second setting must also not be treated as a proven trigger gate: the examined standard `shouldTriggerDeath()` / `canTrigger()` path does not read that duration property. No corresponding `rewardHighValueAdHarvestTraitData` storage entry was located in this snapshot; it does not provide a persisted successful death-trigger event.

Only the relevant feature name and parameters are reported. Device/account identifiers, server keys, request traces, and the raw database are not published.

## Precise relationship to the earlier iOS source hash

The supplied [Codex session record](../evidence/session-review.md) reports a one-line difference between the Android standard source and the previously examined iOS source: `normalizeGpAdEcpm` multiplies a valid positive input by 1,000 on Android, while the iOS form returns that input unchanged.

This relationship was checked again using the actual Android bytes. Changing only that normalization expression produces **15,610 bytes** with SHA-256 **179bf50ae3c0c4a9bd5457281e4876faae728778f6181dbb0d3799b42ec70d61**, exactly matching the iOS plaintext hash already published in this repository.

That verifies the precise source relationship to the earlier iOS hash. It is not a new acquisition or authentication of an iOS CDN response. The advertising-conditioned decision logic is otherwise byte-identical under that single-expression comparison.

## Remaining limits

The new archive supplies no 10.8.2 or 10.8.5 run, despite those versions appearing in the exploratory test-loop source. Android 10.8.1 remains covered by the separate, earlier archive; its missing 700f5 plaintext is not retroactively supplied by captures from another run.

These results strengthen the central code finding and its cross-version corroboration. Active final-board decisions, ordinary-user rollout rates, and revenue effects still require different evidence.
