"""Independent reconstruction of the frozen one-pair selector campaign.

No primary select implementation is read or imported. Core windows come
from threshold states. Singles and the one selected overlap come from
clipped strict blocking intervals. Only the prescribed right endpoint is
tested after a failed duration bound; no full seven-runner set is built.
--write records comparison; default/--check replays without writing.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = '36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e'
DELTA = Q(1, 8)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def near(speed, time):
    phase = (speed*time) % 1
    return min(phase, 1-phase)


def closed_encoding(pieces):
    return [[str(a), str(b)] for a, b in pieces]


def strict_encoding(pieces):
    return [[str(a), str(b), ac, bc] for a, b, ac, bc in pieces]


def core_safe(core):
    scale = 8*prod(core)
    events = {0: [0, 0], scale: [0, 0]}
    for i, speed in enumerate(core):
        unit = scale//(8*speed)
        for k in range(speed):
            events.setdefault((8*k+1)*unit, [0, 0])[0] |= 1 << i
            events.setdefault((8*k+7)*unit, [0, 0])[1] |= 1 << i
    times = sorted(events)
    before = 7
    pieces, start = [], None
    for time in times:
        leaves, enters = events[time]
        point = before & ~(leaves | enters)
        after = (before & ~leaves) | enters
        assert point == sum((near(v, Q(time, scale)) < DELTA) << i for i, v in enumerate(core))
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
    return pieces, len(times)


def belongs(piece, time):
    a, b, ac, bc = piece
    return (a < time or (a == time and ac)) and (time < b or (time == b and bc))


def intersect(left, right):
    pieces = []
    for p in left:
        for q in right:
            a, b = max(p[0], q[0]), min(p[1], q[1])
            ac, bc = belongs(p, a) and belongs(q, a), belongs(p, b) and belongs(q, b)
            if a < b or (a == b and ac and bc):
                pieces.append((a, b, ac, bc))
    return sorted(pieces)


def blocking(speed, window):
    left, right = window
    raw = [(Q(8*k-1, 8*speed), Q(8*k+1, 8*speed), False, False) for k in range(speed+1)]
    return intersect(raw, [(left, right, True, True)])


def duration(pieces):
    return sum((b-a for a, b, *_ in pieces), Q(0))


def right_endpoint(speeds, endpoint):
    distances = [near(speed, endpoint) for speed in speeds]
    valid = min(distances) >= DELTA
    phases = [(speed*endpoint) % 1 for speed in speeds]
    controllers = [[speed, 'right' if phase == DELTA else 'left']
                   for speed, phase in zip(speeds, phases) if phase in (DELTA, 1-DELTA)]
    laps, common = [], None
    if valid:
        for speed in speeds:
            value = speed*endpoint
            lap = value.numerator//value.denominator
            a, b = Q(8*lap+1, 8*speed), Q(8*lap+7, 8*speed)
            assert a <= endpoint <= b
            laps.append(dict(speed=speed, lap=lap, window=(a, b)))
        common = (max(row['window'][0] for row in laps), min(row['window'][1] for row in laps))
        assert common[0] <= endpoint <= common[1]
        assert (common[0] < common[1]) == (not ({direction for _, direction in controllers} == {'left', 'right'}))
    return dict(time=endpoint, distances=distances, phases=phases, valid=valid,
                controllers=controllers, safe_laps=laps, common=common)


def calculate_case(case):
    core, extras = case['core'], case['extras']
    assert len(set(core+extras)) == 7 and len(core) == 3 and len(extras) == 4
    pieces, event_count = core_safe(core)
    positive = [(a, b) for a, b in pieces if a < b]
    assert positive
    window = min(positive, key=lambda piece: (piece[0]-piece[1], piece[0]))
    width = window[1]-window[0]
    blocks = {speed: blocking(speed, window) for speed in extras}
    singles = {speed: duration(blocks[speed]) for speed in extras}
    excess = sum(singles.values())-width
    ranking = sorted(combinations(sorted(extras), 2), key=lambda pair: (-min(singles[v] for v in pair), pair))
    caps = [min(singles[v] for v in pair) for pair in ranking]
    selected, overlap, overlap_pieces = None, None, None
    if excess < 0:
        route, lower = 'singles', -excess
    elif caps[0] <= excess:
        route, lower = 'cap_rejection', -excess
    else:
        route, selected = 'one_pair', ranking[0]
        overlap_pieces = intersect(blocks[selected[0]], blocks[selected[1]])
        overlap = duration(overlap_pieces)
        lower = overlap-excess
    endpoint = None
    if lower > 0:
        outcome = 'positive_duration'
    else:
        endpoint = right_endpoint(sorted(core+extras), window[1])
        if not endpoint['valid']:
            outcome = 'uncertified'
        elif endpoint['common'][0] < endpoint['common'][1]:
            outcome = 'positive_endpoint_interval'
        else:
            outcome = 'isolated_endpoint'
    return dict(id=case['id'], core=core, extras=extras, core_components=pieces,
                core_event_count=event_count, window=window, width=width, blocks=blocks,
                singles=singles, excess=excess, ranking=ranking, caps=caps,
                route=route, selected=selected, overlap=overlap, overlap_pieces=overlap_pieces,
                lower=lower, endpoint=endpoint, outcome=outcome)


def assert_fields(expected, actual, label):
    for field, value in expected.items():
        assert field in actual, (label, 'missing', field)
        assert actual[field] == value, (label, field, 'computed', value, 'archived', actual[field])


def semantic(row):
    endpoint = row['endpoint']
    fallback = None
    if endpoint is not None:
        speeds = sorted(row['core']+row['extras'])
        fallback = dict(time=str(endpoint['time']),
                        distances=[[speed, str(value)] for speed, value in zip(speeds, endpoint['distances'])],
                        valid=endpoint['valid'],
                        failed_speeds=[speed for speed, value in zip(speeds, endpoint['distances']) if value < DELTA],
                        safe_laps=[dict(speed=lap['speed'], lap=lap['lap'], interval=closed_encoding([lap['window']])[0])
                                   for lap in endpoint['safe_laps']],
                        shared_safe_interval=closed_encoding([endpoint['common']])[0] if endpoint['common'] is not None else None,
                        shared_safe_width=str(endpoint['common'][1]-endpoint['common'][0]) if endpoint['common'] is not None else None,
                        equality_controllers=endpoint['controllers'] if endpoint['valid'] else [])
    return dict(id=row['id'], core=row['core'], extras=row['extras'],
                core_components=closed_encoding(row['core_components']),
                selected_window=closed_encoding([row['window']])[0], window_width=str(row['width']),
                single_durations=[[speed, str(row['singles'][speed])] for speed in row['extras']],
                total_single_duration=str(sum(row['singles'].values())), excess=str(row['excess']),
                pair_ranking=[dict(pair=list(pair), cap=str(cap)) for pair, cap in zip(row['ranking'], row['caps'])],
                stage={'singles': 'singles_positive', 'cap_rejection': 'cap_ceiling', 'one_pair': 'queried_pair'}[row['route']],
                selected_pair=list(row['selected']) if row['selected'] else None,
                queried_overlap=str(row['overlap']) if row['overlap'] is not None else None,
                duration_lower_bound=str(row['lower']),
                one_pair_cap_class_failure=row['excess'] >= 0 and row['caps'][0] <= row['excess'],
                selected_query_failure=row['selected'] is not None and row['lower'] <= 0,
                endpoint_fallback=fallback,
                outcome={'positive_endpoint_interval': 'endpoint_interval', 'isolated_endpoint': 'endpoint_contact'}.get(row['outcome'], row['outcome']))


def floor(value):
    return value.numerator//value.denominator


def ceil(value):
    return -floor(-value)


def C(value):
    lap = floor(value)
    phase = value-lap
    return Q(lap, 4)+min(phase, DELTA)+max(Q(0), phase-(1-DELTA))


def P(value):
    phase = value-floor(value)
    return phase*(phase-1)/2


def endpoint_kernel(a, slope, intercept, source, left, right):
    frequency = a-slope
    assert frequency > 0
    arguments = [frequency*t-intercept for t in (left, right)]
    values = list(map(P, arguments))
    W = (values[1]-values[0])/frequency
    return dict(slope=str(slope), intercept=str(intercept), source=source, frequency=str(frequency),
                primitive_arguments=list(map(str, arguments)), primitive_values=list(map(str, values)), W=str(W))


def evaluation_audit(row):
    """Formula-certificate audit; policy values remain direct interval values."""
    left, right = row['window']
    singles = []
    for speed in row['extras']:
        arguments = [speed*left, speed*right]
        values = list(map(C, arguments))
        value = (values[1]-values[0])/speed
        assert value == row['singles'][speed]
        singles.append(dict(speed=speed, arguments=list(map(str, arguments)),
                            primitive_values=list(map(str, values)), duration=str(value)))
    result = dict(single_evaluations=singles, overlap=None)
    stats = dict(candidates=0, event_candidates=0, examined_cells=0, positive_cells=0,
                 direct_strip_overlap_checks=0, single_arguments=[Q(x) for s in singles for x in s['arguments']],
                 overlap_arguments=[])
    if row['selected'] is None:
        return result, stats
    a, b = row['selected']
    h = min((1, 2), key=lambda multiplier: (abs(b-multiplier*a), multiplier))
    residual = b-h*a
    residual_range = sorted([residual*left, residual*right])
    minimum = floor(residual_range[0]-Q(h+1, 8)) if residual else 0
    maximum = ceil(residual_range[1]+Q(h+1, 8)) if residual else 0
    strips, cells = [], []
    total_area = total_correction = total_overlap = Q(0)
    for m in range(minimum, maximum+1):
        points = {left, right}
        if residual:
            for delta in (Q(h+1, 8), -Q(h+1, 8), Q(h-1, 8), -Q(h-1, 8)):
                point = (m+delta)/residual
                if left < point < right:
                    points.add(point)
        points = sorted(points)
        strip_count = 0
        stats['examined_cells'] += len(points)-1
        for u, v in zip(points, points[1:]):
            midpoint = (u+v)/2
            affine_lower, affine_upper = (m-DELTA-residual*midpoint)/h, (m+DELTA-residual*midpoint)/h
            lower_line = (Q(0), -DELTA, 'constant') if -DELTA >= affine_lower else (-Q(residual, h), (m-DELTA)/h, 'affine')
            upper_line = (Q(0), DELTA, 'constant') if DELTA <= affine_upper else (-Q(residual, h), (m+DELTA)/h, 'affine')
            lower_at_mid = lower_line[0]*midpoint+lower_line[1]
            upper_at_mid = upper_line[0]*midpoint+upper_line[1]
            if lower_at_mid >= upper_at_mid:
                continue
            lower = endpoint_kernel(a, *lower_line, u, v)
            upper = endpoint_kernel(a, *upper_line, u, v)
            area = (upper_line[0]-lower_line[0])*(v*v-u*u)/2+(upper_line[1]-lower_line[1])*(v-u)
            correction = Q(upper['W'])-Q(lower['W'])
            overlap = area+correction
            direct = duration(intersect(row['overlap_pieces'], [(u, v, True, True)]))
            assert overlap == direct >= 0, (row['id'], m, u, v, overlap, direct)
            assert Q(lower['frequency']) in (Q(a), Q(b, h)) and Q(upper['frequency']) in (Q(a), Q(b, h))
            cells.append(dict(m=m, interval=[str(u), str(v)], lower=lower, upper=upper,
                              area=str(area), endpoint_correction=str(correction), overlap=str(overlap)))
            strip_count += 1
            stats['direct_strip_overlap_checks'] += 1
            stats['overlap_arguments'].extend(Q(x) for endpoint in (lower, upper) for x in endpoint['primitive_arguments'])
            total_area += area
            total_correction += correction
            total_overlap += overlap
        strips.append(dict(m=m, breakpoints=list(map(str, points)), positive_cell_count=strip_count))
    assert total_overlap == row['overlap']
    stats.update(candidates=len(strips), event_candidates=4*len(strips) if residual else 0,
                 positive_cells=len(cells))
    result['overlap'] = dict(pair=list(row['selected']), h=h, r=residual,
                             residual_range=list(map(str, residual_range)), m_range=[minimum, maximum],
                             candidate_strips=strips, positive_cells=cells, phase_area=str(total_area),
                             endpoint_correction=str(total_correction), overlap=str(total_overlap))
    return result, stats


def operand_bits(values):
    if not values:
        return None
    return dict(maximum_numerator_bits=max(abs(value.numerator).bit_length() for value in values),
                maximum_denominator_bits=max(value.denominator.bit_length() for value in values))


def fraction_strings(value):
    if isinstance(value, str):
        try:
            return [Q(value)]
        except (ValueError, ZeroDivisionError):
            return []
    if isinstance(value, list):
        return [item for child in value for item in fraction_strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in fraction_strings(child)]
    return []


def structural_cost(row, semantics, evaluations, stats):
    queried, endpoint = row['selected'] is not None, row['endpoint'] is not None
    return dict(core_laps_by_speed=[[speed, speed] for speed in row['core']],
                core_laps_total=sum(row['core']), core_event_vertices=row['core_event_count'],
                core_components=len(row['core_components']),
                single_duration_evaluations=4, single_primitive_calls=8, pair_caps=6,
                exact_overlap_queries=int(queried), residual_strip_candidates=stats['candidates'],
                residual_event_candidates=stats['event_candidates'], residual_cells_examined=stats['examined_cells'],
                positive_strip_cells=stats['positive_cells'], overlap_W_calls=2*stats['positive_cells'],
                overlap_P_calls=4*stats['positive_cells'], endpoint_tests=int(endpoint),
                endpoint_distance_evaluations=7*int(endpoint),
                safe_lap_constructions=7 if endpoint and row['endpoint']['valid'] else 0,
                single_primitive_operand_bits=operand_bits(stats['single_arguments']),
                overlap_primitive_operand_bits=operand_bits(stats['overlap_arguments']),
                reported_fraction_bits=operand_bits(fraction_strings(semantics)+fraction_strings(evaluations)))


def primary_intersection_count_only(core):
    """Audit the advertised counter; this path never determines policy inputs."""
    current, count = [(Q(0), Q(1))], 0
    for speed in sorted(core):
        laps = [(Q(8*k+1, 8*speed), Q(8*k+7, 8*speed)) for k in range(speed)]
        left_index = right_index = 0
        output = []
        while left_index < len(current) and right_index < len(laps):
            count += 1
            left, right = current[left_index], laps[right_index]
            a, b = max(left[0], right[0]), min(left[1], right[1])
            if a <= b:
                output.append((a, b))
            if left[1] <= right[1]:
                left_index += 1
            if right[1] <= left[1]:
                right_index += 1
        current = output
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(raw)
    rows = []
    for case in protocol['ordered_cases']:
        row = calculate_case(case)
        rows.append(row)
        if row['outcome'] == 'uncertified':
            break
    source_bytes = (HERE/'results.json').read_bytes()
    source = json.loads(source_bytes)
    assert source['schema_version'] == 1 and source['protocol_sha256'] == PROTOCOL_SHA256
    assert len(source['cases']) == len(rows)
    verification_rows, semantic_rows, audited_costs = [], [], []
    for row, archive in zip(rows, source['cases']):
        semantics = semantic(row)
        assert semantics == archive['semantic'], ('semantic mismatch', row['id'])
        semantic_sha = sha256((canonical(semantics)+'\n').encode()).hexdigest()
        assert semantic_sha == archive['semantic_sha256']
        evaluation, stats = evaluation_audit(row)
        assert evaluation == archive['evaluation'], ('evaluation certificate mismatch', row['id'])
        cost = structural_cost(row, semantics, evaluation, stats)
        cost['core_intersection_iterations'] = primary_intersection_count_only(row['core'])
        assert cost == archive['cost'], ('cost audit mismatch', row['id'], cost, archive['cost'])
        semantic_rows.append(semantics)
        audited_costs.append(cost)
        verification_rows.append(dict(id=row['id'], semantic_sha256=semantic_sha,
                                      complete_semantic_comparison=True,
                                      endpoint_primitive_certificate_comparison=True,
                                      structural_cost_and_reported_operand_audit=True,
                                      independent_core_event_vertices=row['core_event_count'],
                                      independent_core_components=len(row['core_components']),
                                      direct_single_interval_checks=4,
                                      direct_selected_overlap_checks=int(row['selected'] is not None),
                                      direct_positive_strip_overlap_checks=stats['direct_strip_overlap_checks'],
                                      negative_residual_evaluator=(evaluation['overlap']['r'] < 0 if evaluation['overlap'] else False),
                                      selected_pair=semantics['selected_pair'],
                                      queried_overlap=semantics['queried_overlap'],
                                      duration_lower_bound=semantics['duration_lower_bound'], outcome=semantics['outcome'],
                                      primary_cost_audit=cost))
        print('PASS:', row['id'], 'semantic digest, direct intervals, strip certificate and cost audit', flush=True)
    stopped = rows[-1]['id'] if rows and rows[-1]['outcome'] == 'uncertified' else None
    unrun = [case['id'] for case in protocol['ordered_cases'][len(rows):]]
    outcomes = {key: sum(row['outcome'] == key for row in semantic_rows)
                for key in ('positive_duration', 'endpoint_interval', 'endpoint_contact', 'uncertified')}
    expected_summary = dict(processed_cases=len(rows), outcome_counts=outcomes,
                            cap_class_failures=sum(row['one_pair_cap_class_failure'] for row in semantic_rows),
                            selected_query_failures=sum(row['selected_query_failure'] for row in semantic_rows),
                            exact_overlap_queries=sum(row['selected_pair'] is not None for row in semantic_rows),
                            endpoint_tests=sum(row['endpoint_fallback'] is not None for row in semantic_rows),
                            positive_duration_certificates=outcomes['positive_duration']+outcomes['endpoint_interval'])
    assert_fields(dict(stopped_at_uncertified=stopped, unrun_case_ids=unrun, summary=expected_summary,
                       status='OBSERVED frozen known-control policy diagnostic; general implications remain proof candidates; no novelty or speedup claim'),
                  source, 'campaign')
    assert all(row['outcome'] != 'uncertified' for row in rows[:-1])
    numeric_cost_keys = [key for key, value in audited_costs[0].items() if type(value) is int]
    out = dict(status='REPRODUCED frozen known-control policy outputs; general implications remain proof candidates',
               protocol_sha256=PROTOCOL_SHA256, source_results_sha256=sha256(source_bytes).hexdigest(),
               primary_script_sha256=source['script_sha256'],
               verifier_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
               processed_cases=len(rows), stopped_at_uncertified=stopped, unrun_case_ids=unrun,
               semantic_digest_comparisons=len(rows),
               independent_core_components=sum(len(row['core_components']) for row in rows),
               direct_single_interval_checks=4*len(rows),
               direct_selected_overlap_checks=sum(row['selected'] is not None for row in rows),
               direct_positive_strip_overlap_checks=sum(row['direct_positive_strip_overlap_checks'] for row in verification_rows),
               negative_residual_overlap_checks=sum(row['negative_residual_evaluator'] for row in verification_rows),
               methods=['three-core threshold-event states retaining equality and singleton components',
                        'widest-earliest core window fixed before residual calculations',
                        'four clipped strict-blocker interval durations',
                        'frozen cap ranking and direct interval intersection for the chosen pair only',
                        'right-endpoint direct distance tests and seven individual safe laps only when valid',
                        'every positive residual-strip formula independently checked against chosen-pair interval overlap',
                        'separate audit of published formula/call counts, primitive arguments and reported rational bit sizes'],
               limits=[
                   'The campaign stops immediately at its first uncertified case and makes no new endpoint/window/pair choice after failure.',
                   'No full seven-runner allowed set, unselected-pair overlap, benchmark archive or primary implementation is read or reconstructed.',
                   'Core policy windows are event-state results. A separate count-only lap-intersection path audits the primary comparison counter and does not supply policy inputs.',
                   'Primary cost counters describe its specified evaluation path. They are separate from the verifier interval algorithm and are not timing measurements or a speedup claim.',
                   'Primitive bit sizes cover reported C/P arguments; reported-fraction bits cover semantic/evaluation strings. Neither bounds every transient arithmetic operand.',
                   'Agreement on these known controls supplies no arbitrary-speed existence guarantee, core selector theorem, or novelty claim.'],
               primary_numeric_cost_totals={key: sum(cost[key] for cost in audited_costs) for key in numeric_cost_keys},
               summary=expected_summary, cases=verification_rows)
    destination = HERE/'verification.json'
    if args.write:
        destination.write_text(json.dumps(out, indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == out
    print('PASS: complete independent campaign comparison;', 'saved' if args.write else 'read-only replay', flush=True)


if __name__ == '__main__':
    main()
