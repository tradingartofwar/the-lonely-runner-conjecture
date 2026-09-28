"""Frozen one-pair policy, with signed-residual endpoint-primitive evaluation.

Selection uses only supplied-core safe components and four single durations.
At most one pair is queried, then at most one prescribed endpoint is tested.
No benchmark, all-pair archive, or complete seven-speed allowed set is read.
Default/--check replays read-only; --write creates results.json.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import re

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results.json'
PROTOCOL_HASH = '36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e'
DELTA = F(1, 8)
OUTCOMES = ['positive_duration', 'endpoint_interval', 'endpoint_contact', 'uncertified']


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def distance(x):
    p = x % 1
    return min(p, 1-p)


def intersect(a, b):
    out = []
    i = j = iterations = 0
    while i < len(a) and j < len(b):
        iterations += 1
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            out.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        elif b[j][1] < a[i][1]:
            j += 1
        else:
            i += 1
            j += 1
    return out, iterations


def core_safe(core):
    components = [(F(0), F(1))]
    events = {F(0), F(1)}
    iterations = 0
    for v in core:
        laps = [(F(8*j+1, 8*v), F(8*j+7, 8*v)) for j in range(v)]
        events.update(x for lap in laps for x in lap)
        components, count = intersect(components, laps)
        iterations += count
    return components, len(events), iterations


def C(z, arguments):
    arguments.append(z)
    m = floor(z)
    r = z-m
    return F(m, 4)+min(r, DELTA)+max(F(0), r-(1-DELTA))


def P(z, arguments):
    arguments.append(z)
    r = z % 1
    return r*(r-1)/2


def operand_bits(values):
    if not values:
        return None
    return {'maximum_numerator_bits': max(abs(x.numerator).bit_length() for x in values),
            'maximum_denominator_bits': max(x.denominator.bit_length() for x in values)}


def fraction_strings(value):
    if isinstance(value, str) and re.fullmatch(r'-?\d+(?:/\d+)?', value):
        yield F(value)
    elif isinstance(value, dict):
        for child in value.values():
            yield from fraction_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from fraction_strings(child)


def endpoint_data(speed, slope, intercept, source, A, B, primitive_arguments):
    frequency = speed-slope
    assert frequency > 0
    args = [frequency*A-intercept, frequency*B-intercept]
    values = [P(x, primitive_arguments) for x in args]
    W = (values[1]-values[0])/frequency
    return {'slope': str(slope), 'intercept': str(intercept), 'source': source,
            'frequency': str(frequency), 'primitive_arguments': list(map(str, args)),
            'primitive_values': list(map(str, values)), 'W': str(W)}, W


def selected_overlap(pair, A, B):
    a, b = pair
    h = min((1, 2), key=lambda candidate: (abs(b-candidate*a), candidate))
    r = b-h*a
    ra, rb = sorted((r*A, r*B))
    support = (h+1)*DELTA
    mlo, mhi = (floor(ra-support), ceil(rb+support)) if r else (0, 0)
    candidates, cells, p_arguments = [], [], []
    total_area = total_correction = total_overlap = F(0)
    examined = 0
    for m in range(mlo, mhi+1):
        points = {A, B}
        if r:
            for offset in (-(h+1)*DELTA, (h+1)*DELTA, -(h-1)*DELTA, (h-1)*DELTA):
                crossing = (m+offset)/r
                if A < crossing < B:
                    points.add(crossing)
        points = sorted(points)
        positive_count = 0
        for left, right in zip(points, points[1:]):
            examined += 1
            mid = (left+right)/2
            affine_slope = F(-r, h)
            low_intercept, up_intercept = (m-DELTA)/h, (m+DELTA)/h
            if affine_slope*mid+low_intercept > -DELTA:
                ls, ld, lsource = affine_slope, low_intercept, 'affine'
            else:
                ls, ld, lsource = F(0), -DELTA, 'constant'
            if affine_slope*mid+up_intercept < DELTA:
                us, ud, usource = affine_slope, up_intercept, 'affine'
            else:
                us, ud, usource = F(0), DELTA, 'constant'
            if ls*mid+ld >= us*mid+ud:
                continue
            assert (us-ls)*left+ud-ld >= 0 and (us-ls)*right+ud-ld >= 0
            positive_count += 1
            area = (us-ls)*(right*right-left*left)/2+(ud-ld)*(right-left)
            lower, lw = endpoint_data(a, ls, ld, lsource, left, right, p_arguments)
            upper, uw = endpoint_data(a, us, ud, usource, left, right, p_arguments)
            assert F(lower['frequency']) in (F(a), F(b, h))
            assert F(upper['frequency']) in (F(a), F(b, h))
            correction = uw-lw
            overlap = area+correction
            assert area > 0 and overlap >= 0
            cells.append({'m': m, 'interval': [str(left), str(right)], 'lower': lower, 'upper': upper,
                          'area': str(area), 'endpoint_correction': str(correction), 'overlap': str(overlap)})
            total_area += area
            total_correction += correction
            total_overlap += overlap
        candidates.append({'m': m, 'breakpoints': list(map(str, points)), 'positive_cell_count': positive_count})
    assert len(p_arguments) == 4*len(cells)
    record = {'pair': list(pair), 'h': h, 'r': r, 'residual_range': [str(ra), str(rb)],
              'm_range': [mlo, mhi], 'candidate_strips': candidates, 'positive_cells': cells,
              'phase_area': str(total_area), 'endpoint_correction': str(total_correction),
              'overlap': str(total_overlap)}
    cost = {'residual_strip_candidates': len(candidates),
            'residual_event_candidates': 4*len(candidates) if r else 0,
            'residual_cells_examined': examined, 'positive_strip_cells': len(cells),
            'overlap_W_calls': 2*len(cells), 'overlap_P_calls': len(p_arguments),
            'overlap_primitive_operand_bits': operand_bits(p_arguments)}
    return total_overlap, record, cost


def fallback_endpoint(t, speeds):
    distances = [(v, distance(v*t)) for v in speeds]
    failed = [v for v, d in distances if d < DELTA]
    record = {'time': str(t), 'distances': [[v, str(d)] for v, d in distances], 'valid': not failed,
              'failed_speeds': failed, 'safe_laps': [], 'shared_safe_interval': None,
              'shared_safe_width': None, 'equality_controllers': []}
    if failed:
        return record, 'uncertified'
    intervals = []
    for v, d in distances:
        j = floor(v*t)
        left, right = (j+DELTA)/v, (j+1-DELTA)/v
        assert left <= t <= right
        intervals.append((left, right))
        record['safe_laps'].append({'speed': v, 'lap': j, 'interval': [str(left), str(right)]})
        if d == DELTA:
            phase = v*t-j
            direction = 'right' if phase == DELTA else 'left'
            assert phase in (DELTA, 1-DELTA)
            record['equality_controllers'].append([v, direction])
    left, right = max(a for a, b in intervals), min(b for a, b in intervals)
    assert left <= t <= right
    record['shared_safe_interval'] = [str(left), str(right)]
    record['shared_safe_width'] = str(right-left)
    return record, 'endpoint_interval' if left < right else 'endpoint_contact'


def run_case(case):
    core, extras = sorted(case['core']), sorted(case['extras'])
    speeds = sorted(core+extras)
    assert len(core) == 3 and len(extras) == 4 and len(set(speeds)) == 7
    components, event_count, intersection_iterations = core_safe(core)
    positive = [(a, b) for a, b in components if a < b]
    assert positive, 'Frozen policy needs a positive-length supplied-core component'
    A, B = min(positive, key=lambda ab: (-(ab[1]-ab[0]), ab[0]))
    L = B-A
    arguments, singles, single_evaluations = [], {}, []
    for v in extras:
        args = [v*A, v*B]
        values = [C(x, arguments) for x in args]
        duration = (values[1]-values[0])/v
        singles[v] = duration
        single_evaluations.append({'speed': v, 'arguments': list(map(str, args)),
                                   'primitive_values': list(map(str, values)), 'duration': str(duration)})
    T = sum(singles.values(), F(0))
    E = T-L
    ranking = sorted(combinations(extras, 2), key=lambda pair: (-min(singles[v] for v in pair), pair))
    caps = [{'pair': list(pair), 'cap': str(min(singles[v] for v in pair))} for pair in ranking]
    top_cap = F(caps[0]['cap'])
    lower = -E
    chosen, overlap, overlap_record = None, None, None
    overlap_cost = {'residual_strip_candidates': 0, 'residual_event_candidates': 0,
                    'residual_cells_examined': 0, 'positive_strip_cells': 0,
                    'overlap_W_calls': 0, 'overlap_P_calls': 0, 'overlap_primitive_operand_bits': None}
    if E < 0:
        stage = 'singles_positive'
    elif top_cap <= E:
        stage = 'cap_ceiling'
    else:
        stage = 'queried_pair'
        chosen = ranking[0]
        overlap, overlap_record, overlap_cost = selected_overlap(chosen, A, B)
        assert 0 <= overlap <= top_cap
        lower = overlap-E
    if lower > 0:
        fallback, outcome = None, 'positive_duration'
    else:
        fallback, outcome = fallback_endpoint(B, speeds)
    semantic = {
        'id': case['id'], 'core': core, 'extras': extras,
        'core_components': [[str(a), str(b)] for a, b in components],
        'selected_window': [str(A), str(B)], 'window_width': str(L),
        'single_durations': [[v, str(singles[v])] for v in extras],
        'total_single_duration': str(T), 'excess': str(E), 'pair_ranking': caps,
        'stage': stage, 'selected_pair': list(chosen) if chosen else None,
        'queried_overlap': str(overlap) if overlap is not None else None,
        'duration_lower_bound': str(lower), 'one_pair_cap_class_failure': stage == 'cap_ceiling',
        'selected_query_failure': stage == 'queried_pair' and lower <= 0,
        'endpoint_fallback': fallback, 'outcome': outcome,
    }
    evaluation = {'single_evaluations': single_evaluations, 'overlap': overlap_record}
    cost = {
        'core_laps_by_speed': [[v, v] for v in core], 'core_laps_total': sum(core),
        'core_event_vertices': event_count, 'core_components': len(components),
        'core_intersection_iterations': intersection_iterations,
        'single_duration_evaluations': 4, 'single_primitive_calls': len(arguments), 'pair_caps': 6,
        'exact_overlap_queries': int(chosen is not None), **overlap_cost,
        'endpoint_tests': int(fallback is not None),
        'endpoint_distance_evaluations': 7 if fallback else 0,
        'safe_lap_constructions': 7 if fallback and fallback['valid'] else 0,
        'single_primitive_operand_bits': operand_bits(arguments),
        'reported_fraction_bits': operand_bits(list(fraction_strings([semantic, evaluation]))),
    }
    digest = sha256((json.dumps(semantic, sort_keys=True, separators=(',', ':'))+'\n').encode()).hexdigest()
    print(case['id'], 'J', str(A), str(B), 'E', E, 'pair', chosen, 'O', overlap,
          'bound', lower, 'outcome', outcome, flush=True)
    return {'semantic': semantic, 'semantic_sha256': digest, 'evaluation': evaluation, 'cost': cost}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH, 'Frozen protocol changed'
    protocol = json.loads(raw)
    cases, stopped = [], None
    for case in protocol['ordered_cases']:
        result = run_case(case)
        cases.append(result)
        if result['semantic']['outcome'] == 'uncertified':
            stopped = case['id']
            break
    counts = Counter(c['semantic']['outcome'] for c in cases)
    result = {
        'schema_version': 1, 'protocol_sha256': PROTOCOL_HASH,
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'status': 'OBSERVED frozen known-control policy diagnostic; general implications remain proof candidates; no novelty or speedup claim',
        'cases': cases, 'stopped_at_uncertified': stopped,
        'unrun_case_ids': [c['id'] for c in protocol['ordered_cases'][len(cases):]],
        'summary': {'processed_cases': len(cases), 'outcome_counts': {k: counts[k] for k in OUTCOMES},
                    'cap_class_failures': sum(c['semantic']['one_pair_cap_class_failure'] for c in cases),
                    'selected_query_failures': sum(c['semantic']['selected_query_failure'] for c in cases),
                    'exact_overlap_queries': sum(c['cost']['exact_overlap_queries'] for c in cases),
                    'endpoint_tests': sum(c['cost']['endpoint_tests'] for c in cases),
                    'positive_duration_certificates': counts['positive_duration']+counts['endpoint_interval']},
    }
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(OUT.read_text()), 'Archive drift'
    print('PASS: frozen ordered policy, signed-residual chosen-pair primitives, bounded fallback '
          'and stop rule; '+('written' if args.write else 'replayed read-only'))
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
