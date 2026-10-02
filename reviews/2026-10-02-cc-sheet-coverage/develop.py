"""Development only: old 407 cases, archived misses, and auxiliary checks."""
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import ceil, floor, lcm
from pathlib import Path
import criterion as c

HERE = Path(__file__).resolve().parent


def run():
    checks = Counter()
    for n, m, a, b in itertools.product(range(9), range(1, 10), range(-10, 11), range(-10, 11)):
        assert c.floor_sum(n, m, a, b) == sum((a*j+b)//m for j in range(n))
        checks["signed_floor_sum"] += 1
    for n, m, a, b in itertools.product(range(9), range(2, 13), range(-4, 5), range(-4, 5)):
        lo, hi = ceil(F(m, 8)), floor(F(7*m, 8))
        expected = [j for j in range(n) if lo <= (a*j+b) % m <= hi]
        first, count = c.first_residue(n, m, a, b, lo, hi)
        assert count == len(expected) and first == (expected[0] if expected else None)
        checks["inclusive_residue_first_and_count"] += 1
    c.COUNTS.clear()
    raw = (c.ROOT/'reviews/2026-09-30-cc-three-parameter/discovery.json').read_bytes()
    previous = json.loads(raw)
    src = c.old.sources()
    sheets = c.old.objects(src)["sheets"]
    old_menu = previous["menus"]["sheets"]["indices"]
    archived = sorted((row for row in previous["cases"] if row["split"] != "scaling_control"),
                      key=lambda row: tuple(row["pqr"]))
    assert len(archived) == 407
    rows, failures, reasons = [], [], Counter()
    for row in archived:
        lat = c.old.lattice(row["pqr"])
        decisions = [c.contact(sheet, lat) for sheet in sheets]
        bits = ''.join('1' if decision['hit'] else '0' for decision in decisions)
        assert bits == row['hits']['sheets'], row['pqr']
        checks['archived_contact_bits'] += 36
        for i, decision in enumerate(decisions):
            reasons[decision['reason']] += 1
            if decision['hit']:
                c.old.witness(row['pqr'], lat, sheets[i], decision['hit'], src)
                checks['development_physical_witnesses'] += 1
        rows.append({'pqr': row['pqr'], 'bits': bits})
        if not any(bits[i] == '1' for i in old_menu):
            selected_details = []
            for i in old_menu:
                detail = decisions[i]
                h0, h1 = detail['h_range']
                phases = []
                if h0 != h1:
                    for h in range(detail['integer_h_bounds'][0], detail['integer_h_bounds'][1]+1):
                        s = (h-h0)/(h1-h0)
                        x, y, _ = c.old.at(sheets[i], s, F(0))
                        phase = (lat['normalized'][2]*(lat['a']*x+lat['b']*y)) % 1
                        phases.append({'h': h, 'r_phase': phase})
                selected_details.append({'source': i, 'id': src[i]['id'],
                                         **detail, 'pair_contact_phases': phases})
            failures.append({'pqr': row['pqr'], 'd': lat['d'], 'selected_sheet_diagnostics': selected_details,
                             'archived_fallback': row['class_fallback']['sheets']})
    assert len(failures) == 8 and all(row['d'] == 1 for row in failures)
    # Auxiliary inputs exercise constant h and vertical-width boundaries.
    auxiliary = [
        ((1, 2, 3), [[F(1, 8), F(1, 4)], [F(1, 4), F(1, 2)]]),
        ((1, 2, 8), [[F(1, 8), F(1, 4)]]*2),
        ((1, 2, 1), [[F(1, 8), F(1, 4)]]*2),
        ((1, 2, 7), [[F(1, 8), F(1, 4)]]*2),
        ((2, 4, 1), [[F(1, 8), F(1, 4)]]*2),
        ((1, 2, 3), [[F(1, 8), F(1, 3)]]*2),
    ]
    auxiliary_rows = []
    for v, endpoints in auxiliary:
        obj = {'endpoints': endpoints, 'z_range': [F(1, 8), F(7, 8)]}
        lat = c.old.lattice(v)
        decision = c.contact(obj, lat)
        prior = c.old.intersect(obj, lat['relations'])
        assert decision['hit'] == prior
        auxiliary_rows.append({'pqr': v, 'endpoints': endpoints, 'decision': decision})
    # Constructed development obstruction, outside the fresh box. No scan in r.
    physical = c.load_module('old_physical_checker', 'reviews/2026-09-30-cc-three-parameter/verify.py')
    pair_times, per_source = set(), []
    for i, source in enumerate(src):
        A, B = source['endpoints']
        h0, h1 = 2*A[0]-A[1], 2*B[0]-B[1]
        assert A == B or h0 != h1
        times = []
        if A == B:
            if h0.denominator == 1:
                times = [A[0]]
        else:
            for h in range(ceil(min(h0, h1)), floor(max(h0, h1))+1):
                s = (h-h0)/(h1-h0)
                times.append(A[0]+s*(B[0]-A[0]))
        pair_times.update(times)
        per_source.append({'source': i, 'id': source['id'], 'pair_times': times})
    assert pair_times == {F(1, 8), F(7, 40), F(3, 8)}
    resonance = lcm(*(t.denominator for t in pair_times))
    triple = (1, 2, resonance)
    lat = c.old.lattice(triple)
    obstruction_bits = ''.join('1' if c.contact(sheet, lat)['hit'] else '0' for sheet in sheets)
    assert obstruction_bits == physical.physical_contacts(triple, src)['sheets'] == '0'*36
    t = F(25, 152)
    phases = [(v*t) % 1 for v in c.old.speeds(triple)]
    assert all(F(1, 8) <= phase <= F(7, 8) for phase in phases)
    core_interval = [F(25, 152), F(7, 40)]
    labels = [floor(v*core_interval[0]) for v in c.old.speeds((1, 2, 40))[:8]]
    for end in core_interval:
        assert all(F(1, 8) <= v*end-label <= F(7, 8)
                   for v, label in zip(c.old.speeds((1, 2, 40))[:8], labels))
    obstruction = {'status': 'CONSTRUCTED_DEVELOPMENT_COUNTEREXAMPLE', 'pqr': triple,
        'pair_times': sorted(pair_times), 'per_source': per_source, 'resonance_lcm': resonance,
        'all_sheet_bits': obstruction_bits, 'physical_bits_agree': True,
        'physical_witness': {'time': t, 'phases': phases},
        'full8_intervals': physical.safe_intervals(c.old.speeds(triple), F(1, 8)),
        'core_interval': core_interval, 'core_physical_laps': labels,
        'core_width': core_interval[1]-core_interval[0],
        'family': 'p=1,q=2,r=40*k, integer k>=1; see DERIVATION.md for analytic argument',
        'not_a_lonely_runner_counterexample': True}
    menu = c.greedy(rows)
    artifact = {'status': 'PASS_DEVELOPMENT_ONLY', 'archive_sha256': hashlib.sha256(raw).hexdigest(),
                'domain': 'The previously exposed 407 primitive cases in [1,9]^3; no fresh validation evaluated',
                'checks': checks, 'criterion_reasons': reasons, 'criterion_counts': c.COUNTS,
                'old_menu': old_menu, 'new_menu': menu, 'development_rows': rows,
                'eight_old_misses': failures, 'auxiliary_cases': auxiliary_rows,
                'resonance_obstruction': obstruction,
                'limits': 'Same-author development and alternate arithmetic; not fresh validation or independent proof review.'}
    (HERE/'DEVELOPMENT.json').write_text(json.dumps(artifact, default=c.old.encode, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: artifact[k] for k in ('status', 'checks', 'criterion_reasons', 'old_menu', 'new_menu')}, default=c.old.encode))


if __name__ == '__main__':
    run()
