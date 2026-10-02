#!/usr/bin/env python3
"""Compare all frozen and separately labelled follow-on exact records."""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'results.json').read_text())
v=json.loads((HERE/'verification.json').read_text())
rows={r['id']:r for r in p['physical_cases']+p['auxiliary_cases']}
seen=set()
for r in v['cases']:
    c=rows[r['case_id']]
    seen.add(c['id'])
    for key in ('speeds','phases','window','core','triple_wait_bound'):
        assert c[key]==r[key],(c['id'],key)
    assert c['slow_safe_width']==r['slow_safe_lap_width']
    assert F(c['bound_minus_width'])==-F(r['condition_margin'])
    assert c['condition_passes']==r['condition_pass']
    assert c['final_time']==r['fixed22_final']
    assert c['final_safe']==r['fixed22_final_safe']
    assert c['earliest_in_window']==r['oracle_earliest']
    assert c['first_component']==r['oracle_first_component']
    assert len(c['diagnostic_trace'])==len(r['fixed22_trace'])==22
    for a,b in zip(c['diagnostic_trace'],r['fixed22_trace']):
        for key in ('runner_index','speed','input','output'):
            assert a[key]==b[key],(c['id'],key)
    if c['core']:
        assert r['core_window_certified']
assert seen==set(rows) and len(seen)==10

f=json.loads((HERE/'follow_on.json').read_text())
w=json.loads((HERE/'follow_on_verification.json').read_text())
aliases={'auxiliary_equal':'aux_equal','auxiliary_distinct':'aux_distinct'}
rows={r['id']:r for r in f['cases']}
seen=set()
for r in w['cases']:
    key=aliases.get(r['case_id'],r['case_id'])
    c=rows[key]
    seen.add(key)
    for name in ('speeds','phases','anchor','anchor_phases','core','window','extended_window'):
        assert c[name]==r[name],(key,name)
    assert F(c['slow_safe_width'])-F(c['condition_bound'])==F(r['condition_margin'])
    assert c['final_time']==r['fixed22_final']
    assert [F(x)>=0 for x in c['final_margins']]==r['fixed22_safe_flags']==[False,True,True,True]
    assert c['later_witness_step23']==r['first_witness_after_left']
    assert r['window_is_empty']
    assert r['full_allowed_set_in_extended_window']==[[c['later_witness_step23']]*2]
    assert c['extended_window_has_witness']
    assert len(c['trace'])==len(r['fixed22_trace'])==22
    for a,b in zip(c['trace'],r['fixed22_trace']):
        assert a['runner']==b['runner_index']
        assert a['input']==b['input'] and a['output']==b['output']
    assert len(c['cover_chain'])==len(r['open_blocking_cover'])==7
    for a,b in zip(c['cover_chain'],r['open_blocking_cover']):
        assert a['runner']==b['runner_index']
        assert a['relative_meeting_label']==b['relative_lap']
        assert a['left']==b['left'] and a['right']==b['right']
    if c['core']:
        assert r['core_extended_window_certified']
assert seen==set(rows) and len(seen)==3
print(json.dumps({'status':'pass','frozen_cases':10,'frozen_trace_outputs':220,
                  'follow_on_cases':3,'follow_on_trace_outputs':66,'open_cover_intervals':21,
                  'later_witnesses':3,'common_start_counterexample':'verified'}))
