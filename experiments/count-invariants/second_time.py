"""Closed-interval recovery for a selected reference, in units of one lap."""
from fractions import Fraction as F


def next_safe(t, speed, delta):
    phase = (t * speed) % 1
    if phase < delta:
        return t + (delta - phase) / speed
    if phase > 1 - delta:
        return t + (1 + delta - phase) / speed
    return t


def earliest(t, fast, delta):
    """All speeds sorted fastest first. The proof requires 2**len(fast) <= n."""
    if len(fast) == 1:
        return next_safe(t, fast[0], delta)
    earlier = earliest(t, fast[:-1], delta)
    shifted = next_safe(earlier, fast[-1], delta)
    if shifted == earlier:
        return shifted
    return earliest(shifted, fast[:-1], delta)


def repair(speeds, k):
    """Return a time in the specified window, or None if it contains no witness."""
    ordered = sorted(speeds, reverse=True)
    n = len(ordered) + 1
    if not 1 <= k < len(ordered) or 2**k > n:
        raise ValueError("unsupported number of freely wrapping opponents")
    delta = F(1, n)
    left = delta / ordered[-1]
    right = (1 - delta) / ordered[k]
    if left > right:
        return None
    original = F(7, 2 * ordered[0])
    anchor = max(left, min(original, right))
    # A slow blocker has not reached the start of the first safe arc.
    directions = (1, -1) if ordered[-1] * original < delta else (-1, 1)
    for direction in directions:
        t = direction * earliest(direction * anchor, ordered[:k], delta)
        if left <= t <= right:
            return t
    return None
