"""Exact challenge replay; two frozen speed lists and two declared time pairs.

Direct time intersections check the algebraically complete phase partition.
No project imports, numerical grid, new speed case, or new abstract example.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELTA = F(1, 8)


def meet(first, second):
    return sorted(set((max(a, c), min(b, d)) for a, b in first
                      for c, d in second if max(a, c) <= min(b, d)))


def safe(speed, phase=F(0)):
    phase %= 1
    return [(max(F(0), (F(k)+DELTA-phase)/speed),
             min(F(1), (F(k)+1-DELTA-phase)/speed))
            for k in range(-1, speed+1)
            if max(F(0), (F(k)+DELTA-phase)/speed)
            <= min(F(1), (F(k)+1-DELTA-phase)/speed)]


def length(intervals):
    return sum((b-a for a, b in intervals), F(0))


def encode(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def contains(intervals, time):
    return any(a <= time <= b for a, b in intervals)


def distance(value):
    value %= 1
    return min(value, 1-value)


def build():
    protocol = json.loads((HERE/'protocol.json').read_text())
    archive = json.loads((HERE/'results.json').read_text())
    assert archive['protocol_sha256'] == sha256((HERE/'protocol.json').read_bytes()).hexdigest()
    rows = []
    for frozen, case, pair in zip(protocol['cases'], archive['cases'],
                                  protocol['compact_certificate_test']['fixed_candidate_pairs']):
        assert frozen['id'] == case['id'] == pair['case']
        V = frozen['velocities'][-1]
        speeds = [v for v in frozen['velocities'][1:] if v != 11]
        a_set = [(F(0), F(1))]
        for v in speeds:
            a_set = meet(a_set, safe(v))
        assert encode(a_set) == case['A_components']
        assert length(a_set) == F(case['A_duration'])
        events = sorted({F(0)} | {(11*t) % 1 for ab in a_set for t in ab})
        assert list(map(str, events)) == case['phase_events']
        for row in case['phase_points']:
            x = F(row['x'])
            preimages = [(j+x)/11 for j in range(12)
                         if contains(a_set, (j+x)/11)]
            assert list(map(str, preimages)) == row['preimages']
            assert len(preimages) == row['count']
        bulk = []
        for left, right, row in zip(events, events[1:]+[F(1)], case['phase_cells']):
            x = (left+right)/2
            branches = [j for j in range(11) if contains(a_set, (j+x)/11)]
            assert branches == row['preimage_branches']
            assert len(branches) == row['count']
            assert [str(left), str(right)] == [row['left'], row['right']]
            if branches:
                bulk.append((left, right))
        generated = sorted({F(0)} | {(level-e) % 1 for e in events
                                    for level in (DELTA, 1-DELTA)})
        assert list(map(str, generated)) == case['critical_phases']

        def direct(theta):
            allowed = meet(a_set, safe(11, theta))
            duration = length(allowed)
            estimate = length(meet(bulk, safe(1, theta)))/11
            status = 'strict' if duration else 'contacts' if allowed else 'empty'
            contacts = None if duration else [str(a) for a, b in allowed]
            return duration, estimate, status, contacts

        for row in case['theta_points']:
            result = direct(F(row['theta']))
            assert result == (F(row['duration']), F(row['support_estimate']),
                              row['status'], row['contact_times'])
        # Algebraic event completeness fixes every endpoint ordering inside
        # each cell; direct intersection duration is affine there. Two exact
        # interior values determine that affine formula, not a sampled-grid claim.
        for row in case['theta_cells']:
            left, right = F(row['left']), F(row['right'])
            for theta in ((2*left+right)/3, (left+2*right)/3):
                duration, estimate, status, contacts = direct(theta)
                assert duration == F(row['slope'])*theta+F(row['intercept'])
                assert estimate == F(row['support_slope'])*theta+F(row['support_intercept'])
                assert status == row['status'] and contacts == row['contact_times']

        expected = {
            13: ('0', '115/2184', [['0','0',True,True]], [['1/4','3/4',True,True]]),
            16: ('39/4928', '7/96', [['0','1/48',True,True],['47/48','1',True,False]],
                 [['61/128','67/128',True,True]])}[V]
        extrema = case['duration_extrema']
        assert (extrema['minimum'], extrema['maximum'], extrema['minimizer_set'],
                extrema['maximizer_set']) == expected
        expected_metrics = {13: ('1/4','3/4','1/4'),
                            16: ('151/448','45/64','45/64')}[V]
        assert (case['B_metrics']['measure'],
                case['P_metrics']['minimum_covering_arc_length'],
                case['B_metrics']['minimum_covering_arc_length']) == expected_metrics

        times = list(map(F, pair['times']))
        unchanged_distances = [[distance(v*t) for v in speeds] for t in times]
        assert unchanged_distances[0] == unchanged_distances[1]
        cap = min(unchanged_distances[0])
        separation = distance(11*(times[1]-times[0]))
        assert cap == separation/2 == (F(1,8) if V == 13 else F(2,15))
        radius = min([(d-DELTA)/v for v, d in zip(speeds, unchanged_distances[0])]
                     + [(cap-DELTA)/11])
        assert radius == (F(0) if V == 13 else F(1,1320))
        diagnostic = None
        if V == 16:
            at_zero, at_32 = direct(F(0)), direct(F(1,32))
            assert F(1,32) in generated
            assert at_zero[1] == at_32[1] == F(39,4928)
            assert at_zero[0] == F(39,4928) and at_32[0] == F(131,14784)
            diagnostic = dict(theta0=dict(duration=str(at_zero[0]), estimate=str(at_zero[1])),
                              theta_1_over_32=dict(duration=str(at_32[0]),estimate=str(at_32[1])),
                              extra_duration=str(at_32[0]-at_32[1]))
        rows.append(dict(id=case['id'], phase_events=len(events), theta_points=len(generated),
                         theta_cells=len(case['theta_cells']), extrema=extrema,
                         B_measure=expected_metrics[0], covering_arcs=dict(
                             P=expected_metrics[1], B=expected_metrics[2]),
                         pair=dict(times=list(map(str,times)),
                                   unchanged_distances=list(map(str,unchanged_distances[0])),
                                   phase_separation=str(separation), robust_margin=str(cap),
                                   safe_neighborhood_radius=str(radius)),
                         same_estimate_different_duration=diagnostic))
    return dict(status='OBSERVED exact finite checks; general arguments require separate review',
                protocol_sha256=sha256((HERE/'protocol.json').read_bytes()).hexdigest(),
                results_sha256=sha256((HERE/'results.json').read_bytes()).hexdigest(),
                script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(), cases=rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE/'challenge_checks.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(path.read_text()), 'challenge_checks.json differs'
    print(json.dumps(dict(status='PASS', cases=[dict(id=c['id'],
                          theta_points=c['theta_points'], theta_cells=c['theta_cells'])
                          for c in result['cases']]), indent=2))


if __name__ == '__main__':
    main()
