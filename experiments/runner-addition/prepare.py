"""Freeze core geometry and input domains, without evaluating an added runner."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import ceil
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import feasible_intervals


def prepare():
    cfg = json.loads((HERE / "protocol.json").read_text())
    records = []
    for p, q in cfg["pairs"]:
        speeds = [a*p+b*q for a, b in cfg["rows"]]
        if len(set([0] + speeds)) != 9 or sum(speeds) > cfg["max_core_speed_sum"]:
            raise ValueError("STOP: invalid core or core speed budget exceeded")
        pair_records = []
        for ds in cfg["thresholds"]:
            delta = F(ds)
            intervals = feasible_intervals(speeds, delta)
            if not intervals or len(intervals) > cfg["max_components"]:
                raise ValueError("STOP: empty core or component budget exceeded")
            leader = min(range(len(intervals)),
                         key=lambda i: (-(intervals[i][1]-intervals[i][0]), intervals[i][0]))
            width = intervals[leader][1]-intervals[leader][0]
            if width <= 0:
                raise ValueError("STOP: isolated-only core has no width tail")
            cutoff = ceil(2*delta/width)
            if cutoff > cfg["max_tail_cutoff"]:
                raise ValueError("STOP: finite remainder budget exceeded")
            pair_records.append({
                "pair": [p, q], "threshold": ds, "speeds": speeds,
                "components": [[str(a), str(b)] for a, b in intervals],
                "leader": leader, "leader_width": str(width), "cutoff": cutoff,
            })
        matched_cutoff = max(row["cutoff"] for row in pair_records)
        matched = [r for r in range(1, matched_cutoff) if r not in speeds]
        for row in pair_records:
            row["matched_inputs"] = matched
            row["necessary_remainder"] = [r for r in matched if r < row["cutoff"]]
            controls = []
            for candidate in (row["cutoff"], row["cutoff"]+1, 10**6+1, 10**18+1):
                while candidate in speeds:
                    candidate += 1
                if candidate not in controls:
                    controls.append(candidate)
            row["tail_controls"] = controls
        records.extend(pair_records)
    return {
        "study": cfg["study"], "base_commit": cfg["base_commit"],
        "checker_sha256": hashlib.sha256((ROOT / "lonely_runner/checker.py").read_bytes()).hexdigest(),
        "construction": "core-only preparation; no new added-r queries",
        "records": records,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "inputs.json")
    args = parser.parse_args()
    result = prepare()
    with args.output.open("x") as handle:
        handle.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PREPARED_NO_R_EVALUATIONS", "cores": len(result["records"]),
                      "finite_queries": sum(len(r["matched_inputs"]) for r in result["records"]),
                      "output": str(args.output)}))
