"""Exact same-pass test for the endpoints of a candidate trapped interval."""
from math import gcd


def can_trap_pair(pair, fastest):
    """Test the endpoint runners alone, assuming fastest > max(pair.u, pair.w)."""
    u, w = pair.u, pair.w
    if fastest <= max(u, w):
        raise ValueError("The added speed must be fastest.")
    max_width = (2 * u * w - 1) // fastest
    if pair.scaled_width > max_width:
        return False

    g = gcd(u, w)
    period = u // g
    inverse = pow(w // g, -1, period) if period > 1 else 0
    q = g // gcd(fastest, g)
    for width in range(pair.scaled_width, max_width + 1, 16*g):
        # One solution of u*j-w*i=(width+u+w)/16. All time translations
        # for this width differ by multiples of 1/g.
        z = (width + u + w) // 16
        i = (-(z // g) * inverse) % period
        j = (z + w*i) // u
        # q*(V*b - 1/16) < k < q*(V*a + 1/16) for one integer k.
        lower_num = q * (fastest * (16*j - 1) - w)
        first_integer = lower_num // (16*w) + 1
        upper_num = q * (fastest * (16*i + 1) + u)
        if 16*u*first_integer < upper_num:
            return True
    return False
