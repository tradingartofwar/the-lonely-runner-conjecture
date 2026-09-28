"""Exact primary calculation for the frozen lap-band component-count study.

The prearchive phase sees only speeds, windows, and moment-derived eligibility.
It counts integer lap pairs directly; it never constructs a blocking-interval
list or a pair-intersection interval.  Archived component counts, selections,
and containment outcomes are loaded only after all 24 formula counts and all
four formula selections have been fixed.

``--write`` deterministically creates ``results.json``.  ``--check`` is
read-only and reconstructs the complete result with ``fractions.Fraction``.
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
PROTOCOL_SHA256 = "9053ebb58fa30a1841e03bb1aba686fb51631b01480186772f751df63bda1165"
DELTA = F(1, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value) -> F:
    return F(str(value))


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def floor(value: F) -> int:
    return value.numerator // value.denominator


def ceil(value: F) -> int:
    return -floor(-value)


def open_integer_labels(lower: F, upper: F) -> list[int]:
    """Integers k satisfying the strict inequalities lower < k < upper."""
    return list(range(floor(lower) + 1, ceil(upper)))


def mask_for_pair(speeds: tuple[int, ...], pair: tuple[int, int]) -> int:
    return sum(1 << speeds.index(speed) for speed in pair)


def extract_allowed_inputs(protocol: dict, joint: dict) -> dict:
    """Irreversibly project the monolithic source to the prearchive contract."""
    allowed = {}
    for case_spec in protocol["cases"]:
        physical = joint["cases"][case_spec["source_case"]]["physical"]
        allowed[case_spec["id"]] = {
            "speeds": physical["speeds"],
            "window": physical["window"],
            "moments": physical["moments"],
        }
    return allowed


def moment_projection(allowed: dict) -> dict:
    """Consume only speeds, window and moments in the prearchive phase."""
    assert set(allowed) == {"speeds", "window", "moments"}
    speeds = tuple(map(int, allowed["speeds"]))
    window = tuple(map(q, allowed["window"]))
    moments = tuple(map(q, allowed["moments"]))
    total = moments[0]
    singles = tuple(moments[1 << i] for i in range(4))
    pairs = tuple(combinations(speeds, 2))
    pair_values = {
        pair: moments[mask_for_pair(speeds, pair)] for pair in pairs
    }
    c0 = total - sum(singles, F(0)) + sum(pair_values.values(), F(0))
    rows = []
    for pair in pairs:
        complement = tuple(speed for speed in speeds if speed not in pair)
        omitted = pair_values[complement]
        slack = c0 - omitted
        rows.append(
            {
                "base_pair": pair,
                "complement": complement,
                "omitted_pair_overlap": omitted,
                "potential_slack": slack,
                "eligible": slack > 0,
            }
        )
    return {
        "speeds": speeds,
        "window": window,
        "total": total,
        "single_durations": dict(zip(speeds, singles)),
        "pair_durations": {"/".join(map(str, p)): v for p, v in pair_values.items()},
        "C_0": c0,
        "pair_rows": rows,
    }


def lap_band_count(
    pair: tuple[int, int], window: tuple[F, F]
) -> tuple[int, dict, Counter]:
    """Count positive components using only integer lap-band inequalities."""
    a, b = pair
    assert 0 < a < b
    left, right = window
    m_window_lower = a * left - DELTA
    m_window_upper = a * right + DELTA
    m_labels = open_integer_labels(m_window_lower, m_window_upper)
    b_window_lower = b * left - DELTA
    b_window_upper = b * right + DELTA
    band_radius = DELTA * (a + b)
    rows = []
    cost = Counter()
    for m in m_labels:
        raw_lower = (b * m - band_radius) / a
        raw_upper = (b * m + band_radius) / a
        lower = max(b_window_lower, raw_lower)
        upper = min(b_window_upper, raw_upper)
        n_labels = open_integer_labels(lower, upper)
        formula_count = max(0, ceil(upper) - floor(lower) - 1)
        assert formula_count == len(n_labels)
        for n in n_labels:
            assert b_window_lower < n < b_window_upper
            assert abs(b * m - a * n) < band_radius
        rows.append(
            {
                "m": m,
                "raw_band_lower": raw_lower,
                "raw_band_upper": raw_upper,
                "lower": lower,
                "upper": upper,
                "n_labels": n_labels,
                "n_count": len(n_labels),
            }
        )
        cost["m_rows"] += 1
        cost["band_bound_evaluations"] += 2
        cost["max_min_bound_operations"] += 2
        cost["floor_ceil_operations"] += 2
        cost["integer_n_labels_counted"] += len(n_labels)
    count = sum(row["n_count"] for row in rows)
    return count, {
        "smaller_speed": a,
        "larger_speed": b,
        "m_window_lower": m_window_lower,
        "m_window_upper": m_window_upper,
        "candidate_m_labels": m_labels,
        "larger_speed_n_window_lower": b_window_lower,
        "larger_speed_n_window_upper": b_window_upper,
        "band_radius": band_radius,
        "m_rows": rows,
        "component_count": count,
    }, cost


def choose_by_formula(eligible_rows: list[dict], cost: Counter):
    """Frozen selection: count first, direct physical lexicographic tie-break."""
    if not eligible_rows:
        return None
    chosen = eligible_rows[0]
    for row in eligible_rows[1:]:
        cost["component_count_order_comparisons"] += 1
        if row["lap_band_component_count"] < chosen["lap_band_component_count"]:
            chosen = row
        elif row["lap_band_component_count"] == chosen["lap_band_component_count"]:
            cost["component_count_ties"] += 1
            cost["physical_lexicographic_tie_breaks"] += 1
            if row["base_pair"] < chosen["base_pair"]:
                chosen = row
    return chosen["base_pair"]


def build_prearchive_cases(protocol: dict, allowed_inputs: dict) -> dict:
    """Finish every count and selection before any archive outcome is read."""
    output = {}
    for case_spec in protocol["cases"]:
        case_id = case_spec["id"]
        source_case = case_spec["source_case"]
        projected = moment_projection(allowed_inputs[case_id])
        diagnostic_case = case_id == "doubling_112"
        pair_rows = []
        formula_cost = Counter()
        charged_cost = Counter()
        diagnostic_cost = Counter()
        audit_only_cost = Counter()
        for base in projected["pair_rows"]:
            count, table, pair_cost = lap_band_count(
                base["base_pair"], projected["window"]
            )
            category = (
                "diagnostic_selector"
                if base["eligible"] and diagnostic_case
                else "selector_charged"
                if base["eligible"]
                else "all_pair_audit_only"
            )
            row = {
                **base,
                "lap_band_component_count": count,
                "cost_category": category,
                "lap_band_table": table,
                "arithmetic_cost": dict(sorted(pair_cost.items())),
            }
            pair_rows.append(row)
            formula_cost.update(pair_cost)
            if category == "selector_charged":
                charged_cost.update(pair_cost)
            elif category == "diagnostic_selector":
                diagnostic_cost.update(pair_cost)
            else:
                audit_only_cost.update(pair_cost)
        eligible = [row for row in pair_rows if row["eligible"]]
        selection_cost = Counter()
        selected = choose_by_formula(eligible, selection_cost)
        output[case_id] = {
            "source_case": source_case,
            "speeds": projected["speeds"],
            "window": projected["window"],
            "C_0": projected["C_0"],
            "moment_projection": {
                "total": projected["total"],
                "single_durations": projected["single_durations"],
                "pair_durations": projected["pair_durations"],
            },
            "pair_rows": pair_rows,
            "eligible_base_pairs": [row["base_pair"] for row in eligible],
            "formula_selected_base_pair": selected,
            "diagnostic_only_after_pair_exit": diagnostic_case,
            "cost": {
                "all_six_pairs_in_this_window": dict(sorted(formula_cost.items())),
                "selector_charged": dict(sorted(charged_cost.items())),
                "diagnostic_selector": dict(sorted(diagnostic_cost.items())),
                "ineligible_all_pair_audit_only": dict(sorted(audit_only_cost.items())),
                "selection": dict(sorted(selection_cost.items())),
            },
        }
    return output


def archived_component_count(physical: dict, pair: tuple[int, int]) -> int:
    speeds = tuple(physical["speeds"])
    mask = mask_for_pair(speeds, pair)
    # Reading the number of archived interval-derived components is permitted
    # only in the postselection phase.  No interval endpoint is used here.
    return len(physical["intersection_pieces"][str(mask)] if isinstance(
        next(iter(physical["intersection_pieces"])), str
    ) else physical["intersection_pieces"][mask])


def add_archived_comparisons(
    prearchive: dict, joint: dict, selector: dict, cover: dict
) -> tuple[dict, dict]:
    """Attach archive comparisons after selections are immutable."""
    cover_by_name = {case["name"]: case for case in cover["cases"]}
    comparisons = Counter()
    for case_id, case in prearchive.items():
        source_case = case["source_case"]
        physical = joint["cases"][source_case]["physical"]
        selector_case = selector["cases"][case_id]
        selector_rows = {
            tuple(row["base_pair"]): row
            for row in selector_case["all_six_potential_slacks"]
        }
        for row in case["pair_rows"]:
            pair = tuple(row["base_pair"])
            archive_count = archived_component_count(physical, pair)
            prior_row = selector_rows[pair]
            prior_eligible_count = prior_row["positive_component_count"]
            row["postselection_archive_comparison"] = {
                "interval_derived_component_count": archive_count,
                "formula_matches_interval_derived_count": (
                    row["lap_band_component_count"] == archive_count
                ),
                "prior_selector_recorded_count": prior_eligible_count,
                "formula_matches_prior_selector_recorded_count": (
                    None
                    if prior_eligible_count is None
                    else row["lap_band_component_count"] == prior_eligible_count
                ),
            }
            comparisons["all_pair_component_count_comparisons"] += 1
            assert row["lap_band_component_count"] == archive_count
            if prior_eligible_count is not None:
                comparisons["eligible_prior_count_comparisons"] += 1
                assert row["lap_band_component_count"] == prior_eligible_count

        archived_rule = selector_case["frozen_rule_results"][
            "fewest_positive_occurrence_components"
        ]
        archived_selected = archived_rule["selected_base_pair"]
        archived_selected = None if archived_selected is None else tuple(archived_selected)
        formula_selected = case["formula_selected_base_pair"]
        assert formula_selected == archived_selected
        comparisons["selector_comparisons"] += 1
        control = cover_by_name.get(case_id)
        case["postselection_archived_outcome"] = {
            "prior_interval_selector_base_pair": archived_selected,
            "formula_reproduces_prior_selector": formula_selected == archived_selected,
            "prior_containment_query_issued": archived_rule["query_issued"],
            "prior_containment_holds": archived_rule.get("containment_holds"),
            "prior_outcome": archived_rule["outcome"],
            "prior_certified_lower_bound": archived_rule["certified_lower_bound"],
            "pair_only_exit": selector_case["pair_only_exit"],
            "isolated_equality_endpoint": selector_case["isolated_equality_endpoint"],
            "cover_obligation_control_outcome": None if control is None else control["outcome"],
        }
    return prearchive, dict(sorted(comparisons.items()))


def build() -> dict:
    assert sha256(PROTOCOL) == PROTOCOL_SHA256
    protocol = json.loads(PROTOCOL.read_text())
    source = protocol["source_contract"]
    source_paths = {
        "selector_results": ROOT / source["selector_results"],
        "physical_geometry_and_moments": ROOT / source["physical_geometry_and_moments"],
        "control_roles": ROOT / source["control_roles"],
    }
    for key, path in source_paths.items():
        assert sha256(path) == source[f"{key}_sha256"]

    # Phase 1 parses only the physical source and immediately projects away all
    # geometry.  The selector archive and control roles are not parsed yet.
    joint = json.loads(source_paths["physical_geometry_and_moments"].read_text())
    allowed_inputs = extract_allowed_inputs(protocol, joint)
    prearchive = build_prearchive_cases(protocol, allowed_inputs)

    # Phase 2 begins only after all formula selections are fixed.
    selector = json.loads(source_paths["selector_results"].read_text())
    cover = json.loads(source_paths["control_roles"].read_text())
    cases, comparisons = add_archived_comparisons(prearchive, joint, selector, cover)

    all_rows = [row for case in cases.values() for row in case["pair_rows"]]
    return {
        "baseline": protocol["baseline"],
        "protocol_sha256": PROTOCOL_SHA256,
        "primary_sha256": sha256(Path(__file__)),
        "source_contract": source,
        "arithmetic": "fractions.Fraction only; no floating-point decisions",
        "formula": {
            "threshold": DELTA,
            "strictness": "Every displayed lap-window and lap-band bound is open.",
            "per_m_integer_count": "max(0, ceil(upper)-floor(lower)-1)",
            "component_count": "sum of per-m integer n counts",
            "iteration": "candidate m labels of the smaller physical speed only",
        },
        "information_barrier": (
            "All 24 lap-band counts and all four selections are fixed before "
            "archived component counts, interval-selector choices, containment "
            "outcomes, or control roles are parsed."
        ),
        "primary_forbidden_structures": {
            "blocking_interval_lists_constructed": 0,
            "pair_intersection_intervals_constructed": 0,
            "new_containment_queries": 0,
        },
        "cases": cases,
        "counts": {
            "windows": len(cases),
            "physical_pairs": len(all_rows),
            "candidate_m_rows": sum(
                len(row["lap_band_table"]["m_rows"]) for row in all_rows
            ),
            "integer_lap_pairs_counted": sum(
                row["lap_band_component_count"] for row in all_rows
            ),
            "eligible_pairs_total": sum(row["eligible"] for row in all_rows),
            "selector_charged_pairs": sum(
                row["cost_category"] == "selector_charged" for row in all_rows
            ),
            "diagnostic_selector_pairs": sum(
                row["cost_category"] == "diagnostic_selector" for row in all_rows
            ),
            "ineligible_audit_pairs": sum(
                row["cost_category"] == "all_pair_audit_only" for row in all_rows
            ),
            **comparisons,
        },
        "findings": {
            "all_24_formula_counts_match_interval_components": True,
            "all_four_formula_selections_match_prior_selector": True,
            "target_selection": cases["collective_target"]["formula_selected_base_pair"],
            "strict_16_tie_selection": cases["strict_16"]["formula_selected_base_pair"],
            "doubling_112_diagnostic_selection": cases["doubling_112"]["formula_selected_base_pair"],
            "tight_13_selection": cases["tight_13"]["formula_selected_base_pair"],
        },
        "limits": [
            "Finite agreement on four archived windows is OBSERVED, not a general selector theorem.",
            "The elementary lap-band count identity is a proof candidate awaiting independent review.",
            "The formula still iterates speed-dependent lap labels; no constant-time or uniform-runtime claim is made.",
            "The doubling_112 selection is diagnostic after its prior pair-only-positive exit.",
            "The tight_13 isolated equality at 3/8 is separate from positive component counting.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(serialize(build()), indent=2, sort_keys=False) + "\n"
    if args.write:
        OUT.write_text(rendered)
        print(f"wrote {OUT.relative_to(ROOT)}")
    else:
        assert OUT.read_text() == rendered
        print(f"verified {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
