"""Translate inputs into the frozen discovery rule; no ranking edits.

Original (x,y) becomes (u,v)=(y,x), with g=qu-v. The mathematical input
is six-form parent geometry. Known B optima do not enter this program.
"""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN = ROOT / 'reviews/2026-09-29-cc-segment-discovery'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def translate(data):
    transformed = json.loads(json.dumps(data))
    transformed['rows'] = [[b, a] for a, b in data['rows']]
    for parent in transformed['parents']:
        parent['vertices'] = [[y, x, z] for x, y, z in parent['vertices']]
        parent['constraints'] = [[name, [normal[1], normal[0], normal[2]], bound]
                                 for name, normal, bound in parent['constraints']]
    transformed['translation'] = {'coordinates': 'u=y,v=x', 'orbit': 'g=qu-v=-H',
                                   'clock': 't=u', 'fold': 'v<=1/2',
                                   'added_row': [2, 5]}
    return transformed


def main():
    spec = importlib.util.spec_from_file_location('frozen_discovery', FROZEN/'discover.py')
    frozen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(frozen)
    # Bind a translated input coefficient; no source or algorithm edits.
    frozen.ADDED_ROW = (2, 5)
    original = json.loads((FROZEN/'PARENT_INPUT.json').read_text())
    data = translate(original)
    records, counts = frozen.candidates(data)
    cover = frozen.build_cover(records)
    rows = tuple(map(tuple, data['rows'])) + ((2, 5),)
    native_rows = tuple((b, a) for a, b in rows)
    z = F(data['threshold'])
    for s in records:
        for u, v in s['endpoints']:
            assert z <= u <= 1-z and z <= v <= F(1, 2)
            assert all(z <= a*u+b*v-m <= 1-z for (a, b), m in zip(rows, s['labels']))
        if s['tail_cutoff'] is not None:
            assert s['tail_cutoff']*s['dx']-s['dy'] >= 1
    # Freeze choice objects before reading any archived candidate output.
    choice_snapshot = json.dumps(frozen.encode(cover), sort_keys=True)
    old = json.loads((FROZEN/'discovery.json').read_text())
    old_by_id = {s['id']:s for s in old['candidates']}
    assert set(old_by_id) == {s['id'] for s in records}
    for s in records:
        archived = old_by_id[s['id']]
        unswapped = sorted((v, u) for u, v in s['endpoints'])
        assert unswapped == sorted(tuple(map(F, p)) for p in archived['endpoints'])
        assert list(s['labels']) == archived['labels']
        assert list(map(str, s['source_parameters'])) == archived['source_parameters']
    assert choice_snapshot == json.dumps(frozen.encode(cover), sort_keys=True)
    controls = []
    display_order = (1, 0, 2, 3, 4, 5, 6)
    if cover['status'] == 'COMPLETE COVER CERTIFICATE':
        for q in range(2, 26):
            cert = frozen.witness(cover, q, rows)
            u, v = cert['point'];g=cert['h'];H=-g
            x,y=v,u
            assert q*y-x==g and x-q*y==H and cert['time']==y
            speeds_native = [a*q+b for a,b in native_rows]
            laps_native = cert['physical_laps']
            speeds = [speeds_native[i] for i in display_order]
            laps = [laps_native[i] for i in display_order]
            assert speeds == [1,q,q+1,2*q+1,3*q+1,3*q+2,5*q+2]
            checks=[]
            for t,expected_laps in ((u,laps),(1-u,[speed-1-ell for speed,ell in zip(speeds,laps)])):
                positions=[speed*t for speed in speeds]
                actual_laps=[frozen.floor(p) for p in positions]
                phases=[p-ell for p,ell in zip(positions,actual_laps)]
                distances=[min(f,1-f) for f in phases]
                assert actual_laps == expected_laps and min(distances)>=z
                checks.append({'time':t,'laps':actual_laps,'phases':phases,
                               'distances':distances,'minimum':min(distances)})
            cert.update({'g':g,'H':H,'native_point':(x,y,z),
                         'native_speeds':speeds_native,'display_speeds':speeds,
                         'display_laps':laps})
            controls.append({'certificate':cert,'physical':checks})
    out={'status':cover['status'],'scope':'B ray; integer q>=2; one closed 1/8-safe witness',
         'translation':data['translation'],'display_order':display_order,
         'frozen_source_sha256':sha(FROZEN/'discover.py'),
         'input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in
                         (FROZEN/'PARENT_INPUT.json',FROZEN/'discovery.json')},
         'script_sha256':sha(Path(__file__)),
         'choice_snapshot_sha256':hashlib.sha256(choice_snapshot.encode()).hexdigest(),
         'geometry_comparison':'all native endpoints, labels, IDs and source parameters unchanged',
         'candidates':records,'cover':cover,'physical_controls':controls,
         'summary':{**counts,'candidate_records':len(records),
                    'positive_clock_span_records':sum(s['dx']>0 for s in records),
                    'chosen_count':len(cover.get('chosen_ids',[])),'cutoff':cover.get('cutoff'),
                    'physical_q_count':len(controls),'physical_times':2*len(controls),
                    'distance_evaluations':14*len(controls),'new_physical_q_values':0},
         'provenance':'Coordinator adapter over frozen code; separately authored team checks follow'}
    print(json.dumps(frozen.encode(out),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
