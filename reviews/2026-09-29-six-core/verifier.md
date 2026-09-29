# Independent audit: threshold margins and the last two speeds

September 29, 2026. Parent research state: `da05361310a6e0d5607fdd7565ad226f637c8305`.

**Current audit result:** the sourced lower-runner route, including the
sharper pair-span argument in Section 9, leaves the conservative rectangle
**`a<=34,b<=47,c<=281,d<=1268`**. Sections 3–5 preserve the intermediate
limits from the derivation; they are superseded where Section 9 is stronger.
The separate coordinator-approved direct six-core evaluation is also
complete: all 27 declared cases are positive and all 2,495 comparison fields
agree, as detailed in Section 10. No final-speed values were evaluated.

**Status:** internal analytic audit of proof candidates. The implications below
are conditional on precisely stated lower-runner inputs until those inputs
have been checked against primary literature. This report does not establish
the cited lower-runner theorems itself, assert novelty, or provide external
proof certification. No executable mathematical evaluation, speed scan, or
primary-implementation inspection was used to derive these results.

## 1. Scope and the two inputs to be sourced

The physical family is eight common-start runners with selected reference 0
and distinct positive integer speeds

`{1,4,5,a,b,c,d}`, with `a<b<c<d` outside `{1,4,5}`.

The target is distance at least 1/8; equality is safe. The following inputs
must be sourced with the total-runner convention made explicit:

- **Input R6:** any five distinct positive integer speeds have a common time
  at distance at least 1/6 from the stationary reference. This concerns six
  total runners.
- **Input R7:** any six distinct positive integer speeds have a common time
  at distance at least 1/7 from the stationary reference. This concerns seven
  total runners.

The positive integer restriction here is sufficient; no extension to shifted
starts is asserted. Let `M=max(5,b)`. In particular, `M` must not be replaced
by `b` when `(a,b)=(2,3)`. The third residual satisfies `c>=6`, and hence c
is the maximum of the six speeds `{1,4,5,a,b,c}`.

## 2. General threshold-margin lemma

For every real x,y, distance to the nearest integer satisfies

`abs(||x||-||y||)<=abs(x-y)`.

Suppose finitely many positive speeds, all at most V, are simultaneously at
distance at least alpha at time t*, where alpha>beta. For every

`|t-t*|<=(alpha-beta)/V`,

each distance is at least `alpha-v|t-t*|>=beta`. Thus there is a **closed**
beta-safe window of width

`2(alpha-beta)/V`.

This reasoning takes place on a real lift of time, so a window crossing an
integer time is not truncated. For the integer common-start problem it may
subsequently be read modulo one.

## 3. R7 gives d>=7c

Apply R7 to `{1,4,5,a,b,c}`. The margin from 1/7 to 1/8 is 1/56, and
the maximum speed is c. Consequently the six-core has a closed 1/8-safe
window of width `1/(28c)`.

A speed-d blocker is an open interval of width `1/(4d)`. A connected closed
window of at least this width cannot be wholly contained in one such
interval. Since different occurrences are separated, it cannot be covered
by several disjoint occurrences either. Therefore

**`d>=7c` is sufficient.**

The weak inequality is correct: at equality the ends of the blocker are
safe. Together with the inherited `c<=1565` reduction, this alone leaves
`d<=7c-1<=10954`.

## 4. R6 gives c>=9M and a stronger two-speed condition

Apply R6 to `{1,4,5,a,b}`. Its margin from 1/6 to 1/8 is 1/24, giving a
closed 1/8-safe window of width `1/(12M)`.

For the remaining speeds c<d, use the previously derived two-train span
budget

`T2=1/(4c)+1/(2d)`.

The inherited chain argument guarantees a joint-safe point in any closed
window of width at least T2. Since d>c,

`T2<3/(4c)`.

It follows that **`c>=9M` is sufficient**, independently of the size of d
above c. With the inherited `b<=47`, one has M<=47, so unresolved cases
satisfy **`c<=422`**. Applying Section 3 then leaves `d<=2953`.

The more precise two-speed condition, useful below, is

`c>3M` and `d>=6Mc/(c-3M)`.

Indeed, this is exactly the result of solving `T2<=1/(12M)` for d. No
rounding is needed in the mathematical statement; for integer d the first
successful value is the ceiling of the displayed rational expression.

The simple c threshold 9M cannot be decreased by merely inserting d>=c+1
into this same sufficient test. At `c=9M-1,d=c+1`, the test requires
`3M(3c+1)<=c(c+1)`, but the right side minus the left is `-3M`.
This is only a limitation of that sufficient test.

## 5. Combining R6 and R7 gives d>=27M

There is a stronger uniform d cutoff than 7 times the largest allowed c.
Assume `d>=27M` and split according to c:

- If `c<=27M/7`, then `d>=7c`, so Section 3 applies.
- If `c>=27M/7`, then
  `T2<=7/(108M)+2/(108M)=1/(12M)`, so Section 4 applies.

Thus **`d>=27M` is sufficient**, using one of the two core windows according
to the relative size of c. The argument covers the shared boundary and does
not require an integer evaluation domain.

Combining these implications with the inherited first-two-speed reduction
therefore leaves the following conservative finite rectangle:

**`a<=34, b<=47, c<=422, d<=1268`.**

The actual unresolved region also satisfies the stronger parameter-dependent
conditions `c<9M`, `d<27M`, and `d<7c`; when c>3M it additionally satisfies
`d<6Mc/(c-3M)`. The rectangle is not an exhaustive classification of
uncertified configurations, and no configurations in it have been scanned
by this report. Combining sufficient tests is not a proof that the finite
remainder is empty.

## 6. Hand-derived equality fixture

Take the fixed-family core with `(a,b,c)=(2,3,6)`, so its six speeds are
1 through 6. At `t*=1/7`, each has distance at least 1/7. The margin window
is

`W=[47/336,49/336]`, of width `1/168=1/(28c)`.

Add `d=42=7c`. Its collision at t*=1/7 is the center of the open blocked
occurrence `(47/336,49/336)`. Both endpoints of W have speed-42 distance
exactly 1/8 and are safe for every core speed by Section 2. At the right
endpoint, speed 6 also has distance exactly 1/8.

Thus the entire interior of this particular margin window is blocked by d,
but both endpoints survive. This hand calculation confirms why replacing
closed windows by open windows, or declaring equality blocked, would break
the boundary guarantee. It is not a claim about the full-period safe set.

## 7. Audit disposition and remaining dependency

The threshold-margin, single-train, and combined-cutoff arguments above are
internally valid under their stated inputs and the inherited two-train
span lemma. They do not require positive measure after adding the final
runner. The lower-runner witnesses use original common starts; arbitrary
phase robustness is needed only for the already-established auxiliary
single-/two-train window facts.

The coordinator must attach inspected primary-source support for R6 and R7
before describing the resulting bound as an unconditional consequence of
known theorems. Attribution should separate these standard lower-runner
inputs from this project's proposed organization of sufficient certificates.

External mathematical review remains pending. The broad finite remainder
has not been searched, and the hourly automation remains paused.

## 8. Subsequent independent primary-source check

After completing Sections 1–7, this reviewer independently opened the
following primary sources. This resolves the stated source dependency of
R6 and R7; it does not claim independent reproduction of their full proofs.

- Bohman, Holzman and Kleitman, *Six Lonely Runners*, Electronic Journal of
  Combinatorics 8(2), R3 (2001), [author-hosted published PDF](https://holzman.technion.ac.il/files/2012/09/runners.pdf).
  Theorem 2 on printed page 3 supplies R6, indeed for arbitrary positive
  real speeds. The formulation on pages 1–3 and the complete short Lemma 4
  proof were inspected. That lemma gives a direct two-block precedent for
  the pair-window argument; its original threshold is 1/6.
- Barajas and Serra, *The lonely runner with seven runners*, Electronic
  Journal of Combinatorics 15(1), R48 (2008), [published PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v15i1r48/pdf).
  The abstract and printed page 2's integer-frequency formulation establish
  applicability of R7. Our core contains speed 1, so its gcd is one. This
  reviewer read the statement and normalization, not the full casework.
- Kravitz, *Barely lonely runners and very lonely runners: a refined
  approach to the Lonely Runner Problem*, Combinatorial Theory 1 (2021),
  #17, [published PDF](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf).
  Proposition 6.1 on printed pages 12–13 states the fast-runner margin
  consequence. Its proof and page-12 screenshot were inspected; the relevant
  inequalities are non-strict despite text extraction dropping their lower
  bars. Section 3 above is precisely this known consequence with
  `L=1/7, epsilon=1/56`.

The lower-runner inputs and one-fast-runner precedent may therefore be
credited as **KNOWN**. The assembled reduction remains an internally
reviewed proof candidate under the repository's evidence discipline.

## 9. Independently derived sharper pair span

The following refinement was derived before reading the literature review's
matching proposal. It adapts the same two-block mechanism as Bohman,
Holzman and Kleitman's Lemma 4, with target threshold 1/8.

Write `P=1/c>q=1/d`. A selected advancing chain of pair blockers contains
at most one c occurrence and at most two d occurrences. If it contains at
most one of each, its span is at most `(P+q)/4<P/2`.

If it contains two d occurrences around a c occurrence, the c interval must
bridge a d safe gap of length `3q/4`. For strict overlap this requires
`P/4>3q/4`, hence q<P/3. Its span is then less than
`P/4+q/2<5P/12<P/2`. For closed blockers and weak overlaps the same
argument gives q<=P/3 and span at most5P/12, still strictly below P/2.
Contained d occurrences do not enlarge the span beyond the c occurrence
and its two extreme d overlaps; equivalently, the advancing chain omits
them.

Thus every closed window of length `1/(2c)` contains a point outside both
**closed** blocking sets, and hence has a strict joint-safe point. This is
stronger than merely retaining threshold equality. It yields the improved
R6 condition **`c>=6M`** and hence **`c<=281`** among remaining cases.
Combining with the unchanged Section 5 condition gives the conservative
rectangle `a<=34,b<=47,c<=281,d<=1268`. No claim that the constants are
optimal is made.

## 10. Later coordinator-approved exact six-core evaluation

After the analytic review above, the coordinator froze and approved
`PROTOCOL.json`, SHA-256
`25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2`.
Its set-builder uses exactly 36 declared (a,b) branches, c<=62, the
declared span inequality, and the declared sixth/seventh/eighth-anchor
conditions. No optional additional cases or pruning were used.

The independent implementation first generated the input set from the
protocol itself. For each six-core it then generated every rational
threshold event, separately evaluated the modular safety predicate at
every endpoint and open-cell midpoint, and reconstructed all maximal closed
safe components. Primary code and output were not inspected until the
independent output was complete and frozen.

**OBSERVED:** the declared set-builder yields 27 triples. All have positive
safe measure. Their complete records contain 190 positive components and
50 isolated points. The reconstruction evaluated 2,730 threshold endpoints
and 2,703 open cells. The largest value of the declared one-additional-runner
cutoff `ceil(1/(4w))` is 38. No last-runner d values were evaluated.

The independent output `independent_six_core.json` was frozen at SHA-256
`6cbd1cf544659a52eea00cf27fc0879eb6a48658e1544f81c0c4ade2479be736`.
Only then was the primary output opened. `compare_six_core.py` checks the
complete domains and every primary mathematical record field, including
all components, exact measures, widths, tie choices, cutoffs, selected-point
distances, and isolated-point distances reconstructed from the independently
identified isolated points. All **2,495 numerical leaf comparisons pass**.
These fields include intentionally redundant representations of the same
geometric objects; the count is a comparison audit, not a count of independent
mathematical facts.

A separate scalar audit, explicitly included in the frozen protocol's
comparison clause, reuses the archived 31 four-core widths. For each a,
`T2(b,c)<3/(4b)` bounds the possible b, and the smallest admissible c
maximizes T2. The audit checks 45 such scalar inequalities and recovers
exactly the declared 36 pairs. Each retained pair has
`w_a-1/(4b)>0`, and solving the remaining inequality gives a maximum c
cap of 62. This does not evaluate any new six-core safe set.

Files and reproduction:

```bash
python reviews/2026-09-29-six-core/independent_six_core.py
python reviews/2026-09-29-six-core/compare_six_core.py
python reviews/2026-09-29-six-core/audit_branch_reduction.py
```

`comparison.json` records both implementations' hashes and the comparison
outcome; `branch_audit.json` records all 36 scalar branch bounds. The
approved finite evaluation is complete and has stopped. The direct global
six-core argument additionally depends on the coordinator's analytic anchor
and tail reductions; the exact 27 rows alone do not establish that theorem.
