# Block Blast: independent analysis of advertising-linked gameplay controls

This repository documents an independent, AI-assisted **replication and extension** of reverse-engineering findings concerning **Block Blast!**, with a focus on algorithmic piece selection, advertising value, rewarded revives, and player-level modeling. The initial public investigation was published by **Ayo Omolewa (Ayoships)** on 15 October 2026: [original report](https://ayoships.com/breakdowns/block-blast). This project does not claim to have discovered the mechanism first.

**Main result:** Recovered JavaScript includes a path that, when its conditions are satisfied, selects the game's **ZHI_SI_TI** (致死题; approximately "lethal puzzle") offer algorithm based partly on the value of a loaded rewarded advertisement. This is not merely an ad event being logged next to a difficulty event: the advertised value participates in the gameplay decision. Other recovered traits use different criteria to prioritize the same algorithm.

**Scope warning:** Source-code presence does not establish that a remotely configured trait was enabled for every player, that each selection survived subsequent overrides, or the frequency of resulting impossible boards. No population-wide rate, revenue impact, or legal violation is established here.

## Findings at a glance

| Finding | Evidence | Important qualification |
| --- | --- | --- |
| Rewarded-ad value can participate in death-algorithm selection | A recovered RewardHighValueAdHarvestTrait tests score, recent completed rewarded ads, and current ad eCPM before switching the bottom-offer algorithm to ZHI_SI_TI | Remote activation and final-board outcome require separate verification |
| The trigger can recur after a revive | The module increments a per-game trigger counter after a successful revive and raises the next score threshold | Exact defaults can be overridden by trait properties |
| Alternative variants exist | V2 adjusts high-ad-value thresholds by installation age; ZX294 can prioritize ZHI_SI_TI between 80% and 100% of a previous record | A remote reference or downloadable module is not evidence of universal deployment |
| Other ad-value paths exist | Android 10.8.1 includes interstitial-eCPM-driven difficulty/offer modules | The lethal paths are configurable and need not be the default |
| Revive decisions can be modified | Android 10.8.1 contains an AdPlusMinusStrategyTrait that alters revive eligibility under configurable conditions | Shipped capability is not a measurement of actual activation |
| Modeling infrastructure spans platforms | iOS and Android contain modules/definitions for player and advertising features, difficulty, and experiments | Feature availability alone does not prove every feature influences every decision |

## Evidence and sources

The analysis used three locally retained source artifacts (not distributed in this repository):

- An examined iOS IPA labeled **Block Blast! 7.5.1 / build 7512**, bundle **com.blockpuzzle.us.ios**.
- An iOS recovery archive containing decoded embedded assets and separately retrieved remote JavaScript modules.
- An Android **10.8.1** runtime/recovery archive containing APK splits, loader return captures, and instrumentation logs.

See [evidence/hashes.sha256](evidence/hashes.sha256), [evidence/internal-hashes.tsv](evidence/internal-hashes.tsv), [evidence/source-map.md](evidence/source-map.md), [limited decisive excerpts](evidence/code-excerpts.md), and [IPA integrity checks](evidence/signature-verification.md) for source names, sizes, SHA-256 checksums, and classifications.

**Provenance distinction:** The iOS IPA embeds the *registry references* for reward-harvest modules. The recovered implementations themselves were fetched from remotely hosted resources during the later investigation. The IPA's 7.5.1 version metadata must not be used by itself to date those CDN payloads to the original release.

## Read the analysis

- [Rewarded-ad-conditioned death selection](findings/rewarded-ad-death.md)
- [Lethal-piece selection versus actual impossible hands](findings/lethal-piece-algorithms.md)
- [Variants and additional difficulty controls](findings/variants-and-difficulty.md)
- [Revive control and experimental systems](findings/revives-and-experiments.md)
- [Player modeling and advertising features](findings/player-profiling.md)
- [iOS / Android comparison](findings/cross-platform-comparison.md)
- [Methodology](methodology.md), [limitations](limitations.md), [provenance notes](evidence/provenance.md), and [original references](references.md)

## What this publication does and does not say

The code-level finding is that the product contains rules that can condition *selection* of an intentionally lethal piece-generation strategy on monetization-related state. This warrants scrutiny, and it is different from ordinary score-only difficulty adjustment.

The source captures **do not**, on their own, prove: which configuration was assigned to any particular ordinary player; how often a chosen offer was finally used; the company's stated rationale; illegality or criminal conduct; or that all tested remote modules were simultaneously active.

The underlying IPAs/APKs, decrypted proprietary source, and raw logs are **not distributed** with this public repository. This repository contains independently written descriptions, limited source identifiers, hashes, and checking tools; it is not a mirror of the game's source code.

## Reproducibility

A researcher with a lawfully obtained copy of the relevant artifacts can compare SHA-256 values using [tools/verify_hashes.py](tools/verify_hashes.py) and then locate the methods listed in the source map. The method descriptions deliberately distinguish **embedded files**, **live runtime captures**, and **later-retrieved CDN content**. Optional [Ghidra exploration scripts](tools/ghidra/README.md) are retained as supplemental methodology, not primary evidence.

A [HEK decoder and synthetic tests](tools/hek/README.md) provide the byte-format implementation with a caller-supplied key. The [supplementary Daybreak tooling review](evidence/analysis-tooling.md) records the supplied scripts' hashes, capture limitations, and intended Android version loop. The new tests use synthetic inputs; no additional application versions or gameplay outcomes were verified in that update.

This investigation was assisted by ChatGPT/Daybreak for reverse engineering and inspection. Codex assisted the supplementary script review, synthetic decoder validation, and repository documentation. Reported gameplay findings were cross-checked against the files listed in the evidence map during the earlier investigation. The original [Ayoships investigation](https://ayoships.com/breakdowns/block-blast) motivated this independently reproduced analysis; it is not a claim of first discovery. See [references](references.md).

## Attribution and contact

This is a separate reproduction of earlier Block Blast reverse-engineering allegations. The original researcher and any directly consulted public reports should be credited in a release revision with permanent, verified citations.

If correcting an error, open a GitHub issue with the relevant source path, checksum, expected behavior, and reproduction details. Please do not post copyrighted game bundles or player-identifying logs in issues.

**Status:** initial technical publication, 11 November 2026. Findings and limitations may be refined as additional runtime evidence becomes available.
