"""Replay the frozen seventeen-runner study from the repository root with PYTHONPATH=."""
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
from math import gcd

from endpoint_pairs import component_at_strong_time, core_bounds, pair_bound, strong_components, witness_on_component
from lonely_runner.checker import feasible_intervals
from same_pass import can_trap_pair

N = 17
TARGET = Q(1, N)
STRONG = Q(1, N-1)


def cohorts():
    dense = list(combinations(range(1, 18), 15))
    sparse, challenge = [], []
    mandatory = {11, 13, 16, 17, 60, 63, 70}
    for seed in range(8):
        sparse.append(tuple(5*i + 1 + hashlib.sha256(f"seventeen/sparse/{seed}/{i}".encode())
                            .digest()[0] % 5 for i in range(15)))
        ordered = sorted(set(range(1, 76)) - mandatory,
                         key=lambda v: (hashlib.sha256(f"seventeen/challenge/{seed}/{v}".encode())
                                        .digest(), v))
        challenge.append(tuple(sorted(mandatory.union(ordered[:8]))))
    return {"dense": dense, "sparse": sparse, "challenge": challenge,
            "controls": [tuple(range(1, 30, 2)), (*range(1, 15), 112)]}


def verify(speeds, t, n=N):
    a, q = t.as_integer_ratio()
    assert all(n*min(a*v % q, -a*v % q) >= q for v in speeds)


def clock_menu(core):
    return [(a, q) for q in range(2, N+1) for a in range(1, q//2+1)
            if gcd(a, q) == 1 and all(N*min(v*a % q, -v*a % q) >= q for v in core)]


def independent_checks():
    count = 0
    for u, w in combinations(range(1, 30), 2):
        pair = pair_bound(u, w, N)
        components = strong_components((u, w), N)
        for v in range(w+1, 31):
            full = feasible_intervals((u, w, v), TARGET)
            trapped = any(not any(a <= d and c <= b for c, d in full) for a, b in components)
            assert trapped == can_trap_pair(pair, v), (u, w, v)
            count += 1
    pair = pair_bound(7, 9, N)
    assert can_trap_pair(pair, 96) and not can_trap_pair(pair, 126)
    assert component_at_strong_time(range(1, 16), Q(7, 16), N) == (Q(52,119), Q(67,153))
    assert witness_on_component(Q(52,119), Q(67,153), 96, TARGET) is None
    full = feasible_intervals(range(1, 17), TARGET)
    assert full == tuple((Q(a,17),Q(a,17)) for a in range(1,17))
    return count


def check_core(core):
    m = core[-1]
    _, cutoff, pairs = core_bounds(core, N)
    _, _, prior_pairs = core_bounds(core[:-1], N-1)
    chained_core = not any(can_trap_pair(p, m) for p in prior_pairs)
    strong = feasible_intervals(core, STRONG)
    if chained_core:
        assert strong
    core_time = strong[0][0] if strong else None
    if strong:
        verify(core, core_time, N-1)
    components = strong_components(core, N, strong)
    assert bool(components) == bool(strong)
    if strong:
        assert component_at_strong_time(core, core_time, N) in components
    menu = clock_menu(core)
    counts, examples = Counter(), {}
    for v in range(m+1, 16*m+1):
        width = bool(strong) and v >= cutoff
        phase = bool(strong) and (width or not any(can_trap_pair(p, v) for p in pairs))
        clock = any(N*min(v*a % q, -v*a % q) >= q for a, q in menu)
        counts.update({"tuples": 1, "width": width, "same_pass": phase,
                       "gain": phase and not width, "short_clock": clock,
                       "both": phase and clock, "same_pass_only": phase and not clock,
                       "chained": chained_core and phase, "neither": not phase and not clock})
        found = None
        for a, b in components:
            t = witness_on_component(a, b, v, TARGET)
            if phase:
                assert t is not None, (core, v, a, b)
                counts["certified_component_checks"] += 1
            if t is not None:
                assert a <= t <= b
                verify((*core, v), t)
                if found is None:
                    found = t
                if not phase:
                    break
        if found is None:
            full = feasible_intervals((*core, v), TARGET)
            if full:
                found = full[0][0]
                verify((*core, v), found)
            counts["full_solver_fallback"] += 1
        counts["witnessed"] += found is not None
        if found is None:
            examples.setdefault("missing_witness", [v])
        elif phase and not clock and not width:
            examples.setdefault("same_pass_gain_without_short_clock", [v, str(found)])
        elif not phase:
            examples.setdefault("same_pass_unresolved", [v, str(found)])
    return {"core": core, "strong_time": str(core_time) if strong else None,
            "chained_core": chained_core, "counts": dict(counts), "examples": examples}


def check_all_references(core, fastest):
    speeds = (0, *core, fastest)
    witnesses, certified = [], 0
    for ref in speeds:
        signed = tuple(v - ref for v in speeds if v != ref)
        classes = sorted({abs(v) for v in signed})
        retained, added = classes[:-1], classes[-1]
        strong = feasible_intervals(retained, STRONG)
        pairs = [pair_bound(u, w, N) for u, w in combinations(retained, 2)]
        predicted = bool(strong) and not any(can_trap_pair(p, added) for p in pairs)
        if predicted:
            left, right = component_at_strong_time(retained, strong[0][0], N)
            t = witness_on_component(left, right, added, TARGET)
            assert t is not None
            certified += 1
        else:
            full = feasible_intervals(classes, TARGET)
            t = full[0][0] if full else None
        if t is not None:
            verify(signed, t)
        witnesses.append({"reference_speed": ref, "same_pass": predicted,
                          "witness": str(t) if t is not None else None})
    return {"core": core, "fastest": fastest, "same_pass_references": certified,
            "verified_references": sum(row["witness"] is not None for row in witnesses),
            "witnesses": witnesses}


def main():
    panels = cohorts()
    report = {"oracle_triples": independent_checks(), "panels": {}}
    for label, cores in panels.items():
        rows = [check_core(c) for c in cores]
        total = Counter()
        for row in rows:
            total.update(row["counts"])
        report["panels"][label] = {"cores": len(cores), "strong_cores":
                                   sum(r["strong_time"] is not None for r in rows),
                                   "chained_cores": sum(r["chained_core"] for r in rows),
                                   "counts": dict(total), "rows": rows}
    all_refs = [check_all_references(c, v) for c in panels["sparse"] + panels["challenge"]
                for v in (c[-1]+1, 2*c[-1])]
    report["all_references"] = {
        "groups": len(all_refs), "groups_certified": sum(r["same_pass_references"] == N for r in all_refs),
        "groups_verified": sum(r["verified_references"] == N for r in all_refs),
        "references_certified": sum(r["same_pass_references"] for r in all_refs),
        "references_verified": sum(r["verified_references"] for r in all_refs), "rows": all_refs}
    print(json.dumps(report, separators=(",", ":")))


if __name__ == "__main__":
    main()
