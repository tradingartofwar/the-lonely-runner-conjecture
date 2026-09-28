#!/usr/bin/env python3
"""Independent finite threshold reconstruction; no primary imports/results.

The huge input is deliberately checked by a separate symbolic certificate,
never by event enumeration. Standard library only. Default is read-only replay;
--write writes this reviewer's verification.json for initial preservation.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def fl(x):
    return x.numerator // x.denominator


def phase(v, alpha, t):
    x = v * t + alpha
    return x - fl(x)


def safe(v, alpha, t, delta):
    p = phase(v, alpha, t)
    return delta <= p <= 1 - delta


def components(speeds, phases, delta, lo, hi):
    """Rebuild all closed safety components from rational threshold events."""
    assert lo <= hi and all(v > 0 for v in speeds)
    events = {lo, hi}
    for v, alpha in zip(speeds, phases):
        first = fl(v * lo + alpha) - 1
        last = fl(v * hi + alpha) + 1
        assert last - first < 10000, "Never enumerate the large diagnostic"
        for m in range(first, last + 1):
            for p in (delta, 1 - delta):
                t = (m + p - alpha) / v
                if lo <= t <= hi:
                    events.add(t)
    events = sorted(events)

    def all_safe(t):
        return all(safe(v, a, t, delta) for v, a in zip(speeds, phases))

    pieces = [(t, t) for t in events if all_safe(t)]
    for left, right in zip(events, events[1:]):
        if all_safe((left + right) / 2):
            assert all_safe(left) and all_safe(right)
            pieces.append((left, right))
    merged = []
    for left, right in sorted(pieces):
        if merged and left <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(right, merged[-1][1]))
        else:
            merged.append((left, right))
    return merged, len(events)


def serial_component(c):
    return [str(x) for x in c]


def check_case(case_id, pair, phases, delta, window, core=()):
    lo, hi = map(F, window)
    phases = tuple(map(F, phases))
    delta = F(delta)
    if core:
        core_components, _ = components(core, [F(0)] * len(core), delta, lo, hi)
        assert core_components == [(lo, hi)]
    actual, count = components(pair, phases, delta, lo, hi)
    earliest = actual[0][0] if actual else None
    first = actual[0] if actual else None
    equality = [] if earliest is None else [
        i for i, (v, a) in enumerate(zip(pair, phases))
        if phase(v, a, earliest) in (delta, 1 - delta)
    ]
    return {
        "case_id": case_id,
        "speeds": list(pair),
        "phases": list(map(str, phases)),
        "delta": str(delta),
        "window": list(map(str, (lo, hi))),
        "core": list(core),
        "core_window_certified": bool(core),
        "earliest": str(earliest) if earliest is not None else None,
        "first_component": serial_component(first) if first else None,
        "first_component_positive": bool(first and first[0] < first[1]),
        "earliest_equality_labels": equality,
        "all_components": list(map(serial_component, actual)),
        "any_positive_component": any(a < b for a, b in actual),
        "threshold_events": count,
    }


def phase_projection(v, alpha, t, delta):
    """Alternative phase/collision-gap implementation, only for scope traces."""
    p = phase(v, alpha, t)
    if delta <= p <= 1 - delta:
        return t
    if p < delta:
        return t + (delta - p) / v
    return t + (1 + delta - p) / v


def trace(speeds, phases, delta, initial, order):
    t = F(initial)
    out = []
    for i in order:
        t = phase_projection(speeds[i], F(phases[i]), t, F(delta))
        out.append(str(t))
    return out


def large_certificate():
    q, budget = 840, 10**12
    b = 8 * budget * q
    delta, anchor = F(1, 8), F(17, 56)
    slow_entry = anchor + delta / q
    assert (q * anchor).denominator == 1
    assert (b * slow_entry).denominator == 1
    left = slow_entry + delta / b
    right = slow_entry + (1 - delta) / b
    assert left == anchor + F(8 * budget + 1, 64 * budget * q)
    assert right == anchor + F(8 * budget + 7, 64 * budget * q)
    bands = []
    for v in (1, 4, 5, 6, 7, q, b):
        lap = fl(v * left)
        low, high = v * left - lap, v * right - lap
        assert delta <= low <= high <= 1 - delta
        bands.append({"speed": v, "lap": lap,
                      "left_phase": str(low), "right_phase": str(high)})
    assert right < F(5, 16)
    assert right - left == F(3, 32 * budget * q)
    # All times from anchor to slow_entry are blocked by q; then b blocks
    # until left. At right b exits its safe band while every other runner
    # is strictly safe. This certifies earliest time and first component.
    assert bands[-1]["left_phase"] == "1/8"
    assert bands[-1]["right_phase"] == "7/8"
    assert all(delta < F(x["left_phase"]) <= F(x["right_phase"]) < 1-delta
               for x in bands[:-1])
    return {"case_id": "large_B_10e12", "budget": budget,
            "speeds": [q, b], "window": ["17/56", "5/16"],
            "earliest": str(left), "first_component": serial_component((left, right)),
            "width": str(right-left), "lifted_bands": bands,
            "event_enumeration": False}


def build():
    protocol_bytes = (HERE / "protocol.json").read_bytes()
    protocol = json.loads(protocol_bytes)
    rows = []
    for pair in protocol["physical_pairs"]:
        for name, window in protocol["family_windows"].items():
            rows.append(check_case(f"family_{pair[0]}_{pair[1]}_{name}", pair,
                                   (0, 0), "1/8", window, protocol["fixed_core"]))
    for pair in ((840, 6720), (840, 5880)):
        rows.append(check_case(f"obstruction_{pair[0]}_{pair[1]}_I", pair,
                               (0, 0), "1/8", protocol["family_windows"]["I"],
                               protocol["fixed_core"]))
    small = protocol["small_gcd_controls"]
    for pair in small["pairs"]:
        rows.append(check_case(f"small_gcd_{pair[0]}_{pair[1]}", pair,
                               (0, 0), "1/8", small["window"], small["core"]))
    for label, right in (("empty", "9/8"), ("edge", "73/64"), ("positive", "37/32")):
        rows.append(check_case(f"aux_fourth_{label}", (1, 8), (0, 0), "1/8", ("7/8", right)))
    rows.append(check_case("aux_quarter_contacts", (1, 1), (0, "1/2"), "1/4", ("0", "1")))
    assert len(rows) == 20
    fourth_trace = trace((1, 8), (0, 0), "1/8", "7/8", (0, 1, 0, 1))
    assert fourth_trace == ["7/8", "57/64", "9/8", "73/64"]
    third = check_case("scope_delta_third", (1, 1), (0, "1/2"), "1/3", ("0", "2"))
    assert third["earliest"] is None
    third["projection_trace"] = trace((1, 1), (0, "1/2"), "1/3", "0", (0, 1, 0, 1))
    assert third["projection_trace"] == ["1/3", "5/6", "4/3", "11/6"]
    triple = check_case("scope_three_residual", (1, 7, 8), (0, 0, 0), "1/8", ("7/8", "6/5"))
    assert triple["earliest"] == "65/56"
    triple["projection_trace"] = trace((1, 7, 8), (0, 0, 0), "1/8", "7/8", (0, 1, 2, 0, 1, 2))
    assert triple["projection_trace"] == ["7/8", "7/8", "57/64", "9/8", "9/8", "73/64"]
    triple["phase_7_after_two_sweeps"] = str(phase(7, 0, F(73, 64)))
    assert triple["phase_7_after_two_sweeps"] == "63/64"
    follow_trace = trace((1, 7, 8), (0, 0, 0), "1/8", "7/8", (0, 1, 2, 1, 2, 0, 1, 2, 1, 2))
    assert follow_trace[-1] == triple["earliest"] == "65/56"
    ratio7 = next(r for r in rows if r["case_id"] == "obstruction_840_5880_I")
    assert not ratio7["first_component_positive"] and ratio7["any_positive_component"]
    return {
        "method": "Independent exact threshold-event reconstruction; no primary imports or results",
        "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
        "bounded_cases": rows,
        "bounded_case_count": len(rows),
        "fourth_projection_trace": fourth_trace,
        "negative_scope_controls": [third, triple],
        "large_symbolic_case": large_certificate(),
        "post_protocol_follow_on": {
            "scope": "Same frozen three-runner input; nested selector replaces failed two-sweep order",
            "case_id": "scope_three_residual",
            "order": [1, 7, 8, 7, 8, 1, 7, 8, 7, 8],
            "projection_trace": follow_trace,
            "earliest": triple["earliest"],
            "matches_independent_event_reconstruction": True,
            "new_inputs_tested": 0,
        },
        "status": "All explicit assertions passed; finite reconstruction is not proof of the unbounded theorem",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = build()
    output = json.dumps(data, indent=2, sort_keys=True) + "\n"
    target = HERE / "verification.json"
    if args.write:
        target.write_text(output)
    else:
        assert target.read_text() == output, "Reviewer results changed"
    print(json.dumps({"bounded_cases": len(data["bounded_cases"]),
                      "scope_controls": len(data["negative_scope_controls"]),
                      "large_symbolic_case": True,
                      "verification_sha256": hashlib.sha256(output.encode()).hexdigest()}))


if __name__ == "__main__":
    main()
