"""Independent time-domain check of the frozen phase-projection experiment.

The primary calculator is neither read nor imported. A is rebuilt from exact
threshold states. Projection multiplicity uses explicit time preimages.
For every algebraic phase cell, shifted speed11 SAFE time bands intersect A
directly; no phase-density integral is used to compute the true duration.
All possible min/max branch changes are certified to be included in the
partition before point and midpoint checks are used to certify its continuum.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = '8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17'
PRIOR_SHA256 = '612cd4320fc3083476b352f8ce058e345cf2f88a418a36e87228cdbad29c8692'
DELTA = Q(1, 8)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def distance(speed, time, phase=Q(0)):
    z = (speed*time+phase) % 1
    return min(z, 1-z)


def encode_closed(pieces):
    return [[str(a), str(b)] for a, b in pieces]


def merged_closed(pieces):
    answer = []
    for a, b in sorted(pieces):
        if answer and a <= answer[-1][1]:
            answer[-1] = (answer[-1][0], max(answer[-1][1], b))
        else:
            answer.append((a, b))
    return answer


def reconstruct_safe(speeds):
    """Threshold-event state sweep, retaining equality points separately."""
    scale = 8*prod(speeds)
    events = {0: [0, 0], scale: [0, 0]}
    for i, speed in enumerate(speeds):
        unit = scale//(8*speed)
        for k in range(speed):
            events.setdefault((8*k+1)*unit, [0, 0])[0] |= 1 << i
            events.setdefault((8*k+7)*unit, [0, 0])[1] |= 1 << i
    times = sorted(events)
    before = (1 << len(speeds))-1
    start, pieces = None, []
    for time in times:
        exits, enters = events[time]
        point = before & ~(exits | enters)
        after = (before & ~exits) | enters
        assert point == sum((distance(speed, Q(time, scale)) < DELTA) << i
                            for i, speed in enumerate(speeds))
        if not point:
            if start is None:
                start = time
            if after:
                pieces.append((Q(start, scale), Q(time, scale)))
                start = None
        else:
            assert start is None
        before = after
    assert start is None
    return pieces


def time_preimages(A, x):
    assert 0 <= x < 1
    times = {(Q(k)+x)/11 for k in range(12) if 0 <= (Q(k)+x)/11 <= 1
             and any(a <= (Q(k)+x)/11 <= b for a, b in A)}
    return sorted(times)


def phase_projection(A):
    points = sorted({Q(0)} | {(11*t) % 1 for piece in A for t in piece})
    cells = [(a, b, time_preimages(A, (a+b)/2)) for a, b in zip(points, points[1:]+[Q(1)])]
    atoms = [(x, time_preimages(A, x)) for x in points]
    # Circular projection is encoded on [0,1): right endpoint1 is excluded.
    pieces = []
    for x, times in atoms:
        if times:
            pieces.append((x, x, True, True))
    for a, b, times in cells:
        if times:
            pieces.append((a, b, False, False))
    P = merge_flagged(pieces)
    bulk = []
    for a, b, times in cells:
        if times:
            bulk.append((a, b, True, b < 1))
            if b == 1:
                bulk.append((Q(0), Q(0), True, True))
    B = merge_flagged(bulk)
    integral = sum((b-a)*len(times) for a, b, times in cells)
    assert integral == 11*sum(b-a for a, b in A)
    return dict(points=points, cells=cells, atoms=atoms, P=P, B=B,
                mass=integral, support_measure=sum(b-a for a, b, times in cells if times))


def merge_flagged(pieces):
    result = []
    for a, b, ac, bc in sorted(pieces, key=lambda p: (p[0], not p[2], p[1], not p[3])):
        if result and (a < result[-1][1] or (a == result[-1][1] and (ac or result[-1][3]))):
            x, y, xc, yc = result[-1]
            result[-1] = (x, max(y, b), xc, bc if b > y else yc or (bc and b == y))
        else:
            result.append((a, b, ac, bc))
    return result


def encode_flagged(pieces):
    return [[str(a), str(b), ac, bc] for a, b, ac, bc in pieces]


def direct_shifted_times(A, theta):
    """Direct intersections with shifted SAFE time bands, not phase integrals."""
    assert 0 <= theta <= 1
    result = []
    for a, b in A:
        for integer in range(12):
            left = (integer+DELTA-theta)/11
            right = (integer+1-DELTA-theta)/11
            low, high = max(a, left), min(b, right)
            if low <= high:
                result.append((low, high))
    return merged_closed(result)


def direct_slope(A, theta):
    """Slope from active time-domain min/max branches inside an open cell."""
    slope = Q(0)
    for a, b in A:
        for integer in range(12):
            left = (integer+DELTA-theta)/11
            right = (integer+1-DELTA-theta)/11
            if max(a, left) < min(b, right):
                assert a != left and b != right
                slope += (-Q(1, 11) if right < b else 0)-(-Q(1, 11) if left > a else 0)
    return slope


def profile(A):
    """Enumerate every possible endpoint-order/slope switch algebraically."""
    switches = {Q(0), Q(1)}
    for endpoint in {t for piece in A for t in piece}:
        for level in (DELTA, 1-DELTA):
            for integer in range(12):
                theta = integer+level-11*endpoint
                if 0 <= theta <= 1:
                    switches.add(theta)
    circular = {Q(0), Q(1)} | {(level-11*t) % 1 for piece in A for t in piece
                              for level in (DELTA, 1-DELTA)}
    assert switches == circular
    # Match the declared primary partition: the cut point x=0 contributes
    # two harmless candidate boundaries even when it is not an A endpoint.
    switches.update((DELTA, 1-DELTA))
    points = sorted(switches)
    values, allowed = {}, {}
    for theta in points:
        allowed[theta] = direct_shifted_times(A, theta)
        values[theta] = sum(b-a for a, b in allowed[theta])
    cells = []
    for left, right in zip(points, points[1:]):
        mid = (left+right)/2
        pieces = direct_shifted_times(A, mid)
        duration = sum(b-a for a, b in pieces)
        slope = direct_slope(A, mid)
        intercept = duration-slope*mid
        assert values[left] == slope*left+intercept
        assert values[right] == slope*right+intercept
        assert duration == (values[left]+values[right])/2
        cells.append(dict(left=left, right=right, mid=mid, duration=duration,
                          slope=slope, intercept=intercept, allowed=pieces))
    assert values[Q(0)] == values[Q(1)]
    assert allowed[Q(0)] == allowed[Q(1)]
    return dict(points=points, values=values, allowed=allowed, cells=cells)


def support_value(B, theta):
    total = Q(0)
    for a, b, _, _ in B:
        for integer in range(2):
            left, right = integer+DELTA-theta, integer+1-DELTA-theta
            total += max(Q(0), min(b, right)-max(a, left))
    return total/11


def support_slope(B, theta):
    total = Q(0)
    for a, b, _, _ in B:
        for integer in range(2):
            left, right = integer+DELTA-theta, integer+1-DELTA-theta
            if max(a, left) < min(b, right):
                assert a != left and b != right
                total += (-1 if right < b else 0)-(-1 if left > a else 0)
    return total/11


def contains_flagged(pieces, point):
    return any((a < point or (a == point and ac)) and (point < b or (point == b and bc))
               for a, b, ac, bc in pieces)


def phase_metrics(pieces):
    assert pieces
    gaps = []
    for i, piece in enumerate(pieces):
        start = piece[1]
        end = pieces[(i+1) % len(pieces)][0]+(1 if i == len(pieces)-1 else 0)
        if start < end:
            gaps.append((start % 1, end % 1, end-start))
    maximum_gap = max((gap[2] for gap in gaps), default=Q(0))
    return dict(measure=str(sum(b-a for a, b, _, _ in pieces)),
                maximum_circular_gap=str(maximum_gap), minimum_covering_arc_length=str(1-maximum_gap),
                maximal_gap_arcs=[[str(a), str(b), str(length)]
                                  for a, b, length in sorted(gaps) if length == maximum_gap])


def status_of(pieces):
    if any(a < b for a, b in pieces):
        return 'strict', None
    return ('contacts' if pieces else 'empty'), [str(a) for a, b in pieces]


def extrema(profile, values):
    low, high = min(values.values()), max(values.values())
    def level_set(value):
        pieces = [(point, point, True, True) for point in profile['points'][:-1]
                  if values[point] == value]
        for left, right in zip(profile['points'], profile['points'][1:]):
            if values[left] == values[right] == value:
                pieces.append((left, right, True, right < 1))
        return encode_flagged(merge_flagged(pieces))
    return dict(minimum=str(low), maximum=str(high), minimizer_set=level_set(low), maximizer_set=level_set(high))


def calculate_case(case, prior):
    fastest = case['velocities'][7]
    speeds = [1, 4, 5, 6, 7, fastest]
    A = reconstruct_safe(speeds)
    projection = phase_projection(A)
    time_profile = profile(A)
    support_values = {theta: support_value(projection['B'], theta) for theta in time_profile['points']}
    underestimate = {theta: time_profile['values'][theta]-support_values[theta]
                     for theta in time_profile['points']}
    assert min(underestimate.values()) >= 0
    points, cells = [], []
    status_sets = {status: [] for status in ('strict', 'contacts', 'empty')}
    plateau_pieces = {}
    for theta in time_profile['points'][:-1]:
        status, contacts = status_of(time_profile['allowed'][theta])
        points.append(dict(theta=str(theta), duration=str(time_profile['values'][theta]),
                           support_estimate=str(support_values[theta]), status=status, contact_times=contacts))
        status_sets[status].append((theta, theta, True, True))
    for cell in time_profile['cells']:
        left, right, mid = cell['left'], cell['right'], cell['mid']
        status, contacts = status_of(cell['allowed'])
        support = support_value(projection['B'], mid)
        slope = support_slope(projection['B'], mid)
        intercept = support-slope*mid
        assert support_values[left] == slope*left+intercept
        assert support_values[right] == slope*right+intercept
        assert cell['duration']-support >= 0
        cells.append(dict(left=str(left), right=str(right), slope=str(cell['slope']),
                          intercept=str(cell['intercept']), support_slope=str(slope),
                          support_intercept=str(intercept), status=status, contact_times=contacts))
        status_sets[status].append((left, right, False, False))
        if cell['slope'] == 0:
            plateau_pieces.setdefault(cell['duration'], []).append((left, right, True, right < 1))
        if contacts:
            # A zero-duration open theta cell can retain only fixed isolated
            # times of A, so its contact list is constant on that whole cell.
            assert all((Q(time), Q(time)) in A for time in contacts)
    phase_cells = []
    for left, right, times in projection['cells']:
        mid = (left+right)/2
        branches = []
        for time in times:
            branch = 11*time-mid
            assert branch.denominator == 1 and 0 <= branch < 11
            branches.append(int(branch))
        phase_cells.append(dict(left=str(left), right=str(right), count=len(times), preimage_branches=branches))
    prior_rows = []
    assert prior['id'] == case['id'] and prior['velocities'] == case['velocities'] and prior['V'] == fastest
    assert len(prior['offsets']) == fastest
    for offset in range(fastest):
        theta = Q(11*offset, fastest) % 1
        allowed = direct_shifted_times(A, theta)
        duration = sum(b-a for a, b in allowed)
        isolated = [str(a) for a, b in allowed if a == b]
        status, _ = status_of(allowed)
        previous = prior['offsets'][offset]
        assert previous['s'] == offset and previous['phase11'] == str(theta)
        assert previous['full_allowed_t'] == encode_closed(allowed)
        assert previous['total_t_duration'] == str(duration) and previous['contacts_t'] == isolated
        assert previous['global_status'] == {'strict': 'positive_duration', 'contacts': 'contacts_only', 'empty': 'empty'}[status]
        # Direct time value agrees with the affine continuum record, including
        # endpoints and phases not themselves candidate events.
        if theta in time_profile['values']:
            assert duration == time_profile['values'][theta]
        else:
            cell = next(c for c in time_profile['cells'] if c['left'] < theta < c['right'])
            assert duration == cell['slope']*theta+cell['intercept']
        prior_rows.append(dict(s=offset, theta=str(theta), duration=str(duration), status=status,
                               isolated_times=isolated, full_allowed_components=encode_closed(allowed)))
    result = dict(id=case['id'], velocities=case['velocities'], V=fastest, unchanged_speeds=speeds,
                  A_components=encode_closed(A), A_duration=str(sum(b-a for a, b in A)),
                  A_isolated_times=[str(a) for a, b in A if a == b],
                  phase_events=list(map(str, projection['points'])),
                  phase_points=[dict(x=str(x), count=len(times), preimages=list(map(str, times)))
                                for x, times in projection['atoms']], phase_cells=phase_cells,
                  P_components=encode_flagged(projection['P']), B_components=encode_flagged(projection['B']),
                  extra_isolated_projection_points=[str(x) for x, times in projection['atoms']
                                                     if times and not contains_flagged(projection['B'], x)],
                  P_metrics=phase_metrics(projection['P']), B_metrics=phase_metrics(projection['B']),
                  multiplicity_integral=str(projection['mass']),
                  maximum_point_multiplicity=max(len(times) for _, times in projection['atoms']),
                  maximum_bulk_multiplicity=max(len(times) for _, _, times in projection['cells']),
                  critical_phases=list(map(str, time_profile['points'][:-1])),
                  theta_points=points, theta_cells=cells,
                  duration_extrema=extrema(time_profile, time_profile['values']),
                  support_estimate_extrema=extrema(time_profile, support_values),
                  underestimate_extrema=extrema(time_profile, underestimate),
                  duration_plateaus=[dict(value=str(value), phase_components=encode_flagged(merge_flagged(pieces)))
                                     for value, pieces in sorted(plateau_pieces.items())],
                  phase_status_sets={status: encode_flagged(merge_flagged(pieces)) for status, pieces in status_sets.items()},
                  prior_phase_checks=prior_rows)
    result['case_sha256'] = sha256((canonical(result)+'\n').encode()).hexdigest()
    return result, time_profile


def assert_fields(expected, actual, label):
    for field, value in expected.items():
        assert field in actual, (label, 'missing', field)
        assert actual[field] == value, (label, field, 'computed', value, 'archived', actual[field])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(raw)
    assert protocol['reference_index'] == 0 and protocol['chosen_runner_speed'] == 11
    assert len(protocol['cases']) == 2 and protocol['threshold'] == '1/8'
    source_bytes = (HERE/'results.json').read_bytes()
    source = json.loads(source_bytes)
    assert source['schema_version'] == 1 and source['protocol_sha256'] == PROTOCOL_SHA256
    prior_path = HERE.parent/'2026-09-27-fastest-laps'/'phase_results.json'
    prior_bytes = prior_path.read_bytes()
    assert sha256(prior_bytes).hexdigest() == PRIOR_SHA256
    prior = json.loads(prior_bytes)
    assert source['prior_archive'] == dict(path='reviews/2026-09-27-fastest-laps/phase_results.json', sha256=PRIOR_SHA256)
    assert len(source['cases']) == len(prior['cases']) == 2
    records = []
    for index, case in enumerate(protocol['cases']):
        expected, time_profile = calculate_case(case, prior['cases'][index])
        assert_fields(expected, source['cases'][index], case['id'])
        archived = dict(source['cases'][index])
        archived_digest = archived.pop('case_sha256')
        assert sha256((canonical(archived)+'\n').encode()).hexdigest() == archived_digest
        records.append(dict(id=case['id'], case_sha256=expected['case_sha256'],
                            A_component_count=len(expected['A_components']),
                            phase_event_count=len(expected['phase_events']),
                            phase_cell_count=len(expected['phase_cells']),
                            candidate_theta_event_count=len(expected['critical_phases']),
                            direct_theta_point_checks=len(time_profile['points']),
                            direct_theta_cell_midpoint_checks=len(time_profile['cells']),
                            endpoint_affine_identity_checks=2*len(time_profile['cells']),
                            breakpoint_completeness_verified=True,
                            full_case_field_comparison=True,
                            prior_offsets_checked=len(expected['prior_phase_checks']),
                            A_duration=expected['A_duration'], P_metrics=expected['P_metrics'],
                            B_metrics=expected['B_metrics'],
                            maximum_point_multiplicity=expected['maximum_point_multiplicity'],
                            maximum_bulk_multiplicity=expected['maximum_bulk_multiplicity'],
                            duration_extrema=expected['duration_extrema'],
                            support_estimate_extrema=expected['support_estimate_extrema'],
                            underestimate_extrema=expected['underestimate_extrema'],
                            phase_status_sets=expected['phase_status_sets']))
        print('PASS:', case['id'], 'all case fields/digest,', len(time_profile['cells']),
              'algebraic theta cells,', len(expected['prior_phase_checks']), 'prior offsets', flush=True)
    out = dict(status='REPRODUCED exact two-case phase profiles; shifted starts explicitly separated from common-start theta0',
               protocol_sha256=PROTOCOL_SHA256, source_results_sha256=sha256(source_bytes).hexdigest(),
               primary_script_sha256=source['script_sha256'], prior_archive_sha256=PRIOR_SHA256,
               verifier_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
               methods=['threshold-event states and direct event-point distances for A',
                        'explicit safe-time preimage lists and branches for P, N, and B',
                        'direct shifted speed11 SAFE time-band intersections with A',
                        'all algebraic critical theta points plus one exact midpoint per open cell',
                        'time-domain active min/max branches give slopes independently of phase integrals',
                        'exact interval flags for extrema, plateaus, status sets and circular gaps',
                        'all29 prior phases and their entire allowed time sets against pinned archive'],
               continuum_justification=[
                   'For theta in [0,1] and t in A subset (0,1), only safe bands with lap integer0..11 can meet A.',
                   'Each A component [a,b] meets a shifted safe band [L(theta),R(theta)] in a length max(0,min(b,R)-max(a,L)); L and R have slope -1/11.',
                   'A min/max branch or nonempty-intersection change requires L or R to equal a or b. The script enumerates every such equation in [0,1] and checks equality with the endpoint-phase candidate set; translated circle-cut0 adds only redundant boundaries.',
                   'All comparisons therefore have fixed signs inside each generated open cell. Summing the selected affine time-domain branches gives D exactly throughout the cell. Direct endpoint and midpoint values verify the coefficients and continuity.',
                   'At zero duration, contact-only membership may change only when a moving safe boundary crosses an A endpoint or isolated time; these are the same candidates. Every zero-duration open-cell contact is checked to be an isolated fixed time of A.',
                   'The unweighted support estimate has the same min/max argument on B. Its breakpoints are contained in the generated partition, so differences, extrema and merged plateau sets are certified over the entire phase circle.'],
               cases=records, total_prior_offsets_checked=sum(r['prior_offsets_checked'] for r in records),
               total_algebraic_theta_cells=sum(r['direct_theta_cell_midpoint_checks'] for r in records),
               total_direct_theta_points=sum(r['direct_theta_point_checks'] for r in records))
    destination = HERE/'verification.json'
    if args.write:
        destination.write_text(json.dumps(out, indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == out
    print('PASS: full independent continuum-profile comparison;', 'saved' if args.write else 'read-only replay')


if __name__ == '__main__':
    main()
