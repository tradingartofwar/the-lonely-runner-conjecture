# V(q,1) upper-bound continuation — September 29, 2026

Base: `44bd7854cd14c15cc52d991a0c61a22295af1234` on the existing research branch.
The task is the missing matching upper bound for
B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2), integer q>=2, selected reference 0.

Use the existing fixed seven-form ambient model and its threshold-1/8 cells.
Change physical compatibility to H_q=x-q*y in Z. Fold x, not physical time,
to x<=1/2 via simultaneous phase reflection. Preserve singleton cells and
justify optimizer existence on original vertices or edges by the minimal-face
argument. The already supplied lower witnesses all lie strictly above 1/7.

The analytically derived winning peak edges are:

| q mod 6 | Peak (x,y) | (alpha,beta) | Required loss from 1/6 |
| --- | --- | --- | --- |
| 0 | (1/6,1/3) | (-1,4) | 1/[6(4q+1)] |
| 2 | (1/2,1/6) | (-3,5) | 1/[6(5q+3)] |
| 5 | (1/2,2/3) | (-1,2) | 1/[6(2q+1)] |

Residues 1,3,4 reach ambient height 1/6. A scratch exact calculation already
confirmed the 63 winner comparisons and found only the declared winning edge
ties at the smallest allowed q. This protocol records the following full audit
scope; it is not a preregistration of a blind discovery.

1. Reconstruct the fixed geometry by globally intersecting all 48 boundary
   planes in rational arithmetic; compare cells, vertices and edges with the
   pinned original ambient.json, without importing the original geometry code.
2. Rebuild all 21 peak directions from active facets. Certify projection signs,
   peak residues, and 63 inequalities on whole unbounded residue domains.
   Also certify the seven-row explanatory table of minimum losses at each peak.
3. Check finite edge lengths and symbolic physical-time recovery for each
   winning edge. Rerun the previous symbolic lower-bound certificates without
   rerunning its physical optimizer scan.
4. Recompute the bounded slice selector on the already saved q=2,...,150 cases
   and compare with their frozen exact maxima and full maximizing-time sets.
   No additional physical q values, reference runners or families are included.
5. Record the stronger two-maximizer conclusion only if strict competing-edge
   inequalities and actual ambient peak enumeration support it for every q.

The coordinator has read the prior ambient and Ultra upper-check code and is
the author of this continuation. A different computational organization is
not independent authorship, external certification, or formal verification.
Keep the result a complete proof candidate if the argument and checks pass.
No new novelty assessment, external contact, main merge, or recurring work.

Reproduce from the repository root:

```bash
python3 reviews/2026-09-29-ltcm-other-ray-upper/verify_upper.py > /tmp/ltcm-other-ray-upper.json
```
