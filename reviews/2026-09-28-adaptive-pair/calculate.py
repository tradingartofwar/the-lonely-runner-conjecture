"""Adaptive reflected-pair arithmetic: three symbolic branches, eight examples.

Exact Fraction substitutions, circle triangle certificates and safe-lap endpoint
inequalities only. Work does not enumerate speeds, times, laps or phase grids.
General formulas are proof candidates; finite diagnostics do not prove infinity.
--write creates results.json; default/--check recomputes it read-only.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results.json'
PROTOCOL_HASH = '55d73b9e425f4ad8fa74441029cb88569f2091fcb3bdf3494c4cca656d92f7f7'
DELTA = F(1, 8)
FIXED = [1, 4, 5, 6, 7]
EXCLUDED = {1, 4, 5, 6, 7, 11}
BRANCHES = [
    {
        'id': 'nonmultiple8', 'condition': '8 does not divide V', 'time_formula': '1/8',
        'unchanged_phase_formulas': ['1/8', '1/2', '5/8', '3/4', '7/8', 'r/8'],
        'unchanged_distance_formulas': ['1/8', '1/2', '3/8', '1/4', '1/8', 'min(r,8-r)/8'],
        'equality_controller_rule': 'At t: 1 enters right,7 enters left; V enters right if r=1,left if r=7. Reflection reverses directions.',
        'selected_phase_at_t_formula': '3/8', 'separation_formula': '1/4',
        'half_separation_formula': '1/8', 'half_separation_slack_formula': '0',
        'envelope_minimum_formula': '1/8', 'envelope_maximum_formula': '1/8',
        'constant_in_phase': True, 'unchanged_inward_direction': 'none',
        'directed_radius_formula': None, 'directed_radius_slack_formula': None,
    },
    {
        'id': 'multiple8_not56', 'condition': '8 divides V and56 does not divide V', 'time_formula': '17/56',
        'unchanged_phase_formulas': ['17/56', '3/14', '29/56', '23/28', '1/8', 'k/7'],
        'unchanged_distance_formulas': ['17/56', '3/14', '27/56', '5/28', '1/8', 'min(k,7-k)/7'],
        'equality_controller_rule': 'At t only speed7 equals1/8 and enters right. Reflection enters left.',
        'selected_phase_at_t_formula': '19/56', 'separation_formula': '9/28',
        'half_separation_formula': '9/56', 'half_separation_slack_formula': '1/28',
        'envelope_minimum_formula': '1/8', 'envelope_maximum_formula': '1/8',
        'constant_in_phase': True, 'unchanged_inward_direction': 'right',
        'directed_radius_formula': '1/(56V)', 'directed_radius_slack_formula': '(2V-11)/(56V)',
    },
    {
        'id': 'multiple56', 'condition': '56 divides V', 'time_formula': '17/56+1/(8V)',
        'unchanged_phase_formulas': ['17/56+1/(8V)', '3/14+1/(2V)', '29/56+5/(8V)',
                                     '23/28+3/(4V)', '1/8+7/(8V)', '1/8'],
        'unchanged_distance_formulas': ['17/56+1/(8V)', '3/14+1/(2V)', '27/56-5/(8V)',
                                        '5/28-3/(4V)', '1/8+7/(8V)', '1/8'],
        'equality_controller_rule': 'At t only speedV equals1/8 and enters right. Reflection enters left.',
        'selected_phase_at_t_formula': '19/56+11/(8V)', 'separation_formula': '9/28-11/(4V)',
        'half_separation_formula': '9/56-11/(8V)', 'half_separation_slack_formula': '1/28-11/(8V)',
        'envelope_minimum_formula': '1/8', 'envelope_maximum_formula': '1/8',
        'constant_in_phase': True, 'unchanged_inward_direction': 'right',
        'directed_radius_formula': '1/(56V)', 'directed_radius_slack_formula': '(V-44)/(28V)',
    },
]


def distance(x):
    phase = x % 1
    return min(phase, 1 - phase)


def safe_lap(v, t):
    z = v * t
    lap = z.numerator // z.denominator
    phase = z - lap
    left, right = (lap + DELTA) / v, (lap + 1 - DELTA) / v
    assert left <= t <= right
    direction = 'right' if t == left else ('left' if t == right else None)
    return {'lap': lap, 'interval': [str(left), str(right)], 'phase': str(phase),
            'distance': str(distance(z)), 'left_clearance': str(t - left),
            'right_clearance': str(right - t), 'controller_direction': direction}


def branch_values(V):
    """Independent explicit branch formulas, evaluated at a frozen V only."""
    if V % 8:
        r = V % 8
        return ('nonmultiple8', F(1, 8),
                [F(1, 8), F(1, 2), F(5, 8), F(3, 4), F(7, 8), F(r, 8)],
                [F(1, 8), F(1, 2), F(3, 8), F(1, 4), F(1, 8), F(min(r, 8-r), 8)], F(1, 4))
    if V % 56:
        k = (17 * (V // 8)) % 7
        assert 1 <= k <= 6
        return ('multiple8_not56', F(17, 56),
                [F(17, 56), F(3, 14), F(29, 56), F(23, 28), F(1, 8), F(k, 7)],
                [F(17, 56), F(3, 14), F(27, 56), F(5, 28), F(1, 8), F(min(k, 7-k), 7)], F(9, 28))
    assert V >= 56
    h = F(1, 8 * V)
    return ('multiple56', F(17, 56) + h,
            [F(17, 56)+h, F(3, 14)+4*h, F(29, 56)+5*h, F(23, 28)+6*h, F(1, 8)+7*h, F(1, 8)],
            [F(17, 56)+h, F(3, 14)+4*h, F(27, 56)-5*h, F(5, 28)-6*h, F(1, 8)+7*h, F(1, 8)],
            F(9, 28)-22*h)


def calculate(V):
    assert V > 0 and V not in EXCLUDED
    branch, t, expected_phases, expected_distances, expected_separation = branch_values(V)
    times, speeds = [t, 1-t], [*FIXED, V]
    phase_vectors = [[v*s % 1 for v in speeds] for s in times]
    vectors = [[distance(v*s) for v in speeds] for s in times]
    assert phase_vectors[0] == expected_phases and vectors[0] == expected_distances
    assert vectors[0] == vectors[1] and min(vectors[0]) == DELTA
    cap = min(vectors[0])
    selected = [11*s % 1 for s in times]
    separation = distance(selected[1] - selected[0])
    assert separation == distance(22*t) == expected_separation
    half = separation / 2
    signed_arc = (selected[1]-selected[0]) % 1
    if signed_arc > F(1, 2):
        signed_arc -= 1
    equality_phase = -(selected[0] + signed_arc/2) % 1
    assert all(distance(a + equality_phase) == half for a in selected)
    minimum, maximum = min(cap, half), cap
    assert minimum == maximum == DELTA
    assert max(min(cap, distance(a + equality_phase)) for a in selected) == minimum
    assert max(min(cap, distance(a + F(1, 2)-selected[0])) for a in selected) == maximum
    laps = [{'speed': v, 'at_t': safe_lap(v, t), 'at_reflection': safe_lap(v, 1-t)} for v in speeds]
    controllers = [[v for v, d in zip(speeds, ds) if d == DELTA] for ds in vectors]
    directions = [[[r['speed'], r[key]['controller_direction']] for r in laps if r[key]['controller_direction']]
                  for key in ('at_t', 'at_reflection')]
    if branch == 'nonmultiple8':
        assert controllers[0] == [1, 7] + ([V] if V % 8 in (1, 7) else [])
        assert {direction for _, direction in directions[0]} == {'right', 'left'}
    elif branch == 'multiple8_not56':
        assert controllers == [[7], [7]] and directions == [[[7, 'right']], [[7, 'left']]]
    else:
        assert controllers == [[V], [V]] and directions == [[[V, 'right']], [[V, 'left']]]
    directed = None
    if V % 8 == 0:
        radius = F(1, 56*V)
        core_room = F(5, 16)-t
        variable_room = (1-DELTA-phase_vectors[0][-1])/V
        selected_room = (half-DELTA)/11
        room = min(core_room, variable_room, selected_room)
        assert core_room == min(F(row['at_t']['right_clearance']) for row in laps[:-1])
        assert variable_room == F(laps[-1]['at_t']['right_clearance'])
        assert 0 < radius <= room
        if branch == 'multiple56':
            assert variable_room == F(3, 4*V)
        segments = [[v, phase_vectors[0][i], phase_vectors[0][i]+v*radius] for i, v in enumerate(speeds)]
        assert all(DELTA <= a < b <= 1-DELTA for _, a, b in segments)
        # This exact endpoint condition and positive slope prove strictness on
        # every open interior point, without choosing a grid of times.
        endpoint_vectors = [[distance(v*s) for v in speeds] for s in (t+radius, 1-t-radius)]
        assert endpoint_vectors[0] == endpoint_vectors[1]
        assert all(d >= DELTA for ds in endpoint_vectors for d in ds)
        selected_lower = half - 11*radius
        selected_slack = selected_lower - DELTA
        expected_slack = F(2*V-11, 56*V) if branch == 'multiple8_not56' else F(V-44, 28*V)
        assert selected_slack == expected_slack > 0
        directed = {
            'radius': str(radius), 'core_room': str(core_room), 'variable_room': str(variable_room),
            'selected_room': str(selected_room), 'minimum_room': str(room), 'radius_within_room': radius <= room,
            'selected_distance_lower_bound_at_radius': str(selected_lower),
            'selected_slack_at_radius': str(selected_slack),
            'candidate_intervals': [[str(t), str(t+radius)], [str(1-t-radius), str(1-t)]],
            'unchanged_phase_segments': [[v, str(a), str(b)] for v, a, b in segments],
            'unchanged_endpoint_distances': [list(map(str, ds)) for ds in endpoint_vectors],
            'strict_open_interior_verified': True,
        }
    record = {
        'V': V, 'branch': branch, 'times': list(map(str, times)), 'unchanged_speeds': speeds,
        'unchanged_phase_vectors': [list(map(str, ps)) for ps in phase_vectors],
        'unchanged_distance_vectors': [list(map(str, ds)) for ds in vectors], 'unchanged_cap': str(cap),
        'equality_controllers': controllers, 'equality_controller_directions': directions,
        'selected_phase_pair': list(map(str, selected)), 'selected_phase_separation': str(separation),
        'half_separation': str(half), 'half_separation_slack': str(half-DELTA),
        'raw_pair_minimizer_theta': str(equality_phase),
        'pair_envelope_minimum': str(minimum), 'pair_envelope_maximum': str(maximum),
        'constant_in_phase': cap <= half, 'safe_laps': laps, 'directed_certificate': directed,
    }
    print('V', V, branch, 't', t, 'd', separation, 'envelope', minimum,
          'R', directed['radius'] if directed else None,
          'minimum room', directed['minimum_room'] if directed else None, flush=True)
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH, 'Frozen protocol changed'
    protocol = json.loads(raw)
    diagnostics = [calculate(V) for V in protocol['finite_diagnostics']]
    digest = sha256()
    for record in diagnostics:
        digest.update((json.dumps(record, sort_keys=True, separators=(',', ':'))+'\n').encode())
    counts = Counter(r['branch'] for r in diagnostics)
    directed = [r['directed_certificate'] for r in diagnostics if r['directed_certificate'] is not None]
    result = {
        'schema_version': 1, 'protocol_sha256': PROTOCOL_HASH,
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'status': 'OBSERVED exact eight diagnostics; symbolic general implications remain HYPOTHESIS/proof candidates; no novelty claim',
        'unchanged_speed_order': [1, 4, 5, 6, 7, 'V'], 'symbolic_branches': BRANCHES,
        'directed_selection_rule': 'For each theta choose the candidate maximizing speed11 distance, taking t on a tie; use its directed interval. Do not select by the tied full pair margin.',
        'diagnostics': diagnostics, 'diagnostics_sha256': digest.hexdigest(),
        'summary': {'diagnostic_count': len(diagnostics), 'branch_counts': {b['id']: counts[b['id']] for b in BRANCHES},
                    'all_pair_envelopes_constant_threshold': all(r['constant_in_phase'] and F(r['pair_envelope_minimum']) == DELTA for r in diagnostics),
                    'directed_certificate_count': len(directed),
                    'all_directed_checks_pass': all(r['radius_within_room'] and r['strict_open_interior_verified'] and F(r['selected_slack_at_radius']) > 0 for r in directed)},
    }
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(OUT.read_text()), 'Archive drift'
    print('PASS: eight prescribed substitutions, exact reflected-pair envelopes and directed endpoint '
          'certificates; '+('written' if args.write else 'replayed read-only'))


if __name__ == '__main__':
    main()
