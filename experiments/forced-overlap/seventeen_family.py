"""Certify a fixed 16-runner core with any further distinct positive integer speed."""
import argparse
import csv
import json
from fractions import Fraction as Q
from itertools import combinations
from math import ceil
from pathlib import Path

from endpoint_pairs import component_at_strong_time, pair_bound, witness_on_component
from lonely_runner.checker import feasible_intervals
from seventeen_study import N, STRONG, TARGET, cohorts, verify


def prepare_family():
    fixed = (0, *cohorts()["challenge"][0])
    maximum = fixed[-1]
    bound = max(maximum+1, ceil(Q(16*maximum, 15)))
    rows, intervals = [], {}
    for r in fixed:
        signed = tuple(s-r for s in fixed if s != r)
        classes = sorted({abs(s) for s in signed})
        strong = feasible_intervals(classes, STRONG)
        assert strong, r
        t = strong[0][0]
        verify(signed, t, 16)
        pairs = [pair_bound(u, w, N) for u, w in combinations(classes, 2)]
        cutoff = max(p.cutoff for p in pairs)
        role_bound = r + max(classes[-1]+1, ceil(cutoff))
        bound = max(bound, role_bound)
        a, b = component_at_strong_time(classes, t, N)
        assert (b-a) * (role_bound-r) >= Q(2, N)
        rows.append({"reference": r, "strong_time": str(t), "strong_component": [str(a),str(b)],
                     "cutoff": str(cutoff), "tail_from": role_bound})
        intervals[r] = feasible_intervals(classes, TARGET)
    return fixed, bound, rows, intervals


def role_times(v, fixed, bound, rows, intervals):
    if type(v) is not int or v < 1 or v in fixed:
        raise ValueError("The added speed must be a positive integer outside the fixed core.")
    result = []
    for row in rows:
        r = row["reference"]
        candidates = intervals[r] if v < bound else [tuple(map(Q, row["strong_component"]))]
        for a, b in candidates:
            t = witness_on_component(a, b, abs(v-r), TARGET)
            if t is not None:
                break
        else:
            raise AssertionError(("no old-reference witness", r, v))
        verify(tuple(s-r for s in (*fixed, v) if s != r), t)
        result.append(t)
    m = fixed[-1]
    if v > m and 15*v >= 16*m:
        t = Q(1, 2*v-m)
    else:
        allowed = feasible_intervals(tuple(abs(v-s) for s in fixed), TARGET)
        assert allowed, ("no new-reference witness", v)
        t = allowed[0][0]
    verify(tuple(s-v for s in fixed), t)
    return [*result, t]


def run(certificates):
    fixed, bound, rows, intervals = prepare_family()
    finite = [v for v in range(1, bound) if v not in fixed]
    with Path(certificates).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["added_speed", *(f"reference_{s}" for s in fixed), "reference_added"])
        for v in finite:
            writer.writerow([v, *role_times(v, fixed, bound, rows, intervals)])
    for v in [bound, bound+1, 10**25+23]:
        role_times(v, fixed, bound, rows, intervals)
    print(json.dumps({"fixed": fixed, "tail_from": bound, "finite_additions": len(finite),
                      "finite_verified_roles": len(finite)*N, "core_certificates": rows}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--certificates", help="write all finite-case witnesses as CSV")
    action.add_argument("--speed", type=int, help="print exact times for a single added speed")
    args = parser.parse_args()
    if args.speed is not None:
        fixed, bound, rows, intervals = prepare_family()
        try:
            times = role_times(args.speed, fixed, bound, rows, intervals)
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps(dict(zip((*fixed, args.speed), map(str, times))), indent=2))
    else:
        run(args.certificates)
