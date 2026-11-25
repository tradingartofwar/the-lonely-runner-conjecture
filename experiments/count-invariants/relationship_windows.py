"""Replay two 16-runner comparisons on windows centered at rational times.

The retrospective comparison uses the preceding 256-case panels unchanged.
The fresh comparison was specified after fixing the window method: draw 256
uniform lineups per maximum (1024, 1031, 1050, 1260) with seed 202611241600
plus that maximum. The predeclared direct-time cutoff is 7 in both panels.
A post-hoc diagnostic evaluates denominator 32 only on the fresh additions.
All times are exact fractions, and equality at clearance 1/16 is accepted.
"""

from fractions import Fraction
from math import ceil, floor, gcd, lcm
from random import Random

from second_time import earliest, repair
from test_second_time import cleared, draw

N = 16
DELTA = Fraction(1, N)


def half_period_anchors(max_denominator):
    """Reflection preserves every absolute distance on a common-start circle."""
    return [Fraction(h, q) for q in range(2, max_denominator + 1)
            for h in range(1, q // 2 + 1) if gcd(h, q) == 1]


def core_window(core, anchor):
    """Intersection of the core runners' individual safe arcs around anchor."""
    if not cleared(anchor, core, N):
        return None
    laps = [(v, floor(v * anchor)) for v in core]
    left = max((lap + DELTA) / v for v, lap in laps)
    right = min((lap + 1 - DELTA) / v for v, lap in laps)
    return left, right


def first_by_enumeration(window, fast):
    """Independent check on finite panel inputs via exact safe-entry events."""
    left, right = window
    events = {left}
    for v in fast:
        first = ceil(v * left - DELTA)
        last = floor(v * right - DELTA)
        events.update((lap + DELTA) / v for lap in range(first, last + 1))
    return next((t for t in sorted(events) if cleared(t, fast, N)), None)


def anchored_witness(speeds, anchors, *, audit=True):
    ordered = sorted(speeds)
    core, fast = ordered[:-4], ordered[-4:][::-1]
    first_witness = None
    for anchor in anchors:
        window = core_window(core, anchor)
        if window is None:
            continue
        left, right = window
        t = earliest(left, fast, DELTA)
        witness = t if t <= right else None
        if audit:
            assert witness == first_by_enumeration(window, fast)
        if witness is not None:
            assert cleared(witness, speeds, N)
            if first_witness is None:
                first_witness = witness
    return first_witness


def compare(lineups, *, check_32=False):
    anchors = half_period_anchors(7)
    diagnostic = half_period_anchors(32)
    misses = extra = recovered_by_32 = 0
    for speeds in lineups:
        baseline = cleared(Fraction(7, 2 * max(speeds)), speeds, N)
        baseline = baseline or repair(speeds, 4) is not None
        direct = any(cleared(t, speeds, N) for t in anchors)
        witness = anchored_witness(speeds, anchors)
        assert not direct or witness is not None
        if not baseline and not direct:
            misses += 1
            if witness is not None:
                extra += 1
                if check_32 and any(cleared(t, speeds, N) for t in diagnostic):
                    recovered_by_32 += 1
    return misses, extra, recovered_by_32


def controls():
    core = list(range(1, 22, 2))
    t = Fraction(225, 448)
    bank32_multiple = lcm(*range(1, 33))
    for maximum in (840, bank32_multiple):
        speeds = [*core, 28, 42, 56, maximum]
        assert repair(speeds, 4) is None
        assert not cleared(Fraction(7, 2 * maximum), speeds, N)
        assert core_window(core, Fraction(1, 2)) == (Fraction(23, 48), Fraction(25, 48))
        # Boundary enumeration with the enormous speed would be impractical.
        w = anchored_witness(speeds, [Fraction(1, 2)], audit=maximum == 840)
        assert w is not None and cleared(t, speeds, N)
        cutoff = 8 if maximum == 840 else 32
        assert not any(cleared(h, speeds, N) for h in half_period_anchors(cutoff))
    assert cleared(Fraction(1, 16), [*core, 28, 42, 56, 840], N)
    assert (bank32_multiple * t) % 1 == Fraction(1, 2)
    wait = 2 * DELTA * sum(Fraction(a, v) for a, v in zip((8, 4, 2, 1), (840, 56, 42, 28)))
    assert wait == Fraction(23, 1120) < Fraction(1, 24)
    # No isolated fastest speed. Two tight groups start this repair half a lap apart.
    for even_base in (60, bank32_multiple):
        cluster = [even_base + j for j in (0, 2, 4, 6)]
        speeds = [*core, *cluster]
        shifted = Fraction(1, 2) + Fraction(1, 2*even_base)
        assert not cleared(Fraction(1, 2), speeds, N)
        assert cleared(shifted, speeds, N) and repair(speeds, 4) is None
        minimum = min(min(v*shifted % 1, -v*shifted % 1) for v in speeds)
        assert minimum == Fraction(1, 2) - Fraction(21, 2*even_base)
        if even_base == bank32_multiple:
            assert not any(cleared(h, speeds, N) for h in half_period_anchors(32))
    print("The common-phase and two-cluster controls pass, including both denominator-32 tests.")


def run_comparisons():
    old_expected = [(109, 21), (123, 23), (0, 0), (120, 20)]
    for index, label in enumerate(("neutral", "low", "high", "mixed")):
        rng = Random(2026112400 + 10*N + index)
        lineups = (draw(N, index, rng) for _ in range(256))
        misses, extra, _ = compare(lineups)
        assert (misses, extra) == old_expected[index]
        print(f"Previous {label}: {extra} additions among {misses} misses of both baselines.")

    fresh_expected = {1024: (94, 19), 1031: (89, 18), 1050: (119, 47), 1260: (126, 48)}
    for maximum, expected in fresh_expected.items():
        rng = Random(202611241600 + maximum)
        lineups = ([maximum, *rng.sample(range(1, maximum), 14)] for _ in range(256))
        misses, extra, recovered = compare(lineups, check_32=True)
        assert (misses, extra) == expected and recovered == extra
        print(f"Fresh M={maximum}: {extra} additions among {misses} misses of both baselines; "
              f"direct times through denominator 32 recover {recovered} of those additions.")


if __name__ == "__main__":
    controls()
    run_comparisons()
