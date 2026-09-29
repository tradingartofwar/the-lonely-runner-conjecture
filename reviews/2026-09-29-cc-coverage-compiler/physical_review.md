# Separate physical and representation review

September 29, 2026. **PASS within the frozen scope; no result-level defect found.**
This is a separately tasked, differently structured AI review. It does not
constitute human, external, or formal verification, and does not promote the
underlying construction from an internally reviewed proof candidate.

The review consumes the emitted `certificate.json` and compares against
`run.json`. It imports neither `compiler.py` nor the archived selector. The
coordinator's implementation was inspected only after the separately written
physical reconstruction passed. No optimizer, broad scan, new parameter pair,
new reference runner, or external theorem lookup was used.

## Reconstruction independent of the compiler clock

For each emitted menu segment, the reviewer computes the first integer in its
closed projected interval and interpolates the corresponding point. It reads
segment identities, endpoints and joint lap labels from the certificate; the
successful segment names are not hardcoded selection premises.

Let `d=gcd(p,q)`, `P=p/d`, `Q=q/d`, and `h=Qx-Py`. Instead of first using
Bezout coefficients to recover time, solve the coordinate-lap congruence

\[
Qi\equiv-h\pmod P,\qquad 0\le i<P,
\qquad j=\frac{Qi+h}{P}.
\]

When `P=1`, take `i=0`; otherwise invert `Q` modulo `P`. Set

\[
\tau=\frac{x+i}{P},\qquad t=\frac\tau d.
\]

The defining relation gives `P tau=x+i` and `Q tau=y+j`. Since `0<=x,y<1`,
these integers are precisely the two coordinate laps, and `0<=tau<1`.
For row `(a,b)` with joint torus lap `m`, this directly yields

\[
(ap+bq)t=(aP+bQ)\tau
        =m+ai+bj+(ax+by-m).
\]

Thus the independently recovered physical lap is `m+a*i+b*j`. The reviewer
also computes the actual phase and floor from each physical product `v*t`;
all three descriptions agree. This avoids relying on the compiler's Bezout
clock and lap identity as the primary reconstruction.

Bezout choices are then checked separately. The reviewer constructs another
solution using an inverse modulo `Q`, shifts its coefficients by both
`(-Q,+P)` and `(+Q,-P)`, and verifies the recovered clock and all seven laps.
The familiar general cancellation remains valid: a shift by `(kQ,-kP)` changes
the unwrapped clock and its floor by the same integer `k*h`, leaving the
fractional clock and physical laps unchanged.

## Exact finite results

Only the protocol's 18 archived controls were evaluated:
`(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),`
`(1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10)`.
The first is the explicitly labelled repeated-speed auxiliary; the other
17 have seven distinct positive moving speeds.

| Check | Result |
| --- | --- |
| Menu selection, selected point, time and all physical outputs versus `run.json` | All 18 agree exactly |
| Direct selected phases and laps | 126 phase and 126 lap checks pass |
| Direct reflected phases and laps at `1-t` | 126 phase and 126 lap checks pass |
| Alternative Bezout recoveries | 36 clocks and their lap vectors agree |
| Selected menu's closed endpoint bands | All 28 closed-band memberships pass (56 scalar inequalities) |
| Normalization controls `(4,6)` and `(6,10)` | Correct gcd, primitive orbit and time scaling |
| Opening both endpoints of every menu segment at `(1,4)` | Every menu contact disappears |

For each selected segment, at least one phase is constant at a safety boundary
at both endpoints. Affinity therefore gives both joint safety and selected
minimum exactly `1/8` throughout that segment. This is an attained value,
not an optimal-value assertion.

The archived off-axis control `(p,q)=(2,3)` gives point
`(13/28,11/56)`, `h=1`, coordinate laps `(i,j)=(1,2)`, and
`tau=t=41/56`. Its first coordinate is below `1/2` while physical time exceeds
`1/2`; the stored fold is not a physical clock cutoff. Reflection at `15/56`
has complementary phases and laps `v-1-ell`, as checked directly.

The scaled controls preserve their primitive point and phases, with

\[
t(4,6)=\frac{41}{112}=\frac{t(2,3)}2,
\qquad
t(6,10)=\frac{41}{176}=\frac{t(3,5)}2.
\]

The underlying general orbit condition is `qx-py in d Z`, equivalent to
`Qx-Py in Z`. Keeping only raw integrality would lose the primitive component
restriction. This review uses the two declared scaled controls and the
algebraic identity, without adding a new negative parameter fixture.

For `(1,4)`, the leader has no closed integer contact; the fallback's closed
contact is `(x,y)=(1/8,1/2)`, giving `t=1/8`. Opening that segment removes its
only contact. The equality convention is therefore consequential here.

## Information loss, adequacy and cost

| Retained distinction | Why it changes the supported result |
| --- | --- |
| Shared point, all seven labels and closed bands | Separately safe marginal values do not establish joint safety |
| Primitive direction and original gcd | Raw integer contact can include the wrong orbit component; time must scale back |
| Coordinate laps or an equivalent checked Bezout recovery | Geometric safety alone does not supply physical time or physical laps |
| Closed endpoints | The declared `(1,4)` witness is otherwise lost |
| Chosen menu versus complete safe set | A sufficient witness construction cannot answer optimum or all-witness questions |
| Preprocessing versus online evaluation | Constant menu length does not make integer arithmetic constant cost |

For the supported question—one stationary-reference `1/8`-safe time in this
fixed positive family—the two-coordinate model plus primitive arithmetic is
adequate. No larger model is required by these checks. The emitted provenance,
full candidate list, finite domain, contact matrix, and selection steps make
the compilation reviewable. The pinned parent geometry remains the recovery
route if the candidate class is insufficient; stronger outputs require
restoring richer geometry and checking their own obligations.

The emitted preprocessing counts are 24 parent floor edges, 27 labelled
clipping records, 10 descending records, a 21-pair rectangle, eight residual
primitive pairs and 216 candidate/pair contacts. Their reconstruction belongs
to the separate coverage review. The resulting online menu requires at most
two segment tests. The actual evaluator also validates endpoint bands and
computes gcd/Bezout arithmetic; integer sizes and Euclid iteration counts are
parameter dependent. The physical review makes no constant-time or minimal-menu
claim.

The conditional infinite argument remains separate from the 18 controls:
a descending segment has width `alpha*Q+beta*P`, width at least one supplies
a closed integer contact, and the strict positive complement lies in a finite
rectangle whose actual misses need verified fallbacks. Finding no descending
candidate, exhausting a budget, or missing a residual direction describes the
procedure's limits, not a counterexample to loneliness. The emitted named
failure statuses preserve this distinction.

The current attribution/scope record is appropriate: the segment-intersection
mechanism has the Jain–Kravitz precedent recorded in the literature comparison;
its optimal-spectrum conclusion is not inherited here. Rosenfeld already
covers existence for this family. This run automates a previously known
successful certificate in a development example. It supplies no new existence
domain, held-out discovery result, or originality determination.

## Reproduction

From the repository root, after the coordinator has emitted the frozen files:

```sh
python3 reviews/2026-09-29-cc-coverage-compiler/physical_review.py
```

The JSON output is preserved as `physical_review.json`, with hashes of the
certificate, run, protocol and reviewer implementation. The recorded output
reproduces byte-for-byte. The coordinator should repeat the review if any
of those inputs changes.
