# Mathematical audit: what survives, and what is worth carrying forward

Date: 2026-10-02 UTC. Baseline: `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`, branch `research/near-doubling-overlap-2026-09-24`. This is a separate AI review track in the requested team assessment. It is not independent human or formal certification. Existing proof-candidate status is retained; novelty is not claimed. Old packages were not modified and no commits were made by this track.

**Assessment:** I found no fatal mathematical gap in the explicit all-integer-r `(1,2,r)` construction. Its finite remainder, endpoints, normalization and clock lifts survive this review. A small separately written exact check reproduces its fifteen small cases and exposes an additional, precise result: **two fixed connected-component sources are necessary and sufficient for this family**, under the source convention below. The older mixed-kernel/23-advance argument remains the most substantial standalone mathematical candidate for another problem; its destination is periodic **point** feasibility, not ordinary job scheduling. The missing general step is still a structural guarantee that a small useful source menu exists for arbitrary parameter pairs.

## 1. Line-by-line audit of the current construction

Primary target: `reviews/2026-10-02-cc-orbit-intervals/DERIVATION.md`, read in full, together with the full results report, protocol and research note. The asserted family is

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r),
\]

with positive integral parameters, distinct physical speeds, common start, selected reference zero and closed threshold `1/8`. Ten runners require only `1/10`; neither this stronger selected-reference result nor its failure would settle all references.

| Step in the derivation | Audit and reason |
| --- | --- |
| Primitive normalization | With `g=gcd(p,q,r)`, `(A,B,C)=(p,q,r)/g`, `d=gcd(A,B)` and `(P,Q)=(A,B)/d`, both `gcd(P,Q)=1` and `gcd(d,C)=1` follow. No pair-gcd normalization may erase the remaining `d` time occurrences. |
| Complete primitive core `K_(P,Q)` | Exact phase events plus open-cell midpoint predicates and separate endpoint tests determine the complete closed safe set. There are finitely many events for positive integer speeds. This is equivalent to ordinary exact band intersection; agreement establishes implementation correspondence, not nonemptiness for every pair. |
| Constant physical and torus laps on a component | Correct: a nonempty safe component cannot cross a phase wrap because an open neighborhood of every integer phase violates the positive threshold. Fixed laps therefore extend to the component endpoints. An isolated component is still a legitimate source. |
| Source `S_I` and physical inverse | Use a different symbol, say `xi`, for the running core clock to avoid overloading the interval's upper endpoint: `(P xi-L_p,Q xi-L_q,z)`, `xi in I`, `z in [1/8,7/8]`. This is only a notation clarification. Other row laps are `L_i-a_i L_p-b_i L_q`. |
| All lifts | For each `j=0,...,d-1`, `tau=(xi+j)/d` and `t=tau/g` recover the actual normalized/original clocks. Their union is exactly the core-safe set in one normalized full period. These are not optional duplicate records. |
| First-safe-band contact | `k=ceil(CL-7/8)` is precisely the first integer whose safe band's right endpoint is at least `L`. `tau*=max(L,(k+1/8)/C)` also lies at or before that band's right endpoint. Thus `tau*<=U` is necessary and sufficient for contact, including singleton or endpoint contact. |
| Rejection meaning | Failure of every lift of one component rejects only that source. Failure of every component of a complete core rejects `1/8` feasibility for that input. It does not reject `1/10`, and a compressed menu cannot certify full nonexistence. |
| Multiple-lift sufficiency | Because `gcd(C,d)=1`, the `d` phases form a rotated equally spaced grid. For `d>=2` no open quarter-circle can contain the entire grid. Any one nonempty core component then suffices, conditional on retaining every lift. |
| One-lift width bound | Each connected unsafe gap has length `1/(4C)` and is open. A closed interval of width at least this length cannot be contained in one gap. Equality gives a point guarantee, not positive duration. |
| Fixed-pair finite reduction | For `d0=gcd(p,q)`, normalization gives `d=d0/gcd(d0,r)`. Thus `d>=2` iff `d0` does not divide `r`. If `r=d0 C`, `d=1`; a positive source of primitive width `w` covers `C>=ceil(1/(4w))`. Only the remaining small multiples need checking. This assumes the positive source exists and says nothing uniform about all pairs. |
| Isolated-only limitation | Correct: finitely many rational singleton times can all be killed by an added integer speed divisible by their denominator lcm. That observation concerns point-only sources; a positive interval cannot be reduced to finitely many fixed rational contacts without losing this tail property. |
| Scaling | If every speed is multiplied by `lambda>0`, `lambda v * (t/lambda)=vt`. The stated positive-integer scaling is consequently valid, preserving all physical phases and inequalities. The all-r quantifier is still over positive integers in the unscaled family; this does not silently extend it to every arbitrary real added speed. |

The first-contact lemma has an elementary threshold-parameterized form. For `0<delta<=1/2`, speed `C>0`, phase `alpha` and a supplied closed interval `[L,U]`, use

\[
k=\lceil CL+\alpha-(1-\delta)\rceil,
\qquad t_* =\max\{L,(k+\delta-\alpha)/C\}.
\]

Contact exists exactly when `t_*<=U`; width `2 delta/C` suffices. This is a small exact modular-constraint primitive, not a claim that computing the input interval is easy or that the formula is original.

### The eight core bands really contain the proposed interval

For `(p,q)=(1,2)`, let `I=[25/152,7/40]`. The independent check gives the following unwrapped, fixed-lap phase ranges. Every row lies in `[1/8,7/8]`; in particular the lower `19` contact and upper `5` contact are equality-safe.

| Speed | Phase at left endpoint | Phase at right endpoint | Fixed physical lap |
| ---: | ---: | ---: | ---: |
| 1 | 25/152 | 7/40 | 0 |
| 2 | 25/76 | 7/20 | 0 |
| 3 | 75/152 | 21/40 | 0 |
| 4 | 25/38 | 7/10 | 0 |
| 5 | 125/152 | 7/8 | 0 |
| 7 | 23/152 | 9/40 | 1 |
| 10 | 49/76 | 3/4 | 1 |
| 19 | 1/8 | 13/40 | 3 |

The width is `7/40-25/152=1/95`. For every integer `r>=24`, `r/95>1/4`; the added runner cannot block the whole interval. The real width cutoff is `95/4`, whose integer ceiling is 24. The proof does not infer the tail from testing large examples.

The full fifteen-case check was reconstructed using intersections with all of the added runner's exact safe bands, rather than using the candidate formula to decide existence. Formula outputs were then compared with the first point of that separate intersection.

| Admissible `r<24` | First contact in `I` |
| --- | --- |
| 6, 12 | No contact; formula candidates are `3/16`, `17/96`, respectively, both beyond `7/40` |
| 8, 9, 11, 13, 14, 15, 16, 17, 20, 21, 22, 23 | `25/152` |
| 18 | `25/144` |

At `t0=1/8`, the eight core phases are `(1,2,3,4,5,7,2,3)/8`, all safe. The exceptional added phases for `r=6,12` are `3/4,1/2`. Therefore the published piecewise witness is correct on its stated domain. The code additionally checks `r=24,40,80,152*10^60` by direct exact physical inequalities; these four controls are not evidence replacing the analytic tail. The huge case starts with an unsafe integral phase at `25/152` and recovers `25/152+1/(8r)`, so it exercises an actual exact forward contact without enumerating the runner's periods.

The lifting countercontrol is explicit: for `(p,q,r)=(2,4,1)`, the chosen source's canonical lift is `[25/304,7/80]`, entirely unsafe for speed 1. Its second lift is `[177/304,47/80]`, entirely safe for that runner. Thus a purported pair-clock simplification keeping only `j=0` would fail on an actual admissible configuration. The present derivation does not make that mistake.

## 2. Post-review deduction: two sources are optimal in this declared class

This section is a new deduction in the review, not a preregistered prediction, held-out success, novelty claim or promotion of repository claim status.

**Source convention.** One source is one complete connected component of the fixed primitive core `K_(1,2)`, crossed with the added runner's full safe slab. The source menu is fixed before `r` is known. It may select a point within its retained components using `r`, but may not redefine a component, append a new component on demand, or hide the full core in a fallback. The output is one witness for every admissible positive integer `r`, with no optimality or complete-set request. Counting a disconnected union as one source changes the question and voids the lower bound.

Exact band intersection reconstructs the entire core as

\[
K_{1,2}=\{1/8,3/8,5/8,7/8\}
\;\cup\;[25/152,7/40]
\;\cup\;[33/40,127/152].
\]

The two positive intervals are reflections. A short checkable elimination sequence is: the first five speeds `(1,2,3,4,5)` leave

\[
[1/8,7/40],\ [9/32,7/24],\ \{3/8\},\ [17/40,7/16]
\]

and their reflections. Adding speed 7 leaves the four odd eighths and `[9/56,7/40]` with its reflection. Speed 10 leaves these unchanged. Speed 19 raises the first positive interval's left endpoint to `25/152`, and reflects this change on the other side. All intersections are closed.

Now only two added speeds are needed for the lower bound:

| Added speed | Each of the two positive core components | Each of the four singleton core components |
| ---: | --- | --- |
| 6 | Fails | Succeeds |
| 8 | Succeeds | Fails |

For example `6I=[75/76,21/20]` is entirely inside the open unsafe band `(7/8,9/8)`; reflection gives the other interval's failure. Every odd eighth is safe for speed 6. Conversely multiplying an odd eighth by 8 gives an integer, while `8I` has fractional range `[6/19,2/5]`, safely inside the band. The checker also recovers these complete final sets: at `r=6` (and at `r=12`) precisely the four isolated points survive; at `r=8` precisely the two positive intervals survive.

Every single allowed component is therefore refuted by an admissible speed, whereas the existing interval-plus-point construction covers all admissible speeds. **The minimum source count is exactly two.** More than cardinality is necessary: a universally sufficient menu in this class must include both a positive component and an isolated component. This is a precise example of two different kinds of alternatives becoming indispensable under later constraints.

There is also a shorter upper-bound proof. The point `1/8` handles every integer `r` not divisible by 8. Of the multiples of 8 below 24, `r=8` and `r=16` are both safe throughout `I`; their added phases at its left endpoint are `6/19` and `12/19`. The width argument covers every `r>=24`. This reduces the finite proof remainder to two transparent modular controls. It is an alternative explanation of the existing result, not additional family coverage. Any of the four isolated core points works with either positive component, so all eight such two-component menus work; no selection advantage is implied.

## 3. Strongest earlier mechanisms and their actual transfer limits

### Mixed kernel and 23 advancing moves

I read the complete `SHORT_KERNEL_BOUND_2026_09_28.md` argument and its earlier mathematical transfer assessment, and checked the logical steps directly. No fatal gap was found. The argument is stronger and more portable than a fitted finite menu because its hypotheses already allow arbitrary positive real periods and arbitrary phases.

For four periodic open blockers of width `p_i/4`, order periods `P>=q>=r>=s`. One full-period uniform variable for `P`, together with three four-point quarter-period grids, gives average total multiplicity one and a density positive on an interval of width

\[
H=P+3(q+r+s)/4.
\]

A strictly advancing occurrence chain covering that support would have multiplicity at least one everywhere and strictly more than one on an open overlap of positive weight. This contradicts the average. Thus its span is strictly below `H`. The count retains full occurrences: `h` occurrences of period `P` force span at least `(h-3/4)P`, yielding `h<=3`. Pair and triple chains have at most 3 and 7 occurrences because a return to the longest-period label cannot accumulate its full period through the shorter intervening labels. For a triple chain of length at least six, the return inequalities give `r>3s`, `q+2s>3r`, hence `q+r+s<11q/7`. If the four-label chain has three `P` occurrences it instead requires `q+r+s>5P/3`, so each intervening triple piece has at most five occurrences. These two cases give the stated 23 count.

Consequential details survived scrutiny: the discrete-grid average is not pointwise one quarter at threshold endpoints; the continuous factor removes those exceptions only in the integral. The density covers the full support interior even with tied periods. Actual increasing-endpoint chains, including containment and skipped laps, are counted; no minimal-cover hypothesis is smuggled in. Safe endpoints remain available after the integral argument. The count is advancing moves, not raw projection calls, bit complexity or a bound on the numerical values of lap indices. The higher-duty model used by full LRC has aggregate duty greater than one; the critical-duty contradiction cannot be copied there.

The strongest exported assertion is therefore: under these exact open-quarter-duty hypotheses, an earliest-safe-point iterator has a constant advance bound, and every supplied closed window of length at least `H` contains a safe point. This remains a candidate for independent mathematical/formal review. No new trace campaign, implementation benchmark or proof-assistant formalization was performed here.

The export breaks when its output contract changes. Equal periods `4/13` with offsets `0,1/13,2/13,3/13` leave only the times `j/13`. The point claim permits zero duration. Half-open blockers fill those contacts; positive dwell or jitter expands the forbidden intervals and changes the quarter-duty hypotheses. Thus no ordinary scheduling, robustness or throughput advantage follows.

### Two protected openings, interval margins and fastest-core conditioning

The `LAST_RUNNER_COMPATIBILITY` two-window argument was read in full. For positive closed intervals with hull width `D`, gap `G` and maximum individual width `w`, `G<=3w` and `d>=1/(4D)` prevent an arbitrary-phase quarter-duty runner from covering both windows: one occurrence would need `dD<1/4`; two would need `dG>3/4` while `dw<1/4`. Strict versions give positive duration, without a prescribed minimum. This preserves relative placement that a width ranking loses. It supplies a useful sufficient condition once the windows have been obtained; it does not force those windows to exist.

The exact midpoint-radius identity in `EXACT_INTERVAL_CRITERION` is another clean extraction:

\[
\inf_{t\in I}\|vt+\alpha\|
=\max\{\|vm+\alpha\|-|v|h,0\},\qquad\overline I=[m-h,m+h].
\]

Its proof from distance-to-integers and a nearest-integer endpoint is correct, including zero speed and omitted endpoints. It is an exact robust containment test for a supplied affine-phase interval; it does not turn a midpoint alone into a certificate or discover a good interval.

The `FASTEST_CORE_CERTIFICATES` argument was also read in full. Conditioning on a fastest runner bounds each core window by a single slower runner's safe-gap length; each residual blocker is consequently a single interval or empty. Ordering those intervals by left endpoint and linking each to the preceding maximum-right-endpoint interval yields the exact tree union-duration identity. This is a useful representation choice and a concrete reason pair data become sufficient locally. Zero tree duration still cannot distinguish an empty set from isolated solutions. No external mathematical novelty claim is supported by this review.

## 4. What is still missing or would be a fatal overclaim

No local defect was found in the audited all-r or 23-advance proofs. The following stronger implications are unsupported or explicitly false:

1. Complete-core recovery does not prove every core is nonempty. The 1,197 successful cases cannot supply this universal premise, and reconstructing the full safe set is not itself a new existence argument.
2. A fixed rational point-contact source class cannot cover every future integer runner: a denominator multiple defeats it. The archived 36-sheet failure at `r=40k` is an instance. This obstruction was read in the preceding sheet derivation; its full 36-contact enumeration was not rerun here.
3. Width alone cannot choose every phase-compatible alternative. Keeping all positive-width sources is also insufficient at the exact threshold; the `(1,2,6)` and `(1,4,13)` equality losses show why. The former is independently reconstructed here; the latter is attributed to the frozen report.
4. The source-minimum-two result is not a uniform bound over `(p,q)`, not an optimum solver result, and not a bound when an arbitrary disconnected union may count as one source.
5. Neither low-dimensional coordinates nor a succinct witness supply inexpensive discovery. A full core costs event/band construction and storage. The current complete-source stage makes that cost visible; no efficiency claim should be inferred from its simpler last-runner query.
6. A generic application to another open problem needs an actual map of objects, quantifiers and outputs. This record does not establish one for scheduling synthesis, quantum theory, physics or a new information-theoretic principle.

The strongest generalization target is consequently structural: prove a useful source-width/placement bound, or show an unavoidable source-complexity obstruction, for a genuinely parameterized family. Repeating success on a larger box does not answer that question.

## 5. Best next mathematical work, with stop conditions

**First choice: an exact small-source decision on two already exposed pairs, with a proved tail.** Keep the existing widest source fixed for `(1,4)` and `(1,6)`. The archived widths are respectively `1/140` and `11/1428`, so their tails start at added integer speed 35 and 33. Before doing any new evaluation, freeze the complete cores, component source definition, first-contact rule and all admissible finite remainder inputs `r<35` and `r<33`. These are at most 66 integer candidates before distinctness exclusions, not a new box. Retain the exact full-core answer as comparator.

For each pair, ask whether **the fixed widest component plus one other component** covers every finite remainder. Each component's exact hit vector gives a finite set-cover decision. If a second component covers every widest-source miss, the analytic tail plus that finite certificate proves all-r coverage for the pair. If none does, the exhaustive component list proves that no two-source menu containing that leader can work. It is only leader-constrained optimality; it must not be relabeled as the unrestricted minimum. The current `(1,2)` minimum-two certificate is a development control, not another fresh result.

**Stop:** terminate after those two decisions. A full-core miss is a real `1/8` failure for that input, requiring a separate `1/10` question, not a failed LRC verdict. A two-source miss rejects that declared selector class. A pass establishes exactly those two fixed-pair families. Do not enlarge the domain, increase the menu silently, or claim a uniform theorem from these outputs. Proceed beyond this only if the exact successful/failing contacts suggest a symbolic placement criterion with a stated parameter domain.

**Alternative if external mathematical reuse is the priority: independently formalize the 23-advance lemma.** The compact target is the arbitrary-phase, positive-real-period open-quarter-duty theorem with its explicit chain definition. Split obligations into the mixed average, strict-span contradiction and the short combinatorial count. Carry an exact translation back to an earliest-point iterator, separate from dwell or half-open calendars. The pre-existing equality and strict16 controls are semantic fixtures, not evidence of a new application.

**Stop:** a valid 24-advance chain, a gap in positive-density support, or an unjustified endpoint step defeats the candidate and should be preserved. If the formal or independent proof succeeds, stop with that precisely scoped theorem artifact; do not infer external demand, speed superiority or a scheduling result. Do not launch a broad rational phase/period search merely to chase the constant. This review neither contacted reviewers nor launched formalization.

## 6. Primary comparisons and retrieval coverage

Access date for both primary sources below: **2026-10-02 UTC**. This was a targeted comparison, not a literature census. No novelty or priority conclusion follows.

| Primary source | What was actually inspected and what follows |
| --- | --- |
| Beck, Hoşten and Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29, published 2019-06-03. [Author-hosted published PDF](https://math.colgate.edu/~integers/t29/t29.pdf) | Front matter; geometric formulation through Proposition 1; Theorem 4 and its full proof on printed page 12. Theorem 4 attributes arbitrary-phase positive-integer-speed existence at `1/(2k)` to Schoenberg. That basic existence must not be claimed new. The inspected theorem does not state a 23-advance iterator bound. This review did not inspect Schoenberg's original paper or determine priority for the kernel/count. |
| Ludovic Rifford, *On the time for a runner to get lonely*, dated author preprint 2022-02-21. [Author PDF](https://math.univ-cotedazur.fr/u/rifford/Papiers_en_ligne/LR_Rifford.pdf) | Section 2.2, Definition 5, Proposition 4 and its proof, and Proposition 5 through its proof, printed pages 12–14. This is a close occurrence-labelled interval-chain precedent. Its definition includes minimality and strict nonadjacent separation, which cannot automatically be imposed on the repository's actual endpoint-jump traces. The full paper and its exhaustive classifications were not reviewed. |

The latest runner-count frontier, every spectrum claim, solver complexity literature and all possible applications were outside this track. No current-frontier statement is used to justify the assessment.

## 7. Actual read/check ledger

| Material | Coverage and limit |
| --- | --- |
| Required entry/governance | `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, mathematical baseline read. `README`, `HANDOFF`, `LR4_HANDOFF`, research plan, source index and CC representation rules inspected for current state and relevant historical entries. The large history/representation documents were targeted, not read end to end; some initial combined reads were output-truncated and were followed by narrower reads. |
| Current interval package | Full derivation, results report, protocol and research note. Saved development/raw run arrays and implementation files were not exhaustively audited. The full 1,197-case run was not rerun in this track. Reported large counts are attributed to the frozen package. |
| Prior transfer review | Full `reviews/2026-09-30-ultra-transfer-value/math_transfer.md` and package README; coordinator assessment and coverage ledger searched/targeted. This does not certify every earlier track. |
| Earlier proof candidates | Full short-kernel, last-runner compatibility, exact interval and fastest-core notes. The preceding sheet-coverage derivation was read for contact, saturation, floor-sum and finite-contact obstruction context; its programs and exhaustive source enumeration were not rerun. Earlier historical proof candidates outside these notes were not all reaudited. |
| Fresh work in this track | One small, post-exposure exact checker, importing no research implementation, reconstructs the six-component `(1,2)` core; all fifteen small-r contact cases; complete safe sets at `r=6,12,8`; four tail/huge-r physical witnesses; two clock-lift outcomes for `(2,4,1)`; five endpoint/singleton band controls. All assertions pass. The core's intermediate elimination sequence was also printed and inspected. This is independently structured code by a separate AI reviewer, not human certification or held-out research. |
| Not done | No broad speed/phase/word/all-reference search, new large target experiment, 23-trace campaign, benchmark, proof assistant, outreach, git commit, original package edit or claim-status promotion. |

Reproduce the small check from the repository root:

```bash
python reviews/2026-10-02-ultra-value-review/math_audit_check.py
```

The output is `math_audit_checks.json` beside this report. The checker uses only Python's standard library and exact `Fraction` arithmetic. It writes only that uniquely named audit artifact. Its proof controls were selected after reading the original evidence, so they must not be reported as fresh validation.

**Representation checkpoint:** the review retains the selected reference, stronger threshold, closed equality, exact source identity, common physical clock, all lifts, construction cost and query scope. The minimum-two compression preserves one all-r witness, not the entire safe set or every maximizer. The complete six-component core and explicit band reconstruction remain the recovery source. A changed pair, threshold, start phase, source definition or requested output requires rechecking the claim.
