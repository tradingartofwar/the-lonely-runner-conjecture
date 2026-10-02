# Last-runner compatibility across core openings

Date: 2026-09-29. Parent checkpoint: `f3c26e709fa1cd8945968dcd585bd012430c7243`.
Branch: `research/near-doubling-overlap-2026-09-24`.

**Status.** General deductions below are **HYPOTHESIS / internally reviewed proof candidates**; the frozen exact calculations are **OBSERVED**. Six AI reviewers contributed mathematical derivation, adversarial checking, scope review, and two separately structured exact implementations. Internal agreement is not external mathematical certification. No novelty claim or new eight-runner existence claim is made.

The physical setting remains the common-start integer family
\(\{0,1,4,5,a,b,c,d\}\), with distinct positive nonreference speeds,
\(a<b<c<d\), and the selected reference \(0\). Safety means distance **at
least** \(1/8\). A blocking interval is **open**; equality is safe.
Arbitrary final-runner phases and real final speeds below are explicitly
auxiliary extensions. Nothing here checks every reference or the entire
remaining parameter region.

## 1. Main structural result: two openings can force incompatible laps

Let two positive closed intervals in a core-safe set be
\[
 I=[l_1,r_1],\qquad K=[l_2,r_2],\qquad l_1<r_1<l_2<r_2.
\]
Define their hull span, intervening gap, and larger width by
\[
 D=r_2-l_1,\qquad G=l_2-r_1,\qquad
 w=\max(r_1-l_1,r_2-l_2).
\]

A final runner of speed \(d>0\), at any initial phase \(\theta\), has open
blocking intervals of width \(1/(4d)\), separated by safe gaps of width
\(3/(4d)\). If it strictly blocks both entire windows, connectedness forces
each window into one blocking interval. There are only two possibilities:

- The same blocking lap contains both windows, requiring \(dD<1/4\).
- Different blocking laps contain them, requiring \(dG>3/4\).

In either case the larger window also requires \(dw<1/4\).
Consequently:

> **Two-window certificate.** If \(G\le3w\), every \(d\ge1/(4D)\)
> leaves a safe point in \(I\cup K\), at every final-runner phase.
> If \(G<3w\), every \(d>1/(4D)\) leaves positive safe duration,
> at every final-runner phase.

For the existence assertion, the speed threshold excludes the same lap;
the width and gap inequalities exclude different laps.
For positive duration, suppose instead that the final safe set on these
windows has zero length. Every positive closed window must then lie in a
**closed** blocking interval: any strict safety at an endpoint persists
into the window. Same-lap coverage requires \(dD\le1/4\), contrary to the
strict speed threshold. Different-lap coverage requires \(dG\ge3/4\),
while \(dw\le1/4\) and \(G<3w\) give \(dG<3/4\), also a contradiction.

This is an explicit placement constraint: the gap is too short for
different laps, while the hull is too long for one lap. Total safe duration
and the largest individual width do not retain this information.
The result is an application of the repository's earlier two-time and
interval geometry, not a novelty claim for that underlying geometry.

### The inherited narrow core

For \(C=\{1,3,4,5,7,24\}\), two complete positive core-safe components are
\[
 I=[25/56,29/64],\qquad K=[89/192,15/32].
\]
Their exact parameters are
\[
 D=5/224,\qquad G=1/96,\qquad
 w=3/448,\qquad G<3w,\qquad \frac1{4D}=\frac{56}{5}.
\]

Thus this supplied core retains a safe point in its first unit period for
**every real \(d\ge56/5\)** and every final phase. It retains **positive
duration for every real \(d>56/5\)** and every final phase. In particular,
every admissible integer \(d>24\) is covered.

The two supplied intervals are exact rational certificates, independently
checked by hand; their membership in the complete core decomposition is
also in the frozen outputs. The direct interval checks and the six
single-window integer speed bands appear in
[arithmetic.md](../reviews/2026-09-29-last-runner/arithmetic.md) and
[structure.md](../reviews/2026-09-29-last-runner/structure.md).
The pair certificate explains why this core succeeds even when a width-only
sufficient test leaves candidate final speeds.

## 2. Exact containment and the endpoint distinction

Let \(S_C\subset[0,1]\) be the full safe set for an integer core. Retain all
its maximal closed components, including isolated points.
For a positive component \(I=[l,r]\), put \(x=(l+r)/2\) and \(h=(r-l)/2\).
Then
\[
 \max_{t\in I}\|dt+\theta\|
   =\min\bigl(\|dx+\theta\|+dh,\;1/2\bigr).
\]
The final runner strictly blocks all of \(I\) exactly when
\[
 \|dx+\theta\|+dh<1/8.
\]
Equivalently there is a unique integer lap label \(m\) satisfying
\[
 dr+\theta-1/8<m<dl+\theta+1/8.
\]
For a fixed \(m\), since \(l,r>0\) here, the corresponding speed band is
\[
 \frac{m-\theta-1/8}{l}<d<
 \frac{m-\theta+1/8}{r}.
\]
These are the maximum-distance/blocking counterparts of the earlier
[exact interval criterion](EXACT_INTERVAL_CRITERION_2026_09_28.md).
They are exact representations, not by themselves an obstruction to
simultaneous coverage.

Intersect the unions of these bands across the components, keeping the
lap labels compatible with the same \(d,\theta\). Three sets must remain
distinct:

| Set | Meaning |
| --- | --- |
| \(F\) | Every core component, including isolated points, is strictly blocked; no final safe point remains. |
| \(P\) | Every positive closed core component is strictly blocked; isolated core points are ignored. |
| \(Z\) | Every positive closed core component lies in a closed blocker; final safe duration is zero. |

Thus \(F\subseteq P\subseteq Z\), but neither converse is valid in general.
Closed-block containment replaces strict inequalities by weak ones.
A positive component can leave only an endpoint witness; an isolated core
point can survive after all positive components have been strictly covered.

Writing \(w_{\max}\) for the largest core component width:
\[
 d\ge\frac1{4w_{\max}}\ \Longrightarrow\ F=P=\varnothing
 \quad\hbox{at that speed},
\]
whereas automatic positive duration requires
\(d>1/(4w_{\max})\). The equality speed must be checked separately for \(Z\).

For common-start integer \(d\), each reduced core endpoint \(p/q\) has
\(8\mid q\). Strict endpoint blocking requires its centered residue
\(dp\bmod q\) to lie in
\[
 \{-(q/8-1),\ldots,q/8-1\}.
\]
All endpoint and isolated-point residue conditions, **together with**
\(dw_{\max}<1/4\), are equivalent to full strict coverage. Endpoint
conditions alone are insufficient: a high-frequency runner can block both
endpoints while leaving the interval's interior safe.

For endpoints \(l=p/q,r=s/u\), the positive endpoint slacks give the
necessary stricter bound
\[
 d(r-l)\le\frac14-\frac1q-\frac1u.
\]
Additional controlling-speed/gcd slacks are recorded in structure.md.
They complement these reduced-denominator slacks; they are not uniformly
stronger. None of these necessary scalar bounds alone proves that a full
configuration is impossible.

A further relational constraint uses selected safe times with
\(\sum_i h_i t_i=q\in\mathbb Z\), for integer \(h_i\).
Under strict common-start integer-\(d\) blocking, write
\(dt_i=m_i+e_i\), \(|e_i|<1/8\). If \(\sum|h_i|\le8\), then
\[
 \sum_i h_i m_i=dq.
\]
The difference is an integer of magnitude less than one.
With weak blocking and coefficient norm exactly eight, an error of
\(1\) or \(-1\) is possible only when every participating error is an
aligned threshold contact. These contacts are safe equality witnesses.
An arbitrary phase contributes \(\theta\sum h_i\); it cancels
automatically only for a zero-sum relation. This supplies necessary lap
compatibility, without guaranteeing that every core has a useful short
relation.

## 3. Frozen finite check

Before execution, [PROTOCOL.json](../reviews/2026-09-29-last-runner/PROTOCOL.json)
fixed exactly three inherited cores and the two phases \(0,1/2\).
For each core, all component and prefix-intersection bands were retained
over \((c,U]\), where \(c=\max C\) and \(U=1/(4w_{\max})\). If \(U\le c\),
the domain is empty analytically. Only the four old phase-zero diagnostics
\(d=13,16,112,113\) were separately reconstructed.

The primary implementation intersects exact rational speed bands. The
independent implementation reconstructs the core by threshold events,
partitions the speed domain at endpoint contacts, then reconstructs the
final time set at every contact and each intervening cell midpoint.
Its source and output were frozen before it read the primary result.

**OBSERVED:** zero disagreements across 3,162 numerical fields, 1,324
Boolean fields, three text fields, and one null field. The records include
66 core components (62 positive and four isolated), 18 mode records,
380 component-band rows, and 380 prefix rows. The independent calculation
evaluated 799 speed contacts and 799 open speed cells. These are exact data
and workload counts, not numbers of independent proofs.

| Core \(C\) | Phase | Domain | \(F\) | \(P\) | \(Z\) |
| --- | --- | --- | --- | --- | --- |
| \(\{1,4,5,6,7,11\}\) | \(0\) | \((11,28]\) | empty | \((220/17,196/15)\) | \([220/17,196/15]\) |
| same | \(1/2\) | \((11,28]\) | empty | empty | \(\{18\}\) |
| \(\{1,3,4,5,7,24\}\) | \(0\) or \(1/2\) | \((24,112/3]\) | empty | empty | empty |
| \(\{1,4,5,56,64,72\}\) | \(0\) or \(1/2\) | empty: \(U=126/5<72\) | empty domain | empty domain | empty domain |

At phase zero the designated old diagnostics give:

| Final speed and core | Final safe duration | Topology |
| --- | --- | --- |
| \(13\), tight core | \(0\) | Exactly \(1/8,3/8,5/8,7/8\) |
| \(16\), tight core | \(39/4928\) | Four positive components |
| \(112\), small-gcd core | \(53/448\) | 54 positive components |
| \(113\), small-gcd core | \(214673/2278080\) | 50 positive components |

The \(13\) case is decisive against discarding isolated core points:
all positive components are strictly covered, yet four valid moments
remain. The \(18\), phase-\(1/2\) case instead sits on closed-block equality
and has \(Z\ne P\).

For the small-gcd control, \(w_{\max}=5/504\) already guarantees positive
duration at every final phase for every admissible \(d>72\).
The old \(112:113\) comparison remains informative about duration and
placement; it is not an unresolved last-runner existence obstacle.
No new core or designated physical diagnostic was introduced. The frozen
event partition evaluates final speeds within its declared domain; no broad
speed or phase grid was introduced.

## 4. Reflection compresses the integer phase question

For an integer common-start core and integer final \(d\), reflection
\(t\mapsto1-t\) makes the phase image \(A=dS_C\bmod1\) symmetric:
\(A=-A\).

**Existence at every final phase is equivalent to existence at phases
\(0\) and \(1/2\).** To see this, suppose some phase fails. Then \(A\)
fits in an open quarter-circle arc, so every pair has separation \(<1/4\).
Reflection gives \(\|2x\|<1/4\), putting each \(x\) in the open
quarter-circle arc about zero or that about \(1/2\). The two arcs cannot
both be occupied: reflection would supply a cross-pair separated by at
least \(3/8\). Thus all of \(A\) lies in one arc, and phase zero or half
already fails.

The same statement holds for **positive duration**, using the image of
the union of the positive **closed** components, excluding isolated
points, and closed blocker arcs. A pair with separation strictly greater
than \(1/4\) ensures positive duration at every phase; equality only
ensures existence. An empty positive-component image has zero duration
at every phase and is handled separately.

This is a symmetry specialization of
[TWO_TIME_CERTIFICATES_2026_09_27.md](TWO_TIME_CERTIFICATES_2026_09_27.md).
It applies to the full symmetric core period with integer \(d\), not to
an arbitrary clipped window or arbitrary real-\(d\) first-period image.

Together with the frozen bands and the width bound, this establishes the
following internally reviewed consequences for the tight core:

- Every integer \(d>11\) retains a safe point at every final phase.
- Every such \(d\), other than \(13,18\), retains positive duration at
  every final phase. The equality cap \(d=28\) was included in the exact
  domain; independently, two reflected component images at \(28\) fill
  a half-circle, excluding closed quarter-circle containment.

### Analytic follow-up: the exceptional phase sets

This paragraph was derived **after** the frozen computation; it is an
analytic deduction, not a preregistered prediction or a phase scan.
The tight core has positive components
\[
 [17/56,5/16],\quad[41/88,15/32],\quad
 [17/32,47/88],\quad[11/16,39/56],
\]
and isolated points \(1/8,3/8,5/8,7/8\).

At \(d=13\), the image of the positive components is precisely the closed
arc \([-3/32,3/32]\bmod1\). Therefore zero final duration occurs exactly
when \(\|\theta\|\le1/32\). At \(d=18\), that image is exactly
\([3/8,5/8]\), so zero duration occurs only at \(\theta=1/2\bmod1\).
The isolated points ensure existence at every phase in both cases.
At boundary phases, additional equality contacts can also survive at
positive-component endpoints. See
[scope.md, section 7](../reviews/2026-09-29-last-runner/scope.md).

Here the **final** runner is shifted. The earlier
[adaptive reflected-pair study](ADAPTIVE_REFLECTED_PAIR_2026_09_28.md)
shifted runner \(11\); its phase conclusions must not be substituted for
these.

For noninteger real \(d\), first-period bands have a different global
meaning. If the integer core has a safe time \(t_0\), let
\(\beta=\|d\|>0\) and \(m=\lfloor1/(4\beta)\rfloor+1\). Then
\(1/4<m\beta\le1/2\), so the final phases at \(t_0,t_0+m\) are separated
by more than \(1/4\). Both times remain core-safe by integer periodicity.
The two-time certificate gives a surviving point at every final phase;
a strict interior core time gives positive duration. Thus a noninteger
speed's local containment band on \([0,1]\) is not a global counterexample.

## 5. What this closes, and what remains

The last-runner problem now has an exact component/lap formulation, an
explicit two-window incompatibility certificate, and endpoint-sensitive
controls. The strongest new concrete application is the all-phase,
real-speed certificate for the supplied core \(\{1,3,4,5,7,24\}\).
The common-start integer existence specializations are already within
previously credited theory. The auxiliary arbitrary-phase/real-speed claims
are not being attributed to that theory. The research contribution under investigation is the
explicit mechanism and its potential generalization.

The missing universal step is **structural existence of a useful
certificate**. A positive six-core window alone need not meet the final
runner's width bound. We have not shown that every admissible six-core
safe set contains two windows satisfying \(G\le3w\) and
\(D\ge1/(4d)\), or a bounded larger collection with incompatible actual
lap choices. Tight equality-only final cases also require a point route;
a universal positive-duration claim would be false.

**Next manually directed milestone:** derive a guarantee, or a precise
obstruction, for such a protected pair or bounded collection from the
arithmetic of the six-core endpoints. Combine placement, endpoint
residues, and short lap relations while retaining isolated witnesses.
Do not replace this missing implication with an unapproved broad scan.

The previously credited finite reduction
\(a\le34,\ b\le47,\ c\le281,\ d\le1268\) is unchanged and remains
unexhausted. No new all-reference or full-conjecture result follows.
Hourly research stays paused; no +7/+9 restart, paid compute, outreach,
main merge, broad quadruple scan, or phase grid was performed.

## 6. Reproducibility and review record

All records are in
[reviews/2026-09-29-last-runner](../reviews/2026-09-29-last-runner).
The directory includes the frozen protocol, primary predictions and plans,
both sources and complete outputs, the pre-comparison independent freeze,
the comparison script/result, and all six reviewer reports.
[verification.md](../reviews/2026-09-29-last-runner/verification.md)
describes the independent method and full comparison scope.
[challenge.md](../reviews/2026-09-29-last-runner/challenge.md)
records adversarial endpoint and quantifier checks.
MANIFEST.json hashes the preserved artifacts.

Protocol SHA-256:
`660a3a7f27f6a1e7b2c0c68aeea22b42366c7a946d5612e967c6f355999d5aae`.

From the repository root, the original finite calculations are reproducible:

```bash
python reviews/2026-09-29-last-runner/primary_last_runner.py
python reviews/2026-09-29-last-runner/independent_last_runner.py
python reviews/2026-09-29-last-runner/compare_last_runner.py
```

Rerunning after comparison is deterministic reproduction, not a new
independent pre-access freeze. The post-protocol phase classification and
general geometric arguments are separately identified as analytic
deductions. No extra mathematical run was needed to prepare this note.
