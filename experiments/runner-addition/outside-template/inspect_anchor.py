"""Retrospective diagnostic of saved results, not a frozen validation rule.

No new core or contact search. Compare time 1/10 against the saved complete
cores and directly check integer residues for core speeds and leader failures.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def inspect(path):
    raw = path.read_bytes()
    source = json.loads(raw)
    t = F(1,10)
    records = []
    for row in source["families"]:
        d = F(row["threshold"])
        if row["status"] != "EVALUATED":
            records.append({"name":row["name"],"status":"NOT_EVALUATED"})
            continue
        phases = [v*t % 1 for v in row["speeds"]]
        ids = [i for i,(a,b) in enumerate(row["core"]) if F(a) <= t <= F(b)]
        core_safe = all(d <= phase <= 1-d for phase in phases)
        if bool(ids) != core_safe or len(ids) > 1:
            raise ValueError("saved geometry/direct anchor mismatch")
        failures = row["constructor"]["failures"]
        blocked = [r for r in failures if not d <= (r*t % 1) <= 1-d]
        if d == t and blocked != [r for r in failures if r % 10 == 0]:
            raise ValueError("residue criterion mismatch")
        records.append({"name":row["name"],"status":"INSPECTED",
                        "core_residues_mod_10":[v % 10 for v in row["speeds"]],
                        "core_phases":list(map(str,phases)),"core_safe_at_anchor":core_safe,
                        "anchor_component":ids[0] if ids else None,
                        "leader_failures":failures,"exceptions_blocking_anchor":blocked,
                        "anchor_repairs_every_exception":core_safe and not blocked,
                        "constructor_menu":row["constructor"]["ids"]})
    return {"status":"POST_HOC_SOURCE_DIAGNOSTIC","source_results_sha256":hashlib.sha256(raw).hexdigest(),
            "time":str(t),"records":records,
            "limits":"Chosen after outcomes. No new runner inputs or geometry; not held-out evidence, a tuned selector, or a general two-component result."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=HERE / "results/RESULTS.json")
    parser.add_argument("--output",type=Path,default=HERE / "results/ANCHOR_DIAGNOSTIC.json")
    args = parser.parse_args()
    result = inspect(args.input)
    with args.output.open("x") as handle:
        handle.write(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"records":len(result["records"])}))
