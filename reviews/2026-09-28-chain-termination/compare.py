"""Compare independently produced exact records; no new cases or scans."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    primary = json.loads((HERE/'results.json').read_text())
    oracle = json.loads((HERE/'verification.json').read_text())
    assert primary['status'] == oracle['status'] == 'pass'
    assert len(primary['cases']) == len(oracle['cases']) == 12
    field_count = 0
    mapping = dict(final_residual_safe='final_safe', H_at_start='H_start', K_used='K')
    direct = ('id','speeds','window','earliest','final_time','calls','completed_rounds',
        'started_rounds','nonzero_moves','consecutive_overlaps','union_span',
        'selected_excess','selected_excess_from_start','H_union_difference',
        'H_start_difference','Q','eta','Hmax','m_L','K_global','K_phase')
    for p, v in zip(primary['cases'], oracle['cases']):
        for field in direct:
            assert p[field] == v[field], (p['id'], field)
            field_count += 1
        for pk, vk in mapping.items():
            assert p[pk] == v[vk], (p['id'], pk, vk)
            field_count += 1
        assert p['verdict'] == ('empty' if v['verdict']=='empty' else 'earliest_witness')
        field_count += 1
        assert len(p['trace']) == len(v['trace'])
        for a, b in zip(p['trace'], v['trace']):
            assert a == b, (p['id'], a, b)
            field_count += len(a)
        assert len(p['selected_intervals']) == len(v['selected_intervals'])
        for a, b in zip(p['selected_intervals'], v['selected_intervals']):
            assert a['meeting'] == b['occurrence']
            for field in ('runner','left','right'):
                assert a[field] == b[field]
            field_count += 4
        assert p['H_union_difference'] == v['actual_excess_union']
        assert p['H_start_difference'] == v['actual_excess_from_start']
        field_count += 2
    rows = {c['id']:c for c in oracle['cases']}
    assert rows['tight_13']['first_component'] == ['3/8','3/8']
    assert rows['small_gcd_113']['first_component'] == ['129/448','167/576']
    assert rows['common_start_lift_clipped']['all_components'] == []
    lift = rows['common_start_lift_extended']
    assert lift['first_component'] == [lift['earliest'],lift['earliest']]
    assert lift['trace'][22]['output'] == lift['earliest']
    assert all(t['input']==t['output'] for t in lift['trace'][23:])
    counts = dict(cases=12, scalar_calls=sum(c['calls'] for c in oracle['cases']),
        nonzero_moves=sum(c['nonzero_moves'] for c in oracle['cases']),
        exact_field_comparisons=field_count,
        threshold_events=sum(c['threshold_count'] for c in oracle['cases']),
        union_partition_cells=sum(c['union_partition_cells'] for c in oracle['cases']),
        start_partition_cells=sum(c['start_partition_cells'] for c in oracle['cases']),
        empty_windows=sum(c['verdict']=='empty' for c in oracle['cases']),
        max_started_rounds=max(c['started_rounds'] for c in oracle['cases']))
    names = ['protocol.json','primary.py','results.json','verify.py','verification.json','compare.py']
    data = dict(status='pass', counts=counts,
        sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in names},
        review_limit='Separate AI implementation and mathematical challenge; not external human review, novelty review, or a proof by finite testing.')
    (HERE/'comparison.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


if __name__ == '__main__':
    main()
