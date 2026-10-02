#!/usr/bin/env python3
"""Compare the independently produced exact records; never generate them."""
from fractions import Fraction as F
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = json.loads((HERE / "results.json").read_text())
v = json.loads((HERE / "verification.json").read_text())
assert p["status"] == v["status"] == "pass"
assert p["anchor_count"] == v["anchor_count_modulo_one"] == 22
assert p["directional_failures"] == v["directional_first_lap_failures"] == 44
assert p["first_bands_checked"] == v["individual_first_components_reconstructed"] == 308
primary = {(r["anchor"], r["direction"]): r for r in p["all_anchor_records"]}
review = {(r["anchor"], r["direction"]): r for r in v["failures"]}
assert primary.keys() == review.keys()
bands = 0
for key, a in primary.items():
    b = review[key]
    for field in ("entry", "exit", "first_bands"):
        assert a[field] == b[field], (key, field)
    assert a["pair_gap"] == v["smallest_pair_incompatibility_gap"]
    bands += len(a["first_bands"])

d = p["diagnostics"][0]
c = d["original_forward_from_17_over_56"]
assert [c["left"], c["right"]] == v["rescue_component"]
assert c["width"] == v["rescue_width"]
for row in c["runners"]:
    low, high = F(row["phase_left"]), F(row["phase_right"])
    margins = [str(min(x, 1-x)-F(1,8)) for x in (low, high)]
    assert margins == v["endpoint_margins_by_speed"][str(row["speed"])]
c = d["post_protocol_backward_from_3_over_8"]
r = v["post_protocol_same_menu_rescue"]
assert [c["left"], c["right"]] == r["component"]
assert c["width"] == r["width"]
assert r["slow_lap_ordinal"] == d["slow_lap_index"] + 1
assert r["fast_lap_ordinal"] == d["fast_lap_index"] + 1
assert p["ratio7_boundary"]["point"]["left"] == v["ratio_seven_endpoint_control"]["isolated_local_component"]

d = p["diagnostics"][1]
c = d["original_forward_from_17_over_56"]
r = v["large_budget_formula_only"]
assert d["early_lap_budget"] == r["B"]
assert d["fast_speed"] == r["fast_speed"]
assert d["strict_gap"] == r["strict_first_B_lap_gap"]
assert [c["left"], c["right"]] == r["later_interval"]
assert c["width"] == r["width"]
assert d["fast_lap_index"] + 1 == r["fast_lap_ordinal"]
print(json.dumps({"status": "pass", "anchor_direction_records": len(primary),
                  "individual_bands_compared": bands, "rescue_components": 2,
                  "ratio7_contact": "agrees", "large_budget_diagnostic": "agrees"}))
