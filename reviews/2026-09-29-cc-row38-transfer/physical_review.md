# Separate physical review of the frozen (3,8) transfer

September 29, 2026. **PASS within the frozen scope.** This is a separately
structured internal AI review, not external, human, blind or formal review.
It adapts the prior coordinate-lap reviewer without importing production code.
The protocol was read and its hash asserted before the new-row evaluation.

## Recovery and same-point safety

The reviewed family is
(0,p,q,p+q,2p+q,3p+q,3p+2q,3p+8q), with positive integer p,q. Its seventh
moving speed strictly exceeds all preceding speeds. Direct set cardinality
agrees with the domain condition p!=q on every control; (1,1) remains a
repeated-speed auxiliary.

For d=gcd(p,q), P=p/d and Q=q/d, the reviewer projects each candidate's
endpoints under H=Qx-Py. A closed interval contains an integral orbit exactly
when ceil(lower)<=upper. It solves the affine segment directly at that first
integer, preserving the candidate's joint lap labels and actual selected point.

Physical recovery begins with a coordinate-lap congruence, rather than the
production Bezout clock:

- i is the unique residue in 0,...,P-1 with Q*i=-H mod P (i=0 for P=1);
- j=(Q*i+H)/P, tau=(x+i)/P, and t=tau/d;
- the physical lap for row (a,b) with torus lap m is m+a*i+b*j.

Every physical speed times t is multiplied directly. Its floor and fractional
part agree with the recovered laps and the same-point labelled phases.
Reflection uses the archived unit-period convention 1-t. Two independently
constructed shifted Bezout pairs yield the same primitive time and laps.
The two nonprimitive controls (4,6) and (6,10) agree exactly with their
primitive controls after the declared time/speed scaling.

The reviewer checks the saved contact interval, integer, segment parameter,
point, selector order, number of segment tests, Bezout identities, clock floor
and Euclidean division count. It also checks all labelled endpoint bands.
Because each row is affine and has one fixed lap on a candidate, these
endpoint inequalities certify safety throughout that candidate, including
all five singleton candidates.

## Frozen results

All 18 declared parameter pairs have a safe witness and attained minimum
1/8. Seventeen controls have eight distinct speeds including the reference.
The exact review includes:

| Check | Count |
| --- | ---: |
| Physical witnesses | 18 |
| Selected phase checks | 126 |
| Selected lap checks | 126 |
| Reflected phase checks | 126 |
| Reflected lap checks | 126 |
| Alternative Bezout recoveries | 36 |
| Candidate endpoint-band checks | 532 |
| Conditional diagnostic pairs | 0 |

These are the protocol controls only. No extra parameter scan was run.
The first complete physical review execution passed. Additional exact
contact-record and Euclidean-division comparisons were then added before
finalizing the same frozen review; they also passed. There was no production
or reviewer arithmetic correction, and no changed trial or control list.

## Known failed input and repair

The old fixed L/C rule is reconstructed directly from its segment, without
calling the coefficient checker. Its four already recorded rejection attempts
agree exactly. At (p,q)=(1,4), the speeds are
(0,1,4,5,6,7,11,35).

| Construction | Time | Seventh phase | Seventh distance | Overall minimum |
| --- | --- | --- | --- | --- |
| Old fixed L/C selector | 5/16 | 15/16 | 1/16 | 1/16 |
| Emitted compiler menu | 17/56 | 5/8 | 3/8 | 1/8 |

The new witness uses P2:E0-1:K2, the second menu entry. The two records remain
separate. This pair is repaired; the claim of uniform repair additionally
needs the separately reviewed width argument and finite residual coverage.
A failed time never implies that this configuration has no lonely time.

## Endpoint operation and representation adequacy

Opening both endpoints of the complete three-entry menu removes all contacts
at (1,1), (1,2), (2,3), (5,2) and (4,6). These are five parameter controls,
four primitive directions, and include the labelled auxiliary (1,1).
Opening every one of the 38 supplied candidates removes all contact at none
of the 18 controls. Both operations were evaluated and saved separately.
No open-menu or open-all-candidate universal claim follows from this list.

Singleton candidates have no open interior. A nondegenerate segment whose
projection is constant and integral still has interior contacts. These cases
are handled distinctly in the reviewer.

The frozen compiler returned COMPLETE_COVER_CERTIFICATE, so the conditional
richer-parent diagnostic was **not triggered or executed**. Its reviewer path
retains all parent halfspaces, changed laps 1..8, the declared integer-orbit
range and 10,000-section preflight bound, but this successful experiment does
not provide execution evidence for that conditional code path.

This result locates an adequate representation for this test: the supplied
floor-edge candidates retain enough alternatives to repair the compact
selector's failure. It does not demonstrate that recovering parent interiors
was necessary, nor establish general portability.

## Reproduction and limits

From the repository root:

```sh
python3 reviews/2026-09-29-cc-row38-transfer/physical_review.py
```

The deterministic JSON agrees with the saved physical_review.json. It records
input hashes, every candidate endpoint check, all 18 physical records, both
endpoint operations, gcd controls and the known failure comparison.

The review checks exact recovery and finite physical controls. It does not by
itself prove infinite coverage, optimality, the complete safe set, a different
reference-runner statement, novelty or new existence coverage. The universal
construction remains an internally reviewed proof candidate.
