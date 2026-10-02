# Separate physical review of the boundary-phase screen comparison

September 29, 2026. **PASS within the frozen scope.** The review imports no
production code. It reconstructs coordinate-lap clocks, direct physical
products, closed/open contacts, every contact in the frozen comparison union,
and the declared first lost-witness diagnostic. This is internal AI review,
not blind, human or formal proof.

The frozen protocol and all input SHA-256 and Git blob identities are checked.
The first complete reviewer execution passed without correction. No additional
parameter scan, alternative row or post-result candidate modification was run.

## Shared-time and domain checks

The rows are
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8),(54,26).
All nine moving phases and all three added lap labels are checked at one
selected point and one physical time. The new row dominates the earlier rows,
so ten distinct speeds including the reference require exactly p!=q and p!=2q.
The direct cardinality check agrees on every emitted control witness.

Each branch uses the same 22 frozen pairs: 18 primary configurations and four
auxiliaries, (1,1),(2,1),(2,2),(4,2), each with nine distinct speeds. These
are two evaluations of the same declared input list, not 44 distinct speed
configurations. The restricted branch uses all its candidates because it
has no complete primary guarantee. The full branch uses its emitted menu.

For d=gcd(p,q), P=p/d, Q=q/d and integral H=Qx-Py, the reviewer solves
Q*i=-H modulo P with 0<=i<P, puts j=(Q*i+H)/P, tau=(x+i)/P and t=tau/d.
For P=1, i=0. The physical lap for row (a,b) with torus label m is m+ai+bj.
This route is separate from the production Bezout clock. Direct speed products,
reflection 1-t, two alternative Bezout choices and five gcd scaling controls
agree. Candidate identity, first integral contact, interval, parameter and
point are also checked.

## Branch results

| Check | Restricted screen | Full clipping |
| --- | ---: | ---: |
| Frozen parameter controls | 22 | 22 |
| Recovered safe witnesses | 20 | 22 |
| Primary witnesses | 16 | 18 |
| Auxiliary witnesses | 4 | 4 |
| Candidate misses among the controls | 2 | 0 |
| Selected phase checks | 180 | 198 |
| Selected physical lap checks | 180 | 198 |
| Reflected phase checks | 180 | 198 |
| Reflected physical lap checks | 180 | 198 |
| Alternative Bezout recoveries | 40 | 44 |
| Candidate endpoint-band checks | 90 | 1,098 |

Every recovered witness attains minimum exactly 1/8. The restricted control
misses are (1,2) and (1,4); they remain candidate-contact misses, not physical
nonexistence statements. The full branch recovers witnesses for both.

The endpoint-band checks cover all nine labelled rows at both endpoints of
each candidate: five restricted and 61 full. Fixed joint laps and affinity
certify safety throughout each closed candidate.

## Candidate-class comparison and recovered evidence

The reviewer independently tests all candidates against every pair in the
47-pair union of the two residual domains: 3,102 candidate/pair contacts in
total. It matches every contact-id list and first-contact record. All five
restricted candidates are identical to corresponding full candidates,
including endpoints, labels and original edge parameters.

The restricted candidate class misses exactly the three primary directions
(1,2),(1,4),(5,1) within this exhaustive comparison; the full class hits each.
There are no lost auxiliary directions and no directions missed by both
classes. Pair (5,1) belongs to the frozen comparison union, not the 22 physical
controls. No extra physical control or separate time scan was added for it.
The extension from this union to all positive primitive directions depends
on the separately reviewed finite-reduction argument for the two leaders.

The lexicographically first lost primary pair is (1,2). Its first full
contact is P0:E0-1:K1:L2:M13, from source P0:E0-1:K1:L2. Independent recovery
gives

\[
(x,y)=(1/8,1/4),\qquad H=0,\qquad t=1/8.
\]

The ten distinct speeds including the reference are
(0,1,2,3,4,5,7,10,19,106). Their nine moving phases are

\[
(1/8,1/4,3/8,1/2,5/8,7/8,1/4,3/8,1/4),
\]

with physical laps (0,0,0,0,0,0,1,2,13). The minimum is 1/8.
This additional diagnostic record is retained separately from the branch
control counts above.

The coefficient relation is independently reconstructed:
(54,26)-(6,2)=8*3*(2,1). However, the source's raw core value 2x+y has endpoint
values 15/32 and 1/2. It is neither constant nor a retained core boundary
m+1/8 or m+7/8. The exact whole-source screen predicate therefore fails.
The saved decision is NO_SCREEN_CERTIFICATE, with no accepted reason.
A partially clipped full candidate still supplies the physical witness.
This is a concrete loss from the sufficient screen's restriction, not an
unsafe-source or absence-of-loneliness verdict.

## Endpoint operations remain separate

For the restricted branch, opening either its emitted menu or all five
candidates newly removes contacts at (1,3),(2,3),(4,6): three controls,
two primitive directions. These counts exclude (1,2) and (1,4), which already
lack closed restricted contacts.

For the full branch, opening its five-entry menu newly removes contacts at
(1,2),(1,3),(1,4),(3,1). Opening all 61 full candidates newly removes none
of the 22 control contacts. These operations concern different representations;
no universal open-candidate guarantee follows from the control list alone.

Point records have no open interior. A nondegenerate segment with constant
integral projection can retain open contacts. The independent contact method
keeps these cases distinct.

## Conditional paths, reproduction and limits

The full compiler emits a complete certificate, so its full-parent diagnostic
is **NOT_TRIGGERED**. The restricted branch's misses do not trigger that
parent diagnostic; they are diagnosed through the immediate full-candidate
recovery source as the protocol specifies. No full physical-time band-union
diagnostic was executed. Its declared 10,000 speed-sum and 200,000
interval/band-test caps remain separate from any mathematical exhaustion.
There is no threshold change or 1/10 regeneration in this experiment.

From the repository root:

```sh
python3 reviews/2026-09-29-cc-phase-screen/physical_review.py
```

The deterministic physical_review.json retains both branch records, endpoint
checks, scaling controls, every comparison contact, subset checks, the omitted
source predicate and the independently recovered witness.

The CC distinction is now directly testable: a sufficient safety certificate
for selected whole sources does not ensure the restricted sources retain
coverage. Recovering the full clipped candidates restores the missing evidence
here. Universal coverage and exhaustive-comparison arguments remain internally
reviewed proof candidates. No claim is made about arbitrary coefficient rows,
optimum times, complete physical safe sets, other references, new existence
coverage or originality.
