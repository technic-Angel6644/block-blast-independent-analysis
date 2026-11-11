# Rewarded-ad-conditioned death selection

## Summary

A recovered iOS CDN bundle named **RewardHighValueAdHarvestTrait** contains a direct connection between rewarded-ad economics and bottom-piece selection in Block Blast. The source in the provided recovery archive is:

- ios751/remote-decoded/RewardHighValueAdHarvestTrait/index.ff35e.js
- SHA-256: 179bf50ae3c0c4a9bd5457281e4876faae728778f6181dbb0d3799b42ec70d61

The bundle is *not* embedded as plaintext in the IPA. An embedded settings registry references its bundle ID, **ff35e**; the implementation was obtained separately from the application's remote-module infrastructure. Treat the code, the local registry reference, and evidence of historical distribution as distinct items.

## Conditions in the recovered implementation

The relevant method bodies in the recovered source are:

| Approximate lines | Method/field | Observation |
| --- | --- | --- |
| 63–67 | Constants | HIGH_PRICE_MULTIPLIER = 3.5; MEDIUM_PRICE_MULTIPLIER = 1.5; requires three rewarded-ad displays and three successful recent outcomes |
| 92–113 | scoreDeltaStep / currentScoreThreshold | Default increment of 500; threshold is stored historical high score plus increment multiplied by previous triggers + 1 |
| 215–223 | onReviveSuccess | Increments the per-game trigger count and clears the death marker after qualifying revive success |
| 245–251 | onBottomOfferAlgo | If shouldTriggerDeath evaluates true, replaces the bottom-offer algorithm list with a one-element list containing deathAlgorithm; records a triggered-death marker |
| 262–275 | shouldTriggerDeath / canTrigger | Requires qualifying recent ad history, current game, no prior active trigger, minimum score and a target ad ready |
| 276–292 | isTargetAdReady / classifyLoadedRewardLevel | Requires a ready rewarded ad; classifies it using current loaded eCPM relative to previous shown rewarded-ad eCPM |
| 324–340 | storageData | Persists rewarded-ad history, last eCPM, current high-score baseline and death-trigger state |

The deathAlgorithm accessor resolves to **OFFER_TYPE.ZHI_SI_TI**.

Simplified, independently written pseudocode (not a copy of the game's implementation):

~~~text
eligible := enough prior rewarded-ad displays
            AND last three rewarded-ad results completed
high_value_ad := rewarded ad ready
                 AND current eCPM >= 3.5 * last shown rewarded-ad eCPM
score_target := historical_high_score + 500 * (previous_triggers + 1)

IF eligible AND high_value_ad AND score >= score_target
   AND not already triggered in this game:
    select ZHI_SI_TI as the bottom-offer algorithm
    mark triggered death

IF qualifying revive succeeds:
    previous_triggers += 1
    clear triggered death
~~~

The 500-point value is a **default**, not an immutable rule; the trait reads configurable properties. The last-ad comparison requires a valid positive reference value. Selection may also be vetoed or replaced later in the game's algorithm pipeline.

## What the implementation establishes

- Monetization is an actual input to piece-selection logic, rather than simply a metric collected for reporting.
- The design distinguishes a relatively valuable available rewarded ad from ordinary ad availability.
- The same module tracks successful rewarded-ad completion and the intervention's per-game trigger state.
- A successful qualifying revive permits a later trigger at a higher score threshold.

## What it does not establish on its own

- That a particular server-side experiment enabled the trait for every player.
- That the final pieces displayed to users were always the selected death algorithm.
- The rate at which such selections occurred in normal play.
- Whether the original App Store build dated by the IPA metadata received the same remote JavaScript at release.
- Any specific legal finding, loss amount, or intent statement beyond what the code's conditions demonstrate.

The original code path is sufficiently specific to justify controlled runtime replication. Instrument both **the selected algorithm** and **the final three pieces**, including later overrides. Preserve the active configuration, app build, CDN response hashes, ad state and score state during any such test.
