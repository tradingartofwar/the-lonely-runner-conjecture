"""Constant-size endpoint certificate for q, q+8, 2q+1 and arbitrary v>=q.

No project imports. The certificate itself has six affine bands, irrespective
of speed. Direct finite partitions below are verification, not its algorithm.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
J = (F(9, 32), F(3, 8))
L = J[1]-J[0]
CORE = (1, 4, 5)
AREA = F(41, 3840)
TAIL = 179

# Each row is (time interval, affine lower x boundary, affine upper x boundary).
# x=w*t-j; affine functions are stored as (slope, intercept).
BANDS = {
    "q_B": ((J, (F(0), -D), (F(-1, 2), F(1, 16))),),
    "q_A": (((F(11, 32), J[1]), (F(-8), F(23, 8)), (F(0), D)),),
    "A_B": (
        ((J[0], F(7, 24)), (F(15, 2), F(-33, 16)), (F(0), D)),
        ((F(37, 120), F(13, 40)), (F(0), -D), (F(15, 2), F(-39, 16))),
        ((F(13, 40), F(41, 120)), (F(15, 2), F(-41, 16)), (F(15, 2), F(-39, 16))),
        ((F(41, 120), F(43, 120)), (F(15, 2), F(-41, 16)), (F(0), D)),
    ),
}


def floor(x):
    return x.numerator//x.denominator


def distance(x):
    p = x % 1
    return min(p, 1-p)


def primitive(z):
    z += D
    k = floor(z)
    return F(k, 4)+min(z-k, F(1, 4))


def duration(v):
    return (primitive(v*J[1])-primitive(v*J[0]))/v


def phi(z):
    f = z % 1
    return f*(f-1)/2


def band_area(interval, lo, hi):
    a, b = interval
    return (hi[0]-lo[0])*(b*b-a*a)/2+(hi[1]-lo[1])*(b-a)


def endpoint_term(w, affine, interval):
    s, o = affine
    a, b = interval
    frequency = w-s
    assert frequency > 0
    return (phi(frequency*b-o)-phi(frequency*a-o))/frequency


def pair(w, key):
    return sum((band_area(interval, lo, hi)+endpoint_term(w, hi, interval)-endpoint_term(w, lo, interval)
                for interval, lo, hi in BANDS[key]), F(0))


def certificate(q, v=None):
    assert isinstance(q, int) and q >= 6 and q != 7
    A, B = q+8, 2*q+1
    singles = [duration(w) for w in (q, A, B)]
    pairs = [pair(q, "q_B"), pair(q, "q_A"), pair(A, "A_B")]
    excess_base = 3*L/4-sum(singles)-F(3, 16*q)
    lower = excess_base+sum(pairs)
    coarse = AREA-F(5, 8*q)-F(11, 16*A)-F(19, 16*B)
    simpler = AREA-F(61, 32*q)
    assert lower >= coarse >= simpler
    result = {"q": q, "fixed_extras": [q, A, B], "single_durations": singles,
              "pair_order": ["q_B", "q_A", "A_B"], "pair_durations": pairs,
              "uniform_triangle_bound": lower, "uniform_near_pair_bound": excess_base+pairs[0],
              "uniform_best_fixed_pair_bound": excess_base+max(pairs),
              "coarse_tail_bound": coarse, "simple_tail_bound": simpler}
    if v is not None:
        assert isinstance(v, int) and v >= q and v not in (q, A, B)
        exact_v = L-sum(singles)-duration(v)+sum(pairs)
        assert exact_v >= lower
        result.update({"v": v, "triangle_bound_with_exact_v_duration": exact_v})
    return result


def phase_partition(speeds):
    """Separately evaluates phase inequalities on all finite boundary cells."""
    points = set(J)
    for v in (*CORE, *speeds):
        for m in range(floor(v*J[0])-1, floor(v*J[1])+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if J[0] < t < J[1]:
                    points.add(t)
    points = sorted(points)
    states = [F(0) for _ in range(1 << len(speeds))]
    clear_cells = []
    for a, b in zip(points, points[1:]):
        t = (a+b)/2
        assert all(distance(v*t) >= D for v in CORE)
        s = sum(1 << i for i, v in enumerate(speeds) if distance(v*t) < D)
        states[s] += b-a
        if s == 0:
            clear_cells.append([a, b])
    moments = {s: sum(z for k, z in enumerate(states) if k & s == s) for s in range(len(states))}
    boundaries = [t for t in points if all(distance(v*t) >= D for v in (*CORE, *speeds))]
    return {"states": states, "moments": moments, "clear_cells": clear_cells, "valid_boundaries": boundaries}


def derive_bands(multiplier, residual):
    """Reconstruct vertical pair strips from integer labels, independently of q."""
    lo_k = min(residual*J[0], residual*J[1])-(multiplier+1)*D
    hi_k = max(residual*J[0], residual*J[1])+(multiplier+1)*D
    answer = []
    for k in range(floor(lo_k)-1, floor(hi_k)+2):
        low = (F(-residual, multiplier), (k-D)/multiplier)
        high = (F(-residual, multiplier), (k+D)/multiplier)
        lines = ((F(0), -D), (F(0), D), low, high)
        points = set(J)
        for (s, o), (ss, oo) in combinations(lines, 2):
            if s != ss:
                t = (oo-o)/(s-ss)
                if J[0] < t < J[1]:
                    points.add(t)
        points = sorted(points)
        for a, b in zip(points, points[1:]):
            t = (a+b)/2
            evaluate = lambda line: line[0]*t+line[1]
            lo = max((lines[0], low), key=evaluate)
            hi = min((lines[1], high), key=evaluate)
            if evaluate(lo) < evaluate(hi):
                answer.append(((a, b), lo, hi))
    return tuple(sorted(answer))


def verify_merged_AB_terms(A):
    terms = (
        (1, (F(0), D), (J[0], F(7, 24))),
        (-1, (F(0), -D), (F(37, 120), F(13, 40))),
        (1, (F(0), D), (F(41, 120), F(43, 120))),
        (-1, (F(15, 2), F(-33, 16)), (J[0], F(7, 24))),
        (1, (F(15, 2), F(-39, 16)), (F(37, 120), F(41, 120))),
        (-1, (F(15, 2), F(-41, 16)), (F(13, 40), F(43, 120))),
    )
    error = sum(sign*endpoint_term(A, affine, interval) for sign, affine, interval in terms)
    assert error == pair(A, "A_B")-F(281, 61440)
    B = 2*A-15
    assert abs(error) <= F(3, 8*A)+F(3, 4*B)


def main():
    for v in CORE:
        cell = floor(v*J[0])
        assert D <= v*J[0]-cell <= v*J[1]-cell <= 1-D
    for key, multiplier, residual, area in (("q_B", 2, 1, F(9, 4096)),
                                           ("q_A", 1, 8, F(1, 256)),
                                           ("A_B", 2, -15, F(281, 61440))):
        assert derive_bands(multiplier, residual) == tuple(sorted(BANDS[key]))
        assert sum(band_area(*row) for row in BANDS[key]) == area
    assert F(9, 4096)+F(1, 256)+F(281, 61440) == AREA
    # q/B blocking imposes -D<x<D/2-t/2. The q+8 phase x+8t
    # lies strictly between 17/8 and 23/8 over J, so its fractional part is safe.
    assert 8*J[0]-D == F(17, 8)
    assert F(15, 2)*J[1]+D/2 == F(23, 8)
    assert -2*D+J[0] == F(1, 32) and 2*D+J[1] == F(5, 8)
    assert AREA-F(61, 32*TAIL) == F(19, 687360) > 0

    rows = []
    bad = []
    for q in range(6, TAIL):
        if q == 7:
            continue
        cert = certificate(q)
        direct = phase_partition((q, q+8, 2*q+1))
        m = direct["moments"]
        assert cert["single_durations"] == [m[1], m[2], m[4]]
        assert cert["pair_durations"] == [m[5], m[3], m[6]]
        assert m[7] == 0
        assert L-sum(cert["single_durations"])+sum(cert["pair_durations"]) == m[0]-sum(direct["states"][1:])
        assert abs(cert["pair_durations"][0]-F(9, 4096)) <= F(1, 8*q)+F(1, 4*(2*q+1))
        assert abs(cert["pair_durations"][1]-F(1, 256)) <= F(1, 8*q)+F(1, 8*(q+8))
        verify_merged_AB_terms(q+8)
        if cert["uniform_triangle_bound"] <= 0:
            bad.append(q)
        rows.append([q, *cert["single_durations"], *cert["pair_durations"],
                     cert["uniform_triangle_bound"], cert["uniform_near_pair_bound"],
                     cert["uniform_best_fixed_pair_bound"]])
    assert len(rows) == 172
    assert bad == [6, 8, 9, 11, 12, 13, 14, 15, 17, 20, 24, 27]
    assert all(row[7] > 0 for row in rows if row[0] >= 28)

    controls = []
    for q, v in ((6, 30), (27, 43), (28, 44), (28, 29), (28, 1000), (56, 72), (178, 194), (179, 195)):
        cert = certificate(q, v)
        d = phase_partition((q, q+8, 2*q+1, v))
        m = d["moments"]
        base = L-sum(m[1 << i] for i in range(4))
        best_pair = base+max(m[(1 << i) | (1 << j)] for i, j in combinations(range(4), 2))
        triangle = base+m[3]+m[5]+m[6]
        assert m[7] == m[15] == 0
        assert triangle == cert["triangle_bound_with_exact_v_duration"] <= d["states"][0]
        controls.append({**cert, "best_of_six_exact_one_pair_bounds": best_pair,
                         "clear_duration": d["states"][0], "direct": d})
    control = controls[1]
    assert control["best_of_six_exact_one_pair_bounds"] == F(-1777, 893970) < 0
    assert control["triangle_bound_with_exact_v_duration"] == F(2923, 595980) > 0
    assert control["clear_duration"] == F(31309, 1787940)
    assert controls[2]["uniform_triangle_bound"] == F(587, 153216)

    # Adjacent offsets do not inherit the q+8 exclusion.
    adjacent = []
    for offset in (7, 9):
        d = phase_partition((56, 56+offset, 113))
        assert d["moments"][7] > 0
        adjacent.append({"offset": offset, "speeds": [56, 56+offset, 113], "triple_duration": d["moments"][7]})
    huge = [certificate(q, v) for q, v in ((10**12, 10**12+16), (10**12, 10**24+7), (28, 10**40))]
    assert all(c["uniform_triangle_bound"] > 0 for c in huge)
    result = {"date": "2026-09-25", "research_baseline": "59c00ff4e3dea25c0bfd4c47b8ea284dce753034",
              "status": "Unbounded certificate argument awaiting independent review; finite checks are not its unbounded justification; no novelty claim.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "core": CORE, "window": J, "threshold": D, "bands": BANDS, "total_pair_area": AREA,
              "analytic_tail_start": TAIL, "uniform_cutoff": 28,
              "finite_columns": ["q", "D_q", "D_A", "D_B", "O_qB", "O_qA", "O_AB", "H_triangle", "H_near_pair", "H_best_fixed_pair"],
              "finite_rows": rows, "nonpositive_uniform_q_below_tail": bad,
              "controls": controls, "adjacent_offset_controls": adjacent, "large_formula_controls": huge,
              "limits": "Distinct common-start speeds, selected reference 0; q>=28 and arbitrary integer v>=q outside {q,q+8,2q+1}. Six fixed bands give the certificate; finite partitions verify it. No arbitrary-offset or all-reference conclusion."}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("uniform_triangle.json").read_text())
        print("PASS: six affine bands, 172 finite q values, eight four-blocker controls, two offset countercontrols, three large formula controls.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
