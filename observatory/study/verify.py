"""Replay committed inputs and verify every return against the fifteen physical runners."""
import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import ceil, gcd, lcm
from pathlib import Path

import candidate
import panel

HERE = Path(__file__).resolve().parent
SOURCE = panel.ROOT / "experiments/subset-sum-prediction"
sys.path.insert(0, str(panel.EXPERIMENTS / "one-time-prediction"))
sys.path.insert(0, str(SOURCE))
from predict import predict as four_weight
from predictor import choose_time
from score import exact_witness

THRESHOLD = Fraction(1, 16)
METHODS = ("earlier", "four_weight", "candidate", "grid")
BRANCHES = ("complements", "first_lap", "parity", "fixed_lower_phases",
            "fast_wrap", "winding", "separated", "abstain")
GRID = [Fraction(p, q) for q in range(2, 33) for p in range(1, q // 2 + 1) if gcd(p, q) == 1]
REPLAY = "python observatory/study/verify.py"
SOURCE_REVISION = "3316b381ca3386476c2bfda45a6584d6049838b3"
SEAL_REVISION = "5694845cd501f8083e6286be61650e900a66f513"


def exact(speeds, time):
    """Fractional distance from the nearest whole lap; compare the integer residue formula."""
    if time is None:
        return {"time": None, "clearance": None, "limiting_speeds": [], "status": "abstain"}
    p, q = time.as_integer_ratio()
    distances = []
    for v in speeds:
        position = v * time
        distance = abs(position - round(position))
        assert distance == Fraction(min(v * p % q, -v * p % q), q)
        distances.append(distance)
    smallest = min(distances)
    return {
        "time": str(time),
        "clearance": str(smallest),
        "limiting_speeds": [v for v, d in zip(speeds, distances) if d == smallest],
        "status": "valid" if smallest >= THRESHOLD else "unsafe",
    }


def read_inputs(fresh):
    opened = json.loads((SOURCE / "panel.json").read_bytes())["instances"]
    rows = []
    for name, panel_rows in [("historical", opened), ("fresh", fresh["instances"])]:
        middle = [r for r in panel_rows if r["pattern"] == "stretch_middle"]
        assert len(middle) == 12
        assert Counter(tuple(r["scale"]) for r in middle) == {s: 3 for s in panel.SCALES}
        for idx, row in enumerate(middle, 1):
            weights = row["weights"]
            speeds = panel.physical(weights)
            if name == "historical":
                assert row["speeds"] == speeds
            # Enumerate independently by include/exclude choices, not combinations.
            values = [0]
            for weight in weights:
                values += [v + weight for v in values]
            assert sorted(values) == [0, *speeds] and len(set(speeds)) == 15
            assert all(w > sum(weights[:i]) for i, w in enumerate(weights))
            assert gcd(*weights) == 1 and sum(weights) % 16 == 0
            rows.append({"id": f"{name}-{idx:02}", "panel": name, "weights": weights,
                         "speeds": speeds, "scale": row["scale"], "pattern": row["pattern"],
                         "claim_status": "REPRODUCED" if name == "historical" else "OBSERVED"})
    return rows


def predict_all(rows):
    """Produce three frozen outputs on every lineup before the first post-reveal clearance check."""
    choices = []
    for row in rows:
        weights, speeds = row["weights"], row["speeds"]
        q, earlier_time, _ = choose_time(speeds)
        branch, four_time = four_weight(weights)
        proposed = candidate.predict(weights)
        choices.append((q, earlier_time, branch, four_time, proposed))
    return choices


def single_output(speeds, time, branch, work):
    return {**exact(speeds, time), "branch": branch, "work": {
        **work, "times_emitted": int(time is not None), "preselection_clearance_evaluations": 0,
        "postselection_clearance_evaluations": int(time is not None),
    }}


def check_row(row, choice):
    q, earlier_time, branch, four_time, proposed = choice
    weights, speeds = row["weights"], row["speeds"]
    clear = [d for d in range(2, 17) if all(v % d for v in speeds)]
    for d in range(2, 17):
        residue_set = {v % d for v in speeds}
        assert candidate.residue_mask(weights, d) == sum(1 << r for r in residue_set)
    assert proposed == (Fraction(1, clear[0]) if clear else None)
    if proposed is not None:
        assert earlier_time == proposed
    colliders = [v for v in speeds if v % q == 0]
    anchor = Fraction(1, q)
    earlier = single_output(speeds, earlier_time, "shifted" if colliders else "direct", {
        "physical_speeds_read": len(speeds), "denominators_ranked": 15,
        "speed_divisibility_tests_for_ranking": 15 * len(speeds),
        "anchor_divisibility_tests": len(speeds),
        "shift_noncollider_membership_tests": len(speeds) if colliders else 0,
        "directional_headrooms_compared": 2 * (len(speeds) - len(colliders)) if colliders else 0,
    })
    earlier["choices"] = {"anchor": str(anchor), "denominator": q, "colliding_speeds": colliders,
                          "shift": str(earlier_time - anchor)}
    four = single_output(speeds, four_time, branch, {
        "weights_read": 4, "certificate_branches_considered": min(BRANCHES.index(branch) + 1, 7),
    })
    steps = clear[0] - 1 if clear else 15
    new = single_output(speeds, proposed, "direct" if proposed is not None else "abstain", {
        "weights_read": 4, "denominators_tested": steps, "mask_updates": 4 * steps,
    })
    for idx, t in enumerate(GRID, 1):
        grid = exact(speeds, t)
        if grid["status"] == "valid":
            break
    else:
        grid = exact(speeds, None)
    grid.update(branch="first valid in denominator order", work={
        "physical_speeds_read": 15, "grid_capacity": len(GRID),
        "preselection_clearance_evaluations": idx, "times_emitted": int(grid["time"] is not None),
        "postselection_clearance_evaluations": 0,
    })
    row.update(clear_denominators=clear, methods={"earlier": earlier, "four_weight": four,
                                                "candidate": new, "grid": grid})
    if all(method["status"] != "valid" for method in row["methods"].values()):
        row["independent_interval_witness"] = exact(speeds, exact_witness(speeds))
    exploratory_anchors = {"historical-03": 10, "fresh-04": 3}
    if row["id"] in exploratory_anchors:
        denominator = exploratory_anchors[row["id"]]
        colliding = [v for v in speeds if v % denominator == 0]
        shift = THRESHOLD / min(colliding)
        anchor = Fraction(1, denominator)
        audit = exact(speeds, anchor + shift)
        assert audit["clearance"] == "1/16"
        row["exploratory_witness"] = {
            **audit, "anchor": str(anchor), "colliding_speeds": colliding, "shift": str(shift),
            "branch": "post-hoc alternate anchor, forward shift", "claim_status": "OBSERVED",
            "included_in_comparison": False,
        }
    if row["id"] == "historical-03":
        row["exploratory_checks"] = {"opposite_shift": {
            **exact(speeds, Fraction(95, 1536)), "branch": "reverse shift at the original anchor",
            "claim_status": "OBSERVED", "included_in_comparison": False,
        }}


def summary(rows):
    methods = {}
    for name in METHODS:
        returns = [r["methods"][name] for r in rows]
        methods[name] = {outcome: sum(m["status"] == outcome for m in returns)
                         for outcome in ("valid", "unsafe", "abstain")}
    overlaps = {}
    for left, right in combinations(METHODS, 2):
        groups = {"both": [], "left_only": [], "right_only": [], "neither": []}
        for row in rows:
            l, r = (row["methods"][m]["status"] == "valid" for m in (left, right))
            group = "both" if l and r else "left_only" if l else "right_only" if r else "neither"
            groups[group].append(row["id"])
        overlaps[f"{left}_vs_{right}"] = {k: len(ids) for k, ids in groups.items()}
        overlaps[f"{left}_vs_{right}"]["row_ids"] = groups
    work = {}
    for name in METHODS:
        sums = Counter()
        for row in rows:
            sums.update(row["methods"][name]["work"])
        work[name] = dict(sums)
    return {"cases": len(rows), "methods": methods, "overlaps": overlaps, "work": work}


def archive_replay(study_rows):
    with tempfile.TemporaryDirectory() as directory:
        ledger = Path(directory) / "ledger.json"
        subprocess.run([sys.executable, "score.py", "panel.json", str(ledger)], cwd=SOURCE,
                       stdout=subprocess.DEVNULL, check=True)
        if ledger.read_bytes() != (SOURCE / "ledger.json").read_bytes():
            raise ValueError("60-case archived ledger differs")
        subprocess.run([sys.executable, "check_controls.py"], cwd=SOURCE,
                       stdout=subprocess.DEVNULL, check=True)
        rows = json.loads(ledger.read_bytes())
    middle = [r for r in rows if r["pattern"] == "stretch_middle"]
    checked = [r for r in study_rows if r["panel"] == "historical"]
    for original, audit in zip(middle, checked, strict=True):
        methods = audit["methods"]
        assert original["weights"] == audit["weights"]
        assert original["prior"] == (methods["earlier"]["status"] == "valid")
        assert original["method"] == methods["four_weight"]["branch"]
        assert original["time"] == methods["four_weight"]["time"]
        assert original["clearance"] == methods["four_weight"]["clearance"]
        assert original["grid_time"] == methods["grid"]["time"]
    return {"cases": len(rows), "earlier_valid": sum(r["prior"] for r in rows),
            "four_weight_valid": sum(r["time"] is not None for r in rows),
            "four_weight_abstain": sum(r["time"] is None for r in rows),
            "grid_valid": sum(r["grid_time"] is not None for r in rows),
            "ledger_sha256": panel.digest((SOURCE / "ledger.json").read_bytes())}


def controls():
    consecutive = list(range(1, 16))
    equality = exact(consecutive, THRESHOLD)
    assert equality["clearance"] == "1/16" and equality["limiting_speeds"] == [1, 15]
    equality.update(speeds=[0, *consecutive], threshold="1/16", reference=0, claim_status="REPRODUCED")
    archived = []
    for weights in ((1, 6, 11, lcm(*range(1, 33)) - 18), (114, 139, 359, 1100)):
        branch, t = four_weight(weights)
        result = exact(panel.physical(weights), t)
        assert branch == "complements" and result["clearance"] == "1/15"
        archived.append({"weights": list(weights), "branch": branch, **result})
    for total in (112, 128, 144, 160, 16 * 10**9):
        for prefix in ((1, 2, 13), (1, 3, 8), (1, 4, 6)):
            d = total - sum(prefix)
            weights = [*prefix, d]
            speeds = panel.physical(weights)
            anchor = Fraction(1, 12 if prefix == (1, 2, 13) else 16)
            result = exact(speeds, (ceil(d * anchor - THRESHOLD) + THRESHOLD) / d)
            name, t = four_weight(weights)
            prediction = exact(speeds, t)
            assert result["clearance"] == "1/16" and prediction["status"] == "valid"
            archived.append({"weights": weights, "branch": "three-prefix control", **result,
                             "four_weight_prediction": {"branch": name, **prediction}})
    return equality, archived


def reduced_record():
    shared = {"reference": 0, "n": 16, "threshold": "1/16", "minimum_moving_speed": 1,
              "maximum_moving_speed": 112,
              "family": "All nonempty subset sums of four positive superincreasing weights, "
                        "gcd one and total divisible by 16; common start."}
    cases = []
    for weights in ((1, 2, 13, 96), (1, 3, 8, 100), (1, 16, 32, 63), (1, 15, 20, 76)):
        speeds = panel.physical(weights)
        assert gcd(*weights) == 1 and min(speeds) == 1 and max(speeds) == 112
        assert all(w > sum(weights[:i]) for i, w in enumerate(weights))
        cases.append({"weights": list(weights), "speeds": speeds, "at_1_15": exact(speeds, Fraction(1, 15)),
                      "at_1_16": exact(speeds, THRESHOLD)})
    assert [r["at_1_15"]["clearance"] for r in cases] == ["0", "1/15", "1/15", "0"]
    assert all(112 in r["at_1_16"]["limiting_speeds"] for r in cases)
    return {"shared": shared, "at_1_15": "underdetermined", "at_1_16": "no", "cases": cases[:2],
            "additional_cases": cases[2:], "claim_status": "REPRODUCED"}


def build():
    manifest = json.loads((HERE / "freeze.json").read_bytes())
    for path, expected in manifest["file_sha256"].items():
        if panel.digest((panel.ROOT / path).read_bytes()) != expected:
            raise ValueError(f"frozen file changed: {path}")
    fresh = panel.verify(HERE / "reveal")
    rows = read_inputs(fresh)
    choices = predict_all(rows)
    for row, choice in zip(rows, choices):
        check_row(row, choice)
    archive = archive_replay(rows)
    equality, archived = controls()
    summaries = {name: summary([r for r in rows if r["panel"] == name]) for name in ("historical", "fresh")}
    h = summaries["historical"]
    assert (archive["cases"], archive["earlier_valid"], archive["four_weight_valid"], archive["grid_valid"]) == (60, 56, 39, 60)
    assert (h["methods"]["earlier"]["valid"], h["methods"]["four_weight"]["valid"],
            h["methods"]["candidate"]["valid"], h["methods"]["grid"]["valid"]) == (11, 1, 10, 12)
    old_only = h["overlaps"]["earlier_vs_four_weight"]["row_ids"]["left_only"]
    direct = [r["id"] for r in rows if r["id"] in old_only and r["clear_denominators"]]
    assert len(old_only) == 10 and len(direct) == 9
    return {
        "schema_version": 1, "source_revision": SOURCE_REVISION, "seal_revision": SEAL_REVISION,
        "rule_revision": manifest["rule_revision"], "candidate_name": candidate.RULE_REVISION,
        "replay_command": REPLAY, "scope": "Stationary reference 0, common start, 16 runners. "
            "Twelve opened and twelve fresh stretch_middle lineups; three per scale band in each panel.",
        "threshold": "1/16", "historical_baseline": archive,
        "historical_diagnostic": {"earlier_only": old_only, "direct": direct, "shifted": ["historical-09"]},
        "summaries": summaries, "rows": rows, "equality_control": equality,
        "archived_controls": archived, "reduced_record": reduced_record(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", help="print one verified row by ID")
    parser.add_argument("--write", action="store_true", help="replace the versioned results after replay")
    args = parser.parse_args()
    result = build()
    data = (json.dumps(result, indent=2) + "\n").encode()
    target = HERE / "results.json"
    if args.write:
        target.write_bytes(data)
    elif data != target.read_bytes():
        raise SystemExit("Results do not match the versioned evidence.")
    if args.case:
        row = next((r for r in result["rows"] if r["id"] == args.case), None)
        if row is None:
            parser.error("unknown case ID")
        print(json.dumps(row, indent=2))
    else:
        print("Verified the archived 60-row ledger, equality control, 17 archived controls and all 24 study rows.")
        for key, values in result["summaries"].items():
            print(key, json.dumps(values["methods"]))


if __name__ == "__main__":
    main()
