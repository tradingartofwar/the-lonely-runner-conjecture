"""Check a fixed-clock lower/upper bound for one primitive 16-runner family.

At reference 0 the opponents are 1,3,...,21 and M,M+2,M+4,M+6, with M even
and at least 60. A fixed clock is one real time chosen before seeing M. For
s clocks t_i, partition [0,1)^s into 16^s half-open boxes. Two of the 16^s+1
points ({60*j*t_i}) must share a box. The positive difference of their j
values gives M <= 60*16^s for which every ||M*t_i|| < 1/16. This argument
covers arbitrary real clocks. The executable checks finite instances of it,
as well as every lineup under the one-million speed cap.
"""

from fractions import Fraction
from itertools import combinations
from math import isqrt


ODDS = tuple(range(1, 22, 2))
THRESHOLD = Fraction(1, 16)
MAX_SPEED = 1_000_000


def lineup(m):
    return (*ODDS, m, m + 2, m + 4, m + 6)


def residue_distance(speed, numerator, denominator):
    residue = speed * numerator % denominator
    return min(residue, denominator - residue)


def minimum_clearance(speeds, time):
    numerator, denominator = time.as_integer_ratio()
    nearest = min(residue_distance(v, numerator, denominator) for v in speeds)
    return Fraction(nearest, denominator)


def blocker_for_rational_clocks(clocks):
    """Construct the blocked M using the boxes in the lower-bound proof."""
    first_seen = {}
    for j in range(16**len(clocks) + 1):
        cell = tuple(int(16 * ((60*j*t) % 1)) for t in clocks)
        if cell in first_seen:
            return 60 * (j - first_seen[cell])
        first_seen[cell] = j
    raise AssertionError("More points than boxes forces a repeated cell")


def root_clock_blocked(speed, radicand):
    """Test ||speed*sqrt(radicand)|| < 1/16 using exact integer comparisons."""
    square = speed * speed * radicand
    floor_root = isqrt(square)
    return any(
        (16*k - 1)**2 < 256*square < (16*k + 1)**2
        for k in (floor_root, floor_root + 1)
    )


def scale_banks(max_speed):
    lower = 60
    while lower + 6 <= max_speed:
        clock = Fraction(1, 2) + Fraction(1, 16*lower)
        upper = 15*lower - 6
        yield lower, upper, clock
        lower = upper + 2


def check():
    banks = list(scale_banks(MAX_SPEED))
    assert [left for left, right, clock in banks] == [60, 896, 13_436, 201_536]
    assert len(banks) == 4
    assert 60*16**3 + 6 <= MAX_SPEED
    total = 0
    for left, right, clock in banks:
        assert minimum_clearance(lineup(left), clock) == THRESHOLD
        assert minimum_clearance(lineup(right), clock) == THRESHOLD
        # Directly test every opponent in every assigned lineup in the range.
        numerator, denominator = clock.as_integer_ratio()
        for m in range(left, min(right, MAX_SPEED - 6) + 1, 2):
            assert all(
                16 * residue_distance(v, numerator, denominator) >= denominator
                for v in lineup(m)
            )
            total += 1
    assert total == (MAX_SPEED - 6 - 60)//2 + 1 == 499_968

    clocks = [clock for left, right, clock in banks]
    for triple in combinations(clocks, 3):
        blocker = blocker_for_rational_clocks(triple)
        assert blocker % 60 == 0 and 60 <= blocker <= 60*16**3
        assert all(minimum_clearance((blocker,), t) < THRESHOLD for t in triple)

    # A separate lower-bound control uses three irrational times. Squared
    # integer inequalities establish collisions without floating-point error.
    m = 17_940
    assert all(root_clock_blocked(m, radicand) for radicand in (2, 3, 5))
    adaptive_time = Fraction(m + 1, 2*m)
    assert minimum_clearance(lineup(m), adaptive_time) == Fraction(5_973, 11_960)
    assert minimum_clearance(lineup(m), adaptive_time) == Fraction(m - 21, 2*m)

    print(f"{total:,} lineups checked through maximum speed {MAX_SPEED:,}.")
    print("Four fixed clocks:", ", ".join(map(str, clocks)))
    print("Constructed a blocker for each of the four rational three-clock subsets.")
    print(f"sqrt(2), sqrt(3), sqrt(5) blocked at M={m}; "
          f"adaptive time {adaptive_time} gives clearance 5973/11960.")
    print("Three arbitrary real clocks fail by pigeonhole; four suffice for this family.")


if __name__ == "__main__":
    check()
