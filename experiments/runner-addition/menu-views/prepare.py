"""Copy previously verified core geometry; do not evaluate added speeds."""
import argparse
from fractions import Fraction as F
import json
from math import ceil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def prepare():
    cfg = json.loads((HERE / "config.json").read_text())
    prior = json.loads((HERE.parent / "placement/results/RESULTS.json").read_text())
    d = F(cfg["threshold"])
    records = []
    for pair in cfg["pairs"]:
        old = next(x for x in prior["new_records"] if x["pair"] == pair)
        intervals = [tuple(map(F,x["interval"])) for x in old["components"]]
        leader = min(range(len(intervals)),key=lambda i:(-(intervals[i][1]-intervals[i][0]),intervals[i][0]))
        width = intervals[leader][1]-intervals[leader][0]
        cutoff = ceil(2*d/width)
        if cutoff > cfg["max_tail_cutoff"] or len(intervals) > cfg["max_components"]:
            raise ValueError("core budget exceeded")
        speeds = old["speeds"]
        domain = [r for r in range(1,cutoff) if r not in speeds]
        controls = []
        for r in (cutoff,cutoff+1,10**6+1,10**18+1):
            while r in speeds:
                r += 1
            if r not in controls:
                controls.append(r)
        records.append({"pair":pair,"threshold":cfg["threshold"],"speeds":speeds,
                        "components":intervals,"leader":leader,"cutoff":cutoff,
                        "matched_inputs":domain,"necessary_remainder":domain,
                        "tail_controls":controls})
    return {"source_commit":cfg["source_commit"],"records":records,
            "note":"Copied pinned complete cores; no added-speed evaluations in preparation."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=HERE / "inputs.json")
    args = parser.parse_args()
    data = prepare()
    with args.output.open("x") as handle:
        handle.write(json.dumps(data,default=str,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"cores":len(data["records"]),"finite_cases":sum(len(r["matched_inputs"]) for r in data["records"])}))
