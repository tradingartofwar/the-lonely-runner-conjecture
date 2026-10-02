#!/usr/bin/env python3
"""Four direct projections for two residual runners; standard library only.

No lap/time scanning. --check verifies the saved exact results read-only.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
DELTA = F(1, 8)
CORE = (1, 4, 5, 6, 7)
WINDOWS = {"I": (F(17, 56), F(5, 16)),
           "K": (F(17, 48), F(3, 8)),
           "H": (F(25, 56), F(15, 32))}


def ceiling(x):
    return -((-x.numerator) // x.denominator)


def distance(x):
    p = x % 1
    return min(p, 1 - p)


def project(v, alpha, delta, t):
    """Least safe time >=t, including both threshold endpoints."""
    lap = ceiling(v * t + alpha - 1 + delta)
    out = max(t, (lap + delta - alpha) / v)
    assert distance(v * out + alpha) >= delta
    assert 0 <= out - t < 2 * delta / v
    return out, {"speed": str(v), "phase": str(alpha), "input": str(t),
                 "output": str(out), "lap": lap,
                 "advance": str(out - t)}


def lifted_certificate(speeds, phases, delta, left, right):
    rows = []
    for v, alpha in zip(speeds, phases):
        mid = v * (left + right) / 2 + alpha
        lap = mid.numerator // mid.denominator
        lo, hi = v * left + alpha - lap, v * right + alpha - lap
        assert delta <= lo <= hi <= 1 - delta
        rows.append({"speed": str(v), "phase": str(alpha), "lap": lap,
                     "left_phase": str(lo), "right_phase": str(hi),
                     "minimum_margin": str(min(lo - delta, 1 - delta - hi))})
    return rows


def run_case(case_id, speeds, phases, delta, left, right, core=(), kind="physical"):
    a, b = map(F, speeds)
    alpha, beta = map(F, phases)
    assert 0 < a <= b and 0 < delta < F(1, 2)
    assert 2 * delta / b <= (1 - 2 * delta) / a
    assert left <= right
    t = left
    trace = []
    for v, ph in ((a, alpha), (b, beta), (a, alpha), (b, beta)):
        t, row = project(v, ph, delta, t)
        trace.append(row)
    assert all(distance(v * t + ph) >= delta
               for v, ph in ((a, alpha), (b, beta)))
    core_rows = lifted_certificate(core, (F(0),) * len(core), delta, left, right)
    in_window = t <= right
    component = None
    certificate = None
    if in_window:
        end = right
        for v, ph in ((a, alpha), (b, beta)):
            lap = (v * t + ph).numerator // (v * t + ph).denominator
            end = min(end, (lap + 1 - delta - ph) / v)
        assert t <= end
        component = [str(t), str(end)]
        certificate = lifted_certificate(tuple(map(F, core)) + (a, b),
                                         (F(0),) * len(core) + (alpha, beta),
                                         delta, t, end)
    return {"case_id": case_id, "kind": kind,
            "speeds": [str(a), str(b)], "phases": [str(alpha), str(beta)],
            "delta": str(delta), "window": [str(left), str(right)],
            "core": list(core), "core_window_certificate": core_rows,
            "trace": trace, "arithmetic_projections": len(trace),
            "earliest_at_or_after_left": str(t),
            "earliest_in_window": str(t) if in_window else None,
            "first_component": component,
            "first_component_kind": ("positive" if component and t < F(component[1])
                                     else "point" if component else "empty"),
            "full_first_component_certificate": certificate}


def calculate():
    cases = []
    for a, b in ((11, 13), (11, 16), (16, 23), (3, 8)):
        for name, (lo, hi) in WINDOWS.items():
            cases.append(run_case(f"family_{a}_{b}_{name}", (a, b), (0, 0),
                                  DELTA, lo, hi, CORE))
    for case_id, b, kind in (("obstruction_B1_I", 6720, "physical"),
                             ("ratio7_I", 5880, "physical boundary"),
                             ("obstruction_B1000000000000_I", 6720000000000000,
                              "formula-only large input")):
        cases.append(run_case(case_id, (840, b), (0, 0), DELTA,
                              *WINDOWS["I"], CORE, kind))
    for b in (113, 112):
        cases.append(run_case(f"small_gcd_{b}", (56, b), (0, 0), DELTA,
                              F(65, 512), F(79, 576), (1, 4, 5, 64, 72)))
    for suffix, right in (("empty", F(9, 8)), ("edge", F(73, 64)),
                          ("positive", F(37, 32))):
        cases.append(run_case(f"aux_four_{suffix}", (1, 8), (0, 0), DELTA,
                              F(7, 8), right, kind="auxiliary arithmetic"))
    cases.append(run_case("aux_quarter_contact", (1, 1), (0, F(1, 2)),
                          F(1, 4), F(0), F(1), kind="auxiliary shifted phases"))

    # The theorem's speed/threshold condition is deliberately violated here.
    t, trace = F(0), []
    for alpha in (F(0), F(1, 2), F(0), F(1, 2)):
        t, row = project(F(1), alpha, F(1, 3), t)
        trace.append(row)
    assert t == F(11, 6) and distance(t) < F(1, 3)
    bad_threshold = {"delta": "1/3", "speeds": [1, 1], "phases": ["0", "1/2"],
                     "trace": trace, "final_time": str(t),
                     "first_runner_distance": str(distance(t)),
                     "jointly_safe": False}

    # Two sweeps over three residual runners need not finish.
    t, trace = F(7, 8), []
    for v in (1, 7, 8, 1, 7, 8):
        t, row = project(F(v), F(0), DELTA, t)
        trace.append(row)
    assert t == F(73, 64)
    assert distance(7 * t) == F(1, 64) < DELTA
    final_two_sweeps = t
    more = []
    for v in (1, 7, 8):
        t, row = project(F(v), F(0), DELTA, t)
        more.append(row)
    assert t == F(65, 56)
    assert all(distance(v * t) >= DELTA for v in (1, 7, 8))
    three = {"speeds": [1, 7, 8], "phases": ["0", "0", "0"],
             "delta": "1/8", "left": "7/8", "trace": trace,
             "two_sweep_time": str(final_two_sweeps), "blocked_speed": 7,
             "blocked_distance": "1/64", "jointly_safe_after_two_sweeps": False,
             "third_sweep": more, "earliest_after_left": str(t)}
    return {"status": "pass", "cases": cases,
            "case_count": len(cases), "bounded_case_count": len(cases) - 1,
            "scope_failures": {"threshold_outside_hypothesis": bad_threshold,
                               "three_residual_two_sweeps": three},
            "claim_status": "General argument is a proof candidate; finite exact controls only."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    result = calculate()
    target = HERE / "results.json"
    if args.check:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    counts = {k: sum(c["first_component_kind"] == k for c in result["cases"])
              for k in ("positive", "point", "empty")}
    print(json.dumps({"status": "pass", "cases": result["case_count"],
                      "bounded_cases": result["bounded_case_count"],
                      "first_component_outcomes": counts,
                      "scope_counterexamples": 2}))


if __name__ == "__main__":
    main()
