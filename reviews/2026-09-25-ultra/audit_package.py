"""Read-only package audit; no project modules imported and no outputs rewritten.

Run: python audit_package.py /path/to/the-lonely-runner-conjecture
This verifies stored certificate arithmetic, not completeness of reductions or
the unbounded mathematical arguments. Counts include repeated certificates.
"""

from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import ast
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
delta = F(1, 8)
required = {"speed", "integer_part", "phase_left", "phase_right"}
counts = Counter()
unique = set()
hash_count = 0
problems = []
missing_import_hashes = {}


def source_hash(path, expected, evidence):
    global hash_count
    hash_count += 1
    if hashlib.sha256((root / path).read_bytes()).hexdigest() != expected:
        problems.append([evidence, "hash mismatch", path])


def imports(path, seen=None):
    seen = set() if seen is None else seen
    if path in seen:
        return seen
    seen.add(path)
    for node in ast.walk(ast.parse((root / path).read_text())):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith(("scripts.", "lonely_runner.")):
            imports(node.module.replace(".", "/") + ".py", seen)
    return seen


def certificates(obj, evidence, where=""):
    if isinstance(obj, list):
        if obj and all(isinstance(row, dict) and required <= row.keys() for row in obj):
            try:
                starts, ends, speeds = [], [], []
                for row in obj:
                    v, j = F(row["speed"]), F(row["integer_part"])
                    a, b = F(row["phase_left"]), F(row["phase_right"])
                    assert v > 0 and v.denominator == j.denominator == 1
                    assert delta <= a < b <= 1 - delta
                    starts.append((j + a) / v)
                    ends.append((j + b) / v)
                    speeds.append(int(v))
                assert len(set(starts)) == len(set(ends)) == 1
                assert 0 <= starts[0] < ends[0] <= 1
                assert len(set(speeds)) == len(speeds)
                counts[(evidence, len(obj))] += 1
                if len(obj) == 7:
                    unique.add((tuple(sorted(speeds)), starts[0], ends[0]))
            except Exception as exc:
                problems.append([evidence, where, type(exc).__name__])
        for i, value in enumerate(obj):
            certificates(value, evidence, where + "/" + str(i))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            certificates(value, evidence, where + "/" + key)


files = sorted((root / "experiments").glob("*.json"))
for file in files:
    data = json.loads(file.read_text())
    mapping = data.get("source_sha256")
    if isinstance(mapping, dict):
        for path, expected in mapping.items():
            source_hash(path, expected, file.name)
        candidates = [p for p in mapping if p.startswith("scripts/") and Path(p).stem.endswith(file.stem)]
        if candidates:
            missing = imports(candidates[0]) - set(mapping)
            if missing:
                missing_import_hashes[file.name] = sorted(missing)
    elif isinstance(mapping, str) and file.stem == "blocking_overlaps":
        source_hash("experiments/cooperative_blocking.json", mapping, file.name)
    if "checker_sha256" in data:
        source_hash("lonely_runner/checker.py", data["checker_sha256"], file.name)
    if "script_sha256" in data:
        source_hash("scripts/analyze_" + file.stem + ".py", data["script_sha256"], file.name)
    certificates(data, file.name)

summary = {
    "experiment_json_files": len(files),
    "recorded_hashes_checked": hash_count,
    "validated_endpoint_certificate_groups": sum(counts.values()),
    "seven_speed_certificate_occurrences": sum(value for (name, n), value in counts.items() if n == 7),
    "unique_seven_speed_interval_certificates": len(unique),
    "distinct_seven_speed_sets_in_certificates": len({row[0] for row in unique}),
    "missing_transitive_import_hashes": missing_import_hashes,
    "problems": problems,
    "certificate_groups_by_file_and_constraint_count": [[name, n, count] for (name, n), count in sorted(counts.items())],
}
print(json.dumps(summary, indent=2))
if problems:
    raise SystemExit(1)
