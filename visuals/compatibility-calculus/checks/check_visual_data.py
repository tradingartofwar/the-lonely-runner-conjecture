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
