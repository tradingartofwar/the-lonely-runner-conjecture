#!/usr/bin/env python3
"""Independent exact verification for the frozen tie-midpoint study.

This verifier deliberately does not import primary.py.  It reconstructs strict
blocker intersections from their complete rational threshold-event schedules,
then derives midpoint scores and containment answers from those schedules.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.json"
PRIMARY_RESULTS = HERE / "results.json"
PRIMARY_SCRIPT = HERE / "primary.py"
OUTPUT = HERE / "verification.json"
REPORT = HERE / "verification.md"

PINNED = {
    "protocol.json": (PROTOCOL, "e62d116b764aa0869788dffb36785935d08e3de1ddb38d3e0ca11ca23ba3f2e3"),
    "selector_transfer_protocol": (
        ROOT / "reviews/2026-09-28-selector-transfer-audit/protocol.json",
        "ccfdb403abef15f9c2cd9e08ac086232f4842b450f48308ba5a5992f8c3f9c17",
    ),
    "selector_transfer_results": (
        ROOT / "reviews/2026-09-28-selector-transfer-audit/results.json",
        "bc6c3c87803057632e80d85f74af40a6a7f83bebce27b19f0dc3fce9e4e11615",
    ),
    "selector_transfer_note": (
        ROOT / "notes/SELECTOR_TRANSFER_AUDIT_2026_09_28.md",
        "772d120dc40fc37e15d9d88822fa1d46b220f825992de2c6cbde15dfbe377e4f",
    ),
    "floor_sum_results": (
        ROOT / "reviews/2026-09-28-floor-sum-component-count/results.json",
        "f50852b82c52fff7dedac640dd82ca32be048db53a6337402dd453e7fbffce8c",
    ),
    "one_query_results": (
        ROOT / "reviews/2026-09-28-one-containment-selector/results.json",
        "7f84d1dc9b561045648969bd4d1491df66abb7fd53e1908259fdfd42e1f34cb5",
    ),
}

ACTIVE_IDS = (
    "squares:1,2,5:12",
    "squares:1,2,5:39",
    "fibonacci:1,2,4:1",
    "fibonacci:1,2,4:11",
    "fibonacci:1,2,4:22",
    "fibonacci:1,2,4:32",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def F(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(str(value))


def S(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def floor_fraction(x: Fraction) -> int:
    return x.numerator // x.denominator


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


def distance_to_integer(x: Fraction) -> Fraction:
    q = floor_fraction(x)
    f = x - q
    return min(f, 1 - f)


def blocks(v: int, t: Fraction) -> bool:
    return distance_to_integer(v * t) < Fraction(1, 8)


def thresholds(v: int, left: Fraction, right: Fraction) -> list[Fraction]:
    """All exact distance=1/8 thresholds in the closed analysis window.

    The archived event ledger charges a threshold that coincides with a window
    endpoint.  Event-set deduplication still leaves one geometric endpoint, and
    strict blocker semantics still make the equality point safe.
    """
    lo = floor_fraction(v * left) - 2
    hi = ceil_fraction(v * right) + 2
    out = set()
    for lap in range(lo, hi + 1):
        for sign in (-1, 1):
            t = Fraction(8 * lap + sign, 8 * v)
            if left <= t <= right:
                out.add(t)
    return sorted(out)


def threshold_schedule(speeds: Iterable[int], left: Fraction, right: Fraction) -> dict[str, Any]:
    per_speed = {v: thresholds(v, left, right) for v in speeds}
    raw = sum(len(values) for values in per_speed.values())
    events = sorted({left, right, *(t for values in per_speed.values() for t in values)})
    return {
        "per_speed": per_speed,
        "raw_in_window_thresholds": raw,
        "events": events,
        "unique_threshold_events_including_window_endpoints": len(events),
        "open_cells": len(events) - 1,
    }


def component_rows(pair: tuple[int, int], left: Fraction, right: Fraction) -> list[dict[str, Any]]:
    schedule = threshold_schedule(pair, left, right)
    rows: list[dict[str, Any]] = []
    for lo, hi in zip(schedule["events"], schedule["events"][1:]):
        mid = (lo + hi) / 2
        if all(blocks(v, mid) for v in pair):
            laps = [floor_fraction(v * mid + Fraction(1, 2)) for v in pair]
            rows.append(
                {
                    "interval": [S(lo), S(hi)],
                    "left_included": lo == left and all(blocks(v, lo) for v in pair),
                    "right_included": hi == right and all(blocks(v, hi) for v in pair),
                    "laps": laps,
                    "midpoint": S(mid),
                }
            )
    return rows


def midpoint_pair_row(
    pair: tuple[int, int], complement: tuple[int, int], left: Fraction, right: Fraction
) -> dict[str, Any]:
    components = component_rows(pair, left, right)
    phase_rows: list[dict[str, Any]] = []
    margins: list[Fraction] = []
    for component in components:
        midpoint = F(component["midpoint"])
        values = []
        for v in complement:
            distance = distance_to_integer(v * midpoint)
            margin = distance - Fraction(1, 8)
            margins.append(margin)
            values.append({"speed": v, "distance": S(distance), "signed_margin": S(margin)})
        phase_rows.append({"midpoint": S(midpoint), "complement_phases": values})
    if not margins:
        raise AssertionError(f"minimum-count pair {pair} has no reconstructed component")
    return {
        "base_pair": list(pair),
        "complement": list(complement),
        "components": components,
        "component_count": len(components),
        "midpoint_rows": phase_rows,
        "pair_score": S(min(margins)),
    }


def containment(
    pair: tuple[int, int], complement: tuple[int, int], speeds: tuple[int, ...], left: Fraction, right: Fraction
) -> dict[str, Any]:
    schedule = threshold_schedule(speeds, left, right)
    violations: list[dict[str, Any]] = []
    # Open cells establish every positive-interval failure.
    for lo, hi in zip(schedule["events"], schedule["events"][1:]):
        mid = (lo + hi) / 2
        if all(blocks(v, mid) for v in pair):
            bad = [v for v in complement if blocks(v, mid)]
            if bad:
                violations.append(
                    {"kind": "open_cell", "interval": [S(lo), S(hi)], "witness": S(mid), "blocking": bad}
                )
    # Event checks catch a possible included endpoint or simultaneous-threshold singleton.
    for t in schedule["events"]:
        if all(blocks(v, t) for v in pair):
            bad = [v for v in complement if blocks(v, t)]
            if bad:
                violations.append({"kind": "event", "time": S(t), "blocking": bad})
    return {
        "base_pair": list(pair),
        "complement": list(complement),
        "containment_holds": not violations,
        "violations": violations,
        "event_ledger": {
            "raw_in_window_thresholds": schedule["raw_in_window_thresholds"],
            "unique_threshold_events_including_window_endpoints": schedule[
                "unique_threshold_events_including_window_endpoints"
            ],
            "open_cells": schedule["open_cells"],
            "event_points_checked": len(schedule["events"]),
        },
    }


def row_key(row: dict[str, Any]) -> tuple[int, int]:
    return tuple(row["base_pair"])


def derive() -> dict[str, Any]:
    checked_hashes = {}
    for label, (path, expected) in PINNED.items():
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(f"pinned hash mismatch for {label}: {actual} != {expected}")
        checked_hashes[label] = actual

    source = json.loads(PINNED["selector_transfer_results"][0].read_text())
    protocol = json.loads(PROTOCOL.read_text())
    expected_development = {"squares:1,2,5:12", "squares:1,2,5:39"}
    expected_controls = {
        "fibonacci:1,2,4:1",
        "fibonacci:1,2,4:11",
        "fibonacci:1,2,4:22",
        "fibonacci:1,2,4:32",
    }
    if set(protocol["frozen_domain"]["development_records"]) != expected_development:
        raise AssertionError("literal development scope changed")
    if set(protocol["frozen_domain"]["archival_control_records"]) != expected_controls:
        raise AssertionError("literal archival-control scope changed")
    if protocol["frozen_domain"]["named_control"] != "strict_16":
        raise AssertionError("named control changed")
    if protocol["frozen_domain"]["dispatch_controls"] != ["doubling_112", "tight_13"]:
        raise AssertionError("dispatch controls changed")

    records = []
    total_tied_pairs = total_components = total_midpoints = total_phase_reductions = 0
    total_score_comparisons = total_lex_tiebreaks = 0
    selected_logical_queries = 0
    oracle_queries = 0
    selected_thresholds = selected_cells = oracle_thresholds = oracle_cells = 0

    def verify_tie_record(record_id: str, data: dict[str, Any], role: str) -> dict[str, Any]:
        nonlocal total_tied_pairs, total_components, total_midpoints, total_phase_reductions
        nonlocal total_score_comparisons, total_lex_tiebreaks, selected_logical_queries, oracle_queries
        nonlocal selected_thresholds, selected_cells, oracle_thresholds, oracle_cells

        speeds = tuple(data["speeds"])
        left, right = map(F, data["window"])
        if F(data["pair_only_minimum"]) > 0:
            raise AssertionError(f"active tie record unexpectedly pair-only: {record_id}")
        eligible = [row for row in data["pair_rows"] if row["eligible"]]
        if not eligible:
            raise AssertionError(f"active tie record lacks eligible rows: {record_id}")
        minimum = min(row["component_count"] for row in eligible)
        tied = [row for row in eligible if row["component_count"] == minimum]
        if len(tied) < 2:
            raise AssertionError(f"active tie record lacks minimum-count tie: {record_id}")
        scored = []
        for source_row in tied:
            pair = tuple(source_row["base_pair"])
            complement = tuple(source_row["complement"])
            rebuilt = midpoint_pair_row(pair, complement, left, right)
            if rebuilt["component_count"] != source_row["component_count"]:
                raise AssertionError(f"component-count mismatch: {record_id} {pair}")
            scored.append(rebuilt)
        total_tied_pairs += len(scored)
        total_components += sum(row["component_count"] for row in scored)
        total_midpoints += sum(row["component_count"] for row in scored)
        total_phase_reductions += 2 * sum(row["component_count"] for row in scored)
        total_score_comparisons += len(scored) - 1
        best_score = max(F(row["pair_score"]) for row in scored)
        best_rows = [row for row in scored if F(row["pair_score"]) == best_score]
        if len(best_rows) > 1:
            total_lex_tiebreaks += 1
        selected = min(best_rows, key=row_key)
        lex_choice = min(scored, key=row_key)
        selected_containment = containment(
            tuple(selected["base_pair"]), tuple(selected["complement"]), speeds, left, right
        )
        selected_logical_queries += 1
        selected_thresholds += selected_containment["event_ledger"]["raw_in_window_thresholds"]
        selected_cells += selected_containment["event_ledger"]["open_cells"]
        oracle = []
        archived_oracle = {tuple(row["base_pair"]): row for row in data["postselection_oracle"]["queries"]}
        for score_row in scored:
            result = containment(
                tuple(score_row["base_pair"]), tuple(score_row["complement"]), speeds, left, right
            )
            archive = archived_oracle[tuple(score_row["base_pair"])]
            if result["containment_holds"] != archive["containment_holds"]:
                raise AssertionError(f"archive containment mismatch: {record_id} {score_row['base_pair']}")
            for field in (
                "raw_in_window_thresholds",
                "unique_threshold_events_including_window_endpoints",
                "open_cells",
            ):
                if result["event_ledger"][field] != archive["event_ledger"][field]:
                    raise AssertionError(f"archive event-ledger mismatch: {record_id} {score_row['base_pair']} {field}")
            oracle.append(result)
            oracle_queries += 1
            oracle_thresholds += result["event_ledger"]["raw_in_window_thresholds"]
            oracle_cells += result["event_ledger"]["open_cells"]
        return {
            "id": record_id,
            "role": role,
            "speeds": list(speeds),
            "window": data["window"],
            "minimum_component_count": minimum,
            "tied_pair_scores": scored,
            "candidate_choice": selected["base_pair"],
            "candidate_score": selected["pair_score"],
            "lexicographic_comparator_choice": lex_choice["base_pair"],
            "selected_containment": selected_containment,
            "all_tied_pair_oracle": oracle,
        }

    for record_id in ACTIVE_IDS:
        role = "development" if record_id in expected_development else "archival_control"
        records.append(verify_tie_record(record_id, source["cases"][record_id], role))

    # strict_16 is represented under controls rather than cases, but obeys the same frozen tie rule.
    strict = source["controls"]["strict_16"]
    strict_proxy = {
        **strict,
        "pair_rows": strict["pair_rows"],
        "postselection_oracle": {
            "queries": [
                containment(
                    tuple(row["base_pair"]),
                    tuple(row["complement"]),
                    tuple(strict["speeds"]),
                    F(strict["window"][0]),
                    F(strict["window"][1]),
                )
                for row in strict["pair_rows"]
                if row["eligible"] and row["component_count"] == 1
            ]
        },
    }
    # Adapt independently rebuilt rows to the archived-oracle fields consumed above.
    strict_proxy["postselection_oracle"]["queries"] = [
        {
            "base_pair": row["base_pair"],
            "containment_holds": row["containment_holds"],
            "event_ledger": {k: row["event_ledger"][k] for k in (
                "raw_in_window_thresholds",
                "unique_threshold_events_including_window_endpoints",
                "open_cells",
            )},
        }
        for row in strict_proxy["postselection_oracle"]["queries"]
    ]
    records.append(verify_tie_record("strict_16", strict_proxy, "named_control"))

    doubling = source["controls"]["doubling_112"]
    if F(doubling["pair_only_minimum"]) <= 0:
        raise AssertionError("doubling_112 did not dispatch through pair-only exit")
    tight = source["controls"]["tight_13"]
    tight_eligible = [row for row in tight["pair_rows"] if row["eligible"]]
    if tight_eligible:
        raise AssertionError("tight_13 unexpectedly has an eligible positive-slack pair")
    isolated = tight["isolated_equality_endpoint"]
    if not (
        isolated["time"] == "3/8"
        and isolated["valid"]
        and isolated["isolated"]
        and not isolated["positive_duration"]
    ):
        raise AssertionError("tight_13 isolated-equality dispatch changed")

    reflection_pairs = [
        ("squares:1,2,5:12", "squares:1,2,5:39"),
        ("fibonacci:1,2,4:1", "fibonacci:1,2,4:32"),
        ("fibonacci:1,2,4:11", "fibonacci:1,2,4:22"),
    ]
    by_id = {row["id"]: row for row in records}
    reflection_checks = []
    for first, second in reflection_pairs:
        a, b = by_id[first], by_id[second]
        checks = {
            "candidate_choice_equal": a["candidate_choice"] == b["candidate_choice"],
            "candidate_score_equal": a["candidate_score"] == b["candidate_score"],
            "oracle_outcomes_equal": [q["containment_holds"] for q in a["all_tied_pair_oracle"]]
            == [q["containment_holds"] for q in b["all_tied_pair_oracle"]],
        }
        if not all(checks.values()):
            raise AssertionError(f"reflection mismatch: {first}, {second}: {checks}")
        reflection_checks.append({"records": [first, second], **checks})

    # Classification is deliberately postselection: midpoint score is not a proof.
    sign_rows = []
    false_positive = false_negative = inversions = 0
    for record in records:
        score_map = {tuple(r["base_pair"]): F(r["pair_score"]) for r in record["tied_pair_scores"]}
        outcomes = {tuple(q["base_pair"]): q["containment_holds"] for q in record["all_tied_pair_oracle"]}
        for pair, score in score_map.items():
            holds = outcomes[pair]
            predicts = score >= 0
            false_positive += int(predicts and not holds)
            false_negative += int((not predicts) and holds)
            sign_rows.append({
                "record": record["id"], "base_pair": list(pair), "score": S(score),
                "score_nonnegative": predicts, "containment_holds": holds,
            })
        pairs = sorted(score_map)
        for p in pairs:
            for q in pairs:
                if score_map[p] > score_map[q] and (not outcomes[p]) and outcomes[q]:
                    inversions += 1

    cost = {
        "candidate_selection": {
            "active_tie_records": len(records),
            "tied_pairs": total_tied_pairs,
            "reconstructed_components": total_components,
            "midpoint_samples": total_midpoints,
            "complement_phase_reductions": total_phase_reductions,
            "distance_computations": total_phase_reductions,
            "score_order_comparisons": total_score_comparisons,
            "physical_lexicographic_tie_breaks": total_lex_tiebreaks,
        },
        "selected_queries": {
            "logical_compound_containment_queries": selected_logical_queries,
            "raw_in_window_thresholds": selected_thresholds,
            "open_cells": selected_cells,
        },
        "postselection_oracle": {
            "logical_compound_containment_queries": oracle_queries,
            "raw_in_window_thresholds": oracle_thresholds,
            "open_cells": oracle_cells,
        },
    }

    return {
        "status": "PASS",
        "method": "independent exact threshold-event reconstruction; no import of primary.py",
        "arithmetic": "fractions.Fraction only",
        "checked_source_hashes": checked_hashes,
        "literal_scope": {
            "development_records": sorted(expected_development),
            "archival_control_records": sorted(expected_controls),
            "named_control": "strict_16",
            "dispatch_controls": ["doubling_112", "tight_13"],
            "active_label_count": len(records),
            "active_reflection_mechanisms": 4,
        },
        "records": records,
        "reflection_checks": reflection_checks,
        "dispatch_checks": {
            "doubling_112": {
                "outcome": "pair_only_exit_before_scoring",
                "pair_only_minimum": doubling["pair_only_minimum"],
                "score_pairs": 0,
                "duration_queries": 0,
            },
            "tight_13": {
                "outcome": "no_eligible_pair_no_duration_query",
                "score_pairs": 0,
                "duration_queries": 0,
                "isolated_equality_time": isolated["time"],
                "isolated_equality_valid": True,
                "positive_duration": False,
            },
        },
        "postselection_score_audit": {
            "rows": sign_rows,
            "false_positives": false_positive,
            "false_negatives": false_negative,
            "score_order_inversions": inversions,
        },
        "cost_ledger": cost,
    }


def recursive_compare(expected: Any, actual: Any, path: str = "$") -> list[str]:
    """Compare all expected fields while allowing primary-only explanatory fields."""
    differences: list[str] = []
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected object, got {type(actual).__name__}"]
        for key, value in expected.items():
            if key not in actual:
                differences.append(f"{path}.{key}: missing")
            else:
                differences.extend(recursive_compare(value, actual[key], f"{path}.{key}"))
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            differences.append(f"{path}: list shape {len(expected)} != {len(actual) if isinstance(actual, list) else 'non-list'}")
        elif isinstance(actual, list):
            for i, (e, a) in enumerate(zip(expected, actual)):
                differences.extend(recursive_compare(e, a, f"{path}[{i}]"))
    elif expected != actual:
        differences.append(f"{path}: {expected!r} != {actual!r}")
    return differences


def primary_comparison(verification: dict[str, Any]) -> dict[str, Any]:
    if not PRIMARY_RESULTS.exists():
        return {"status": "PENDING", "reason": "results.json not present when verifier ran"}
    primary = json.loads(PRIMARY_RESULTS.read_text())
    expected = {
        "records": [
            {
                "id": row["id"],
                "candidate_choice": row["candidate_choice"],
                "candidate_score": row["candidate_score"],
                "lexicographic_comparator_choice": row["lexicographic_comparator_choice"],
                "tied_pair_scores": [
                    {
                        "base_pair": score["base_pair"],
                        "complement": score["complement"],
                        "component_count": score["component_count"],
                        "pair_score": score["pair_score"],
                        "components_and_samples": [
                            {
                                "interval": component["interval"],
                                "laps": component["laps"],
                                "left_included": component["left_included"],
                                "right_included": component["right_included"],
                                "midpoint": component["midpoint"],
                                "complement_evaluations": [
                                    {
                                        "speed": phase["speed"],
                                        "distance_to_integer": phase["distance"],
                                        "signed_safety_margin": phase["signed_margin"],
                                    }
                                    for phase in score["midpoint_rows"][index]["complement_phases"]
                                ],
                            }
                            for index, component in enumerate(score["components"])
                        ],
                    }
                    for score in row["tied_pair_scores"]
                ],
                "selected_containment_holds": row["selected_containment"]["containment_holds"],
                "selected_event_ledger": {
                    key: row["selected_containment"]["event_ledger"][key]
                    for key in (
                        "raw_in_window_thresholds",
                        "unique_threshold_events_including_window_endpoints",
                        "open_cells",
                    )
                },
                "all_tied_pair_containments": [
                    {
                        "base_pair": q["base_pair"],
                        "containment_holds": q["containment_holds"],
                        "event_ledger": {
                            key: q["event_ledger"][key]
                            for key in (
                                "raw_in_window_thresholds",
                                "unique_threshold_events_including_window_endpoints",
                                "open_cells",
                            )
                        },
                    }
                    for q in row["all_tied_pair_oracle"]
                ],
            }
            for row in verification["records"]
        ],
        "dispatch_checks": {
            "doubling_112": {
                "pair_only_minimum": verification["dispatch_checks"]["doubling_112"]["pair_only_minimum"],
                "scored_tied_pairs": 0,
                "query_issued": False,
            },
            "tight_13": {
                "scored_tied_pairs": 0,
                "query_issued": False,
                "isolated_equality_time": "3/8",
            },
        },
        "cost_ledger": {
            "candidate": {
                "tied_pairs": verification["cost_ledger"]["candidate_selection"]["tied_pairs"],
                "reconstructed_positive_components": verification["cost_ledger"]["candidate_selection"][
                    "reconstructed_components"
                ],
                "midpoint_samples": verification["cost_ledger"]["candidate_selection"]["midpoint_samples"],
                "complement_phase_reductions": verification["cost_ledger"]["candidate_selection"][
                    "complement_phase_reductions"
                ],
                "distance_computations": verification["cost_ledger"]["candidate_selection"][
                    "distance_computations"
                ],
                "pair_score_comparisons": verification["cost_ledger"]["candidate_selection"][
                    "score_order_comparisons"
                ],
            },
            "selected": {
                "logical_queries": verification["cost_ledger"]["selected_queries"][
                    "logical_compound_containment_queries"
                ],
                "raw_in_window_thresholds": verification["cost_ledger"]["selected_queries"][
                    "raw_in_window_thresholds"
                ],
                "open_cells": verification["cost_ledger"]["selected_queries"]["open_cells"],
            },
            "oracle": {
                "logical_queries": verification["cost_ledger"]["postselection_oracle"][
                    "logical_compound_containment_queries"
                ],
                "raw_in_window_thresholds": verification["cost_ledger"]["postselection_oracle"][
                    "raw_in_window_thresholds"
                ],
                "open_cells": verification["cost_ledger"]["postselection_oracle"]["open_cells"],
            },
        },
        "outcomes": {
            "false_positives": verification["postselection_score_audit"]["false_positives"],
            "false_negatives": verification["postselection_score_audit"]["false_negatives"],
            "score_order_inversions": verification["postselection_score_audit"]["score_order_inversions"],
        },
    }

    def primary_record(record_id: str) -> dict[str, Any]:
        row = primary["controls"][record_id] if record_id == "strict_16" else primary["cases"][record_id]
        return {
            "id": row["id"],
            "candidate_choice": row["candidate_selected_pair"],
            "candidate_score": row["selected_result"]["selected_pair_score"],
            "lexicographic_comparator_choice": row["inherited_lexicographic_pair"],
            "tied_pair_scores": [
                {
                    "base_pair": score["base_pair"],
                    "complement": score["complement"],
                    "component_count": score["component_count"],
                    "pair_score": score["pair_score"],
                    "components_and_samples": [
                        {
                            "interval": component["interval"],
                            "laps": component["laps"],
                            "left_included": component["left_included"],
                            "right_included": component["right_included"],
                            "midpoint": component["midpoint"],
                            "complement_evaluations": [
                                {
                                    "speed": phase["speed"],
                                    "distance_to_integer": phase["distance_to_integer"],
                                    "signed_safety_margin": phase["signed_safety_margin"],
                                }
                                for phase in component["complement_evaluations"]
                            ],
                        }
                        for component in score["components_and_samples"]
                    ],
                }
                for score in row["scored_tied_pairs"]
            ],
            "selected_containment_holds": row["selected_query"]["containment_holds"],
            "selected_event_ledger": row["selected_query"]["event_ledger"],
            "all_tied_pair_containments": [
                {
                    "base_pair": query["base_pair"],
                    "containment_holds": query["containment_holds"],
                    "event_ledger": query["event_ledger"],
                }
                for query in row["postselection_tied_pair_oracle"]["queries"]
            ],
        }

    actual = {
        "records": [primary_record(row["id"]) for row in verification["records"]],
        "dispatch_checks": {
            "doubling_112": {
                "pair_only_minimum": primary["controls"]["doubling_112"]["pair_only_minimum"],
                "scored_tied_pairs": len(primary["controls"]["doubling_112"]["scored_tied_pairs"]),
                "query_issued": primary["controls"]["doubling_112"]["selected_result"]["query_issued"],
            },
            "tight_13": {
                "scored_tied_pairs": len(primary["controls"]["tight_13"]["scored_tied_pairs"]),
                "query_issued": primary["controls"]["tight_13"]["selected_result"]["query_issued"],
                "isolated_equality_time": primary["controls"]["tight_13"]["isolated_equality_endpoint"]["time"],
            },
        },
        "cost_ledger": {
            "candidate": {
                "tied_pairs": primary["aggregate_cost_ledgers"]["candidate_preselection_midpoint_scores"][
                    "tied_pairs"
                ],
                "reconstructed_positive_components": primary["aggregate_cost_ledgers"][
                    "candidate_preselection_midpoint_scores"
                ]["reconstructed_positive_components"],
                **{
                    key: primary["aggregate_cost_ledgers"]["candidate_preselection_midpoint_scores"][
                        "prescribed_midpoint_operations"
                    ][key]
                    for key in ("midpoint_samples", "complement_phase_reductions", "distance_computations")
                },
                "pair_score_comparisons": primary["aggregate_cost_ledgers"][
                    "candidate_preselection_midpoint_scores"
                ]["pair_choice_operations"]["pair_score_comparisons"],
            },
            "selected": {
                "logical_queries": primary["counts"]["selected_logical_queries"],
                "raw_in_window_thresholds": primary["aggregate_cost_ledgers"]["selected_one_query"][
                    "raw_in_window_thresholds"
                ],
                "open_cells": primary["aggregate_cost_ledgers"]["selected_one_query"]["open_cells"],
            },
            "oracle": {
                "logical_queries": primary["counts"]["tied_pair_label_queries_in_oracle"],
                "raw_in_window_thresholds": primary["aggregate_cost_ledgers"][
                    "postselection_all_tied_pair_oracle_charged_separately"
                ]["raw_in_window_thresholds"],
                "open_cells": primary["aggregate_cost_ledgers"][
                    "postselection_all_tied_pair_oracle_charged_separately"
                ]["open_cells"],
            },
        },
        "outcomes": {
            "false_positives": primary["outcomes"]["midpoint_sign_prediction_counts"].get("false_positive", 0),
            "false_negatives": primary["outcomes"]["midpoint_sign_prediction_counts"].get("false_negative", 0),
            "score_order_inversions": primary["outcomes"]["score_order_inversion_labels"],
        },
    }
    differences = recursive_compare(expected, actual)
    return {
        "status": "PASS" if not differences else "FAIL",
        "primary_py_sha256": sha256(PRIMARY_SCRIPT),
        "primary_results_sha256": sha256(PRIMARY_RESULTS),
        "compared_fields": count_scalars(expected),
        "differences": differences,
    }


def count_scalars(value: Any) -> int:
    if isinstance(value, dict):
        return sum(count_scalars(v) for v in value.values())
    if isinstance(value, list):
        return sum(count_scalars(v) for v in value)
    return 1


def render_report(result: dict[str, Any]) -> str:
    audit = result["postselection_score_audit"]
    cost = result["cost_ledger"]
    comparison = result["primary_comparison"]
    lines = [
        "# Independent tie-midpoint verification",
        "",
        f"**Status:** {result['status']}",
        "",
        "This verifier independently reconstructs every blocker threshold event with exact rational arithmetic. "
        "It does not import `primary.py` or any primary helper.",
        "",
        "## Scope",
        "",
        f"- Active labels: {result['literal_scope']['active_label_count']} (four reflection mechanisms)",
        f"- Tied pairs: {cost['candidate_selection']['tied_pairs']}",
        f"- Reconstructed positive components / midpoint samples: {cost['candidate_selection']['reconstructed_components']}",
        f"- Complement phase reductions: {cost['candidate_selection']['complement_phase_reductions']}",
        f"- Selected compound queries: {cost['selected_queries']['logical_compound_containment_queries']}",
        f"- Postselection oracle queries: {cost['postselection_oracle']['logical_compound_containment_queries']}",
        f"- Score-sign false positives / false negatives: {audit['false_positives']} / {audit['false_negatives']}",
        f"- Score-order inversions: {audit['score_order_inversions']}",
        "",
        "## Dispatch and semantics",
        "",
        "- `doubling_112` exits on its inherited positive pair-only minimum before scoring.",
        "- `tight_13` has no positive-slack eligible pair, issues no duration query, and retains only the valid isolated equality at `3/8`.",
        "- Strict blocker semantics use distance `< 1/8`; equality is safe. Open cells and every exact event point were checked.",
        "- Reflected labels agree on choices, scores, and containment outcomes; they are not counted as independent validation.",
        "",
        "## Primary comparison",
        "",
        f"- Status: {comparison['status']}",
    ]
    if "compared_fields" in comparison:
        lines.append(f"- Compared scalar fields: {comparison['compared_fields']}")
    if comparison.get("differences"):
        lines += ["- Differences:"] + [f"  - {item}" for item in comparison["differences"]]
    if comparison.get("reason"):
        lines.append(f"- Note: {comparison['reason']}")
    lines += [
        "",
        "## Limits",
        "",
        "This is an independently structured internal exact check, not independent human mathematical validation. "
        "The finite midpoint score is a selector diagnostic, not a containment proof.",
        "",
    ]
    return "\n".join(lines)


def assemble() -> dict[str, Any]:
    result = derive()
    result["primary_comparison"] = primary_comparison(result)
    if result["primary_comparison"]["status"] != "PASS":
        result["status"] = "FAIL"
    result["verification_scalar_fields"] = count_scalars(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = assemble()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    report = render_report(result)
    if args.write:
        OUTPUT.write_text(encoded)
        REPORT.write_text(report)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
        print(f"wrote {REPORT.relative_to(ROOT)}")
    else:
        if not OUTPUT.exists() or OUTPUT.read_text() != encoded:
            raise SystemExit("verification.json is stale; run --write")
        if not REPORT.exists() or REPORT.read_text() != report:
            raise SystemExit("verification.md is stale; run --write")
        print("independent verification artifacts are current")
    if result["status"] != "PASS":
        raise SystemExit("verification failed")


if __name__ == "__main__":
    main()
