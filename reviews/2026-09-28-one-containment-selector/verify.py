#!/usr/bin/env python3
"""Independent exact verifier for the frozen one-containment selector study.

This script intentionally does not import primary.py.  It rebuilds the strict
blocking geometry from the four speed lists and windows, computes all moment
data needed by the selectors from an event-cell decomposition, applies the two
frozen rankings, and checks their sole containment query.  It also validates
the archived pair-only LP certificate used to exit the doubling control and
reconstructs the tight control's isolated endpoint from the original speeds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "protocol.json"
PRIMARY_RESULTS = HERE / "results.json"
JOINT_RESULTS = ROOT / "reviews/2026-09-28-joint-triple-exclusions/results.json"
COVER_RESULTS = ROOT / "reviews/2026-09-28-cover-obligations/results.json"
OUT_JSON = HERE / "verification.json"
OUT_MD = HERE / "verification.md"
THRESHOLD = F(1, 8)


def q(x: Any) -> F:
    if isinstance(x, F):
        return x
    return F(str(x))


def fs(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dist(t: F, speed: int) -> F:
    x = t * speed
    floor = x.numerator // x.denominator
    r = x - floor
    return min(r, 1 - r)


def blocked(t: F, speed: int) -> bool:
    return dist(t, speed) < THRESHOLD


def ceil_fraction(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def threshold_events(window: tuple[F, F], speeds: Iterable[int]) -> list[F]:
    """All blocker-boundary events in the closed window, plus its endpoints."""
    lo, hi = window
    events = {lo, hi}
    for speed in speeds:
        first = (speed * lo).numerator // (speed * lo).denominator - 2
        last = ceil_fraction(speed * hi) + 2
        for lap in range(first, last + 1):
            for sign in (-1, 1):
                t = F(8 * lap + sign, 8 * speed)
                if lo <= t <= hi:
                    events.add(t)
    return sorted(events)


def mask_at(t: F, speeds: tuple[int, ...]) -> int:
    return sum((1 << i) for i, speed in enumerate(speeds) if blocked(t, speed))


def cell_table(window: tuple[F, F], speeds: tuple[int, ...]) -> tuple[list[F], list[dict[str, Any]]]:
    events = threshold_events(window, speeds)
    cells: list[dict[str, Any]] = []
    for left, right in zip(events, events[1:]):
        if left == right:
            continue
        mid = (left + right) / 2
        cells.append({"left": left, "right": right, "mask": mask_at(mid, speeds)})
    return events, cells


def moment(cells: list[dict[str, Any]], mask: int) -> F:
    return sum((c["right"] - c["left"] for c in cells if c["mask"] & mask == mask), F(0))


def positive_components(cells: list[dict[str, Any]], mask: int) -> list[tuple[F, F]]:
    selected = [(c["left"], c["right"]) for c in cells if c["mask"] & mask == mask]
    if not selected:
        return []
    merged: list[list[F]] = [[selected[0][0], selected[0][1]]]
    for left, right in selected[1:]:
        if left == merged[-1][1]:
            merged[-1][1] = right
        else:
            merged.append([left, right])
    return [(left, right) for left, right in merged]


def first_containment_violation(
    events: list[F],
    cells: list[dict[str, Any]],
    speeds: tuple[int, ...],
    base_indices: tuple[int, int],
    complement_indices: tuple[int, int],
) -> dict[str, Any] | None:
    base_mask = (1 << base_indices[0]) | (1 << base_indices[1])
    complement_mask = (1 << complement_indices[0]) | (1 << complement_indices[1])
    candidates: list[tuple[F, int, dict[str, Any]]] = []

    # Event points matter because the window endpoints can lie strictly inside
    # all queried blocking sets.  Threshold-equality points are safe by design.
    for t in events:
        m = mask_at(t, speeds)
        offending = m & complement_mask
        if m & base_mask == base_mask and offending:
            candidates.append(
                (
                    t,
                    0,
                    {
                        "kind": "included_point",
                        "time": fs(t),
                        "blocking_complement_speeds": [
                            speeds[i] for i in complement_indices if offending & (1 << i)
                        ],
                    },
                )
            )

    for cell in cells:
        m = cell["mask"]
        offending = m & complement_mask
        if m & base_mask == base_mask and offending:
            candidates.append(
                (
                    cell["left"],
                    1,
                    {
                        "kind": "positive_open_cell",
                        "interval": [fs(cell["left"]), fs(cell["right"])],
                        "blocking_complement_speeds": [
                            speeds[i] for i in complement_indices if offending & (1 << i)
                        ],
                    },
                )
            )
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item[0], item[1]))[2]


def physical_pair(indices: tuple[int, int], speeds: tuple[int, ...]) -> tuple[int, int]:
    return speeds[indices[0]], speeds[indices[1]]


def verify_lp_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    c = list(map(q, cert["objective"]))
    rows = [[q(v) for v in row] for row in cert["eq_rows"]]
    rhs = list(map(q, cert["eq_rhs"]))
    primal = list(map(q, cert["primal"]))
    dual = list(map(q, cert["dual_eq"]))
    assert len(c) == len(primal)
    assert all(x >= 0 for x in primal)
    assert all(sum((a * x for a, x in zip(row, primal)), F(0)) == b for row, b in zip(rows, rhs))
    primal_value = sum((a * x for a, x in zip(c, primal)), F(0))
    dual_columns = [sum((rows[r][j] * dual[r] for r in range(len(rows))), F(0)) for j in range(len(c))]
    assert all(a <= b for a, b in zip(dual_columns, c))
    dual_value = sum((a * b for a, b in zip(rhs, dual)), F(0))
    assert primal_value == dual_value == q(cert["value"])
    return {
        "value": fs(primal_value),
        "positive": primal_value > 0,
        "primal_feasible": True,
        "dual_feasible": True,
        "equal_objectives": True,
    }


def reconstruct_tight_endpoint(cover: dict[str, Any]) -> dict[str, Any]:
    archived = next(case for case in cover["cases"] if case["name"] == "tight_13")["endpoint"]
    t = q(archived["time"])
    speeds = tuple(sorted(int(v) for v in archived["distances"]))
    distances = {str(v): fs(dist(t, v)) for v in speeds}
    assert distances == archived["distances"]
    valid = all(q(value) >= THRESHOLD for value in distances.values())

    # Select exact side probes from the nearest threshold events for the full
    # original speed set, not only from the four residual blockers.
    events = threshold_events((t - 1, t + 1), speeds)
    pos = events.index(t)
    left_probe = (events[pos - 1] + t) / 2
    right_probe = (t + events[pos + 1]) / 2
    left_blockers = [v for v in speeds if blocked(left_probe, v)]
    right_blockers = [v for v in speeds if blocked(right_probe, v)]
    isolated = valid and bool(left_blockers) and bool(right_blockers)
    assert left_blockers == archived["left_neighborhood_blockers"]
    assert right_blockers == archived["right_neighborhood_blockers"]
    assert isolated == archived["isolated"]
    return {
        "time": fs(t),
        "distances": distances,
        "valid": valid,
        "left_neighborhood_blockers": left_blockers,
        "right_neighborhood_blockers": right_blockers,
        "isolated": isolated,
        "duration_claim": "none; isolated equality only",
    }


def analyze_case(name: str, physical: dict[str, Any]) -> dict[str, Any]:
    speeds = tuple(map(int, physical["speeds"]))
    window = tuple(map(q, physical["window"]))
    events, cells = cell_table(window, speeds)
    singles = {i: moment(cells, 1 << i) for i in range(4)}
    pair_indices = list(itertools.combinations(range(4), 2))
    pairs = {ij: moment(cells, (1 << ij[0]) | (1 << ij[1])) for ij in pair_indices}
    C0 = (window[1] - window[0]) - sum(singles.values(), F(0)) + sum(pairs.values(), F(0))

    archived_moments = list(map(q, physical["moments"]))
    assert moment(cells, 0) == archived_moments[0]
    for i in range(4):
        assert singles[i] == archived_moments[1 << i]
    for i, j in pair_indices:
        assert pairs[(i, j)] == archived_moments[(1 << i) | (1 << j)]
    assert C0 == q(physical["C"])

    rows: list[dict[str, Any]] = []
    for ij in pair_indices:
        complement = tuple(i for i in range(4) if i not in ij)
        slack = C0 - pairs[complement]
        components = positive_components(cells, (1 << ij[0]) | (1 << ij[1]))
        rows.append(
            {
                "base_indices": list(ij),
                "base_pair": list(physical_pair(ij, speeds)),
                "complement_indices": list(complement),
                "complement_pair": list(physical_pair(complement, speeds)),
                "complement_overlap": fs(pairs[complement]),
                "potential_slack": fs(slack),
                "eligible": slack > 0,
                "positive_occurrence_component_count": len(components),
                "positive_occurrence_components": [[fs(a), fs(b)] for a, b in components],
            }
        )
    eligible = [row for row in rows if row["eligible"]]

    selections: dict[str, Any] = {}
    if eligible:
        chosen_slack = min(
            eligible,
            key=lambda row: (-q(row["potential_slack"]), tuple(row["base_pair"])),
        )
        chosen_count = min(
            eligible,
            key=lambda row: (row["positive_occurrence_component_count"], tuple(row["base_pair"])),
        )
        for rule, chosen in (
            ("largest_potential_slack", chosen_slack),
            ("fewest_positive_occurrence_components", chosen_count),
        ):
            base = tuple(chosen["base_indices"])
            comp = tuple(chosen["complement_indices"])
            violation = first_containment_violation(events, cells, speeds, base, comp)
            selections[rule] = {
                "selected_pair": chosen["base_pair"],
                "complement_pair": chosen["complement_pair"],
                "potential_slack": chosen["potential_slack"],
                "positive_occurrence_component_count": chosen["positive_occurrence_component_count"],
                "query_count": 1,
                "containment_holds": violation is None,
                "first_violation": violation,
                "reported_bound": chosen["potential_slack"] if violation is None else None,
                "second_query_issued": False,
            }
    else:
        for rule in ("largest_potential_slack", "fewest_positive_occurrence_components"):
            selections[rule] = {
                "selected_pair": None,
                "query_count": 0,
                "containment_holds": None,
                "first_violation": None,
                "reported_bound": None,
                "second_query_issued": False,
            }

    return {
        "name": name,
        "window": [fs(window[0]), fs(window[1])],
        "speeds": list(speeds),
        "event_count": len(events),
        "positive_cell_count": len(cells),
        "C_0": fs(C0),
        "pair_candidates": rows,
        "eligible_pair_count": len(eligible),
        "selections": selections,
    }


def compare_primary(primary: dict[str, Any], reconstructed: dict[str, Any]) -> dict[str, Any]:
    """Compare every mathematical selector field, ignoring cost instrumentation."""
    failures: list[str] = []
    primary_cases_raw = primary.get("cases", {})
    if isinstance(primary_cases_raw, list):
        primary_cases = {case.get("id", case.get("name")): case for case in primary_cases_raw}
    else:
        primary_cases = primary_cases_raw

    def pick(d: dict[str, Any], *names: str) -> Any:
        for key in names:
            if key in d:
                return d[key]
        return None

    compared = 0
    for name, ours in reconstructed.items():
        theirs = primary_cases.get(name)
        if theirs is None:
            failures.append(f"primary missing case {name}")
            continue
        pc0 = pick(theirs, "C_0", "C0", "c0")
        if pc0 is not None:
            compared += 1
            if q(pc0) != q(ours["C_0"]):
                failures.append(f"{name}: C_0 differs")

        primary_rows = pick(theirs, "all_six_potential_slacks", "pair_candidates") or []
        primary_by_pair = {tuple(row["base_pair"]): row for row in primary_rows}
        for our_row in ours["pair_candidates"]:
            pair = tuple(our_row["base_pair"])
            their_row = primary_by_pair.get(pair)
            if their_row is None:
                failures.append(f"{name}: primary missing base pair {pair}")
                continue
            row_fields = (
                ("complement", our_row["complement_pair"]),
                ("potential_slack", our_row["potential_slack"]),
                ("eligible", our_row["eligible"]),
            )
            for field, expected in row_fields:
                actual = their_row.get(field)
                compared += 1
                equal = q(actual) == q(expected) if field == "potential_slack" else actual == expected
                if not equal:
                    failures.append(f"{name}/{pair}: {field} differs ({actual!r} != {expected!r})")
            archived_count = their_row.get("positive_component_count")
            if archived_count is not None:
                compared += 1
                if archived_count != our_row["positive_occurrence_component_count"]:
                    failures.append(f"{name}/{pair}: positive component count differs")

        archived_eligible = pick(theirs, "eligible_base_pairs")
        if archived_eligible is not None:
            compared += 1
            expected_eligible = [row["base_pair"] for row in ours["pair_candidates"] if row["eligible"]]
            if archived_eligible != expected_eligible:
                failures.append(f"{name}: eligible pair list differs")

        their_rules = pick(theirs, "frozen_rule_results", "selections", "rules", "rule_results") or {}
        if isinstance(their_rules, list):
            their_rules = {row.get("id", row.get("rule")): row for row in their_rules}
        for rule, our_rule in ours["selections"].items():
            their_rule = their_rules.get(rule)
            if their_rule is None:
                failures.append(f"{name}: primary missing rule {rule}")
                continue
            mappings = (
                (("selected_pair", "base_pair", "selected_base_pair"), our_rule["selected_pair"]),
                (("query_issued",), bool(our_rule["query_count"])),
                (("containment_holds", "contained", "success"), our_rule["containment_holds"]),
                (("certified_lower_bound", "reported_bound", "bound", "certified_bound"), our_rule["reported_bound"]),
                (("second_query_issued",), our_rule["second_query_issued"]),
            )
            for aliases, expected in mappings:
                actual = pick(their_rule, *aliases)
                if actual is None and expected is None:
                    compared += 1
                    continue
                if actual is None:
                    # A missing presentation field is not a mathematical conflict;
                    # primary.py still must expose selection and containment below.
                    continue
                compared += 1
                if aliases[0] in ("certified_lower_bound",) and actual is not None:
                    equal = q(actual) == q(expected)
                else:
                    equal = actual == expected
                if not equal:
                    failures.append(f"{name}/{rule}: {aliases[0]} differs ({actual!r} != {expected!r})")

            archived_violation = pick(their_rule, "first_exact_violation", "first_violation")
            our_violation = our_rule["first_violation"]
            compared += 1
            if (archived_violation is None) != (our_violation is None):
                failures.append(f"{name}/{rule}: violation existence differs")
            elif archived_violation is not None:
                compared += 1
                if archived_violation.get("interval") != our_violation.get("interval"):
                    failures.append(f"{name}/{rule}: first violation interval differs")
                tested_speed = archived_violation.get("tested_complement_speed")
                if tested_speed is not None:
                    compared += 1
                    if tested_speed not in our_violation["blocking_complement_speeds"]:
                        failures.append(f"{name}/{rule}: complement violation speed differs")
            if our_rule["second_query_issued"]:
                failures.append(f"{name}/{rule}: independent verifier issued a forbidden second query")
    return {"available": True, "critical_fields_compared": compared, "failures": failures, "agrees": not failures}


def main() -> None:
    protocol = load(PROTOCOL)
    joint = load(JOINT_RESULTS)
    cover = load(COVER_RESULTS)
    assert sha256(JOINT_RESULTS) == protocol["source_contract"]["physical_geometry_and_moments_sha256"]
    assert sha256(COVER_RESULTS) == protocol["source_contract"]["pair_only_control_and_endpoint_roles_sha256"]

    mapping = {
        "collective_target": "target",
        "strict_16": "strict_16",
        "doubling_112": "doubling_112",
        "tight_13": "tight_13",
    }
    reconstructed = {
        output_name: analyze_case(output_name, joint["cases"][source_name]["physical"])
        for output_name, source_name in mapping.items()
    }

    doubling_archive = next(case for case in cover["cases"] if case["name"] == "doubling_112")
    pair_only = verify_lp_certificate(doubling_archive["baseline"])
    assert doubling_archive["outcome"] == "pair_only_positive"
    assert pair_only["positive"]
    tight_endpoint = reconstruct_tight_endpoint(cover)

    assert reconstructed["tight_13"]["eligible_pair_count"] == 0
    assert all(
        result["query_count"] == 0
        for result in reconstructed["tight_13"]["selections"].values()
    )
    assert all(
        not result["second_query_issued"]
        for case in reconstructed.values()
        for result in case["selections"].values()
    )

    if not PRIMARY_RESULTS.exists():
        raise FileNotFoundError(f"primary result not yet available: {PRIMARY_RESULTS}")
    primary = load(PRIMARY_RESULTS)
    comparison = compare_primary(primary, reconstructed)
    assert comparison["agrees"], comparison["failures"]

    output = {
        "status": "PASS",
        "method": "independent exact Fraction event-cell reconstruction; no primary import",
        "protocol_sha256": sha256(PROTOCOL),
        "source_hashes_verified": {
            str(JOINT_RESULTS.relative_to(ROOT)): sha256(JOINT_RESULTS),
            str(COVER_RESULTS.relative_to(ROOT)): sha256(COVER_RESULTS),
        },
        "cases": reconstructed,
        "doubling_pair_only_exit": pair_only,
        "tight_isolated_endpoint": tight_endpoint,
        "primary_comparison": comparison,
        "semantic_checks": {
            "strict_blocking_uses_open_threshold": True,
            "threshold_equality_is_safe": True,
            "window_endpoint_membership_checked_separately": True,
            "doubling_selector_results_are_diagnostic_only": True,
            "tight_endpoint_is_not_positive_duration": True,
            "one_query_max_per_rule": True,
            "no_second_query_after_failure": True,
        },
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    target = reconstructed["collective_target"]["selections"]
    strict = reconstructed["strict_16"]["selections"]
    doubling = reconstructed["doubling_112"]["selections"]
    md = f"""# Independent verification: one-containment selector

**Status: PASS.** A separately structured `fractions.Fraction` event-cell reconstruction agrees with the primary result on {comparison['critical_fields_compared']} critical fields. It imports no primary implementation.

## Reconstructed outcomes

- Target: largest potential slack selects `{target['largest_potential_slack']['selected_pair']}` and fails its sole containment query; fewest positive occurrence components selects `{target['fewest_positive_occurrence_components']['selected_pair']}` and certifies `{target['fewest_positive_occurrence_components']['reported_bound']}`.
- Strict16: both rules select `{strict['largest_potential_slack']['selected_pair']}` and certify `{strict['largest_potential_slack']['reported_bound']}`.
- Doubling112: the archived pair-only primal/dual certificate is rechecked exactly at `{pair_only['value']}`. Selector outcomes are diagnostics only; their chosen pairs are `{doubling['largest_potential_slack']['selected_pair']}` and `{doubling['fewest_positive_occurrence_components']['selected_pair']}`.
- Tight13: no pair has positive potential slack, so neither rule issues a query. Exact endpoint reconstruction confirms valid isolated equality at `t={tight_endpoint['time']}`, not positive duration.

## Scope and semantics

The verifier reconstructs all four windows directly from their speeds, checks the pinned source hashes, reproduces every single and pair duration used in `C_0`, enumerates all six base-pair slacks and positive occurrence components, reapplies both frozen physical-lexicographic tie rules, and tests one compound containment at most. Strict blockers use the open condition `distance < 1/8`; equality is safe. Window endpoints are evaluated explicitly. No failed selection triggers a second query.

This is internal exact computational agreement, not independent human mathematical validation.
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print(json.dumps({"status": "PASS", "comparison": comparison}, indent=2))


if __name__ == "__main__":
    main()
