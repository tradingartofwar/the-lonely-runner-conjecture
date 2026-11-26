"""Compare the clocks blocked by triples of outsiders on a prime grid."""

from collections import defaultdict
from itertools import combinations, permutations


def analyse(prime):
    def distance(speed, h):
        return min((h * speed) % prime, (-h * speed) % prime)

    core = range(1, 13)
    clocks = tuple(h for h in range(1, (prime + 1) // 2)
                   if all(16 * distance(s, h) >= prime for s in core))
    blocks = {s: {h for h in clocks if 16 * distance(s, h) < prime}
              for s in range(13, (prime + 1) // 2)}
    counts = defaultdict(lambda: [0, 0])
    for triple in combinations(blocks, 3):
        rows = [blocks[s] for s in triple]
        # Canonicalize joint pair and single counts using the same relabelling.
        key = min((len(a), len(b), len(c), len(a & b), len(a & c), len(b & c))
                  for a, b, c in permutations(rows))
        has_clock = len(set(clocks) - set.union(*rows)) > 0
        counts[key][has_clock] += 1
    triples = sum(blocked + clear for blocked, clear in counts.values())
    blocked = sum(pair[0] for pair in counts.values())
    ambiguous = sum(b + c for b, c in counts.values() if b and c)
    if prime == 73:
        assert clocks == (5, 17, 26, 28, 34)
        assert [blocks[s] for s in (15, 28, 13)] == [{5, 34}, {26, 34}, {17, 28, 34}]
        assert blocks[17] == {17, 26}
        assert 16 * min(distance(s, 5) for s in (*core, 17, 28, 13)) > prime
    return len(clocks), triples, blocked, ambiguous


if __name__ == "__main__":
    expected = {73: (5, 2024, 51, 6), 79: (7, 2925, 2, 0), 83: (2, 3654, 746, 0),
                89: (3, 4960, 220, 0), 97: (4, 7140, 843, 0)}
    for prime, row in expected.items():
        observed = analyse(prime)
        assert observed == row
        print(prime, observed)

