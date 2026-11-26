"""Exact paired anchor-swap replay against every signed endpoint on abstentions."""
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial.rule import predict
from observatory.escape_trial.reentry_membership import rescue
from observatory.escape_trial.anchor_swap.rule import swapped


def assess(weights):
    speeds = [0]
    for weight in weights:
        speeds += [s+weight for s in speeds]
    speeds = speeds[1:]
    trials = []
    for q in range(2,17):
        m = min(v for v in speeds if v % q == 0)
        for sign in (1,-1):
            t = Fraction(16*m + sign*q,16*m*q)
            phases = [(v*t.numerator) % t.denominator for v in speeds]
            distances = [min(p,t.denominator-p) for p in phases]
            clearance = Fraction(min(distances),t.denominator)
            trials.append(dict(q=q,sign=sign,t=str(t),clearance=str(clearance)))
    def issue(rule):
        choice = rule(weights)
        if choice is None:
            return None
        q,sign,t = choice
        record, = [r for r in trials if (r["q"],r["sign"]) == (q,sign)]
        assert record["t"] == str(t)
        return record
    return dict(weights=weights,original=issue(rescue),swapped=issue(swapped),trials=trials)


def main():
    raw = (HERE/'panel.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == "3b3839849a6104ca96864f8579f09eea0053273793ab605ca6d6e21f246e97ab"
    panel = json.loads(raw)
    cells,cases = [],[]
    safe = lambda t: t is not None and Fraction(t["clearance"]) >= Fraction(1,16)
    for c in panel["cells"]:
        lo,hi = c["band"]
        rows = [w for w in panel["rows"] if lo <= w[0] <= hi]
        assert len(rows) == c["accepted"]
        misses = [assess(w) for w in rows if predict(w) is None]
        counts = dict.fromkeys(("original_only","swapped_only","both","neither","unsafe","recoverable"),0)
        for row in misses:
            a,b = row["original"],row["swapped"]
            counts[("neither","swapped_only","original_only","both")[2*safe(a)+safe(b)]] += 1
            counts["unsafe"] += sum(x is not None and not safe(x) for x in (a,b))
            counts["recoverable"] += any(map(safe,row["trials"]))
        cells.append(dict(**c,abstentions=len(misses),**counts))
        cases.extend(misses)
    print(json.dumps(dict(cells=cells,cases=cases), separators=(",",":")))


if __name__ == "__main__":
    main()
