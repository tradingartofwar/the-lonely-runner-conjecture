"""Prescribed Fibonacci prefixes, pair comparisons, and four nearby controls.

Run: python -m scripts.check_fibonacci_patterns
All maxima use the exact checker with its separate closed-interval crosscheck.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import check, circular_distance
from scripts.analyze_cooperative_blocking import peak_faces

ROOT = Path(__file__).resolve().parents[1]
FIB = (1,2,3,5,8,13,21,34,55,89,144,233,377)
CONTROLS = {
    '21_to_20':(1,2,3,5,8,13,20),
    '21_to_22':(1,2,3,5,8,13,22),
    '13_to_12':(1,2,3,5,8,12,21),
    '13_to_14':(1,2,3,5,8,14,21),
}


def evaluate(label, speeds, all_references):
    actual = (0,*speeds)
    rows = []
    for ref in range(len(actual) if all_references else 1):
        result = check(actual, reference=ref)
        maximum = result['maximum']
        assert maximum['crosschecked_with_intervals']
        assert Q(maximum['separation']) >= Q(1,len(actual))
        if ref == 0:
            selected = result
        rows.append({'actual_speed_in_reference_frame':actual[ref],
                     'maximum':maximum['separation'], 'tight':maximum['tight'],
                     'peak_times':maximum['times_original']})
    maximum = Q(selected['maximum']['separation'])
    return {'label':label, 'n':len(actual), 'selected_reference_speed':0,
            'relative_speeds':speeds, 'target':str(Q(1,len(actual))),
            'selected_maximum':str(maximum),
            'selected_peak_times':selected['maximum']['times_original'],
            'selected_peak_faces':[peak_faces(speeds,Q(t),maximum)
                                   for t in selected['maximum']['times_original']],
            'all_references_checked':all_references, 'reference_results':rows,
            'minimum_over_all_reference_maxima':str(min(Q(r['maximum']) for r in rows)) if all_references else None,
            'tight_reference_speeds':[r['actual_speed_in_reference_frame'] for r in rows if r['tight']] if all_references else None}


def main():
    prefixes = [evaluate(f'prefix_{k}',FIB[:k],all_references=k<=9)
                for k in range(2,14)]
    controls = [evaluate(label,V,True) for label,V in CONTROLS.items()]
    expected = ['1/3','1/4','1/4',*(['2/11']*4),*(['5/29']*4),'13/76']
    assert [r['selected_maximum'] for r in prefixes] == expected
    for row in prefixes:
        if row['all_references_checked'] and row['n']>=5:
            assert row['tight_reference_speeds'] == []
    assert [r['selected_maximum'] for r in controls] == ['2/11','1/6','2/11','2/11']
    assert all(row['minimum_over_all_reference_maxima']==row['selected_maximum']
               for row in prefixes if row['all_references_checked'])

    pair_results = []
    for a,b in zip(FIB[:7],FIB[1:8]):
        result = check((0,a,b))
        assert result['maximum']['crosschecked_with_intervals']
        pair_results.append({'speeds':[a,b],'n':3,'target':'1/3',
                             'maximum':result['maximum']['separation'],
                             'peak_times':result['maximum']['times_original']})
    assert [r['maximum'] for r in pair_results] == ['1/3','2/5','1/2','6/13','10/21','1/2','27/55']

    # Any equal-distance opposite-phase pair meets at an integer value of
    # (a+b)t. If a+b is present, that third speed has distance zero.
    triad_checks = []
    for a,b,c in [*zip(FIB,FIB[1:],FIB[2:]),(4,7,11)]:
        assert a+b == c
        contacts = 0
        for j in range(1,c):
            t = Q(j,c)
            da,db,dc = (circular_distance(v*t) for v in (a,b,c))
            assert da == db and dc == 0
            if da>0:
                contacts += 1
        triad_checks.append({'speeds':[a,b,c], 'opposite_equal_distance_contacts_blocked':contacts})
    t = Q(3,8)
    snapshot = [{'relative_speed':v,'phase':str(v*t%1),
                 'distance':str(circular_distance(v*t))} for v in (3,5,8)]
    assert [r['distance'] for r in snapshot] == ['1/8','1/8','0']

    # Derive the observed plateau failure directly from the old peak times.
    failures = []
    for old_t,added in ((Q(3,11),55),(Q(8,29),377)):
        assert circular_distance(added*old_t) == 0
        failures.append({'old_peak_time':str(old_t),'added_fibonacci_speed':added,
                         'laps_at_old_time':str(added*old_t),'distance':'0'})
    # The same first plateau need not use a Fibonacci replacement.
    witness = Q(3,11)
    assert circular_distance(20*witness) == Q(5,11)
    assert circular_distance(21*witness) == Q(3,11)
    assert circular_distance(22*witness) == 0

    F = [0,1]
    L = [2,1]
    for _ in range(10):
        F.append(F[-1]+F[-2]);L.append(L[-1]+L[-2])
    patterned_rows = []
    for m,n in ((2,6),(3,10),(4,14)):
        row = next(r for r in prefixes if r['n']==n)
        height,t = Q(F[2*m-1],L[2*m+1]),Q(F[2*m],L[2*m+1])
        assert Q(row['selected_maximum']) == height
        assert row['selected_peak_times'] == [str(t),str(1-t)]
        patterned_rows.append({'m':m,'first_n':n,'height':str(height),
                               'times':[str(t),str(1-t)],
                               'F_numerator_index':2*m-1,'Lucas_denominator_index':2*m+1})
    calls = sum(len(r['reference_results']) for r in prefixes+controls)+len(pair_results)
    assert calls == 95
    data = {'date':'2026-09-20','base_commit':'9d0c1ad083e843d73409f883126870a10b2674e0',
            'checker_sha256':hashlib.sha256((ROOT/'lonely_runner/checker.py').read_bytes()).hexdigest(),
            'scope':'12 prescribed Fibonacci prefixes (n=3..14), all references for n<=10; 4 eight-runner controls with all references; 7 selected-reference Fibonacci pairs.',
            'reference_evaluations':calls,'repeated_evaluation_note':'The selected reference of (0,1,2) appears in both prefix and pair comparisons.',
            'fibonacci_prefixes':prefixes,'nearby_controls':controls,'pair_comparisons':pair_results,
            'additive_triad_checks':triad_checks,'snapshot_3_8':snapshot,
            'plateau_breaks':failures,'fibonacci_lucas_matches':patterned_rows,
            'limitations':'No general Fibonacci-prefix maximum formula proved; the third four-case plateau is checked only at its first case n=14. Not all references were checked for n=11..14. No novelty or general LRC proof claim.'}
    (ROOT/'experiments/fibonacci_patterns.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'reference_evaluations':calls,
                      'prefixes':[{key:r[key] for key in ('n','selected_maximum','selected_peak_times','all_references_checked','tight_reference_speeds')} for r in prefixes],
                      'controls':[{key:r[key] for key in ('label','selected_maximum','tight_reference_speeds')} for r in controls],
                      'fibonacci_lucas_matches':patterned_rows},indent=2))


if __name__ == '__main__':
    main()
