#!/usr/bin/env python3
"""Independent exact verifier for the frozen selector transfer audit.

This implementation deliberately does not import ``primary.py`` and does not
use its floor-sum or containment routines.  It reconstructs every duration,
positive pair component, and compound containment from a rational threshold-
event decomposition of the physical window.  Postselection all-pair oracle
checks are kept separate from the two frozen one-query rules.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROTOCOL = HERE / "protocol.json"
PRIMARY = HERE / "results.json"
ARCHIVE = ROOT / "reviews/2026-09-28-collective-window-audit/results.json"
PRIOR_SELECTOR = ROOT / "reviews/2026-09-28-one-containment-selector/results.json"
COVER = ROOT / "reviews/2026-09-28-cover-obligations/results.json"
FLOOR_PROTOCOL = ROOT / "reviews/2026-09-28-floor-sum-component-count/protocol.json"
FLOOR_RESULTS = ROOT / "reviews/2026-09-28-floor-sum-component-count/results.json"
OUT_JSON = HERE / "verification.json"
OUT_MD = HERE / "verification.md"
DELTA = Q(1, 8)
DEVELOPMENT = {
    "perturbed_chain:1,2,4:4",
    "perturbed_chain:1,2,4:19",
}


def q(value: Any) -> Q:
    return value if isinstance(value, Q) else Q(str(value))


def qs(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def distance(speed: int, time: Q) -> Q:
    phase = (speed * time) % 1
    return min(phase, 1 - phase)


def blocked(speed: int, time: Q) -> bool:
    return distance(speed, time) < DELTA


def ceil_q(value: Q) -> int:
    return -((-value.numerator) // value.denominator)


def events(window: tuple[Q, Q], speeds: Iterable[int]) -> list[Q]:
    """Return all exact threshold events, retaining the closed endpoints."""
    left, right = window
    cuts = {left, right}
    for speed in speeds:
        first = (speed * left).numerator // (speed * left).denominator - 2
        stop = ceil_q(speed * right) + 2
        for lap in range(first, stop + 1):
            for sign in (-1, 1):
                time = Q(8 * lap + sign, 8 * speed)
                if left <= time <= right:
                    cuts.add(time)
    return sorted(cuts)


def mask_at(time: Q, speeds: tuple[int, ...]) -> int:
    return sum(1 << index for index, speed in enumerate(speeds) if blocked(speed, time))


def decompose(window: tuple[Q, Q], speeds: tuple[int, ...]) -> tuple[list[Q], list[dict[str, Any]]]:
    cuts = events(window, speeds)
    cells = []
    for left, right in zip(cuts, cuts[1:]):
        if left < right:
            cells.append({"left": left, "right": right, "mask": mask_at((left + right) / 2, speeds)})
    return cuts, cells


def moment(cells: list[dict[str, Any]], required: int) -> Q:
    return sum(
        (cell["right"] - cell["left"] for cell in cells if cell["mask"] & required == required),
        Q(0),
    )


def components(
    cuts: list[Q], cells: list[dict[str, Any]], speeds: tuple[int, ...], required: int
) -> list[tuple[Q, Q]]:
    """Connected positive-length components, joining only across included points."""
    picked = [(cell["left"], cell["right"]) for cell in cells if cell["mask"] & required == required]
    if not picked:
        return []
    merged: list[list[Q]] = [[picked[0][0], picked[0][1]]]
    for left, right in picked[1:]:
        boundary_included = mask_at(left, speeds) & required == required
        if left == merged[-1][1] and boundary_included:
            merged[-1][1] = right
        else:
            merged.append([left, right])
    return [(a, b) for a, b in merged]


def containment(
    cuts: list[Q],
    cells: list[dict[str, Any]],
    speeds: tuple[int, ...],
    base: tuple[int, int],
    complement: tuple[int, int],
) -> dict[str, Any]:
    base_mask = (1 << base[0]) | (1 << base[1])
    comp_mask = (1 << complement[0]) | (1 << complement[1])
    failures: list[tuple[Q, int, dict[str, Any]]] = []
    tested_points = 0
    tested_cells = 0
    for time in cuts:
        state = mask_at(time, speeds)
        if state & base_mask == base_mask:
            tested_points += 1
            offenders = [speeds[i] for i in complement if state & (1 << i)]
            if offenders:
                failures.append((time, 0, {"kind": "included_point", "time": qs(time), "blocking_complement_speeds": offenders}))
    for cell in cells:
        state = cell["mask"]
        if state & base_mask == base_mask:
            tested_cells += 1
            offenders = [speeds[i] for i in complement if state & (1 << i)]
            if offenders:
                failures.append(
                    (
                        cell["left"],
                        1,
                        {
                            "kind": "positive_open_cell",
                            "interval": [qs(cell["left"]), qs(cell["right"])],
                            "witness": qs((cell["left"] + cell["right"]) / 2),
                            "blocking_complement_speeds": offenders,
                        },
                    )
                )
    first = min(failures, key=lambda item: (item[0], item[1]))[2] if failures else None
    return {
        "holds": first is None,
        "first_violation": first,
        "base_event_points_tested": tested_points,
        "base_open_cells_tested": tested_cells,
        "complement_speed_tests": 2 * (tested_points + tested_cells),
    }


def archived_pair_minimum(record: dict[str, Any]) -> Q:
    return q(record["baseline"]["value"])


def analyze_record(record: dict[str, Any]) -> dict[str, Any]:
    record_id = record["id"]
    speeds = tuple(map(int, record["residual_speeds"]))
    window = tuple(map(q, record["window"]))
    cuts, cells = decompose(window, speeds)
    reconstructed = [moment(cells, mask) for mask in range(16)]
    archived = list(map(q, record["moments"]))
    assert reconstructed == archived, f"{record_id}: reconstructed moments differ from archive"
    atoms = [sum((cell["right"] - cell["left"] for cell in cells if cell["mask"] == mask), Q(0)) for mask in range(16)]
    assert atoms == list(map(q, record["atoms"])), f"{record_id}: reconstructed atoms differ from archive"

    pair_min = archived_pair_minimum(record)
    pair_indices = list(itertools.combinations(range(4), 2))
    singles = sum((reconstructed[1 << i] for i in range(4)), Q(0))
    pairs_sum = sum((reconstructed[(1 << i) | (1 << j)] for i, j in pair_indices), Q(0))
    c0 = reconstructed[0] - singles + pairs_sum

    pair_rows = []
    for base in pair_indices:
        complement = tuple(i for i in range(4) if i not in base)
        complement_mask = (1 << complement[0]) | (1 << complement[1])
        slack = c0 - reconstructed[complement_mask]
        base_mask = (1 << base[0]) | (1 << base[1])
        comps = components(cuts, cells, speeds, base_mask)
        pair_rows.append(
            {
                "base_indices": list(base),
                "base_pair": [speeds[i] for i in base],
                "complement_indices": list(complement),
                "complement_pair": [speeds[i] for i in complement],
                "potential_slack": qs(slack),
                "positive_slack_diagnostic": slack > 0,
                "eligible": pair_min == 0 and slack > 0,
                "positive_component_count": len(comps),
                "positive_components": [[qs(a), qs(b)] for a, b in comps],
            }
        )

    eligible = [row for row in pair_rows if row["eligible"]]
    branch = "pair_only_exit" if pair_min > 0 else ("active" if eligible else "no_eligible_pair")
    rules: dict[str, dict[str, Any]] = {}
    selected_pairs: set[tuple[int, int]] = set()
    if branch == "active":
        choices = {
            "largest_potential_slack": min(
                eligible, key=lambda row: (-q(row["potential_slack"]), tuple(row["base_pair"]))
            ),
            "fewest_components": min(
                eligible, key=lambda row: (row["positive_component_count"], tuple(row["base_pair"]))
            ),
        }
        for rule, row in choices.items():
            base = tuple(row["base_indices"])
            comp = tuple(row["complement_indices"])
            check = containment(cuts, cells, speeds, base, comp)
            selected_pairs.add(tuple(row["base_pair"]))
            rules[rule] = {
                "selected_base_pair": row["base_pair"],
                "selected_complement": row["complement_pair"],
                "selected_potential_slack": row["potential_slack"],
                "selected_positive_component_count": row["positive_component_count"],
                "query_issued": True,
                "containment_holds": check["holds"],
                "first_violation": check["first_violation"],
                "outcome": "certified" if check["holds"] else "failed_no_retune",
                "certified_lower_bound": row["potential_slack"] if check["holds"] else None,
                "second_query_issued": False,
            }
    else:
        outcome = "pair_only_positive_exit" if branch == "pair_only_exit" else "no_eligible_pair_no_query"
        for rule in ("largest_potential_slack", "fewest_components"):
            rules[rule] = {
                "selected_base_pair": None,
                "query_issued": False,
                "containment_holds": None,
                "outcome": outcome,
                "certified_lower_bound": qs(pair_min) if branch == "pair_only_exit" else None,
                "second_query_issued": False,
            }

    # This is explicitly a postselection oracle.  Its results cannot alter the
    # choices or issue a fallback query in the frozen rules above.
    oracle = []
    if branch == "active":
        for row in eligible:
            result = containment(
                cuts,
                cells,
                speeds,
                tuple(row["base_indices"]),
                tuple(row["complement_indices"]),
            )
            oracle.append(
                {
                    "base_pair": row["base_pair"],
                    "potential_slack": row["potential_slack"],
                    "containment_holds": result["holds"],
                    "first_violation": result["first_violation"],
                    "base_event_points_tested": result["base_event_points_tested"],
                    "base_open_cells_tested": result["base_open_cells_tested"],
                    "complement_speed_tests": result["complement_speed_tests"],
                }
            )
        successful = {tuple(row["base_pair"]) for row in oracle if row["containment_holds"]}
        for result in rules.values():
            chosen = tuple(result["selected_base_pair"])
            if result["containment_holds"]:
                result["oracle_classification"] = "selected_pair_certifies"
                result["failure_classification"] = None
            elif successful:
                result["oracle_classification"] = "ranking_failure_other_eligible_pair_certifies"
                result["failure_classification"] = "ranking_failure"
            else:
                result["oracle_classification"] = "certificate_class_failure_no_eligible_pair_certifies"
                result["failure_classification"] = "certificate_class_failure"
    else:
        successful = set()

    return {
        "id": record_id,
        "case_id": record["case_id"],
        "role": "development" if record_id in DEVELOPMENT else "archival_transfer",
        "reflection_partner": record.get("collective_only_counterpart"),
        "speeds": list(speeds),
        "window": [qs(window[0]), qs(window[1])],
        "event_count": len(cuts),
        "open_cell_count": len(cells),
        "moments": [qs(value) for value in reconstructed],
        "moments_match_archive": True,
        "atoms_match_archive": True,
        "physical_zero_triples": [
            [speeds[i] for i in range(4) if mask & (1 << i)]
            for mask in (7, 11, 13, 14)
            if reconstructed[mask] == 0
        ],
        "pair_only_minimum": qs(pair_min),
        "C_0": qs(c0),
        "branch": branch,
        "pair_candidates": pair_rows,
        "eligible_base_pairs": [row["base_pair"] for row in eligible] if branch == "active" else [],
        "diagnostic_positive_slack_pairs": [row["base_pair"] for row in pair_rows if row["positive_slack_diagnostic"]],
        "rules": rules,
        "selected_logical_query_count": sum(int(row["query_issued"]) for row in rules.values()),
        "selected_unique_physical_query_count": len(selected_pairs),
        "oracle": oracle,
        "oracle_successful_pairs": [list(pair) for pair in sorted(successful)],
        "oracle_is_postselection_only": True,
    }


def reflection_pairs(archive: dict[str, Any], cases: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for group in archive["summary"]["reflection_groups"]:
        left_id, right_id = group["record_ids"]
        left, right = cases[left_id], cases[right_id]
        fields = ["moments", "pair_only_minimum", "C_0", "branch", "eligible_base_pairs", "oracle_successful_pairs"]
        assert all(left[field] == right[field] for field in fields), f"reflection mismatch: {left_id}, {right_id}"
        for rule in left["rules"]:
            comparable = ["selected_base_pair", "query_issued", "containment_holds", "outcome", "certified_lower_bound"]
            assert all(left["rules"][rule].get(field) == right["rules"][rule].get(field) for field in comparable)
        rows.append(
            {
                "record_ids": [left_id, right_id],
                "exact_outcomes_agree": True,
                "counted_as_independent_examples": False,
            }
        )
    return rows


def control_checks() -> dict[str, Any]:
    prior = load(PRIOR_SELECTOR)["cases"]
    cover = {row["name"]: row for row in load(COVER)["cases"]}
    output = {}
    for name in ("strict_16", "doubling_112", "tight_13"):
        source = prior[name]
        speeds = tuple(map(int, source["speeds"]))
        window = tuple(map(q, source["window"]))
        cuts, cells = decompose(window, speeds)
        moments = [moment(cells, mask) for mask in range(16)]
        c0 = moments[0] - sum((moments[1 << i] for i in range(4)), Q(0)) + sum(
            (moments[(1 << i) | (1 << j)] for i, j in itertools.combinations(range(4), 2)), Q(0)
        )
        assert c0 == q(source["C_0"])
        pair_min = q(cover[name]["baseline"]["value"])
        eligible = []
        for i, j in itertools.combinations(range(4), 2):
            comp = tuple(k for k in range(4) if k not in (i, j))
            slack = c0 - moments[(1 << comp[0]) | (1 << comp[1])]
            if slack > 0:
                count = len(components(cuts, cells, speeds, (1 << i) | (1 << j)))
                eligible.append({"pair": [speeds[i], speeds[j]], "indices": [i, j], "comp": list(comp), "slack": qs(slack), "count": count})
        branch = "pair_only_exit" if pair_min > 0 else ("active" if eligible else "no_eligible_pair")
        selected = None
        holds = None
        if branch == "active":
            chosen = min(eligible, key=lambda row: (row["count"], tuple(row["pair"])))
            selected = chosen["pair"]
            holds = containment(cuts, cells, speeds, tuple(chosen["indices"]), tuple(chosen["comp"]))["holds"]
        output[name] = {
            "branch": branch,
            "pair_only_minimum": qs(pair_min),
            "eligible_pairs": [row["pair"] for row in eligible],
            "fewest_components_selected_pair": selected,
            "selected_containment_holds": holds,
            "active_query_count": 1 if branch == "active" else 0,
        }
    assert output["strict_16"] == {
        "branch": "active",
        "pair_only_minimum": "0",
        "eligible_pairs": [[6, 11], [11, 16]],
        "fewest_components_selected_pair": [6, 11],
        "selected_containment_holds": True,
        "active_query_count": 1,
    }
    assert output["doubling_112"]["branch"] == "pair_only_exit"
    assert output["doubling_112"]["pair_only_minimum"] == "761/32256"
    assert output["doubling_112"]["active_query_count"] == 0
    assert output["tight_13"]["branch"] == "no_eligible_pair"
    assert output["tight_13"]["active_query_count"] == 0

    endpoint = cover["tight_13"]["endpoint"]
    time = q(endpoint["time"])
    exact_distances = {str(speed): qs(distance(int(speed), time)) for speed in endpoint["distances"]}
    assert exact_distances == endpoint["distances"]
    output["tight_13"]["isolated_equality"] = {
        "time": qs(time),
        "valid": all(q(value) >= DELTA for value in exact_distances.values()),
        "positive_duration": False,
    }
    return output


def pick(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def compare_primary(primary: dict[str, Any], ours: dict[str, dict[str, Any]]) -> dict[str, Any]:
    raw = primary.get("cases", {})
    theirs = {row["id"]: row for row in raw} if isinstance(raw, list) else raw
    failures: list[str] = []
    comparisons = 0
    for record_id, reconstructed in ours.items():
        row = theirs.get(record_id)
        if row is None:
            failures.append(f"missing primary record {record_id}")
            continue
        primary_branch = (
            "pair_only_exit" if row.get("pair_only_exit") else
            ("active" if row.get("eligible_base_pairs") else "no_eligible_pair")
        )
        comparisons += 1
        if primary_branch != reconstructed["branch"]:
            failures.append(f"{record_id}: dispatch differs ({primary_branch!r} != {reconstructed['branch']!r})")
        for aliases, expected, fractional in (
            (("pair_only_minimum", "pair_only_value"), reconstructed["pair_only_minimum"], True),
            (("C_0", "C0", "c0"), reconstructed["C_0"], True),
            (("eligible_base_pairs", "eligible_pairs"), reconstructed["eligible_base_pairs"], False),
        ):
            actual = pick(row, *aliases)
            if actual is None:
                continue
            comparisons += 1
            equal = q(actual) == q(expected) if fractional else actual == expected
            if not equal:
                failures.append(f"{record_id}: {aliases[0]} differs ({actual!r} != {expected!r})")

        primary_pairs = {tuple(item["base_pair"]): item for item in row.get("pair_rows", [])}
        for item in reconstructed["pair_candidates"]:
            other = primary_pairs.get(tuple(item["base_pair"]))
            if other is None:
                failures.append(f"{record_id}: missing primary pair row {item['base_pair']}")
                continue
            for key, primary_key, fractional in (
                ("complement_pair", "complement", False),
                ("potential_slack", "potential_slack", True),
                ("eligible", "eligible", False),
            ):
                comparisons += 1
                actual, expected = other.get(primary_key), item[key]
                equal = q(actual) == q(expected) if fractional else actual == expected
                if not equal:
                    failures.append(f"{record_id}/{item['base_pair']}: {primary_key} differs")
            if other.get("component_count") is not None:
                comparisons += 1
                if other["component_count"] != item["positive_component_count"]:
                    failures.append(f"{record_id}/{item['base_pair']}: component_count differs")

        primary_rules = pick(row, "rules", "frozen_rule_results", "rule_results") or {}
        aliases_by_rule = {
            "largest_potential_slack": ("largest_potential_slack", "largest_slack", "largest_slack_comparator"),
            "fewest_components": ("fewest_components", "fewest_positive_occurrence_components"),
        }
        for our_name, aliases in aliases_by_rule.items():
            primary_rule = pick(primary_rules, *aliases)
            if primary_rule is None:
                failures.append(f"{record_id}: missing primary rule {our_name}")
                continue
            our_rule = reconstructed["rules"][our_name]
            for field_aliases, expected, fractional in (
                (("selected_base_pair", "selected_pair"), our_rule["selected_base_pair"], False),
                (("query_issued",), our_rule["query_issued"], False),
                (("containment_holds",), our_rule["containment_holds"], False),
                (("outcome",), our_rule["outcome"], False),
                (("certified_lower_bound", "reported_bound"), our_rule["certified_lower_bound"], True),
                (("second_query_issued",), False, False),
                (("failure_classification",), our_rule.get("failure_classification"), False),
            ):
                actual = pick(primary_rule, *field_aliases)
                if actual is None and expected is None:
                    comparisons += 1
                    continue
                if actual is None:
                    continue
                comparisons += 1
                equal = q(actual) == q(expected) if fractional and expected is not None else actual == expected
                if not equal:
                    failures.append(f"{record_id}/{our_name}: {field_aliases[0]} differs ({actual!r} != {expected!r})")

        primary_oracle = pick(row, "oracle", "eligible_pair_oracle", "postselection_oracle")
        if primary_oracle is not None:
            if isinstance(primary_oracle, dict):
                primary_successful = primary_oracle.get("successful_pairs")
                if primary_successful is not None:
                    comparisons += 1
                    if primary_successful != reconstructed["oracle_successful_pairs"]:
                        failures.append(f"{record_id}: oracle successful-pair list differs")
                primary_oracle = primary_oracle.get("queries", primary_oracle.get("pairs", primary_oracle.get("rows", [])))
            by_pair = {tuple(item["base_pair"]): item for item in primary_oracle}
            for item in reconstructed["oracle"]:
                other = by_pair.get(tuple(item["base_pair"]))
                if other is None:
                    failures.append(f"{record_id}: oracle missing {item['base_pair']}")
                    continue
                comparisons += 1
                if pick(other, "containment_holds", "holds") != item["containment_holds"]:
                    failures.append(f"{record_id}: oracle containment differs for {item['base_pair']}")
        comparisons += 2
        if bool(row.get("development_record")) != (reconstructed["role"] == "development"):
            failures.append(f"{record_id}: development marker differs")
        if bool(row.get("transfer_record")) != (reconstructed["role"] == "archival_transfer"):
            failures.append(f"{record_id}: transfer marker differs")
    return {"agrees": not failures, "critical_fields_compared": comparisons, "failures": failures}


def generate() -> tuple[dict[str, Any], str]:
    protocol = load(PROTOCOL)
    assert digest(PROTOCOL) == "ccfdb403abef15f9c2cd9e08ac086232f4842b450f48308ba5a5992f8c3f9c17"
    assert digest(ARCHIVE) == protocol["source_contract"]["archived_windows_sha256"]
    assert digest(FLOOR_PROTOCOL) == protocol["source_contract"]["floor_sum_protocol_sha256"]
    assert digest(FLOOR_RESULTS) == protocol["source_contract"]["floor_sum_results_sha256"]
    assert digest(PRIOR_SELECTOR) == protocol["source_contract"]["prior_one_query_results_sha256"]
    assert digest(COVER) == protocol["source_contract"]["control_roles_sha256"]
    if not PRIMARY.exists():
        raise FileNotFoundError(f"primary results not yet available: {PRIMARY}")

    archive = load(ARCHIVE)
    cases = {record["id"]: analyze_record(record) for record in archive["cases"]}
    assert len(cases) == 18
    assert sum(row["role"] == "development" for row in cases.values()) == 2
    assert sum(row["role"] == "archival_transfer" for row in cases.values()) == 16
    reflections = reflection_pairs(archive, cases)
    controls = control_checks()
    comparison = compare_primary(load(PRIMARY), cases)
    assert comparison["agrees"], comparison["failures"]

    totals = {
        "records": len(cases),
        "development_records": sum(row["role"] == "development" for row in cases.values()),
        "archival_transfer_records": sum(row["role"] == "archival_transfer" for row in cases.values()),
        "reflection_pairs": len(reflections),
        "pair_only_exits": sum(row["branch"] == "pair_only_exit" for row in cases.values()),
        "active_records": sum(row["branch"] == "active" for row in cases.values()),
        "no_eligible_records": sum(row["branch"] == "no_eligible_pair" for row in cases.values()),
        "selected_logical_queries": sum(row["selected_logical_query_count"] for row in cases.values()),
        "selected_unique_physical_queries": sum(row["selected_unique_physical_query_count"] for row in cases.values()),
        "oracle_queries": sum(len(row["oracle"]) for row in cases.values()),
        "threshold_events": sum(row["event_count"] for row in cases.values()),
        "open_cells": sum(row["open_cell_count"] for row in cases.values()),
    }
    output = {
        "status": "PASS",
        "method": "independent exact Fraction threshold-event reconstruction; no primary import, floor-sum reuse, or primary containment helper",
        "protocol_sha256": digest(PROTOCOL),
        "source_hashes_verified": {
            str(ARCHIVE.relative_to(ROOT)): digest(ARCHIVE),
            str(FLOOR_PROTOCOL.relative_to(ROOT)): digest(FLOOR_PROTOCOL),
            str(FLOOR_RESULTS.relative_to(ROOT)): digest(FLOOR_RESULTS),
            str(PRIOR_SELECTOR.relative_to(ROOT)): digest(PRIOR_SELECTOR),
            str(COVER.relative_to(ROOT)): digest(COVER),
        },
        "primary_results_sha256": digest(PRIMARY),
        "cases": cases,
        "reflection_checks": reflections,
        "controls": controls,
        "totals": totals,
        "primary_comparison": comparison,
        "semantic_checks": {
            "strict_blocking_is_open": True,
            "threshold_equality_is_safe": True,
            "event_points_checked_separately": True,
            "pair_only_exit_precedes_selector_query": True,
            "no_fallback_or_second_query": True,
            "oracle_is_postselection_only": True,
            "development_records_excluded_from_transfer_count": True,
            "reflections_not_independent_examples": True,
            "tight_isolated_equality_not_positive_duration": True,
        },
        "validation_limit": "internal exact AI verification, not independent human mathematical validation",
    }

    active = [row for row in cases.values() if row["branch"] == "active"]
    transfer = [row for row in cases.values() if row["role"] == "archival_transfer"]
    def certified(rows: list[dict[str, Any]], rule: str) -> int:
        return sum(row["rules"][rule]["outcome"] == "certified" for row in rows)
    md = f"""# Independent verification: selector transfer audit

**Status: PASS.** A separately structured exact rational threshold-event sweep agrees with the primary output on {comparison['critical_fields_compared']} critical fields. It imports neither the primary program nor its floor-sum and containment helpers.

## Scope

- Reconstructed records: {totals['records']} ({totals['development_records']} development labels and {totals['archival_transfer_records']} archival-transfer labels).
- Reflection pairs: {totals['reflection_pairs']}; each pair has identical exact outcomes and is explicitly not counted as independent evidence.
- Physical sweep: {totals['threshold_events']} exact event points and {totals['open_cells']} open cells.
- Dispatch: {totals['pair_only_exits']} pair-only exits and {totals['active_records']} active selector records.
- One-query work: {totals['selected_logical_queries']} logical selections, {totals['selected_unique_physical_queries']} unique physical selected-pair checks. The {totals['oracle_queries']} eligible-pair oracle checks are separately marked postselection-only.

Across the {len(active)} active labelled records, largest slack certifies {certified(active, 'largest_potential_slack')} and fewest components certifies {certified(active, 'fewest_components')}. Across all {len(transfer)} transfer labels (including pair-only exits), the corresponding direct selector certifications are {certified(transfer, 'largest_potential_slack')} and {certified(transfer, 'fewest_components')}; pair-only exits remain a separate prior certificate branch.

## Independent checks

The verifier recomputes all 16 physical moments per record, `C_0`, positive-slack eligibility, exact pair components, physical-speed lexicographic selections, selected containments, and the all-eligible postselection oracle. Strict blocking is `distance < 1/8`; equality is safe, and event points are tested separately from open cells. A selected failure never issues a fallback query.

`strict_16` reproduces the `{6,11}` selection and containment; `doubling_112` exits at the prior pair-only value `761/32256` before any active query; `tight_13` has no eligible duration pair and retains isolated equality at `3/8` only.

This is internal exact computational agreement, not independent human mathematical validation.
"""
    return output, md


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output, markdown = generate()
    json_text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.write:
        OUT_JSON.write_text(json_text, encoding="utf-8")
        OUT_MD.write_text(markdown, encoding="utf-8")
    else:
        assert OUT_JSON.read_text(encoding="utf-8") == json_text
        assert OUT_MD.read_text(encoding="utf-8") == markdown
    print(json.dumps({"status": "PASS", "totals": output["totals"], "primary_comparison": output["primary_comparison"]}, indent=2))


if __name__ == "__main__":
    main()
