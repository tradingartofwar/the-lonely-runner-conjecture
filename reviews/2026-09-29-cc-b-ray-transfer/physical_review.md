# B-ray physical review — preparation record

Author: separate internal AI reviewer (`b_physical_review`). Date: September 29, 2026.
Status at this checkpoint: awaiting the coordinator's frozen selected-segment output; no selected formulas or transfer result have been read.

## Read order and dependencies

1. Read AGENTS.md and this package's PROTOCOL.md.
2. Read the current and historical summaries in the first 14,000 characters of README.md and HANDOFF.md, plus CLAIM_STATUS.md and CONTRIBUTING.md. These governance excerpts included high-level historical B-ray optimum summaries and edge descriptions. No old B-ray optimum/witness source file or selector mathematical source has been opened.
3. Derived the physical identities below before receiving the selected result. The checker will use selected segment endpoints and local laps as claims under test, and will not import discovery/selector code.

This is separately authored internal AI checking, not independent human certification, a blind study, or a novelty review.

## Physical identities derived before the result

Write x={qt}, y={t}, and g=qy-x=-H. On the displayed fundamental domain t=y and qt=x+g. For an original coefficient row (a,b), the physical speed is aq+b. If ax+by=m+phi with 1/8<=phi<=7/8, then

    (aq+b)t = phi + (m+a*g).

Thus the physical lap is m+a*g, not m+b*g. The display order (1,q,q+1,2q+1,3q+1,3q+2,5q+2) permutes original row indices to (1,0,2,3,4,5,6). This permutation must also apply to laps and phases.

Reflection sends t to 1-t, phi to 1-phi and lap to speed-1-lap. Reflected torus coordinates are (1-x,1-y), with reflected g=q-1-g. The local reflected label is a+b-1-m, giving the same physical lap identity. The reflected point need not satisfy the original x<=1/2 fold; that fold is a representative convention, not a physical time bound.

## Fixed verification plan

After selection is frozen, test only q=2,...,25 and their reflections. Compute each speed*time and its exact floor directly, independently of claimed laps; compare every phase, lap, orbit identity and selected point. Reconstruct candidate time from the supplied segment with a separately written integer interval calculation. Prove universal phase safety using affine endpoint bands and exact polynomial physical identities on each selected segment; coverage belongs to the separate arithmetic audit. Test wrong clock t=x and wrong lap m+b*g on the same selected controls, preserving the first concrete failures. Do not run an optimizer or add physical q inputs.

## Completed result

**PASS. No physical-recovery defect found.** After the coordinator announced the selection frozen, this reviewer read `transfer.json`, then authored and ran `physical_review.py`. It imports only Python standard-library modules and does not import, inspect or call `transfer.py`, the frozen discovery implementation, or an old B-ray physical optimizer. The supplied segment endpoints, labels, order and selected times are claims under test; the direct fractions and floors are recomputed. This preserves separate implementation, but the review is not blind because the coordinator's claims were visible.

The checker reproduces both selected records, every selected/reflected phase and lap for q=2,...,25, and 336 exact distances. All selected and reflected minimum distances equal 1/8. It also certifies 56 endpoint band inequalities and 56 direct physical polynomial band inequalities over four infinite residue domains. No physical q input was added beyond the declared 24 controls.

### Independently recovered clock formulas

The frozen segments are in canonical coordinates (u,v)=(y,x). Their endpoints determine their lines directly:

| Segment | Canonical endpoints | Line | Recovered physical time |
| --- | --- | --- | --- |
| P1:E1-3:K1 | (1/4,5/24), (1/2,1/8) | v=7/24-u/3 | t=u=(24g+7)/(8(3q+1)) |
| P3:E0-1:K2 | (1/8,1/2), (3/8,3/8) | v=9/16-u/2 | t=u=(16g+9)/(8(2q+1)) |

Substituting these lines into g=qu-v gives each formula with a positive denominator for q>=2. On the primary segment the projected interval is [(6q-5)/24,(4q-1)/8], whose width is (3q+1)/12. It is at least 1 for q>=4; q=3 hits g=1, while q=2 misses and takes the fallback with g=0. Thus this physical certificate does not depend on finite samples for its all-q scope. The separate arithmetic reviewer audits discovery and ranking more broadly.

### Universal phase certificate

For either selected segment, every original phase av+bu-m is affine along the segment. The checker obtains each endpoint phase and proves it lies in the **closed** interval [1/8,7/8]. Convexity of this interval proves safety at every point on the segment. The identity

    (aq+b)u - (m+a(qu-v)) = av+bu-m

then turns ambient phases into actual physical phases whenever g=qu-v is integral. Because these phases are strictly between 0 and 1, m+ag is the actual floor, not merely a candidate label. Reflection follows exactly from the identities recorded above.

The direct physical calculation supplies another certificate for every primary branch. Its first integer is

    g=ceil((6q-5)/24)=ceil(q/4).

Write q=4a+r and use the following exhaustive domains for q>=3:

| r | Domain | g |
| --- | --- | --- |
| 0 | a>=1 | a |
| 1 | a>=1 | a+1 |
| 2 | a>=1 | a+1 |
| 3 | a>=0 | a+1 |

Let N=24g+7, D=8(3q+1), and for a coefficient row (A,B) let ell=m+A*g. The checker forms the polynomial P=(A*q+B)*N-ell*D directly. It proves both 8P-D>=0 and 7D-8P>=0 by substituting a=a_min+s: every remaining coefficient is nonnegative for s>=0. D is positive. This gives 7 rows times 2 inequalities times 4 unbounded domains, with every exact coefficient retained in `physical_review.json`. No numerical interpolation, sampled sign test or optimizer is used.

For the remaining q=2, t=9/40 has display-ordered physical phases

    (9,18,27,5,23,32,28)/40

and laps (0,0,0,1,1,1,2), all in [5/40,35/40]. The primary branch has phase 7/8 at speed 3q+1; the fallback q=2 has phase 1/8 at speed 5. Hence the selected separation is exactly 1/8 throughout, without asserting optimality.

### Counterchecks that expose consequential errors

Using the wrong clock t=x fails 22 of the 24 declared controls. The first is q=2: the selected native point is (x,y)=(9/20,9/40). The wrong time 9/20 gives speed 2 a phase of 9/10 and distance 1/10<1/8. The correct time y=9/40 has minimum distance 1/8.

Using the wrong lap m+b*g disagrees with actual floors in 23 controls. At q=3, t=31/80 and g=1, the speed-1 row would receive lap 1 rather than its actual lap 0; the resulting claimed phase is -49/80. This is a failure of the proposed physical certificate, not a claim that the correctly recovered time is unsafe. The full exact failure lists are preserved in the JSON.

### Information-loss check and limits

The swap of torus coordinates preserves safe geometry but changes the physical clock and which coefficient multiplies the orbit integer in the lap formula. Labels, coordinate meanings, display permutation and the inverse map are consequential information: omitting them can turn a valid ambient point into an unsafe physical-time claim, as the countercheck demonstrates. Reflected points need not lie in the chosen folded chart. A smaller selected-segment record is adequate for one witness only when these maps remain attached.

This review does not certify candidate-discovery completeness, global optimum values, all maximizing times, complete safe sets, other references, a new family, formal verification or novelty. The all-q phase and recovery argument remains an internally checked proof candidate requiring external mathematical assessment under repository evidence rules.

Reproduce from repository root:

    python reviews/2026-09-29-cc-b-ray-transfer/physical_review.py

Output: `physical_review.json`. It records SHA-256 hashes of the frozen input and checker source. The coordinator can rerun the script and compare its output byte for byte.
