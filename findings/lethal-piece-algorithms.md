# Lethal-piece algorithms and what selection proves

The game uses a named offer type **ZHI_SI_TI** (致死题, roughly "lethal puzzle"), referenced by its strategy and bottom-offer controllers. Different traits can request or prioritize this algorithm under different conditions.

## Three distinct stages

**1. Trigger evaluation.** A trait such as RewardHighValueAdHarvestTrait, ZX294, or ADPushBackModel examines gameplay and/or advertising state.

**2. Algorithm selection or prioritization.** A trait changes the algorithm request:

- Standard RewardHighValueAdHarvestTrait replaces the **bottom-offer algorithm list**.
- ZX294 prepends ZHI_SI_TI to an **algorithm priority list**.
- ADPushBackModelTrait can replace the **algorithm selection list** after an interstitial eCPM test.

These operations are not semantically equivalent. Reordering priorities can fail to determine the final selected algorithm if another rule has precedence.

**3. Final piece generation.** The game resolves strategy conflicts, generates its three offered pieces and displays the hand. The final offer can be checked for solvability by enumerating placements and clearing rules.

A source line requesting ZHI_SI_TI is direct proof of an implemented *selection* mechanism. It is not, by itself, a complete runtime trace proving that the player was dealt an unwinnable hand.

## What a robust reproduction should capture

For one observed attempt:

1. Board representation before dealing the hand.
2. Active trait identity, its configuration and triggering input values.
3. Candidate algorithm(s) and any priority/fallback structures.
4. The final accepted algorithm ID and source trait, after all overrides.
5. The exact three pieces returned by the generator.
6. Whether any legal ordering and placements can place all three (with row and column clears).
7. Whether revive UI was shown, accepted, and rewarded ad completed.

If the final three-piece offer has **zero valid arrangements**, that is stronger evidence than a name that translates to "lethal puzzle." For comparison, the original researcher [published an example of exhaustive-solver testing](https://ayoships.com/breakdowns/block-blast). This repository does not claim an independent end-to-end solvability test from the 10.8.1 source capture alone.

## Why other traits matter

The examined Android code also contains **DeadlyToHardTrait**, **ClassNewDeathOptimizeTrait** and **ConsecutiveLossRecoveryTrait**, which can sometimes soften difficulty or prevent particular lethal results. Such mechanisms may coexist with ad-conditioned lethal requests. The analysis must examine conflict resolution and final output rather than treating each trait in isolation.
