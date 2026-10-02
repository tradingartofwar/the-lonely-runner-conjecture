#!/usr/bin/env python3
"""Exact shared-lap, residual-set, and contact certificates for two controls.

This standalone checker imports no project implementation. --write generates
arithmetic.json; default/--check recomputes and compares without modifying it.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse
import json


HERE = Path(__file__).resolve().parent
RESIDUALS = [1, 4, 5, 6, 7, 11]
PROTOCOL_HASH = "f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d"


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def safe_laps(v):
    return [(F(8*m + 1, 8*v), F(8*m + 7, 8*v)) for m in range(v)]


def intersect(A, B):
    return sorted((max(a, c), min(b, d)) for a, b in A for c, d in B
                  if max(a, c) <= min(b, d))


def common_safe(speeds):
    result = [(F(0), F(1))]
    for v in speeds:
        result = intersect(result, safe_laps(v))
    return result


def phase(v, t):
    x = v*t
    return x - x.numerator // x.denominator


def direct_distances(speeds, t):
    return [min(phase(v, t), 1-phase(v, t)) for v in speeds]


def controllers(speeds, t):
    return {"lower": [v for v in speeds if phase(v, t) == F(1, 8)],
            "upper": [v for v in speeds if phase(v, t) == F(7, 8)]}


def cell_certificate(speeds, cell):
    left, right = cell
    mid = (left + right)/2
    laps = [(v*mid).numerator // (v*mid).denominator for v in speeds]
    bounds = [(F(8*m+1, 8*v), F(8*m+7, 8*v))
              for v, m in zip(speeds, laps)]
    assert max(a for a, _ in bounds) == left
    assert min(b for _, b in bounds) == right
    for a, b in bounds:
        assert a <= left <= right <= b
    ds = direct_distances(speeds, mid)
    assert min(ds) >= F(1, 8)
    assert (min(ds) > F(1, 8)) == (left < right)
    lower = controllers(speeds, left)["lower"]
    upper = controllers(speeds, right)["upper"]
    determinants = []
    for a in lower:
        p = (a*left).numerator // (a*left).denominator
        for b in upper:
            q = (b*right).numerator // (b*right).denominator
            delta = a*(8*q+7) - b*(8*p+1)
            assert right-left == F(delta, 8*a*b)
            determinants.append({"lower_speed": a, "upper_speed": b,
                                 "lower_lap": p, "upper_lap": q,
                                 "integer_gap": delta,
                                 "width": F(delta, 8*a*b)})
    return {"interval": cell, "duration": right-left,
            "lap_vector": laps, "lap_bounds": bounds,
            "left_controllers": controllers(speeds, left),
            "right_controllers": controllers(speeds, right),
            "endpoint_determinants": determinants,
            "witness": {"time": mid, "distances": ds,
                        "kind": "strict" if left < right else "equality"}}


def pair_contacts(speeds):
    rows = []
    for a, b in combinations(speeds, 2):
        g = gcd(a, b)
        opposite = (a+b)//g % 8 == 0
        same = abs(a-b)//g % 8 == 0
        contacts = []
        for numerator, label in [(1, "lower"), (7, "upper")]:
            for m in range(a):
                t = F(8*m+numerator, 8*a)
                bphase = phase(b, t)
                if bphase not in (F(1, 8), F(7, 8)):
                    continue
                blabel = "lower" if bphase == F(1, 8) else "upper"
                ds = direct_distances(speeds, t)
                contacts.append({"time": t, "orientations": [label, blabel],
                                 "all_runners_safe": min(ds) >= F(1, 8),
                                 "blocking_speeds": [v for v, d in zip(speeds, ds)
                                                     if d < F(1, 8)]})
        assert any(x["orientations"][0] != x["orientations"][1]
                   for x in contacts) == opposite
        assert any(x["orientations"][0] == x["orientations"][1]
                   for x in contacts) == same
        assert sum(x["orientations"] == ["lower", "upper"]
                   for x in contacts) == (g if opposite else 0)
        assert sum(x["orientations"] == ["lower", "lower"]
                   for x in contacts) == (g if same else 0)
        rows.append({"speeds": [a, b], "gcd": g,
                     "primitive_sum": (a+b)//g,
                     "primitive_difference": abs(a-b)//g,
                     "opposite_contact_possible": opposite,
                     "same_contact_possible": same,
                     "contacts": sorted(contacts, key=lambda x: x["time"])})
    return rows


def residues(V):
    records = []
    for m in range(V):
        quotients = [v*m//V for v in RESIDUALS]
        rs = [v*m % V for v in RESIDUALS]
        assert rs[0] == m  # The fixed residual speed 1 anchors the shared lap.
        assert all(rs[i] == v*rs[0] % V for i, v in enumerate(RESIDUALS))
        determinants = []
        for i, j in combinations(range(6), 2):
            delta = RESIDUALS[i]*rs[j] - RESIDUALS[j]*rs[i]
            assert delta % V == 0
            assert delta//V == RESIDUALS[j]*quotients[i] - RESIDUALS[i]*quotients[j]
            determinants.append([RESIDUALS[i], RESIDUALS[j], delta//V])
        next_rs = [(r+v) % V for r, v in zip(rs, RESIDUALS)]
        assert next_rs == [v*((m+1) % V) % V for v in RESIDUALS]
        records.append({"m": m, "residues": rs, "quotients": quotients,
                        "next_residues": next_rs,
                        "pair_determinants_divided_by_V": determinants})
    return records


def offset_alignment(V):
    """Arithmetic of the frozen lap shifts, without another phase outcome scan."""
    assert gcd(11, V) == 1
    rows = []
    for s in range(V):
        defect = 11*s % V
        for m in range(V):
            assert ((11*(m+s) % V)-11*m) % V == defect
            assert ((11*(m+s) % V)-11*((m+s) % V)) % V == 0
        assert (defect == 0) == (s == 0)
        rows.append({"offset": s, "speed11_start_phase": F(defect, V),
                     "single_shift_pair_1_11_determinant_mod_V": defect,
                     "common_start_pair_relation_preserved": s == 0,
                     "all_runner_shift_pair_relation_preserved": True})
    return rows


def fastest_effect(V, A):
    rows = []
    for cell in A:
        a, b = cell
        survivors = intersect([cell], safe_laps(V))
        row = {"residual_cell": cell, "fastest_image": [V*a, V*b],
               "survivors": survivors}
        if a == b:
            row["point_phase"] = phase(V, a)
            row["point_safe"] = bool(survivors)
        elif not survivors:
            mid_phase = V*(a+b)/2
            k = (mid_phase+F(1, 2)).numerator // (mid_phase+F(1, 2)).denominator
            lower_margin = V*a - (k-F(1, 8))
            upper_margin = k+F(1, 8) - V*b
            assert lower_margin > 0 and upper_margin > 0
            row["strict_cover"] = {"collision_lap": k,
                                   "lower_phase_margin": lower_margin,
                                   "upper_phase_margin": upper_margin}
        for left, right in survivors:
            midpoint = (left+right)/2
            m = (V*midpoint).numerator // (V*midpoint).denominator
            assert F(1, 8) <= V*left-m <= V*right-m <= F(7, 8)
        rows.append(row)
    return rows


def continuous_phase_certificate():
    """Check exact constants of the separately supplied symbolic arguments.

    This is not a numerical phase scan or a machine proof of the universal
    quantifiers; arithmetic.md supplies those implications explicitly.
    """
    unchanged13 = [1, 4, 5, 6, 7, 13]
    left13 = (F(17, 48), F(3, 8))
    right13 = (1-left13[1], 1-left13[0])
    assert left13[1]-left13[0] == F(1, 48)
    c13 = [cell_certificate(unchanged13, cell) for cell in [left13, right13]]
    assert phase(11, F(3, 8)) == F(1, 8)
    assert phase(11, F(5, 8)) == F(7, 8)
    images13 = [[11*t-4 for t in left13], [11*t-7 for t in right13]]
    assert images13 == [[F(-5, 48), F(1, 8)], [F(-1, 8), F(5, 48)]]
    assert images13[0][0] <= images13[1][1]
    phase_union13 = [min(row[0] for row in images13), max(row[1] for row in images13)]
    assert phase_union13 == [F(-1, 8), F(1, 8)]
    unchanged16 = [1, 4, 5, 6, 7, 16]
    left16 = (F(25, 56), F(15, 32))
    right16 = (1-left16[1], 1-left16[0])
    c16 = [cell_certificate(unchanged16, cell) for cell in [left16, right16]]
    images = [[11*t-5 for t in left16], [11*t-6 for t in right16]]
    assert images == [[F(-5, 56), F(5, 32)], [F(-5, 32), F(5, 56)]]
    phase_union = [min(row[0] for row in images), max(row[1] for row in images)]
    assert images[0][0] <= images[1][1]  # The image intervals overlap.
    assert phase_union == [F(-5, 32), F(5, 32)]
    phase_union_length = phase_union[1]-phase_union[0]
    clear_phase_lower_bound = phase_union_length-F(1, 4)
    clear_time_lower_bound = clear_phase_lower_bound/11
    assert clear_time_lower_bound == F(1, 176)
    unchanged_phase_survivors = intersect([left16, right16], safe_laps(11))
    assert sum((b-a for a, b in unchanged_phase_survivors), F(0)) == F(1, 176)
    return {"status": "HYPOTHESIS / proof candidates; exact constants checked, universal phase argument in arithmetic.md",
            "numerical_phase_scan_performed": False,
            "tight13": {"unchanged_speeds": unchanged13,
                        "unchanged_safe_cells": c13,
                        "theta_domain": "0 < theta < 1, modulo one",
                        "speed11_centered_phase_images": images13,
                        "phase_union": phase_union13,
                        "phase_union_length": F(1, 4),
                        "shifted_blocking_arc_length": F(1, 4),
                        "circular_distance_d": "min(theta, 1-theta)",
                        "phase_overlap_formula": "max(0, 1/4-d)",
                        "duration_lower_bound": "min(d, 1/4)/11",
                        "secondary_one_sided_duration_bound": "min(1/48, theta/11, (1-theta)/11)",
                        "nonzero_protocol_offset_lower_bound": F(1, 143)},
            "strict16": {"unchanged_speeds": unchanged16,
                         "unchanged_safe_cells": c16,
                         "speed11_centered_phase_images": images,
                         "phase_union": phase_union,
                         "phase_union_length": phase_union_length,
                         "shifted_blocking_arc_length": F(1, 4),
                         "clear_phase_lower_bound": clear_phase_lower_bound,
                         "duration_lower_bound": clear_time_lower_bound,
                         "sharp_on_restricted_union_at_theta_zero": True,
                         "theta_zero_restricted_survivors": unchanged_phase_survivors}}


def build():
    protocol_bytes = (HERE/"protocol.json").read_bytes()
    assert sha256(protocol_bytes).hexdigest() == PROTOCOL_HASH
    protocol = json.loads(protocol_bytes)
    assert protocol["residual_speeds"] == RESIDUALS
    assert [case["velocities"] for case in protocol["cases"]] == [
        [0]+RESIDUALS+[13], [0]+RESIDUALS+[16]]
    A = common_safe(RESIDUALS)
    expected_A = [(F(1, 8), F(1, 8)), (F(17, 56), F(5, 16)),
                  (F(3, 8), F(3, 8)), (F(41, 88), F(15, 32)),
                  (F(17, 32), F(47, 88)), (F(5, 8), F(5, 8)),
                  (F(11, 16), F(39, 56)), (F(7, 8), F(7, 8))]
    assert A == expected_A
    cases = []
    for prescribed in protocol["cases"]:
        speeds = prescribed["velocities"][1:]
        V = speeds[-1]
        allowed = intersect(A, safe_laps(V))
        cells = []
        for cell in allowed:
            cert = cell_certificate(speeds, cell)
            midpoint = sum(cell)/2
            m = (V*midpoint).numerator // (V*midpoint).denominator
            cert["fastest_lap"] = m
            cert["normalized_interval"] = [V*t-m for t in cell]
            cert["shared_residues"] = [v*m % V for v in RESIDUALS]
            for v, r in zip(RESIDUALS, cert["shared_residues"]):
                for t, u in zip(cell, cert["normalized_interval"]):
                    assert phase(v, t) == phase(1, (r+v*u)/V)
            cells.append(cert)
        if V == 13:
            assert allowed == [(F(q, 8), F(q, 8)) for q in (1, 3, 5, 7)]
        else:
            assert allowed == [(F(17, 56), F(39, 128)),
                               (F(41, 88), F(15, 32)),
                               (F(17, 32), F(47, 88)),
                               (F(89, 128), F(39, 56))]
            assert all(len(cell["endpoint_determinants"]) == 1 and
                       cell["endpoint_determinants"][0]["integer_gap"] == 1
                       for cell in cells)
        cases.append({"id": prescribed["id"], "fastest_speed": V,
                      "residue_periods": [[v, V//gcd(v, V)] for v in RESIDUALS],
                      "protocol_offset_alignment": offset_alignment(V),
                      "laps": residues(V), "fastest_effect_on_A": fastest_effect(V, A),
                      "allowed_cells": cells,
                      "allowed_duration": sum((b-a for a, b in allowed), F(0)),
                      "isolated_points": [a for a, b in allowed if a == b],
                      "pair_contact_checks": pair_contacts(speeds)})
    return encode({"status": "OBSERVED exact arithmetic in the two prescribed common-start cases",
                   "protocol_sha256": PROTOCOL_HASH,
                   "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                   "residual_speeds": RESIDUALS,
                   "residual_allowed_cells": [cell_certificate(RESIDUALS, c) for c in A],
                   "residual_allowed_duration": sum((b-a for a, b in A), F(0)),
                   "continuous_phase_candidates": continuous_phase_certificate(),
                   "cases": cases,
                   "totals": {"cases": 2, "shared_lap_records": 29,
                              "pair_determinant_checks": 29*15,
                              "pair_contact_criteria_checks": 2*21,
                              "residual_components": len(A),
                              "final_allowed_components": sum(len(c["allowed_cells"]) for c in cases)}})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE/"arithmetic.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2)+"\n")
    else:
        assert json.loads(path.read_text()) == result, "arithmetic.json mismatch"
    print(json.dumps(result["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
