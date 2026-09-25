"""Mixed-sign offsets: local tiling escape and actual contact classification.

Run: python -m scripts.analyze_signed_tilings [--figure]
Four prescribed signed profiles, six small q values each, and direct large-q
certificates. No coefficient-box scan. See SIGNED_TILING_RULE.md for scope.
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
from scripts.analyze_local_overlap import intersect
from scripts.analyze_two_variable_speeds import phase_certificate
from scripts.analyze_local_tilings import chamber_certificate, phase_model
from scripts.analyze_local_tilings import DEPENDENCIES as PRIOR_DEPENDENCIES

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "3615cdeb8cc99e5d582494108ae3049076cf267b"
DEPENDENCIES = (*PRIOR_DEPENDENCIES, "scripts/analyze_local_tilings.py")
D = Q(1, 8)
CASES = (
    ("all_negative_control", (-4, -12, -10, -22), Q(3, 16)),
    ("mixed_unreachable_tiling", (4, -4, -6, 6), Q(3, 16)),
    ("mixed_contact_types", (-11, 13, -4, 8), Q(3, 16)),
    ("mixed_period_24", (4, -8, -13, 5), Q(5, 24)),
)
SMALL_Q = (5, 7, 9, 16, 17, 18)


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def sign(x):
    return 1 if x > 0 else -1


def actual_speeds(p, q):
    speeds = (q, 2*q, 3*q, *(abs(a)*q+sign(a)*b for b, a in p["terms"]))
    assert q >= 5 and min(speeds) > 0 and len(set(speeds)) == 7
    return speeds


def profile(name, coefficients, x0):
    assert all(isinstance(a, int) and abs(a) >= 4 for a in coefficients)
    terms = tuple(zip((1, 1, 2, 2), coefficients))
    frozen = frozen_phase(terms, x0)
    assert frozen["clear_phase_duration"] == 0
    assert all(circular_distance(k*x0) > D for k in (1, 2, 3))
    assert ((coefficients[1]-coefficients[0])*x0) % 1 == Q(1, 2)
    assert sorted(((a-2*coefficients[0])*x0) % 1 for a in coefficients[2:]) == [Q(3, 8), Q(5, 8)]
    blocks = []
    for i, (b, a) in enumerate(terms):
        for m in range(b):
            left = ((m-a*x0-D)/b) % 1
            blocks.append({"left": left, "right": left+2*D/b, "runner": i, "r": Q(a, b)})
    blocks.sort(key=lambda row: row["left"])
    contacts, gaps = [], []
    for i, left in enumerate(blocks):
        right = blocks[(i+1) % len(blocks)]
        assert left["right"] == right["left"]+(i == len(blocks)-1)
        c, delta = left["right"] % 1, left["r"]-right["r"]
        assert delta != 0
        s = sign(delta)
        kind = "isolated" if left["r"]*right["r"] > 0 else "starts_interval" if s == 1 else "ends_interval"
        contacts.append({"contact": c, "left_runner": left["runner"], "right_runner": right["runner"],
                         "left_r": left["r"], "right_r": right["r"], "delta": delta, "contact_kind": kind})
        gaps.append({"contact": c, "sign": s, "A": max(left["r"], right["r"]),
                     "B": min(left["r"], right["r"]), "left_r": left["r"], "right_r": right["r"]})
    contacts.sort(key=lambda c: c["contact"])
    gaps.sort(key=lambda c: c["contact"])
    assert len(set(Q(a, b) for b, a in terms)) == 4
    assert sum(c["delta"] for c in contacts) == 0
    K = sum(abs(c["delta"]) for c in contacts)/2
    M = max(abs(Q(a, b)) for b, a in terms)
    d = x0.denominator
    assert d % 8 == 0 and d <= 2*abs(coefficients[1]-coefficients[0]) <= 4*M
    core_radius = min(min((k*x0) % 1-D, 1-D-(k*x0) % 1)/k for k in (1, 2, 3))
    assert core_radius >= Q(1, 3*d) >= 1/(12*M)
    H = 1/(16*M+1)
    collisions = []
    for i, c in enumerate(contacts):
        nxt = contacts[(i+1) % len(contacts)]
        distance = nxt["contact"]-c["contact"]+(i == len(contacts)-1)
        relative = max(abs(a-b) for a in (c["left_r"], c["right_r"])
                       for b in (nxt["left_r"], nxt["right_r"]))
        assert distance >= D and relative <= 2*M
        assert relative*H < distance
        collisions.append({"spacing": distance, "max_relative_velocity": relative,
                           "remaining_spacing_at_H": distance-relative*H})
    assert 1/(17*M-1) < H < core_radius
    return {"name": name, "terms": terms, "x0": x0, "tiling_profile": frozen,
            "blocks": blocks, "contacts": contacts, "gaps": gaps, "K": K, "M": M, "H": H,
            "residue_period": lcm(*(c["contact"].denominator for c in contacts)),
            "uniform_bound_certificate": {"x0_denominator": d, "denominator_upper_bound": 4*M,
                "core_radius": core_radius, "core_radius_lower_bound": 1/(12*M),
                "collision_bounds": collisions, "q17_entry_bound": 1/(17*M-1), "sufficient_q": 17}}


def relative_slopes(g, q):
    low = -g["sign"]*(g["left_r"]+Q(1, q))
    high = -g["sign"]*(g["right_r"]+Q(1, q))
    assert low < high and low != 0 and high != 0
    return low, high


def solve_wedge(low, high, displacement, H):
    """Solve low*h <= displacement <= high*h exactly, for 0<=h<=H."""
    lo, hi = Q(0), H
    if low > 0:
        hi = min(hi, displacement/low)
    else:
        lo = max(lo, displacement/low)
    if high > 0:
        lo = max(lo, displacement/high)
    else:
        hi = min(hi, displacement/high)
    return (lo, hi) if lo <= hi else None


def nearest_candidates(p, q):
    rows = []
    for g in p["gaps"]:
        z = q*g["contact"]-p["x0"]
        integers = {ceil(z)-1, floor(z)+1}
        if z.denominator == 1:
            integers.add(int(z))
        low, high = relative_slopes(g, q)
        for j in sorted(integers):
            displacement = (j-z)/q
            interval = solve_wedge(low, high, displacement, p["H"])
            rows.append({"contact": g["contact"], "sign": g["sign"], "raw_j": j, "j": j % q,
                         "relative_slopes": (low, high), "initial_displacement": displacement,
                         "h_interval": interval})
    return rows


def time_interval(p, q, row):
    lo, hi = row["h_interval"]
    return tuple(sorted(((p["x0"]+row["sign"]*lo+row["j"])/q,
                         (p["x0"]+row["sign"]*hi+row["j"])/q)))


def extreme_construction(p, q):
    M = p["M"]
    g = next(g for g in p["gaps"] if max(abs(g["left_r"]), abs(g["right_r"])) == M)
    r = next(r for r in (g["left_r"], g["right_r"]) if abs(r) == M)
    edge = -g["sign"]*(r+Q(1, q))
    low, high = relative_slopes(g, q)
    assert (edge == high and edge > 0) or (edge == low and edge < 0)
    z = q*g["contact"]-p["x0"]
    j = floor(z)+1 if edge > 0 else ceil(z)-1
    displacement = (j-z)/q
    assert 0 < abs(displacement) <= Q(1, q)
    entry = displacement/edge
    assert 0 < entry <= 1/(q*M-1)
    interval = solve_wedge(low, high, displacement, p["H"])
    if q >= 17:
        assert interval and interval[0] == entry < interval[1] <= p["H"]
    return {"contact": g["contact"], "sign": g["sign"], "j": j % q, "raw_j": j,
            "extreme_ratio": r, "relative_edge_velocity": edge,
            "entry_h": entry, "entry_bound": 1/(q*M-1), "h_interval": interval}


def complete_local_model(p, q):
    result = []
    for g in p["gaps"]:
        low, high = relative_slopes(g, q)
        for shift in (-1, 0, 1):
            for j in range(q):
                displacement = (p["x0"]+j)/q-g["contact"]-shift
                interval = solve_wedge(low, high, displacement, p["H"])
                if interval:
                    result.append(time_interval(p, q, {"j": j, "sign": g["sign"], "h_interval": interval}))
    return merged(result)


def interval_certificate(speeds, interval):
    midpoint = sum(interval)/2
    minimum = min(circular_distance(v*midpoint) for v in speeds)
    assert minimum > D
    return {"interval": interval, "midpoint": midpoint, "strict_minimum": minimum,
            "phase_certificate": phase_certificate(speeds, interval)}


def actual_check(p, q, complete):
    speeds = actual_speeds(p, q)
    candidates = nearest_candidates(p, q)
    positive = [r for r in candidates if r["h_interval"] and r["h_interval"][0] < r["h_interval"][1]]
    nearest = min(positive, key=lambda r: r["h_interval"][0]) if positive else None
    zero = [c for c in p["contacts"] if (q*c["contact"]-p["x0"]).denominator == 1]
    extreme = extreme_construction(p, q)
    result = {"q": q, "complete": complete, "speeds": speeds, "nearest_candidates": candidates,
              "nearest_positive_component": nearest, "zero_contacts": zero, "extreme_construction": extreme,
              "certificates": []}
    if nearest:
        result["certificates"].append(interval_certificate(speeds, time_interval(p, q, nearest)))
    if q >= 17:
        assert nearest
        result["certificates"].append(interval_certificate(speeds, time_interval(p, q, extreme)))
    if complete:
        full = feasible_intervals(speeds, D)
        assert full == boundary_certificate(speeds)["complete_allowed_set"]
        windows = tuple(((p["x0"]-p["H"]+j)/q, (p["x0"]+p["H"]+j)/q) for j in range(q))
        local = intersect(full, windows)
        assert local == complete_local_model(p, q)
        distance = []
        for j, window in enumerate(windows):
            for a, b in intersect(full, (window,)):
                if a < b:
                    distance.extend((abs(q*a-j-p["x0"]), abs(q*b-j-p["x0"])))
        assert bool(distance) == bool(nearest)
        if distance:
            assert min(distance) == nearest["h_interval"][0]
        classified = []
        for c in zero:
            t = c["contact"]
            component = next((a, b) for a, b in full if a <= t <= b)
            a, b = component
            if c["contact_kind"] == "isolated":
                assert a == b == t
            elif c["contact_kind"] == "starts_interval":
                assert a == t < b
            else:
                assert a < t == b
            classified.append({"contact": t, "kind": c["contact_kind"], "full_component": component})
        result["classified_contacts"] = classified
        result["complete_local_allowed_intervals"] = local
        result["full_component_count"] = len(full)
    return result


def residue_contacts(p):
    rows = []
    for residue in range(p["residue_period"]):
        q = residue+p["residue_period"]
        speeds = actual_speeds(p, q)
        contacts = []
        for c in p["contacts"]:
            t = c["contact"]
            if (q*t-p["x0"]).denominator != 1:
                continue
            phases = [v*t % 1 for v in speeds]
            active = [v for v in speeds if circular_distance(v*t) == D]
            assert len(active) == 2 and all(circular_distance(v*t) >= D for v in speeds)
            active_phases = [v*t % 1 for v in active]
            if c["contact_kind"] == "isolated":
                assert sorted(active_phases) == [D, 1-D]
                assert ((active[0]+active[1])*t).denominator == 1
            else:
                assert active_phases == ([D, D] if c["contact_kind"] == "starts_interval" else [1-D, 1-D])
                assert ((active[0]-active[1])*t).denominator == 1
            contacts.append({"contact": t, "kind": c["contact_kind"], "active_speeds": active,
                             "active_phases": active_phases, "all_phases": phases})
        rows.append({"q_mod_period": residue, "representative_q": q, "contacts": contacts})
    return rows


def contact_figures(p):
    result = []
    for q, t0, expected in ((5, Q(7, 16), "ends_interval"), (7, Q(5, 16), "starts_interval"), (9, Q(11, 16), "isolated")):
        case = next(c for c in p["actual_checks"] if c["q"] == q)
        hit = next(c for c in case["classified_contacts"] if c["contact"] == t0)
        assert hit["kind"] == expected
        speeds = case["speeds"]
        radius = Q(1, 100*max(speeds))
        pieces = []
        for s in (-1, 1):
            endpoint = t0+s*radius
            controller = min(speeds, key=lambda v: circular_distance(v*endpoint))
            slope = (circular_distance(controller*endpoint)-D)/(s*radius)
            interval = tuple(sorted((t0, endpoint)))
            rows = []
            for v in speeds:
                m = floor(v*t0)
                phases = [v*t-m for t in interval]
                lower = [D+slope*(t-t0) for t in interval]
                assert all(0 <= z <= 1 for z in phases)
                assert all(circular_distance(v*t) >= d for t, d in zip(interval, lower))
                rows.append({"speed": v, "phases": phases, "distance_lower_bounds": lower})
            phases = [controller*t-floor(controller*t0) for t in interval]
            assert max(phases) <= Q(1, 2) or min(phases) >= Q(1, 2)
            assert circular_distance(controller*t0) == D
            pieces.append({"side": s, "interval": interval, "controller": controller, "slope": slope, "rows": rows})
        active = [v for v in speeds if circular_distance(v*t0) == D]
        result.append({"q": q, "time": t0, "kind": expected, "radius": radius, "pieces": pieces,
                       "full_component": hit["full_component"], "active_speeds": active,
                       "sum_times_contact": sum(active)*t0, "difference_times_contact": (active[0]-active[1])*t0})
    return result


def figure(examples):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"svg.hashsalt": "signed-tiling-rule", "font.size": 10})
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True)
    titles = {"ends_interval": "An interval ends", "starts_interval": "An interval begins", "isolated": "An isolated instant"}
    for ax, row in zip(axes, examples):
        rad = row["radius"]
        heights = [float(D-row["pieces"][0]["slope"]*rad), float(D), float(D+row["pieces"][1]["slope"]*rad)]
        ax.plot([-1, 0, 1], heights, color="#247c66", linewidth=2.5)
        ax.axhline(float(D), color="#9b4b27", linestyle="--", linewidth=1.2)
        ax.scatter([0], [float(D)], color="#9b4b27", zorder=5)
        if row["kind"] != "isolated":
            ax.axvspan(-1 if row["kind"] == "ends_interval" else 0,
                       0 if row["kind"] == "ends_interval" else 1, color="#96c5a7", alpha=.16)
        ax.set_title(titles[row["kind"]]+f"\nq={row['q']}, t={row['time']}", loc="left", fontsize=11, fontweight="bold")
        ax.set_xlabel("Time change / local radius")
        ax.set_xticks([-1, 0, 1])
        ax.grid(alpha=.15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes[0].set_ylabel("Minimum distance to reference runner")
    axes[0].set_yticks([.115, .125, .135], ["1/8 - .01", "1/8", "1/8 + .01"])
    fig.suptitle("An exact threshold contact has three possible local behaviors", x=.09, ha="left", fontsize=14)
    fig.text(.09, .025, "One mixed-offset family: 0, q, 2q, 3q, 11q-1, 13q+1, 4q-2, 8q+2. Green shading marks strict separation.", fontsize=9)
    fig.subplots_adjust(left=.09, right=.98, top=.76, bottom=.20, wspace=.24)
    fig.savefig(ROOT/"figures/signed_tiling_rule.svg", metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    profiles = []
    for name, coefficients, x0 in CASES:
        p = profile(name, coefficients, x0)
        p["chambers"] = [chamber_certificate(p, s) for s in (-1, 1)]
        frozen_controls = []
        for s in (-1, 1):
            for h in (Q(0), p["H"]/2, p["H"]):
                f = frozen_phase(p["terms"], x0+s*h)
                assert f["allowed_phases"] == phase_model(p, s, h)
                assert f["clear_phase_duration"] == p["K"]*h
                frozen_controls.append({"sign": s, "h": h, "allowed": f["allowed_phases"]})
        p["frozen_controls"] = frozen_controls
        p["residue_contacts"] = residue_contacts(p)
        p["actual_checks"] = [actual_check(p, q, True) for q in SMALL_Q]
        p["actual_checks"].append(actual_check(p, 100_003, False))
        print(name, "K=", p["K"], "M=", p["M"], "H=", p["H"], "period=", p["residue_period"], flush=True)
        profiles.append(p)
    examples = contact_figures(profiles[2])
    positive = profile("positive_compatibility", (4, 12, 10, 22), Q(3, 16))
    positive_check = actual_check(positive, 8, True)
    actual = [c for p in profiles for c in p["actual_checks"]]
    counts = {"specified_signed_profiles": 4, "parametric_chambers": 8, "affine_cells": 96,
              "runner_cell_certificates": 384, "vertex_phase_checks": 1536,
              "frozen_geometry_controls": 24, "contact_residue_classes": sum(p["residue_period"] for p in profiles),
              "full_boundary_and_local_model_comparisons": sum(c["complete"] for c in actual),
              "positive_compatibility_full_comparisons": 1, "large_q_direct_checks": 4,
              "strict_interval_certificates": sum(len(c["certificates"]) for c in actual)+len(positive_check["certificates"]),
              "classified_contacts_in_complete_checks": sum(len(c.get("classified_contacts", [])) for c in actual),
              "uniform_extreme_construction_certificates": sum(c["q"] >= 17 for c in actual),
              "exact_contact_curve_sides": 6}
    paths = ("scripts/analyze_signed_tilings.py", *DEPENDENCIES)
    data = {"date_utc": "2026-09-25", "base_commit": BASE_COMMIT,
            "claim_status": "OBSERVED for stated finite checks; uniform q>=17 and general contact classification are HYPOTHESIS/proof candidates pending independent review. No novelty claim.",
            "scope": "Eight common-start runners, reference 0, threshold 1/8, equality counts. Positive coefficients a_i>=4 with signed offsets sigma_i*b_i, b=(1,1,2,2); actual q>=5. Requires a tiling at a strictly safe core phase. No claim that q>=8 fails in the larger class.",
            "selection": "Four prescribed normalized coefficient vectors, six q values 5,7,9,16,17,18 each and one direct q=100003 check. One q=8 positive-offset compatibility check. No coefficient-box or sampled-time search. Repeated geometry is not independent evidence.",
            "limits": "Uniform 17 is sufficient, not asserted sharp. Does not cover arbitrary offsets, absence of tiling, unsafe cores, all references, or the full conjecture. Existing helpers unchanged; broader regression suite not rerun. No independent review or wider novelty audit.",
            "profiles": profiles, "positive_compatibility": positive_check, "contact_examples": examples,
            "verification_counts": counts,
            "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
    (ROOT/"experiments/signed_tilings.json").write_text(json.dumps(data, indent=2, default=str)+"\n")
    if args.figure:
        figure(examples)
    print(json.dumps(counts, indent=2))
    for row in examples:
        print(row["q"], row["time"], row["kind"], row["full_component"], row["active_speeds"])


if __name__ == "__main__":
    main()
