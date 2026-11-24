"""Replay the frozen comparison with independent exact endpoint enumeration."""

from fractions import Fraction as F
from itertools import combinations
from math import ceil, floor
from random import Random
from second_time import earliest, repair


def cleared(t, speeds, n):
    a, d = t.numerator, t.denominator
    return all(n * min(a*v % d, -a*v % d) >= d for v in speeds)


def endpoint_witness(speeds, k):
    # In a nonempty closed feasible set the earliest time is either the left
    # endpoint or one of the boundary times of a freely wrapping speed.
    ordered = sorted(speeds, reverse=True)
    n = len(speeds) + 1
    left, right = F(1, n * ordered[-1]), F(n - 1, n * ordered[k])
    if left > right:
        return None
    if cleared(left, speeds, n):
        return left
    candidates = set()
    for speed in ordered[:k]:
        for sign in (-1, 1):
            offset = F(sign, n)
            for lap in range(ceil(left*speed - offset), floor(right*speed - offset) + 1):
                candidates.add((lap + offset)/speed)
    return next((t for t in sorted(candidates) if cleared(t, speeds, n)), None)


def draw(n, panel, rng):
    m = 1009
    if panel == 0:
        return [m, *rng.sample(range(1, m), n - 2)]
    speeds = [m]
    if panel in (1, 3):
        speeds.append(rng.randrange(1, ceil(F(2*m, 7*n))))
    if panel in (2, 3):
        lo, hi = F(m*(2*n - 1), 7*n), F(m*(2*n + 1), 7*n)
        speeds.append(rng.randint(ceil(lo), floor(hi)))
    speeds.extend(rng.sample(range(ceil(F(m, 25)), m//5 + 1), n - 1 - len(speeds)))
    return speeds


def run_panels():
    for n in (14, 15, 16):
        for panel, name in enumerate(("neutral", "low", "high", "mixed")):
            rng = Random(2026112400 + 10*n + panel)
            failures = 0
            recovered = [0] * (n.bit_length() - 1)
            for _ in range(256):
                speeds = draw(n, panel, rng)
                assert len(set(speeds)) == n - 1
                if cleared(F(7, 2*max(speeds)), speeds, n):
                    assert panel == 0
                    continue
                failures += 1
                last_hit = False
                for index in range(len(recovered)):
                    k = index + 1
                    t = repair(speeds, k)
                    oracle = endpoint_witness(speeds, k)
                    assert (t is None) == (oracle is None)
                    if t is not None:
                        assert cleared(t, speeds, n)
                        recovered[index] += 1
                    assert not last_hit or t is not None
                    last_hit = t is not None
            print(n, name, failures, *recovered)


def check_jump_times():
    checked = 0
    for n, k in ((8, 3), (15, 3), (16, 4)):
        delta = F(1, n)
        for subset in combinations(range(1, 10), k):
            fast = sorted(subset, reverse=True)
            # A direct scan of candidate entry times up to the proven wait cap.
            cap = sum(2*delta*2**(k - j - 1)/v for j, v in enumerate(fast))
            for start in (F(-2, 7), F(0), F(1, 17), (1 - delta)/fast[0], F(4, 9)):
                end = start + cap
                events = {start}
                for speed in fast:
                    for lap in range(ceil(start*speed - delta), floor(end*speed - delta) + 1):
                        events.add((lap + delta)/speed)
                expected = next(t for t in sorted(events) if cleared(t, fast, n))
                assert earliest(start, fast, delta) == expected
                checked += 1
    print("Earliest times checked:", checked)


def controls():
    n = 16
    low = [9, *range(11, 23), 150, 560]
    t0 = F(1, 160)
    assert not cleared(t0, low, n) and cleared(t0, low[1:], n)
    assert not cleared(F(1, 144), [150], n)
    assert not cleared(F(17, 2400), [560], n)
    assert repair(low, 1) is None and repair(low, 2) == F(13, 1792)
    assert cleared(F(13, 1792), low, n)
    high = [*range(12, 25), 160, 560]
    assert not cleared(t0, high, n) and cleared(t0, high[:-2] + [560], n)
    assert repair(high, 1) == F(3, 512) and cleared(F(3, 512), high, n)
    miss = [1, *range(31, 56, 2), 101]
    assert cleared(F(7, 202), miss[1:], n) and not cleared(F(7, 202), [1], n)
    assert all(repair(miss, k) is None for k in (1, 2, 3, 4))
    assert cleared(F(1, 2), miss, n)
    # Earliest includes equality, for either direction and repeated magnitudes.
    for count in (1, 2, 3, 4):
        for t in (F(-1,16), F(1,16), F(15,16), F(17,16)):
            assert earliest(t, [1]*count, F(1,16)) == t


if __name__ == "__main__":
    controls()
    check_jump_times()
    run_panels()
