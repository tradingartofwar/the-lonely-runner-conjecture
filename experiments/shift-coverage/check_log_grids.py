"""Reproduce the initial 16-runner prime-grid counts. Standard library only."""

from collections import defaultdict
from math import comb, gcd


def prime_grid_masks(p):
    """Blocked nonzero times, up to sign, indexed by the speed modulo p up to sign."""
    m = (p - 1) // 2
    return [
        sum(1 << (t - 1) for t in range(1, m + 1)
            if 16 * min(v * t % p, -v * t % p) < p)
        for v in range(1, m + 1)
    ]


def histogram_from_times(p):
    """Count supports by testing their union of blocked times on the original grid."""
    masks = prime_grid_masks(p)
    m = len(masks)
    full = (1 << m) - 1
    suffix = [0] * (m + 1)
    for j in reversed(range(m)):
        suffix[j] = suffix[j + 1] | masks[j]
    hist = [0] * 16

    def visit(j, used, blocked):
        if blocked == full:
            for extra in range(1 + min(15 - used, m - j)):
                hist[used + extra] += comb(m - j, extra)
        elif j < m and used < 15 and blocked | suffix[j] == full:
            visit(j + 1, used + 1, blocked | masks[j])
            visit(j + 1, used, blocked)

    visit(0, 0, 0)
    return hist


def log_stencil(p):
    """Shortest cyclic interval containing the logs, over every generator and shift."""
    m = (p - 1) // 2
    for generator in range(2, p):
        logs = {}
        residue = 1
        while min(residue, p - residue) not in logs:
            logs[min(residue, p - residue)] = len(logs)
            residue = residue * generator % p
        if len(logs) == m:
            break
    labels = [logs[v] for v in range(1, (p - 1) // 16 + 1)]
    best = None
    for scale in range(1, m):
        if gcd(scale, m) != 1:
            continue
        residues = sorted(scale * value % m for value in labels)
        for i, start in enumerate(residues):
            width = (residues[i - 1] - start) % m
            if best is None or width <= best[-1]:
                trial = sorted((x - start) % m for x in residues)
                if best is None or (width, trial) < (best[-1], best):
                    best = trial
    return best


def histogram_from_logs(p):
    """Trace a transfer matrix for circular occupied/missing unsigned speed classes."""
    stencil = log_stencil(p)
    width = stencil[-1]
    if not width:
        raise ValueError("This checker expects at least two blocked residue classes.")
    required = sum(1 << t for t in stencil)
    m = (p - 1) // 2
    context_count = 1 << width
    hist = [0] * 16
    # Cyclic words on labelled sites correspond to closed walks from their first context.
    for initial in range(context_count):
        counts = {(initial, 0): 1}
        for _ in range(m):
            following = defaultdict(int)
            for (context, occupied), count in counts.items():
                for bit in (0, 1):
                    window = 2 * context + bit
                    if window & required and occupied + bit <= 15:
                        following[window % context_count, occupied + bit] += count
            counts = following
        for occupied in range(16):
            hist[occupied] += counts.get((initial, occupied), 0)
    return stencil, hist


def main():
    for p, expected_minimum in ((37, 9), (41, 10), (43, 12), (47, 12), (53, 11), (59, 12), (61, 12)):
        stencil, hist = histogram_from_logs(p)
        assert hist == histogram_from_times(p)
        multisets = sum(count * comb(14, size - 1)
                        for size, count in enumerate(hist) if count)
        minimum = next(size for size, count in enumerate(hist) if count)
        assert minimum == expected_minimum
        print(p, tuple(stencil), sum(hist), multisets, minimum)


if __name__ == "__main__":
    main()
