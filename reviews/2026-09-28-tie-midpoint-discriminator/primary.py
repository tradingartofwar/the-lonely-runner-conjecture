"""Exact primary calculation for the frozen tie-midpoint discriminator.

The implementation enforces the information barrier in ``protocol.json``:

* selector-transfer data are copied field-by-field into a deliberately small
  projection and the source object is deleted;
* tied components and midpoint scores are then reconstructed exactly;
* the selected containment queries are completed and frozen;
* only then are all tied pairs queried as a charged oracle and the pinned
  archive reloaded for comparison.

``--write`` deterministically writes ``results.json``.  ``--check`` is
read-only and requires a byte-equivalent reconstruction after JSON parsing.
All mathematical decisions use integers and ``fractions.Fraction``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.json"
OUT = HERE / "results.json"
PROTOCOL_SHA256 = "e62d116b764aa0869788dffb36785935d08e3de1ddb38d3e0ca11ca23ba3f2e3"
DELTA = F(1, 8)


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


def add_cost(target: Counter, source: dict | Counter) -> None:
    target.update({key: int(value) for key, value in source.items()})


def phase(speed: int, time: F) -> F:
    return (speed * time) % 1


def distance(speed: int, time: F) -> F:
    p = phase(speed, time)
    return min(p, 1 - p)


def is_blocking(speed: int, time: F, cost: Counter | None = None) -> bool:
    if cost is not None:
        cost["phase_reductions"] += 1
        cost["distance_computations"] += 1
        cost["blocking_state_comparisons"] += 1
    return distance(speed, time) < DELTA


# -------------------------------------------------------------------------
# Literal source projections.  No source containment result, duration,
# violation, mechanism, or frozen decision is copied across this boundary.


def project_records(source: dict, wanted: tuple[str, ...]) -> dict:
    projected = {}
    for record_id in wanted:
        row = source["cases"][record_id]
        pair_rows = []
        for pair_row in row["pair_rows"]:
            if pair_row["eligible"]:
                pair_rows.append({
                    "base_pair": tuple(map(int, pair_row["base_pair"])),
                    "complement": tuple(map(int, pair_row["complement"])),
                    "potential_slack": q(pair_row["potential_slack"]),
                    "component_count": int(pair_row["component_count"]),
                })
        projected[record_id] = {
            "id": str(row["id"]),
            "speeds": tuple(map(int, row["speeds"])),
            "window": tuple(map(q, row["window"])),
            "pair_only_minimum": q(row["pair_only_minimum"]),
            "eligible_pairs": tuple(pair_rows),
        }
    return projected


def project_controls(source: dict, wanted: tuple[str, ...]) -> dict:
    projected = {}
    for name in wanted:
        row = source["cases"][name]
        exit_row = row["pair_only_exit"]
        pair_only = q(exit_row["archived_positive_optimum"]) if exit_row else F(0)
        eligible = []
        # The frozen dispatch is literal: a positive pair-only optimum prevents
        # even diagnostic component fields from crossing the projection.
        if pair_only == 0:
            for pair_row in row["all_six_potential_slacks"]:
                if bool(pair_row["eligible"]):
                    eligible.append({
                        "base_pair": tuple(map(int, pair_row["base_pair"])),
                        "complement": tuple(map(int, pair_row["complement"])),
                        "potential_slack": q(pair_row["potential_slack"]),
                        "component_count": int(pair_row["positive_component_count"]),
                    })
        isolated = None
        if row["isolated_equality_endpoint"] is not None:
            isolated = {"time": q(row["isolated_equality_endpoint"]["time"])}
        projected[name] = {
            "id": name,
            "speeds": tuple(map(int, row["speeds"])),
            "window": tuple(map(q, row["window"])),
            "pair_only_minimum": pair_only,
            "eligible_pairs": tuple(eligible),
            "isolated_equality_endpoint": isolated,
        }
    return projected


# -------------------------------------------------------------------------
# Exact positive blocker components and prescribed midpoint samples.


def blocking_pieces(speed: int, window: tuple[F, F], cost: Counter) -> list[dict]:
    left, right = window
    pieces = []
    for lap in range(floor(speed * left) - 1, floor(speed * right) + 2):
        cost["lap_candidates"] += 1
        raw_left = (F(lap) - DELTA) / speed
        raw_right = (F(lap) + DELTA) / speed
        cost["clip_comparisons"] += 2
        lo, hi = max(left, raw_left), min(right, raw_right)
        cost["nonempty_comparisons"] += 1
        if lo < hi:
            pieces.append({
                "interval": (lo, hi),
                "lap": lap,
                "left_included": is_blocking(speed, lo, cost),
                "right_included": is_blocking(speed, hi, cost),
            })
    cost["blocking_pieces"] += len(pieces)
    return pieces


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


def midpoint_score(
    speeds: tuple[int, ...], window: tuple[F, F], pair: tuple[int, int]
) -> dict:
    reconstruction_cost = Counter()
    components = base_components(pair, window, reconstruction_cost)
    complement = tuple(speed for speed in speeds if speed not in pair)
    score_cost = Counter()
    samples = []
    margins = []
    for component_index, component in enumerate(components):
        left, right = component["interval"]
        midpoint = (left + right) / 2
        score_cost["midpoint_samples"] += 1
        evaluations = []
        for speed in complement:
            p = phase(speed, midpoint)
            d = min(p, 1 - p)
            margin = d - DELTA
            score_cost["complement_phase_reductions"] += 1
            score_cost["distance_computations"] += 1
            score_cost["signed_margin_subtractions"] += 1
            margins.append(margin)
            evaluations.append({
                "speed": speed,
                "phase": p,
                "distance_to_integer": d,
                "signed_safety_margin": margin,
            })
        samples.append({
            "component_index": component_index,
            "interval": component["interval"],
            "laps": component["laps"],
            "left_included": component["left_included"],
            "right_included": component["right_included"],
            "midpoint": midpoint,
            "complement_evaluations": evaluations,
        })
    assert margins
    score = margins[0]
    for margin in margins[1:]:
        score_cost["minimum_margin_comparisons"] += 1
        if margin < score:
            score = margin
    return {
        "base_pair": pair,
        "complement": complement,
        "component_count": len(components),
        "components_and_samples": samples,
        "pair_score": score,
        "score_predicts_containment": score >= 0,
        "reconstruction_cost": dict(sorted(reconstruction_cost.items())),
        "midpoint_score_cost": dict(sorted(score_cost.items())),
    }


def choose_maximin(scored: list[dict]) -> tuple[tuple[int, int], Counter]:
    assert scored
    cost = Counter()
    chosen = scored[0]
    for row in scored[1:]:
        cost["pair_score_comparisons"] += 1
        if row["pair_score"] > chosen["pair_score"]:
            chosen = row
        elif row["pair_score"] == chosen["pair_score"]:
            cost["exact_pair_score_ties"] += 1
            cost["physical_lexicographic_tie_breaks"] += 1
            if row["base_pair"] < chosen["base_pair"]:
                chosen = row
    return chosen["base_pair"], cost


# -------------------------------------------------------------------------
# Exact full containment query, prohibited until selections are immutable.


def threshold_event_ledger(speeds: tuple[int, ...], window: tuple[F, F]) -> dict:
    left, right = window
    events = {left, right}
    raw = 0
    for speed in speeds:
        for lap in range(floor(speed * left) - 1, floor(speed * right) + 2):
            for sign in (-1, 1):
                point = (F(lap) + sign * DELTA) / speed
                if left <= point <= right:
                    raw += 1
                    events.add(point)
    ordered = sorted(events)
    return {
        "raw_in_window_thresholds": raw,
        "unique_threshold_events_including_window_endpoints": len(ordered),
        "open_cells": len(ordered) - 1,
    }


def intersect_violation(
    base: dict, blocker: dict, speed: int, cost: Counter
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
        assert distance(speed, witness) < DELTA
        return {
            "kind": "positive_interval",
            "interval": (lo, hi),
            "left_included": left_included,
            "right_included": right_included,
            "witness": witness,
            "witness_phase": phase(speed, witness),
            "tested_complement_speed": speed,
            "base_laps": base["laps"],
            "complement_lap": blocker["lap"],
        }
    if lo == hi and left_included and right_included:
        assert distance(speed, lo) < DELTA
        return {
            "kind": "included_endpoint",
            "time": lo,
            "tested_complement_speed": speed,
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
    complement_pieces = {
        speed: blocking_pieces(speed, window, cost) for speed in complement
    }
    violations = []
    for component in base:
        for speed in complement:
            for blocker in complement_pieces[speed]:
                cost["base_complement_piece_tests"] += 1
                found = intersect_violation(component, blocker, speed, cost)
                if found is not None:
                    violations.append(found)
    violations.sort(key=violation_key)
    cost["containment_conclusions"] += 1
    return {
        "base_pair": pair,
        "complement": complement,
        "base_positive_component_count": len(base),
        "containment_holds": not violations,
        "violation_count": len(violations),
        "first_exact_violation": violations[0] if violations else None,
        "all_exact_violations": violations,
        "event_ledger": threshold_event_ledger(speeds, window),
        "operation_cost": dict(sorted(cost.items())),
        "endpoint_semantics": "strict blocker distance<1/8; equality is safe",
    }


# -------------------------------------------------------------------------
# Dispatch, scoring, selected query, and separately charged tied-pair oracle.


def prepare_case(projected: dict, role: str) -> dict:
    pair_only = projected["pair_only_minimum"]
    eligible = list(projected["eligible_pairs"])
    base = {
        "id": projected["id"],
        "role": role,
        "speeds": projected["speeds"],
        "window": projected["window"],
        "pair_only_minimum": pair_only,
        "eligible_pair_count": len(eligible),
        "forbidden_preselection_fields_retained": [],
    }
    if pair_only > 0:
        base.update({
            "dispatch": "pair_only_positive_exit",
            "minimum_component_count": None,
            "tied_minimum_pairs": [],
            "scored_tied_pairs": [],
            "candidate_selected_pair": None,
            "inherited_lexicographic_pair": None,
            "choice_cost": {},
        })
        return base
    if not eligible:
        base.update({
            "dispatch": "no_eligible_pair_no_duration_query",
            "minimum_component_count": None,
            "tied_minimum_pairs": [],
            "scored_tied_pairs": [],
            "candidate_selected_pair": None,
            "inherited_lexicographic_pair": None,
            "choice_cost": {},
        })
        return base
    minimum = min(row["component_count"] for row in eligible)
    tied = sorted(
        (row for row in eligible if row["component_count"] == minimum),
        key=lambda row: row["base_pair"],
    )
    if len(tied) == 1:
        pair = tied[0]["base_pair"]
        base.update({
            "dispatch": "unique_minimum_count_retains_prior_selection",
            "minimum_component_count": minimum,
            "tied_minimum_pairs": [pair],
            "scored_tied_pairs": [],
            "candidate_selected_pair": pair,
            "inherited_lexicographic_pair": pair,
            "choice_cost": {},
        })
        return base
    scored = []
    for row in tied:
        score = midpoint_score(projected["speeds"], projected["window"], row["base_pair"])
        assert score["component_count"] == row["component_count"]
        score["potential_slack"] = row["potential_slack"]
        scored.append(score)
    selected, choice_cost = choose_maximin(scored)
    base.update({
        "dispatch": "minimum_count_tie_midpoint_scored",
        "minimum_component_count": minimum,
        "tied_minimum_pairs": [row["base_pair"] for row in tied],
        "scored_tied_pairs": scored,
        "candidate_selected_pair": selected,
        "inherited_lexicographic_pair": tied[0]["base_pair"],
        "choice_cost": dict(sorted(choice_cost.items())),
    })
    return base


def potential_slack(projected: dict, pair: tuple[int, int]) -> F:
    return next(
        row["potential_slack"] for row in projected["eligible_pairs"]
        if row["base_pair"] == pair
    )


def attach_selected_query(prepared: dict, projected: dict) -> None:
    dispatch = prepared["dispatch"]
    if dispatch == "pair_only_positive_exit":
        prepared["selected_result"] = {
            "query_issued": False,
            "outcome": "pair_only_positive_exit",
            "certified_lower_bound": projected["pair_only_minimum"],
            "second_or_fallback_query_issued": False,
        }
        return
    if dispatch == "no_eligible_pair_no_duration_query":
        prepared["selected_result"] = {
            "query_issued": False,
            "outcome": "no_eligible_pair_no_duration_query",
            "certified_lower_bound": None,
            "second_or_fallback_query_issued": False,
        }
        if projected.get("isolated_equality_endpoint") is not None:
            prepared["isolated_equality_endpoint"] = projected["isolated_equality_endpoint"]
        return
    pair = prepared["candidate_selected_pair"]
    query = containment_query(projected["speeds"], projected["window"], pair)
    prepared["selected_query"] = query
    prepared["selected_result"] = {
        "query_issued": True,
        "selected_base_pair": pair,
        "selected_pair_score": next(
            (row["pair_score"] for row in prepared["scored_tied_pairs"] if row["base_pair"] == pair),
            None,
        ),
        "containment_holds": query["containment_holds"],
        "outcome": "certified" if query["containment_holds"] else "failed_no_retune",
        "certified_lower_bound": potential_slack(projected, pair) if query["containment_holds"] else None,
        "counterfactual_bound_if_containment_held": potential_slack(projected, pair),
        "first_exact_violation": query["first_exact_violation"],
        "second_or_fallback_query_issued": False,
    }


def attach_oracle(prepared: dict, projected: dict) -> None:
    if prepared["dispatch"] != "minimum_count_tie_midpoint_scored":
        prepared["postselection_tied_pair_oracle"] = {
            "queries": [],
            "charged_separately_from_selected_query": True,
            "cannot_change_frozen_choice": True,
        }
        return
    score_by_pair = {row["base_pair"]: row for row in prepared["scored_tied_pairs"]}
    queries = []
    for pair in prepared["tied_minimum_pairs"]:
        query = containment_query(projected["speeds"], projected["window"], pair)
        score = score_by_pair[pair]
        predicted = score["score_predicts_containment"]
        actual = query["containment_holds"]
        query["midpoint_pair_score"] = score["pair_score"]
        query["midpoint_sign_prediction"] = predicted
        query["prediction_class"] = (
            "true_positive" if predicted and actual
            else "false_positive" if predicted and not actual
            else "false_negative" if not predicted and actual
            else "true_negative"
        )
        queries.append(query)
    selected = prepared["candidate_selected_pair"]
    selected_query = next(row for row in queries if row["base_pair"] == selected)
    inversion_witnesses = []
    for higher in queries:
        for lower in queries:
            if (
                higher["midpoint_pair_score"] > lower["midpoint_pair_score"]
                and not higher["containment_holds"]
                and lower["containment_holds"]
            ):
                inversion_witnesses.append({
                    "higher_scored_failed_pair": higher["base_pair"],
                    "higher_score": higher["midpoint_pair_score"],
                    "lower_scored_successful_pair": lower["base_pair"],
                    "lower_score": lower["midpoint_pair_score"],
                })
    prepared["postselection_tied_pair_oracle"] = {
        "queries": queries,
        "successful_pairs": [row["base_pair"] for row in queries if row["containment_holds"]],
        "failed_pairs": [row["base_pair"] for row in queries if not row["containment_holds"]],
        "prediction_class_counts": dict(sorted(Counter(row["prediction_class"] for row in queries).items())),
        "selected_pair_contains": selected_query["containment_holds"],
        "score_order_inversion": bool(inversion_witnesses),
        "score_order_inversion_witnesses": inversion_witnesses,
        "charged_separately_from_selected_query": True,
        "cannot_change_frozen_choice": True,
    }


def attach_archive_comparison(prepared: dict, source_case: dict) -> None:
    tied_source = {
        tuple(row["base_pair"]): row
        for row in source_case["postselection_oracle"]["queries"]
        if tuple(row["base_pair"]) in prepared["tied_minimum_pairs"]
    }
    oracle = prepared["postselection_tied_pair_oracle"]["queries"]
    comparisons = []
    for query in oracle:
        source = tied_source[query["base_pair"]]
        assert query["containment_holds"] == source["containment_holds"]
        assert query["first_exact_violation"] == _fractionize(source["first_exact_violation"])
        comparisons.append({
            "base_pair": query["base_pair"],
            "containment_matches_pinned_archive": True,
            "first_violation_matches_pinned_archive": True,
        })
    lex_pair = prepared["inherited_lexicographic_pair"]
    lex_query = next((row for row in oracle if row["base_pair"] == lex_pair), None)
    prepared["postselection_archive_comparison"] = {
        "tied_pair_comparisons": comparisons,
        "inherited_lexicographic_pair": lex_pair,
        "inherited_lexicographic_containment_holds": (
            lex_query["containment_holds"] if lex_query is not None else None
        ),
        "archive_used_to_change_candidate_choice": False,
    }


def _fractionize(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return q(value)
        except (ValueError, ZeroDivisionError):
            return value
    if isinstance(value, list):
        return tuple(_fractionize(item) for item in value)
    if isinstance(value, dict):
        return {key: _fractionize(item) for key, item in value.items()}
    return value


def reflection_audit(cases: dict) -> list[dict]:
    groups = (
        ("squares:1,2,5:12", "squares:1,2,5:39", "development"),
        ("fibonacci:1,2,4:1", "fibonacci:1,2,4:32", "archival_control"),
        ("fibonacci:1,2,4:11", "fibonacci:1,2,4:22", "archival_control"),
    )
    output = []
    for first_id, second_id, role in groups:
        first, second = cases[first_id], cases[second_id]
        assert first["candidate_selected_pair"] == second["candidate_selected_pair"]
        assert [row["pair_score"] for row in first["scored_tied_pairs"]] == [
            row["pair_score"] for row in second["scored_tied_pairs"]
        ]
        assert first["selected_result"]["outcome"] == second["selected_result"]["outcome"]
        assert first["postselection_tied_pair_oracle"]["successful_pairs"] == second["postselection_tied_pair_oracle"]["successful_pairs"]
        output.append({
            "record_ids": (first_id, second_id),
            "role": role,
            "scores_choices_and_outcomes_match": True,
            "counted_as_independent_validation": False,
        })
    return output


def query_cost(queries: list[dict]) -> dict:
    total = Counter()
    for query in queries:
        add_cost(total, query["operation_cost"])
        add_cost(total, query["event_ledger"])
    return dict(sorted(total.items()))


def score_cost(cases: list[dict]) -> dict:
    reconstruction = Counter()
    score = Counter()
    choice = Counter()
    tied_pairs = components = 0
    for case in cases:
        for row in case["scored_tied_pairs"]:
            tied_pairs += 1
            components += row["component_count"]
            add_cost(reconstruction, row["reconstruction_cost"])
            add_cost(score, row["midpoint_score_cost"])
        add_cost(choice, case["choice_cost"])
    return {
        "tied_pairs": tied_pairs,
        "reconstructed_positive_components": components,
        "component_reconstruction_operations": dict(sorted(reconstruction.items())),
        "prescribed_midpoint_operations": dict(sorted(score.items())),
        "pair_choice_operations": dict(sorted(choice.items())),
    }


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

    development_ids = tuple(protocol["frozen_domain"]["development_records"])
    archive_ids = tuple(protocol["frozen_domain"]["archival_control_records"])
    wanted = development_ids + archive_ids

    # Literal projection/deletion is part of the frozen information contract.
    raw_selector = json.loads(paths["selector_transfer_results"].read_text())
    records = project_records(raw_selector, wanted)
    del raw_selector
    raw_controls = json.loads(paths["one_query_results"].read_text())
    controls_projected = project_controls(
        raw_controls, (protocol["frozen_domain"]["named_control"], *protocol["frozen_domain"]["dispatch_controls"])
    )
    del raw_controls

    cases = {
        record_id: prepare_case(
            records[record_id],
            "development" if record_id in development_ids else "archival_control",
        )
        for record_id in wanted
    }
    controls = {
        name: prepare_case(controls_projected[name], "named_control" if name == "strict_16" else "dispatch_control")
        for name in controls_projected
    }

    # Choices are all immutable before any full containment answer exists.
    for record_id in wanted:
        attach_selected_query(cases[record_id], records[record_id])
    for name in controls:
        attach_selected_query(controls[name], controls_projected[name])

    # The oracle is recomputed and charged separately; it cannot change choices.
    for record_id in wanted:
        attach_oracle(cases[record_id], records[record_id])
    for name in controls:
        attach_oracle(controls[name], controls_projected[name])

    # Pinned outcomes are reloaded only now, after choices and outcomes froze.
    post_selector = json.loads(paths["selector_transfer_results"].read_text())
    for record_id in wanted:
        attach_archive_comparison(cases[record_id], post_selector["cases"][record_id])
    del post_selector

    post_controls = json.loads(paths["one_query_results"].read_text())
    # strict_16 is the sole scored control and has a pinned all-pair query set.
    strict_source = post_controls["cases"]["strict_16"]
    source_queries = {
        tuple(row["base_pair"]): row
        for row in strict_source["unique_physical_containment_queries"]
    }
    strict_comparisons = []
    for query in controls["strict_16"]["postselection_tied_pair_oracle"]["queries"]:
        source = source_queries.get(query["base_pair"])
        if source is not None:
            assert query["containment_holds"] == source["containment_holds"]
        strict_comparisons.append({
            "base_pair": query["base_pair"],
            "pinned_control_query_available": source is not None,
            "containment_matches_pinned_control": True if source is not None else None,
        })
    controls["strict_16"]["postselection_archive_comparison"] = {
        "tied_pair_comparisons": strict_comparisons,
        "archive_used_to_change_candidate_choice": False,
    }
    del post_controls

    assert controls["doubling_112"]["selected_result"]["outcome"] == "pair_only_positive_exit"
    assert controls["doubling_112"]["selected_result"]["certified_lower_bound"] == F(761, 32256)
    assert controls["tight_13"]["selected_result"]["outcome"] == "no_eligible_pair_no_duration_query"
    assert controls["tight_13"]["isolated_equality_endpoint"]["time"] == F(3, 8)

    reflections = reflection_audit(cases)
    active = list(cases.values()) + [controls["strict_16"]]
    selected_queries = [case["selected_query"] for case in active if "selected_query" in case]
    oracle_queries = [
        query for case in active
        for query in case["postselection_tied_pair_oracle"]["queries"]
    ]
    predictions = Counter(
        query["prediction_class"] for query in oracle_queries
    )

    development = [cases[item] for item in development_ids]
    archival = [cases[item] for item in archive_ids]
    result = {
        "baseline": protocol["baseline"],
        "protocol_sha256": PROTOCOL_SHA256,
        "primary_sha256": sha256(Path(__file__)),
        "source_contract": protocol["source_contract"],
        "arithmetic": "integers and fractions.Fraction only; no floating-point decisions",
        "information_barrier": (
            "Pinned selector outputs were literally projected to identifiers, speeds, windows, pair-only minima, eligible pairs, potential slacks and component counts, then deleted. Full containment answers were reloaded only after midpoint choices, selected queries and the separately charged tied-pair oracle were immutable."
        ),
        "cases": cases,
        "controls": controls,
        "reflection_audit": reflections,
        "counts": {
            "development_labels": len(development),
            "development_reflection_mechanisms": 1,
            "archival_control_labels": len(archival),
            "archival_control_reflection_mechanisms": 2,
            "named_control_labels_and_mechanisms": 1,
            "active_tie_labels": len(active),
            "active_tie_reflection_mechanisms_including_strict_16": 4,
            "candidate_selected_query_success_labels": sum(case["selected_result"]["outcome"] == "certified" for case in active),
            "candidate_selected_query_success_mechanisms": 4,
            "candidate_selected_query_failure_labels": sum(case["selected_result"]["outcome"] == "failed_no_retune" for case in active),
            "tied_pair_label_queries_in_oracle": len(oracle_queries),
            "tied_pair_reflection_mechanism_queries_in_oracle": 9,
            "selected_logical_queries": len(selected_queries),
            "selected_physical_window_queries": len(selected_queries),
            "selected_reflection_mechanism_queries": 4,
            "second_or_fallback_queries": 0,
            "pair_only_dispatch_exits": 1,
            "no_eligible_pair_dispatch_exits": 1,
        },
        "outcomes": {
            "development_score_orders_known_success_before_known_failure": all(
                case["candidate_selected_pair"] == (25, 121) for case in development
            ),
            "development_selected_queries_certified": sum(case["selected_result"]["outcome"] == "certified" for case in development),
            "development_failed_tied_pair_labels": sum(len(case["postselection_tied_pair_oracle"]["failed_pairs"]) for case in development),
            "archival_control_selected_queries_certified": sum(case["selected_result"]["outcome"] == "certified" for case in archival),
            "strict_16_selected_query_certified": controls["strict_16"]["selected_result"]["outcome"] == "certified",
            "midpoint_sign_prediction_counts": dict(sorted(predictions.items())),
            "score_order_inversion_labels": sum(case["postselection_tied_pair_oracle"]["score_order_inversion"] for case in active),
            "all_control_tied_pairs_contain": all(
                query["containment_holds"]
                for case in archival + [controls["strict_16"]]
                for query in case["postselection_tied_pair_oracle"]["queries"]
            ),
        },
        "aggregate_cost_ledgers": {
            "candidate_preselection_midpoint_scores": score_cost(active),
            "selected_one_query": query_cost(selected_queries),
            "postselection_all_tied_pair_oracle_charged_separately": query_cost(oracle_queries),
            "comparison_policy": "Unlike operations are not combined into a synthetic runtime score.",
        },
        "findings": {
            "finite_status": "OBSERVED on frozen development and archival controls",
            "development_fit_is_validation": False,
            "archival_controls_are_prospective_held_out": False,
            "midpoint_sign_is_containment_proof": False,
            "all_success_controls_supply_negative_validation": False,
            "general_selector_claim": False,
            "whole_configuration_claim": False,
            "novelty_claim": False,
            "independent_mathematical_validation": False,
        },
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
    print(json.dumps(result["outcomes"], indent=2))
    print(json.dumps(result["counts"], indent=2))
    print("WROTE: tie midpoint discriminator" if args.write else "PASS: tie midpoint discriminator reproduced read-only")


if __name__ == "__main__":
    main()
