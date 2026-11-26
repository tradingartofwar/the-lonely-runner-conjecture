"""Replay two lineups whose anchor summaries agree and endpoint clearances differ."""

from fractions import Fraction
from itertools import combinations

from .reentry_membership import classes_at, inspect
from .rule import residue_extrema


def main():
    cases = [
        ((1, 5, 13, 29), Fraction(1, 32), [29, 35]),
        ((1, 5, 17, 25), Fraction(1, 16), [6, 26]),
    ]
    anchor = Fraction(1, 3)
    threshold = Fraction(1, 16)
    summaries = []
    for weights, expected_clearance, expected_limiters in cases:
        speeds = sorted(sum(group) for size in range(1, 5)
                        for group in combinations(weights, size))
        colliders = [speed for speed in speeds if speed % 3 == 0]
        assert colliders == [6, 18, 30, 42, 48]
        summaries.append(residue_extrema(weights, 3))
        endpoint = anchor + threshold / min(colliders)
        assert endpoint == Fraction(11, 32)
        distances = {speed: abs(speed * endpoint - round(speed * endpoint))
                     for speed in speeds}
        clearance = min(distances.values())
        limiters = [speed for speed in speeds if distances[speed] == clearance]
        assert (clearance, limiters) == (expected_clearance, expected_limiters)
        blockers = [speed for speed in speeds if distances[speed] < threshold]
        assert blockers == [speed for speed in speeds if speed % 32 in {0, 3, 29}]
        predicted, blocker = inspect(classes_at(weights, 3), 3, 1)
        if blockers:
            assert predicted is None and blocker in blockers
        else:
            assert predicted == endpoint and blocker is None
        print(f"{weights}: minimum {clearance} at {limiters}; "
              f"{'passes' if clearance >= threshold else 'fails'} at {endpoint}")
    assert summaries[0] == summaries[1]


if __name__ == "__main__":
    main()
