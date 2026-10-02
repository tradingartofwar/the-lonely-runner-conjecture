"""One offset of magnitude two, three of magnitude one: exact finite reduction.

Run: python -m scripts.analyze_unequal_perturbations [--figure]
All 64 offset vectors, two frozen core phases, 44 residual configurations,
and one rounded diagnostic per vector. No unbounded or sampled-time search.
"""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals
from scripts.analyze_affine_family import frozen_phase
from scripts.analyze_core_transfer import boundary_certificate
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "e42a8f52d15a59c76d9a98463551a9473acb8e2d"
D = Q(1, 8)
PHASES = (Q(1, 4), Q(1, 5))
DEPENDENCIES = (
    "lonely_runner/checker.py", "scripts/analyze_affine_family.py",
    "scripts/analyze_core_transfer.py", "scripts/analyze_local_overlap.py",
    "scripts/analyze_blocking_overlaps.py", "scripts/analyze_overlap_placement.py",
    "scripts/analyze_phase_discrepancy.py", "scripts/analyze_residual_overlap.py",
    "scripts/analyze_two_variable_speeds.py",
)


def floor(x):
    return x.numerator // x.denominator


def profiles(offsets):
    terms = tuple((abs(a), k if a > 0 else -k) for k, a in zip(range(4, 8), offsets))
    result = []
    for x in PHASES:
        # Multiplying the original position by sign(a) preserves its distance.
        p = frozen_phase(terms, x)
        lo, hi = max(p["allowed_phases"], key=lambda ab: ab[1] - ab[0])
        width = hi - lo
        assert width > 0
        certificate = []
        for k, a in zip(range(4, 8), offsets):
            left, right = k * x + a * lo, k * x + a * hi
            integer = floor(left)
            assert integer == floor(right)
            assert D <= left - integer <= 1 - D
            assert D <= right - integer <= 1 - D
            certificate.append({"k": k, "offset": a, "integer_part": integer,
                                "left_phase": left - integer, "right_phase": right - integer})
        result.append({"core_phase": x, "geometry": p, "chosen_interval": (lo, hi),
                       "width": width, "midpoint": (lo + hi) / 2,
                       "sufficient_q": floor(1 / width) + 1,
                       "interval_endpoint_certificate": certificate})
    return result


def actual_grid(q, offsets, p):
    x = p["core_phase"]
    blocked = [[] for _ in offsets]
    hist = [0] * 5
    safe, strict = [], []
    for j in range(q):
        t = (x + j) / q
        distances = []
        for i, (k, a) in enumerate(zip(range(4, 8), offsets)):
            assert (k * q + a) * t % 1 == (k * x + a * t) % 1
            distances.append(circular_distance((k * q + a) * t))
            if distances[-1] < D:
                blocked[i].append(j)
        count = sum(d < D for d in distances)
        hist[count] += 1
        assert (count == 0) == any(lo <= t <= hi for lo, hi in p["geometry"]["allowed_phases"])
        if count == 0:
            safe.append(j)
        if min(distances) > D:
            strict.append(j)
    bounds = []
    for a, indices in zip(offsets, blocked):
        g = gcd(q, abs(a))
        bound = g * ((q // g + 3) // 4)
        assert len(indices) <= bound
        bounds.append({"gcd": g, "bound": bound})
    total = sum(map(len, blocked))
    redundant = sum(max(m - 1, 0) * n for m, n in enumerate(hist))
    assert len(safe) == q - total + redundant
    return {"core_phase": x, "blocked_indices": blocked, "individual_bounds": bounds,
            "histogram": hist, "T": total, "R": redundant, "N": len(safe),
            "survivors": safe, "strict_survivors": strict}


def actual_certificate(q, offsets, p, remainder):
    speeds = (q, 2 * q, 3 * q, *(k * q + a for k, a in zip(range(4, 8), offsets)))
    assert min(speeds) > 0 and len(set(speeds)) == 7
    x, centre = p["core_phase"], p["midpoint"]
    j = floor(q * centre - x + Q(1, 2)) % q
    rounded = (x + j) / q
    drift = circular_distance(rounded - centre)
    assert drift <= Q(1, 2 * q)
    full = None
    if remainder:
        full = feasible_intervals(speeds, D)
        assert boundary_certificate(speeds)["complete_allowed_set"] == full
        lo, hi = max(full, key=lambda ab: ab[1] - ab[0])
        assert lo < hi
        witness = (lo + hi) / 2
    else:
        assert q >= p["sufficient_q"] and drift < p["width"] / 2
        witness = rounded
    distances = {str(v): circular_distance(v * witness) for v in speeds}
    minimum = min(distances.values())
    assert minimum > D
    radius = (minimum - D) / (2 * max(speeds))
    interval = (witness - radius, witness + radius)
    assert 0 < interval[0] < interval[1] < 1
    certificate = phase_certificate(speeds, interval)
    if full is not None:
        assert intersect(full, (interval,)) == (interval,)
    row = {"q": q, "offsets": offsets, "speeds": speeds, "finite_remainder": remainder,
           "rounded_time": rounded, "rounded_minimum": min(circular_distance(v * rounded) for v in speeds),
           "rounding_circular_drift": drift, "witness": witness, "minimum": minimum,
           "distances": distances, "strict_interval": interval, "endpoint_certificate": certificate}
    if full is not None:
        row["full_allowed_summary"] = {
            "duration": duration(full), "components": len(full),
            "isolated": sum(lo == hi for lo, hi in full),
            "sha256_json_string_endpoints": hashlib.sha256(json.dumps(full, default=str).encode()).hexdigest()}
    return row


def figure(controls):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    matplotlib.rcParams.update({"svg.hashsalt": "unequal-perturbations", "font.size": 10})
    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
    for ax, control in zip(axes, controls):
        p = control["profile"]
        x = p["slow_time"]
        for i, (b, a) in enumerate(p["terms_b_a"]):
            phase = (a * x) % 1
            for m in range(-1, b + 2):
                lo, hi = max(Q(0), (m - D - phase) / b), min(Q(1), (m + D - phase) / b)
                if lo < hi:
                    ax.broken_barh([(float(lo), float(hi - lo))], (3-i-0.24, .48),
                                  facecolors="#cf7970", alpha=.9)
        for lo, hi in p["allowed_phases"]:
            if lo < hi:
                ax.axvspan(float(lo), float(hi), color="#9dceb0", alpha=.45)
            else:
                ax.scatter(float(lo), -.55, marker="|", color="#926100", s=110)
        ax.set_title(control["title"], loc="left", fontweight="bold", fontsize=11)
        ax.set_yticks(range(4), [f"rate {b}" for b, a in reversed(p["terms_b_a"])])
        ax.set_ylim(-.85,3.5)
        ax.grid(axis="x", alpha=.2)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
    axes[-1].set_xticks([i/8 for i in range(9)], [str(Q(i,8)) for i in range(9)])
    axes[-1].set_xlim(0,1)
    axes[-1].set_xlabel("Auxiliary phase around one cycle (actual-time reachability is checked separately)")
    fig.suptitle("Same blocking duration; different ability to tile", x=.1, ha="left", fontsize=15)
    fig.legend(handles=[Patch(facecolor="#cf7970", label="Blocked interval (endpoints excluded)"),
                        Patch(facecolor="#9dceb0", label="Clear interval"),
                        Line2D([],[],color="#926100", marker="|", linestyle="None", markersize=10,
                               label="Isolated equality phase")], loc="lower center", ncol=3, frameon=False)
    fig.subplots_adjust(left=.1,right=.98,top=.90,bottom=.13,hspace=.48)
    fig.savefig(ROOT / "figures/unequal_perturbations.svg", metadata={"Date":None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure", action="store_true")
    args = parser.parse_args()
    rows, cases, misses = [], [], []
    for doubled in range(4,8):
        for signs in product((-1,1), repeat=4):
            offsets = tuple(s*(2 if k == doubled else 1) for k,s in zip(range(4,8),signs))
            pp = profiles(offsets)
            chosen = min(pp, key=lambda p:(p["sufficient_q"],p["core_phase"]))
            cutoff = chosen["sufficient_q"]
            rows.append({"doubled_index": doubled, "offsets": offsets, "profiles": pp,
                         "selected_phase": chosen["core_phase"], "sufficient_q": cutoff})
            for q in range(4,max(4,cutoff)+1):
                remainder = q < cutoff
                row = actual_certificate(q, offsets, chosen, remainder)
                row["grids"] = [actual_grid(q, offsets, p) for p in pp]
                if not any(g["strict_survivors"] for g in row["grids"]):
                    assert remainder
                    maximum = exact_maximum(row["speeds"])
                    assert maximum.value > D
                    assert feasible_intervals(row["speeds"], maximum.value) == tuple((t,t) for t in maximum.times)
                    row["maximum"] = maximum.value
                    row["all_maximizing_times"] = maximum.times
                    misses.append({"q":q,"offsets":offsets,"maximum":maximum.value,
                                   "all_maximizing_times":maximum.times,
                                   "strict_witness":row["witness"], "witness_core_phase":q*row["witness"]%1})
                cases.append(row)
        print(f"doubled index {doubled}: all sixteen sign vectors pass", flush=True)
    assert len(rows) == 64
    assert Counter(r["sufficient_q"] for r in rows) == {3:8,4:32,5:12,6:8,7:2,9:2}
    assert sum(c["finite_remainder"] for c in cases) == 44
    assert len(cases) == 108 and len(misses) == 8
    # Geometry controls: the last is deliberately a free-phase control,
    # not a common-start instance of the investigated family.
    controls = [
        {"title":"Four unit rates: perfect tiling, clear length 0",
         "scope":"Unit-offset comparison at x=1/4", "profile":frozen_phase(((1,4),(1,5),(1,6),(1,7)),Q(1,4))},
        {"title":"One doubled rate: overlap leaves clear length 1/8",
         "scope":"Offsets (2,1,1,1) at x=1/4", "profile":frozen_phase(((2,4),(1,5),(1,6),(1,7)),Q(1,4))},
        {"title":"One tripled rate: perfect tiling returns for these independent phases",
         "scope":"Free-phase geometry only; not an actual configuration in this family",
         "profile":frozen_phase(((1,-1),(1,-3),(1,-5),(3,0)),Q(1,6))}]
    assert [p["profile"]["clear_phase_duration"] for p in controls] == [0,Q(1,8),0]
    assert controls[2]["profile"]["allowed_phases"] == tuple((Q(i,24),Q(i,24)) for i in (1,7,9,15,17,23))
    # A doubled offset may share a factor with q, invalidating the old coprime count.
    gcd_control = next(c for c in cases if c["q"]==4 and c["offsets"]==(2,-1,1,-1))
    fifth = next(g for g in gcd_control["grids"] if g["core_phase"]==Q(1,5))
    assert fifth["blocked_indices"][0] == [0,2]
    assert len(fifth["blocked_indices"][0]) > (4+3)//4
    counts = {"offset_vectors":len(rows), "frozen_profiles":2*len(rows),
              "finite_remainder_certificates":44, "rounded_diagnostics":64,
              "strict_actual_interval_certificates":len(cases),
              "complete_boundary_reconstructions":44, "maximum_full_peak_crosschecks":len(misses),
              "actual_grid_profiles":2*len(cases), "actual_grid_choices":2*sum(c["q"] for c in cases),
              "no_strict_survivor_at_either_chosen_phase":len(misses), "geometry_controls":len(controls)}
    source_paths = ("scripts/analyze_unequal_perturbations.py",*DEPENDENCIES)
    data = {"date":"2026-09-25", "base_commit":BASE_COMMIT,
            "scope":"Eight common-start runners, reference 0; integer q>=4; speeds 0,q,2q,3q,4q+a4,...,7q+a7. Exactly one |ak|=2, other three |ak|=1; all signs and all four positions.",
            "selection":"Two prescribed core phases. Profile-specific width cutoffs reduce all q to exactly 44 cases; one rounded diagnostic per offset vector. Eight missed-strictness controls reuse remainder cases. No speed-box scan.",
            "claim_status":{"finite_checks":"OBSERVED, exact rational",
                "all_q_strictness":"HYPOTHESIS/proof candidate, independent review pending",
                "tiling_divisibility":"HYPOTHESIS/proof candidate: for three rate-one blockers and one rate-m blocker, perfect tiling requires m divides 3; sufficient free-phase constructions for m=1,3",
                "novelty":"Unestablished; known pre-jump precedent S15; no wider novelty audit"},
            "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths},
            "profiles":rows,"cases":cases,"missed_strict_grids":misses,
            "geometry_controls":controls,"coprime_count_counterexample":{"q":4,"offsets":(2,-1,1,-1),"grid":fifth},
            "verification_counts":counts,
            "limits":"Selected reference only. General argument relies on the written finite reduction, not extrapolation. No general maximum formula, independent proof review, or novelty claim. Existing helpers unchanged; broader regression suite not rerun. Tripled-rate tiling is a free-phase geometry control only."}
    (ROOT/"experiments/unequal_perturbations.json").write_text(json.dumps(data,indent=2,default=str)+"\n")
    if args.figure:
        figure(controls)
    print(json.dumps(counts,indent=2))


if __name__ == "__main__":
    main()
