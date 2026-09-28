#!/usr/bin/env python3
"""Independent exact verification for the frozen floor-sum component counter.

This file intentionally does not import ``primary.py``.  It verifies the open
strip in two differently oriented finite ways:

* direct enumeration of every integer point in the inherited lap rectangle;
* a column-wise half-plane identity, summing clipped m-prefixes for fixed n.

It also rebuilds pair-intersection components from blocker endpoints and only
then compares the resulting points/counts and selector with the pinned archive
and (when present) the primary ``results.json``.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL_PATH = HERE / "protocol.json"
RESULTS_PATH = HERE / "results.json"
OUTPUT_PATH = HERE / "verification.json"
REPORT_PATH = HERE / "verification.md"

EXPECTED_PROTOCOL_SHA256 = (
    "a398539b747b9510259e5a134090f3eb6430370588d735bdec12f67260ec5724"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def frac(value: Any) -> Fraction:
    return Fraction(str(value))


def fs(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def strict_integer_range(lower: Fraction, upper: Fraction) -> tuple[int, int]:
    """Integers x satisfying lower < x < upper, as an inclusive range."""

    return floor_fraction(lower) + 1, ceil_fraction(upper) - 1


def blocker_intervals(
    speed: int, window: tuple[Fraction, Fraction]
) -> list[tuple[Fraction, Fraction, int]]:
    left, right = window
    delta = Fraction(1, 8)
    lo, hi = strict_integer_range(speed * left - delta, speed * right + delta)
    intervals: list[tuple[Fraction, Fraction, int]] = []
    for lap in range(lo, hi + 1):
        interval_left = max(left, (Fraction(lap) - delta) / speed)
        interval_right = min(right, (Fraction(lap) + delta) / speed)
        if interval_left < interval_right:
            intervals.append((interval_left, interval_right, lap))
    return intervals


def event_sweep(
    a: int, b: int, window: tuple[Fraction, Fraction]
) -> dict[str, Any]:
    a_intervals = blocker_intervals(a, window)
    b_intervals = blocker_intervals(b, window)
    events = sorted(
        {window[0], window[1]}
        | {endpoint for left, right, _ in a_intervals for endpoint in (left, right)}
        | {endpoint for left, right, _ in b_intervals for endpoint in (left, right)}
    )
    cells: list[dict[str, Any]] = []
    active_flags: list[bool] = []
    for left, right in zip(events, events[1:]):
        if left == right:
            continue
        sample = (left + right) / 2
        a_lap = next(
            (lap for lo, hi, lap in a_intervals if lo < sample < hi), None
        )
        b_lap = next(
            (lap for lo, hi, lap in b_intervals if lo < sample < hi), None
        )
        active = a_lap is not None and b_lap is not None
        active_flags.append(active)
        if active:
            cells.append(
                {
                    "interval": [fs(left), fs(right)],
                    "sample": fs(sample),
                    "laps": [a_lap, b_lap],
                }
            )
    components = sum(
        1
        for index, active in enumerate(active_flags)
        if active and (index == 0 or not active_flags[index - 1])
    )
    return {
        "events": len(events),
        "open_cells": max(0, len(events) - 1),
        "jointly_blocked_open_cells": len(cells),
        "positive_components": components,
        "active_cells": cells,
    }


def direct_pair(
    a: int, b: int, window: tuple[Fraction, Fraction]
) -> dict[str, Any]:
    left, right = window
    delta = Fraction(1, 8)
    m_min, m_max = strict_integer_range(a * left - delta, a * right + delta)
    n_min, n_max = strict_integer_range(b * left - delta, b * right + delta)
    S = a + b

    points: list[tuple[int, int]] = []
    scanned = 0
    if m_min <= m_max and n_min <= n_max:
        for m in range(m_min, m_max + 1):
            for n in range(n_min, n_max + 1):
                scanned += 1
                D = 8 * b * m - 8 * a * n
                if -S < D < S:
                    points.append((m, n))

    # Independent orientation: for each n, sum the m-prefix satisfying D <= K.
    def half_plane_by_columns(K: int) -> tuple[int, list[dict[str, int]]]:
        total = 0
        columns: list[dict[str, int]] = []
        if m_min > m_max or n_min > n_max:
            return 0, columns
        for n in range(n_min, n_max + 1):
            upper = (8 * a * n + K) // (8 * b)
            clipped_upper = min(m_max, upper)
            contribution = max(0, clipped_upper - m_min + 1)
            total += contribution
            columns.append(
                {
                    "n": n,
                    "unclipped_m_upper": upper,
                    "contribution": contribution,
                }
            )
        return total, columns

    lower_H, lower_columns = half_plane_by_columns(-S)
    upper_H, upper_columns = half_plane_by_columns(S - 1)
    column_count = upper_H - lower_H

    intervals: list[dict[str, Any]] = []
    for m, n in points:
        component_left = max(
            left,
            (Fraction(m) - delta) / a,
            (Fraction(n) - delta) / b,
        )
        component_right = min(
            right,
            (Fraction(m) + delta) / a,
            (Fraction(n) + delta) / b,
        )
        intervals.append(
            {
                "laps": [m, n],
                "interval": [fs(component_left), fs(component_right)],
                "positive": component_left < component_right,
            }
        )

    sweep = event_sweep(a, b, window)
    checks = {
        "direct_equals_column_half_plane_difference": len(points) == column_count,
        "all_reconstructed_intervals_positive": all(
            item["positive"] for item in intervals
        ),
        "event_sweep_component_count_matches": sweep["positive_components"]
        == len(points),
    }
    return {
        "lap_rectangle": {
            "m_min": m_min,
            "m_max": m_max,
            "n_min": n_min,
            "n_max": n_max,
            "rectangle_points_scanned": scanned,
        },
        "scaled_strip": {"S": S, "strict_D_lower": -S, "strict_D_upper": S},
        "direct_points": [list(point) for point in points],
        "direct_count": len(points),
        "column_half_planes": [
            {"K": -S, "H": lower_H, "columns": lower_columns},
            {"K": S - 1, "H": upper_H, "columns": upper_columns},
        ],
        "column_half_plane_difference_count": column_count,
        "reconstructed_components": intervals,
        "event_sweep": sweep,
        "checks": checks,
    }


def archived_points(pair_row: dict[str, Any]) -> list[list[int]]:
    return [
        [row["m"], n]
        for row in pair_row["lap_band_table"]["m_rows"]
        for n in row["n_labels"]
    ]


def primary_pair_index(primary_case: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    return {
        tuple(row["base_pair"]): row for row in primary_case.get("pair_rows", [])
    }


def primary_half_planes_match(
    primary_row: dict[str, Any], independent: dict[str, Any]
) -> bool | None:
    planes = primary_row.get("half_planes")
    if not isinstance(planes, list):
        trace = primary_row.get("lap_rectangle_and_floor_sum_trace", {})
        upper = trace.get("half_plane_upper")
        lower = trace.get("half_plane_lower_subtracted")
        if isinstance(upper, dict) and isinstance(lower, dict):
            planes = [upper, lower]
    if not isinstance(planes, list):
        return None
    expected = {
        item["K"]: item["H"] for item in independent["column_half_planes"]
    }
    observed: dict[int, int] = {}
    for item in planes:
        count = item.get("H", item.get("half_plane_count"))
        if "K" not in item or count is None:
            return None
        observed[int(item["K"])] = int(count)
    return observed == expected


def build_verification() -> dict[str, Any]:
    protocol_sha = sha256(PROTOCOL_PATH)
    assert protocol_sha == EXPECTED_PROTOCOL_SHA256, (
        f"protocol hash changed: {protocol_sha}"
    )
    protocol = load_json(PROTOCOL_PATH)

    source_checks: dict[str, Any] = {}
    for key in (
        "lap_band_protocol",
        "lap_band_results",
        "cached_interval_results",
        "physical_geometry",
    ):
        rel = protocol["source_contract"][key]
        expected = protocol["source_contract"][f"{key}_sha256"]
        actual = sha256(ROOT / rel)
        source_checks[key] = {
            "path": rel,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "matches": actual == expected,
        }
        assert actual == expected, f"pinned source changed: {rel}"

    lap_archive = load_json(ROOT / protocol["source_contract"]["lap_band_results"])
    primary = load_json(RESULTS_PATH) if RESULTS_PATH.exists() else None

    case_results: dict[str, Any] = {}
    all_assertions: list[bool] = []
    all_pair_count = 0
    total_rectangle_points = 0
    total_events = 0
    total_cells = 0
    total_components = 0
    primary_fields_compared = 0

    for case_id in ("collective_target", "strict_16", "doubling_112", "tight_13"):
        archived_case = lap_archive["cases"][case_id]
        speeds = [int(value) for value in archived_case["speeds"]]
        window = tuple(frac(value) for value in archived_case["window"])
        archived_rows = {
            tuple(row["base_pair"]): row for row in archived_case["pair_rows"]
        }
        primary_case = (primary or {}).get("cases", {}).get(case_id)
        primary_rows = primary_pair_index(primary_case) if primary_case else {}
        pairs: list[dict[str, Any]] = []
        counts_for_selection: dict[tuple[int, int], int] = {}

        for a, b in itertools.combinations(speeds, 2):
            pair = (a, b)
            independent = direct_pair(a, b, window)
            archived_row = archived_rows[pair]
            archive_comparison = {
                "points_match_archived_lap_rows": independent["direct_points"]
                == archived_points(archived_row),
                "count_matches_archived_lap_count": independent["direct_count"]
                == archived_row["lap_band_component_count"],
                "count_matches_archived_interval_count": independent["direct_count"]
                == archived_row["postselection_archive_comparison"][
                    "interval_derived_component_count"
                ],
            }
            all_assertions.extend(archive_comparison.values())
            all_assertions.extend(independent["checks"].values())
            counts_for_selection[pair] = independent["direct_count"]

            primary_comparison: dict[str, Any] | None = None
            if pair in primary_rows:
                primary_row = primary_rows[pair]
                primary_rectangle = primary_row.get(
                    "lap_rectangle",
                    primary_row.get("lap_rectangle_and_floor_sum_trace", {}),
                )
                independent_rectangle = independent["lap_rectangle"]
                rectangle_match = all(
                    int(primary_rectangle.get(key)) == independent_rectangle[key]
                    for key in ("m_min", "m_max", "n_min", "n_max")
                )
                count_match = int(primary_row["floor_sum_component_count"]) == independent[
                    "direct_count"
                ]
                plane_match = primary_half_planes_match(primary_row, independent)
                primary_comparison = {
                    "lap_rectangle_matches": rectangle_match,
                    "component_count_matches": count_match,
                    "half_plane_totals_match": plane_match,
                }
                all_assertions.extend([rectangle_match, count_match])
                primary_fields_compared += 5
                if plane_match is not None:
                    all_assertions.append(plane_match)
                    primary_fields_compared += 2

            pairs.append(
                {
                    "base_pair": [a, b],
                    "eligible": bool(archived_row["eligible"]),
                    **independent,
                    "archive_comparison": archive_comparison,
                    "primary_comparison": primary_comparison,
                }
            )
            all_pair_count += 1
            total_rectangle_points += independent["lap_rectangle"][
                "rectangle_points_scanned"
            ]
            total_events += independent["event_sweep"]["events"]
            total_cells += independent["event_sweep"]["open_cells"]
            total_components += independent["direct_count"]

        eligible_pairs = [
            tuple(row["base_pair"])
            for row in archived_case["pair_rows"]
            if row["eligible"]
        ]
        selected = (
            min(eligible_pairs, key=lambda pair: (counts_for_selection[pair], pair))
            if eligible_pairs
            else None
        )
        archived_selected = archived_case["formula_selected_base_pair"]
        selection_matches_archive = (
            (list(selected) if selected else None) == archived_selected
        )
        all_assertions.append(selection_matches_archive)

        primary_selected = (
            primary_case.get("floor_sum_selected_base_pair") if primary_case else None
        )
        selection_matches_primary = (
            (list(selected) if selected else None) == primary_selected
            if primary_case
            else None
        )
        if selection_matches_primary is not None:
            all_assertions.append(selection_matches_primary)
            primary_fields_compared += 1

        case_results[case_id] = {
            "speeds": speeds,
            "window": [fs(window[0]), fs(window[1])],
            "pairs": pairs,
            "independent_selected_base_pair": list(selected) if selected else None,
            "archived_selected_base_pair": archived_selected,
            "selection_matches_archive": selection_matches_archive,
            "primary_selected_base_pair": primary_selected,
            "selection_matches_primary": selection_matches_primary,
        }

    equality_controls = []
    for a, b, m, n, expected_D, contact in (
        (3, 5, 1, 2, -8, Fraction(3, 8)),
        (3, 5, 2, 3, 8, Fraction(5, 8)),
    ):
        D = 8 * b * m - 8 * a * n
        S = a + b
        left = max((Fraction(m) - Fraction(1, 8)) / a, (Fraction(n) - Fraction(1, 8)) / b)
        right = min((Fraction(m) + Fraction(1, 8)) / a, (Fraction(n) + Fraction(1, 8)) / b)
        checks = {
            "expected_scaled_difference": D == expected_D,
            "on_excluded_boundary": abs(D) == S,
            "zero_length_contact": left == right == contact,
            "not_in_strict_strip": not (-S < D < S),
        }
        all_assertions.extend(checks.values())
        equality_controls.append(
            {
                "a": a,
                "b": b,
                "m": m,
                "n": n,
                "D": D,
                "S": S,
                "contact": fs(contact),
                "checks": checks,
            }
        )

    primary_protocol_match = None
    if primary is not None:
        primary_protocol_match = primary.get("protocol_sha256") == protocol_sha
        all_assertions.append(primary_protocol_match)
        primary_fields_compared += 1

    return {
        "baseline": protocol["baseline"],
        "protocol_sha256": protocol_sha,
        "verifier": "independent direct lattice enumeration, column-wise half-plane identity, and blocker-endpoint event sweep; no primary import",
        "arithmetic": "integers and fractions.Fraction only; no floating-point decisions",
        "source_hash_checks": source_checks,
        "primary_results_present": primary is not None,
        "primary_protocol_matches": primary_protocol_match,
        "cases": case_results,
        "strict_equality_contact_controls": equality_controls,
        "scope": {
            "cases": len(case_results),
            "physical_pairs": all_pair_count,
            "direct_rectangle_points_scanned": total_rectangle_points,
            "event_sweep_events_with_per_pair_endpoint_duplication": total_events,
            "event_sweep_open_cells": total_cells,
            "positive_components": total_components,
            "primary_critical_fields_compared": primary_fields_compared,
        },
        "all_checks_passed": all(all_assertions),
    }


def render_report(data: dict[str, Any]) -> str:
    rows = []
    for case_id, case in data["cases"].items():
        counts = ", ".join(
            f"{pair['base_pair'][0]}/{pair['base_pair'][1]}={pair['direct_count']}"
            for pair in case["pairs"]
        )
        selected = case["independent_selected_base_pair"]
        selected_text = "/".join(map(str, selected)) if selected else "none"
        rows.append(f"| `{case_id}` | {counts} | {selected_text} | yes |")
    primary_text = (
        f"compared {data['scope']['primary_critical_fields_compared']} critical fields"
        if data["primary_results_present"]
        else "not yet present; rerun after `results.json` is written"
    )
    return "\n".join(
        [
            "# Independent floor-sum component-count verification",
            "",
            "**Status:** PASS" if data["all_checks_passed"] else "**Status:** FAIL",
            "",
            "The verifier does not import `primary.py`. It enumerates every integer",
            "point in each inherited lap rectangle, independently evaluates both",
            "half-planes by fixed-`n` column prefixes, and rebuilds positive pair",
            "components by an exact blocker-endpoint event sweep.",
            "",
            "| case | exact pair counts | selected eligible pair | archive match |",
            "| --- | --- | --- | --- |",
            *rows,
            "",
            f"Primary comparison: {primary_text}.",
            "",
            "Strictness controls exclude both `D=-S` at `t=3/8` and `D=+S` at",
            "`t=5/8` for `(a,b)=(3,5)`: each is a zero-length contact, not a",
            "positive component.",
            "",
            "Scope: "
            f"{data['scope']['physical_pairs']} pairs, "
            f"{data['scope']['direct_rectangle_points_scanned']} rectangle points, "
            f"{data['scope']['event_sweep_open_cells']} open event cells, and "
            f"{data['scope']['positive_components']} positive components. "
            "This is separately structured internal AI verification, not independent",
            "human mathematical validation.",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data = build_verification()
    serialized = json.dumps(data, indent=2, sort_keys=True) + "\n"
    report = render_report(data)
    if args.write:
        OUTPUT_PATH.write_text(serialized)
        REPORT_PATH.write_text(report)
    else:
        assert OUTPUT_PATH.read_text() == serialized, "verification.json is stale"
        assert REPORT_PATH.read_text() == report, "verification.md is stale"
    assert data["all_checks_passed"]
    print(
        "PASS: "
        f"{data['scope']['physical_pairs']} pairs, "
        f"{data['scope']['direct_rectangle_points_scanned']} rectangle points, "
        f"{data['scope']['event_sweep_open_cells']} event cells, "
        f"{data['scope']['primary_critical_fields_compared']} primary fields"
    )


if __name__ == "__main__":
    main()
