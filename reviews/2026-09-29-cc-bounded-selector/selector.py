"""Select one 1/8-safe time for A_q. No optimizer or q-sized enumeration.

Proof candidate: notes/CC_BOUNDED_SELECTOR_2026_09_29.md.
This coordinator-authored implementation uses only two fixed parent edges.
"""

from dataclasses import dataclass
from fractions import Fraction as F

ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
THRESHOLD = F(1, 8)


@dataclass(frozen=True)
class Segment:
    name: str
    parent: int
    labels: tuple
    low_x: F
    high_x: F
    intercept: F
    slope: int

    def y(self, x):
        return self.intercept + self.slope * x

    def orbit_interval(self, q):
        return (q * self.low_x - self.y(self.low_x),
                q * self.high_x - self.y(self.high_x))


SEGMENTS = (
    Segment("E1", 1, (0, 0, 0, 0, 0, 1, 1),
            F(1, 8), F(5, 24), F(7, 8), -3),
    Segment("E2", 3, (0, 0, 0, 1, 1, 1, 2),
            F(3, 8), F(1, 2), F(9, 8), -2),
)


def ceiling(value):
    return -((-value.numerator) // value.denominator)


def select(q):
    """Return time, joint orbit and laps; at most two integer interval tests.

    q is a Python integer >=2. The operation count is bounded, but integer
    bit complexity and Fraction normalization costs are not constant.
    """
    if isinstance(q, bool) or not isinstance(q, int) or q < 2:
        raise ValueError("q must be an integer >= 2")
    for attempt, segment in enumerate(SEGMENTS, start=1):
        low, high = segment.orbit_interval(q)
        h = ceiling(low)
        if h <= high:
            x = (h + segment.intercept) / (q - segment.slope)
            y = segment.y(x)
            return {
                "q": q, "segment": segment.name, "parent": segment.parent,
                "attempts": attempt, "time": x, "point": (x, y, THRESHOLD),
                "h": h, "orbit_interval": (low, high),
                "torus_laps": segment.labels,
                "physical_laps": tuple(m + b * h
                                       for m, (_, b) in zip(segment.labels, ROWS)),
            }
    raise ArithmeticError("two-segment coverage certificate failed")


def select_formula(q):
    """Closed-form equivalent, used as an implementation crosscheck."""
    if isinstance(q, bool) or not isinstance(q, int) or q < 2:
        raise ValueError("q must be an integer >= 2")
    h = (q + 3) // 8
    if 24 * h <= 5 * q - 6:
        return F(8 * h + 7, 8 * (q + 3))
    h = (3 * q + 4) // 8
    if 8 * h <= 4 * q - 1:
        return F(8 * h + 9, 8 * (q + 2))
    raise ArithmeticError("two-segment coverage certificate failed")
