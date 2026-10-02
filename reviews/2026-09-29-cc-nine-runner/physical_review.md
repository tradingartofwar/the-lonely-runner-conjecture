# Separate physical review of the joint nine-runner transfer

September 29, 2026. **PASS within the frozen scope.** The reviewer imports no
production code. It uses exact coordinate-lap congruences, direct speed
multiplication and independent endpoint contact calculations. This is a
separately structured internal AI review, not blind, human or formal review.

The frozen protocol hash and every pinned source SHA-256 and Git blob identity
are verified before reviewing the emitted stage. The first complete physical
review run passed. During preparation, the reviewer was aligned with the
production schema: the production witness does not emit segment_tests, so
first-contact identity is independently reconstructed while an explicit test
count is compared only if supplied. That alignment preceded execution and
changed no trial, control, mathematical operation or production behavior.

## Domain and simultaneous recovery

The eight moving rows are
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8).
All eight phases are evaluated at the same recovered time. Both added laps
belong to the same selected point and are retained in every record.

For positive p,q, the first six speeds are distinct exactly when p!=q.
Both added speeds exceed those six. Their equality is
6p+2q=3p+8q, equivalent to p=2q. The direct cardinality check therefore
agrees with the nine-distinct-speed condition p!=q and p!=2q.

The 20 frozen controls contain 16 primary configurations and four auxiliaries:
(1,1),(2,1),(2,2),(4,2). Each auxiliary has eight distinct speeds including
the reference; it is not relabelled as a nine-distinct-speed case.

For d=gcd(p,q), P=p/d and Q=q/d, the reviewer obtains H=Qx-Py from the selected
segment's first integral contact. It solves

\[
Q i\equiv-H\pmod P,\quad 0\le i<P,\qquad
j=(Qi+H)/P,\quad \tau=(x+i)/P,\quad t=\tau/d.
\]

For P=1 use i=0. A row (a,b) with torus lap m then has physical lap
m+ai+bj. Direct products vt recover the same phases and floors. The reviewer
also verifies the production Bezout identities and clock, reflected time
1-t, two alternative Bezout recoveries, selected candidate identity, contact
interval/integer/parameter and Euclidean division count.

Four scaling comparisons are explicit: (4,6) with (2,3), (6,10) with (3,5),
(2,2) with (1,1), and (4,2) with (2,1). Primitive time, point, torus phases
and physical laps agree; speeds and actual times scale oppositely.

## Reached stage and exact results

Only Stage A at 1/8 was reached. Its emitted certificate is complete for all
labelled positive directions, including the auxiliaries. All 20 controls have
safe witnesses, with attained minimum exactly 1/8.

| Check | Count |
| --- | ---: |
| Parameter controls | 20 |
| Primary nine-distinct-speed witnesses | 16 |
| Auxiliary repeated-speed witnesses | 4 |
| Selected phase checks | 160 |
| Selected physical lap checks | 160 |
| Reflected phase checks | 160 |
| Reflected physical lap checks | 160 |
| Alternative Bezout recoveries | 40 |
| Candidate endpoint-band checks | 576 |

The 576 endpoint-band checks cover eight joint labelled bands at both endpoints
of all 36 candidates. Affinity with fixed joint labels makes these endpoint
checks sufficient for safety throughout each closed candidate.

At (p,q)=(1,4), the speeds including the reference are
(0,1,4,5,6,7,11,14,35). The selected time is 17/56. The two added phases are
1/4 and 5/8 at that same time, and the overall minimum is 1/8.
At auxiliary (1,1), the emitted final fallback selects time 7/24; the two added
phases are 1/3 and 5/24. Scaling to (2,2) gives time 7/48 with the same phases.

These are exact checks on the frozen configurations. The infinite guarantee
also depends on the separate coverage argument, which remains a proof candidate.
A 1/8 guarantee implies the requested nine-runner 1/9 threshold by comparison;
it does not establish a theorem for arbitrary nine-runner speed sets.

## Equality and conditional paths

Opening both endpoints of every chosen menu segment removes all menu contacts
at (1,2),(2,3),(4,6): three primary controls representing two primitive
directions. Opening every supplied candidate removes all contacts at none of
the 20 controls. These are distinct operations with separately saved results;
no universal open-candidate coverage claim is inferred from the finite list.

Singleton candidates have no open interior. Nondegenerate segments with
constant integral projection retain interior contacts. The independent
contact function distinguishes these cases.

Stage A already gives a complete primary guarantee. Consequently Stage B at
1/9 is **NOT_TRIGGERED**, and no stage9.json is present. The richer-parent
diagnostic is also **NOT_TRIGGERED**. No direct physical-time diagnostic,
threshold-1/9 geometry, or additional parameter control was evaluated.

The conditional reviewer code can intersect per-speed physical safe-lap
interval unions over one unit period for the one diagnosed primitive pair,
with the first-coordinate phase restricted to at most 1/2. This route is
independent of parent orbit sections and can check a found witness or bounded
exhaustion. It was not exercised here and earns no execution-validation claim.

## Reproduction and scope

From the repository root:

```sh
python3 reviews/2026-09-29-cc-nine-runner/physical_review.py
```

The deterministic output is saved as physical_review.json. It retains every
physical record, both endpoint-contact operations, candidate endpoint bands,
scaling checks and explicit untriggered paths.

The useful CC distinction is simultaneous compatibility: two added rows need
one shared contact and both correct laps. Separate safe times would not pass
this review. Domain cardinality, labelled auxiliaries and endpoint operations
also survive the transfer. The results do not establish optimality, a complete
safe set, arbitrary-coefficient portability, another reference-runner result,
new existence coverage or originality.
