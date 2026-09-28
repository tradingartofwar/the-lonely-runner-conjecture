#!/usr/bin/env python3
"""Independent exact audit of protocol.json; standard library only.

This verifier receives only the frozen protocol, not the primary implementation.
It enumerates open occurrences and their full boundary partition explicitly.
"""

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROUND = (0, 1, 2, 3, 2, 3, 1, 2, 3, 2, 3)


def ceiling(x):
    return -((-x.numerator) // x.denominator)


def occurrences(period, start, left, right):
    """An explicit finite list includes every open occurrence meeting [L,R]."""
    low = (left - start) // period - 2
    high = ceiling((right - start) / period) + 2
    result = []
    for m in range(low, high + 1):
        a = start + m * period
        b = a + period / 4
        if b >= left and a <= right:
            result.append((m, a, b))
    return result


def contains(occurrence, t):
    return occurrence[1] < t < occurrence[2]


def safe(t, trains):
    return not any(contains(occ, t) for train in trains for occ in train)


def complete_safe_components(trains, left, right):
    """Classify every threshold point and every open partition cell."""
    boundaries = {left, right}
    for train in trains:
        for _, a, b in train:
            if left <= a <= right:
                boundaries.add(a)
            if left <= b <= right:
                boundaries.add(b)
    boundaries = sorted(boundaries)
    pieces = [(t, t) for t in boundaries if safe(t, trains)]
    point_classification = [{"time": t, "safe": safe(t, trains)}
                            for t in boundaries]
    cell_classification = []
    for a, b in zip(boundaries, boundaries[1:]):
        is_safe = safe((a + b) / 2, trains)
        cell_classification.append({"left": a, "right": b, "safe": is_safe})
        if is_safe:
            # Complements of open blockers are closed; inspect both endpoints.
            assert safe(a, trains) and safe(b, trains)
            pieces.append((a, b))
    merged = []
    for a, b in sorted(pieces):
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged, point_classification, cell_classification


def square_occurrences(word):
    result = []
    for start in range(len(word)):
        for size in range(1, (len(word) - start) // 2 + 1):
            if word[start:start + size] == word[start + size:start + 2 * size]:
                result.append({"start": start, "block_length": size,
                               "block": word[start:start + size]})
    return result


def run_selector(trains, periods, left, right):
    order = sorted(range(4), key=lambda label: (1 / periods[label], label))
    schedule = [order[position] for position in ROUND]
    t = left
    trace = []
    rounds = 0
    # The finite occurrence list supplies a check budget, not an assumed theorem.
    available = sum(len(train) for train in trains)
    visited_moves = set()
    if safe(t, trains):
        status = "safe"
    else:
        status = None
        while status is None:
            rounds += 1
            changed = False
            for label in schedule:
                before = t
                blocking = [occ for occ in trains[label] if contains(occ, t)]
                assert len(blocking) <= 1
                chosen = blocking[0] if blocking else None
                if chosen is not None:
                    t = chosen[2]
                    assert t > before
                    key = (label, chosen[0])
                    assert key not in visited_moves
                    visited_moves.add(key)
                    assert len(visited_moves) <= available
                    changed = True
                trace.append({"call": len(trace) + 1, "round": rounds,
                              "label": label, "before": before, "after": t,
                              "moved": t != before,
                              "occurrence": None if chosen is None else
                              {"m": chosen[0], "left": chosen[1], "right": chosen[2]}})
                if t > right:
                    status = "empty"
                    break
            if status is None:
                if safe(t, trains):
                    status = "safe"
                else:
                    assert changed, "An unsafe complete round must advance."
    nonzero = [entry for entry in trace if entry["moved"]]
    labels = [entry["label"] for entry in nonzero]
    squares = square_occurrences(labels)
    return order, {"status": status, "time": t, "calls": len(trace),
                   "rounds": rounds, "trace": trace, "nonzero_trace": nonzero,
                   "moving_labels": labels, "advances": len(nonzero),
                   "square_free": not squares, "squares": squares}


def affine_endpoint(label, occurrence, right=False):
    """Eight coefficients: four periods followed by four starts."""
    coefficients = [F(0) for _ in range(8)]
    coefficients[label] = F(occurrence) + (F(1, 4) if right else 0)
    coefficients[4 + label] = F(1)
    return coefficients


def cycle_checks(tile, periods, starts):
    word = tile["word"]
    counts = [word.count(label) for label in range(4)]
    assert counts == tile["q"]
    base_indices = []
    seen = [0] * 4
    for label in word:
        base_indices.append(seen[label])
        seen[label] += 1
    result = []
    for anchor in range(4):
        first = word.index(anchor)
        chain = []
        for position in range(first, first + len(word) + 1):
            cycle, offset = divmod(position, len(word))
            label = word[offset]
            m = base_indices[offset] + cycle * counts[label]
            chain.append((label, m))
        assert chain[-1][0] == anchor
        assert chain[-1][1] - chain[0][1] == counts[anchor]
        coefficients = [F(0)] * 8
        gaps = []
        for (i, m), (j, n) in zip(chain, chain[1:]):
            actual = starts[i] + (m + F(1, 4)) * periods[i] - starts[j] - n * periods[j]
            previous = affine_endpoint(i, m, right=True)
            following = affine_endpoint(j, n)
            difference = [a - b for a, b in zip(previous, following)]
            coefficients = [a + b for a, b in zip(coefficients, difference)]
            gaps.append({"previous_label": i, "previous_m": m,
                         "next_label": j, "next_m": n, "gap": actual})
        expected_coefficients = [F(q, 4) for q in counts] + [F(0)] * 4
        expected_coefficients[anchor] -= counts[anchor]
        expected = sum(F(q, 4) * p for q, p in zip(counts, periods)) - counts[anchor] * periods[anchor]
        total = sum(gap["gap"] for gap in gaps)
        coefficient_value = sum(c * v for c, v in zip(coefficients, periods + starts))
        result.append({"anchor": anchor, "q": counts, "chain": chain,
                       "gaps": gaps, "sum": total, "expected": expected,
                       "coefficients": coefficients,
                       "expected_coefficients": expected_coefficients,
                       "identity_ok": total == expected == coefficient_value,
                       "coefficient_identity_ok": coefficients == expected_coefficients})
    return result


def occupancy(fixture):
    x, phase = F(fixture["x"]), F(fixture["phase"])
    threshold = F(1, 8)
    # ||t+phase||<1/8: intervals centered at integer-phase.
    clips = []
    for m in range((phase - threshold) // 1 - 2, ceiling(x + phase + threshold) + 3):
        a, b = F(m) - phase - threshold, F(m) - phase + threshold
        clipped_left, clipped_right = max(F(0), a), min(x, b)
        if clipped_left < clipped_right:
            clips.append({"m": m, "left": clipped_left, "right": clipped_right})
    measured = sum((clip["right"] - clip["left"] for clip in clips), F(0))
    whole = x // 1
    fraction = x - whole
    formula = F(whole, 4) + max(F(0), fraction - F(3, 4))
    return {"x": x, "phase": phase, "clips": clips, "blocked": measured,
            "formula": formula, "x_over_7": x / 7,
            "formula_ok": measured == formula,
            "inequality_ok": measured >= x / 7,
            "equality": measured == x / 7}


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def main():
    protocol_path = HERE / "protocol.json"
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    left, right = map(F, protocol["window"])
    cases = []
    for tile in protocol["tiles"]:
        for perturbation in protocol["perturbations"]:
            values = {"periods": list(map(F, tile["periods"])),
                      "starts": list(map(F, tile["starts"]))}
            if perturbation["field"] is not None:
                values[perturbation["field"]][perturbation["runner"]] += F(perturbation["delta"])
            periods, starts = values["periods"], values["starts"]
            assert all(p > 0 for p in periods)
            trains = [occurrences(p, s, left, right) for p, s in zip(periods, starts)]
            components, points, cells = complete_safe_components(trains, left, right)
            earliest = components[0][0] if components else None
            order, selector = run_selector(trains, periods, left, right)
            agreement = ((selector["status"] == "empty" and earliest is None)
                         or (selector["status"] == "safe" and selector["time"] == earliest))
            cycles = cycle_checks(tile, periods, starts)
            cases.append({"tile": tile["id"], "perturbation": perturbation["id"],
                          "periods": periods, "starts": starts, "order": order,
                          "window": [left, right], "safe_components": components,
                          "earliest": earliest, "threshold_points": points,
                          "partition_cells": cells, "selector": selector,
                          "selector_agrees_with_partition": agreement,
                          "cycles": cycles})
    occupancy_checks = [occupancy(fixture) for fixture in protocol["occupancy_fixtures"]]
    summary = {
        "window_cases": len(cases),
        "partition_points": sum(len(case["threshold_points"]) for case in cases),
        "partition_cells": sum(len(case["partition_cells"]) for case in cases),
        "cycle_anchor_checks": sum(len(case["cycles"]) for case in cases),
        "occupancy_checks": len(occupancy_checks),
        "selector_partition_agreements": sum(case["selector_agrees_with_partition"] for case in cases),
        "square_free_words": sum(case["selector"]["square_free"] for case in cases),
        "cycles_pass": all(cycle["identity_ok"] and cycle["coefficient_identity_ok"]
                           for case in cases for cycle in case["cycles"]),
        "occupancy_pass": all(item["formula_ok"] and item["inequality_ok"]
                              for item in occupancy_checks),
        "max_advances_observed": max(case["selector"]["advances"] for case in cases),
        "max_calls_observed": max(case["selector"]["calls"] for case in cases),
    }
    summary["all_pass"] = (summary["selector_partition_agreements"] == len(cases)
                           and summary["square_free_words"] == len(cases)
                           and summary["cycles_pass"] and summary["occupancy_pass"])
    result = {"protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
              "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "Explicit open occurrences; complete threshold partition; direct containment projection.",
              "status": "OBSERVED on frozen auxiliary fixtures; not a theorem or primary-output comparison.",
              "summary": summary, "cases": cases, "occupancy": occupancy_checks}
    (HERE / "verification.json").write_text(json.dumps(encode(result), indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if not summary["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
