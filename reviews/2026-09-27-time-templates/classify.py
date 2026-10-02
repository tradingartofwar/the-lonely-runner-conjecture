"""Exact fixed-time residue classification, using only circle inequalities.

All 120 coefficient classes; no allowed-time reconstruction or template search.
The two symmetric time pairs have equal unchanged caps. Triangle inequality
proves their all-phase margins; exact equality phases certify sharpness.
--write creates classification.json; default/--check replays read-only.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'classification.json'
PROTOCOL_HASH = '0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02'
PERIOD = 120
THRESHOLD = F(1, 8)
EXCLUDED = [1, 4, 5, 6, 7, 11]
UNCHANGED_FIXED = [1, 4, 5, 6, 7]
STATUSES = ['strict', 'threshold', 'failure']


def distance(x):
    r = x % 1
    return min(r, 1 - r)


def status(margin):
    return 'strict' if margin > THRESHOLD else ('threshold' if margin == THRESHOLD else 'failure')


def template_metadata(template):
    times = list(map(F, template['times']))
    assert len(times) == 2 and times[0] + times[1] == 1
    phases = [(11 * t) % 1 for t in times]
    signed_arc = (phases[1] - phases[0]) % 1
    if signed_arc > F(1, 2):
        signed_arc -= 1
    separation = abs(signed_arc)
    half = separation / 2
    equality_phase = -(phases[0] + signed_arc / 2) % 1
    assert distance(phases[0] + equality_phase) == distance(phases[1] + equality_phase) == half
    return {'id': template['id'], 'times': list(map(str, times)), 'selected_speed': 11,
            'selected_phases': list(map(str, phases)), 'circular_separation': str(separation),
            'half_separation': str(half), 'half_separation_attained_at_theta': str(equality_phase)}


def classify_pair(V, residue, metadata):
    times = list(map(F, metadata['times']))
    vectors = [[distance(v * t) for v in [*UNCHANGED_FIXED, V]] for t in times]
    residue_vectors = [[distance(v * t) for v in [*UNCHANGED_FIXED, residue]] for t in times]
    assert vectors == residue_vectors  # V and residue differ by a multiple of both denominators.
    assert vectors[0] == vectors[1]  # d(v(1-t),Z)=d(vt,Z), for integer v.
    cap = min(vectors[0])
    half = F(metadata['half_separation'])
    minimum, maximum = min(cap, half), cap
    phases = list(map(F, metadata['selected_phases']))
    def full_pair_margin(theta):
        return max(min(cap, distance(a + theta)) for a in phases)
    # The circle triangle inequality proves the lower bound for every theta;
    # this explicit equality phase establishes that the minimum is attained.
    assert full_pair_margin(F(metadata['half_separation_attained_at_theta'])) == minimum
    # Translate the first selected phase to1/2 to attain the unchanged cap.
    assert full_pair_margin(F(1, 2) - phases[0]) == maximum
    constant = cap <= half
    assert constant == (minimum == maximum)
    return {'unchanged_distance_vectors': [list(map(str, vector)) for vector in vectors],
            'unchanged_cap': str(cap), 'minimum_best_margin': str(minimum),
            'maximum_best_margin': str(maximum), 'constant_in_phase': constant, 'status': status(minimum)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raw = (HERE / 'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH, 'Frozen protocol changed'
    protocol = json.loads(raw)
    assert protocol['classification']['residues'] == list(range(PERIOD))
    assert protocol['family']['selected_shifted_speed'] == 11
    templates = [template_metadata(t) for t in protocol['fixed_templates']]
    assert lcm(*(F(t).denominator for meta in templates for t in meta['times'])) == PERIOD
    rows, digest = [], sha256()
    for residue in range(PERIOD):
        V = PERIOD if residue == 0 else (residue + PERIOD if residue in EXCLUDED else residue)
        assert V > 0 and V not in EXCLUDED and V % PERIOD == residue
        assert not (V - PERIOD > 0 and V - PERIOD not in EXCLUDED)
        pairs = {meta['id']: classify_pair(V, residue, meta) for meta in templates}
        assert all(pair['constant_in_phase'] for pair in pairs.values()), 'Union reduction requires proven constancy'
        margin = max(F(pair['minimum_best_margin']) for pair in pairs.values())
        union = {'minimum_best_margin': str(margin), 'maximum_best_margin': str(margin),
                 'constant_in_phase': True, 'status': status(margin)}
        row = {'residue': residue, 'least_admissible_V': V, 'templates': pairs, 'union': union}
        rows.append(row)
        digest.update((json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode())
    counts = {}
    for meta in templates:
        counter = Counter(r['templates'][meta['id']]['status'] for r in rows)
        counts[meta['id']] = {s: counter[s] for s in STATUSES}
    union_counts = Counter(r['union']['status'] for r in rows)
    failed = [r['residue'] for r in rows if r['union']['status'] == 'failure']
    representatives = [{'residue': r['residue'], 'V': r['least_admissible_V']}
                       for r in rows if r['union']['status'] == 'failure']
    result = {
        'schema_version': 1,
        'status': 'OBSERVED exact120-class calculation; supplied all-integer residue argument is a proof candidate; no novelty claim',
        'protocol_sha256': PROTOCOL_HASH, 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'period': PERIOD, 'threshold': str(THRESHOLD), 'excluded_V': EXCLUDED,
        'unchanged_runner_indices': [1, 2, 3, 4, 5, 7],
        'templates': templates, 'residue_rows': rows, 'residue_rows_sha256': digest.hexdigest(),
        'summary': {'residue_count': PERIOD, 'templates': counts,
                    'union': {s: union_counts[s] for s in STATUSES},
                    'all_pair_margins_constant': all(p['constant_in_phase'] for r in rows for p in r['templates'].values())},
        'failed_residue_classes': failed, 'failure_representatives': representatives,
    }
    if args.write:
        OUT.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    else:
        assert result == json.loads(OUT.read_text()), 'Archive drift'
    print(json.dumps(result['summary'], sort_keys=True))
    print('Failed residues:', failed, 'least admissible representatives:', representatives)
    print('PASS: all120 fixed coefficient classes, exact substitutions, circle triangle certificates '
          'and constant four-time envelopes; ' + ('written' if args.write else 'replayed read-only'))


if __name__ == '__main__':
    main()
