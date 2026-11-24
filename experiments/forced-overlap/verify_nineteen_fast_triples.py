"""Check the rational certificates for three fast newcomers to Q."""

from fractions import Fraction as F
from math import gcd

CORE = (*range(15), 105)
K = 1680
DELTA = F(1, 19)
GAP_LIMIT = 840
# Centers retained by the denominator-ordered search in NINETEEN_CLOSE_PROTOCOL.md.
CENTERS = {
    2: [1], 3: [1], 4: [1], 5: [1, 2], 17: [1], 19: [1], 20: [1],
    21: [1, 10], 22: [1, 7], 23: [1, 8, 11], 24: [1], 25: [1, 8, 12],
    26: [1, 9], 27: [1, 13], 28: [1, 9], 29: [1, 7, 10, 14],
    30: [1], 31: [1, 10, 15], 32: [1], 33: [1, 8, 16], 34: [1, 11],
    35: [1, 2, 17], 37: [1, 9], 38: [1], 47: [16],
}


def norm(t):
    phase = t % 1
    return min(phase, 1 - phase)


def midpoint(p, q):
    phases = sorted(set((s * p) % q for s in CORE))
    arcs = zip(phases, phases[1:] + [phases[0] + q])
    a, b = max(arcs, key=lambda arc: arc[1] - arc[0])
    if F(b - a, q) < 2 * DELTA + F(max(CORE), K):
        raise ValueError(("insufficient room", p, q))
    return F(a + b, 2 * q)


def check_gap_pairs():
    allowed = [0] * (GAP_LIMIT + 1)
    centers = []
    for q, numerators in CENTERS.items():
        for p in numerators:
            theta = midpoint(p, q)
            t = F(p, q)
            bit = 1 << len(centers)
            centers.append((t, theta))
            for d in range(1, GAP_LIMIT + 1):
                if norm(d * t) >= DELTA + F(d, 2 * K):
                    allowed[d] |= bit
    pairs = 0
    for e in range(1, GAP_LIMIT + 1):
        for d in range(1, e + 1):
            if not allowed[d] & allowed[e]:
                raise ValueError(("uncovered pair", d, e))
            pairs += 1
    return centers, allowed, pairs


def check_bounds():
    a, b = F(96, 1729), F(113, 1995)
    for i, r in enumerate(CORE):
        for s in CORE[i + 1:]:
            v = s - r
            lap = (v * a).__floor__()
            if not lap + DELTA <= v * a <= v * b <= lap + 1 - DELTA:
                raise ValueError(("fixed interval", r, s))
    if 13 * (K - max(CORE)) * (b - a) <= 6:
        raise ValueError("fixed references")
    margin = F(3, 28) - F(15, K) - F(4, K - 105) - F(4, 45) - F(4, 840)
    if margin != F(17, 8400):
        raise ValueError("moderate gap bound")
    length = F(1, 200)
    beta = 1 - 5 * (2 * DELTA + 7 * length)
    other_margin = beta * (length - F(1, 2 * (K - 7))) - 2 * DELTA * (2 * length + F(1, K - 105) + F(1, 840))
    if other_margin != F(364759, 2288664000):
        raise ValueError("small gap bound")
    if F(1, 5) - 44 * length / 2 < DELTA:
        raise ValueError("small gap drifts too far")
    for d in range(1, 45):
        if all(d % q == 0 for q in range(2, 6)):
            raise ValueError(("no grid", d))


def check_controls(centers, allowed):
    controls = [(1680, 1, 1), (1680, 419, 419), (1680, 420, 420), (1680, 1, 419),
                (1680, 419, 1), (1680, 60, 360), (1681, 1, 1), (10**12 + 1680, 1, 1),
                (1680, 44, 841), (1680, 45, 841), (1680, 841, 1), (1680, 1, 10**6),
                (1680, 786, 14)]
    clocks = [F(p, q) for q in range(2, 129) for p in range(1, q // 2 + 1) if gcd(p, q) == 1]
    roles = shifts = 0
    for u, a, b in controls:
        new = (u, u + a, u + a + b)
        group = (*CORE, *new)
        for r in group:
            differences = [abs(s - r) for s in group if s != r]
            if not any(all(norm(v * t) >= DELTA for v in differences) for t in clocks):
                raise ValueError(("missing direct witness", u, a, b, r))
            roles += 1
            if r in new:
                d, e = sorted(abs(s - r) for s in new if s != r)
                if e <= GAP_LIMIT:
                    bits = allowed[d] & allowed[e]
                    i = (bits & -bits).bit_length() - 1
                    t0, theta = centers[i]
                    offset = theta - r * t0
                    t = t0 + (offset - round(offset)) / r
                    if abs(t - t0) > F(1, 2 * r) or any(norm(v * t) < DELTA for v in differences):
                        raise ValueError(("shifted witness failed", u, a, b, r))
                    shifts += 1
    return roles, shifts


if __name__ == "__main__":
    check_bounds()
    centers, allowed, pairs = check_gap_pairs()
    roles, shifts = check_controls(centers, allowed)
    print(f"{len(centers)} centers cover {pairs:,} gap pairs.")
    print(f"{roles} direct role checks and {shifts} constructed-time checks passed.")
