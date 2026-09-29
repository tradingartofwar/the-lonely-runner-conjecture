"""Narrow witness/equality audit, declared before execution on 2026-09-29.

Scope: the E/C affine charts symbolically over their complete stated error
intervals; the q=4 threshold-1/8 safe set by direct closed-band intersection.
No other physical q input, ambient reconstruction, optimum scan, or new family.
Only standard-library exact rational arithmetic; no original checker imports.
"""
from fractions import Fraction as F
from pathlib import Path
import json

OUT = Path(__file__).with_suffix('.json')
ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))


def affine_value(pair, e):
    return pair[0] + pair[1] * e


charts = (
    ('E', (F(1, 3), -2), (F(5, 6), 1), F(1, 42),
     (0, 0, 1, 1, 1, 2, 3),
     ((F(1, 3), -2), (F(5, 6), 1), (F(1, 6), -1),
      (F(1, 2), -3), (F(5, 6), -5), (F(2, 3), -4),
      (F(1, 3), -8))),
    ('C', (F(1, 2), -3), (F(1, 6), 5), F(1, 24),
     (0, 0, 0, 1, 1, 1, 2),
     ((F(1, 2), -3), (F(1, 6), 5), (F(2, 3), 2),
      (F(1, 6), -1), (F(2, 3), -4), (F(5, 6), 1),
      (F(5, 6), -5))),
)
chart_records = []
for name, x, y, end, labels, stated_phases in charts:
    phases = tuple((a*x[0] + b*y[0] - m, a*x[1] + b*y[1])
                   for (a, b), m in zip(ROWS, labels))
    assert phases == stated_phases
    records = []
    for phase in phases:
        # z = 1/6-e, 1-z = 5/6+e.
        lower = (phase[0] - F(1, 6), phase[1] + 1)
        upper = (F(5, 6) - phase[0], 1 - phase[1])
        endpoints = [(affine_value(lower, e), affine_value(upper, e))
                     for e in (F(0), end)]
        assert all(min(pair) >= 0 for pair in endpoints)
        records.append(dict(phase=phase, lower_slack=lower,
                            upper_slack=upper, endpoint_slacks=endpoints))
    assert any(r['lower_slack'] == (0, 0) for r in records)
    assert any(r['upper_slack'] == (0, 0) for r in records)
    chart_records.append(dict(chart=name, error_interval=(F(0), end),
                              phases=records))

# The finite family member q=4 only. Each speed's closed safe bands cover
# exactly {t in [0,1] : ||v*t|| >= 1/8}; intersection therefore retains
# every isolated point as well as every positive component.
speeds = (1, 4, 5, 6, 7, 11, 13)
threshold = F(1, 8)
safe = [(F(0), F(1))]
stages = []
for speed in speeds:
    bands = [((lap + threshold)/speed,
              (lap + 1 - threshold)/speed) for lap in range(speed)]
    next_safe = set()
    for left, right in safe:
        for start, end in bands:
            lo, hi = max(left, start), min(right, end)
            if lo <= hi:
                next_safe.add((lo, hi))
    safe = sorted(next_safe)
    stages.append(dict(speed=speed, safe_components=safe))
expected = [(F(j, 8), F(j, 8)) for j in (1, 3, 5, 7)]
assert safe == expected
physical_records = []
for t, _ in safe:
    laps = tuple((v*t).numerator // (v*t).denominator for v in speeds)
    phases = tuple(v*t-lap for v, lap in zip(speeds, laps))
    assert min(min(p, 1-p) for p in phases) == threshold
    physical_records.append(dict(time=t, physical_laps=laps, phases=phases))


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


record = dict(scope='Two affine charts and q=4 threshold-safe-set only',
              affine_charts=chart_records, q4_intersection_stages=stages,
              q4_physical_witnesses=physical_records)
OUT.write_text(json.dumps(encode(record), indent=2) + '\n')
print('PASS: E/C affine identities and 56 endpoint inequalities; '
      'q=4 complete safe set is {1/8,3/8,5/8,7/8}.')
