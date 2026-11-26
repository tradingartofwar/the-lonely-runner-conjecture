# The first safe interval after 1/3 for (14, 17, 103, 154)

**OBSERVED.** On this revealed lineup the first closed safe interval going forward from 1/3 is **[625/1872, 1375/4112]**. Speed 117 reaches phase 1/16 at the left endpoint. Speed 257 reaches phase 15/16 at the right endpoint. Each is the sole limiting speed at its endpoint. This calculation follows the frozen comparison and concerns only the stationary reference, with all 16 runners starting together.

Write the time as 1/3 + h, with h nonnegative. A speed v starts with phase r/3, where r = v mod 3. Until it passes phase 15/16 on this lap, its safe offsets satisfy 1/16 ≤ r/3 + vh ≤ 15/16. The 15 nonempty subset speeds give these exact restrictions.

| Residue r | Speeds | Last entry at or after h = 0 | First exit boundary |
|---|---|---|---|
| 0 | 117, 120, 168, 171, 288 | 1/1872 at 117 | 5/1536 at 288 |
| 1 | 31, 103, 154, 271, 274 | already safe at 0 | 29/13152 at 274 |
| 2 | 14, 17, 134, 185, 257 | already safe at 0 | 13/12336 at 257 |

Speed 117 blocks every offset from zero up to, and excluding, 1/1872. Once it enters, every speed is safe through the smallest exit boundary, 13/12336. Speed 257 blocks immediately after that boundary. Adding 1/3 gives the stated interval, of width 125/240552. The closed endpoints count because the minimum distance there equals the inclusive threshold 1/16.

Run this command from any directory with Python 3 to recompute the boundaries and check the exact distance of every speed at both endpoints.

```sh
python - <<'PY'
from fractions import Fraction as F
from itertools import combinations

w = (14, 17, 103, 154)
speeds = sorted(sum(c) for k in range(1, 5) for c in combinations(w, k))
anchor = F(1, 3)
target = F(1, 16)
left = anchor + max((target - F(v % 3, 3)) / v for v in speeds)
right = anchor + min((1 - target - F(v % 3, 3)) / v for v in speeds)
assert (left, right) == (F(625, 1872), F(1375, 4112))
for t, expected in ((left, 117), (right, 257)):
    p, q = t.as_integer_ratio()
    distances = {v: F(min(v*p % q, -v*p % q), q) for v in speeds}
    limiting = [v for v in speeds if distances[v] == min(distances.values())]
    assert min(distances.values()) == target and limiting == [expected]
    print(t, min(distances.values()), limiting)
PY
```
