"""Replay ENDPOINT_PROTOCOL.md using only integer and rational arithmetic."""
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from math import gcd

from endpoint_pairs import TARGET, core_bounds, pair_bound, strong_components, witness_on_component
from lonely_runner.checker import feasible_intervals


def panels():
    dense = list(combinations(range(1, 17), 14))
    prefix = tuple(range(1, 14))
    controls = [prefix + (17,), prefix + (26,), tuple(range(1, 28, 2))]
    sparse = []
    for seed in range(8):
        core = []
        for i in range(14):
            digest = hashlib.sha256(f"endpoint/{seed}/{i}".encode("ascii")).digest()
            core.append(6*i + 1 + digest[0] % 6)
        sparse.append(tuple(core))
    return {"dense": dense, "controls": controls, "sparse": sparse}


def verify_distances(core, fastest, t):
    p, q = t.as_integer_ratio()
    for speed in (*core, fastest):
        residue = speed*p % q
        assert 16 * min(residue, q - residue) >= q


def audit_core(core):
    largest = core[-1]
    original, refined, _ = core_bounds(core)
    second = core[-2]
    normalized_sum = (second + largest) // gcd(second, largest)
    assert (refined == original) == (normalized_sum % 15 == 0)
    assert refined <= original
    components = strong_components(core)
    assert components
    checked = old_hits = new_hits = trapped = 0
    for fastest in range(largest + 1, 15 * largest + 1):
        old_hits += fastest >= original
        new_hits += fastest >= refined
        sampled = fastest in {largest+1, 2*largest, 5*largest, 10*largest, 15*largest}
        full = feasible_intervals((*core, fastest), TARGET) if sampled else ()
        for a, b in components:
            t = witness_on_component(a, b, fastest)
            if sampled:
                assert (t is not None) == any(c <= b and a <= d for c, d in full)
            if t is None:
                trapped += 1
                assert fastest < refined
            else:
                assert a <= t <= b
                verify_distances(core, fastest, t)
            checked += 1
    total = 14 * largest
    return {
        "core": core, "original_cutoff": str(original), "refined_cutoff": str(refined),
        "tested": total, "original_certified": old_hits, "refined_certified": new_hits,
        "additional": new_hits - old_hits, "unresolved": total - new_hits,
        "component_cases": checked, "trapped_components": trapped,
    }


def extra_controls():
    # Directly enumerate boundary differences across a period plus wraparound.
    for u, w in combinations(range(1, 25), 2):
        widths = (u*(16*j - 1) - w*(16*i + 1)
                  for i in range(u) for j in range(1, 2*w + 1))
        assert pair_bound(u, w).scaled_width == min(d for d in widths if 15*d >= u+w)

    # A real trapped interval can coexist with a full witness elsewhere.
    core = tuple(range(1, 15))
    left, right = Fraction(97, 112), Fraction(111, 128)
    assert (left, right) in strong_components(core)
    assert left < Fraction(13, 15) < right
    assert witness_on_component(left, right, 90) is None
    verify_distances(core, 90, TARGET)


def main():
    extra_controls()
    base = tuple(range(1, 15))
    left, right = Fraction(1, 16), Fraction(15, 224)
    assert (left, right) in strong_components(base)
    verify_distances(base, 15, left)
    verify_distances(base, 210, right)
    study = {}
    for label, cores in panels().items():
        rows = [audit_core(c) for c in cores]
        totals = {k: sum(r[k] for r in rows) for k in
                  ("tested", "original_certified", "refined_certified", "additional",
                   "unresolved", "component_cases", "trapped_components")}
        study[label] = {"cores": len(rows), "no_additional_coverage":
                        sum(r["additional"] == 0 for r in rows), **totals, "rows": rows}
    print(json.dumps(study, indent=2))


if __name__ == "__main__":
    main()
