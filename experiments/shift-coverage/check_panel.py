"""Selected four-prime panel with a zero-count control. Reuse the adjacent binary lift checker."""
from math import gcd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "proof-survivors"))
from binary_lifts import descendants


def strict_shift(speeds, divisor):
    n = 1 + len(speeds)
    if not any(v % divisor == 0 for v in speeds):
        return False
    blocked = 0
    for v in speeds:
        if v % divisor:
            multiplicity = gcd(v, divisor)
            order = divisor // multiplicity
            blocked += multiplicity * ((2 * order + n - 1) // n)
    return blocked < divisor


expected = {83: (2112, 768), 89: (128, 0), 97: (64, 0), 101: (64, 0), 103: (0, 0)}
for prime, (expected_raw, after_four) in expected.items():
    parents = [tuple(range(1, 16))]
    for level in (1, 2, 4, 8):
        parents = descendants(parents, level * prime, 16)
    raw = len(parents)
    counts = []
    for divisor in (2, 4, 8, 16):
        parents = [w for w in parents if not strict_shift(w, divisor)]
        counts.append(len(parents))
    print(prime, raw, *counts, flush=True)
    assert raw == expected_raw and counts == [raw, after_four, 0, 0]
