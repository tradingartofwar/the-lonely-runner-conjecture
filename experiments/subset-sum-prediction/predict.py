"""One certified time or an abstention, from four weights. No time grid."""
from fractions import Fraction as F
from math import ceil, gcd

DELTA = F(1, 16)


def positive_chart(weights):
    """Keep the earliest feasible winding number at each prefix."""
    left, right = F(0), F(1)
    speed_sum = laps = 0
    for i, speed in enumerate(weights, start=1):
        speed_sum += speed
        cap = 1 - (5-i) * DELTA
        # For this lap, require left <= (laps + k + cap) / speed_sum.
        # The other lower bound on time, (k+delta)/speed, grows at least
        # as fast with k as that upper bound. right is fixed at this step.
        k = max(0, ceil(speed_sum * left - laps - cap))
        laps += k
        left = max(left, (k + DELTA) / speed)
        right = min(right, (laps + cap) / speed_sum)
        if left > right:
            return None
    return (left + right) / 2


def predict(weights):
    a, b, c, d = weights
    total = sum(weights)
    if a % 5 and a % 5 == b % 5 == c % 5:
        # Anchor the three small generators at 1/5 and put the total at ±1/15.
        start = F(pow(a, -1, 5), 5)
        y = total * start
        eps = F(1, 15)
        if y % 1 == F(1, 5):
            return "complements", (int(y) - eps) / total
        return "complements", (ceil(y - eps) + eps) / total
    if total <= 15 * a:
        return "first_lap", F(1, total + a)
    odd = sorted(v for v in weights if v % 2)
    even = [v for v in weights if not v % 2]
    least_even = min([*even, odd[0] + odd[1]])
    if total <= 15 * least_even and total - odd[0] <= 7 * least_even:
        return "parity", F(1, 2) + DELTA / least_even
    lower_sum = a + b + c
    g = gcd(a, b, c)
    if g * (14*a - lower_sum) >= 16*a:
        base = DELTA / a
        # Adding j/g fixes the three lower phases. The fast phase can be
        # chosen from a grid of spacing 1/g, with gcd(d,g)=1.
        step = ceil(g * (DELTA - d*base))
        j = step * pow(d, -1, g) % g
        return "fixed_lower_phases", base + F(j, g)
    k = ceil(F(d - a, 16*a))
    if lower_sum * (16*k + 1) <= 14*d:
        return "fast_wrap", F(16*k + 1, 16*d)
    t = positive_chart(weights)
    if t is not None:
        return "winding", t
    # Four successive alignments. Future drifts cost less than 1/speed.
    ratio_sum = sum(F(sum(weights[:j]), weights[j]) for j in (1, 2, 3))
    if ratio_sum <= F(11, 16):
        t = DELTA / a
        for v in weights[1:]:
            t = (ceil(v * t - DELTA) + DELTA) / v
        return "separated", t
    return "abstain", None

