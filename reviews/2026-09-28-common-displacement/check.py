"""Arithmetic candidate and separate threshold-state reconstruction on four old controls."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def floor(x):
    return x.numerator // x.denominator


def distance(x):
    q = x - floor(x)
    return min(q, 1 - q)


def candidate(speeds, t0, direction):
    n = len(speeds) + 1
    delta = F(1, n)
    assert t0.denominator <= n
    rows = []
    for v in speeds:
        phase = (v * t0) % 1
        assert phase == 0 or delta <= phase <= 1 - delta
        if phase == 0:
            entry, exit_ = delta / v, (1 - delta) / v
        else:
            entry = F(0)
            exit_ = ((1 - delta - phase) if direction == 1 else (phase - delta)) / v
        rows.append({'speed': v, 'phase': str(phase),
                     'entry': str(entry), 'exit': str(exit_)})
    entry = max(F(row['entry']) for row in rows)
    exit_ = min(F(row['exit']) for row in rows)
    times = sorted((t0 + direction * entry, t0 + direction * exit_))
    return {'anchor': str(t0), 'direction': direction, 'rows': rows,
            'entry': str(entry), 'exit': str(exit_), 'budget': str(exit_ - entry),
            'entry_controllers': [r['speed'] for r in rows if F(r['entry']) == entry],
            'exit_controllers': [r['speed'] for r in rows if F(r['exit']) == exit_],
            'result': 'positive_interval' if exit_ > entry else
                      'valid_instant' if exit_ == entry else 'failed_first_safe_bands',
            'time_interval': [str(t) for t in times] if entry <= exit_ else None}


def first_band_by_events(v, t0, direction, delta):
    """Sweep one full displacement lap; retain closed cells and singleton endpoints."""
    last = F(1, v)
    events = {F(0), last}
    center_lap = floor(v * t0)
    for lap in range(center_lap - 2, center_lap + 3):
        for phase in (delta, 1 - delta):
            s = direction * ((lap + phase) / v - t0)
            if 0 <= s <= last:
                events.add(s)
    events = sorted(events)
    intervals = [(s, s) for s in events if distance(v * (t0 + direction * s)) >= delta]
    for left, right in zip(events, events[1:]):
        if distance(v * (t0 + direction * (left + right) / 2)) >= delta:
            intervals.append((left, right))
    merged = []
    for left, right in sorted(intervals):
        if merged and left <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], right))
        else:
            merged.append((left, right))
    assert merged
    return merged[0]


def check_time_interval(speeds, left, right, delta):
    events = {left, right}
    for v in speeds:
        for lap in range(floor(v * left) - 1, floor(v * right) + 2):
            for phase in (delta, 1 - delta):
                t = (lap + phase) / v
                if left <= t <= right:
                    events.add(t)
    events = sorted(events)
    for t in events:
        assert all(distance(v * t) >= delta for v in speeds)
    for lo, hi in zip(events, events[1:]):
        assert all(distance(v * (lo + hi) / 2) > delta for v in speeds)
    return len(events), max(0, len(events) - 1)


def derive():
    protocol_bytes = (HERE / 'protocol.json').read_bytes()
    protocol = json.loads(protocol_bytes)
    predictions = {}
    for label, velocities in protocol['controls'].items():
        speeds = velocities[1:]
        assert len(velocities) == len(set(velocities)) == 8 and velocities[0] == 0
        predictions[label] = [
            candidate(speeds, F(t), direction)
            for t in protocol['anchors'] for direction in protocol['directions']]
    digest = hashlib.sha256(json.dumps(predictions, sort_keys=True).encode()).hexdigest()
    comparisons = 0
    events_checked = cells_checked = 0
    for label, rows in predictions.items():
        speeds = protocol['controls'][label][1:]
        delta = F(1, len(speeds) + 1)
        for row in rows:
            actual_bands = []
            for runner in row['rows']:
                band = first_band_by_events(runner['speed'], F(row['anchor']), row['direction'], delta)
                assert list(map(str, band)) == [runner['entry'], runner['exit']]
                actual_bands.append(band)
                comparisons += 1
            lo, hi = max(x[0] for x in actual_bands), min(x[1] for x in actual_bands)
            assert str(lo) == row['entry'] and str(hi) == row['exit']
            if lo <= hi:
                left, right = map(F, row['time_interval'])
                num_events, num_cells = check_time_interval(speeds, left, right, delta)
                events_checked += num_events
                cells_checked += num_cells
                row['midpoint_witness'] = str((left + right) / 2)
                row['minimum_at_midpoint'] = str(min(distance(v * (left + right) / 2) for v in speeds))
            else:
                slow = next(r for r in row['rows'] if F(r['entry']) == lo)
                early = next(r for r in row['rows'] if F(r['exit']) == hi)
                assert slow['speed'] != early['speed']
                row['conflict'] = {
                    'runner_not_yet_in_first_safe_band': slow['speed'],
                    'runner_already_left_current_safe_band': early['speed'],
                    'latest_entry': str(lo), 'earliest_exit': str(hi)}
    # The declared strict16 failure at the first anchor is not failed loneliness.
    old_witness = F(17, 56)
    assert all(distance(v * old_witness) >= F(1, 8)
               for v in protocol['controls']['strict_16'][1:])
    # The tight anchor is truly isolated, with opposite boundary controllers.
    eps = F(1, 1000000)
    assert distance(F(1, 8) - eps) < F(1, 8)
    assert distance(7 * (F(1, 8) + eps)) < F(1, 8)
    count = {key: sum(r['result'] == key for rows in predictions.values() for r in rows)
             for key in ['positive_interval', 'valid_instant', 'failed_first_safe_bands']}
    return {'status': 'PASS', 'baseline': protocol['baseline'],
        'protocol_sha256': hashlib.sha256(protocol_bytes).hexdigest(),
        'prediction_sha256_before_verification': digest,
        'counts': {'candidate_records': 16, 'individual_band_comparisons': comparisons,
                   'certificate_events_checked': events_checked, 'certificate_cells_checked': cells_checked,
                   **count},
        'records': predictions,
        'verification': 'One AI author; residue formula versus threshold-state sweep, exact fractions only.',
        'limits': protocol['scope_limits']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = derive()
    encoded = json.dumps(data, indent=2, sort_keys=True) + '\n'
    path = HERE / 'results.json'
    if args.write:
        path.write_text(encoded)
    else:
        assert path.read_text() == encoded, 'stale results'
    print(json.dumps(data['counts'], indent=2))
    for label, rows in data['records'].items():
        for row in rows:
            print(label, row['anchor'], row['direction'], row['result'],
                  row['budget'], row['time_interval'])
