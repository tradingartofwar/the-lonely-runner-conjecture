#!/usr/bin/env python3
"""Independent exact reconstruction and fixed22 projection diagnostic.

No primary code/results imports. Threshold events supply the independent
bounded oracle. Projection traces use fractional-phase cases rather than the
coordinator's ceiling formula. Standard library only; default replay is read-only.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def floor(x):
    return x.numerator // x.denominator


def frac(x):
    return x - floor(x)


def safe(v, alpha, t, delta):
    return delta <= frac(v * t + alpha) <= 1 - delta


def allowed(speeds, phases, delta, lo, hi):
    events = {lo, hi}
    for v, alpha in zip(speeds, phases):
        low_lap = floor(v * lo + alpha) - 1
        high_lap = floor(v * hi + alpha) + 1
        assert high_lap - low_lap < 10000
        for lap in range(low_lap, high_lap + 1):
            for boundary in (delta, 1 - delta):
                t = (lap + boundary - alpha) / v
                if lo <= t <= hi:
                    events.add(t)
    events = sorted(events)

    def all_safe(t):
        return all(safe(v, ph, t, delta) for v, ph in zip(speeds, phases))

    parts = [(t, t) for t in events if all_safe(t)]
    for a, b in zip(events, events[1:]):
        if all_safe((a + b) / 2):
            assert all_safe(a) and all_safe(b)
            parts.append((a, b))
    components = []
    for a, b in sorted(parts):
        if components and a <= components[-1][1]:
            components[-1] = (components[-1][0], max(b, components[-1][1]))
        else:
            components.append((a, b))
    return components, len(events)


def project_from_phase(v, alpha, delta, t):
    p = frac(v * t + alpha)
    if delta <= p <= 1 - delta:
        return t
    if p < delta:
        return t + (delta - p) / v
    return t + (1 + delta - p) / v


def trace22(speeds, phases, delta, lo):
    triple = (1, 2, 3, 2, 3, 1, 2, 3, 2, 3)
    order = (0,) + triple + (0,) + triple
    assert len(order) == 22
    t = lo
    rows = []
    for i in order:
        old = t
        t = project_from_phase(speeds[i], phases[i], delta, t)
        assert 0 <= t - old < 2 * delta / speeds[i]
        assert safe(speeds[i], phases[i], t, delta)
        rows.append({"runner_index": i, "speed": speeds[i],
                     "input": str(old), "output": str(t)})
    return t, rows


def case_record(case_id, speeds, phases, delta, window, core, kind):
    assert len(speeds) == 4 and list(speeds) == sorted(speeds)
    assert speeds[0] > 0
    lo, hi = map(F, window)
    phases = list(map(F, phases))
    delta = F(delta)
    oracle, event_count = allowed(speeds, phases, delta, lo, hi)
    if core:
        core_oracle, _ = allowed(core, [F(0)] * len(core), delta, lo, hi)
        assert core_oracle == [(lo, hi)]
    a, b, c, d = speeds
    triple_wait = 2 * delta / b + 4 * delta / c + 8 * delta / d
    slow_width = (1 - 2 * delta) / a
    condition = triple_wait <= slow_width
    final, trace = trace22(speeds, phases, delta, lo)
    final_safe = all(safe(v, ph, final, delta) for v, ph in zip(speeds, phases))
    if final > hi:
        raw_verdict = "empty"
        assert not oracle
    elif final_safe:
        raw_verdict = "earliest"
        assert oracle and oracle[0][0] == final
    else:
        raw_verdict = "inconclusive"
        if oracle:
            assert final <= oracle[0][0]
    if condition:
        assert final_safe
    first = oracle[0] if oracle else None
    return {
        "case_id": case_id, "kind": kind, "speeds": list(speeds),
        "phases": list(map(str, phases)), "delta": str(delta),
        "window": list(map(str, (lo, hi))), "core": list(core),
        "core_window_certified": bool(core),
        "triple_wait_bound": str(triple_wait), "slow_safe_lap_width": str(slow_width),
        "condition_margin": str(slow_width - triple_wait),
        "condition_pass": condition,
        "gated_condition_verdict": ("verified_by_condition" if condition else "unverified_by_condition"),
        "fixed22_trace": trace, "fixed22_final": str(final),
        "fixed22_final_safe": final_safe, "raw_verdict": raw_verdict,
        "unsafe_final_labels": [i for i, (v, ph) in enumerate(zip(speeds, phases))
                                if not safe(v, ph, final, delta)],
        "oracle_earliest": str(first[0]) if first else None,
        "oracle_first_component": list(map(str, first)) if first else None,
        "oracle_first_component_positive": bool(first and first[0] < first[1]),
        "oracle_all_components": [list(map(str, p)) for p in oracle],
        "oracle_any_positive_component": any(l < r for l, r in oracle),
        "oracle_total_duration": str(sum((r - l for l, r in oracle), F(0))),
        "oracle_threshold_events": event_count,
        "oracle_earliest_equality_labels": [] if not first else [
            i for i, (v, ph) in enumerate(zip(speeds, phases))
            if frac(v * first[0] + ph) in (delta, 1 - delta)
        ],
    }


def build():
    raw = (HERE / "protocol.json").read_bytes()
    protocol = json.loads(raw)
    out = []
    for row in protocol["cases"]:
        out.append(case_record(row["id"], row["speeds"], (0, 0, 0, 0),
                               protocol["threshold"], protocol["physical_window"],
                               protocol["physical_core"], "physical"))
    for row in protocol["auxiliary_cases"]:
        out.append(case_record(row["id"], row["speeds"], row["phases"],
                               protocol["threshold"], row["window"], (), "auxiliary"))
    assert len(out) == 10
    assert all(not row["condition_pass"] for row in out[:8])
    assert all(row["condition_pass"] for row in out[8:])
    assert out[-1]["condition_margin"] == "0"
    assert out[-1]["oracle_earliest"] == "1/120"
    assert out[-1]["oracle_first_component"] == ["1/120", "1/120"]
    return {"method": "Independent exact threshold events; phase-case22trace; no primary imports",
            "protocol_sha256": hashlib.sha256(raw).hexdigest(),
            "bounded_case_count": len(out), "cases": out,
            "limits": "Finite10inputs; unbounded conditional theorem rests on supplied proof; no unconditional22theorem asserted"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    result = build()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    target = HERE / "verification.json"
    if args.write:
        target.write_text(output)
    else:
        assert target.read_text() == output
    print(json.dumps({"case_count": len(result["cases"]),
                      "condition_passes": sum(c["condition_pass"] for c in result["cases"]),
                      "raw_verdicts": {label: sum(c["raw_verdict"] == label for c in result["cases"])
                                       for label in ("earliest", "empty", "inconclusive")},
                      "verification_sha256": hashlib.sha256(output.encode()).hexdigest()}))


if __name__ == "__main__":
    main()
