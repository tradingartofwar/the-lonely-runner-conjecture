"""Small exact controls for the candidate second integer relation at sixteen runners."""

from fractions import Fraction
from itertools import combinations_with_replacement
from math import gcd
from random import Random

from second_time import repair
from test_second_time import cleared, draw


def normalize(coefficients):
    factor = gcd(*coefficients)
    sign = 1 if next(v for v in coefficients if v) > 0 else -1
    return tuple(sign * v // factor for v in coefficients)


def small_relations(speeds):
    """Compare sums of at most three speeds with repetitions allowed."""
    previous = {}
    first_odd = None
    examples = set()
    for length in range(4):
        for indices in combinations_with_replacement(range(len(speeds)), length):
            weight = sum(speeds[i] for i in indices)
            for other in previous.setdefault(weight, []):
                coefficients = [0] * len(speeds)
                for i in indices:
                    coefficients[i] += 1
                for i in other:
                    coefficients[i] -= 1
                relation = normalize(coefficients)
                assert sum(v * c for v, c in zip(speeds, relation)) == 0
                assert sum(c * c for c in relation) <= 36
                examples.add(relation)
                if sum(relation) % 2:
                    first_odd = relation
                # Distinct normalized vectors are linearly independent in pairs.
                if first_odd and len(examples) >= 2:
                    return True
            previous[weight].append(indices)
    return False


def reduced_relation_bound():
    """Bound an independent vector after subtracting a multiple of m."""
    a = Fraction(16, 7)**2
    maxima = []
    for length in range(3, 32, 2):
        b = Fraction(1, 1) / (Fraction(7, 16) - Fraction(1, 2 * length))**2
        for support in range(1, min(15, length) + 1):
            v = 14 * a + support * (b - a)
            # Every positive absolute coefficient starts at 1. Putting all
            # excess into one coordinate maximizes their sum of squares.
            sq_upper = min(73, (length - support + 1)**2 + support - 1)
            maxima.append(min(v, v - b + Fraction(sq_upper, 4)))
    return max(maxima)


def main():
    assert reduced_relation_bound() == Fraction(2831627, 33124) < 86
    assert Fraction(11 * 16**2, 7**2) + Fraction(3 * 48**2, 13**2) == Fraction(814592, 8281)
    assert 98 < Fraction(814592, 8281) < 99
    assert small_relations(tuple(range(1, 16)))
    alternative = (1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18)
    for speeds in (tuple(range(1, 16)), alternative):
        a, b, c, d = speeds[:4]
        assert a + b == c and a + c == d
    assert min(min(v % 5, -v % 5) for v in alternative) == 1
    base = 32
    speeds = (1, base, base + 1, *(base**j for j in range(2, 14)))
    assert len(speeds) == 15 and not small_relations(speeds)
    assert all(min(v % 5, -v % 5) >= 1 for v in speeds)
    rng = Random(2026112400 + 10 * 16)
    cases = []
    for _ in range(256):
        speeds = draw(16, 0, rng)
        if not cleared(Fraction(7, 2 * max(speeds)), speeds, 16) and repair(speeds, 4) is None:
            cases.append(speeds)
    hits = sum(small_relations(speeds) for speeds in cases)
    assert hits == len(cases) == 135
    print(f"Two independent relations including one odd-sum relation in {hits} of {len(cases)} residual lineups.")
    print("Rank-one control clears at 1/5. Consecutive equality control has two short relations.")


if __name__ == "__main__":
    main()

