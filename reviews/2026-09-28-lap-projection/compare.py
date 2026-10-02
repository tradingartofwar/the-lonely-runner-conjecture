#!/usr/bin/env python3
"""Compare separately generated records, including every frozen bounded case."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
p = json.loads((HERE / "results.json").read_text())
v = json.loads((HERE / "verification.json").read_text())
f = json.loads((HERE / "follow_on.json").read_text())
rows = {c["case_id"]: c for c in p["cases"]}
aliases = {
    "obstruction_840_6720_I": "obstruction_B1_I",
    "obstruction_840_5880_I": "ratio7_I",
    "small_gcd_56_113": "small_gcd_113",
    "small_gcd_56_112": "small_gcd_112",
    "aux_fourth_empty": "aux_four_empty",
    "aux_fourth_edge": "aux_four_edge",
    "aux_fourth_positive": "aux_four_positive",
    "aux_quarter_contacts": "aux_quarter_contact",
}
seen = set()
for r in v["bounded_cases"]:
    key = aliases.get(r["case_id"], r["case_id"])
    c = rows[key]
    assert key not in seen
    seen.add(key)
    assert c["speeds"] == list(map(str, r["speeds"]))
    for field in ("phases", "delta", "window", "core"):
        assert c[field] == r[field], (key, field)
    assert c["earliest_in_window"] == r["earliest"], key
    assert c["first_component"] == r["first_component"], key
    assert (c["first_component_kind"] == "positive") == r["first_component_positive"]
    if c["core"]:
        assert r["core_window_certified"]
assert len(seen) == p["bounded_case_count"] == v["bounded_case_count"] == 20
assert set(rows) - seen == {"obstruction_B1000000000000_I"}

large = rows["obstruction_B1000000000000_I"]
other = v["large_symbolic_case"]
assert large["earliest_in_window"] == other["earliest"]
assert large["first_component"] == other["first_component"]
for a, b in zip(large["full_first_component_certificate"], other["lifted_bands"]):
    assert a["speed"] == str(b["speed"])
    for field in ("lap", "left_phase", "right_phase"):
        assert a[field] == b[field]
assert len(large["full_first_component_certificate"]) == len(other["lifted_bands"]) == 7

assert [r["output"] for r in rows["aux_four_positive"]["trace"]] == v["fourth_projection_trace"]
bad, three = v["negative_scope_controls"]
assert bad["earliest"] is None
assert [r["output"] for r in p["scope_failures"]["threshold_outside_hypothesis"]["trace"]] == bad["projection_trace"]
x = p["scope_failures"]["three_residual_two_sweeps"]
assert [r["output"] for r in x["trace"]] == three["projection_trace"]
assert x["earliest_after_left"] == three["earliest"]
assert f["earliest"] == three["earliest"] == v["post_protocol_follow_on"]["earliest"]
assert f["first_component"] == three["first_component"]
assert [r["output"] for r in f["trace"]] == v["post_protocol_follow_on"]["projection_trace"]

# Preserve the distinction between an isolated earliest component and duration
# elsewhere in the very same window.
ratio = next(r for r in v["bounded_cases"] if r["case_id"] == "obstruction_840_5880_I")
assert not ratio["first_component_positive"] and ratio["any_positive_component"]
print(json.dumps({"status": "pass", "bounded_cases_compared": len(seen),
                  "large_lifted_bands_compared": 7, "scope_controls_compared": 2,
                  "post_protocol_triple_trace": "all10outputs agree",
                  "ratio7_point_then_positive": True}))
