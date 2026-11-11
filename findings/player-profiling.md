# Player modeling and advertising features

The examined builds contain a feature-extraction architecture that can combine gameplay state, session history, device information, and advertising revenue signals.

## iOS modelFeature implementation

Source: ios751/type01-decoded/assets/modelFeature/index.cc817.js  
SHA-256: 1f8d2ce618cc454198210db8980b805406181cea63ce11db0817e86fbe5450ba

Examples of feature families found in the recovered implementation/documentation:

- country and device_model;
- rewarded-ad eCPM averages, maxima and revenue over configurable ranges;
- interstitial-ad eCPM and revenue;
- score, historical high score, clears, combinations, duration, and revive events;
- registration/install age and session-history-derived measures;
- model feature sets used by trait configuration or inference requests.

The names of feature calculators should not be conflated with proof that all were used by the particular rewarded-ad death rule. The **standard RewardHighValueAdHarvestTrait already demonstrates a direct relationship without requiring a learned model**: its visible condition compares rewarded-ad eCPM and checks ad completion history and a score threshold.

The feature registry nonetheless shows broader infrastructure that could support predictive player segmentation, LTV modeling, and remotely configured experiments. It is more precise to say **these features are available in the application** than to claim a particular model necessarily used all of them.

## Privacy and consumer-protection questions

Technically relevant issues to investigate include:

1. Whether the features are associated with persistent account/device identifiers.
2. Whether values are processed locally, transmitted to Hungry Studio, or provided to advertising partners.
3. Whether consent and disclosures describe the actual profiling and gameplay-control purposes.
4. Whether age-related or country-related features affect monetization or loss-selection decisions.
5. Whether model outputs are used in algorithm choice, revive eligibility, or ad presentation.

The code examined here does not establish a breach of any specific law. Jurisdiction, actual processing, disclosures, legal basis, and effects on players require separate analysis.

## How to confirm model influence

A complete model-inference claim requires tracing a named feature through the feature registry, vector construction, inference invocation or response, selected strategy, and final board outcome. Co-location of telemetry and an algorithm module is not by itself sufficient.
