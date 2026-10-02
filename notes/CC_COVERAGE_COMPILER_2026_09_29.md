# Compatibility Calculus: compiling a two-parameter coverage certificate

September 29, 2026. Input branch snapshot:
`17b2fca8541540af52cd6c5bf2b09c26c646d240`.

**Status:** implemented exact certificate assembly for the existing family;
the universal argument remains an internally reviewed proof candidate.
This is materially AI-generated work. The successful segments were already
known when the procedure was designed. It is not a blind discovery experiment,
a new family result, or an external verification of the earlier proof.

The new [compiler](../reviews/2026-09-29-cc-coverage-compiler/compiler.py)
recomputes the preserved candidate geometry, selects a leading segment, derives
its entire finite exceptional domain, finds fallback contacts, and emits a
[machine-readable certificate](../reviews/2026-09-29-cc-coverage-compiler/certificate.json).
The evaluator then reads that serialized certificate and recovers physical
times. Neither selected segment identity nor exceptional pair is hardcoded in
the compiler's coverage rule.

## 1. Input and fixed selection rule

The supported family and question are unchanged:

\[
V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q),\qquad p,q\in\mathbb Z_{>0}.
\]

Select one time when the stationary common-start reference is at least 1/8
from every moving runner. The eight speeds are distinct when p!=q. The
repeated-speed case is retained only as a labelled auxiliary in the reduction.
No optimal value, full safe set, or changed reference is requested.

The [protocol](../reviews/2026-09-29-cc-coverage-compiler/PROTOCOL.md) was frozen
before the new implementation's first run. The compiler reads the existing
six-form PARENT_INPUT.json and reuses only the pinned clipping function from
the parent-edge discovery program. It does not call that program's old A-ray
ranking, read the known two-segment selector, or use the full child atlas.
The original 24 floor edges give 27 closed labelled records. All seven bands
are checked at both endpoints; affine convexity certifies the whole segment.

Orient each segment so its endpoints are lexicographically ordered. It can
lead the certificate exactly when its increment is (alpha,-beta), with both
alpha and beta positive. Rank these descending candidates by

\[
B=(\lceil1/\beta\rceil-1)(\lceil1/\alpha\rceil-1),
\]

then by numerical parent, edge and lap provenance. B is the size of a strict
bounding rectangle for possible exceptions. Choose the first candidate; the
rule does not backtrack over leaders. The predeclared budget is 400 rectangle
pairs, checked before enumeration. A greedy fallback step maximizes newly
covered residual pairs, using the same provenance tie-break. This produces
a sufficient menu, with no claim of a minimum-size menu or best ranking.

## 2. Why the remaining check is finite

Let d=gcd(p,q), P=p/d, Q=q/d. Physical compatibility is the integral projection
H=Qx-Py. On a descending segment its width is

\[
W(P,Q)=\alpha Q+\beta P.
\]

If W>=1, the closed projected interval contains its rounded-up lower endpoint.
Interpolation recovers the same jointly safe point. Thus only W<1 needs a
separate check. Positivity implies

\[
1\le P\le\lceil1/\beta\rceil-1,\qquad
1\le Q\le\lceil1/\alpha\rceil-1.
\]

Enumerating every coprime pair in that rectangle satisfying W<1 is therefore
a complete finite reduction for this supplied segment, not a parameter-box
experiment offered as evidence outside the box. Width below one is not itself
a miss: every residual interval still receives its exact integer-contact test.
Point records and constant projection intervals also remain valid candidates.

For the present input there are ten descending records. The leading record is
P3:E0-1:K2, with alpha=1/8 and beta=1/4. Its rectangle has 21 pairs,
P<=3 and Q<=7. The strict width condition is Q+2P<8, leaving precisely eight
primitive pairs, including auxiliary (1,1):

| P | Residual Q values | Leading segment misses |
| --- | --- | --- |
| 1 | 1,2,3,4,5 | 2,4 |
| 2 | 1,3 | none |
| 3 | 1 | none |

The full 27-by-8 matrix has 216 exact contact tests. The greedy step chooses
P1:E1-3:K1 and covers both misses. The emitted menu is consequently the same
two segments as the earlier hand-derived construction:

| Order | Segment | Projection interval |
| --- | --- | --- |
| 1 | 3/8<=x<=1/2, y=9/8-2x | [3(Q-P)/8,(4Q-P)/8] |
| 2 | 1/8<=x<=5/24, y=7/8-3x | [(Q-4P)/8,(5Q-6P)/24] |

The identities and intervals above are reported outputs and derived formulas,
not selection hints passed into the new compiler.

## 3. From the emitted record to actual runners

The evaluator tries the generated menu in order, takes the first integer
contact, and interpolates its point (x,y). For rP+sQ=1, put

\[
T=rx+sy,\quad N=\lfloor T\rfloor,\quad \tau=T-N,\quad t=\tau/d.
\]

For coefficient row (a,b) and its retained torus lap m, the physical lap is

\[
\ell=m+(-as+br)H-(aP+bQ)N.
\]

Then (ap+bq)t=ell+(ax+by-m), preserving the same safe phase. The existing
[two-parameter note](CC_TWO_PARAMETER_WITNESS_2026_09_29.md) proves the orbit
equivalence, clock and lap formulas, including Bezout-choice independence.
The compiler adds automatic certificate assembly; it does not change those
identities or promote their proof status.

The evaluator is intended for this generated record. It checks the selected
segment's safety and recovered physical identities, but is not a complete
validator for arbitrary externally supplied certificates. Verification of the
whole coverage table and selection rule is a separate task in this package.

Only the previous 18 physical controls were used: 17 distinct-speed cases and
the labelled (1,1) auxiliary. The generated witnesses have minimum exactly
1/8. Reflection, physical laps and alternative Bezout recovery are checked.
The separate physical reviewer recovers the clock through coordinate laps:
solve Q*i=-H modulo P with 0<=i<P, set j=(Q*i+H)/P, and obtain
tau=(x+i)/P, with physical laps m+a*i+b*j. This changes the checking method,
not the configurations tested. The package records exact comparisons to the
archived selector only after the new run.

## 4. Failures that carry useful information

Four predeclared ablations check distinct outcomes:

| Input change | Output | Meaning |
| --- | --- | --- |
| Keep only non-descending candidates | NO_DESCENDING_SEGMENT | This sufficient finite-reduction rule cannot start. |
| Keep only the selected leader | UNCOVERED_PRIMITIVE_PAIRS: (1,2),(1,4) | Every supplied candidate misses each listed pair. |
| Set the rectangle budget to zero | SCOPE_LIMIT, zero pairs enumerated | The resource policy stops the check. |
| Increase the leader's first lap by one | INVALID_CANDIDATE | Its labelled endpoints violate safety. |

None is a counterexample to loneliness. The outcomes carry different amounts
of information. NO_DESCENDING_SEGMENT and SCOPE_LIMIT do not establish that
the supplied candidate class cannot cover all directions. By contrast, the
completed contact table behind UNCOVERED_PRIMITIVE_PAIRS proves that every
supplied candidate misses each listed pair: the greedy loop stops only when
none covers a remaining pair. No different leader or menu drawn solely from
those same records can repair that miss. Additional geometry may do so, as
the existing P1 record repairs the deliberately restricted leader-only input.

Closed equality remains consequential. For (1,4), the leading interval is
[9/8,15/8], which contains no integer. The fallback interval is [0,7/12]; its
only integer is the endpoint zero. Opening both selected segments removes
the menu's witness, even though the actual closed problem is safe.

## 5. Evidence and CC adequacy checkpoint

The coverage reviewer reconstructs clipped edge geometry by supporting-line
and band-boundary intersections, without importing the compiler or reused
clipping code. The physical reviewer uses the coordinate-lap reconstruction
above. Reports, scripts, exact outputs, input hashes and reproduction results
are in the [review package](../reviews/2026-09-29-cc-coverage-compiler/).
These are separately tasked AI checks, not external human or formal proof.

The current representation carries enough information for one witness:
joint endpoints and labels, closed contact, the positive primitive domain,
complete exception coverage, and physical recovery. The new addition is a
record of why the menu covers an unbounded domain and why a failed attempt
failed. Parent interiors, newly created child edges and most safe points are
still omitted. Stronger questions or candidate-class failure require returning
to the pinned parent inequalities and full child geometry.

Preprocessing used 24 floor edges, 27 clipped records, 10 descending candidates,
21 rectangle pairs and 216 residual contact tests. Online selection uses at
most two segment tests for this emitted menu, plus gcd/extended-Euclid work
and arithmetic with parameter-dependent bit lengths. The complete audit
record retains all candidates and the contact matrix; it is larger than the
two-segment data needed to evaluate a witness. No speedup or minimal-storage
claim is made.

The [literature comparison](CC_LITERATURE_COMPARISON_2026_09_29.md) continues to
govern attribution: Rosenfeld already covers existence; Jain–Kravitz
Proposition 7.1 supplies a close segment-intersection precedent. This adapts
that mechanism to threshold-safe segments and positive directions without
inheriting optimal-spectrum finiteness. The specific certificate's originality
and the reliability of discovery beyond this development example remain open.

The next useful experiment is a predeclared transfer to a changed seventh
coefficient row, with the parent geometry fixed and explicit failure bounds.
That requires parameterizing the clipping input and checking the changed
distinct-speed domain before any run. No such transfer is performed here.
