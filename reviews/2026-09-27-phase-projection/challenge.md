# Challenge review: two-time completeness has a specific robustness quantifier

September 28 UTC; scope fixed by the September 27 Pacific protocol. Only the
two prescribed velocity lists, their exact algebraic phase partitions, and
the two prescribed time pairs were checked. Material AI involvement:
mathematical review, exact reconstruction, and writing. No new speed case,
time-pair search, phase grid, or abstract countermodel was added.

**Verdict:** the covering-arc criteria, the fixed two-time certificates, and
the representation hierarchy are sound with the endpoint and multiplicity
distinctions below. A further supplied argument makes two-time certificates
complete for the *all-phase robustness question* at threshold 1/8. It does
not establish that arbitrary configurations have that robustness, or that
feasibility at the original common-start phase implies a robust pair.

General deductions are **HYPOTHESIS / proof candidates** under repository
rules. Exact constants and finite algebraic profile comparisons are
**OBSERVED** within these two fixed inputs. Agreement among AI reviewers is
not independent human proof certification.

## 1. The two covering-arc inequalities have different equality cases

Let A be the compact unchanged-safe time set, P its image under the chosen
runner's phase map, and B the closure of its positive-length phase support.
For a nonempty compact circle set K, let c(K) be the minimum length of a
containing **closed** circular arc. Put a=2delta, with 0<delta<1/2.

For phase theta, the chosen runner blocks an **open** arc O_theta of length
a. Thus

`some allowed time exists iff P is not contained in O_theta`,

whereas, for the present finite interval unions,

`positive duration exists iff B is not contained in closure(O_theta)`.

The universal criteria follow:

| Question | Exact criterion |
| --- | --- |
| Is some allowed time present for every phase? | P is nonempty and c(P)>=a |
| Is positive duration present for every phase? | B is nonempty and c(B)>a |

If compact P fits inside an open arc of length a, its extreme points have
positive clearance from the arc endpoints, so c(P)<a. Conversely a shorter
containing closed arc fits inside such an open blocker. This proves the
first criterion, including equality.

Zero duration permits all of B to lie inside the blocker's **closed** arc:
surviving boundary points carry no mass. Hence zero duration is possible
exactly when c(B)<=a. If B is not contained in the closed blocker, its
positive-length support leaves positive measure outside. This proves the
second criterion. Empty B gives identically zero duration; empty P gives no
allowed time. The full circle has c=1, not zero.

In the finite-union setting, `B=closure(interior(P))`. Do not generalize that
topological identity to arbitrary compact sets without addressing their
measure-theoretic structure.

The fixed controls expose the endpoint distinction exactly:

| V | Bulk measure | c(P) | c(B) | All-phase conclusion |
| ---: | ---: | ---: | ---: | --- |
| 13 | 1/4 | 3/4 | 1/4 | Always nonempty; phase zero can have only contacts |
| 16 | 151/448 | 45/64 | 45/64 | Always positive duration |

There is a useful limitation on the narrative for V=13. Its extra isolated
projected points `{3/8,5/8}` are **not necessary** for all-phase existence in
this particular control. B13 is already a closed arc of length 1/4, so its
endpoints prevent containment in an open blocker of the same length. The
extra points add equality times and enlarge c(P), but do not change global
nonemptiness in this family.

## 2. Two times are complete for this robustness question

The following small circle argument strengthens a merely sufficient-pair
interpretation. It is a supplied proof candidate, with no additional
configuration or search.

**Point version.** For a nonempty compact phase set P and `0<a<=1/3`,

`c(P)>=a iff some two points of P have circular separation >=a`.

The reverse direction is immediate: a containing arc cannot be shorter than
the circular separation of its two points. For the forward direction, use
the contrapositive. Suppose every pair distance is less than a. Rotate one
point to zero. Every point then has a unique lift in `(-a,a)`. Compactness
gives extreme lifts L<=0<=R; let w=R-L<2a. Their circular separation is
`min(w,1-w)<a`. If w>=a, this forces `w>1-a`, impossible because
`w<2a<=1-a`. Therefore P lies in an arc of length w<a.

At delta=1/8, combine this fact at a=1/4 with the open-blocker criterion.
All-phase nonemptiness is equivalent to the existence of two unchanged-safe
times whose chosen-runner phases are separated by at least 1/4. Their
preimages are actual safe times by definition of P.

**Strict version.** For `0<a<1/3`, the same reasoning with weak pair bounds
shows that if all pair distances are at most a, then c(P)<=a. Indeed the
extreme span now satisfies `w<=2a<1-a`, ruling out the alternative
`w>=1-a`. Hence `c(B)>a` supplies two bulk phase points separated by more
than a.

For finite unions of safe intervals from nonzero runner speeds, B is the
closure of phase images of fully strict unchanged-safe times: inside each
positive time interval only finitely many threshold events need be avoided.
Perturb the two bulk phase points into such images while retaining their
strict separation. The resulting two times have a common unchanged margin
c>delta and chosen-runner separation d>2delta. The two-time triangle
inequality then guarantees `min(c,d/2)>delta` for every phase.

Conversely any such strict pair plainly guarantees a strict time for every
phase. Thus at delta=1/8 two-time certificates are also complete for
all-phase positive duration. The strict geometric argument is stated only
for a<1/3; its boundary must not be silently included.

This is **not** completeness for ordinary single-phase feasibility. The
original common-start question asks about one phase, while the criterion
requires robustness to every starting phase of one selected runner. Nor
does completeness show how to find the pair cheaply, establish that an
arbitrary velocity list has one, or make either prescribed pair optimal.

## 3. The fixed two-time arithmetic is correct and does bypass full A

For two phase points x,y separated by d, every rotation satisfies

`d <= ||x+theta|| + ||y+theta||`.

Therefore one distance is at least d/2. The unchanged constraints must be
checked at **both** times, since the winner can depend on theta.

| V | Prescribed times | Unchanged minimum at both times | Chosen phase separation | Guaranteed full margin |
| ---: | --- | ---: | ---: | ---: |
| 13 | 1/8,7/8 | 1/8 | 1/4 | 1/8 |
| 16 | 7/15,8/15 | 2/15 | 4/15 | 2/15 |

The full unchanged distance vectors are respectively

`(1/8,1/2,3/8,1/4,1/8,3/8)` and

`(7/15,2/15,1/3,1/5,4/15,7/15)`.

Both prescribed times have an unchanged runner exactly at the displayed
cap. Thus the best minimum distance among these two times is identically
1/8 or 2/15 as theta varies, rather than merely bounded below by it. This
is exact performance of each fixed pair, not optimization over all times.

The V=13 pair cannot certify strictness: unchanged speeds 1 and 7 oppose at
threshold at both times. The V=16 pair has uniform excess 1/120 and proves
strictness without constructing A, P, N, or a complete duration profile.

A reviewed compact duration consequence uses unchanged-safe radius
`R=1/480` and chosen-runner guaranteed radius `rho=1/1320`. The symmetric
intersection gives width 1/660. More sharply, the chosen safe lap has width
3/44>2R, so it cannot truncate both sides of the unchanged-safe interval.
The surviving width is at least

`R+rho=1/352`.

The latter interval may depend on theta; the two radius-rho intervals are
a fixed menu. Both deductions are weaker than the full-support sharp bound,
but their smaller input certificate is the point.

I reviewed [the main two-time note](../../notes/TWO_TIME_CERTIFICATES_2026_09_27.md)
and the separate arithmetic/certificate reports. No error was found in
these fixed-pair arguments. The completeness qualification above concerns
all-phase robustness and must accompany any stronger general interpretation.

## 4. Multiplicity restores duration, not automatically time topology

Full P determines empty/contact-only/strict **status** for every phase in
this setting, because it also determines B. It does not determine duration,
contact counts, or the identities of the surviving times.

- N almost everywhere determines the duration profile through
  `D(theta)=(1/11) integral N(x) 1_safe_theta(x) dx`.
- When D=0, pointwise event multiplicities give the contact count by summing
  N over the finite surviving projected set. Almost-everywhere N cannot do
  that.
- To recover actual time locations, or distinguish isolated time branches
  alongside continuing intervals, retain the explicit preimage branches and
  endpoint fibers. Unlabelled counts do not identify branch connections.

The representation report's **sole** abstract example verifies both losses:
`A1=[1/44,1/22]` and `A2=A1 union (A1+1/11)` have the same projection
`[1/4,1/2]`. At theta=0 their durations differ; at theta=5/8 they have two
versus four isolated times. These are abstract time sets, not a second pair
of physical runner configurations. This review introduces no other example.

Multiplicity is not necessary for *every* quantitative conclusion. In the
V=16 control,

`D(theta) >= (|B|-1/4)/11 = (151/448-1/4)/11 = 39/4928`.

Phase zero attains the bound, certifying the exact continuum minimum from
support measure plus an attaining calculation. Yet multiplicity changes
the minimizer set: the unweighted support estimate stays at this minimum
for `||theta||<=1/32`, while D stays minimal only for `||theta||<=1/48`.

At the algebraic event theta=1/32, the independent reconstruction confirms

`support estimate = 39/4928`, `D = 131/14784`,

whose difference is 1/1056. The extra contribution comes from surviving
phase cells with more than one time preimage. The unweighted estimate is
a lower bound, not another physical runner realization.

## 5. Exact profile checks and remaining limits

The independently predicted extrema agree with the primary output:

| V | Minimum and its phases | Maximum and its phases |
| ---: | --- | --- |
| 13 | 0, only theta=0 | 115/2184 on [1/4,3/4] |
| 16 | 39/4928 on the circular interval [-1/48,1/48] | 7/96 on [61/128,67/128] |

The separate [challenge checker](challenge_check.py) imports no project or
other review code. It reconstructs the unchanged-safe sets and direct time
intersections, independently regenerates every phase event and every
candidate theta breakpoint, checks exact fibers and bulk branches, and
compares all **43 theta-event values and 43 open-cell affine formulas**.
It also checks the two fixed pairs, support metrics, extrema, and the
support-estimate discrepancy above.

The continuum verification is not a phase grid. A breakpoint can occur only
when a translated chosen threshold meets a projected time-component
endpoint. Between independently regenerated consecutive breakpoints the
endpoint ordering is fixed, so direct intersection lengths are affine.
Two exact interior evaluations verify each archived affine formula; all
boundary values are checked separately.

```bash
python -B reviews/2026-09-27-phase-projection/challenge_check.py --check
```

[challenge_checks.json](challenge_checks.json) pins the inspected archive,
protocol, and checker. No discrepancy was found within this scope. The
geometry proves conditional certificate completeness; it does not supply
universal all-phase robustness or a proof of common-start Lonely Runner.
