"""Exact primary calculation for the frozen one-containment selector study.

The implementation has an intentional information barrier.  ``prequery``
constructs the six moment slacks and, only for the second frozen rule, base-pair
component counts.  It receives no complementary-runner geometry.  Only after
both selections are fixed does ``containment_query`` construct schedules for
the selected pair's complementary runners.  A failed query is final: there is
no fallback candidate or post-result reranking.

``--write`` deterministically creates ``results.json``.  ``--check`` is
read-only and reconstructs the complete archive using ``fractions.Fraction``.
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
FROZEN_PROTOCOL_SHA256 = "42c3fe75734e7fc137b3ffc9de805172661acb988b3d39162517adb50028a607"
DELTA = F(1, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value) -> F:
    return F(str(value))


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Counter):
        value = dict(value)
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def floor(value: F) -> int:
    return value.numerator // value.denominator


def phase(speed: int, time: F) -> F:
    return (speed * time) % 1


def distance(speed: int, time: F) -> F:
    p = phase(speed, time)
    return min(p, 1 - p)


def is_blocking(speed: int, time: F, cost: Counter | None = None) -> bool:
    if cost is not None:
        cost["phase_fold_comparisons"] += 1
        cost["blocking_state_comparisons"] += 1
    return distance(speed, time) < DELTA


def blocking_pieces(speed: int, window: tuple[F, F], cost: Counter) -> list[dict]:
    """Return strict blocking pieces with exact endpoint membership."""
    lo_window, hi_window = window
    pieces = []
    for lap in range(floor(speed * lo_window) - 1, floor(speed * hi_window) + 2):
        cost["lap_candidates"] += 1
        raw_lo = (F(lap) - DELTA) / speed
        raw_hi = (F(lap) + DELTA) / speed
        cost["clip_comparisons"] += 2
        lo = max(lo_window, raw_lo)
        hi = min(hi_window, raw_hi)
        cost["nonempty_comparisons"] += 1
        if lo < hi:
            pieces.append(
                {
                    "interval": (lo, hi),
                    "lap": lap,
                    "left_included": is_blocking(speed, lo, cost),
                    "right_included": is_blocking(speed, hi, cost),
                }
            )
    cost["blocking_pieces"] += len(pieces)
    return pieces


def intersect_pieces(first: list[dict], second: list[dict], cost: Counter) -> list[dict]:
    """Intersect two ordered strict-piece lists, retaining endpoint semantics."""
    i = j = 0
    output = []
    while i < len(first) and j < len(second):
        cost["join_steps"] += 1
        left, right = first[i], second[j]
        a, b = left["interval"]
        c, d = right["interval"]
        cost["join_clip_comparisons"] += 2
        lo, hi = max(a, c), min(b, d)
        cost["join_nonempty_comparisons"] += 1
        if lo < hi:
            output.append(
                {
                    "interval": (lo, hi),
                    "laps": (left["lap"], right["lap"]),
                    "left_included": (
                        (left["left_included"] if lo == a else True)
                        and (right["left_included"] if lo == c else True)
                    ),
                    "right_included": (
                        (left["right_included"] if hi == b else True)
                        and (right["right_included"] if hi == d else True)
                    ),
                }
            )
        cost["join_advance_comparisons"] += 1
        if b < d:
            i += 1
        else:
            cost["join_advance_comparisons"] += 1
            if d < b:
                j += 1
            else:
                i += 1
                j += 1
    cost["positive_components"] += len(output)
    return output


def base_components(
    pair: tuple[int, int], window: tuple[F, F], cost: Counter
) -> list[dict]:
    first = blocking_pieces(pair[0], window, cost)
    second = blocking_pieces(pair[1], window, cost)
    return intersect_pieces(first, second, cost)


def mask_for_pair(speeds: tuple[int, ...], pair: tuple[int, int]) -> int:
    return sum(1 << speeds.index(speed) for speed in pair)


def source_pair_interval_crosscheck(physical: dict, pair: tuple[int, int], components: list[dict]) -> None:
    speeds = tuple(physical["speeds"])
    mask = mask_for_pair(speeds, pair)
    archived = [tuple(map(q, piece)) for piece in physical["intersection_pieces"][mask]]
    assert archived == [tuple(piece["interval"]) for piece in components]


def make_moment_view(physical: dict) -> dict:
    """Project the source to the moment-only information contract."""
    speeds = tuple(physical["speeds"])
    moments = tuple(map(q, physical["moments"]))
    total = moments[0]
    singles = tuple(moments[1 << index] for index in range(4))
    pair_rows = []
    all_pairs = tuple(combinations(speeds, 2))
    pair_values = {pair: moments[mask_for_pair(speeds, pair)] for pair in all_pairs}
    c0 = total - sum(singles, F(0)) + sum(pair_values.values(), F(0))
    assert c0 == q(physical["C"])
    for base_pair in all_pairs:
        complement = tuple(speed for speed in speeds if speed not in base_pair)
        omitted = pair_values[complement]
        pair_rows.append(
            {
                "base_pair": base_pair,
                "complement": complement,
                "omitted_pair_overlap": omitted,
                "potential_slack": c0 - omitted,
            }
        )
    return {
        "speeds": speeds,
        "window": tuple(map(q, physical["window"])),
        "total": total,
        "single_durations": dict(zip(speeds, singles)),
        "pair_durations": {pair: value for pair, value in pair_values.items()},
        "C_0": c0,
        "pair_rows": pair_rows,
        "actual_uncovered_duration": q(physical["U"]),
    }


def choose_largest_slack(eligible: list[dict], cost: Counter) -> tuple[int, int] | None:
    """Frozen rule 1; consumes moments only."""
    if not eligible:
        return None
    chosen = eligible[0]
    for row in eligible[1:]:
        cost["slack_order_comparisons"] += 1
        if row["potential_slack"] > chosen["potential_slack"]:
            chosen = row
        else:
            cost["slack_equality_comparisons"] += 1
            if row["potential_slack"] == chosen["potential_slack"]:
                cost["physical_lexicographic_tie_breaks"] += 1
                if row["base_pair"] < chosen["base_pair"]:
                    chosen = row
    return chosen["base_pair"]


def choose_fewest_components(eligible: list[dict], cost: Counter) -> tuple[int, int] | None:
    """Frozen rule 2; slack is deliberately not a secondary key."""
    if not eligible:
        return None
    chosen = eligible[0]
    for row in eligible[1:]:
        cost["component_count_order_comparisons"] += 1
        if row["positive_component_count"] < chosen["positive_component_count"]:
            chosen = row
        else:
            cost["component_count_equality_comparisons"] += 1
            if row["positive_component_count"] == chosen["positive_component_count"]:
                cost["physical_lexicographic_tie_breaks"] += 1
                if row["base_pair"] < chosen["base_pair"]:
                    chosen = row
    return chosen["base_pair"]


def prequery(physical: dict) -> dict:
    """Select both pairs without constructing any complementary-runner state."""
    moment = make_moment_view(physical)
    eligibility_cost = Counter()
    eligible = []
    for row in moment["pair_rows"]:
        eligibility_cost["strict_positivity_comparisons"] += 1
        row["eligible"] = row["potential_slack"] > 0
        if row["eligible"]:
            eligible.append(row)

    slack_cost = Counter()
    largest = choose_largest_slack(eligible, slack_cost)

    # This is the larger prequery contract.  Only the two base-runner schedules
    # are reconstructed for each eligible pair.  No complement speed is passed
    # to base_components, and the selector receives only the resulting count.
    component_cost = Counter()
    component_cache = {}
    per_pair_cost = {}
    for row in eligible:
        pair_cost = Counter()
        pair = row["base_pair"]
        components = base_components(pair, moment["window"], pair_cost)
        source_pair_interval_crosscheck(physical, pair, components)
        component_cache[pair] = components
        row["positive_component_count"] = len(components)
        per_pair_cost[pair] = dict(sorted(pair_cost.items()))
        component_cost.update(pair_cost)
    count_selection_cost = Counter()
    fewest = choose_fewest_components(eligible, count_selection_cost)

    public_rows = []
    for row in moment["pair_rows"]:
        public_rows.append(
            {
                **row,
                "positive_component_count": row.get("positive_component_count"),
                "component_enumeration_cost": per_pair_cost.get(row["base_pair"]),
            }
        )
    return {
        "moment_view": {key: value for key, value in moment.items() if key != "pair_rows"},
        "all_six_pairs": public_rows,
        "eligible_base_pairs": [row["base_pair"] for row in eligible],
        "selections": {
            "largest_potential_slack": largest,
            "fewest_positive_occurrence_components": fewest,
        },
        "cost": {
            "moment_contract": {
                "archived_fraction_reads": 11,
                "additions_or_subtractions_for_C_0_and_six_slacks": 16,
                **dict(sorted(eligibility_cost.items())),
                **dict(sorted(slack_cost.items())),
            },
            "component_count_extension": {
                **dict(sorted(component_cost.items())),
                **dict(sorted(count_selection_cost.items())),
                "eligible_pair_intersections_enumerated": len(eligible),
                "complement_runner_states_read": 0,
            },
            "runtime_claim": False,
        },
        # Private bridge.  It is deliberately omitted from serialized output.
        "_component_cache": component_cache,
    }


def intersection_violation(
    base: dict, blocker: dict, tested_speed: int, cost: Counter
) -> dict | None:
    a, b = base["interval"]
    c, d = blocker["interval"]
    cost["violation_clip_comparisons"] += 2
    lo, hi = max(a, c), min(b, d)
    left_included = (
        (base["left_included"] if lo == a else True)
        and (blocker["left_included"] if lo == c else True)
    )
    right_included = (
        (base["right_included"] if hi == b else True)
        and (blocker["right_included"] if hi == d else True)
    )
    cost["violation_nonempty_comparisons"] += 1
    if lo < hi:
        witness = (lo + hi) / 2
        assert is_blocking(tested_speed, witness)
        return {
            "kind": "positive_interval",
            "interval": (lo, hi),
            "left_included": left_included,
            "right_included": right_included,
            "witness": witness,
            "witness_phase": phase(tested_speed, witness),
            "tested_complement_speed": tested_speed,
            "base_laps": base["laps"],
            "complement_lap": blocker["lap"],
        }
    if lo == hi and left_included and right_included:
        assert is_blocking(tested_speed, lo)
        return {
            "kind": "included_endpoint",
            "time": lo,
            "tested_complement_speed": tested_speed,
            "base_laps": base["laps"],
            "complement_lap": blocker["lap"],
        }
    return None


def violation_key(item: dict) -> tuple:
    time = item["interval"][0] if item["kind"] == "positive_interval" else item["time"]
    return (time, item["tested_complement_speed"], item["kind"])


def containment_query(
    physical: dict,
    pair: tuple[int, int],
    base: list[dict],
) -> dict:
    """The sole post-selection operation that reads complement geometry."""
    speeds = tuple(physical["speeds"])
    window = tuple(map(q, physical["window"]))
    complement = tuple(speed for speed in speeds if speed not in pair)
    cost = Counter()
    complement_blocks = {
        speed: blocking_pieces(speed, window, cost) for speed in complement
    }
    violations = []
    for component in base:
        for speed in complement:
            for blocker in complement_blocks[speed]:
                cost["base_complement_piece_tests"] += 1
                found = intersection_violation(component, blocker, speed, cost)
                if found is not None:
                    violations.append(found)
    violations.sort(key=violation_key)
    holds = not violations
    cost["containment_conclusions"] = 1
    return {
        "base_pair": pair,
        "complement": complement,
        "base_positive_components": base,
        "base_positive_component_count": len(base),
        "containment_holds": holds,
        "violation_count": len(violations),
        "first_exact_violation": violations[0] if violations else None,
        "all_exact_violations": violations,
        "query_cost": dict(sorted(cost.items())),
        "endpoint_semantics": "base and complement blockers are strict; equality at distance 1/8 is safe",
    }


def row_for_pair(rows: list[dict], pair: tuple[int, int]) -> dict:
    return next(row for row in rows if row["base_pair"] == pair)


def tight_endpoint(endpoint: dict) -> dict:
    assert endpoint["time"] == "3/8" and endpoint["valid"] and endpoint["isolated"]
    return {
        "time": q(endpoint["time"]),
        "distances": {int(speed): q(value) for speed, value in endpoint["distances"].items()},
        "valid": endpoint["valid"],
        "isolated": endpoint["isolated"],
        "positive_duration": False,
        "left_neighborhood_blockers": endpoint["left_neighborhood_blockers"],
        "right_neighborhood_blockers": endpoint["right_neighborhood_blockers"],
    }


def analyze_case(case_spec: dict, physical: dict, cover_case: dict) -> dict:
    prepared = prequery(physical)
    component_cache = prepared.pop("_component_cache")
    selections = prepared["selections"]

    # The information barrier ends here: both rule outputs are immutable before
    # any selected pair is given to containment_query.
    selected_pairs = []
    for rule in ("largest_potential_slack", "fewest_positive_occurrence_components"):
        pair = selections[rule]
        if pair is not None and pair not in selected_pairs:
            selected_pairs.append(pair)
    query_by_pair = {
        pair: containment_query(physical, pair, component_cache[pair])
        for pair in selected_pairs
    }

    rules = {}
    for rule in ("largest_potential_slack", "fewest_positive_occurrence_components"):
        pair = selections[rule]
        if pair is None:
            rules[rule] = {
                "selected_base_pair": None,
                "query_issued": False,
                "outcome": "no_eligible_pair_no_query",
                "certified_lower_bound": None,
                "retuned": False,
            }
            continue
        row = row_for_pair(prepared["all_six_pairs"], pair)
        query = query_by_pair[pair]
        rules[rule] = {
            "selected_base_pair": pair,
            "selected_complement": row["complement"],
            "selected_potential_slack": row["potential_slack"],
            "selected_positive_component_count": row["positive_component_count"],
            "query_issued": True,
            "query_physical_calculation_reused_by_other_rule": list(selections.values()).count(pair) == 2,
            "containment_holds": query["containment_holds"],
            "first_exact_violation": query["first_exact_violation"],
            "outcome": "certified" if query["containment_holds"] else "failed_no_retune",
            "certified_lower_bound": row["potential_slack"] if query["containment_holds"] else None,
            "counterfactual_bound_if_containment_held": row["potential_slack"],
            "retuned": False,
            "second_query_issued": False,
        }

    name = case_spec["id"]
    is_doubling = name == "doubling_112"
    pair_only_exit = None
    if is_doubling:
        assert cover_case["outcome"] == "pair_only_positive"
        pair_only_exit = {
            "precedes_selector": True,
            "archived_positive_optimum": q(cover_case["baseline"]["value"]),
            "selector_results_are_diagnostic_only": True,
        }
        assert pair_only_exit["archived_positive_optimum"] > 0

    endpoint = tight_endpoint(cover_case["endpoint"]) if name == "tight_13" else None
    if name == "tight_13":
        assert not prepared["eligible_base_pairs"]
        assert all(not result["query_issued"] for result in rules.values())

    # Verify every generated selected schedule against the pinned archive after
    # selection.  This validation does not feed either ranking.
    for pair, query in query_by_pair.items():
        source_pair_interval_crosscheck(physical, pair, query["base_positive_components"])

    return {
        "expected_role": case_spec["expected_role"],
        "window": tuple(map(q, physical["window"])),
        "speeds": tuple(physical["speeds"]),
        "C_0": prepared["moment_view"]["C_0"],
        "actual_uncovered_duration_from_archive": prepared["moment_view"]["actual_uncovered_duration"],
        "all_six_potential_slacks": prepared["all_six_pairs"],
        "eligible_base_pairs": prepared["eligible_base_pairs"],
        "prequery_information_and_cost": prepared["cost"],
        "frozen_rule_results": rules,
        "unique_physical_containment_queries": [query_by_pair[pair] for pair in selected_pairs],
        "logical_query_count": sum(result["query_issued"] for result in rules.values()),
        "unique_physical_query_count": len(selected_pairs),
        "pair_only_exit": pair_only_exit,
        "isolated_equality_endpoint": endpoint,
        "diagnostic_only": is_doubling,
    }


def load_sources(protocol: dict) -> tuple[dict, dict]:
    joint_path = ROOT / protocol["source_contract"]["physical_geometry_and_moments"]
    cover_path = ROOT / protocol["source_contract"]["pair_only_control_and_endpoint_roles"]
    assert sha256(joint_path) == protocol["source_contract"]["physical_geometry_and_moments_sha256"]
    assert sha256(cover_path) == protocol["source_contract"]["pair_only_control_and_endpoint_roles_sha256"]
    return json.loads(joint_path.read_text()), json.loads(cover_path.read_text())


def build(old=None) -> dict:
    assert sha256(PROTOCOL) == FROZEN_PROTOCOL_SHA256
    protocol = json.loads(PROTOCOL.read_text())
    joint, cover = load_sources(protocol)
    cover_by_name = {case["name"]: case for case in cover["cases"]}
    source_name = {
        "collective_target": "target",
        "strict_16": "strict_16",
        "doubling_112": "doubling_112",
        "tight_13": "tight_13",
    }
    cases = {}
    for case_spec in protocol["cases"]:
        name = case_spec["id"]
        source_case = joint["cases"][source_name[name]]["physical"]
        control = cover_by_name.get(source_name[name], {})
        cases[name] = analyze_case(case_spec, source_case, control)

    assert cases["collective_target"]["frozen_rule_results"]["largest_potential_slack"]["selected_base_pair"] == (61, 100)
    assert cases["collective_target"]["frozen_rule_results"]["largest_potential_slack"]["outcome"] == "failed_no_retune"
    assert cases["collective_target"]["frozen_rule_results"]["fewest_positive_occurrence_components"]["selected_base_pair"] == (15, 38)
    assert cases["collective_target"]["frozen_rule_results"]["fewest_positive_occurrence_components"]["certified_lower_bound"] == F(49, 524400)
    assert all(
        result["certified_lower_bound"] == F(1, 896)
        for result in cases["strict_16"]["frozen_rule_results"].values()
    )
    assert cases["doubling_112"]["pair_only_exit"]["archived_positive_optimum"] == F(761, 32256)
    assert all(
        result["outcome"] == "failed_no_retune"
        for result in cases["doubling_112"]["frozen_rule_results"].values()
    )

    all_case_values = list(cases.values())
    out = serialize(
        {
            "baseline": protocol["baseline"],
            "protocol_sha256": FROZEN_PROTOCOL_SHA256,
            "primary_sha256": sha256(Path(__file__)),
            "source_contract": protocol["source_contract"],
            "arithmetic": "fractions.Fraction only; no floating-point decisions",
            "information_barrier": "Both rule selections are frozen before containment_query receives any complementary-runner geometry.",
            "endpoint_semantics": "Strict blockers use distance<1/8; equality is in the closed safe set.",
            "cases": cases,
            "counts": {
                "windows": len(cases),
                "base_pairs": sum(len(case["all_six_potential_slacks"]) for case in all_case_values),
                "eligible_base_pairs": sum(len(case["eligible_base_pairs"]) for case in all_case_values),
                "positive_components_enumerated_for_component_rule": sum(
                    sum(
                        row["positive_component_count"] or 0
                        for row in case["all_six_potential_slacks"]
                        if row["eligible"]
                    )
                    for case in all_case_values
                ),
                "logical_rule_queries": sum(case["logical_query_count"] for case in all_case_values),
                "unique_physical_containment_queries": sum(case["unique_physical_query_count"] for case in all_case_values),
                "failed_logical_queries": sum(
                    result["query_issued"] and not result["containment_holds"]
                    for case in all_case_values
                    for result in case["frozen_rule_results"].values()
                ),
                "successful_logical_queries": sum(
                    result["query_issued"] and result["containment_holds"]
                    for case in all_case_values
                    for result in case["frozen_rule_results"].values()
                ),
                "second_queries_after_failure": 0,
            },
            "findings": {
                "target_largest_slack_rule": "fails on selected pair (61,100); no retuning",
                "target_fewest_components_rule": "selects (15,38) and certifies 49/524400",
                "strict_16": "both rules select (6,11) and certify 1/896 using one reused physical query",
                "doubling_112": "pair-only optimum 761/32256 exits first; both selector diagnostics fail",
                "tight_13": "no positive-slack pair, no query, isolated valid equality t=3/8 retained",
                "general_selector_claim": False,
                "whole_configuration_claim": False,
                "novelty_claim": False,
                "independent_mathematical_validation": False,
            },
            "scope": protocol["scope"],
            "interpretation_limits": protocol["interpretation_limits"],
        }
    )
    if old is not None:
        assert out == old
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    old = None if args.write else json.loads(OUT.read_text())
    data = build(old)
    if args.write:
        OUT.write_text(json.dumps(data, indent=2) + "\n")
    for name, case in data["cases"].items():
        print(name, case["frozen_rule_results"])
    print(data["counts"])
    print("WROTE: exact selector archive" if args.write else "PASS: exact selector archive reproduced read-only")


if __name__ == "__main__":
    main()
