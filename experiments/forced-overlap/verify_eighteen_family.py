"""Verify every finite witness and the bounds used for the two infinite regions."""
import json
import lzma
from fractions import Fraction as Q
from math import ceil, floor
from pathlib import Path

FIXED = (0, 11, 13, 16, 17, 20, 28, 38, 39, 42, 43, 52, 56, 60, 63, 70)
DELTA = Q(1, 18)
CERTIFICATE = Path(__file__).with_name("eighteen_family.json.xz")


def check_interval(reference, speeds, endpoints):
    a, b = map(Q, endpoints)
    assert 0 <= a <= b <= 1
    for speed in speeds:
        u = abs(speed - reference)
        if u:
            lap = floor(u*a)
            assert lap + DELTA <= u*a <= u*b <= lap + 1 - DELTA
    return a, b


def surviving_time(pool, u):
    """Find a lap whose closed safe band intersects the image of a stored interval."""
    for a, b in pool:
        lap = ceil(u*a - (1-DELTA))
        if lap <= floor(u*b - DELTA):
            t = max(a, (lap + DELTA) / u)
            assert a <= t <= b
            return t
    raise AssertionError(("no surviving time", u, pool))


def check_time(reference, speeds, t):
    p, q = t.as_integer_ratio()
    assert 0 <= p <= q
    for speed in speeds:
        if speed != reference:
            residue = (speed-reference)*p % q
            assert q <= 18*residue <= 17*q, (reference, speed, t)


def verify_large_region(doc, cutoff):
    assert cutoff >= 420
    assert len(doc["base_intervals"]) == len(FIXED)
    for r, endpoints in zip(FIXED, doc["base_intervals"]):
        a, b = check_interval(r, FIXED, endpoints)
        assert (cutoff-r)*7*(b-a) > 2
    length = Q(1, 2*max(FIXED))
    assert 5*length - Q(7,cutoff) - Q(2,120) > 0
    for d in range(1,120):
        q = next(q for q in range(2,8) if d % q)
        assert (1-Q(max(FIXED),cutoff)) / (2*q) >= DELTA
        residue_distance = Q(min(d % q, -d % q),q)
        assert residue_distance - Q(d,2*q*cutoff) >= DELTA


def verify_row(row):
    x, tail = row["x"], row["tail"]
    old = (*FIXED, x)
    m = max(old)
    assert tail > m and 16*tail >= 17*m
    assert len(row["intervals"]) == len(old)
    pools = []
    for r, encoded_pool in zip(old, row["intervals"]):
        pool = [check_interval(r, old, endpoints) for endpoints in encoded_pool]
        a, b = pool[0]
        assert (tail-r)*(b-a) >= 2*DELTA
        pools.append(pool)

    exceptions = iter(row["new_reference_exceptions"])
    pairs = 0
    for y in range(x+1, tail):
        if y in FIXED:
            continue
        speeds = (*old, y)
        for r, pool in zip(old, pools):
            check_time(r, speeds, surviving_time(pool, abs(y-r)))
        if y > m and 16*y >= 17*m:
            t = Q(1,2*y-m)
        else:
            t = Q(next(exceptions))
        check_time(y, speeds, t)
        pairs += 1
    assert next(exceptions, None) is None
    return pairs


def verify():
    if not __debug__:
        raise RuntimeError("Run the checker with Python assertions enabled.")
    doc = json.loads(lzma.decompress(CERTIFICATE.read_bytes()))
    assert tuple(doc["fixed"]) == FIXED
    cutoff = doc["large_cutoff"]
    verify_large_region(doc, cutoff)
    rows = doc["small_rows"]
    expected = [x for x in range(1,cutoff) if x not in FIXED]
    assert [row["x"] for row in rows] == expected
    pairs = sum(verify_row(row) for row in rows)
    assert pairs == doc["finite_pairs"]
    print(f"Verified {len(rows)} tails and the region x >= {cutoff}.")
    print(f"Verified all 18 roles on {pairs:,} finite pairs ({18*pairs:,} lonely times).")


if __name__ == "__main__":
    verify()
