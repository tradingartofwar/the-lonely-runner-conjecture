"""Frozen one-output rescue for four-weight first-arc abstentions."""
from bisect import bisect_left
from fractions import Fraction
from itertools import combinations


def classes_at(weights, q):
    groups = {}
    for length in range(1, 5):
        for subset in combinations(weights, length):
            speed = sum(subset)
            groups.setdefault(speed % q, []).append(speed)
    return {r: sorted(members) for r, members in groups.items()}


def inspect(groups, q, sign):
    """Return (time, blocker). (None, None) means untested by the bounded rule."""
    if 0 not in groups:
        return None, None
    m = groups[0][0]
    denominator = 16 * m * q
    radius = m * q
    for residue, members in groups.items():
        offset = 16 * m * ((sign * residue) % q)
        first = (offset + q * members[0] - radius) // denominator + 1
        last = (offset + q * members[-1] + radius - 1) // denominator
        if last - first + 1 > 4:
            return None, None
        for lap in range(first, last + 1):
            center = lap * denominator - offset
            smallest = (center - radius) // q + 1
            largest = (center + radius - 1) // q
            index = bisect_left(members, smallest)
            if index < len(members) and members[index] <= largest:
                return None, members[index]
    return Fraction(16 * m + sign * q, denominator), None


def rescue(weights):
    """Apply only to first-arc abstentions. Return at most one (q, sign, time)."""
    for q in (3, 5, 7):
        groups = classes_at(weights, q)
        for sign in (1, -1):
            time, _ = inspect(groups, q, sign)
            if time is not None:
                return q, sign, time
    return None


if __name__ == "__main__":
    opened = [
        ((60, 63, 449, 644), Fraction(107, 320)),
        ((260, 264, 1567, 2101), Fraction(1409, 4224)),
    ]
    for weights, expected in opened:
        assert rescue(weights) == (3, 1, expected)
        print(weights, expected)
    weights = (257, 258, 1543, 2070)
    assert inspect(classes_at(weights, 5), 5, 1) == (None, 3613)
    print(weights, "q=5 forward rejected at interior speed 3613")
