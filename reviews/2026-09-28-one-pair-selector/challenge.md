# Adversarial review: one-pair selection and its separate fallback

September 28, 2026. Frozen protocol SHA256:
`36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e`.
The scope is eight common-start runners, reference 0, threshold 1/8,
and the ordered six supplied-core inputs in `protocol.json`. The core is
an input; this experiment does not solve core selection. All frozen
configurations have distinct positive nonreference speeds and global gcd 1.
Material AI involvement includes the mathematical and methodological
review and writing. General arguments retain HYPOTHESIS / proof-candidate
status; exact finite results have only their declared observed/reproduced
scope. No novelty claim or external proof certification is made.

## 1. What is genuinely tested

The rule commits to the widest core-safe component before seeing any
residual duration, then spends four single-duration calculations and at
most one exact pair query on that component. This differs from the old
selector that evaluated every pair on every component and selected the
largest bound. It remains a heuristic opening and pair selector, with a
separate endpoint route. An exact overlap evaluator does not make the
heuristic successful on all inputs.

The controls and their outcomes were known when the rule was designed.
Freezing the rule prevents further tuning during this campaign; it does
not make these controls blind or held-out validation. Separate numerical
implementations establish reproducibility, not independence of experimental
design. No success fraction should be interpreted as a probability of
success on arbitrary inputs.

"From the speeds" is not by itself an information restriction: a full
allowed-set reconstruction is also a function of the speeds. The useful
restriction here is the explicit operation contract. The primary must not
use an old benchmark or all-pair archive in its selection. Subsequent
benchmark comparison must remain a separate audit.

## 2. The cap test is a valid impossibility statement for one certificate

Write `L=|J|`, `E=sum(D_i)−L`, and
`C_*=max_{i<j}min(D_i,D_j)`. Every overlap satisfies

`O_ij <= min(D_i,D_j) <= C_*`,

while the grouped union bound gives `U_J>=O_ij−E`. Therefore `C_*<=E`
proves that **no one-pair lower bound can be positive on this selected
window**, without querying any overlap. It does not prove zero actual
duration, an empty allowed set, or failure of every tree certificate.
Equality in this cap test must be retained: a zero lower bound is not a
positive-duration certificate.

Conversely, `C_*>E` establishes only that the marginals permit a successful
pair. For the chosen pair, its real score is

`O−E = (C_*−E)−(C_*−O)`.

The cap surplus must exceed the cap loss caused by placement. Ranking a
cap is not ranking an overlap, predicting an overlap, or lower-bounding it.
Even after one query fails, the budget forbids trying the next pair.

The maximum cap equals the second-largest duration, but ties matter for
the selected labels. Enumerating and sorting all six pairs by the frozen
key is not always equivalent to simply selecting the two largest-duration
labels; a lexicographically earlier pair of tied durations may omit a
strictly largest-duration runner.

An unqueried overlap must remain null, not be represented by zero. In the
`E<0` branch, singles alone succeed. In the cap-ceiling branch, the reported
`−E` remains the singles lower bound, while `C_*−E` is an upper bound on
the best possible one-pair certificate score. These have different meanings.

The archived local ceiling control already demonstrates the distinction:
for core `{1,2,4}`, extras `{3,5,6,8}`, and `J=[9/32,7/16]`,
`E=1/20`, the best actual pair overlap is `1/24`, and every one-pair bound
fails. A tree nevertheless gives the exact positive duration `11/480`.
This is a local limitation of the certificate class, not merely choosing
the wrong edge. Selecting another window can be a different strategy,
but this frozen policy does not do that.

## 3. Signed residuals are an evaluation coordinate, not a selection score

For the already chosen pair `a<b`, let `h in {1,2}` minimize
`(abs(b−ha),h)` and let `r=b−ha`. If runner a blocks, write
`x=at−j in (−1/8,1/8)`. The other runner blocks precisely when

`|hx+rt−m|<1/8`

for an integer m. Thus the permitted x interval has endpoints

`ell=max(−1/8,(m−1/8−rt)/h)`,
`u=min(1/8,(m+1/8−rt)/h)`.

It has positive width only for `|rt−m|<(h+1)/8`. Since this radius is
at most 3/8, at most one integer m contributes at each time. Integrating
its width alone gives phase area, not actual overlap along x=at−j.

The complete affine changes occur at

`rt=m±(h+1)/8` and `rt=m±(h−1)/8`.

For h=1 the inner two events coincide and require deduplication. When
r<0 the time endpoints reverse order; sorting them and allowing negative
m preserves the strips. When r=0 division by r is invalid, but the
constant m=0 strip remains. Distinct a<b then forces h=2 and exact doubling.

The overlap primitive in `schema.md` and `arithmetic.md` has the correct
sign. Almost everywhere on a positive strip,

`1_pair = floor(at−ell)−floor(at−u)`.

With `P(z)=frac(z)(frac(z)−1)/2`, integrating its fractional-part remainder
gives strip area plus `W(u)−W(ell)`. For either endpoint slope s,

`a−s is a or a+r/h=b/h`,

which is strictly positive even when r is negative. One must retain signed
r in the endpoints and primitive arguments. Changing r to −r preserves
the kernel's width but need not preserve actual time occupancy.

Integer hits of the floor arguments and zero-width support boundaries have
zero duration; this justifies the measure formula only. It does not justify
discarding endpoints from the separate lonely-time predicate. The schema's
closed endpoint handling is necessary.

Choosing a small residual may reduce the number of strips used to evaluate
this pair. It does not make the pair's overlap larger or its net certificate
positive, and minimizing the residual does not prove optimal evaluation
cost. No new kernel-ranking experiment is performed here.

## 4. Endpoint recovery must not erase pair-path failures

If the duration path fails, the rule tests exactly the selected J's right
endpoint against all seven constraints. If valid, each runner has a unique
closed safe lap containing that time. Their common intersection is an
exact local certificate, obtained without reconstructing the full allowed
set. A positive-width intersection has strictly safe interior. A singleton
has opposing threshold directions and is only a point certificate.

This is a distinct mechanism from `O−E>0`. A successful endpoint interval
cannot retrospectively make the cap ranking successful, and an endpoint
contact cannot be counted as a positive-duration certificate. Reports need
separate fields for cap-class rejection, selected-query failure, endpoint
outcome, and final policy outcome, as the schema provides.

If the endpoint fails, the policy is uncertified even when an archived
strict interval lies inside its chosen window. It must not then test the
left endpoint, another component, another pair, a midpoint, or a tree.
The ordered campaign stops on the first **final uncertified policy
outcome**. It can legitimately continue after a pair-path failure rescued
by the prescribed endpoint, but that earlier pair failure remains visible.
Unrun cases must remain uncomputed, not merely omitted from the summary.

## 5. What the budget and evidence can establish

Four duration calculations use eight single primitive calls. An exact
overlap query can require many candidate strips, sorted residual events,
positive affine cells, and periodic primitive calls. The declared count
of four P evaluations per positive cell matches two endpoint corrections
with two endpoints each. Candidate events before filtering, duplicate h=1
events, and discarded cells also cost work and must be counted as stated.

The protocol additionally pays for constructing the supplied core's whole
closed safe set and for a possible seven-runner endpoint/lap check. The
counter contract is much more informative than saying "one query," but
reported rational operand sizes are not the maximum sizes of all transient
arithmetic and do not establish bit complexity. No uniform or measured
runtime speedup follows from these counts alone.

The input contract does not select a core and the frozen controls do not
test behavior under general changes of scale. Their global gcd is already
one. General symmetry or runtime claims would require an explicit broader
contract, not silent normalization changes in this campaign.

## 6. Review of the completed primary records and synthesis

The inspected `results.json` contains the six frozen cases in their
prescribed order. `select.py` chooses the window before residual evaluation,
executes at most one selected overlap call and one right-endpoint test per
case, and breaks immediately on an uncertified policy outcome. Its input
reads do not include the benchmark archives or a full allowed set. Reading
its own bytes for provenance and reading `results.json` for replay comparison
do not enter selection.

The outcomes agree with the synthesis:

| Case | Pair path | Endpoint route | Final result |
| --- | --- | --- | --- |
| fast_113 | 56/113: `1223/911232>0` | Not invoked | Positive duration |
| changed_core | 56/72: `2169/202496>0` | Not invoked | Positive duration |
| doubling_112 | 56/64: `59/16128>0` | Not invoked | Positive duration |
| tight_13 | 6/11: `−421/32032` | Singleton 3/8 | Point certificate only |
| one_pair_ceiling | No query: `C_*=E=1/20` | `[17/40,7/16]`, width 1/80 | Positive interval from endpoint |
| strict_16 | 6/11: `−171/9856` | 3/8 blocked by speed 16 | Uncertified; stop |

For the tight endpoint, speeds 5 and 13 require movement left while speed
11 requires movement right. Their shared safe-lap intersection is therefore
the recorded singleton. In the ceiling case, only speed 2 is at equality,
with its safe direction left; the recorded positive shared interval is
consistent with that orientation. No invalid endpoint is supplied with a
fabricated safe-lap intersection.

The selected-pair evaluator uses five queries, ten positive affine cells,
and forty P calls. The twice-used pair 6/11 is actually reevaluated and
charged twice; no unimplemented caching saving is claimed. The changed-core
query uses h=1,r=16; the 56/64 query uses h=1,r=8; 56/113 uses h=2,r=1;
and 6/11 exercises h=2,r=−1. These agree with the frozen representation key.

Two coverage limits of the finite test should remain explicit. No case
uses the `E<0` singles-only exit. Also, the input named doubling_112 selects
56/64, so the r=0 evaluator branch is not exercised by a frozen query.
Its handling has a supplied symbolic/code review, not a finite r=0 result
in this campaign. The first final failure occurs in the sixth and last
case, so there are no unrun cases; no earlier-stop savings are observed.

Most importantly, the old benchmarks show **no window in this batch where
the chosen pair fails but another pair would have a positive bound**. The
first three windows are one-pair-certifiable and the rule succeeds on them.
The last three are not one-pair-certifiable. This defeats a universal claim
for the whole policy but does not supply a counterexample to the narrower
claim that cap ranking finds a useful pair whenever one exists on its
chosen window. Nor do three known successes prove that narrower claim.

For strict_16 the archived best pair gives `−169/14784` and the best tree
gives `−23/29568`, while actual local duration is `1/896`. The older
`ULTRA_REVIEW_2026_09_25.md` also supplies an abstract complete-cover
arrangement with all the same singles and pair totals. Therefore generic
event inequalities using just those totals cannot force this opening.
This is not a second physical runner realization. Extra runner geometry,
such as the already established triple exclusion, or a different window
can explain the physical opening; neither is part of the frozen fallback.

The synthesis's marginal-cap sharpness argument is sound: nested abstract
measurable sets of the prescribed individual durations attain every pair
cap. It correctly does not assert that those sets are realizable by these
runner speeds. The proposed next question must likewise preserve the
difference between proving a structural exclusion cheaply, choosing when
to request it, and guaranteeing that some available certificate succeeds.

No remaining mathematical, endpoint, or policy-budget correction was found
in the inspected schema, arithmetic/structure reports, primary records, or
`notes/ONE_PAIR_SELECTION_2026_09_28.md`. This report independently derives
and reviews the implications; the separately structured verifier owns the
finite reconstruction and reports its comparison status. No additional
case, full seven-runner reconstruction, alternate query, or new computation
outside the frozen scope was introduced here.
