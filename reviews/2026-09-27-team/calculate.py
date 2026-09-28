"""Frozen six-case experiment: exact integer intervals and prefix integrals.

No project imports or floating point. All 35 labelled cores at reference 0.
--write creates the archive; default/--check replays it without writing.
The separate verifier reconstructs threshold events and uses Kruskal.
"""
from bisect import bisect_left, bisect_right
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = '578ad79f2d65ffe7309e3b1ae576de98e24ccaab1c23d3ea2600cedb5a9636a2'
CORES = list(combinations(range(1, 8), 3))
OUT = HERE / 'results.json'


def intersect(a, b):
    """Intersect two ordered disjoint lists of closed intervals."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            result.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        elif b[j][1] < a[i][1]:
            j += 1
        else:
            i += 1
            j += 1
    return result


def member(piece, t):
    a, b, ac, bc = piece
    return (a < t < b) or (t == a and ac) or (t == b and bc)


def strict_intersect(a, b):
    """Intersect interval lists, keeping membership of both endpoints."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        lc = member(a[i], lo) and member(b[j], lo)
        rc = member(a[i], hi) and member(b[j], hi)
        if lo < hi or (lo == hi and lc and rc):
            result.append((lo, hi, lc, rc))
        if a[i][1] < b[j][1]:
            i += 1
        elif b[j][1] < a[i][1]:
            j += 1
        else:
            i += 1
            j += 1
    return result


class PointSet:
    def __init__(self, pieces):
        self.pieces = pieces
        self.ends = [p[1] for p in pieces]

    def on(self, a, b):
        i = bisect_left(self.ends, a)
        result = []
        while i < len(self.pieces) and self.pieces[i][0] <= b:
            result.extend(strict_intersect([self.pieces[i]], [(a, b, True, True)]))
            i += 1
        return result

    def nonempty_on(self, a, b):
        i = bisect_left(self.ends, a)
        while i < len(self.pieces) and self.pieces[i][0] <= b:
            p = self.pieces[i]
            lo, hi = max(p[0], a), min(p[1], b)
            if lo < hi or (lo == hi and member(p, lo)):
                return True
            i += 1
        return False


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


def spanning_trees(vertices):
    if len(vertices) <= 1:
        return [()]
    edges = list(combinations(vertices, 2))
    answer = []
    for chosen in combinations(edges, len(vertices) - 1):
        seen = {vertices[0]}
        for _ in vertices:
            for i, j in chosen:
                if i in seen or j in seen:
                    seen.update((i, j))
        if len(seen) == len(vertices):
            answer.append(chosen)
    return answer


TREE_CACHE = {v: spanning_trees(v) for k in range(5) for v in combinations(range(1, 8), k)}


def optimal_tree(vertices, pairs):
    # Cache trees are lexicographic; strict > preserves the first maximizer.
    best = None
    for tree in TREE_CACHE[tuple(vertices)]:
        weight = sum(pairs[edge] for edge in tree)
        if best is None or weight > best[0]:
            best = (weight, tree)
    return best


def induced_components(active, tree):
    if not active:
        return 0
    # An induced subgraph of a tree is a forest: c = vertices - edges.
    return len(active) - sum(i in active and j in active for i, j in tree)


def rational(x, denominator):
    return str(Fraction(x, denominator))


def direct_witness(t, speeds):
    ds = [min((speeds[i] * t) % 1, 1 - (speeds[i] * t) % 1) for i in range(1, 8)]
    assert min(ds) >= Fraction(1, 8)
    return {'time': str(t), 'distances': list(map(str, ds)),
            'kind': 'strict' if min(ds) > Fraction(1, 8) else 'equality'}


def witness_in(pieces, speeds, denominator):
    if not pieces:
        return None
    positive = [(a, b) for a, b in pieces if a < b]
    a, b = max(positive, key=lambda p: p[1] - p[0]) if positive else pieces[0]
    result = direct_witness(Fraction(a + b, 2 * denominator), speeds)
    assert (result['kind'] == 'strict') == bool(positive)
    return result


COUNT_FIELDS = [
    'components', 'singleton_components', 'positive_bound_components',
    'positive_actual_components', 'positive_actual_tree_misses',
    'positive_bound_without_reduction', 'positive_bound_without_nonempty_containment',
    'windows_with_vanished', 'windows_with_nonempty_proper_containment',
    'windows_with_equal_nonempty', 'windows_with_reduction',
    'full_reduced_bound_mismatches', 'allowed_set_reduction_mismatches',
    'slack_identity_mismatches', 'exact_tree_components', 'positive_slack_components',
]


def empty_summary():
    return {**{k: 0 for k in COUNT_FIELDS}, 'retained_count_histogram': [0] * 5,
            'vanished_count_histogram': [0] * 5, 'sum_tree_slack': 0,
            'maximum_tree_slack': 0, 'minimum_bound': None, 'maximum_bound': None}


def finish_summary(summary, denominator):
    for k in ('sum_tree_slack', 'maximum_tree_slack', 'minimum_bound', 'maximum_bound'):
        summary[k] = rational(summary[k], denominator)
    return summary


def sum_summaries(summaries):
    out = {k: sum(s[k] for s in summaries) for k in COUNT_FIELDS}
    for k in ('retained_count_histogram', 'vanished_count_histogram'):
        out[k] = [sum(s[k][i] for s in summaries) for i in range(5)]
    out['sum_tree_slack'] = str(sum(Fraction(s['sum_tree_slack']) for s in summaries))
    for k, op in [('maximum_tree_slack', max), ('minimum_bound', min), ('maximum_bound', max)]:
        out[k] = str(op(Fraction(s[k]) for s in summaries))
    return out


def qkey(record):
    a, b = record['window']
    return (-record['bound'], len(record['retained']), -(b - a), record['core'], a)


def concise(record, denominator):
    return {'component_index': record['component_index'],
            'window': [rational(x, denominator) for x in record['window']],
            'bound': rational(record['bound'], denominator),
            'actual_duration': rational(record['actual'], denominator),
            'retained': list(record['retained']),
            'tree_slack': rational(record['actual'] - record['bound'], denominator),
            'tree_edges': [list(e) for e in record['tree']]}


def run_case(case):
    velocities = case['velocities']
    speeds = {i: abs(velocities[i] - velocities[0]) for i in range(1, 8)}
    assert len(velocities) == len(set(velocities)) == 8
    L = lcm(*speeds.values())
    denominator = 8 * L
    safe, blocks, point_blocks = {}, {}, {}
    for i, v in speeds.items():
        unit = L // v
        safe[i] = [((8 * j + 1) * unit, (8 * j + 7) * unit) for j in range(v)]
        pieces = [(0, unit, True, False)]
        pieces += [((8 * j - 1) * unit, (8 * j + 1) * unit, False, False) for j in range(1, v)]
        pieces += [((8 * v - 1) * unit, denominator, False, True)]
        point_blocks[i] = PointSet(pieces)
        blocks[i] = [(a, b) for a, b, _, _ in pieces]
    violations = {}
    for i in speeds:
        for j in speeds:
            if i != j:
                violations[i, j] = PointSet(strict_intersect(
                    point_blocks[i].pieces, [(a, b, True, True) for a, b in safe[j]]))
    intersections = {(): [(0, denominator)]}
    integrals = {}
    for k in range(5):
        for subset in combinations(range(1, 8), k):
            if subset:
                intersections[subset] = intersect(intersections[subset[:-1]], blocks[subset[-1]])
            integrals[subset] = Integral(intersections[subset])
    full = [(0, denominator)]
    for i in range(1, 8):
        full = intersect(full, safe[i])
    actual_integral = Integral(full)
    full_duration = actual_integral.prefix[-1]
    global_witness = witness_in(full, speeds, denominator)
    core_records, all_endpoints, winner = [], set(), None
    for core in CORES:
        windows = [(0, denominator)]
        for i in sorted(core, key=lambda label: speeds[label]):
            windows = intersect(windows, safe[i])
        assert windows
        residual = tuple(i for i in range(1, 8) if i not in core)
        subsets = [tuple(residual[j] for j in range(4) if mask & (1 << j)) for mask in range(16)]
        summary, digest, best = empty_summary(), sha256(), None
        actual_sum = 0
        for component_index, (a, b) in enumerate(windows):
            all_endpoints.update((a, b))
            moments = [integrals[s].on(a, b) for s in subsets]
            singles = {i: moments[1 << j] for j, i in enumerate(residual)}
            pairs = {(i, j): integrals[i, j].on(a, b) for i, j in combinations(residual, 2)}
            vanished = tuple(i for i in residual if not point_blocks[i].nonempty_on(a, b))
            edges = tuple((i, j) for i in residual for j in residual
                          if i != j and not violations[i, j].nonempty_on(a, b))
            edge_set = set(edges)
            nonempty = tuple(i for i in residual if i not in vanished)
            proper = tuple((i, j) for i, j in edges if i in nonempty and j in nonempty
                           and (j, i) not in edge_set)
            equality_classes = []
            ungrouped = set(nonempty)
            while ungrouped:
                i = min(ungrouped)
                group = tuple(j for j in nonempty if j == i or ((i, j) in edge_set and (j, i) in edge_set))
                equality_classes.append(group)
                ungrouped.difference_update(group)
            retained = tuple(group[0] for group in equality_classes
                             if not any((group[0], j) in proper for j in nonempty))
            full_weight, full_tree = optimal_tree(residual, pairs)
            reduced_weight, reduced_tree = optimal_tree(retained, pairs)
            full_bound = b - a - sum(singles.values()) + full_weight
            bound = b - a - sum(singles[i] for i in retained) + reduced_weight
            actual = actual_integral.on(a, b)
            actual_sum += actual
            local_allowed = intersect([(a, b)], full)
            reduced_allowed = [(a, b)]
            for i in retained:
                reduced_allowed = intersect(reduced_allowed, safe[i])
            # Boolean inversion gives the full four-blocker occupancy masses.
            atoms = moments[:]
            for bit in range(4):
                for mask in range(16):
                    if not mask & (1 << bit):
                        atoms[mask] -= atoms[mask | (1 << bit)]
            assert all(m >= 0 for m in atoms) and sum(atoms) == b - a
            assert atoms[0] == actual
            component_masses = [0] * 5
            for active, mass in zip(subsets, atoms):
                component_masses[induced_components(active, full_tree)] += mass
            measured_slack = sum(max(c - 1, 0) * mass for c, mass in enumerate(component_masses))
            slack = actual - bound
            summary['full_reduced_bound_mismatches'] += full_bound != bound
            summary['allowed_set_reduction_mismatches'] += local_allowed != reduced_allowed
            summary['slack_identity_mismatches'] += measured_slack != slack
            assert full_bound == bound <= actual
            assert local_allowed == reduced_allowed
            assert measured_slack == slack
            if a == b:
                assert actual == bound == 0
            summary['components'] += 1
            summary['singleton_components'] += a == b
            summary['positive_bound_components'] += bound > 0
            summary['positive_actual_components'] += actual > 0
            summary['positive_actual_tree_misses'] += actual > 0 and bound <= 0
            summary['positive_bound_without_reduction'] += bound > 0 and len(retained) == 4
            has_nonempty_containment = any(i in nonempty and j in nonempty for i, j in edges)
            summary['positive_bound_without_nonempty_containment'] += bound > 0 and not has_nonempty_containment
            summary['windows_with_vanished'] += bool(vanished)
            summary['windows_with_nonempty_proper_containment'] += bool(proper)
            summary['windows_with_equal_nonempty'] += any(len(group) > 1 for group in equality_classes)
            summary['windows_with_reduction'] += len(retained) < 4
            summary['retained_count_histogram'][len(retained)] += 1
            summary['vanished_count_histogram'][len(vanished)] += 1
            summary['exact_tree_components'] += slack == 0
            summary['positive_slack_components'] += slack > 0
            summary['sum_tree_slack'] += slack
            summary['maximum_tree_slack'] = max(summary['maximum_tree_slack'], slack)
            for field, op in [('minimum_bound', min), ('maximum_bound', max)]:
                summary[field] = bound if summary[field] is None else op(summary[field], bound)
            row = [rational(a, denominator), rational(b, denominator), rational(bound, denominator),
                   rational(actual, denominator), vanished, edges, retained]
            digest.update((json.dumps(row, separators=(',', ':')) + '\n').encode())
            record = dict(component_index=component_index, core=core, residual=residual, window=(a, b),
                          bound=bound, actual=actual, retained=retained, tree=reduced_tree,
                          full_bound=full_bound, full_tree=full_tree, vanished=vanished,
                          edges=edges, proper=proper, equality_classes=equality_classes,
                          moments=moments, atoms=atoms, component_masses=component_masses,
                          subsets=subsets, singles=singles, pairs=pairs, allowed=local_allowed)
            if a < b and (best is None or qkey(record) < qkey(best)):
                best = record
        assert actual_sum == full_duration
        core_records.append({'core': list(core), 'residual': list(residual),
                             'component_sha256': digest.hexdigest(),
                             'summary': finish_summary(summary, denominator),
                             'q_best': concise(best, denominator) if best else None})
        if best is not None and (winner is None or qkey(best) < qkey(winner)):
            winner = best
    summary = sum_summaries([r['summary'] for r in core_records])
    summary['positive_cores'] = sum(r['summary']['positive_bound_components'] > 0 for r in core_records)
    fastest = max(speeds, key=speeds.get)
    fastest_cores = [r for r in core_records if fastest in r['core']]
    fastest_diagnostic = {
        'fastest_runner_index': fastest,
        'cores': len(fastest_cores),
        'components': sum(r['summary']['components'] for r in fastest_cores),
        'exact_components': sum(r['summary']['exact_tree_components'] for r in fastest_cores),
        'nonexact_components': sum(r['summary']['positive_slack_components'] for r in fastest_cores),
        'maximum_slack': str(max(Fraction(r['summary']['maximum_tree_slack']) for r in fastest_cores)),
    }
    assert winner is not None
    a, b = winner['window']
    cert = concise(winner, denominator)
    cert.update(core=list(winner['core']), residual=list(winner['residual']),
                core_speeds=[speeds[i] for i in winner['core']],
                residual_speeds=[speeds[i] for i in winner['residual']],
                full_bound=rational(winner['full_bound'], denominator),
                full_tree_edges=[list(e) for e in winner['full_tree']],
                vanished=list(winner['vanished']), containment_edges=[list(e) for e in winner['edges']],
                proper_nonempty_containment_edges=[list(e) for e in winner['proper']],
                equal_nonempty_classes=[list(c) for c in winner['equality_classes'] if len(c) > 1],
                removed_cover=[[i, min(j for j in winner['retained'] if (i, j) in winner['edges'])]
                               for i in winner['residual'] if i not in winner['vanished'] and i not in winner['retained']],
                strict_blocker_components=[[i, [[rational(x, denominator), rational(y, denominator), lc, rc]
                                               for x, y, lc, rc in point_blocks[i].on(a, b)]] for i in winner['residual']],
                single_durations=[[i, rational(m, denominator)] for i, m in winner['singles'].items()],
                pair_durations=[[i, j, rational(m, denominator)] for (i, j), m in winner['pairs'].items()],
                intersection_durations=[[list(s), rational(m, denominator)] for s, m in zip(winner['subsets'], winner['moments'])],
                active_state_durations=[[list(s), rational(m, denominator)] for s, m in zip(winner['subsets'], winner['atoms'])],
                slack_by_active_components=[[c, rational(m, denominator)] for c, m in enumerate(winner['component_masses'])],
                allowed_components=[[rational(x, denominator), rational(y, denominator)] for x, y in winner['allowed']],
                witness=witness_in(winner['allowed'], speeds, denominator))
    fallback = None
    outcome = 'positive_tree' if winner['bound'] > 0 else 'inconclusive'
    if winner['bound'] <= 0:
        fallback = {'tested_count': 0, 'candidate_count': len(all_endpoints), 'witness': None}
        for t in sorted(all_endpoints):
            fallback['tested_count'] += 1
            if all(8 * min(speeds[i] * t % denominator, denominator - speeds[i] * t % denominator) >= denominator
                   for i in range(1, 8)):
                fallback['witness'] = direct_witness(Fraction(t, denominator), speeds)
                outcome = 'endpoint_fallback'
                break
    result = {
        'id': case['id'], 'velocities': velocities, 'reference_index': 0,
        'integer_denominator': denominator,
        'full_allowed_components': [[rational(a, denominator), rational(b, denominator)] for a, b in full],
        'full_allowed_duration': rational(full_duration, denominator),
        'full_positive_component_count': sum(a < b for a, b in full),
        'full_isolated_points': [rational(a, denominator) for a, b in full if a == b],
        'global_witness': global_witness,
        'time_one_eighth_distances': [str(min(Fraction(v, 8) % 1, 1 - Fraction(v, 8) % 1)) for v in speeds.values()],
        'summary': summary, 'cores': core_records, 'selected_certificate': cert,
        'fastest_core_diagnostic': fastest_diagnostic,
        'selection_outcome': outcome, 'endpoint_fallback': fallback,
        'strict_all_core_failure': full_duration > 0 and winner['bound'] <= 0,
    }
    print(case['id'], 'windows', summary['components'], 'positive cores', summary['positive_cores'],
          'bound', cert['bound'], 'actual', cert['actual_duration'], 'retained', cert['retained'],
          'misses', summary['positive_actual_tree_misses'], flush=True)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = ap.parse_args()
    protocol_bytes = (HERE / 'protocol.json').read_bytes()
    assert sha256(protocol_bytes).hexdigest() == PROTOCOL_HASH, 'Frozen protocol changed'
    protocol = json.loads(protocol_bytes)
    assert protocol['reference_index'] == 0 and protocol['n'] == 8
    cases = [run_case(case) for case in protocol['cases']]
    totals = sum_summaries([c['summary'] for c in cases])
    totals['positive_cores'] = sum(c['summary']['positive_cores'] for c in cases)
    result = {'schema_version': 1,
              'status': 'OBSERVED exact finite experiment; no theorem or novelty claim',
              'protocol_sha256': PROTOCOL_HASH,
              'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'core_order': [list(c) for c in CORES], 'cases': cases, 'totals': totals}
    if args.write:
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == json.loads(OUT.read_text()), 'Archive drift'
    print('PASS: all six prescribed cases; exact strict maps, all full/reduced optima, '
          'allowed-set preservation and slack identities; ' + ('written' if args.write else 'replayed read-only'))


if __name__ == '__main__':
    main()
