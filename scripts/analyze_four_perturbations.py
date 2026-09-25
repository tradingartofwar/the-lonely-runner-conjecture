"""Four unit perturbations: continuous gaps and reachable time grids.

Run: python -m scripts.analyze_four_perturbations [--figure]
Six q values (3..8), all sixteen sign choices, and one unchanged control.
q=3..6 exhausts the finite remainder of the written q>=7 construction.
Exact Fractions certify every claim; optional Matplotlib draws the figure.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals
from scripts.analyze_core_transfer import boundary_certificate, merged
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "070a04996b8e51a77a7b81fdc61ca0d96e931499"
D = Q(1, 8)
QS = (3, 4, 5, 6, 7, 8)
SIGNS = tuple(product((-1, 1), repeat=4))


def floor(x):
    return x.numerator // x.denominator


def phase_profile(signs, x):
    """Exact frozen system; compare affine strips with boundary cells."""
    centres = tuple((-s * k * x) % 1 for k, s in zip(range(4, 8), signs))
    allowed = ((Q(0), Q(1)),)
    for c in centres:
        p = (-c) % 1
        windows = []
        for m in (0, 1):
            a, b = max(Q(0), m + D - p), min(Q(1), m + 1 - D - p)
            if a <= b:
                windows.append((a, b))
        allowed = intersect(allowed, windows)
    cuts = sorted({Q(0), Q(1), *((c + z * D) % 1 for c in centres for z in (-1, 1))})
    hist, individual, good = [Q(0)] * 5, [Q(0)] * 4, []
    for a, b in zip(cuts, cuts[1:]):
        t = (a + b) / 2
        bad = [circular_distance(k * x + s * t) < D for k, s in zip(range(4, 8), signs)]
        hist[sum(bad)] += b - a
        for i, flag in enumerate(bad):
            individual[i] += flag * (b - a)
        if not any(bad):
            good.append((a, b))
    good.extend((t, t) for t in cuts if all(circular_distance(k * x + s * t) >= D
                                        for k, s in zip(range(4, 8), signs)))
    assert merged(good) == allowed
    assert individual == [Q(1, 4)] * 4 and sum(hist) == 1
    redundancy = sum(max(m - 1, 0) * length for m, length in enumerate(hist))
    assert hist[0] == duration(allowed) == redundancy
    unique = sorted(set(centres))
    gaps = [(left, (unique[(i + 1) % len(unique)] - left) % 1 or Q(1))
            for i, left in enumerate(unique)]
    left, gap = max(gaps, key=lambda row: row[1])
    assert sum(max(g - Q(1, 4), 0) for start, g in gaps) == hist[0]
    return {"signs": signs, "core_phase": x, "centres": centres,
            "allowed_phases": allowed, "blocking_histogram": hist,
            "clear_phase_length": hist[0], "redundant_phase_blocking": redundancy,
            "largest_gap_start": left, "largest_gap_length": gap,
            "largest_gap_midpoint": (left + gap / 2) % 1}


def grid(q, signs, p):
    x = p["core_phase"]
    speeds = (q, 2 * q, 3 * q, *(k * q + s for k, s in zip(range(4, 8), signs)))
    times = tuple((x + j) / q for j in range(q))
    bad_sets = [set() for _ in range(4)]
    hist, survivors, strict = [0] * 5, [], []
    for j, t in enumerate(times):
        bad = []
        for i, (k, s) in enumerate(zip(range(4, 8), signs)):
            assert (k * q + s) * t % 1 == (k * x + s * t) % 1
            if circular_distance((k * q + s) * t) < D:
                bad.append(i)
                bad_sets[i].add(j)
        hist[len(bad)] += 1
        minimum = min(circular_distance(v * t) for v in speeds)
        assert (not bad) == (minimum >= D)
        assert (not bad) == any(a <= t <= b for a, b in p["allowed_phases"])
        if minimum >= D:
            survivors.append(j)
        if minimum > D:
            strict.append(j)
    T = sum(map(len, bad_sets))
    R = sum(max(m - 1, 0) * count for m, count in enumerate(hist))
    assert len(survivors) == hist[0] == q - T + R
    assert all(len(s) <= (q + 3) // 4 for s in bad_sets)
    return {"core_phase": x, "blocked_indices_by_runner": [sorted(s) for s in bad_sets],
            "blocking_count_histogram": hist, "total_blocked_indices_T": T,
            "redundant_blocking_R": R, "surviving_indices": survivors,
            "strict_surviving_indices": strict, "survivor_count_N": len(survivors)}


def classify(full, t):
    component = next(((a, b) for a, b in full if a <= t <= b), None)
    if component is None:
        return {"time": t, "classification": "blocked", "component": None}
    a, b = component
    status = "isolated" if a == b else "opens_right" if a == t else "opens_left" if b == t else "interior"
    return {"time": t, "classification": status, "component": component}


def analyze(q, signs, profiles):
    speeds = (q, 2 * q, 3 * q, *(k * q + s for k, s in zip(range(4, 8), signs)))
    assert len(set(speeds)) == 7 and min(speeds) > 0
    full = feasible_intervals(speeds, D)
    independent = boundary_certificate(speeds)
    assert full == independent["complete_allowed_set"]
    maximum = exact_maximum(speeds)
    assert feasible_intervals(speeds, maximum.value) == tuple((t, t) for t in maximum.times)
    reaches_quarter = signs[1] == -signs[3] and q % 4 == (1 if signs[1] == 1 else 3)
    assert (maximum.value == Q(1, 4)) == reaches_quarter
    if reaches_quarter:
        assert maximum.times == (Q(1, 4), Q(3, 4))
    grids = [grid(q, signs, profiles[x]) for x in (Q(1, 4), Q(1, 5))]
    for g in grids:
        reflected = grid(q, signs, profiles[1 - g["core_phase"]])
        assert reflected["surviving_indices"] == sorted(q - 1 - j for j in g["surviving_indices"])
        assert reflected["blocking_count_histogram"] == g["blocking_count_histogram"]
        for bad, other in zip(g["blocked_indices_by_runner"], reflected["blocked_indices_by_runner"]):
            assert other == sorted(q - 1 - j for j in bad)
    if signs[1] == signs[3]:
        assert grids[0]["survivor_count_N"] == (2 if q % 4 == 2 else 0)
        assert not grids[0]["strict_surviving_indices"]
    p = profiles[Q(1, 5)]
    centre = p["largest_gap_midpoint"]
    j = floor(q * centre - Q(1, 5) + Q(1, 2)) % q
    rounded = (Q(1, 5) + j) / q
    assert circular_distance(rounded - centre) <= Q(1, 2 * q)
    lower = min(Q(1, 5), p["largest_gap_length"] / 2 - Q(1, 2 * q))
    rounded_minimum = min(circular_distance(v * rounded) for v in speeds)
    assert rounded_minimum >= lower
    if q >= 7:
        assert lower >= Q(1, 5) - Q(1, 2 * q) > D
        witness = rounded
        method = "largest-gap rounding; in analytic q>=7 range"
    else:
        a, b = max(full, key=lambda ab: ab[1] - ab[0])
        assert a < b
        witness = (a + b) / 2
        method = "exact finite-remainder interval midpoint"
    distances = {v: circular_distance(v * witness) for v in speeds}
    minimum = min(distances.values())
    assert minimum > D
    radius = (minimum - D) / (2 * max(speeds))
    interval = (witness - radius, witness + radius)
    assert intersect(full, (interval,)) == (interval,)
    return {"q": q, "signs": signs, "relative_speeds": speeds,
            "maximum": maximum.value, "all_maximizing_times": maximum.times,
            "grids": grids, "reflected_grids_checked": True,
            "rounding_attempt": {"time": rounded, "minimum": rounded_minimum,
                                 "lower_bound": lower, "in_analytic_range": q >= 7},
            "strict_witness": {"method": method, "time": witness, "distances": distances,
                "interval": interval, "affine_certificate": phase_certificate(speeds, interval)},
            "allowed_summary": {"clear_duration": duration(full),
                "positive_components": sum(a < b for a, b in full),
                "isolated_components": sum(a == b for a, b in full),
                "sha256_json_string_endpoints": hashlib.sha256(json.dumps(full, default=str).encode()).hexdigest()}}


def figure(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    matplotlib.rcParams.update({"svg.hashsalt": "four-perturbations", "font.size": 10})
    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
    titles = ("Perfect tiling: no interval remains", "An opening exists, but the actual choices miss it",
              "A changed core position makes the opening reachable")
    for ax, row, title in zip(axes, rows, titles):
        p, g = row["phase"], row["grid"]
        x = p["core_phase"]
        for i, c in enumerate(p["centres"]):
            for shift in (-1, 0, 1):
                a, b = max(Q(0), c - D + shift), min(Q(1), c + D + shift)
                if a < b:
                    ax.broken_barh([(float(a), float(b - a))], (3 - i - 0.25, 0.5),
                                   facecolors="#cf7970", alpha=0.8)
        for a, b in p["allowed_phases"]:
            if a < b:
                ax.axvspan(float(a), float(b), color="#91c9a8", alpha=0.24)
            else:
                ax.scatter([float(a)], [-0.8], marker="|", color="#936800", s=100)
        for j in range(4):
            t = (x + j) / 4
            safe = j in g["surviving_indices"]
            color = "#247747" if safe else "#343c48"
            ax.axvline(float(t), color=color, linestyle=":" if not safe else "-", alpha=0.7)
            ax.scatter([float(t)], [-0.8], color=color, s=28, zorder=4)
            ax.text(float(t), -1.1, str(t), ha="center", va="top", fontsize=9)
        ax.set_yticks([3, 2, 1, 0], ["17", "21", "25", "29"])
        ax.set_ylabel("Changed speed")
        ax.set_ylim(-1.65, 3.5)
        ax.set_xlim(0, 1)
        ax.set_title(f"{title}\nx = {x}; clear phase length {p['clear_phase_length']}; "
                     f"discrete T = {g['total_blocked_indices_T']}, R = {g['redundant_blocking_R']}, "
                     f"survivors N = {g['survivor_count_N']}", loc="left", fontsize=11)
    axes[-1].set_xlabel("Auxiliary phase τ; dots mark actual times at this core position")
    fig.suptitle("Four blockers: an opening must meet the actual time grid", fontsize=15)
    fig.text(0.5, 0.925, "One configuration: 0,4,8,12,17,21,25,29. Threshold 1/8; core position x = 4t mod 1.",
             ha="center", fontsize=10)
    fig.legend(handles=[Patch(facecolor="#cf7970", label="Blocked phase (open endpoints)"),
                        Patch(facecolor="#91c9a8", alpha=0.5, label="Allowed interval"),
                        Line2D([], [], linestyle="none", marker="|", color="#936800",
                               markersize=10, label="Allowed isolated phase")],
               loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.005))
    fig.tight_layout(rect=(0, 0.06, 1, 0.90), h_pad=1.2)
    target = ROOT / "figures/four_perturbations.svg"
    target.parent.mkdir(exist_ok=True)
    fig.savefig(target, metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    cache, phase_rows = {}, []
    for signs in SIGNS:
        profiles = {x: phase_profile(signs, x) for x in (Q(1, 4), Q(3, 4), Q(1, 5), Q(4, 5))}
        p = profiles[Q(1, 4)]
        if signs[1] == signs[3]:
            assert p["allowed_phases"] == tuple((Q(r, 8), Q(r, 8)) for r in (1, 3, 5, 7))
        else:
            expected = (((Q(1, 8), Q(3, 8)), (Q(5, 8), Q(5, 8)), (Q(7, 8), Q(7, 8)))
                        if signs[1] == 1 else
                        ((Q(1, 8), Q(1, 8)), (Q(3, 8), Q(3, 8)), (Q(5, 8), Q(7, 8))))
            assert p["allowed_phases"] == expected
        fifth = profiles[Q(1, 5)]
        assert all((5 * c).denominator == 1 for c in fifth["centres"])
        assert fifth["largest_gap_length"] >= Q(2, 5)
        assert fifth["clear_phase_length"] >= Q(3, 20)
        for x in (Q(1, 4), Q(1, 5)):
            assert profiles[1 - x]["allowed_phases"] == tuple(sorted((1 - b, 1 - a) for a, b in profiles[x]["allowed_phases"]))
        cache[signs] = profiles
        phase_rows.extend(profiles.values())
    cases = []
    for q in QS:
        cases.extend(analyze(q, signs, cache[signs]) for signs in SIGNS)
        print(f"q={q}: all sixteen signs pass complete maxima, grids, and strict certificates", flush=True)
    comparison = []
    for x in (Q(1, 4), Q(1, 5), Q(2, 11)):
        signs = (1, 1, 1, 1)
        p = phase_profile(signs, x)
        g = grid(4, signs, p)
        comparison.append({"phase": p, "grid": g})
    assert [(r["phase"]["clear_phase_length"], r["grid"]["redundant_blocking_R"],
             r["grid"]["survivor_count_N"]) for r in comparison] == [(Q(0), 0, 0), (Q(3, 20), 0, 0), (Q(9, 44), 1, 1)]
    extra_reflected = phase_profile((1, 1, 1, 1), Q(9, 11))
    assert grid(4, (1, 1, 1, 1), extra_reflected)["survivor_count_N"] == 1
    contacts = []
    for signs, status in (((1, 1, 1, 1), "isolated"), ((1, 1, -1, 1), "opens_right")):
        speeds = (6, 12, 18, *(6 * k + s for k, s in zip(range(4, 8), signs)))
        full = feasible_intervals(speeds, D)
        row = classify(full, Q(3, 8))
        assert row["classification"] == status
        row.update({"signs": signs, "speeds": speeds,
                    "blocking_ends": [v for v in speeds if v * Q(3, 8) % 1 == D],
                    "blocking_starts": [v for v in speeds if v * Q(3, 8) % 1 == 1 - D]})
        contacts.append(row)
    assert contacts[1]["component"] == (Q(3, 8), Q(55, 144))
    baseline_speeds = tuple(4 * k for k in range(1, 8))
    baseline_full = feasible_intervals(baseline_speeds, D)
    baseline_max = exact_maximum(baseline_speeds)
    assert baseline_max.value == D and duration(baseline_full) == 0
    assert baseline_full == boundary_certificate(baseline_speeds)["complete_allowed_set"]
    assert baseline_full == tuple((t, t) for t in baseline_max.times)
    paths = ("scripts/analyze_four_perturbations.py", "lonely_runner/checker.py",
             "scripts/analyze_core_transfer.py", "scripts/analyze_local_overlap.py",
             "scripts/analyze_blocking_overlaps.py", "scripts/analyze_overlap_placement.py",
             "scripts/analyze_phase_discrepancy.py", "scripts/analyze_residual_overlap.py",
             "scripts/analyze_two_variable_speeds.py")
    counts = {"family_configurations": len(cases), "unchanged_controls": 1,
              "maximum_full_peak_crosschecks": len(cases) + 1,
              "complete_boundary_reconstructions": len(cases) + 1,
              "distinct_frozen_phase_profiles": len(phase_rows) + 2,
              "distinct_actual_grid_profiles": 4 * len(cases) + 2,
              "actual_grid_choices": 4 * sum(c["q"] for c in cases) + 8,
              "finite_remainder_certificates": sum(c["q"] < 7 for c in cases),
              "analytic_range_diagnostics": sum(c["q"] >= 7 for c in cases),
              "strict_interval_certificates": len(cases),
              "quarter_ceiling_cases": sum(c["maximum"] == Q(1, 4) for c in cases),
              "selected_contact_classifications": len(contacts)}
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
            "scope": "Eight common-start runners; reference 0; 0,q,2q,3q,4q+s4,...,7q+s7; q>=3 integer, each s=+-1. Exact finite computations only q=3..8 and the stated control.",
            "selection": "q=3..6 exhausts the 64-case remainder below the analytic q>=7 bound; q=7,8 tests that bound and its neighbor. All 16 sign choices are required. The q=4 all-plus phase comparison and q=6 contact comparison reuse configurations. No broad scan.",
            "claim_status": {"finite_checks": "OBSERVED: exact rational calculations.",
                "all_q_strictness": "HYPOTHESIS/proof candidate: analytic construction for q>=7 plus 64 explicit rational certificates for q=3..6; independent review outstanding.",
                "phase_geometry_and_ceiling_classification": "HYPOTHESIS/proof candidates; no novelty claim.",
                "positive_auxiliary_gap_always_hits_actual_grid": "DISPROVEN by q=4 all-plus at x=1/5.",
                "auxiliary_singleton_must_be_actual_singleton": "DISPROVEN by q=6 signs (+,+,-,+) at t=3/8."},
            "time_convention": "Frozen x=q*t mod1; auxiliary phase tau is varied independently for geometry. Actual times at this x are only tau=t=(x+j)/q, j=0..q-1. Complete actual results use t in [0,1].",
            "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "phase_profiles": phase_rows, "cases": cases, "q4_all_plus_comparison": comparison,
            "q6_contact_controls": contacts,
            "unchanged_control": {"q": 4, "speeds": baseline_speeds, "maximum": baseline_max.value,
                                  "complete_allowed_set": baseline_full},
            "verification_counts": counts,
            "limits": "The all-q claim relies on the written finite reduction, not extrapolation. No formula for the general maximum is claimed except the exact 1/4-attainment classification. All witnesses concern reference 0 only. Complete actual allowed unions are independently reconstructed and summarized by exact counts, duration, and hashes. Existing helpers are unchanged. No independent mathematical review or novelty claim."}
    (ROOT / "experiments/four_perturbations.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    if args.figure:
        figure(comparison)
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
