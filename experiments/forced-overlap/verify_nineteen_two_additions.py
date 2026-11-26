"""Exact finite verifier for two free integer speeds beyond the fixed 17-runner group."""

from fractions import Fraction
from functools import lru_cache
from math import gcd

FIXED = (*range(15), 105, 420)
M = max(FIXED)
N = 19
K = 4 * M
MAX_Y = N * (K - 1)
TIMES = [(p, q) for q in range(2, 65) for p in range(1, q // 2 + 1) if gcd(p, q) == 1]


def safe(difference, p, q, n):
    residue = p * difference % q
    return n * min(residue, q - residue) >= q


def fixed_times(r, n):
    differences = [abs(s - r) for s in FIXED if s != r]
    for p, q in TIMES:
        if all(safe(u, p, q, n) for u in differences):
            yield p, q


def base_interval(r):
    differences = [abs(s - r) for s in FIXED if s != r]
    for p, q in fixed_times(r, N):
        laps = [(u, (u * p) // q) for u in differences]
        a = max(Fraction(N * lap + 1, N * u) for u, lap in laps)
        b = min(Fraction(N * (lap + 1) - 1, N * u) for u, lap in laps)
        if 15 * (K - r) * (b - a) > 4:
            return a, b
    raise ValueError(f"No sufficiently wide interval for {r}")


@lru_cache(None)
def repetitions(q, limit):
    # One bit at positions 0, q, 2q, ... through the last full or partial period.
    copies = (limit + q - 1) // q
    return ((1 << (copies * q)) - 1) // ((1 << q) - 1)


@lru_cache(maxsize=20000)
def safe_mask(residue_class, p, q, limit):
    # Bit v is set precisely when a runner at speed v clears the reference.
    period = sum(1 << v for v in range(q) if safe(v - residue_class, p, q, N))
    return period * repetitions(q, limit)


def cover(r, candidates, remaining, limit):
    for p, q in candidates:
        remaining &= ~safe_mask(r % q, p, q, limit)
        if not remaining:
            return
    first_failure = (remaining & -remaining).bit_length() - 1
    raise ValueError(f"No time for reference {r} against additional speed {first_failure}")


def exact_control(group):
    """Find one scalar rational witness per runner without using packed bit sets."""
    minima = []
    for r in group:
        for p, q in TIMES:
            residues = [(p * (s - r)) % q for s in group if s != r]
            distance = Fraction(min(min(a, q - a) for a in residues), q)
            if N * distance >= 1:
                minima.append(distance)
                break
        else:
            raise ValueError(f"Missing direct control witness for {r} in {group}")
    return min(minima)


def verify():
    base = tuple(FIXED)
    if len(set(base)) != 17 or M != 420 or K != 1680:
        raise ValueError("Unexpected fixed group")
    intervals = {r: base_interval(r) for r in base}
    # In the three-addition corollary, 420 becomes a free slot and M drops to 105.
    core = base[:-1]
    if any(13 * (K - r) * (intervals[r][1] - intervals[r][0]) <= 6 for r in core):
        raise ValueError("A fixed reference lacks room for three large additions")
    duration_margin = Fraction(7, 2 * max(core)) - Fraction(15, K) - Fraction(8, 420)
    if duration_margin != Fraction(3, 560):
        raise ValueError("Incorrect large-gap margin")
    pool18 = {r: list(fixed_times(r, 18)) for r in base}
    pool19 = {r: list(fixed_times(r, 19)) for r in base}
    fixed_bits = sum(1 << s for s in base)
    finite_pairs = rows = 0
    for x in range(1, K):
        if x in base:
            continue
        # Certify the 18 old runners at 1/18 before adjoining a very fast y.
        for r in base:
            if not any(safe(x - r, p, q, 18) for p, q in pool18[r]):
                raise ValueError(f"Missing 1/18 witness for {r}, x={x}")
        if next(fixed_times(x, 18), None) is None:
            raise ValueError(f"Missing 1/18 witness for x={x}")
        cutoff = N * max(M, x)
        # The interval of legal y is [x+1, cutoff), with fixed speeds removed.
        ys = ((1 << cutoff) - (1 << (x + 1))) & ~fixed_bits
        finite_pairs += ys.bit_count()
        rows += 1
        for r in base:
            candidates = ((p, q) for p, q in pool19[r] if safe(x - r, p, q, N))
            cover(r, candidates, ys, MAX_Y)
        cover(x, fixed_times(x, N), ys, MAX_Y)

    # For y at or above this bound, 1/(2y) clears every x<K and all fixed speeds.
    half_lap_cutoff = (N * (K - 1) + (N - 3)) // (N - 2)
    for y in range(2, half_lap_cutoff):
        if y in base:
            continue
        xs = ((1 << min(K, y)) - 2) & ~fixed_bits
        if xs:
            cover(y, fixed_times(y, N), xs, K)
    if (rows, finite_pairs) != (1663, 26929083):
        raise ValueError("The finite ranges do not match the stated counts")
    controls = [(15, 16), (419, 421), (481, 482), (480, 9120),
                (1679, 31900), (1679, 31901), (1680, 1681), (1680, 2800)]
    for x, y in controls:
        exact_control((*base, x, y))
    exact_control((*core, 1680, 2100, 2520))
    print(f"{rows:,} single-speed tails, {finite_pairs:,} finite pairs, {N*finite_pairs:,} finite roles.")
    print(f"Checked {len(base)} fixed-reference intervals for x >= {K}.")


if __name__ == "__main__":
    verify()
