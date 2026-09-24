"""Exact two-exceptional-runner comparisons; no speed-set scan.

Run: python -m scripts.analyze_two_perturbations [--figure]
Family: 0,q,...,5q,6q+a,7q+b; q>=3; a,b in {-1,1}.
Seven prescribed q values plus three explicitly constructed controls.
See notes/TWO_PERTURBATIONS.md for the unreviewed all-q arguments.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals
from scripts.analyze_core_transfer import boundary_certificate
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "ed4bc8e5ce37cbfdadf0683ff0967ecb54e9a82f"
D, L = Q(1, 8), Q(1, 6)
QS = (3, 4, 5, 6, 7, 8, 12)


def ceil(x):
    return -((-x.numerator) // x.denominator)


def family_speeds(q, a, b):
    return (*range(q, 6 * q, q), 6 * q + a, 7 * q + b)


def predicted_peaks(q, b):
    ranges = ({1: (q, 4 * q), 5: (2 * q, 5 * q)} if b == 1 else
              {1: (2 * q, 5 * q), 5: (q, 4 * q)})
    return tuple(Q(m, 6 * q) for m in range(1, 6 * q)
                 if m % 6 in ranges and ranges[m % 6][0] <= m <= ranges[m % 6][1])


def grid_profile(q, extras, x, threshold):
    """Classify every core-preserving choice; retain exact discrete overlap."""
    times = tuple((x + j) / q for j in range(q))
    blocked, equal, rows = [], [], []
    for w in extras:
        distances = tuple(circular_distance(w * t) for t in times)
        bad = {j for j, d in enumerate(distances) if d < threshold}
        equality = {j for j, d in enumerate(distances) if d == threshold}
        d = gcd(w, q)
        orbit_size = q // d
        bound = d * ceil(2 * threshold * orbit_size)
        assert len(bad) <= bound
        phases = {w * t % 1 for t in times}
        assert len(phases) == orbit_size
        rows.append({"speed": w, "gcd_with_q": d, "distinct_phases": orbit_size,
                     "blocked_indices": sorted(bad), "threshold_equal_indices": sorted(equality),
                     "individual_block_count_bound": bound})
        blocked.append(bad)
        equal.append(equality)
    both = blocked[0] & blocked[1]
    survivors = set(range(q)) - blocked[0] - blocked[1]
    count = q - len(blocked[0]) - len(blocked[1]) + len(both)
    assert len(survivors) == count
    lower = q - sum(row["individual_block_count_bound"] for row in rows)
    assert count >= lower
    for j in survivors:
        assert min(circular_distance(k * q * times[j]) for k in range(1, 6)) == L
    if all(gcd(w, q) == 1 for w in extras) and q >= 3 and threshold == D:
        assert lower == q - 2 * ceil(Q(q, 4)) > 0
    return {"core_phase": x, "threshold": threshold, "times": times,
            "runners": rows, "both_block_indices": sorted(both),
            "surviving_indices": sorted(survivors), "survivor_count": count,
            "counting_lower_bound": lower,
            "strict_surviving_indices": sorted(survivors - equal[0] - equal[1])
            if threshold < L else []}


def analyze(label, q, extras, family=None):
    speeds = (*range(q, 6 * q, q), *extras)
    assert min(speeds) > 0 and len(speeds) == len(set(speeds)) == 7
    full = feasible_intervals(speeds, D)
    independent = boundary_certificate(speeds)
    assert full == independent["complete_allowed_set"]
    maximum = exact_maximum(speeds)
    assert feasible_intervals(speeds, maximum.value) == tuple((t, t) for t in maximum.times)
    grids = [grid_profile(q, extras, x, threshold)
             for x, threshold in product((Q(1, 6), Q(5, 6)), (D, L))]
    if family:
        a, b = family
        assert q >= 3 and a in (-1, 1) and b in (-1, 1)
        assert maximum.value == L and maximum.times == predicted_peaks(q, b)
        residue = 1 if b == 1 else 5
        earliest_m = q + (residue - q) % 6
        assert maximum.times[0] == Q(earliest_m, 6 * q)
        for g in grids:
            assert g["survivor_count"] > 0
        # On the x=1/6 orbit, simultaneous 1/6 safety is a single half interval.
        left, right = (L, Q(2, 3)) if b == 1 else (Q(1, 3), Q(5, 6))
        g = grids[1]
        assert g["core_phase"] == L and g["threshold"] == L
        assert g["surviving_indices"] == [j for j, t in enumerate(g["times"]) if left <= t <= right]
        # A constructive witness without searching the q choices.
        j = ceil(q * left - L)
        witness = (L + j) / q
        assert 0 <= j < q and left <= witness < left + Q(1, q) <= right
        assert min(circular_distance(v * witness) for v in speeds) == L
    else:
        witness = maximum.times[0]
    result = {"label": label, "q": q, "extras": extras, "signs_a_b": family,
              "relative_speeds": speeds, "maximum": maximum.value,
              "all_maximizing_times": maximum.times,
              "earliest_maximum_t": maximum.times[0],
              "earliest_maximum_u": q * maximum.times[0], "grids": grids,
              "allowed_summary": {"clear_duration": duration(full),
                  "positive_components": sum(a < b for a, b in full),
                  "isolated_components": sum(a == b for a, b in full),
                  "sha256_json_string_endpoints": hashlib.sha256(json.dumps(full, default=str).encode()).hexdigest()}}
    if maximum.value > D:
        distances = {v: circular_distance(v * witness) for v in speeds}
        radius = (min(distances.values()) - D) / (2 * max(speeds))
        interval = (witness - radius, witness + radius)
        assert intersect(full, (interval,)) == (interval,)
        result["strict_witness"] = {"time": witness, "distances": distances,
            "interval": interval, "affine_certificate": phase_certificate(speeds, interval)}
    return result


def figure(cases):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    matplotlib.rcParams.update({"svg.hashsalt": "two-perturbations", "font.size": 11})
    selections = [("q3_a1_b1", L, "An opening survives"),
                  ("q2_grid_covered", D, "Every choice in this schedule is blocked"),
                  ("q4_ceiling_lost", D, "Equality survives at every choice")]
    colors = {"below": "#f5c8c2", "equal": "#f6df9b", "above": "#cce6d7"}
    fig, axes = plt.subplots(3, 1, figsize=(11, 8))
    for ax, (label, threshold, title) in zip(axes, selections):
        c = next(c for c in cases if c["label"] == label)
        q, extras = c["q"], c["extras"]
        times = tuple((L + j) / q for j in range(q))
        distances = [[circular_distance(v * t) for t in times] for v in extras]
        distances.append([min(L, *[row[j] for row in distances]) for j in range(q)])
        ax.set_axis_off()
        ax.set_title(f"{title}\nq = {q}; changed speeds {extras[0]}, {extras[1]}; target = {threshold}",
                     loc="left", fontsize=12, pad=8)
        cells = [[str(d) for d in row] for row in distances]
        fills = [[colors["below" if d < threshold else "equal" if d == threshold else "above"]
                  for d in row] for row in distances]
        table = ax.table(cellText=cells, cellColours=fills,
                         colLabels=[f"t = {t}" for t in times],
                         rowLabels=[f"Speed {v}" for v in extras] + ["Nearest to 0"],
                         cellLoc="center", rowLoc="center", bbox=[0.12, 0.1, 0.88, 0.72])
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        for cell in table.get_celld().values():
            cell.set_edgecolor("#ffffff")
            cell.set_linewidth(1.5)
    fig.suptitle("Two blockers: distinguish a chosen schedule from all possible times", fontsize=15)
    fig.text(0.5, 0.92, "At these times, the five core runners have the same positions and minimum distance 1/6.", ha="center", fontsize=10)
    fig.legend(handles=[Patch(facecolor=colors["below"], label="Below target: blocked"),
                        Patch(facecolor=colors["equal"], label="Exactly target: valid"),
                        Patch(facecolor=colors["above"], label="Above target")],
               loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.005))
    fig.tight_layout(rect=(0.025, 0.06, 0.985, 0.90), h_pad=2)
    target = ROOT / "figures/two_perturbations.svg"
    target.parent.mkdir(exist_ok=True)
    fig.savefig(target, metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    cases = []
    for q in QS:
        for a, b in product((-1, 1), repeat=2):
            cases.append(analyze(f"q{q}_a{a}_b{b}", q, (6 * q + a, 7 * q + b), (a, b)))
        for b in (-1, 1):
            minus, plus = [c for c in cases if c["q"] == q and c["signs_a_b"][1] == b]
            assert minus["all_maximizing_times"] == plus["all_maximizing_times"]
        print(f"q={q}: four sign choices pass complete maximum, grid, and interval checks", flush=True)
    controls = [analyze("q2_grid_covered", 2, (13, 19)),
                analyze("q4_ceiling_lost", 4, (27, 33)),
                analyze("q3_unchanged", 3, (18, 21))]
    covered, ceiling, unchanged = controls
    assert covered["maximum"] == Q(1, 7)
    assert all(g["survivor_count"] == 0 for g in covered["grids"])
    assert ceiling["maximum"] == Q(6, 37)
    for g in ceiling["grids"]:
        assert g["survivor_count"] == (4 if g["threshold"] == D else 0)
        assert g["strict_surviving_indices"] == []
    assert unchanged["maximum"] == D and unchanged["allowed_summary"]["clear_duration"] == 0
    # This q=2 sign combination has duplicate speeds; it is not an eight-runner input.
    assert len(set(family_speeds(2, 1, -1))) == 6
    cases.extend(controls)
    paths = ("scripts/analyze_two_perturbations.py", "lonely_runner/checker.py",
             "scripts/analyze_core_transfer.py", "scripts/analyze_local_overlap.py",
             "scripts/analyze_blocking_overlaps.py", "scripts/analyze_overlap_placement.py",
             "scripts/analyze_phase_discrepancy.py", "scripts/analyze_residual_overlap.py",
             "scripts/analyze_two_variable_speeds.py")
    counts = {"family_configurations": 4 * len(QS), "countercontrols": len(controls),
              "maximum_and_complete_peak_crosschecks": len(cases),
              "complete_boundary_reconstructions": len(cases),
              "grid_profiles": 4 * len(cases),
              "grid_choices_classified": sum(4 * c["q"] for c in cases),
              "individual_discrete_count_bounds": 8 * len(cases),
              "strict_interval_certificates": sum("strict_witness" in c for c in cases)}
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
            "scope": "Eight common-start runners, reference 0; five q-multiple core speeds, two exceptions. Main family q>=3, a,b=+-1; finite inputs q=3,4,5,6,7,8,12. Three explicit controls.",
            "selection": "q=3..8 covers all residues modulo 6 in the earliest-time formula; q=12 checks a doubled multiple of 6. q=2 tests the exact counting boundary; q=4 tests the stronger 1/6 ceiling and threshold equality. One unchanged q=3 baseline. No broad scan.",
            "time_convention": "Complete allowed sets and peaks use original t in [0,1]; normalized u=q*t. Core-preserving grids t=(x+j)/q, x=1/6 or 5/6, 0<=j<q.",
            "claim_status": {"finite_checks": "OBSERVED: exact rational computations.",
                "all_q_formulas_and_grid_bound": "HYPOTHESIS/proof candidates: elementary derivations; independent review outstanding.",
                "pre_jump_technique": "KNOWN; S15. S17 gives related modular two-runner results under different assumptions. No novelty claim.",
                "every_core_optimal_grid_always_has_a_threshold_survivor": "DISPROVEN by q=2, extras 13 and 19.",
                "two_coprime_exceptions_always_attain_core_ceiling": "DISPROVEN by q=4, extras 27 and 33."},
            "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "cases": cases, "verification_counts": counts,
            "limits": "No arbitrary-speed or all-reference theorem. Complete allowed unions are reconstructed twice in memory and summarized by exact durations, counts, and endpoint hashes. All peak times, all grid memberships, and strict interval certificates are retained. The infinite-family implication comes from the written arguments. Exact computations are not independent mathematical review."}
    (ROOT / "experiments/two_perturbations.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    if args.figure:
        figure(cases)
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
