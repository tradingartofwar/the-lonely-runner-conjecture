"""Check the 13-runner residual seed lists in the original archived text logs."""

from collections import defaultdict
from math import isqrt
from pathlib import Path
import re
import sys


def check(log_folder):
    # Table 1, k=12, in Sungkawichai and Trakulthongchai.
    primes = {p for p in range(167, 734) if p != 173
              and all(p % f for f in range(2, isqrt(p) + 1))}
    seen = defaultdict(set)
    for path in sorted(log_folder.iterdir()):
        if not path.is_file():
            continue
        prime = None
        for line in path.read_text().splitlines():
            match = re.search(r"Parameters:\s*p\s*=\s*(\d+),\s*k\s*=\s*(\d+)", line)
            if match:
                prime = int(match[1]) if int(match[2]) == 12 else None
            if "seeds:" in line and prime in primes:
                for group in re.findall(r"\(([\d\s]+)\)", line):
                    seed = tuple(sorted(map(int, group.split())))
                    assert len(seed) == 12
                    seen[prime].add(seed)

    assert set(seen) == primes
    for prime, seeds in seen.items():
        def representative(value):
            residue = value % prime
            return min(residue, prime - residue)

        orbit = {tuple(sorted(representative(a * i) for i in range(1, 13)))
                 for a in range(1, prime)}
        assert len(seeds) == 12 and seeds <= orbit
    print(f"{len(primes)} primes; {sum(map(len, seen.values()))} archived seeds match.")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
