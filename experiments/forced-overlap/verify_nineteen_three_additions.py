"""Exhaust the bounded reference runners for Q plus three arbitrary added speeds."""

import argparse
from collections import Counter
from itertools import islice
from math import gcd, lcm

from verify_nineteen_fast_triples import CORE, K, check_bounds, check_gap_pairs

N = 19
CLOCKS = [(p, q) for q in range(2, 65) for p in range(1, q // 2 + 1) if gcd(p, q) == 1]


def safe(speed, p, q):
    residue = speed * p % q
    return N * min(residue, q - residue) >= q


def interval_at(known, p, q):
    """Intersect the closed safe bands of known speeds that contain time p/q."""
    a, c = 0, 1  # left endpoint a/c
    b, f = 1, 1  # right endpoint b/f
    for speed in known:
        lap = speed * p // q
        denominator = N * speed
        left = N * lap + 1
        right = N * (lap + 1) - 1
        if left * c > a * denominator:
            a, c = left, denominator
        if right * f < b * denominator:
            b, f = right, denominator
    h = lcm(c, f)
    return a * (h // c), b * (h // f), h


def choose_interval(known, times):
    best = None
    for p, q in islice(times, 12):
        a, b, h = interval_at(known, p, q)
        if b > a and (best is None or (b - a) * best[2] > (best[1] - best[0]) * h):
            best = a, b, h
    if best is None:
        raise ValueError(("no positive-width interval", known))
    return best


def candidate_speeds(interval, k):
    """Relative speeds that block at least 1/k of the chosen interval."""
    a, b, h = interval
    width = b - a
    last = (2 * k * h) // (N * width)
    denominator = N * k * h
    left = N * (k * a + width)
    right = N * (k * b - width)
    offset = k * h
    return [
        v for v in range(1, last + 1)
        if (v * left - offset + denominator - 1) // denominator <= (v * right + offset) // denominator
    ]


def audit_interval(known, interval, k, candidates):
    """Check the safe bands and recompute the candidate list by integrating blocking time."""
    a, b, h = interval
    for v in known:
        lap = v * a // h
        if not (N * lap + 1) * h <= N * v * a <= N * v * b <= (N * (lap + 1) - 1) * h:
            raise ValueError(("unsafe interval", v, interval))

    def blocked(position):
        # Cumulative blocked phase through position/h, in units of 1/(N*h).
        laps, remainder = divmod(position, h)
        scaled = N * remainder
        return 2 * h * laps + min(scaled, h) + max(0, scaled - (N - 1) * h)

    width = b - a
    # This larger cutoff only uses the full-period occupation bound.
    last = (2 * k * h) // ((N - 2 * k) * width)
    measured = []
    for v in range(1, last + 1):
        occupied = blocked(v * b) - blocked(v * a)
        if k * occupied >= N * v * width:
            measured.append(v)
    if measured != candidates:
        raise ValueError(("candidate disagreement", interval, k, candidates, measured))


def check_node(known, times, k, counts, audit):
    interval = choose_interval(known, times)
    candidates = candidate_speeds(interval, k)
    counts["intervals", k] += 1
    counts["speeds", k] += len(candidates)
    if audit:
        audit_interval(known, interval, k, candidates)
    if k > 1:
        for v in candidates:
            kept = [(p, q) for p, q in times if safe(v, p, q)]
            check_node((*known, v), kept, k - 1, counts, audit)
        return

    # With one opponent left, certify each exceptional integer speed at an exact time.
    remaining = candidates
    for p, q in times:
        unchecked = []
        for v in remaining:
            if safe(v, p, q):
                if audit:
                    for s in (*known, v):
                        residue = s * p % q
                        if not q <= N * residue <= (N - 1) * q:
                            raise ValueError(("bad rational witness", s, v, p, q))
            else:
                unchecked.append(v)
        remaining = unchecked
        if not remaining:
            break
    if remaining:
        raise ValueError(("missing witnesses", known, remaining))


def check_controls():
    for k in (1, 2, 3):
        interval = (19 - k, 19 + k, 38)
        actual = candidate_speeds(interval, k)
        audit_interval((), interval, k, actual)
        if actual != [2]:
            raise ValueError(("equality control", interval, actual))

    tight = tuple(range(1, 19))
    times = [(p, q) for p, q in CLOCKS if all(safe(v, p, q) for v in tight)]
    if not times:
        raise ValueError("isolated-time control has no witness")
    if any(b > a for a, b, _ in (interval_at(tight, p, q) for p, q in times)):
        raise ValueError("isolated-time control has a positive-width interval")


def verify(audit):
    # The separate fast-role certificate covers R >= K with two arbitrary other gaps.
    check_controls()
    check_bounds()
    _, _, pairs = check_gap_pairs()
    counts = Counter()
    for r in range(K):
        known = tuple(sorted({abs(s - r) for s in CORE if s != r}))
        seeds = CLOCKS
        if 2 * min(known) > max(known):
            seeds = [(1, 2 * max(known)), *CLOCKS]
        times = [(p, q) for p, q in seeds if all(safe(v, p, q) for v in known)]
        k = 3 if r in CORE else 2
        check_node(known, times, k, counts, audit)

    expected = {3: (16, 89), 2: (1753, 145821), 1: (145821, 2416526)}
    for k, expected_row in expected.items():
        observed = counts["intervals", k], counts["speeds", k]
        if observed != expected_row:
            raise ValueError(("unexpected coverage count", k, observed))
        print(f"{k} unknown: {observed[0]:,} intervals, {observed[1]:,} candidate speeds")
    print(f"All {K:,} bounded references and the fast-role certificate ({pairs:,} gap pairs) passed.")
    if audit:
        print("Blocking-time integration and direct checks of every terminal witness also passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", action="store_true", help="also integrate every blocking interval and recheck witnesses")
    verify(parser.parse_args().audit)
