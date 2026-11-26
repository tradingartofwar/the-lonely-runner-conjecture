"""One stationary-reference prediction from four positive integer weights."""

from fractions import Fraction
from typing import NamedTuple


RULE_REVISION = "four-weight-first-escape-v1"
TARGET = Fraction(1, 16)


class Residue(NamedTuple):
    count: int
    least: int
    greatest: int


def residue_extrema(weights, q):
    """Nonempty subsets of the processed weights, grouped by residue."""
    classes = {}
    for weight in weights:
        previous = classes.copy()
        additions = [(weight % q, Residue(1, weight, weight))]
        for r, old in previous.items():
            shifted = Residue(old.count, old.least + weight, old.greatest + weight)
            additions.append(((r + weight) % q, shifted))
        for r, new in additions:
            if r in classes:
                old = classes[r]
                new = Residue(old.count + new.count, min(old.least, new.least),
                              max(old.greatest, new.greatest))
            classes[r] = new
    return classes


def _directional_room(classes, q, sign):
    """First noncollider edge in this direction, with an extremal speed per tie."""
    edges = []
    for r, speeds in classes.items():
        if r:
            phase = Fraction(r, q)
            distance = 1 - TARGET - phase if sign == 1 else phase - TARGET
            edges.append((distance / speeds.greatest, speeds.greatest))
    if not edges:
        return None, ()
    room = min(t for t, _ in edges)
    return room, tuple(sorted(v for t, v in edges if t == room))


def _prediction(q, sign, escape, room, room_speeds, colliders, denominators, directions):
    anchor = Fraction(1, q)
    return dict(q=q, anchor=anchor, sign=sign, escape=escape, time=anchor + sign * escape,
                room=room, room_speeds=room_speeds,
                collider_count=colliders.count if colliders else 0,
                collider_min=colliders.least if colliders else None,
                collider_max=colliders.greatest if colliders else None,
                denominators_examined=denominators, directions_examined=directions)


def screen(weights):
    """Return (prediction or None, distinct residue tables built, signed room tests)."""
    weights = tuple(weights)
    if len(weights) != 4 or any(type(w) is not int or w <= 0 for w in weights):
        raise ValueError("Expected four positive integer weights")

    tables = {}
    for q in range(2, 17):
        classes = residue_extrema(weights, q)
        tables[q] = classes
        if 0 not in classes:
            result = _prediction(q, 0, Fraction(0), None, (), None, len(tables), 0)
            return result, len(tables), 0

    directions = 0
    for q, classes in tables.items():
        colliders = classes[0]
        if colliders.greatest > 15 * colliders.least:
            continue
        escape = TARGET / colliders.least
        for sign in (1, -1):
            directions += 1
            room, room_speeds = _directional_room(classes, q, sign)
            if room is None or escape <= room:
                result = _prediction(q, sign, escape, room, room_speeds, colliders,
                                     len(tables), directions)
                return result, len(tables), directions
    return None, len(tables), directions


def predict(weights):
    """Return the one proposed time with its certificate, or None."""
    return screen(weights)[0]
