# Adversarial mathematical review: duration collisions and contacts

Date: 2026-09-27. Reviewer: a separately tasked AI reviewer in the six-reviewer Ultra exercise. Material AI involvement includes this reasoning, implementation, and report. This is not independent human certification, a novelty audit, or promotion of any candidate to established status.

The parent supplied pinned baseline `e94a87f650264826569cae63412c43a5175f5ae4`. The working directory is an API-synced snapshot, not a Git checkout; I did not independently verify its remote Git tree. Exact SHA-256 hashes of every substantive input used here are in `rigor_check.json`. I wrote only this report and its accompanying `rigor_check.py` / `rigor_check.json`.

## Outcome and scope

I found no fatal mathematical defect in the scoped claims of `DISTINCTION_AUDIT_2026_09_25.md`, `RESIDUE_COLLISIONS_2026_09_27.md`, or `CONTACT_MOMENTS_2026_09_27.md`. In particular, the two successive physical information-loss conclusions survive a separately structured exact reconstruction:

| Fixed extra speeds; variable speeds | Retained data | Different target |
| --- | --- | --- |
| 6,7,11; 45 versus 90 | All labelled single/pair durations on J | U=1/210 versus 31/5040 |
| 6,7,11; 266 versus 532 | Those durations and all blocker-pair gcds | U=13/2128 versus 1/152 |
| 3,10,28; 1680 versus 3360 | Every subset duration and every nonzero-relative-speed pair gcd | F_J={9/32} versus empty |

Throughout this report, J=[9/32,3/8], the selected reference has speed zero, core speeds are 1,4,5, there are eight common-start runners, and equality at 1/8 is safe. These restrictions are essential. These examples neither contradict Lonely Runner nor establish a general window-selection theorem.

The finite evidence additionally reproduces all 118 nonzero residue-pair families for fixed 6,7,11, all 34 for fixed 6,7,3, their separate zero-vector classes, and the original 2,775-input collision classification. The unbounded implications have a correct-looking finite reduction; they retain the repository's proof-candidate status.

## Independent reconstruction

The new verifier imports only Python's standard library and does not import any reviewed script or project checker. It constructs each runner's blocked intervals and closed safe intervals directly from integer laps. It obtains all 16 joint moments by interval intersection, obtains exact-state masses by Boolean-lattice inversion, and obtains complete allowed components by repeated closed-safe-interval intersection. This differs from the archived moment checks, which partition threshold events and classify midpoint states.

For the infinite residue reductions I used the unshifted primitive

`A(z)=floor(z)/4 + min(frac(z),1/8) + max(0,frac(z)-7/8)`.

Thus A(0)=0; it differs from the note's C by a constant. Its derivative is the strict blocking indicator away from finitely many boundaries. I evaluate rational endpoint corrections directly, with no copied integer correction table. Proportional rows are normalized by the magnitude of their first nonzero entry. To solve matching-speed congruences, I solve each linear congruence separately and combine them by generalized CRT, rather than using the archived simultaneous Bezout formula or enumerating k. The resulting complete family records match the archives exactly.

The check reconstructs 35 physical cases and compares 27 against every archived moment, exact-state mass, and local component list from the two latest notes. The other eight are the four earlier distinction-audit pairs. It separately reconstructs all 2,775 earlier signatures by interval intersections. A bounded denominator check covers y=1,...,8192; the unbounded denominator conclusion instead rests on the argument below.

## The duration-loss examples

Fixed blockers 6,7,11 leave `[17/56,5/16] union {3/8}`. Since B6 and B7 are disjoint, every triple containing both and every quadruple intersection vanish. Inclusion-exclusion consequently becomes

`U=|J|-sum(D_i)+sum(O_ij)-H`,

where `H=|B6 intersect B11 intersect By|+|B7 intersect B11 intersect By|`.

For 45 versus 90, the first triple has lengths 1/720 and 0, respectively; the second vanishes for both. The first triple for 45 is `(127/360,17/48)`. Doubling the speed moves the relevant lower blocking endpoint to 17/48, meeting the end of B6 without creating positive triple overlap. All single/pair totals remain equal. Hence U increases by exactly 1/720. The complete local sets are

* y=45: `[17/56,37/120] union {3/8}`;
* y=90: `[17/56,223/720] union {5/16,3/8}`.

The extra point 5/16 in the second case is real: speed 90 enters safety exactly as speed 6 leaves it. A duration computation alone must not claim to have enumerated these points.

For 266 versus 532, the respective first triple durations are 1/1064 and 1/2128; the second is 1/1064 in both. The change is 1/2128. The variable blocker has gcds (2,7,1) with (6,7,11) in both cases. This is genuinely stronger than the 45/90 example, but it does not preserve gcd with core speed 4: those values are 2 and 4. The note states this limitation correctly.

The one-scalar repair `|By intersect [17/56,5/16]|` is sufficient for U because the displayed interval is the entire positive-measure opening of the fixed constraints. It is configuration-dependent information. Its simplicity here gives no bound on the complexity of analogous openings for arbitrary inputs.

## Why the residue classifications are complete within their domains

Let `q_r` be a correction vector for the four variable single/pair statistics. Endpoint rationality gives the exact identity

`M(y)=M0+q_(y mod P)/y`.

It follows that equality requires `q_r/y=q_s/z`. For nonzero vectors and positive speeds, this requires a common signed ray, not merely a common line. If their magnitude ratio reduces to coprime a:b, every equality has y=ak, z=bk. Thus the only remaining problem is

`ak=r mod P, bk=s mod P`.

Because gcd(a,b)=1, the combined congruence is solvable exactly when `br=as mod P`; if solvable, its solution k is unique modulo P. For sufficiency, choose u,v with ua+vb=1 and set k=ur+vs: multiplying by a or b and using the compatibility congruence returns r or s. This also proves uniqueness by applying u,v to the difference of two solutions. My separate CRT implementation agrees with every archived parameterization.

The complete counts reproduce as follows:

| Domain | Period | Nonzero rays | Same-ray residue pairs | Admissible nonzero families | Zero residues |
| --- | ---: | ---: | ---: | ---: | --- |
| Fixed 6,7,11 | 7392 | 5186 | 3240 | 118 | 0,3696 |
| Fixed 6,7,3 | 672 | 534 | 168 | 34 | 0,336 |

For the first row, 62 families change U, 46 preserve all blocker-pair gcds, and eight do both. For the second, 12 families have empty J and 22 retain {3/8}. First admissible parameter values, including exclusions of repeated fixed speeds, agree with the archives. The smallest first-row pair is 45/90.

The zero vector needs its own treatment: it can match every other zero-vector speed, but never a nonzero correction. These are precisely the multiples of 3696 and 336 in the respective domains. A nonzero residue cannot yield distinct speeds with identical summaries at that same residue; dividing its fixed nonzero vector by different positive speeds changes the vector. Thus there is no omitted same-residue family.

These are counts of residue-pair families, not independent discoveries or necessarily disjoint equivalence classes. Completeness applies to changing one positive integer speed with the specified three fixed blockers, fixed role labels, fixed window and threshold. It is not a classification of arbitrary physical moment collisions.

All matched speeds in the first classification are at least 45. For y>28 a connected y-blocking interval has length 1/(4y)<1/112. It cannot cover the fixed positive interval S; using multiple blocking intervals necessarily leaves a positive safe gap between them. Hence every classified collision member has U>0. The earlier zero-duration cases y=3,10,13,26 remain valid, have isolated equality, and have no distinct matching summary in this classification.

## The denominator exclusion is valid, and sharper than generic measure rhetoric

Write D_y=p/q in lowest terms. If 8 does not divide y, every clipped blocking endpoint has denominator dividing lcm(8y,32), whose 2-adic valuation is at most five. The reduced q therefore cannot contain 64.

If 16 divides y, the scaled window endpoints are integers or half-integers. The periodic correction `A(z)-z/4` vanishes at both phase 0 and phase 1/2, so D_y=3/128 and the reduced denominator has exactly seven factors of 2.

For y=8h with h odd, the scaled left endpoint is 9h/4, with fractional part 1/4 or 3/4, and the right endpoint is the integer 3h. Here A(n+1/4)=A(n+3/4)=n/4+1/8, whereas A at an integer m equals m/4. The scaled blocked length is therefore an odd multiple of 1/8; division by 8h gives reduced denominator with exactly six factors of 2. Equivalently, direct calculation yields `(3h-1)/(128h)` for h=1 mod 4 and `(3h+1)/(128h)` for h=3 mod 4; the numerator has exactly one factor of 2.

Therefore `64 divides denominator(D_y)` iff `8 divides y`. At 3/8, an integer-speed runner strictly blocks iff 8 divides its speed. The labelled single duration already identifies safety at this particular endpoint, even when the other speeds change. Thus “durations assign no mass to points” alone does not prove that they cannot indirectly identify a point in a restricted physical class. The note handles this subtlety correctly.

The exact criterion is not uniformly stable under absolute measurement error. The 672m versus 672m+1 construction gives opposite outcomes with maximal moment discrepancy `3/[128(672m+1)]`. This is a separate issue from the exact collision in the next section.

## Complete moments and gcds still lose local existence

The fixed blockers 3,10,28 cover the open interior of J, retaining both endpoints. The first B28 interval overlaps B10, and B10 overlaps B3, so there is no hidden interior gap. The relevant endpoint denominators divide 3360. For y=1680h, every fixed-region endpoint has integer or half-integer scaled phase. Since the periodic correction takes the same value at those phases, the blocked duration in every fixed atom is exactly one quarter of that atom's length.

Consequently all joint moments and exact-state masses remain fixed. A useful sharpened interpretation is that, for uniformly sampled t in J, the Boolean event “the variable runner blocks” is exactly Bernoulli(1/4)-independent of the complete fixed Boolean blocking-state vector. This is independence of these observables, not of physical phases, trajectories, or successive times. No statistic obtained by integrating an arbitrary function of this same instantaneous Boolean state can distinguish the examples; higher algebraic order cannot fix this information loss.

At the remaining candidates,

`y(3/8)=630h`, and `y(9/32)=945h/2`.

The right endpoint is always blocked. The left endpoint has phase 1/2 for odd h and 0 for even h, giving exactly the claimed alternation. Every fixed speed divides 1680, so all 21 gcds among the seven nonzero relative speeds stay unchanged for all h. Including gcd(0,y), reduced ratios, or the variable speed itself would distinguish the configurations; those are not the compressed data under test.

At the retained left contact, speed 4 supplies the lower closed-safe bound and speed 28 the upper bound, both at 9/32. For odd h the variable safe lap `(945h-1)/2` includes the contact strictly. For even h the variable runner fails there. This confirms a genuine feasible singleton rather than an endpoint accidentally retained by an open/closed convention.

The arithmetic reviewer independently develops the general rational-partition version and a full-period extension of this aliasing mechanism; those extensions are intentionally not duplicated here. The local state-independence conclusion above already follows from the reviewed argument.

## Earlier audit and implications

The original bounded search has exactly 2771 labelled signatures on 2775 inputs and exactly the four archived pairs. The first three have all moments equal; the x=21 pair preserves pair moments but redistributes triples without changing their sum. All four change complete allowed components but retain positive U. Thus their old negative statement about different-U matches within y<=80 was correct; 45/90 does not invalidate it.

The redundancy claim for speed 21 is also pointwise correct: both its blocking pieces lie strictly within the corresponding 7- or 6-blocking pieces, while speed 2 never blocks J. Replacing 2 by 21 therefore changes no allowed point after adding any common admissible fourth blocker. More detailed data are not automatically more relevant data.

The strongest useful consequence is an explicit separation of research targets. A pair-duration certificate needs additional joint-occupancy information to compute U in the 45/90 example. A complete duration certificate already contains all that information but still needs a contact supplement to decide local nonemptiness in the 1680/3360 example. The denominator result simultaneously warns that such supplements may sometimes be inferred indirectly from existing exact data. A next proposed summary should state its admissible physical class and target first, then be tested on all three controls rather than justified by informal claims about “pairwise information” or “missing topology.”

## Reproduction, provenance, and limits

From the snapshot root:

```bash
python -B reviews/2026-09-27-ultra/rigor_check.py --check
```

Expected result: PASS, 35 physical cases, 27 complete archived-case comparisons, both full classification records matched, and no denominator failure in 1..8192. The JSON also records the independent 2775-input audit search, complete local moments/states/components, and input/script hashes. The `--check` mode is read-only: it recomputes all mathematical evidence, compares it with the archive, and verifies that the archived review-script hash matches the current script. Recorded input hashes describe the reviewed baseline; they are not freshness checks, so later governance updates to HANDOFF, CLAIM_STATUS, README, and similar files do not invalidate the mathematical replay. Default invocation without `--check` rewrites only its own `rigor_check.json` while preserving those baseline input hashes.

Inputs read: AGENTS, README, CLAIM_STATUS, CONTRIBUTING, current HANDOFF, the three named mathematical notes, their standalone primary verifiers, both latest crosscheck scripts, and the three primary archives. All substantive inputs are hashed. No original notes, scripts, archives, handoffs, GitHub objects, or external messages were changed. I did not run the whole project regression suite, audit the general Lonely Runner literature, inspect a formal proof assistant translation, or verify remote tree provenance. This is exact reproduced evidence plus line-by-line mathematical review within the stated scope, with the repository's independent-review and novelty limitations preserved.
