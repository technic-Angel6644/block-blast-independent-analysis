# Limitations and interpretation guide

This is a study of **implemented and captured client-side mechanisms**, not a survey of all players.

## Established

- The recovered standard reward-harvest source contains a direct conditional link between rewarded-ad economic value and ZHI_SI_TI bottom-offer selection.
- The recovered ZX294 source has a different, pre-high-score interval and priority-list design.
- The Android 10.8.1 runtime class bundle contains configurable interstitial-eCPM difficulty/offer paths.
- A recovered revive-control module can modify normal revive results under conditions.
- The examined app packages and recovery archives have reproducible SHA-256 checksums.
- Four retained evaluator captures of the standard Android reward-harvest source are byte-identical; independent decoding of its encrypted resource reproduces those bytes.
- Three retained Android APKs identify as 10.7.3, 10.7.4 and 10.8.0; their embedded settings decode exactly to corresponding early evaluator captures.
- A retained client configuration names RewardHighValueAdHarvest with scoreDeltaStep 1,000. This establishes stored configuration, not completion of the gameplay branch.

## Not established by the artifacts alone

- The percentage of users receiving any particular feature, variant or server-assigned experiment.
- Whether the chosen algorithm survived all competing rules and produced an impossible final offer in each case.
- Any population-wide frequency of deliberate losses, increase in ad impressions, or revenue attributable to that behavior.
- That CDN modules downloaded later were present or activated when a particular historical IPA version first shipped.
- Whether each model feature was used for a specific inference in a particular player session.
- Developer intent outside the intent implied by the mechanics' actual conditionals and names.
- Any conclusion about unlawful conduct in a specific jurisdiction.
- Successful testing of every Android version named in the supplementary scripts. The additional recovery archive has no 10.8.2 or 10.8.5 run; its 10.7.2 package label also lacks APK/package-dump confirmation.
- That cached configuration is an authenticated server response, that its feature was instantiated with those properties, or that it caused an observed final hand.
- A trustworthy historical distribution or publication date established solely by the supplied session's timestamps.

## Supplementary-tooling scope

The [Daybreak script review](evidence/analysis-tooling.md) adds methodology details. Fixed offsets, assumed register/string layouts, filtering and dump limits constrain the collectors; its fingerprint check is at a different location from the evaluator hook. Some exploratory scripts modify the process, and source presence does not show whether they were used for a particular capture. The [public HEK decoder](tools/hek/README.md) passed synthetic tests and now also matches actual retained Android assets as described in [the multi-version verification](findings/android-multiversion.md). This update inspects those retained artifacts rather than newly running the application on a device. The supplied session is history from the same investigation, not an additional independent replication.

## Language discipline

- Prefer **"contains code that can select a lethal-piece algorithm"** over **"every player is forced to lose"**.
- Prefer **"rewarded-ad eCPM is part of the trigger condition"** over **"all advertising revenue is used to rig every game"**.
- Prefer **"downloaded later from the app's CDN"** over **"embedded in the IPA"** for remote implementations.
- Prefer **"independently reproduced the reported code paths"** over **"independently discovered the behavior"**.

A future controlled runtime study could substantially narrow these uncertainties.
