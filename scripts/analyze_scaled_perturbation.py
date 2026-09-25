"""Exact prescribed comparisons of 0,q,...,6q,7q+s, s=-1,0,1.

Run: python -m scripts.analyze_scaled_perturbation [--figure]
All certification uses Fractions. Optional plotting converts exact curve
vertices to floats for display only. See notes/SCALED_PERTURBATION.md.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals
from scripts.analyze_core_transfer import boundary_certificate
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "ff422cbc30ef0625c04b5af5c1961ab41df9da59"
D = Q(1, 8)
QS = (2, 3, 4, 7, 9, 11, 14, 29, 37)
CORE_WINDOWS = ((Q(1, 8), Q(7, 48)), (Q(9, 32), Q(7, 24)),
                (Q(3, 8), Q(3, 8)), (Q(17, 40), Q(7, 16)),
                (Q(9, 16), Q(23, 40)), (Q(5, 8), Q(5, 8)),
                (Q(17, 24), Q(23, 32)), (Q(41, 48), Q(7, 8)))


def old_prediction(t, r, s):
    if s == 0:
        return "isolated"
    plus = {1: t > Q(1, 4), 3: t < Q(1, 4) or t > Q(1, 2),
            5: t < Q(1, 2) or t > Q(3, 4), 7: t < Q(3, 4)}
    minus = {1: t < Q(3, 4), 3: t < Q(1, 2) or t > Q(3, 4),
             5: t < Q(1, 4) or t > Q(1, 2), 7: t > Q(1, 4)}
    if not (plus if s == 1 else minus)[r]:
        return "blocked"
    return {1: "opens_right", 3: "isolated", 5: "isolated", 7: "opens_left"}[r]


def new_contacts(q, s):
    """Closed-form endpoint congruences; no search over times."""
    result = []
    for modulus, plus, minus, t in ((48, 11, 37, Q(5, 48)),
                                  (32, 29, 3, Q(3, 32)),
                                  (16, 7, 9, Q(1, 16))):
        if s and q % modulus == (plus if s == 1 else minus):
            result.extend((t, 1 - t))
    assert len(result) <= 2
    return tuple(sorted(result))


def compare(q, s):
    speeds = (*range(q, 7 * q, q), 7 * q + s)
    old = [(Q(8 * j + r, 8 * q), r) for j in range(q) for r in (1, 3, 5, 7)]
    old_times = {t for t, r in old}
    full = feasible_intervals(speeds, D)
    boundary = boundary_certificate(speeds)
    assert boundary["complete_allowed_set"] == full
    maximum = exact_maximum(speeds)
    expected_maximum = Q(1, 8) if s == 0 else Q(1, 7)
    peaks = (tuple(sorted(old_times)) if s == 0 else
             tuple(Q(m, 7 * q) for m in range(q, 6 * q + 1) if m % 7))
    assert maximum.value == expected_maximum and maximum.times == peaks
    assert feasible_intervals(speeds, maximum.value) == tuple((t, t) for t in peaks)
    if s:
        assert len(peaks) == 5 * q + 1 - ((6 * q) // 7 - (q - 1) // 7)
    classified = {key: [] for key in ("blocked", "isolated", "opens_left", "opens_right")}
    for t, r in old:
        components = [(a, b) for a, b in full if a <= t <= b]
        assert len(components) <= 1
        if not components:
            category = "blocked"
        else:
            a, b = components[0]
            if a == b:
                category = "isolated"
            elif a == t < b:
                category = "opens_right"
            elif a < t == b:
                category = "opens_left"
            else:
                raise AssertionError("An original touch cannot become an interior point")
        assert category == old_prediction(t, r, s)
        if s:
            assert circular_distance((7 * q + s) * t) != D
        classified[category].append(t)
    counts = {key: len(value) for key, value in classified.items()}
    if s:
        side_count = (3 * q) // 4 if s == 1 else (3 * q + 3) // 4
        singleton_count = (2 * ((q + 2) // 4 + q // 2) if s == 1 else
                           2 * ((q + 1) // 2 + (q + 1) // 4))
        assert counts["opens_left"] == counts["opens_right"] == side_count
        assert counts["isolated"] == singleton_count
    singletons = tuple(a for a, b in full if a == b)
    expected_new = new_contacts(q, s)
    assert singletons == tuple(sorted((*classified["isolated"], *expected_new)))
    positive = [(a, b) for a, b in full if a < b]
    new_intervals = [(a, b) for a, b in positive if not any(a <= t <= b for t in old_times)]
    assert all(sum(a <= t <= b for t in old_times) <= 1 for a, b in positive)
    assert len(new_intervals) == len(positive) - counts["opens_left"] - counts["opens_right"]
    result = {"q": q, "s": s, "relative_speeds": speeds,
              "maximum": maximum.value, "all_maximizing_times": peaks,
              "earliest_maximum_t": peaks[0], "earliest_maximum_u": q * peaks[0],
              "old_touch_classification": classified, "old_touch_counts": counts,
              "new_isolated_contacts": [c for c in boundary["isolated_contact_certificates"]
                                        if c["time"] in expected_new],
              "allowed_summary": {"positive_components": len(positive),
                  "isolated_components": len(singletons), "clear_duration": duration(full),
                  "new_positive_components_without_old_touch": len(new_intervals),
                  "first_new_positive_component": new_intervals[0] if new_intervals else None,
                  "sha256_json_string_endpoints": hashlib.sha256(json.dumps(full, default=str).encode()).hexdigest(),
                  "boundary_count": boundary["boundary_count"]}}
    if s:
        m = q + (q % 7 == 0)
        t = Q(m, 7 * q)
        assert peaks[0] == t
        distances = {v: circular_distance(v * t) for v in speeds}
        assert min(distances.values()) == Q(1, 7)
        radius = Q(1, 112 * max(speeds))
        interval = (t - radius, t + radius)
        assert intersect(full, (interval,)) == (interval,)
        result["strict_witness"] = {"time": t, "distances": distances,
            "interval": interval, "affine_certificate": phase_certificate(speeds, interval)}
    else:
        assert duration(full) == 0 and not positive
    return result


def exact_curve(speeds):
    """All exact vertices of the lower envelope on [0,1], for plotting only."""
    cuts = sorted({Q(m, 2 * v) for v in speeds for m in range(2 * v + 1)})
    points = set(cuts)
    for a, b in zip(cuts, cuts[1:]):
        mid = (a + b) / 2
        lines = []
        for v in speeds:
            p = v * mid
            whole = p.numerator // p.denominator
            lines.append((v, Q(-whole)) if p % 1 < Q(1, 2) else (-v, Q(whole + 1)))
        for (va, ia), (vb, ib) in combinations(lines, 2):
            if va != vb:
                t = (ib - ia) / (va - vb)
                if a < t < b:
                    points.add(t)
    vertices = []
    for t in sorted(points):
        d = min(circular_distance(v * t) for v in speeds)
        while len(vertices) >= 2:
            (a, da), (b, db) = vertices[-2:]
            if (db - da) * (t - b) != (d - db) * (b - a):
                break
            vertices.pop()
        vertices.append((t, d))
    return vertices


def figure(cases):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"svg.hashsalt": "scaled-perturbation", "font.size": 10})
    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True, sharey=True)
    for ax, s in zip(axes, (0, -1, 1)):
        case = next(c for c in cases if c["q"] == 7 and c["s"] == s)
        vertices = exact_curve(case["relative_speeds"])
        assert max(d for t, d in vertices) == case["maximum"]
        ax.plot([float(7 * t) for t, d in vertices], [float(d) for t, d in vertices],
                color="#1e5d83", linewidth=1.1)
        ax.axhline(1 / 8, color="#ba6323", linestyle="--", linewidth=1.1)
        ax.axhline(1 / 7, color="#3b8262", linestyle=":", linewidth=1)
        ax.set_title(f"Last normalized speed = {Q(49 + s, 7)}    |    best separation = {case['maximum']}", loc="left")
        ax.set_yticks([0, 1 / 8, 1 / 7], ["0", "1/8", "1/7"])
        ax.set_ylim(-0.006, 0.174)
        ax.grid(axis="x", color="#dddddd", linewidth=0.5)
        if s:
            u = float(case["earliest_maximum_u"])
            ax.scatter([u], [1 / 7], color="#3b8262", s=25, zorder=4)
            ax.annotate("First 1/7 at u = 8/7", (u, 1 / 7), xytext=(u + 0.24, 0.16),
                        fontsize=9, arrowprops={"arrowstyle": "-", "color": "#3b8262"})
    axes[-1].set_xlim(0, 7)
    axes[-1].set_xlabel("Normalized time u = 7t (the speed-1 runner's laps)")
    fig.supylabel("Distance from reference 0 to its nearest runner (laps)")
    fig.suptitle("A small speed change breaks exact tightness\nEight runners; first six moving speeds normalized to 1,2,3,4,5,6", fontsize=14)
    fig.text(0.5, 0.012, "Exact piecewise-linear curves, q = 7. Each panel follows the selected reference runner only.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0.02, 0.04, 1, 0.95))
    target = ROOT / "figures/scaled_perturbation.svg"
    target.parent.mkdir(exist_ok=True)
    fig.savefig(target, metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    assert feasible_intervals(range(1, 7), D) == CORE_WINDOWS
    cases = []
    for q in QS:
        for s in (-1, 0, 1):
            case = compare(q, s)
            cases.append(case)
        print(f"q={q}: all three exact maximum, boundary, touch, and witness checks pass", flush=True)
    assert sum(bool(c["new_isolated_contacts"]) for c in cases) == 6
    paths = ("scripts/analyze_scaled_perturbation.py", "lonely_runner/checker.py",
             "scripts/analyze_core_transfer.py", "scripts/analyze_local_overlap.py",
             "scripts/analyze_blocking_overlaps.py", "scripts/analyze_overlap_placement.py",
             "scripts/analyze_phase_discrepancy.py", "scripts/analyze_residual_overlap.py",
             "scripts/analyze_two_variable_speeds.py")
    counts = {"configurations": len(cases), "maximum_and_peak_set_crosschecks": len(cases),
              "complete_boundary_reconstructions": len(cases),
              "old_touch_classifications": sum(4 * c["q"] for c in cases),
              "strict_interval_certificates": sum(c["s"] != 0 for c in cases),
              "new_isolated_contact_classes": 6,
              "new_isolated_contact_certificates": sum(len(c["new_isolated_contacts"]) for c in cases)}
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
            "scope": "Eight common-start runners, selected reference 0, speeds 0,q,2q,...,6q,7q+s; integer q>=2, s=-1,0,1. Finite checks only for the listed q values.",
            "time_convention": "Every allowed set and peak list is on original t in [0,1]. Normalized speeds divide by q, and normalized time is u=q*t. Baseline repeats q times in this window; perturbed configurations have period 1 in t.",
            "selection": "Initial controls q=2,3,4,7,14; q=9,11,29,37 added specifically to check the four remaining endpoint-congruence classes. No broad scan.",
            "claim_status": {"finite_computation": "OBSERVED: exact rational checks.",
                "all_q_formulas": "HYPOTHESIS/proof candidate: complete elementary derivations, independent review outstanding.",
                "pre_jump_mechanism": "KNOWN technique, Kravitz 2021 Section 2 (S15). Our specialization is not claimed new."},
            "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "core_allowed_phases": CORE_WINDOWS, "cases": cases, "verification_counts": counts,
            "limits": "Positive-duration allowed unions are reconstructed in memory by two methods; summaries retain exact duration, component counts, and endpoint hashes. Every maximum time and old-touch classification is retained, plus all new isolated-contact and strict-witness certificates. The infinite-family conclusion follows from the written argument, not these checks. No all-reference conclusion or novelty claim; no independent review."}
    (ROOT / "experiments/scaled_perturbation.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    if args.figure:
        figure(cases)
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
