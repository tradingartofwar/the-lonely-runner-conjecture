#!/usr/bin/env python3
"""Compare every declared mathematical record after independent freezing."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def sha(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def main():
    freeze = json.loads((HERE / "INDEPENDENT_FREEZE.json").read_text())
    assert sha("PROTOCOL.json") == freeze["protocol_sha256"]
    assert sha("independent_last_runner.py") == freeze["source_sha256"]
    assert sha("independent_last_runner_results.json") == freeze["output_sha256"]
    assert freeze["primary_access_before_freeze"] is False
    independent = json.loads((HERE / "independent_last_runner_results.json").read_text())
    primary = json.loads((HERE / "primary_last_runner.json").read_text())
    counts = {"numeric_leaf_fields": 0, "boolean_leaf_fields": 0,
              "text_leaf_fields": 0, "null_leaf_fields": 0,
              "list_nodes": 0, "dictionary_nodes": 0}
    differences = []

    def walk(a, b, path="records"):
        if type(a) is not type(b):
            differences.append({"path": path, "issue": "type mismatch"})
            return
        if isinstance(a, dict):
            counts["dictionary_nodes"] += 1
            if a.keys() != b.keys():
                differences.append({"path": path, "issue": "dictionary keys differ"})
            for key in a.keys() & b.keys():
                walk(a[key], b[key], path + "." + key)
        elif isinstance(a, list):
            counts["list_nodes"] += 1
            if len(a) != len(b):
                differences.append({"path": path, "issue": "list lengths differ"})
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, path + "[" + str(i) + "]")
        else:
            if isinstance(a, bool):
                counts["boolean_leaf_fields"] += 1
            elif a is None:
                counts["null_leaf_fields"] += 1
            elif isinstance(a, int):
                counts["numeric_leaf_fields"] += 1
            else:
                try:
                    Fraction(a)
                except ValueError:
                    counts["text_leaf_fields"] += 1
                else:
                    counts["numeric_leaf_fields"] += 1
            if a != b:
                differences.append({"path": path, "independent": a, "primary": b})

    walk(independent["records"], primary["records"])
    result = {"status": "PASS" if not differences else "FAIL",
              "scope": "All declared mathematical record fields, including component and prefix bands",
              "source_files": {name: sha(name) for name in [
                  "PROTOCOL.json", "independent_last_runner.py",
                  "independent_last_runner_results.json", "INDEPENDENT_FREEZE.json",
                  "primary_last_runner.py", "primary_last_runner.json",
                  "compare_last_runner.py"]},
              "comparison_counts": counts, "disagreement_count": len(differences),
              "differences": differences, "independent_counts": independent["counts"]}
    (HERE / "comparison_last_runner.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "comparison_counts": counts,
                      "disagreement_count": len(differences)}, indent=2))
    assert not differences


if __name__ == "__main__":
    main()
