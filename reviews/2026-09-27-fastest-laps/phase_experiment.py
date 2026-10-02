"""Exact finite normalized-lap phase permutation experiment.

Only --write writes phase_results.json. Default/--check rebuilds and compares
read-only. No project imports; standard library and exact rationals only.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'protocol.json'
OUT = HERE / 'phase_results.json'
PROTOCOL_SHA = 'f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d'
D = F(1, 8)
A, B = D, 1-D
RESIDUAL = (1, 4, 5, 6, 7, 11)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def digest(obj):
    return sha256(canonical(obj).encode()).hexdigest()


def distance(x):
    y = x % 1
    return min(y, 1-y)


def encoded(parts):
    return [[str(a), str(b)] for a, b in parts]


def pattern(V, v, m):
    """Build strict normalized blockers from collision integers, then clip."""
    residue = v*m % V
    pieces = []
    # residue/V + v*u/V lies in (0,2), so only 0,1,2 may block it.
    for z in range(3):
        lo = (V*(z-D)-residue)/v
        hi = (V*(z+D)-residue)/v
        left, right = max(A, lo), min(B, hi)
        if left < right:
            pieces.append((left, right, lo < left < hi, lo < right < hi))
    assert len(pieces) <= 1
    return pieces


def encode_pattern(pieces):
    return [[str(a), str(b), lc, rc] for a, b, lc, rc in pieces]


def blocked(t, pieces):
    return any((a < t or a == t and lc) and (t < b or t == b and rc)
               for a, b, lc, rc in pieces)


def local_allowed(patterns):
    """Complement the strict interval union, retaining every safe endpoint."""
    pieces = [p for row in patterns.values() for p in row]
    cuts = sorted({A, B} | {x for a, b, _, _ in pieces for x in (a, b)})
    safe = {x: not blocked(x, pieces) for x in cuts}
    parts = [(x, x) for x in cuts if safe[x]]
    for x, y in zip(cuts, cuts[1:]):
        if not blocked((x+y)/2, pieces):
            assert safe[x] and safe[y]
            parts.append((x, y))
    result = []
    for a, b in sorted(parts):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(b, result[-1][1]))
        else:
            result.append((a, b))
    return result


def classify(parts):
    if any(a < b for a, b in parts):
        return 'positive_duration'
    return 'contacts_only' if parts else 'empty'


def substitution(V, m, u, offsets):
    t = (m+u)/V
    ds = [distance(v*t+F(v*offsets[v], V)) for v in RESIDUAL]
    ds.append(distance(V*t))
    assert min(ds) >= D
    return dict(time=str(t), distances=list(map(str, ds)),
                kind='strict' if min(ds) > D else 'equality')


def lap_result(V, m, offsets, patterns_by_lap):
    sources = {v: (m+offsets[v]) % V for v in RESIDUAL}
    patterns = {v: patterns_by_lap[sources[v]][v] for v in RESIDUAL}
    parts = local_allowed(patterns)
    duration = sum((b-a for a, b in parts), F(0))
    isolated = [a for a, b in parts if a == b]
    witnesses = [substitution(V, m, u, offsets) for u in isolated]
    positive = [(a, b) for a, b in parts if a < b]
    witness_u = ((positive[0][0]+positive[0][1])/2 if positive
                 else isolated[0] if isolated else None)
    witness = substitution(V, m, witness_u, offsets) if witness_u is not None else None
    if positive:
        assert witness['kind'] == 'strict'
    return dict(m=m, source_lap11=sources[11],
                patterns=[dict(speed=v, source_lap=sources[v],
                               blockers=encode_pattern(patterns[v])) for v in RESIDUAL],
                allowed_u=encoded(parts), duration_u=str(duration),
                duration_t=str(duration/V), isolated_u=list(map(str, isolated)),
                status=classify(parts), witness_u=str(witness_u) if witness_u is not None else None,
                witness_t=witness, isolated_t_witnesses=witnesses)


def normalized_signature(row):
    return {key: row[key] for key in ('allowed_u', 'duration_u', 'isolated_u', 'status')}


def inventory(patterns):
    return digest(sorted([encode_pattern(p) for p in patterns], key=canonical))


def offset_summary(V, s, laps):
    duration = sum((F(r['duration_u']) for r in laps), F(0))
    contacts = []
    full = []
    for row in laps:
        m = row['m']
        full += [[str((m+F(a))/V), str((m+F(b))/V)] for a, b in row['allowed_u']]
        contacts += [str((m+F(u))/V) for u in row['isolated_u']]
    assert len(contacts) == len(set(contacts))
    return dict(s=s, phase11=str(F(11*s, V) % 1),
                total_u_duration=str(duration), total_t_duration=str(duration/V),
                global_status=('positive_duration' if duration > 0
                               else 'contacts_only' if contacts else 'empty'),
                isolated_contact_count=len(contacts), normalized_contact_count=len(contacts),
                contacts_t=contacts, full_allowed_t=full,
                local_statuses=[r['status'] for r in laps], laps=laps)


def run_case(case):
    V = case['velocities'][-1]
    assert tuple(case['velocities'][1:-1]) == RESIDUAL
    base_patterns = [{v: pattern(V, v, m) for v in RESIDUAL} for m in range(V)]
    base_inventory = {v: inventory([row[v] for row in base_patterns]) for v in RESIDUAL}
    offsets = []
    for s in range(V):
        shifts = {v: (s if v == 11 else 0) for v in RESIDUAL}
        laps = [lap_result(V, m, shifts, base_patterns) for m in range(V)]
        inv = {v: inventory([base_patterns[(m+shifts[v]) % V][v] for m in range(V)])
               for v in RESIDUAL}
        assert inv == base_inventory
        row = offset_summary(V, s, laps)
        row['runner_pattern_inventory_sha256'] = [[v, inv[v]] for v in RESIDUAL]
        row['per_runner_pattern_multisets_preserved'] = True
        offsets.append(row)
    base = offsets[0]
    controls = []
    for s in range(V):
        shifts = {v: s for v in RESIDUAL}
        laps = [lap_result(V, m, shifts, base_patterns) for m in range(V)]
        for m, row in enumerate(laps):
            assert normalized_signature(row) == normalized_signature(base['laps'][(m+s) % V])
        total = sum((F(r['duration_u']) for r in laps), F(0))
        contacts = sum(len(r['isolated_u']) for r in laps)
        assert total == F(base['total_u_duration'])
        assert contacts == base['isolated_contact_count']
        controls.append(dict(s=s, source_laps=[(m+s) % V for m in range(V)],
                             total_u_duration=str(total), total_t_duration=str(total/V),
                             isolated_contact_count=contacts,
                             lap_permutation_verified=True,
                             normalized_lap_signatures_sha256=digest([
                                 normalized_signature(r) for r in laps])))
    def first_change(predicate):
        return next((r['s'] for r in offsets[1:] if predicate(r)), None)
    local_exists = [r != 'empty' for r in base['local_statuses']]
    changes = dict(
        total_duration=first_change(lambda r: r['total_t_duration'] != base['total_t_duration']),
        local_existence=first_change(lambda r: [x != 'empty' for x in r['local_statuses']] != local_exists),
        local_three_way_status=first_change(lambda r: r['local_statuses'] != base['local_statuses']),
        global_existence=first_change(lambda r: (r['global_status'] != 'empty') != (base['global_status'] != 'empty')),
        global_three_way_status=first_change(lambda r: r['global_status'] != base['global_status']),
        isolated_contact_count=first_change(lambda r: r['isolated_contact_count'] != base['isolated_contact_count']))
    return dict(id=case['id'], V=V, velocities=case['velocities'], residual_speeds=list(RESIDUAL),
                original_patterns=[dict(m=m, patterns=[dict(speed=v, blockers=encode_pattern(row[v]))
                                    for v in RESIDUAL]) for m, row in enumerate(base_patterns)],
                runner_pattern_inventory_sha256=[[v, base_inventory[v]] for v in RESIDUAL],
                offsets=offsets, earliest_nonzero_changes=changes, all_shift_control=controls)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assert sha256(PROTOCOL.read_bytes()).hexdigest() == PROTOCOL_SHA
    protocol = json.loads(PROTOCOL.read_text())
    result = dict(status='OBSERVED finite shifted-start thought experiment; s=0 alone is common-start',
                  protocol_sha256=PROTOCOL_SHA,
                  script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  schema_version=1,
                  normalized_window=[str(A), str(B)],
                  cases=[run_case(case) for case in protocol['cases']])
    if args.write:
        OUT.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(OUT.read_text()), 'phase_results.json differs'
    print(json.dumps(dict(status='PASS', outcomes=[dict(
        id=c['id'], earliest_changes=c['earliest_nonzero_changes'],
        offsets=[dict(s=r['s'], duration=r['total_t_duration'], status=r['global_status'],
                      contacts=r['isolated_contact_count']) for r in c['offsets']])
        for c in result['cases']]), indent=2))


if __name__ == '__main__':
    main()
