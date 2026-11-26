"""Two replacements in consecutive n-runner instances, for reference zero.

Removing any two of 1,...,n-1 leaves n-3 core opponents. Insert distinct
integer speeds n <= v < w. Exact open safe intervals and two analytic bounds
reduce all unbounded pairs to a finite list in the reported panels. A blocked
phase arc occupies 2/n of each complete period. The final partial period can
cost at most the blocked duration 2/(n*v) of a full period. The resulting
finite calculations use rational arithmetic only. Use Python 3.11 or later.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from itertools import combinations
from math import ceil, floor


@cache
def safe_intervals(speed, delta):
    """All open intervals in [0,1] where this runner strictly clears the target."""
    return tuple(
        ((j + delta) / speed, (j + 1 - delta) / speed)
        for j in range(speed)
    )


def intersect(first, second):
    """Intersect two sorted lists of disjoint open intervals in linear time."""
    points = []
    i = j = 0
    while i < len(first) and j < len(second):
        a, b = first[i]
        c, d = second[j]
        left, right = max(a, c), min(b, d)
        if left < right:
            points.append((left, right))
        if b <= d:
            i += 1
        if d <= b:
            j += 1
    return tuple(points)


def clearance_at(speeds, time):
    return min(min((v * time) % 1, (-v * time) % 1) for v in speeds)


def direct_strict_witness(speeds, n):
    """Look directly for a rational witness, independently of the intervals."""
    for q in range(n + 1, 2 * max(speeds) + 1):
        for p in range(1, q // 2 + 1):
            if all(n * min((p * s) % q, (-p * s) % q) > q for s in speeds):
                return Fraction(p, q)
    # The interval method decides cases where the scan finds no witness.
    return None


def boundary_witness(speeds, delta):
    """If no strict time exists, a witness must touch an arc endpoint."""
    for v in speeds:
        for pair in safe_intervals(v, delta):
            for endpoint in pair:
                if clearance_at(speeds, endpoint) >= delta:
                    return endpoint
    return None


@dataclass
class Counts:
    cores: int = 0
    small_v_rows: int = 0
    finite_pairs: int = 0
    strict: int = 0
    max_small_v: int = 0
    max_finite_w: int = 0


def classify(n, keep_through=0):
    if n <= 4:
        raise ValueError("the two-speed measure bound needs n > 4")
    delta = Fraction(1, n)
    base = set(range(1, n))
    counts = Counts()
    equal, below = [], []
    for missing in combinations(range(keep_through + 1, n), 2):
        counts.cores += 1
        core = sorted(base.difference(missing))
        windows = ((Fraction(0), Fraction(1)),)
        for speed in core:
            windows = intersect(windows, safe_intervals(speed, delta))
        width = max(b - a for a, b in windows)
        assert n * (n - 1)**2 * width >= 1

        # On a window of length L a speed v blocks at most 2*(L+1/v)/n.
        # For (n-4)*L*v >= 4 and w>v, the two blocked measures sum
        # to strictly less than L.
        for v in range(n, ceil(4 / ((n - 4) * width))):
            counts.small_v_rows += 1
            counts.max_small_v = max(counts.max_small_v, v)
            narrower = intersect(windows, safe_intervals(v, delta))
            assert narrower
            remaining_width = max(b - a for a, b in narrower)
            assert n * (n - 1) * v * remaining_width >= 1

            # Each individual closed bad pass has width 2*delta/w.
            # If it is strictly shorter than an open surviving interval,
            # that interval contains a point with strict clearance.
            limit = floor(2 * delta / remaining_width)
            for w in range(v + 1, limit + 1):
                counts.finite_pairs += 1
                counts.max_finite_w = max(counts.max_finite_w, w)
                surviving = intersect(narrower, safe_intervals(w, delta))
                speeds = (*core, v, w)
                if surviving:
                    a, b = surviving[0]
                    assert clearance_at(speeds, (a + b) / 2) > delta
                    assert direct_strict_witness(speeds, n) is not None
                    counts.strict += 1
                else:
                    t = boundary_witness(speeds, delta)
                    if t is None:
                        below.append((missing, v, w))
                    else:
                        equal.append((missing, v, w, t))
    return counts, equal, below


if __name__ == "__main__":
    expected_finite = {8: 119, 15: 731, 16: 706, 17: 584, 18: 1025}
    for count in (8, 15, 16, 17, 18):
        counts, equal, below = classify(count)
        expected_equal = [((2, 3), 11, 13, Fraction(1, 8))] if count == 8 else []
        assert equal == expected_equal and not below
        assert counts.strict + len(equal) == counts.finite_pairs
        assert counts.finite_pairs == expected_finite[count]
        print(f"n={count}; {counts}")
        print(f"Equality-only instances: {equal}")
        print(f"Below-threshold instances: {below}")

    # Check Zhang's second published positive control. This single lineup
    # at n=74 is separate from the complete unbounded panels above.
    control = sorted((set(range(1, 74)) - {70, 72}) | {140, 144})
    delta = Fraction(1, 74)
    windows = ((Fraction(0), Fraction(1)),)
    for speed in control:
        windows = intersect(windows, safe_intervals(speed, delta))
    assert not windows and clearance_at(control, delta) == delta
    print("n=74 positive control: exact maximum 1/74 for omissions 70,72 and additions 140,144.")
