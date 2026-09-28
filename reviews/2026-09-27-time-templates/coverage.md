# What the fixed-time classification adds to existing coverage

September 27, 2026, Pacific research date; September 28 UTC. This is the representation and prior-coverage audit for the [frozen protocol](protocol.json), baseline `e7dc510cc157a3d8e8c1ee81cca3922f48270bc1`. Scope is eight runners `{0,1,4,5,6,7,11,V}`, positive integer V outside `{1,4,5,6,7,11}`, reference 0, threshold 1/8. Only runner 11 may have initial phase theta. All other runners start at 0; theta=0 is the original common-start problem. V is a parameter, not necessarily the fastest speed.

**The classification supplies compact certificates robust to every phase of runner 11. It does not add common-start coverage to this family: an earlier adaptive witness already covers every admissible V.** Moreover, every integer in the three classes missed by the frozen menu already has common-start positive duration under the existing tail argument. Failure of the menu must be kept separate from failure of phase robustness or loneliness.

The finite exact classification is independently **REPRODUCED** in [classification_verification.json](classification_verification.json). Supplied unbounded arithmetic, geometric, and prior family arguments retain **HYPOTHESIS / proof-candidate** status under [CLAIM_STATUS.md](../../CLAIM_STATUS.md). This audit uses repository sources and direct mathematical comparisons; it makes no external literature or novelty claim. Material AI involvement includes the comparison, reasoning, and writing.

## 1. Exact scope of the new certificate

For a reflected pair t,1−t, all unchanged integer speeds have equal distances at its two times. Let their common minimum be c. If the two phases of runner 11 have circular separation d, the circle triangle inequality gives

`max(||11t+theta||,||11(1−t)+theta||) >= d/2`.

In each frozen template c<=d/2. The best full distance within the pair is consequently **exactly c at every theta**, because the unchanged runners also impose the upper bound c at both times. This pointwise constancy is stronger than an infimum over phases.

| Frozen pair | Fixed unchanged distances, speeds 1,4,5,6,7 | Runner-11 phase separation | Full best-of-pair margin at every theta |
| --- | --- | ---: | --- |
| 1/8, 7/8 | 1/8, 1/2, 3/8, 1/4, 1/8 | 1/4 | `min(1/8,||V/8||)` |
| 7/15, 8/15 | 7/15, 2/15, 1/3, 1/5, 4/15 | 4/15 | `min(2/15,||7V/15||)` |

Thus the eighth pair works at threshold exactly when 8 does not divide V and never gives a strict witness. The fifteenth pair gives margin 2/15, hence strictness, unless `V mod15` is 0,2,13. Its margins on those three residues are 0,1/15,1/15 respectively. These conclusions use substitutions at the prescribed times, without constructing the full safe set.

Taking the maximum of the two constant margins yields:

| Four-time outcome | Arithmetic condition | Classes modulo 120 |
| --- | --- | ---: |
| Strict for every theta, margin 2/15 | `V mod15` outside `{0,2,13}` | 96 |
| Threshold certificate for every theta, margin 1/8 | `V mod15` in `{0,2,13}` and `8` does not divide V | 21 |
| All four times fail for every theta | `V mod120` in `{0,32,88}` | 3 |

The last row follows by writing V=8k and solving `8k=0,2,13 mod15`. The menu margin is 0 on residue 0 and 1/15 on residues 32,88. The least positive admissible representatives are respectively 120,32,88. Excluding six individual speeds does not exclude their whole residue classes.

Period 120 is sufficient because 120 times each of the four rational times is an integer. This proves the fixed-time coefficients repeat for all admissible V in each class. It is not a claim that the complete configurations repeat or that 120 is minimal. The counts describe this menu's classes, not a proportion of all Lonely Runner instances solved. The 21 threshold classes are not a classification of tight configurations: other times can be strict.

The independent verifier checks 240 pair envelopes and 120 four-time envelopes by exact affine phase cells and event points, with a separate safe-arc coverage calculation. The infinite conclusion comes from the supplied residue argument, not from extrapolating a list of 120 speed tests.

## 2. What was already covered at common start

[VARIABLE_SPEED_FAMILY.md](../../notes/VARIABLE_SPEED_FAMILY.md), dated September 24, gives the explicit rule

\[
t(V)=\begin{cases}
1/8,&8\nmid V,\\
17/56,&8\mid V\text{ and }56\nmid V,\\
17/56+1/(8V),&56\mid V.
\end{cases}
\]

All six fixed runners are safe on `S=[17/56,5/16]`, with strict inequalities in its interior. Nonzero eighth and seventh residues justify the first two cases. In the last case runner V exits its blocking interval before S closes. This already supplies a common-start witness for **every** admissible V. It does not assert optimal distance or strictness for every V.

The same day's [TWO_VARIABLE_SPEEDS.md](../../notes/TWO_VARIABLE_SPEEDS.md) treats the broader common-start family `{0,1,4,5,6,7,x,y}` and already records 7/15 as a witness for the pair `(11,16)`. The present use of 7/15 together with 8/15 adds a phase-uniform certificate and an arithmetic transfer rule; the common-start witness is not newly discovered here.

[CORE_EXCHANGE_NEIGHBORS_2026_09_27.md](../../notes/CORE_EXCHANGE_NEIGHBORS_2026_09_27.md), under “A fixed successful certificate for the whole tail,” gives

\[
U_J(V)\ge\frac3{448}-\frac3{16V}>0\qquad(V\ge29),
\]

using the fixed core `{1,4,6}`, `J=[9/32,5/16]`, and a fixed exact tree. This is a positive-duration common-start certificate. Every positive member of each missed class is at least 32,88,120 respectively, so the bound covers **all members of all three missed classes**, not just the diagnostic representatives. This use of the old analytic bound does not extrapolate their new diagnostics.

The containment behind the old tree includes `B_11 intersect J` contained in `B_7 intersect J` at phase zero. It cannot be silently carried over to arbitrary initial phase of 11. Accordingly, the comparison is:

| Statement | Quantifiers and contribution |
| --- | --- |
| Old adaptive witness | Every admissible V; some time at theta=0 |
| Old fixed-window tail | Every V>=29; positive common-start duration |
| New fixed-menu classification | Listed unbounded arithmetic classes; for every theta, a successful time among the prescribed two or four |
| New missed-class diagnostics | Only the three prescribed representatives; full phase-projection decisions and direct common-start checks |

These are different certificate and quantifier improvements within a previously covered common-start family. None establishes a general Lonely Runner result, treats every reference, or proves novelty.

## 3. What the diagnostics can and cannot establish

For a given representative let A_V be the full time set safe for the unchanged speeds `{1,4,5,6,7,V}`. Let P_V be its image under `11t mod1`, retaining isolated points, and let B_V be the closure of its positive interval support. Write c(K) for the shortest closed circular arc containing K. The supplied covering criteria from [PHASE_PROJECTION_2026_09_27.md](../../notes/PHASE_PROJECTION_2026_09_27.md) are

\[
\text{nonempty at every theta}\iff c(P_V)\ge1/4,
\qquad
\text{positive duration at every theta}\iff c(B_V)>1/4.
\]

The strict versus weak inequality preserves equality contacts. Full projection answers the all-phase question after reconstructing A_V; a midpoint of a common-start component answers only theta=0. Neither procedure is an arithmetic rule that selects useful times without first resolving the joint safe set.

The three frozen representative diagnostics are complete in [diagnostics.json](diagnostics.json) and independently reconstructed in [diagnostics_verification.json](diagnostics_verification.json). In all three, A_V has no isolated components, P_V=B_V, and c(B_V)>1/4. Thus all three are **strict for every phase of runner 11**, although none of the four prescribed times works at any phase. Their direct common-start witnesses are selected by the frozen longest-component midpoint rule, not by a new template search.

| Representative V | c(P_V)=c(B_V) | Common-start duration | Chosen common-start time | Minimum distance there |
| ---: | ---: | ---: | ---: | ---: |
| 120 | 183/224 | 53/3360 | 821/2688 | 53/384 |
| 32 | 1387/1792 | 9/896 | 1097/3584 | 73/512 |
| 88 | 183/224 | 37/2464 | 437/1408 | 97/704 |

The archives contain 38 positive unchanged-safe components and 14 positive common-start components across these inputs, with no isolated components in either list. The independent reconstruction uses a threshold-time partition and direct phase-preimage checks, rather than importing the primary implementation. These are bounded **OBSERVED / REPRODUCED** calculations; their all-phase interpretations use the supplied general covering argument.

Period 120 belongs only to the four frozen evaluations. It provides no periodicity theorem for A_V, P_V, B_V, durations, components, witnesses, or actual phase robustness. The full diagnostics for V=120,32,88 therefore cannot be copied to V+120.

The earlier two-time completeness argument is conditional: at this threshold, if a configuration is nonempty for every phase of the selected runner, some pair of unchanged-safe times is a certificate. Under the finite nonzero-speed assumptions, all-phase positive duration likewise admits a strict pair. This does not promise one of the frozen pairs will succeed, establish phase robustness for arbitrary configurations, or supply a way to find the pair directly from speeds. The stronger all-phase target itself is not required by the original common-start conjecture.

## 4. Why another fixed rational menu cannot finish this family

The obstruction was already stated in [VARIABLE_SPEED_FAMILY.md](../../notes/VARIABLE_SPEED_FAMILY.md), under “Counterchecks and limitations of the pattern.” Given any finite collection of rational times, choose V to be a sufficiently large common multiple of their reduced denominators. Then V is distinct from the fixed speeds and collides at every listed time. This defeats that menu already at common start and continues to defeat it for every phase of runner 11.

For the present menu, the denominator multiple is 120, exactly its residue-zero obstruction. Appending finitely many more fixed rational pairs can change the missed classes but cannot eliminate this obstruction over unbounded V. The existing adaptive rule shows why this is a restriction on fixed menus rather than an impossibility of an inexpensive witness rule.

A meaningful further selection problem is therefore a **V-dependent** pair or another adaptive certificate, chosen from permitted arithmetic data before full allowed-set reconstruction. Its scope would have to be stated: common-start coverage is already available here, whereas one-runner-phase robustness would be a stronger target. Finding a pair retrospectively from a computed projection would verify its existence but would not resolve the desired selection problem. No additional pair search is part of this round.

## 5. Connection to the preserved small-gcd priority

[SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md](../../notes/SMALL_GCD_DISTINCTION_REVIEW_2026_09_27.md) concerns a different family and the existing control `{0,1,4,5,56,113,64,72}`. Its local certificate on `J=[9/32,3/8]` needs both actual single-blocking durations and the overlap placed by `113−2·56=1`. With `T` the sum of singles and `O` that selected overlap, it proves

`U_J >= |J|−T+O = 1223/911232 > 0`.

Keeping only exact singles or only the selected overlap while retaining the other coarse allowance remains inconclusive. The old audit already explains this repair and records small-gcd infinite-family proof candidates. The unresolved issue is which speed assumptions permit selection of a useful opening and enough local arithmetic information to force a witness, with controlled evaluation cost.

The common methodological point is **conditioning before compression**. Here, fixing two times retains their joint placement on the common clock; after that, unchanged distance caps and the selected runner's two-phase separation suffice for a universal-in-theta certificate. In the 56/113 control, conditioning on a useful interval and retaining concentration plus overlap placement gives the positive duration bound. Whole-period scalar summaries or a failed coarse certificate can lose the information the local decision needs.

These mechanisms answer different questions. A fixed-time residue classification is not a result about arbitrary four-blocker local overlap, and the 56/113 argument does not automatically select robust time pairs. A full gcd together with a reduced ratio reconstructs the pair of speeds; the loss is in subsequent compression to selected summaries, not in those complete arithmetic inputs themselves. Fixed-size output also need not mean fixed-cost evaluation.

The shared open priority is an a priori, speed-derived selection rule with a precise scope and endpoint route. This round supplies one exact compact classification and preserves its failures. It does not authorize a new speed search, reopen the parked +7/+9 extension, or turn retrospective exact reconstruction into a general selection theorem.
