"""Exact distinction audit: existing-domain collisions and two stress cases.

Standard library only. Closed-component reconstruction is independent of the
periodic-integral signatures used to group the existing 2775-pair domain.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import gcd
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
J = (F(9, 32), F(3, 8))
CORE = (1, 4, 5)
FIXED = (*CORE, 6, 7)
I6 = (F(5, 16), F(17, 48))
I7 = (J[0], F(17, 56))


def floor(x):
    return x.numerator//x.denominator


def distance(x):
    p = x % 1
    return min(p, 1-p)


def primitive(z):
    z += D
    n = floor(z)
    return F(n, 4)+min(z-n, F(1, 4))


def duration(v, interval=J):
    a, b = interval
    return (primitive(v*b)-primitive(v*a))/v


def occurrences(v, interval=J):
    a, b = interval
    return [(max(a, (m-D)/v), min(b, (m+D)/v))
            for m in range(floor(v*a-D)+1, -floor(-(v*b+D)))]


def signature(x, y):
    # D6,D7 and O67 are fixed; these seven entries retain all variable
    # single/pair moments with vertex roles (6,7,x,y), not a sorted multiset.
    return (duration(x), duration(y), duration(x, I6), duration(y, I6),
            duration(x, I7), duration(y, I7),
            sum((duration(y, I) for I in occurrences(x)), F(0)))


def schedule(extras, window=J, core=CORE):
    speeds = (*core, *extras)
    a, b = window
    points = set(window)
    for v in speeds:
        for m in range(floor(v*a)-1, floor(v*b)+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if a < t < b:
                    points.add(t)
    points = sorted(points)
    masses = [F(0)]*(1 << len(extras))
    pieces = []
    for left, right in zip(points, points[1:]):
        t = (left+right)/2
        assert all(distance(v*t) >= D for v in core)
        state = sum(1 << i for i, v in enumerate(extras) if distance(v*t) < D)
        masses[state] += right-left
        if state == 0:
            pieces.append((left, right))
    boundaries = [t for t in points if all(distance(v*t) >= D for v in speeds)]
    pieces.extend((t, t) for t in boundaries)
    components = []
    for left, right in sorted(pieces):
        if components and left <= components[-1][1]:
            components[-1] = (components[-1][0], max(right, components[-1][1]))
        else:
            components.append((left, right))
    moments = [sum(z for state, z in enumerate(masses) if state & subset == subset)
               for subset in range(len(masses))]
    single = [moments[1 << i] for i in range(len(extras))]
    pairs = [moments[(1 << i) | (1 << j)] for i, j in combinations(range(len(extras)), 2)]
    triple = [moments[s] for s in range(len(masses)) if s.bit_count() == 3]
    E = sum(single)-(b-a)
    R = sum(max(s.bit_count()-1, 0)*z for s, z in enumerate(masses))
    assert masses[0] == R-E == sum((right-left for left, right in components), F(0))
    if len(extras) == 4:
        assert R == sum(pairs)-sum(triple)+moments[15]
    contacts = []
    for left, right in components:
        if left != right:
            continue
        contacts.append({"time": left, "threshold_controllers": [
            {"speed": v, "phase": (v*left) % 1,
             "direction": "enters safe region" if (v*left) % 1 == D else "leaves safe region"}
            for v in speeds if distance(v*left) == D]})
    return {"extras": extras, "window": window, "single_durations": single, "pair_durations": pairs,
            "pair_gcds": [gcd(a, b) for a, b in combinations(extras, 2)],
            "moments_by_mask": moments, "state_durations_by_mask": masses,
            "E": E, "R": R, "clear_duration": masses[0], "components": components,
            "positive_components": sum(a < b for a, b in components),
            "isolated_components": sum(a == b for a, b in components), "isolated_contacts": contacts}


def safe_lap_cell(speeds, witness, window=J):
    rows = []
    for v in speeds:
        k = floor(v*witness)
        left, right = (k+D)/v, (k+1-D)/v
        assert left <= witness <= right
        rows.append({"speed": v, "lap": k, "left": left, "right": right})
    a = max(window[0], max(r["left"] for r in rows))
    b = min(window[1], min(r["right"] for r in rows))
    assert a <= b
    for r, s in combinations(rows, 2):
        assert r["speed"]*(s["lap"]+D) <= s["speed"]*(r["lap"]+1-D)
        assert s["speed"]*(r["lap"]+D) <= r["speed"]*(s["lap"]+1-D)
    return {"speeds": speeds, "witness": witness, "rows": rows, "cell": [a, b], "width": b-a,
            "active_lower_speeds": [r["speed"] for r in rows if r["left"] == a],
            "active_upper_speeds": [r["speed"] for r in rows if r["right"] == b],
            "witness_margin": min(distance(v*witness)-D for v in speeds)}


def main():
    groups = defaultdict(list)
    domain = [v for v in range(1, 81) if v not in FIXED]
    signatures = []
    for x, y in combinations(domain, 2):
        sig = signature(x, y)
        groups[sig].append((x, y))
        signatures.append([x, y, *sig])
    collisions = [pairs for pairs in groups.values() if len(pairs) > 1]
    assert len(signatures) == 2775 and len(groups) == 2771
    assert collisions == [[(2, 23), (2, 69)], [(2, 25), (2, 75)],
                          [(8, 25), (8, 75)], [(21, 25), (21, 75)]]
    matched = []
    for pairs in collisions:
        rows = [schedule((6, 7, x, y)) for x, y in pairs]
        a, b = rows
        assert a["single_durations"] == b["single_durations"]
        assert a["pair_durations"] == b["pair_durations"]
        assert a["pair_gcds"] != b["pair_gcds"]
        assert a["clear_duration"] == b["clear_duration"] > 0
        assert a["components"] != b["components"]
        for (x, y), r in zip(pairs, rows):
            sig = signature(x, y)
            assert sig == (*r["single_durations"][2:], *[r["pair_durations"][i] for i in (1, 2, 3, 4, 5)])
        all_moments_same = a["moments_by_mask"] == b["moments_by_mask"]
        assert all_moments_same == (pairs[0][0] != 21)
        matched.append({"variable_pairs": pairs, "same_all_moments": all_moments_same, "cases": rows})
    assert [r["positive_components"] for r in matched[0]["cases"]] == [2, 3]
    assert [(r["positive_components"], r["isolated_components"]) for r in matched[1]["cases"]] == [(3, 0), (4, 1)]
    assert matched[1]["cases"][1]["isolated_contacts"][0]["time"] == F(3, 8)

    # A genuinely different higher-order pattern with unchanged target duration.
    a, b = matched[3]["cases"]
    assert [a["moments_by_mask"][13], a["moments_by_mask"][14]] == [F(0), F(3, 800)]
    assert [b["moments_by_mask"][13], b["moments_by_mask"][14]] == [F(1, 300), F(1, 2400)]
    # B21 is already covered by B6 union B7. B2 is empty on J. This proves
    # identical complete allowed sets after adding ANY common fourth blocker.
    assert occurrences(2) == []
    intervals21 = occurrences(21)
    assert intervals21 == [(J[0], F(7, 24)), (F(55, 168), F(19, 56))]
    assert I7[0] <= intervals21[0][0] < intervals21[0][1] <= I7[1]
    assert I6[0] <= intervals21[1][0] < intervals21[1][1] <= I6[1]
    assert occurrences(8) == [(F(23, 64), J[1])]
    assert I6[1] < F(23, 64) and I7[1] < F(23, 64)
    # Logical identities prove that pair moments determine U for every y
    # in each of these three fixed-x classes, not just the matching controls.
    for x in (2, 8, 21):
        for s in range(16):
            b6, b7, bx, by = [int(bool(s & (1 << i))) for i in range(4)]
            if b6 and b7:
                continue
            if x == 2 and bx:
                continue
            if x == 8 and b6+b7+bx > 1:
                continue
            if x == 21 and bx and not (b6 or b7):
                continue
            if x == 8:
                count = 1-b6-b7-bx-by+(b6+b7+bx)*by
            else:
                count = 1-b6-b7-by+(b6+b7)*by
            assert count == int(s == 0)
    for i in range(2):
        assert matched[1]["cases"][i]["components"] == matched[3]["cases"][i]["components"]

    stress = [schedule((6, 7, 11, 13)), schedule((56, 113, 64, 72))]
    assert stress[0]["clear_duration"] == 0 and stress[0]["components"] == [(F(3, 8), F(3, 8))]
    assert stress[1]["clear_duration"] == F(6193, 260352) and stress[1]["positive_components"] == 11
    cells = [safe_lap_cell((*CORE, 6, 7, 11, 13), F(3, 8)),
             safe_lap_cell((*CORE, 56, 113, 64, 72), F(83, 226))]
    assert cells[0]["width"] == 0 and cells[0]["active_lower_speeds"] == [11]
    assert cells[0]["active_upper_speeds"] == [5, 13]
    assert cells[1]["cell"] == [F(329, 904), F(335, 904)]
    assert cells[1]["width"] == F(3, 452) and cells[1]["witness_margin"] == F(35, 904)

    ratio_cases = [schedule((80, 240, 88, 96)), schedule((160, 240, 88, 96))]
    assert ratio_cases[0]["single_durations"] == ratio_cases[1]["single_durations"]
    assert ratio_cases[0]["pair_durations"][0] == ratio_cases[1]["pair_durations"][0] == F(1, 128)
    assert ratio_cases[0]["E"] == ratio_cases[1]["E"] == F(1, 1408)
    assert ratio_cases[0]["pair_durations"] != ratio_cases[1]["pair_durations"]
    assert [r["clear_duration"] for r in ratio_cases] == [F(1153, 42240), F(613, 21120)]

    # Reproduce the existing abstract event alteration. It is NOT a second
    # physical speed configuration or a counterexample to the conjecture.
    old = schedule((6, 7, 11, 16))
    theta = F(1, 896)
    alternate = old["state_durations_by_mask"].copy()
    for s in (0, 5, 9, 12):
        alternate[s] -= theta
    for s in (1, 4, 8, 13):
        alternate[s] += theta
    assert min(alternate) >= 0 and alternate[0] == 0
    alt_moments = [sum(z for s, z in enumerate(alternate) if s & mask == mask) for mask in range(16)]
    assert all(alt_moments[s] == old["moments_by_mask"][s] for s in range(16) if s.bit_count() <= 2)

    # Both zero duration, but a local existence difference needs endpoint data.
    empty = schedule((6, 7, 3, 8))
    assert empty["clear_duration"] == 0 and empty["components"] == []
    assert empty["moments_by_mask"] != stress[0]["moments_by_mask"]
    result = {"date": "2026-09-25", "research_baseline": "f25e26f2074b036643a2c791f32aacc26856356b",
              "status": "Exact bounded audit and elementary representation arguments; no new general LRC claim or novelty claim.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "core": CORE, "window": J, "threshold": D,
              "signature_search": {"domain": "Existing x<y<=80, x,y outside {1,4,5,6,7}", "inputs": 2775,
                  "unique_signatures": 2771, "collision_classes": 4, "collision_members": 8,
                  "different_duration_matches": 0, "different_local_existence_matches": 0,
                  "rows_sha256": hashlib.sha256(json.dumps(signatures, default=str, separators=(",", ":")).encode()).hexdigest()},
              "matched_cases": matched,
              "redundant_constraint": {"B21_occurrences": intervals21, "covering_intervals": [I7, I6],
                                       "B8_occurrences": occurrences(8),
                                       "statement": "B21 is contained in B6 union B7; B2 is empty; B8 is disjoint from B6 and B7. Pair moments suffice for U for all admissible y in each fixed-x class 2,8,21."},
              "stress_cases": stress, "closed_safe_lap_cells": cells, "ratio_controls": ratio_cases,
              "abstract_same_pair_data": {"actual": old, "alternate_state_durations": alternate, "alternate_moments": alt_moments},
              "zero_measure_empty_control": empty,
              "limits": "All actual matches use common-start speeds, the same core/window/threshold, and labelled roles. No whole-configuration scaling. No physical same-pair-data match with different duration or existence was found in the stated domain. The abstract alteration has a different scope."}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("distinction_audit.json").read_text())
        print("PASS: 2775 signatures, four physical collision pairs, two stress/lattice cases, ratio controls, redundancy and abstract-moment controls.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
