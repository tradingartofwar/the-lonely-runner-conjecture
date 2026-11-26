"""Adversarial replay, independent of trial inputs and the frozen predictor."""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "one-time-prediction"))
from predictor import choose_time  # The archived fifteen-speed ranking.

TARGET = Fraction(1, 16)


def physical(weights):
    speeds = sorted(sum(group) for n in range(1, 5) for group in combinations(weights, n))
    assert len(set(speeds)) == 15
    return speeds


def residue_groups(speeds, q):
    groups = defaultdict(list)
    for v in speeds:
        groups[v % q].append(v)
    return groups


def certificate(groups, q, sign):
    """First-arc inequalities, integer cross-products, sorted physical classes."""
    colliders = groups[0]
    slowest = colliders[0]
    if colliders[-1] > 15 * slowest:
        return False
    for residue, group in groups.items():
        if residue:
            room = 15 * q - 16 * residue if sign == 1 else 16 * residue - q
            if q * group[-1] > slowest * room:
                return False
    return True


def modular_distances(speeds, p, denominator):
    """Independent physical endpoint calculation, in units of 1/denominator."""
    return {v: min(v * p % denominator, -v * p % denominator) for v in speeds}


def audit(weights, counts):
    speeds = physical(weights)
    direct, certified, safe = [], [], []
    for q in range(2, 17):
        groups = residue_groups(speeds, q)
        if 0 not in groups:
            direct.append(q)
            assert 16 * min(modular_distances(speeds, 1, q).values()) >= q
            continue
        scale = 16 * groups[0][0]
        for sign in (1, -1):
            denominator = scale * q
            distances = modular_distances(speeds, scale + sign*q, denominator)
            good = 16 * min(distances.values()) >= denominator
            cert = certificate(groups, q, sign)
            if cert:
                assert good, (weights, q, sign)
                certified.append((q, sign))
            if good:
                safe.append((q, sign))
            counts["signed_shifts"] += 1
            counts["certified_shifts"] += cert
            counts["safe_declined_shifts"] += good and not cert
    counts["rows"] += 1
    counts["direct_rows"] += bool(direct)
    counts["abstaining_rows"] += not direct and not certified
    return direct, certified, safe


def outside_box():
    for a, x, j, k in product(range(257, 261), range(1, 17), range(16), range(2)):
        b = a + x
        c = a + b + 4*a + j
        first_three = a + b + c
        d = 16 * (2*first_three // 16 + 1 + k) - first_three
        if gcd(a, b, c, d) == 1:
            yield a, b, c, d


def inspect(weights, q, sign):
    speeds = physical(weights)
    groups = residue_groups(speeds, q)
    h = TARGET / min(groups[0])
    t = Fraction(1, q) + sign * h
    numerator_distances = modular_distances(speeds, t.numerator, t.denominator)
    distances = {v: Fraction(d, t.denominator) for v, d in numerator_distances.items()}
    minimum = min(distances.values())
    limiters = [v for v in speeds if distances[v] == minimum]
    boundaries = []
    for v in speeds:
        if v % q:
            phase = Fraction(v % q, q)
            room = 1 - TARGET - phase if sign == 1 else phase - TARGET
            boundaries.append((room / v, v))
    edge = min(boundaries, default=None)
    print(f"{weights} q={q} sign={sign:+d} h={h} earliest edge={edge}"
          f" time={t} minimum={minimum} at {limiters}")
    return t, minimum, limiters, distances, edge


def main():
    counts = Counter()
    abstentions = []
    for weights in outside_box():
        direct, certified, safe = audit(weights, counts)
        if not direct and not certified:
            abstentions.append((weights, safe))
    assert counts == dict(rows=1769, direct_rows=1408, abstaining_rows=1,
                          signed_shifts=47760, certified_shifts=11549,
                          safe_declined_shifts=2294)
    missed = (260, 264, 1567, 2101)
    assert abstentions == [(missed, [(3, 1), (5, 1), (10, 1), (10, -1), (12, -1)])]
    print(dict(counts))
    print("All-anchor abstentions and safe earliest escapes:", abstentions)

    t, minimum, limiters, _, edge = inspect(missed, 3, 1)
    assert (t, minimum, limiters, edge) == (Fraction(1409, 4224), TARGET, [264],
                                            (Fraction(13, 188736), 3932))
    reentries = [v for v in physical(missed) if v % 3 and
                 Fraction(v % 3, 3) + Fraction(v, 4224) >= 1 + TARGET]
    assert reentries == [3668, 3928, 3932, 4192]
    assert inspect(missed, 3, -1)[1:3] == (Fraction(53, 1408), [1567])
    assert choose_time(physical(missed))[:2] == (16, Fraction(4193, 67072))
    assert inspect(missed, 16, 1)[1:3] == (Fraction(2625, 67072), [1567])
    assert inspect(missed, 16, -1)[1:3] == (Fraction(1567, 67072), [2625])

    # Endpoint-only testing of class extremes misses the sole unsafe trajectory.
    interior = (257, 258, 1543, 2070)
    groups = residue_groups(physical(interior), 5)
    t, minimum, _, distances, _ = inspect(interior, 5, 1)
    assert (t, minimum) == (Fraction(1649, 8240), Fraction(317, 8240))
    assert [v for v, d in distances.items() if d < TARGET] == [3613]
    assert all(distances[group[0]] >= TARGET and distances[group[-1]] >= TARGET
               for group in groups.values())
    assert groups[3] == [258, 1543, 2058, 2328, 3613, 4128]

    # Equality in headroom and in the maximum-collider check, respectively.
    weights = (258, 261, 522, 1453)
    assert certificate(residue_groups(physical(weights), 3), 3, 1)
    _, minimum, limiters, _, edge = inspect(weights, 3, 1)
    assert (minimum, limiters, edge) == (TARGET, [258, 2494], (Fraction(1, 4128), 2494))
    binary = (258, 516, 1032, 2064)
    assert certificate(residue_groups(physical(binary), 2), 2, 1)
    assert inspect(binary, 2, 1)[1:3] == (TARGET, [258, 3870])

    # Constructed outside the stretch-middle shape. The old ranking succeeds.
    big = lcm(*range(2, 17))
    wrapped = (257, 271, big, 17*big)
    assert audit(wrapped, Counter())[:2] == ([], [])
    t, minimum, limiters, _, _ = inspect(wrapped, 5, 1)
    assert choose_time(physical(wrapped))[:2] == (5, t)
    assert (t, minimum, limiters) == (Fraction(461261, 2306304), TARGET, [big, 17*big])


if __name__ == "__main__":
    main()
