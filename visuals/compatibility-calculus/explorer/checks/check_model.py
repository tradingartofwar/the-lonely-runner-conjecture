#!/usr/bin/env python3
"""Physical-time countercheck of every enabled ray/q/form-count combination.

The browser model uses certified polytope edge-plane intersections. This checker
uses direct speed-distance arithmetic and closed safe-band intersections instead.
"""
import argparse
import hashlib
import itertools
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]


def safe_set(speeds, z):
    result = [(F(0), F(1))]
    for v in speeds:
        bands = [((m + z) / v, (m + 1 - z) / v) for m in range(v)]
        out, i, j = [], 0, 0
        while i < len(result) and j < len(bands):
            a, b = result[i]
            c, d = bands[j]
            if max(a, c) <= min(b, d):
                out.append((max(a, c), min(b, d)))
            if b < d:
                i += 1
            elif b > d:
                j += 1
            else:
                i += 1
                j += 1
        result = sorted(set(out))
    return result


def minimum(speeds, t):
    n, d = t.numerator, t.denominator
    return F(min(min(v*n % d, d-v*n % d) for v in speeds), d)


def optimize(speeds):
    # The lower envelope of nonzero tent slopes peaks at a tent top or an
    # opposing-slope contact. Enumerate those exact physical times, not samples.
    times = {F(0), F(1)}
    for v in speeds:
        times.update(F(2*m+1, 2*v) for m in range(v))
    for u, v in itertools.combinations(speeds, 2):
        times.update(F(m, u+v) for m in range(1, u+v))
    values = {t: minimum(speeds, t) for t in times}
    best = max(values.values())
    return best, sorted(t for t, value in values.items() if value == best)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    records = json.loads(subprocess.check_output(['node', str(HERE/'model_records.cjs')], text=True))
    assert len(records) == 236
    selected = []
    for record in records:
        ray, q, count = record['ray'], record['q'], record['count']
        speeds = ([1, q, q+1, q+2, q+3, 2*q+3, 2*q+5] if ray == 'A' else
                  [1, q, q+1, 2*q+1, 3*q+1, 3*q+2, 5*q+2])[:count]
        assert record['speeds'] == speeds
        best, times = optimize(speeds)
        assert F(record['maximum']) == best, (ray, q, count, 'maximum')
        assert list(map(F, record['times'])) == times, (ray, q, count, 'all maximizers')
        for z in ['1/8', '1/7', '1/6']:
            assert [tuple(map(F, p)) for p in record['safe'][z]] == safe_set(speeds, F(z)), (ray, q, count, z)
        w = record['witness']
        assert minimum(speeds, F(w['time'])) >= F(1, 8)
        x, y, z = map(F, w['point'])
        assert (q*x-y if ray == 'A' else x-q*y) == w['h']
        assert F(w['time']) == (x if ray == 'A' else y)
        if ray == 'B' and count == 7:
            assert F(record['capMaximum']) == best > F(1, 7)
        if q in ([3, 4, 5, 6, 10, 60] if ray == 'A' else [2, 3, 4, 5, 6, 7, 60]):
            selected.append(record)
    inputs = ['explorer/model.js', 'js/cc-core.js', 'data/cc_geometry.json',
              'data/cc_examples.json', 'explorer/checks/check_model.py', 'explorer/checks/model_records.cjs']
    report = {'status': 'PASS', 'systems': 236, 'closed_safe_sets': 708,
              'complete_optimizer_sets': 236, 'physical_witnesses': 236,
              'B_cap_to_full_atlas_comparisons': 59, 'q_range': [2, 60],
              'source_commit': json.loads((PACKAGE/'data/visual_manifest.json').read_text())['source_commit'],
              'input_sha256': {p: hashlib.sha256((PACKAGE/p).read_bytes()).hexdigest() for p in inputs},
              'limits': 'Finite scope, independently structured same-author checks; no all-q proof or new family.'}
    if args.write:
        (HERE/'model_check.json').write_text(json.dumps(report, indent=2) + '\n')
        (HERE/'expected_controls.json').write_text(json.dumps(selected, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
