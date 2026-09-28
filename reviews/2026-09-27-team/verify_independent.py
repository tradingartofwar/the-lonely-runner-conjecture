"""Independent exact reconstruction of the frozen six-case transfer test.

The primary calculator is neither read nor imported. Threshold events on a
product-denominator grid produce point states, open-cell states, and complete
closed core-safe components. Point and cell membership are both used for set
containment. Representative subsets are exhausted, while maximum trees are
computed with Kruskal (not the primary's spanning-tree enumeration).

--write records the comparison; default/--check replays it without writing.
"""
import argparse
from bisect import bisect_left, bisect_right
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = '578ad79f2d65ffe7309e3b1ae576de98e24ccaab1c23d3ea2600cedb5a9636a2'
CORES = list(combinations(range(1, 8), 3))
CORE_MASKS = [sum(1 << (i-1) for i in core) for core in CORES]
EXTRAS = [tuple(i for i in range(1, 8) if i not in core) for core in CORES]
PAIR_POSITIONS = list(combinations(range(4), 2))
PROJECTED = [[sum(((state >> (runner-1)) & 1) << j
                 for j, runner in enumerate(extra)) for state in range(128)]
             for extra in EXTRAS]


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def digest(obj):
    return sha256(canonical(obj).encode()).hexdigest()


def exact_distance(speed, time):
    phase = (speed*time) % 1
    return min(phase, 1-phase)


def maximum_tree(nodes, pair_weights):
    """Maximum weight, then lexicographically first sorted edge list."""
    parent = {i: i for i in nodes}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    chosen, weight = [], 0
    for edge in sorted(combinations(nodes, 2),
                       key=lambda e: (-pair_weights[e], e)):
        a, b = map(find, edge)
        if a != b:
            parent[a] = b
            chosen.append(edge)
            weight += pair_weights[edge]
    assert len(chosen) == max(0, len(nodes)-1)
    return weight, sorted(chosen)


def induced_components(nodes, edges, active):
    remaining = {i for i in nodes if i in active}
    count = 0
    while remaining:
        count += 1
        reached = {min(remaining)}
        previous = set()
        while previous != reached:
            previous = set(reached)
            for a, b in edges:
                if a in remaining and b in remaining and (a in reached or b in reached):
                    reached.update((a, b))
        remaining.difference_update(reached)
    return count


def analyze_component(core_index, left, right, masses, point_states, cell_states):
    """All exact local information derives from event atoms and their masses."""
    extra = EXTRAS[core_index]
    present = point_states | cell_states
    states = [s for s in range(16) if present >> s & 1]
    singles = {i: sum(masses[s] for s in range(16) if s >> j & 1)
               for j, i in enumerate(extra)}
    pairs = {(extra[i], extra[j]): sum(masses[s] for s in range(16)
                                       if s >> i & 1 and s >> j & 1)
             for i, j in PAIR_POSITIONS}
    contained = {(i, j) for a, i in enumerate(extra) for b, j in enumerate(extra)
                 if all(not (s >> a & 1) or s >> b & 1 for s in states)}
    vanished = [i for a, i in enumerate(extra) if not any(s >> a & 1 for s in states)]
    # Exhaust representative subsets by cardinality, then original labels.
    retained = next(c for n in range(5) for c in combinations(extra, n)
                    if all(i in vanished or any((i, j) in contained for j in c)
                           for i in extra))
    classes, classified = [], set(vanished)
    for i in extra:
        if i not in classified:
            equal = [j for j in extra if j not in vanished
                     and (i, j) in contained and (j, i) in contained]
            classes.append(equal)
            classified.update(equal)
    assert all(min(group) in retained or any((group[0], j) in contained
               and (j, group[0]) not in contained for j in retained) for group in classes)
    width = right-left
    assert sum(masses) == width
    fw, fe = maximum_tree(extra, pairs)
    rw, re = maximum_tree(retained, pairs)
    full_bound = width-sum(singles.values())+fw
    reduced_bound = width-sum(singles[i] for i in retained)+rw
    assert full_bound == reduced_bound <= masses[0]
    full_components, reduced_components = [], []
    full_slack = reduced_slack = 0
    for s, mass in enumerate(masses):
        active = {i for p, i in enumerate(extra) if s >> p & 1}
        fc = induced_components(extra, fe, active)
        rc = induced_components(retained, re, active)
        full_components.append(fc)
        reduced_components.append(rc)
        assert bool(active) == bool(active.intersection(retained)) or not (present >> s & 1)
        full_slack += mass*max(0, fc-1)
        reduced_slack += mass*max(0, rc-1)
    assert full_slack == masses[0]-full_bound
    assert reduced_slack == masses[0]-reduced_bound
    return dict(core=CORES[core_index], extra=extra, window=(left, right), width=width,
                masses=masses, point_states=point_states, cell_states=cell_states,
                singles=singles, pairs=pairs, contained=contained, vanished=vanished,
                classes=classes, retained=retained, full_bound=full_bound,
                reduced_bound=reduced_bound, full_tree_weight=fw, reduced_tree_weight=rw,
                full_tree_edges=fe, reduced_tree_edges=re, actual=masses[0],
                full_active_components=full_components, reduced_active_components=reduced_components,
                slack=full_slack)


def reconstruct(velocities):
    assert len(velocities) == len(set(velocities)) == 8 and velocities[0] == 0
    speeds = [abs(v-velocities[0]) for v in velocities[1:]]
    scale = 8*prod(speeds)
    events = {0: [0, 0], scale: [0, 0]}
    for i, speed in enumerate(speeds):
        unit = scale//(8*speed)
        for lap in range(speed):
            events.setdefault((8*lap+1)*unit, [0, 0])[0] |= 1 << i
            events.setdefault((8*lap+7)*unit, [0, 0])[1] |= 1 << i
    times = sorted(events)
    full, full_start = [], None
    starts = [None]*35
    masses = [[0]*16 for _ in CORES]
    point_states, cell_states = [0]*35, [0]*35
    rows = [[] for _ in CORES]
    point_global, cell_global = [], []
    before = 127
    for t_index, time in enumerate(times):
        leaves, enters = events[time]
        point = before & ~(leaves | enters)
        after = (before & ~leaves) | enters
        point_global.append(point)
        cell_global.append(after)
        if not point:
            if full_start is None:
                full_start = time
            if after:
                full.append((full_start, time))
                full_start = None
        else:
            assert full_start is None
        for c, mask in enumerate(CORE_MASKS):
            if not point & mask:
                if starts[c] is None:
                    starts[c] = time
                point_states[c] |= 1 << PROJECTED[c][point]
                if after & mask:
                    rows[c].append(analyze_component(c, starts[c], time, masses[c],
                                                     point_states[c], cell_states[c]))
                    starts[c] = None
                    masses[c], point_states[c], cell_states[c] = [0]*16, 0, 0
            else:
                assert starts[c] is None
            if t_index+1 < len(times) and not after & mask:
                state = PROJECTED[c][after]
                masses[c][state] += times[t_index+1]-time
                cell_states[c] |= 1 << state
        before = after
    assert full_start is None and all(s is None for s in starts)
    duration = sum(b-a for a, b in full)
    for core_rows in rows:
        assert sum(r['actual'] for r in core_rows) == duration
        for row in core_rows:
            a, b = row['window']
            row['allowed'] = [(u, v) for u, v in full if a <= u <= v <= b]
            assert sum(v-u for u, v in row['allowed']) == row['actual']
    candidates = [r for group in rows for r in group if r['width'] > 0]
    winner = min(candidates, key=lambda r: (-r['reduced_bound'], len(r['retained']),
                                          -r['width'], r['core'], r['window'][0]))
    endpoints = sorted({t for group in rows for r in group for t in r['window']})
    valid_endpoints = [t for t in endpoints
                       if all(exact_distance(v, Fraction(t, scale)) >= Fraction(1, 8)
                              for v in speeds)]
    assert bool(valid_endpoints) == bool(full)
    return dict(scale=scale, speeds=speeds, rows=rows, full=full, duration=duration,
                winner=winner, endpoints=endpoints, valid_endpoints=valid_endpoints,
                times=times, point_global=point_global, cell_global=cell_global)


def rational(value, scale):
    return str(Fraction(value, scale))


def intervals(pieces, scale):
    return [[rational(a, scale), rational(b, scale)] for a, b in pieces]


def relation_edges(row):
    return [[i, j] for i, j in sorted(row['contained']) if i != j]


def proper_edges(row):
    return [[i, j] for i, j in sorted(row['contained'])
            if i != j and i not in row['vanished'] and (j, i) not in row['contained']]


def equal_classes(row):
    return [group for group in row['classes'] if len(group) >= 2]


def selection_key(row):
    return (-row['reduced_bound'], len(row['retained']), -row['width'],
            row['core'], row['window'][0])


COUNT_FIELDS = ('components', 'singleton_components', 'positive_bound_components',
                'positive_actual_components', 'positive_actual_tree_misses',
                'positive_bound_without_reduction',
                'positive_bound_without_nonempty_containment',
                'windows_with_vanished', 'windows_with_nonempty_proper_containment',
                'windows_with_equal_nonempty', 'windows_with_reduction',
                'full_reduced_bound_mismatches', 'allowed_set_reduction_mismatches',
                'slack_identity_mismatches', 'exact_tree_components',
                'positive_slack_components')


def summarize(rows, scale):
    result = {key: 0 for key in COUNT_FIELDS}
    result.update(retained_count_histogram=[0]*5, vanished_count_histogram=[0]*5)
    for row in rows:
        bound, actual = row['reduced_bound'], row['actual']
        proper, equals = proper_edges(row), equal_classes(row)
        reduced = len(row['retained']) < 4
        result['components'] += 1
        result['singleton_components'] += row['width'] == 0
        result['positive_bound_components'] += bound > 0
        result['positive_actual_components'] += actual > 0
        result['positive_actual_tree_misses'] += actual > 0 and bound <= 0
        result['positive_bound_without_reduction'] += bound > 0 and not reduced
        result['positive_bound_without_nonempty_containment'] += bound > 0 and not proper and not equals
        result['windows_with_vanished'] += bool(row['vanished'])
        result['windows_with_nonempty_proper_containment'] += bool(proper)
        result['windows_with_equal_nonempty'] += bool(equals)
        result['windows_with_reduction'] += reduced
        result['retained_count_histogram'][len(row['retained'])] += 1
        result['vanished_count_histogram'][len(row['vanished'])] += 1
        result['exact_tree_components'] += row['slack'] == 0
        result['positive_slack_components'] += row['slack'] > 0
    result.update(sum_tree_slack=rational(sum(r['slack'] for r in rows), scale),
                  maximum_tree_slack=rational(max(r['slack'] for r in rows), scale),
                  minimum_bound=rational(min(r['reduced_bound'] for r in rows), scale),
                  maximum_bound=rational(max(r['reduced_bound'] for r in rows), scale))
    return result


def aggregate(summaries):
    result = {key: sum(s[key] for s in summaries) for key in COUNT_FIELDS}
    for field in ('retained_count_histogram', 'vanished_count_histogram'):
        result[field] = [sum(s[field][i] for s in summaries) for i in range(5)]
    result['sum_tree_slack'] = str(sum((Fraction(s['sum_tree_slack']) for s in summaries), Fraction(0)))
    for field, operation in (('maximum_tree_slack', max), ('minimum_bound', min), ('maximum_bound', max)):
        result[field] = str(operation(Fraction(s[field]) for s in summaries))
    result['positive_cores'] = sum(s.get('positive_cores', int(s['positive_bound_components'] > 0))
                                   for s in summaries)
    return result


def component_digest(rows, scale):
    accumulator = sha256()
    for row in rows:
        payload = [*intervals([row['window']], scale)[0],
                   rational(row['reduced_bound'], scale), rational(row['actual'], scale),
                   row['vanished'], relation_edges(row), list(row['retained'])]
        accumulator.update((json.dumps(payload, separators=(',', ':'))+'\n').encode())
    return accumulator.hexdigest()


def q_record(row, rows, scale):
    return dict(component_index=next(i for i, item in enumerate(rows) if item is row),
                window=intervals([row['window']], scale)[0],
                bound=rational(row['reduced_bound'], scale),
                actual_duration=rational(row['actual'], scale), retained=list(row['retained']),
                tree_slack=rational(row['slack'], scale),
                tree_edges=[list(edge) for edge in row['reduced_tree_edges']])


def blocker_components(reconstruction, row, runner):
    """Stitch strict bad cells and occupied boundary points without intervals."""
    a, b = row['window']
    times = reconstruction['times']
    lo, hi = bisect_left(times, a), bisect_right(times, b)
    assert times[lo] == a and times[hi-1] == b
    pieces, start = [], None
    flag = 1 << (runner-1)
    for index in range(lo, hi):
        t = times[index]
        point = bool(reconstruction['point_global'][index] & flag)
        after = index < hi-1 and bool(reconstruction['cell_global'][index] & flag)
        if start is not None and not point:
            pieces.append((start[0], t, start[1], False))
            start = None
        if point and start is None:
            start = (t, True)
        if after and start is None:
            start = (t, False)
        if not after and start is not None:
            pieces.append((start[0], t, start[1], point))
            start = None
    assert start is None
    scale = reconstruction['scale']
    return [[rational(x, scale), rational(y, scale), xc, yc] for x, y, xc, yc in pieces]


def assert_fields(expected, actual, label):
    for field, value in expected.items():
        assert field in actual, (label, 'missing', field)
        assert actual[field] == value, (label, field, 'computed', value, 'archived', actual[field])


def verify_witness(witness, velocities, allowed, scale, require_strict=True):
    if witness is None:
        assert not allowed
        return
    time = Fraction(witness['time'])
    assert any(Fraction(a, scale) <= time <= Fraction(b, scale) for a, b in allowed)
    distances = [exact_distance(v-velocities[0], time) for v in velocities[1:]]
    assert min(distances) >= Fraction(1, 8)
    assert witness['distances'] == list(map(str, distances))
    assert witness['kind'] == ('strict' if min(distances) > Fraction(1, 8) else 'equality')
    if require_strict and any(a < b for a, b in allowed):
        assert witness['kind'] == 'strict'


def verify_selected(row, reconstruction, archive, velocities):
    scale = reconstruction['scale']
    core_index = CORES.index(row['core'])
    expected = q_record(row, reconstruction['rows'][core_index], scale)
    expected.update(core=list(row['core']), residual=list(row['extra']),
                    core_speeds=[velocities[i] for i in row['core']],
                    residual_speeds=[velocities[i] for i in row['extra']],
                    full_bound=rational(row['full_bound'], scale),
                    full_tree_edges=[list(edge) for edge in row['full_tree_edges']],
                    vanished=row['vanished'], containment_edges=relation_edges(row),
                    proper_nonempty_containment_edges=proper_edges(row),
                    equal_nonempty_classes=equal_classes(row),
                    removed_cover=[[i, min(j for j in row['retained'] if (i, j) in row['contained'])]
                                   for i in row['extra'] if i not in row['retained'] and i not in row['vanished']],
                    strict_blocker_components=[[i, blocker_components(reconstruction, row, i)] for i in row['extra']],
                    single_durations=[[i, rational(row['singles'][i], scale)] for i in row['extra']],
                    pair_durations=[[i, j, rational(value, scale)] for (i, j), value in row['pairs'].items()],
                    allowed_components=intervals(row['allowed'], scale))
    all_subsets = [[i for p, i in enumerate(row['extra']) if mask >> p & 1] for mask in range(16)]
    expected['intersection_durations'] = [[subset, rational(sum(m for s, m in enumerate(row['masses'])
                                                                 if s & mask == mask), scale)]
                                          for mask, subset in enumerate(all_subsets)]
    expected['active_state_durations'] = [[subset, rational(row['masses'][mask], scale)]
                                         for mask, subset in enumerate(all_subsets)]
    expected['slack_by_active_components'] = [[count, rational(sum(m for mask, m in enumerate(row['masses'])
                                                               if row['full_active_components'][mask] == count), scale)]
                                             for count in range(5)]
    assert_fields(expected, archive, 'selected_certificate')
    verify_witness(archive['witness'], velocities, row['allowed'], scale)


def verify_case(case, record):
    result = reconstruct(case['velocities'])
    scale = result['scale']
    assert record['id'] == case['id'] and record['velocities'] == case['velocities']
    assert record['reference_index'] == 0
    # Primary coordinates need not be our independent product grid.
    denominator = record['integer_denominator']
    assert isinstance(denominator, int) and all(denominator % (8*v) == 0 for v in result['speeds'])
    assert_fields(dict(full_allowed_components=intervals(result['full'], scale),
                       full_allowed_duration=rational(result['duration'], scale),
                       full_positive_component_count=sum(a < b for a, b in result['full']),
                       full_isolated_points=[rational(a, scale) for a, b in result['full'] if a == b],
                       time_one_eighth_distances=[str(exact_distance(v, Fraction(1, 8))) for v in result['speeds']]),
                  record, case['id'])
    verify_witness(record['global_witness'], case['velocities'], result['full'], scale)
    assert len(record['cores']) == len(CORES)
    summaries = []
    independent_core_digests = []
    for c, rows in enumerate(result['rows']):
        summary = summarize(rows, scale)
        candidates = [row for row in rows if row['width'] > 0]
        best = min(candidates, key=selection_key) if candidates else None
        expected = dict(core=list(CORES[c]), residual=list(EXTRAS[c]),
                        component_sha256=component_digest(rows, scale), summary=summary,
                        q_best=q_record(best, rows, scale) if best is not None else None)
        assert_fields(expected, record['cores'][c], (case['id'], CORES[c]))
        independent_core_digests.append(expected['component_sha256'])
        summaries.append(summary)
    case_summary = aggregate(summaries)
    assert_fields(case_summary, record['summary'], (case['id'], 'summary'))
    winner = result['winner']
    verify_selected(winner, result, record['selected_certificate'], case['velocities'])
    if winner['reduced_bound'] > 0:
        assert record['selection_outcome'] == 'positive_tree' and record['endpoint_fallback'] is None
    else:
        first = result['valid_endpoints'][0] if result['valid_endpoints'] else None
        fallback = record['endpoint_fallback']
        assert fallback['candidate_count'] == len(result['endpoints'])
        assert fallback['tested_count'] == (result['endpoints'].index(first)+1 if first is not None else len(result['endpoints']))
        assert record['selection_outcome'] == ('endpoint_fallback' if first is not None else 'inconclusive')
        verify_witness(fallback['witness'], case['velocities'], result['full'], scale, require_strict=False)
        if first is not None:
            assert fallback['witness']['time'] == rational(first, scale)
    assert record['strict_all_core_failure'] == bool(result['duration'] and winner['reduced_bound'] <= 0)
    flat = [row for rows in result['rows'] for row in rows]
    fastest = max(range(1, 8), key=lambda i: abs(case['velocities'][i]-case['velocities'][0]))
    fastest_cores = [rows for c, rows in enumerate(result['rows']) if fastest in CORES[c]]
    fastest_rows = [row for rows in fastest_cores for row in rows]
    fastest_diagnostic = dict(fastest_runner_index=fastest, cores=len(fastest_cores),
                              components=len(fastest_rows),
                              exact_components=sum(row['slack'] == 0 for row in fastest_rows),
                              nonexact_components=sum(row['slack'] != 0 for row in fastest_rows),
                              maximum_slack=rational(max(row['slack'] for row in fastest_rows), scale))
    assert_fields(fastest_diagnostic, record['fastest_core_diagnostic'], (case['id'], 'fastest_core_diagnostic'))
    tie_bound = [row for row in flat if row['width'] > 0 and row['reduced_bound'] == winner['reduced_bound']]
    tie_count = [row for row in tie_bound if len(row['retained']) == len(winner['retained'])]
    tie_width = [row for row in tie_count if row['width'] == winner['width']]
    tie_core = [row for row in tie_width if row['core'] == winner['core']]
    return dict(id=case['id'], components=len(flat),
                singleton_components=case_summary['singleton_components'],
                core_component_digests=independent_core_digests,
                full_allowed_components_sha256=digest(intervals(result['full'], scale)),
                full_allowed_duration=rational(result['duration'], scale),
                full_isolated_points=[rational(a, scale) for a, b in result['full'] if a == b],
                positive_cores=case_summary['positive_cores'],
                positive_bound_components=case_summary['positive_bound_components'],
                positive_actual_tree_misses=case_summary['positive_actual_tree_misses'],
                strict_all_core_failure=record['strict_all_core_failure'],
                selected_core=list(winner['core']),
                selected_window=intervals([winner['window']], scale)[0],
                selected_bound=rational(winner['reduced_bound'], scale),
                selected_retained=list(winner['retained']),
                fastest_core_diagnostic=fastest_diagnostic,
                selection_ties_remaining_after_each_key=[len(tie_bound), len(tie_count), len(tie_width), len(tie_core), 1],
                summary=case_summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument('--write', action='store_true')
    choice.add_argument('--check', action='store_true')
    args = parser.parse_args()
    protocol_bytes = (HERE/'protocol.json').read_bytes()
    assert sha256(protocol_bytes).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(protocol_bytes)
    assert protocol['n'] == 8 and protocol['reference_index'] == 0
    assert protocol['threshold'] == '1/8' and protocol['time_interval'] == ['0', '1']
    assert len(protocol['cases']) == 6
    result_bytes = (HERE/'results.json').read_bytes()
    source = json.loads(result_bytes)
    assert source['schema_version'] == 1 and source['protocol_sha256'] == PROTOCOL_SHA256
    assert source['core_order'] == [list(core) for core in CORES]
    assert len(source['cases']) == 6
    records = []
    for case, record in zip(protocol['cases'], source['cases']):
        result = verify_case(case, record)
        records.append(result)
        print('PASS:', case['id'], result['components'], 'complete components', flush=True)
    totals = aggregate([record['summary'] for record in records])
    assert_fields(totals, source['totals'], 'totals')
    out = dict(status='REPRODUCED within the six fixed configurations, reference 0 only',
               protocol_sha256=PROTOCOL_SHA256,
               source_results_sha256=sha256(result_bytes).hexdigest(),
               source_primary_script_sha256=source['script_sha256'],
               verifier_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
               methods=['integer product-denominator threshold-event sweep',
                        'separate point and open-cell blocker states for strict containment',
                        'exhaustive minimal covering representative subsets',
                        'Kruskal maximum spanning trees with lexicographic edge ties',
                        'induced active-subgraph component-count slack identity',
                        'all core digest streams, selection ties, and direct witness distances'],
               configurations=6, references=6, labelled_cores=210,
               components=sum(record['components'] for record in records),
               core_digest_comparisons=210,
               strict_all_core_failures=sum(record['strict_all_core_failure'] for record in records),
               totals=totals, cases=records)
    destination = HERE/'verification.json'
    if args.write:
        destination.write_text(json.dumps(out, indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == out
    print('PASS: all six cases, 210 cores,', out['components'], 'components; read-only replay' if not args.write else 'components; comparison saved')


if __name__ == '__main__':
    main()
