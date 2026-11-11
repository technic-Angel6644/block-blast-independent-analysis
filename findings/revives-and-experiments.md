# Revive controls and experimental infrastructure

## AdPlusMinusStrategyTrait: Android 10.8.1 runtime capture

Source: android1081/type01-capture/loader-return-0045-_data_user_0_com.block.juggle_files_gamecaches_AdPlusMinusStrategyTrait_179209600343333.js.bin  
SHA-256: 72796c763f40fb96599672ab21e4ca0137b6fc77cac07453ca626ed692b06be7

The recovered module contains configurable logic surrounding revive availability, previous high scores, recent performance, prior revive usage, and advertising display. Some paths can alter an otherwise normal revive decision.

This is noteworthy because gameplay difficulty and revive opportunities need not be treated as independent. The available source shows that revive eligibility itself can be modified using player state.

Some recovered branches also adjust post-revive gameplay, including relief from harder algorithms; this complicates simple narratives that the game only ever increases difficulty.

## Multi-armed-bandit and UCB systems

The examined iOS IPA's decoded embedded code includes trait families for:

- MABGameLifecycleHandlerTrait;
- CTRefactorUCBBlockPoolStrategyTrait;
- experimental block-selection and revive-related modules.

A *multi-armed bandit* chooses among candidate experimental policies based on feedback; *UCB* refers to an upper-confidence-bound selection strategy. Their presence makes experimentation plausible but does not establish which metric an individual policy optimizes. In particular, MABGameLifecycleHandlerTrait itself is primarily lifecycle infrastructure rather than proof of a specific outcome policy.

Earlier Android runtime findings supplied in the investigation describe a captured MABXiBaiTrait that tracked revive show/success rates and death-algorithm executions. That earlier module is **not independently verified from the Android 10.8.1 archive examined for this report**, so the associated result is recorded as prior-session evidence rather than presented as a fresh cross-version confirmation.

## Required next experiment

To establish real-world behavioral impact, capture for one test run:

1. The version, exact fetched remote modules, active experiment assignment and trait properties.
2. The board, offer state, score, recent ad history, current loaded ad eCPM, and high-score baseline.
3. Any request to select ZHI_SI_TI.
4. Which algorithm actually wins conflict resolution, and the final offered three pieces.
5. Whether the final offer is solvable by exhaustive enumeration.
6. Whether a revive was displayed, completed, and led to the next trigger.

Only with that sequence can code-level capability be reliably converted into a statement about an observed user-facing event.
