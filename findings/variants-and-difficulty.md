# Variants and additional difficulty controls

These are **separate implementations**, not interchangeable names for one algorithm. Their co-existence in a registry or on a CDN does not establish that all were enabled for the same player.

## RewardHighValueAdHarvestV2Trait (recovered iOS remote bundle)

Source: ios751/remote-decoded/RewardHighValueAdHarvestV2Trait/index.677f6.js  
SHA-256: 18058c2fe83077c947fd199c292d56e312c8d6167d73b7a14d95fe640229bd90

The V2 code uses installation-age segments when classifying a valuable rewarded ad:

| Installation-age segment | High-price multiplier |
| --- | ---: |
| New | 3.2× |
| Middle | 2.7× |
| Older | 3.0× |

It again evaluates a personalized score threshold and can choose ZHI_SI_TI through the bottom-offer pathway. The default scoreDeltaStep is **1,000** rather than the standard trait's 500.

**Important exception:** V2 makes the requirement for recent non-abandoned ads configurable, and its default value for requireRecentNoEscape is false. It would be inaccurate to generalize the standard module's three-successful-ads prerequisite to every V2 configuration.

## ZX294_RewardHighValueAdHarvestTrait (recovered iOS remote bundle)

Source: ios751/remote-decoded/ZX294_RewardHighValueAdHarvestTrait/index.9aa15.js  
SHA-256: 4c10cea979bf066babaa4fd0306b2a8b952299abac0a258d595194bc34d376d6

This implementation uses a **different intervention window**:

- HIGH_PRICE_MULTIPLIER = 3.5.
- HIGH_SCORE_PERCENT = 0.8.
- GAME_COUNT_THRESHOLD = 10.
- The initial trigger requires a positive previous record, a current score at least 80% but below 100% of that record, a sufficiently valuable ready rewarded ad, and a game-count interval check.
- Once continuousDeathActive is set, subsequent qualifying algorithm-condition events insert ZHI_SI_TI at the front of the priority list.
- The flag is cleared if the current score reaches the saved previous record.

**Mechanism distinction:** This is a priority-list insertion, not the standard trait's replacement of the bottom-offer algorithm list. It can increase the chance of a lethal offer without by itself proving that the final board actually used one.

The phrase "near a high score" is more precise for ZX294 than "after breaking a high score." Note that the code also tracks whether an actual algorithm execution succeeded.

## Interstitial-ad-related controls in Android 10.8.1

Source: android1081/type01-capture/loader-return-0022-assets_class_index.ba28a.js.bin  
SHA-256: 56f3d70a525a24aab6404e00dcb0dba6d8e400a42505ac855fe9beb2273eb657

The class_index includes **ADPushBackModelTrait** and **ADPushBackModelModifyTrait**. Both evaluate full-screen *interstitial* ad eCPM and gameplay time. Their implementations can, subject to conditions and configuration, select or prioritize ZHI_SI_TI.

- The non-modified version defaults to choosing a hard algorithm (KUN_NAN_TI) rather than the lethal one unless isHard is disabled.
- The modified version has a configurable hardPer probability, with **default 0**, so its hard/lethal priority path is not active under that default.
- Depending on its roundPlus state, the modified version can prioritize clearing/easier algorithms instead.

This is a **configurable capability**, not proof that ordinary Android players were regularly given ad-value-triggered lethal offers by these two specific classes.

## Countervailing protections

The Android capture also contains traits that can make gameplay easier or replace lethal strategies, including **DeadlyToHardTrait**, **ClassNewDeathOptimizeTrait**, and **ConsecutiveLossRecoveryTrait**.

The presence of protection code does not negate the existence of monetization-linked death-selection code. It does mean the final outcome must be reconstructed at the algorithm-resolution stage, rather than inferred from a single trait's proposed selection.
