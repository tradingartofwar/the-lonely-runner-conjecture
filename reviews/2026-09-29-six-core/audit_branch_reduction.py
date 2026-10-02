#!/usr/bin/env python3
"""Protocol-authorized scalar audit of archived widths and 36 branches.

No six-core safe sets or new physical tuples are evaluated here.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = "25c818133f6e78054d14e82bf4b0f0c6b63c9dd7d1ca9a12071d83f878b891a2"


def floor(x):
    return x.numerator // x.denominator


def main():
    ppath = HERE / "PROTOCOL.json"
    assert sha256(ppath.read_bytes()).hexdigest() == PROTOCOL_HASH
    protocol = json.loads(ppath.read_text())
    archive = HERE.parent / "2026-09-29-core-windows" / "independent_core_windows.json"
    rows = json.loads(archive.read_text())["rows"]
    assert [r["a"] for r in rows] == [2, 3] + list(range(6, 35))
    declared = sorted((int(a), b) for a, bs in protocol["a_b_branches"].items() for b in bs)
    widths = {r["a"]: F(r["width"]) for r in rows}
    for a, w in protocol["widths"].items():
        assert widths[int(a)] == F(w)
    derived = []
    branch_rows = []
    scalar_b_evaluations = 0
    for a, w in widths.items():
        # For b beyond this bound, T2(b,c)<3/(4b)<w for every c>b.
        for b in range(a + 1, floor(F(3, 4) / w) + 1):
            if b in {1, 4, 5}:
                continue
            cmin = b + 1
            while cmin in {1, 4, 5}:
                cmin += 1
            scalar_b_evaluations += 1
            if F(1, 4 * b) + F(1, 2 * cmin) >= w:
                derived.append((a, b))
                gap = w - F(1, 4 * b)
                assert gap > 0
                cmax = floor(1 / (2 * gap))
                branch_rows.append({"a": a, "b": b, "width": str(w),
                                    "c_min": cmin, "c_max": cmax})
    assert derived == declared
    assert len(derived) == 36
    max_c = max(r["c_max"] for r in branch_rows)
    assert max_c == 62
    result = {
        "status": "PASS",
        "scope": "Scalar branch inequalities using only archived four-core widths; no additional six-core evaluation",
        "archived_a_count": len(rows),
        "scalar_b_evaluations": scalar_b_evaluations,
        "declared_and_derived_pair_count": len(derived),
        "maximum_c_bound": max_c,
        "branch_bounds": branch_rows,
        "tail_argument": "For a>=35, three remaining trains have span at most7/(4a)<=1/20<3/32, the width of the fixed core window J; the strict inequality gives a positive opening.",
        "sha256": {"PROTOCOL.json": PROTOCOL_HASH,
                   "archived_independent_core_windows.json": sha256(archive.read_bytes()).hexdigest(),
                   "audit_branch_reduction.py": sha256(Path(__file__).read_bytes()).hexdigest()},
    }
    (HERE / "branch_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "archived_a_count", "scalar_b_evaluations", "declared_and_derived_pair_count", "maximum_c_bound")}))


if __name__ == "__main__":
    main()
