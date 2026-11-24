"""Classify the equality cases for the 16-shift test, and check exact examples."""

from functools import cache
from fractions import Fraction
from itertools import combinations_with_replacement
from math import gcd

N = 16
FULL = (1 << N) - 1
# Odd speeds are identified with their negatives mod 16. Even labels are gcd(v,16).
TYPES = (1, 3, 5, 7, 2, 4, 8)


def capacity(label):
    return 2 if label % 2 else label


def shapes(label):
    """All possible maximal blocker sets, allowing any starting phase."""
    if label % 2:
        step = pow(label, -1, N)
        return {(1 << j) | (1 << ((j + step) % N)) for j in range(N)}
    stride = N // label
    return {sum(1 << j for j in range(start, N, stride)) for start in range(stride)}


def blocked_shifts(v, time):
    indices = range(N)
    den = N * time.denominator
    return sum(1 << j for j in indices
               if N * min((v * (N * time.numerator + j * time.denominator)) % den,
                          (-v * (N * time.numerator + j * time.denominator)) % den) < den)


MASKS = {label: tuple(sorted(shapes(label))) for label in TYPES}


@cache
def tiling(bag, free):
    if not bag:
        return () if not free else None
    for mask in MASKS[bag[0]]:
        if free & mask == mask:
            rest = tiling(bag[1:], free ^ mask)
            if rest is not None:
                return (mask,) + rest
    return None


def phase_controls():
    """Realize every maximal blocker set at the SAME starting time via CRT."""
    time = Fraction(1, 31)
    examples = {}
    for label in TYPES:
        options = {}
        for v in range(label, 16 * 31, 16):
            mask = blocked_shifts(v, time)
            if mask.bit_count() == capacity(label):
                options[mask] = v
        assert set(options) == set(MASKS[label])
        examples[label] = options
    return examples


def strict_shift_applies(bag, d):
    # Fixed speeds are multiples of 16. Every label represents an actual speed
    # with the same gcd with each divisor d of 16.
    cost = 0
    for v in bag:
        g = gcd(v, d)
        if g != d:
            cost += g * ((2 * (d // g) + N - 1) // N)
    return cost < d


def classify():
    controls = phase_controls()
    time = Fraction(1, 31)
    total = rejected = beyond_strict = 0
    for size in range(2, 9):
        for bag in combinations_with_replacement(TYPES, size):
            if sum(v % 2 for v in bag) < 2 or sum(map(capacity, bag)) != N:
                continue
            total += 1
            # Most restrictive class first, to limit the number of tiling states.
            bag = tuple(sorted(bag, key=lambda v: len(MASKS[v])))
            witness = tiling(bag, FULL)
            if witness is None:
                rejected += 1
                if not any(strict_shift_applies(bag, d) for d in (2, 4, 8, 16)):
                    beyond_strict += 1
                    assert len(bag) >= 6
                continue
            # Distinct physical speeds. Adding 496 preserves both residues.
            speeds = [controls[v][mask] + 496 * i for i, (v, mask)
                      in enumerate(zip(bag, witness))]
            core = [480 + 496 * (size + j) for j in range(15 - size)]
            assert len(set(core + speeds)) == 15 and all(blocked_shifts(v, time) == 0 for v in core)
            covered = 0
            for v in speeds:
                covered |= blocked_shifts(v, time)
            assert covered == FULL
    assert (total, rejected, beyond_strict) == (845, 542, 457)
    print(f"{total} profiles: {rejected} force overlap; {total-rejected} have physical controls;"
          f" {beyond_strict} beyond the strict dyadic counts.")


def clearance(speeds, time):
    den = time.denominator
    residue = (v * time.numerator % den for v in speeds)
    return Fraction(min(min(x, den - x) for x in residue), den)


def grid_max(speeds, den):
    return max(clearance(speeds, Fraction(j, den)) for j in range(den))


def check_examples():
    speeds = (1, 2, 3, 4, 5, 12, *(16 * i for i in range(1, 10)))
    assert grid_max(speeds, 272) == Fraction(1, 17)
    assert clearance(speeds, Fraction(21, 160)) == Fraction(1, 10)

    p = 37
    support = tuple(sorted({min(pow(4, i, p), -pow(4, i, p) % p) for i in range(9)}))
    assert support == (1, 3, 4, 7, 9, 10, 11, 12, 16)
    p37 = (1, 2, 3, 4, 5, 12) + tuple(16 * a for a in support)
    assert grid_max(p37, 592) == Fraction(2, 37)
    assert clearance(p37, Fraction(1, 13)) == Fraction(1, 13)
    assert not any(strict_shift_applies((1, 2, 3, 4, 5, 4), d) for d in (2, 4, 8, 16))

    core = (3, 13, 16, 17, 23, 38, 42, 54, 55, 74, 77, 93, 120)
    large = tuple(16 * v for v in core) + (1, 503)
    assert grid_max(core, 251) == Fraction(15, 251)
    assert grid_max(large, 4016) == Fraction(15, 251)
    assert clearance(large, Fraction(6, 25)) == Fraction(2, 25)
    print("The 272-, 592-, and 4016-point controls and off-grid witnesses passed.")


if __name__ == "__main__":
    classify()
    check_examples()
