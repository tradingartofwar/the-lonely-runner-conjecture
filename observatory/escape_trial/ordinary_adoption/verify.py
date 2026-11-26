"""Reproduce both policies from physical subset speeds and check the timing ledger."""

import json
import math
from fractions import Fraction
from itertools import combinations

from measure import HERE, KINDS, encoded, load_panel, paired_record, summarize

DELTA = Fraction(1, 16)
CLOCKS = range(2, 17)


def physical(weights):
    return sorted(sum(members) for count in range(1, 5) for members in combinations(weights, count))


def first_arc(speeds):
    colliders = {}
    for q in CLOCKS:
        hits = [speed for speed in speeds if speed % q == 0]
        if not hits:
            return Fraction(1, q)
        colliders[q] = min(hits)
    for q, minimum in colliders.items():
        for direction in (1, -1):
            scale = 16*q*minimum
            if all(scale <= 16*(16*minimum*((direction*v) % q) + q*v) <= 15*scale for v in speeds):
                return Fraction(1, q) + direction*DELTA/minimum
    return None


def physical_clearance(speeds, time):
    if time is None:
        return None
    distance = min(abs(v*time-round(v*time)) for v in speeds)
    return distance.numerator, distance.denominator


def bounded_endpoint(speeds, q):
    collisions = [v for v in speeds if v % q == 0]
    if not collisions:
        return None
    step = DELTA/min(collisions)
    groups = [[v for v in speeds if v % q == r] for r in range(q)]
    for sign in (1, -1):
        bounded = True
        for residue, members in enumerate(groups):
            if not members:
                continue
            phase = Fraction((sign*residue) % q, q)
            low = phase + members[0]*step
            high = phase + members[-1]*step
            windows = math.ceil(high+DELTA)-math.floor(low-DELTA)-1
            if windows > 4:
                bounded = False
                break
        if bounded:
            t = Fraction(1, q) + sign*step
            distance, scale = physical_clearance(speeds, t)
            if 16*distance >= scale:
                return t
    return None


def switch_to_seven(speeds):
    zero = [v for v in speeds if v % 4 == 0]
    smallest = min(zero)
    if any(abs(v-16*smallest) < smallest for v in zero):
        return True
    for center in (4*smallest, 12*smallest):
        odd = {v % 4 for v in speeds if abs(v-center) < smallest and v % 2}
        if odd == {1, 3}:
            return True
    return False


def compare(weights):
    speeds = physical(weights)
    t = first_arc(speeds)
    for q in (3, 5):
        if t is not None:
            break
        t = bounded_endpoint(speeds, q)
    if t is not None:
        return paired_record(weights, (t, t), None, speeds, physical_clearance)
    choice = 7 if switch_to_seven(speeds) else 4
    fixed = bounded_endpoint(speeds, 4)
    if choice == 7:
        step = DELTA/min(v for v in speeds if v % 4 == 0)
        for sign in (1, -1):
            numerator, denominator = physical_clearance(speeds, Fraction(1, 4) + sign*step)
            assert 16*numerator < denominator, weights
    candidate = bounded_endpoint(speeds, 7) if choice == 7 else fixed
    return paired_record(weights, (fixed, candidate), choice, speeds, physical_clearance)


def timing_check(payload, panel_hash, ordinary_count, eligible_count):
    assert payload["panel_sha256"] == panel_hash
    ordinary = payload["modes"]["ordinary"]
    starts = list(range(0, ordinary_count, 4096))
    assert [(x["round"],x["start"],x["rows"]) for x in ordinary] == [
        (i,start,min(4096,ordinary_count-start)) for i in range(3) for start in starts
    ]
    final = payload["modes"]["eligible"]
    assert [(x["round"],x["rows"],x["repetitions"]) for x in final] == [
        (i,eligible_count,32) for i in range(9) if eligible_count
    ]
    for mode, rows in payload["modes"].items():
        for x in rows:
            parity = x["round"] + (x["start"]//4096 if mode == "ordinary" else 0)
            assert x["order"] == list(KINDS if parity%2 == 0 else KINDS[::-1])
            assert all(type(x[k][clock]) is int and x[k][clock] > 0 for k in KINDS for clock in ("wall_ns","cpu_ns"))


if __name__ == "__main__":
    panel_hash, bands = load_panel()
    result = dict(panel_sha256=panel_hash, **summarize(bands, compare))
    assert encoded(result) == (HERE/"results.json").read_bytes(), "Independent exact result differs"
    timing_check(json.loads((HERE/"timing.json").read_bytes()), panel_hash,
                 result["total"]["ordinary"], result["total"]["eligible"])
    import sys
    sys.stdout.buffer.write(encoded(result))
