# Compatibility Calculus: the frozen changed-coefficient test succeeds

September 29, 2026. Input branch:
`50d0379628f4a1097d30bbc55d38c581c4338f02`.

**Result:** the unchanged coverage rule transfers from seventh row (5,2) to
the predeclared row (6,2), producing a different sufficient two-segment menu.
This is evidence of portability to one selected change. It is not a general
portability theorem or new Lonely Runner existence coverage. The complete
construction argument remains an internally reviewed proof candidate.

The [protocol](../reviews/2026-09-29-cc-coefficient-transfer/PROTOCOL.md) fixed
the row, ranking, bounds, controls and conditional failure diagnostic before
any changed-row computation. No alternative row was screened, no ranking was
tuned after the result, and no implementation correction was needed in the
first run. The work and separate reviews are materially AI-generated.

## 1. What changed and what stayed fixed

We increased the first seventh-row coefficient by one, replacing 5p+2q by
6p+2q. The new family is

\[
(p,q,p+q,2p+q,3p+q,3p+2q,6p+2q),\qquad p,q>0.
\]

All parameters are integers. The last five speeds strictly increase and
exceed both initial speeds, so including the stationary reference gives
eight distinct speeds exactly when p!=q. The repeated-speed (1,1) case is
explicitly labelled auxiliary. Common start, selected stationary reference
and closed threshold 1/8 are unchanged.

The implementation parameterizes the old affine edge clipping by the added
row. It imports the hash-pinned compiler's original `compile_records` and
`select` functions without modifying either. The ranking still minimizes
the strict exception rectangle, ties still use numerical provenance, the
rectangle budget remains 400 pairs, and the greedy fallback rule is unchanged.
All previous packages remain read-only.

Before running (6,2), the parameterized clipper reproduces every one of the
old row's 27 candidate records and all original coverage fields exactly.
This regression checks the adaptation against the old implementation; the
changed run then receives the changed geometry as its actual input.

| Recorded quantity | Original row (5,2) | Changed row (6,2) |
| --- | --- | --- |
| Clipped candidate records | 27 | 24 |
| Descending candidates eligible to lead | 10 | 14 |
| Leading segment | P3:E0-1:K2 | P2:E0-3:K2 |
| Bounding rectangle / primitive residual pairs | 21 / 8 | 21 / 8 |
| Full residual contact matrix | 216 entries | 192 entries |
| Actual leader misses | (1,2), (1,4) | (1,2) |
| Selected fallback | P1:E1-3:K1 | P0:E0-1:K1, vertical |

There are no point records in the changed candidate set. The changed clipper
examines the same 24 parent floor edges and 24 edge/lap combinations, within
the predeclared 256-combination cap. None of the resource limits is reached.

## 2. The certificate produced by the fixed rule

The two selected segments, with all seven torus laps, are

| Use | Closed segment | Torus laps |
| --- | --- | --- |
| Leader | 1/4<=x<=3/8, y=7/8-2x | (0,0,0,0,1,1,2) |
| Fallback | x=1/8, 3/16<=y<=1/4 | (0,0,0,0,0,0,1) |

On the leader the fractional phases are

\[
x,\quad 7/8-2x,\quad 7/8-x,\quad 7/8,\quad
x-1/8,\quad 3/4-x,\quad 2x-1/4.
\]

On the fallback they are

\[
1/8,\quad y,\quad 1/8+y,\quad 1/4+y,\quad
3/8+y,\quad 3/8+2y,\quad 2y-1/4.
\]

Each phase lies in [1/8,7/8] at both endpoints and is affine, proving safety
of the entire closed segment. The fourth leader phase and first fallback
phase give minimum distance exactly 1/8 everywhere on their respective
segments. No optimum is asserted.

Set d=gcd(p,q), P=p/d, Q=q/d. The leader's projection by H=Qx-Py is

\[
I(P,Q)=\left[\frac{2Q-3P}{8},\frac{3Q-P}{8}\right],
\qquad |I|=\frac{Q+2P}{8}.
\]

For Q+2P>=8, rounding the lower endpoint upward gives an integer contact,
including width equality. The selected point is

\[
h=\left\lceil\frac{2Q-3P}{8}\right\rceil,
\qquad x=\frac{8h+7P}{8(Q+2P)},\qquad y=7/8-2x.
\]

The complete primitive residual triangle Q+2P<8 is the same eight-pair set
as before, but its intervals and actual misses have changed:

| (P,Q) | Leader interval | First integer | Contact? |
| --- | --- | --- | --- |
| (1,1), auxiliary | [-1/8,1/4] | 0 | yes |
| (1,2) | [1/8,5/8] | 1 | no |
| (1,3) | [3/8,1] | 1 | yes, endpoint |
| (1,4) | [5/8,11/8] | 1 | yes |
| (1,5) | [7/8,7/4] | 1 | yes |
| (2,1) | [-1/2,1/8] | 0 | yes |
| (2,3) | [0,7/8] | 0 | yes, endpoint |
| (3,1) | [-7/8,0] | 0 | yes, endpoint |

The fallback projects to [Q/8-P/4,Q/8-3P/16]. At (1,2) this is [0,1/16],
so h=0 gives (x,y)=(1/8,1/4) and primitive time 1/8. For original parameters
(d,2d), the physical time is 1/(8d). Thus the finite table and width argument
cover every positive primitive pair, and normalization covers all positive
integer pairs in the stated scope.

These equations explain the emitted result after the run. They were not
supplied to the compiler as a new selected menu or exception table.

## 3. Physical recovery and the exact checks

For each selected point, choose rP+sQ=1 and put

\[
T=rx+sy,\quad N=\lfloor T\rfloor,\quad
\tau=T-N,\quad t=\tau/d.
\]

For row (a,b) with torus lap m, use
ell=m+(-as+br)h-(aP+bQ)N. Then (ap+bq)t=ell+(ax+by-m).
The [earlier two-parameter derivation](CC_TWO_PARAMETER_WITNESS_2026_09_29.md)
proves this general recovery identity. The changed seventh row must be passed
through it; the old seventh physical speed and lap cannot be retained.

The declared 18 parameter pairs all produce checked witnesses. They represent
newly evaluated speed configurations under the changed coefficient, even
though the parameter list is reused. There are 17 distinct-speed configurations
and the auxiliary (1,1). All minima are exactly 1/8; selected/reflected phases,
physical laps and alternative Bezout choices agree.

The separate physical reviewer obtains time primarily through coordinate
laps: solve Qi=-h modulo P with 0<=i<P, set j=(Qi+h)/P, then
tau=(x+i)/P. Its physical lap is m+a*i+b*j. This independently reconstructs
the emitted physical quantities without importing the production recovery.
The geometry reviewer instead reconstructs clipped edges through supporting
line/band-boundary intersections, then checks all 24 candidates, 14 ranking
entries, eight residual pairs, 192 full contact entries and greedy choices.

For example (p,q)=(2,3) now selects t=1/8, with speeds
(2,3,5,7,9,12,18) and fractional phases
(2,3,5,7,1,4,2)/8. Scaling to (4,6) gives t=1/16 with the same phases.
This illustrates why reusing parameter names does not mean reusing the old
physical experiment or its old selected time.

The conditional full-parent diagnostic was **not triggered**: no primitive
pair was left uncovered. No parent-interior search or added-geometry repair
was executed, and this successful test does not validate that failure-repair
path. Source hashes, regression and output reproduction are preserved in the
[review package](../reviews/2026-09-29-cc-coefficient-transfer/).

## 4. What the transfer teaches CC

**Leader eligibility and fallback eligibility are different roles.** The
selected fallback is vertical, so it does not meet the descending condition
used for the leading finite reduction. It is nevertheless a valid exact
repair for the remaining pair. The original rule correctly retains all safe
candidates for fallback. This does not establish that the vertical segment
is necessary for every possible certificate; it records what the fixed rule
actually selected.

**Loss from the compact menu is different from loss from its richer source.**
Opening both endpoints of the two selected segments removes contacts for
(1,2), (1,3), (2,3), (3,1), and scaled (4,6) among the 18 controls. Those are
four distinct primitive directions. The physical reviewer also opens all
24 available candidates on the same declared pairs; every pair retains some
contact in that larger set. The compact menu therefore depends on closed
equality for those selections. This is not evidence that all safe witnesses
for those physical instances require endpoints.

**Successful transfer has a specific scope.** The old rule operates on new
geometry and chooses a different menu without changing its ranking or recovery
logic. That is the portability result obtained here. A single minimal
coefficient change does not establish reliable discovery for arbitrary
coefficients, thresholds, references or stronger outputs.

For this one-witness task the existing two-coordinate model remains adequate.
It retains joint labels, closed contacts, the primitive orbit, original gcd,
time/lap recovery, complete residual coverage and role-specific selection.
It still omits most safe points and the full child geometry. The pinned parent
inequalities remain the recovery route when the restricted candidate class
fails or a stronger question is asked.

Preprocessing and online cost remain separate. The emitted menu has two
segments, but gcd/Bezout steps and integer bit lengths depend on the input.
The audit includes all candidates and the finite contact matrix; it is larger
than the data needed for one online witness. No optimal menu or speedup is
claimed.

## 5. Attribution, limits and next question

The [literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md) still governs
the interpretation: Rosenfeld's inspected eight-runner result already covers
existence for seven distinct positive speeds. The threshold-level segment
mechanism has the Jain–Kravitz precedent recorded there; optimal-spectrum
finiteness is not inherited. This experiment checks a particular adapted
construction procedure. It establishes neither priority nor external proof.

A useful next question is to characterize, symbolically, which additional
coefficient rows are compatible with this newly selected geometry. That would
separate the range of a fixed certificate from the compiler's ability to find
different certificates. Freeze that scope before another run; no further
coefficient rows were tested in this experiment.
