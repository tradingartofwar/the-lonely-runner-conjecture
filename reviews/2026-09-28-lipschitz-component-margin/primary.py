"""Exact primary calculation for the frozen Lipschitz component-margin study.

The candidate sees only a literal projection of the pinned midpoint study.  It
reconstructs every tied base component and computes the lower bound

    dist(v * midpoint(I), Z) - 1/8 - v * width(I) / 2.

Choices and certificate decisions are immutable before any containment result
is calculated or reloaded.  The all-tied containment sweep is a separately
charged postselection audit.  ``--write`` deterministically writes
``results.json``; ``--check`` is read-only and requires exact reconstruction.
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
PROTOCOL_SHA256 = "3903410dec2f61deda37c9fe7d03fb6ae24034fc80c78f8426faa9e81f4cae0c"
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
# Literal source projection.  No containment answer, actual duration,
# violation, reflection/mechanism label, or prior candidate decision crosses.


def project_tied_case(source: dict) -> dict:
    tied = []
    for row in source["scored_tied_pairs"]:
        tied.append({
            "base_pair": tuple(map(int, row["base_pair"])),
            "complement": tuple(map(int, row["complement"])),
            "potential_slack": q(row["potential_slack"]),
            "component_count": int(row["component_count"]),
        })
    return {
        "id": str(source["id"]),
        "speeds": tuple(map(int, source["speeds"])),
        "window": tuple(map(q, source["window"])),
        "pair_only_minimum": q(source["pair_only_minimum"]),
        "tied_pairs": tuple(tied),
    }


def project_dispatch_control(name: str, source: dict) -> dict:
    isolated = source.get("isolated_equality_endpoint")
    return {
        "id": name,
        "speeds": tuple(map(int, source["speeds"])),
        "window": tuple(map(q, source["window"])),
        "pair_only_minimum": q(source["pair_only_minimum"]),
        "tied_pairs": (),
        "isolated_equality_endpoint": (
            {"time": q(isolated["time"])} if isolated is not None else None
        ),
    }


# -------------------------------------------------------------------------
# Exact positive blocker components.


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


def lipschitz_score(
    speeds: tuple[int, ...], window: tuple[F, F], pair: tuple[int, int]
) -> dict:
    reconstruction_cost = Counter()
    components = base_components(pair, window, reconstruction_cost)
    complement = tuple(speed for speed in speeds if speed not in pair)
    score_cost = Counter()
    component_rows = []
    lower_margins = []
    for component_index, component in enumerate(components):
        left, right = component["interval"]
        width = right - left
        midpoint = (left + right) / 2
        score_cost["component_width_computations"] += 1
        score_cost["midpoint_samples"] += 1
        score_cost["midpoint_divisions_by_two"] += 1
        evaluations = []
        for speed in complement:
            p = phase(speed, midpoint)
            d = min(p, 1 - p)
            midpoint_margin = d - DELTA
            radius_bound = speed * width / 2
            lower_margin = midpoint_margin - radius_bound
            score_cost["complement_phase_reductions"] += 1
            score_cost["nearest_integer_distances"] += 1
            score_cost["midpoint_margin_subtractions"] += 1
            score_cost["speed_width_products"] += 1
            score_cost["radius_divisions_by_two"] += 1
            score_cost["lower_margin_subtractions"] += 1
            score_cost["certificate_sign_comparisons"] += 1
            lower_margins.append(lower_margin)
            evaluations.append({
                "speed": speed,
                "phase_at_midpoint": p,
                "distance_at_midpoint": d,
                "midpoint_signed_margin": midpoint_margin,
                "component_width": width,
                "speed_width_product": speed * width,
                "lipschitz_radius_bound": radius_bound,
                "lipschitz_lower_margin": lower_margin,
                "lower_margin_nonnegative": lower_margin >= 0,
                "numeric_identity_verified": (
                    lower_margin == d - DELTA - speed * width / 2
                ),
            })
        component_rows.append({
            "component_index": component_index,
            "interval": component["interval"],
            "laps": component["laps"],
            "left_included": component["left_included"],
            "right_included": component["right_included"],
            "closure_used_by_lemma": True,
            "width": width,
            "midpoint": midpoint,
            "complement_evaluations": evaluations,
        })
    assert lower_margins
    score = lower_margins[0]
    for margin in lower_margins[1:]:
        score_cost["minimum_lower_margin_comparisons"] += 1
        if margin < score:
            score = margin
    return {
        "base_pair": pair,
        "complement": complement,
        "component_count": len(components),
        "components_and_bounds": component_rows,
        "pair_score": score,
        "score_nonnegative": score >= 0,
        "certificate_semantics": (
            "score>=0 is sufficient for full compound containment; "
            "score<0 is inconclusive"
        ),
        "reconstruction_cost": dict(sorted(reconstruction_cost.items())),
        "lipschitz_score_cost": dict(sorted(score_cost.items())),
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
# Exact containment audit.  This code is prohibited until choices and
# certificate outcomes have frozen.


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
# Frozen dispatch, scoring, certification, and postselection audit.


def prepare_active(projected: dict, role: str) -> dict:
    tied = list(projected["tied_pairs"])
    assert len(tied) >= 2
    counts = {row["component_count"] for row in tied}
    assert len(counts) == 1
    scored = []
    for row in sorted(tied, key=lambda item: item["base_pair"]):
        score = lipschitz_score(
            projected["speeds"], projected["window"], row["base_pair"]
        )
        assert score["component_count"] == row["component_count"]
        assert score["complement"] == row["complement"]
        score["potential_slack"] = row["potential_slack"]
        scored.append(score)
    selected, choice_cost = choose_maximin(scored)
    selected_row = next(row for row in scored if row["base_pair"] == selected)
    certified = selected_row["pair_score"] >= 0
    slack = next(
        row["potential_slack"] for row in tied if row["base_pair"] == selected
    )
    return {
        "id": projected["id"],
        "role": role,
        "speeds": projected["speeds"],
        "window": projected["window"],
        "pair_only_minimum": projected["pair_only_minimum"],
        "forbidden_preselection_fields_retained": [],
        "dispatch": "minimum_count_tie_lipschitz_scored",
        "minimum_component_count": next(iter(counts)),
        "tied_minimum_pairs": [row["base_pair"] for row in tied],
        "scored_tied_pairs": scored,
        "candidate_selected_pair": selected,
        "inherited_lexicographic_pair": min(row["base_pair"] for row in tied),
        "choice_cost": dict(sorted(choice_cost.items())),
        "selected_result": {
            "containment_query_issued_preselection": False,
            "selected_base_pair": selected,
            "selected_pair_score": selected_row["pair_score"],
            "certificate_issued": certified,
            "outcome": (
                "lipschitz_whole_component_certified"
                if certified else "negative_score_inconclusive_no_retune"
            ),
            "certified_lower_bound": slack if certified else None,
            "counterfactual_bound_if_certificate_held": slack,
            "second_or_fallback_query_issued": False,
        },
    }


def prepare_dispatch(projected: dict, role: str) -> dict:
    base = {
        "id": projected["id"],
        "role": role,
        "speeds": projected["speeds"],
        "window": projected["window"],
        "pair_only_minimum": projected["pair_only_minimum"],
        "forbidden_preselection_fields_retained": [],
        "tied_minimum_pairs": [],
        "scored_tied_pairs": [],
        "candidate_selected_pair": None,
        "choice_cost": {},
    }
    if projected["pair_only_minimum"] > 0:
        base["dispatch"] = "pair_only_positive_exit_before_tie_scoring"
        base["selected_result"] = {
            "certificate_issued": True,
            "outcome": "pair_only_positive_exit",
            "certified_lower_bound": projected["pair_only_minimum"],
            "second_or_fallback_query_issued": False,
        }
    else:
        base["dispatch"] = "no_eligible_duration_pair"
        base["selected_result"] = {
            "certificate_issued": False,
            "outcome": "no_eligible_pair_no_duration_query",
            "certified_lower_bound": None,
            "second_or_fallback_query_issued": False,
        }
        if projected["isolated_equality_endpoint"] is not None:
            base["isolated_equality_endpoint"] = projected["isolated_equality_endpoint"]
    base["postselection_tied_pair_audit"] = {
        "queries": [],
        "charged_separately_from_candidate": True,
        "cannot_change_frozen_choice_or_certificate": True,
    }
    return base


def attach_audit(prepared: dict, projected: dict) -> None:
    score_by_pair = {row["base_pair"]: row for row in prepared["scored_tied_pairs"]}
    queries = []
    for pair in prepared["tied_minimum_pairs"]:
        query = containment_query(projected["speeds"], projected["window"], pair)
        score = score_by_pair[pair]
        nonnegative = score["score_nonnegative"]
        actual = query["containment_holds"]
        assert not (nonnegative and not actual), (
            "Nonnegative Lipschitz certificate contradicted exact containment", pair
        )
        query["lipschitz_pair_score"] = score["pair_score"]
        query["score_nonnegative"] = nonnegative
        query["audit_class"] = (
            "sufficient_certificate_true_positive"
            if nonnegative and actual
            else "negative_score_containing_pair"
            if actual
            else "negative_score_failed_pair"
        )
        queries.append(query)
    selected = prepared["candidate_selected_pair"]
    selected_query = next(row for row in queries if row["base_pair"] == selected)
    prepared["postselection_tied_pair_audit"] = {
        "queries": queries,
        "containing_pairs": [row["base_pair"] for row in queries if row["containment_holds"]],
        "failed_pairs": [row["base_pair"] for row in queries if not row["containment_holds"]],
        "audit_class_counts": dict(sorted(Counter(row["audit_class"] for row in queries).items())),
        "selected_pair_contains": selected_query["containment_holds"],
        "nonnegative_false_positive_count": 0,
        "charged_separately_from_candidate": True,
        "cannot_change_frozen_choice_or_certificate": True,
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


def attach_archive_comparison(prepared: dict, source: dict) -> None:
    prior = {
        tuple(row["base_pair"]): row
        for row in source["postselection_tied_pair_oracle"]["queries"]
    }
    comparisons = []
    for query in prepared["postselection_tied_pair_audit"]["queries"]:
        archived = prior[query["base_pair"]]
        assert query["containment_holds"] == archived["containment_holds"]
        assert query["first_exact_violation"] == _fractionize(
            archived["first_exact_violation"]
        )
        comparisons.append({
            "base_pair": query["base_pair"],
            "containment_matches_pinned_archive": True,
            "first_violation_matches_pinned_archive": True,
        })
    prepared["postselection_archive_comparison"] = {
        "tied_pair_comparisons": comparisons,
        "archive_used_to_change_candidate_choice_or_certificate": False,
    }


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
        assert first["postselection_tied_pair_audit"]["containing_pairs"] == second["postselection_tied_pair_audit"]["containing_pairs"]
        output.append({
            "record_ids": (first_id, second_id),
            "role": role,
            "scores_choices_certificates_and_audits_match": True,
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
            add_cost(score, row["lipschitz_score_cost"])
        add_cost(choice, case["choice_cost"])
    return {
        "tied_pairs": tied_pairs,
        "reconstructed_positive_components": components,
        "component_reconstruction_operations": dict(sorted(reconstruction.items())),
        "lipschitz_bound_operations": dict(sorted(score.items())),
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

    development_ids = tuple(protocol["scope"]["development"])
    archive_ids = tuple(protocol["scope"]["archival_controls"])
    wanted = development_ids + archive_ids

    # Literal projection and source deletion enforce the preselection barrier.
    raw_midpoint = json.loads(paths["midpoint_results"].read_text())
    records = {
        record_id: project_tied_case(raw_midpoint["cases"][record_id])
        for record_id in wanted
    }
    controls_projected = {
        "strict_16": project_tied_case(raw_midpoint["controls"]["strict_16"]),
        "doubling_112": project_dispatch_control(
            "doubling_112", raw_midpoint["controls"]["doubling_112"]
        ),
        "tight_13": project_dispatch_control(
            "tight_13", raw_midpoint["controls"]["tight_13"]
        ),
    }
    del raw_midpoint

    cases = {
        record_id: prepare_active(
            records[record_id],
            "development" if record_id in development_ids else "archival_control",
        )
        for record_id in wanted
    }
    controls = {
        "strict_16": prepare_active(controls_projected["strict_16"], "named_control"),
        "doubling_112": prepare_dispatch(controls_projected["doubling_112"], "dispatch_control"),
        "tight_13": prepare_dispatch(controls_projected["tight_13"], "dispatch_control"),
    }

    # All choices and certificate outcomes are now immutable.  Only now may
    # the separately charged exact containment schedules be constructed.
    for record_id in wanted:
        attach_audit(cases[record_id], records[record_id])
    attach_audit(controls["strict_16"], controls_projected["strict_16"])

    # Reload archived answers only after candidate outcomes and audit results.
    post_midpoint = json.loads(paths["midpoint_results"].read_text())
    for record_id in wanted:
        attach_archive_comparison(cases[record_id], post_midpoint["cases"][record_id])
    attach_archive_comparison(
        controls["strict_16"], post_midpoint["controls"]["strict_16"]
    )
    del post_midpoint

    assert controls["doubling_112"]["selected_result"]["certified_lower_bound"] == F(761, 32256)
    assert controls["tight_13"]["isolated_equality_endpoint"]["time"] == F(3, 8)

    reflections = reflection_audit(cases)
    active = list(cases.values()) + [controls["strict_16"]]
    audit_queries = [
        query for case in active
        for query in case["postselection_tied_pair_audit"]["queries"]
    ]
    audit_classes = Counter(query["audit_class"] for query in audit_queries)
    development = [cases[item] for item in development_ids]
    archival = [cases[item] for item in archive_ids]
    selected_certificates = [case for case in active if case["selected_result"]["certificate_issued"]]

    result = {
        "baseline": protocol["baseline"],
        "protocol_sha256": PROTOCOL_SHA256,
        "primary_sha256": sha256(Path(__file__)),
        "source_contract": protocol["source_contract"],
        "arithmetic": "integers and fractions.Fraction only; no floating-point decisions",
        "information_barrier": (
            "The pinned midpoint output was literally projected to ids, speeds, windows, pair-only values, tied pairs, complements, potential slacks and component counts, then deleted. Components and Lipschitz scores were reconstructed before any containment schedule or answer was calculated or reloaded."
        ),
        "candidate_lemma": (
            "Distance to the nearest integer is 1-Lipschitz, so on closure(I), "
            "distance(v*t,Z)-1/8 >= distance(v*mid(I),Z)-1/8-v*width(I)/2."
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
            "tied_pair_label_instances": len(audit_queries),
            "tied_pair_reflection_mechanism_instances": 9,
            "selected_lipschitz_certified_labels": len(selected_certificates),
            "selected_lipschitz_certified_mechanisms": sum(
                cases[first]["selected_result"]["certificate_issued"]
                for first in ("squares:1,2,5:12", "fibonacci:1,2,4:1", "fibonacci:1,2,4:11")
            ) + controls["strict_16"]["selected_result"]["certificate_issued"],
            "selected_negative_inconclusive_labels": len(active) - len(selected_certificates),
            "preselection_containment_queries": 0,
            "second_or_fallback_queries": 0,
            "pair_only_dispatch_exits": 1,
            "no_eligible_pair_dispatch_exits": 1,
        },
        "outcomes": {
            "development_selected_pair_is_25_121": all(
                case["candidate_selected_pair"] == (25, 121) for case in development
            ),
            "development_selected_certified_labels": sum(
                case["selected_result"]["certificate_issued"] for case in development
            ),
            "development_failed_25_169_refused_labels": sum(
                not next(
                    row["score_nonnegative"] for row in case["scored_tied_pairs"]
                    if row["base_pair"] == (25, 169)
                ) for case in development
            ),
            "archival_control_selected_certified_labels": sum(
                case["selected_result"]["certificate_issued"] for case in archival
            ),
            "strict_16_selected_certified": controls["strict_16"]["selected_result"]["certificate_issued"],
            "postselection_audit_class_counts": dict(sorted(audit_classes.items())),
            "nonnegative_score_false_positives": sum(
                query["score_nonnegative"] and not query["containment_holds"]
                for query in audit_queries
            ),
            "negative_score_containing_pairs": sum(
                not query["score_nonnegative"] and query["containment_holds"]
                for query in audit_queries
            ),
            "all_numeric_identities_verified": all(
                evaluation["numeric_identity_verified"]
                for case in active
                for row in case["scored_tied_pairs"]
                for component in row["components_and_bounds"]
                for evaluation in component["complement_evaluations"]
            ),
        },
        "aggregate_cost_ledgers": {
            "candidate_preselection_lipschitz_scores": score_cost(active),
            "postselection_all_tied_pair_audit_charged_separately": query_cost(audit_queries),
            "comparison_policy": "Unlike operations are not combined into a synthetic runtime score.",
        },
        "findings": {
            "finite_status": "OBSERVED on frozen development and archival controls",
            "nonnegative_score_is_sufficient_containment_certificate": True,
            "negative_score_implies_failed_containment": False,
            "development_fit_is_validation": False,
            "archival_controls_are_prospective_held_out": False,
            "general_selector_claim": False,
            "whole_configuration_claim": False,
            "new_existence_coverage": False,
            "runtime_claim": False,
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
    print("WROTE: Lipschitz component margin" if args.write else "PASS: Lipschitz component margin reproduced read-only")


if __name__ == "__main__":
    main()
