"""Primary exact calculation for the frozen shared-pair protocol.

The calculation deliberately keeps two questions separate:

* does every positive-length occurrence of the frozen base pair lie in the
  closed safe phase intervals of both complementary runners; and
* if it does, is the resulting already-known five-edge lower bound positive?

``--write`` creates the deterministic archive.  ``--check`` is read-only and
reconstructs every archived field with standard-library ``Fraction``
arithmetic.  No claim beyond the cases frozen in ``protocol.json`` is made.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.json"
OUT = HERE / "results.json"
FROZEN_PROTOCOL_SHA256 = "52cdd98452f9e47c082bb53703b1a20dc07fa9e47860bc7bbf0e2eb1d00378f3"
DELTA = F(1, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def floor(value: F) -> int:
    return value.numerator // value.denominator


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Counter):
        value = dict(value)
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(v) for v in value]
    return value


def cmp(cost: Counter | None, category: str, left: F, op: str, right: F) -> bool:
    """Charge a semantic exact-rational comparison used by the certificate.

    Sorting, dictionary equality, assertions, and archive readback comparisons
    are verification/bookkeeping and are intentionally outside this ledger.
    """
    if cost is not None:
        cost["exact_rational_comparisons"] += 1
        cost["comparison_" + category] += 1
    if op == "<":
        return left < right
    if op == "<=":
        return left <= right
    if op == "==":
        return left == right
    if op == ">=":
        return left >= right
    if op == ">":
        return left > right
    raise ValueError(op)


def charged_max(a: F, b: F, cost: Counter | None, category: str) -> F:
    return b if cmp(cost, category, a, "<", b) else a


def charged_min(a: F, b: F, cost: Counter | None, category: str) -> F:
    return a if cmp(cost, category, a, "<", b) else b


def phase(speed: int, time: F) -> F:
    return (speed * time) % 1


def distance(speed: int, time: F) -> F:
    p = phase(speed, time)
    return min(p, 1 - p)


def phase_state(speed: int, time: F, cost: Counter | None = None) -> dict:
    p = phase(speed, time)
    d = min(p, 1 - p)
    if cmp(cost, "phase_state", d, "<", DELTA):
        state = "blocking"
    elif cmp(cost, "phase_state", d, "==", DELTA):
        state = "contact"
    else:
        state = "safe"
    return {"phase": p, "distance": d, "state": state}


def blocking_pieces(speed: int, window: tuple[F, F], cost: Counter | None) -> list[dict]:
    """Strict blocking pieces, with exact lap labels and endpoint membership."""
    lo_window, hi_window = window
    pieces = []
    for lap in range(floor(speed * lo_window) - 1, floor(speed * hi_window) + 2):
        if cost is not None:
            cost["lap_candidates"] += 1
        raw_lo = (F(lap) - DELTA) / speed
        raw_hi = (F(lap) + DELTA) / speed
        lo = charged_max(lo_window, raw_lo, cost, "lap_clip")
        hi = charged_min(hi_window, raw_hi, cost, "lap_clip")
        if cmp(cost, "lap_nonempty", lo, "<", hi):
            left_included = phase_state(speed, lo, cost)["state"] == "blocking"
            right_included = phase_state(speed, hi, cost)["state"] == "blocking"
            pieces.append(
                {
                    "interval": (lo, hi),
                    "lap": lap,
                    "left_included": left_included,
                    "right_included": right_included,
                }
            )
    if cost is not None:
        cost["blocking_pieces_enumerated"] += len(pieces)
    return pieces


def intersect_piece_lists(
    first: list[dict], second: list[dict], cost: Counter | None, *, output_key: str
) -> list[dict]:
    """Two-pointer positive-length intersection retaining both lap labels."""
    i = j = 0
    output = []
    while i < len(first) and j < len(second):
        if cost is not None:
            cost["pair_component_intersection_steps"] += 1
        a, b = first[i]["interval"]
        c, d = second[j]["interval"]
        lo = charged_max(a, c, cost, "intersection_clip")
        hi = charged_min(b, d, cost, "intersection_clip")
        if cmp(cost, "intersection_nonempty", lo, "<", hi):
            left_included = (
                (first[i]["left_included"] if lo == a else True)
                and (second[j]["left_included"] if lo == c else True)
            )
            right_included = (
                (first[i]["right_included"] if hi == b else True)
                and (second[j]["right_included"] if hi == d else True)
            )
            output.append(
                {
                    "interval": (lo, hi),
                    "laps": (first[i]["lap"], second[j]["lap"]),
                    "left_included": left_included,
                    "right_included": right_included,
                }
            )
        # Charge one comparison when unequal, two when equality is tested.
        if cmp(cost, "intersection_advance", b, "<", d):
            i += 1
        elif cmp(cost, "intersection_advance", d, "<", b):
            j += 1
        else:
            i += 1
            j += 1
    if cost is not None:
        cost[output_key] += len(output)
    return output


def phase_boundaries(speed: int, interval: tuple[F, F], cost: Counter) -> list[F]:
    """Interior integer and threshold crossings for one tested phase."""
    lo, hi = interval
    candidates = []
    for lap in range(floor(speed * lo) - 1, floor(speed * hi) + 2):
        for offset in (F(0), DELTA, 1 - DELTA):
            cost["phase_boundary_candidates"] += 1
            t = (lap + offset) / speed
            if cmp(cost, "phase_boundary", lo, "<", t) and cmp(
                cost, "phase_boundary", t, "<", hi
            ):
                candidates.append(t)
    return candidates


def endpoint_record(time: F, speeds: tuple[int, ...], cost: Counter) -> dict:
    cost["endpoint_times_checked"] += 1
    states = {}
    for speed in speeds:
        cost["endpoint_speed_checks"] += 1
        states[speed] = phase_state(speed, time, cost)
    return {"time": time, "states": states}


def analyze_component(
    component: dict,
    base_pair: tuple[int, int],
    complement: tuple[int, int],
    cost: Counter,
) -> dict:
    """Partition only at relevant phase boundaries and test every exact cell."""
    lo, hi = component["interval"]
    split_points = []
    per_speed_boundaries = {}
    for speed in complement:
        boundaries = phase_boundaries(speed, (lo, hi), cost)
        per_speed_boundaries[speed] = boundaries
        split_points.extend(boundaries)
    points = [lo] + sorted(set(split_points)) + [hi]
    cost["threshold_partitions"] += len(points) - 2

    cells = []
    violations = []
    for cell_lo, cell_hi in zip(points, points[1:]):
        mid = (cell_lo + cell_hi) / 2
        ranges = {}
        for speed in complement:
            lap = floor(speed * mid)
            p_lo = speed * cell_lo - lap
            p_hi = speed * cell_hi - lap
            safe_closed = cmp(cost, "phase_safe", DELTA, "<=", p_lo) and cmp(
                cost, "phase_safe", p_hi, "<=", 1 - DELTA
            )
            cost["complement_phase_range_checks"] += 1
            ranges[speed] = {
                "phase_lap": lap,
                "unwrapped_endpoint_phase_range": (p_lo, p_hi),
                "safe_closed_range": safe_closed,
            }
            mid_state = phase_state(speed, mid, cost)
            if mid_state["state"] == "blocking":
                violations.append(
                    {
                        "kind": "positive_interval",
                        "interval_semantics": "open cell; endpoint membership is recorded separately",
                        "tested_speed": speed,
                        "interval": (cell_lo, cell_hi),
                        "witness": mid,
                        "witness_phase": mid_state["phase"],
                        "base_laps": component["laps"],
                    }
                )
        cells.append({"interval": (cell_lo, cell_hi), "phase_ranges": ranges})

    endpoint_records = [
        endpoint_record(lo, base_pair + complement, cost),
        endpoint_record(hi, base_pair + complement, cost),
    ]
    for which, record, included in (
        ("left", endpoint_records[0], component["left_included"]),
        ("right", endpoint_records[1], component["right_included"]),
    ):
        if included:
            for speed in complement:
                if record["states"][speed]["state"] == "blocking":
                    # Usually adjacent to a positive cell; retained anyway so
                    # endpoint membership is never inferred from duration.
                    violations.append(
                        {
                            "kind": "included_endpoint",
                            "side": which,
                            "tested_speed": speed,
                            "time": record["time"],
                            "base_laps": component["laps"],
                        }
                    )
    return {
        **component,
        "phase_boundaries": per_speed_boundaries,
        "cells": cells,
        "endpoints": endpoint_records,
        "violations": violations,
    }


def moment_index(speeds: list[int], subset: tuple[int, ...]) -> int:
    return sum(1 << speeds.index(speed) for speed in subset)


def five_edge_arithmetic(physical: dict, base_pair: tuple[int, int], complement: tuple[int, int], holds: bool) -> dict:
    speeds = list(physical["speeds"])
    moments = list(map(F, physical["moments"]))
    total = moments[0]
    singles = [moments[1 << i] for i in range(4)]
    pair_masks = [sum(1 << i for i in pair) for pair in combinations(range(4), 2)]
    pairs = [moments[mask] for mask in pair_masks]
    c0 = total - sum(singles, F(0)) + sum(pairs, F(0))
    omitted_mask = moment_index(speeds, complement)
    omitted_overlap = moments[omitted_mask]
    counterfactual = c0 - omitted_overlap
    actual_u = F(physical["U"])
    assert c0 == F(physical["C"])
    if holds:
        assert counterfactual <= actual_u
    return {
        "formula": "U >= C_0 - O_cd - T_abc - T_abd",
        "status": "certified" if holds else "not_applicable_containment_failed",
        "C_0": c0,
        "omitted_pair": complement,
        "O_cd": omitted_overlap,
        "implied_triple_upper_bounds": [
            {"speeds": base_pair + (complement[0],), "upper": F(0)},
            {"speeds": base_pair + (complement[1],), "upper": F(0)},
        ] if holds else [],
        "lower_bound": counterfactual if holds else None,
        "counterfactual_bound_if_containment_held": counterfactual,
        "actual_uncovered_duration_from_archive": actual_u,
        "positive": bool(holds and counterfactual > 0),
        "operation_ledger": {
            "archived_total_single_pair_fraction_reads": 11,
            "rational_additions_or_subtractions_for_C0_and_bound": 11,
            "zero_triple_bounds_inserted": 2 if holds else 0,
            "positivity_comparisons": 1 if holds else 0,
            "runtime_claim": False,
        },
    }


def separate_triple_reconstruction(
    base_pair: tuple[int, int], third: int, window: tuple[F, F]
) -> dict:
    """Cost comparator that rebuilds one complete triple from scratch."""
    cost = Counter()
    blocks = [blocking_pieces(speed, window, cost) for speed in base_pair + (third,)]
    cost["individual_blocking_pieces_enumerated"] = cost.pop("blocking_pieces_enumerated")
    pair = intersect_piece_lists(blocks[0], blocks[1], cost, output_key="pair_overlap_components")
    # Adapt the third-runner records to the generic pair intersection shape.
    pair_third = []
    i = j = 0
    while i < len(pair) and j < len(blocks[2]):
        cost["triple_component_intersection_steps"] += 1
        a, b = pair[i]["interval"]
        c, d = blocks[2][j]["interval"]
        lo = charged_max(a, c, cost, "intersection_clip")
        hi = charged_min(b, d, cost, "intersection_clip")
        if cmp(cost, "intersection_nonempty", lo, "<", hi):
            pair_third.append(
                {
                    "interval": (lo, hi),
                    "laps": pair[i]["laps"] + (blocks[2][j]["lap"],),
                }
            )
        if cmp(cost, "intersection_advance", b, "<", d):
            i += 1
        elif cmp(cost, "intersection_advance", d, "<", b):
            j += 1
        else:
            i += 1
            j += 1
    cost["triple_overlap_components"] = len(pair_third)
    cost["triple_queries"] = 1
    cost["triple_duration_additions"] = len(pair_third)
    duration = sum((p["interval"][1] - p["interval"][0] for p in pair_third), F(0))
    return {"third_speed": third, "pieces": pair_third, "duration": duration, "cost": finalize_cost(cost)}


def finalize_cost(cost: Counter) -> dict:
    categories = sorted(k for k in cost if k.startswith("comparison_"))
    assert cost["exact_rational_comparisons"] == sum(cost[k] for k in categories)
    return dict(sorted(cost.items()))


def analyze_attempt(
    name: str,
    physical: dict,
    window: tuple[F, F],
    base_pair: tuple[int, int],
    complement: tuple[int, int],
    *,
    validate_archived_blocks: bool = True,
) -> dict:
    cost = Counter()
    base_blocks = [blocking_pieces(speed, window, cost) for speed in base_pair]
    cost["base_runner_blocking_pieces"] = cost.pop("blocking_pieces_enumerated")
    pair_components = intersect_piece_lists(
        base_blocks[0], base_blocks[1], cost, output_key="pair_overlap_components"
    )
    analyzed = [analyze_component(p, base_pair, complement, cost) for p in pair_components]
    all_violations = [v for component in analyzed for v in component["violations"]]
    positive_violations = [v for v in all_violations if v["kind"] == "positive_interval"]
    holds = not all_violations
    cost["containment_conclusions"] = 1

    # Crosscheck the generated base schedules against the archived physical
    # schedule while ignoring the older archive's measure-only endpoint flags.
    if validate_archived_blocks:
        archived_blocks = physical["blocks"]
        speed_to_index = {speed: i for i, speed in enumerate(physical["speeds"])}
        for speed, pieces in zip(base_pair, base_blocks):
            assert [list(p["interval"]) for p in pieces] == [
                list(map(F, interval)) for interval in archived_blocks[speed_to_index[speed]]
            ]

    separate = [separate_triple_reconstruction(base_pair, third, window) for third in complement]
    if holds:
        assert all(item["duration"] == 0 for item in separate)
    else:
        assert any(item["duration"] > 0 for item in separate)

    arithmetic = five_edge_arithmetic(physical, base_pair, complement, holds)
    full_schedule_pieces = sum(len(pieces) for pieces in physical["blocks"])
    output = {
        "name": name,
        "window": window,
        "base_pair": base_pair,
        "complement": complement,
        "base_blocking_pieces": {speed: pieces for speed, pieces in zip(base_pair, base_blocks)},
        "pair_overlap_components": analyzed,
        "containment_holds": holds,
        "positive_violation_count": len(positive_violations),
        "first_positive_violation": positive_violations[0] if positive_violations else None,
        "all_violations": all_violations,
        "five_edge_arithmetic": arithmetic,
        "information_contract": {
            "pair_selection": "supplied and frozen before calculation",
            "cached_base_pair_occurrence_tables": 1,
            "complement_safety_predicates": 2,
            "logical_compression_claim": "One shared base-pair occurrence table supports two distinct complement-safety predicates; this is not a one-bit certificate and does not select the pair.",
            "full_schedule_blocking_pieces_from_archive": full_schedule_pieces,
            "selected_base_blocking_pieces_enumerated": cost["base_runner_blocking_pieces"],
            "complement_blocking_piece_lists_enumerated_by_shared_certificate": 0,
            "runtime_claim": False,
        },
        "cost": finalize_cost(cost),
        "comparison_with_two_separate_triples": {
            "description": "Each comparator rebuilds both base schedules and one complementary schedule, then performs two interval joins.",
            "interpretation_limit": "Descriptive implementation ledger only: the difference mixes common-subexpression reuse with phase-range testing versus complete complement-schedule construction, so it is not an intrinsic factor-of-two or runtime claim.",
            "reconstructions": separate,
            "combined_cost": combine_costs([item["cost"] for item in separate]),
        },
    }
    return output


def combine_costs(costs: list[dict]) -> dict:
    total = Counter()
    for cost in costs:
        total.update(cost)
    return dict(sorted(total.items()))


def reflection_of_attempt(target: dict, physical: dict) -> dict:
    lo, hi = map(F, target["frozen_case"]["window"])
    reflected_window = (1 - hi, 1 - lo)
    reflected = analyze_attempt(
        "collective_target_reflection",
        physical,
        reflected_window,
        tuple(target["frozen_case"]["base_pair"]),
        tuple(target["frozen_case"]["complement"]),
        validate_archived_blocks=False,
    )
    original_intervals = [tuple(map(F, c["interval"])) for c in target["analysis"]["pair_overlap_components"]]
    reflected_intervals = [tuple(map(F, c["interval"])) for c in reflected["pair_overlap_components"]]
    assert [(1 - b, 1 - a) for a, b in reversed(original_intervals)] == reflected_intervals
    reflected["selection_reused"] = True
    reflected["independent_example"] = False
    reflected["exact_reverse_of_target_components"] = True
    return reflected


def sparse_comparison(source: dict) -> dict:
    records = {row["replacement"]: row for row in source["finite_results"]}
    selected = {}
    for speed in (13, 16):
        row = records[speed]
        selected[speed] = {
            "triple_6_11_w_possible": row["triple_6_11_w_possible"],
            "triple_7_11_w_possible": row["triple_7_11_w_possible"],
            "clear_lower_bound": F(row["clear_lower_bound"]),
            "actual_clear_duration": F(row["actual_clear_duration"]),
        }
    return {
        "status": "prior archived comparator; not rerun or presented as new",
        "test_formula": "floor(w*a-1/8)+1 < w*b+1/8",
        "two_test_operation_ledger": {
            "integer_rational_multiplications": 4,
            "rational_additions_or_subtractions": 6,
            "floors": 2,
            "strict_rational_comparisons": 2,
        },
        "applicable_archived_controls": selected,
        "nonapplicable_cases": ["collective_target", "doubling_112"],
    }


def tight_isolated_contact() -> dict:
    """Keep the equality-only control separate from duration containment."""
    time = F(3, 8)
    speeds = (1, 4, 5, 6, 7, 11, 13)
    states = {speed: phase_state(speed, time) for speed in speeds}
    valid = all(record["state"] != "blocking" for record in states.values())
    left_blockers = [speed for speed, record in states.items() if record["phase"] == DELTA]
    right_blockers = [speed for speed, record in states.items() if record["phase"] == 1 - DELTA]
    assert valid and left_blockers == [11] and right_blockers == [5, 13]
    return {
        "time": time,
        "states": states,
        "valid": valid,
        "blocks_immediately_left": left_blockers,
        "blocks_immediately_right": right_blockers,
        "isolated": True,
        "positive_duration": False,
    }


def load_sources(protocol: dict) -> dict:
    loaded = {}
    for key, relative in (
        ("joint_results", protocol["source_contract"]["joint_results"]),
        ("cover_results", protocol["source_contract"]["cover_results"]),
        ("sparse_results", protocol["source_contract"]["sparse_results"]),
    ):
        path = ROOT / relative
        expected = protocol["source_contract"][key + "_sha256"]
        assert sha256(path) == expected
        loaded[key] = json.loads(path.read_text())
    return loaded


def build(old=None) -> dict:
    assert sha256(PROTOCOL) == FROZEN_PROTOCOL_SHA256
    protocol = json.loads(PROTOCOL.read_text())
    sources = load_sources(protocol)
    joint_cases = sources["joint_results"]["cases"]
    physical_by_name = {
        "collective_target": joint_cases["target"]["physical"],
        "strict_16": joint_cases["strict_16"]["physical"],
        "doubling_112": joint_cases["doubling_112"]["physical"],
        "tight_13": joint_cases["tight_13"]["physical"],
    }

    cases = {}
    frozen_by_name = {case["name"]: case for case in protocol["frozen_cases"]}
    for name in ("collective_target", "strict_16", "tight_13"):
        frozen = frozen_by_name[name]
        physical = physical_by_name[name]
        assert frozen["residual_speeds"] == physical["speeds"]
        assert list(map(F, frozen["window"])) == list(map(F, physical["window"]))
        analysis = analyze_attempt(
            name,
            physical,
            tuple(map(F, frozen["window"])),
            tuple(frozen["base_pair"]),
            tuple(frozen["complement"]),
        )
        cases[name] = {"frozen_case": frozen, "analysis": analysis}

    frozen = frozen_by_name["doubling_112"]
    physical = physical_by_name["doubling_112"]
    attempts = []
    for base_pair in combinations(frozen["residual_speeds"], 2):
        complement = tuple(speed for speed in frozen["residual_speeds"] if speed not in base_pair)
        attempts.append(
            analyze_attempt(
                "doubling_112:" + ",".join(map(str, base_pair)),
                physical,
                tuple(map(F, frozen["window"])),
                tuple(base_pair),
                complement,
            )
        )
    assert len(attempts) == 6
    assert all(not attempt["containment_holds"] for attempt in attempts)
    assert all(attempt["first_positive_violation"] is not None for attempt in attempts)
    cases["doubling_112"] = {
        "frozen_case": frozen,
        "diagnostic_only": True,
        "post_result_selection": False,
        "attempts": attempts,
    }

    reflection = reflection_of_attempt(cases["collective_target"], physical_by_name["collective_target"])
    assert cases["collective_target"]["analysis"]["containment_holds"]
    assert cases["strict_16"]["analysis"]["containment_holds"]
    assert cases["tight_13"]["analysis"]["containment_holds"]
    assert cases["collective_target"]["analysis"]["five_edge_arithmetic"]["lower_bound"] == F(49, 524400)
    assert cases["strict_16"]["analysis"]["five_edge_arithmetic"]["lower_bound"] == F(1, 896)
    assert cases["tight_13"]["analysis"]["five_edge_arithmetic"]["lower_bound"] == -F(1, 182)

    selected_costs = [cases[name]["analysis"]["cost"] for name in ("collective_target", "strict_16", "tight_13")]
    diagnostic_costs = [attempt["cost"] for attempt in attempts]
    out = serialize(
        {
            "baseline": protocol["baseline"],
            "protocol_sha256": FROZEN_PROTOCOL_SHA256,
            "primary_sha256": sha256(Path(__file__)),
            "source_contract": protocol["source_contract"],
            "arithmetic": "fractions.Fraction only",
            "endpoint_semantics": "strict blocking distance<1/8; equality belongs to closed safe set",
            "cases": cases,
            "target_reflection": reflection,
            "tight_13_isolated_contact": tight_isolated_contact(),
            "cost_summary": {
                "selected_cases_combined": combine_costs(selected_costs),
                "six_doubling_diagnostics_combined": combine_costs(diagnostic_costs),
                "ledger_definition": "Semantic comparisons executed by interval clipping/joining, phase-boundary tests, phase-range bounds, and endpoint classification; sorting, assertions, and archive bookkeeping excluded.",
            },
            "old_sparse_arithmetic_comparison": sparse_comparison(sources["sparse_results"]),
            "findings": {
                "selected_containments_certified": ["collective_target", "strict_16", "tight_13"],
                "selected_positive_five_edge_bounds": ["collective_target", "strict_16"],
                "selected_nonpositive_control": "tight_13",
                "doubling_containments_failed": 6,
                "doubling_positive_violation_certificates": 6,
                "general_selection_claim": False,
                "novelty_claim": False,
                "independent_mathematical_validation": False,
            },
            "scope": protocol["scope"],
        }
    )
    if old is not None:
        assert out == old
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    old = None if args.write else json.loads(OUT.read_text())
    data = build(old)
    if args.write:
        OUT.write_text(json.dumps(data, indent=2) + "\n")
    for name in ("collective_target", "strict_16", "tight_13"):
        analysis = data["cases"][name]["analysis"]
        print(
            name,
            "containment=", analysis["containment_holds"],
            "components=", len(analysis["pair_overlap_components"]),
            "bound=", analysis["five_edge_arithmetic"]["lower_bound"],
        )
    failures = data["cases"]["doubling_112"]["attempts"]
    print("doubling_112 failed containments=", sum(not item["containment_holds"] for item in failures))
    print("PASS: exact shared-pair containment archive reproduced read-only" if args.check else "WROTE: exact shared-pair containment archive")


if __name__ == "__main__":
    main()
