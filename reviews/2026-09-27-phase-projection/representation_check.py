#!/usr/bin/env python3
"""Exact check of the protocol's sole abstract, non-runner time-set pair."""
from fractions import Fraction as Q
import json

DELTA = Q(1, 8)
SPEED = 11
A1 = ((Q(1, 44), Q(1, 22)),)
A2 = A1 + tuple((a + Q(1, 11), b + Q(1, 11)) for a, b in A1)


def allowed(time_set, theta):
    out = []
    for a, b in time_set:
        low = (SPEED * a + theta).__floor__() - 1
        high = (SPEED * b + theta).__floor__() + 1
        for j in range(low, high + 1):
            left = max(a, (j + DELTA - theta) / SPEED)
            right = min(b, (j + 1 - DELTA - theta) / SPEED)
            if left <= right:
                out.append((left, right))
    return tuple(sorted(set(out)))


def duration(intervals):
    return sum((b - a for a, b in intervals), Q(0))


def encode(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def main():
    # Each source interval fits wholly inside one phase-map branch.
    projection = []
    for time_set in (A1, A2):
        pieces = set()
        for a, b in time_set:
            j = (SPEED * a).__floor__()
            assert (SPEED * b).__floor__() == j
            pieces.add((SPEED * a - j, SPEED * b - j))
        projection.append(tuple(sorted(pieces)))
    assert projection[0] == projection[1] == ((Q(1, 4), Q(1, 2)),)

    rows = []
    for label, time_set, expected in [('A1', A1, Q(1, 44)),
                                      ('A2', A2, Q(1, 22))]:
        at_zero = allowed(time_set, Q(0))
        at_contact = allowed(time_set, Q(5, 8))
        endpoints = tuple((t, t) for ab in time_set for t in ab)
        assert at_zero == time_set
        assert duration(at_zero) == expected
        assert at_contact == endpoints
        assert duration(at_contact) == 0
        rows.append({'id': label, 'time_set': encode(time_set),
                     'phase_zero_allowed': encode(at_zero),
                     'phase_zero_duration': str(duration(at_zero)),
                     'phase_5_over_8_allowed': encode(at_contact),
                     'phase_5_over_8_contact_count': len(at_contact)})
    print(json.dumps({'status': 'one abstract pair; not runner configurations',
                      'projection': encode(projection[0]), 'cases': rows}, indent=2))


if __name__ == '__main__':
    main()
