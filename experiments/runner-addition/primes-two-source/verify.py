#!/usr/bin/env python3
"""Exact retrospective check of the primes-derived two-source argument.

No imports from the experiment or checker implementations. This is same-author
verification of exposed data, not independent proof review or a new trial.
"""
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def phase(speed, time):
    return (speed * time) % 1


def safe(time, speeds, d):
    return all(d <= phase(v, time) <= 1 - d for v in speeds)


def complete_core(speeds, d):
    # Every predicate changes only at these events. Keep point cells separately
    # so isolated equality witnesses cannot disappear in interval sampling.
    events = {F(0), F(1)}
    for v in speeds:
        for j in range(v):
            events.update(((j + d) / v, (j + 1 - d) / v))
    events = sorted(events)
    pieces = [(t, t) for t in events if safe(t, speeds, d)]
    for a, b in zip(events, events[1:]):
        if safe((a + b) / 2, speeds, d):
            require(safe(a, speeds, d) and safe(b, speeds, d),
                    'A safe open cell has an unsafe endpoint')
            pieces.append((a, b))
    merged = []
    for a, b in sorted(pieces):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged, len(events)


def tail_time(r, a, d):
    x = r * a
    m = x.numerator // x.denominator
    f = x - m
    if d <= f <= 1 - d:
        return a, 'already_safe'
    if f < d:
        return (m + d) / r, 'below_safe_band'
    return (m + 1 + d) / r, 'above_safe_band'


def verify():
    cert = json.loads((HERE / 'CERTIFICATE.json').read_text())
    sources = {}
    for name, expected in cert['sources'].items():
        path = ROOT / name
        require(digest(path) == expected, 'Pinned source changed: ' + name)
        sources[Path(name).name] = json.loads(path.read_text())
    source = next(x for x in sources['RESULTS.json']['families']
                  if x['name'] == 'primes')
    export = next(x for x in sources['CERTIFICATES.json']['families']
                  if x['name'] == 'primes')
    scope = cert['scope']
    speeds = scope['core_speeds']
    d = F(scope['threshold'])
    require(speeds == [2, 3, 5, 7, 10, 13, 17, 19]
            and speeds == source['speeds'] == export['core_speeds'], 'Core scope')
    require(d == F(1, 10) and scope['total_runners'] == len(speeds) + 2 == 10
            and scope['reference'] == 0 and scope['common_start'] is True
            and scope['period'] == ['0', '1'], 'Runner/threshold scope')
    require(cert['source_commit'] == 'f7f87f7dd59b4809397730550fb0fd1a48eab2a1',
            'Source commit label')
    require(sources['CERTIFICATES.json']['source_results_sha256'] ==
            cert['sources']['experiments/runner-addition/unrestricted-single/results/RESULTS.json'],
            'Export binding')

    rows = cert['lower_bound']['half_components']
    require(rows == export['blockers'][:10], 'Changed half-certificate')
    half = [tuple(map(F, row['interval'])) for row in rows]
    require([row['component'] for row in rows] == list(range(10)), 'Half IDs')
    require(all(0 < a <= b < F(1, 2) for a, b in half), 'Half domain')
    expected = half + [(1-b, 1-a) for a, b in reversed(half)]
    core, events = complete_core(speeds, d)
    require(core == expected, 'Complete event geometry differs from table')
    require(core == [tuple(map(F, x['interval'])) for x in source['components']],
            'Source components differ from reconstructed core')
    require([x['id'] for x in source['components']] == list(range(20)), 'Source IDs')
    blockers = []
    for row in rows:
        a, b = map(F, row['interval'])
        r, m = row['r'], row['blocking_integer']
        require(isinstance(r, int) and r > 0 and r not in speeds, 'Blocker admissibility')
        require(isinstance(m, int), 'Blocking integer')
        for i, left, right, integer in (
            (row['component'], a, b, m),
            (19-row['component'], 1-b, 1-a, r-m),
        ):
            require((integer-d)/r < left <= right < (integer+d)/r,
                    'Non-strict or incorrect blocker')
            require(export['blockers'][i] == {
                'component': i, 'interval': [str(left), str(right)],
                'r': r, 'blocking_integer': integer}, 'Reflected source mismatch')
            blockers.append({'component': i, 'r': r, 'm': integer,
                             'left_phase_margin': str(r*left-integer+d),
                             'right_phase_margin': str(integer+d-r*right)})
    require(sorted({x['r'] for x in blockers}) ==
            cert['lower_bound']['recorded_blocker_speeds'] == [1, 4, 6, 8, 9],
            'Blocker list')

    upper = cert['upper_bound']
    a, b = map(F, upper['interval'])
    p = F(upper['repair_time'])
    require((a, b) == core[upper['interval_component']], 'Upper interval')
    repair = tuple(map(F, upper['repair_component_interval']))
    require(repair == core[upper['repair_component']] and repair[0] <= p <= repair[1],
            'Repair component')
    require(len(upper['core_laps']) == len(speeds), 'Lap vector length')
    bands = []
    for v, lap in zip(speeds, upper['core_laps']):
        require(isinstance(lap, int) and d <= v*a-lap <= v*b-lap <= 1-d,
                'Interval core-safety band')
        bands.append({'speed': v, 'lap': lap, 'phases': [str(v*a-lap), str(v*b-lap)]})
    require(safe(p, speeds, d), 'Repair core safety')
    require(phase(17, p) == phase(17, a) == d, 'Core equality was lost')
    w, R = b-a, upper['tail_from']
    require(w == F(upper['width']) == F(27, 1615) and R == 12, 'Width/tail')
    q = 2*d/w
    require((q.numerator+q.denominator-1)//q.denominator == R, 'Tail ceiling')
    require(2*d/R < w, 'Tail gap is not shorter than interval')
    finite = [r for r in range(1, R) if r not in speeds]
    require([x['r'] for x in upper['finite_witnesses']] == finite, 'Finite completeness')
    witnesses = []
    for row in upper['finite_witnesses']:
        r, t = row['r'], F(row['time'])
        require(t == p if r in upper['exceptions'] else t == a, 'Finite rule')
        require(safe(t, speeds+[r], d), 'Finite physical witness')
        witnesses.append({'r': r, 'time': str(t), 'added_phase': str(phase(r, t))})
    require(upper['exceptions'] == [4, 8], 'Exception scope')
    for r, m in ((4, 1), (8, 2)):
        require((m-d)/r < a <= b < (m+d)/r, 'Leader exception')

    # One complete denominator residue period above the tail threshold checks
    # all reachable branches. The proof of all-r validity is the displacement
    # inequality in ARGUMENT.md, not this bounded implementation check.
    branches = Counter()
    boundary_hits = Counter()
    tail_controls = []
    for seed in range(R, R+a.denominator):
        r = seed
        while r in speeds:
            r += a.denominator
        t, branch = tail_time(r, a, d)
        require(a <= t <= b and safe(t, speeds+[r], d), 'Tail physical witness')
        require(0 <= t-a < 2*d/r <= 2*d/R < w, 'Tail displacement')
        if phase(r, a) in (d, 1-d):
            require(t == a, 'Safe boundary unnecessarily discarded')
            boundary_hits[str(phase(r, a))] += 1
        branches[branch] += 1
        tail_controls.append({'r': r, 'branch': branch, 'time': str(t),
                              'added_phase': str(phase(r, t))})
    require(set(branches) == {'already_safe', 'below_safe_band', 'above_safe_band'},
            'Recovery branch unexercised')
    require(set(boundary_hits) == {str(d), str(1-d)}, 'Equality branch unexercised')

    checks = cert['semantic_checks']
    r = checks['fixed_endpoint_failure_speed']
    require(r not in speeds and phase(r, a) == phase(r, p) == 0, 'Fixed-time failure')
    t, _ = tail_time(r, a, d)
    require(t == F(checks['tail_example_time']) == F(411, 1700), 'Moving-contact example')
    require(not safe(p, [checks['repair_only_failure_speed']], d), 'Point-only failure')
    require(checks['interval_only_failure_speed'] == 4, 'Interval-only countercheck')
    return {
        'status': 'PASS', 'claim_status': 'same-author proof candidate; independent review pending',
        'kind': 'retrospective explanation check; not held-out validation',
        'source_commit': cert['source_commit'], 'source_sha256': cert['sources'],
        'artifact_sha256': {name: digest(HERE/name) for name in
                            ('ARGUMENT.md', 'CERTIFICATE.json', 'verify.py')},
        'counts': {'core_components': len(core), 'half_components': len(half),
                   'threshold_events': events, 'strict_blockers': len(blockers),
                   'core_interval_bands': len(bands), 'finite_witnesses': len(witnesses),
                   'tail_control_speeds': len(tail_controls)},
        'core_interval_bands': bands, 'repair_phases': [str(phase(v, p)) for v in speeds],
        'blockers': sorted(blockers, key=lambda row: row['component']),
        'finite_witnesses': witnesses, 'tail_branches': dict(sorted(branches.items())),
        'tail_equality_hits': dict(sorted(boundary_hits.items())),
        'tail_control_witnesses': tail_controls,
        'tail_width_margin_at_12': str(w-2*d/R),
        'fixed_endpoint_failure': {'r': r, 'endpoint_phases': ['0', '0'],
                                   'recovered_time': str(t), 'added_phase': str(phase(r, t))},
        'minimum_candidate': 2,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(verify(), indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')
