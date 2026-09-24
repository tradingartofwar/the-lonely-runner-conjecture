"""Exact local comparison of q,2q+r for residuals r=1,2,3.

Run: python -m scripts.analyze_residual_overlap
Optional figure: python -m scripts.analyze_residual_overlap --figure
The exact analysis uses the standard library; the figure requires matplotlib.
Nine prescribed configurations, no parameter search or sampled time grid.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from math import gcd
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_blocking_overlaps import blocking_intervals
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_overlap_placement import boundary_measure, single_duration
from scripts.analyze_two_variable_speeds import phase_certificate


ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "77663f45fe7991b613b3d37244c589bf8e24b70b"
CORE = (1, 4, 5)
D = Q(1, 8)
J = (Q(9, 32), Q(3, 8))
L = J[1] - J[0]
PRESETS = ((56, 64, 72), (57, 64, 72), (6, 7, 11))


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def positive_parts(intervals):
    return tuple((a, b) for a, b in intervals if a < b)


def phase_slice_width(t, r):
    """Width of possible signed fast phases x; not a time occupancy rate."""
    return min(D, max(Q(0), (3 * D - circular_distance(r * t)) / 2))


def phase_profile(r):
    """All slope-change points of the slice-width function on J."""
    points = {*J}
    for m in range(floor(r * J[0]) - 1, ceil(r * J[1]) + 2):
        for offset in (-3 * D, -D, D, 3 * D):
            t = (m + offset) / r
            if J[0] < t < J[1]:
                points.add(t)
    return tuple((t, phase_slice_width(t, r)) for t in sorted(points))


def allowed_phase_region(r):
    """Endpoint pairs for the necessary strict condition ||rt||<3/8."""
    pieces = []
    for m in range(floor(r * J[0]) - 1, ceil(r * J[1]) + 2):
        a, b = max(J[0], (m - 3 * D) / r), min(J[1], (m + 3 * D) / r)
        if a < b:
            pieces.append((a, b))
    return tuple(pieces)


def affine_windows(q, r):
    """Construct intersections from meeting index j and residual integer m.

    At simultaneous blocking x=qt-j and y=(2q+r)t-(2j+m)
    satisfy y=2x+rt-m. Bounds are clipped directly from these inequalities.
    """
    b = 2 * q + r
    rows = []
    j_lo, j_hi = floor(q * J[0] - D), ceil(q * J[1] + D)
    m_lo, m_hi = floor(r * J[0] - 3 * D), ceil(r * J[1] + 3 * D)
    for j in range(j_lo, j_hi + 1):
        for m in range(m_lo, m_hi + 1):
            left = max(J[0], (j - D) / q, (2 * j + m - D) / b)
            right = min(J[1], (j + D) / q, (2 * j + m + D) / b)
            if left < right:
                t = (left + right) / 2
                x, y = q * t - j, b * t - (2 * j + m)
                assert y == 2 * x + r * t - m
                assert abs(x) < D and abs(y) < D
                assert circular_distance(r * t) < 3 * D
                rows.append({"j": j, "m": m, "interval": (left, right), "width": right - left})
    rows.sort(key=lambda row: row["interval"])
    assert all(a["interval"][1] <= b["interval"][0] for a, b in zip(rows, rows[1:]))
    return rows


def analyze(q, r, u, v):
    b = 2 * q + r
    blockers = (q, b, u, v)
    speeds = (*CORE, *blockers)
    assert len(set(speeds)) == 7
    rows = affine_windows(q, r)
    overlap_intervals = tuple(row["interval"] for row in rows)
    direct = positive_parts(intersect(intersect(blocking_intervals(q), blocking_intervals(b)), (J,)))
    assert overlap_intervals == direct
    support = allowed_phase_region(r)
    assert positive_parts(intersect(direct, support)) == direct
    overlap = duration(direct)
    individual = {str(w): single_duration(w) for w in blockers}
    for w in blockers:
        assert individual[str(w)] == duration(intersect(blocking_intervals(w), (J,)))
    excess = sum(individual.values()) - L
    allowed = intersect(feasible_intervals(speeds, D), (J,))
    clear = duration(allowed)
    histogram = boundary_measure(blockers)
    assert histogram[0] == clear
    redundancy = sum(max(m - 1, 0) * width for m, width in enumerate(histogram))
    assert clear == redundancy - excess
    assert clear >= overlap - excess >= -excess
    row = {"q": q, "residual_r": r, "pair": [q, b], "other_two": [u, v],
        "pair_gcd": gcd(q, b), "affine_overlap_windows": rows,
        "pair_overlap_duration": overlap, "individual_blocking_durations": individual,
        "excess_E": excess, "single_duration_only_lower_bound": -excess,
        "one_pair_lower_bound": overlap - excess, "actual_clear_duration": clear,
        "allowed_intervals": allowed, "blocking_histogram": histogram}
    if clear > 0:
        interval = max(allowed, key=lambda ab: ab[1] - ab[0])
        cert = phase_certificate(speeds, interval)
        t = sum(interval) / 2
        distances = {str(w): circular_distance(w * t) for w in speeds}
        assert min(distances.values()) > D
        row.update({"certified_clear_interval": interval, "affine_phase_certificate": cert,
                    "witness": {"time": t, "distances": distances, "minimum": min(distances.values())}})
    else:
        assert (q, r) == (6, 1)
        assert allowed == ((Q(3, 8), Q(3, 8)),)
    if q == 6:
        assert (Q(3, 8), Q(3, 8)) in allowed
        assert all(circular_distance(w * Q(3, 8)) >= D for w in speeds)
    return row


def make_figure(cases):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FixedFormatter

    # Deterministic SVG; floats appear only in this display layer.
    plt.rcParams.update({"svg.hashsalt": "residual-overlap-v1", "font.size": 12,
                         "font.family": "DejaVu Sans", "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.subplots_adjust(left=.16, right=.97, top=.74, bottom=.29)
    purple = "#6550a1"
    selected = [row for row in cases if row["q"] == 56]
    for row in selected:
        r = row["residual_r"]
        y = 4 - r
        ax.broken_barh([(float(a), float(b - a)) for a, b in
            (w["interval"] for w in row["affine_overlap_windows"])],
            (y - .16, .32), facecolors=purple, edgecolors="none", zorder=3)
        ax.hlines(y, float(J[0]), float(J[1]), color="#e7e5eb", linewidth=1, zorder=1)
    ax.broken_barh([(float(J[0]), float(Q(5, 16) - J[0]))], (1.65, .7),
                  facecolors="#eeedf2", edgecolors="none", zorder=0)
    ax.text(float((J[0] + Q(5, 16)) / 2), 2.39, "Overlap impossible here", ha="center", fontsize=10, color="#605b69")
    ticks = [J[0], Q(5, 16), Q(1, 3), J[1]]
    ax.xaxis.set_major_locator(FixedLocator([float(t) for t in ticks]))
    ax.xaxis.set_major_formatter(FixedFormatter(["9/32", "5/16", "1/3", "3/8"]))
    ax.set_xlim(float(J[0]), float(J[1]))
    ax.set_ylim(.45, 3.55)
    ax.set_yticks([3, 2, 1], ["56 & 113\nr = 1", "56 & 114\nr = 2", "56 & 115\nr = 3"])
    ax.tick_params(axis="both", length=0, pad=10)
    ax.set_xlabel("Time within the same fixed-runner opening", labelpad=12)
    ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
    fig.text(.04, .93, "Where the pair blocks at the same time", fontsize=19, weight="bold", color="#272133")
    fig.text(.04, .85, "Only the second speed changes. Purple segments show exact intervals when both runners block.", fontsize=11, color="#605b69")
    fig.text(.04, .04, "Eight total runners; distance threshold 1/8. These purple intervals are blocking overlaps, not clear times.\nWidths come from exact rational endpoints; the smallest segment may be hard to see at screen resolution.", fontsize=9, color="#605b69")
    out = ROOT / "figures/residual_overlap.svg"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, metadata={"Date": None})
    # Disposable visual-inspection copy; the SVG is the saved figure.
    fig.savefig(ROOT.parent / "residual_overlap_preview.png", dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    cases = [analyze(q, r, u, v) for q, u, v in PRESETS for r in (1, 2, 3)]
    lookup = {(row["q"], row["residual_r"]): row for row in cases}
    expected = {
        (56, 1): (Q(9, 3616), Q(1045, 911232), Q(6193, 260352)),
        (56, 2): (Q(13, 8512), -Q(109, 153216), Q(7117, 306432)),
        (56, 3): (Q(29, 2240), Q(671, 927360), Q(2729, 88320)),
        (6, 1): (Q(1, 208), Q(1445, 96096), Q(0)),
        (6, 2): (Q(1, 168), Q(25, 924), Q(1, 112)),
        (6, 3): (Q(1, 60), Q(461, 36960), Q(1, 112)),
    }
    for key, values in expected.items():
        row = lookup[key]
        assert tuple(row[k] for k in ("pair_overlap_duration", "excess_E", "actual_clear_duration")) == values
    assert [w["width"] for w in lookup[(56, 2)]["affine_overlap_windows"]] == [Q(k, 25536) for k in (5, 13, 21)]
    assert [w["width"] for w in lookup[(56, 3)]["affine_overlap_windows"]] == [Q(107, 51520)] + [Q(1, 460)] * 5
    assert lookup[(56, 2)]["single_duration_only_lower_bound"] > 0
    assert lookup[(6, 2)]["one_pair_lower_bound"] < 0 < lookup[(6, 2)]["actual_clear_duration"]
    assert lookup[(6, 3)]["one_pair_lower_bound"] > 0
    # Reversal: which residual gives more overlap changes when q moves by 1.
    assert lookup[(56, 1)]["pair_overlap_duration"] > lookup[(56, 2)]["pair_overlap_duration"]
    assert lookup[(57, 1)]["pair_overlap_duration"] < lookup[(57, 2)]["pair_overlap_duration"]
    # The permitted phase width is not actual occupancy: no overlap at 1/3.
    assert phase_slice_width(Q(1, 3), 3) == D
    assert circular_distance(56 * Q(1, 3)) == circular_distance(115 * Q(1, 3)) == Q(1, 3)
    profiles = {str(r): phase_profile(r) for r in (1, 2, 3)}
    assert profiles["1"] == ((J[0], Q(3, 64)), (J[1], Q(0)))
    assert profiles["2"] == ((J[0], Q(0)), (Q(5, 16), Q(0)), (J[1], Q(1, 16)))
    assert profiles["3"] == ((J[0], Q(7, 64)), (Q(7, 24), D), (J[1], D))
    slice_areas = {r: sum(((b - a) * (ka + kb) / 2 for (a, ka), (b, kb) in
                          zip(profile, profile[1:])), Q(0)) for r, profile in profiles.items()}
    assert slice_areas == {"1": Q(9, 4096), "2": Q(1, 512), "3": Q(143, 12288)}
    dependencies = ("scripts/analyze_residual_overlap.py", "scripts/analyze_overlap_placement.py",
        "scripts/analyze_local_overlap.py", "scripts/analyze_blocking_overlaps.py",
        "scripts/analyze_two_variable_speeds.py", "lonely_runner/checker.py")
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
        "claim_status": {"finite_cases": "OBSERVED", "general_phase_derivation": "HYPOTHESIS: elementary argument awaiting independent review", "arbitrary_coverage": "OPEN"},
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
        "scope": "Eight total common-start runners; selected reference 0; positive distinct integer speeds; target 1/8.",
        "fixed_core": CORE, "J": J, "length_J": L,
        "necessary_overlap_condition": "||(B-2A)t|| < 3/8",
        "phase_slice_width": "min(1/8,max(0,(3/8-||rt||)/2)); possible fast-phase width, not actual time occupancy",
        "phase_slice_profiles": profiles,
        "reference_slice_areas_not_actual_time_durations": slice_areas, "cases": cases,
        "verification_counts": {"prescribed_configurations": 9, "affine_overlap_crosschecks": 9,
            "single_duration_crosschecks": 36, "independent_full_duration_checks": 9,
            "positive_clear_interval_certificates": 8, "small_q_endpoint_checks": 3},
        "limitations": "No new uniform cutoff for r=2 or r=3. Phase availability does not force trajectory occupancy. Bound failures are inconclusive. Equality points retained. No all-reference or novelty claim.",
    }
    (ROOT / "experiments/residual_overlap.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    if args.figure:
        make_figure(cases)
    print(json.dumps({"cases": [{k: row[k] for k in ("q", "residual_r", "pair_gcd", "pair_overlap_duration", "excess_E", "one_pair_lower_bound", "actual_clear_duration")} for row in cases], "counts": data["verification_counts"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
