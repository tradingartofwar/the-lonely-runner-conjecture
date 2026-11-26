"""Classify all 16 roles after two replacements of speeds in 1..15.

Take any two omissions and insert 16 <= v < w. The adjacent two-swap checker
justifies the two variable-speed tail used after subtracting the old root.

A new root R >= 61 has a direct proof. Let d=w-v. When d >= 60, use
0 <= t <= 1/30: all old phases lie in [0,1/2]. A strict root phase in
(9/16,15/16) protects every old runner. It occupies at least
(3/8)(1/30-1/R) time. The other runner blocks at most (1/8)(1/30+1/d).
The difference is positive because 1/15 > 3/61 + 1/60. For d <= 59 choose
q in {2,3,4,5} with q not dividing d; their least common multiple is 60.
At t=1/q+1/(2qR) the phase of each gap R-s to an old runner s is displaced
from its original q-grid point by a number in [(1-15/R)/(2q), 1/(2q)].
This guarantees clearance >1/16. The other new runner has distance at least
(1-d/(2R))/q > 1/16. Each root can use its own time. Positive time found
at larger R needs no search. The finite-range code supports equality contacts.
"""
from fractions import Fraction as F
from functools import cache
from itertools import combinations
from math import ceil, floor, gcd
from lr_two_swap import safe_intervals, intersect, boundary_witness
from lr_one_swap import single_speed_leaves_window


DELTA = F(1, 16)


@cache
def windows(gaps):
    result = ((F(0), F(1)),)
    for gap in gaps:
        result = intersect(result, safe_intervals(gap, DELTA))
    return result


def width(intervals):
    return max(b - a for a, b in intervals)


def remaining_type(intervals, core, final):
    if single_speed_leaves_window(intervals, final, DELTA):
        return 'strict'
    return 'equality' if boundary_witness((*core, final), DELTA) is not None else 'below'


def check_remaining(final_low, intervals, core):
    for final in range(final_low, floor(2 * DELTA / width(intervals)) + 1):
        status = remaining_type(intervals, core, final)
        if status != 'strict':
            yield final, status


def old_roles(missing, old):
    # In the reference frame of any old root, the two new runners are still
    # faster than it. Apply the exact same measure and width arguments used at zero.
    for root in old:
        gaps = tuple(sorted({abs(s - root) for s in old if s != root}))
        base = windows(gaps)
        for v in range(16 - root, ceil(1 / (3 * width(base)))):
            narrowed = intersect(base, safe_intervals(v, DELTA))
            for w, kind in check_remaining(v + 1, narrowed, (*gaps, v)):
                yield root, root + v, root + w, kind


def fast_controls():
    # For 17<=R<=60, initially keep all sixteen old speeds even if two will
    # later be deleted. The first-lap interval is nonempty in this range.
    needs_actual_core = []
    for root in range(17, 61):
        intervals = ((DELTA / (root - 15), (1 - DELTA) / root),)
        gaps = tuple(range(root - 15, root + 1))
        last = floor(2 * DELTA / width(intervals))
        for d in range(1, last + 1):
            if not single_speed_leaves_window(intervals, d, DELTA):
                if not single_speed_leaves_window(windows(gaps), d, DELTA):
                    needs_actual_core.append((root, d))
    assert needs_actual_core == [(17, 1)]
    return needs_actual_core


def new_roles(missing, old, needs_actual_core):
    # R=16 can only be the slower newcomer. R=17 can be either newcomer,
    # and absolute relative gap 1 means the other runner is 16 or 18.
    root = 16
    gaps = tuple(sorted(root - s for s in old))
    for d, status in check_remaining(1, windows(gaps), gaps):
        yield root, root, root + d, status
    for root, d in needs_actual_core:
        gaps = tuple(sorted(root - s for s in old))
        status = remaining_type(windows(gaps), gaps, d)
        if status != 'strict':
            for other in (root - d, root + d):
                yield root, min(root, other), max(root, other), status


def cross_check_small_lineups():
    """Use rational clock masks independently of the interval and tail tests."""
    maximum = 30
    clocks = [(p, q) for q in range(2, 2 * maximum + 1)
              for p in range(1, q // 2 + 1) if gcd(p, q) == 1]
    strict_masks = []
    for gap in range(maximum + 1):
        mask = sum(1 << i for i, (p, q) in enumerate(clocks)
                   if 16 * min(gap*p % q, -gap*p % q) > q)
        strict_masks.append(mask)

    full = (1 << len(clocks)) - 1
    strict = equal = 0
    for omitted in combinations(range(1, 16), 2):
        retained = [s for s in range(16) if s not in omitted]
        for x, y in combinations(range(16, maximum + 1), 2):
            speeds = [*retained, x, y]
            for root in speeds:
                gaps = {abs(v - root) for v in speeds if v != root}
                surviving = full
                for gap in gaps:
                    surviving &= strict_masks[gap]
                if surviving:
                    strict += 1
                else:
                    # Consecutive gaps certify equality over all real times.
                    assert gaps == set(range(1, 16))
                    equal += 1
    assert (strict, equal) == (176279, 121)
    print(f"Independent finite replay: {strict:,} strict roles and {equal} equality roles.")


def main():
    cross_check_small_lineups()
    required = fast_controls()
    equality = []
    below = []
    for missing in combinations(range(1, 16), 2):
        old = tuple(v for v in range(16) if v not in missing)
        records = (*old_roles(missing, old), *new_roles(missing, old, required))
        for root, v, w, kind in records:
            rec = missing, root, v, w
            if kind == 'below':
                below.append(rec)
            else:
                equality.append(rec)
    print(len(equality), 'equality-only roles;', len(below), 'below-threshold roles.')
    nonconsecutive = sum(
        {abs(s-root) for s in (*[i for i in range(16) if i not in omitted], v, w) if s != root} != set(range(1, 16))
        for omitted, root, v, w in equality)
    print('Nonconsecutive equality patterns:', nonconsecutive)
    print('Equality roots:', sorted({row[1] for row in equality}))
    print('Strictly subthreshold:', below)
    assert len(equality) == 121 and not below and not nonconsecutive
    assert ((5, 6), 15, 24, 25) in equality


if __name__ == '__main__':
    main()
