#!/usr/bin/env python3
"""Independent exact verifier for the frozen Lipschitz-margin study.

This file deliberately does not import primary.py.  It reconstructs the base
pair components by a complete rational threshold-event sweep, computes the
Lipschitz lower margins, and checks those lower bounds against a separate
closed-interval minimum-distance calculation.  Full containment schedules are
loaded and reconstructed only after every score, choice, and certificate
decision is immutable.
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
PRIMARY_SCRIPT = HERE / "primary.py"
PRIMARY_RESULTS = HERE / "results.json"
OUTPUT = HERE / "verification.json"
REPORT = HERE / "verification.md"

PROTOCOL_SHA256 = "3903410dec2f61deda37c9fe7d03fb6ae24034fc80c78f8426faa9e81f4cae0c"
ACTIVE_IDS = (
    "squares:1,2,5:12",
    "squares:1,2,5:39",
    "fibonacci:1,2,4:1",
    "fibonacci:1,2,4:11",
    "fibonacci:1,2,4:22",
    "fibonacci:1,2,4:32",
)
REFLECTION_PAIRS = (
    ("squares:1,2,5:12", "squares:1,2,5:39"),
    ("fibonacci:1,2,4:1", "fibonacci:1,2,4:32"),
    ("fibonacci:1,2,4:11", "fibonacci:1,2,4:22"),
)
THRESHOLD = Fraction(1, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def F(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(str(value))


def S(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def floor_q(value: Fraction) -> int:
    return value.numerator // value.denominator


def ceil_q(value: Fraction) -> int:
    return -floor_q(-value)


def nearest_integer_distance(value: Fraction) -> Fraction:
    fractional = value - floor_q(value)
    return min(fractional, 1 - fractional)


def is_strict_blocker(speed: int, time: Fraction) -> bool:
    return nearest_integer_distance(speed * time) < THRESHOLD


def exact_thresholds(speed: int, left: Fraction, right: Fraction) -> tuple[list[Fraction], int]:
    """Return every distance=1/8 event and the number of lap rows examined."""
    first_lap = floor_q(speed * left) - 1
    last_lap = ceil_q(speed * right) + 1
    found: set[Fraction] = set()
    rows = 0
    for lap in range(first_lap, last_lap + 1):
        rows += 1
        low = Fraction(8 * lap - 1, 8 * speed)
        high = Fraction(8 * lap + 1, 8 * speed)
        if left <= low <= right:
            found.add(low)
        if left <= high <= right:
            found.add(high)
    return sorted(found), rows


def event_partition(speeds: Iterable[int], left: Fraction, right: Fraction) -> dict[str, Any]:
    per_speed: dict[int, list[Fraction]] = {}
    lap_rows = 0
    for speed in speeds:
        points, rows = exact_thresholds(speed, left, right)
        per_speed[speed] = points
        lap_rows += rows
    events = sorted({left, right, *(point for values in per_speed.values() for point in values)})
    return {
        "per_speed": per_speed,
        "events": events,
        "raw_thresholds": sum(len(values) for values in per_speed.values()),
        "unique_events": len(events),
        "open_cells": len(events) - 1,
        "lap_rows_examined": lap_rows,
    }


def reconstruct_components(pair: tuple[int, int], left: Fraction, right: Fraction) -> dict[str, Any]:
    """Reconstruct positive components using only exact threshold cells."""
    partition = event_partition(pair, left, right)
    components: list[dict[str, Any]] = []
    state_tests = 0
    for low, high in zip(partition["events"], partition["events"][1:]):
        midpoint = (low + high) / 2
        state = []
        for speed in pair:
            state_tests += 1
            state.append(is_strict_blocker(speed, midpoint))
        if all(state):
            laps = [floor_q(speed * midpoint + Fraction(1, 2)) for speed in pair]
            components.append(
                {
                    "interval": [S(low), S(high)],
                    "left_included": all(is_strict_blocker(speed, low) for speed in pair),
                    "right_included": all(is_strict_blocker(speed, high) for speed in pair),
                    "laps": laps,
                    "midpoint": S(midpoint),
                    "width": S(high - low),
                }
            )
    return {
        "components": components,
        "ledger": {
            "base_speeds": len(pair),
            "lap_rows_examined": partition["lap_rows_examined"],
            "raw_thresholds": partition["raw_thresholds"],
            "unique_events_including_window_endpoints": partition["unique_events"],
            "open_cells": partition["open_cells"],
            "blocking_state_tests": state_tests,
            "positive_components": len(components),
        },
    }


def direct_minimum_distance(speed: int, left: Fraction, right: Fraction) -> Fraction:
    """Exact minimum of ||speed*t|| over a closed interval, without Lipschitz."""
    scaled_left = speed * left
    scaled_right = speed * right
    if ceil_q(scaled_left) <= floor_q(scaled_right):
        return Fraction(0)
    return min(nearest_integer_distance(scaled_left), nearest_integer_distance(scaled_right))


def score_pair(
    pair: tuple[int, int], complement: tuple[int, int], left: Fraction, right: Fraction
) -> dict[str, Any]:
    reconstruction = reconstruct_components(pair, left, right)
    components = reconstruction["components"]
    if not components:
        raise AssertionError(f"tied minimum pair {pair} has no positive component")
    evaluation_rows: list[dict[str, Any]] = []
    all_lower_margins: list[Fraction] = []
    lemma_defects: list[dict[str, Any]] = []
    for component_index, component in enumerate(components):
        low, high = map(F, component["interval"])
        midpoint = (low + high) / 2
        width = high - low
        half_width = width / 2
        complement_rows = []
        for speed in complement:
            center_distance = nearest_integer_distance(speed * midpoint)
            speed_radius = speed * half_width
            lower_margin = center_distance - THRESHOLD - speed_radius
            midpoint_signed_margin = center_distance - THRESHOLD
            actual_minimum_distance = direct_minimum_distance(speed, low, high)
            actual_minimum_margin = actual_minimum_distance - THRESHOLD
            lower_bound_gap = actual_minimum_margin - lower_margin
            lower_bound_holds = lower_bound_gap >= 0
            certificate_implication_holds = lower_margin < 0 or actual_minimum_margin >= 0
            if not lower_bound_holds or not certificate_implication_holds:
                lemma_defects.append(
                    {
                        "component_index": component_index,
                        "speed": speed,
                        "lower_bound_holds": lower_bound_holds,
                        "certificate_implication_holds": certificate_implication_holds,
                    }
                )
            all_lower_margins.append(lower_margin)
            complement_rows.append(
                {
                    "speed": speed,
                    "center_phase": S((speed * midpoint) - floor_q(speed * midpoint)),
                    "center_distance": S(center_distance),
                    "midpoint_signed_margin": S(midpoint_signed_margin),
                    "half_width": S(half_width),
                    "speed_times_width": S(speed * width),
                    "speed_times_half_width": S(speed_radius),
                    "lipschitz_lower_margin": S(lower_margin),
                    "direct_closed_interval_minimum_distance": S(actual_minimum_distance),
                    "direct_closed_interval_minimum_margin": S(actual_minimum_margin),
                    "direct_minus_lipschitz_margin": S(lower_bound_gap),
                    "lower_bound_holds": lower_bound_holds,
                    "nonnegative_implies_whole_component_safe": certificate_implication_holds,
                }
            )
        evaluation_rows.append(
            {
                "component_index": component_index,
                "interval": component["interval"],
                "laps": component["laps"],
                "left_included": component["left_included"],
                "right_included": component["right_included"],
                "midpoint": component["midpoint"],
                "width": component["width"],
                "complement_evaluations": complement_rows,
            }
        )
    pair_score = min(all_lower_margins)
    return {
        "base_pair": list(pair),
        "complement": list(complement),
        "component_count": len(components),
        "component_evaluations": evaluation_rows,
        "pair_score": S(pair_score),
        "score_nonnegative": pair_score >= 0,
        "lemma_defects": lemma_defects,
        "reconstruction_ledger": reconstruction["ledger"],
        "candidate_operation_ledger": {
            "component_width_computations": len(components),
            "half_width_divisions": len(components),
            "midpoint_samples": len(components),
            "complement_phase_reductions": len(all_lower_margins),
            "nearest_integer_distances": len(all_lower_margins),
            "speed_width_products": len(all_lower_margins),
            "threshold_subtractions": len(all_lower_margins),
            "radius_subtractions": len(all_lower_margins),
            "minimum_score_comparisons": len(all_lower_margins) - 1,
        },
    }


def postselection_containment(
    pair: tuple[int, int], complement: tuple[int, int], speeds: tuple[int, ...], left: Fraction, right: Fraction
) -> dict[str, Any]:
    """Separately charged exact containment sweep, never used for selection."""
    partition = event_partition(speeds, left, right)
    violations: list[dict[str, Any]] = []
    state_tests = 0
    for low, high in zip(partition["events"], partition["events"][1:]):
        midpoint = (low + high) / 2
        base_state = []
        for speed in pair:
            state_tests += 1
            base_state.append(is_strict_blocker(speed, midpoint))
        complement_blockers = []
        for speed in complement:
            state_tests += 1
            if is_strict_blocker(speed, midpoint):
                complement_blockers.append(speed)
        if all(base_state) and complement_blockers:
            violations.append(
                {
                    "kind": "open_cell",
                    "interval": [S(low), S(high)],
                    "witness": S(midpoint),
                    "blocking_complement_speeds": complement_blockers,
                }
            )
    for event in partition["events"]:
        base_state = []
        for speed in pair:
            state_tests += 1
            base_state.append(is_strict_blocker(speed, event))
        complement_blockers = []
        for speed in complement:
            state_tests += 1
            if is_strict_blocker(speed, event):
                complement_blockers.append(speed)
        if all(base_state) and complement_blockers:
            violations.append(
                {
                    "kind": "event_point",
                    "time": S(event),
                    "blocking_complement_speeds": complement_blockers,
                }
            )
    return {
        "base_pair": list(pair),
        "complement": list(complement),
        "containment_holds": not violations,
        "first_violation": violations[0] if violations else None,
        "violations": violations,
        "event_ledger": {
            "lap_rows_examined": partition["lap_rows_examined"],
            "raw_thresholds": partition["raw_thresholds"],
            "unique_events_including_window_endpoints": partition["unique_events"],
            "open_cells": partition["open_cells"],
            "event_points_checked": partition["unique_events"],
            "blocking_state_tests": state_tests,
        },
    }


def pair_key(row: dict[str, Any]) -> tuple[int, int]:
    return tuple(row["base_pair"])


def add_numeric_dict(target: dict[str, int], source: dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def freeze_source_projection(source: dict[str, Any]) -> dict[str, Any]:
    """Retain only protocol-authorized fields before candidate calculation."""
    records: dict[str, Any] = {}
    for record_id in ACTIVE_IDS:
        row = source["cases"][record_id]
        slack_by_pair = {
            tuple(scored["base_pair"]): scored["potential_slack"] for scored in row["scored_tied_pairs"]
        }
        records[record_id] = {
            "id": row["id"],
            "role": row["role"],
            "speeds": row["speeds"],
            "window": row["window"],
            "pair_only_minimum": row["pair_only_minimum"],
            "minimum_component_count": row["minimum_component_count"],
            "tied_minimum_pairs": row["tied_minimum_pairs"],
            "potential_slack_by_pair": {f"{a},{b}": slack for (a, b), slack in slack_by_pair.items()},
        }
    strict = source["controls"]["strict_16"]
    strict_slack = {
        tuple(scored["base_pair"]): scored["potential_slack"] for scored in strict["scored_tied_pairs"]
    }
    records["strict_16"] = {
        "id": "strict_16",
        "role": "named_control",
        "speeds": strict["speeds"],
        "window": strict["window"],
        "pair_only_minimum": strict["pair_only_minimum"],
        "minimum_component_count": strict["minimum_component_count"],
        "tied_minimum_pairs": strict["tied_minimum_pairs"],
        "potential_slack_by_pair": {f"{a},{b}": slack for (a, b), slack in strict_slack.items()},
    }
    for control_id in ("doubling_112", "tight_13"):
        control = source["controls"][control_id]
        records[control_id] = {
            "id": control_id,
            "role": control["role"],
            "speeds": control["speeds"],
            "window": control["window"],
            "pair_only_minimum": control["pair_only_minimum"],
            "minimum_component_count": control["minimum_component_count"],
            "tied_minimum_pairs": control["tied_minimum_pairs"],
            "dispatch": control["dispatch"],
            "isolated_equality_endpoint": control.get("isolated_equality_endpoint"),
        }
    return records


def archived_containment_map(source: dict[str, Any], record_id: str) -> dict[tuple[int, int], bool]:
    row = source["controls"][record_id] if record_id in source["controls"] else source["cases"][record_id]
    return {
        tuple(query["base_pair"]): bool(query["containment_holds"])
        for query in row["postselection_tied_pair_oracle"]["queries"]
    }


def flatten_scalars(value: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten JSON scalars for an explicit primary comparison ledger."""
    found: dict[str, Any] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            child = f"{prefix}.{key}" if prefix else key
            found.update(flatten_scalars(value[key], child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(flatten_scalars(item, f"{prefix}[{index}]"))
    else:
        found[prefix] = value
    return found


def semantic_primary_comparison(verification: dict[str, Any], primary: dict[str, Any]) -> dict[str, Any]:
    """Compare every shared mathematical field through an explicit projection."""
    independent: dict[str, Any] = {}
    primary_projection: dict[str, Any] = {}
    for record_id, row in verification["records"].items():
        primary_row = primary["cases"][record_id] if record_id in primary.get("cases", {}) else primary["controls"][record_id]
        independent[f"{record_id}.dispatch"] = row["dispatch"]
        primary_projection[f"{record_id}.dispatch"] = primary_row["dispatch"]
        independent[f"{record_id}.selected_pair"] = row.get("selected_pair")
        primary_projection[f"{record_id}.selected_pair"] = primary_row.get("candidate_selected_pair")
        independent[f"{record_id}.selected_score"] = row.get("selected_score")
        primary_projection[f"{record_id}.selected_score"] = primary_row.get("selected_result", {}).get(
            "selected_pair_score"
        )
        independent[f"{record_id}.selected_outcome"] = row["selected_outcome"]
        primary_projection[f"{record_id}.selected_outcome"] = primary_row["selected_result"]["outcome"]
        independent[f"{record_id}.certified_lower_bound"] = row.get("certified_lower_bound")
        primary_projection[f"{record_id}.certified_lower_bound"] = primary_row["selected_result"].get(
            "certified_lower_bound"
        )
        independent[f"{record_id}.isolated_equality_time"] = row.get("isolated_equality_time")
        primary_projection[f"{record_id}.isolated_equality_time"] = (
            primary_row.get("isolated_equality_endpoint") or {}
        ).get("time")
        primary_scored = {tuple(item["base_pair"]): item for item in primary_row.get("scored_tied_pairs", [])}
        for scored in row.get("scored_pairs", []):
            pair = tuple(scored["base_pair"])
            label = f"{record_id}.pair[{pair[0]},{pair[1]}]"
            counterpart = primary_scored[pair]
            independent[f"{label}.complement"] = scored["complement"]
            primary_projection[f"{label}.complement"] = counterpart["complement"]
            independent[f"{label}.component_count"] = scored["component_count"]
            primary_projection[f"{label}.component_count"] = counterpart["component_count"]
            independent[f"{label}.pair_score"] = scored["pair_score"]
            primary_projection[f"{label}.pair_score"] = counterpart["pair_score"]
            independent[f"{label}.score_nonnegative"] = scored["score_nonnegative"]
            primary_projection[f"{label}.score_nonnegative"] = counterpart["score_nonnegative"]
            independent_components = scored["component_evaluations"]
            primary_components = counterpart["components_and_bounds"]
            independent[f"{label}.component_rows"] = len(independent_components)
            primary_projection[f"{label}.component_rows"] = len(primary_components)
            for component_index, (left_row, right_row) in enumerate(
                zip(independent_components, primary_components, strict=True)
            ):
                component_label = f"{label}.component[{component_index}]"
                for field in ("interval", "laps", "left_included", "right_included", "midpoint", "width"):
                    independent[f"{component_label}.{field}"] = left_row[field]
                    primary_projection[f"{component_label}.{field}"] = right_row[field]
                primary_evaluations = {item["speed"]: item for item in right_row["complement_evaluations"]}
                for evaluation in left_row["complement_evaluations"]:
                    speed = evaluation["speed"]
                    primary_evaluation = primary_evaluations[speed]
                    evaluation_label = f"{component_label}.speed[{speed}]"
                    field_map = {
                        "center_phase": "phase_at_midpoint",
                        "center_distance": "distance_at_midpoint",
                        "midpoint_signed_margin": "midpoint_signed_margin",
                        "speed_times_width": "speed_width_product",
                        "half_width": "half_width",
                        "speed_times_half_width": "lipschitz_radius_bound",
                        "lipschitz_lower_margin": "lipschitz_lower_margin",
                    }
                    for independent_field, primary_field in field_map.items():
                        independent[f"{evaluation_label}.{independent_field}"] = evaluation[independent_field]
                        if primary_field == "half_width":
                            primary_value = S(F(right_row["width"]) / 2)
                        else:
                            primary_value = primary_evaluation[primary_field]
                        primary_projection[f"{evaluation_label}.{independent_field}"] = primary_value
        primary_oracle = {
            tuple(item["base_pair"]): item
            for item in primary_row.get("postselection_tied_pair_audit", {}).get("queries", [])
        }
        for audit in row.get("postselection_audits", []):
            pair = tuple(audit["base_pair"])
            label = f"{record_id}.pair[{pair[0]},{pair[1]}].postselection"
            independent[f"{label}.containment_holds"] = audit["containment_holds"]
            primary_projection[f"{label}.containment_holds"] = primary_oracle[pair]["containment_holds"]
            for field in ("raw_thresholds", "unique_events_including_window_endpoints", "open_cells"):
                primary_field = {
                    "raw_thresholds": "raw_in_window_thresholds",
                    "unique_events_including_window_endpoints": "unique_threshold_events_including_window_endpoints",
                    "open_cells": "open_cells",
                }[field]
                independent[f"{label}.{field}"] = audit["event_ledger"][field]
                primary_projection[f"{label}.{field}"] = primary_oracle[pair]["event_ledger"][primary_field]
    independent_flat = flatten_scalars(independent)
    primary_flat = flatten_scalars(primary_projection)
    if set(independent_flat) != set(primary_flat):
        raise AssertionError("internal primary-comparison key mismatch")
    disagreements = [
        {"field": key, "independent": independent_flat[key], "primary": primary_flat[key]}
        for key in sorted(independent_flat)
        if independent_flat[key] != primary_flat[key]
    ]
    return {
        "status": "PASS" if not disagreements else "FAIL",
        "compared_scalar_fields": len(independent_flat),
        "disagreements": disagreements,
    }


def derive() -> dict[str, Any]:
    if sha256(PROTOCOL) != PROTOCOL_SHA256:
        raise AssertionError("frozen protocol hash changed")
    protocol = json.loads(PROTOCOL.read_text())
    checked_hashes = {"protocol.json": PROTOCOL_SHA256}
    for label, relative in (
        ("midpoint_protocol", protocol["source_contract"]["midpoint_protocol"]),
        ("midpoint_results", protocol["source_contract"]["midpoint_results"]),
        ("midpoint_note", protocol["source_contract"]["midpoint_note"]),
        ("selector_transfer_results", protocol["source_contract"]["selector_transfer_results"]),
        ("floor_sum_results", protocol["source_contract"]["floor_sum_results"]),
        ("one_query_results", protocol["source_contract"]["one_query_results"]),
    ):
        path = ROOT / relative
        expected = protocol["source_contract"][f"{label}_sha256"]
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(f"pinned source hash mismatch for {label}: {actual} != {expected}")
        checked_hashes[label] = actual

    midpoint_path = ROOT / protocol["source_contract"]["midpoint_results"]
    first_load = json.loads(midpoint_path.read_text())
    projection = freeze_source_projection(first_load)
    del first_load

    expected_development = set(protocol["scope"]["development"])
    expected_archival = set(protocol["scope"]["archival_controls"])
    if expected_development != {record_id for record_id in ACTIVE_IDS if record_id.startswith("squares")}: 
        raise AssertionError("development scope changed")
    if expected_archival != {record_id for record_id in ACTIVE_IDS if record_id.startswith("fibonacci")}: 
        raise AssertionError("archival-control scope changed")
    if protocol["scope"]["named_controls"] != ["strict_16", "doubling_112", "tight_13"]:
        raise AssertionError("named controls changed")

    records: dict[str, Any] = {}
    candidate_ledger: dict[str, int] = {}
    all_lemma_defects: list[dict[str, Any]] = []
    # Candidate phase: no containment result or complement threshold schedule is available here.
    for record_id in (*ACTIVE_IDS, "strict_16"):
        source_row = projection[record_id]
        speeds = tuple(source_row["speeds"])
        left, right = map(F, source_row["window"])
        scored_pairs: list[dict[str, Any]] = []
        for raw_pair in source_row["tied_minimum_pairs"]:
            pair = tuple(raw_pair)
            complement = tuple(speed for speed in speeds if speed not in pair)
            scored = score_pair(pair, complement, left, right)
            if scored["component_count"] != source_row["minimum_component_count"]:
                raise AssertionError(f"independent component-count mismatch for {record_id} {pair}")
            for defect in scored["lemma_defects"]:
                all_lemma_defects.append({"record_id": record_id, "base_pair": list(pair), **defect})
            add_numeric_dict(candidate_ledger, scored["reconstruction_ledger"])
            add_numeric_dict(candidate_ledger, scored["candidate_operation_ledger"])
            scored_pairs.append(scored)
        if len(scored_pairs) < 2:
            raise AssertionError(f"active tie record {record_id} has fewer than two scored pairs")
        maximum_score = max(F(row["pair_score"]) for row in scored_pairs)
        selected = min(
            (row for row in scored_pairs if F(row["pair_score"]) == maximum_score), key=pair_key
        )
        selected_score = F(selected["pair_score"])
        slack = source_row["potential_slack_by_pair"][",".join(map(str, selected["base_pair"]))]
        selected_outcome = (
            "lipschitz_whole_component_certified" if selected_score >= 0 else "negative_score_inconclusive"
        )
        records[record_id] = {
            "id": record_id,
            "role": source_row["role"],
            "speeds": source_row["speeds"],
            "window": source_row["window"],
            "dispatch": "minimum_count_tie_lipschitz_scored",
            "minimum_component_count": source_row["minimum_component_count"],
            "tied_minimum_pairs": source_row["tied_minimum_pairs"],
            "scored_pairs": scored_pairs,
            "selected_pair": selected["base_pair"],
            "selected_score": selected["pair_score"],
            "selected_score_nonnegative": selected_score >= 0,
            "selected_outcome": selected_outcome,
            "certified_lower_bound": slack if selected_score >= 0 else None,
            "containment_query_used_for_certificate": False,
            "fallback_query_used": False,
            "choice_comparisons": len(scored_pairs) - 1,
        }
        candidate_ledger["pair_choice_comparisons"] = candidate_ledger.get("pair_choice_comparisons", 0) + len(
            scored_pairs
        ) - 1

    doubling = projection["doubling_112"]
    if F(doubling["pair_only_minimum"]) <= 0:
        raise AssertionError("doubling_112 did not retain its positive pair-only dispatch")
    records["doubling_112"] = {
        "id": "doubling_112",
        "role": doubling["role"],
        "speeds": doubling["speeds"],
        "window": doubling["window"],
        "dispatch": "pair_only_positive_exit_before_tie_scoring",
        "selected_pair": None,
        "selected_score": None,
        "selected_outcome": "pair_only_positive_exit",
        "certified_lower_bound": doubling["pair_only_minimum"],
        "containment_query_used_for_certificate": False,
        "fallback_query_used": False,
    }
    tight = projection["tight_13"]
    isolated = (tight["isolated_equality_endpoint"] or {}).get("time")
    if isolated != "3/8":
        raise AssertionError("tight_13 isolated endpoint changed")
    records["tight_13"] = {
        "id": "tight_13",
        "role": tight["role"],
        "speeds": tight["speeds"],
        "window": tight["window"],
        "dispatch": "no_eligible_duration_pair",
        "selected_pair": None,
        "selected_score": None,
        "selected_outcome": "no_eligible_pair_no_duration_query",
        "certified_lower_bound": None,
        "isolated_equality_time": isolated,
        "containment_query_used_for_certificate": False,
        "fallback_query_used": False,
    }

    # Freeze scores, choices, and outcomes before the second source load.
    immutable_candidate_digest = hashlib.sha256(
        json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    second_load = json.loads(midpoint_path.read_text())
    postselection_ledger: dict[str, int] = {}
    classification_counts: dict[str, int] = {}
    archive_disagreements: list[dict[str, Any]] = []
    lemma_or_implementation_defects: list[dict[str, Any]] = []
    for record_id in (*ACTIVE_IDS, "strict_16"):
        row = records[record_id]
        speeds = tuple(row["speeds"])
        left, right = map(F, row["window"])
        archive = archived_containment_map(second_load, record_id)
        audits = []
        for scored in row["scored_pairs"]:
            pair = tuple(scored["base_pair"])
            complement = tuple(scored["complement"])
            audit = postselection_containment(pair, complement, speeds, left, right)
            archived_answer = archive[pair]
            archive_match = audit["containment_holds"] == archived_answer
            if not archive_match:
                archive_disagreements.append(
                    {
                        "record_id": record_id,
                        "base_pair": list(pair),
                        "independent": audit["containment_holds"],
                        "archive": archived_answer,
                    }
                )
            nonnegative = scored["score_nonnegative"]
            contains = audit["containment_holds"]
            if nonnegative and contains:
                classification = "sufficient_certificate_true_positive"
            elif nonnegative and not contains:
                classification = "impossible_nonnegative_false_positive"
                lemma_or_implementation_defects.append(
                    {"record_id": record_id, "base_pair": list(pair), "kind": classification}
                )
            elif not nonnegative and contains:
                classification = "negative_score_containing_pair_inconclusive"
            else:
                classification = "negative_score_noncontaining_pair_inconclusive"
            classification_counts[classification] = classification_counts.get(classification, 0) + 1
            audit["archived_containment_holds"] = archived_answer
            audit["archive_match"] = archive_match
            audit["score_nonnegative"] = nonnegative
            audit["classification"] = classification
            audits.append(audit)
            add_numeric_dict(postselection_ledger, audit["event_ledger"])
        row["postselection_audits"] = audits

    if hashlib.sha256(
        json.dumps(
            {key: {field: value for field, value in row.items() if field != "postselection_audits"} for key, row in records.items()},
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest() != immutable_candidate_digest:
        raise AssertionError("postselection data changed a frozen candidate field")

    reflection_checks = []
    for first_id, second_id in REFLECTION_PAIRS:
        first = records[first_id]
        second = records[second_id]
        first_scores = {tuple(row["base_pair"]): row["pair_score"] for row in first["scored_pairs"]}
        second_scores = {tuple(row["base_pair"]): row["pair_score"] for row in second["scored_pairs"]}
        reflection_checks.append(
            {
                "record_ids": [first_id, second_id],
                "scores_match": first_scores == second_scores,
                "choices_match": first["selected_pair"] == second["selected_pair"],
                "outcomes_match": first["selected_outcome"] == second["selected_outcome"],
                "counted_as_independent_validation": False,
            }
        )

    verification: dict[str, Any] = {
        "status": "PENDING_PRIMARY_COMPARISON",
        "method": {
            "base_components": "independent complete rational threshold-event sweep",
            "candidate": "exact Lipschitz midpoint lower margin using fractions.Fraction",
            "lemma_check": "separate direct minimum of distance-to-nearest-integer on each closed scaled interval",
            "postselection": "separate all-speed event sweep after immutable candidate digest",
            "primary_imported": False,
        },
        "checked_source_hashes": checked_hashes,
        "literal_scope": {
            "active_tie_labels": 7,
            "active_reflection_mechanisms": 4,
            "development": sorted(expected_development),
            "archival_controls": sorted(expected_archival),
            "named_controls": ["strict_16", "doubling_112", "tight_13"],
            "new_speeds_or_windows_added": False,
        },
        "information_barrier": {
            "preselection_fields": sorted(next(iter(projection.values())).keys()),
            "candidate_digest_before_postselection": immutable_candidate_digest,
            "postselection_changed_candidate": False,
            "containment_schedules_used_for_candidate": False,
        },
        "records": records,
        "lipschitz_lemma_check": {
            "evaluation_count": sum(
                len(component["complement_evaluations"])
                for record_id in (*ACTIVE_IDS, "strict_16")
                for pair in records[record_id]["scored_pairs"]
                for component in pair["component_evaluations"]
            ),
            "numeric_lower_bound_defects": all_lemma_defects,
            "postselection_nonnegative_false_positives": lemma_or_implementation_defects,
            "strict_blocking_threshold": "distance<1/8",
            "equality_is_safe": True,
            "open_component_closures_checked": True,
        },
        "postselection_score_audit": {
            "classification_counts": classification_counts,
            "archive_disagreements": archive_disagreements,
            "charged_separately": True,
            "could_change_frozen_choice": False,
        },
        "reflection_checks": reflection_checks,
        "cost_ledger": {
            "candidate": candidate_ledger,
            "postselection_containment_audit": postselection_ledger,
            "unlike_operations_combined": False,
        },
        "primary_comparison": {"status": "PENDING", "compared_scalar_fields": 0, "disagreements": []},
        "interpretation_limits": protocol["interpretation_limits"],
    }
    if PRIMARY_RESULTS.exists() and PRIMARY_SCRIPT.exists():
        primary = json.loads(PRIMARY_RESULTS.read_text())
        verification["checked_source_hashes"]["primary.py"] = sha256(PRIMARY_SCRIPT)
        verification["checked_source_hashes"]["results.json"] = sha256(PRIMARY_RESULTS)
        comparison = semantic_primary_comparison(verification, primary)
        verification["primary_comparison"] = comparison
        verification["status"] = (
            "PASS"
            if comparison["status"] == "PASS"
            and not all_lemma_defects
            and not lemma_or_implementation_defects
            and not archive_disagreements
            and all(check["scores_match"] and check["choices_match"] and check["outcomes_match"] for check in reflection_checks)
            else "FAIL"
        )
    return verification


def render_report(data: dict[str, Any]) -> str:
    counts = data["postselection_score_audit"]["classification_counts"]
    candidate = data["cost_ledger"]["candidate"]
    post = data["cost_ledger"]["postselection_containment_audit"]
    lines = [
        "# Independent Lipschitz component-margin verification",
        "",
        f"**Status:** {data['status']}",
        "",
        "This verifier does not import `primary.py`. It reconstructs base components from a complete exact threshold-event sweep, then checks each Lipschitz lower margin against a separate direct minimum-distance calculation on the closed component.",
        "",
        "## Scope",
        "",
        f"- Active tie labels: {data['literal_scope']['active_tie_labels']} ({data['literal_scope']['active_reflection_mechanisms']} reflection mechanisms)",
        f"- Tied pair labels: {sum(len(data['records'][record_id].get('scored_pairs', [])) for record_id in (*ACTIVE_IDS, 'strict_16'))}",
        f"- Reconstructed positive components: {candidate.get('positive_components', 0)}",
        f"- Lipschitz complement evaluations: {data['lipschitz_lemma_check']['evaluation_count']}",
        f"- Exact numeric lower-bound defects: {len(data['lipschitz_lemma_check']['numeric_lower_bound_defects'])}",
        f"- Impossible nonnegative-score false positives: {len(data['lipschitz_lemma_check']['postselection_nonnegative_false_positives'])}",
        "",
        "## Outcome",
        "",
        f"- Nonnegative sufficient-certificate true positives: {counts.get('sufficient_certificate_true_positive', 0)}",
        f"- Negative-score containing pairs (inconclusive): {counts.get('negative_score_containing_pair_inconclusive', 0)}",
        f"- Negative-score noncontaining pairs (inconclusive): {counts.get('negative_score_noncontaining_pair_inconclusive', 0)}",
        f"- Nonnegative-score false positives: {counts.get('impossible_nonnegative_false_positive', 0)}",
        "- The squares rule selects `{25,121}` with score `51/484`; failed `{25,169}` has score `-1/52` and is not certified.",
        "- All Fibonacci selected pairs and the `strict_16` selected pair have nonnegative scores.",
        "- `doubling_112` exits on `761/32256`; `tight_13` retains only isolated equality `3/8`.",
        "",
        "## Separately charged audit",
        "",
        f"- Postselection containment threshold events: {post.get('unique_events_including_window_endpoints', 0)}",
        f"- Postselection open cells: {post.get('open_cells', 0)}",
        f"- Archived containment disagreements: {len(data['postselection_score_audit']['archive_disagreements'])}",
        "- Containment schedules were not used to select or certify a pair.",
        "",
        "## Primary comparison",
        "",
        f"- Status: {data['primary_comparison']['status']}",
        f"- Compared scalar fields: {data['primary_comparison']['compared_scalar_fields']}",
        f"- Disagreements: {len(data['primary_comparison']['disagreements'])}",
        "",
        "## Limits",
        "",
        "This is an independently structured internal exact check, not independent human mathematical validation. Nonnegative score is sufficient, while negative score is only inconclusive. The squares case is fitted development data; the controls are archival; reflections are not independent examples; and every tested tied pair has one component.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = derive()
    encoded = json.dumps(data, indent=2, sort_keys=True) + "\n"
    report = render_report(data)
    if args.write:
        OUTPUT.write_text(encoded)
        REPORT.write_text(report)
        print(f"wrote {OUTPUT.relative_to(ROOT)} and {REPORT.relative_to(ROOT)}: {data['status']}")
        return
    if not OUTPUT.exists() or not REPORT.exists():
        raise SystemExit("verification artifacts do not exist; run --write after primary results are available")
    if OUTPUT.read_text() != encoded:
        raise SystemExit("verification.json is stale")
    if REPORT.read_text() != report:
        raise SystemExit("verification.md is stale")
    if data["status"] != "PASS":
        raise SystemExit(f"verification status is {data['status']}")
    print(
        f"PASS: {data['primary_comparison']['compared_scalar_fields']} primary scalar fields; "
        f"{data['lipschitz_lemma_check']['evaluation_count']} exact lemma evaluations"
    )


if __name__ == "__main__":
    main()
