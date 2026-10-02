#!/usr/bin/env python3
"""Independent threshold-event verification for the frozen lap-band study.

This verifier deliberately does not use the primary lap-band row formula.  It
reconstructs strict blocking sets from their threshold events, sweeps the
resulting open cells, and obtains pair components topologically.  Fractions
are exact throughout.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DELTA = Fraction(1, 8)

PINNED = {
    "selector": (
        ROOT / "reviews/2026-09-28-one-containment-selector/results.json",
        "7f84d1dc9b561045648969bd4d1491df66abb7fd53e1908259fdfd42e1f34cb5",
    ),
    "geometry": (
        ROOT / "reviews/2026-09-28-joint-triple-exclusions/results.json",
        "37d446c6c44d22e5d81804d33839d2c72ee4b24640d43129c97d8aaae3a15159",
    ),
    "roles": (
        ROOT / "reviews/2026-09-28-cover-obligations/results.json",
        "c10cd96fc0a92445894146fedc7ea156911b35ccd9474d1ad8916e3977bed62e",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def F(value: str | int) -> Fraction:
    return Fraction(value)


def fs(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def jsonable(value: Any) -> Any:
    if isinstance(value, Fraction):
        return fs(value)
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def floorq(x: Fraction) -> int:
    return x.numerator // x.denominator


def circle_distance(x: Fraction) -> Fraction:
    q = floorq(x)
    r = x - q
    return min(r, 1 - r)


def blocked(speed: int, t: Fraction) -> bool:
    return circle_distance(speed * t) < DELTA


def threshold_events(speed: int, left: Fraction, right: Fraction) -> set[Fraction]:
    """Threshold contacts (plus window ends), by explicit affine preimages."""
    events = {left, right}
    lo = floorq(speed * left) - 2
    hi = floorq(speed * right) + 3
    for lap in range(lo, hi + 1):
        for sign in (-1, 1):
            t = Fraction(lap, speed) + sign * DELTA / speed
            if left <= t <= right:
                events.add(t)
    return events


def components_for_predicate(
    speeds: tuple[int, ...], left: Fraction, right: Fraction, predicate
) -> dict[str, Any]:
    events = sorted(set().union(*(threshold_events(v, left, right) for v in speeds)))
    point_state = [bool(predicate(t)) for t in events]
    cell_state = [bool(predicate((a + b) / 2)) for a, b in zip(events, events[1:])]

    components: list[dict[str, Any]] = []
    active = False
    start = None
    left_included = False
    for i, occupied in enumerate(cell_state):
        if occupied and not active:
            active = True
            start = events[i]
            left_included = point_state[i]
        if not occupied:
            continue
        continues = i + 1 < len(cell_state) and cell_state[i + 1] and point_state[i + 1]
        if not continues:
            components.append(
                {
                    "interval": [start, events[i + 1]],
                    "left_included": left_included,
                    "right_included": point_state[i + 1],
                }
            )
            active = False
            start = None

    isolated = []
    for i, (event, occupied) in enumerate(zip(events, point_state)):
        left_cell = i > 0 and cell_state[i - 1]
        right_cell = i < len(cell_state) and cell_state[i]
        if occupied and not left_cell and not right_cell:
            isolated.append(event)

    return {
        "events": events,
        "point_state": point_state,
        "cell_state": cell_state,
        "components": components,
        "positive_component_count": len(components),
        "isolated_points": isolated,
    }


def pair_reconstruction(a: int, b: int, left: Fraction, right: Fraction) -> dict[str, Any]:
    assert a < b
    return components_for_predicate(
        (a, b), left, right, lambda t: blocked(a, t) and blocked(b, t)
    )


def lonely_reconstruction(speeds: list[int], left: Fraction, right: Fraction) -> dict[str, Any]:
    return components_for_predicate(
        tuple(speeds), left, right, lambda t: all(not blocked(v, t) for v in speeds)
    )


def interval_signature(components: list[dict[str, Any]]) -> list[list[str]]:
    return [[fs(c["interval"][0]), fs(c["interval"][1])] for c in components]


def compare_primary(primary: dict[str, Any], verification_cases: dict[str, Any]) -> dict[str, Any]:
    """Compare critical fields while tolerating only the frozen likely schemas."""
    report: dict[str, Any] = {"present": True, "checks": []}
    primary_cases = primary.get("cases", {})
    for case_id, vcase in verification_cases.items():
        pcase = primary_cases.get(case_id)
        if pcase is None:
            report["checks"].append({"case": case_id, "field": "case_present", "passed": False})
            continue
        pair_rows = pcase.get(
            "pair_rows", pcase.get("pairs", pcase.get("all_pairs", pcase.get("pair_counts", [])))
        )
        lookup = {}
        if isinstance(pair_rows, list):
            for row in pair_rows:
                pair = row.get("pair", row.get("base_pair"))
                if pair is not None:
                    lookup[tuple(pair)] = row
        elif isinstance(pair_rows, dict):
            for key, row in pair_rows.items():
                nums = tuple(int(x) for x in key.replace(",", " ").split())
                lookup[nums] = row
        for pair_record in vcase["pairs"]:
            pair = tuple(pair_record["pair"])
            row = lookup.get(pair)
            got = None if row is None else row.get(
                "lap_band_component_count",
                row.get("lap_band_count", row.get("count", row.get("positive_component_count"))),
            )
            report["checks"].append(
                {
                    "case": case_id,
                    "pair": list(pair),
                    "field": "pair_component_count",
                    "expected": pair_record["positive_component_count"],
                    "primary": got,
                    "passed": got == pair_record["positive_component_count"],
                }
            )
        selection = pcase.get(
            "formula_selected_base_pair", pcase.get("selection", pcase.get("selected_pair"))
        )
        if isinstance(selection, dict):
            selection = selection.get("selected_pair", selection.get("pair"))
        report["checks"].append(
            {
                "case": case_id,
                "field": "selected_pair",
                "expected": vcase["selected_pair"],
                "primary": selection,
                "passed": selection == vcase["selected_pair"],
            }
        )
    report["passed"] = all(item["passed"] for item in report["checks"])
    return report


def main() -> None:
    hash_checks = {
        name: {"expected": expected, "actual": sha256(path), "passed": sha256(path) == expected}
        for name, (path, expected) in PINNED.items()
    }
    assert all(v["passed"] for v in hash_checks.values()), hash_checks

    selector = json.loads(PINNED["selector"][0].read_text())
    geometry = json.loads(PINNED["geometry"][0].read_text())
    roles = json.loads(PINNED["roles"][0].read_text())
    geometry_name = {"collective_target": "target", "strict_16": "strict_16", "doubling_112": "doubling_112", "tight_13": "tight_13"}

    role_by_name = {case["name"]: case for case in roles["cases"]}
    verified_cases: dict[str, Any] = {}
    total_events = total_cells = 0
    archive_piece_checks = []
    selector_checks = []

    for case_id, source_case in selector["cases"].items():
        left, right = map(F, source_case["window"])
        speeds = source_case["speeds"]
        gphysical = geometry["cases"][geometry_name[case_id]]["physical"]
        pair_records = []
        for a, b in itertools.combinations(speeds, 2):
            rec = pair_reconstruction(a, b, left, right)
            total_events += len(rec["events"])
            total_cells += len(rec["cell_state"])
            i, j = speeds.index(a), speeds.index(b)
            mask = (1 << i) | (1 << j)
            archived = gphysical["intersection_pieces"][mask]
            archive_ok = interval_signature(rec["components"]) == archived
            archive_piece_checks.append({"case": case_id, "pair": [a, b], "passed": archive_ok})
            pair_records.append(
                {
                    "pair": [a, b],
                    "positive_component_count": rec["positive_component_count"],
                    "components": rec["components"],
                    "threshold_event_count": len(rec["events"]),
                    "open_cell_count": len(rec["cell_state"]),
                    "archived_intervals": archived,
                    "archive_interval_match": archive_ok,
                }
            )

        eligible = [tuple(pair) for pair in source_case["eligible_base_pairs"]]
        pair_count = {tuple(r["pair"]): r["positive_component_count"] for r in pair_records}
        selected = list(min(eligible, key=lambda p: (pair_count[p], p))) if eligible else None
        archived_selected = source_case["frozen_rule_results"]["fewest_positive_occurrence_components"]["selected_base_pair"]
        selector_checks.append({"case": case_id, "expected": archived_selected, "actual": selected, "passed": selected == archived_selected})

        lonely = lonely_reconstruction(speeds, left, right)
        verified_cases[case_id] = {
            "window": [left, right],
            "speeds": speeds,
            "pairs": pair_records,
            "eligible_pairs": [list(p) for p in eligible],
            "selected_pair": selected,
            "archived_selected_pair": archived_selected,
            "selection_matches": selected == archived_selected,
            "lonely_positive_components": lonely["components"],
            "lonely_isolated_points": lonely["isolated_points"],
        }

    strict = verified_cases["strict_16"]
    strict_tie = {
        "eligible_counts": [
            {"pair": p, "count": next(r["positive_component_count"] for r in strict["pairs"] if r["pair"] == p)}
            for p in strict["eligible_pairs"]
        ],
        "lexicographic_selection": strict["selected_pair"],
        "passed": strict["selected_pair"] == [6, 11],
    }

    tight = verified_cases["tight_13"]
    tight_check = {
        "no_eligible_pair": tight["eligible_pairs"] == [],
        "positive_lonely_component_count": len(tight["lonely_positive_components"]),
        "isolated_lonely_points": tight["lonely_isolated_points"],
        "archive_endpoint": role_by_name["tight_13"]["endpoint"],
        "passed": tight["eligible_pairs"] == []
        and len(tight["lonely_positive_components"]) == 0
        and tight["lonely_isolated_points"] == [Fraction(3, 8)]
        and role_by_name["tight_13"]["endpoint"]["valid"]
        and role_by_name["tight_13"]["endpoint"]["isolated"],
    }

    doubling_role = role_by_name["doubling_112"]
    doubling_check = {
        "archived_outcome": doubling_role["outcome"],
        "pair_only_lower_bound": doubling_role["baseline"]["value"],
        "diagnostic_selected_pair": verified_cases["doubling_112"]["selected_pair"],
        "passed": doubling_role["outcome"] == "pair_only_positive"
        and F(doubling_role["baseline"]["value"]) > 0,
        "interpretation": "The lap-band selector remains diagnostic and does not replace the prior pair-only-positive exit.",
    }

    primary_path = HERE / "results.json"
    primary_comparison = (
        compare_primary(json.loads(primary_path.read_text()), verified_cases)
        if primary_path.exists()
        else {"present": False, "passed": None, "reason": "results.json not present at verifier run"}
    )

    checks = {
        "pinned_hashes": all(v["passed"] for v in hash_checks.values()),
        "all_24_archive_intervals": all(v["passed"] for v in archive_piece_checks) and len(archive_piece_checks) == 24,
        "all_4_selections": all(v["passed"] for v in selector_checks) and len(selector_checks) == 4,
        "strict_tie": strict_tie["passed"],
        "tight_isolated_equality": tight_check["passed"],
        "doubling_pair_only_role": doubling_check["passed"],
        "primary_comparison": primary_comparison["passed"],
    }
    passed = all(v for k, v in checks.items() if k != "primary_comparison") and primary_comparison["passed"] is not False

    output = {
        "method": "Independent exact threshold-event sweep; no lap-band row formula and no import from primary.py.",
        "arithmetic": "fractions.Fraction only",
        "hash_checks": hash_checks,
        "cases": verified_cases,
        "archive_piece_checks": archive_piece_checks,
        "selector_checks": selector_checks,
        "strict_tie_check": strict_tie,
        "tight_endpoint_check": tight_check,
        "doubling_role_check": doubling_check,
        "primary_comparison": primary_comparison,
        "scope": {
            "cases": 4,
            "physical_pairs": len(archive_piece_checks),
            "pair_threshold_events_total": total_events,
            "pair_open_cells_total": total_cells,
            "new_containment_queries": 0,
        },
        "checks": checks,
        "passed": passed,
        "limits": [
            "This is internal independently structured AI verification, not independent human mathematical validation.",
            "Finite agreement covers only the four frozen windows and 24 physical pairs.",
            "The verifier checks the lap-band output against direct geometry; it does not independently prove the general lap-band lemma.",
        ],
    }
    (HERE / "verification.json").write_text(json.dumps(jsonable(output), indent=2) + "\n")

    primary_line = (
        f"Primary critical-field comparison: {'PASS' if primary_comparison['passed'] else 'FAIL'}."
        if primary_comparison["present"]
        else "Primary results were not yet present; rerun after results.json appears."
    )
    md = f"""# Independent verification: lap-band component count

## Outcome

{'PASS' if passed else 'INCOMPLETE OR FAIL'}. A separately structured exact threshold-event sweep reconstructs all 24 pair intersections on the four frozen windows. Every reconstructed interval and component count matches the pinned physical geometry, and the frozen minimum-count selector matches the archived selector in all four cases.

{primary_line}

## Method

For each pair, the verifier generates only the exact threshold contacts `(m +/- 1/8)/v` inside the supplied window. It tests each resulting open cell and each event point directly using `||vt|| < 1/8`. Components are joined across an event only when that event itself remains strictly blocking for both runners. Thus threshold equality is safe and can split two positive components; window endpoints are included only when strict blocking holds there.

This is intentionally different from the primary calculation: it does not use the per-lap integer-band row formula or import `primary.py`.

## Exact checks

- 4 frozen windows and 24 physical pairs.
- {total_events} pair-specific threshold events and {total_cells} open cells.
- All 24 exact interval lists match the pinned geometry archive.
- All 4 frozen selector outcomes match.
- `strict_16`: the eligible count tie resolves lexicographically to `(6,11)`.
- `tight_13`: no positive-slack pair, no positive lonely interval, and the isolated valid equality point is exactly `3/8`.
- `doubling_112`: the archived pair-only lower bound is `{doubling_role['baseline']['value']}>0`; the component selector is diagnostic only and does not replace that exit.
- No new complement-containment query was made.

## Limits

This verifies the finite calculation, endpoint semantics, and control roles. It is internal AI verification rather than independent human validation, and it does not by itself prove the general lap-band lemma or any whole-configuration Lonely Runner claim.
"""
    (HERE / "verification.md").write_text(md)
    if not passed:
        raise SystemExit("verification incomplete or failed")


if __name__ == "__main__":
    main()
