"""Alternate physical-time checks. Does not import discovery or prior code."""
from fractions import Fraction as F
from pathlib import Path
from math import floor, gcd
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8)]
D = F(1,8)
CHECKS = {'contact_bits':0,'witnesses':0,'source_endpoint_bands':0,
          'negative_event_decompositions':0,'negative_events_checked':0}


def encode(x):
    if isinstance(x,F): return str(x)
    raise TypeError(type(x).__name__)


def xy_member(point, endpoints):
    x,y = point
    A,B = endpoints
    dx,dy = B[0]-A[0], B[1]-A[1]
    if dx == 0 and dy == 0:
        return point == A
    s = (x-A[0])/dx if dx else (y-A[1])/dy
    return 0 <= s <= 1 and [x,y] == [A[0]+s*dx,A[1]+s*dy]


def merge(intervals):
    ans=[]
    for l,u in sorted(intervals):
        if l > u: continue
        if ans and l <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1],u)
        else: ans.append([l,u])
    return ans


def common(left,right):
    out=[]; i=j=0
    while i<len(left) and j<len(right):
        l=max(left[i][0],right[j][0]); u=min(left[i][1],right[j][1])
        if l<=u: out.append([l,u])
        if left[i][1]<right[j][1]: i+=1
        elif right[j][1]<left[i][1]: j+=1
        else: i+=1; j+=1
    return merge(out)


def bands(v,delta):
    return [[(j+delta)/v,(j+1-delta)/v] for j in range(v)]


def safe_intervals(vs,delta):
    if sum(vs)>1000: raise RuntimeError('SCOPE_LIMIT: physical bands')
    out=[[F(0),F(1)]]
    for v in vs:
        out=common(out,bands(v,delta))
    return out


def negative_crosscheck(vs,delta):
    events=sorted({F(0),F(1)}|{x for v in vs for interval in bands(v,delta) for x in interval})
    if len(events)>2000: raise RuntimeError('SCOPE_LIMIT: negative events')
    tests=events+[(a+b)/2 for a,b in zip(events,events[1:])]
    for t in tests:
        assert not all(delta <= (v*t)%1 <= 1-delta for v in vs)
    CHECKS['negative_event_decompositions']+=1
    CHECKS['negative_events_checked']+=len(tests)


def physical_contacts(v,src):
    """Independent complete contact tables using t, not integer projections."""
    p,q,r=v
    edge_times={z:[(j+z)/r for j in range(r)] for z in [D,1-D]}
    wraps=sorted({F(j,p) for j in range(p+1)}|{F(j,q) for j in range(q+1)})
    pieces=[(l,u,floor(p*(l+u)/2),floor(q*(l+u)/2)) for l,u in zip(wraps,wraps[1:])]
    r_bands=bands(r,D)
    edge_hits=[]; sheet_hits=[]
    for s in src:
        A,B=s['endpoints']; dx,dy=B[0]-A[0],B[1]-A[1]
        for z in [D,1-D]:
            edge_hits.append(any(xy_member([(p*t)%1,(q*t)%1],[A,B]) for t in edge_times[z]))
        hit=False
        for l,u,i,j in pieces:
            if dx==0 and dy==0:
                t=(i+A[0])/p
                if l<=t<=u and [(p*t)%1,(q*t)%1]==A and D <= (r*t)%1 <= 1-D:
                    hit=True;break
                continue
            det=p*dy-q*dx
            rhs=(i+A[0])*dy-(j+A[1])*dx
            if det:
                t=rhs/det
                if l<=t<=u and xy_member([(p*t)%1,(q*t)%1],[A,B]) and D <= (r*t)%1 <= 1-D:
                    hit=True;break
            elif rhs==0:
                if dx: v0,v1=(i+A[0])/p,(i+B[0])/p
                else: v0,v1=(j+A[1])/q,(j+B[1])/q
                lower=max(l,min(v0,v1)); upper=min(u,max(v0,v1))
                if lower<=upper and common([[lower,upper]],r_bands):
                    hit=True;break
        sheet_hits.append(hit)
    return {'edges':''.join('1' if x else '0' for x in edge_hits),
            'sheets':''.join('1' if x else '0' for x in sheet_hits)}


def inspect_witness(v,w,src,objects,lat):
    if w is None: return
    t=F(w['time']); point=list(map(F,w['point'])); x,y,z=point
    vs=[a*v[0]+b*v[1] for a,b in BASE]+[v[2]]
    obj=objects[w['object']]; source=src[w['source']]
    assert obj['source']==w['source'] and xy_member([x,y],source['endpoints'])
    A,B=source['endpoints']; s=F(w['s'])
    assert 0<=s<=1 and [x,y]==[A[i]+s*(B[i]-A[i]) for i in [0,1]]
    assert F(obj['z_range'][0])<=z<=F(obj['z_range'][1])
    assert [(k*t)%1 for k in v]==point
    phases=[(k*t)%1 for k in vs]
    assert phases==list(map(F,w['phases']))
    assert all(D<=f<=1-D for f in phases)
    assert [floor(k*t) for k in vs]==w['physical_laps']
    assert w['torus_laps']==source['labels']+[0]
    assert [a*x+b*y-l for (a,b),l in zip(BASE,source['labels'])]+[z]==phases
    assert [(k*(1-t))%1 for k in vs]==[1-f for f in phases]
    assert [floor(k*(1-t)) for k in vs]==[k-1-l for k,l in zip(vs,w['physical_laps'])]
    assert min(min(f,1-f) for f in phases)==F(w['minimum'])
    assert F(w['tau'])==t*lat['g']
    assert F(w['pair_clock'])==lat['a']*x+lat['b']*y
    assert F(w['recovery_raw'])==lat['c']*F(w['pair_clock'])+lat['e']*z
    assert F(w['recovery_raw'])%1==F(w['tau'])
    assert [sum(F(a)*b for a,b in zip(row,point)) for row in lat['relations']]==[w['H1'],w['H2']]
    CHECKS['witnesses']+=1


def diagnostic_time(v,intervals,delta,src):
    l,u=intervals[0]; t=(l+u)/2
    # Reflection folds x without restricting the physical time domain.
    if (v[0]*t)%1 > F(1,2): t=1-t
    point=[(k*t)%1 for k in v]
    x,y,z=point
    vs=[a*v[0]+b*v[1] for a,b in BASE]+[v[2]]
    phases=[(k*t)%1 for k in vs]
    assert all(delta<=f<=1-delta for f in phases)
    labels=[floor(a*x+b*y) for a,b in BASE]+[0]
    return {'pqr':v,'time':t,'point':point,'threshold':delta,
            'physical_laps':[floor(k*t) for k in vs],'torus_laps':labels,
            'phases':phases,'minimum':min(min(f,1-f) for f in phases),
            'source_xy_memberships':[s['id'] for s in src if xy_member([x,y],s['endpoints'])]}


def run():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    for path,expected in pins['files'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected['sha256'],path
    raw=(HERE/'discovery.json').read_bytes(); data=json.loads(raw)
    assert data['protocol_sha256']==pins['protocol_sha256']
    assert data['rows']==[[a,b,0] for a,b in BASE]+[[0,0,1]]
    src=[{**s,'endpoints':[list(map(F,p)) for p in s['endpoints']]} for s in data['sources']]
    for s in src:
        for p in s['endpoints']:
            for (a,b),label in zip(BASE,s['labels']):
                assert D<=a*p[0]+b*p[1]-label<=1-D
                CHECKS['source_endpoint_bands']+=1
    objects={o['id']:o for group in data['objects'].values() for o in group}
    rows=sorted(data['cases'],key=lambda x:(x['split']=='scaling_control',tuple(x['pqr'])))
    first={k:None for k in ['edge_loss_sheet_repair','sheet_menu_loss_class_repair',
                            'sheet_class_loss_physical8','threshold8_obstruction',
                            'physical10_miss']}
    records=[]
    for row in rows:
        v=row['pqr']; lat=row['lattice']; A,B,C=lat['normalized']; d=lat['d']
        assert len(set([0]+[a*v[0]+b*v[1] for a,b in BASE]+[v[2]]))==10
        assert lat['g']==gcd(*v) and [k*lat['g'] for k in [A,B,C]]==v
        assert d==gcd(A,B) and [lat['P']*d,lat['Q']*d]==[A,B]
        assert lat['a']*lat['P']+lat['b']*lat['Q']==1
        assert lat['c']*d+lat['e']*C==1
        R,S=lat['relations']
        cross=[R[1]*S[2]-R[2]*S[1],R[2]*S[0]-R[0]*S[2],R[0]*S[1]-R[1]*S[0]]
        assert cross==[A,B,C]
        actual=physical_contacts(v,src)
        assert actual==row['hits'],('contact mismatch',v)
        CHECKS['contact_bits']+=sum(len(s) for s in actual.values())
        for kind in ['edges','sheets']:
            menu=data['menus'][kind]['indices']; hits=actual[kind]
            expected=next((i for i in menu if hits[i]=='1'),None)
            chosen=row['selected'][kind]
            assert (chosen is not None)==(expected is not None)
            if chosen: assert chosen['object']==data['objects'][kind][expected]['id']
            fallback=row['class_fallback'][kind]
            assert (fallback is not None)==(chosen is None and '1' in hits)
            for w in [chosen,fallback]: inspect_witness(v,w,src,objects,lat)
        if row['split']=='scaling_control': continue
        edge='1' in actual['edges']; sheet='1' in actual['sheets']
        assert not edge or sheet
        if not edge and sheet and first['edge_loss_sheet_repair'] is None:
            first['edge_loss_sheet_repair']={'pqr':v,'witness':row['selected']['sheets'] or row['class_fallback']['sheets']}
        if sheet and row['selected']['sheets'] is None and first['sheet_menu_loss_class_repair'] is None:
            first['sheet_menu_loss_class_repair']={'pqr':v,'witness':row['class_fallback']['sheets']}
        vs=[a*v[0]+b*v[1] for a,b in BASE]+[v[2]]
        intervals=safe_intervals(vs,D); weak=None
        if not intervals:
            negative_crosscheck(vs,D)
            weak=safe_intervals(vs,F(1,10))
            if weak and first['threshold8_obstruction'] is None:
                first['threshold8_obstruction']=diagnostic_time(v,weak,F(1,10),src)
            elif not weak:
                negative_crosscheck(vs,F(1,10))
                if first['physical10_miss'] is None: first['physical10_miss']={'pqr':v}
        if not sheet and intervals and first['sheet_class_loss_physical8'] is None:
            first['sheet_class_loss_physical8']=diagnostic_time(v,intervals,D,src)
        assert not sheet or bool(intervals)
        records.append({'pqr':v,'split':row['split'],'full8_intervals':intervals,
                        'full10_intervals_when8_empty':weak,'edge_class':edge,'sheet_class':sheet})
    # Check the frozen greedy selection independently from the saved bit tables.
    train=[x for x in data['cases'] if x['split']=='train']
    for kind in ['edges','sheets']:
        uncovered=set(range(len(train))); indices=[]
        for step in range(8):
            if not uncovered: break
            scores=[sum(train[j]['hits'][kind][i]=='1' for j in uncovered)
                    for i in range(len(data['objects'][kind]))]
            if max(scores)==0: break
            i=scores.index(max(scores)); indices.append(i)
            uncovered={j for j in uncovered if train[j]['hits'][kind][i]=='0'}
        assert indices==data['menus'][kind]['indices']
        assert sorted(uncovered)==data['menus'][kind]['uncovered_train_rows']
    controls=[r for r in data['cases'] if r['split']=='scaling_control']
    scaling=0
    for base,double in zip(controls[::2],controls[1::2]):
        assert double['pqr']==[2*k for k in base['pqr']]
        assert double['hits']==base['hits']
        for kind in ['edges','sheets']:
            for route in ['selected','class_fallback']:
                a,b=base[route][kind],double[route][kind]
                if a:
                    assert b and 2*F(b['time'])==F(a['time']) and a['phases']==b['phases']
                    assert a['physical_laps']==b['physical_laps']
        scaling+=1
    diagnostics=data['diagnostics']
    f=diagnostics['false_marginal']
    if f:
        assert all(-(-F(l)//1)<=F(u)//1 for l,u in f['ranges'])
        row=next(r for r in rows if r['pqr']==f['pqr'] and r['split']!='scaling_control')
        assert row['hits'][f['kind']][f['object_index']]=='0'
    f=diagnostics['unsaturated_false_point']
    if f:
        point=list(map(F,f['raw_hit']['point']))
        assert all(sum(a*b for a,b in zip(rel,point)).denominator==1 for rel in f['raw_relations'])
        assert any(sum(a*b for a,b in zip(rel,point)).denominator!=1 for rel in f['saturated_relations'])
        obj=f['object']; assert xy_member(point[:2],[list(map(F,p)) for p in obj['endpoints']])
        assert F(obj['z_range'][0])<=point[2]<=F(obj['z_range'][1])
    f=diagnostics['lost_clock_lift']
    if f:
        assert not D<=F(f['canonical_r_phase'])<=1-D
        assert (f['pqr'][2]*F(f['canonical_time']))%1==F(f['canonical_r_phase'])
    summary={'status':'PASS','scope':'Exact frozen finite domains; same-author alternate implementation',
             'checks':CHECKS,'scaling_pairs':scaling,'physical_cases':len(records),
             'full8_hits':sum(bool(x['full8_intervals']) for x in records),
             'full8_misses':sum(not x['full8_intervals'] for x in records),
             'conditional_full10_hits':sum(bool(x['full10_intervals_when8_empty']) for x in records),
             'physical10_misses':sum(x['full10_intervals_when8_empty']==[] for x in records),
             'sheet_class_misses_with_physical8':sum(not x['sheet_class'] and bool(x['full8_intervals']) for x in records),
             'edge_losses_repaired_by_sheets':sum(not x['edge_class'] and x['sheet_class'] for x in records)}
    result={'discovery_sha256':hashlib.sha256(raw).hexdigest(),'summary':summary,
            'first_examples':first,'physical_baselines':records}
    (HERE/'verification.json').write_text(json.dumps(result,default=encode,sort_keys=True,separators=(',',':'))+'\n')
    (HERE/'verification_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__': run()
