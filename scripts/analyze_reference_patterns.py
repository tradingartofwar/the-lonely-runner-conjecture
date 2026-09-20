"""Group existing eight-runner results and certify near-peak timing windows."""

import json
from collections import defaultdict
from fractions import Fraction as Q
from math import gcd
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals

ROOT = Path(__file__).resolve().parents[1]
D = Q(1, 8)


def main():
    roles = json.loads((ROOT/'experiments/reference_runner_roles.json').read_text())
    cooperative = json.loads((ROOT/'experiments/cooperative_blocking.json').read_text())
    configs = {}
    for c in roles['cases']:
        if c['n'] == 8:
            configs[tuple(sorted(c['actual_speeds']))] = {
                'label': c['label'], 'rows': [(r['speed'],r['maximum']) for r in c['runners']]}
    for c in cooperative['cases']:
        key = tuple(sorted(c['actual_speeds_in_label_order']))
        rows = [(r['actual_speed'],r['maximum']) for r in c['all_references']]
        if key in configs:
            assert dict(configs[key]['rows']) == dict(rows)
        configs[key] = {'label':c['label'], 'rows':rows}

    groups = defaultdict(list)
    for actual, c in configs.items():
        for reference, maximum in c['rows']:
            if Q(maximum) != D:
                continue
            absolute = [abs(v-reference) for v in actual if v != reference]
            divisor = gcd(*absolute)
            primitive = tuple(sorted({v//divisor for v in absolute}))
            groups[primitive].append({'configuration':c['label'], 'actual_speeds':actual,
                                      'reference_speed':reference, 'gcd':divisor,
                                      'original_n':len(actual)})
    assert len(configs) == 10 and len(groups) == 3
    assert sum(map(len,groups.values())) == 7

    neighborhoods = []
    for c in cooperative['cases']:
        if not c['tight']:
            continue
        speeds = c['relative_speeds_in_label_order']
        rows = []
        for epsilon in (Q(1,800),Q(1,8000)):
            allowed = feasible_intervals(speeds,D-epsilon)
            expected = []
            for peak in c['peak_faces']:
                t = Q(peak['time'])
                a = t-epsilon/peak['left_slope']
                b = t+epsilon/abs(peak['right_slope'])
                expected.append((a,b))
                # Certify the complete local distance envelope. Every distance
                # is affine between the included m/(2v) corners, so endpoint
                # inequalities suffice on each piece. An active curve attains it.
                for left,right,slope,controller in [
                    (a,t,peak['left_slope'],peak['left_controller']),
                    (t,b,peak['right_slope'],peak['right_controller'])]:
                    for v in speeds:
                        cuts = {left,right,*(Q(m,2*v) for m in range(2*v+1) if left<Q(m,2*v)<right)}
                        for tau in cuts:
                            assert circular_distance(v*tau) >= D+slope*(tau-t)
                            if v == controller:
                                assert circular_distance(v*tau) == D+slope*(tau-t)
            assert tuple(expected) == allowed
            rows.append({'epsilon':str(epsilon), 'threshold':str(D-epsilon),
                         'intervals':[[str(a),str(b)] for a,b in allowed],
                         'widths':[str(b-a) for a,b in allowed],
                         'total_width':str(sum(b-a for a,b in allowed)),
                         'total_width_over_epsilon':str(sum(b-a for a,b in allowed)/epsilon)})
        neighborhoods.append({'label':c['label'],'relative_speeds':speeds,
                              'peak_faces':c['peak_faces'],'relaxations':rows})
    lookup = {r['label']:r for r in neighborhoods}
    assert lookup['consecutive']['relaxations'] == lookup['single_replacement']['relaxations']
    ratio = Q(lookup['double_replacement']['relaxations'][0]['widths'][1])/Q(lookup['consecutive']['relaxations'][0]['widths'][1])
    assert ratio == Q(45,143)
    t = Q(1,12)
    separation = lambda V: min(circular_distance(v*t) for v in V)
    assert separation(lookup['consecutive']['relative_speeds']) == Q(1,12)
    assert separation(lookup['single_replacement']['relative_speeds']) == 0

    individual = []
    for v in sorted({v for c in cooperative['cases'] for v in c['relative_speeds_in_label_order']}):
        allowed = feasible_intervals((v,),D)
        blocked_fraction = 1-sum(b-a for a,b in allowed)
        assert blocked_fraction == Q(1,4)
        individual.append({'relative_speed':v,'blocked_fraction':str(blocked_fraction)})

    data = {'date':'2026-09-20','base_commit':'c2e78cd515141dfdf75e29fa90826ad0585168e3',
            'scope':'Existing data for 10 distinct eight-runner configurations; 3 selected tight distance curves',
            'distinct_configurations':len(configs),'tight_references':sum(map(len,groups.values())),
            'groups':[{'primitive_absolute_relative_speeds':key,'members':members} for key,members in sorted(groups.items())],
            'near_peak_windows':neighborhoods,'middle_window_width_ratio_double_to_consecutive':str(ratio),
            'different_away_from_peaks':{'time':'1/12','consecutive_gap':'1/12','single_replacement_gap':'0'},
            'individual_blocking_fractions':individual,
            'limitations':'Grouping is within the selected data; equal normalization is sufficient, not asserted necessary, for curve equivalence. No complete tight-instance classification.'}
    (ROOT/'experiments/reference_patterns.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'configurations':len(configs),'tight_references':data['tight_references'],
                      'normalized_groups':len(groups),'middle_window_ratio':str(ratio),
                      'individual_blocking_fraction':'1/4',
                      'near_peak_complete_intervals_certified':True},indent=2))


if __name__ == '__main__':
    main()
