"""Primary exact calculation for the frozen selector-transfer audit.

The calculation has three deliberately separated phases.

1. Project each archived record to its id, four residual speeds, window,
   total/single/pair moments and supplied pair-only minimum.  Component scores
   are then obtained by the frozen open-strip floor sum; no lap loop or
   interval list occurs in this phase.
2. Freeze both one-query decisions.  Only then construct the selected physical
   intersections and test their complements.
3. After those outcomes are immutable, reconstruct every eligible containment
   as an oracle audit and finally attach archive classifications.

``--write`` deterministically writes ``results.json``; ``--check`` is read
only and reconstructs it with exact integer/Fraction arithmetic.
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
PROTOCOL_SHA256 = "ccfdb403abef15f9c2cd9e08ac086232f4842b450f48308ba5a5992f8c3f9c17"
DELTA = F(1, 8)
RULES = ("fewest_components", "largest_slack_comparator")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value) -> F:
    return F(str(value))


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Counter):
        value = dict(value)
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(item) for item in value]
    return value


def floor(value: F) -> int:
    return value.numerator // value.denominator


def ceil(value: F) -> int:
    return -floor(-value)


def ceil_div(numerator: int, denominator: int) -> int:
    assert denominator > 0
    return -((-numerator) // denominator)


def strict_integer_range(lower: F, upper: F) -> tuple[int, int]:
    return floor(lower) + 1, ceil(upper) - 1


def add_cost(target: Counter, source: dict | Counter) -> None:
    target.update({key: int(value) for key, value in source.items()})


# ---------------------------------------------------------------------------
# Frozen open-strip floor sum.  There is no per-lap loop in these functions.


def floor_sum_nonnegative(
    n: int, modulus: int, coefficient: int, offset: int, cost: Counter
) -> int:
    assert n >= 0 and modulus > 0 and coefficient >= 0 and offset >= 0
    answer = 0
    while True:
        cost["euclidean_rounds"] += 1
        if coefficient >= modulus:
            quotient, coefficient = divmod(coefficient, modulus)
            cost["quotient_divisions"] += 1
            cost["remainder_operations"] += 1
            answer += (n - 1) * n * quotient // 2
        if offset >= modulus:
            quotient, offset = divmod(offset, modulus)
            cost["quotient_divisions"] += 1
            cost["remainder_operations"] += 1
            answer += n * quotient
        y_max = coefficient * n + offset
        cost["floor_sum_terminal_comparisons"] += 1
        if y_max < modulus:
            return answer
        n, offset = divmod(y_max, modulus)
        cost["quotient_divisions"] += 1
        cost["remainder_operations"] += 1
        modulus, coefficient = coefficient, modulus


def floor_sum_range(
    first: int,
    stop: int,
    coefficient: int,
    offset: int,
    modulus: int,
    cost: Counter,
) -> int:
    if first >= stop:
        return 0
    count = stop - first
    shifted = coefficient * first + offset
    quotient, normalized = divmod(shifted, modulus)
    cost["floor_sum_range_calls"] += 1
    cost["signed_offset_normalizations"] += 1
    return count * quotient + floor_sum_nonnegative(
        count, modulus, coefficient, normalized, cost
    )


def half_plane_count(
    *, K: int, A: int, Q: int, m_min: int, m_max: int,
    n_min: int, n_max: int, cost: Counter
) -> int:
    cost["strip_half_plane_calls"] += 1
    m_count = max(0, m_max - m_min + 1)
    n_count = max(0, n_max - n_min + 1)
    if not m_count or not n_count:
        return 0
    B = -K + Q - 1
    cost["threshold_ceil_divisions"] += 2
    first_one = ceil_div(Q * (n_min + 1) - B, A)
    first_sat = ceil_div(Q * (n_min + n_count) - B, A)
    stop = m_max + 1
    first_one = min(stop, max(m_min, first_one))
    first_sat = min(stop, max(m_min, first_sat))
    assert first_one <= first_sat
    raw_middle = floor_sum_range(first_one, first_sat, A, B, Q, cost)
    middle_count = first_sat - first_one
    below = raw_middle - middle_count * n_min + (stop - first_sat) * n_count
    return m_count * n_count - below


def component_count_floor_sum(
    pair: tuple[int, int], window: tuple[F, F]
) -> tuple[int, dict, Counter]:
    a, b = pair
    assert 0 < a < b
    left, right = window
    m_min, m_max = strict_integer_range(a * left - DELTA, a * right + DELTA)
    n_min, n_max = strict_integer_range(b * left - DELTA, b * right + DELTA)
    A, Q, S = 8 * b, 8 * a, a + b
    cost = Counter()
    upper = half_plane_count(
        K=S - 1, A=A, Q=Q, m_min=m_min, m_max=m_max,
        n_min=n_min, n_max=n_max, cost=cost,
    )
    lower = half_plane_count(
        K=-S, A=A, Q=Q, m_min=m_min, m_max=m_max,
        n_min=n_min, n_max=n_max, cost=cost,
    )
    cost["strip_subtractions"] += 1
    count = upper - lower
    assert count >= 0
    return count, {
        "m_lap_rectangle": [m_min, m_max],
        "n_lap_rectangle": [n_min, n_max],
        "scaled_open_strip": [-S + 1, S - 1],
        "upper_half_plane_count": upper,
        "lower_half_plane_count_subtracted": lower,
        "component_count": count,
    }, cost


# ---------------------------------------------------------------------------
# Exact postselection geometry.  Lap loops occur only here, after selection.


def phase(speed: int, time: F) -> F:
    return (speed * time) % 1


def distance(speed: int, time: F) -> F:
    value = phase(speed, time)
    return min(value, 1 - value)


def is_blocking(speed: int, time: F, cost: Counter | None = None) -> bool:
    if cost is not None:
        cost["phase_fold_comparisons"] += 1
        cost["blocking_state_comparisons"] += 1
    return distance(speed, time) < DELTA


def blocking_pieces(speed: int, window: tuple[F, F], cost: Counter) -> list[dict]:
    left, right = window
    output = []
    for lap in range(floor(speed * left) - 1, floor(speed * right) + 2):
        cost["lap_candidates"] += 1
        raw_left = (F(lap) - DELTA) / speed
        raw_right = (F(lap) + DELTA) / speed
        cost["clip_comparisons"] += 2
        lo, hi = max(left, raw_left), min(right, raw_right)
        cost["nonempty_comparisons"] += 1
        if lo < hi:
            output.append({
                "interval": (lo, hi),
                "lap": lap,
                "left_included": is_blocking(speed, lo, cost),
                "right_included": is_blocking(speed, hi, cost),
            })
    cost["blocking_pieces"] += len(output)
    return output


def base_components(
    pair: tuple[int, int], window: tuple[F, F], cost: Counter
) -> list[dict]:
    first = blocking_pieces(pair[0], window, cost)
    second = blocking_pieces(pair[1], window, cost)
    i = j = 0
    output = []
    while i < len(first) and j < len(second):
        cost["join_steps"] += 1
        x, y = first[i], second[j]
        a, b = x["interval"]
        c, d = y["interval"]
        cost["join_clip_comparisons"] += 2
        lo, hi = max(a, c), min(b, d)
        cost["join_nonempty_comparisons"] += 1
        if lo < hi:
            output.append({
                "interval": (lo, hi),
                "laps": (x["lap"], y["lap"]),
                "left_included": (
                    (x["left_included"] if lo == a else True)
                    and (y["left_included"] if lo == c else True)
                ),
                "right_included": (
                    (x["right_included"] if hi == b else True)
                    and (y["right_included"] if hi == d else True)
                ),
            })
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


def threshold_event_ledger(speeds: tuple[int, ...], window: tuple[F, F]) -> dict:
    left, right = window
    events = {left, right}
    raw_thresholds = 0
    for speed in speeds:
        for lap in range(floor(speed * left) - 1, floor(speed * right) + 2):
            for sign in (-1, 1):
                point = (F(lap) + sign * DELTA) / speed
                if left <= point <= right:
                    raw_thresholds += 1
                    events.add(point)
    ordered = sorted(events)
    return {
        "raw_in_window_thresholds": raw_thresholds,
        "unique_threshold_events_including_window_endpoints": len(ordered),
        "open_cells": max(0, len(ordered) - 1),
    }


def intersect_violation(
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
    return time, item["tested_complement_speed"], item["kind"]


def containment_query(
    speeds: tuple[int, ...], window: tuple[F, F], pair: tuple[int, int]
) -> dict:
    complement = tuple(speed for speed in speeds if speed not in pair)
    cost = Counter()
    base = base_components(pair, window, cost)
    complement_blocks = {
        speed: blocking_pieces(speed, window, cost) for speed in complement
    }
    violations = []
    for component in base:
        for speed in complement:
            for blocker in complement_blocks[speed]:
                cost["base_complement_piece_tests"] += 1
                found = intersect_violation(component, blocker, speed, cost)
                if found is not None:
                    violations.append(found)
    violations.sort(key=violation_key)
    cost["containment_conclusions"] += 1
    return {
        "base_pair": pair,
        "complement": complement,
        "base_components": base,
        "base_positive_component_count": len(base),
        "containment_holds": not violations,
        "violation_count": len(violations),
        "first_exact_violation": violations[0] if violations else None,
        "all_exact_violations": violations,
        "event_ledger": threshold_event_ledger(speeds, window),
        "operation_cost": dict(sorted(cost.items())),
        "endpoint_semantics": "strict blocker distance<1/8; equality is safe",
    }


# ---------------------------------------------------------------------------
# Projection, frozen choices, case analysis and postselection comparisons.


def mask_for_pair(speeds: tuple[int, ...], pair: tuple[int, int]) -> int:
    return sum(1 << speeds.index(speed) for speed in pair)


def project_archived_cases(archive: dict) -> dict:
    """Irreversibly project the monolithic archive before calculation."""
    projected = {}
    for case in archive["cases"]:
        speeds = tuple(map(int, case["residual_speeds"]))
        moments = tuple(map(q, case["moments"]))
        pairs = tuple(combinations(speeds, 2))
        projected[case["id"]] = {
            "id": case["id"],
            "case_id": case["case_id"],
            "speeds": speeds,
            "window": tuple(map(q, case["window"])),
            "total": moments[0],
            "single_moments": {speed: moments[1 << index] for index, speed in enumerate(speeds)},
            "pair_moments": {pair: moments[mask_for_pair(speeds, pair)] for pair in pairs},
            "pair_only_minimum": q(case["baseline"]["value"]),
        }
    return projected


def choose_fewest(rows: list[dict], cost: Counter) -> tuple[int, int] | None:
    if not rows:
        return None
    chosen = rows[0]
    for row in rows[1:]:
        cost["component_count_order_comparisons"] += 1
        if row["component_count"] < chosen["component_count"]:
            chosen = row
        elif row["component_count"] == chosen["component_count"]:
            cost["component_count_ties"] += 1
            cost["physical_lexicographic_tie_breaks"] += 1
            if row["base_pair"] < chosen["base_pair"]:
                chosen = row
    return chosen["base_pair"]


def choose_largest(rows: list[dict], cost: Counter) -> tuple[int, int] | None:
    if not rows:
        return None
    chosen = rows[0]
    for row in rows[1:]:
        cost["slack_order_comparisons"] += 1
        if row["potential_slack"] > chosen["potential_slack"]:
            chosen = row
        elif row["potential_slack"] == chosen["potential_slack"]:
            cost["slack_ties"] += 1
            cost["physical_lexicographic_tie_breaks"] += 1
            if row["base_pair"] < chosen["base_pair"]:
                chosen = row
    return chosen["base_pair"]


def preselect(projected: dict) -> dict:
    speeds, window = projected["speeds"], projected["window"]
    c0 = (
        projected["total"]
        - sum(projected["single_moments"].values(), F(0))
        + sum(projected["pair_moments"].values(), F(0))
    )
    pair_only_exit = projected["pair_only_minimum"] > 0
    all_floor_cost, active_floor_cost, diagnostic_floor_cost = Counter(), Counter(), Counter()
    rows = []
    for pair in combinations(speeds, 2):
        complement = tuple(speed for speed in speeds if speed not in pair)
        slack = c0 - projected["pair_moments"][complement]
        count, transform, pair_cost = component_count_floor_sum(pair, window)
        eligible = (not pair_only_exit) and slack > 0
        category = (
            "pair_only_exit_validation_diagnostic" if pair_only_exit
            else "active_eligible_score" if eligible
            else "ineligible_all_pair_validation"
        )
        add_cost(all_floor_cost, pair_cost)
        if category == "active_eligible_score":
            add_cost(active_floor_cost, pair_cost)
        elif category == "pair_only_exit_validation_diagnostic":
            add_cost(diagnostic_floor_cost, pair_cost)
        rows.append({
            "base_pair": pair,
            "complement": complement,
            "omitted_pair_overlap": projected["pair_moments"][complement],
            "potential_slack": slack,
            "eligible": eligible,
            "component_count": count,
            "floor_sum_transform": transform,
            "floor_sum_cost": dict(sorted(pair_cost.items())),
            "cost_category": category,
        })
    eligible = [row for row in rows if row["eligible"]]
    selection_cost = Counter()
    decisions = {
        "fewest_components": choose_fewest(eligible, selection_cost),
        "largest_slack_comparator": choose_largest(eligible, selection_cost),
    }
    return {
        "C_0": c0,
        "pair_only_minimum": projected["pair_only_minimum"],
        "pair_only_exit": pair_only_exit,
        "pair_rows": rows,
        "eligible_base_pairs": [row["base_pair"] for row in eligible],
        "decisions": decisions,
        "floor_sum_cost": {
            "all_six_pair_validation": dict(sorted(all_floor_cost.items())),
            "active_eligible_scores": dict(sorted(active_floor_cost.items())),
            "pair_only_exit_diagnostics": dict(sorted(diagnostic_floor_cost.items())),
            "selection_comparisons": dict(sorted(selection_cost.items())),
        },
        "primary_preselection_forbidden_structures": {
            "per_lap_loops": 0,
            "blocking_interval_lists": 0,
            "pair_intersection_lists": 0,
            "complement_states_read": 0,
        },
    }


def row_by_pair(rows: list[dict], pair: tuple[int, int]) -> dict:
    return next(row for row in rows if row["base_pair"] == pair)


def analyze_active_case(projected: dict) -> dict:
    prepared = preselect(projected)
    speeds, window = projected["speeds"], projected["window"]

    # Selected physical calculations begin only after both choices are fixed.
    selected_pairs = []
    if not prepared["pair_only_exit"]:
        for rule in RULES:
            pair = prepared["decisions"][rule]
            if pair is not None and pair not in selected_pairs:
                selected_pairs.append(pair)
    selected_queries = {
        pair: containment_query(speeds, window, pair) for pair in selected_pairs
    }
    for pair, query in selected_queries.items():
        assert query["base_positive_component_count"] == row_by_pair(
            prepared["pair_rows"], pair
        )["component_count"]

    frozen_rule_results = {}
    for rule in RULES:
        pair = prepared["decisions"][rule]
        if prepared["pair_only_exit"]:
            frozen_rule_results[rule] = {
                "selected_base_pair": None,
                "query_issued": False,
                "outcome": "pair_only_positive_exit",
                "certified_lower_bound": prepared["pair_only_minimum"],
                "second_query_issued": False,
            }
        elif pair is None:
            frozen_rule_results[rule] = {
                "selected_base_pair": None,
                "query_issued": False,
                "outcome": "no_eligible_pair_no_query",
                "certified_lower_bound": None,
                "second_query_issued": False,
            }
        else:
            row = row_by_pair(prepared["pair_rows"], pair)
            query = selected_queries[pair]
            frozen_rule_results[rule] = {
                "selected_base_pair": pair,
                "selected_complement": row["complement"],
                "selected_potential_slack": row["potential_slack"],
                "selected_component_count": row["component_count"],
                "query_issued": True,
                "physical_query_reused_between_rules": list(prepared["decisions"].values()).count(pair) == 2,
                "containment_holds": query["containment_holds"],
                "first_exact_violation": query["first_exact_violation"],
                "outcome": "certified" if query["containment_holds"] else "failed_no_retune",
                "certified_lower_bound": row["potential_slack"] if query["containment_holds"] else None,
                "counterfactual_bound_if_containment_held": row["potential_slack"],
                "second_query_issued": False,
            }

    # Oracle starts only after the frozen result records above are complete.
    oracle_queries = {
        tuple(row["base_pair"]): containment_query(speeds, window, tuple(row["base_pair"]))
        for row in prepared["pair_rows"] if row["eligible"]
    }
    for pair, query in oracle_queries.items():
        assert query["base_positive_component_count"] == row_by_pair(
            prepared["pair_rows"], pair
        )["component_count"]
    successful_oracle = sorted(
        pair for pair, query in oracle_queries.items() if query["containment_holds"]
    )
    for rule in RULES:
        result = frozen_rule_results[rule]
        if result["outcome"] == "failed_no_retune":
            result["failure_classification"] = (
                "ranking_failure" if successful_oracle else "certificate_class_failure"
            )
        else:
            result["failure_classification"] = None

    return {
        "id": projected["id"],
        "case_id": projected["case_id"],
        "speeds": speeds,
        "window": window,
        "C_0": prepared["C_0"],
        "pair_only_minimum": prepared["pair_only_minimum"],
        "pair_only_exit": prepared["pair_only_exit"],
        "pair_rows": prepared["pair_rows"],
        "eligible_base_pairs": prepared["eligible_base_pairs"],
        "preselection_decisions": prepared["decisions"],
        "frozen_rule_results": frozen_rule_results,
        "selected_unique_physical_queries": [selected_queries[pair] for pair in selected_pairs],
        "selected_logical_query_count": sum(
            result["query_issued"] for result in frozen_rule_results.values()
        ),
        "selected_unique_physical_query_count": len(selected_pairs),
        "postselection_oracle": {
            "eligible_pairs_tested": len(oracle_queries),
            "successful_pairs": successful_oracle,
            "queries": [oracle_queries[pair] for pair in sorted(oracle_queries)],
            "cannot_change_frozen_rules": True,
        },
        "floor_sum_cost": prepared["floor_sum_cost"],
        "primary_preselection_forbidden_structures": prepared["primary_preselection_forbidden_structures"],
    }


def query_cost_sum(queries: list[dict]) -> dict:
    total = Counter()
    for query in queries:
        add_cost(total, query["operation_cost"])
        add_cost(total, query["event_ledger"])
    return dict(sorted(total.items()))


def attach_archive_comparison(result: dict, archived: dict, development_ids: set[str]) -> None:
    result["development_record"] = result["id"] in development_ids
    result["transfer_record"] = result["id"] not in development_ids
    triple_values = [q(row["certificate"]["value"]) for row in archived["cover_triple_minima"]]
    archived_classification = (
        "pair_only_positive"
        if q(archived["baseline"]["value"]) > 0
        else "collective_only_counterpart"
        if archived["collective_only_counterpart"]
        else "individual_triple_forced_under_cover"
    )
    if archived_classification == "individual_triple_forced_under_cover":
        assert any(value > 0 for value in triple_values)
    if archived_classification == "collective_only_counterpart":
        assert triple_values and all(value == 0 for value in triple_values)
    result["postselection_archive_comparison"] = {
        "actual_positive_uncovered_duration": q(archived["archived_actual_duration"]),
        "archive_pair_only_minimum": q(archived["baseline"]["value"]),
        "collective_only_counterpart": bool(archived["collective_only_counterpart"]),
        "archived_mechanism_classification": archived_classification,
        "cover_triple_minima": [
            {
                "speeds": row["speeds"],
                "minimum_under_cover": q(row["certificate"]["value"]),
            }
            for row in archived["cover_triple_minima"]
        ],
        "archive_data_used_to_change_frozen_rule": False,
        "sparse_triple_and_alternate_window_results_are_known_prior_work": True,
    }


def reflection_audit(cases: dict, groups: list[dict]) -> list[dict]:
    output = []
    for group in groups:
        first_id, second_id = group["record_ids"]
        first, second = cases[first_id], cases[second_id]
        assert first["speeds"] == second["speeds"]
        assert first["pair_only_minimum"] == second["pair_only_minimum"]
        assert first["eligible_base_pairs"] == second["eligible_base_pairs"]
        assert first["preselection_decisions"] == second["preselection_decisions"]
        for rule in RULES:
            a, b = first["frozen_rule_results"][rule], second["frozen_rule_results"][rule]
            assert a["outcome"] == b["outcome"]
            assert a["certified_lower_bound"] == b["certified_lower_bound"]
            assert a["failure_classification"] == b["failure_classification"]
        assert first["postselection_oracle"]["successful_pairs"] == second["postselection_oracle"]["successful_pairs"]
        output.append({
            "record_ids": (first_id, second_id),
            "outcomes_match_exactly": True,
            "counted_as_independent_examples": False,
            "collective_only_counterpart": bool(group["collective_only_counterpart"]),
        })
    return output


def analyze_controls(prior: dict) -> dict:
    """Reapply the frozen dispatch/counter/query to the three named controls."""
    output = {}
    for name in ("strict_16", "doubling_112", "tight_13"):
        source = prior["cases"][name]
        speeds = tuple(map(int, source["speeds"]))
        window = tuple(map(q, source["window"]))
        pair_only = q(source["pair_only_exit"]["archived_positive_optimum"]) if source["pair_only_exit"] else F(0)
        rows = []
        for old in source["all_six_potential_slacks"]:
            pair = tuple(map(int, old["base_pair"]))
            count, transform, cost = component_count_floor_sum(pair, window)
            rows.append({
                "base_pair": pair,
                "complement": tuple(map(int, old["complement"])),
                "potential_slack": q(old["potential_slack"]),
                "eligible": pair_only == 0 and q(old["potential_slack"]) > 0,
                "component_count": count,
                "floor_sum_transform": transform,
                "floor_sum_cost": dict(sorted(cost.items())),
            })
        eligible = [row for row in rows if row["eligible"]]
        choice_cost = Counter()
        choices = {
            "fewest_components": choose_fewest(eligible, choice_cost),
            "largest_slack_comparator": choose_largest(eligible, choice_cost),
        }
        queries = {}
        if pair_only == 0:
            for pair in choices.values():
                if pair is not None and pair not in queries:
                    queries[pair] = containment_query(speeds, window, pair)
        rule_results = {}
        for rule, pair in choices.items():
            if pair_only > 0:
                rule_results[rule] = {"outcome": "pair_only_positive_exit", "query_issued": False, "certified_lower_bound": pair_only}
            elif pair is None:
                rule_results[rule] = {"outcome": "no_eligible_pair_no_query", "query_issued": False, "certified_lower_bound": None}
            else:
                row = row_by_pair(rows, pair)
                query = queries[pair]
                rule_results[rule] = {
                    "selected_base_pair": pair,
                    "query_issued": True,
                    "containment_holds": query["containment_holds"],
                    "outcome": "certified" if query["containment_holds"] else "failed_no_retune",
                    "certified_lower_bound": row["potential_slack"] if query["containment_holds"] else None,
                    "first_exact_violation": query["first_exact_violation"],
                }
        endpoint = source["isolated_equality_endpoint"] if name == "tight_13" else None
        output[name] = {
            "speeds": speeds,
            "window": window,
            "pair_only_minimum": pair_only,
            "pair_rows": rows,
            "choices": choices,
            "rule_results": rule_results,
            "unique_physical_queries": [queries[pair] for pair in sorted(queries)],
            "isolated_equality_endpoint": endpoint,
        }
    assert all(
        row["certified_lower_bound"] == F(1, 896)
        for row in output["strict_16"]["rule_results"].values()
    )
    assert all(
        row["outcome"] == "pair_only_positive_exit" and row["certified_lower_bound"] == F(761, 32256)
        for row in output["doubling_112"]["rule_results"].values()
    )
    assert all(
        row["outcome"] == "no_eligible_pair_no_query"
        for row in output["tight_13"]["rule_results"].values()
    )
    assert output["tight_13"]["isolated_equality_endpoint"]["time"] == "3/8"
    return output


def build(old=None) -> dict:
    assert sha256(PROTOCOL) == PROTOCOL_SHA256
    protocol = json.loads(PROTOCOL.read_text())
    paths = {}
    for key, value in protocol["source_contract"].items():
        if key.endswith("_sha256"):
            continue
        path = ROOT / value
        assert sha256(path) == protocol["source_contract"][f"{key}_sha256"]
        paths[key] = path

    archive_preselection = json.loads(paths["archived_windows"].read_text())
    projected = project_archived_cases(archive_preselection)
    assert len(projected) == protocol["scope"]["archived_records"]
    # Make the projection literal: no full row, archived classification,
    # reflection group, atom, LP certificate or actual duration survives into
    # the decision/calculation phase.
    del archive_preselection
    cases = {case_id: analyze_active_case(record) for case_id, record in projected.items()}

    # Only now, with both frozen rules and every oracle classification already
    # immutable, reload the pinned archive for comparisons and reflection QA.
    archive_postselection = json.loads(paths["archived_windows"].read_text())
    archived_rows = archive_postselection["cases"]
    reflection_groups = archive_postselection["summary"]["reflection_groups"]
    development_ids = set(protocol["frozen_domain"]["development_records"])
    archived_by_id = {row["id"]: row for row in archived_rows}
    for case_id, result in cases.items():
        attach_archive_comparison(result, archived_by_id[case_id], development_ids)
    reflections = reflection_audit(cases, reflection_groups)
    transfer_reflection_groups = [
        group for group in reflections
        if not cases[group["record_ids"][0]]["development_record"]
    ]
    development_reflection_groups = [
        group for group in reflections
        if cases[group["record_ids"][0]]["development_record"]
    ]

    prior_controls = json.loads(paths["prior_one_query_results"].read_text())
    controls = analyze_controls(prior_controls)

    values = list(cases.values())
    transfer = [case for case in values if case["transfer_record"]]
    development = [case for case in values if case["development_record"]]

    def outcome_count(scope_cases: list[dict], rule: str, outcome: str) -> int:
        return sum(case["frozen_rule_results"][rule]["outcome"] == outcome for case in scope_cases)

    selected_queries = [
        query for case in values for query in case["selected_unique_physical_queries"]
    ]
    oracle_queries = [
        query for case in values for query in case["postselection_oracle"]["queries"]
    ]
    floor_all, floor_active, floor_exit = Counter(), Counter(), Counter()
    for case in values:
        add_cost(floor_all, case["floor_sum_cost"]["all_six_pair_validation"])
        add_cost(floor_active, case["floor_sum_cost"]["active_eligible_scores"])
        add_cost(floor_exit, case["floor_sum_cost"]["pair_only_exit_diagnostics"])

    result = {
        "baseline": protocol["baseline"],
        "protocol_sha256": PROTOCOL_SHA256,
        "primary_sha256": sha256(Path(__file__)),
        "source_contract": protocol["source_contract"],
        "arithmetic": "integers and fractions.Fraction only; no floating-point decisions",
        "information_barrier": (
            "The 18 records were irreversibly projected to ids, speeds, windows, moments and pair-only minima before all decisions. Selected geometry began only after both choices; the all-eligible oracle began only after frozen outcomes."
        ),
        "cases": cases,
        "reflection_audit": reflections,
        "controls": controls,
        "counts": {
            "archived_records": len(values),
            "development_records": len(development),
            "transfer_records": len(transfer),
            "reflection_pairs": len(reflections),
            "transfer_reflection_pairs": len(transfer_reflection_groups),
            "development_reflection_pairs": len(development_reflection_groups),
            "independent_examples_claimed": 0,
            "pair_only_positive_exits": sum(case["pair_only_exit"] for case in values),
            "active_zero_pair_only_records": sum(not case["pair_only_exit"] for case in values),
            "eligible_pair_scores": sum(len(case["eligible_base_pairs"]) for case in values),
            "selected_logical_queries": sum(case["selected_logical_query_count"] for case in values),
            "selected_unique_physical_queries": len(selected_queries),
            "oracle_eligible_pair_queries": len(oracle_queries),
            "second_or_fallback_queries": 0,
        },
        "transfer_outcomes": {
            rule: {
                "certified": outcome_count(transfer, rule, "certified"),
                "failed_no_retune": outcome_count(transfer, rule, "failed_no_retune"),
                "pair_only_positive_exit": outcome_count(transfer, rule, "pair_only_positive_exit"),
                "no_eligible_pair_no_query": outcome_count(transfer, rule, "no_eligible_pair_no_query"),
                "ranking_failures": sum(case["frozen_rule_results"][rule]["failure_classification"] == "ranking_failure" for case in transfer),
                "certificate_class_failures": sum(case["frozen_rule_results"][rule]["failure_classification"] == "certificate_class_failure" for case in transfer),
            }
            for rule in RULES
        },
        "postselection_archived_mechanism_counts": dict(sorted(Counter(
            case["postselection_archive_comparison"]["archived_mechanism_classification"]
            for case in values
        ).items())),
        "development_outcomes": {
            rule: {
                "certified": outcome_count(development, rule, "certified"),
                "failed_no_retune": outcome_count(development, rule, "failed_no_retune"),
            }
            for rule in RULES
        },
        "transfer_reflection_pair_outcomes": {
            rule: dict(sorted(Counter(
                cases[group["record_ids"][0]]["frozen_rule_results"][rule]["outcome"]
                for group in transfer_reflection_groups
            ).items()))
            for rule in RULES
        },
        "aggregate_cost_ledgers": {
            "floor_sum_all_108_pair_validation": dict(sorted(floor_all.items())),
            "floor_sum_active_eligible_scores": dict(sorted(floor_active.items())),
            "floor_sum_pair_only_exit_diagnostics": dict(sorted(floor_exit.items())),
            "selected_unique_containment_queries": query_cost_sum(selected_queries),
            "postselection_all_eligible_oracle_queries": query_cost_sum(oracle_queries),
            "comparison_policy": "Unlike operations are not combined and no wall-clock inference is made.",
        },
        "findings": {
            "finite_status": "OBSERVED on the frozen archival records",
            "transfer_is_prospective_held_out_validation": False,
            "reflections_are_independent_examples": False,
            "general_selector_claim": False,
            "whole_configuration_claim": False,
            "novelty_claim": False,
            "independent_mathematical_validation": False,
        },
        "scope": protocol["scope"],
        "interpretation_limits": protocol["interpretation_limits"],
    }
    output = serial(result)
    if old is not None:
        assert output == old
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    old = None if args.write else json.loads(OUT.read_text())
    result = build(old)
    if args.write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["transfer_outcomes"], indent=2))
    print(result["counts"])
    print("WROTE: selector transfer audit" if args.write else "PASS: selector transfer audit reproduced read-only")


if __name__ == "__main__":
    main()
