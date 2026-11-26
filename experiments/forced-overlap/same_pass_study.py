"""Replay SAME_PASS_PROTOCOL.md. Run with PYTHONPATH=. from the repository root."""
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd

from endpoint_pairs import TARGET, core_bounds, pair_bound, strong_components, witness_on_component
from endpoint_study import panels, verify_distances
from lonely_runner.checker import feasible_intervals
from same_pass import can_trap_pair


def oracle_checks():
    checked = 0
    for u, w in combinations(range(1, 28), 2):
        pair = pair_bound(u, w)
        components = strong_components((u, w))
        for v in range(w+1, 29):
            full = feasible_intervals((u, w, v), TARGET)
            trapped = any(not any(a <= d and c <= b for c, d in full)
                          for a, b in components)
            assert can_trap_pair(pair, v) == trapped, (u, w, v)
            checked += 1
    assert can_trap_pair(pair_bound(7, 8), 90)
    assert not can_trap_pair(pair_bound(7, 8), 112)  # width equality
    base = tuple(range(1, 15))
    a, b = Fraction(1, 16), Fraction(15, 224)
    assert (a, b) in strong_components(base)
    verify_distances(base, 15, a)
    verify_distances(base, 210, b)
    return checked


def clock_menu(core):
    return [(a, q) for q in range(2, 17) for a in range(1, q//2 + 1)
            if gcd(a, q) == 1 and all(16 * min(v*a % q, -v*a % q) >= q for v in core)]


def audit_core(core):
    largest = max(core)
    _, cutoff, pairs = core_bounds(core)
    components = strong_components(core)
    assert components
    menu = clock_menu(core)
    counts = Counter()
    examples = {}
    for v in range(largest+1, 15*largest+1):
        width = v >= cutoff
        same_pass = width or not any(can_trap_pair(p, v) for p in pairs)
        clock = any(16 * min(v*a % q, -v*a % q) >= q for a, q in menu)
        counts.update({"total": 1, "width": width, "same_pass": same_pass,
                       "new": same_pass and not width, "clock": clock,
                       "same_and_clock": same_pass and clock, "same_only": same_pass and not clock,
                       "new_only": same_pass and not width and not clock,
                       "undecided_by_both": not same_pass and not clock})
        if not same_pass:
            examples.setdefault("unresolved", [core, v])
            continue
        for a, b in components:
            t = witness_on_component(a, b, v)
            assert t is not None and a <= t <= b, (core, v, a, b)
            verify_distances(core, v, t)
            counts["verified_components"] += 1
        if not width:
            key = "gain" if clock else "gain_without_short_clock"
            examples.setdefault(key, [core, v, str(t)])
    return counts, examples


def main():
    cohorts = panels()
    cohorts["holdout"] = [
        tuple(5*i + 1 + hashlib.sha256(f"same-pass-holdout/{j}/{i}".encode("ascii"))
              .digest()[0] % 5 for i in range(14)) for j in range(8)
    ]
    report = {"oracle_triples": oracle_checks(), "panels": {}}
    for label, cores in cohorts.items():
        counts = Counter()
        examples = {}
        for core in cores:
            measured, found = audit_core(core)
            counts.update(measured)
            for k, v in found.items():
                examples.setdefault(k, v)
        report["panels"][label] = {"counts": dict(counts), "examples": examples}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
