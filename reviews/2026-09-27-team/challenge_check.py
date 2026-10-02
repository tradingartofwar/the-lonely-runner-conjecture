"""Small, exact hostile-review diagnostics. Only the six frozen inputs.

The abstract Boolean checks use no physical speed configurations. The primary
archive audit reads its summaries/certificates; it is not a second reconstruction
of every time component. Default/--check is read-only; --write saves this scope.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def trees(n):
    if n == 1:
        return [()]
    out = []
    for edges in combinations(list(combinations(range(n), 2)), n - 1):
        reached = {0}
        while True:
            enlarged = reached | {v for edge in edges if reached.intersection(edge)
                                  for v in edge}
            if enlarged == reached:
                break
            reached = enlarged
        if len(reached) == n:
            out.append(edges)
    return out


def components(active, edges):
    active = set(active)
    count = 0
    while active:
        reached = {min(active)}
        while True:
            enlarged = reached | {v for edge in edges
                                  if reached.intersection(edge)
                                  for v in edge if v in active}
            if enlarged == reached:
                break
            reached = enlarged
        active -= reached
        count += 1
    return count


def boolean_checks():
    checked = 0
    rows = []
    for n in range(1, 5):
        all_trees = trees(n)
        for mask in range(1 << n):
            active = {i for i in range(n) if mask & (1 << i)}
            slacks = []
            for edges in all_trees:
                active_edges = sum(i in active and j in active for i, j in edges)
                slack = int(not active) - (1-len(active)+active_edges)
                assert slack == max(components(active, edges)-1, 0)
                if n == 4:
                    # Four-set exact-state formula: pairs not in T, and
                    # triples weighted by degree of their omitted vertex - 1.
                    expected = 0
                    if len(active) == 2:
                        expected = int(tuple(sorted(active)) not in edges)
                    elif len(active) == 3:
                        missing = next(iter(set(range(4))-active))
                        expected = sum(missing in edge for edge in edges)-1
                    assert slack == expected
                slacks.append(slack)
                checked += 1
            if n == 4:
                assert F(sum(slacks), len(slacks)) == (
                    F(1, 2) if len(active) in (2, 3) else F(0))
        rows.append(dict(vertices=n, trees=len(all_trees), states=1 << n))
    return dict(tree_state_checks=checked, scopes=rows,
                four_vertex_average_slack_coefficients=['0','0','1/2','1/2','0'])


def modular_checks(protocol):
    rows = []
    for case in protocol['cases']:
        speeds = case['velocities'][1:]
        witnesses = []
        for d in range(2, 8):
            distances = [F(min(v % d, d-v % d), d) for v in speeds]
            if min(distances) > F(1, 8):
                witnesses.append(dict(time=str(F(1, d)),
                                      minimum=str(min(distances)),
                                      distances=list(map(str, distances))))
        rows.append(dict(id=case['id'], denominator_scope='2..7',
                         strict_reciprocal_witnesses=witnesses))
    return rows


def primary_audit(protocol):
    path = HERE / 'results.json'
    archive = json.loads(path.read_text())
    assert archive['protocol_sha256'] == sha256((HERE/'protocol.json').read_bytes()).hexdigest()
    rows = []
    assert len(archive['cases']) == len(protocol['cases'])
    for case, frozen in zip(archive['cases'], protocol['cases']):
        assert case['id'] == frozen['id']
        assert case['velocities'] == frozen['velocities']
        speeds = frozen['velocities']
        fastest = max(range(1, 8), key=lambda i: abs(speeds[i]-speeds[0]))
        fast_cores = [core for core in case['cores'] if fastest in core['core']]
        assert len(fast_cores) == 15
        positive = F(case['full_allowed_duration']) > 0
        for core in fast_cores:
            summary = core['summary']
            assert summary['exact_tree_components'] == summary['components']
            assert F(summary['sum_tree_slack']) == 0
            assert summary['positive_slack_components'] == 0
            assert summary['positive_actual_tree_misses'] == 0
            if positive:
                assert summary['positive_bound_components'] > 0
        selected = case['selected_certificate']
        a, b = map(F, selected['window'])
        states = [(set(active), F(mass)) for active, mass in selected['active_state_durations']]
        edges = [tuple(edge) for edge in selected['full_tree_edges']]
        assert sum(mass for _, mass in states) == b-a
        true_clear = sum(mass for active, mass in states if not active)
        slack = sum(mass*max(components(active, edges)-1, 0) for active, mass in states)
        singles = {i:F(mass) for i,mass in selected['single_durations']}
        pairs = {(i,j):F(mass) for i,j,mass in selected['pair_durations']}
        value = b-a-sum(singles.values())+sum(pairs[e] for e in edges)
        assert value == F(selected['bound']) == F(selected['full_bound'])
        assert true_clear == F(selected['actual_duration'])
        assert slack == true_clear-value == F(selected['tree_slack'])
        for witness in (case['global_witness'], selected['witness']):
            assert witness is not None
            time = F(witness['time'])
            distances = []
            for speed in speeds[1:]:
                phase = ((speed-speeds[0])*time) % 1
                distances.append(min(phase, 1-phase))
            assert distances == list(map(F, witness['distances']))
            assert min(distances) > F(1, 8)
            assert witness['kind'] == 'strict'
        split_retained = [i for i, intervals in selected['strict_blocker_components']
                          if i in selected['retained'] and len(intervals) >= 2]
        if slack > 0:
            assert split_retained
        for i in split_retained:
            assert (b-a)*abs(speeds[i]-speeds[0]) > F(3, 4)
        bests = [(core, core['q_best']) for core in case['cores'] if core['q_best'] is not None]
        def key(entry):
            core, item = entry
            left, right = map(F, item['window'])
            return (-F(item['bound']), len(item['retained']), -(right-left),
                    tuple(core['core']), left)
        winner, item = min(bests, key=key)
        assert winner['core'] == selected['core']
        assert item['window'] == selected['window']
        rows.append(dict(id=case['id'], fastest_index=fastest,
                         fastest_speed=speeds[fastest],
                         guaranteed_exact_cores=15,
                         fastest_core_components=sum(c['summary']['components'] for c in fast_cores),
                         selected_core=selected['core'], selected_bound=str(value),
                         selected_actual=str(true_clear), selected_slack=str(slack),
                         selected_split_retained=split_retained,
                         selected_contains_fastest=fastest in selected['core']))
    return dict(results_sha256=sha256(path.read_bytes()).hexdigest(), cases=rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    protocol_path = HERE/'protocol.json'
    protocol = json.loads(protocol_path.read_text())
    output = dict(status='OBSERVED exact finite checks; general arguments require review',
                  scope='Six frozen speed inputs; reference 0; no added cases',
                  script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  protocol_sha256=sha256(protocol_path.read_bytes()).hexdigest(),
                  boolean_checks=boolean_checks(),
                  modular_checks=modular_checks(protocol),
                  primary_audit=primary_audit(protocol))
    path = HERE/'challenge_checks.json'
    if args.write:
        path.write_text(json.dumps(output, indent=2)+'\n')
    else:
        assert output == json.loads(path.read_text()), 'challenge_checks.json differs'
    print(json.dumps(dict(status='PASS', boolean_checks=output['boolean_checks'],
                         primary_audit=output['primary_audit']), indent=2))


if __name__ == '__main__':
    main()
