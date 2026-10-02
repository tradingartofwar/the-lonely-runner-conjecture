#!/usr/bin/env python3
"""Independent threshold-event verification of shared pair containment.

Standard library only.  This file does not import primary.py or any helper
from the primary implementation.  Geometry is reconstructed from exact
threshold events and checked on every open cell and every event point.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
THRESHOLD = Q(1, 8)


def floor_q(x):
    return x.numerator // x.denominator


def frac(x):
    return x - floor_q(x)


def distance(speed, time):
    phase = frac(Q(speed) * time)
    return min(phase, 1 - phase)


def blocking(speed, time):
    return distance(speed, time) < THRESHOLD


def state(speeds, time):
    return sum((1 << i) for i, speed in enumerate(speeds)
               if blocking(speed, time))


def threshold_times(speed, left, right):
    """All strict-interior times with phase 1/8 or 7/8."""
    answer = set()
    first = floor_q(Q(speed) * left) - 2
    last = floor_q(Q(speed) * right) + 2
    for lap in range(first, last + 1):
        for boundary in (THRESHOLD, 1 - THRESHOLD):
            time = (Q(lap) + boundary) / speed
            if left < time < right:
                answer.add(time)
    return answer


def intervals_from_cells(cells, points, predicate):
    """Connected positive-length runs, retaining event-point connectivity."""
    runs = []
    start = None
    stop = None
    indices = []
    for i, cell in enumerate(cells):
        keep = predicate(cell['state'])
        if keep:
            if start is None:
                start = cell['left']
                indices = [i]
            elif stop != cell['left'] or not predicate(points[cell['left']]['state']):
                runs.append((start, stop, indices))
                start = cell['left']
                indices = [i]
            else:
                indices.append(i)
            stop = cell['right']
        elif start is not None:
            runs.append((start, stop, indices))
            start = stop = None
            indices = []
    if start is not None:
        runs.append((start, stop, indices))
    return runs


def stringify_intervals(runs):
    return [[str(left), str(right)] for left, right, _ in runs]


def reconstruct(case):
    speeds = case['residual_speeds']
    left, right = map(Q, case['window'])
    cuts = {left, right}
    events_by_speed = {}
    for speed in speeds:
        events = threshold_times(speed, left, right)
        events_by_speed[speed] = events
        cuts.update(events)
    cuts = sorted(cuts)

    point_records = {}
    for time in cuts:
        point_records[time] = {
            'state': state(speeds, time),
            'distances': [distance(speed, time) for speed in speeds],
            'event_speeds': [speed for speed in speeds
                             if distance(speed, time) == THRESHOLD],
        }
    cells = []
    masses = [Q(0)] * 16
    for left_cut, right_cut in zip(cuts, cuts[1:]):
        midpoint = (left_cut + right_cut) / 2
        mask = state(speeds, midpoint)
        # Two additional exact probes guard against a missed state change.
        assert state(speeds, (3 * left_cut + right_cut) / 4) == mask
        assert state(speeds, (left_cut + 3 * right_cut) / 4) == mask
        cells.append({'left': left_cut, 'right': right_cut,
                      'midpoint': midpoint, 'state': mask})
        masses[mask] += right_cut - left_cut

    moments = []
    for mask in range(16):
        moments.append(sum(masses[s] for s in range(16)
                           if s & mask == mask))

    blocker_runs = {}
    blocker_records = {}
    for i, speed in enumerate(speeds):
        runs = intervals_from_cells(
            cells, point_records, lambda mask, bit=1 << i: bool(mask & bit))
        blocker_runs[speed] = runs
        records = []
        for lo, hi, cell_indices in runs:
            midpoint = (lo + hi) / 2
            lap = floor_q(Q(speed) * midpoint + Q(1, 2))
            assert all(floor_q(Q(speed) * cells[j]['midpoint'] + Q(1, 2)) == lap
                       for j in cell_indices)
            records.append({
                'left': str(lo), 'right': str(hi), 'lap': lap,
                'left_included': blocking(speed, lo),
                'right_included': blocking(speed, hi),
            })
        blocker_records[str(speed)] = records

    return {
        '_cuts': cuts,
        '_points': point_records,
        '_cells': cells,
        '_blocker_runs': blocker_runs,
        'window': list(map(str, (left, right))),
        'speeds': speeds,
        'open_cells': [
            {'left': str(c['left']), 'right': str(c['right']),
             'state': c['state']}
            for c in cells
        ],
        'event_points': [
            {'time': str(time), 'state': point_records[time]['state'],
             'event_speeds': point_records[time]['event_speeds'],
             'distances': dict(zip(map(str, speeds),
                                   map(str, point_records[time]['distances'])))}
            for time in cuts
        ],
        'atoms': list(map(str, masses)),
        'moments': list(map(str, moments)),
        'blocker_components': blocker_records,
        'counts': {
            'interior_threshold_events': len(cuts) - 2,
            'open_cells': len(cells),
            'event_points': len(cuts),
            'state_distance_comparisons': 4 * (3 * len(cells) + len(cuts)),
            'blocking_pieces_all_runners': sum(len(x) for x in blocker_runs.values()),
            'blocker_endpoint_distance_checks': 2 * sum(len(x) for x in blocker_runs.values()),
        },
    }


def pair_test(reconstruction, pair, complement):
    speeds = reconstruction['speeds']
    cells = reconstruction['_cells']
    points = reconstruction['_points']
    blocker_runs = reconstruction['_blocker_runs']
    pair_indices = [speeds.index(speed) for speed in pair]
    complement_indices = [speeds.index(speed) for speed in complement]
    pair_mask = sum(1 << i for i in pair_indices)
    complement_mask = sum(1 << i for i in complement_indices)
    pair_runs = intervals_from_cells(
        cells, points, lambda mask: mask & pair_mask == pair_mask)

    # Independently count the standard monotone two-list intersection steps.
    first_runs, second_runs = (blocker_runs[speed] for speed in pair)
    first_index = second_index = 0
    intersection_steps = 0
    while first_index < len(first_runs) and second_index < len(second_runs):
        intersection_steps += 1
        first_right = first_runs[first_index][1]
        second_right = second_runs[second_index][1]
        if first_right <= second_right:
            first_index += 1
        if second_right <= first_right:
            second_index += 1

    component_records = []
    for lo, hi, cell_indices in pair_runs:
        midpoint = (lo + hi) / 2
        laps = {str(speed): floor_q(Q(speed) * midpoint + Q(1, 2))
                for speed in pair}
        interior_events = [time for time in points if lo < time < hi]
        phase_cells = []
        for j in cell_indices:
            cell = cells[j]
            phase_cells.append({
                'left': str(cell['left']), 'right': str(cell['right']),
                'state': cell['state'],
                'complement_distances_at_midpoint': {
                    str(speed): str(distance(speed, cell['midpoint']))
                    for speed in complement
                },
            })
        component_records.append({
            'left': str(lo), 'right': str(hi), 'base_laps': laps,
            'left_pair_blocks': all(blocking(speed, lo) for speed in pair),
            'right_pair_blocks': all(blocking(speed, hi) for speed in pair),
            'left_included_in_pair_blocking_set': all(blocking(speed, lo) for speed in pair),
            'right_included_in_pair_blocking_set': all(blocking(speed, hi) for speed in pair),
            'interior_event_points': list(map(str, interior_events)),
            'complement_endpoint_phases': {
                str(speed): [str(frac(Q(speed) * lo)), str(frac(Q(speed) * hi))]
                for speed in complement
            },
            'complement_endpoint_distances': {
                str(speed): [str(distance(speed, lo)), str(distance(speed, hi))]
                for speed in complement
            },
            'closure_complement_safe': all(
                distance(speed, time) >= THRESHOLD
                for speed in complement for time in (lo, hi)
            ),
            'phase_cells': phase_cells,
        })

    open_violations = []
    for cell in cells:
        if cell['state'] & pair_mask == pair_mask and cell['state'] & complement_mask:
            bad = [speeds[i] for i in complement_indices
                   if cell['state'] & (1 << i)]
            open_violations.append({
                'left': str(cell['left']), 'right': str(cell['right']),
                'witness': str(cell['midpoint']),
                'blocking_complement': bad,
                'state': cell['state'],
            })
    point_violations = []
    for time, point in points.items():
        if point['state'] & pair_mask == pair_mask and point['state'] & complement_mask:
            point_violations.append({
                'time': str(time), 'state': point['state'],
                'blocking_complement': [
                    speeds[i] for i in complement_indices
                    if point['state'] & (1 << i)
                ],
            })

    # A failed closed-safe containment must have a positive-cell witness here:
    # all blocker sets are relatively open in the supplied window.
    contains = not open_violations and not point_violations
    if not contains:
        assert open_violations

    internal_complement_events = 0
    for lo, hi, _ in pair_runs:
        internal_complement_events += sum(
            lo < time < hi and any(speed in points[time]['event_speeds']
                                   for speed in complement)
            for time in points)

    piece_counts = [len(blocker_runs[speed]) for speed in pair]
    return {
        'base_pair': pair,
        'complement': complement,
        'containment_holds': contains,
        'pair_components': component_records,
        'open_cell_violations': open_violations,
        'event_point_violations': point_violations,
        'first_positive_violation': open_violations[0] if open_violations else None,
        'implied_zero_triples': [sorted(pair + [speed]) for speed in complement]
                                if contains else [],
        'logical_certificate': {
            'preselected_shared_pair': pair,
            'selection_performed': False,
            'zero_triple_predicates': [
                {'speeds': sorted(pair + [speed]), 'upper_bound': '0'}
                for speed in complement
            ] if contains else [],
            'predicate_count': 2 if contains else 0,
            'single_information_bit': False,
        },
        'cost': {
            'base_runner_blocking_pieces': sum(piece_counts),
            'base_piece_pair_comparisons': piece_counts[0] * piece_counts[1],
            'pair_component_intersection_steps': intersection_steps,
            'positive_pair_components': len(pair_runs),
            'complement_component_checks': 2 * len(pair_runs),
            'internal_complement_threshold_partitions': internal_complement_events,
            'complement_phase_range_checks': 2 * (len(pair_runs) + internal_complement_events),
            'pair_component_endpoint_inclusion_checks': 2 * len(pair_runs),
            'pair_component_endpoint_base_distance_checks': 4 * len(pair_runs),
            'open_cell_predicate_checks': len(cells),
            'event_point_predicate_checks': len(points),
        },
    }


def public_reconstruction(record):
    return {key: value for key, value in record.items() if not key.startswith('_')}


def five_edge(case, reconstruction, test):
    moments = list(map(Q, reconstruction['moments']))
    total = moments[0]
    singles = sum(moments[1 << i] for i in range(4))
    pair_masks = [sum(1 << i for i in ij) for ij in combinations(range(4), 2)]
    all_pair_constant = total - singles + sum(moments[mask] for mask in pair_masks)
    speeds = reconstruction['speeds']
    complement_mask = sum(1 << speeds.index(speed) for speed in test['complement'])
    triple_masks = [
        sum(1 << speeds.index(speed) for speed in test['base_pair'] + [extra])
        for extra in test['complement']
    ]
    triple_bounds = [moments[mask] for mask in triple_masks]
    assert test['containment_holds']
    assert triple_bounds == [Q(0), Q(0)]
    raw = all_pair_constant - moments[complement_mask] - sum(triple_bounds)
    return {
        'all_six_pair_constant': str(all_pair_constant),
        'omitted_complement_pair': test['complement'],
        'omitted_complement_overlap': str(moments[complement_mask]),
        'triple_masks': triple_masks,
        'triple_upper_bounds': list(map(str, triple_bounds)),
        'raw_lower_bound': str(raw),
        'positive_duration_certified': raw > 0,
        'nonnegative_lower_bound': str(max(Q(0), raw)),
    }


def verify_sources(protocol):
    verified = {}
    for key in ('joint_results', 'cover_results', 'sparse_results'):
        path = ROOT / protocol['source_contract'][key]
        digest = sha256(path.read_bytes()).hexdigest()
        assert digest == protocol['source_contract'][key + '_sha256']
        verified[key] = {'path': str(path.relative_to(ROOT)), 'sha256': digest}
    return verified


def compare_archives(protocol, reconstructions, selected, arithmetic):
    joint = json.loads((ROOT / protocol['source_contract']['joint_results']).read_text())
    cover = json.loads((ROOT / protocol['source_contract']['cover_results']).read_text())
    sparse = json.loads((ROOT / protocol['source_contract']['sparse_results']).read_text())

    archive_names = {'collective_target': 'target', 'strict_16': 'strict_16',
                     'doubling_112': 'doubling_112', 'tight_13': 'tight_13'}
    comparison = {}
    for name, archive_name in archive_names.items():
        own = reconstructions[name]
        archived = joint['cases'][archive_name]['physical']
        for key in ('window', 'speeds', 'atoms', 'moments'):
            assert public_reconstruction(own)[key] == archived[key], (name, key)
        own_blocks = [
            [[piece['left'], piece['right']] for piece in own['blocker_components'][str(speed)]]
            for speed in own['speeds']
        ]
        assert own_blocks == archived['blocks'], (name, 'blocks')
        comparison[name] = {'joint_geometry_equal': True}

    cover_by_name = {case['name']: case for case in cover['cases']}
    for name in ('strict_16', 'doubling_112', 'tight_13'):
        own = reconstructions[name]
        archived = cover_by_name[name]
        for speed, archived_pieces in zip(own['speeds'], archived['blocks']):
            own_pieces = own['blocker_components'][str(speed)]
            assert [[p['left'], p['right'], [p['lap']]] for p in own_pieces] == archived_pieces
        comparison[name]['cover_blockers_and_laps_equal'] = True

    sparse_by_replacement = {r['replacement']: r for r in sparse['finite_results']}
    assert arithmetic['strict_16']['nonnegative_lower_bound'] == sparse_by_replacement[16]['clear_lower_bound']
    assert arithmetic['tight_13']['nonnegative_lower_bound'] == sparse_by_replacement[13]['clear_lower_bound']
    sparse_intervals = {
        'triple_6_11_w_possible': (Q(31, 88), Q(17, 48)),
        'triple_7_11_w_possible': (Q(9, 32), Q(25, 88)),
    }
    recomputed_sparse_tests = {}
    for replacement in (13, 16):
        recomputed_sparse_tests[str(replacement)] = {}
        for label, (left, right) in sparse_intervals.items():
            possible = floor_q(replacement * left - THRESHOLD) + 1 < replacement * right + THRESHOLD
            assert possible == sparse_by_replacement[replacement][label]
            recomputed_sparse_tests[str(replacement)][label] = possible
    comparison['sparse_arithmetic'] = {
        'strict_16_replacement': 16,
        'strict_16_clear_lower_bound': sparse_by_replacement[16]['clear_lower_bound'],
        'tight_13_replacement': 13,
        'tight_13_clear_lower_bound': sparse_by_replacement[13]['clear_lower_bound'],
        'old_two_occurrence_tests_recomputed': recomputed_sparse_tests,
        'old_test_formula': 'floor(w*a-1/8)+1 < w*b+1/8',
        'note': ('The old sparse tests use the two different fixed regions P and Q; '
                 'they are not this preselected shared-pair containment or its five-edge correction.'),
    }
    return comparison


def reflection_check(case, original):
    reflected_case = dict(case)
    left, right = map(Q, case['window'])
    reflected_case['window'] = [str(1 - right), str(1 - left)]
    reflected = reconstruct(reflected_case)
    original_public = public_reconstruction(original)
    reflected_public = public_reconstruction(reflected)
    assert reflected_public['atoms'] == original_public['atoms']
    assert reflected_public['moments'] == original_public['moments']
    expected_cells = [
        {'left': str(1 - Q(cell['right'])),
         'right': str(1 - Q(cell['left'])), 'state': cell['state']}
        for cell in reversed(original_public['open_cells'])
    ]
    assert reflected_public['open_cells'] == expected_cells
    test = pair_test(reflected, case['base_pair'], case['complement'])
    assert test['containment_holds']
    return {
        'window': reflected_case['window'],
        'open_cells_reverse_exactly': True,
        'atoms_equal': True,
        'moments_equal': True,
        'selected_containment_holds': True,
        'no_duplicate_selection': True,
        'reconstruction_counts': reflected_public['counts'],
    }


def tight_endpoint_check():
    time = Q(3, 8)
    speeds = [1, 4, 5, 6, 7, 11, 13]
    distances = {str(speed): str(distance(speed, time)) for speed in speeds}
    assert all(distance(speed, time) >= THRESHOLD for speed in speeds)
    left_blockers = [speed for speed in speeds if frac(Q(speed) * time) == THRESHOLD]
    right_blockers = [speed for speed in speeds if frac(Q(speed) * time) == 1 - THRESHOLD]
    assert left_blockers == [11]
    assert right_blockers == [5, 13]
    return {
        'time': str(time), 'distances': distances, 'valid': True,
        'left_neighborhood_blockers': left_blockers,
        'right_neighborhood_blockers': right_blockers,
        'isolated': True, 'positive_duration': False,
    }


def compare_primary(result):
    """Compare after all independent calculations; tolerate only documented keys."""
    path = HERE / 'results.json'
    assert path.exists(), 'primary results.json is required for final verification'
    primary = json.loads(path.read_text())
    assert primary['protocol_sha256'] == result['protocol_sha256']
    assert primary['source_contract'] == {
        key: value for key, value in json.loads((HERE / 'protocol.json').read_text())['source_contract'].items()
    }
    comparison = {'results_sha256': sha256(path.read_bytes()).hexdigest()}
    if (HERE / 'primary.py').exists():
        digest = sha256((HERE / 'primary.py').read_bytes()).hexdigest()
        assert primary.get('primary_sha256') == digest
        comparison['primary_sha256'] = digest

    # Compare by mathematical content, independent of presentation details.
    primary_cases = primary['cases']
    aliases = {'collective_target': ('collective_target', 'target'),
               'strict_16': ('strict_16',), 'tight_13': ('tight_13',)}
    comparable_cost_keys = [
        'base_runner_blocking_pieces', 'pair_component_intersection_steps',
        'pair_overlap_components', 'complement_phase_range_checks',
        'threshold_partitions', 'endpoint_times_checked',
    ]
    for own_name, candidates in aliases.items():
        key = next((candidate for candidate in candidates if candidate in primary_cases), None)
        assert key is not None
        other = primary_cases[key].get('analysis', primary_cases[key])
        own = result['cases'][own_name]
        assert other['containment_holds'] == own['containment']['containment_holds']
        assert other['five_edge_arithmetic']['lower_bound'] == own['five_edge']['raw_lower_bound']
        assert other['information_contract']['pair_selection'] == 'supplied and frozen before calculation'
        assert other['information_contract']['cached_base_pair_occurrence_tables'] == 1
        assert other['information_contract']['complement_safety_predicates'] == 2
        assert other['information_contract']['runtime_claim'] is False
        own_components = own['containment']['pair_components']
        assert len(other['pair_overlap_components']) == len(own_components)
        for primary_component, own_component in zip(other['pair_overlap_components'], own_components):
            assert primary_component['interval'] == [own_component['left'], own_component['right']]
            assert primary_component['laps'] == [
                own_component['base_laps'][str(speed)] for speed in own['containment']['base_pair']
            ]
            assert primary_component['left_included'] == own_component['left_included_in_pair_blocking_set']
            assert primary_component['right_included'] == own_component['right_included_in_pair_blocking_set']
            assert own_component['closure_complement_safe'] is True
        own_cost = own['containment']['cost']
        mapped_cost = {
            'base_runner_blocking_pieces': own_cost['base_runner_blocking_pieces'],
            'pair_component_intersection_steps': own_cost['pair_component_intersection_steps'],
            'pair_overlap_components': own_cost['positive_pair_components'],
            'complement_phase_range_checks': own_cost['complement_phase_range_checks'],
            'threshold_partitions': own_cost['internal_complement_threshold_partitions'],
            'endpoint_times_checked': own_cost['pair_component_endpoint_inclusion_checks'],
        }
        assert {cost_key: other['cost'][cost_key] for cost_key in comparable_cost_keys} == mapped_cost
    doubling = primary_cases['doubling_112']
    primary_tests = doubling.get(
        'attempts', doubling.get('diagnostic_pairs', doubling.get('pair_tests', doubling.get('containments'))))
    assert primary_tests is not None
    if isinstance(primary_tests, dict):
        primary_tests = list(primary_tests.values())
    assert len(primary_tests) == 6
    own_tests = result['doubling_112_diagnostics']
    for other, own in zip(primary_tests, own_tests):
        assert other['base_pair'] == own['base_pair']
        assert other['complement'] == own['complement']
        assert other['containment_holds'] == own['containment_holds'] is False
        assert other['first_positive_violation']['interval'] == [
            own['first_positive_violation']['left'], own['first_positive_violation']['right']]
        assert other['first_positive_violation']['witness'] == own['first_positive_violation']['witness']
        assert other['first_positive_violation']['tested_speed'] in own['first_positive_violation']['blocking_complement']
        assert len(other['pair_overlap_components']) == len(own['pair_components'])
        for primary_component, own_component in zip(other['pair_overlap_components'], own['pair_components']):
            assert primary_component['interval'] == [own_component['left'], own_component['right']]
            assert primary_component['laps'] == [
                own_component['base_laps'][str(speed)] for speed in own['base_pair']
            ]
            assert primary_component['left_included'] == own_component['left_included_in_pair_blocking_set']
            assert primary_component['right_included'] == own_component['right_included_in_pair_blocking_set']
        own_cost = own['cost']
        mapped_cost = {
            'base_runner_blocking_pieces': own_cost['base_runner_blocking_pieces'],
            'pair_component_intersection_steps': own_cost['pair_component_intersection_steps'],
            'pair_overlap_components': own_cost['positive_pair_components'],
            'complement_phase_range_checks': own_cost['complement_phase_range_checks'],
            'threshold_partitions': own_cost['internal_complement_threshold_partitions'],
            'endpoint_times_checked': own_cost['pair_component_endpoint_inclusion_checks'],
        }
        assert {cost_key: other['cost'][cost_key] for cost_key in comparable_cost_keys} == mapped_cost
    selected_primary = [primary_cases[name]['analysis'] for name in
                        ('collective_target', 'strict_16', 'tight_13')]
    for summary_key, records in (
            ('selected_cases_combined', selected_primary),
            ('six_doubling_diagnostics_combined', primary_tests)):
        archived_summary = primary['cost_summary'][summary_key]
        for cost_key, archived_value in archived_summary.items():
            assert sum(record['cost'][cost_key] for record in records) == archived_value
    assert primary['target_reflection']['containment_holds'] is True
    assert primary['target_reflection']['exact_reverse_of_target_components'] is True
    assert primary['target_reflection']['selection_reused'] is True
    assert primary['target_reflection']['independent_example'] is False
    contact = primary['tight_13_isolated_contact']
    own_contact = result['tight_13_endpoint']
    assert contact['time'] == own_contact['time']
    assert {speed: value['distance'] for speed, value in contact['states'].items()} == own_contact['distances']
    assert contact['blocks_immediately_left'] == own_contact['left_neighborhood_blockers']
    assert contact['blocks_immediately_right'] == own_contact['right_neighborhood_blockers']
    assert contact['valid'] == own_contact['valid'] is True
    assert contact['isolated'] == own_contact['isolated'] is True
    assert contact['positive_duration'] == own_contact['positive_duration'] is False
    comparison['mathematical_results_equal'] = True
    comparison['selected_case_containments_bounds_components_endpoints_and_costs_equal'] = 3
    comparison['selected_information_contracts_equal'] = 3
    comparison['doubling_failures_witnesses_components_endpoints_and_costs_equal'] = 6
    comparison['primary_operation_ledger_internal_sums_checked'] = {
        'selected_cases': len(selected_primary),
        'doubling_diagnostics': len(primary_tests),
        'selected_exact_rational_comparisons': primary['cost_summary']['selected_cases_combined']['exact_rational_comparisons'],
        'doubling_exact_rational_comparisons': primary['cost_summary']['six_doubling_diagnostics_combined']['exact_rational_comparisons'],
    }
    comparison['exact_rational_comparison_totals_not_equated'] = (
        'Implementation-specific totals differ because the verifier performs a full event sweep.'
    )
    return comparison


def make_markdown(result):
    cases = result['cases']
    lines = [
        '# Independent exact verification', '',
        'Status: **OBSERVED/REPRODUCED** for the frozen finite cases. This',
        'separately authored AI verification is not independent human mathematical validation.', '',
        '`verify.py` imports neither `primary.py` nor its helpers. It reconstructs exact',
        'rational threshold events, checks every open cell and every event point, and only',
        'then compares the resulting mathematical claims with the primary output.', '',
        '## Result', '',
        '| Case | Shared pair containment | Five-edge raw bound | Duration conclusion |',
        '| --- | --- | ---: | --- |',
    ]
    for name in ('collective_target', 'strict_16', 'tight_13'):
        record = cases[name]
        arith = record['five_edge']
        conclusion = ('positive duration' if arith['positive_duration_certified']
                      else 'no positive-duration certificate')
        lines.append(f"| `{name}` | {record['containment']['containment_holds']} | "
                     f"{arith['raw_lower_bound']} | {conclusion} |")
    lines += [
        '',
        'The target containment simultaneously certifies the two supplied zero triples;',
        'logically these remain **two zero-triple predicates over one preselected shared pair**.',
        'The certificate is neither a one-bit-information claim nor a pair selector. The pair',
        'is fixed by the frozen protocol before this calculation.',
        'A competent cached triple comparator can also reuse that one pair-occurrence table;',
        'the shared traversal still evaluates two complement-safety predicates. Thus the',
        'uncached two-reconstruction comparison is an implementation ledger, not an intrinsic',
        'factor-of-two information or runtime theorem.',
        'Its five-edge correction gives `49/524400`. The fixed strict-16 containment gives',
        '`1/896`. Tight-13 also has the containment, but its raw five-edge value is `-1/182`;',
        'it therefore does not convert the valid isolated point `t=3/8` into positive duration.', '',
        'All six diagnostic base pairs in doubling-112 fail. Each failure in',
        '`verification.json` retains an exact positive open interval, its midpoint witness,',
        'the violating complement runner, and the threshold-event state.', '',
        '## Exact scope and checks', '',
    ]
    summary = result['summary']
    lines += [
        f"The four original windows contain **{summary['open_cells']} open cells** and",
        f"**{summary['event_points']} cut/event points including window endpoints**. The reflected target adds",
        f"**{summary['reflection_open_cells']} open cells** and",
        f"**{summary['reflection_event_points']} cut/event points including endpoints**. Exact state reconstruction",
        'agrees with the pinned joint geometry (atoms, moments, blocker pieces), and the three',
        'controls also agree with the separately archived blocker/lap lists.', '',
        'The reflected target is the exact reversed cell sequence with identical masses and',
        'moments; it is not re-selected or counted as an independent example. At tight-13\'s',
        'endpoint, runner 11 blocks immediately to the left while runners 5 and 13 block',
        'immediately to the right.', '',
        'Source SHA-256 values are checked before use. The old sparse replacement-16 bound',
        '`1/896` and replacement-13 nonnegative bound `0` are reproduced as comparisons;',
        'the old sparse edge tests are not conflated with the present shared certificate.', '',
        '## Reproduction and limits', '',
        '```bash',
        'python -B reviews/2026-09-28-shared-pair-containment/verify.py --check',
        '```', '',
        'The check is read-only and verifies protocol/source/primary hashes, exact geometry,',
        'containments, six explicit failures, reflection, endpoint semantics, arithmetic, and',
        'the committed JSON and Markdown bytes. The result proves only these supplied finite',
        'windows and fixed pairs. It gives no general pair-selection theorem, no new speed or',
        'window coverage, and no novelty claim. Positive-duration statements remain distinct',
        'from isolated equality; archived abstract measurable covers are not runner realizations.', '',
    ]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true',
                        help='read-only replay against committed outputs')
    args = parser.parse_args()

    protocol_path = HERE / 'protocol.json'
    protocol = json.loads(protocol_path.read_text())
    assert protocol['frozen_before_calculation'] is True
    source_hashes = verify_sources(protocol)
    frozen = {case['name']: case for case in protocol['frozen_cases']}

    # Complete all independent geometry before reading primary output.
    reconstructions = {name: reconstruct(case) for name, case in frozen.items()}
    selected = {}
    arithmetic = {}
    for name in ('collective_target', 'strict_16', 'tight_13'):
        case = frozen[name]
        test = pair_test(reconstructions[name], case['base_pair'], case['complement'])
        assert test['containment_holds'], name
        selected[name] = test
        arithmetic[name] = five_edge(case, reconstructions[name], test)

    doubling = reconstructions['doubling_112']
    diagnostic = []
    speeds = frozen['doubling_112']['residual_speeds']
    for pair_tuple in combinations(speeds, 2):
        pair = list(pair_tuple)
        complement = [speed for speed in speeds if speed not in pair]
        test = pair_test(doubling, pair, complement)
        assert not test['containment_holds']
        assert test['first_positive_violation'] is not None
        diagnostic.append(test)
    assert len(diagnostic) == 6

    archive_comparison = compare_archives(
        protocol, reconstructions, selected, arithmetic)
    reflection = reflection_check(frozen['collective_target'],
                                  reconstructions['collective_target'])
    endpoint = tight_endpoint_check()

    result = {
        'method': ('separately authored exact rational threshold-event cell/state '
                   'reconstruction; every open cell and event point checked'),
        'protocol_sha256': sha256(protocol_path.read_bytes()).hexdigest(),
        'source_hashes': source_hashes,
        'cases': {},
        'doubling_112_diagnostics': diagnostic,
        'target_reflection': reflection,
        'tight_13_endpoint': endpoint,
        'archive_comparison': archive_comparison,
    }
    for name in ('collective_target', 'strict_16', 'tight_13'):
        result['cases'][name] = {
            'reconstruction': public_reconstruction(reconstructions[name]),
            'containment': selected[name],
            'five_edge': arithmetic[name],
        }
    result['cases']['doubling_112'] = {
        'reconstruction': public_reconstruction(doubling),
        'all_six_containments_fail': True,
    }
    result['summary'] = {
        'selected_containments_pass': 3,
        'doubling_containments_fail': 6,
        'open_cells': sum(r['counts']['open_cells'] for r in
                          (public_reconstruction(x) for x in reconstructions.values())),
        'event_points': sum(r['counts']['event_points'] for r in
                            (public_reconstruction(x) for x in reconstructions.values())),
        'reflection_open_cells': reflection['reconstruction_counts']['open_cells'],
        'reflection_event_points': reflection['reconstruction_counts']['event_points'],
        'target_bound': arithmetic['collective_target']['raw_lower_bound'],
        'strict_16_bound': arithmetic['strict_16']['raw_lower_bound'],
        'tight_13_raw_bound': arithmetic['tight_13']['raw_lower_bound'],
        'tight_13_isolated_equality': endpoint['isolated'],
    }
    result['primary_comparison'] = compare_primary(result)

    json_text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    markdown_text = make_markdown(result)
    json_path = HERE / 'verification.json'
    markdown_path = HERE / 'verification.md'
    if args.check:
        assert json_path.read_text() == json_text
        assert markdown_path.read_text() == markdown_text
        print('PASS:', json.dumps(result['summary'], sort_keys=True))
    else:
        json_path.write_text(json_text)
        markdown_path.write_text(markdown_text)
        print('Wrote verification outputs:', json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
