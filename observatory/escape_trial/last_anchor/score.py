"""Recompute every paired return and audit all four signed physical times."""
import hashlib
import json
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial.last_anchor.arms import first_issue
from observatory.escape_trial.rule import predict

TARGET = Fraction(1,16)
PANEL_HASH = "325a7feec6300c1d49ccd9c5b2b87b06c2fa5c8e574fff41af2913f0ec002419"


def physical_trial(speeds, q, sign):
    collider = min(v for v in speeds if v % q == 0)
    time = Fraction(1,q) + sign * Fraction(1,16*collider)
    phases = [(v * time.numerator) % time.denominator for v in speeds]
    distances = [min(p,time.denominator-p) for p in phases]
    worst = min(distances)
    clearance = Fraction(worst,time.denominator)
    return dict(sign=sign, time=str(time), clearance=str(clearance), safe=clearance>=TARGET,
                limiters=[v for v,d in zip(speeds,distances) if d==worst])


def check(weights):
    assert predict(weights) is None
    assert all(first_issue(weights,q) is None for q in (3,5))
    speeds = sorted(sum(s) for size in range(1,5) for s in combinations(weights,size))
    rec = {"weights":weights}
    successes = []
    for q in (4,7):
        trials = [physical_trial(speeds,q,sign) for sign in (1,-1)]
        returned = first_issue(weights,q)
        issued = None
        if returned:
            sign, time = returned
            issued, = [t for t in trials if t["sign"] == sign]
            assert issued["time"] == str(time)
        successes.append(bool(issued and issued["safe"]))
        rec[str(q)] = dict(issued_sign=issued and issued["sign"], trials=trials)
    rec["outcome"] = ("neither","7_only","4_only","both")[2*successes[0]+successes[1]]
    return rec


def score():
    raw = (HERE/"selected.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PANEL_HASH
    cells, cases = [],[]
    for cell in json.loads(raw)["conditional"]:
        counts = dict.fromkeys(("4_only","7_only","both","neither","unsafe_issued"),0)
        for weights in cell["rows"]:
            rec = check(weights)
            counts[rec["outcome"]] += 1
            counts["unsafe_issued"] += sum(t["sign"] == rec[q]["issued_sign"] and not t["safe"]
                                         for q in ("4","7") for t in rec[q]["trials"])
            cases.append(rec)
        cells.append(dict(band=cell["band"],cases=len(cell["rows"]),**counts))
    return dict(selected_sha256=PANEL_HASH, cells=cells, cases=cases)


if __name__ == "__main__":
    print(json.dumps(score(), separators=(",",":")))
