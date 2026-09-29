#!/usr/bin/env python3
"""Exact acceptance checks for the serialization, geometry and physical maps.

No sampled time grid. Physical controls use closed band intersection and an
opposing-contact optimizer, not the cap selector. This is same-author checking,
not independent mathematical review. No new physical inputs beyond the plan.
"""
import hashlib
import itertools
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
ROWS = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)]


def decode(x):
    if isinstance(x,dict):
        if {'num','den','text','float'} <= x.keys():
            f=F(x['num'],x['den'])
            assert str(f)==x['text'] and float(f)==x['float']
            return f
        return {k:decode(v) for k,v in x.items()}
    if isinstance(x,list): return [decode(v) for v in x]
    return x


def load(name): return decode(json.loads((PACKAGE/'data'/name).read_text()))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def frac(x): return x-x.__floor__()
def dist(x): return min(frac(x),1-frac(x))


def rank(rows):
    a=[list(map(F,r)) for r in rows]
    n=0
    for col in range(3):
        pivot=next((i for i in range(n,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[n],a[pivot]=a[pivot],a[n]
        z=a[n][col];a[n]=[x/z for x in a[n]]
        for i in range(len(a)):
            if i!=n:
                z=a[i][col];a[i]=[x-z*y for x,y in zip(a[i],a[n])]
        n+=1
    return n


def safe_set(speeds,z):
    result=[(F(0),F(1))]
    for v in speeds:
        bands=[((m+z)/v,(m+1-z)/v) for m in range(v)]
        result=sorted(set((max(a,c),min(b,d)) for a,b in result for c,d in bands if max(a,c)<=min(b,d)))
    return result


def optimize(speeds):
    # A maximum of the tent lower envelope lies at a tent peak or opposing contact.
    times={F(0),F(1)}
    for v in speeds: times.update(F(2*m+1,2*v) for m in range(v))
    for u,v in itertools.combinations(speeds,2): times.update(F(m,u+v) for m in range(1,u+v))
    values={t:min(dist(v*t) for v in speeds) for t in times}
    best=max(values.values())
    return best,sorted(t for t,value in values.items() if value==best)


def main():
    g,e=load('cc_geometry.json'),load('cc_examples.json')
    counts={}
    hashes=json.loads((PACKAGE/'data/source_hashes.json').read_text())
    for path,digest in hashes['files'].items():
        pinned = subprocess.check_output(['git','show',f"{hashes['source_commit']}:{path}"],cwd=ROOT)
        assert hashlib.sha256(pinned).hexdigest()==digest, path
    for path,digest in hashes['implementation_files'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest, path
    counts['source_hashes']=len(hashes['files'])
    counts['implementation_hashes']=len(hashes['implementation_files'])
    cells,caps=g['full_cells'],g['top_caps']
    assert (len(cells),sum(len(c['vertices']) for c in cells),sum(len(c['edges']) for c in cells),sum(c['singleton'] for c in cells),len(caps))==(10,33,45,3,7)
    for c in cells:
        vertices=c['vertices']
        assert rank([[a-b for a,b in zip(v,vertices[0])] for v in vertices[1:]])==c['dimension']
        for x,y,z in vertices:
            assert F(1,8)<=z and x<=F(1,2)
            assert all(z<=a*x+b*y-m<=1-z for (a,b),m in zip(ROWS,c['labels']))
    for cap in caps:
        cell=cells[cap['cell']];p=cap['peak'];rays=cap['rays']
        assert cap['vertices']==[p]+[[p[i]+r[i]/42 for i in range(3)] for r in rays]
        clipped={tuple(v) for v in cell['vertices'] if v[2]>=F(1,7)}
        for i,j in cell['edges']:
            a,b=cell['vertices'][i],cell['vertices'][j]
            if (a[2]-F(1,7))*(b[2]-F(1,7))<0:
                u=(F(1,7)-a[2])/(b[2]-a[2]);clipped.add(tuple(a[k]+u*(b[k]-a[k]) for k in range(3)))
        assert clipped==set(map(tuple,cap['vertices']))
    counts.update(cells=10,vertex_occurrences=33,edge_occurrences=45,singletons=3,exact_caps=7)
    atlas=g['parent_child'];parents,children=atlas['parents'],atlas['children']
    assert len(parents)==8 and len(children)==10
    assert sum(len(p['empty_seventh_laps']) for p in atlas['parent_child_map'])==46
    old_vertices={tuple(v) for p in parents for v in p['vertices']}
    new_vertices={tuple(v) for c in children for v in c['vertices']}
    assert (len(old_vertices & new_vertices),len(new_vertices-old_vertices),len(old_vertices-new_vertices))==(27,6,5)
    face_edges=0
    for child,cell in zip(children,cells):
        assert child['vertices']==cell['vertices'] and child['edges']==cell['edges'] and child['labels']==cell['labels']
        parent=parents[child['parent_index']]
        for v in child['vertices']:
            assert all(dot(normal,v)<=bound for _,normal,bound in child['constraints'])
        for i,j in child['edges']:
            u,v=child['vertices'][i],child['vertices'][j]
            active=[normal for _,normal,bound in parent['constraints'] if dot(normal,u)==bound==dot(normal,v)]
            face_edges+=3-rank(active)==2
    assert face_edges==9
    counts.update(parents=8,empty_branches=46,inherited_vertices=27,new_vertices=6,removed_vertices=5,new_face_edges=9)
    for example in e['A']:
        q,vs=example['q'],example['speeds'];w=example['witness'];t=w['time']
        assert min(dist(v*t) for v in vs)==F(1,8)
        cert=example['selector']['certificate'];x,y,z=cert['point'];h=q*x-y
        assert h.denominator==1 and x==t and y==frac(q*t)
        assert cert['physical_laps']==[m+b*h for m,(_,b) in zip(cert['torus_laps'],ROWS)]
        tr=example['transfer']
        if tr:
            for n,key in [(6,'six_safe_components_at_1_over_8'),(7,'seven_safe_components_at_1_over_8')]:
                safe=safe_set(vs[:n],F(1,8));assert safe==list(map(tuple,tr[key]))
                opt,times=optimize(vs[:n]);r=next(r for r in tr['optimization'] if r['coordinates']==n)
                assert (opt,times)==(r['maximum'],r['all_maximizing_times'])
            if q==4:
                assert safe==[(F(i,8),F(i,8)) for i in (1,3,5,7)]
                assert sum(a<b for a,b in safe_set(vs[:6],F(1,8)))==4
            if q==10: assert F(17,35) in times and F(18,35) in times
    for q,t in [(4,F(1,8)),(5,F(25,56)),(6,F(5,24))]:
        record=next(r for r in e['A'] if r['q']==q)
        assert record['witness']['time']==t
    assert next(r for r in e['A'] if r['q']==5)['selector']['certificate']['segment']=='E2'
    segments=g['selectors']['A']['segments']
    for s in segments:
        for ep in s['endpoints']:
            x,y,z=ep['point'];assert all(z<=a*x+b*y-m<=1-z for (a,b),m in zip(ROWS,s['torus_laps']))
    for r in g['selectors']['A']['small_coverage']:
        q=r['q'];lo,hi=F(q-4,8),F(5*q-6,24)
        assert r['accept']==(lo.__ceil__()<=hi)==(q!=5)
    counts.update(A_controls=5,physical_transfer_optimizations=6,selector_endpoint_inequalities=56)
    # Section 05: project the endpoints directly and enumerate the integer set.
    # This checks the slope/intercept builder through a different route.
    selector=e['selector_visual'];trial_count=0
    assert [c['q'] for c in selector['controls']]==[3,4,5,6,10]
    for control in selector['controls']:
        q=control['q'];valid=[]
        for i,(segment,trial) in enumerate(zip(selector['segments'],control['trials'])):
            endpoints=segment['endpoints']
            lo,hi=sorted(q*x-y for x,y,z in endpoints)
            integers=[h for h in range(lo.__floor__()-1,hi.__ceil__()+2) if lo<=h<=hi]
            assert trial['interval']==[lo,hi] and trial['width']==hi-lo
            assert trial['first_integer']==lo.__ceil__()
            assert trial['accepted']==bool(integers)
            assert trial['lower_equality']==(bool(integers) and integers[0]==lo)
            assert trial['upper_equality']==(bool(integers) and integers[0]==hi)
            if integers:
                h=integers[0];u=(h-lo)/(hi-lo)
                point=[a+u*(b-a) for a,b in zip(*endpoints)]
                assert trial['point']==point
                x,y,z=point;assert q*x-y==h and y==frac(q*x)
                assert all(z<=a*x+b*y-m<=1-z for (a,b),m in zip(ROWS,segment['torus_laps']))
                valid.append(i)
            else:assert trial['point'] is None
            trial_count+=1
        assert control['selected_index']==valid[0] and control['attempts']==valid[0]+1
        selected=control['trials'][valid[0]];segment=selector['segments'][valid[0]]
        x,y,z=selected['point'];h=q*x-y
        original=control['witness'];reflected=control['reflected']
        speeds=next(a['speeds'] for a in e['A'] if a['q']==q)
        assert original['time']==x and reflected['time']==1-x
        for witness in [original,reflected]:
            t=witness['time']
            assert witness['minimum']==min(dist(v*t) for v in speeds)==F(1,8)
            assert [r['lap'] for r in witness['runners']]==[(v*t).__floor__() for v in speeds]
            assert [r['phase'] for r in witness['runners']]==[frac(v*t) for v in speeds]
            assert [r['distance'] for r in witness['runners']]==[dist(v*t) for v in speeds]
        assert [r['lap'] for r in original['runners']]==[m+b*h for m,(a,b) in zip(segment['torus_laps'],ROWS)]
    s3,s4,s5,s6,s10=selector['controls']
    assert s3['trials'][0]['first_integer']==0 and s3['trials'][0]['interval'][0]==F(-1,8)
    assert s4['trials'][0]['lower_equality'] and s6['trials'][0]['upper_equality']
    assert s5['attempts']==2 and s5['witness']['time']==F(25,56)
    assert s10['trials'][0]['width']>=1 and s10['witness']['time']==F(15,104)
    counts.update(selector_visual_controls=5,selector_visual_interval_checks=trial_count,
                  selector_visual_physical_and_reflection=True,selector_visual_states=11,
                  selector_visual_closed_endpoints_and_negative_rounding=True)
    # Section 06: independently enumerate the strict blocking occurrences,
    # and obtain the closed safe set by intersecting all seven safe bands.
    clock=e['clock_visual'];lo,hi=clock['window'];delta=clock['threshold']
    assert clock['speeds']==[1,4,5,6,7,11,16] and (lo,hi,delta)==(F(9,32),F(3,8),F(1,8))
    expected=[]
    for v in clock['extras']:
        for m in range(v+1):
            a,b=max(lo,(m-delta)/v),min(hi,(m+delta)/v)
            if a<b:
                expected.append({'id':f'v{v}m{m}','speed':v,'meeting':m,'interval':[a,b],
                                 'closed':[dist(v*t)<delta for t in [a,b]]})
    assert sorted(clock['episodes'],key=lambda e:e['id'])==sorted(expected,key=lambda e:e['id'])
    clipped=[(max(a,lo),min(b,hi)) for a,b in safe_set(clock['speeds'],delta) if max(a,lo)<=min(b,hi)]
    assert clipped==list(map(tuple,clock['safe_components']))==[(F(17,56),F(39,128))]
    assert sum(b-a for a,b in clipped)==clock['safe_duration']==F(1,896)
    assert all(any(a<=lo<=hi<=b for a,b in safe_set([v],delta)) for v in clock['core'])
    expected_pairs=[]
    for a,b in itertools.combinations(expected,2):
        left=max(a['interval'][0],b['interval'][0]);right=min(a['interval'][1],b['interval'][1])
        if left<right:expected_pairs.append((frozenset([a['id'],b['id']]),left,right))
    assert len(expected_pairs)==len(clock['pairs'])==4
    for pair in clock['pairs']:
        left,right=pair['interval']
        assert (frozenset(pair['episodes']),left,right) in expected_pairs
        assert pair['duration']==right-left and pair['time']==(left+right)/2
        assert pair['closed']==[all(dist(v*t)<delta for v in pair['speeds']) for t in [left,right]]
        assert clock['controls'][pair['control_index']]['time']==pair['time']
    for a,b,c in itertools.product(*[[e for e in expected if e['speed']==v] for v in [6,11,16]]):
        assert max(e['interval'][0] for e in [a,b,c])>min(e['interval'][1] for e in [a,b,c])
    cuts=sorted({lo,hi}|{x for e in expected for x in e['interval']})
    assert [c['time'] for c in clock['controls']]==sorted(cuts+[(a+b)/2 for a,b in zip(cuts,cuts[1:])])
    for control in clock['controls']:
        t=control['time'];active=[]
        for row,v in zip(control['runners'],clock['speeds']):
            assert row['speed']==v and row['phase']==frac(v*t) and row['lap']==(v*t).__floor__()
            assert row['distance']==dist(v*t) and row['blocked']==(dist(v*t)<delta)
            if row['blocked']:
                active.append(v);assert row['meeting']==(v*t+F(1,2)).__floor__()
            else:assert row['meeting'] is None
        assert control['active_speeds']==active and control['minimum']==min(dist(v*t) for v in clock['speeds'])
        assert control['active_episodes']==[e['id'] for e in clock['episodes'] if abs(e['speed']*t-e['meeting'])<delta]
        assert control['boundary']==(t in cuts)
    assert [clock['controls'][i]['time'] for i in clock['safe_indices']]==[F(17,56),F(545,1792),F(39,128)]
    assert all(not clock['controls'][i]['active_speeds'] for i in clock['safe_indices'])
    default=clock['controls'][clock['default_index']]
    six=next(r for r in default['runners'] if r['speed']==6)
    assert default['time']==F(81,256) and (six['lap'],six['meeting'])==(1,2)
    counts.update(clock_occurrences=6,clock_pair_edges=4,clock_exact_time_controls=19,
                  clock_strict_boundaries_and_closed_safe_set=True,clock_meeting_distinct_from_completed_lap=True,
                  clock_no_local_6_11_16_triple=True)
    # Section 07: incremental edge clipping, independent of the builder's
    # enumeration of triples of boundary planes.
    construction=e['cell_visual'];construction_states=0
    for ci,record in enumerate(construction['cells']):
        vertices=sorted(itertools.product([F(0),F(1,2)],[F(0),F(1)],[F(1,8),F(1,2)]))
        edges=[(i,j) for i,j in itertools.combinations(range(8),2) if sum(a!=b for a,b in zip(vertices[i],vertices[j]))==1]
        constraints=construction['frame'].copy()
        for stage,poly in enumerate(record['stages']):
            if stage:
                for normal,bound in record['bands'][stage-1]:
                    values=[dot(normal,p)-bound for p in vertices]
                    clipped={p for p,value in zip(vertices,values) if value<=0}
                    for i,j in edges:
                        if values[i]*values[j]<0:
                            u=values[i]/(values[i]-values[j])
                            clipped.add(tuple(a+u*(b-a) for a,b in zip(vertices[i],vertices[j])))
                    vertices=sorted(clipped);constraints.append([normal,bound])
                    edges=[(i,j) for i,j in itertools.combinations(range(len(vertices)),2)
                           if rank([n for n,b in constraints if dot(n,vertices[i])==b==dot(n,vertices[j])])>=2]
            assert vertices==list(map(tuple,poly['vertices']))
            assert edges==list(map(tuple,poly['edges']))
            dimension=rank([[a-b for a,b in zip(p,vertices[0])] for p in vertices[1:]])
            assert dimension==poly['dimension']
            assert all(dot(n,p)<=b for p in vertices for n,b in constraints)
            facets=set()
            for n,b in constraints:
                ids=tuple(i for i,p in enumerate(vertices) if dot(n,p)==b)
                if len(ids)>2 and rank([[a-b for a,b in zip(vertices[i],vertices[ids[0]])] for i in ids[1:]])==2:facets.add(frozenset(ids))
            assert {frozenset(f) for f in poly['faces']}==facets
            for face in poly['faces']:
                assert all(tuple(sorted([i,j])) in edges for i,j in zip(face,face[1:]+face[:1]))
            construction_states+=1
        assert set(vertices)==set(map(tuple,cells[ci]['vertices']))
        certified_edges={frozenset([tuple(cells[ci]['vertices'][i]),tuple(cells[ci]['vertices'][j])]) for i,j in cells[ci]['edges']}
        assert {frozenset([vertices[i],vertices[j]]) for i,j in edges}==certified_edges
    speeds_for_q4=[1,4,5,6,7,11,13]
    for case in construction['lap_cases']:
        bounds=[((ell+F(1,8))/v,(ell+F(7,8))/v) for v,ell in zip(case['speeds'],case['physical_laps'])]
        assert bounds==list(map(tuple,case['bounds']))
        lo=max(a for a,b in bounds);hi=min(b for a,b in bounds)
        assert (lo,hi)==(case['lower'],case['upper'])
        expected={'interval':(F(17,56),F(5,16)),'point':(F(3,8),F(3,8)),'empty':(F(33,104),F(5,16))}
        assert (lo,hi)==expected[case['id']]
        assert case['physical_laps']==[m+b*case['h'] for m,(a,b) in zip(case['torus_laps'],ROWS)]
        if lo>hi:assert case['time'] is None and case['point'] is None and case['witness'] is None
        else:
            t=(lo+hi)/2;x,y,z=case['point'];assert t==x==case['time'] and 4*x-y==1
            assert all(z<=a*x+b*y-m<=1-z for (a,b),m in zip(ROWS,case['torus_laps']))
            assert all(dist(v*t)>=z for v in case['speeds'])
            assert [r['phase'] for r in case['witness']['runners']]==[frac(v*t) for v in speeds_for_q4]
    counts.update(cell_construction_states=construction_states,cell_incremental_clipping=True,
                  cell_final_vertices_edges_match_atlas=True,cell_closed_lap_controls=3)
    # Controls for section 03, checked against full physical sets and parent facets.
    a4=next(r for r in e['A'] if r['q']==4)
    closed_segment_times=[];open_segment_times=[]
    segment_ranges=[]
    for segment in segments:
        p0,p1=[ep['point'] for ep in segment['endpoints']]
        h0,h1=[4*p[0]-p[1] for p in [p0,p1]]
        assert h0<h1
        segment_ranges.append([h0,h1])
        for h in range(h0.__ceil__(),h1.__floor__()+1):
            t=p0[0]+(h-h0)/(h1-h0)*(p1[0]-p0[0])
            assert min(dist(v*t) for v in a4['speeds'])>=F(1,8)
            closed_segment_times.append(t)
            if h0<h<h1:open_segment_times.append(t)
    assert segment_ranges==[[F(0),F(7,12)],[F(9,8),F(15,8)]]
    assert closed_segment_times==[F(1,8)] and not open_segment_times
    a10=next(r for r in e['A'] if r['q']==10)
    face_times=[];edge_times=[]
    for origin in a10['transfer']['folded_child_maximizer_origins']:
        parent=parents[origin['parent_index']];point=origin['point']
        active=[n for _,n,b in parent['constraints'] if dot(n,point)==b]
        dimension=3-rank(active)
        assert dimension==origin['parent_face_dimension']
        target=face_times if dimension==2 else edge_times
        assert dimension in [1,2]
        target.extend([origin['time'],1-origin['time']])
    opt,all_times=optimize(a10['speeds'])
    assert opt==F(1,7) and sorted(edge_times+face_times)==all_times
    assert sorted(face_times)==[F(17,35),F(18,35)] and len(edge_times)==6
    counts.update(representation_questions=6,representation_q4_closed_segment_times=['1/8'],
                  representation_q4_open_segment_times=[],representation_q10_edge_times=6,
                  representation_q10_face_times=['17/35','18/35'])
    marginal=e['marginal_counterexample'];parent=parents[2]
    floor=[p for p in parent['vertices'] if p[2]==F(1,8)]
    assert [min(4*x-y for x,y,z in floor),max(4*x-y for x,y,z in floor)]==marginal['marginal_H_range']
    assert [min(5*x+2*y for x,y,z in floor),max(5*x+2*y for x,y,z in floor)]==marginal['marginal_S_range']
    section=[]
    for a,b in itertools.combinations(floor,2):
        ha,hb=4*a[0]-a[1],4*b[0]-b[1]
        if min(ha,hb)<=1<=max(ha,hb) and ha!=hb:
            u=(1-ha)/(hb-ha);section.append([a[i]+u*(b[i]-a[i]) for i in range(3)])
    assert sorted(section)==sorted(marginal['conditional_section_endpoints'])
    s=sorted(5*x+2*y for x,y,z in section)
    assert s==marginal['conditional_S_range'] and F(15,8)<s[0]<=s[-1]<F(17,8)
    point=[F(17,35),F(6,7),F(1,7)]
    normals=[normal for _,normal,bound in parents[7]['constraints'] if dot(normal,point)==bound]
    assert rank(normals)==1
    assert all(dot(normal,point)<=bound for _,normal,bound in parents[7]['constraints'])
    child=children[9]
    assert rank([normal for _,normal,bound in child['constraints'] if dot(normal,point)==bound])==2
    counts.update(marginal_same_slice_control=True,q10_parent_face_dimension=2,q10_child_face_dimension=1)
    joint=e['joint_visual']
    assert joint['triangle_xy']==floor
    assert joint['triangle_hs']==[[4*x-y,5*x+2*y] for x,y,z in floor]
    assert joint['section_xy']==section and joint['conditional_S']==s
    x,y,z=joint['fake_xy'];h,S=joint['fake_hs']
    assert (h,S)==(4*x-y,5*x+2*y)==(F(1),F(17,8))
    assert joint['marginal_H'][0]<=h<=joint['marginal_H'][1]
    assert joint['marginal_S'][0]<=S<=joint['marginal_S'][1]
    assert any(dot(normal,[x,y,z])>bound for _,normal,bound in parent['constraints'])
    assert 2*x+y>1-z and min(frac(6*x),1-frac(6*x))==F(5,52)<z
    assert joint['fake_failed_speeds']==[6]
    assert joint['safe_child_H'].denominator!=1
    assert joint['collision_ratio']==F(6,13) and joint['collision_point'][0]==F(4,13)
    vs=[1,4,5,6,7,11,13]
    for control in joint['slice_controls']:
        x,y,z=control['point'];w=control['witness']
        assert 4*x-y==1 and x==w['time']
        assert all(dot(normal,[x,y,z])<=bound for _,normal,bound in parent['constraints'])
        assert [r['phase'] for r in w['runners']]==[frac(v*x) for v in vs]
        assert [r['distance'] for r in w['runners']]==[dist(v*x) for v in vs]
        assert all(dist(v*x)>=z for v in vs[:6]) and dist(vs[6]*x)<z
    assert joint['conditional_S'][0]-F(15,8)==F(1,14)
    assert F(17,8)-joint['conditional_S'][1]==F(1,16)
    assert safe_set(vs,z)==[(t,t) for t in joint['full_safe_times']]
    counts.update(joint_candidate_failed_speed=6,joint_slice_controls=14,joint_collision_time='4/13',
                  joint_closed_interval_strictly_blocked=True)
    # Independent 2D halfspace reconstruction of the section builder's edge cuts.
    def sliced_vertices(poly,q,h):
        constraints=[([n[0]+q*n[1],n[2]],b+h*n[1]) for _,n,b in poly['constraints']]
        result=set()
        for (a,b),(c,d) in itertools.combinations(constraints,2):
            det=a[0]*c[1]-a[1]*c[0]
            if not det:continue
            t=(b*c[1]-a[1]*d)/det
            z=(a[0]*d-b*c[0])/det
            if all(n[0]*t+n[1]*z<=bound for n,bound in constraints):
                result.add((t,q*t-h,z))
        return sorted(result)
    scene_expected={'removed':(4,2,1,F(4,13),None),
                    'equality':(4,4,1,F(3,8),F(3,8)),
                    'face':(10,7,4,F(16,33),F(17,35))}
    section_checks=0
    for scene in e['transfer_visual']:
        q,pi,h,old_t,new_t=scene_expected[scene['id']]
        assert (scene['q'],scene['parent_index'],scene['orbit_integer'])==(q,pi,h)
        assert list(map(tuple,scene['parent_section']))==sliced_vertices(parents[pi],q,h)
        assert scene['child_indices']==[i for i,c in enumerate(children) if c['parent_index']==pi]
        section_checks+=1
        after=[]
        for section in scene['child_sections']:
            assert list(map(tuple,section['points']))==sliced_vertices(children[section['child_index']],q,h)
            after.extend(section['points']);section_checks+=1
        assert scene['before_point'][0]==old_t
        assert scene['before_point'][2]==max(p[2] for p in scene['parent_section'])
        if new_t is None:assert not after and scene['after_point'] is None
        else:
            assert scene['after_point'][0]==new_t
            assert scene['after_point'][2]==max(p[2] for p in after)
        vs=next(a['speeds'] for a in e['A'] if a['q']==q)
        for key in ['before_physical','after_physical','before_reflected','after_reflected']:
            witness=scene[key]
            if witness is None:continue
            t=witness['time']
            assert witness['minimum']==min(dist(v*t) for v in vs)
            assert [r['lap'] for r in witness['runners']]==[(v*t).__floor__() for v in vs]
            assert [r['phase'] for r in witness['runners']]==[frac(v*t) for v in vs]
            assert [r['distance'] for r in witness['runners']]==[dist(v*t) for v in vs]
        for point in scene['singleton_orbits']:
            x,y,z=point['point'];assert point['H']==q*x-y
    removed,equality,face=e['transfer_visual']
    assert removed['singleton_orbits'][0]['H']==F(11,8)
    assert equality['singleton_orbits'][0]['H']==1
    assert face['before_physical']['runners'][-1]['distance']==F(4,33)<F(1,8)
    assert face['after_point']==[F(17,35),F(6,7),F(1,7)]
    assert face['after_physical']['active_speeds']==[10,25]
    counts.update(transfer_visual_scenes=3,transfer_visual_halfspace_sections=section_checks,
                  transfer_visual_reflected_phases=True,transfer_visual_empty_point_polygon=True)
    for example in e['B']:
        q=example['q'];vs=example['speeds'];best,times=optimize(vs)
        assert (best,times)==(example['maximum'],example['times'])
        assert safe_set(vs,best)==[(t,t) for t in times]
        compatible=[]
        for c,cap in zip(example['contacts'],caps):
            p=cap['peak'];h0=p[0]-q*p[1];ds=[r[0]-q*r[1] for r in cap['rays']]
            assert c['h0']==h0 and c['directions']==ds
            # Independent contact enumeration at every integer reached over the cap.
            lo=h0+F(1,42)*min(ds);hi=h0+F(1,42)*max(ds)
            losses=[]
            for h in range(lo.__ceil__(),hi.__floor__()+1):
                if h==h0: losses.append(F(0))
                elif h<h0: losses.append((h-h0)/min(ds))
                else: losses.append((h-h0)/max(ds))
            assert bool(losses)==c['in_cap']
            if not losses:continue
            assert min(losses)==c['loss']
            compatible.append(c['loss'])
            x,y,z=c['point'];h=x-q*y
            assert h.denominator==1 and z==F(1,6)-c['loss']
            assert all(z<=a*x+b*y-m<=1-z for (a,b),m in zip(ROWS,cap['labels']))
            coefficient_laps=[m-a*h for m,(a,b) in zip(cap['labels'],ROWS)]
            physical_laps=[coefficient_laps[i] for i in [1,0,2,3,4,5,6]]
            assert physical_laps==[(v*y).__floor__() for v in vs]
            assert min(dist(v*y) for v in vs)==z
            assert [v-1-l for v,l in zip(vs,physical_laps)]==[(v*(1-y)).__floor__() for v in vs]
        assert min(compatible)==example['loss'] and best>F(1,7)
        for w in example['witnesses']:
            assert [r['phase'] for r in w['runners']]==[frac(v*w['time']) for v in vs]
    counts.update(B_controls=6,B_cap_contact_checks=42,B_residues=list(range(6)),B_optima_and_complete_maximizers=True)
    print(json.dumps({'status':'PASS','checks':counts,
                      'limits':'Finite display controls and source/data integrity; same-author checks; all-q claims remain the pinned proof candidates.'},indent=2))


if __name__=='__main__':main()
