"""Independent event-state and Kruskal check of the frozen 29 fastest laps.

No primary or phase-calculation implementation is read or imported. Direct
phase equations create threshold events. Exact point states and open-cell
states retain strict blocker endpoints and isolated allowed contacts.
--write saves the comparison; default/--check replays without writes.
"""
import argparse
from bisect import bisect_left, bisect_right
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = 'f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d'
SPEEDS = (1, 4, 5, 6, 7, 11)
EDGES = list(combinations(range(1, 7), 2))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def distance(speed, time, phase=Q(0)):
    z = (speed*time+phase) % 1
    return min(z, 1-z)


def fraction(value, scale):
    return str(Q(value, scale))


def intervals(value, scale):
    return [[fraction(a, scale), fraction(b, scale)] for a, b in value]


def threshold_sweep(velocities, phases=None):
    """Integer events from v*t+phase = integer+1/8 or integer+7/8."""
    speeds = velocities[1:]
    phases = [Q(0)]*len(speeds) if phases is None else phases
    scale = 8*prod(speeds)
    events = {0: [0, 0], scale: [0, 0]}
    for i, (speed, phase) in enumerate(zip(speeds, phases)):
        for integer in range(-1, speed+2):
            for kind, level in enumerate((Q(1, 8), Q(7, 8))):
                time = (integer+level-phase)/speed
                if 0 <= time <= 1:
                    location = time*scale
                    assert location.denominator == 1
                    events.setdefault(int(location), [0, 0])[kind] |= 1 << i
    times = sorted(events)
    before = sum((distance(v, -Q(1, 2*scale), phase) < Q(1, 8)) << i
                 for i, (v, phase) in enumerate(zip(speeds, phases)))
    points, cells = [], []
    for time in times:
        leaves, enters = events[time]
        point = before & ~(leaves | enters)
        after = (before & ~leaves) | enters
        points.append(point)
        cells.append(after)
        before = after
    # Direct distances at each threshold are a separate local endpoint check.
    for time, point in zip(times, points):
        assert point == sum((distance(v, Q(time, scale), phase) < Q(1, 8)) << i
                            for i, (v, phase) in enumerate(zip(speeds, phases)))
    return dict(scale=scale, times=times, points=points, cells=cells,
                velocities=velocities, phases=phases)


def closed_allowed(sweep, mask, left=0, right=None):
    times = sweep['times']
    right = sweep['scale'] if right is None else right
    lo, hi = bisect_left(times, left), bisect_right(times, right)
    assert times[lo] == left and times[hi-1] == right
    result, start = [], None
    for index in range(lo, hi):
        time = times[index]
        point_safe = not sweep['points'][index] & mask
        cell_safe = index < hi-1 and not sweep['cells'][index] & mask
        if point_safe:
            if start is None:
                start = time
            if not cell_safe:
                result.append((start, time))
                start = None
        else:
            assert start is None and not cell_safe
    assert start is None
    return result


def strict_blocker(sweep, runner, left, right):
    times = sweep['times']
    lo, hi = bisect_left(times, left), bisect_right(times, right)
    assert times[lo] == left and times[hi-1] == right
    result, start = [], None
    flag = 1 << (runner-1)
    for index in range(lo, hi):
        time = times[index]
        point_bad = bool(sweep['points'][index] & flag)
        cell_bad = index < hi-1 and bool(sweep['cells'][index] & flag)
        if start is not None and not point_bad:
            result.append((start[0], time, start[1], False))
            start = None
        if point_bad and start is None:
            start = (time, True)
        if cell_bad and start is None:
            start = (time, False)
        if not cell_bad and start is not None:
            result.append((start[0], time, start[1], point_bad))
            start = None
    assert start is None
    return result


def maximum_tree(weights):
    roots = {i: i for i in range(1, 7)}
    def find(i):
        while i != roots[i]:
            roots[i] = roots[roots[i]]
            i = roots[i]
        return i
    edges, weight = [], 0
    for edge in sorted(EDGES, key=lambda edge: (-weights[edge], edge)):
        a, b = map(find, edge)
        if a != b:
            roots[a] = b
            edges.append(edge)
            weight += weights[edge]
    assert len(edges) == 5
    return weight, sorted(edges)


def induced_count(state, edges):
    remaining = {i for i in range(1, 7) if state >> (i-1) & 1}
    count = 0
    while remaining:
        count += 1
        reached, previous = {min(remaining)}, set()
        while reached != previous:
            previous = set(reached)
            for i, j in edges:
                if i in remaining and j in remaining and (i in reached or j in reached):
                    reached.update((i, j))
        remaining -= reached
    return count


def inspect_lap(sweep, lap):
    speed = sweep['velocities'][7]
    scale = sweep['scale']
    left, right = (8*lap+1)*(scale//(8*speed)), (8*lap+7)*(scale//(8*speed))
    times = sweep['times']
    lo, hi = bisect_left(times, left), bisect_right(times, right)
    assert times[lo] == left and times[hi-1] == right
    masses = [0]*64
    present_points, present_cells = set(), set()
    for index in range(lo, hi):
        present_points.add(sweep['points'][index] & 63)
        if index < hi-1:
            state = sweep['cells'][index] & 63
            present_cells.add(state)
            masses[state] += times[index+1]-times[index]
    blocks = {i: strict_blocker(sweep, i, left, right) for i in range(1, 7)}
    assert all(len(pieces) <= 1 for pieces in blocks.values())
    singles = {i: sum(value for state, value in enumerate(masses) if state >> (i-1) & 1)
               for i in range(1, 7)}
    pairs = {(i, j): sum(value for state, value in enumerate(masses)
                        if state >> (i-1) & 1 and state >> (j-1) & 1) for i, j in EDGES}
    tree_weight, tree_edges = maximum_tree(pairs)
    bound = right-left-sum(singles.values())+tree_weight
    allowed = closed_allowed(sweep, 127, left, right)
    actual = sum(b-a for a, b in allowed)
    slack_by_components = [0]*7
    for state, value in enumerate(masses):
        slack_by_components[induced_count(state, tree_edges)] += value
    assert sum(masses) == right-left
    assert actual == masses[0] == bound
    assert sum(max(i-1, 0)*value for i, value in enumerate(slack_by_components)) == actual-bound == 0
    return dict(lap=lap, window=(left, right), blocks=blocks,
                masses=masses, present_points=present_points, present_cells=present_cells,
                singles=singles, pairs=pairs, tree_weight=tree_weight, tree_edges=tree_edges,
                bound=bound, allowed=allowed, actual=actual,
                slack_by_components=slack_by_components)


def assert_fields(expected, actual, label):
    for field, value in expected.items():
        assert field in actual, (label, 'missing', field)
        assert actual[field] == value, (label, field, 'computed', value, 'archived', actual[field])


def controllers(sweep, time):
    return [i for i, (speed, phase) in enumerate(zip(sweep['velocities'][1:], sweep['phases']), 1)
            if distance(speed, Q(time, sweep['scale']), phase) == Q(1, 8)]


def is_allowed(sweep, time):
    return all(distance(speed, Q(time, sweep['scale']), phase) >= Q(1, 8)
               for speed, phase in zip(sweep['velocities'][1:], sweep['phases']))


def witness(sweep, allowed, widest=True):
    if not allowed:
        return None
    positive = [(a, b) for a, b in allowed if a < b]
    if positive:
        a, b = min(positive, key=lambda edge: (edge[0]-edge[1], edge[0])) if widest else positive[0]
        time = Q(a+b, 2*sweep['scale'])
    else:
        time = Q(allowed[0][0], sweep['scale'])
    distances = [distance(speed, time, phase)
                 for speed, phase in zip(sweep['velocities'][1:], sweep['phases'])]
    assert min(distances) >= Q(1, 8)
    kind = 'strict' if min(distances) > Q(1, 8) else 'equality'
    if positive:
        assert kind == 'strict'
    return dict(time=str(time), distances=list(map(str, distances)), kind=kind)


def encode_strict(piece, scale, fastest=None, lap=0):
    if piece is None:
        return None
    a, b, ac, bc = piece
    if fastest is None:
        return [fraction(a, scale), fraction(b, scale), ac, bc]
    return [str(Q(a*fastest, scale)-lap), str(Q(b*fastest, scale)-lap), ac, bc]


def lap_record(sweep, row):
    scale = sweep['scale']
    fastest = sweep['velocities'][7]
    lap = row['lap']
    left, right = row['window']
    vanished = [i for i, pieces in row['blocks'].items() if not pieces]
    nonempty = [i for i in range(1, 7) if i not in vanished]
    nonempty.sort(key=lambda i: (row['blocks'][i][0][0], -row['blocks'][i][0][1], i))
    states = row['present_points'] | row['present_cells']
    contained = [[i, j] for i in range(1, 7) for j in range(1, 7) if i != j
                 and all(not (state >> (i-1) & 1) or state >> (j-1) & 1 for state in states)]
    blocks = []
    for i in range(1, 7):
        piece = row['blocks'][i][0] if row['blocks'][i] else None
        collision = None
        if piece is not None:
            midpoint = Q(piece[0]+piece[1], 2*scale)
            speed = sweep['velocities'][i]
            collision = (speed*midpoint+Q(1, 2)).numerator//(speed*midpoint+Q(1, 2)).denominator
            assert abs(speed*midpoint-collision) < Q(1, 8)
        blocks.append(dict(index=i, speed=sweep['velocities'][i], collision_lap=collision,
                           interval=encode_strict(piece, scale),
                           normalized_interval=encode_strict(piece, scale, fastest, lap)))
    scan, touching, frontier = [], {}, None
    for i in nonempty:
        a, b, ac, bc = row['blocks'][i][0]
        previous = None if frontier is None else [fraction(frontier[0], scale), frontier[1]]
        survives, control = None, []
        if frontier is None:
            junction, advances = 'first', True
            frontier = (b, bc)
        else:
            junction = 'overlap' if a < frontier[0] else ('touch' if a == frontier[0] else 'gap')
            if junction == 'touch':
                survives, control = is_allowed(sweep, a), controllers(sweep, a)
                touching[a] = [fraction(a, scale), survives, control]
            advances = b > frontier[0]
            if advances:
                frontier = (b, bc)
            elif b == frontier[0]:
                frontier = (b, bc or frontier[1])
        scan.append(dict(index=i, junction=junction, frontier_before=previous,
                         frontier_after=[fraction(frontier[0], scale), frontier[1]],
                         advances=advances, touch_survives=survives, touch_controllers=control))
    initial_gap = (left, row['blocks'][nonempty[0]][0][0]) if nonempty else (left, right)
    final_gap = (frontier[0], right) if frontier is not None else None
    if initial_gap[0] == initial_gap[1]:
        initial_gap = None
    if final_gap is not None and final_gap[0] == final_gap[1]:
        final_gap = None
    allowed = row['allowed']
    status = 'strict' if row['actual'] else ('contacts' if allowed else 'covered')
    return dict(m=lap, window=intervals([row['window']], scale)[0], width=fraction(right-left, scale),
                residues=[[i, sweep['velocities'][i]*lap % fastest] for i in range(1, 7)],
                residue_lifts=[[i, sweep['velocities'][i]*lap//fastest] for i in range(1, 7)],
                blockers=blocks, vanished=vanished, containment_edges=contained,
                qualitative_signature=[vanished, nonempty, contained],
                single_durations=[[i, fraction(row['singles'][i], scale)] for i in range(1, 7)],
                pair_durations=[[i, j, fraction(row['pairs'][i, j], scale)] for i, j in EDGES],
                tree_edges=[list(edge) for edge in row['tree_edges']],
                tree_weight=fraction(row['tree_weight'], scale), tree_bound=fraction(row['bound'], scale),
                actual_duration=fraction(row['actual'], scale), tree_slack=fraction(row['actual']-row['bound'], scale),
                union_duration=fraction(right-left-row['actual'], scale),
                allowed_components=intervals(allowed, scale),
                isolated_points=[fraction(a, scale) for a, b in allowed if a == b], status=status,
                witness=witness(sweep, allowed),
                allowed_endpoint_controllers=[[fraction(t, scale), controllers(sweep, t)]
                                               for t in sorted({u for interval in allowed for u in interval})],
                coverage_scan=scan,
                scan_initial_gap=intervals([initial_gap], scale)[0] if initial_gap is not None else None,
                scan_final_gap=intervals([final_gap], scale)[0] if final_gap is not None else None,
                scan_touch_points=[touching[t] for t in sorted(touching)])


def summarize_laps(rows):
    return dict(laps=len(rows), covered_laps=sum(row['status'] == 'covered' for row in rows),
                contact_only_laps=sum(row['status'] == 'contacts' for row in rows),
                strict_laps=sum(row['status'] == 'strict' for row in rows),
                positive_tree_laps=sum(Q(row['tree_bound']) > 0 for row in rows),
                exact_tree_laps=sum(Q(row['tree_slack']) == 0 for row in rows),
                isolated_point_count=sum(len(row['isolated_points']) for row in rows),
                positive_component_count=sum(a != b for row in rows for a, b in row['allowed_components']),
                touch_junction_count=sum(s['junction'] == 'touch' for row in rows for s in row['coverage_scan']),
                surviving_touch_count=sum(s['touch_survives'] is True for row in rows for s in row['coverage_scan']),
                maximum_tree_slack=str(max(Q(row['tree_slack']) for row in rows)))


def common_start_case(case):
    velocities = case['velocities']
    sweep = threshold_sweep(velocities)
    rows = [inspect_lap(sweep, lap) for lap in range(velocities[7])]
    encoded = [lap_record(sweep, row) for row in rows]
    full = closed_allowed(sweep, 127)
    fixed = closed_allowed(sweep, 63)
    # Closed-safe interval intersections provide an additional consistency check.
    intersected = []
    for a, b in fixed:
        for row in rows:
            c, d = row['window']
            left, right = max(a, c), min(b, d)
            if left <= right:
                intersected.append((left, right))
    assert sorted(intersected) == full
    assert [piece for row in rows for piece in row['allowed']] == full
    stream = sha256()
    for record in encoded:
        stream.update((canonical(record)+'\n').encode())
    expected = dict(id=case['id'], velocities=velocities, V=velocities[7],
                    laps=encoded, lap_records_sha256=stream.hexdigest(),
                    full_allowed_components=intervals(full, sweep['scale']),
                    full_allowed_duration=fraction(sum(b-a for a, b in full), sweep['scale']),
                    full_isolated_points=[fraction(a, sweep['scale']) for a, b in full if a == b],
                    global_witness=witness(sweep, full), summary=summarize_laps(encoded))
    return expected, intervals(fixed, sweep['scale']), fraction(sum(b-a for a, b in fixed), sweep['scale'])


def qualitative_groups(cases):
    groups = {}
    for case in cases:
        for row in case['laps']:
            signature = row['qualitative_signature']
            key = canonical(signature)
            group = groups.setdefault(key, dict(signature=signature, members=[], statuses=set()))
            group['members'].append([case['id'], row['m']])
            group['statuses'].add(row['status'])
    return [dict(signature=group['signature'], members=group['members'],
                 statuses=sorted(group['statuses']), status_collision=len(group['statuses']) > 1)
            for _, group in sorted(groups.items())]


def normalized_patterns(sweep, row, offset=None, shift_all=False):
    fastest, lap = sweep['velocities'][7], row['lap']
    result = []
    for i, speed in enumerate(SPEEDS, 1):
        pattern = dict(speed=speed,
                       blockers=[encode_strict(piece, sweep['scale'], fastest, lap)
                                 for piece in row['blocks'][i]])
        if offset is not None:
            pattern['source_lap'] = (lap+offset) % fastest if shift_all or speed == 11 else lap
        result.append(pattern)
    return result


def normalized_signature(sweep, row):
    fastest, lap, scale = sweep['velocities'][7], row['lap'], sweep['scale']
    allowed = [[str(Q(a*fastest, scale)-lap), str(Q(b*fastest, scale)-lap)]
               for a, b in row['allowed']]
    return dict(allowed_u=allowed, duration_u=fraction(row['actual']*fastest, scale),
                isolated_u=[a for a, b in allowed if a == b],
                status='positive_duration' if row['actual'] else ('contacts_only' if allowed else 'empty'))


def pattern_inventory(patterns):
    return [[speed, digest(sorted([lap[i]['blockers'] for lap in patterns], key=canonical))]
            for i, speed in enumerate(SPEEDS)]


def verify_phases(case, archive):
    velocities, fastest = case['velocities'], case['velocities'][7]
    original = threshold_sweep(velocities)
    original_rows = [inspect_lap(original, m) for m in range(fastest)]
    originals = [normalized_patterns(original, row) for row in original_rows]
    original_inventory = pattern_inventory(originals)
    assert_fields(dict(id=case['id'], V=fastest, velocities=velocities, residual_speeds=list(SPEEDS),
                       original_patterns=[dict(m=m, patterns=patterns) for m, patterns in enumerate(originals)],
                       runner_pattern_inventory_sha256=original_inventory), archive, ('phase', case['id']))
    assert len(archive['offsets']) == len(archive['all_shift_control']) == fastest
    expected_offsets, expected_controls = [], []
    for offset in range(fastest):
        phases = [Q(0)]*7
        phases[5] = Q(11*offset, fastest) % 1
        sweep = threshold_sweep(velocities, phases)
        rows = [inspect_lap(sweep, m) for m in range(fastest)]
        laps, patterns_for_inventory = [], []
        for row in rows:
            lap = row['lap']
            patterns = normalized_patterns(sweep, row, offset)
            # Check the pattern-shift interpretation against independent direct phase equations.
            for index, pattern in enumerate(patterns):
                assert pattern['blockers'] == originals[pattern['source_lap']][index]['blockers']
            patterns_for_inventory.append(patterns)
            signature = normalized_signature(sweep, row)
            selected_witness = witness(sweep, row['allowed'], widest=False)
            witness_u = (str(Q(selected_witness['time'])*fastest-lap)
                         if selected_witness is not None else None)
            laps.append(dict(m=lap, source_lap11=(lap+offset) % fastest, patterns=patterns,
                             **signature, duration_t=fraction(row['actual'], sweep['scale']),
                             witness_u=witness_u, witness_t=selected_witness,
                             isolated_t_witnesses=[witness(sweep, [(a, b)])
                                                   for a, b in row['allowed'] if a == b]))
        full = closed_allowed(sweep, 127)
        actual = sum(b-a for a, b in full)
        isolated = [fraction(a, sweep['scale']) for a, b in full if a == b]
        inventory = pattern_inventory(patterns_for_inventory)
        assert inventory == original_inventory
        expected = dict(s=offset, phase11=str(phases[5]), total_u_duration=fraction(actual*fastest, sweep['scale']),
                        total_t_duration=fraction(actual, sweep['scale']),
                        global_status='positive_duration' if actual else ('contacts_only' if full else 'empty'),
                        isolated_contact_count=len(isolated), normalized_contact_count=sum(len(lap['isolated_u']) for lap in laps),
                        contacts_t=isolated, full_allowed_t=intervals(full, sweep['scale']),
                        local_statuses=[lap['status'] for lap in laps],
                        runner_pattern_inventory_sha256=inventory,
                        per_runner_pattern_multisets_preserved=True, laps=laps)
        assert_fields(expected, archive['offsets'][offset], ('phase', case['id'], offset))
        expected_offsets.append(expected)
        # A separate direct physical arrangement shifts all six initial phases.
        all_phases = [Q(speed*offset, fastest) % 1 for speed in SPEEDS]+[Q(0)]
        control_sweep = threshold_sweep(velocities, all_phases)
        control_rows = [inspect_lap(control_sweep, m) for m in range(fastest)]
        signatures = [normalized_signature(control_sweep, row) for row in control_rows]
        assert signatures == [normalized_signature(original, original_rows[(m+offset) % fastest])
                              for m in range(fastest)]
        for row in control_rows:
            shifted = normalized_patterns(control_sweep, row)
            assert shifted == originals[(row['lap']+offset) % fastest]
        control_full = closed_allowed(control_sweep, 127)
        control_duration = sum(b-a for a, b in control_full)
        control = dict(s=offset, source_laps=[(m+offset) % fastest for m in range(fastest)],
                       total_u_duration=fraction(control_duration*fastest, control_sweep['scale']),
                       total_t_duration=fraction(control_duration, control_sweep['scale']),
                       isolated_contact_count=sum(a == b for a, b in control_full),
                       lap_permutation_verified=True, normalized_lap_signatures_sha256=digest(signatures))
        assert control['total_t_duration'] == expected_offsets[0]['total_t_duration']
        assert control['isolated_contact_count'] == expected_offsets[0]['isolated_contact_count']
        assert_fields(control, archive['all_shift_control'][offset], ('all_shift_control', case['id'], offset))
        expected_controls.append(control)
    baseline = expected_offsets[0]
    comparisons = dict(total_duration=lambda r: r['total_t_duration'] != baseline['total_t_duration'],
                       local_existence=lambda r: [x != 'empty' for x in r['local_statuses']] != [x != 'empty' for x in baseline['local_statuses']],
                       local_three_way_status=lambda r: r['local_statuses'] != baseline['local_statuses'],
                       global_existence=lambda r: bool(r['full_allowed_t']) != bool(baseline['full_allowed_t']),
                       global_three_way_status=lambda r: r['global_status'] != baseline['global_status'],
                       isolated_contact_count=lambda r: r['isolated_contact_count'] != baseline['isolated_contact_count'])
    earliest = {key: next((record['s'] for record in expected_offsets[1:] if predicate(record)), None)
                for key, predicate in comparisons.items()}
    assert_fields(earliest, archive['earliest_nonzero_changes'], ('earliest', case['id']))
    return dict(id=case['id'], arrangements=fastest, shifted_laps=fastest*fastest,
                direct_all_residual_shift_controls=fastest,
                offset_records_sha256=digest(expected_offsets),
                all_shift_control_records_sha256=digest(expected_controls),
                earliest_nonzero_changes=earliest,
                outcomes=[[row['s'], row['total_t_duration'], row['isolated_contact_count'], row['global_status']]
                          for row in expected_offsets])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(raw)
    assert len(protocol['cases']) == 2 and protocol['reference_index'] == 0
    assert protocol['threshold'] == '1/8' and protocol['residual_speeds'] == list(SPEEDS)
    primary_bytes = (HERE/'results.json').read_bytes()
    primary = json.loads(primary_bytes)
    phase_bytes = (HERE/'phase_results.json').read_bytes()
    phase_archive = json.loads(phase_bytes)
    assert primary['schema_version'] == phase_archive['schema_version'] == 1
    assert primary['protocol_sha256'] == phase_archive['protocol_sha256'] == PROTOCOL_SHA256
    assert phase_archive['normalized_window'] == ['1/8', '7/8']
    assert len(primary['cases']) == len(phase_archive['cases']) == 2
    expected_cases, phase_records, common_records = [], [], []
    expected_fixed, expected_fixed_duration = None, None
    for index, case in enumerate(protocol['cases']):
        expected, fixed, fixed_duration = common_start_case(case)
        assert_fields(expected, primary['cases'][index], case['id'])
        denominator = primary['cases'][index]['integer_denominator']
        assert isinstance(denominator, int) and all(denominator % (8*v) == 0 for v in case['velocities'][1:])
        if expected_fixed is not None:
            assert fixed == expected_fixed and fixed_duration == expected_fixed_duration
        expected_fixed, expected_fixed_duration = fixed, fixed_duration
        expected_cases.append(expected)
        common_records.append({key: expected[key] for key in ('id', 'V', 'lap_records_sha256',
                               'full_allowed_components', 'full_allowed_duration', 'full_isolated_points', 'summary')})
        print('PASS:', case['id'], expected['V'], 'common-start laps, all fields and digest', flush=True)
        phase_records.append(verify_phases(case, phase_archive['cases'][index]))
        print('PASS:', case['id'], expected['V'], 'speed11 phase offsets and all-residual-shift controls', flush=True)
    groups = qualitative_groups(expected_cases)
    summary = {key: sum(case['summary'][key] for case in expected_cases)
               for key in expected_cases[0]['summary'] if key != 'maximum_tree_slack'}
    summary.update(maximum_tree_slack=str(max(Q(case['summary']['maximum_tree_slack']) for case in expected_cases)),
                   qualitative_groups=len(groups),
                   qualitative_status_collision_groups=sum(group['status_collision'] for group in groups))
    assert_fields(dict(fixed_residual_speeds=list(SPEEDS), fixed_safe_components=expected_fixed,
                       fixed_safe_duration=expected_fixed_duration, qualitative_groups=groups, summary=summary),
                  primary, 'top-level')
    out = dict(status='REPRODUCED exact bounded common-start calculations and separately labelled shifted-start comparisons',
               protocol_sha256=PROTOCOL_SHA256,
               source_results_sha256=sha256(primary_bytes).hexdigest(),
               source_phase_results_sha256=sha256(phase_bytes).hexdigest(),
               primary_script_sha256=primary['script_sha256'],
               phase_script_sha256=phase_archive['script_sha256'],
               verifier_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
               methods=['direct phase threshold equations and integer product-denominator event-state sweep',
                        'strict point and open-cell membership, with all event points directly checked',
                        '64 residual-state duration masses; six singles and fifteen pairs',
                        'Kruskal maximum spanning trees and active-subgraph slack identity',
                        'direct witnesses and endpoint controllers; deterministic cover scans',
                        'fixed-six closed-safe intersections and complete common-start lap record digests',
                        'direct physical phase arrangements for all29 speed11 offsets and all29 all-residual controls'],
               common_start_configurations=2, common_start_laps=29,
               shifted_start_offset_arrangements=29, shifted_start_lap_records=425,
               all_residual_shift_controls=29, common_start_cases=common_records,
               fixed_safe_components=expected_fixed, fixed_safe_duration=expected_fixed_duration,
               summary=summary, phase_cases=phase_records)
    destination = HERE/'verification.json'
    if args.write:
        destination.write_text(json.dumps(out, indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == out
    print('PASS: independent complete comparison;', 'saved' if args.write else 'read-only replay')


if __name__ == '__main__':
    main()
