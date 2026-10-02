"""Exact two-doubled-offset study; classification, finite reduction, controls.

Run: python -m scripts.analyze_two_doubled_offsets [--figure]
96 offset vectors, 608 necessary tiling candidates, two prescribed phases,
48 residual configurations and 96 rounded diagnostics. No speed-box scan.
"""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

from lonely_runner.checker import circular_distance, exact_maximum, feasible_intervals
from scripts.analyze_affine_family import frozen_phase
from scripts.analyze_core_transfer import boundary_certificate
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate
from scripts.analyze_unequal_perturbations import DEPENDENCIES as PRIOR_DEPENDENCIES
from scripts.analyze_unequal_perturbations import actual_grid, floor, profiles

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "7a697c12b47c1e597c05f509c512cacb6198cd31"
D = Q(1, 8)
DEPENDENCIES = (*PRIOR_DEPENDENCIES, "scripts/analyze_unequal_perturbations.py")
CONTROL_TERMS = ((1, 4), (1, 12), (2, 10), (2, 22))


def tiling_criterion(terms, x):
    units = [a * x % 1 for b, a in terms if b == 1]
    doubles = [a * x % 1 for b, a in terms if b == 2]
    assert len(units) == len(doubles) == 2
    shifts = sorted((p - 2 * units[0]) % 1 for p in doubles)
    return (units[1] - units[0]) % 1 == Q(1, 2) and shifts == [Q(3, 8), Q(5, 8)]


def tiling_candidates(terms):
    units = [a for b, a in terms if b == 1]
    doubles = [a for b, a in terms if b == 2]
    d = units[1] - units[0]
    candidates = []
    assert d != 0
    if d % 4 == 0:
        assert abs(d) == 12 and sorted(map(abs, units)) == [5, 7]
        assert sorted(map(abs, doubles)) == [4, 6]
        assert all((b - 2 * units[0]) % 2 == 0 for b in doubles)
    for r in range(abs(d)):
        x = Q(2 * r + 1, 2 * abs(d))
        assert (d * x) % 1 == Q(1, 2)
        p = frozen_phase(terms, x)
        tile = tiling_criterion(terms, x)
        assert tile == (p["clear_phase_duration"] == 0)
        assert not tile
        candidates.append({"core_phase": x,
                           "doubled_shifts": [(b * x - 2 * units[0] * x) % 1 for b in doubles],
                           "clear_phase_length": p["clear_phase_duration"]})
    return {"unit_difference": d, "divisible_by_four": d % 4 == 0, "checks": candidates}


def compact_profile(p):
    result = {k: v for k, v in p.items() if k != "geometry"}
    result["geometry"] = {k: p["geometry"][k] for k in (
        "terms_b_a", "slow_time", "allowed_phases", "clear_phase_duration",
        "redundant_blocking", "blocking_count_histogram", "individual_blocked_durations")}
    return result


def certify(speeds, t, full=None):
    distances = {str(v): circular_distance(v * t) for v in speeds}
    minimum = min(distances.values())
    assert minimum > D
    radius = (minimum - D) / (2 * max(speeds))
    interval = (t - radius, t + radius)
    assert 0 < interval[0] < interval[1] < 1
    certificate = phase_certificate(speeds, interval)
    if full is not None:
        assert intersect(full, (interval,)) == (interval,)
    return {"time": t, "minimum": minimum, "distances": distances,
            "strict_interval": interval, "endpoint_certificate": certificate}


def family_case(q, offsets, pp, chosen):
    speeds = (q, 2*q, 3*q, *(k*q+a for k,a in zip(range(4,8),offsets)))
    assert min(speeds) > 0 and len(set(speeds)) == 7
    grids = [actual_grid(q, offsets, p) for p in pp]
    assert any(g["strict_survivors"] for g in grids)
    remainder = q < chosen["sufficient_q"]
    full = None
    if remainder:
        full = feasible_intervals(speeds, D)
        assert full == boundary_certificate(speeds)["complete_allowed_set"]
        g = next(g for g in grids if g["strict_survivors"])
        x, j = g["core_phase"], g["strict_survivors"][0]
        t = (x+j)/q
        method = "first strict survivor at a prescribed phase; complete finite remainder"
    else:
        x, centre = chosen["core_phase"], chosen["midpoint"]
        j = floor(q*centre-x+Q(1,2)) % q
        t = (x+j)/q
        assert circular_distance(t-centre) <= Q(1,2*q) < chosen["width"]/2
        method = "interval midpoint rounded to the actual time grid"
    row = {"q": q, "offsets": offsets, "speeds": speeds, "finite_remainder": remainder,
           "grids": grids, "witness_core_phase": x, "method": method,
           "certificate": certify(speeds, t, full)}
    assert q*t % 1 == x
    if full is not None:
        row["complete_allowed_summary"] = {"duration": duration(full), "components": len(full),
            "isolated": sum(a == b for a,b in full),
            "sha256_json_string_endpoints": hashlib.sha256(json.dumps(full,default=str).encode()).hexdigest()}
    return row


def control_grid(q, terms, x):
    p = frozen_phase(terms, x)
    assert tiling_criterion(terms, x) == (p["clear_phase_duration"] == 0)
    speeds = (q,2*q,3*q,*(a*q+b for b,a in terms))
    blocked, survivors, strict, hist = [[] for _ in terms], [], [], [0]*5
    for j in range(q):
        t = (x+j)/q
        bad = []
        for i,(b,a) in enumerate(terms):
            assert (a*q+b)*t % 1 == (a*x+b*t) % 1
            if circular_distance((a*q+b)*t) < D:
                bad.append(i)
                blocked[i].append(j)
        hist[len(bad)] += 1
        minimum = min(circular_distance(v*t) for v in speeds)
        assert (not bad) == (minimum >= D)
        if not bad:
            survivors.append(j)
        if minimum > D:
            strict.append(j)
    T = sum(map(len,blocked))
    R = sum(max(m-1,0)*n for m,n in enumerate(hist))
    assert len(survivors) == q-T+R
    return {"core_phase":x,"geometry":p,"grid":{"q":q,"times":[(x+j)/q for j in range(q)],
            "blocked_indices":blocked,"histogram":hist,"T":T,"R":R,"N":len(survivors),
            "survivors":survivors,"strict_survivors":strict}}


def boundary_control():
    rows = [control_grid(5,CONTROL_TERMS,x) for x in (Q(3,16),Q(1,5),Q(1,4))]
    expected = (Q(0),Q(1,8),Q(3,8),Q(1,2),Q(5,8),Q(7,8),Q(1))
    assert rows[0]["geometry"]["allowed_phases"] == tuple((t,t) for t in expected)
    assert all((8*t).denominator == 1 for t in expected)
    assert min(circular_distance(k*Q(3,16)) for k in (1,2,3)) == Q(3,16) > D
    assert [(r["geometry"]["clear_phase_duration"],r["grid"]["N"]) for r in rows] == [(0,0),(Q(7,40),0),(Q(1,2),3)]
    speeds = (5,10,15,21,61,52,112)
    full = feasible_intervals(speeds,D)
    assert boundary_certificate(speeds)["complete_allowed_set"] == full
    maximum = exact_maximum(speeds)
    assert maximum.value == Q(1,4) and maximum.times == (Q(9,20),Q(11,20))
    assert feasible_intervals(speeds,maximum.value) == tuple((t,t) for t in maximum.times)
    return {"scope":"Changed coefficients, outside the 4,5,6,7 family; common start is retained",
            "terms_b_a":CONTROL_TERMS,"q":5,"speeds":speeds,"profiles":rows,
            "maximum":maximum.value,"all_maximizing_times":maximum.times,
            "certificate":certify(speeds,Q(9,20),full),
            "all_integer_q_grid_obstruction":"At x=3/16 every allowed phase has denominator dividing 8, so q*t cannot have fractional part 3/16 for any integer q."}


def figure(control):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    matplotlib.rcParams.update({"svg.hashsalt":"two-doubled-offsets","font.size":10})
    fig,axes = plt.subplots(3,1,figsize=(11,9),sharex=True)
    titles = ("x = 3/16: perfect tiling; every actual choice is blocked",
              "x = 1/5: an opening exists; all five actual choices still miss it",
              "x = 1/4: three actual choices reach the openings")
    for ax,row,title in zip(axes,control["profiles"],titles):
        x,p,g = row["core_phase"],row["geometry"],row["grid"]
        for i,(b,a) in enumerate(CONTROL_TERMS):
            phase = a*x % 1
            for m in range(-1,b+2):
                lo,hi = max(Q(0),(m-D-phase)/b),min(Q(1),(m+D-phase)/b)
                if lo < hi:
                    ax.broken_barh([(float(lo),float(hi-lo))],(3-i-.23,.46),facecolors="#ce786d",alpha=.9)
        for lo,hi in p["allowed_phases"]:
            if lo < hi:
                ax.axvspan(float(lo),float(hi),color="#98cbaa",alpha=.4)
            else:
                ax.scatter(float(lo),-.5,color="#946600",marker="|",s=95)
        for j,t in enumerate(g["times"]):
            safe = j in g["survivors"]
            color = "#1d7442" if safe else "#35414d"
            ax.axvline(float(t),color=color,linestyle="-" if safe else ":",alpha=.6)
            ax.scatter(float(t),-.8,color=color,s=25,zorder=5)
            ax.text(float(t),-1.03,str(t),ha="center",va="top",fontsize=9)
        ax.set_yticks(range(4),[f"rate {b}" for b,a in reversed(CONTROL_TERMS)])
        ax.set_ylim(-1.45,3.45)
        ax.set_title(title,loc="left",fontweight="bold",fontsize=11)
        ax.grid(axis="x",alpha=.16)
        for side in ("top","right","left"):
            ax.spines[side].set_visible(False)
    axes[-1].set_xlim(0,1)
    axes[-1].set_xticks([i/8 for i in range(9)],[str(Q(i,8)) for i in range(9)])
    axes[-1].set_xlabel("Auxiliary phase; vertical lines mark actual times for q = 5")
    fig.suptitle("Boundary control: changing coefficients allows tiling",x=.1,ha="left",fontsize=15)
    fig.text(.1,.94,"Same eight speeds in every panel: 0, 5, 10, 15, 21, 52, 61, 112",fontsize=10)
    fig.legend(handles=[Patch(facecolor="#ce786d",label="Blocked (open intervals)"),
                        Patch(facecolor="#98cbaa",label="Clear interval"),
                        Line2D([],[],color="#946600",marker="|",linestyle="None",markersize=9,label="Isolated equality phase")],
               loc="lower center",ncol=3,frameon=False)
    fig.subplots_adjust(left=.1,right=.98,top=.89,bottom=.11,hspace=.4)
    fig.savefig(ROOT/"figures/two_doubled_offsets.svg",metadata={"Date":None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figure",action="store_true")
    args = parser.parse_args()
    families,cases = [],[]
    for doubled in combinations(range(4,8),2):
        for signs in product((-1,1),repeat=4):
            offsets = tuple(s*(2 if k in doubled else 1) for k,s in zip(range(4,8),signs))
            terms = tuple((abs(a),k if a>0 else -k) for k,a in zip(range(4,8),offsets))
            candidates = tiling_candidates(terms)
            pp = profiles(offsets)
            for p in pp:
                assert not tiling_criterion(terms,p["core_phase"])
                assert p["geometry"]["clear_phase_duration"] > 0
            chosen = min(pp,key=lambda p:(p["sufficient_q"],p["core_phase"]))
            cutoff = chosen["sufficient_q"]
            families.append({"doubled_indices":doubled,"offsets":offsets,
                "tiling_candidate_check":candidates,"profiles":[compact_profile(p) for p in pp],
                "selected_phase":chosen["core_phase"],"sufficient_q":cutoff})
            cases.extend(family_case(q,offsets,pp,chosen) for q in range(5,max(5,cutoff)+1))
        print(f"doubled indices {doubled}: all sixteen signs pass",flush=True)
    assert len(families) == 96
    assert Counter(r["sufficient_q"] for r in families) == {4:28,5:32,6:32,9:4}
    candidate_count = sum(len(r["tiling_candidate_check"]["checks"]) for r in families)
    assert candidate_count == 608 and sum(r["tiling_candidate_check"]["divisible_by_four"] for r in families) == 8
    assert len(cases) == 144 and sum(c["finite_remainder"] for c in cases) == 48
    control = boundary_control()
    counts = {"offset_vectors":96,"prescribed_family_phase_profiles":192,
              "necessary_tiling_candidate_profiles":608,"family_tilings_at_candidates":0,
              "finite_remainder_certificates":48,"rounded_diagnostics":96,
              "family_strict_actual_interval_certificates":144,"control_strict_interval_certificates":1,
              "complete_actual_boundary_reconstructions":49,"maximum_full_peak_crosschecks":1,
              "actual_grid_profiles":2*len(cases)+3,
              "actual_grid_choices":2*sum(c["q"] for c in cases)+15,
              "changed_coefficient_control_profiles":3}
    paths = ("scripts/analyze_two_doubled_offsets.py",*DEPENDENCIES)
    data = {"date_utc":"2026-09-25","base_commit":BASE_COMMIT,
            "scope":"Eight common-start runners, reference 0; integer q>=5; speeds 0,q,2q,3q,4q+a4,...,7q+a7; exactly two |ak|=2, other two |ak|=1. All six placements and sixteen sign choices.",
            "selection":"608 possible core phases after the necessary unit-antipodality reduction; two prescribed phases give vector-specific width cutoffs, leaving exactly 48 residual configurations. One rounded diagnostic per vector. One changed-coefficient boundary control; no speed-box scan.",
            "claim_status":{"finite_checks":"OBSERVED, exact rational",
                "tiling_criterion_and_parity_obstruction":"HYPOTHESIS/proof candidates; independent review pending",
                "all_q_strictness":"HYPOTHESIS/proof candidate including the finite reduction; witnesses exist at x=1/4 or 1/5",
                "novelty":"Unestablished; S15 supplies known pre-jump precedent; no wider novelty audit"},
            "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
            "families":families,"cases":cases,"changed_coefficient_control":control,
            "verification_counts":counts,
            "limits":"Selected reference and stated coefficients only. Common start by itself does not prohibit auxiliary tiling, as the boundary control shows. Positive auxiliary room and actual-grid reachability remain separate. Existing helpers unchanged; broader regression suite not rerun. No independent proof review, novelty claim or general-conjecture solution."}
    (ROOT/"experiments/two_doubled_offsets.json").write_text(json.dumps(data,indent=1,default=str)+"\n")
    if args.figure:
        figure(control)
    print(json.dumps(counts,indent=2))


if __name__ == "__main__":
    main()
