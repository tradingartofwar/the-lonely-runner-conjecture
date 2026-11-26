"""Generate the certificate for two independent additions to the fixed sixteen speeds."""
import argparse
import csv
import json
import lzma
from fractions import Fraction as Q
from functools import lru_cache
from math import ceil, gcd
from pathlib import Path

from endpoint_pairs import component_at_strong_time, witness_on_component
from lonely_runner.checker import _intersect, feasible_intervals
from verify_seventeen_family import FIXED

ROOT = Path(__file__).resolve().parent
DELTA = Q(1, 18)
TRANSFER = (*range(15), 105)


@lru_cache(None)
def fixed_intervals(r, fixed=FIXED):
    return feasible_intervals(tuple(abs(p-r) for p in fixed if p != r), DELTA)


@lru_cache(None)
def one_runner(u):
    return feasible_intervals((u,), DELTA)


def widest(intervals):
    return max(intervals, key=lambda z: z[1]-z[0])


def strings(interval):
    return [str(t) for t in interval]


@lru_cache(None)
def small_clocks(r, fixed=FIXED):
    differences = {abs(r-p) for p in fixed if r != p}
    return tuple(Q(a,q) for q in range(2, 33) for a in range(1, q//2+1)
                 if gcd(a,q) == 1 and all(18*min(a*v % q,-a*v % q) >= q for v in differences))


def new_role_time(r, gap, fixed=FIXED):
    """Keep r clear of all fixed runners and of one other at relative speed gap."""
    for t in small_clocks(r, fixed):
        p, q = t.as_integer_ratio()
        if 18*min(gap*p % q,-gap*p % q) >= q:
            return t
    for a,b in fixed_intervals(r, fixed):
        t = witness_on_component(a, b, gap, DELTA)
        if t is not None:
            return t
    raise ArithmeticError(("new reference lacks witness", r, gap))


def check_distances(r, speeds, t):
    p,q = t.as_integer_ratio()
    assert all(18*min((s-r)*p % q, (r-s)*p % q) >= q for s in speeds if s != r)


def row_for_x(x, old_times=None, fixed=FIXED):
    fixed_x = (*fixed, x)
    diameter = max(fixed)
    m = max(diameter, x)
    bound = max(m+1, ceil(Q(17*m,16)))
    pools = []
    available = []
    for i,r in enumerate(fixed_x):
        signed = tuple(abs(s-r) for s in fixed_x if s != r)
        if old_times is not None:
            inherited = component_at_strong_time(signed, old_times[i], 18)
        if r != x:
            intervals = _intersect(fixed_intervals(r, fixed), one_runner(abs(x-r)))
            first = widest(intervals)
            available.append(intervals)
        else:
            if old_times is not None:
                first = inherited
            elif x > diameter and 15*x >= 16*diameter:
                t = Q(1, 2*x-diameter)
                first = component_at_strong_time(signed, t, 18)
            else:
                first = widest(fixed_intervals(x, fixed))
            available.append(())
        if first[0] >= first[1]:
            raise ArithmeticError(("no positive-width interval", x, r))
        pools.append([first])
        bound = max(bound, r + ceil(2*DELTA / (first[1]-first[0])))
    finite_y = [y for y in range(x+1,bound) if y not in fixed]
    exceptional = []
    for y in finite_y:
        for i,r in enumerate(fixed_x):
            gap = abs(y-r)
            for a,b in pools[i]:
                t = witness_on_component(a,b,gap,DELTA)
                if t is not None:
                    break
            else:
                if r == x:
                    t = new_role_time(x, gap, fixed)
                    pools[i].append((t,t))
                else:
                    for a,b in available[i]:
                        t = witness_on_component(a,b,gap,DELTA)
                        if t is not None:
                            pools[i].append((a,b))
                            break
                    else:
                        raise ArithmeticError(("fixed reference lacks witness",x,y,r))
            check_distances(r, (*fixed_x,y), t)
        if y > m and 16*y >= 17*m:
            t = Q(1,2*y-m)
        else:
            t = new_role_time(y, y-x, fixed)
            exceptional.append(str(t))
        check_distances(y, (*fixed_x,y),t)
    return {"x":x, "tail":bound, "intervals":[list(map(strings,pool)) for pool in pools],
            "new_reference_exceptions":exceptional}, len(finite_y)


def generate(transfer=False):
    fixed = TRANSFER if transfer else FIXED
    intervals = [widest(fixed_intervals(r, fixed)) for r in fixed]
    cutoff = max([6*max(fixed)] + [1 + int(r + Q(2,7)/(b-a))
                                  for r, (a,b) in zip(fixed, intervals)])
    prior = None
    if not transfer:
        with (ROOT / "seventeen_family_witnesses.csv").open(newline="") as f:
            reader = csv.reader(f)
            next(reader)
            prior = {int(row[0]): tuple(map(Q,row[1:])) for row in reader}
    rows = []
    finite = 0
    for x in range(1,cutoff):
        if x in fixed:
            continue
        times = prior[x] if prior is not None else None
        row, count = row_for_x(x, times, fixed)
        rows.append(row)
        finite += count
    return {"fixed": fixed, "large_cutoff":cutoff, "base_intervals":list(map(strings,intervals)),
            "finite_pairs":finite, "small_rows":rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="output .json.xz proof certificate")
    parser.add_argument("--transfer", action="store_true", help="use the second, adversarial core")
    args = parser.parse_args()
    doc = generate(args.transfer)
    payload = json.dumps(doc,separators=(",",":")).encode()
    args.out.write_bytes(lzma.compress(payload, preset=6))
    print(f"K={doc['large_cutoff']}, strips={len(doc['small_rows'])}, finite pairs={doc['finite_pairs']}")
