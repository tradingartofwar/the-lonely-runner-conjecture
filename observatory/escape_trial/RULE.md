# A first escape for several colliding runners

**HYPOTHESIS — prospective pilot.** On the separately committed middle-gap panel, at least one lineup on which the direct reciprocal predictor abstains will receive a safe signed prediction. Zero such gains falsifies this finite-panel forecast. A separate, stronger comparison counts gains on rows missed by both the direct predictor and the earlier fifteen-speed predictor. A single wrong physical clearance, a direct return differing from the original direct rule, or a certificate whose recorded first edge disagrees with the physical speeds challenges the implementation. Each abstention stays in the denominator. Coverage of every lineup is open.

## What the rule predicts

All sixteen runners start together on a unit circle. Relative to the stationary reference, the fifteen moving speeds are the nonempty subset sums of four positive integer weights. The pilot's four weights have distinct subset sums. A distance of exactly δ = 1/16 passes. The input consists of the four weights alone.

For a reciprocal anchor 1/q, partition the subset sums by residue r modulo q. For each occupied r, store its count, smallest speed mᵣ and greatest speed Mᵣ. Start with no occupied residues. When adding a weight w, keep every old group, insert the singleton w and translate each **previous** group by w into residue (r+w) mod q. Shift both extrema by w. When groups coincide, add the counts and take the smallest and greatest endpoints. These three contributions partition the nonempty subsets of the enlarged prefix. The empty subset never supplies a speed of zero.

1. Inspect q = 2 through 16 in increasing order. As soon as residue zero is absent, return 1/q. Each phase is then between 1/q and 1−1/q inclusive. This preserves every return of the [direct reciprocal predictor](../study/candidate.py).
2. If every anchor has colliders, revisit the stored tables in increasing q. At a given q take the escape duration h = δ/m₀. In either direction the slowest collider reaches distance δ at h. All colliders have reached the first safe arc and are still in it exactly when M₀h ≤ 1−δ, or M₀ ≤ 15m₀. Skip that denominator if this fails.
3. Test forward first, then backward. Each nonzero residue starts inside the closed safe arc. Its direction-specific distance to the outgoing edge is constant within that residue. Dividing it by the **greatest** speed gives the earliest arrival at the edge. The room until any noncollider reaches its outgoing edge is

   $$
   H_+=\min_{r\ne0}\frac{1-\delta-r/q}{M_r},\qquad
   H_-=\min_{r\ne0}\frac{r/q-\delta}{M_r}.
   $$

   An empty minimum is infinite. Accept the first direction s for which h ≤ Hₛ and return 1/q + s h. When h = Hₛ, the slowest collider and the limiting noncollider both meet the threshold at that instant. With strict inequality, every collider has escaped before any noncollider reaches its outgoing edge. With no qualifying direction, abstain.

The continuous interval justified by the first-lap calculation is h through min(Hₛ, (1−δ)/M₀), measured along the chosen direction from the anchor. It may be a single point. The rule returns its near endpoint. A collider can enter a later safe arc, and a noncollider can leave its initial arc and re-enter. Such motions can produce safe endpoints that this test declines. The [opened challenger](../study/challenger.md) gives a re-entry example at 1/10 + 1/640.

## Why the five-collision example qualifies

**OBSERVED on the previously opened fresh-04.** For (14,17,103,154) every direct anchor has a collider. At 1/2 the extreme colliders are 14 and 288, and 288 exceeds 15 × 14. At 1/3 the residue groups are

| Residue | Count | Least speed | Greatest speed |
|---|---:|---:|---:|
| 0 | 5 | 117 | 288 |
| 1 | 5 | 31 | 274 |
| 2 | 5 | 14 | 257 |

The colliders are 117, 120, 168, 171 and 288. At h = 1/1872 even speed 288 has traveled only 2/13 of a lap. The first forward edge belongs to 257 at H₊ = 13/12336. The shift fits strictly. The rule returns 625/1872 at the beginning of the [previously verified interval](../study/shift-derivation.md). Speed 117 is the only runner at distance 1/16 there. The backward direction also has room (13/13152 at speed 274). The fixed sign order selects forward.

## Opened comparisons before freeze

**OBSERVED.** All 180 residue tables on the twelve original stretch_middle rows matched counts and extrema reconstructed from the fifteen speeds. The selector builds 146 residue tables across the twelve rows and evaluates 12 signed headrooms. It preserves the ten direct returns and recovers both direct abstentions. These opened examples shaped the rule.

| Previously opened weights | Direct reciprocal | Earlier fifteen-speed return and clearance | First-escape return and clearance | Limiting speed at first-escape return |
|---|---|---|---|---|
| 41, 80, 435, 564 | abstained | 1775/15984, 1/16 | 2321/6960, 1/16 | 435 |
| 3, 5, 28, 60 | abstained | 97/1536, 11/512 | 65/448, 1/16 | 28 |
| 14, 17, 103, 154 (previous fresh-04) | abstained | 289/4608, 17/4608 | 625/1872, 1/16 | 117 |

## Budget, ties and replay

Revision `four-weight-first-escape-v1` builds at most 15 distinct tables of four weight updates apiece. It checks at most 30 signed headrooms, with zero full physical-time evaluations in selection. A rejected collider spread costs no headroom check. A direct exit costs zero signed checks. Both passes visit q in increasing order. Forward wins if both signs qualify. The public call `predict(weights)` returns one certificate dictionary or `None`; `screen(weights)` also reports both work counters on abstention. The certificate stores the positive escape duration separately from the sign. For shifted predictions, `room_speeds` lists the fastest speed in each tied first-edge residue. All accepted finite rooms are positive, so this gives every first-edge speed on the trial domain. On a direct return sign and escape are zero and room is inapplicable. A shifted return with no noncolliders records room as `None` (unbounded). The independent scorer computes final clearance and all speeds attaining it.

From the repository root, this opened-only replay independently checks all fifteen modular distances, the direct baseline, and every residue summary on the original twelve rows:

```sh
python - <<'PY'
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
from observatory.escape_trial.rule import residue_extrema, screen
from observatory.study.candidate import predict as direct

rows = json.loads(Path('experiments/subset-sum-prediction/panel.json').read_text())['instances']
cases = [tuple(row['weights']) for row in rows if row['pattern'] == 'stretch_middle']
counts = Counter()
tables = signs = 0
for w in cases + [(14, 17, 103, 154)]:
    speeds = sorted(sum(c) for n in range(1, 5) for c in combinations(w, n))
    for q in range(2, 17):
        by_r = {r: [v for v in speeds if v % q == r] for r in {v % q for v in speeds}}
        assert residue_extrema(w, q) == {r: (len(v), min(v), max(v)) for r, v in by_r.items()}
    result, n_tables, n_signs = screen(w)
    assert result is not None
    t = result['time']
    p, d = t.as_integer_ratio()
    dist = {v: F(min(v*p % d, -v*p % d), d) for v in speeds}
    assert min(dist.values()) >= F(1, 16)
    assert direct(w) == (None if result['sign'] else t)
    if w in cases:
        counts[bool(result['sign'])] += 1
        tables += n_tables
        signs += n_signs
    print(w, t, min(dist.values()), [v for v in speeds if dist[v] == min(dist.values())])
assert (len(cases), counts[False], counts[True], tables, signs) == (12, 10, 2, 146, 12)
PY
```

AI-assisted derivation and implementation. The certificate concerns one selected reference and inclusive first-arc travel. Estimates of predictive coverage are specific to the panel on which the frozen rule is scored.
