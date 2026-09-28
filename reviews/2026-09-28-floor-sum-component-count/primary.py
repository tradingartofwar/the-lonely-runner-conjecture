"""Exact primary calculation for the frozen Euclidean floor-sum study.

The prearchive phase projects the prior result to speeds, windows, inherited
eligibility, and strict lap rectangles.  It then counts the open-strip lattice
points without iterating over either lap coordinate and without constructing
blocking or intersection intervals.  Archived counts, decisions, and cost
ledgers are attached only after all 24 counts and four decisions are fixed.

``--write`` deterministically creates ``results.json``.  ``--check`` is
read-only and reconstructs the complete result with exact integer/Fraction
arithmetic.
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
PROTOCOL_SHA256 = "a398539b747b9510259e5a134090f3eb6430370588d735bdec12f67260ec5724"
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


def ceil_div(numerator: int, denominator: int) -> int:
    assert denominator > 0
    return -((-numerator) // denominator)


def strict_integer_range(lower: F, upper: F) -> tuple[int, int]:
    """Inclusive integer bounds for lower < z < upper."""
    return floor(lower) + 1, ceil(upper) - 1


def add_cost(target: Counter, source: dict) -> None:
    target.update({key: int(value) for key, value in source.items()})


def floor_sum_nonnegative(
    n: int, modulus: int, coefficient: int, offset: int, cost: Counter
) -> tuple[int, list[dict]]:
    """Return sum_{i=0}^{n-1} floor((coefficient*i+offset)/modulus).

    This is the standard quotient/remainder Euclidean recurrence.  The caller
    supplies nonnegative inputs.  Trace records expose every recurrence round;
    no lap-coordinate iteration occurs here.
    """
    assert n >= 0 and modulus > 0 and coefficient >= 0 and offset >= 0
    answer = 0
    trace = []
    while True:
        cost["euclidean_rounds"] += 1
        record = {
            "n_in": n,
            "modulus_in": modulus,
            "coefficient_in": coefficient,
            "offset_in": offset,
            "answer_in": answer,
        }
        if coefficient >= modulus:
            quotient = coefficient // modulus
            remainder = coefficient % modulus
            cost["quotient_divisions"] += 1
            cost["remainder_operations"] += 1
            contribution = (n - 1) * n * quotient // 2
            answer += contribution
            coefficient = remainder
            record["coefficient_reduction"] = {
                "quotient": quotient,
                "remainder": remainder,
                "contribution": contribution,
            }
        else:
            record["coefficient_reduction"] = None
        if offset >= modulus:
            quotient = offset // modulus
            remainder = offset % modulus
            cost["quotient_divisions"] += 1
            cost["remainder_operations"] += 1
            contribution = n * quotient
            answer += contribution
            offset = remainder
            record["offset_reduction"] = {
                "quotient": quotient,
                "remainder": remainder,
                "contribution": contribution,
            }
        else:
            record["offset_reduction"] = None
        y_max = coefficient * n + offset
        cost["floor_sum_terminal_comparisons"] += 1
        record.update(
            {
                "reduced_coefficient": coefficient,
                "reduced_offset": offset,
                "y_max": y_max,
                "answer_after_reductions": answer,
            }
        )
        if y_max < modulus:
            record["terminal"] = True
            trace.append(record)
            break
        next_n = y_max // modulus
        next_offset = y_max % modulus
        cost["quotient_divisions"] += 1
        cost["remainder_operations"] += 1
        record["terminal"] = False
        record["reciprocal_step"] = {
            "next_n": next_n,
            "next_modulus": coefficient,
            "next_coefficient": modulus,
            "next_offset": next_offset,
        }
        trace.append(record)
        n, offset, modulus, coefficient = (
            next_n,
            next_offset,
            coefficient,
            modulus,
        )
    return answer, trace


def floor_sum_range(
    first: int,
    stop: int,
    coefficient: int,
    offset: int,
    modulus: int,
    cost: Counter,
) -> tuple[int, dict | None]:
    """Sum floor((coefficient*m+offset)/modulus), first <= m < stop."""
    if first >= stop:
        return 0, None
    count = stop - first
    shifted_offset = coefficient * first + offset
    normalization_quotient = shifted_offset // modulus
    normalized_offset = shifted_offset % modulus
    cost["floor_sum_range_calls"] += 1
    cost["signed_offset_normalizations"] += 1
    reduced_sum, trace = floor_sum_nonnegative(
        count, modulus, coefficient, normalized_offset, cost
    )
    total = count * normalization_quotient + reduced_sum
    return total, {
        "first": first,
        "stop_exclusive": stop,
        "term_count": count,
        "shifted_offset": shifted_offset,
        "normalization_quotient": normalization_quotient,
        "normalized_offset": normalized_offset,
        "normalized_floor_sum": reduced_sum,
        "range_floor_sum": total,
        "euclidean_trace": trace,
    }


def half_plane_count(
    *,
    K: int,
    A: int,
    Q: int,
    m_min: int,
    m_max: int,
    n_min: int,
    n_max: int,
    cost: Counter,
) -> tuple[int, dict]:
    """Count rectangle points with A*m-Q*n <= K, without a lap loop."""
    cost["strip_half_plane_calls"] += 1
    m_count = max(0, m_max - m_min + 1)
    n_count = max(0, n_max - n_min + 1)
    if m_count == 0 or n_count == 0:
        return 0, {
            "K": K,
            "empty_rectangle": True,
            "half_plane_count": 0,
        }

    # ceil((A*m-K)/Q)-n_min = floor((A*m+B)/Q)-n_min.
    B = -K + Q - 1
    cost["threshold_ceil_divisions"] += 2
    first_ge_one_raw = ceil_div(Q * (n_min + 1) - B, A)
    first_ge_n_count_raw = ceil_div(Q * (n_min + n_count) - B, A)
    stop = m_max + 1
    first_ge_one = min(stop, max(m_min, first_ge_one_raw))
    first_ge_n_count = min(stop, max(m_min, first_ge_n_count_raw))
    assert first_ge_one <= first_ge_n_count

    raw_middle_sum, range_trace = floor_sum_range(
        first_ge_one, first_ge_n_count, A, B, Q, cost
    )
    middle_count = first_ge_n_count - first_ge_one
    clipped_middle_sum = raw_middle_sum - middle_count * n_min
    saturated_count = stop - first_ge_n_count
    below_threshold_count = clipped_middle_sum + saturated_count * n_count
    rectangle_size = m_count * n_count
    result = rectangle_size - below_threshold_count
    assert 0 <= result <= rectangle_size
    return result, {
        "K": K,
        "empty_rectangle": False,
        "ceil_threshold_offset_B": B,
        "x_definition": f"floor(({A}*m+{B})/{Q})-{n_min}",
        "first_m_x_ge_1_raw": first_ge_one_raw,
        "first_m_x_ge_n_count_raw": first_ge_n_count_raw,
        "first_m_x_ge_1_clipped": first_ge_one,
        "first_m_x_ge_n_count_clipped": first_ge_n_count,
        "middle_range": [first_ge_one, first_ge_n_count],
        "middle_term_count": middle_count,
        "raw_middle_floor_sum": raw_middle_sum,
        "clipped_middle_sum": clipped_middle_sum,
        "saturated_term_count": saturated_count,
        "below_threshold_count": below_threshold_count,
        "rectangle_size": rectangle_size,
        "range_floor_sum_trace": range_trace,
        "half_plane_count": result,
    }


def floor_sum_component_count(
    pair: tuple[int, int], window: tuple[F, F]
) -> tuple[int, dict, Counter]:
    """Count open-strip rectangle points with no per-m or per-n iteration."""
    a, b = pair
    assert 0 < a < b
    left, right = window
    assert left < right
    m_lower, m_upper = a * left - DELTA, a * right + DELTA
    n_lower, n_upper = b * left - DELTA, b * right + DELTA
    m_min, m_max = strict_integer_range(m_lower, m_upper)
    n_min, n_max = strict_integer_range(n_lower, n_upper)
    A, Q, S = 8 * b, 8 * a, a + b
    cost = Counter()
    upper_count, upper_trace = half_plane_count(
        K=S - 1,
        A=A,
        Q=Q,
        m_min=m_min,
        m_max=m_max,
        n_min=n_min,
        n_max=n_max,
        cost=cost,
    )
    lower_count, lower_trace = half_plane_count(
        K=-S,
        A=A,
        Q=Q,
        m_min=m_min,
        m_max=m_max,
        n_min=n_min,
        n_max=n_max,
        cost=cost,
    )
    cost["strip_subtractions"] += 1
    count = upper_count - lower_count
    assert count >= 0
    return count, {
        "smaller_speed": a,
        "larger_speed": b,
        "m_window_open_bounds": [m_lower, m_upper],
        "n_window_open_bounds": [n_lower, n_upper],
        "m_min": m_min,
        "m_max": m_max,
        "m_count": max(0, m_max - m_min + 1),
        "n_min": n_min,
        "n_max": n_max,
        "n_count": max(0, n_max - n_min + 1),
        "scaled_coefficient_A": A,
        "scaled_n_coefficient_Q": Q,
        "scaled_open_radius_S": S,
        "integer_open_strip": [-S + 1, S - 1],
        "half_plane_upper": upper_trace,
        "half_plane_lower_subtracted": lower_trace,
        "component_count": count,
    }, cost


def project_allowed_inputs(protocol: dict, lap_archive: dict) -> dict:
    """Irreversibly retain only prearchive-contract data from the prior file."""
    allowed = {}
    for case_spec in protocol["cases"]:
        case_id = case_spec["id"]
        archived = lap_archive["cases"][case_id]
        allowed[case_id] = {
            "speeds": tuple(map(int, archived["speeds"])),
            "window": tuple(map(q, archived["window"])),
            "eligibility": {
                tuple(map(int, row["base_pair"])): bool(row["eligible"])
                for row in archived["pair_rows"]
            },
        }
    return allowed


def choose_by_count(rows: list[dict], cost: Counter):
    eligible = [row for row in rows if row["eligible"]]
    if not eligible:
        return None
    chosen = eligible[0]
    for row in eligible[1:]:
        cost["component_count_order_comparisons"] += 1
        if row["floor_sum_component_count"] < chosen["floor_sum_component_count"]:
            chosen = row
        elif row["floor_sum_component_count"] == chosen["floor_sum_component_count"]:
            cost["component_count_ties"] += 1
            cost["physical_lexicographic_tie_breaks"] += 1
            if row["base_pair"] < chosen["base_pair"]:
                chosen = row
    return chosen["base_pair"]


def build_prearchive(protocol: dict, allowed: dict) -> dict:
    cases = {}
    for case_spec in protocol["cases"]:
        case_id = case_spec["id"]
        source = allowed[case_id]
        diagnostic_case = case_id == "doubling_112"
        all_cost, charged_cost = Counter(), Counter()
        diagnostic_cost, audit_cost = Counter(), Counter()
        rows = []
        for pair in combinations(source["speeds"], 2):
            eligible = source["eligibility"][pair]
            count, table, pair_cost = floor_sum_component_count(pair, source["window"])
            category = (
                "diagnostic_selector"
                if eligible and diagnostic_case
                else "selector_charged"
                if eligible
                else "all_pair_audit_only"
            )
            row = {
                "base_pair": pair,
                "eligible": eligible,
                "cost_category": category,
                "floor_sum_component_count": count,
                "lap_rectangle_and_floor_sum_trace": table,
                "arithmetic_cost": dict(sorted(pair_cost.items())),
            }
            rows.append(row)
            all_cost.update(pair_cost)
            if category == "selector_charged":
                charged_cost.update(pair_cost)
            elif category == "diagnostic_selector":
                diagnostic_cost.update(pair_cost)
            else:
                audit_cost.update(pair_cost)
        selection_cost = Counter()
        selected = choose_by_count(rows, selection_cost)
        cases[case_id] = {
            "speeds": source["speeds"],
            "window": source["window"],
            "eligible_base_pairs": [row["base_pair"] for row in rows if row["eligible"]],
            "pair_rows": rows,
            "floor_sum_selected_base_pair": selected,
            "diagnostic_only_after_pair_exit": diagnostic_case,
            "cost": {
                "floor_sum_all_six_pairs": dict(sorted(all_cost.items())),
                "floor_sum_selector_charged": dict(sorted(charged_cost.items())),
                "floor_sum_diagnostic_selector": dict(sorted(diagnostic_cost.items())),
                "floor_sum_ineligible_all_pair_audit_only": dict(sorted(audit_cost.items())),
                "floor_sum_selection": dict(sorted(selection_cost.items())),
            },
        }
    return cases


def aggregate_prior_row_cost(case: dict, category: str) -> dict:
    total = Counter()
    for row in case["pair_rows"]:
        if row["cost_category"] == category:
            add_cost(total, row["arithmetic_cost"])
    return dict(sorted(total.items()))


def add_postselection_comparisons(
    cases: dict, lap_archive: dict, interval_archive: dict
) -> dict:
    comparisons = Counter()
    for case_id, case in cases.items():
        prior_case = lap_archive["cases"][case_id]
        interval_case = interval_archive["cases"][case_id]
        prior_rows = {
            tuple(row["base_pair"]): row for row in prior_case["pair_rows"]
        }
        interval_rows = {
            tuple(row["base_pair"]): row
            for row in interval_case["all_six_potential_slacks"]
        }
        for row in case["pair_rows"]:
            pair = tuple(row["base_pair"])
            prior_row = prior_rows[pair]
            interval_row = interval_rows[pair]
            prior_count = prior_row["lap_band_component_count"]
            assert row["floor_sum_component_count"] == prior_count
            comparisons["all_pair_component_count_comparisons"] += 1
            cached_cost = interval_row["component_enumeration_cost"]
            row["postselection_archive_comparison"] = {
                "prior_lap_band_component_count": prior_count,
                "floor_sum_matches_prior_lap_band_count": True,
                "prior_row_formula_cost": prior_row["arithmetic_cost"],
                "cached_interval_enumeration_cost": cached_cost,
            }
            if cached_cost is not None:
                comparisons["eligible_cached_interval_cost_records"] += 1

        prior_selected = prior_case["formula_selected_base_pair"]
        prior_selected = None if prior_selected is None else tuple(prior_selected)
        assert case["floor_sum_selected_base_pair"] == prior_selected
        comparisons["selector_comparisons"] += 1

        prior_cost = prior_case["cost"]
        case["cost"]["postselection_row_formula_exact_reuse"] = {
            "all_six_pairs_in_this_window": prior_cost["all_six_pairs_in_this_window"],
            "selector_charged": prior_cost["selector_charged"],
            "diagnostic_selector": prior_cost["diagnostic_selector"],
            "ineligible_all_pair_audit_only": prior_cost[
                "ineligible_all_pair_audit_only"
            ],
            "selection": prior_cost["selection"],
        }
        case["cost"]["postselection_cached_interval_exact_reuse"] = (
            interval_case["prequery_information_and_cost"]["component_count_extension"]
        )
        case["postselection_archived_decision"] = {
            "prior_lap_band_selected_base_pair": prior_selected,
            "floor_sum_reproduces_prior_selection": True,
            "prior_interval_selected_base_pair": interval_case["frozen_rule_results"][
                "fewest_positive_occurrence_components"
            ]["selected_base_pair"],
            "pair_only_exit": interval_case["pair_only_exit"],
            "isolated_equality_endpoint": interval_case["isolated_equality_endpoint"],
        }
    return dict(sorted(comparisons.items()))


def sum_category(cases: dict, floor_key: str) -> Counter:
    total = Counter()
    for case in cases.values():
        total.update(case["cost"][floor_key])
    return total


def sum_prior_category(cases: dict, category: str) -> Counter:
    total = Counter()
    for case in cases.values():
        prior = case["cost"]["postselection_row_formula_exact_reuse"]
        total.update(prior[category])
    return total


def sum_cached_interval_cases(cases: dict, case_ids: tuple[str, ...]) -> Counter:
    total = Counter()
    for case_id in case_ids:
        ledger = cases[case_id]["cost"][
            "postselection_cached_interval_exact_reuse"
        ]
        total.update({key: int(value) for key, value in ledger.items()})
    return total


def loop_comparison(floor_cost: Counter, row_cost: Counter) -> dict:
    rounds = floor_cost["euclidean_rounds"]
    rows = row_cost["m_rows"]
    relation = "less" if rounds < rows else "equal" if rounds == rows else "greater"
    return {
        "floor_sum_euclidean_rounds": rounds,
        "row_formula_m_rows": rows,
        "rounds_vs_rows": relation,
        "warning": "These loop units are not equal-cost primitives; no runtime inference is made.",
    }


def build() -> dict:
    assert sha256(PROTOCOL) == PROTOCOL_SHA256
    protocol = json.loads(PROTOCOL.read_text())
    source = protocol["source_contract"]
    source_paths = {
        "lap_band_results": ROOT / source["lap_band_results"],
        "cached_interval_results": ROOT / source["cached_interval_results"],
        "physical_geometry": ROOT / source["physical_geometry"],
    }
    for key, path in source_paths.items():
        assert sha256(path) == source[f"{key}_sha256"]

    # Phase 1: access only fields authorized by project_allowed_inputs.  The
    # archive object is discarded before any floor-sum calculation begins.
    lap_source = json.loads(source_paths["lap_band_results"].read_text())
    allowed = project_allowed_inputs(protocol, lap_source)
    del lap_source
    cases = build_prearchive(protocol, allowed)

    # Endpoint unit control permitted by the protocol: D=-S is contact and is
    # removed by H(S-1)-H(-S).  It is not a new selector case.
    negative_equality_contact_D = 8 * 5 * 1 - 8 * 3 * 2
    positive_equality_contact_D = 8 * 5 * 2 - 8 * 3 * 3
    assert negative_equality_contact_D == -(3 + 5)
    assert positive_equality_contact_D == 3 + 5

    # Phase 2: reload archives only after all counts and branch records are fixed.
    lap_archive = json.loads(source_paths["lap_band_results"].read_text())
    interval_archive = json.loads(source_paths["cached_interval_results"].read_text())
    comparisons = add_postselection_comparisons(cases, lap_archive, interval_archive)

    all_rows = [row for case in cases.values() for row in case["pair_rows"]]
    floor_all = sum_category(cases, "floor_sum_all_six_pairs")
    floor_charged = sum_category(cases, "floor_sum_selector_charged")
    floor_diagnostic = sum_category(cases, "floor_sum_diagnostic_selector")
    floor_audit = sum_category(cases, "floor_sum_ineligible_all_pair_audit_only")
    row_all = sum_prior_category(cases, "all_six_pairs_in_this_window")
    row_charged = sum_prior_category(cases, "selector_charged")
    row_diagnostic = sum_prior_category(cases, "diagnostic_selector")
    row_audit = sum_prior_category(cases, "ineligible_all_pair_audit_only")
    interval_charged = sum_cached_interval_cases(
        cases, ("collective_target", "strict_16", "tight_13")
    )
    interval_diagnostic = sum_cached_interval_cases(cases, ("doubling_112",))

    return {
        "baseline": protocol["baseline"],
        "protocol_sha256": PROTOCOL_SHA256,
        "primary_sha256": sha256(Path(__file__)),
        "source_contract": source,
        "arithmetic": "integers and fractions.Fraction only; no floating-point decisions",
        "counter": {
            "scaled_difference": "D=8*b*m-8*a*n",
            "open_strip": "-S+1 <= D <= S-1, where S=a+b",
            "half_plane_difference": "H(S-1)-H(-S)",
            "lap_iteration": "none",
            "floor_sum": "signed-offset normalization followed by quotient/remainder Euclidean recurrence",
            "cost_conventions": {
                "threshold_ceil_divisions": "Two exact threshold-index ceil divisions per nonempty half-plane call.",
                "signed_offset_normalizations": "One quotient/remainder normalization per nonempty middle range; kept separate from recurrence quotient/remainder counts.",
                "quotient_divisions_and_remainders": "Only variable-modulus operations inside the nonnegative Euclidean recurrence.",
                "floor_sum_terminal_comparisons": "One y_max<modulus comparison per Euclidean round.",
            },
        },
        "information_barrier": (
            "All 24 floor-sum counts and all four branch records were fixed from "
            "speeds, windows, inherited eligibility and derived strict lap "
            "rectangles before archived counts, choices, outcomes, or cost "
            "ledgers were accessed."
        ),
        "primary_forbidden_structures": {
            "per_m_loops": 0,
            "per_n_loops": 0,
            "blocking_interval_lists_constructed": 0,
            "pair_intersection_intervals_constructed": 0,
            "new_containment_queries": 0,
        },
        "endpoint_unit_control": {
            "a": 3,
            "b": 5,
            "S": 8,
            "contacts": [
                {
                    "m": 1,
                    "n": 2,
                    "D": negative_equality_contact_D,
                    "classification": "excluded equality D=-S",
                },
                {
                    "m": 2,
                    "n": 3,
                    "D": positive_equality_contact_D,
                    "classification": "excluded equality D=+S",
                },
            ],
            "positive_components_counted": 0,
        },
        "cases": cases,
        "counts": {
            "windows": len(cases),
            "physical_pairs": len(all_rows),
            "lattice_components_counted": sum(
                row["floor_sum_component_count"] for row in all_rows
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
        "aggregate_cost_ledgers": {
            "floor_sum": {
                "all_24_pairs": dict(sorted(floor_all.items())),
                "selector_charged": dict(sorted(floor_charged.items())),
                "doubling_diagnostic": dict(sorted(floor_diagnostic.items())),
                "ineligible_audit": dict(sorted(floor_audit.items())),
            },
            "row_formula_exact_reuse": {
                "all_24_pairs": dict(sorted(row_all.items())),
                "selector_charged": dict(sorted(row_charged.items())),
                "doubling_diagnostic": dict(sorted(row_diagnostic.items())),
                "ineligible_audit": dict(sorted(row_audit.items())),
            },
            "euclidean_rounds_vs_m_rows": {
                "all_24_pairs": loop_comparison(floor_all, row_all),
                "selector_charged": loop_comparison(floor_charged, row_charged),
                "doubling_diagnostic": loop_comparison(
                    floor_diagnostic, row_diagnostic
                ),
                "ineligible_audit": loop_comparison(floor_audit, row_audit),
            },
            "cached_interval_enumeration_exact_reuse": {
                "selector_charged": dict(sorted(interval_charged.items())),
                "doubling_diagnostic": dict(sorted(interval_diagnostic.items())),
                "scope_note": (
                    "Only eligible-pair shared-cache selector ledgers are comparable; "
                    "per-case ledgers are also preserved under cases[*].cost."
                ),
            },
            "comparison_policy": (
                "Primitive ledgers are side by side only; unlike operations are not "
                "combined into a score and imply no wall-clock ordering."
            ),
        },
        "findings": {
            "all_24_floor_sum_counts_match_prior_lap_band_counts": True,
            "all_four_archived_branch_records_match": True,
            "target_selection": cases["collective_target"][
                "floor_sum_selected_base_pair"
            ],
            "strict_16_tie_selection": cases["strict_16"][
                "floor_sum_selected_base_pair"
            ],
            "doubling_112_diagnostic_selection": cases["doubling_112"][
                "floor_sum_selected_base_pair"
            ],
            "tight_13_selection": cases["tight_13"][
                "floor_sum_selected_base_pair"
            ],
            "strict_boundary_contact_excluded": True,
        },
        "limits": [
            "The 24 exact matches are OBSERVED on four frozen windows, not held-out selector validation.",
            "The transformed floor-sum identity is an AI-assisted proof candidate, not an established or novelty claim.",
            "Euclidean rounds and lap rows are different-cost units; the side-by-side ledger supports no wall-clock claim.",
            "The floor-sum representation removes lap-row iteration but adds threshold transformations, clipping, and recurrence bookkeeping.",
            "The doubling_112 selection remains diagnostic after its prior pair-only-positive exit.",
            "The tight_13 equality at 3/8 remains separate from positive-duration component counting.",
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
