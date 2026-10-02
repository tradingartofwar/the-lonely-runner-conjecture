# Two-parameter coverage compiler protocol — September 29, 2026

Frozen before this implementation's first run. Source branch head:
`17b2fca8541540af52cd6c5bf2b09c26c646d240`.

## Supported question and input boundary

Produce a checkable sufficient certificate selecting one closed 1/8-safe time
for the stationary reference in the seven-form positive integer family
(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q). Distinct speeds require p!=q;
(1,1) remains an explicitly labelled repeated-speed auxiliary in the finite
reduction. This is a development example with a known successful answer,
not blind discovery, a new family trial, optimality or a novelty claim.

Read only the preserved PARENT_INPUT.json and reuse the unchanged `candidates`
clipping function from reviews/2026-09-29-cc-segment-discovery/discover.py.
Recompute the 27 closed labelled candidate records from the six-form parent
geometry. Do not import the old coverage ranking, known selector, child atlas,
optimizer or prior two-segment answer into the compiler. Strip unused A-ray
tail fields. Check all endpoint phases and labels against all seven bands.
Candidate order is numerical parent, edge endpoints, added lap.

## Frozen selection and finite reduction

Orient endpoints lexicographically. A leading segment is eligible precisely
when alpha=dx>0 and beta=-dy>0. Its projected width is alpha*Q+beta*P.
All positive primitive pairs with width>=1 are covered by closed integer
interval contact. Remaining pairs lie in the exact strict rectangle
1<=P<=ceil(1/beta)-1, 1<=Q<=ceil(1/alpha)-1.

Rank eligible records by the number of lattice pairs in this rectangle, then
canonical provenance. Choose the first; do not try alternative leaders if its
subsequent fallback search fails. The rectangle budget is 400 pairs. Stop with
SCOPE_LIMIT before enumeration if the chosen rectangle exceeds the budget.
Enumerate its positive coprime pairs satisfying alpha*Q+beta*P<1, including
(1,1) when applicable, ordered by P then Q. Record the complete domain.

For every candidate and every residual pair, calculate the closed projection
[min(Qx-Py),max(Qx-Py)], round its lower endpoint upward, and retain the
contact exactly when that integer is <= the upper endpoint. Degenerate image
intervals and point records are retained. If an image is constant and integral,
use the first endpoint. Otherwise interpolate the first integer contact.

Start the menu with the leader. Greedily append the candidate covering the most
currently missed residual pairs; break ties by canonical provenance. Stop when
all are covered or every remaining candidate covers zero. This is a sufficient
menu, with no minimality claim. Store the full contact matrix and each step.

## Certificate, arithmetic, and failure outputs

Emit rows, threshold, all candidate endpoints and labels, ranking/bounds, chosen
leader/menu, exact residual domain, contact matrix and fallback steps. Include
hashes of input and reused clipping implementation. The evaluator consumes the
emitted certificate (not hardcoded segment identities), normalizes d=gcd(p,q),
P=p/d,Q=q/d, uses H=Qx-Py, and recovers tau={r*x+s*y}, t=tau/d for rP+sQ=1.
Store torus/physical laps using the existing explicit recovery identity.

Failure statuses must distinguish INVALID_CANDIDATE, NO_DESCENDING_SEGMENT,
SCOPE_LIMIT and UNCOVERED_PRIMITIVE_PAIRS. They concern this procedure and
candidate class, not a counterexample to loneliness. Uncovered output names
every missed residual pair. A budget limit is not a mathematical failure.

## Bounded controls and separate review

No physical scan. Reuse exactly the prior 18 controls:
(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
(1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10).
Check phases, physical laps, reflection and an alternative Bezout choice.
Compare generated witnesses to the archived selector output only after the
compiler run; matching is not a premise or a requirement for a valid witness.

Fixed failure controls: feed only non-descending candidates; feed only the
selected leader (test uncovered pairs); set rectangle budget to zero; corrupt
the leader's first lap by +1. Check that excluding both endpoints of all menu
segments loses the already known (1,4) witness. These are ablations of this
input, not additional families or parameter scans.

Separate AI reviewers will (a) reconstruct the residual/contact certificate
without importing compiler code, test corruption/failure semantics and inspect
the conditional infinite argument; (b) reconstruct physical time from coordinate
lap congruences, directly check the 18 physical cases and inspect information
loss. Coordinator runs the implementation and reconciles results. AI review
does not constitute human or formal verification.

## Attribution and scope

The elementary width-versus-orbit-spacing mechanism has the credited precedent
in Jain–Kravitz Proposition 7.1 recorded in CC_LITERATURE_COMPARISON_2026_09_29.md.
We adapt its intersection mechanism to threshold-safe segments and positive
directions; optimal-spectrum finiteness is not inherited. Rosenfeld already
covers existence for the family. The advance sought here is automatic assembly
of the explicit certificate. No new external theorem reading is required.

Retain closed equality, joint labels, primitive orbit and physical recovery.
Omit parent interiors and complete safe sets; restore the pinned atlas if the
candidate class is insufficient or a stronger output is requested. Report
preprocessing counts separately from online segment tests and variable-cost
gcd/Bezout arithmetic. Preserve any correction with its timing and impact.
