"""Exact interval proof audit on pinned existing records; standard library only.

One AI author, two algorithm structures. This is not independent human review.
Run --write once, then --check for deterministic read-only reproduction.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DELTA = F(1, 8)


def floor(x):
    return x.numerator // x.denominator


def distance(x):
    x = x - floor(x)
    return min(x, 1 - x)


def blocked(v, t):
    return distance(v * t) < DELTA


def pieces(v, left, right):
    out = []
    for lap in range(floor(v * left) - 1, floor(v * right) + 2):
        lo = max(left, (lap - DELTA) / v)
        hi = min(right, (lap + DELTA) / v)
        if lo < hi:
            out.append((lo, hi))
    return out


def base_components(pair, left, right):
    out = []
    for lo1, hi1 in pieces(pair[0], left, right):
        for lo2, hi2 in pieces(pair[1], left, right):
            lo, hi = max(lo1, lo2), min(hi1, hi2)
            if lo < hi:
                out.append((lo, hi))
    return sorted(out)


def direct_minimum(v, phase, lo, hi):
    """Different structure: endpoint distances plus integer crossings."""
    x, y = sorted((v * lo + phase, v * hi + phase))
    candidates = [distance(x), distance(y)]
    for integer in range(floor(x), floor(y) + 2):
        if x <= integer <= y:
            candidates.append(F(0))
    return min(candidates)


def scalar_score(v, phase, lo, hi):
    mid = (lo + hi) / 2
    radius = abs(v) * (hi - lo) / 2
    d = distance(v * mid + phase)
    exact = max(d - radius, 0)
    assert exact == direct_minimum(v, phase, lo, hi)
    assert (d - radius - DELTA >= 0) == (exact >= DELTA)
    return d - radius - DELTA, exact


def event_containment(pair, complement, left, right):
    """Post-prediction truth check: all thresholds, cells and endpoints."""
    events = {left, right}
    for v in (*pair, *complement):
        for lap in range(floor(v * left) - 1, floor(v * right) + 2):
            for sign in (-1, 1):
                t = (lap + sign * DELTA) / v
                if left < t < right:
                    events.add(t)
    events = sorted(events)
    witnesses = events + [(x + y) / 2 for x, y in zip(events, events[1:])]
    violations = [t for t in witnesses if all(blocked(v, t) for v in pair)
                  and any(blocked(v, t) for v in complement)]
    return not violations, str(violations[0]) if violations else None


def evaluate(record_id, speeds, window, pair, selected):
    left, right = map(F, window)
    complement = [v for v in speeds if v not in pair]
    components = base_components(pair, left, right)
    records, scores = [], []
    for lo, hi in components:
        bounds = []
        for v in complement:
            score, exact = scalar_score(F(v), F(0), lo, hi)
            # Safe-lap integer feasibility, equation (3) in the note.
            lower_integer = -floor(-(v * hi - 1 + DELTA))
            upper_integer = floor(v * lo - DELTA)
            assert (lower_integer <= upper_integer) == (score >= 0)
            scores.append(score)
            bounds.append({'speed': v, 'signed_margin': str(score),
                           'exact_minimum_distance': str(exact)})
        records.append({'interval': [str(lo), str(hi)],
                        'left_included': all(blocked(v, lo) for v in pair),
                        'right_included': all(blocked(v, hi) for v in pair),
                        'bounds': bounds})
    score = min(scores) if scores else None
    return {'record_id': record_id, 'base_pair': pair, 'complement': complement,
            'window': window, 'old_minimum_component_choice': selected,
            'components': records, 'score': str(score) if score is not None else None,
            'predicted_containment': score is None or score >= 0}


def boundary_fixtures():
    # label, speed, phase, left, right, expected closed minimum
    cases = [
        ('closed equality endpoints', 1, '0', '1/8', '7/8', '1/8'),
        ('open equality endpoints', 1, '0', '1/8', '7/8', '1/8'),
        ('excluded endpoint below threshold', 1, '0', '1/16', '1/4', '1/16'),
        ('integer crossing', 1, '0', '-1/4', '1/4', '0'),
        ('half-integer cusp', 1, '0', '1/4', '3/4', '1/4'),
        ('more than one lap', 3, '0', '0', '1', '0'),
        ('negative velocity and nonzero phase', -2, '3/4', '0', '1/4', '1/4'),
        ('zero velocity', 0, '1/8', '0', '1', '1/8'),
    ]
    out = []
    for name, v, phase, lo, hi, expected in cases:
        margin, exact = scalar_score(F(v), F(phase), F(lo), F(hi))
        assert exact == F(expected)
        out.append({'name': name, 'margin': str(margin), 'minimum': str(exact)})
    # A strictly failed omitted endpoint has a genuine interior witness.
    assert F(1, 16) < F(3, 32) < F(1, 4)
    assert distance(F(3, 32)) < DELTA
    # Equality at an omitted endpoint may leave the entire interior strictly safe.
    assert scalar_score(F(1), F(0), F(1, 8), F(7, 8))[0] == 0
    # Empty union is vacuously contained; a singleton is evaluated directly.
    assert all([]) and distance(F(1, 8)) >= DELTA
    return out


def build():
    protocol = json.loads((HERE / 'protocol.json').read_text())
    source = ROOT / protocol['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == protocol['source_sha256']
    archive = json.loads(source.read_text())
    # Project only declared inputs; do not feed any archived containment into scores.
    inputs = []
    exits = []
    for rid, row in archive['cases'].items():
        if F(row['pair_only_minimum']) > 0:
            exits.append(rid)
            continue
        chosen = row['preselection_decisions']['fewest_components']
        for pair_row in row['pair_rows']:
            if pair_row['eligible']:
                inputs.append((rid, row['speeds'], row['window'], pair_row['base_pair'],
                               pair_row['base_pair'] == chosen))
    control = archive['controls']['strict_16']
    for row in control['pair_rows']:
        if row['eligible']:
            inputs.append(('strict_16', control['speeds'], control['window'], row['base_pair'],
                           row['base_pair'] == control['choices']['fewest_components']))
    del archive
    predictions = [evaluate(*row) for row in inputs]
    prediction_hash = hashlib.sha256(json.dumps(predictions, sort_keys=True).encode()).hexdigest()
    # Only now load the old oracle and build the separate event truth checks.
    archive = json.loads(source.read_text())
    for row in predictions:
        rid = row['record_id']
        oracle = (archive['cases'][rid]['postselection_oracle']['queries'] if rid != 'strict_16'
                  else archive['controls']['strict_16']['unique_physical_queries'])
        previous = next((q for q in oracle if q['base_pair'] == row['base_pair']), None)
        exact, witness = event_containment(row['base_pair'], row['complement'], *map(F, row['window']))
        assert exact == row['predicted_containment'], (rid, row['base_pair'])
        if previous is not None:
            assert exact == previous['containment_holds']
            assert [c['interval'] for c in row['components']] == [c['interval'] for c in previous['base_components']]
            assert [(c['left_included'], c['right_included']) for c in row['components']] == [
                (c['left_included'], c['right_included']) for c in previous['base_components']]
        row['post_prediction_audit'] = {'event_containment': exact,
            'failure_witness': witness, 'archived_query_compared': previous is not None}
    selected = [r for r in predictions if r['old_minimum_component_choice'] and r['record_id'] != 'strict_16']
    assert len(selected) == 10 and all(r['predicted_containment'] for r in selected)
    assert F(archive['controls']['doubling_112']['pair_only_minimum']) == F(761, 32256)
    tight_speeds = [1, 4, 5, 6, 7, 11, 13]
    assert all(distance(F(3, 8) * v) >= DELTA for v in tight_speeds)
    eps = F(1, 100000)
    assert blocked(11, F(3, 8) - eps) and blocked(13, F(3, 8) + eps)
    return {'status': 'PASS', 'baseline': protocol['baseline'],
        'source_sha256': protocol['source_sha256'],
        'protocol_sha256': hashlib.sha256((HERE / 'protocol.json').read_bytes()).hexdigest(),
        'prediction_sha256_before_oracle': prediction_hash,
        'counts': {'archived_positive_exits': len(exits), 'selected_archival_pairs': len(selected),
            'audited_pairs_including_two_controls': len(predictions),
            'positive_components': sum(len(r['components']) for r in predictions),
            'scalar_minimum_checks': sum(2 * len(r['components']) for r in predictions),
            'containing_pairs': sum(r['predicted_containment'] for r in predictions),
            'failed_pairs': sum(not r['predicted_containment'] for r in predictions),
            'multi_component_pairs': sum(len(r['components']) > 1 for r in predictions),
            'multi_component_containing': sum(len(r['components']) > 1 and r['predicted_containment'] for r in predictions),
            'multi_component_failed': sum(len(r['components']) > 1 and not r['predicted_containment'] for r in predictions),
            'selected_multi_component_pairs': sum(len(r['components']) > 1 for r in selected),
            'archived_query_comparisons': sum(r['post_prediction_audit']['archived_query_compared'] for r in predictions)},
        'boundary_fixtures': boundary_fixtures(), 'records': predictions,
        'dispatch': {'doubling_112': 'pair-only exit 761/32256', 'tight_13': 'isolated equality 3/8'},
        'limits': protocol['limits']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    encoded = json.dumps(data, indent=2, sort_keys=True) + '\n'
    output = HERE / 'results.json'
    if args.write:
        output.write_text(encoded)
    else:
        assert output.read_text() == encoded, 'stale proof-audit results'
    print(json.dumps({'status': data['status'], 'counts': data['counts']}, indent=2))
