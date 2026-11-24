"""Test baseline compatibility and an explicit common relation at two lifted grids."""

from collections import Counter
from math import lcm
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "proof-survivors"))
from binary_lifts import descendants


def fourth_doubling(prime):
    rows = [tuple(range(1, 16))]
    for level in (1, 2, 4, 8):
        rows = descendants(rows, prime * level, 16)
    assert len(rows) == 64
    for row in rows:
        assert sorted(v % 16 == 0 for v in row) == [False]*2 + [True]*13
        assert (row[0] + row[1] - row[2]) % (16 * prime) == 0
        assert all(v % 16 == 0 for v in row[:3])
    return rows


def fingerprint(row):
    # All thirteen zeros match, leaving the unordered signed pair of odd residues.
    def form(u):
        return tuple(sorted(min((u*v) % 16, (-u*v) % 16) for v in row if v % 16))
    return min(form(u) for u in range(1, 16, 2))


def verify_pair(left, right):
    # Preserve positions 1,2,3 and permute only the remaining core/exceptions.
    p, q = 97, 101
    left_odd = [v for v in left if v % 16]
    right_odd = [v for v in right if v % 16]
    for u in range(1,16,2):
        for ordered in (right_odd, right_odd[::-1]):
            for a in (1,-1):
                for b in (1,-1):
                    odd = [a*u*ordered[0], b*u*ordered[1]]
                    if any((x-y)%16 for x,y in zip(left_odd,odd)):
                        continue
                    # u is coprime to 16*q. Each of the 13 core labels reduces to zero.
                    lc = [v for v in left if v % 16 == 0]
                    rc = [u*v for v in right if v % 16 == 0]
                    joined = []
                    for x,y in zip(lc+left_odd,rc+odd):
                        assert (x-y)%16 == 0
                        w = x + 16*p * (((y-x)//16) * pow(p,-1,q) % q)
                        assert (w-x) % (16*p) == 0 and (w-y) % (16*q) == 0
                        joined.append(w)
                    assert (joined[0]+joined[1]-joined[2]) % lcm(16*p,16*q) == 0
                    return True
    return False


if __name__ == "__main__":
    left, right = fourth_doubling(97), fourth_doubling(101)
    print("mod-16 type counts:", Counter(map(fingerprint, left)), Counter(map(fingerprint, right)))
    tally = Counter()
    for x in left:
        for y in right:
            can_match = fingerprint(x) == fingerprint(y)
            has_triple = verify_pair(x,y)
            assert can_match == has_triple
            tally[can_match,has_triple] += 1
    assert tally == {(False, False): 2560, (True, True): 1536}
    print("aligned, triple:", sorted(tally.items()))
