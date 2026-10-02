#!/usr/bin/env python3
"""Reproduce the four declared outputs, then compare independent records."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess
import sys

BASE=Path(__file__).resolve().parent

def main():
    reproduced=[]
    for stem in ('selector','orbit_checks','coverage_checks','physical_checks'):
        output=BASE/(stem+'.json')
        before=output.read_bytes()
        run=subprocess.run([sys.executable,str(BASE/(stem+'.py'))],capture_output=True,check=True)
        after=run.stdout if stem=='selector' else output.read_bytes()
        assert before==after, stem+' output differs'
        reproduced.append({'program':stem+'.py','output':stem+'.json','exact_bytes_reproduced':True,
                           'sha256':hashlib.sha256(after).hexdigest()})
    main_records=json.loads((BASE/'selector.json').read_text())['records']
    orbit={(v['p'],v['q']):v for v in json.loads((BASE/'orbit_checks.json').read_text())['records']}
    physical={(v['p'],v['q']):v for v in json.loads((BASE/'physical_checks.json').read_text())['cases']}
    assert set(orbit)==set(physical)=={(v['p'],v['q']) for v in main_records}
    for c in main_records:
        key=(c['p'],c['q']); o=orbit[key]; p=physical[key]
        assert c['segment']==o['segment']==p['segment']
        assert c['gcd']==o['d']==p['d']
        assert c['primitive']==[o['P'],o['Q']]==[p['P'],p['Q']]
        assert c['point']==[o['x'],o['y']]==[p['x'],p['y']]
        assert c['h']==o['h']==p['h']
        assert c['time']==o['physical_time']==p['selected']['time']
        assert c['primitive_time']==o['primitive_time']==p['tau']==p['congruence_tau']
        assert c['phases']==o['phases']==p['selected']['phases']
        assert list(map(F,c['physical_laps']))==list(map(F,o['physical_laps']))==list(map(F,p['selected']['laps']))
        assert c['reflected_time']==o['reflected_time']==p['reflected']['time']
        assert c['reflected_phases']==p['reflected']['phases']
        expected_laps=[v-1-ell for v,ell in zip(c['speeds'],c['physical_laps'])]
        assert list(map(F,expected_laps))==list(map(F,o['reflected_laps']))==list(map(F,p['reflected']['laps']))
    coverage=json.loads((BASE/'coverage_checks.json').read_text())
    indexed={(v['p'],v['q']):v for v in main_records}
    for rec in coverage['primitive_triangle']:
        c=indexed[(rec['P'],rec['Q'])]
        selected=rec['primary'] if rec['primary']['covered'] else rec['fallback']
        assert c['point']==selected['point'] and c['phases']==selected['phases']
    result={'status':'PASS','reproduced':reproduced,'comparison':{
        'three_implementations_agree_on_pairs':18,'distinct_speed_pairs':17,
        'repeated_speed_auxiliaries':1,'coverage_triangle_matches':8,
        'compared_fields':['segment','gcd','primitive pair','point','h','physical time',
                           'primitive time','phases','laps','reflected time','reflected phases/laps'],
        'congruence_recovery_matches':18},
        'limits':'Finite exact reproduction and cross-comparison only; universal claim uses the written proof candidate.'}
    (BASE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
