"""Exact continuum check of the two predeclared time-pair certificates.

Uses only protocol inputs, no primary profile or project imports. Phase
partitions are derived from distance corners, cap crossings, and affine
equalities, not from a sampled phase grid. --write writes certificates.json;
default/--check compares read-only.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'protocol.json'
OUT = HERE / 'certificates.json'
PROTOCOL_SHA = '8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17'


def distance(x):
    y = x % 1
    return min(y, 1-y)


def line(left, right, fn):
    slope = (fn(right)-fn(left))/(right-left)
    return slope, fn(left)-slope*left


def value(coefficients, x):
    slope, intercept = coefficients
    return slope*x+intercept


def extremal_set(cuts, cells, key, target):
    """Represent an extremal set on the phase circle without duplicating 1."""
    intervals = []
    points = {t % 1 for t in cuts if cells['evaluate'][key](t) == target}
    for a, b, coeffs in cells['lines'][key]:
        if coeffs == (F(0), target):
            if intervals and intervals[-1][1] == a:
                intervals[-1] = (intervals[-1][0], b)
            else:
                intervals.append((a, b))
    if intervals == [(F(0), F(1))]:
        return dict(full_circle=True, closed_intervals=[], isolated_points=[])
    points = {t for t in points if not any(a <= t <= b for a, b in intervals)}
    return dict(full_circle=False,
                closed_intervals=[[str(a), str(b)] for a, b in intervals],
                isolated_points=list(map(str, sorted(points))))


def case_certificate(case, candidate, chosen, threshold):
    times = list(map(F, candidate['times']))
    assert len(times) == 2
    unchanged = [v for v in case['velocities'][1:] if v != chosen]
    rows = []
    for t in times:
        ds = [(v, distance(v*t)) for v in unchanged]
        rows.append(dict(time=str(t), unchanged_distances=[[v, str(d)] for v, d in ds],
                         unchanged_minimum=str(min(d for _, d in ds)),
                         unchanged_bottleneck_speeds=[v for v, d in ds if d == min(x for _, x in ds)],
                         chosen_runner_base_phase=str((chosen*t) % 1)))
    phases = [F(r['chosen_runner_base_phase']) for r in rows]
    caps = [F(r['unchanged_minimum']) for r in rows]
    separation = distance(phases[1]-phases[0])
    geometric_bound = min(min(caps), separation/2)
    signed_diff = (phases[1]-phases[0]) % 1
    if signed_diff > F(1, 2):
        signed_diff -= 1
    raw_min_phase = (-(phases[0]+signed_diff/2)) % 1
    assert max(distance(x+raw_min_phase) for x in phases) == separation/2

    # Each raw distance has corners at phase 0 and 1/2. Clipping at cap c
    # introduces only raw-distance crossings c and 1-c.
    cuts = {F(0), F(1)}
    for x, c in zip(phases, caps):
        cuts |= {(-x) % 1, (F(1, 2)-x) % 1, (c-x) % 1, (-c-x) % 1}
    funcs = {
        'raw_speed11': [lambda theta, x=x: distance(x+theta) for x in phases],
        'full_margin': [lambda theta, x=x, c=c: min(c, distance(x+theta))
                        for x, c in zip(phases, caps)]}
    preliminary = sorted(cuts)
    crossings = set()
    for a, b in zip(preliminary, preliminary[1:]):
        for functions in funcs.values():
            first, second = [line(a, b, fn) for fn in functions]
            if first[0] != second[0]:
                t = (second[1]-first[1])/(first[0]-second[0])
                if a < t < b:
                    crossings.add(t)
    cuts = sorted(cuts | crossings)
    lines = {key: [] for key in funcs}
    profile = []
    for a, b in zip(cuts, cuts[1:]):
        mid = (a+b)/2
        item = dict(left=str(a), right=str(b))
        for key, functions in funcs.items():
            coefficients = [line(a, b, fn) for fn in functions]
            for coeffs, fn in zip(coefficients, functions):
                assert value(coeffs, mid) == fn(mid)
            winner = max(range(2), key=lambda i: value(coefficients[i], mid))
            selected = coefficients[winner]
            lines[key].append((a, b, selected))
            assert all(value(selected, t) == max(fn(t) for fn in functions) for t in (a, mid, b))
            item[key] = dict(slope=str(selected[0]), intercept=str(selected[1]),
                             maximizing_time_index=winner)
        profile.append(item)
    evaluate = {key: (lambda t, fs=fs: max(fn(t) for fn in fs)) for key, fs in funcs.items()}
    extrema = {}
    for key in funcs:
        minimum = min(evaluate[key](t) for t in cuts)
        maximum = max(evaluate[key](t) for t in cuts)
        extrema[key] = dict(minimum=str(minimum), maximum=str(maximum),
                           argmin=extremal_set(cuts, dict(lines=lines, evaluate=evaluate), key, minimum))
    assert F(extrema['raw_speed11']['minimum']) == separation/2
    assert F(extrema['full_margin']['minimum']) >= geometric_bound
    exact_margin = F(extrema['full_margin']['minimum'])
    return dict(id=case['id'], velocities=case['velocities'], chosen_runner_speed=chosen,
                times=rows, circular_phase_separation=str(separation),
                geometric_half_separation=str(separation/2),
                geometric_universal_margin_lower_bound=str(geometric_bound),
                raw_geometric_minimizing_phase=str(raw_min_phase),
                exact_worst_phase_best_of_two_margin=str(exact_margin),
                excess_above_threshold=str(exact_margin-threshold),
                certifies_all_phase_existence=exact_margin >= threshold,
                certifies_all_phase_strictness=exact_margin > threshold,
                extrema=extrema,
                phase_event_points=[dict(phase=str(t), raw_speed11=str(evaluate['raw_speed11'](t)),
                                         full_margin=str(evaluate['full_margin'](t))) for t in cuts[:-1]],
                phase_cells=profile,
                phase_one_identified_with_zero=True,
                full_margin_constant=extrema['full_margin']['minimum'] == extrema['full_margin']['maximum'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assert sha256(PROTOCOL.read_bytes()).hexdigest() == PROTOCOL_SHA
    protocol = json.loads(PROTOCOL.read_text())
    candidates = {row['case']: row for row in protocol['compact_certificate_test']['fixed_candidate_pairs']}
    result = dict(status='OBSERVED exact constants; supplied all-phase geometric certificate; no global optimality claim',
                  protocol_sha256=PROTOCOL_SHA,
                  script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  cases=[case_certificate(case, candidates[case['id']], protocol['chosen_runner_speed'],
                                          F(protocol['threshold'])) for case in protocol['cases']])
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(OUT.read_text()), 'certificates.json differs'
    print(json.dumps(dict(status='PASS', cases=[dict(
        id=c['id'], separation=c['circular_phase_separation'],
        worst_margin=c['exact_worst_phase_best_of_two_margin'],
        strict_excess=c['excess_above_threshold'], constant=c['full_margin_constant'])
        for c in result['cases']]), indent=2))


if __name__ == '__main__':
    main()
