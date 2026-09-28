"""Exact bounded replay of a supplied chain-termination proof candidate.

Run from repository root: python reviews/2026-09-28-chain-termination/primary.py
Only the frozen protocol supplies cases. No interval-event or lap enumeration
is used to select the earliest time; chain records are produced by the moves.
Material AI involvement; independent verifier and scope are in this directory.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
DELTA = F(1, 8)
PROTOCOL_SHA256 = "134f1825868d1bde006f3cf7f1d523047fc89410d3acaf8da5add4ec658608c0"


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def phase(v, t):
    return v * t - floor(v * t)


def safe(v, t):
    return DELTA <= phase(v, t) <= 1 - DELTA


def h(x):
    return min(x, DELTA) + max(F(0), x - (1 - DELTA)) - x / 4


def potential(speeds, t):
    return sum((h(phase(v, t)) / v for v in speeds), F(0))


def analyze(case, order):
    speeds = case["speeds"]
    assert len(speeds) == 4 and all(isinstance(v, int) and v > 0 for v in speeds)
    assert speeds == sorted(speeds)
    L, R = map(F, case["window"])
    assert L <= R
    core_certificate = []
    for v in case["core"]:
        m = floor(v * L)
        assert m + DELTA <= v * L <= v * R <= m + 1 - DELTA
        core_certificate.append(dict(speed=v, lap=m, phase_left=v*L-m, phase_right=v*R-m))
    reciprocal_sum = sum((F(1, v) for v in speeds), F(0))
    Q = max(lcm(a, b) for a, b in combinations(speeds, 2))
    eta = F(1, 8 * Q)
    budget = F(3, 16) * reciprocal_sum
    Hmax = budget / 2
    m_L = sum(not safe(v, L) for v in speeds)
    K_global = floor(1 + budget / eta)
    K_phase = m_L + floor((Hmax - potential(speeds, L)) / eta)
    bound = min(K_global, K_phase)
    t = L
    trace, intervals = [], []
    rounds = 0
    while not all(safe(v, t) for v in speeds):
        rounds += 1
        assert rounds <= bound, "Exceeds analytic nonterminal round bound"
        for i in order:
            v = speeds[i]
            m = ceil(v * t - 1 + DELTA)
            nxt = max(t, (m + DELTA) / v)
            trace.append(dict(runner=i, input=t, output=nxt))
            if nxt > t:
                A, B = (m - DELTA) / v, (m + DELTA) / v
                assert A < t < B == nxt
                if intervals:
                    prev = intervals[-1]
                    assert min(prev["right"], B) - max(prev["left"], A) >= eta
                intervals.append(dict(runner=i, meeting=m, left=A, right=B))
                assert len(intervals) <= bound, "Exceeds analytic nonzero-move bound"
            t = nxt
            if t > R:
                break
        if t > R:
            break
    verdict = "empty" if t > R else "earliest_witness"
    if verdict == "earliest_witness":
        assert all(safe(v, t) for v in speeds)
    overlaps = [min(a["right"], b["right"]) - max(a["left"], b["left"])
                for a, b in zip(intervals, intervals[1:])]
    N = len(intervals)
    if intervals:
        A = min(x["left"] for x in intervals)
        B = intervals[-1]["right"]
        selected_excess = sum((x["right"]-x["left"] for x in intervals), F(0)) - (B-A)
        selected_excess_from_start = sum((x["right"]-max(L,x["left"]) for x in intervals), F(0)) - (B-L)
        H_union_difference = potential(speeds, B) - potential(speeds, A)
        H_start_difference = potential(speeds, B) - potential(speeds, L)
        assert (N-1)*eta <= selected_excess <= H_union_difference <= budget
        assert (N-m_L)*eta <= selected_excess_from_start <= H_start_difference <= Hmax-potential(speeds, L)
        span = [A, B]
    else:
        span = [L, L]
        selected_excess = selected_excess_from_start = H_union_difference = H_start_difference = F(0)
    return dict(id=case["id"], kind=case["kind"], speeds=speeds, window=[L,R], core_certificate=core_certificate,
        verdict=verdict, earliest=t if verdict=="earliest_witness" else None, final_time=t,
        final_residual_safe=all(safe(v,t) for v in speeds), trace=trace, calls=len(trace),
        completed_rounds=len(trace)//len(order), started_rounds=rounds, nonzero_moves=N,
        selected_intervals=intervals, consecutive_overlaps=overlaps, union_span=span,
        selected_excess=selected_excess, selected_excess_from_start=selected_excess_from_start,
        H_union_difference=H_union_difference, H_start_difference=H_start_difference,
        reciprocal_sum=reciprocal_sum, Q=Q, eta=eta, global_budget=budget, Hmax=Hmax,
        H_at_start=potential(speeds,L), phase_budget=Hmax-potential(speeds,L), m_L=m_L,
        K_global=K_global, K_phase=K_phase, K_used=bound)


def main():
    raw = (HERE / "protocol.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(raw)
    results = [analyze(c, protocol["algorithm"]["round_order"]) for c in protocol["cases"]]
    data = dict(status="pass", claim_status="OBSERVED on the frozen cases; analytic bounds remain HYPOTHESIS/proof candidate",
        baseline=protocol["baseline"], protocol_sha256=PROTOCOL_SHA256,
        primary_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), cases=results,
        counts=dict(window_cases=len(results), physical_configurations=9, auxiliary_configurations=2,
            nonzero_moves=sum(c["nonzero_moves"] for c in results), calls=sum(c["calls"] for c in results),
            empty=sum(c["verdict"]=="empty" for c in results)))
    (HERE / "results.json").write_text(json.dumps(data,indent=2,default=str)+"\n")
    print(json.dumps({"counts":data["counts"],"cases":[{k:c[k] for k in ["id","nonzero_moves","calls","K_global","K_phase","verdict","earliest"]} for c in results]},indent=2,default=str))


if __name__ == "__main__":
    main()
