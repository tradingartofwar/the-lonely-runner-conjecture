"""Exact shape inequalities, with outward-rounded logarithms only for reporting."""

from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import lcm, prod


def q(t):
    return 1 + 2*t - t*t


def b(m, t):
    return 1 + 2*t + (2*m - 3)*t*t


def cubic(m, t):
    return (m - 1)*(2*m - 3)*t**3 + (2*m - 5)*t*t + (m - 5)*t - 1


def minimizer_bracket(m):
    lo, hi = F(0), F(1)
    assert m >= 5 and cubic(m, lo) < 0 < cubic(m, hi)
    for _ in range(45):
        mid = (lo + hi)/2
        if cubic(m, mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def shape_power(m, lo, hi):
    """Lower bound on h_m(t)^m for lo <= t <= hi <= 1."""
    return b(m, lo)**m * q(lo)**(m*(m - 2)) / hi**(2*(m - 1))


def product_bounds(n):
    m = n - 1
    prefix = [F(4*r*r, n*n*(n - r)**2) for r in range(m)]
    increments = [v - u for u, v in zip(prefix, prefix[1:])]
    assert all(3*v > 4*u for u, v in zip(increments, increments[1:]))
    k = prod(increments)
    lo, hi = minimizer_bracket(m)
    floor = shape_power(m, lo, hi)
    # c = 7/2 means the fastest runner is a half-lap away.
    left, right = F(2, 7*n), F(2*(n - 1), 7*n)
    assert left < lo < hi < right < 1
    outside = min(shape_power(m, left, left), shape_power(m, right, right))
    assert outside > floor
    power = 2*(m - 1)
    factor = 1 / k**(m*(m - 1))
    unrestricted = factor / floor**(m - 1)
    restricted = factor / (floor**(m - 2) * outside)
    # Exact upper bounds on the speed product raised to 'power'.
    return lo, hi, power, unrestricted, restricted


def upper_log(bound, power):
    with localcontext() as ctx:
        ctx.prec = 45
        # ln is correctly rounded to nearest. Expand one step on each side.
        ln_num = Decimal(bound.numerator).ln().next_plus()
        ln_den = Decimal(bound.denominator).ln().next_minus()
        return ((ln_num - ln_den).next_plus() / Decimal(power)).next_plus()


def check_reduction(m):
    # Compare the full-dimensional formula and its scalar lower bound
    # by clearing all radical powers. Check equality on a repeated coordinate.
    for others in [[F(1, 11)]*(m - 1),
                   [F(i, m) for i in range(1, m)],
                   [F(1, 9)]*(m - 2) + [F(1)]]:
        u = [F(1), *others]
        sum_w = sum(t*t/q(t) for t in u)
        h_full_to_m = sum_w**m * prod(q(t)**m/t**2 for t in u)
        lower = prod(shape_power(m, t, t) for t in others)
        assert h_full_to_m**(m - 1) >= lower
        assert (h_full_to_m**(m - 1) == lower) == (len(set(others)) == 1)


def check_physical_clock():
    # Fourteen slower opponents and one fastest opponent of the reference.
    speeds = [*range(10, 23), 150, 560]
    def distances(vs):
        t = F(7, 2*max(vs))
        return [min(v*t % 1, -v*t % 1) for v in vs]
    assert len(speeds) == 15 and min(distances(speeds)) == F(1, 16)
    assert distances(speeds)[0] == distances(speeds)[-2] == F(1, 16)
    assert min(distances([9, *speeds[1:]])) == F(9, 160)


if __name__ == "__main__":
    check_physical_clock()
    for n in (14, 15, 16):
        m = n - 1
        check_reduction(m)
        lo, hi, power, original, improved = product_bounds(n)
        log_original = upper_log(original, power)
        log_improved = upper_log(improved, power)
        divisor = lcm(*range(2, n + 1))
        gate = upper_log(improved / divisor**power, power)
        print(f"{n}: shape ratio {float((lo+hi)/2):.9f}, log product before "
              f"{log_original:.8f}, after {log_improved:.8f}, "
              f"prime threshold {gate:.8f} (display rounded to nearest)")
        if n == 16:
            assert log_improved < Decimal("496.044") and gate < Decimal("482.556")
            # Conditional on the independent 16-runner dual-cap multiplier.
            cap = F(12150, 9163)
            capped_gate = upper_log(improved / (divisor**power * cap**(m*(m-1))), power)
            print(f"16 with reported dual cap, conditional threshold {capped_gate:.8f}")
