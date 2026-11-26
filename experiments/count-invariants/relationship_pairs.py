"""Check 16-runner pairs with identical pair-distance multisets at every time.

Their speed sets are direct sums A+B and A+(max(B)-B). Ordered differences have
the form (a-a')+(b-b'). Negating the second difference just exchanges b and b',
so the ordered difference multisets coincide. Each positive absolute gap is
counted twice among ordered pairs. Applying d -> ||d*t|| to the unordered gaps
therefore proves equality of the pair-distance multisets for every real t.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals


def pair_gaps(lineup):
    return Counter(v - u for u, v in combinations(sorted(lineup), 2))


def snapshot(lineup, time):
    """Keep physical runner labels while finding the nearest other runner."""
    nearest = {v: F(1) for v in lineup}
    distances = Counter()
    for u, v in combinations(lineup, 2):
        distance = circular_distance((v - u) * time)
        distances[distance] += 1
        nearest[u] = min(distance, nearest[u])
        nearest[v] = min(distance, nearest[v])
    lonely = tuple(v for v in lineup if nearest[v] >= F(1, len(lineup)))
    return distances, lonely


def best_by_runner(lineup):
    result = {}
    for ref in lineup:
        speeds = sorted({abs(v - ref) for v in lineup if v != ref})
        best = exact_maximum(speeds)
        # A separate closed-interval check at the claimed maximum must recover
        # exactly these isolated points. A larger value would imply an interval.
        assert feasible_intervals(speeds, best.value) == tuple((t, t) for t in best.times)
        result[ref] = (best.value, best.times[0])
    return result


def main():
    x, y = (0, 1, 4, 7), (0, 9, 18, 28)
    one = sorted(a + b for a in x for b in y)
    two = sorted(a + 28 - b for a in x for b in y)
    assert len(set(one)) == len(set(two)) == 16
    assert pair_gaps(one) == pair_gaps(two) and sum(pair_gaps(one).values()) == 120
    spectra = [snapshot(lineup, F(1, 3)) for lineup in (one, two)]
    assert spectra == [({F(0): 51, F(1, 3): 69}, ()),
                       ({F(0): 51, F(1, 3): 69}, (0,))]
    counts = [[sum(v % 3 == j for v in lineup) for j in range(3)] for lineup in (one, two)]
    assert counts == [[3, 10, 3], [1, 6, 9]]
    print(f"t=1/3: position counts {counts}, lonely speeds () / (0,)")

    a, b = (0, 1, 3, 7), (0, 9, 20, 44)
    first = sorted(x + y for x in a for y in b)
    second = sorted(x + 44 - y for x in a for y in b)
    assert len(set(first)) == len(set(second)) == 16
    gaps = pair_gaps(first)
    assert sum(gaps.values()) == 120 and gaps == pair_gaps(second)

    for time, expected in [(F(1, 4), ((10,), ())), (F(7, 17), ((), (38, 45)))]:
        distances_a, lonely_a = snapshot(first, time)
        distances_b, lonely_b = snapshot(second, time)
        assert distances_a == distances_b and (lonely_a, lonely_b) == expected
        if time == F(1, 4):
            assert distances_a == {F(0): 31, F(1, 4): 60, F(1, 2): 29}
            occupancies = [[sum(v % 4 == j for v in lineup) for j in range(4)]
                           for lineup in (first, second)]
            assert occupancies == [[5, 4, 1, 6], [4, 3, 2, 7]]
            print("Quarter-lap position counts:", occupancies)
        print(f"t={time}: lonely speeds {lonely_a} / {lonely_b}")

    for lineup, expected_zero, expected_worst in [
        (first, (F(1, 6), F(25, 54)), (3, F(2, 17), F(3, 34))),
        (second, (F(4, 25), F(37, 75)), (35, F(1, 9), F(7, 18))),
    ]:
        maxima = best_by_runner(lineup)
        worst = min(value for value, time in maxima.values())
        tightest = [(v, value, time) for v, (value, time) in maxima.items() if value == worst]
        assert maxima[0] == expected_zero and tightest == [expected_worst]
        print(f"Speed 0 maximum {maxima[0][0]} at {maxima[0][1]}; "
              f"worst runner {tightest[0][0]} reaches {worst} at {tightest[0][2]}")


if __name__ == "__main__":
    main()
