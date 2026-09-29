#!/usr/bin/env python3
"""Exact physical opposing-contact audit; no project mathematical imports.

Construction predates this reviewer's opening of the archived verification.json.
The original verify.py, ambient.py, and audit.py have not been read or imported.
Only q=2..25 receive exhaustive physical optimum checks; large q values receive
the displayed witness evaluation only. See physical_review.md for completeness.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FROZEN_COMMIT = "8a967b30fcd73abd814e4c8f7f53f216c4b3f61e"
SMALL_Q = tuple(range(2, 26))
LARGE_Q = tuple(range(100002, 100008))


def speeds(q):
    return (1, q, q + 1, q + 2, q + 3, 2 * q + 3, 2 * q + 5)


def phase(v, t):
    """Actual common-start physical phase, without ambient coordinates."""
    value = v * t
    return value - value.numerator // value.denominator


def physical_value(vs, t):
    ps = [phase(v, t) for v in vs]
    return min(min(p, 1 - p) for p in ps)


def proposed(q):
    """Candidate theorem transcription used only after exhaustive calculation."""
    if q == 4:
        return F(1, 8), F(1, 8), "exceptional q=4"
    if q % 3 == 0:
        value = F(q, 3 * (2 * q + 1))
        return value, 2 * value, "q divisible by 3"
    if q % 6 in (1, 2):
        return F(1, 6), F(1, 6), "q mod 6 in {1,2}"
    if q % 6 == 4:
        value = F(q - 1, 3 * (2 * q + 1))
        return value, 2 * value, "q mod 6=4, q>=10"
    assert q % 6 == 5
    value = F(q + 1, 2 * (3 * q + 5))
    return value, 3 * value, "q mod 6=5"


def candidate_times(vs):
    """Enumerate strict opposing contacts and all individual tent peaks.

    Opposing active tents have phases p and 1-p, hence (v+w)t is
    integral. Iterate that integer once per unordered speed pair, then
    test actual phases for the two possible strict slope orientations.
    Phase=1/2 contacts are covered independently by every runner's peaks.
    """
    candidates = {F(0): ["endpoint"], F(1): ["endpoint"]}
    tested = 0
    contacts = 0
    peaks = 0
    for v, w in combinations(vs, 2):
        total_speed = v + w
        for n in range(1, total_speed):
            tested += 1
            t = F(n, total_speed)
            p, r = phase(v, t), phase(w, t)
            strict_opposite = (0 < p < F(1, 2) < r < 1 or
                               0 < r < F(1, 2) < p < 1)
            if p + r == 1 and strict_opposite:
                contacts += 1
                rising, falling = (v, w) if p < F(1, 2) else (w, v)
                candidates.setdefault(t, []).append({
                    "rising_speed": rising, "falling_speed": falling,
                    "integer_speed_sum_times_t": n,
                })
    for v in vs:
        for j in range(v):
            peaks += 1
            t = F(2 * j + 1, 2 * v)
            candidates.setdefault(t, []).append({"peak_speed": v})
    return candidates, {
        "integer_speed_sum_candidates_tested_with_multiplicity": tested,
        "strict_opposing_contact_occurrences": contacts,
        "individual_peak_occurrences": peaks,
        "unique_candidate_times_including_endpoints": len(candidates),
    }


def time_certificate(vs, t, value, origins=None):
    ps = [phase(v, t) for v in vs]
    ds = [min(p, 1 - p) for p in ps]
    result = {
        "time": t,
        "physical_laps": [(v * t).numerator // (v * t).denominator for v in vs],
        "phases": ps,
        "distances": ds,
        "minimum_distance": min(ds),
        "active_speeds": [v for v, d in zip(vs, ds) if d == value],
    }
    assert min(ds) == value
    if origins is not None:
        result["candidate_origins"] = origins
    return result


def exhaustive_small(q):
    assert q in SMALL_Q
    vs = speeds(q)
    candidates, counts = candidate_times(vs)
    evaluated = [(physical_value(vs, t), t) for t in candidates]
    best = max(value for value, t in evaluated)
    winners = sorted(t for value, t in evaluated if value == best)
    # The witness/formula is never used to build or prune the candidate set.
    claimed, witness, branch = proposed(q)
    assert best == claimed, (q, best, claimed)
    assert witness in winners, (q, witness, winners)
    assert winners == sorted(1 - t for t in winners)
    return {
        "q": q, "speeds": vs, "maximum": best,
        "maximizing_times": winners,
        "maximizer_certificates": [time_certificate(vs, t, best, candidates[t])
                                   for t in winners],
        "candidate_counts": counts,
        "proposed_formula": claimed, "proposed_witness": witness,
        "branch": branch, "formula_matches": best == claimed,
        "proposed_witness_is_maximizer": witness in winners,
        "reflection_closed": True,
    }


def witness_only(q):
    assert q in LARGE_Q
    claimed, witness, branch = proposed(q)
    vs = speeds(q)
    certificate = time_certificate(vs, witness, claimed)
    assert all(claimed <= p <= 1 - claimed for p in certificate["phases"])
    return {
        "q": q, "q_mod_6": q % 6, "speeds": vs,
        "branch": branch, "claimed_maximum": claimed,
        "witness_certificate": certificate,
        "actual_witness_value_equals_claimed": True,
        "scope": "witness only; no exhaustive upper bound or optimum calculation",
    }


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, tuple):
        return [encode(v) for v in obj]
    if isinstance(obj, list):
        return [encode(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    return obj


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def compare_archive(small, large):
    """Comparison-only adapter added after fresh construction and first run.

    This archive is read only after every independent calculation has finished.
    It never supplies candidates, upper bounds, arithmetic or stopping criteria.
    """
    archive_path = ROOT / "reviews/2026-09-29-ltcm-spectrum/verification.json"
    archived = json.loads(archive_path.read_text())
    old_small = {row["q"]: row for row in archived["small_q"]}
    assert set(old_small) == set(SMALL_Q)
    comparisons = []
    for row in small:
        old = old_small[row["q"]]
        old_times = sorted(F(t) for t in old["all_maximizers"])
        same_maximum = row["maximum"] == F(old["maximum"])
        same_times = row["maximizing_times"] == old_times
        comparisons.append({
            "q": row["q"], "maximum_matches": same_maximum,
            "complete_maximizer_set_matches": same_times,
            "archived_maximizer_count": len(old_times),
        })
        assert same_maximum and same_times, (row["q"], row, old)
    fresh_large = {row["q"]: row for row in large}
    old_large_comparisons = []
    for old in archived["large_q"]:
        assert old["q"] in LARGE_Q
        row = fresh_large[old["q"]]
        certificate = row["witness_certificate"]
        matches = (certificate["time"] == F(old["witness"]) and
                   certificate["distances"] == [F(d) for d in old["distances"]] and
                   row["claimed_maximum"] == F(old["claimed_maximum"]))
        assert matches
        old_large_comparisons.append({"q": old["q"], "witness_fields_match": matches})
    return {
        "status": "all comparisons pass",
        "read_order": "archive first opened after checker construction and first complete fresh run",
        "archive_sha256": digest(archive_path),
        "small_q_comparisons": comparisons,
        "existing_large_witness_comparisons": old_large_comparisons,
        "small_q_maximum_values_compared": len(comparisons),
        "small_q_complete_time_sets_compared": len(comparisons),
        "small_q_maximizing_times_compared": sum(len(row["maximizing_times"]) for row in small),
        "differences": [],
    }


def main():
    small = [exhaustive_small(q) for q in SMALL_Q]
    large = [witness_only(q) for q in LARGE_Q]
    assert {row["q_mod_6"] for row in large} == set(range(6))
    result = {
        "status": "bounded exact physical cross-check; internally AI-authored review",
        "date": "2026-09-29",
        "frozen_candidate_commit_from_protocol": FROZEN_COMMIT,
        "commit_validation_limit": "This mounted source snapshot has no .git metadata; coordinator reports separate GitHub HEAD and input-hash verification.",
        "method": "strict opposing tent contacts plus individual tent peaks and endpoints",
        "arithmetic": "Python standard-library fractions.Fraction; no floating point",
        "small_q_scope": SMALL_Q,
        "large_witness_only_scope": LARGE_Q,
        "independence": {
            "project_mathematical_imports": [],
            "original_verify_py_read_before_construction": False,
            "original_verify_py_read_at_all": False,
            "ambient_selector_or_breakpoint_partition_used": False,
            "shared_implementation_dependency": "Python fractions.Fraction and integer arithmetic",
            "authorship_limit": "Separately tasked AI reviewer; not independent human review or formal verification",
            "theorem_and_inputs_known_during_construction": True,
        },
        "source_sha256": {
            "physical_check.py": digest(Path(__file__)),
            "PROTOCOL.md": digest(HERE / "PROTOCOL.md"),
            "notes/LTCM_EXACT_SPECTRUM_2026_09_29.md": digest(ROOT / "notes/LTCM_EXACT_SPECTRUM_2026_09_29.md"),
        },
        "small_q_results": small,
        "large_q_witness_results": large,
        "archive_comparison": compare_archive(small, large),
    }
    output = HERE / "physical_check.json"
    output.write_text(json.dumps(encode(result), indent=2) + "\n")
    counts = {key: sum(row["candidate_counts"][key] for row in small)
              for key in small[0]["candidate_counts"]}
    print(json.dumps({"small_cases": len(small), "large_witnesses": len(large),
                      "maximizing_times_total": sum(len(row["maximizing_times"]) for row in small),
                      "candidate_counts": counts, "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
