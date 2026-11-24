"""Verify every finite witness and the bounds used for the two infinite regions."""
import argparse
import json
import lzma
from fractions import Fraction as Q
from math import ceil, floor
from pathlib import Path

FIXED = (0, 11, 13, 16, 17, 20, 28, 38, 39, 42, 43, 52, 56, 60, 63, 70)
TRANSFER = (*range(15), 105)
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


def verify_large_region(doc, cutoff, fixed=FIXED, gap_boundary=120, *, recenter=False):
    diameter = max(fixed)
    assert cutoff > diameter and gap_boundary > 0
    assert len(doc["base_intervals"]) == len(fixed)
    for r, endpoints in zip(fixed, doc["base_intervals"]):
        a, b = check_interval(r, fixed, endpoints)
        assert (cutoff-r)*7*(b-a) > 2
    length = Q(1, 2*diameter)
    assert 5*length - Q(7,cutoff) - Q(2,gap_boundary) > 0
    for d in range(1,gap_boundary):
        q = next(q for q in range(2,8) if d % q)
        # For all larger R the fixed-speed lower bound increases, and the
        # perturbation of d/q decreases. Check both bounds at the cutoff.
        shift = Q(1, q*(2*cutoff-diameter)) if recenter else Q(1, 2*q*cutoff)
        assert (cutoff-diameter)*shift >= DELTA
        assert Q(1,q) - cutoff*shift >= DELTA
        residue_distance = Q(min(d % q, -d % q),q)
        assert residue_distance - d*shift >= DELTA


def verify_transfer_control():
    x, y, q = 420, 480, 7
    assert q == next(k for k in range(2,8) if (y-x) % k)
    speeds = (*TRANSFER, x, y)

    def nearest(t):
        return min(min((s-x)*t % 1, (x-s)*t % 1) for s in speeds if s != x)

    old_time = Q(1,q) + Q(1,2*q*x)
    new_time = Q(1,q) + Q(1,q*(2*x-max(TRANSFER)))
    assert old_time == Q(841,5880) and nearest(old_time) == Q(3,56) < DELTA
    assert new_time == Q(736,5145) and nearest(new_time) == Q(3,49) > DELTA
    check_time(x, speeds, new_time)


def verify_row(row, fixed=FIXED):
    x, tail = row["x"], row["tail"]
    old = (*fixed, x)
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
        if y in fixed:
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


def verify(transfer=False):
    if not __debug__:
        raise RuntimeError("Run the checker with Python assertions enabled.")
    fixed = TRANSFER if transfer else FIXED
    path = CERTIFICATE.with_name("eighteen_transfer.json.xz") if transfer else CERTIFICATE
    doc = json.loads(lzma.decompress(path.read_bytes()))
    assert tuple(doc["fixed"]) == fixed
    cutoff = doc["large_cutoff"]
    diameter = max(fixed)
    assert cutoff >= 6*diameter
    verify_large_region(doc, cutoff, fixed, ceil(Q(12*diameter,7)))
    if transfer:
        verify_transfer_control()
        verify_large_region(doc, 4*diameter, fixed, 1 + (8*diameter)//3, recenter=True)
    rows = doc["small_rows"]
    expected = [x for x in range(1,cutoff) if x not in fixed]
    assert [row["x"] for row in rows] == expected
    pairs = sum(verify_row(row, fixed) for row in rows)
    assert pairs == doc["finite_pairs"]
    print(f"Verified {len(rows)} tails and the region x >= {cutoff}.")
    print(f"Verified all 18 roles on {pairs:,} finite pairs ({18*pairs:,} lonely times).")
    if transfer:
        print("The recentered clock also verifies the fast region x >= 420.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transfer", action="store_true", help="verify the second core")
    verify(parser.parse_args().transfer)
