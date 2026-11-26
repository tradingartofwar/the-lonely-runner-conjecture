"""Replay the sealed family and compare the frozen predictors."""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path

from predict import predict
from generate import generate

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "one-time-prediction"))
from predictor import choose_time
sys.path.insert(0, str(HERE.parent / "two-replacements"))
from lr_two_swap import safe_intervals, intersect, boundary_witness

DELTA = F(1, 16)
SEED_DIGEST = "a34e9480ae761947d7f7001e7589704048822b95156708692d37454c48ffbde6"
PANEL_DIGEST = "8b68c80e3af724ccdd4436e682e052d357bba6e8b477922a00430abdda9e9830"


def clearance(speeds, time):
    p, q = time.as_integer_ratio()
    return F(min(min(v*p % q, -v*p % q) for v in speeds), q)


def exact_witness(speeds):
    windows = ((F(0), F(1)),)
    for v in speeds:
        windows = intersect(windows, safe_intervals(v, DELTA))
    if windows:
        l, r = windows[0]
        return (l+r)/2
    return boundary_witness(speeds, DELTA)


def main():
    panel = json.loads(Path(sys.argv[1]).read_bytes())
    assert hashlib.sha256(bytes.fromhex(panel["seed_hex"])).hexdigest() == SEED_DIGEST
    assert generate(panel["seed_hex"]) == panel
    assert hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest() == PANEL_DIGEST
    rows = panel["instances"]
    predictions = [predict(r["weights"]) for r in rows]
    simpler = [F(1, sum(r["weights"]) + r["weights"][0]) for r in rows]
    old = [choose_time(r["speeds"])[1] for r in rows]
    clocks = [F(p, q) for q in range(2, 33) for p in range(1, q//2+1) if gcd(p,q)==1]
    print("Direct comparison grid:", len(clocks), "times")
    groups, methods, overlaps = defaultdict(Counter), Counter(), Counter()
    ledger = []
    for r, (name, t), simple, prev in zip(rows, predictions, simpler, old):
        w, speeds = r["weights"], r["speeds"]
        assert gcd(*w) == 1 and sum(w) % 16 == 0
        assert sorted(sum(s) for k in range(1,5) for s in combinations(w,k)) == speeds
        m = clearance(speeds, t) if t is not None else None
        passed = m is not None and m >= DELTA
        assert t is None or passed
        if name == "complements":
            assert m == F(1,15)
        simple_ok = clearance(speeds, simple) >= DELTA
        old_ok = clearance(speeds, prev) >= DELTA
        grid_t = next((h for h in clocks if clearance(speeds, h) >= DELTA), None)
        grid_ok = grid_t is not None
        extra = exact_witness(speeds) if not (passed or simple_ok or old_ok or grid_ok) else None
        if extra is not None:
            assert clearance(speeds, extra) >= DELTA
        for key in (r["pattern"], "all"):
            groups[key].update(dict(cases=1, predicted=passed, first_lap=simple_ok,
                                    prior=old_ok, grid=grid_ok, known=bool(passed or simple_ok or old_ok or grid_ok or extra)))
        methods[name] += 1
        overlaps[passed, old_ok, grid_ok] += 1
        ledger.append(dict(weights=w, pattern=r["pattern"], method=name, time=str(t) if t else None,
                           clearance=str(m) if m else None, first_lap=simple_ok, prior=old_ok,
                           grid_time=str(grid_t) if grid_t else None, oracle=str(extra) if extra else None))
    for key, row in groups.items():
        print(key, dict(row))
    print("Branches:", dict(methods))
    print("Overlap (prediction, prior rule, grid):", sorted(overlaps.items()))
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(ledger, indent=2) + "\n")


if __name__ == "__main__":
    main()

