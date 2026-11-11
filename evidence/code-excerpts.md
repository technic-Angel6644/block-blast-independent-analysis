# Minimal decisive excerpts and source locations

The complete decrypted commercial JavaScript is **not** reproduced here. This page lists the smallest excerpts needed to identify the relevant behavior, with an independently written explanation.

## Standard rewarded-ad death trigger

Source: ios751/remote-decoded/RewardHighValueAdHarvestTrait/index.ff35e.js  
SHA-256: 179bf50ae3c0c4a9bd5457281e4876faae728778f6181dbb0d3799b42ec70d61

The direct assignment at approximately source lines 245–249 is:

~~~javascript
if (this.shouldTriggerDeath()) {
    hs.algorithmBottomSequenceInfo.setAlgorithmBottomList([this.deathAlgorithm]);
}
~~~

The deathAlgorithm accessor at lines 100–103 resolves to the named offer type **ZHI_SI_TI**. The same branch records currentGameHasTriggeredDeath, and the revive-success handler at lines 215–222 increments the per-game trigger counter.

The decisive dependencies can be located without reproducing longer source blocks:

| Lines | Function | Relevant condition |
| --- | --- | --- |
| 107–110 | currentScoreThreshold | Historical high score plus scoreDeltaStep multiplied by trigger count + 1 |
| 262–267 | shouldTriggerDeath | Qualifying ad-completion history, current-game and score-state checks, and isTargetAdReady |
| 268–275 | canTrigger | Last three rewarded-ad results completed |
| 276–292 | isTargetAdReady / classifyLoadedRewardLevel | Ready rewarded ad and eCPM comparison (3.5× high threshold) |

## ZX294

Source: ios751/remote-decoded/ZX294_RewardHighValueAdHarvestTrait/index.9aa15.js  
SHA-256: 4c10cea979bf066babaa4fd0306b2a8b952299abac0a258d595194bc34d376d6

See approximately lines 191–215. The initial continuousDeathActive state is entered between 80% and 100% of a prior high score, contingent on a valuable ready rewarded ad and a game-count interval. While active, the code *prioritizes* ZHI_SI_TI.

## Android interstitial controls

Source: android1081/type01-capture/loader-return-0022-assets_class_index.ba28a.js.bin  
SHA-256: 56f3d70a525a24aab6404e00dcb0dba6d8e400a42505ac855fe9beb2273eb657

See the ADPushBackModelModifyTrait and ADPushBackModelTrait sections, roughly source lines 1294–1510. Both compare interstitial-ad eCPM against earlier eCPM state before choosing between easier, harder, and optionally lethal strategies.

**Interpretation limit:** these code excerpts identify decision requests and options, not experimentally measured activation across the game's population.
