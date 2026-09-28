# Adaptive pairs: coverage gain and the next selection question

September 28, 2026. Review of the [frozen protocol](protocol.json), baseline `3ffb0c7b5edb75a81e60de0ceed58f5a40edae7b`. There are eight runners `{0,1,4,5,6,7,11,V}`, with positive integer V outside `{1,4,5,6,7,11}`, reference 0, and threshold 1/8. Only runner 11 has variable initial phase theta. General implications below remain **HYPOTHESIS / proof candidates** under [CLAIM_STATUS.md](../../CLAIM_STATUS.md). This is an internal prior-coverage and representation audit, with material AI reasoning and writing; no external literature or novelty claim is made.

**The adaptive pair adds all-phase robustness for every admissible V, using the previously available common-start witness and its reflection. It adds no new common-start coverage to this family.** The useful change is both a stronger phase quantifier and a direct arithmetic selection rule that avoids full safe-set reconstruction. The supplied argument is collected in [ADAPTIVE_REFLECTED_PAIR_2026_09_28.md](../../notes/ADAPTIVE_REFLECTED_PAIR_2026_09_28.md).

## 1. The exact difference from earlier coverage

[VARIABLE_SPEED_FAMILY.md](../../notes/VARIABLE_SPEED_FAMILY.md), September 24, already supplies

\[
t(V)=\begin{cases}
1/8,&8\nmid V,\\
17/56,&8\mid V\text{ and }56\nmid V,\\
17/56+1/(8V),&56\mid V.
\end{cases}
\]

Its result is `for every V, t(V) is safe at theta=0`. The adaptive claim is

\[
\forall V\ \forall\theta\ \exists s\in\{t(V),1-t(V)\}:
\min_{v\in\{1,4,5,6,7,V\}}\|vs\|\ge1/8,
\qquad \|11s+\theta\|\ge1/8.
\]

The pair depends on V and is selected before theta is known. The winning member may depend on theta; both need not work at a given phase. In particular this is not a single time that works for every phase.

The old witness checks unchanged safety at t(V). Integer reflection gives equal unchanged distances at 1−t(V). The genuinely additional check is runner 11's two-phase separation `d=||22t(V)||`, not common-start feasibility alone:

| Branch | Unchanged distance cap c at both times | Selected-runner separation d |
| --- | ---: | ---: |
| 8 does not divide V | 1/8 | 1/4 |
| 8 divides V, 56 does not | 1/8 | 9/28 |
| 56 divides V | 1/8 | `9/28−11/(4V)`, at least 61/224 |

The two-time inequality gives `max(||11t+theta||,||11(1−t)+theta||)>=d/2`. Each row has d/2>=c. Since an unchanged runner caps both times at c, the full best-of-pair distance is **identically 1/8 at every theta in every branch**. The unbounded conclusion rests on the three symbolic branches and their inequalities, not the eight prescribed finite diagnostic inputs.

[TIME_TEMPLATE_CLASSIFICATION_2026_09_27.md](../../notes/TIME_TEMPLATE_CLASSIFICATION_2026_09_27.md) previously certified every phase on 117 of 120 fixed-time coefficient classes. Its failures were `V=0,32,88 mod120`. The adaptive pair covers every admissible integer in those three classes as well. This is an algebraic extension of the phase-robust certificate, not an extrapolation of the prior diagnostics at V=120,32,88.

| Existing or current certificate | Coverage and retained advantage |
| --- | --- |
| Old adaptive single time | All admissible V, common start |
| Old four fixed times | Every phase on 117/120 coefficient classes; distance 2/15 on 96 classes |
| New adaptive reflected pair | Every phase for all admissible V; pair distance exactly 1/8 |
| Old fixed-window tail | Positive common-start duration for every V>=29 |

The adaptive pair closes a coverage gap but should not replace the old fifteenth pair when its stronger 2/15 separation is useful. The old common-start tail already covers every integer in each failed fixed-menu class strictly. Its containment of runner 11's blocker is phase-specific and cannot establish the new all-phase statement by itself.

Only this selected reference and this fixed family are treated. Arbitrary initial phases for all runners, other selected speeds, arbitrary seven-speed inputs, and general Lonely Runner do not follow.

## 2. What the small certificate retains and discards

The certificate retains two actual times, unchanged distance caps, and the selected runner's phase separation. Those data suffice for its all-phase threshold assertion. It does not recover the complete unchanged-safe set A, projection P, phase multiplicities, complete surviving time set, exact duration, maximum separation over all times, or the number and location of isolated contacts.

An equality cap at the selected times also does not decide strictness elsewhere or immediately beside them. Opposing entry and exit contacts can isolate a time; contacts all moving into safety on one side can admit a strict interval when the remaining runners have slack. That distinction requires the directed endpoint checks specified in this round's protocol, beyond the scalar c,d summary. The old V=13 control must remain contact-only at common start even though it is feasible at every runner-11 phase and strict at every nonzero phase.

The reviewed directed argument supplies `D_V(theta)>=1/(56V)>0` whenever 8 divides V, for every theta. Choose the pair member with larger **runner-11 distance**, then move inward: right from t(V), left from its reflection. Choosing arbitrarily between equal full minima would discard the selected runner's needed slack. This closes all-phase strictness throughout all three former failed residue classes, using the new uniform argument rather than the three old projections. When 8 does not divide V, the pair's opposing unchanged contacts remain locally isolated; no full-configuration strictness classification follows from that fact.

Where a directed argument supplies a positive neighborhood, its radius is a sufficient duration bound, not the complete duration. Speed-dependent time widths may shrink even when phase separation has a fixed positive reserve. The existence of an efficiently checked pair does not make omitted duration or topology data redundant for other questions.

The earlier [two-time completeness argument](../../notes/TWO_TIME_CERTIFICATES_2026_09_27.md) is conditional on one-runner phase robustness. The present construction supplies robustness and finds a pair in this restricted family. It does not turn conditional completeness into an arbitrary-speed selection theorem. Robustness to all phases remains a stronger auxiliary target than the original common-start conjecture.

## 3. Why adaptation matters

The finite rational-menu obstruction was already explicit in the September 24 variable-speed note. For any finite list of rational times independent of V, a sufficiently large common multiple of their reduced denominators is an admissible speed colliding at every time in that list. No such list can certify this family for all V, even at common start.

The adaptive rule escapes the obstruction in its third branch by moving the time by `1/(8V)`, placing runner V exactly at safe threshold. It uses a bounded number of arithmetic operations; increasing integer bit lengths still affect cost. The fixed family supplies the safe interval `[17/56,5/16]` in advance. No enumeration of V's meetings or construction of the full joint safe set is required. These are the concrete algorithmic advantages, without a claim of optimal complexity or new underlying existence coverage.

## 4. One bounded next task

After this family is closed, return to the preserved [small-gcd selection priority](../../notes/SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md): **prepare and challenge one arithmetic selection rule with a declared input and cost contract**. First audit the inputs needed to choose one opening and one local overlap certificate before inspecting the full allowed set; freeze that contract before committing to a rule. A concrete diagnostic budget is one selected core opening, its four single-blocking durations, one selected pair overlap, and one directly checked endpoint if the duration certificate fails. The selector must identify the opening and pair from its declared speed arithmetic before seeing their eventual joint allowed set. Record endpoint/interval enumeration costs and integer bit costs separately from the number of reported quantities.

The intended gain must be a proved sufficient speed condition or lower certificate-evaluation cost, rather than another exact reconstruction or a stronger constant in the current family.

Use only three already recorded diagnostic requirements:

| Existing control | What the proposed rule must confront |
| --- | --- |
| Core `{1,4,5}`, extras `{56,113,64,72}` | Exact local single durations together with the 56/113 overlap certify positivity; either correction alone was insufficient |
| Core `{1,3,5}`, the same four extras, opening `[17/40,23/40]` | The 56/113 overlap is zero there although another pair, 56/72, certifies a positive opening |
| Core `{1,4,5}`, extras `{6,7,11,13}` | A zero-duration equality route is necessary; a negative duration bound is not absence of a valid time |

These facts are archived in [CORE_TRANSFER.md](../../notes/CORE_TRANSFER.md) and the small-gcd review. They are known controls, not held-out validation. The task should yield either a stated sufficient selection condition with its proof obligations, or a specific failure identifying missing input. Stop at the first unresolved failure; retain it rather than retuning the rule on more examples. No new speed scan or full-set reconstruction is needed.

This would differ from the already-completed selector that evaluates every component and every pair or tree, then chooses the greatest bound. Repeating that exhaustive local evaluation is not a new selection mechanism. A prescribed budget makes the information cost part of the question, and a protected endpoint route prevents tight cases from being silently excluded.

The common issue is selecting where a compact summary is informative. The 56/113 family has different fixed speeds, four residual blockers, and a common-start local-overlap problem; the new all-phase pair statement cannot simply be transferred to it. Existing small-gcd infinite-family candidates also remain in force. Their hypothesis and uniformity gaps, rather than the already-explained 56/113 numerical example, are the priority. Further fixed-pair tuning, cutoff polishing, and the parked +7/+9 extension are not the proposed next task.
