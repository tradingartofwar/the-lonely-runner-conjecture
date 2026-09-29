# Compatibility Calculus: frozen discovery rule transfers to the B ray

September 29, 2026. Research input base:
`6b2b9316dbc87499a1cb5184aadbd6614d4d6c32`.

**Status: HYPOTHESIS / complete proof candidate with internal AI team review.**
This is a transfer of a sufficient witness-construction rule to a previously
studied ray, not new physical family coverage, an optimum claim, independent
human certification, formal verification or a novelty determination.

The frozen parent-only discovery rule succeeds on

\[
B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2),\qquad q\in\mathbb Z,\ q\ge2.
\]

After an explicit coordinate translation, the unchanged ranking and covering
rule selects the same two geometric segments as on A, in the opposite order
to the A discovery certificate. P1 supplies a physical \(1/8\)-safe time for
every \(q\ge3\); P3 supplies \(q=2\) at \(t=9/40\). Online selection takes at
most two integer-rounding tests. Every returned separation is exactly \(1/8\).

The review then exposed a further simplification: **P3 alone covers every
\(q\ge2\)**. This is documented below as a post-protocol deduction and separate
verification. The frozen discovery run and its two-segment output remain intact.

## 1. The translation is part of the certificate

There are eight common-start runners and the selected reference remains
stationary. The torus coefficient rows are unchanged:

\[
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
\]

The two substitutions give different clocks and integer conditions:

| Item | A ray | B ray |
| --- | --- | --- |
| Coordinates | \(x=\{t\},\ y=\{qt\}\) | \(x=\{qt\},\ y=\{t\}\) |
| Physical time | \(t=x\) | \(t=y\) |
| Speed of row \((a,b)\) | \(a+bq\) | \(aq+b\) |
| Native integer orbit | \(h=qx-y\) | \(H=x-qy\) |
| Physical lap for torus lap \(m\) | \(m+bh\) | \(m-aH\) |
| Stored geometric fold | \(x\le1/2\) | \(x\le1/2\) |

For B, put \(u=y,\ v=x\) and \(g=qu-v=-H\). The frozen selector then sees
its usual form \(g=qu-v\), clock \(t=u\) and transformed row \((b,a)\).
The seventh row becomes \((2,5)\). Its physical identity is

\[
(aq+b)u=\underbrace{m+ag}_{\text{physical lap}}
       +\underbrace{av+bu-m}_{\text{fractional phase}}.
\]

All endpoints lie strictly between zero and one in both torus coordinates.
The original fold becomes **\(v\le1/2\)**. It is not a restriction
\(u\le1/2\) on every candidate. The selected times happen to be in the first
half, but that is an output property, not a substitute input assumption.

Native row order gives speeds \((q,1,q+1,2q+1,3q+1,3q+2,5q+2)\). Permute
the first two speeds, phases and laps together to display \(B_q\) above.
Reflection gives \(t'=1-t\), fractional phases \(1-f_i\), and physical laps
\(v_i-1-\ell_i\), where here \(v_i\) denotes a speed. A reflected torus point
need not lie in the stored fold; physical reflection remains valid.

## 2. Exactly what was kept fixed

The [protocol](../reviews/2026-09-29-cc-b-ray-transfer/PROTOCOL.md) was saved
before running the transfer. The
[adapter](../reviews/2026-09-29-cc-b-ray-transfer/transfer.py) imports the
unchanged [A discovery functions](../reviews/2026-09-29-cc-segment-discovery/discover.py).
It swaps vertex coordinates, constraint-normal coordinates and coefficient
rows, binds the added row to \((2,5)\), and calls the original candidate,
cover and witness functions. It does not call the A-specific reporting main,
whose fold assertion refers to its old first coordinate.

Parent IDs, original vertex IDs, edge incidence, lap labels, closed clipping,
provenance tie-breaks, minimum-cutoff ranking, greedy prefix covering and the
\(Q>26\) scope guard are unchanged. Endpoint orientation is lexicographic in
the translated clock/orbit coordinates, as required by the same rule.

The discovery choices use only six-form parents and the added band. The old
candidate output is read afterward to verify that undoing the swap preserves
all native geometric segments and labels. No known B optimum, optimum witness
or child-cell selection enters the discovery choices.

The 24 floor edges still give 27 labelled clipping records, including nine
point records. Fifteen now have positive span in the physical-clock coordinate.
This differs from A's 13 because the clock changed, not the safe geometry.

## 3. Coverage and explicit recovered times

For any compatible segment oriented with \(\Delta u>0\), the same frozen
cutoff is

\[
Q=\max\left(2,\left\lceil\frac{1+\Delta v}{\Delta u}\right\rceil\right).
\]

For every integer \(q\ge Q\), the orbit interval has width
\(q\Delta u-\Delta v\ge1\) and therefore contains an integer. Round its lower
endpoint and interpolate on that same segment. This is the previous conditional
finite-reduction proof with renamed coordinates, not a new existence premise.

The least cutoff is four. The provenance tie-break chooses P1 first.

| Role | Original geometric segment | Canonical endpoints \((u,v)\) | Width and cutoff |
| --- | --- | --- | --- |
| Primary P1, edge 1–3, lap 1 | \(1/8\le x\le5/24,\ y=7/8-3x\) | \((1/4,5/24),(1/2,1/8)\) | \((3q+1)/12\), \(Q=4\) |
| Fallback P3, edge 0–1, lap 2 | \(3/8\le x\le1/2,\ y=9/8-2x\) | \((1/8,1/2),(3/8,3/8)\) | \((2q+1)/8\), \(Q=4\) |

For the primary segment,

\[
g\in I_1(q)=\left[\frac{6q-5}{24},\frac{4q-1}{8}\right].
\]

The only integers below the cutoff that need testing are:

| \(q\) | Primary interval | First integer | Result |
| --- | --- | --- | --- |
| 2 | \([7/24,7/8]\) | 1 | Misses; use fallback. |
| 3 | \([13/24,11/8]\) | 1 | Succeeds; \(t=31/80\). |

Thus the primary succeeds for every \(q\ge3\). Its rounded integer is

\[
g=\left\lceil\frac{6q-5}{24}\right\rceil
 =\left\lfloor\frac{q+3}{4}\right\rfloor,
\qquad t=\frac{24g+7}{8(3q+1)}.
\]

The rounding identity follows by writing \(q=4a+r\), \(0\le r<4\):
\(g=a\) for \(r=0\), and \(g=a+1\) otherwise.

The fallback interval is

\[
I_2(q)=\left[\frac{q-4}{8},\frac{3(q-1)}8\right].
\]

At \(q=2\), it is \([-1/4,3/8]\), so \(g=0\) and
\(t=(16g+9)/[8(2q+1)]=9/40\). The native point is
\((x,y,z)=(9/20,9/40,1/8)\), with \(H=0\). In displayed B-speed order,
the phases are

\[
\frac1{40}(9,18,27,5,23,32,28),
\]

all in \([5,35]/40\). This closes the only gap.

The two segments' seven affine phase charts are the same native charts already
proved in the [A two-segment note](CC_BOUNDED_SELECTOR_2026_09_29.md). Coordinate
swapping preserves them. The fifth native phase on P1 is constantly \(7/8\),
and the fourth on P3 is constantly \(1/8\), establishing exact separation
\(1/8\). Physical safety follows from the identity in section 1, so these
statements cover every integer \(q\), not just the finite controls.

Preprocessing checks 27-by-2 prefix entries and makes one greedy addition.
Online selection uses at most two interval roundings/tests and one interpolation.
Arithmetic bit costs grow with \(q\); no constant-time or optimality claim is
made. No candidate ranking or exceptional-case rule was retuned after execution.

## 4. Team verification

The coordinate, discovery and physical reviewers had separate assignments.
Their reports preserve read order and dependencies. All share the project
context and are AI collaborators; this is not independent human certification
or a blind evaluation against an unknown family. The discovery rule was frozen
before this B execution, but previous work on the B family was already known.

Detailed outcomes and coordinator reproduction are recorded in the
[review package](../reviews/2026-09-29-cc-b-ray-transfer/).

| Check | Result | Separation and limitation |
| --- | --- | --- |
| [Coordinate review](../reviews/2026-09-29-cc-b-ray-transfer/coordinate_review.md) | Clock, orbit sign, row/lap maps, reflection and fold checked; own adapter agrees on candidates and witnesses. | Derivation saved before new output; reuses frozen discovery functions, so it is not a separate enumeration implementation. |
| [Discovery review](../reviews/2026-09-29-cc-b-ray-transfer/discovery_review.md) | Separately implemented clipping and coverage reproduce all 27 records, 54 prefix entries and 24 recovered controls. | Parent-only reconstruction frozen before coordinator comparison; supplied parent geometry remains an input dependency. |
| [Physical review](../reviews/2026-09-29-cc-b-ray-transfer/physical_review.md) | 336 direct phase checks, 56 endpoint inequalities and 56 polynomial inequalities on four infinite residue domains pass. | No selector import or optimum search; direct physical controls are only \(q=2,\ldots,25\) and reflections. |

No result-level defect was found in the frozen transfer. The checks also
preserve failures of superficially similar translations:

- At \(q=2\), replacing the correct clock \(t=y=9/40\) by \(t=x=9/20\)
  gives speed 2 distance \(1/10<1/8\). Wrong-clock recovery fails in 22 of
  the 24 declared controls.
- At \(q=3\), \(g=1,t=31/80\). Original row \((1,0)\) has speed 3 and
  physical lap 1. Using \(m+bg\) yields lap 0 and phase \(93/80\);
  using the wrong orbit sign yields phase \(173/80\).
- A valid unselected candidate at the same declared \(q=2\) has
  \((u,v)=(41/56,13/28)\). It satisfies the actual fold \(v\le1/2\)
  but would be discarded by an invented \(u\le1/2\) restriction. This
  shows loss of a valid candidate, not failure of the selected cover.

## 5. Post-protocol simplification: one segment is enough

After freezing and comparing the discovery outputs, the arithmetic reviewer
noticed that P3 has the same cutoff four **and covers both prefix inputs**.
Therefore it covers every \(q\ge2\) by itself. The original rule first chooses
P1 by provenance and then adds P3; it never claimed minimum cardinality.

The [dated addendum](../reviews/2026-09-29-cc-b-ray-transfer/POST_PROTOCOL_SIMPLIFICATION.md)
records this deduction before further physical checks. Neither the original
rule nor its output was changed. The smaller selector is

\[
\boxed{\quad
g=\left\lfloor\frac{q+3}{8}\right\rfloor,
\qquad t=\frac{16g+9}{8(2q+1)},\qquad q\ge2.
\quad}
\]

Indeed P3 has orbit interval
\([(q-4)/8,3(q-1)/8]\), whose width \((2q+1)/8\) is at least one for
\(q\ge4\). At \(q=2,3\) it contains \(g=0\). Its first integer is precisely
the displayed floor expression. Recovering the point gives
\(u=t\in[1/8,3/8]\) and \(v=9/16-u/2\).

In displayed B-speed order the seven fractional phases on this same point are

\[
\left(
u,\ \frac9{16}-\frac u2,\ \frac9{16}+\frac u2,\ \frac18,
\ \frac{11}{16}-\frac u2,\ \frac{11}{16}+\frac u2,
\ \frac{13}{16}-\frac u2
\right).
\]

Every entry lies in \([1/8,7/8]\) for the entire interval
\(1/8\le u\le3/8\), and the fourth is exactly \(1/8\). Combined with integer
orbit recovery, this proves the one-segment all-q candidate directly. It uses
one rounding and one rational time evaluation; no lookup of exceptions is needed.

The [separate supplement](../reviews/2026-09-29-cc-b-ray-transfer/single_segment_review.md)
checks this formula using the same 24 archived q inputs and their reflections,
with the continuous phase and unbounded coverage argument. These are additional
selected-time evaluations on those inputs, not a larger q scan. This smaller
certificate demonstrates that a successful transfer need not be maximally
compressed. The source record and frozen selection remain available.

## 6. Adequacy and the boundary of this transfer

**Representation/version:** CC segment discovery with explicit ray adapter,
version 1; the frozen discovery rule itself is unchanged. The reviewed P3-only
certificate is a subsequent output compression with its own verification.

**Question/output:** one physical \(1/8\)-safe witness for every integer
\(q\ge2\) on B, with the selected stationary reference fixed.

**Domain and operation:** the same seven torus forms and closed floor, translated
clock/orbit coordinates, fixed parent-edge candidates, integer rounding and
recovery. The common-start and integer-speed assumptions remain explicit.

**Retained information:** native and canonical coordinates, orbit sign, clock,
fold, row permutation, lap/phase identities, closed candidate geometry,
deterministic choices, tail and prefix coverage, and preprocessing/online costs.

**Omitted information:** optimum values, complete maximizing sets, most safe
times, face interiors and new face-cut edges. The unchanged richer atlas and
B optimum review remain available for those questions. The selected separation
of \(1/8\) is not generally optimal; that omission is intentional here.

**Source and recovery:** parent input and frozen discovery code at
`6b2b9316dbc87499a1cb5184aadbd6614d4d6c32`; the native B map is also recorded in
[the earlier B review](CC_OTHER_RAY_REVIEW_2026_09_29.md). Undo the coordinate
swap to recover native torus points, then use \(t=y\) and \(\ell_i=m_i-a_iH\).
Restore the full labelled geometry before changing the requested output.

**Evidence/limits:** an all-q coverage argument, separately authored internal
AI checks and declared physical controls. Success on A and B supports these
two translations; it does not force compatible segments for arbitrary
coefficient families or references.

**Failure/enrichment trigger:** wrong clock, orbit sign, lap coefficient,
display permutation, fold, band, cutoff or prefix coverage. A candidate-class
failure requires examining omitted geometry before drawing a physical
conclusion. A new substitution or requested output needs a new adequacy check.

**Framework adaptation:** standard affine coordinate substitution translates
the CC carrier while retaining the existing clipping, integer-width and finite
covering operations. No new external theorem or formal language is needed for
this step. Credit for standard methods and historical source discussions remains
in the prior notes; no fresh literature or novelty assessment was undertaken.
The concrete change and rechecked guarantees are documented above, following
the [working rules](CC_REPRESENTATION_RULES.md).

**Next bounded question:** derive the integer-orbit and physical recovery map
for a general primitive substitution \((p,q)\) in the same seven-form model,
then ask which parameter directions these segments actually cover. The B clock
\(t=y\) cannot simply be carried over when both parameters vary. No such
extension or new physical scan has been performed in this transfer.
