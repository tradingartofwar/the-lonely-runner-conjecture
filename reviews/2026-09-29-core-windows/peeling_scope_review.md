# Cross-review of five-core positivity and the conservative synthesis

September 29, 2026. Reviewer: the core-peeling AI collaborator.

**Status: HYPOTHESIS / proof-candidate review, not independent human review.**
This review reads `scope.md` and preserves `peeling.md`. All checks below
are direct rational derivations; no mathematical executable, additional
speed enumeration, phase scan, or tuple scan was run. No novelty claim.

## 1. Fixed-core discrepancy and the twelve small speeds

The fixed-core safe set is six disjoint closed intervals, with total width
3/8, as listed in both reports. A primitive of the v-blocker indicator minus
1/4 rises by `(3/4)*(1/(4v))=3/(16v)` across each blocker and falls by the
same amount across the following safe gap. Its range is therefore exactly
3/(16v). Endpoint values do not affect this integral calculation.

On each core interval I the blocked measure is at most
`width(I)/4+3/(16v)`. Summation over six intervals gives

`Q(v)<=3/32+9/(8v)`.

For v>=16 this is at most `21/128<1/6`, so the twelve displayed small speeds
in `scope.md` exhaust the remaining domain. I checked their intersections
by identifying each contributing integer-centered blocker in the scaled
intervals vA,vB,vC. The entries below give `center: contributing length`;
omitted entries contribute no positive length.

| v | Contributions in vA | Contributions in vB | Contributions in vC |
| --- | --- | --- | --- |
| 2 | none | none | `1:1/16` |
| 3 | none | `1:1/4` | none |
| 6 | `1:7/40` | `2:1/4` | none |
| 7 | `1:1/4` | `2:5/32` | `3:3/20` |
| 8 | `1:1/8` | `3:1/8` | none |
| 9 | none | `3:1/4` | `4:1/4` |
| 10 | none | `3:1/4` | none |
| 11 | `2:1/20` | `3:1/32, 4:1/4` | `5:1/4` |
| 12 | `2:9/40` | `4:1/4` | `5:1/40` |
| 13 | `2:1/4` | `4:1/4` | `6:7/32` |
| 14 | `2:1/4` | `4:3/16, 5:1/4` | `6:7/40` |
| 15 | `2:1/4` | `5:1/4` | `7:5/32` |

Multiplication of each row total by 2/v reproduces all twelve Q(v) values
in `scope.md`, including the maximum 1/6 at v=3. The factor 2 follows from
reflection t -> 1-t and integer v; it would require reconsideration for
noninteger speeds or arbitrary phases. The report correctly keeps those
assumptions in scope.

Thus the proposed universal inequality `Q(v)<=1/6` is supported by the
displayed complete analytic argument.

## 2. Five-core measure, components, and the pair budget

The union bound inside the fixed safe set S gives

`measure(safe{1,4,5,a,b}) >= 3/8-Q(a)-Q(b) >= 1/24`.

No independence assumption is used. Actual overlap of the two added blocked
sets only improves this estimate. This corrects the apparent stopping point
described at the end of `peeling.md`: total nominal duty above one does not
prevent a stronger fixed-core argument from forcing positive measure.

The conservative positive-component count `K<=a+b+6` is valid. Each
integer-speed blocked train has at most v relevant interior cuts, and a
single interval deletion can increase the number of positive components by
at most one. Safe singletons do not contribute measure. The safe set is
closed, so closures of its positive components remain safe. Pigeonhole
therefore gives a closed five-core window of width at least `1/(24K)`.

For c<d, a strict chain uses c at most once and d at most twice, by the
two-label return contradiction already written in `peeling.md`. Its span is
strictly below `1/(4c)+1/(2d)`. Consequently every closed interval of that
width contains a point safe for c,d. Since d>c,

`1/(4c)+1/(2d) < 3/(4c) <= 1/(24K)`

whenever c>=18K. Open blockers and closed safe windows preserve equality at
the outer width test; no positive final safe duration is asserted.

## 3. Conservative synthesis

The b>=48 theorem in `peeling.md` is standalone for all admissible a, not
only a<=34: its a>=22 branch uses

`H<=1/22+9/(4*48)=65/704<3/32`,

which has no upper restriction on a. The remaining branches are 11<=a<=21
and the seven explicit a values below 11.

Combine the inherited a>=35 criterion, the b>=48 criterion, and the
five-core bound:

1. If a>=35, the inherited four-residual H test succeeds.
2. If b>=48, the peeling argument succeeds, regardless of the value of a.
3. Otherwise a<=34 and b<=47, so `K<=a+b+6<=87`. If c>=1566, then
   `c>=18*87>=18K`, and the pair budget succeeds in a five-core window.

Therefore every configuration with **c>=1566** is covered, and any
configuration not certified by these criteria must satisfy

`a<=34, b<=47, c<=1565`,

with d still unbounded. These are deliberately conservative constants. This
is a finite restriction on the first three residuals, not a completed finite
reduction for all four or a proof of final-stage existence.

For completeness, the method-limit tuple in `peeling.md` is arithmetically
sound:

`H(21,47,48,49)-3/32=335/442176>0`,

`T_3(47,48,49)-1/28=95/221088>0`.

Every interval safe for speed 21 has width at most 1/28. Thus the two tests
specified there cannot certify that tuple. The later five-core criterion is
an additional test; the earlier limitation was never a claim against it.

## 4. Supplementary observations, not used in the main constant

Two elementary slack reductions were reported to the coordinator and are
recorded here without further optimization. The endpoint blocked intervals
cannot split any component, giving `K<=a+b+4<=85`. Distinct a,b mean that at
most one can equal 3; every other allowed v has `Q(v)<=21/128`, from the
same table and the same large-v inequality. Thus five-core measure is at
least `3/8-1/6-21/128=17/384`. These two refinements would give a window of
width at least `17/(384*85)=1/1920`, and hence the sufficient condition
c>=1440. The main synthesis deliberately retains c>=1566. No additional
cases were evaluated to obtain the supplementary observation.

Also, t=1/6 is strictly safe for the fixed core. Any integer residual not
divisible by 6 has distance at least 1/6 at that time. Therefore failure of
this single witness requires **some residual** to be divisible by 6, which
is stronger than merely requiring a residual divisible by 3. This was sent
to the arithmetic collaborator. It need not be the smallest residual a.
