"""Bounded retrospective constructive diagnostic; exact, no project imports.

The candidate rule was written in structure.md before this script was run.
Default and --check compare with the committed structure.json read-only.
--write writes only this review's structure.json.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'protocol.json'
OUT = HERE / 'structure.json'
PRIMARY = HERE / 'results.json'
D = F(1, 8)


def distance(x):
    r = x % 1
    return min(r, 1-r)


def distances(speeds, t):
    return [distance(v*t) for v in speeds]


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def interval_min_distance(v, a, b):
    left, right = v*a, v*b
    if ceil(left) <= floor(right):
        return F(0)
    return min(distance(left), distance(right))


def reciprocal_diagnostic(case):
    speeds = case['velocities'][1:]
    sources = {}
    def add(t, label):
        sources.setdefault(t, []).append(label)
    add(F(1, 2*min(speeds)), 'half_slowest_lap')
    for v, w in combinations(speeds, 2):
        add(F(1, v+w), f'pair_sum:{v}+{w}')
    rows = []
    for t in sorted(sources):
        ds = distances(speeds, t)
        # A second form evaluates the same rational substitutions with integers.
        integer_ds = [F(min((v*t.numerator) % t.denominator,
                            t.denominator-(v*t.numerator) % t.denominator),
                        t.denominator) for v in speeds]
        assert ds == integer_ds
        rows.append(dict(t=str(t), sources=sources[t],
                         distances=list(map(str, ds)), minimum=str(min(ds)),
                         safe=min(ds) >= D, strict=min(ds) > D))
    passing = [r for r in rows if r['strict']]
    selected = None
    if passing:
        row = passing[0]
        t = F(row['t'])
        ds = list(map(F, row['distances']))
        radius = min((d-D)/v for d, v in zip(ds, speeds))
        a, b = t-radius/2, t+radius/2
        interval_ds = [interval_min_distance(v, a, b) for v in speeds]
        assert F(0) <= a < b <= F(1)
        assert min(interval_ds) > D
        selected = dict(**row, lipschitz_radius=str(radius),
                        local_strict_interval=[str(a), str(b)],
                        interval_min_distances=list(map(str, interval_ds)),
                        trivial_tree_bound=str(b-a))
    half = next(r for r in rows if 'half_slowest_lap' in r['sources'])
    return dict(id=case['id'], velocities=case['velocities'],
                distinct_candidate_count=len(rows),
                safe_count=sum(r['safe'] for r in rows),
                strict_count=len(passing), half_slowest_lap=half,
                earliest_strict=selected, candidates=rows)


def active_components(active, edges):
    """Count forest components by explicit flood fill, including isolates."""
    unseen = set(active)
    count = 0
    while unseen:
        count += 1
        reached = {min(unseen)}
        while True:
            expanded = reached | {b for a, b in edges if a in reached and b in unseen}
            expanded |= {a for a, b in edges if b in reached and a in unseen}
            if expanded == reached:
                break
            reached = expanded
        unseen -= reached
    return count


def selected_analysis(case):
    """Rebuild only the primary Q winner's exact event cells and tree slack."""
    cert = case['selected_certificate']
    speeds = case['velocities']
    residual = cert['residual']
    a, b = map(F, cert['window'])
    cuts = {a, b}
    for i in residual:
        v = speeds[i]
        for m in range(v):
            for phase in (D, 1-D):
                t = (m+phase)/v
                if a < t < b:
                    cuts.add(t)
    cuts = sorted(cuts)
    masses = {}
    cells = []
    for x, y in zip(cuts, cuts[1:]):
        mid = (x+y)/2
        active = tuple(i for i in residual if distance(speeds[i]*mid) < D)
        masses[active] = masses.get(active, F(0)) + y-x
        cells.append((x, y, active))
    primary_masses = {tuple(s): F(d) for s, d in cert['active_state_durations'] if F(d)}
    assert masses == primary_masses
    assert masses.get((), F(0)) == F(cert['actual_duration'])
    singles = {i: sum(d for s, d in masses.items() if i in s) for i in residual}
    pairs = {e: sum(d for s, d in masses.items() if set(e) <= set(s))
             for e in combinations(residual, 2)}
    total_singles = sum(singles.values(), F(0))
    # Enumerate the 16 labelled trees, independently of the primary choice.
    values = []
    for edges in combinations(list(pairs), len(residual)-1):
        if active_components(residual, edges) == 1:
            values.append((b-a-total_singles+sum(pairs[e] for e in edges), edges))
    best = max(value for value, _ in values)
    assert best == F(cert['bound']) == F(cert['full_bound'])
    tree = [tuple(e) for e in cert['full_tree_edges']]
    assert b-a-total_singles+sum(pairs[e] for e in tree) == best
    patterns = []
    fragmentation = F(0)
    for s, d in sorted(masses.items()):
        count = active_components(s, tree)
        cost = max(count-1, 0)*d
        fragmentation += cost
        patterns.append(dict(active_indices=list(s), active_speeds=[speeds[i] for i in s],
                             duration=str(d), induced_components=count,
                             fragmentation_cost=str(cost)))
    assert fragmentation == F(cert['tree_slack'])
    assert fragmentation == masses.get((), F(0))-best
    fastest_index = max(range(1, len(speeds)), key=lambda i: abs(speeds[i]))
    fast_cores = [r for r in case['cores'] if fastest_index in r['core']]
    assert len(fast_cores) == 15
    fastest = dict(
        core_count=len(fast_cores),
        components=sum(r['summary']['components'] for r in fast_cores),
        exact_tree_components=sum(r['summary']['exact_tree_components'] for r in fast_cores),
        positive_actual_tree_misses=sum(r['summary']['positive_actual_tree_misses'] for r in fast_cores),
        positive_cores=sum(r['summary']['positive_bound_components'] > 0 for r in fast_cores),
        maximum_bound=str(max(F(r['summary']['maximum_bound']) for r in fast_cores)))
    assert fastest['components'] == fastest['exact_tree_components']
    assert fastest['positive_actual_tree_misses'] == 0
    return dict(id=case['id'], core_speeds=cert['core_speeds'],
                window=cert['window'], bound=cert['bound'],
                actual_duration=cert['actual_duration'], tree_slack=cert['tree_slack'],
                full_tree_speed_edges=[[speeds[i], speeds[j]] for i, j in tree],
                retained_speeds=[speeds[i] for i in cert['retained']],
                vanished_speeds=[speeds[i] for i in cert['vanished']],
                proper_nonempty_containment_speed_edges=[
                    [speeds[i], speeds[j]] for i, j in cert['proper_nonempty_containment_edges']],
                blocker_interval_counts=[
                    [speeds[i], len(parts)] for i, parts in cert['strict_blocker_components']],
                active_patterns=patterns,
                positive_fragmentation_patterns=[r for r in patterns if F(r['fragmentation_cost']) > 0],
                fragmentation_open_cells=[dict(window=[str(x), str(y)],
                    active_speeds=[speeds[i] for i in s],
                    induced_components=active_components(s, tree))
                    for x, y, s in cells if active_components(s, tree) > 1],
                fastest_core_summary=fastest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--include-primary', action='store_true',
                        help='Include fixed primary Q-winner structural review')
    args = parser.parse_args()
    protocol = json.loads(PROTOCOL.read_text())
    result = dict(
        status='OBSERVED; retrospective diagnostic, separate from primary selection',
        scope='Only six protocol cases, reference 0, n=8, threshold 1/8',
        rule='1/(2*v_min) and 1/(v_i+v_j), all unordered nonreference pairs; earliest strict',
        protocol_sha256=sha256(PROTOCOL.read_bytes()).hexdigest(),
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        cases=[reciprocal_diagnostic(case) for case in protocol['cases']])
    include_primary = args.include_primary
    if not args.write and OUT.exists():
        include_primary |= 'primary_structural_review' in json.loads(OUT.read_text())
    if include_primary:
        primary = json.loads(PRIMARY.read_text())
        assert primary['protocol_sha256'] == result['protocol_sha256']
        assert [c['id'] for c in primary['cases']] == [c['id'] for c in result['cases']]
        result['primary_results_sha256'] = sha256(PRIMARY.read_bytes()).hexdigest()
        result['primary_structural_review'] = [selected_analysis(c) for c in primary['cases']]
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(OUT.read_text()), 'structure.json differs'
    print(json.dumps(dict(status='PASS', cases=[dict(
        id=c['id'], tested=c['distinct_candidate_count'], strict=c['strict_count'],
        earliest=c['earliest_strict']['t'] if c['earliest_strict'] else None,
        half_slowest_minimum=c['half_slowest_lap']['minimum']) for c in result['cases']]), indent=2))


if __name__ == '__main__':
    main()
