"""Check separate lonely clocks for all roles in a structured 16-runner family.

Lineups are {0,1,3,...,21,M,M+2,M+4,M+6}, with even M >= 60.
For these lineups, this verifier checks the odd and fast references, and the
companion fixed-clock verifier treats reference 0. It also checks clocks for
all roles on a more general class with independently varying speeds.
Different runners may use different times.
"""

from fractions import Fraction as F
from random import Random


ODDS = tuple(range(1, 22, 2))
SLOW = (0, *ODDS)
FAST_OFFSETS = (0, 2, 4, 6)
ODD_NUMERATORS = (1, 3, 5, 7, 9, 11)


def is_clear(gap, numerator, denominator):
    residue = gap*numerator % denominator
    return 16*min(residue, denominator - residue) >= denominator


def lineup(m):
    return (*SLOW, *(m+j for j in FAST_OFFSETS))


def clearance(reference, speeds, t):
    num, den = t.as_integer_ratio()
    return F(min(min((v-reference)*num % den, (reference-v)*num % den)
                 for v in speeds if v != reference), den)


def check_odd_roles():
    # Every even M mod 26 occurs once in this range. The six possible odd
    # clocks, allowed residues and each opponent only depend on M mod 26.
    minimum_survivors = len(ODD_NUMERATORS)
    for m in range(60, 86, 2):
        speeds = lineup(m)
        evens = [v for v in speeds if v % 2 == 0]
        for root in ODDS:
            for other in ODDS:
                if other != root:
                    assert all(is_clear(other-root, h, 26) for h in ODD_NUMERATORS)
            for v in evens:
                assert sum(not is_clear(v-root, h, 26) for h in ODD_NUMERATORS) <= 1
            survivors = sum(clearance(root, speeds, F(h, 26)) >= F(1,16)
                            for h in ODD_NUMERATORS)
            assert survivors >= 1
            minimum_survivors = min(minimum_survivors, survivors)
    return minimum_survivors


def fast_scale_cover(maximum):
    """Return contiguous integer ranges and a fixed time valid on each range."""
    cover = []
    lower, scale = 60, F(32)
    while lower <= maximum:
        left = scale + 21
        right = 11*scale/5
        # The next interval starts no later than this right endpoint.
        assert 3*scale/2 + 21 <= right
        upper = min(maximum, right.numerator//right.denominator)
        assert left <= lower <= upper <= right
        t = F(1,5) + 1/(16*scale)
        cover.append((lower, upper, t))
        lower = upper + 1
        scale *= F(3,2)
    return cover


def check_fast_roles(maximum):
    # Test each even root up to maximum. For a fixed R the differences to the
    # slow group depend only on R; all possible fast companions have absolute
    # difference 2, 4, or 6. All arithmetic in the exhaustive loop is integral.
    cover = fast_scale_cover(maximum)
    checked = 0
    for lower, upper, fixed_time in cover:
        fixed_num, fixed_den = fixed_time.as_integer_ratio()
        assert all(is_clear(v, fixed_num, fixed_den) for v in (2,4,6))
        for root in range(lower + lower % 2, upper + 1, 2):
            if root % 8:
                adapt_num, adapt_den = 1, 8
            else:
                # 1/8 + 1/(16*R)
                adapt_num, adapt_den = 2*root + 1, 16*root
            assert all(is_clear(v, adapt_num, adapt_den) for v in (2,4,6))
            for s in SLOW:
                assert is_clear(root-s, fixed_num, fixed_den)
                assert is_clear(root-s, adapt_num, adapt_den)
            checked += 1
    assert checked == (maximum - 60)//2 + 1
    # Isolate half-open/inclusive arithmetic near several scale transitions.
    for lower, upper, t in (cover[0], cover[len(cover)//2], cover[-1]):
        for root in (lower + lower % 2, upper - upper % 2):
            for j in FAST_OFFSETS:
                m = root - j
                if m >= 60:
                    assert clearance(root, lineup(m), t) >= F(1,16)
    return checked, len(cover)


def check_varied_lineup(m, odds, fast):
    """Check all fifteen opponents at a role-specific witness for every role."""
    assert len(odds) == 11 and len({s % 26 for s in odds}) == 11
    assert all(s > 0 and s % 2 == 1 and 8*s <= 7*m for s in odds)
    assert len(fast) == 4 and min(fast) == m and 8*max(fast) <= 15*m
    assert {s % 8 for s in fast} == {0, 2, 4, 6}
    speeds = (0, *odds, *fast)

    stationary_time = F(1, 2) + F(1, 2*m)
    stationary_clearance = clearance(0, speeds, stationary_time)
    assert stationary_clearance >= F(1, 16)
    for root in odds:
        assert any(all(is_clear(speed-root, h, 26) for speed in speeds if speed != root)
                   for h in ODD_NUMERATORS)
    for root in fast:
        time = F(1, 8)
        if root % 8 == 0:
            time += F(1, 16*root)
        assert clearance(root, speeds, time) >= F(1, 16)
    return stationary_clearance


def check_varied_families():
    # Each opposite-parity gap blocks at most one of the six candidate times.
    # Every same-parity gap between distinct odd residue classes passes all six.
    for gap in range(1, 26):
        failures = sum(not is_clear(gap, h, 26) for h in ODD_NUMERATORS)
        assert failures <= gap % 2

    rng = Random(162608)
    count = 0
    for m in (*range(24, 182, 2), 254, 256, 408, 1000, 8192):
        odd_limit = 7*m//8
        fast_limit = 15*m//8
        by_mod26 = [range(r, odd_limit + 1, 26) for r in range(1, 26, 2)]
        odd_classes = [group for group in by_mod26 if len(group)]
        by_mod8 = [range(m + shift, fast_limit + 1, 8) for shift in (2, 4, 6)]
        # Include lower and upper representatives, then vary both groups
        # independently with a fixed seed. Deduplication counts actual lineups.
        odds_choices = {tuple(group[0] for group in odd_classes[:11]),
                        tuple(sorted(group[-1] for group in odd_classes[-11:]))}
        fast_choices = {(m, *(group[0] for group in by_mod8)),
                        (m, *sorted(group[-1] for group in by_mod8))}
        for _ in range(3):
            odds_choices.add(tuple(sorted(rng.choice(group)
                                          for group in rng.sample(odd_classes, 11))))
            fast_choices.add((m, *sorted(rng.choice(group) for group in by_mod8)))
        for odds in sorted(odds_choices):
            for fast in sorted(fast_choices):
                check_varied_lineup(m, odds, fast)
                count += 1

    # Separate equality cases: 7M/8 is odd for M=72, whereas 15M/8 is even
    # for M=80. Each extremal opponent realizes exactly 1/16 for reference 0.
    slow_boundary = tuple(s for s in ODDS if s != 11) + (63,)
    assert max(slow_boundary)*8 == 7*72
    assert check_varied_lineup(72, slow_boundary, (72, 90, 108, 118)) == F(1, 16)
    fast_boundary = (80, 98, 132, 150)
    assert max(fast_boundary)*8 == 15*80
    assert check_varied_lineup(80, ODDS, fast_boundary) == F(1, 16)
    return count


def check_collision_repair():
    """Test a wider class with a single colliding even pair at time 1/8.

    After translation or reversal, put the colliding pair at 0 and F, with F
    divisible by 8. The eleven odd speeds lie between the pair, distinct mod
    26. The other even speeds have distinct nonzero residues modulo 8, and
    lie in [-2F, 3F]; translation makes every speed nonnegative if desired.
    """
    count = 0
    rng = Random(162613)
    for span in (24, 32, 40, 56, 64, 80, 128, 200, 360, 1024):
        odd_classes = [range(r, span + 1, 26) for r in range(1, 26, 2)]
        odd_classes = [group for group in odd_classes if len(group)]
        even_classes = [range(-2*span + r, 3*span + 1, 8) for r in (2, 4, 6)]
        odds_choices = {tuple(group[0] for group in odd_classes[:11])}
        evens_choices = {tuple(group[-1] for group in even_classes),
                         tuple(group[0] for group in even_classes)}
        for _ in range(8):
            odds_choices.add(tuple(sorted(rng.choice(group)
                                          for group in rng.sample(odd_classes, 11))))
            evens_choices.add(tuple(rng.choice(group) for group in even_classes))
        for odds in sorted(odds_choices):
            for evens in sorted(evens_choices):
                speeds = (0, span, *evens, *odds)
                for root in (0, span):
                    assert clearance(root, speeds, F(1, 8)+F(1, 16*span)) == F(1, 16)
                for root in evens:
                    assert clearance(root, speeds, F(1, 8)) >= F(1, 16)
                for root in odds:
                    assert any(all(is_clear(v-root, h, 26) for v in speeds if v != root)
                               for h in ODD_NUMERATORS)
                count += 1
    return count


if __name__ == "__main__":
    survivors = check_odd_roles()
    checked, count = check_fast_roles(1_000_000)
    print(f"143 odd-reference residue cases checked. Minimum passing clocks out of six: {survivors}.")
    print(f"{checked:,} even fast reference speeds checked through 1,000,000 against "
          "both the adaptive time and their assigned fixed time.")
    print(f"{count} fast-role times + 6 odd-role times + 4 stationary times "
          f"gives an all-role fixed schedule of at most {count+10} times at that ceiling.")
    varied = check_varied_families()
    print(f"{varied:,} independently varied lineups and two explicit equality "
          "controls passed all sixteen roles; all 25 nonzero gap residues "
          "modulo 26 passed the odd-role test.")
    repaired = check_collision_repair()
    print(f"{repaired:,} lineups from the wider single-collision class passed "
          "all roles, including signed even speeds outside the colliding pair.")
