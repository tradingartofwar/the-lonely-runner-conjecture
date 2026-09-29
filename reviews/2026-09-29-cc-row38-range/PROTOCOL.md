# Frozen coefficient range of the row-(3,8) selector

September 29, 2026. Input head 64bda7a065abcff312ab0cac17f5b12a49b91221.
Frozen before new coefficient enumeration and physical trials. The algebraic
proposals below were derived before freezing and are to be reviewed, not
presented as blind predictions. No new discovery, clipping or optimization.

## Fixed selector, domain and four distinct contracts

Keep the emitted first-integer rule unchanged: leader L is y=9/8-x,
1/4<=x<=3/8. Its only missed primitive directions are (1,4),(2,1),(1,1).
The used fallback points are F=(17/56,3/14), G=(9/28,9/56), and auxiliary
C=(1/8,1/8), respectively. Keep the complete emitted menu as source; no
retuned compiler run. Normalize d=gcd(p,q), P=p/d,Q=q/d, H=Qx-Py in Z.

Vary only the positive integer seventh row (A,B). First six rows remain
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2); threshold is closed 1/8. Define:

- W: every point of L and the entire first fallback segment S is safe,
  where S is y=9/8-3x, 7/24<=x<=55/168. Exclude unused auxiliary geometry.
- R: every point of L and the two used points F,G is safe.
- T: every actual output for all positive integer p!=q is safe.
- T_all: T and the actual p=q auxiliary output C are safe.

Do not assume T=R, W=R or T_all=T. General eight-distinct-speed use requires
p!=q and (A-a)p+(B-b)q!=0 for the four rows (1,1),(2,1),(3,1),(3,2).
Label their identically repeated coefficient rows as empty domains. Any
seventh failure at p!=q is automatically distinct-speed because the six
core phases are safe. Auxiliary failures do not have that interpretation.

## Proposed exact reductions, to check before enumeration

Put M=P+Q and rho=(P-2M) mod8. On a leader hit rho<=M and
(x,y)=(1/4+rho/(8M),7/8-rho/(8M)). Primitive directions are exactly
M>=2,1<=P<M,gcd(P,M)=1, Q=M-P. The leader support is countable and closed,
with only accumulation point E=(1/4,7/8). Excluding p=q removes only C,
not a leader point. Verify support, closure, missed directions and recovery.

Let delta=A-B and a=(9B+2delta) mod8. The leader raw phase is
(9B+2delta)/8+delta*rho/(8M). E is selected at (2,3). If a=0 E fails.
If delta>0,a=7 or delta<0,a=1, choose j=max(2,floor(7|delta|/8)+1)
on P=1,Q=4j; its positive drift 7|delta|/[8(4j+1)] is <1/4 into danger.

Otherwise for D=|delta|>=14 let c=7-a for positive delta, or a-1 for
negative delta. Then 1<=c<=6, and choose an integer j in the open interval
((7D/(c+2)-1)/4,(7D/c-1)/4). Its length is at least 7D/96>1 and its lower
endpoint is at least 45/16, so floor(lower)+1 is admissible and >=3.
This gives a physical failure at (1,4j), proving T implies |delta|<=13.

After rejecting a=0 and outward boundary cases, the remaining available
margin is >=1/8. For |delta|<=13 and M>=91, drift<=7*13/(8*91)=1/8.
Thus enumerate exactly 2<=M<=91,1<=P<M,gcd(P,M)=1 in increasing M,P order;
include its known fallbacks. The M=91 overlap with the proved tail is harmless.

The joint phase period on L,F,G,C is (A,B)->(A+56,B+56), adding raw values
63,29,27,14 respectively. It is not a phase period on all of S. Complete
T/R/T_all reduction: delta=-13..13, B mod56=0..55, represented by B=b+56,
A=B+delta (1,512 cells). Save every decision, finite failure count and first
failure; a failed tail gate must already have a witnessed finite failure.

R uses one common eighth-grid safe lap for endpoint numerators
2A+7B and 3A+6B, and residues (17A+12B) mod56,(18A+9B) mod56 in [7,49].
T_all additionally requires (A+B) mod8 !=0. W adds one common safe lap
for S endpoint numerators 49A+42B and 55A+24B over denominator168, whose
safe offsets are [21,147]. W implies |A-B|<=6, |A-3B|<=21, hence B<=13.
Enumerate B=1..13,delta=-6..6 with A=B+delta>0; do not infer its bound
from observed acceptance. Record all accepted rows and their shared laps.

## Compare actual coefficient sets, not unlike residue counts

Use the pinned prior 42-class predicate for the old selector. Old acceptance
implies epsilon=A-2B in [-6,6]. New T implies delta=A-B in [-13,13].
Their intersection must satisfy B=delta-epsilon<=19 and A<=32.
Enumerate B=1..19,delta=-13..13,A=B+delta>0, retaining the complete overlap.
If new T=R, its bound may be sharpened afterward, as a deduction only.

The old accepted progression (6+16k,2+8k) has new delta=4+8k and is outside
new T for k>=2. The known new progression (3+56k,8+56k) has old epsilon
-13-56k and is outside old acceptance for every k>=0. Verify these identities
and membership hypotheses. Do not compare class counts as though periods
(16,8) and (56,56) described the same quotient.

## Frozen physical checks and derived certificates

Reuse exactly the prior18 pairs:
(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
(1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10).
Evaluate rows (3,8),(59,64),(6,2) on this list (54 records). Reproduce all
common physical fields of archived (3,8) records. The shift by(56,56) must
preserve times/phases but change seventh laps by the role-specific integers.
Do not assume the p=q auxiliary is safe for (6,2). Check four identically
repeated core rows at (2,3), preserving actual distinctness flags.

For each failed T cell, recover its first failed primitive pair from the
complete reduction. For each T-but-not-T_all cell recover auxiliary (1,1)
separately. These are derived rejection certificates, not held-out trials.
Check physical time, seven speeds, phases, laps, reflection with zero-phase
handling, gcd and exact distinctness. Recompute seventh torus laps.

Add six analytic large-slope controls: delta in +/-14,+/-15,+/-(10^12+14),
D=|delta|, b=(2-2delta) mod8, B=8*(floor(D/8)+1)+b, A=B+delta. These have
left residue2; use the proved open-j construction, retaining strict bounds.
Add old-only row (38,18): construct its new-rule failure analytically and
evaluate the old selector on that same pair, preserving both times/results.

If T exceeds R, choose the positive representative of the first accepted
outside-R cell in delta,b order and evaluate it on the same18 pairs. Otherwise
do not add such controls. Record W/R/T differences from the complete outputs.
The declared (59,64) lift may supply a W-vs-T counterexample; if so exhibit a
strict unsafe point of S by intersecting its raw interval with an integer and
choosing the first integer contact. This is ambient evidence, not necessarily
an actual selected physical point.

## Review, stopping and information loss

Three separately tasked AI reviewers check support/large-slope/tail proofs,
exact classification/comparison without production imports, and physical
coordinate-lap recovery without production imports. Findings may be shared;
no blind, human or formal review claim. Preserve corrections and timing.
Reproduce only these frozen outputs. If a proposed bound fails, record it and
derive a replacement before expanding enumeration; never hide the failure.

Assess which whole-segment obligations preserve the operational question,
which discarded points matter, and whether the p=q auxiliary changes the
coefficient answer. Existing literature attribution and existence coverage
remain pinned; no new priority claim or literature-frontier audit. Universal
results remain internally reviewed proof candidates. No outside contact,
main merge, altered discovery rule, broader scan or unattended work.
