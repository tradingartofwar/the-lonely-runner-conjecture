# Separate coefficient and physical-certificate audit

September 29, 2026. Status: internal AI review of a proof-candidate
implementation. This is neither external human review nor formal proof.

## Method and independence

The reviewer read the frozen protocol, repository evidence rules and the
previous selector-support argument before the new runtime was available.
The independent mathematical routines in `audit.py` were written before
reading production outputs and do not import production code. The reviewer
first checked the 216 old representatives and 48 large rows independently,
then inspected the runtime and adapted field comparisons to its JSON schema.
The audit reads serialized outputs to compare them to these reconstructions.
Findings are shared with the coordinator; this is not a blind replication.

For leader endpoint values z_0 and z_1, the shared integer lap must belong
to the intersection [ceil(z_i-7/8), floor(z_i-1/8)] over i=0,1. This checks
the whole segment against a single connected safe band. C is checked by
its actual fractional value. It independently recovers the simple R
criterion without trusting a stored acceptance table.

For physical recovery the audit first projects the two leader endpoints,
takes the first integer in that interval and solves the contact equation
directly. If the interval misses, it verifies the primitive pair is (1,2)
before using C. With h=Qx-Py, it solves Q i = -h (mod P), 0<=i<P, and sets
j=(Q i+h)/P and tau=(x+i)/P. This yields Q tau=y+j and physical t=tau/d.
Direct multiplication by each actual speed checks the phases and laps;
the independently derived lap relation is m+a i+b j. Reflection is 1-t,
including nonprimitive controls, matching the declared unit-period rule.

## Rejection branch derivation

The precedence is significant. A C collision is tested before the left
endpoint collision; both precede outward-boundary and large-slope formulas.
The finite menu is used only for the remaining |A-2 B|<=13 cases. Its totality
comes from the previous complete 216-cell classification, not from a claim
that eleven directions suffice for arbitrary slopes.

For the outward branch, j=max(2,floor(7 D/8)+1) gives strictly positive drift
7 D/(32 j)<1/4 into the adjacent open forbidden band. For the remaining
large-slope branch, 1<=c<=6 and D>=14. Its open j interval has length
7 D/(2 c(c+2))>=98/96>1, so floor(lower)+1 is strictly below upper and above
lower, including an integer lower endpoint. The lower endpoint exceeds 3,
so the selected j belongs to the actual-output sequence. Both slope signs
are handled by the direction-dependent c and checked physically.

All rejection records must have six safe core phases, a seventh distance
strictly below 1/8, p!=q and eight distinct total speeds. An added speed
coinciding with a safe core speed could not have an unsafe phase at the
same time, so a failed seventh output proves the necessary noncollision
as well as the explicit speed comparison. Accepted rows that identically
repeat (1,1),(2,1),(3,1) or (3,2) retain an empty distinct-speed domain flag;
their auxiliary safety guarantee is still meaningful.

## Frozen-scope results

The independently reconstructed base 216 decisions agree with the archive:
42 accept and 174 reject. The declared new precedence gives 100 finite-menu,
22 outward-boundary, 24 left-collision and 28 C-collision rejections.
Forty returned directions differ from the archive's first-small-direction
certificate. This is an intended change of certificate identity, with no
change of the coefficient decision.

The frozen 48 large-coefficient cases independently give 36 large-slope,
6 outward-boundary and 6 left-collision rejections. All 36 strict intervals
contain the selected integer, and all 48 direct physical failures pass.
The specified delta residues do not trigger a C collision in these 48 cases.

The complete serialized-output audit passes **27,401 field comparisons**:

| Frozen group | Checked records | Result |
| --- | ---: | --- |
| Base coefficients | 216 | 42 accept, 174 reject; all archive decisions agree |
| Period shift K=10^20 | 216 | Same decisions, directions, phases; exact changed laps agree |
| Large coefficients | 48 | All reject; analytic branch evidence and physical failures agree |
| Archived physical configurations | 54 | Direct recovery and all shared archive fields agree |
| Named physical/domain/equality controls | 8 | Safety, failure and repeated-speed flags agree |
| Invalid Python API inputs | 15 | ValueError is recorded separately from mathematical rejection |
| CLI normal and optimized runs | 18 | Statuses and exit codes agree; paired JSON outputs identical |

The coefficient total is 84 accept and 396 reject. Rejection branch totals
are 200 finite-menu, 56 C-collision, 54 left-collision, 50 outward-boundary and
36 large-slope. The report retains all 40 changed baseline rejection pairs.
For accepted periodic pairs it checks leader lap increment 7K and C lap
increment 4K. For rejected periodic pairs it checks unchanged selected points,
times and phases, recomputed torus/physical/reflected laps and unchanged core
records. Large integer values remain exact throughout.

The first serialized audit run reached the CLI scope comparison and found a
review-harness assumption about unspecified argument placement: the coordinator
used p=2 for missing q and placed the invalid text `two` in B; the reviewer
had assumed p=4 and `two` in A. Aligning those two harness descriptors with
the actual frozen controls produced the pass above. No mathematical or
production defect, additional trial or change of the protocol resulted.

`audit.json` records input hashes, branch totals, field counts and all 40
certificate-identity differences. Reproduce from the repository root with
`python3 reviews/2026-09-29-cc-coefficient-checker/audit.py` after producing
`validation.json`. No additional coefficient or physical trial is introduced
by this review.

## Information-loss checkpoint

The acceptance bit alone omits which common lap band supplied the guarantee,
the distinct-speed domain and how to recover a physical witness. A rejection
bit alone omits the explicit failing input and the fact that only this
selector failed. The audited records must retain those distinctions. Large
periodic shifts preserve phases and directions while changing exact laps;
reusing old lap labels would not be a valid certificate translation.
