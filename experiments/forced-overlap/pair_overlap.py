"""Exact overlap of two strict Lonely Runner blocker sets on a cyclic grid."""

from math import gcd


def floor_sum(count, modulus, slope, offset):
    """Return sum((slope*i + offset)//modulus for i in range(count))."""
    if count < 0 or modulus <= 0:
        raise ValueError("count must be nonnegative and modulus positive")
    total = 0
    while True:
        slope_quotient, slope = divmod(slope, modulus)
        offset_quotient, offset = divmod(offset, modulus)
        total += slope_quotient * count * (count - 1) // 2
        total += offset_quotient * count
        endpoint = slope * count + offset
        if endpoint < modulus:
            return total
        count, offset = divmod(endpoint, modulus)
        modulus, slope = slope, modulus


def blocked_pair_count(denominator, total_runners, first_speed, second_speed):
    """Count a mod d where both distances to an integer are strictly < 1/n."""
    if denominator < 1 or total_runners < 2:
        raise ValueError("denominator must be positive and total_runners at least 2")
    common = gcd(denominator, first_speed, second_speed)
    period = denominator // common
    first = (first_speed // common) % period
    second = (second_speed // common) % period
    first_gcd = gcd(first, period)
    first_period = period // first_gcd
    first_radius = (first_period - 1) // total_runners
    second_radius = (period - 1) // total_runners
    if first_period == 1:
        multiplier = 0
    else:
        inverse = pow(first // first_gcd, -1, first_period)
        multiplier = (second * inverse) % first_period

    count = 2 * first_radius + 1
    offset = multiplier * first_radius
    upper = floor_sum(count, first_period, -multiplier, offset + second_radius)
    lower = floor_sum(count, first_period, -multiplier, offset - second_radius - 1)
    return common * (upper - lower)
