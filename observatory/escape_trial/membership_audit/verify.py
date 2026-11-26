"""Replay a paired, exact comparison on committed weights. Write JSON to stdout."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial.rule import predict
from observatory.escape_trial.reentry_membership import rescue

PANEL = "7a4504b8a533eb2fd4ea2926035643b58d178386c9b11b75a1f100a76341b5dd"
TARGET = Fraction(1,16)


def clearance(speeds, t):
    distances = [abs(v*t-round(v*t)) for v in speeds]
    least = min(distances)
    return least, [v for v, distance in zip(speeds, distances) if distance == least]


def assess(w):
    speeds = sorted(sum(v for i,v in enumerate(w) if mask & (1<<i)) for mask in range(1,16))
    trials = []
    for q in range(2,17):
        m = min(v for v in speeds if v % q == 0)
        for sign in (1,-1):
            t = Fraction(1,q) + Fraction(sign,16*m)
            minimum, limiting = clearance(speeds, t)
            trials.append(dict(q=q, sign=sign, time=str(t), clearance=str(minimum), limiting=limiting))
    result = rescue(w)
    issued = None
    if result is not None:
        q,sign,t = result
        check = next(x for x in trials if (x["q"], x["sign"]) == (q,sign))
        assert str(t) == check["time"]
        issued = check
    available = sum(Fraction(trial["clearance"]) >= TARGET for trial in trials)
    return dict(weights=w, available=available, issued=issued, trials=trials)


def main():
    raw = (HERE/"panel.json").read_bytes()
    assert sha256(raw).hexdigest() == PANEL
    panel = json.loads(raw)
    counts, cases = [], []
    for cell in panel["cells"]:
        lo,hi = cell["band"]
        rows = [w for w in panel["rows"] if lo <= w[0] <= hi]
        assert len(rows) == cell["accepted"]
        misses = [assess(w) for w in rows if predict(w) is None]
        proposed = [x["issued"] for x in misses if x["issued"] is not None]
        safe = sum(Fraction(p["clearance"]) >= TARGET for p in proposed)
        counts.append(dict(**cell, abstentions=len(misses), recoverable=sum(x["available"]>0 for x in misses),
                           issued=len(proposed), safe=safe, unsafe=len(proposed)-safe))
        cases.extend(misses)
    print(json.dumps(dict(cells=counts, cases=cases), separators=(",",":")))


if __name__ == "__main__":
    main()
