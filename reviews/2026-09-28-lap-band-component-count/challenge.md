# Adversarial review: lap-band component count

September 28, 2026 UTC. Reviewed against the frozen protocol at baseline
`bf5795ed41c06fc45be02f7b7c3a2c273de27749`, the archived one-containment
selector, and the earlier lap-labelled and sparse-selector notes. This is an
internal AI review, not independent mathematical validation.

## Verdict

**No fatal defect in the frozen candidate lemma, provided its proof makes two
currently implicit facts explicit.** First, the Helly step needs
*positive-length pairwise intersections* of the window and the two open lap
intervals, not merely intersection of their closures. Second, the bijection
from lap pairs to connected components uses `delta<1/2`, which makes the lap
label of a blocking runner unique. With `delta=1/8`, positive integer distinct
speeds and a nondegenerate closed rational window, both facts hold.

The proposed count is therefore an exact lattice-point reformulation of the
component count. It is not a new selector result, a held-out validation, a
constant-time or speed-independent shortcut, or evidence that the selector
generalizes. It replaces interval-object construction by an iteration over the
smaller speed's participating lap labels. Across many pairs, that iteration can
repeat work that a cached interval construction would share.

The final note and results should make the corrections and limits below
explicit.

## 1. Exact derivation and endpoint attack

For speed `v>0` and integer lap label `q`, write

`I_(v,q) = J intersect ((q-delta)/v,(q+delta)/v)`.

This set has positive length exactly when

`vL-delta < q < vR+delta`.

For `a<b`, the two uncut open lap intervals have positive overlap exactly when

`(m-delta)/a < (n+delta)/b` and
`(n-delta)/b < (m+delta)/a`,

equivalently

`|b*m-a*n| < delta*(a+b)`.

The two participation inequalities say that each open lap interval overlaps
`J` in positive length. The band inequality says the two open lap intervals
overlap each other in positive length. Three intervals on the line whose three
pairwise intersections have positive length have a positive common
intersection: if `ell` is their greatest lower endpoint and `u` their least
upper endpoint, either they come from the same interval, where `ell<u`, or the
corresponding pair's positive intersection gives `ell<u`. This is the precise
one-dimensional Helly step needed here.

Closed window endpoints do not justify changing any inequality to non-strict.
A lap ending at `L` has no blocked time in `J`, while a lap beginning at `L`
can have positive blocked time immediately to the right. The stated strict
participation bounds distinguish these orientations correctly. Likewise,
band equality is only threshold contact and contributes no duration.

Two exact boundary controls:

- With `delta=1/8`, `a=3`, `b=5`, `m=1`, `n=2`, the determinant is
  `|5*1-3*2|=1=delta*(3+5)`. The open laps meet only at `t=3/8`, where both
  distances equal `1/8`; there is no positive pair component. The strict band
  correctly rejects it.
- With speed `1`, lap `0`, and `J=[1/8,1/4]`, the lap ends at the left window
  endpoint and contributes nothing: `L-delta=0=m`, so the strict lower
  participation test rejects it. By contrast, a lap whose left threshold is
  `L` satisfies the participation inequalities and contributes immediately to
  the right. Thus window clipping does not create an off-by-one exception.

For fixed eligible `m`, intersecting the `n`-participation interval with the
band interval gives exactly the frozen

`lower=max(bL-delta,(b*m-delta*(a+b))/a)`,

`upper=min(bR+delta,(b*m+delta*(a+b))/a)`.

The integer count in the open interval is

`max(0,ceil(upper)-floor(lower)-1)`.

This handles integral lower or upper endpoints correctly. For example,
`(0,3)` contains two integers and gives `ceil(3)-floor(0)-1=2`; `(0,3.2)`
contains three and gives `4-0-1=3`.

## 2. Why lap pairs really count components

The proof must not stop after counting nonempty lap-pair intersections. For a
blocking time `t`, `||vt||<delta<1/2` determines a unique integer nearest to
`vt`, hence a unique lap label. Therefore a time cannot lie in intersections
from two distinct `(m,n)` labels. Each surviving labelled intersection is
itself an interval and hence one connected component. Distinct labelled
intersections cannot join through a threshold point because blocking is strict;
there is in fact a positive same-runner safe gap between consecutive blocking
laps when `2*delta<1`. This supplies the claimed bijection.

Common divisors do not break the argument. They can make determinant patterns
repeat at translated times, but the translated occurrences have different lap
labels and remain different components. Duplicate absolute speeds would need a
separate statement: the frozen domain uses `a<b`, so equal-speed labelled
runners are outside this lemma rather than silently covered by it. The result
should not be exported to `delta=1/2`, where uniqueness/gap reasoning changes.

## 3. Independent spot calculations

Direct exact arithmetic from the windows and speeds, without reading archived
component tables, gives the following pair counts:

| Case | Pair counts in physical-speed lexicographic order | Frozen selector consequence |
| --- | --- | --- |
| target `{15,38,61,100}` | `1,1,1,2,2,3` | eligible pairs are `{15,38}:1` and `{61,100}:3`; select `{15,38}` |
| strict16 `{6,7,11,16}` | `0,1,1,1,0,1` | eligible `{6,11}` and `{11,16}` tie at 1; lex selects `{6,11}` |
| doubling112 `{56,64,72,112}` | `2,3,6,3,5,4` | all eligible; select `{56,64}` diagnostically after the pair-only exit |
| tight13 `{6,7,11,13}` | `0,1,1,1,1,0` | no positive-slack pair, so there is no selector decision |

Representative exact rows also attack the floor/ceiling implementation:

- target `{15,38}` has only `m=3`; its clipped `n` range is
  `859/120<n<193/24`, containing only `n=8`;
- target `{61,100}` has the three surviving labels `(11,18)`, `(12,20)`,
  `(13,21)`;
- strict `{11,16}` has candidate `m=3` with no integer in
  `(35/8,411/88)` and `m=4` with only `n=6` in `(485/88,49/8)`;
- doubling `{56,112}` has the six pairs `(m,2m)` for `m=16,...,21`;
- tight `{11,13}` has no integer in either candidate row, so its count is zero.

These agree with the archived interval-derived counts where those counts were
eligible and visible. Agreement is a check of the representation, not fresh
evidence for the selector's success.

## 4. Required scope and cost corrections

1. **Say “no interval-list construction,” not “no geometry.”** The determinant
   strip is exactly the overlap geometry expressed arithmetically. The primary
   still examines every participating `m` of the smaller speed and performs
   rational window/band clipping for that row.
2. **No uniform cheapness claim.** The row count is on the order of
   `a*(R-L)+O(1)` for the chosen smaller speed `a`; it can grow with speed and
   window length. The integer count formula does not mathematically require
   enumerating the surviving `n` labels, but the primary implementation does
   materialize all 41 of them as inspectable certificates. It avoids storing
   interval objects; that alone does not establish a runtime improvement.
   Also, smaller physical speed is only a deterministic iteration convention,
   not a theorem that it always has fewer clipped labels: for `a=8`, `b=9`,
   `J=[1/8,1/4]`, the smaller speed has candidate labels `{1,2}` while the
   larger has only `{2}`.
3. **Account for caching and repeated work.** Across all six pairs of a
   four-runner window, an interval implementation can construct each runner's
   blocking laps once and reuse them. A pairwise lap-band implementation can
   rescan the same smaller-speed `m` rows for several partners. Any cost table
   should distinguish arithmetic rows, rational comparisons, and storage from
   a claimed asymptotic speedup.
4. **Separate validation overhead from selector charge.** The primary computes
   all 24 physical pair counts for checking. Ten pairs have positive slack,
   but six of those belong to doubling112 after its pair-only exit and are
   classified as diagnostics. Thus the artifact reports four active
   selector-charged pairs, six diagnostic eligible pairs, and fourteen
   ineligible audit pairs. This is a reasonable resolution of the protocol's
   competing phrases “exactly the pairs with positive slack” and “doubling112
   remains a diagnostic,” but the note should preserve all three counts rather
   than call all ten active selector costs.
5. **Do not overread the controls.** Doubling112 exits on its independent
   pair-only certificate before selection, so its chosen pair and failed
   containment are diagnostics. Tight13 has no eligible pair, and its isolated
   valid point `t=3/8` is not represented by positive component counts.
   Ineligible zero-count pairs in strict16 and tight13 must not be allowed to
   bypass the frozen positive-slack eligibility rule.
6. **Preserve the development-case warning.** The target's successful
   one-component pair, the competing three-component pair, and the selector
   outcome were known before this protocol. Reproducing that ordering through
   an exact equivalent formula is not held-out selection validation and cannot
   increase confidence that “fewest components” works on new windows.
7. **Do not call four records four nontrivial selections.** Target and strict16
   are active decisions; doubling112 is diagnostic after exit; tight13 returns
   `None` because its eligible set is empty. The implementation's four archive
   comparisons are valid, but phrases such as “all four selections” compress
   materially different branches.
8. **Describe the information barrier as a dependency barrier.** The primary
   parses the complete joint-geometry JSON in phase 1, then projects and uses
   only windows, speeds and moments before selection. It does not access the
   component fields until phase 2, and it delays parsing the selector/control
   archives. That establishes an inspectable code-dependency order, not literal
   blindness to geometry (the full joint object is already in memory, and the
   development geometry was known before the protocol). Either isolate a
   minimal preselection source or use this narrower honest description.

## 5. Prior-work and claim-status correction

The earlier lap-labelled note already defines the clipped occurrences
`I_(v,m)` and emphasizes that their number grows with speed. The sparse
triple-exclusion work already uses arithmetic lap compatibility to avoid some
explicit occurrence enumeration. The present determinant band and open-integer
count should therefore be described as an elementary algebraic restatement and
cost refinement of that existing representation. No novelty search was
performed, and no novelty claim is warranted.

The general lemma may be recorded as an AI-assisted elementary proof candidate
pending independent review. The exact four-window agreement is **OBSERVED**.
The selector remains a development-case heuristic with no general guarantee.

## Required before finalization

- Include the positive-length Helly argument and the `delta<1/2` unique-label
  component-bijection argument in the research note or linked derivation.
- State explicitly that equal speeds are outside the frozen `a<b` domain and
  that gcd collisions do not merge components.
- Report strict inequalities at window and band boundaries; preserve the
  zero-length `a=3,b=5` contact as an adversarial control if the artifact has a
  boundary-test section.
- Report speed-dependent row counts and distinguish four active charged pairs,
  six eligible doubling diagnostics, and fourteen ineligible audit pairs from
  the 24 validation pairs. Avoid “constant-time,” “uniformly cheaper,” or
  “component-free” wording.
- Replace “all four selections” with “all four archived branch records” (or
  equivalent), because one is diagnostic and one has no eligible pair.
- Label target agreement as exact representation recovery on a development
  case, not new evidence for selector reliability or new Lonely Runner
  coverage.
