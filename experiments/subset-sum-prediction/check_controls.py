"""Independent controls for the infinite subfamilies in README.md."""
from fractions import Fraction as F
from itertools import combinations
from math import ceil, lcm

from predict import predict


def sums(weights):
    return {sum(subset) for size in range(1, 5) for subset in combinations(weights, size)}


def minimum(weights, t):
    p, q = t.as_integer_ratio()
    return F(min(min(p*v % q, -p*v % q) for v in sums(weights)), q)


def fixed_clock_obstruction():
    # Each listed denominator divides S, so the full subset always collides.
    total = lcm(*range(1, 33))
    w = (1, 6, 11, total - 18)
    assert all(total % q == 0 for q in range(1, 33))
    method, t = predict(w)
    assert method == "complements" and minimum(w, t) == F(1, 15)

    example = (114, 139, 359, 1100)
    method, t = predict(example)
    assert method == "complements" and t == F(20551, 25680)
    assert minimum(example, t) == F(1, 15)


def three_prefixes():
    prefixes = [(1, 2, 13), (1, 3, 8), (1, 4, 6)]
    for total in [112, 128, 144, 160, 16*10**9]:
        covered = set()
        for lower in prefixes:
            fast = total - sum(lower)
            weights = (*lower, fast)
            covered.update(sums(weights))
            # Use a positive lower-phase arc around the prefix-specific anchor,
            # then move the fast phase to 1/16 with one arithmetic rounding.
            anchor = F(1, 12) if lower == prefixes[0] else F(1, 16)
            t = (ceil(fast * anchor - F(1,16)) + F(1,16)) / fast
            assert minimum(weights, t) == F(1,16)
            name, frozen_time = predict(weights)
            assert name != "abstain" and minimum(weights, frozen_time) >= F(1,16)
        assert set(range(1,17)) <= covered


if __name__ == "__main__":
    fixed_clock_obstruction()
    three_prefixes()
    print("Confirmed the complement time, fixed-clock obstruction, and equal-extrema controls.")

