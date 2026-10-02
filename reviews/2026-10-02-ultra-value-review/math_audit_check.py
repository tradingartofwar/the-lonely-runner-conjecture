"""Small, fixed exact audit; no imports from research implementations.

Run from any directory. Outputs only sibling math_audit_checks.json.
This is a post-exposure proof audit, not fresh validation or broad search.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math

DELTA = F(1, 8)
CORE = (1, 2, 3, 4, 5, 7, 10, 19)
I = (F(25, 152), F(7, 40))
SMALL = (6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23)


def safe(v, t):
    phase = v * t % 1
    return DELTA <= phase <= 1 - DELTA


def intersect(a, b):
    result = []
    for l, u in a:
        for L, U in b:
            x, y = max(l, L), min(u, U)
            if x <= y:
                result.append((x, y))
    result.sort()
    merged = []
    for l, u in result:
        if merged and l <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(u, merged[-1][1]))
        else:
            merged.append((l, u))
    return merged


def bands(v):
    return [((k + DELTA) / v, (k + 1 - DELTA) / v)
            for k in range(v)]


def complete(vs):
    result = [(F(0), F(1))]
    for v in vs:
        result = intersect(result, bands(v))
    return result


def contact(r, interval=I):
    l, u = interval
    k = math.ceil(r * l - 1 + DELTA)
    return max(l, (k + DELTA) / r)


core = complete(CORE)
core_stages = {str(n): complete(CORE[:n]) for n in (5, 6, 7, 8)}
assert I in core
assert (F(1, 8), F(1, 8)) in core
assert I[1] - I[0] == F(1, 95)
endpoint_phases = [(v, v * I[0] % 1, v * I[1] % 1,
                    math.floor(v * I[0]), math.floor(v * I[1]))
                   for v in CORE]
assert all(DELTA <= a <= b <= 1 - DELTA and lap_a == lap_b
           for _, a, b, lap_a, lap_b in endpoint_phases)
small_records = []
for r in SMALL:
    exact_intersection = intersect([I], bands(r))
    candidate = contact(r)
    assert bool(exact_intersection) == (candidate <= I[1])
    if exact_intersection:
        assert candidate == exact_intersection[0][0]
    witness = F(1, 8) if r in (6, 12) else candidate
    assert all(safe(v, witness) for v in (*CORE, r))
    small_records.append(dict(r=r, interval_safe_set=exact_intersection,
                              candidate=candidate, witness=witness))
assert [row['r'] for row in small_records if not row['interval_safe_set']] == [6, 12]

# Complete sets for the two exceptional r and one singleton countercontrol.
whole_sets = {r: complete((*CORE, r)) for r in (6, 12, 8)}
isolated = [(l, u) for l, u in core if l == u]
positive = [(l, u) for l, u in core if l < u]
assert whole_sets[6] == whole_sets[12] == isolated
assert all(not intersect(positive, bands(r)) for r in (6, 12))
assert not intersect(isolated, bands(8))
assert whole_sets[8]

# Fixed tail controls use direct physical inequalities; no huge period expansion.
tail = []
for r in (24, 40, 80, 152 * 10**60):
    t = contact(r)
    assert I[0] <= t <= I[1]
    assert all(safe(v, t) for v in (*CORE, r))
    tail.append(dict(r=r, witness=t,
                     phases=[v * t % 1 for v in (*CORE, r)]))

# Clock lift failure is checked directly for (p,q,r)=(2,4,1).
lift_records = []
for j in range(2):
    J = ((I[0] + j) / 2, (I[1] + j) / 2)
    contact_set = intersect([J], bands(1))
    lift_records.append(dict(j=j, lifted_interval=J, contact_set=contact_set))
assert not lift_records[0]['contact_set']
assert lift_records[1]['contact_set']
lift_t = lift_records[1]['contact_set'][0][0]
assert all(safe(v, lift_t) for v in (*(2*x for x in CORE), 1))

# Deliberate weak-boundary controls, including exact width and singleton failure.
controls = []
for interval, r in [((F(7, 8), F(9, 8)), 1),
                    ((F(0), F(1, 8)), 1),
                    ((F(0), F(1, 9)), 1),
                    ((F(1, 8), F(1, 8)), 1),
                    ((F(0), F(0)), 1)]:
    t = contact(r, interval)
    hit = t <= interval[1]
    if hit:
        assert safe(r, t)
    controls.append(dict(interval=interval, r=r, contact=t, hit=hit))
assert [x['hit'] for x in controls] == [True, True, False, True, False]

out = dict(status='PASS', arithmetic='fractions.Fraction; no research-code imports',
           scope='post-exposure fixed proof audit, no fresh validation',
           interval=I, interval_width=I[1]-I[0],
           endpoint_phases=endpoint_phases, core=core, core_stages=core_stages,
           small=small_records, full_sets=whole_sets,
           tail=tail, clock_lifts=lift_records, boundary_controls=controls,
           singleton_sources=isolated, positive_source_count=len(positive),
           source_minimality='Two sources are necessary and sufficient when each source is one complete core component, chosen before r, with no fallback.')
target = Path(__file__).with_name('math_audit_checks.json')
target.write_text(json.dumps(out, default=str, indent=2) + '\n')
print(json.dumps(dict(status=out['status'], core_components=len(core),
                     positive_components=len(positive),
                     isolated_components=len(isolated), small_checks=len(SMALL),
                     small_interval_misses=[6,12], output=str(target)), indent=2))
