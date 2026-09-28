"""Independent bounded missed-class diagnostic reconstruction.

No project imports and no reading/importing diagnose.py. Reconstruct A and
the common-start set from exact threshold vertices/open cells. Reconstruct
P and B by direct phase-preimage existence tests; do not compute a phase
multiplicity or duration profile. Default/--check is read-only; --write writes
only diagnostics_verification.json.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'protocol.json'
CLASSIFICATION = HERE / 'classification.json'
PRIMARY = HERE / 'diagnostics.json'
OUT = HERE / 'diagnostics_verification.json'
PROTOCOL_SHA = '0932c23c6c65dd8faaae4d319770ae0bca583237c0f92fee9c5ae7f8ce474f02'
D = F(1, 8)
PERIOD = 120
FORBIDDEN = {1, 4, 5, 6, 7, 11}
COUNTERS = dict(time_vertices=0, time_cells=0, phase_vertices=0, phase_cells=0)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def object_hash(obj):
    return sha256((json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()).hexdigest()


def distance(x):
    y = x % 1
    return min(y, 1-y)


def safe(speeds, t):
    return all(distance(v*t) >= D for v in speeds)


def merge_closed(pieces):
    result = []
    for a, b in sorted(pieces):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], b))
        else:
            result.append((a, b))
    return result


def time_set(speeds):
    events = {F(0), F(1)}
    for v in speeds:
        for m in range(v+1):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if 0 <= t <= 1:
                    events.add(t)
    events = sorted(events)
    vertices = {t: safe(speeds, t) for t in events}
    pieces = [(t, t) for t in events if vertices[t]]
    for a, b in zip(events, events[1:]):
        if safe(speeds, (a+b)/2):
            assert vertices[a] and vertices[b]
            pieces.append((a, b))
    COUNTERS['time_vertices'] += len(events)
    COUNTERS['time_cells'] += len(events)-1
    return merge_closed(pieces)


def encode_time(pieces):
    return [[str(a), str(b)] for a, b in pieces]


def total_length(pieces):
    return sum((b-a for a, b, *flags in pieces), F(0))


def merge_flagged(pieces):
    """Canonical union in the cut interval [0,1), retaining all point flags."""
    result = []
    for a, b, lc, rc in sorted(pieces):
        if a == b and not (lc and rc):
            continue
        if not result:
            result.append((a, b, lc, rc))
            continue
        x, y, xl, yr = result[-1]
        if a < y or a == y and (yr or lc):
            new_left = xl or lc if a == x else xl
            if b > y:
                result[-1] = (x, b, new_left, rc)
            elif b == y:
                result[-1] = (x, y, new_left, yr or rc)
            else:
                result[-1] = (x, y, new_left, yr)
        else:
            result.append((a, b, lc, rc))
    assert all(not (b == 1 and rc) for a, b, lc, rc in result)
    assert all(a != 1 for a, b, lc, rc in result)
    return result


def phase_from_states(events, point_states, cell_states):
    pieces = [(x, x, True, True) for x, occupied in zip(events, point_states) if occupied]
    endpoints = events+[F(1)]
    pieces += [(a, b, False, False) for a, b, occupied in
               zip(endpoints, endpoints[1:], cell_states) if occupied]
    return merge_flagged(pieces)


def phase_sets(unchanged, A):
    events = sorted({F(0)} | {11*t % 1 for a, b in A for t in (a, b)})
    def has_preimage(x):
        # The endpoint j=11 is included for completeness; speed1 makes t=1
        # unsafe here. Only existence is recorded, never multiplicity.
        return any(safe(unchanged, (j+x)/11)
                   for j in range(12) if 0 <= (j+x)/11 <= 1)
    points = [has_preimage(x) for x in events]
    endpoints = events+[F(1)]
    cells = [has_preimage((a+b)/2) for a, b in zip(endpoints, endpoints[1:])]
    # The image of compact A is closed on the circle.
    assert all(not cells[i] or points[i] and points[(i+1) % len(events)] for i in range(len(events)))
    P = phase_from_states(events, points, cells)
    bulk_points = [cells[i-1] or cells[i] for i in range(len(events))]
    B = phase_from_states(events, bulk_points, cells)
    extra = [x for x, p, b in zip(events, points, bulk_points) if p and not b]
    COUNTERS['phase_vertices'] += len(events)
    COUNTERS['phase_cells'] += len(cells)
    return P, B, extra


def encode_phase(pieces):
    return [[str(a), str(b), lc, rc] for a, b, lc, rc in pieces]


def metrics(pieces):
    if not pieces:
        return dict(nonempty=False, measure='0', maximum_circular_gap='1',
                    minimum_covering_arc_length='0', maximal_gap_arcs=[])
    gaps = []
    for index, piece in enumerate(pieces):
        start = piece[1]
        end = pieces[(index+1) % len(pieces)][0]
        length = end-start+(1 if index == len(pieces)-1 else 0)
        if length > 0:
            gaps.append((start % 1, end % 1, length))
    maximum = max((g[2] for g in gaps), default=F(0))
    return dict(nonempty=True, measure=str(total_length(pieces)),
                maximum_circular_gap=str(maximum),
                minimum_covering_arc_length=str(1-maximum),
                maximal_gap_arcs=[[str(a), str(b), str(g)] for a, b, g in sorted(gaps)
                                  if g == maximum])


def witness(speeds, pieces):
    positive = [(a, b) for a, b in pieces if a < b]
    if positive:
        a, b = min(positive, key=lambda p: (-(p[1]-p[0]), p[0]))
        t = (a+b)/2
    elif pieces:
        t = pieces[0][0]
    else:
        return None
    phases = [v*t % 1 for v in speeds]
    ds = [min(x, 1-x) for x in phases]
    assert min(ds) >= D
    assert not positive or min(ds) > D
    return dict(time=str(t), kind='strict' if min(ds) > D else 'equality',
                phases=list(map(str, phases)), distances=list(map(str, ds)),
                minimum_distance=str(min(ds)))


def reconstruct_case(residue, V):
    unchanged = [1, 4, 5, 6, 7, V]
    positive = [1, 4, 5, 6, 7, 11, V]
    A = time_set(unchanged)
    P, B, extra = phase_sets(unchanged, A)
    pm, bm = metrics(P), metrics(B)
    common = time_set(positive)
    common_length = total_length(common)
    data = dict(residue=residue, V=V, velocities=[0]+positive, unchanged_speeds=unchanged,
                A_components=encode_time(A), A_duration=str(total_length(A)),
                A_positive_component_count=sum(a < b for a, b in A),
                A_isolated_times=[str(a) for a, b in A if a == b],
                P_components=encode_phase(P), B_components=encode_phase(B),
                extra_isolated_projection_points=list(map(str, extra)),
                P_metrics=pm, B_metrics=bm,
                all_phase_decisions=dict(
                    nonempty_for_every_phase=pm['nonempty'] and F(pm['minimum_covering_arc_length']) >= 2*D,
                    positive_duration_for_every_phase=bm['nonempty'] and F(bm['minimum_covering_arc_length']) > 2*D,
                    nonempty_covering_margin=str(F(pm['minimum_covering_arc_length'])-2*D),
                    positive_duration_covering_margin=str(F(bm['minimum_covering_arc_length'])-2*D),
                    criterion_status='supplied covering criteria; general proof-candidate status retained'),
                common_start_components=encode_time(common),
                common_start_duration=str(common_length),
                common_start_positive_component_count=sum(a < b for a, b in common),
                common_start_isolated_times=[str(a) for a, b in common if a == b],
                common_start_status='strict' if common_length > 0 else 'contacts' if common else 'empty',
                common_start_witness=witness(positive, common))
    data['case_sha256'] = object_hash(data)
    return data


def totals(cases):
    return dict(cases=len(cases),
                A_components=sum(len(c['A_components']) for c in cases),
                A_positive_components=sum(c['A_positive_component_count'] for c in cases),
                A_isolated_times=sum(len(c['A_isolated_times']) for c in cases),
                common_start_components=sum(len(c['common_start_components']) for c in cases),
                common_start_positive_components=sum(c['common_start_positive_component_count'] for c in cases),
                common_start_isolated_times=sum(len(c['common_start_isolated_times']) for c in cases),
                all_phase_nonempty_cases=sum(c['all_phase_decisions']['nonempty_for_every_phase'] for c in cases),
                all_phase_positive_duration_cases=sum(c['all_phase_decisions']['positive_duration_for_every_phase'] for c in cases),
                common_start_strict_cases=sum(c['common_start_status'] == 'strict' for c in cases),
                common_start_contact_cases=sum(c['common_start_status'] == 'contacts' for c in cases),
                common_start_empty_cases=sum(c['common_start_status'] == 'empty' for c in cases))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assert file_hash(PROTOCOL) == PROTOCOL_SHA
    classification = json.loads(CLASSIFICATION.read_text())
    assert classification['protocol_sha256'] == PROTOCOL_SHA
    residues = classification['failed_residue_classes']
    assert residues == sorted(set(residues)) and all(0 <= r < PERIOD for r in residues)
    selected = []
    for residue in residues:
        V = residue if residue > 0 else PERIOD
        while V in FORBIDDEN:
            V += PERIOD
        assert V > 0 and V % PERIOD == residue and V not in FORBIDDEN
        assert all(x in FORBIDDEN for x in range(residue or PERIOD, V, PERIOD))
        selected.append(dict(residue=residue, V=V))
    assert selected == classification['failure_representatives']
    performed = len(residues) <= 6
    cases = [reconstruct_case(**row) for row in selected] if performed else []
    summary = totals(cases)
    primary = json.loads(PRIMARY.read_text())
    assert primary['protocol_sha256'] == PROTOCOL_SHA
    assert primary['classification_sha256'] == file_hash(CLASSIFICATION)
    assert primary['failed_residues'] == residues
    assert primary['selected_representatives'] == selected
    assert primary['diagnostics_performed'] == performed
    assert primary['stop_reason'] == (None if performed else 'more_than_six_failed_classes')
    assert len(primary['cases']) == len(cases)
    for rebuilt, stored in zip(cases, primary['cases']):
        if rebuilt != stored:
            differences = [key for key in set(rebuilt) | set(stored) if rebuilt.get(key) != stored.get(key)]
            raise AssertionError(f'V={rebuilt["V"]} differs: {differences}')
    assert summary == primary['totals']
    result = dict(status='PASS; independent exact reconstruction, no diagnose.py read/import',
                  protocol_sha256=PROTOCOL_SHA, classification_sha256=file_hash(CLASSIFICATION),
                  diagnostics_sha256=file_hash(PRIMARY),
                  verifier_sha256=file_hash(Path(__file__)),
                  failed_residues=residues, selected_representatives=selected,
                  diagnostics_performed=performed,
                  stop_reason=None if performed else 'more_than_six_failed_classes',
                  method='threshold-time state partition; direct preimage-existence phase partition; circle endpoint/gap reconstruction',
                  method_counts=COUNTERS, cases=cases, totals=summary)
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(OUT.read_text()), 'diagnostics_verification.json differs'
    print(json.dumps(dict(status='PASS', cases=[dict(
        V=c['V'], P_cover=c['P_metrics']['minimum_covering_arc_length'],
        B_cover=c['B_metrics']['minimum_covering_arc_length'],
        common_start_duration=c['common_start_duration'],
        witness=c['common_start_witness']['time'] if c['common_start_witness'] else None)
        for c in cases], totals=summary), indent=2))


if __name__ == '__main__':
    main()
