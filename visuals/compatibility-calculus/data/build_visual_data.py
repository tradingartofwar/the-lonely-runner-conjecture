#!/usr/bin/env python3
"""Deterministic browser data from pinned exact certificates; no prose parsing.

All construction uses Fraction. Floats are rendering conveniences only.
Run from any directory. --check compares outputs without writing them.
"""
import argparse
import hashlib
import json
import re
import subprocess
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]
PIN = '6b2b9316dbc87499a1cb5184aadbd6614d4d6c32'
REPO = 'https://github.com/tradingartofwar/the-lonely-runner-conjecture'
PREFIX = 'reviews/2026-09-29-'
SOURCES = {
    'geometry': PREFIX + 'cc-other-ray-review/geometry_check.json',
    'caps': PREFIX + 'cc-other-ray-review/reconciliation.json',
    'physical_b': PREFIX + 'cc-other-ray-review/physical_check.json',
    'arithmetic_b': PREFIX + 'cc-other-ray-review/arithmetic_check.json',
    'transfer': PREFIX + 'cc-six-seven-transfer/verification.json',
    'transfer_countercheck': PREFIX + 'cc-six-seven-transfer/countercheck.json',
    'selector': PREFIX + 'cc-bounded-selector/verification.json',
    'selector_countercheck': PREFIX + 'cc-bounded-selector/countercheck.json',
    'original_geometry': PREFIX + 'ltcm-spectrum/ambient.json',
    'clock_occurrences': 'reviews/2026-09-25-lr2/lap_constraints.json',
}
NOTES = [
    'AGENTS.md', 'CLAIM_STATUS.md',
    'notes/MATHEMATICAL_BASELINE.md',
    'notes/LAP_LABELLED_CONSTRAINTS.md',
    'notes/DISTINCTION_AUDIT_2026_09_25.md',
    'reviews/2026-09-25-lr2/check_lap_constraints.py',
    'notes/CC_VISUAL_PRESENTATION_PLAN_2026_09_29.md',
    'notes/CC_REPRESENTATION_RULES.md',
    'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md',
    'notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md',
    'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md',
    'notes/CC_BOUNDED_SELECTOR_2026_09_29.md',
]
ROWS = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2)]
B_CONTROLS = [2, 3, 4, 5, 6, 7]
A_CONTROLS = [3, 4, 5, 6, 10]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source_bytes(path):
    """Keep the visual's mathematical snapshot stable as research continues."""
    return subprocess.check_output(['git', 'show', f'{PIN}:{path}'], cwd=ROOT)


def fraction(value):
    q = F(value)
    return {'num': q.numerator, 'den': q.denominator, 'text': str(q), 'float': float(q)}


def exact(value):
    if isinstance(value, F):
        return fraction(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(?:/\d+)?', value):
        return fraction(value)
    if isinstance(value, (tuple, list)):
        return [exact(v) for v in value]
    if isinstance(value, dict):
        return {k: exact(v) for k, v in value.items()}
    return value


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()


def speeds(ray, q):
    return [1, q, q+1, q+2, q+3, 2*q+3, 2*q+5] if ray == 'A' else [1, q, q+1, 2*q+1, 3*q+1, 3*q+2, 5*q+2]


def witness(ray, q, t):
    runners = []
    for v in speeds(ray, q):
        lap = (v*t).__floor__()
        phase = v*t-lap
        runners.append({'speed': v, 'lap': lap, 'phase': phase, 'distance': min(phase, 1-phase)})
    minimum = min(r['distance'] for r in runners)
    return {'time': t, 'minimum': minimum, 'runners': runners,
            'active_speeds': [r['speed'] for r in runners if r['distance'] == minimum]}


def contact(cap, q):
    p = cap['peak']
    h0 = p[0]-q*p[1]
    directions = [r[0]-q*r[1] for r in cap['rays']]
    low, high = min(directions), max(directions)
    rho = h0-h0.__floor__()
    if rho == 0:
        loss, direction_index, h = F(0), None, int(h0)
    else:
        candidates = [(rho/-low, directions.index(low), h0.__floor__()),
                      ((1-rho)/high, directions.index(high), h0.__ceil__())]
        loss, direction_index, h = min(candidates)
    in_cap = loss <= F(1, 42)
    point = p if direction_index is None else [p[i]+loss*cap['rays'][direction_index][i] for i in range(3)]
    return {'cap': cap['id'], 'cell': cap['cell'], 'h0': h0, 'directions': directions,
            'd_min': low, 'd_max': high, 'rho': rho, 'loss': loss,
            'direction_index': direction_index, 'orbit_integer': h, 'in_cap': in_cap,
            'point': point if in_cap else None,
            'interval': [h0+loss*low, h0+loss*high] if in_cap else None}


def joint_visual(src):
    """Derived display controls for the pinned q=4 marginal counterexample."""
    record = src['transfer']['marginal_projection_counterexample']
    parent = src['transfer']['parents'][record['parent_index']]
    z, q = F(record['height']), record['q']
    triangle = [list(map(F, p)) for p in parent['vertices'] if F(p[2]) == z]
    image = [[q*x-y, 5*x+2*y] for x,y,_ in triangle]
    h, s = map(F, record['false_positive_pair'])
    fake = [(s+2*h)/(2*q+5), (q*s-5*h)/(2*q+5), z]
    fake_check = witness('A', q, fake[0])
    failed = [r['speed'] for r in fake_check['runners'] if r['distance'] < z]
    assert failed == [6]
    section = [list(map(F,p)) for p in record['conditional_section_endpoints']]
    low, high = map(F, record['conditional_S_range'])
    collision_ratio = (F(2)-low)/(high-low)
    collision_point = [section[0][i]+collision_ratio*(section[1][i]-section[0][i]) for i in range(3)]
    assert collision_ratio == F(6,13) and collision_point[0] == F(4,13)
    slice_controls = []
    for position in range(14):
        p = [section[0][i]+F(position,13)*(section[1][i]-section[0][i]) for i in range(3)]
        slice_controls.append({'position':position,'point':p,'witness':witness('A',q,p[0])})
    return {'q':q, 'threshold':z, 'parent_index':record['parent_index'],
            'parent_labels':parent['labels'], 'triangle_xy':triangle, 'triangle_hs':image,
            'section_xy':section, 'conditional_S':[low,high],
            'marginal_H':list(map(F,record['marginal_H_range'])),
            'marginal_S':list(map(F,record['marginal_S_range'])),
            'orbit_integer':int(h), 'fake_hs':[h,s], 'fake_xy':fake,
            'fake_physical':fake_check, 'fake_failed_speeds':failed,
            'safe_child_xy':list(map(F,record['only_child_point'])),
            'safe_child_H':F(record['child_H']),
            'safe_band_edges':[F(2)-z,F(2)+z], 'collision_ratio':collision_ratio,
            'collision_point':collision_point, 'collision_physical':witness('A',q,collision_point[0]),
            'slice_controls':slice_controls,
            'full_safe_times':[F(i,8) for i in [1,3,5,7]],
            'source':SOURCES['transfer'],
            'status':'REPRODUCED — exact q=4 counterexample; derived display controls are same-author checks'}



def orbit_section(poly, q, h):
    """Intersect a bounded certified polytope with H=qx-y using its edges."""
    vertices=[list(map(F,v)) for v in poly['vertices']]
    points={tuple(v) for v in vertices if q*v[0]-v[1]==h}
    for i,j in poly['edges']:
        a,b=vertices[i],vertices[j]
        ha,hb=q*a[0]-a[1],q*b[0]-b[1]
        if min(ha,hb)<h<max(ha,hb):
            r=(F(h)-ha)/(hb-ha)
            points.add(tuple(a[k]+r*(b[k]-a[k]) for k in range(3)))
    return [list(v) for v in sorted(points)]


def transfer_visual(src):
    """Three exact before/after controls, not intermediate physical systems."""
    atlas=src['transfer']
    result=[]
    for name,q,pi,h in [('removed',4,2,1),('equality',4,4,1),('face',10,7,4)]:
        parent=atlas['parents'][pi]
        children=[(i,c) for i,c in enumerate(atlas['children']) if c['parent_index']==pi]
        before=orbit_section(parent,q,h)
        after=[{'child_index':i,'points':orbit_section(c,q,h)} for i,c in children]
        old=max(before,key=lambda p:p[2])
        remaining=[p for c in after for p in c['points']]
        new=max(remaining,key=lambda p:p[2]) if remaining else None
        old_physical=witness('A',q,old[0]);new_physical=witness('A',q,new[0]) if new else None
        assert min(r['distance'] for r in old_physical['runners'][:6])==old[2]
        if new:assert new_physical['minimum']==new[2]
        singleton_orbits=[{'child_index':i,'point':list(map(F,c['vertices'][0])),
                           'H':q*F(c['vertices'][0][0])-F(c['vertices'][0][1])}
                          for i,c in children if c['dimension']==0]
        result.append({'id':name,'q':q,'parent_index':pi,'orbit_integer':h,
                       'child_indices':[i for i,c in children], 'parent_section':before,
                       'child_sections':after, 'before_point':old,'after_point':new,
                       'before_physical':old_physical,'after_physical':new_physical,
                       'before_reflected':witness('A',q,1-old[0]),
                       'after_reflected':witness('A',q,1-new[0]) if new else None,
                       'singleton_orbits':singleton_orbits,
                       'source':SOURCES['transfer'],
                       'status':'REPRODUCED — exact finite parent/child and orbit controls'})
    return result



def selector_visual(src):
    """Derive both projected intervals; retain the pinned E1-then-E2 order."""
    segments=[]
    for raw in src['selector']['segments']:
        endpoints=[list(map(F,p['point'])) for p in raw['endpoints']]
        a,b=endpoints
        d=(a[1]-b[1])/(b[0]-a[0]);c=a[1]+d*a[0]
        segments.append({'segment':raw['segment'],'parent':raw['parent'],
                         'endpoints':endpoints,'torus_laps':raw['torus_laps'],
                         'c':c,'d':d,'x_interval':[a[0],b[0]]})
    archive={r['certificate']['q']:r['certificate'] for r in src['selector']['physical_controls']}
    controls=[]
    for q in A_CONTROLS:
        trials=[]
        for segment in segments:
            lo,hi=[(q+segment['d'])*x-segment['c'] for x in segment['x_interval']]
            h=lo.__ceil__();accepted=h<=hi
            point=None
            if accepted:
                x=(h+segment['c'])/(q+segment['d']);y=segment['c']-segment['d']*x
                point=[x,y,F(1,8)]
            trials.append({'segment':segment['segment'],'interval':[lo,hi],
                           'width':hi-lo,'first_integer':h,'accepted':accepted,
                           'lower_equality':accepted and h==lo,'upper_equality':accepted and h==hi,
                           'point':point})
        chosen=next(i for i,t in enumerate(trials) if t['accepted'])
        point=trials[chosen]['point'];t=point[0]
        assert trials[chosen]['segment']==archive[q]['segment']
        assert point==list(map(F,archive[q]['point']))
        controls.append({'q':q,'trials':trials,'selected_index':chosen,'attempts':chosen+1,
                         'witness':witness('A',q,t),'reflected':witness('A',q,1-t)})
    return {'segments':segments,'controls':controls,'threshold':F(1,8),
            'source':SOURCES['selector'],'status':'Exact finite controls of the pinned two-segment proof candidate'}


def clock_visual(src):
    """One archived local window; preserve strict blocking and meeting identity."""
    archive=src['clock_occurrences'];case=next(c for c in archive['cases'] if c['replacement']==16)
    window=list(map(F,archive['window']));delta=F(archive['threshold'])
    core=archive['core'];extras=[6,7,11,16];vs=sorted(core+extras)
    episodes=[]
    for e in case['episodes']:
        v,m=e['speed'],e['lap'];a,b=F(e['left']),F(e['right'])
        assert (a,b)==(max(window[0],(m-delta)/v),min(window[1],(m+delta)/v))
        episodes.append({'id':f'v{v}m{m}','speed':v,'meeting':m,'interval':[a,b],
                         'closed':[abs(v*a-m)<delta,abs(v*b-m)<delta]})
    by_label={(e['speed'],e['meeting']):e for e in episodes}
    pairs=[]
    for edge in case['positive_pair_edges']:
        a,b=[by_label[tuple(label)] for label in edge['episodes']]
        lo=max(a['interval'][0],b['interval'][0]);hi=min(a['interval'][1],b['interval'][1])
        assert hi-lo==F(edge['duration'])
        def contains(e,t):return abs(e['speed']*t-e['meeting'])<delta
        pair_speeds=sorted([a['speed'],b['speed']])
        pairs.append({'id':'pair-'+ '-'.join(map(str,pair_speeds)),'speeds':pair_speeds,
                      'episodes':[a['id'],b['id']],'interval':[lo,hi],
                      'closed':[all(contains(e,t) for e in [a,b]) for t in [lo,hi]],
                      'duration':hi-lo,'time':(lo+hi)/2})
    safe=[list(map(F,c)) for c in case['clear_cells_closures']]
    assert safe==[[F(17,56),F(39,128)]]
    cuts=sorted(set(window+[v for e in episodes for v in e['interval']]))
    times=sorted(set(cuts+[(a+b)/2 for a,b in zip(cuts,cuts[1:])]+[p['time'] for p in pairs]))
    controls=[]
    for t in times:
        runners=[]
        for v in vs:
            lap=(v*t).__floor__();phase=v*t-lap;distance=min(phase,1-phase);blocked=distance<delta
            runners.append({'speed':v,'lap':lap,'phase':phase,'distance':distance,'blocked':blocked,
                            'meeting':(v*t+F(1,2)).__floor__() if blocked else None})
        controls.append({'time':t,'boundary':t in cuts,'runners':runners,
                         'minimum':min(r['distance'] for r in runners),
                         'active_speeds':[r['speed'] for r in runners if r['blocked']],
                         'active_episodes':[e['id'] for e in episodes if abs(e['speed']*t-e['meeting'])<delta]})
    for p in pairs:p['control_index']=times.index(p['time'])
    return {'source':SOURCES['clock_occurrences'],'window':window,'threshold':delta,
            'core':core,'extras':extras,'speeds':vs,'episodes':episodes,'pairs':pairs,
            'safe_components':safe,'safe_duration':F(case['direct_clear_duration']),
            'safe_indices':[times.index(safe[0][0]),times.index(sum(safe[0])/2),times.index(safe[0][1])],
            'controls':controls,'default_index':next(p['control_index'] for p in pairs if p['speeds']==[6,16]),
            'status':'REPRODUCED — one archived configuration in one closed local window; no family or general theorem'}


def cell_visual(src):
    """Construct each archived label cell by adding its seven closed bands."""
    from itertools import combinations
    def dot(a,b):return sum(x*y for x,y in zip(a,b))
    def determinant(a,b,c):
        return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
    def rank(rows):
        a=[list(map(F,row)) for row in rows];r=0
        for col in range(3):
            p=next((i for i in range(r,len(a)) if a[i][col]),None)
            if p is None:continue
            a[r],a[p]=a[p],a[r];q=a[r][col];a[r]=[x/q for x in a[r]]
            for i in range(r+1,len(a)):
                q=a[i][col];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
            r+=1
        return r
    def poly(constraints):
        vertices=set()
        for triple in combinations(constraints,3):
            rows=[list(map(F,c[0])) for c in triple];bounds=[F(c[1]) for c in triple]
            det=determinant(*rows)
            if not det:continue
            columns=list(zip(*rows))
            point=tuple(determinant(*(columns[:i]+[tuple(bounds)]+columns[i+1:]))/det for i in range(3))
            if all(dot(n,point)<=b for n,b in constraints):vertices.add(point)
        vertices=sorted(vertices)
        dimension=rank([[x-y for x,y in zip(p,vertices[0])] for p in vertices[1:]]) if vertices else -1
        edges=[]
        for i,j in combinations(range(len(vertices)),2):
            active=[n for n,b in constraints if dot(n,vertices[i])==b==dot(n,vertices[j])]
            if rank(active)>=2:edges.append([i,j])
        face_sets=set()
        for n,b in constraints:
            ids=tuple(i for i,v in enumerate(vertices) if dot(n,v)==b)
            if len(ids)>=3 and rank([[x-y for x,y in zip(vertices[i],vertices[ids[0]])] for i in ids[1:]])==2:face_sets.add(ids)
        faces=[]
        for ids in sorted(face_sets):
            order=[ids[0]]
            while len(order)<len(ids):
                candidates=[j if i==order[-1] else i for i,j in edges if order[-1] in [i,j] and i in ids and j in ids]
                nxt=next((i for i in sorted(candidates) if i not in order),None)
                assert nxt is not None
                order.append(nxt)
            faces.append(order)
        return {'vertices':vertices,'edges':edges,'faces':faces,'dimension':dimension}
    frame=[([-1,0,0],F(0)),([1,0,0],F(1,2)),([0,-1,0],F(0)),([0,1,0],F(1)),([0,0,-1],F(-1,8)),([0,0,1],F(1,2))]
    records=[]
    for ci,raw in enumerate(src['geometry']['cells']):
        constraints=frame.copy();stages=[poly(constraints)];bands=[]
        for (a,b),m in zip(ROWS,raw['labels']):
            band=[([-a,-b,1],F(-m)),([a,b,1],F(m+1))]
            bands.append(band);constraints+=band;stages.append(poly(constraints))
        assert set(stages[-1]['vertices'])=={tuple(map(F,p)) for p in raw['vertices']}
        assert stages[-1]['dimension']==raw['dimension']
        records.append({'id':f'C{ci}','labels':raw['labels'],'bands':bands,'stages':stages})
    cases=[]
    parent=src['transfer']['parents'][2]
    for name,labels,n in [('interval',parent['labels'],6),('point',src['geometry']['cells'][5]['labels'],7),('empty',src['geometry']['cells'][3]['labels'],7)]:
        laps=[m+b for m,(a,b) in zip(labels,ROWS)]
        vs=speeds('A',4)[:n];bounds=[[(F(l)+F(1,8))/v,(F(l)+F(7,8))/v] for l,v in zip(laps,vs)]
        lo=max(b[0] for b in bounds);hi=min(b[1] for b in bounds)
        t=(lo+hi)/2 if lo<=hi else None
        cases.append({'id':name,'q':4,'h':1,'count':n,'torus_laps':labels,'physical_laps':laps,'speeds':vs,
                      'bounds':bounds,'lower':lo,'upper':hi,'time':t,
                      'point':[t,4*t-1,F(1,8)] if t is not None else None,
                      'witness':witness('A',4,t) if t is not None else None})
    return {'frame':frame,'cells':records,'lap_cases':cases,'source':SOURCES['geometry'],
            'status':'REPRODUCED — exact finite label cells and three archived q=4 lap controls'}


def opening_visual():
    """A translated consecutive-speed fixture, with all four references.

    The boundary partition is complete: truth can change only where a signed
    relative phase meets delta or 1-delta. Midpoints classify each open piece;
    endpoints are tested separately and retained even when isolated.
    """
    velocities=[1,2,3,4]; delta=F(1,4); references=[]
    controls=[F(0),F(1,4),F(1,3),F(3,8),F(1,2),F(3,4),F(1)]
    for ref,sr in enumerate(velocities):
        relative=[s-sr for s in velocities]
        def state(t):
            absolute=[s*t-(s*t).__floor__() for s in velocities]
            phases=[u*t-(u*t).__floor__() for u in relative]
            distances=[min(p,1-p) for p in phases]
            nearest=min(d for i,d in enumerate(distances) if i!=ref)
            return {'time':t,'absolute':absolute,'relative_phases':phases,
                    'distances':distances,'minimum':nearest,'safe':nearest>=delta,
                    'nearest':[i for i,d in enumerate(distances) if i!=ref and d==nearest]}
        events={F(0),F(1)}
        for v in map(abs,relative):
            if v:
                events.update((m+d)/v for m in range(v) for d in [delta,1-delta])
        cuts=sorted(events)
        pieces=[(t,t) for t in cuts if state(t)['safe']]
        pieces += [(a,b) for a,b in zip(cuts,cuts[1:]) if state((a+b)/2)['safe']]
        components=[]
        for a,b in sorted(pieces):
            if components and a<=components[-1][1]:components[-1][1]=max(b,components[-1][1])
            else:components.append([a,b])
        references.append({'index':ref,'speed':sr,'relative_speeds':relative,'safe_components':components,
                           'witness_time':F(1,4) if ref in [0,3] else F(1,3),
                           'controls':[state(t) for t in controls]})
    return {'velocities':velocities,'total_runners':4,'threshold':delta,'period':F(1),
            'time_denominator':96,'references':references,'control_times':controls,
            'source':'notes/MATHEMATICAL_BASELINE.md',
            'status':'REPRODUCED — finite four-runner illustration of the standard reference change'}


def story_visual(src, b_examples):
    """Closing recaps reuse exact certificates; they introduce no new domain."""
    b=next(r for r in b_examples if r['q']==6)
    c=next(c for c in b['contacts'] if c['cap']==b['winner_caps'][0])
    contact_steps=[]
    for stage,loss in enumerate([F(0),c['loss']/2,c['loss'],c['loss']]):
        interval=[c['h0']+loss*c['d_min'],c['h0']+loss*c['d_max']]
        integers=list(range(interval[0].__ceil__(),interval[1].__floor__()+1))
        contact_steps.append({'stage':stage,'loss':loss,'height':F(1,6)-loss,
                              'interval':interval,'integers':integers,
                              'point':c['point'] if stage>=2 else None,
                              'witness':witness('B',6,c['point'][1]) if stage==3 else None})
    a=next(r for r in src['transfer']['physical_controls'] if r['q']==4)
    components=[list(map(F,p)) for p in a['seven_safe_components_at_1_over_8']]
    positive=[p for p in components if p[0]<p[1]]
    j=joint_visual(src)
    return {'cases':['contact','equality','joint'],'steps':4,
            'contact':{'q':6,'ray':'B','cap':c['cap'],'speeds':b['speeds'],
                       'h0':c['h0'],'maximum':b['maximum'],'times':b['times'],
                       'controls':contact_steps,'source':SOURCES['physical_b']},
            'equality':{'q':4,'ray':'A','threshold':F(1,8),'speeds':speeds('A',4),
                        'components':components,'positive_components':positive,
                        'duration':sum((hi-lo for lo,hi in components),F(0)),
                        'witnesses':[witness('A',4,lo) for lo,hi in components],
                        'source':SOURCES['transfer']},
            'joint':{'q':4,'ray':'A','parent':2,'threshold':j['threshold'],
                     'orbit_integer':j['orbit_integer'],'marginal_H':j['marginal_H'],
                     'marginal_S':j['marginal_S'],'candidate_hs':j['fake_hs'],
                     'candidate_point':j['fake_xy'],'candidate_physical':j['fake_physical'],
                     'failed_speeds':j['fake_failed_speeds'],'conditional_S':j['conditional_S'],
                     'blocking_edges':j['safe_band_edges'],'source':SOURCES['transfer']},
            'status':'REPRODUCED — three finite recaps; all-q assertions retain their pinned proof-candidate status'}


def build():
    src = {key: json.loads(source_bytes(path)) for key, path in SOURCES.items()}
    cells, caps = [], []
    for ci, raw in enumerate(src['geometry']['cells']):
        vertices = [list(map(F, v)) for v in raw['vertices']]
        cell = {**raw, 'id': f'C{ci}', 'vertices': vertices,
                'singleton': raw['dimension'] == 0, 'source': SOURCES['geometry']}
        cells.append(cell)
        if not raw['peak_indices']:
            continue
        peak = vertices[raw['peak_indices'][0]]
        rays = [[F(e['alpha']), F(e['beta']), F(-1)] for e in raw['peak_edges']]
        caps.append({'id': chr(65+len(caps)), 'cell': ci, 'peak': peak, 'rays': rays,
                     'labels': raw['labels'], 'cut_loss': F(1, 42),
                     'vertices': [peak] + [[peak[i]+r[i]/42 for i in range(3)] for r in rays],
                     'source': SOURCES['geometry'], 'status': 'REPRODUCED — fixed finite geometry'})
    b_examples = []
    archived_b = {r['q']: r for r in src['physical_b']['exhaustive_results']}
    for q in B_CONTROLS:
        contacts = [contact(c, q) for c in caps]
        loss = min(c['loss'] for c in contacts if c['in_cap'])
        winners = [c for c in contacts if c['in_cap'] and c['loss'] == loss]
        times = sorted({c['point'][1] for c in winners} | {1-c['point'][1] for c in winners})
        assert times == list(map(F, archived_b[q]['claimed_times']))
        assert F(1, 6)-loss == F(archived_b[q]['maximum'])
        b_examples.append({'q': q, 'ray': 'B', 'residue': q % 6, 'speeds': speeds('B', q),
                           'contacts': contacts, 'winner_caps': [c['cap'] for c in winners],
                           'loss': loss, 'maximum': F(1, 6)-loss, 'times': times,
                           'witnesses': [witness('B', q, t) for t in times],
                           'archive': archived_b[q], 'source': SOURCES['physical_b']})
    selector_by_q = {r['certificate']['q']: r for r in src['selector']['physical_controls']}
    a_examples = [{'q': q, 'ray': 'A', 'speeds': speeds('A', q),
                   'selector': selector_by_q[q],
                   'witness': witness('A', q, F(selector_by_q[q]['certificate']['time'])),
                   'transfer': next((r for r in src['transfer']['physical_controls'] if r['q'] == q), None)}
                  for q in A_CONTROLS]
    families = {
        'common': {'total_runners': 8, 'moving_runners': 7, 'reference_speed': 0,
                   'common_start': True, 'closed_threshold': F(1, 8), 'rows': ROWS,
                   'fold': 'If x>1/2, reflect BOTH coordinates (x,y) -> (1-x,1-y).'},
        'A': {'speed_formulas': ['1','q','q+1','q+2','q+3','2q+3','2q+5'],
              'coordinates': 'x={t}, y={qt}', 'orbit': 'h=qx-y in Z', 'clock': 't=x',
              'physical_laps': 'ell_i=m_i+b_i*h', 'coefficient_to_speed_order': [0,1,2,3,4,5,6]},
        'B': {'speed_formulas': ['1','q','q+1','2q+1','3q+1','3q+2','5q+2'],
              'coordinates': 'x={qt}, y={t}', 'orbit': 'h=x-qy in Z', 'clock': 't=y',
              'physical_laps': 'ell_i=m_i-a_i*h; then swap the first two entries',
              'coefficient_to_speed_order': [1,0,2,3,4,5,6]},
        'reflection': 't -> 1-t; ell_i -> v_i-1-ell_i at positive separation',
    }
    geometry = exact({'full_cells': cells, 'top_caps': caps, 'parameter_families': families,
                      'parent_child': {k: src['transfer'][k] for k in ['parents','children','parent_child_map','removed_parent_vertices','summary']},
                      'selectors': {'A': {k: src['selector'][k] for k in ['segments','small_coverage','width_certificate','unbounded_residue_coverage']},
                                    'B': {'formula': 'min(rho/(-d_min),(1-rho)/d_max); zero when h0 is integral',
                                          'source': 'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md'}}})
    examples = exact({'A': a_examples, 'B': b_examples,
                      'opening_visual': opening_visual(),
                      'story_visual': story_visual(src,b_examples),
                      'joint_visual': joint_visual(src),
                      'transfer_visual': transfer_visual(src),
                      'selector_visual': selector_visual(src),
                      'clock_visual': clock_visual(src),
                      'cell_visual': cell_visual(src),
                      'marginal_counterexample': src['transfer']['marginal_projection_counterexample'],
                      'q10_face_contact': src['transfer_countercheck']['q10_new_face_contact']})
    hashes = {p: digest(source_bytes(p)) for p in sorted(set(SOURCES.values()) | set(NOTES))}
    implementation_paths = [Path(__file__), PACKAGE/'presentation.template.html', PACKAGE/'opening.template.html', PACKAGE/'story.template.html', PACKAGE/'joint.template.html', PACKAGE/'representation.template.html', PACKAGE/'transfer.template.html', PACKAGE/'selector.template.html', PACKAGE/'clock.template.html', PACKAGE/'cell.template.html', PACKAGE/'css/cc.css',
                            *sorted((PACKAGE/'js').glob('*.js')),
                            PACKAGE/'checks/check_visual_data.py', PACKAGE/'checks/check_browser.cjs']
    source_hashes = {'source_commit': PIN, 'algorithm': 'sha256', 'files': hashes,
                     'implementation_files': {str(p.relative_to(ROOT)): digest(p.read_bytes())
                                              for p in implementation_paths if p.exists()}}
    controls = {'geometry': {'cells':10,'vertices':33,'edges':45,'singletons':3,'caps':7},
                'transfer': {'parents':8,'children':10,'empty_branches':46,'inherited_vertices':27,
                             'new_vertices':6,'removed_vertices':5,'new_face_edges':9},
                'A_q': A_CONTROLS, 'B_q': B_CONTROLS,
                'q4_safe_times': ['1/8','3/8','5/8','7/8'], 'q10_required_times':['17/35','18/35'],
                'selector_fallback': {'q':5,'time':'25/56'},
                'selector_endpoints': {'4':'1/8','6':'5/24'}}
    controls['joint_visual'] = {'q':4,'parent':2,'height':'1/8','candidate_time':'33/104',
                               'candidate_failed_speed':6,'candidate_failed_distance':'5/52',
                               'conditional_S':['109/56','33/16'],'slice_controls':14,
                               'collision_time':'4/13','slice_failed_speed':13}
    controls['representation'] = {'questions':6, 'comparison_states':12,
                                  'B_q6_maximum':'4/25','B_q6_maximizers':['9/25','16/25'],
                                  'A_q4_closed_segment_witnesses':['1/8'], 'A_q4_open_segment_witnesses':[],
                                  'A_q10_old_edge_maximizers':6,'A_q10_omitted_face_times':['17/35','18/35']}
    controls['transfer_visual'] = {'scenes':3,'stages':3,'q4_removed_parent':2,
                                   'q4_surviving_time':'3/8','q10_before_time':'16/33',
                                   'q10_after_time':'17/35','q10_after_height':'1/7'}
    controls['selector_visual'] = {'q':A_CONTROLS,'states':11,'fallback_q':5,
                                   'times':['7/48','1/8','25/56','5/24','15/104'],
                                   'endpoint_q':[4,6],'attempts':[1,1,2,1,1]}
    controls['clock_visual'] = {'speeds':[1,4,5,6,7,11,16],'window':['9/32','3/8'],
                               'occurrences':6,'pair_edges':4,'modes':2,
                               'exact_time_controls':len(examples['clock_visual']['controls']),
                               'safe_interval':['17/56','39/128'],'safe_duration':'1/896'}
    controls['cell_visual'] = {'cells':10,'stages_per_cell':8,'lap_cases':3,'singletons':['C0','C3','C5'],
                              'six_vertex_cell':'C7','positive_interval':['17/56','5/16'],
                              'singleton_time':'3/8','empty_bounds':['33/104','5/16']}
    controls['opening_visual'] = {'velocities':[1,2,3,4],'references':4,'frames':2,'threshold':'1/4',
                                 'time_denominator':96,'exact_snapshots':28,
                                 'outer_reference_safe_set':[['1/4','1/4'],['3/4','3/4']],
                                 'inner_reference_safe_set':[['1/4','3/8'],['5/8','3/4']]}
    controls['story_visual'] = {'cases':['contact','equality','joint'],'steps':4,'states':12,
                               'contact_integer':-2,'contact_time':'9/25','contact_minimum':'4/25',
                               'equality_points':4,'positive_duration_components':0,
                               'false_candidate_time':'33/104','failed_speed':6,
                               'local_joint_intersection':'empty'}
    data_hash = digest(json_bytes({'geometry': geometry, 'examples': examples, 'sources':source_hashes}))
    manifest = {'schema_version':1,'source_commit':PIN,'repository':REPO,'data_build_sha256':data_hash,
                'sources':SOURCES, 'claim_status':{'geometry':'REPRODUCED — exact finite certificate',
                'spectrum':'HYPOTHESIS — internally reviewed proof candidate; independent assessment remains open',
                'rendering':'ILLUSTRATION — animation and floating-point rendering are not proof'},
                'scope': 'Opening: four common-start runners at speeds 1,2,3,4 with all four references. Advanced sections: selected stationary reference among eight common-start runners; fixed A/B families and a separately labelled archived 6/7/11/16 blocking example on J=[9/32,3/8].',
                'retained':'Full labelled cells including singletons, cap directions, same-point orbit, exact recovery, canonical controls.',
                'omitted_by_first_slice':'Complete 1/8-safe sets, other reference runners, A-ray interactions, parent-child animations.',
                'recovery':'Use the full_cells and parent_child data and the pinned notes before changing threshold, family or requested output.',
                'scene_sources':{'opening':'notes/MATHEMATICAL_BASELINE.md','story':'notes/CC_REPRESENTATION_RULES.md','cap':SOURCES['geometry'],'projection':'notes/CC_OTHER_RAY_REVIEW_2026_09_29.md',
                                 'first_hit':'notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md','physical':SOURCES['physical_b'],
                                 'joint_compatibility':SOURCES['transfer'], 'joint_derivation':'notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md',
                                 'representation_rules':'notes/CC_REPRESENTATION_RULES.md',
                                 'representation_selector':'notes/CC_BOUNDED_SELECTOR_2026_09_29.md',
                                 'parent_child_geometry':SOURCES['transfer'],
                                 'parent_child_physical':SOURCES['transfer_countercheck'],
                                 'selector_geometry':SOURCES['selector'],
                                 'selector_physical':SOURCES['selector_countercheck'],
                                 'shared_clock':SOURCES['clock_occurrences'],
                                 'occurrence_identity':'notes/LAP_LABELLED_CONSTRAINTS.md',
                                 'cell_construction':SOURCES['geometry'], 'lap_bridge':SOURCES['transfer']},
                'implementation_scope':'Exact data and nine connected sections, including common-start/reference-motion opening, seven mathematical chapters, and the closing CC story with three exact recaps and distinct question/ray branches. Standalone figure exports and research explorer remain pending.'}
    return {'cc_geometry.json':geometry,'cc_examples.json':examples,'source_hashes.json':source_hashes,
            'visual_manifest.json':manifest}, controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data, controls = build()
    outputs = {PACKAGE/'data'/name:json_bytes(value) for name,value in data.items()}
    outputs[PACKAGE/'checks/expected_controls.json'] = json_bytes(controls)
    template = PACKAGE/'presentation.template.html'
    if template.exists():
        html = template.read_text()
        html = html.replace('<!-- CC_OPENING -->', (PACKAGE/'opening.template.html').read_text())
        html = html.replace('<!-- CC_STORY -->', (PACKAGE/'story.template.html').read_text())
        html = html.replace('<!-- CC_JOINT -->', (PACKAGE/'joint.template.html').read_text())
        html = html.replace('<!-- CC_REPRESENTATION -->', (PACKAGE/'representation.template.html').read_text())
        html = html.replace('<!-- CC_TRANSFER -->', (PACKAGE/'transfer.template.html').read_text())
        html = html.replace('<!-- CC_SELECTOR -->', (PACKAGE/'selector.template.html').read_text())
        html = html.replace('<!-- CC_CLOCK -->', (PACKAGE/'clock.template.html').read_text())
        html = html.replace('<!-- CC_CELL -->', (PACKAGE/'cell.template.html').read_text())
        payload = {'geometry':data['cc_geometry.json'],'examples':data['cc_examples.json'], 'manifest':data['visual_manifest.json']}
        html = html.replace('/* CC_DATA */', 'const CC_DATA = '+json.dumps(payload,ensure_ascii=False).replace('</','<\\/')+';')
        html = html.replace('/* CC_CSS */', (PACKAGE/'css/cc.css').read_text())
        html = html.replace('/* CC_JS */', '\n'.join((PACKAGE/'js'/p).read_text() for p in ['cc-core.js','cc-geometry.js','cc-deck.js','cc-joint.js','cc-representation.js','cc-transfer.js','cc-selector.js','cc-clock.js','cc-cell.js','cc-opening.js','cc-story.js','cc-navigation.js']))
        outputs[PACKAGE/'presentation.html'] = html.encode()
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                raise SystemExit(f'Stale generated output: {path.relative_to(ROOT)}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print(('Verified' if args.check else 'Wrote')+f' {len(outputs)} deterministic outputs; data {data["visual_manifest.json"]["data_build_sha256"][:16]}')


if __name__ == '__main__':
    main()
