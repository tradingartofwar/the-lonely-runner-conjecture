"""Replay the fixed one-sixth test, from the repository root with PYTHONPATH=."""
import argparse
import json
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from math import gcd

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals
from run import dyadic_witness

TARGET = Q(1, 6)


def safe_residue(a, q):
    a %= q
    return 6 * min(a, q - a) >= q


def dyadic_catalog():
    for q in range(2, 257):
        for a in range(1, q // 2 + 1):
            if gcd(a, q) != 1:
                continue
            phase = a
            seen = set()
            while phase not in seen:
                if not safe_residue(phase, q):
                    break
                seen.add(phase)
                phase = 2 * phase % q
            else:
                yield Q(a, q)


@lru_cache(None)
def verify_orbit(t):
    # At most q residues exist, so q consecutive safe phases suffice.
    phase = t
    for _ in range(t.denominator):
        assert circular_distance(phase) >= TARGET
        phase = (2 * phase) % 1


def run(certificate_path=None):
    menu = list(dyadic_catalog())
    classified = Counter()
    first = {}
    misses = {}
    prefix = [2**i for i in range(11)]
    for r, s in combinations(range(1, 129), 2):
        for t in menu:
            a, q = t.as_integer_ratio()
            if safe_residue(r*a, q) and safe_residue(s*a, q):
                verify_orbit(t)
                assert min(circular_distance(r*t), circular_distance(s*t)) >= TARGET
                classified[str(t)] += 1
                first[r, s] = t
                break
        else:
            intervals = feasible_intervals([r, s, *prefix], TARGET)
            misses[f"{r},{s}"] = [[str(l), str(h)] for l, h in intervals]
    if certificate_path:
        with open(certificate_path, "w", encoding="utf-8") as output:
            output.write("r,s,first_witness\n")
            for (r, s), t in first.items():
                output.write(f"{r},{s},{t}\n")
    largest = max(t.denominator for t in first.values())
    assert first[3, 5] == TARGET
    return {
        "catalog_size": len(menu), "pairs": len(first) + len(misses),
        "witnessed": len(first), "first_witness_counts": classified,
        "largest_first_denominator": largest,
        "largest_denominator_cases": [[r, s, str(t)] for (r, s), t in first.items()
                                     if t.denominator == largest],
        "misses_prefix_intervals": misses
    }


def pair_witness(r, s):
    """Return a single rational time for both extras and the entire dyadic core."""
    if any(type(v) is not int or v <= 0 for v in (r, s)):
        raise ValueError("Use positive integer speeds.")
    lifts = 0
    while r % 2 == 0 and s % 2 == 0:
        r //= 2
        s //= 2
        lifts += 1
    if r % 2 and s % 2:
        t = TARGET
    else:
        odd, even = (r, s) if r % 2 else (s, r)
        x, _ = dyadic_witness(even // 2)
        t = max((x / 2, (x + 1) / 2), key=lambda y: circular_distance(odd * y))
    for _ in range(lifts):
        t = (t + 1) / 2 if t < Q(1, 2) else t / 2
    return t


@lru_cache(None)
def minimum_orbit_distance(t):
    # Trace the returned witness itself to a repeated residue, including preperiod.
    a, q = t.as_integer_ratio()
    seen = set()
    least = q
    while a not in seen:
        seen.add(a)
        least = min(least, a, q - a)
        a = 2 * a % q
    return Q(least, q)


def audit_construction():
    def check(r, s):
        t = pair_witness(r, s)
        denominator = t.denominator
        while denominator % 2 == 0:
            denominator //= 2
        assert denominator in (3, 5)
        assert min(circular_distance(r*t), circular_distance(s*t),
                   minimum_orbit_distance(t)) >= TARGET
        return t

    for r, s in combinations(range(1, 129), 2):
        check(r, s)

    # Include large even speeds on both sides of one-extra scale transitions,
    # odd speeds in either input position, and long common factors of two.
    stress = set()
    for k in (5, 40, 100):
        for offset in (-3, 0, 3):
            even = 2 * (12 * 4**k + offset)
            for odd in (3, 5, 2**(2*k + 1) + 1):
                for e in (0, 1, 80):
                    stress.add((2**e * odd, 2**e * even))
                    stress.add((2**e * even, 2**e * odd))
    for r, s in sorted(stress):
        check(r, s)

    # Consecutive speeds form a finite obstruction. Its exact peak times give
    # an independent equality check before adding all the higher powers.
    maximum = exact_maximum(range(1, 6))
    assert maximum.value == TARGET and set(maximum.times) == {TARGET, 1 - TARGET}
    for e in (0, 1, 3, 8, 200):
        scale = 2**e
        t = check(3 * scale, 5 * scale)
        assert (scale * t) % 1 in maximum.times
    # Three extras (3,5,6) force every equality time onto a denominator-seven cycle.
    triple = exact_maximum(range(1, 7))
    sevenths = {Q(i, 7) for i in range(1, 7)}
    assert triple.value == Q(1, 7) and set(triple.times) == sevenths
    assert all(minimum_orbit_distance(t) == Q(1, 7) for t in sevenths)
    return {"bounded_pairs": 8128, "large_ordered_cases": len(stress),
            "three_extra_control_times": [str(t) for t in triple.times],
            "sharp_family_checks": 5, "control_peak_times": [str(t) for t in maximum.times]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", help="export the first catalog witness for each successful pair as CSV")
    args = parser.parse_args()
    print(json.dumps({"frozen": run(args.rows), "construction": audit_construction()}, indent=2))
