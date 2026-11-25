"""Recheck physical and reflected alignment on the old 16-runner neutral misses.

Run this file with Python 3.11 or later. The reference is stationary. All the
moving speeds on this panel are positive, so equal residues mean equal physical
positions. Equal distances also allow reflected positions.
"""

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations
from math import gcd, isqrt
from random import Random

from second_time import repair
from test_second_time import cleared, draw


@cache
def nontrivial_divisors(value):
    found = set()
    for divisor in range(1, isqrt(value) + 1):
        if value % divisor == 0:
            found.update((divisor, value // divisor))
    found.discard(1)
    return found


def candidate_groups(slower, allow_reflection):
    """List maximal class sizes for all possible reduced time denominators."""
    denominators = set()
    for left, right in combinations(slower, 2):
        denominators.update(nontrivial_divisors(right - left))
        if allow_reflection:
            denominators.update(nontrivial_divisors(right + left))

    groups = []
    for q in denominators:
        classes = Counter()
        for speed in slower:
            r = speed % q
            if r:  # A group at the reference cannot provide clearance.
                key = min(r, q - r) if allow_reflection else r
                classes[key] += 1
        size = max(classes.values(), default=0)
        if size >= 2:
            groups.append((size, q))
    # At a reduced time h/q, multiplication by h permutes residue classes and
    # preserves reflection. Hence these group sizes work for all reduced h/q.
    return sorted(groups, key=lambda pair: (-pair[0], pair[1]))


def grid_witness(speeds, q):
    """Try every reduced numerator up to time reflection, with exact clearance."""
    if any(speed % q == 0 for speed in speeds):
        return None
    for h in range(1, q // 2 + 1):
        if gcd(h, q) != 1:
            continue
        if all(16 * min(speed*h % q, -speed*h % q) >= q for speed in speeds):
            return Fraction(h, q)
    return None


def largest_witness_group(speeds, groups, tested):
    for size, q in groups:
        if q not in tested:
            tested[q] = grid_witness(speeds, q)
        if tested[q] is not None:
            assert cleared(tested[q], speeds, 16)
            return size
    return 0


def classify(speeds):
    slower = sorted(speeds)[:11]
    tested = {}
    return tuple(
        largest_witness_group(speeds, candidate_groups(slower, reflect), tested)
        for reflect in (False, True)
    )


def run():
    # Replay the original neutral draw sequence, including discarded draws.
    rng = Random(2026112400 + 10*16)
    residual = []
    for _ in range(256):
        speeds = draw(16, 0, rng)
        if not cleared(Fraction(7, 2*max(speeds)), speeds, 16) and repair(speeds, 4) is None:
            residual.append(speeds)
    assert len(residual) == 135

    largest = [classify(speeds) for speeds in residual]
    rows = [
        (k, sum(pos >= k for pos, _ in largest), sum(dist >= k for _, dist in largest))
        for k in range(11, 1, -1)
    ]
    assert rows == [
        (11, 0, 2), (10, 0, 2), (9, 0, 3), (8, 0, 6), (7, 1, 15),
        (6, 5, 31), (5, 19, 67), (4, 61, 125), (3, 134, 135), (2, 135, 135),
    ]
    print("Minimum group size | one common position | one common distance")
    for k, pos, dist in rows:
        print(f"{k:18} | {pos:19} | {dist:19}")

    first_denominators = [
        next((q for q in range(2, 33) if grid_witness(speeds, q) is not None), None)
        for speeds in residual
    ]
    fixed_counts = {
        limit: sum(q is not None and q <= limit for q in first_denominators)
        for limit in (8, 16, 32)
    }
    assert fixed_counts == {8: 45, 16: 127, 32: 135}
    print("Witness counts without requiring alignment, by denominator limit:", fixed_counts)

    # For 0,1,...,15 every witness for zero spaces 16 positions equally around
    # the circle. Its reduced denominator is 16; all positions are distinct
    # and at most two opponents occupy the same distance from zero.
    control = classify(list(range(1, 16)))
    assert control == (0, 2)
    print("Consecutive lineup, largest witness groups of size at least two:", control)


if __name__ == "__main__":
    run()
