"""Independent exact envelopes for the frozen two-template classification.

No primary classify implementation is read or imported. Circle-distance
corners, cap crossings and all affine-line intersections form a complete
algebraic partition for the best available full margin. Exact branch checks
certify every phase, rather than inferring a continuum from sampled phases.
--write records the comparison; default/--check replays read-only.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = '0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02'
FIXED_SPEEDS = (1, 4, 5, 6, 7)
EXCLUDED = {1, 4, 5, 6, 7, 11}
DELTA = Q(1, 8)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def near(value):
    phase = value % 1
    return min(phase, 1-phase)


def clipped_line(beta, cap, theta):
    phase = (theta+beta) % 1
    distance = min(phase, 1-phase)
    if distance >= cap:
        return Q(0), cap
    slope = Q(1) if phase < Q(1, 2) else Q(-1)
    return slope, distance-slope*theta


def exact_envelope(betas, caps):
    """Partition all clipped distance kinks and every envelope crossing."""
    base = {Q(0), Q(1)}
    for beta, cap in zip(betas, caps):
        assert 0 <= beta < 1 and 0 <= cap <= Q(1, 2)
        for phase in (Q(0), Q(1, 2), cap, 1-cap):
            base.add((phase-beta) % 1)
    cuts = set(base)
    for a, b in zip(sorted(base), sorted(base)[1:]):
        mid = (a+b)/2
        lines = [clipped_line(beta, cap, mid) for beta, cap in zip(betas, caps)]
        for (slope, intercept), (other_slope, other_intercept) in combinations(lines, 2):
            if slope != other_slope:
                root = (other_intercept-intercept)/(slope-other_slope)
                if a < root < b:
                    cuts.add(root)
    cuts = sorted(cuts)
    values = {theta: max(min(cap, near(theta+beta)) for beta, cap in zip(betas, caps))
              for theta in cuts}
    cells = []
    for a, b in zip(cuts, cuts[1:]):
        mid = (a+b)/2
        lines = [clipped_line(beta, cap, mid) for beta, cap in zip(betas, caps)]
        # No branch line changes and no nonidentical line crossing can occur
        # in this open cell; hence the midpoint winner wins throughout it.
        for (slope, intercept), (other_slope, other_intercept) in combinations(lines, 2):
            if slope != other_slope:
                root = (other_intercept-intercept)/(slope-other_slope)
                assert not a < root < b
        winner = max(range(len(lines)), key=lambda i: (lines[i][0]*mid+lines[i][1], -i))
        slope, intercept = lines[winner]
        assert values[a] == slope*a+intercept and values[b] == slope*b+intercept
        for i, (beta, cap) in enumerate(zip(betas, caps)):
            assert min(cap, near(mid+beta)) == lines[i][0]*mid+lines[i][1]
            assert min(cap, near(a+beta)) == lines[i][0]*a+lines[i][1]
            assert min(cap, near(b+beta)) == lines[i][0]*b+lines[i][1]
        cells.append(dict(left=a, right=b, slope=slope, intercept=intercept, winner=winner))
    minimum, maximum = min(values.values()), max(values.values())
    constant = minimum == maximum
    if constant:
        assert all(cell['slope'] == 0 and cell['intercept'] == minimum for cell in cells)
        assert all(value == minimum for value in values.values())
    return dict(cuts=cuts, values=values, cells=cells, minimum=minimum, maximum=maximum,
                constant=constant)


def safe_phase_cover(betas, caps, target):
    """Independent closed-arc coverage check for a proposed uniform margin."""
    arcs = []
    for beta, cap in zip(betas, caps):
        if cap < target:
            continue
        if target == 0:
            arcs.append((Q(0), Q(1)))
            continue
        for lap in range(2):
            left, right = lap+target-beta, lap+1-target-beta
            a, b = max(Q(0), left), min(Q(1), right)
            if a <= b:
                arcs.append((a, b))
    merged = []
    for a, b in sorted(arcs):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged == [(Q(0), Q(1))]


def evaluate_residue(residue, templates):
    records = []
    combined_betas, combined_caps = [], []
    for template in templates:
        times = list(map(Q, template['times']))
        vectors = [[near(speed*time) for speed in (*FIXED_SPEEDS, residue)] for time in times]
        caps = list(map(min, vectors))
        betas = [(11*time) % 1 for time in times]
        envelope = exact_envelope(betas, caps)
        raw = exact_envelope(betas, [Q(1, 2)]*2)
        separation = near(betas[1]-betas[0])
        assert raw['minimum'] == separation/2
        assert safe_phase_cover(betas, caps, envelope['minimum'])
        assert safe_phase_cover(betas, caps, DELTA) == (envelope['minimum'] >= DELTA)
        assert vectors[0] == vectors[1] and caps[0] == caps[1]
        assert envelope['constant'] and envelope['minimum'] == caps[0]
        records.append(dict(template_id=template['id'], times=times, vectors=vectors, caps=caps,
                            betas=betas, phase_separation=separation, raw=raw, envelope=envelope))
        combined_betas.extend(betas)
        combined_caps.extend(caps)
    envelope = exact_envelope(combined_betas, combined_caps)
    assert envelope['constant']
    assert envelope['minimum'] == max(r['envelope']['minimum'] for r in records)
    assert safe_phase_cover(combined_betas, combined_caps, DELTA) == (envelope['minimum'] >= DELTA)
    return dict(residue=residue, templates=records, union=envelope)


def least_admissible(residue):
    candidate = residue if residue > 0 else 120
    while candidate in EXCLUDED:
        candidate += 120
    assert candidate > 0 and candidate not in EXCLUDED and candidate % 120 == residue
    return candidate


def assert_fields(expected, actual, label):
    for field, value in expected.items():
        assert field in actual, (label, 'missing', field)
        assert actual[field] == value, (label, field, 'computed', value, 'archived', actual[field])


def status(margin):
    return 'strict' if margin > DELTA else ('threshold' if margin == DELTA else 'failure')


def encode_envelope(envelope):
    return dict(event_points=[[str(theta), str(envelope['values'][theta])] for theta in envelope['cuts']],
                open_cells=[[str(cell['left']), str(cell['right']), str(cell['slope']),
                             str(cell['intercept']), cell['winner']] for cell in envelope['cells']])


def expected_row(record):
    residue = record['residue']
    representative = least_admissible(residue)
    templates = {}
    for template in record['templates']:
        vectors = [[near(speed*time) for speed in (*FIXED_SPEEDS, representative)]
                   for time in template['times']]
        assert vectors == template['vectors']
        envelope = template['envelope']
        templates[template['template_id']] = dict(
            unchanged_distance_vectors=[list(map(str, vector)) for vector in vectors],
            unchanged_cap=str(template['caps'][0]),
            minimum_best_margin=str(envelope['minimum']),
            maximum_best_margin=str(envelope['maximum']),
            constant_in_phase=envelope['constant'], status=status(envelope['minimum']))
    envelope = record['union']
    return dict(residue=residue, least_admissible_V=representative, templates=templates,
                union=dict(minimum_best_margin=str(envelope['minimum']),
                           maximum_best_margin=str(envelope['maximum']),
                           constant_in_phase=envelope['constant'], status=status(envelope['minimum'])))


def template_metadata(templates, records):
    result = []
    for index, template in enumerate(templates):
        calculation = records[0]['templates'][index]
        raw = calculation['raw']
        minimizers = [theta for theta in raw['cuts'][:-1] if raw['values'][theta] == raw['minimum']]
        assert len(minimizers) == 1
        attaining = minimizers[0]
        assert max(near(attaining+beta) for beta in calculation['betas']) == calculation['phase_separation']/2
        result.append(dict(id=template['id'], times=template['times'], selected_speed=11,
                           selected_phases=list(map(str, calculation['betas'])),
                           circular_separation=str(calculation['phase_separation']),
                           half_separation=str(calculation['raw']['minimum']),
                           half_separation_attained_at_theta=str(attaining)))
    return result


def summary(rows, templates):
    def counts(values):
        return {key: values.count(key) for key in ('strict', 'threshold', 'failure')}
    return dict(residue_count=len(rows),
                templates={template['id']: counts([row['templates'][template['id']]['status'] for row in rows])
                           for template in templates},
                union=counts([row['union']['status'] for row in rows]),
                all_pair_margins_constant=all(row['templates'][template['id']]['constant_in_phase']
                                              for row in rows for template in templates))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = (HERE/'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_SHA256
    protocol = json.loads(raw)
    assert protocol['classification']['residues'] == list(range(120))
    templates = protocol['fixed_templates']
    assert [t['times'] for t in templates] == [['1/8', '7/8'], ['7/15', '8/15']]
    for template in templates:
        for time in map(Q, template['times']):
            assert (120*time).denominator == 1
    records = [evaluate_residue(residue, templates) for residue in range(120)]
    failed = [row['residue'] for row in records if row['union']['minimum'] < DELTA]
    source_bytes = (HERE/'classification.json').read_bytes()
    source = json.loads(source_bytes)
    assert source['schema_version'] == 1 and source['protocol_sha256'] == PROTOCOL_SHA256
    rows = [expected_row(record) for record in records]
    stream = sha256()
    for row in rows:
        stream.update((canonical(row)+'\n').encode())
    expected_summary = summary(rows, templates)
    expected = dict(period=120, threshold='1/8', excluded_V=sorted(EXCLUDED),
                    unchanged_runner_indices=[1, 2, 3, 4, 5, 7],
                    templates=template_metadata(templates, records),
                    residue_rows=rows, residue_rows_sha256=stream.hexdigest(),
                    summary=expected_summary, failed_residue_classes=failed,
                    failure_representatives=[dict(residue=residue, V=least_admissible(residue)) for residue in failed])
    assert_fields(expected, source, 'classification')
    verification_rows = []
    for record in records:
        envelopes = {template['template_id']: template['envelope'] for template in record['templates']}
        envelopes['union_of_four_times'] = record['union']
        verification_rows.append(dict(residue=record['residue'],
                                      envelopes={name: dict(minimum=str(envelope['minimum']),
                                                            maximum=str(envelope['maximum']),
                                                            constant_in_phase=envelope['constant'],
                                                            event_point_count=len(envelope['cuts']),
                                                            open_cell_count=len(envelope['cells']),
                                                            exact_envelope_sha256=digest(encode_envelope(envelope)))
                                                 for name, envelope in envelopes.items()}))
    out = dict(status='REPRODUCED all120 fixed-time residue classes with an exact phase-envelope and sufficient-period certificate',
               protocol_sha256=PROTOCOL_SHA256, source_classification_sha256=sha256(source_bytes).hexdigest(),
               primary_script_sha256=source['script_sha256'],
               verifier_script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
               residue_rows_sha256=stream.hexdigest(),
               residue_classes=120, fixed_times=['1/8', '7/8', '7/15', '8/15'],
               pair_envelopes_verified=240, union_envelopes_verified=120,
               open_phase_cells_checked=sum(envelope['open_cell_count']
                                            for row in verification_rows for envelope in row['envelopes'].values()),
               phase_event_points_checked=sum(envelope['event_point_count']
                                              for row in verification_rows for envelope in row['envelopes'].values()),
               methods=['direct exact unchanged-distance vectors at all four prescribed times',
                        'full clipped circle-distance envelopes with kink, cap, and crossing events',
                        'closed safe-phase arc coverage at the computed uniform margin and1/8',
                        'direct admissible-representative substitutions and period120 divisibility',
                        'full primary residue-row equality and canonical stream digest'],
               continuum_and_period_argument=[
                   'The full margin at one fixed time is min(c,||theta+beta||). Its only slope kinks occur at phase0,phase1/2,or a crossing of the distance with cap c; all are enumerated exactly.',
                   'On each resulting cell every single-time margin is affine. All pairwise affine crossing roots in that cell are added; no order change can remain within a final open cell.',
                   'The winning affine function is therefore the exact maximum throughout each final cell. Every cell and all endpoint values are checked. All240 pair envelopes and120 four-time envelopes have slope0 and identical endpoint values, certifying constancy for every theta.',
                   'An independent union of closed safe-phase arcs verifies that each computed margin is attained or exceeded at every theta, including equality at the1/8 threshold.',
                   'For each of the four prescribed times,120*t is an integer. Replacing V by V+120 adds an integer to V*t and leaves all unchanged distances unchanged. Speed11 phases and all other coefficients are fixed, so the complete theta envelopes and classification repeat for every admissible integer in each residue class.',
                   'The least positive admissible representative is obtained from the residue, replacing0 by120 and adding120 only when a fixed excluded speed is encountered. Failure here concerns only the four prescribed times; no complete allowed-time set or diagnostic search is performed.'],
               summary=expected_summary, failed_residue_classes=failed,
               failure_representatives=expected['failure_representatives'], cases=verification_rows)
    destination = HERE/'classification_verification.json'
    if args.write:
        destination.write_text(json.dumps(out, indent=2)+'\n')
    else:
        assert json.loads(destination.read_text()) == out
    print('PASS: all120 classes,240 pair envelopes,120 union envelopes and full row digest;',
          'saved' if args.write else 'read-only replay', flush=True)
    print('Failed classes:', failed, '; representatives:', list(map(least_admissible, failed)), flush=True)


if __name__ == '__main__':
    main()
