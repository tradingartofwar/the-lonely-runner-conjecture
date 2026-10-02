#!/usr/bin/env python3
"""Exact common-lap certificates for the six predeclared selected results.

Uses only Python's standard library and no other project implementation.
Default/--check recomputes and compares; --write creates lattice.json.
"""

from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json


HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(item) for item in value]
    return value


def common_cell(velocities, time):
    """The exact closed safe cell containing an already safe rational time."""
    laps = []
    for index, speed in enumerate(velocities[1:], 1):
        phase = speed * time
        lap = phase.numerator // phase.denominator
        left = F(8 * lap + 1, 8 * speed)
        right = F(8 * lap + 7, 8 * speed)
        assert left <= time <= right
        laps.append({"index": index, "speed": speed, "lap": lap,
                     "left": left, "right": right})
    left = max(F(0), *(row["left"] for row in laps))
    right = min(F(1), *(row["right"] for row in laps))
    assert left <= time <= right
    pair_slacks = [[
        lower["speed"] * (8 * upper["lap"] + 7)
        - upper["speed"] * (8 * lower["lap"] + 1)
        for upper in laps] for lower in laps]
    assert all(value >= 0 for row in pair_slacks for value in row)
    assert (left < right) == all(value > 0 for row in pair_slacks for value in row)
    return {"interval": [left, right],
            "length": right - left,
            "lap_vector": [row["lap"] for row in laps],
            "left_controllers": [row["index"] for row in laps
                                 if row["left"] == left],
            "right_controllers": [row["index"] for row in laps
                                  if row["right"] == right],
            "pair_lap_slack_matrix": pair_slacks,
            "runner_laps": laps}


def witness_certificate(velocities, archived):
    time = F(archived["time"])
    cell = common_cell(velocities, time)
    a, b = time.numerator, time.denominator
    slacks = []
    distances = []
    for row in cell["runner_laps"]:
        v, m = row["speed"], row["lap"]
        lower = 8 * v * a - b * (8 * m + 1)
        upper = b * (8 * m + 7) - 8 * v * a
        assert lower >= 0 and upper >= 0
        slacks.append([row["index"], lower, upper])
        phase = v * time - m
        distances.append(min(phase, 1 - phase))
    assert distances == list(map(F, archived["distances"]))
    strict = all(lower > 0 and upper > 0 for _, lower, upper in slacks)
    assert strict == (archived["kind"] == "strict")
    return {"time": time, "kind": archived["kind"],
            "numerator": a, "denominator": b,
            "integer_slacks": slacks,
            "minimum_distance": min(distances),
            "margin_above_threshold": min(distances) - F(1, 8),
            "cell": cell}


def interval_certificate(velocities, archived):
    left, right = map(F, archived)
    cell = common_cell(velocities, (left + right) / 2)
    assert cell["interval"] == [left, right]
    endpoint_slacks = []
    for row in cell["runner_laps"]:
        v, m = row["speed"], row["lap"]
        lower = 8 * v * left.numerator - left.denominator * (8 * m + 1)
        upper = right.denominator * (8 * m + 7) - 8 * v * right.numerator
        assert lower >= 0 and upper >= 0
        endpoint_slacks.append([row["index"], lower, upper])
    cell["endpoint_integer_slacks"] = endpoint_slacks
    return cell


def build():
    protocol = json.loads((HERE / "protocol.json").read_text())
    results = json.loads((HERE / "results.json").read_text())
    assert protocol["n"] == 8 and protocol["reference_index"] == 0
    assert protocol["threshold"] == "1/8"
    assert results["protocol_sha256"] == digest(HERE / "protocol.json")
    assert [row["id"] for row in protocol["cases"]] == [
        row["id"] for row in results["cases"]]
    cases = []
    for prescribed, case in zip(protocol["cases"], results["cases"]):
        velocities = case["velocities"]
        assert velocities == prescribed["velocities"]
        assert velocities[0] == 0 and all(v > 0 for v in velocities[1:])
        selected = case["selected_certificate"]
        window = list(map(F, selected["window"]))
        components = [interval_certificate(velocities, item)
                      for item in selected["allowed_components"]]
        global_components = {tuple(map(F, item))
                             for item in case["full_allowed_components"]}
        for component in components:
            left, right = component["interval"]
            assert window[0] <= left <= right <= window[1]
            assert (left, right) in global_components
        duration = sum((item["length"] for item in components), F(0))
        assert duration == F(selected["actual_duration"])
        global_witness = witness_certificate(velocities, case["global_witness"])
        chosen_witness = witness_certificate(velocities, selected["witness"])
        assert tuple(global_witness["cell"]["interval"]) in global_components
        assert any(chosen_witness["cell"]["interval"] == item["interval"]
                   for item in components)
        cases.append({"id": case["id"], "velocities": velocities,
                      "selected_core": selected["core"],
                      "selected_window": window,
                      "selected_tree_bound": F(selected["bound"]),
                      "selected_actual_duration": duration,
                      "selected_surviving_cells": components,
                      "selected_witness": chosen_witness,
                      "global_witness": global_witness,
                      "same_global_and_selected_witness_cell":
                      global_witness["cell"]["interval"] ==
                      chosen_witness["cell"]["interval"]})
    return encode({"status": "OBSERVED exact certificates in the six fixed cases",
                   "protocol_sha256": digest(HERE / "protocol.json"),
                   "results_sha256": digest(HERE / "results.json"),
                   "script_sha256": digest(Path(__file__)),
                   "cases": cases,
                   "totals": {"cases": len(cases),
                              "witnesses": 2 * len(cases),
                              "selected_surviving_cells": sum(
                                  len(row["selected_surviving_cells"])
                                  for row in cases)}})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE / "lattice.json"
    if args.write:
        path.write_text(json.dumps(result, indent=2) + "\n")
    else:
        assert json.loads(path.read_text()) == result, "lattice.json mismatch"
    print(json.dumps(result["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
