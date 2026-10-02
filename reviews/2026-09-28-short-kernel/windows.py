#!/usr/bin/env python3
"""Frozen 12-row width arithmetic plus only the declared strict16 event check."""

from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
PROTOCOL = HERE / "windows_protocol.json"
assert sha256(PROTOCOL.read_bytes()).hexdigest() == (
    "6d78b53e166441480ab3a4d76484698156615cd7792da6f7bd7a3bbfee10378a"
)
protocol = json.loads(PROTOCOL.read_text())


def resolve_source(field):
    """Prefer the canonical repository layout; retain the frozen scratch path."""
    historical = Path(protocol[field])
    canonical = PROJECT / "reviews" / "2026-09-28-chain-termination" / historical.name
    return canonical if canonical.is_file() else PROJECT / historical


old_protocol_path = resolve_source("source_protocol")
old_results_path = resolve_source("source_results")
assert sha256(old_protocol_path.read_bytes()).hexdigest() == (
    "134f1825868d1bde006f3cf7f1d523047fc89410d3acaf8da5add4ec658608c0"
)
assert sha256(old_results_path.read_bytes()).hexdigest() == (
    "02edb5fe0b579b79a65c900af37d9431bc99ae640db006fb4aca7874fd69145a"
)
old_protocol = json.loads(old_protocol_path.read_text())
old_results = json.loads(old_results_path.read_text())
old_cases = {row["id"]: row for row in old_protocol["cases"]}
old_output = {row["id"]: row for row in old_results["cases"]}
assert len(protocol["cases"]) == len(old_cases) == 12
assert [r["id"] for r in protocol["cases"]] == list(old_cases)

rows = []
for row in protocol["cases"]:
    previous = old_cases[row["id"]]
    archived = old_output[row["id"]]
    for field in ("speeds", "window"):
        assert row[field] == previous[field] == archived[field]
    periods = [F(1, v) for v in row["speeds"]]
    width = F(row["window"][1]) - F(row["window"][0])
    total = sum(periods, F(0))
    span = F(3, 4) * total + F(1, 4) * max(periods)
    assert str(total) == archived["reciprocal_sum"]
    rows.append({
        "id": row["id"],
        "speeds": row["speeds"],
        "window": row["window"],
        "S": str(total),
        "H": str(span),
        "width": str(width),
        "H_over_width": str(span / width),
        "width_minus_H": str(width - span),
        "S_sufficient": total <= width,
        "H_sufficient": span <= width,
        "newly_sufficient": span <= width < total,
        "archived_verdict": archived["verdict"],
        "archived_earliest": archived.get("earliest"),
        "archived_final_time": archived["final_time"],
    })

# Only the frozen strict16 diagnostic receives an endpoint reconstruction.
strict = next(row for row in protocol["cases"] if row["id"] == "strict_16")
left, right = map(F, strict["window"])
occurrences = []
for speed in strict["speeds"]:
    # A conservative, explicitly bounded lap range, only on this one input.
    for lap in range(int(speed * left) - 1, int(speed * right) + 2):
        lo, hi = F(8 * lap - 1, 8 * speed), F(8 * lap + 1, 8 * speed)
        if lo < right and hi > left:
            occurrences.append((speed, lap, lo, hi))
events = sorted({left, right} | {
    endpoint for _, _, lo, hi in occurrences
    for endpoint in (max(left, lo), min(right, hi))
})
cells = []
nonzero = []
prefix = F(0)
prefix_records = [{"time": str(left), "value": "0"}]
for lo, hi in zip(events, events[1:]):
    midpoint = (lo + hi) / 2
    value = sum(a < midpoint < b for _, _, a, b in occurrences) - 1
    cells.append({"left": str(lo), "right": str(hi), "f": value})
    if value:
        nonzero.append((lo, hi, value))
    prefix += value * (hi - lo)
    prefix_records.append({"time": str(hi), "value": str(prefix)})

expected = protocol["strict16_frozen_analytic_claim"]
observed_positive = [[str(lo), str(hi)] for lo, hi, value in nonzero if value == 1]
observed_negative = [[str(lo), str(hi)] for lo, hi, value in nonzero if value == -1]
assert all(abs(value) == 1 for _, _, value in nonzero)
assert observed_positive == expected["positive_intervals"]
assert observed_negative == expected["negative_intervals"]
assert prefix == F(expected["total_signed_excess"])
prefix_values = [F(record["value"]) for record in prefix_records]
assert min(prefix_values) == 0 and max(prefix_values) == prefix
assert max(F(1, speed) for speed in strict["speeds"]) > right - left
safe_endpoints = []
for point in events:
    safe = all(F(1, 8) <= speed * point % 1 <= F(7, 8)
               for speed in strict["speeds"])
    if safe:
        safe_endpoints.append(str(point))
assert safe_endpoints == ["17/56", "39/128"]

output = {
    "status": "pass",
    "claim_status": protocol["claim_status"],
    "protocol_sha256": sha256(PROTOCOL.read_bytes()).hexdigest(),
    "source_protocol_sha256": sha256(old_protocol_path.read_bytes()).hexdigest(),
    "source_results_sha256": sha256(old_results_path.read_bytes()).hexdigest(),
    "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    "cases": rows,
    "summary": {
        "cases": len(rows),
        "S_sufficient": sum(row["S_sufficient"] for row in rows),
        "H_sufficient": sum(row["H_sufficient"] for row in rows),
        "newly_sufficient": sum(row["newly_sufficient"] for row in rows),
        "H_equals_width": sum(F(row["H"]) == F(row["width"]) for row in rows),
    },
    "strict16": {
        "occurrences": [
            {"speed": speed, "lap": lap, "left": str(lo), "right": str(hi)}
            for speed, lap, lo, hi in occurrences
        ],
        "events": [str(t) for t in events],
        "cells": cells,
        "positive_intervals": observed_positive,
        "negative_intervals": observed_negative,
        "total_signed_excess": str(prefix),
        "prefix_values_at_events": prefix_records,
        "prefix_min": str(min(prefix_values)),
        "prefix_max": str(max(prefix_values)),
        "suffix_min": str(min(prefix - x for x in prefix_values)),
        "suffix_max": str(max(prefix - x for x in prefix_values)),
        "safe_endpoints": safe_endpoints,
        "safe_interval": ["17/56", "39/128"],
        "safe_duration": "1/896",
        "all_translates_obstruction": "Analytic implication of prefix/suffix signs and box width >= window width; no translate was searched or evaluated.",
    },
}
(HERE / "windows_results.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output["summary"]))
for row in rows:
    print(row["id"], "H=" + row["H"], "width=" + row["width"],
          "passes=" + str(row["H_sufficient"]),
          "archived=" + str(row["archived_earliest"]))
print("strict16 total signed excess:", prefix)
print("strict16 prefix and suffix range: [0,", prefix, "]")
