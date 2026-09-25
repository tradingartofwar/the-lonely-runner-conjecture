"""Two-speed sparse certificates and a prescribed two-window selector.

Standard library only. --check reproduces the archived JSON. Finite partitions
verify stated finite domains; the unbounded implications are in the note.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
CORE = (1, 4, 5, 6, 7)
J = (F(9, 32), F(3, 8))
H = (F(25, 56), F(15, 32))
I6 = (F(5, 16), F(17, 48))
I7 = (J[0], F(17, 56))
D6, D7 = I6[1]-I6[0], I7[1]-I7[0]
ZERO_PAIRS = ((2, 3), (10, 11), (11, 13), (11, 26))


def floor(x):
    return x.numerator//x.denominator


def ceil(x):
    return -floor(-x)


def distance(x):
    p = x % 1
    return min(p, 1-p)


def primitive(x):
    y = x+D
    return F(floor(y), 4)+min(y-floor(y), F(1, 4))


def blocked(v, window):
    a, b = window
    return (primitive(v*b)-primitive(v*a))/v


def laps(v, window):
    a, b = window
    return range(floor(v*a-D)+1, ceil(v*b+D))


def occurrences(v, window):
    a, b = window
    return [(max(a, (m-D)/v), min(b, (m+D)/v)) for m in laps(v, window)]


def pair_duration(x, y, window):
    assert x < y
    return sum((blocked(y, interval) for interval in occurrences(x, window)), F(0))


def lattice_witness(x, y, window):
    """Find integer lap labels using pairwise interval compatibility.

    No time partition or enumeration of y's laps is used.
    """
    a, b = window
    for m in laps(x, window):
        lower = max(y*a-D, (y*m-D*(x+y))/x)
        upper = min(y*b+D, (y*m+D*(x+y))/x)
        n = floor(lower)+1
        if n < upper:
            assert abs(y*m-x*n) < D*(x+y)
            left = max(a, (m-D)/x, (n-D)/y)
            right = min(b, (m+D)/x, (n+D)/y)
            assert left < right
            return {"laps": [m, n], "intersection_endpoints": [left, right]}
    return None


def masks(h6, h7):
    for mask in range(32):
        if h6 and mask & 19 == 19:
            continue
        if h7 and mask & 28 == 28:
            continue
        yield mask


def graph_count_check(x, y, mask, h6, h7):
    edges = ((6, x), (6, y), (7, x), (7, y), (x, y))
    for bits in range(16):
        state = {v for i, v in enumerate((6, 7, x, y)) if bits >> i & 1}
        if {6, 7} <= state:
            continue
        if not h6 and {6, x, y} <= state:
            continue
        if not h7 and {7, x, y} <= state:
            continue
        e = sum(bool(mask >> i & 1) and set(edge) <= state for i, edge in enumerate(edges))
        assert 1-len(state)+e <= int(not state)


def sparse(x, y):
    assert 0 < x < y and x not in CORE and y not in CORE
    wx = blocked(x, J)
    weights = [blocked(x, I6), blocked(y, I6), blocked(x, I7),
               blocked(y, I7), pair_duration(x, y, J)]
    w6, w7 = lattice_witness(x, y, I6), lattice_witness(x, y, I7)
    h6, h7 = w6 is not None, w7 is not None
    if h6 and h7:
        loss = min(weights[4], min(weights[:2])+min(weights[2:4]))
    elif h6:
        loss = min(weights[0], weights[1], weights[4])
    elif h7:
        loss = min(weights[2], weights[3], weights[4])
    else:
        loss = F(0)
    choices = [(sum((z for i, z in enumerate(weights) if mask >> i & 1), F(0)),
                -mask.bit_count(), -mask) for mask in masks(h6, h7)]
    weight, _, neg_mask = max(choices)
    mask = -neg_mask
    assert weight == sum(weights)-loss
    graph_count_check(x, y, mask, h6, h7)
    base = J[1]-J[0]-D6-D7-wx-blocked(y, J)
    lower = base+weight
    bipartite = base+sum(weights[:4])
    assert lower >= bipartite
    return {"pair": [x, y], "triple_flags": [h6, h7], "graph_mask": mask,
            "clear_lower_bound": lower, "pair_weights": weights,
            "lattice_witnesses": [w6, w7], "bipartite_lower_bound": bipartite,
            "smaller_speed_occurrences_in_J": len(laps(x, J))}


def direct(x, y, window=J):
    speeds = (*CORE, x, y)
    points = set(window)
    for v in speeds:
        for m in range(floor(v*window[0])-1, floor(v*window[1])+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if window[0] < t < window[1]:
                    points.add(t)
    points = sorted(points)
    clear = F(0)
    triple = [F(0), F(0)]
    pair = F(0)
    clear_cells = []
    for a, b in zip(points, points[1:]):
        t = (a+b)/2
        bad = {v for v in speeds if distance(v*t) < D}
        if not bad:
            clear += b-a
            clear_cells.append([a, b])
        for i, v in enumerate((6, 7)):
            if {v, x, y} <= bad:
                triple[i] += b-a
        if {x, y} <= bad:
            pair += b-a
    valid = [t for t in points if all(distance(v*t) >= D for v in speeds)]
    return {"clear_duration": clear, "triple_durations": triple,
            "pair_duration": pair, "valid_boundaries": valid, "clear_cells": clear_cells}


def checked_case(x, y):
    s, d = sparse(x, y), direct(x, y)
    assert s["clear_lower_bound"] <= d["clear_duration"]
    assert s["triple_flags"] == [t > 0 for t in d["triple_durations"]]
    assert s["pair_weights"][4] == d["pair_duration"]
    return s, d


def tail_profile(x):
    """A fixed conservative graph valid for all y, with L_x-C_x/y bound."""
    dx = blocked(x, J)
    a, c = blocked(x, I6), blocked(x, I7)
    k = len(laps(x, J))
    weights = (a, D6/4, c, D7/4, dx/4)
    base = F(3, 4)*(J[1]-J[0])-D6-D7-dx
    choices = []
    for mask in masks(a > 0, c > 0):
        limit = base+sum((z for i, z in enumerate(weights) if mask >> i & 1), F(0))
        if limit <= 0:
            continue
        coefficient = F(3, 16)*(1+bool(mask & 2)+bool(mask & 8)+k*bool(mask & 16))
        cutoff = floor(coefficient/limit)+1
        choices.append((cutoff, -limit, mask, coefficient))
    cutoff, neg_limit, mask, coefficient = min(choices)
    assert -neg_limit-coefficient/cutoff > 0
    return {"x": x, "cutoff_y": cutoff, "limit_L": -neg_limit,
            "error_C": coefficient, "fixed_graph_mask": mask, "occurrence_count": k}


def select_certificate(x, y):
    assert 0 < x < y and x not in CORE and y not in CORE
    if x >= 34:
        lower = (H[1]-H[0])/2-F(3, 16)*(F(1, x)+F(1, y))
        assert lower > 0
        return {"pair": [x, y], "window": H, "method": "fast individual-duration bound",
                "clear_lower_bound": lower, "enumerated_laps": 0}
    if x == 3:
        lower = H[1]-H[0]-blocked(y, H)
        assert lower > 0
        return {"pair": [x, y], "window": H, "method": "one blocked-duration evaluation",
                "clear_lower_bound": lower, "enumerated_laps": 0}
    s = sparse(x, y)
    assert s["smaller_speed_occurrences_in_J"] <= 4
    if s["clear_lower_bound"] > 0:
        return {"pair": [x, y], "window": J, "method": "two triple tests and selected graph",
                "clear_lower_bound": s["clear_lower_bound"],
                "enumerated_smaller_speed_laps_for_pair_integral": s["smaller_speed_occurrences_in_J"]}
    assert (x, y) in ZERO_PAIRS
    assert all(distance(v*F(3, 8)) >= D for v in (*CORE, x, y))
    return {"pair": [x, y], "window": J, "method": "equality witness", "time": F(3, 8)}


def main():
    for W, speeds in ((J, (1, 4, 5)), (H, CORE), (H, (*CORE, 3))):
        for v in speeds:
            cell = floor(v*W[0])
            assert D <= v*W[0]-cell <= v*W[1]-cell <= 1-D
    assert (H[1]-H[0])/2-F(3, 16)*(F(1, 34)+F(1, 34)) == F(1, 7616)
    assert F(3, 4)*(H[1]-H[0])-F(3, 16*12) == F(1, 896)

    profiles = [tail_profile(x) for x in range(1, 34) if x not in (*CORE, 3)]
    assert len(profiles) == 27 and max(p["occurrence_count"] for p in profiles) == 4
    finite = []
    for p in profiles:
        x = p["x"]
        for y in range(x+1, p["cutoff_y"]):
            if y in CORE:
                continue
            s, d = checked_case(x, y)
            zero = (x, y) in ZERO_PAIRS
            if zero:
                assert s["clear_lower_bound"] == d["clear_duration"] == 0
                expected = [F(5, 16), F(3, 8)] if (x, y) in ((10, 11), (11, 26)) else [F(3, 8)]
                assert d["valid_boundaries"] == expected
            else:
                assert s["clear_lower_bound"] > 0
            finite.append([x, y, s["clear_lower_bound"], d["clear_duration"], s["triple_flags"]])
        # Exercise each written tail bound at its first admissible y.
        y = max(x+1, p["cutoff_y"])
        s, d = checked_case(x, y)
        assert s["clear_lower_bound"] >= p["limit_L"]-p["error_C"]/y > 0
    assert len(finite) == 819
    assert sum(row[2] > 0 for row in finite) == 815

    special = []
    for y in (8, 9, 10, 11):
        clear = H[1]-H[0]-blocked(y, H)
        assert clear == direct(3, y, H)["clear_duration"] > 0
        special.append({"pair": [3, y], "clear_duration_in_H": clear})

    # Prescribed exploratory box, retained separately from the proof reduction.
    grid_rows, empty, equality, missed = [], [], [], []
    domain = [v for v in range(1, 81) if v not in CORE]
    for x, y in combinations(domain, 2):
        s, d = checked_case(x, y)
        grid_rows.append([x, y, s["clear_lower_bound"], d["clear_duration"], s["triple_flags"]])
        if d["clear_duration"] == 0:
            (equality if d["valid_boundaries"] else empty).append([x, y])
        elif s["clear_lower_bound"] <= 0:
            missed.append([x, y])
    assert len(grid_rows) == 2775 and len(empty) == 10 and len(equality) == 67
    assert not missed and empty == [[3, v] for v in range(8, 81, 8)]

    controls = []
    for x, y in ((11, 13), (11, 16), (14, 17), (16, 23), (40, 48), (3, 8)):
        s, d = checked_case(x, y)
        h = direct(x, y, H)
        controls.append({**s, "direct_J": d, "direct_H": h})
    cooperative = controls[3]
    assert cooperative["direct_J"]["clear_cells"] == [[F(17, 48), F(47, 128)]]
    assert cooperative["clear_lower_bound"] == F(5, 384)
    assert cooperative["direct_H"]["clear_duration"] == F(5, 224)
    # The old small interval is entirely covered, including both endpoints.
    old = direct(16, 23, (F(17, 56), F(5, 16)))
    assert old["clear_duration"] == 0 and old["valid_boundaries"] == []
    # Explicit small example of the lap-strip incompatibility for I6.
    assert list(laps(16, I6)) == [5] and list(laps(23, I6)) == [8]
    assert abs(23*5-16*8) == 13 > F(39, 8)

    # Exercise every routing branch; large cases have no direct time partition.
    selected_controls = [select_certificate(x, y) for x, y in
                         ((2, 3), (3, 8), (3, 56*10**12), (11, 56*10**12),
                          (16, 10**12+1), (33, 2**80+1), (1000, 10**12))]

    result = {
        "date": "2026-09-25", "research_baseline": "249de490b2881622ee44c7191691e11f67771b8d",
        "status": "Existing two-parameter family; new certificate selection synthesis awaiting independent review; no novelty claim.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixed_speeds": CORE, "threshold": D, "window_J": J, "window_H": H,
        "selection": "Use H if x=3 or x>=34; otherwise use J, with t=3/8 for the four finite zero cases.",
        "tail_profiles": profiles, "finite_reduction_count": len(finite),
        "finite_positive_count": 815, "finite_columns": ["x", "y", "bound", "actual_duration", "triple_flags"],
        "finite_rows": finite, "finite_zero_pairs": ZERO_PAIRS,
        "special_x3_controls": special,
        "grid": {"domain": "x<y<=80, x,y outside {1,4,5,6,7}", "cases": len(grid_rows),
                 "positive_duration_cases": 2698, "missed_positive_cases": missed,
                 "empty_pairs": empty, "equality_pairs": equality,
                 "complete_rows_sha256": hashlib.sha256(json.dumps(grid_rows, default=str, separators=(",", ":")).encode()).hexdigest()},
        "controls": controls,
        "selected_formula_controls": selected_controls,
        "limits": "The grid is diagnostic only; the unbounded argument uses the analytic fast branch, 27 strip bounds, four x=3 controls, and 819 reduced finite cases. Fixed-window and selected-reference scope only.",
    }
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("two_speed_transfer.json").read_text())
        print("PASS: 27 strip bounds, 819 reduced cases, x=3 controls, 2775 diagnostic pairs, and cooperative-window failure.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
