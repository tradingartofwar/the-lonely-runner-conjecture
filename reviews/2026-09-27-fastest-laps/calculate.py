"""Exact 29-lap original common-start experiment; no shifted-start calculations.

Closed safe intersections, strict interval flags, integer prefix integrals,
and exhaustive enumeration of all 1,296 six-node labelled spanning trees.
Default/--check replays the archive read-only; --write creates it.
"""
from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results.json'
PROTOCOL_HASH = 'f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d'
RESIDUAL = (1, 4, 5, 6, 7, 11)
LABELS = tuple(range(1, 7))
EDGES = list(combinations(LABELS, 2))


def intersect(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            out.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        elif b[j][1] < a[i][1]:
            j += 1
        else:
            i += 1
            j += 1
    return out


def member(p, t):
    a, b, ac, bc = p
    return a < t < b or (a == t and ac) or (b == t and bc)


def clip(p, a, b):
    lo, hi = max(p[0], a), min(p[1], b)
    lc, rc = member(p, lo), member(p, hi)
    if lo < hi or (lo == hi and lc and rc):
        return (lo, hi, lc, rc)
    return None


def subset(p, q):
    if p is None:
        return True
    if q is None:
        return False
    return ((p[0] > q[0] or (p[0] == q[0] and (not p[2] or q[2]))) and
            (p[1] < q[1] or (p[1] == q[1] and (not p[3] or q[3]))))


class Integral:
    def __init__(self, pieces):
        self.pieces = [(a, b) for a, b in pieces if a < b]
        self.starts = [a for a, b in self.pieces]
        self.prefix = [0]
        for a, b in self.pieces:
            self.prefix.append(self.prefix[-1] + b - a)

    def at(self, t):
        i = bisect_right(self.starts, t) - 1
        if i < 0:
            return 0
        a, b = self.pieces[i]
        return self.prefix[i] + min(t, b) - a

    def on(self, a, b):
        return self.at(b) - self.at(a)


def trees():
    out = []
    for chosen in combinations(EDGES, 5):
        seen = {1}
        for _ in LABELS:
            for i, j in chosen:
                if i in seen or j in seen:
                    seen.update((i, j))
        if len(seen) == 6:
            out.append(chosen)
    assert len(out) == 1296
    return out


TREES = trees()


def q(x, d):
    return str(Fraction(x, d))


def encode_components(pieces, d):
    return [[q(a, d), q(b, d)] for a, b in pieces]


def safe_intervals(v, d):
    unit = d // (8 * v)
    assert unit * 8 * v == d
    return [((8 * j + 1) * unit, (8 * j + 7) * unit) for j in range(v)]


def strict_intervals(v, d):
    unit = d // (8 * v)
    return [(max(0, (8 * j - 1) * unit), min(d, (8 * j + 1) * unit), j == 0, j == v)
            for j in range(v + 1)]


def full_safe(speeds, d):
    out = [(0, d)]
    for v in speeds:
        out = intersect(out, safe_intervals(v, d))
    return out


def direct(t, velocities):
    return [min(v * t % 1, 1 - v * t % 1) for v in velocities[1:]]


def witness(pieces, velocities, d):
    if not pieces:
        return None
    positive = [(a, b) for a, b in pieces if a < b]
    a, b = max(positive, key=lambda p: p[1] - p[0]) if positive else pieces[0]
    t = Fraction(a + b, 2 * d)
    distances = direct(t, velocities)
    assert min(distances) >= Fraction(1, 8)
    kind = 'strict' if min(distances) > Fraction(1, 8) else 'equality'
    assert (kind == 'strict') == bool(positive)
    return {'time': str(t), 'distances': list(map(str, distances)), 'kind': kind}


def controllers(t, velocities, d):
    return [i for i in range(1, 8)
            if 8 * min(velocities[i] * t % d, d - velocities[i] * t % d) == d]


def survives(t, velocities, d):
    return all(8 * min(v * t % d, d - v * t % d) >= d for v in velocities[1:])


def coverage_scan(local, left_order, a, b, velocities, d):
    frontier = None
    rows = []
    touches = {}
    for index in left_order:
        lo, hi, lc, rc = local[index]
        before = None if frontier is None else [q(frontier[0], d), frontier[1]]
        touch_survives, touch_controllers = None, []
        if frontier is None:
            junction, advances = 'first', True
            frontier = (hi, rc)
        else:
            junction = 'overlap' if lo < frontier[0] else ('touch' if lo == frontier[0] else 'gap')
            if junction == 'touch':
                touch_survives = survives(lo, velocities, d)
                touch_controllers = controllers(lo, velocities, d)
                touches[lo] = [q(lo, d), touch_survives, touch_controllers]
            advances = hi > frontier[0]
            if hi > frontier[0]:
                frontier = (hi, rc)
            elif hi == frontier[0]:
                frontier = (hi, frontier[1] or rc)
        rows.append({'index': index, 'junction': junction, 'frontier_before': before,
                     'frontier_after': [q(frontier[0], d), frontier[1]], 'advances': advances,
                     'touch_survives': touch_survives, 'touch_controllers': touch_controllers})
    if not left_order:
        initial, final = [q(a, d), q(b, d)], None
    else:
        first_left = local[left_order[0]][0]
        initial = [q(a, d), q(first_left, d)] if first_left > a else None
        final = [q(frontier[0], d), q(b, d)] if frontier[0] < b else None
    return rows, initial, final, [touches[t] for t in sorted(touches)]


def union_measure(local):
    intervals = sorted((p[0], p[1]) for p in local.values() if p is not None)
    total = 0
    right = None
    for a, b in intervals:
        if right is None or a > right:
            total += b - a
            right = b
        elif b > right:
            total += b - right
            right = b
    return total


COUNT_FIELDS = ['laps', 'covered_laps', 'contact_only_laps', 'strict_laps',
                'positive_tree_laps', 'exact_tree_laps', 'isolated_point_count',
                'positive_component_count', 'touch_junction_count', 'surviving_touch_count']


def run_case(case):
    velocities = case['velocities']
    assert velocities == [0, *RESIDUAL, velocities[7]]
    V = velocities[7]
    assert V > max(RESIDUAL)
    d = 8 * lcm(*velocities[1:])
    fixed_safe = full_safe(RESIDUAL, d)
    full = intersect(fixed_safe, safe_intervals(V, d))
    full_integral = Integral(full)
    strict = {i: strict_intervals(velocities[i], d) for i in LABELS}
    singles = {i: Integral([(a, b) for a, b, _, _ in strict[i]]) for i in LABELS}
    pairs = {(i, j): Integral(intersect([(a, b) for a, b, _, _ in strict[i]],
                                      [(a, b) for a, b, _, _ in strict[j]])) for i, j in EDGES}
    records, digest = [], sha256()
    summary = {key: 0 for key in COUNT_FIELDS}
    summary['maximum_tree_slack'] = '0'
    for m, (a, b) in enumerate(safe_intervals(V, d)):
        local, blocker_records = {}, []
        for i in LABELS:
            clipped = [(j, clip(p, a, b)) for j, p in enumerate(strict[i])]
            clipped = [(j, p) for j, p in clipped if p is not None]
            assert len(clipped) <= 1
            collision_lap, p = clipped[0] if clipped else (None, None)
            local[i] = p
            interval = [q(p[0], d), q(p[1], d), p[2], p[3]] if p else None
            normalized = [q(V * p[0] - m * d, d), q(V * p[1] - m * d, d), p[2], p[3]] if p else None
            blocker_records.append({'index': i, 'speed': velocities[i], 'collision_lap': collision_lap,
                                    'interval': interval, 'normalized_interval': normalized})
        vanished = [i for i in LABELS if local[i] is None]
        edges = [[i, j] for i in LABELS for j in LABELS if i != j and subset(local[i], local[j])]
        left_order = sorted((i for i in LABELS if local[i] is not None),
                            key=lambda i: (local[i][0], -local[i][1], i))
        signature = [vanished, left_order, edges]
        ds = {i: singles[i].on(a, b) for i in LABELS}
        os = {edge: pairs[edge].on(a, b) for edge in EDGES}
        for i in LABELS:
            assert ds[i] == (local[i][1] - local[i][0] if local[i] else 0)
        for i, j in EDGES:
            assert os[i, j] == (max(0, min(local[i][1], local[j][1]) - max(local[i][0], local[j][0]))
                               if local[i] and local[j] else 0)
        best_weight, best_tree = -1, None
        for tree in TREES:
            weight = sum(os[edge] for edge in tree)
            if weight > best_weight:
                best_weight, best_tree = weight, tree
        bound = b - a - sum(ds.values()) + best_weight
        allowed = intersect([(a, b)], fixed_safe)
        actual = sum(y - x for x, y in allowed)
        union = union_measure(local)
        assert bound == actual == full_integral.on(a, b) == b - a - union
        status = 'strict' if actual > 0 else ('contacts' if allowed else 'covered')
        scan, initial, final, touch_points = coverage_scan(local, left_order, a, b, velocities, d)
        isolated = [q(x, d) for x, y in allowed if x == y]
        endpoint_times = sorted({t for pair in allowed for t in pair})
        for t in endpoint_times:
            assert survives(t, velocities, d)
        row = {
            'm': m, 'window': [q(a, d), q(b, d)], 'width': q(b - a, d),
            'residues': [[i, velocities[i] * m % V] for i in LABELS],
            'residue_lifts': [[i, velocities[i] * m // V] for i in LABELS],
            'blockers': blocker_records, 'vanished': vanished, 'containment_edges': edges,
            'qualitative_signature': signature,
            'single_durations': [[i, q(ds[i], d)] for i in LABELS],
            'pair_durations': [[i, j, q(os[i, j], d)] for i, j in EDGES],
            'tree_edges': [list(edge) for edge in best_tree], 'tree_weight': q(best_weight, d),
            'tree_bound': q(bound, d), 'actual_duration': q(actual, d),
            'tree_slack': q(actual - bound, d), 'union_duration': q(union, d),
            'allowed_components': encode_components(allowed, d), 'isolated_points': isolated,
            'status': status, 'witness': witness(allowed, velocities, d),
            'allowed_endpoint_controllers': [[q(t, d), controllers(t, velocities, d)] for t in endpoint_times],
            'coverage_scan': scan, 'scan_initial_gap': initial, 'scan_final_gap': final,
            'scan_touch_points': touch_points,
        }
        records.append(row)
        digest.update((json.dumps(row, sort_keys=True, separators=(',', ':')) + '\n').encode())
        summary['laps'] += 1
        summary['covered_laps'] += status == 'covered'
        summary['contact_only_laps'] += status == 'contacts'
        summary['strict_laps'] += status == 'strict'
        summary['positive_tree_laps'] += bound > 0
        summary['exact_tree_laps'] += bound == actual
        summary['isolated_point_count'] += len(isolated)
        summary['positive_component_count'] += sum(x < y for x, y in allowed)
        summary['touch_junction_count'] += sum(r['junction'] == 'touch' for r in scan)
        summary['surviving_touch_count'] += sum(r['touch_survives'] is True for r in scan)
        print(case['id'], 'lap', m, status, 'duration', q(actual, d), 'contacts', isolated, flush=True)
    assert sum(Fraction(r['actual_duration']) for r in records) == Fraction(full_integral.prefix[-1], d)
    assert [ab for r in records for ab in r['allowed_components']] == encode_components(full, d)
    return {'id': case['id'], 'velocities': velocities, 'V': V, 'integer_denominator': d,
            'laps': records, 'lap_records_sha256': digest.hexdigest(),
            'full_allowed_components': encode_components(full, d),
            'full_allowed_duration': q(full_integral.prefix[-1], d),
            'full_isolated_points': [q(a, d) for a, b in full if a == b],
            'global_witness': witness(full, velocities, d), 'summary': summary}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raw = (HERE / 'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH, 'Frozen protocol changed'
    protocol = json.loads(raw)
    assert protocol['reference_index'] == 0 and protocol['residual_speeds'] == list(RESIDUAL)
    fixed_d = 8 * lcm(*RESIDUAL)
    fixed = full_safe(RESIDUAL, fixed_d)
    cases = [run_case(c) for c in protocol['cases']]
    groups = {}
    for case in cases:
        for row in case['laps']:
            signature = row['qualitative_signature']
            key = json.dumps(signature, separators=(',', ':'))
            if key not in groups:
                groups[key] = {'signature': signature, 'members': [], 'statuses': set()}
            groups[key]['members'].append([case['id'], row['m']])
            groups[key]['statuses'].add(row['status'])
    group_records = []
    for key in sorted(groups):
        group = groups[key]
        group['statuses'] = sorted(group['statuses'])
        group['status_collision'] = len(group['statuses']) > 1
        group_records.append(group)
    summary = {key: sum(c['summary'][key] for c in cases) for key in COUNT_FIELDS}
    summary.update(maximum_tree_slack=str(max(Fraction(c['summary']['maximum_tree_slack']) for c in cases)),
                   qualitative_groups=len(group_records),
                   qualitative_status_collision_groups=sum(g['status_collision'] for g in group_records))
    result = {'schema_version': 1, 'status': 'OBSERVED exact finite common-start experiment; no novelty claim',
              'protocol_sha256': PROTOCOL_HASH, 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'fixed_residual_speeds': list(RESIDUAL), 'fixed_safe_components': encode_components(fixed, fixed_d),
              'fixed_safe_duration': q(sum(b - a for a, b in fixed), fixed_d),
              'cases': cases, 'qualitative_groups': group_records, 'summary': summary}
    if args.write:
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == json.loads(OUT.read_text()), 'Archive drift'
    print('PASS: all 29 fixed common-start laps, strict intervals, moments, exhaustive trees, '
          'allowed sets, controllers, residues, and cover scans; ' + ('written' if args.write else 'replayed read-only'))
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
