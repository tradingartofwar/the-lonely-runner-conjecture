"""Exact same-pass test for the endpoints of a candidate trapped interval."""
from math import gcd


def can_trap_pair(pair, fastest):
    """Test the endpoint runners alone, assuming fastest > max(pair.u, pair.w)."""
    u, w, n = pair.u, pair.w, pair.total
    if fastest <= max(u, w):
        raise ValueError("The added speed must be fastest.")
    max_width = (2 * u * w - 1) // fastest
    if pair.scaled_width > max_width:
        return False

    g = gcd(u, w)
    period = u // g
    inverse = pow(w // g, -1, period) if period > 1 else 0
    q = g // gcd(fastest, g)
    for width in range(pair.scaled_width, max_width + 1, n*g):
        # One solution of u*j-w*i=(width+u+w)/n. All time translations
        # for this width differ by multiples of 1/g.
        z = (width + u + w) // n
        i = (-(z // g) * inverse) % period
        j = (z + w*i) // u
        # q*(V*b - 1/n) < k < q*(V*a + 1/n) for one integer k.
        lower_num = q * (fastest * (n*j - 1) - w)
        first_integer = lower_num // (n*w) + 1
        upper_num = q * (fastest * (n*i + 1) + u)
        if n*u*first_integer < upper_num:
            return True
    return False
