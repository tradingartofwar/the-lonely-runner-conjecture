# Distinction audit: what collective coverage hides

September 25, 2026. Repository baseline: `f25e26f2074b036643a2c791f32aacc26856356b`. This audit follows Vance's request to pause the next family extension and examine representation loss. AI materially supplied the review, exact comparisons, and writing. Finite facts below are **OBSERVED/REPRODUCED** within their stated scope; general internally derived arguments remain subject to the repository's independent-review requirement. No novelty or general-conjecture claim is made.

The formal objective remains Lonely Runner. The working question is whether the other runners can collectively block every allowable moment. The immediate aim is to identify information sufficient for particular targets, and information that can be discarded without changing those targets.

## 1. Main findings and corrections to the starting prompt

1. **We found physical configurations with identical complete joint blocking-duration data but different allowed-set topology.** In the same fixed window, replacing 23 by 69 while retaining speeds 1,2,4,5,6,7 changes two positive openings into three. Replacing 25 by 75 in that fixed background changes three intervals into four intervals plus an isolated point. These are actual common-start runner configurations, not synthetic event arrangements or whole-configuration time scalings.
2. **The physical matching experiment did not find different clear duration or different local existence with the same single/pair data.** The existing 2,775-input domain has four matching pairs; all have equal positive duration. The earlier same-pair-data/zero-duration obstruction remains an abstract event arrangement. Its logical scope must not be widened to a second physical speed configuration.
3. **Some additional distinctions are irrelevant to the target.** On this window, speed 21 only blocks where 6 or 7 already blocks, while speed 2 never blocks. Replacing 2 by 21 changes overlap statistics but preserves the complete allowed set after any common fourth blocker is added. A more detailed model need not preserve every distinction.
4. **Exact local redundancy and concentration already determine clear duration.** Once both R and E are known, `U=R-E` leaves no missing variable for that target. The difficult task is obtaining sufficient speed-derived bounds without first solving the coverage problem. Temporal arrangement and endpoint data are still needed for other targets.
5. **The lattice premise needs updating.** Local integer lap-lattice certificates were constructed in [TWO_SPEED_SPARSE_TRANSFER.md](TWO_SPEED_SPARSE_TRANSFER.md), and the later [uniform triangle certificate](UNIFORM_TRIANGLE_CERTIFICATE.md) uses fixed affine strips. This audit additionally writes closed safe-lap cells for both requested stress cases. The general polyhedral/zonotope program remains unimplemented; the interval checker already contains equivalent closed-interval feasibility information.

The proposed +7/+9 family extension is parked while this audit becomes the current research entry point.

## 2. Specify the object and the target before judging a summary

Unless a separate example says otherwise, use eight total runners, common starts, selected reference 0, relative integer speeds, threshold `delta=1/8`, core `{1,4,5}`, and

$$J=[9/32,3/8],\qquad |J|=3/32.$$

Each nonzero integer relative speed blocks one quarter of the full unit time period. This statement is not a claim about every short window. There are seven relative runners in the original problem; the four-blocker accounting studies the four remaining constraints after choosing a three-runner-safe window. The threshold stays 1/8 throughout that split.

For extra runner i let

$$B_i=\{t\in J:\|v_i t\|<1/8\},\qquad
F=J\setminus\bigcup_iB_i.$$

Keep these targets distinct:

| Target | Information required by its definition |
| --- | --- |
| Local existence | Whether F is nonempty, including points |
| Positive local duration | Whether U=|F| is positive |
| Amount of local clear time | The value of U |
| Shape and placement | Components, lengths, positions, ordering, and isolated points of F |
| Selected-reference existence over a period | Whether at least one window or boundary works for that reference |
| Full conjecture | The required existence statement for every selected reference and every admissible configuration |

Topology, metric size, and position are themselves different: a list of component types does not specify their lengths or locations. Whole-configuration speed scaling can multiply the number of components observed in a unit time interval without changing full-period feasibility; normalization should remove that trivial source of apparent novelty.

For a summary map S and target T, the useful sufficiency question is:

> Within the stated class of physical configurations, does S(v)=S(w) force T(v)=T(w)?

A matching pair with different T disproves sufficiency. A different S with the same T shows that some distinctions in S may be unnecessary. Failure to find a matching pair in a finite domain proves neither general sufficiency nor general insufficiency.

The complete speed list, common start, threshold, and time domain already determine the trajectory and every B_i. The information loss occurs when we compress those data or use a relaxation. It does not demonstrate missing physical state variables.

## 3. Audit of the distinctions already in the research record

| Distinction | Exact evidence already obtained | Status and limit |
| --- | --- | --- |
| Individual amount vs collective coverage | Every runner has full-period blocked fraction 1/4, yet the archived configurations have different allowed durations and contacts | Demonstrated; individual averages are insufficient |
| Redundancy vs local concentration | On the union of core openings, extras 6/7/11/13 have R=E=34079/240240 and U=0; 6/7/8/11 have less R but U=29/1232 | Demonstrated in [LOCAL_OVERLAP.md](LOCAL_OVERLAP.md); not an assertion that increasing R with E fixed could decrease U |
| Global vs useful local overlap | The guaranteed common-start overlap lies where core speed 1 also blocks | Demonstrated location obstruction; global redundancy alone does not place a witness in a core opening |
| Reduced ratio vs repetition period | Known pair formula depends on coprime a,b; g=gcd(A,B) supplies joint phase period 1/g | Literature result reproduced in [SPEED_RATIOS.md](SPEED_RATIOS.md); an indicator can have additional symmetry, so do not silently identify every displayed period with its minimal period |
| Pair fraction/period vs configuration alignment | The 80/240 and 160/240 examples share rho=1/12, g=80, all four single durations, and selected local pair overlap 1/128, but have different U | Rechecked here; their other pair totals differ, so they are not a same-complete-pair-data counterexample |
| Pair durations vs higher joint occupancy | Ultra's 6/7/11/16 alteration preserves all single/pair durations and removes uncovered mass | Exact abstract-event obstruction, reproduced here; not a physical second configuration |
| Runner vertices vs interval occurrences | In the same case, overlaps with runner 16 require lap 5 for runner 6 and lap 6 for runner 11 | Demonstrated in [LAP_LABELLED_CONSTRAINTS.md](LAP_LABELLED_CONSTRAINTS.md); unions of intervals lose the common-intersection property of single intervals |
| Possibility vs duration of a joint overlap | With 56/64/72/112, a positive four-way duration prevents any cyclic graph from meeting the uncorrected active-forest condition, but subtracting its duration restores a stronger certificate | Demonstrated in [FOUR_BLOCKER_CYCLE_CORRECTIONS.md](FOUR_BLOCKER_CYCLE_CORRECTIONS.md); this limits a certificate class, not all possible inequalities |
| Complete joint durations vs temporal arrangement | Three matching pairs in this audit have every joint duration equal but different component structure | New bounded physical demonstration; all have equal positive U |
| Zero duration vs no solution | Tight 6/7/11/13 retains t=3/8 in J; 6/7/3/8 has empty J | Both exact; their other statistics differ. These are not matched complete-moment examples |
| Boundary position vs crossing direction | Frozen odd-eighth allowed sets agree for exceptional speeds 25/31/37/43 and 25/31/35/43, but the actual component at 3/8 is respectively a point and [3/8,55/144] | Archived exact comparison in [FOUR_PERTURBATIONS.md](FOUR_PERTURBATIONS.md); same frozen snapshot does not mean same motion |
| Auxiliary geometry vs actual reachability | A shared shear preserves every frozen allowed geometry up to rotation but changes tiling-contact reachability; the q=5 original has none at its tiling and the sheared case has t=7/16 | Demonstrated in [LOCAL_TILING_RULE.md](LOCAL_TILING_RULE.md); equality of frozen geometry is not equality of its alignment with the actual trajectory |
| Two contact controllers vs all constraints | A core threshold can turn the two exceptional runners' apparent interval start into an isolated contact | Exact example and scoped candidate analysis in the [Ultra review](ULTRA_REVIEW_2026_09_25.md), Section 4 |
| Failed certificate vs empty window | The old gcd bound fails for 56/113 while actual openings remain; the (3,8m) family really empties J but has solutions in H | Demonstrated; better information cannot create a witness in an empty chosen window |
| Selected reference vs complete configuration | Reference changes alter the relative constraints; common boosts preserve distances, while one selected-reference proof does not cover every reference | Required quantifier distinction throughout the repository |

There are two further terminology traps. First, the **full reduced ratio a:b together with g reconstructs A and B**. The loss occurs when replacing that information by rho, a period, or a coarse discrepancy bound; ratio and gcd themselves do not discard the pair's speeds. Second, “pairwise information” can mean a number, a compatibility predicate on lap labels, or an entire two-coordinate trajectory. The failure of pair-duration summaries is not a proof that all pairwise representations have the same limitation.

## 4. What each level of duration information can and cannot see

Let M(t) be the number of active blockers. Write

$$E=\sum_iD_i-|J|,\qquad R=\int_J(M(t)-1)_+\,dt.$$

Then U=R-E exactly. With four blockers, let P2 be the sum of the six pair durations, P3 the sum of the four triple durations, and Q the four-way duration. Counting each active subset gives

$$R=P2-P3+Q,\qquad U=-E+P2-P3+Q.$$

Thus the additional scalar needed beyond E and P2 to determine **duration** is

$$H=P3-Q.$$

Equivalently, if h_r is the duration with exactly r blockers active, then `H=h_3+3h_4`. Triple and four-way overlap are not interchangeable, and simply subtracting every triple without restoring Q overcorrects the all-four state.

This suggests a focused quantity to bound, but evaluating H by reconstructing all states merely recovers the answer. A useful certificate derives an upper bound on H from speed structure. The recent excluded triangles are examples with a relevant correction equal to zero; the four-cycle examples pay for a nonzero correction.

For each subset A, the intersection moment is `m_A=|intersection_(i in A) B_i|`. The complete set of moments determines every exact-state duration by inclusion-exclusion, including the empty-state duration U. Therefore:

- Two configurations with **all** joint durations equal cannot have different U.
- They can have different temporal ordering, component counts, interval lengths, first feasible times, and isolated contacts.
- For arbitrary measurable event models, a duration table cannot distinguish an empty allowed set from surviving points when U=0. Whether physical restrictions make a particular table sufficient for that decision is a separate realization question. The current physical matching search has not supplied identical complete moments with these two different outcomes.

The claim about complete moments is an algebraic fact about finite event sets; the temporal loss is demonstrated by actual runners below. Formal information-theoretic “synergy” has not been calculated. Uniform time on a chosen window could turn these masses into probabilities, but a target and decomposition convention would still be needed, and probability-zero contacts would remain invisible to duration statistics.

## 5. Physical matched summaries: what the existing domain reveals

We revisited exactly the already-studied domain

$$\{0,1,4,5,6,7,x,y\},\quad x<y\le80,
\quad x,y\notin\{1,4,5,6,7\}.$$

It contains 2,775 inputs. Single and pair durations were aligned by runner roles `(6,7,x,y)`, not sorted as anonymous numbers. D6,D7 and O67 are fixed, so the seven varying entries are `Dx,Dy,O6x,O6y,O7x,O7y,Oxy`. This also preserves all corresponding seven-runner moments involving the core: the core is safe everywhere on J.

There are 2,771 distinct signatures and exactly four collision classes, each containing two configurations:

| Variable pairs (x,y) | Strongest verified matching summary | Common U | Allowed components in J |
| --- | --- | ---: | --- |
| (2,23), (2,69) | Every joint duration | 13/552 | 2 intervals vs 3 intervals |
| (2,25), (2,75) | Every joint duration | 83/4200 | 3 intervals vs 4 intervals plus 1 point |
| (8,25), (8,75) | Every joint duration | 41/4200 | 2 intervals vs 3 intervals |
| (21,25), (21,75) | All single and pair durations | 83/4200 | 3 intervals vs 4 intervals plus 1 point |

All configurations retain the same core, window, threshold, common start, and six unchanged physical speeds within each pair. Because speed 1 stays fixed, this is not a common scaling of the whole configuration.

The matching claim is specifically about duration summaries. The speed ratios and pair gcds are **not** all equal: for example, gcd(6,23)=1 while gcd(6,69)=3, and gcd(6,25)=1 while gcd(6,75)=3. These existing arithmetic statistics already distinguish the displayed pairs. The experiment proves what duration moments discard; it does not prove that all our arithmetic representations discard the distinction, or that reconstructing the entire chronology is the only possible repair.

### Complete joint durations, different openings

For `(x,y)=(2,23)`, the complete allowed set is

$$[57/184,5/16]\ \cup\ [17/48,3/8].$$

For `(2,69)`, it is

$$[169/552,5/16]\ \cup\ [17/48,199/552]\ \cup\ [67/184,3/8].$$

Every joint occupancy duration is identical, but the first valid time and the component structure differ. The common clear duration is 13/552.

### A contact disappears from every duration statistic

For `(2,25)`, the components are

$$[17/56,5/16],\quad [17/48,71/200],\quad [73/200,3/8].$$

For `(2,75)`, they are

$$[17/56,61/200],\quad [37/120,5/16],\quad
[17/48,43/120],\quad [217/600,223/600],\quad\{3/8\}.$$

The single, pair, triple, four-way, and exact-state durations all agree. At the isolated point in the second case, speed 75 has phase 1/8 and enters safety, while core speed 5 has phase 7/8 and leaves safety. Their opposing crossings isolate the valid time. A duration-only representation cannot record that point as an additional component.

These pairs show loss of **how** lonely time survives. They do not show loss of **whether** it survives: all eight inputs have positive duration. No same-single/pair-signature pair with different duration or local existence was found in this finite domain. This negative result is part of the audit.

## 6. An apparent distinction that is irrelevant here

The fourth collision changes triple occupancy:

| Extras | T_(6,21,y) | T_(7,21,y) | Sum |
| --- | ---: | ---: | ---: |
| 6,7,21,25 | 0 | 3/800 | 3/800 |
| 6,7,21,75 | 1/300 | 1/2400 | 3/800 |

The pair totals match and the total triple correction matches, so U matches. Different triple identities do not by themselves force different duration.

There is a stronger structural explanation. On J,

$$B_{21}=[9/32,7/24)\ \cup\ (55/168,19/56).$$

The first piece is contained in `B7=[9/32,17/56)`, and the second in `B6=(5/16,17/48)`. Meanwhile B2 is empty. Thus

$$B_{21}\subset B_6\cup B_7,\qquad B_2=\varnothing.$$

For **any common fourth blocker y**, replacing 2 by 21 therefore leaves the entire allowed set in J unchanged, including contacts. It changes individual totals and creates higher-order intersections, but adds no coverage. This is an exact constraint implication, not a statistical association.

Because B6 and B7 are disjoint, `T_(6,21,y)+T_(7,21,y)=O_(21,y)`. The higher-order correction is already constrained by a lower-order total plus this geometric implication. More detailed triple allocation is unnecessary for this target.

This gives a useful standard for the relational hypothesis: a runner's additional blocking effect depends on the configuration in which it is placed. It does not follow that every relational feature is decisive, or that greater model detail must improve a certificate.

There is also a scoped sufficiency result. B6 and B7 are disjoint, and `B8=(23/64,3/8]` is disjoint from both. For x=2 or 8, at most two of `(6,7,x,y)` can block at once, so all triple corrections vanish. For x=21, the redundant constraint can be removed and only `(6,7,y)` remain, again with no triple. Consequently **the single/pair durations determine U for every admissible y in each fixed-x class x=2,8,21**. The verifier checks the corresponding Boolean identities. This explains why all four collision pairs preserve duration; a search for different U inside only these classes would be pursuing an already-excluded outcome. Their temporal and contact differences remain real.

## 7. Revisit the two requested stress cases

Both cases are now resolved by existing exact representations. They are diagnostic examples of weak summaries or estimates, not a pair that is indistinguishable under our current complete measures.

| Extras | E on J | R on J | U on J | Complete local outcome |
| --- | ---: | ---: | ---: | --- |
| 6,7,11,13 | 1445/96096 | 1445/96096 | 0 | Only t=3/8 |
| 56,113,64,72 | 1045/911232 | 5049/202496 | 6193/260352 | 11 positive intervals |

The tight case illustrates exact cancellation and the necessity of closed-boundary feasibility. The 56/113 case illustrates the weakness of a gcd-based local error estimate. Its old bound `-755/3072` is inconclusive, but the already-derived local 56/113 overlap gives a positive one-pair certificate `1223/911232`. The later triangle, tree, and cycle work supplies additional information. A short full repetition period was sufficient for an earlier method, not necessary for the opening itself.

### Closed safe-lap certificates make the difference explicit

For each speed v, select an integer lap k. Its allowed interval in that lap is

$$\frac{k+1/8}{v}\le t\le\frac{k+7/8}{v}.$$

For a vector of lap labels, intersect these closed intervals with J:

$$a_* = \max\left(\inf J,\max_i\frac{k_i+1/8}{v_i}\right),\qquad
b_* = \min\left(\sup J,\min_i\frac{k_i+7/8}{v_i}\right).$$

The assignment is infeasible if `a_*>b_*`, a contact if equal, and an interval if `a_*<b_*`. This is a mixed integer/linear description: k is integer and t satisfies linear inequalities. Eliminating t uses the corresponding pairwise lower-versus-upper inequalities and the window bounds. It is equivalent to the safe-interval feasibility calculation, not a new efficient search theorem.

| Speeds in displayed order | Integer safe-lap labels | Closed joint cell | Active lower / upper constraints |
| --- | --- | --- | --- |
| 1,4,5,6,7,11,13 | 0,1,1,2,2,4,4 | {3/8} | Lower: 11. Upper: 5 and 13 |
| 1,4,5,56,113,64,72 | 0,1,1,20,41,23,26 | [329/904,335/904] | Lower and upper: 113 |

The second cell has width 3/452. The witness 83/226 has minimum-distance margin `35/904` above 1/8. The first cell has zero width but is feasible. The audit constructs and checks both certificates explicitly. Their local feasible dimensions are zero and one; this does not add physical dimensions to the runners' motion.

The first cell is the whole local allowed set, as separately verified. The second is one of eleven components; a single feasible lap assignment does not claim to describe all of them. The complete seven-coordinate polyhedral/zonotope investigation remains open as a computational/structural project.

## 8. Representations: retained information, lost information, and cost

| Representation | What it retains | What it suppresses or cannot supply alone |
| --- | --- | --- |
| Speeds, common start, and exact time map | The entire deterministic schedule | Nothing about this stated model; extracting consequences may be difficult |
| Individual durations | Local marginal amounts | Co-occurrence, placement, endpoint contacts |
| Runner-level pair durations | Marginals and pair occupancy totals | Higher joint occupancy; temporal ordering; lap compatibility; contacts |
| All joint duration moments | Complete state-occupation distribution and exact U | Temporal arrangement and isolated contacts |
| Lap-labelled interval graph | Which particular intervals overlap; enough interval structure for exact union duration | Endpoint membership unless recorded; cost can grow with speeds |
| Blocking lap lattice | Common-time compatibility of selected blocking occurrences | A successful window or equality witness unless supplied separately |
| Closed safe-lap cells | Feasible intervals, contacts, and active boundaries for selected integer labels | A general way to find a useful label vector without exhaustive search |
| Frozen auxiliary geometry | Allowed phase geometry at a fixed auxiliary coordinate | Whether the actual shared-clock trajectory reaches it; crossing direction if motion is omitted |
| Ordered threshold events with contact directions | Temporal reconstruction, component joins/splits, and endpoint behavior | Compression benefit: listing every event is the exact checker in another form |
| Constraint implications, such as B21 subset B6 union B7 | Redundancy that can remove irrelevant distinctions | How to select a small sufficient set of implications for arbitrary speeds |

This answers the relational possibility precisely at the level supported by evidence. The shared-clock feasible set restricts which phase and lap combinations can coexist. Some of those restrictions are not recoverable from our chosen summaries. No extra dynamical interaction or new physical field is required by these results. An information-theoretic synergy value remains undefined, and an unrestricted “relationships force a gap” principle remains a hypothesis.

## 9. What remains a hypothesis or an open problem

- **A general relational obstruction to complete blocking:** structured families have candidates, but no arbitrary-speed/n obstruction has been established here.
- **Pair summaries within the physical class:** the abstract event obstruction proves a limit of unrestricted moment inequalities. Whether a particular pair-summary value admits physical schedules with different local clear duration requires a realization argument or an actual matched pair.
- **Topology as a forcing mechanism:** we have shown that summaries can lose topology. We have not shown that preserving every topological detail is necessary or sufficient for an efficient existence proof.
- **A small universally sufficient set of compatibility or contact constraints:** the one-triple exclusion and special window selectors demonstrate restricted success, not a universal bound on required information or work.
- **General window and reference selection:** making one local certificate exact does not imply that its window contains a solution, or that the selected reference covers all references.
- **Independent status:** exact finite calculations and elementary identities do not promote the accumulated unbounded AI-assisted proof candidates to independently reviewed results.

## 10. Three investigations with clear failure tests

### Priority 1: classify physical collisions in a deliberately small family

Keep the four matching pairs above as controls, including the now-explained duration sufficiency for x=2,8,21. Use x=11 as a next nontrivial anchor, where the original excluded-triangle example lives. With x fixed, each y-dependent moment is a constant leading term plus an endpoint-residue coefficient divided by y. The relevant rational endpoints permit a residue-based classification rather than a blind expansion of a speed scan.

Ask whether identical single/pair data can give different U. For the separate zero-duration question, use the x=3 branch: before adding y its only allowed point is 3/8, and y removes that point exactly when 8 divides y. Test whether complete moment collisions can cross that residue distinction. Preserve role labels, core/window/threshold, and common start. Exclude whole-configuration scaling as an explanation.

**Discriminating outcomes:** a physical matched counterexample proves insufficiency on that class; a complete collision classification showing the target always agrees proves a scoped sufficiency result. The x=2,8,21 constraint analysis shows the value of that negative outcome. The current 2,775-input search alone settles neither new anchor question.

### Priority 2: identify the smallest contact/ordering record that repairs a demonstrated loss

Use `(2,23)/(2,69)` to test ordering and component structure, and `(2,25)/(2,75)` to test the isolated contact. First test inexpensive arithmetic features already available, including pair gcds; distinguishing the examples is weaker than predicting their component structure. Add endpoint membership, active threshold phases, and crossing directions to selected lap cells only as needed. Reuse the 35/37 frozen-snapshot control and the core's third-controller example to challenge any two-runner rule.

**Discriminating outcomes:** a compact record that predicts the component/contact difference is useful; two cases with the same proposed record but different local behavior reject it. If the record must list every event to succeed, report exact reconstruction rather than a new compression or forcing principle. Closed safe-lap cells provide an existing exact benchmark.

### Priority 3: measure the value of added constraints before adding more detail

For four blockers, use 16 nonnegative exact-state masses. Fix the observed single/pair moments and minimize the empty-state mass. Then add only speed-justified constraints: forbidden triple states, lap incompatibilities, or implications such as B21 subset B6 union B7. This is a small linear feasibility/optimization model; an exact dual inequality can make any positive bound reviewable.

**Discriminating outcomes:** the existing 6/7/11/16 alternative already gives baseline optimum zero, while its actual forbidden triple repairs the opening certificate. Conversely, adding details that do not improve the best bound identifies irrelevant information for that target. A feasible zero-mass abstract model is still not a physical complete-cover construction. This experiment asks how much additional information is sufficient, not how many facts can be recorded.

No solver campaign, enlarged speed scan, outside review request, or next family extension was launched as part of these proposals.

## 11. Verification and continuity

```bash
python -B reviews/2026-09-25-lr2/check_distinction_audit.py --check
```

[Standalone script](../reviews/2026-09-25-lr2/check_distinction_audit.py) and [exact archive](../reviews/2026-09-25-lr2/distinction_audit.json). The archive pins the script hash and the digest of all 2,775 signature rows. It contains the four collision pairs, every moment/state duration for them, complete local components, isolated-contact controllers, the redundancy implication, both stress cases and safe-lap cells, the ratio controls, and the reproduced abstract alteration.

Signatures use periodic interval integration; component reconstruction separately partitions all threshold events with exact rational predicates and keeps valid endpoints. An additional session check with the existing closed-interval intersection checker agrees on all 14 actual-case component lists, including every isolated point. Its source SHA-256 is `ba240664c273d254d0ab8d2da053dc1248dd0b0a88cd5f1c4ed35a3f6c579971`. The standalone archived command does not import that checker. Historical evidence was not overwritten, and older tiling/global-overlap findings cited in the audit were reviewed from their existing records rather than all rerun.

The methodological principle is retained: **when the mathematics refuses an explanation, check whether two things have been conflated.** Add its useful counterpart: once a distinction is visible, test whether it changes the target. Both information loss and unnecessary detail can obstruct a good representation.
