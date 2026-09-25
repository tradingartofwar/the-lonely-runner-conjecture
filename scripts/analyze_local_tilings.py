"""Local escape at four-blocker tilings; exact, targeted certificates.

Run: python -m scripts.analyze_local_tilings [--figure]
Four prescribed common-start profiles, no coefficient-box or time-grid scan.
General implications remain proof candidates; see LOCAL_TILING_RULE.md.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from math import lcm
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_affine_family import frozen_phase
from scripts.analyze_core_transfer import boundary_certificate, merged
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate
from scripts.analyze_tiling_escape import DEPENDENCIES as PRIOR_DEPENDENCIES

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "f8c021deabfd92d55ce8ede0e4171ccb5efd95be"
DEPENDENCIES = (*PRIOR_DEPENDENCIES, "scripts/analyze_tiling_escape.py")
D = Q(1, 8)
CASES = (
    ("original", (4, 12, 10, 22), Q(3, 16)),
    ("sheared", (5, 13, 12, 24), Q(3, 16)),
    ("three_each_side", (4, 12, 10, 6), Q(3, 16)),
    ("period_24", (4, 16, 11, 29), Q(5, 24)),
)


def floor(z):
    return z.numerator // z.denominator


def ceil(z):
    return -floor(-z)


def gap_lines(g):
    c, s, a, b = g["contact"], g["sign"], g["A"], g["B"]
    return ((c, -a), (c, -b)) if s == 1 else ((c, b), (c, a))


def value(line, h):
    return line[0] + line[1] * h


def profile(name, coefficients, x0):
    terms = tuple(zip((1, 1, 2, 2), coefficients))
    assert min(coefficients) >= 4
    phase = frozen_phase(terms, x0)
    assert phase["clear_phase_duration"] == 0
    assert all(circular_distance(k*x0) > D for k in (1, 2, 3))
    assert ((coefficients[1]-coefficients[0])*x0) % 1 == Q(1, 2)
    assert sorted(((a-2*coefficients[0])*x0) % 1 for a in coefficients[2:]) == [Q(3, 8), Q(5, 8)]
    blocks = []
    for i, (b, a) in enumerate(terms):
        for m in range(b):
            left = ((m - a*x0 - D)/b) % 1
            blocks.append({"left": left, "right": left+2*D/b,
                           "runner": i, "r": Q(a, b)})
    blocks.sort(key=lambda row: row["left"])
    contacts, gaps = [], []
    for i, left in enumerate(blocks):
        right = blocks[(i+1) % len(blocks)]
        assert left["right"] == right["left"] + (i == len(blocks)-1)
        c = left["right"] % 1
        delta = left["r"] - right["r"]
        assert delta != 0
        contacts.append({"contact": c, "left_runner": left["runner"],
                         "right_runner": right["runner"],
                         "left_r": left["r"], "right_r": right["r"], "delta": delta})
        gaps.append({"contact": c, "sign": 1 if delta > 0 else -1,
                     "A": max(left["r"], right["r"]),
                     "B": min(left["r"], right["r"])})
    contacts.sort(key=lambda c: c["contact"])
    gaps.sort(key=lambda g: (g["sign"], g["contact"]))
    assert sum(c["delta"] for c in contacts) == 0
    K = sum(abs(c["delta"]) for c in contacts)/2
    assert K > 0
    radii = []
    for i, c in enumerate(contacts):
        nxt = contacts[(i+1) % len(contacts)]
        distance = nxt["contact"]-c["contact"]+(i == len(contacts)-1)
        speed = max(abs(a-b) for a in (c["left_r"], c["right_r"])
                    for b in (nxt["left_r"], nxt["right_r"]))
        if speed:
            radii.append(distance/speed)
    core_radius = min(min((k*x0) % 1-D, 1-D-(k*x0) % 1)/k for k in (1, 2, 3))
    max_r = max(Q(a, b) for b, a in terms)
    denominator = x0.denominator
    unit_difference = abs(coefficients[1]-coefficients[0])
    assert denominator % 8 == 0 and denominator <= 2*unit_difference < 2*max_r
    assert core_radius >= Q(1, 3*denominator)
    assert max_r*core_radius > Q(1, 6)
    H = 1/(8*max_r)
    assert H < min(*radii, core_radius)
    cutoff = 8
    assert 1/(max_r*cutoff+1) < H
    period = lcm(*(c["contact"].denominator for c in contacts))
    return {"name": name, "terms": terms, "x0": x0, "tiling_profile": phase,
            "blocks": blocks, "contacts": contacts, "gaps": gaps, "K": K,
            "H": H, "core_radius": core_radius, "cluster_collision_radii": radii,
            "max_r": max_r, "sufficient_q": cutoff, "residue_period": period,
            "uniform_bound_certificate": {"x0_denominator": denominator,
                "unit_coefficient_difference": unit_difference, "denominator_upper_bound": 2*unit_difference,
                "core_radius_lower_bound": Q(1, 3*denominator),
                "normalized_core_radius": max_r*core_radius,
                "normalized_collision_radii": [max_r*r for r in radii]}}


def chamber_certificate(p, s):
    terms, x0, H = p["terms"], p["x0"], p["H"]
    lines = [(c["contact"], -s*r) for c in p["contacts"]
             for r in (c["left_r"], c["right_r"])]
    lines.sort(key=lambda line: value(line, H/2))
    cells, good = [], []
    for i, left in enumerate(lines):
        right = lines[i+1] if i+1 < len(lines) else (lines[0][0]+1, lines[0][1])
        assert value(left, H/2) < value(right, H/2)
        assert all(value(left, h) <= value(right, h) for h in (Q(0), H))
        midpoint = (value(left, H/2)+value(right, H/2))/2
        rows, blocked = [], []
        for j, (b, a) in enumerate(terms):
            middle = a*(x0+s*H/2)+b*midpoint
            bad = circular_distance(middle) < D
            integer = floor(middle+Q(1, 2)) if bad else floor(middle)
            low, high = (integer-D, integer+D) if bad else (integer+D, integer+1-D)
            vertices = [a*(x0+s*h)+b*value(line, h)
                        for h in (Q(0), H) for line in (left, right)]
            assert all(low <= z <= high for z in vertices)
            if bad:
                blocked.append(j)
            rows.append({"runner": j, "blocked": bad, "bounds": (low, high), "vertices": vertices})
        if not blocked:
            good.append((left, right))
        cells.append({"left": left, "right": right, "blocked_runners": blocked, "certificates": rows})
    expected = [gap_lines(g) for g in p["gaps"] if g["sign"] == s]
    assert sorted(good) == sorted(expected)
    assert sum(r[1]-l[1] for l, r in good) == p["K"]
    core = []
    for k in (1, 2, 3):
        m = floor(k*x0)
        phases = [k*(x0+s*h)-m for h in (Q(0), H)]
        assert all(D < z < 1-D for z in phases)
        core.append({"speed_multiple": k, "endpoint_phases": phases})
    return {"sign": s, "cells": cells, "core_certificate": core}


def phase_model(p, s, h):
    result = []
    if not h:
        contacts = [c["contact"] for c in p["contacts"]]
        if Q(0) in contacts:
            contacts.append(Q(1))
        return tuple((c, c) for c in sorted(contacts))
    for g in p["gaps"]:
        if g["sign"] != s:
            continue
        left, right = gap_lines(g)
        for shift in (-1, 0, 1):
            a, b = max(Q(0), value(left, h)+shift), min(Q(1), value(right, h)+shift)
            if a <= b:
                result.append((a, b))
    return merged(result)


def candidate(p, q, g):
    z = q*g["contact"]-p["x0"]
    j = floor(z) if g["sign"] == 1 else ceil(z)
    rho = g["sign"]*(z-j)
    hits_at_zero = rho == 0
    if hits_at_zero:
        j -= g["sign"]
        rho = Q(1)
    assert 0 < rho <= 1
    return {**g, "j": j % q, "rho": rho, "hits_at_zero": hits_at_zero,
            "entry_h": rho/(g["A"]*q+1), "exit_h": rho/(g["B"]*q+1)}


def residue_certificate(p):
    rows = []
    for residue in range(p["residue_period"]):
        q = residue + 3*p["residue_period"]
        candidates = [candidate(p, q, g) for g in p["gaps"]]
        winner = min(candidates, key=lambda c: (c["rho"]/c["A"], c["rho"]))
        comparisons, cutoff = [], 3
        for c in candidates:
            slope = c["rho"]*winner["A"] - winner["rho"]*c["A"]
            constant = c["rho"]-winner["rho"]
            assert slope >= 0 and (slope > 0 or constant >= 0)
            if slope > 0:
                cutoff = max(cutoff, floor(-constant/slope)+1)
            comparisons.append({"contact": c["contact"], "sign": c["sign"],
                                "slope": slope, "constant": constant})
        assert all(c["slope"]*cutoff+c["constant"] >= 0 for c in comparisons)
        rows.append({"q_residue": residue, "mismatches": [c["rho"] for c in candidates],
                     "zero_contacts": [c["contact"] for c in candidates if c["hits_at_zero"]],
                     "eventual_winner": winner, "winner_cutoff": cutoff, "comparisons": comparisons})
    return rows


def model_actual(p, q):
    x0, H = p["x0"], p["H"]
    result = [(c["contact"], c["contact"]) for c in p["contacts"]
              if (q*c["contact"]-x0).denominator == 1]
    for g in p["gaps"]:
        s = g["sign"]
        for shift in (-1, 0, 1):
            c = g["contact"]+shift
            for j in range(q):
                rho = s*(q*c-x0-j)
                if rho <= 0:
                    continue
                a, b = rho/(g["A"]*q+1), min(H, rho/(g["B"]*q+1))
                if a <= b:
                    result.append(tuple(sorted(((x0+s*a+j)/q, (x0+s*b+j)/q))))
    return merged(result)


def actual_check(p, q, complete):
    x0, H = p["x0"], p["H"]
    speeds = (q, 2*q, 3*q, *(a*q+b for b, a in p["terms"]))
    assert min(speeds) > 0 and len(set(speeds)) == 7
    cc = [candidate(p, q, g) for g in p["gaps"]]
    first = min(cc, key=lambda c: c["entry_h"])
    zero = [c["contact"] for c in p["contacts"] if (q*c["contact"]-x0).denominator == 1]
    certificates = []
    for c in cc:
        lo, hi = c["entry_h"], min(H, c["exit_h"])
        if lo >= hi:
            continue
        times = tuple(sorted(((x0+c["sign"]*lo+c["j"])/q, (x0+c["sign"]*hi+c["j"])/q)))
        mid = sum(times)/2
        distance = min(circular_distance(v*mid) for v in speeds)
        assert distance > D
        cert = phase_certificate(speeds, times)
        certificates.append({"contact": c["contact"], "sign": c["sign"], "interval": times,
                             "strict_midpoint": mid, "strict_minimum": distance, "certificate": cert})
    if q >= p["sufficient_q"]:
        assert certificates and first["entry_h"] < H
    result = {"q": q, "complete": complete, "speeds": speeds, "zero_contacts": zero,
              "six_candidates": cc, "first_positive_component_entry": first,
              "strict_interval_certificates": certificates}
    if complete:
        full = feasible_intervals(speeds, D)
        assert full == boundary_certificate(speeds)["complete_allowed_set"]
        windows = tuple(((x0-H+j)/q, (x0+H+j)/q) for j in range(q))
        local = intersect(full, windows)
        assert local == model_actual(p, q)
        assert all((c, c) in full for c in zero)
        distances = []
        for j, window in enumerate(windows):
            for a, b in intersect(full, (window,)):
                if a < b:
                    da, db = q*a-j-x0, q*b-j-x0
                    assert da*db > 0
                    distances.extend((abs(da), abs(db)))
        if distances:
            assert min(distances) == first["entry_h"]
        else:
            assert first["entry_h"] >= H
        result["complete_local_allowed_intervals"] = local
        result["full_component_count"] = len(full)
    return result


def counterchecks(profiles):
    original, sheared, three, period24 = profiles
    assert original["K"] == sheared["K"] == 14
    assert three["K"] == 11 and period24["K"] == 21
    # Adding b to each coefficient shears the phase picture without changing widths.
    assert [(b, a+b) for b, a in original["terms"]] == list(sheared["terms"])
    assert sorted((c["contact"]-original["x0"]) % 1 for c in original["contacts"]) == sorted(c["contact"] for c in sheared["contacts"])
    for s in (-1, 1):
        assert sorted(g["A"]-g["B"] for g in original["gaps"] if g["sign"] == s) == sorted(g["A"]-g["B"] for g in sheared["gaps"] if g["sign"] == s)
    assert [sum(g["sign"] == s for g in three["gaps"]) for s in (-1, 1)] == [3, 3]
    assert period24["residues"][5]["zero_contacts"] and not period24["residues"][13]["zero_contacts"]
    frozen_grid = []
    for p in (original, sheared):
        for epsilon in (-Q(1, 10_000), Q(0), Q(1, 10_000)):
            x = p["x0"]+epsilon
            phase = frozen_phase(p["terms"], x)
            survivors = [(x+j)/5 for j in range(5) if all(circular_distance(a*x+b*(x+j)/5) >= D for b, a in p["terms"])]
            assert phase["clear_phase_duration"] == p["K"]*abs(epsilon)
            if epsilon:
                assert phase["clear_phase_duration"] > 0 and not survivors
            else:
                assert survivors == ([] if p is original else [Q(7, 16)])
            frozen_grid.append({"profile": p["name"], "q": 5, "epsilon": epsilon,
                                "clear_length": phase["clear_phase_duration"], "survivors": survivors})
    # An independently shifted auxiliary system can move as a rigid tiling.
    # It is not a distinct-speed common-start runner example.
    rigid_terms = ((1, 4, Q(0)), (1, 4, Q(1, 2)), (2, 8, Q(3, 8)), (2, 8, Q(5, 8)))
    rigid = []
    for epsilon in (-Q(1, 112), Q(0), Q(1, 112)):
        region = ((Q(0), Q(1)),)
        for b, a, shift in rigid_terms:
            phase = (a*epsilon+shift) % 1
            intervals = []
            for m in range(-1, b+1):
                left, right = max(Q(0), (m+D-phase)/b), min(Q(1), (m+1-D-phase)/b)
                if left <= right:
                    intervals.append((left, right))
            region = intersect(region, intervals)
        expected = sorted((c-4*epsilon) % 1 for c in (Q(1, 8), Q(1, 4), Q(3, 8), Q(5, 8), Q(3, 4), Q(7, 8)))
        assert region == tuple((c, c) for c in expected) and duration(region) == 0
        rigid.append({"epsilon": epsilon, "allowed": region})
    # Exact sharp local maximum at the sheared q=5 equality contact.
    t0, radius = Q(7, 16), Q(1, 1000)
    speeds = (5, 10, 15, 26, 66, 62, 122)
    peak_rows = []
    for s, controller, slope in ((-1, 62, Q(62)), (1, 66, -Q(66))):
        interval = tuple(sorted((t0, t0+s*radius)))
        rows = []
        for v in speeds:
            integer = floor(v*t0)
            phases = [v*t-integer for t in interval]
            assert all(0 <= z <= 1 for z in phases)
            lower = [D+slope*(t-t0) for t in interval]
            assert all(circular_distance(v*t) >= bound for t, bound in zip(interval, lower))
            rows.append({"speed": v, "phases": phases, "distance_lower_bounds": lower})
        assert all(circular_distance(controller*t) == D+slope*(t-t0) for t in interval)
        peak_rows.append({"side": s, "interval": interval, "controller": controller, "slope": slope, "rows": rows})
    return {"same_width_shear": True, "frozen_grid_controls": frozen_grid,
            "rigid_shifted_phase_control": {"terms_b_a_shift": rigid_terms, "profiles": rigid},
            "isolated_peak": {"q": 5, "time": t0, "radius": radius, "certificates": peak_rows}}


def figure(profiles):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"svg.hashsalt": "local-tiling-rule", "font.size": 10})
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.8, 5))
    # Sheared q=5 contact c=7/16. Only its local wedge is shown.
    left.fill_between([-1, 0], [.006, 0], [.013, 0], color="#82b89b", alpha=.7, label="Auxiliary opening")
    left.plot([-1, 1], [-.0002, .0002], color="#37434f", linewidth=2, label="Actual-time branch")
    left.scatter([0], [0], color="#9b4b27", zorder=5)
    left.annotate("Valid contact", xy=(0, 0), xytext=(.16, .004), arrowprops={"arrowstyle": "->"}, fontsize=9)
    left.set_xlabel("Core phase change epsilon (thousandths)")
    left.set_ylabel("Auxiliary phase minus 7/16")
    left.set_title("An opening the branch cannot enter here", loc="left", fontsize=11, fontweight="bold")
    left.legend(frameon=False, fontsize=9, loc="upper right")
    left.set_xlim(-1, 1)
    right.plot([-1, 0, 1], [.125-.062, .125, .125-.066], color="#247c66", linewidth=2.5)
    right.axhline(.125, color="#9b4b27", linestyle="--", label="Required separation: 1/8")
    right.scatter([0], [.125], color="#9b4b27", zorder=5)
    right.set_xlabel("Time change from 7/16 (thousandths)")
    right.set_ylabel("Minimum distance to reference runner")
    right.set_title("The actual contact is an isolated instant", loc="left", fontsize=11, fontweight="bold")
    right.set_yticks([.0625, .125], ["1/16", "1/8"])
    right.legend(frameon=False, loc="lower center", fontsize=9)
    for ax in (left, right):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=.15)
    fig.suptitle("A geometric opening and a reachable time are different conditions", x=.08, ha="left", fontsize=14)
    fig.text(.08, .025, "Eight common-start runners: 0, 5, 10, 15, 26, 62, 66, 122. Equality counts at t=7/16; strict intervals exist elsewhere.", fontsize=9)
    fig.subplots_adjust(left=.08, right=.98, top=.82, bottom=.20, wspace=.30)
    fig.savefig(ROOT/"figures/local_tiling_rule.svg", metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    profiles = []
    for name, coefficients, x0 in CASES:
        p = profile(name, coefficients, x0)
        p["chambers"] = [chamber_certificate(p, s) for s in (-1, 1)]
        controls = []
        for s in (-1, 1):
            for h in (Q(0), p["H"]/2, p["H"]):
                frozen = frozen_phase(p["terms"], x0+s*h)
                assert frozen["allowed_phases"] == phase_model(p, s, h)
                assert frozen["clear_phase_duration"] == p["K"]*h
                controls.append({"sign": s, "h": h, "allowed": frozen["allowed_phases"]})
        p["frozen_controls"] = controls
        p["residues"] = residue_certificate(p)
        values = sorted({3, 5, 6, max(3, p["sufficient_q"]-1), p["sufficient_q"], p["sufficient_q"]+1})
        p["actual_checks"] = [actual_check(p, q, True) for q in values]
        p["actual_checks"].append(actual_check(p, 100_003, False))
        print(name, "K=", p["K"], "H=", p["H"], "Q=", p["sufficient_q"],
              "period=", p["residue_period"], "q=", values, flush=True)
        profiles.append(p)
    controls = counterchecks(profiles)
    actual = [c for p in profiles for c in p["actual_checks"]]
    counts = {"specified_common_start_profiles": len(profiles), "parametric_chambers": 8,
              "affine_cells": 96, "runner_cell_certificates": 384, "vertex_phase_checks": 1536,
              "frozen_geometry_controls": 24, "residue_classes": sum(p["residue_period"] for p in profiles),
              "residue_comparisons_including_self": sum(6*p["residue_period"] for p in profiles),
              "full_boundary_and_local_model_comparisons": sum(c["complete"] for c in actual),
              "large_q_direct_checks": sum(not c["complete"] for c in actual),
              "strict_interval_certificates": sum(len(c["strict_interval_certificates"]) for c in actual),
              "isolated_contacts_in_complete_checks": sum(len(c["zero_contacts"]) for c in actual if c["complete"]),
              "frozen_actual_grid_controls": 6, "rigid_shifted_phase_controls": 3,
              "isolated_peak_side_certificates": 2}
    paths = ("scripts/analyze_local_tilings.py", *DEPENDENCIES)
    data = {"date_utc": "2026-09-25", "base_commit": BASE_COMMIT,
            "claim_status": "Finite exact checks OBSERVED; general local escape argument HYPOTHESIS/proof candidate, independent review pending; no novelty claim.",
            "selection": "Four specified profiles selected to preserve geometry while changing arithmetic, change the gap counts, and change the residue period. Six small q values per profile include 3,5,6 and below/at/above the sufficient cutoff; one direct q=100003 check per profile. Symmetry/repeated geometry is included, not independent samples.",
            "limits": "Conditional local escape at a strictly safe core phase with a rates-1,1,2,2 tiling; positive integer coefficients >=4, reference 0 only. Uniform q>=8 cutoff is a proof candidate, sufficient and not asserted sharp. q=3,5,6 are diagnostics, not an unbounded small-q theorem. No arbitrary-speed or all-reference theorem, no global maximum calculation. Existing helpers unchanged; broader regression suite not rerun. No independent review or wider novelty audit.",
            "profiles": profiles, "counterchecks": controls, "verification_counts": counts,
            "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
    (ROOT/"experiments/local_tilings.json").write_text(json.dumps(data, indent=2, default=str)+"\n")
    if args.figure:
        figure(profiles)
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
