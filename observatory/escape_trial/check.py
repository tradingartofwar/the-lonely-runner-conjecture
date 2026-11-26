"""Replay the precommitted middle-gap trial and compare against individual runner trajectories."""
import argparse
import json
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import floor, gcd
from pathlib import Path

import seal

HERE = Path(__file__).resolve().parent
ROOT = seal.ROOT
sys.path.insert(0, str(ROOT))
from observatory.study.candidate import predict as direct
sys.path.insert(0, str(ROOT / "experiments/subset-sum-prediction"))
sys.path.insert(0, str(ROOT / "experiments/one-time-prediction"))
from predict import predict as archived_four
from predictor import choose_time

LIMIT = F(1, 16)
DENOMINATORS = range(2, 17)
GRID = [F(p, q) for q in range(2, 33) for p in range(1, q // 2 + 1) if gcd(p, q) == 1]
METHODS = ("escape", "direct", "earlier", "archived_four", "grid")


def require(test, reason):
    if not test:
        raise ValueError(reason)


def as_json(data):
    return (json.dumps(data, indent=2, default=str) + "\n").encode()


def inputs():
    files = [
        ("original", ROOT / "experiments/subset-sum-prediction/panel.json"),
        ("previous", seal.STUDY / "reveal/panel.json"),
        ("fresh", HERE / "reveal/panel.json"),
    ]
    output = []
    all_weights = set()
    for cohort, path in files:
        rows = [r for r in json.loads(path.read_bytes())["instances"] if r["pattern"] == "stretch_middle"]
        require(Counter(tuple(r["scale"]) for r in rows) == dict.fromkeys(seal.previous.SCALES, 3), cohort)
        for number, r in enumerate(rows, 1):
            w = tuple(r["weights"])
            require(w not in all_weights and len(w) == 4 and gcd(*w) == 1 and sum(w) % 16 == 0,
                    "Malformed or repeated input")
            require(all(v > sum(w[:i]) for i, v in enumerate(w)), "Not superincreasing")
            all_weights.add(w)
            physical = sorted(sum(s) for k in range(1, 5) for s in combinations(w, k))
            require(len(set(physical)) == 15 and physical == r.get("speeds", physical), "Speeds disagree")
            output.append({"id": f"{cohort}-{number:02}", "cohort": cohort,
                           "weights": list(w), "scale": r["scale"], "speeds": physical})
    return output


def frozen_rule():
    manifest = json.loads((HERE / "freeze.json").read_bytes())
    for name, expected in manifest["file_sha256"].items():
        require(seal.previous.digest((ROOT / name).read_bytes()) == expected, f"Frozen file changed: {name}")
    for path in ("observatory/escape_trial/rule.py", "observatory/escape_trial/commitment.json"):
        require(path in manifest["file_sha256"], f"Missing digest: {path}")
    from observatory.escape_trial import rule
    return rule


def outputs(rule, rows):
    choices = []
    for row in rows:
        w, speeds = row["weights"], row["speeds"]
        new, anchors, directions = rule.screen(w)
        require(new == rule.predict(w), "Inconsistent predictor entry points")
        q, t, _ = choose_time(speeds)
        branch, four_t = archived_four(w)
        choices.append({"id": row["id"], "escape": new, "denominators_examined": anchors,
                        "directions_examined": directions, "direct": direct(w),
                        "earlier": {"q": q, "time": t}, "archived_four": {"branch": branch, "time": four_t}})
    return choices


def clearance(speeds, time):
    if time is None:
        return {"time": None, "clearance": None, "limiting_speeds": [], "status": "abstain"}
    distances = {v: abs(v * time - round(v * time)) for v in speeds}
    p, q = time.as_integer_ratio()
    require(all(d * q == min(v*p % q, -v*p % q) for v, d in distances.items()), "Distance disagrees")
    minimum = min(distances.values())
    return {"time": time, "clearance": minimum, "limiting_speeds": [v for v in speeds if distances[v] == minimum],
            "status": "valid" if minimum >= LIMIT else "unsafe"}


def arc_check(speeds, q, sign):
    """Lift every runner's phase to its own closed safe interval on the real line."""
    anchor = F(1, q)
    colliders = [v for v in speeds if v % q == 0]
    escape = LIMIT / min(colliders)
    candidate = anchor + sign * escape
    rooms = {}
    violations = []
    for v in speeds:
        initial = v * anchor
        lap = floor(initial)
        if initial == lap and sign < 0:
            lap -= 1
        left, right = lap + LIMIT, lap + 1 - LIMIT
        if initial.denominator != 1:
            edge = right if sign > 0 else left
            rooms[v] = abs(edge / v - anchor)
        if not left <= v * candidate <= right:
            violations.append(v)
    room = min(rooms.values(), default=None)
    return {"q": q, "sign": sign, "anchor": anchor, "time": candidate, "escape": escape,
            "colliders": colliders, "room": room, "room_speeds": [v for v in rooms if rooms[v] == room],
            "outside_first_arc": violations}


def first_window(speeds, d):
    """The slowest collider blocks until entry. A first edge blocks immediately after exit."""
    collider_edge = (1 - LIMIT) / max(d["colliders"])
    exit_offset = min(collider_edge, d["room"]) if d["room"] is not None else collider_edge
    require(d["escape"] <= exit_offset and not d["outside_first_arc"], "Invalid window")
    ends = sorted((d["time"], d["anchor"] + d["sign"] * exit_offset))
    edge_scores = [clearance(speeds, t) for t in ends]
    require(all(r["clearance"] == LIMIT for r in edge_scores), "Endpoint is not a threshold contact")
    return {"endpoints": ends, "width": ends[1] - ends[0],
            "limiting_speeds": [r["limiting_speeds"] for r in edge_scores]}


def physical_screen(speeds):
    clear = [q for q in DENOMINATORS if all(v % q for v in speeds)]
    options = [arc_check(speeds, q, sign) for q in DENOMINATORS if q not in clear for sign in (1, -1)]
    accepted = [o for o in options if not o["outside_first_arc"]]
    if clear:
        first = {"time": F(1, clear[0]), "q": clear[0], "sign": 0}
    elif accepted:
        first = accepted[0]
    else:
        first = None
    return first, clear, options


def grid(speeds):
    for count, t in enumerate(GRID, 1):
        result = clearance(speeds, t)
        if result["status"] == "valid":
            return {**result, "grid_trials": count}
    return {**clearance(speeds, None), "grid_trials": len(GRID)}


def compare_archive(row, methods, old):
    if row["cohort"] == "fresh":
        return
    archived = old[tuple(row["weights"])]
    for here, previous in (("direct", "candidate"), ("earlier", "earlier"),
                           ("archived_four", "four_weight"), ("grid", "grid")):
        for key in ("time", "clearance", "limiting_speeds", "status"):
            val = methods[here][key]
            require((str(val) if isinstance(val, F) else val) == archived[previous][key],
                    f"Replay mismatch: {row['id']} {here} {key}")


def assess(rule, row, choices, old):
    speeds = row["speeds"]
    for q in DENOMINATORS:
        actual = {}
        for v in speeds:
            actual.setdefault(v % q, []).append(v)
        extrema = {r: (len(values), min(values), max(values)) for r, values in actual.items()}
        require(rule.residue_extrema(row["weights"], q) == extrema, "Residue counts or extrema disagree")
    first, clear, directions = physical_screen(speeds)
    expected_tables = clear[0] - 1 if clear else len(DENOMINATORS)
    expected_directions = 0
    if not clear:
        for d in directions:
            if max(d["colliders"]) <= 15 * min(d["colliders"]):
                expected_directions += 1
                if not d["outside_first_arc"]:
                    break
    require((choices["denominators_examined"], choices["directions_examined"])
            == (expected_tables, expected_directions), "Selection work counters disagree")
    new = choices["escape"]
    require((first is None) == (new is None), f"Abstention disagrees: {row['id']}")
    if first is not None:
        require(all(first[k] == new[k] for k in ("q", "sign", "time")), f"Selected time disagrees: {row['id']}")
        if new["sign"]:
            c = first["colliders"]
            require((new["collider_min"], new["collider_max"], new["collider_count"]) == (min(c), max(c), len(c)),
                    "Colliding speeds disagree")
            require(all(first[k] == new[k] for k in ("anchor", "room", "escape")), "Directional edge disagrees")
            require(set(first["room_speeds"]) == set(new["room_speeds"]), "Limiting edge speeds disagree")
    require(choices["direct"] == (F(1, clear[0]) if clear else None), "Direct baseline disagrees")
    times = {"escape": None if new is None else new["time"], "direct": choices["direct"],
             "earlier": choices["earlier"]["time"], "archived_four": choices["archived_four"]["time"]}
    methods = {name: clearance(speeds, t) for name, t in times.items()}
    methods["grid"] = grid(speeds)
    require(methods["escape"]["status"] != "unsafe", f"Unsafe new return: {row['id']}")
    compare_archive(row, methods, old)
    skipped_safe = []
    for d in directions:
        score = clearance(speeds, d["time"])
        if d["outside_first_arc"]:
            if score["status"] == "valid":
                skipped_safe.append({**d, "score": score})
        else:
            require(score["status"] == "valid", "Unsafe independently certified endpoint")
    record = {**row, "clear_denominators": clear, "methods": methods,
              "branch": "abstain" if new is None else ("shift" if new["sign"] else "direct"),
              "selection_work": {"distinct_residue_tables": expected_tables, "signed_headrooms": expected_directions,
                                 "preselection_clearance_evaluations": 0},
              "blocked_anchor_directions_checked": len(directions),
              "certified_directions": sum(not d["outside_first_arc"] for d in directions),
              "safe_endpoints_outside_first_arc": len(skipped_safe)}
    if new is not None and new["sign"]:
        record["selected_shift"] = {**first, "first_safe_window": first_window(speeds, first)}
    if new is None or (not clear and skipped_safe):
        record["first_skipped_safe"] = skipped_safe[0] if skipped_safe else None
    return record


def summary(rows):
    counts = {m: {outcome: sum(r["methods"][m]["status"] == outcome for r in rows)
                  for outcome in ("valid", "unsafe", "abstain")} for m in METHODS}
    pairs = {}
    for name in METHODS[1:]:
        groups = {"both_valid": [], "escape_only": [], "baseline_only": [], "neither_valid": []}
        for r in rows:
            a, b = (r["methods"][m]["status"] == "valid" for m in ("escape", name))
            group = ("both_valid" if b else "escape_only") if a else ("baseline_only" if b else "neither_valid")
            groups[group].append(r["id"])
        pairs[name] = groups
    return {"methods": counts, "branches": dict(Counter(r["branch"] for r in rows)),
            "selection_work": {key: sum(r["selection_work"][key] for r in rows) for key in rows[0]["selection_work"]},
            "grid_trials": sum(r["methods"]["grid"]["grid_trials"] for r in rows),
            "comparisons": pairs}


def named_controls(rows):
    cases = (("previous-04", 3, 1), ("original-03", 16, 1),
             ("original-03", 16, -1), ("original-02", 10, 1))
    controls = []
    for row_id, q, sign in cases:
        r = next(r for r in rows if r["id"] == row_id)
        option = arc_check(r["speeds"], q, sign)
        control = {"id": row_id, **option, "score": clearance(r["speeds"], option["time"])}
        if not option["outside_first_arc"]:
            control["first_safe_window"] = first_window(r["speeds"], option)
        controls.append(control)
    return controls


def challenger_abstention(rule):
    # Identified in the independent adversarial box outside the four pilot bands.
    weights = (260, 264, 1567, 2101)
    speeds = sorted(sum(s) for k in range(1, 5) for s in combinations(weights, k))
    first, clear, options = physical_screen(speeds)
    require(rule.predict(weights) is None and first is None and not clear, "Challenger abstention disagrees")
    safe = [o for o in options if clearance(speeds, o["time"])["status"] == "valid"]
    require([(o["q"], o["sign"]) for o in safe] == [(3, 1), (5, 1), (10, 1), (10, -1), (12, -1)],
            "Challenger alternate endpoints disagree")
    return {"weights": weights, "included_in_cohorts": False, "escape_status": "abstain",
            "safe_skipped_directions": [[o["q"], o["sign"]] for o in safe],
            "first_skipped": {**safe[0], "score": clearance(speeds, safe[0]["time"])}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.add_mutually_exclusive_group()
    options.add_argument("--capture", action="store_true", help="record choices and stop before clearance scoring")
    options.add_argument("--write", action="store_true", help="score captured choices and record the evidence")
    parser.add_argument("--case", help="print one checked case")
    args = parser.parse_args()
    rule = frozen_rule()
    seal.verify(HERE / "reveal")
    rows = inputs()
    choices = outputs(rule, rows)
    vector = HERE / "predictions.json"
    if args.capture:
        with vector.open("xb") as out:
            out.write(as_json(choices))
        print("Recorded all single-output predictions before scoring.")
        return
    require(vector.read_bytes() == as_json(choices), "Predictions do not reproduce")
    archived_rows = json.loads((seal.STUDY / "results.json").read_bytes())["rows"]
    old = {tuple(r["weights"]): r["methods"] for r in archived_rows}
    audited = [assess(rule, r, c, old) for r, c in zip(rows, choices, strict=True)]
    summaries = {group: summary([r for r in audited if r["cohort"] == group])
                 for group in ("original", "previous", "fresh")}
    fresh = [r for r in audited if r["cohort"] == "fresh"]
    gains = [r for r in fresh if r["branch"] == "shift" and r["methods"]["direct"]["status"] == "abstain"
             and r["methods"]["escape"]["status"] == "valid"]
    forecast = {"at_least_one_valid_signed_gain_over_direct": bool(gains),
                "qualifying_rows": [r["id"] for r in gains],
                "also_missed_by_earlier": [r["id"] for r in gains if r["methods"]["earlier"]["status"] != "valid"],
                "selected_multi_collider_gains": [r["id"] for r in gains if len(r["selected_shift"]["colliders"]) > 1]}
    results = {"fresh_forecast": forecast, "cohorts": summaries, "rows": audited, "opened_controls": named_controls(rows),
               "challenger_abstention": challenger_abstention(rule)}
    target = HERE / "results.json"
    if args.write:
        target.write_bytes(as_json(results))
    else:
        require(target.read_bytes() == as_json(results), "Evidence does not reproduce")
    if args.case:
        found = next((r for r in audited if r["id"] == args.case), None)
        if found is None:
            parser.error("Unknown case")
        print(as_json(found).decode(), end="")
    else:
        print("Verified commitment, frozen rules, prediction vector, physical arcs, witnesses and grid.")
        for group, s in summaries.items():
            print(group, s["branches"], {k: v["valid"] for k, v in s["methods"].items()})


if __name__ == "__main__":
    main()
