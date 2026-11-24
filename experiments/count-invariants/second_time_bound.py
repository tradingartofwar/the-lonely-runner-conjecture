"""Rational lower bounds for the geometric penalty of failing the clock windows."""

from decimal import Decimal
from fractions import Fraction as F
from functools import lru_cache
from math import prod
from check_shape import minimizer_bracket, shape_power, upper_log


def ratio_floors(n, a, depth):
    """Lower bounds on the fast speeds, all normalized to the fastest."""
    floors = [F(1)]
    wait_units = F(0)  # max wait divided by delta, in normalized time
    for _ in range(depth):
        if a == 0:
            floors.append(F(0))
            continue
        wait_units = 2*wait_units + 2/floors[-1]
        floors.append((n - 1)/(1/a + wait_units))
    return floors[1:]


def ceilings(n, bins=512):
    m = n - 1
    depth = n.bit_length() - 1
    lo, hi = minimizer_bracket(m)
    prefix = [F(4*r*r, n*n*(n-r)**2) for r in range(m)]
    increments = [b-a for a, b in zip(prefix, prefix[1:])]
    assert all(3*b > 4*a for a, b in zip(increments, increments[1:]))
    k_flag = prod(increments)
    # All nonfast speeds at least 1/(n-1) give a witness at (n-1)/(n*M).
    limit = F(1, n - 1)
    assert limit < lo
    floor_all = int(shape_power(m, lo, hi))

    @lru_cache(maxsize=None)
    def power_at(x):
        return int(shape_power(m, x, x))

    penalties = [None] * depth
    for i in range(bins):
        lower, upper = limit*i/bins, limit*(i+1)/bins
        # h_m decreases on [lower,upper]. Endpoints at zero require no evaluation.
        factors = power_at(upper)
        for j, fast_lower in enumerate(ratio_floors(n, lower, depth)):
            if fast_lower >= 1:
                break  # a failure would require a speed strictly larger than 1
            factors *= power_at(fast_lower) if fast_lower >= hi else floor_all
            # One factor for the slowest and j+1 factors on separate fast slots.
            exponent = m - 3 - j
            value = factors * floor_all**exponent
            if penalties[j] is None or value < penalties[j]:
                penalties[j] = value
    power = 2*(m - 1)
    ceilings = []
    for penalty in penalties:
        bound = 1/(k_flag**(m*(m - 1))*penalty)
        ceilings.append(upper_log(bound, power))
    return ceilings


if __name__ == "__main__":
    for n in (14, 15, 16):
        row = ceilings(n)
        print(n, *(f"{v:.8f}" for v in row))
        assert all(a >= b for a, b in zip(row, row[1:]))
        target = {14: "339.714", 15: "413.279", 16: "495.218"}[n]
        assert row[-1] < Decimal(target)
