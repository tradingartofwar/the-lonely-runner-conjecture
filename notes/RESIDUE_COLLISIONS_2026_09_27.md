# Physical matches that change lonely duration

September 27, 2026. Continuation of Priority 1 in the [distinction audit](DISTINCTION_AUDIT_2026_09_25.md). Baseline: `f4eecb08eeb790064536551b2bbd44706a7c4a38`. Material AI involvement: derivation, exact computation, counterchecks, and writing.

**Result:** two actual common-start configurations can have identical labelled individual and pairwise blocking durations in the chosen window, yet different lonely duration. The smallest matching pair in the fixed-speed-11 family uses **45 and 90**. The **266/532** pair also preserves every pair gcd among the four extra blockers. This answers the physical-realizability question left open by the earlier abstract state-mass alteration.

**Status:** the concrete examples and finite residue table are **OBSERVED**, with separately structured exact checks. The proposed sufficiency of these local pair-duration summaries for U is **DISPROVEN** by the examples; adding blocker-pair gcds is also insufficient. The complete unbounded classification below is a **HYPOTHESIS/proof candidate** with a finite reduction and exhaustive arithmetic certificate, awaiting independent review. No novelty or general Lonely Runner result is claimed.

## 1. Exact scope

Keep velocities `{0,1,4,5,6,7,11,y}`, with positive integer y outside `{1,4,5,6,7,11}`. All eight runners start together. Select reference 0, threshold `1/8`, core `{1,4,5}`, and `J=[9/32,3/8]`. Equality counts. Only y changes; this is not a rescaling of the whole configuration.

For the extra blockers labelled `(6,7,11,y)`, let `B_v={t in J: ||vt||<1/8}`, `D_v=|B_v|`, and `O_vw=|B_v intersect B_w|`. The core never strictly blocks on J, so its local single/pair moments are zero. Thus matching all four extra singles and six extra pairs also matches all such local moments among the seven nonreference runners.

The variable part of that labelled summary is exactly

`M(y)=(D_y,O_6y,O_7y,O_11y)`.

All other entries are fixed. These are local durations, not full-period overlaps, reduced speed ratios, or a complete arithmetic description.

## 2. The decisive physical pair

The configurations with y=45 and y=90 have the following identical data:

| Quantity | Both configurations |
| --- | ---: |
| D6 | 1/24 |
| D7 | 5/224 |
| D11 | 9/352 |
| Dy | 1/45 |
| O6,7 | 0 |
| O6,11 | 1/528 |
| O7,11 | 1/352 |
| O6,y | 1/120 |
| O7,y | 1/180 |
| O11,y | 1/180 |

Yet their complete local allowed sets differ:

| Variable speed | Complete allowed set in J | U |
| --- | --- | ---: |
| 45 | `[17/56,37/120] union {3/8}` | 1/210 |
| 90 | `[17/56,223/720] union {5/16,3/8}` | 31/5040 |

The second has exactly `1/720` more positive duration. Both still have valid isolated equality points; these are preserved in the certificates, not inferred from measure.

Speed 90 was outside the audit's earlier y<=80 domain, so this does not contradict its bounded negative result.

The missing correction is explicit. Since B6 and B7 are disjoint, every quadruple intersection and both triples containing 6 and 7 vanish. Write

`H(y)=T_(6,11,y)+T_(7,11,y)`.

Then `U=-E+P2-H`, where `E=sum(D)-|J|` and P2 is the sum of all six pair durations. For these two configurations,

| Quantity | y=45 | y=90 |
| --- | ---: | ---: |
| E | 1999/110880 | 1999/110880 |
| T6,11,y | 1/720 | 0 |
| T7,11,y | 0 | 0 |
| R=P2-H | 361/15840 | 383/15840 |

The triple for 45 occurs on `(127/360,17/48)`. For 90, the relevant blocking occurrence starts at `17/48`, exactly where B6 ends. Boundary contact replaces interior triple overlap. All pair totals remain the same, while their simultaneous placement changes.

This supplies the missing physical counterexample. The earlier 6/7/11/16 abstract alteration remains useful evidence about unrestricted event models, but need no longer carry the claim that actual runner pair-duration summaries can lose U. Neither example is a counterexample to Lonely Runner.

## 3. Repetition frequency does not repair these summaries

The next smallest match uses y=266 and y=532:

| Variable data | Both configurations |
| --- | ---: |
| Dy | 25/1064 |
| O6,y | 11/1064 |
| O7,y | 3/532 |
| O11,y | 1/152 |
| gcd(6,y), gcd(7,y), gcd(11,y) | (2,7,1) |

The fixed singles, fixed pairs, and fixed gcds agree automatically. Nevertheless,

| Quantity | y=266 | y=532 |
| --- | ---: | ---: |
| T6,11,y | 1/1064 | 1/2128 |
| T7,11,y | 1/1064 | 1/1064 |
| U | 13/2128 | 1/152 |

The difference is `1/2128`. Thus even the pair repetition periods determined by gcds **among these four blockers**, together with all their local single/pair durations, do not determine U.

Do not broaden the match: `gcd(4,266)=2` whereas `gcd(4,532)=4`, and the reduced speed ratios also differ. We have not matched every arithmetic statistic used anywhere in the project. Ratio plus gcd still reconstructs an entire pair of speeds. The tested compression is local duration plus blocker-pair repetition data.

## 4. Recovering the lost quantity

The fixed blockers are

`B6=(5/16,17/48)`,

`B7=[9/32,17/56)`,

`B11=[9/32,25/88) union (31/88,3/8)`.

Their complement in J is exactly `S union {3/8}`, with `S=[17/56,5/16]` and `|S|=1/112`. Therefore

`U(y)=1/112-|B_y intersect S|`.

Two equivalent one-scalar repairs are now concrete: retain H, the total necessary triple correction, or retain y's blocked duration inside the **simultaneous opening of the fixed runners**. The latter is an overlap with a configuration-defined set, not with an individual runner. This makes relational information precise without assuming a new physical field.

For this family, S is just one interval, so the quantity is cheap to compute by endpoint integration. No claim follows that the simultaneous opening of an arbitrary collection has bounded complexity. Recovering U also does not recover component arrangement or isolated contacts; those still require boundary information.

## 5. Finite reduction for every positive integer speed

Define a blocking primitive and its periodic correction by

`C(z)=floor(z+1/8)/4+min(frac(z+1/8),1/4)`,

`psi(z)=C(z)-z/4`.

C has the blocking indicator as its derivative away from threshold points, and `C(z+1)=C(z)+1/4`, so psi is 1-periodic. For a finite interval union A,

`|B_y intersect A|=|A|/4 + (1/y) sum_[a,b]inA (psi(yb)-psi(ya))`.

All endpoints in J, B6, B7, B11, S, and the two fixed overlaps have denominators dividing

`P=lcm(32,48,56,88)=7392`.

Consequently there are integer coefficient vectors e(r), `0<=r<P`, such that

`M(y)=M0+e(r)/(4Py)`, where `r=y mod P` and `M0=(|J|,|B6|,|B7|,|B11|)/4`.

Let c(r) be the corresponding coefficient for S. Then

`U(y)=3/448-c(r)/(4Py)`.

This is exact at every positive integer speed, including small speeds. Open versus closed integration endpoints do not affect duration; the full allowed sets are checked separately.

### Exhaustive equality test

For nonzero e(r), set `g_r=gcd` of its four integer coordinates, taken positive, and retain the signed primitive vector `e(r)/g_r`. Equality `M(y)=M(z)` requires the same primitive vector. Opposite signs do not match at positive speeds.

For residues r,s with the same vector, reduce `g_r:g_s` to coprime positive integers a:b. Then all possible matches have

`y=a k`, `z=b k`, with `a k=r mod P`, `b k=s mod P`.

These congruences are solvable exactly when `b r=a s mod P`. If `u a+v b=1`, the unique solution modulo P is `k=u r+v s mod P`. This proves both completeness and a finite test. Every positive k in that residue class is admitted except where y or z repeats a fixed speed. The archive records the first admissible k; six families skip a forbidden small member. Equal multipliers at distinct residues cannot match. At one nonzero residue, equal summaries force y=z, which is not a distinct-configuration match.

The only zero-vector residues are 0 and 3696, and both have c=0. They give one further infinite equivalence class: all positive multiples of 3696 share the same M and `U=3/448`. A nonzero vector cannot match this class.

This reduces the unbounded question to the complete 7392-row table, with no arbitrary upper speed cutoff.

## 6. Classification and its limits

The exact table has 5186 nonzero signed primitive vectors. There are 3240 unordered pairs of residues sharing one of those vectors. Exactly **118** distinct-residue pairs satisfy the congruence condition, each giving an infinite family of matching speed pairs.

| Nonzero collision families | Count |
| --- | ---: |
| Different U | 62 |
| Equal U | 56 |
| Same blocker-pair gcds | 46 |
| Same blocker-pair gcds and different U | 8 |

These are residue-pair classes, not 118 independent mathematical mechanisms. The additional zero-vector equivalence class is counted separately.

The first two families are particularly simple. For every integer m>=0:

1. Set `y=45+7392m`, `z=2y`. All pair-duration summaries match, but `U(z)-U(y)=1/(16y)`. More explicitly, `U(y)=3/448-39/(448y)` and `U(z)=3/448-11/(448y)`.
2. Set `y=266+7392m`, `z=2y`. The blocker-pair gcds also match, but `U(z)-U(y)=1/(8y)`. Here `U(y)=3/448-5/(32y)` and `U(z)=3/448-1/(32y)`.

The pair 45/90 minimizes `max(y,z)` over all distinct admissible matches in this fixed family. This is not a minimality claim over arbitrary runner configurations.

Useful negative controls are retained: 336/1344 has matching pair moments and equal U despite different higher moments; 3696/7392 matches every joint duration moment and U. Their complete component lists are archived too. Higher-order differences need not always change the target.

**No existence distinction appears among these matches.** Every member of a matching pair has speed at least 45. For any y>28, each connected y-blocking interval has length `1/(4y)<|S|`; the connected interval S cannot be covered in measure by those separated intervals. Hence U>0. Exact checks of the 22 admissible speeds through 28 find zero U only at y=3,10,13,26; each retains equality times, and none has a distinct matched summary in the classification. Thus this experiment separates positive amounts of lonely time, not positive duration versus zero, or empty versus equality-only allowed sets.

## 7. Reproduction and counterchecks

```bash
python -B reviews/2026-09-27-lr2/check_residue_collisions.py --check
python -B reviews/2026-09-27-lr2/crosscheck_residue_controls.py --check
```

The [standalone classifier](../reviews/2026-09-27-lr2/check_residue_collisions.py) uses only the standard library. The [exact archive](../reviews/2026-09-27-lr2/residue_collisions.json) pins its source hash, the complete residue-table digest, all 118 family parameterizations, the zero class, all state masses and moments of eight physical controls, and the four equality cases.

Verification is targeted at the reduction and the claimed distinction:

- The integer periodic correction agrees with the rational primitive at every one of the 7392 grid points. Every residue row also agrees with rational endpoint integration in all seven relevant regions.
- The congruence criterion is checked by independently enumerating k modulo P for every distinct-multiplier candidate pair. Each admitted family is additionally checked by rational endpoint integration at its first two admissible parameters. These checks supplement the all-k derivation; they do not replace it.
- Direct threshold-event partitions independently recover all moments and complete components of the eight physical controls and the 22 small-speed cases.
- The [separate comparison](../reviews/2026-09-27-lr2/crosscheck_residue_controls.py) uses the existing closed-safe-interval intersection checker on all eight physical controls and four equality cases. All 12 complete component lists and durations agree. The [comparison archive](../reviews/2026-09-27-lr2/residue_checker_comparison.json) pins the checker and all local dependencies by SHA-256.

No old source, checker behavior, or historical output changed. The existing draft research branch remains the review location. This continuation did not run a solver campaign, reopen the parked +7/+9 extension, or make an outside publication or review request.

## 8. Next discriminating question

**Follow-up completed later September 27:** [CONTACT_MOMENTS_2026_09_27.md](CONTACT_MOMENTS_2026_09_27.md) preserves the result. The fixed 6/7/3 family rules out the proposed match: the reduced denominator of D_y alone identifies safety at 3/8. Its full-moment 336/672 control does lose left-endpoint safety, masked by runner 7. Changing the fixed triple to 3/10/28 makes that loss decisive: y=1680 and 3360 have identical complete moments, exact-state durations, and all pair gcds among the seven nonzero relative speeds, but F_J={9/32} versus empty. All y=1680h share those statistics while local existence alternates with h's parity. The question below is retained as the prompt that led to this completed follow-up.

The duration-loss question now has a physical answer, including a blocker-gcd control and infinite families. Do not repeat a wider speed scan for that purpose.

The next unresolved distinction is **existence at zero measure**. Use the previously identified x=3 branch: its fixed-runner allowed set in J is `{3/8}`, and adding y removes it exactly when 8 divides y. Ask whether two actual configurations can match **all joint duration moments** while landing on opposite sides of that endpoint test. An exact residue reduction can either find a physical empty/contact pair or show why this restricted family rules one out. The 16-state constraint-value experiment remains another option, now with physical matched-duration controls available.
