"""Choose one time from integer speeds. No witness evaluation occurs here."""

from fractions import Fraction


def choose_time(speeds):
    # Each denominator <=16 is safe at 1/q unless a gap is divisible by q.
    # Prefer the fewest collisions, then the shortest escape from the slowest.
    def key(q):
        hits = [v for v in speeds if v % q == 0]
        return len(hits), -min(hits, default=0), q

    q = min(range(2, 17), key=key)
    anchor = Fraction(1, q)
    colliding = [v for v in speeds if v % q == 0]
    if not colliding:
        return q, anchor, anchor
    first_escape = Fraction(1, 16 * min(colliding))
    away = [v for v in speeds if v % q]
    # Before the first exit of a noncollider from its current closed safe arc,
    # each time direction has the following guaranteed headroom.
    forward = min((Fraction(15*q - 16*(v % q), 16*q*v) for v in away), default=1)
    backward = min((Fraction(16*(v % q) - q, 16*q*v) for v in away), default=1)
    direction = 1 if forward >= backward else -1
    return q, anchor + direction * first_escape, anchor + first_escape

