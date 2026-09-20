"""Exact blocking schedules for seven existing eight-runner examples.

Run: python -m scripts.analyze_blocking_overlaps
No new speed-set search. Cells are cut at every blocking-status boundary;
their rational midpoints represent whole constant-status cells, not a time grid.
"""

import hashlib
import json
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals

ROOT = Path(__file__).resolve().parents[1]
D = Q(1, 8)


def blocking_intervals(v):
    return [(max(Q(0), (Q(j)-D)/v), min(Q(1), (Q(j)+D)/v))
            for j in range(v+1)]


def intersection_length(left, right):
    # Direct interval-pair intersection, independent of the schedule partition.
    return sum((max(Q(0), min(b,d)-max(a,c))
                for a,b in left for c,d in right), Q(0))


def analyze_case(case):
    speeds = case['relative_speeds_in_label_order']
    cuts = sorted({Q(0), Q(1), *(x for v in speeds
                  for interval in blocking_intervals(v) for x in interval)})
    histogram = defaultdict(Q)
    pair_lengths = defaultdict(Q)
    cells = []
    for a,b in zip(cuts,cuts[1:]):
        t = (a+b)/2
        blocked = sorted(v for v in speeds if circular_distance(v*t) < D)
        histogram[len(blocked)] += b-a
        for pair in combinations(blocked,2):
            pair_lengths[pair] += b-a
        cells.append({'open_interval':[str(a),str(b)], 'strict_blockers':blocked})
    assert sum(histogram.values()) == 1
    individual_total = sum(j*width for j,width in histogram.items())
    assert individual_total == Q(7,4)
    allowed = feasible_intervals(speeds,D)
    safe_duration = sum((b-a for a,b in allowed),Q(0))
    assert safe_duration == histogram[0]
    assert [[str(a),str(b)] for a,b in allowed] == case['allowed_intervals']
    extra_blocking = sum(max(0,j-1)*width for j,width in histogram.items())
    assert extra_blocking == Q(3,4)+safe_duration
    assert sum(pair_lengths.values()) == sum(j*(j-1)//2*width for j,width in histogram.items())
    pairs = []
    for a,b in combinations(sorted(speeds),2):
        overlap = intersection_length(blocking_intervals(a),blocking_intervals(b))
        assert overlap == pair_lengths[a,b]
        pairs.append({'speeds':[a,b], 'both_blocking_duration':str(overlap)})
    handoffs = []
    for t in cuts:
        outgoing = [v for v in speeds if v*t % 1 == D]
        incoming = [v for v in speeds if v*t % 1 == 1-D]
        if outgoing and incoming:
            for a in outgoing:
                for b in incoming:
                    p = a*t-D
                    q = b*t+D
                    assert p.denominator == q.denominator == 1
                    assert 8*(a*q-b*p) == a+b
            handoffs.append({'time':str(t),'blocking_ends':outgoing,
                             'blocking_starts':incoming,
                             'strict_blockers':[v for v in speeds if circular_distance(v*t)<D]})
    return {'label':case['label'], 'original_n':8, 'reference_speed':1,
            'relative_speeds':speeds, 'selected_maximum':case['maximum'],
            'all_reference_evidence':'cooperative_blocking.json',
            'histogram_duration_by_number_blocking':{str(j):str(histogram[j]) for j in range(8)},
            'safe_duration':str(safe_duration), 'extra_blocking_duration':str(extra_blocking),
            'summed_pair_overlap':str(sum(pair_lengths.values())),
            'pair_overlaps':pairs, 'allowed_intervals':case['allowed_intervals'],
            'opposite_boundary_contacts':handoffs, 'schedule_cells':cells}


def local_example(label,p,q):
    a,b = 11,13
    left = ((Q(p)-D)/a,(Q(p)+D)/a)
    right = ((Q(q)-D)/b,(Q(q)+D)/b)
    determinant = a*q-b*p
    assert determinant > 0
    signed_gap = right[0]-left[1]
    assert signed_gap == Q(8*determinant-a-b,8*a*b)
    relation = 'overlap' if signed_gap<0 else 'touch' if signed_gap==0 else 'gap'
    result = {'label':label,'speeds':[a,b], 'meeting_numerators':[p,q],
              'meeting_times':[str(Q(p,a)),str(Q(q,b))],
              'blocking_windows':[[str(x) for x in left],[str(x) for x in right]],
              'determinant':determinant,'signed_gap':str(signed_gap),'relation':relation}
    if relation == 'gap':
        cover = ((Q(2)-D)/7,(Q(2)+D)/7)
        assert cover[0] < left[1] < right[0] < cover[1]
        result['gap_covered_by_speed'] = 7
        result['covering_window'] = list(map(str,cover))
    elif relation == 'touch':
        t = left[1]
        speeds = (1,4,5,6,7,11,13)
        assert min(circular_distance(v*t) for v in speeds) == D
        result['all_seven_clear_at'] = str(t)
    return result


def main():
    source_path = ROOT/'experiments/cooperative_blocking.json'
    source = json.loads(source_path.read_text())
    cases = [analyze_case(c) for c in source['cases']]
    examples = [local_example('overlap',5,6),local_example('touch',4,5),
                local_example('gap_covered_elsewhere',3,4)]
    assert [e['signed_gap'] for e in examples] == ['-2/143','0','2/143']
    lookup = {c['label']:c for c in cases}
    assert Q(lookup['double_replacement']['summed_pair_overlap']) < Q(lookup['control_12_13']['summed_pair_overlap']) < Q(lookup['consecutive']['summed_pair_overlap'])
    assert all(lookup[label]['safe_duration']=='0' for label in ('consecutive','single_replacement','double_replacement'))
    assert lookup['control_12_13']['safe_duration'] == '115/2184'
    data = {'date':'2026-09-20','base_commit':'03f950b65b1544c99a085b15ddf82d47381caf64',
            'source_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
            'scope':'Seven existing selected-reference schedules; three local views of the same 11/13 pair. No new speed-set search.',
            'original_n':8, 'threshold':str(D),'local_pair_examples':examples,'cases':cases,
            'limitations':'Durations ignore isolated endpoints. Closed allowed intervals are retained and independently crosschecked. Pair-overlap totals are not a tightness classification; no novelty or general LRC proof claim.'}
    (ROOT/'experiments/blocking_overlaps.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'cases':[{k:c[k] for k in ('label','safe_duration','summed_pair_overlap','extra_blocking_duration')} for c in cases],
                      'local_examples':examples,'pair_overlap_crosschecks':sum(len(c['pair_overlaps']) for c in cases)},indent=2))


if __name__ == '__main__':
    main()
