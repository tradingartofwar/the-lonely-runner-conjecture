#!/usr/bin/env python3
"""Independent physical review of the frozen row38 coefficient-range records.
No coordinator/compiler/checker imports. Rebuild contact from segment projection,
recover time by coordinate-lap congruences, then multiply the physical speeds.
"""
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PROTOCOL_HASH = '95811494876e2c62d6c288c21f8ba42b2983e486a25eb6e7b7633a0e0fc8a26a'
CORE = [(1,0),(0,1),(1,1),(2,1),(3,1),(3,2)]
PAIRS = [(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
         (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10)]
SEGMENTS = [
    ('L', [(F(1,4),F(7,8)),(F(3,8),F(3,4))]),
    ('S', [(F(7,24),F(1,4)),(F(55,168),F(1,7))]),
    ('C', [(F(1,8),F(1,8)),(F(1,8),F(3,16))]),
]
COUNTS = {'records':0, 'scalar_field_comparisons':0, 'selected_phase_checks':0,
          'selected_lap_checks':0, 'reflected_phase_checks':0,
          'reflected_lap_checks':0, 'alternative_bezout_recoveries':0}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def phase(x):
    return x-floor(x)

def compare(got,want,label):
    if isinstance(want,dict):
        assert isinstance(got,dict), label
        for key,value in want.items():
            assert key in got,(label,key,'missing')
            compare(got[key],value,label+'.'+key)
    elif isinstance(want,list):
        assert isinstance(got,list) and len(got)==len(want),(label,'shape')
        for i,(x,y) in enumerate(zip(got,want)):
            compare(x,y,f'{label}[{i}]')
    else:
        assert got==want,(label,got,want)
        COUNTS['scalar_field_comparisons']+=1

def choose(P,Q,old=False):
    segments = [('L',[(F(1,4),F(3,8)),(F(3,8),F(1,8))]),
                ('C',[(F(1,8),F(1,4)),(F(1,8),F(1,4))])] if old else SEGMENTS
    for role,(U,V) in segments:
        u,v = Q*U[0]-P*U[1],Q*V[0]-P*V[1]
        lo,hi = min(u,v),max(u,v)
        h = ceil(lo)
        if h>hi:
            continue
        if u==v:
            point=U
        else:
            lam=(F(h)-u)/(v-u)
            assert 0<=lam<=1
            point=tuple(U[k]+lam*(V[k]-U[k]) for k in range(2))
        if not old and role=='S':
            assert (P,Q) in [(1,4),(2,1)]
            role = 'F' if (P,Q)==(1,4) else 'G'
        if not old and role=='C':
            assert (P,Q)==(1,1)
        return role,point,h
    raise ArithmeticError('Frozen complete menu had no contact')

def recover(A,B,p,q,old=False):
    d=gcd(p,q);P,Q=p//d,q//d
    role,(x,y),h=choose(P,Q,old)
    assert Q*x-P*y==h
    # Find completed primitive p-laps using the orbit congruence, not Bezout.
    i=(-h*pow(Q,-1,P))%P if P>1 else 0
    assert (Q*i+h)%P==0
    j=(Q*i+h)//P
    tau=(x+i)/P
    assert 0<tau<1 and Q*tau==y+j
    assert floor(P*tau)==i and floor(Q*tau)==j
    t=tau/d
    rows=CORE+[(A,B)]
    speeds=[a*p+b*q for a,b in rows]
    torus=[floor(a*x+b*y) for a,b in rows]
    phases=[phase(v*t) for v in speeds]
    laps=[floor(v*t) for v in speeds]
    assert phases==[a*x+b*y-m for (a,b),m in zip(rows,torus)]
    assert laps==[m+a*i+b*j for (a,b),m in zip(rows,torus)]
    assert all(F(1,8)<=v<=F(7,8) for v in phases[:6])
    distances=[min(v,1-v) for v in phases]
    safe=distances[-1]>=F(1,8)
    distinct=len(set([0]+speeds))==8
    collisions=[list(row) for row in CORE[2:] if (A-row[0])*p+(B-row[1])*q==0]
    assert distinct==bool(p!=q and not collisions)
    if not safe and p!=q:
        assert distinct and not collisions
    reflected_time=1-t
    reflected=[phase(v*reflected_time) for v in speeds]
    reflected_laps=[floor(v*reflected_time) for v in speeds]
    assert reflected==[0 if z==0 else 1-z for z in phases]
    assert reflected_laps==[v-l-(z!=0) for v,l,z in zip(speeds,laps,phases)]
    # Verify two other Bezout choices solely as a crosscheck of the congruence clock.
    r=pow(P,-1,Q) if Q>1 else 0
    s=(1-r*P)//Q
    assert r*P+s*Q==1
    for k in (-1,1):
        rr,ss=r+k*Q,s-k*P
        raw=rr*x+ss*y;N=floor(raw)
        assert phase(raw)==tau
        assert laps==[m+(-a*ss+b*rr)*h-(a*P+b*Q)*N for (a,b),m in zip(rows,torus)]
    M=Q+2*P if old else P+Q
    rho=(-P-2*M)%8 if old else (P-2*M)%8
    return {'row':[A,B],'pair':[p,q],'gcd':d,'primitive':[P,Q],'role':role,
            'point':[str(x),str(y)],'h':h,'M':M,'rho':rho,
            'primitive_time':str(tau),'time':str(t),'speeds':speeds,
            'torus_laps':torus,'physical_laps':laps,'phases':list(map(str,phases)),
            'reflected_time':str(reflected_time),'reflected_phases':list(map(str,reflected)),
            'reflected_laps':reflected_laps,'distinct_speeds':distinct,
            'minimum':str(min(distances)),'seventh_safe':safe,
            'coordinate_laps':[i,j],'distances':list(map(str,distances)),
            'core_safe':True,'seventh_core_collisions':collisions}

def review_record(emitted,label,old=False):
    A,B=emitted['row'];p,q=emitted['pair']
    rec=recover(A,B,p,q,old)
    optional={'coordinate_laps','distances','core_safe','seventh_core_collisions'}
    compare(emitted,{k:v for k,v in rec.items() if k not in optional},label)
    for key in optional:
        if key in emitted:
            compare(emitted[key],rec[key],label+'.'+key)
    r,s=emitted['bezout'];N=emitted['N'];P,Q=rec['primitive'];x,y=map(F,rec['point'])
    assert r*P+s*Q==1 and N==floor(r*x+s*y)
    assert phase(r*x+s*y)==F(rec['primitive_time'])
    rows=CORE+[(A,B)]
    assert emitted['physical_laps']==[m+(-a*s+b*r)*rec['h']-(a*P+b*Q)*N
        for (a,b),m in zip(rows,rec['torus_laps'])]
    if 'alternate_bezout_time' in emitted:
        compare(emitted['alternate_bezout_time'],rec['time'],label+'.alternate_bezout_time')
    COUNTS['records']+=1
    for key in ('selected_phase_checks','selected_lap_checks','reflected_phase_checks','reflected_lap_checks'):
        COUNTS[key]+=7
    COUNTS['alternative_bezout_recoveries']+=2
    return rec


def main():
    assert sha(HERE/'PROTOCOL.md')==PROTOCOL_HASH
    classification=json.loads((HERE/'classification.json').read_text())
    controls=json.loads((HERE/'controls.json').read_text())
    cells={(c['delta'],c['B_mod56']):c for c in classification['cells']}
    assert len(cells)==1512
    input_paths=[HERE/'PROTOCOL.md', HERE/'classification.json', HERE/'controls.json',
                 HERE/'auxiliary_failures.json']
    by_role={role:0 for role in ('L','F','G','C')}
    primary=[]
    zero_phase_failures=0
    for delta in range(-13,14):
        filename=f"delta_{'m' if delta<0 else 'p'}{abs(delta)}.json"
        path=HERE/'failures'/filename
        input_paths.append(path)
        failures=json.loads(path.read_text())
        expected=[c for c in classification['cells'] if c['delta']==delta and not c['T']]
        assert len(expected)==len(failures)
        for n,(emitted,cell) in enumerate(zip(failures,expected)):
            label=f'primary.{delta}.{n}'
            compare(emitted['row'],cell['representative'],label+'.row')
            compare(emitted['pair'],cell['first_failure_pair'],label+'.first_failure_pair')
            compare(emitted['delta'],delta,label+'.delta')
            compare(emitted['B_mod56'],cell['B_mod56'],label+'.B_mod56')
            rec=review_record(emitted,label)
            assert not rec['seventh_safe'] and rec['distinct_speeds']
            assert F(rec['minimum'])<F(1,8) and rec['pair'][0]!=rec['pair'][1]
            primary.append((delta,cell['B_mod56']))
            by_role[rec['role']]+=1
            zero_phase_failures+=F(rec['phases'][-1])==0
    assert set(primary)=={k for k,c in cells.items() if not c['T']}
    auxiliary=json.loads((HERE/'auxiliary_failures.json').read_text())
    expected_aux=[c for c in classification['cells'] if c['T'] and not c['T_all']]
    assert len(auxiliary)==len(expected_aux)
    for n,(emitted,cell) in enumerate(zip(auxiliary,expected_aux)):
        compare(emitted['row'],cell['representative'],f'auxiliary.{n}.row')
        compare(emitted['pair'],[1,1],f'auxiliary.{n}.pair')
        compare(emitted['delta'],cell['delta'],f'auxiliary.{n}.delta')
        compare(emitted['B_mod56'],cell['B_mod56'],f'auxiliary.{n}.B_mod56')
        rec=review_record(emitted,f'auxiliary.{n}')
        assert rec['role']=='C' and not rec['distinct_speeds'] and not rec['seventh_safe']
        assert F(rec['phases'][-1])==0
    declared=[(list(row),list(pair)) for row in [(3,8),(59,64),(6,2)] for pair in PAIRS]
    declared += [(list(row),[2,3]) for row in CORE[2:]]
    assert [(w['row'],w['pair']) for w in controls['physical_controls']]==declared
    records=[review_record(w,f'control.{n}') for n,w in enumerate(controls['physical_controls'])]
    for rec in records:
        row=tuple(rec['row']);pair=tuple(rec['pair'])
        assert rec['seventh_safe']==(row!=(6,2) or pair!=(1,1))
        if row in CORE[2:]:
            assert not rec['distinct_speeds'] and rec['seventh_core_collisions']==[list(row)]
    archived_path=HERE.parent/'2026-09-29-cc-row38-transfer/run.json'
    input_paths.append(archived_path)
    archived=json.loads(archived_path.read_text())['controls']
    assert len(archived)==18
    compare(controls['archive_fields_compared'],288,'archive_fields_compared')
    compare(controls['phase_period_pairs_compared'],18,'phase_period_pairs_compared')
    archived_fields=['gcd','primitive','distinct_speeds','point','h','primitive_time',
                     'time','speeds','torus_laps','phases','physical_laps','minimum',
                     'reflected_time','reflected_phases','reflected_laps']
    for n,(new,old) in enumerate(zip(records[:18],archived)):
        compare(old,{key:new[key] for key in archived_fields},f'archived.{n}')
    # The period preserves phase and time but changes seventh integer laps.
    shifts={'L':63,'F':29,'G':27,'C':14}
    phase_period=[]
    for n,(base,lift) in enumerate(zip(records[:18],records[18:36])):
        for field in ('point','h','primitive_time','time','phases','reflected_time','reflected_phases'):
            compare(lift[field],base[field],f'period.{n}.{field}')
        assert base['torus_laps'][:6]==lift['torus_laps'][:6]
        assert base['physical_laps'][:6]==lift['physical_laps'][:6]
        difference=lift['torus_laps'][-1]-base['torus_laps'][-1]
        assert difference==shifts[base['role']]
        i,j=base['coordinate_laps']
        physical_difference=lift['physical_laps'][-1]-base['physical_laps'][-1]
        assert physical_difference==difference+56*(i+j)
        phase_period.append({'pair':base['pair'],'role':base['role'],
                             'seventh_torus_lap_increment':difference,
                             'seventh_physical_lap_increment':physical_difference})
    for offset in (0,18,36):
        by_pair={tuple(w['pair']):w for w in records[offset:offset+18]}
        for big,small in [((4,6),(2,3)),((6,10),(3,5))]:
            left,right=by_pair[big],by_pair[small]
            assert left['gcd']==2 and right['gcd']==1
            assert 2*F(left['time'])==F(right['time'])
            for field in ('point','primitive_time','phases','physical_laps','torus_laps'):
                assert left[field]==right[field]
    large=[]
    expected_deltas=[-14,14,-15,15,-(10**12+14),10**12+14]
    assert [w['construction']['delta'] for w in controls['large_slope_controls']]==expected_deltas
    def check_large(item,label,expected_row=None):
        emitted=item['witness'];A,B=emitted['row'];delta=A-B;D=abs(delta)
        a=(2*A+7*B)%8
        c=7-a if delta>0 else a-1
        lower=(F(7*D,c+2)-1)/4;upper=(F(7*D,c)-1)/4
        j=floor(lower)+1
        assert lower<j<upper and j>=3
        compare(item['construction'],{'delta':delta,'c':c,'j':j,
                'open_j_interval':[str(lower),str(upper)]},label+'.construction')
        compare(emitted['pair'],[1,4*j],label+'.pair')
        if expected_row is not None:
            compare(emitted['row'],expected_row,label+'.row')
        rec=review_record(emitted,label)
        assert not rec['seventh_safe'] and rec['distinct_speeds']
        return {'row':rec['row'],'pair':rec['pair'],'time':rec['time'],
                'seventh_phase':rec['phases'][-1],'minimum':rec['minimum'],
                'construction':item['construction']}
    for n,item in enumerate(controls['large_slope_controls']):
        delta=expected_deltas[n];D=abs(delta);b=(2-2*delta)%8
        B=8*(D//8+1)+b;A=B+delta
        assert (2*A+7*B)%8==2
        large.append(check_large(item,f'large.{n}',[A,B]))
    old_only=controls['old_only']
    new=check_large({'witness':old_only['new_failure'],'construction':old_only['construction']},
                    'old_only.new',[38,18])
    old=review_record(old_only['old_witness'],'old_only.old',old=True)
    assert old['row']==[38,18] and old['pair']==new['pair']
    assert old['seventh_safe'] and old['distinct_speeds'] and old['minimum']=='1/8'
    assert old['time']!=new['time']
    outside=[c for c in classification['cells'] if c['T'] and not c['R']]
    if outside:
        first=outside[0]
        assert [(w['row'],w['pair']) for w in controls['conditional_outside_R']]==[(first['representative'],list(p)) for p in PAIRS]
        for n,w in enumerate(controls['conditional_outside_R']):
            review_record(w,f'outside_R.{n}')
    else:
        assert controls['conditional_outside_R']==[]
    ambient=controls['ambient_fallback_failure']
    A,B=59,64;U,V=SEGMENTS[1][1]
    values=[A*x+B*y for x,y in (U,V)]
    raw=ceil(min(values))
    assert raw<=max(values)
    x=(F(raw)-F(9*B,8))/(A-3*B);y=F(9,8)-3*x
    assert U[0]<x<V[0] and A*x+B*y==raw
    assert all(F(1,8)<=phase(a*x+b*y)<=F(7,8) for a,b in CORE)
    compare(ambient,{'row':[A,B],'point':[str(x),str(y)],'seventh_raw':raw,
            'seventh_phase':0,'strictly_inside_S':True,'all_core_safe':True},'ambient')
    assert len(primary)==1307 and len(auxiliary)==27 and len(records)==58
    compare(controls['counts'],{'physical_controls':58,'large_slope_controls':6,
                              'old_only_pairs':1,'conditional_outside_R':len(controls['conditional_outside_R'])},'control_counts')
    out={'status':'PASS','review_type':'Separately structured internal AI physical review',
         'method':'Direct preserved-segment projection; coordinate-lap congruence; exact physical multiplication. No production imports.',
         'protocol_sha256':PROTOCOL_HASH,'script_sha256':sha(Path(__file__)),
         'input_sha256':{str(path.relative_to(HERE.parent.parent)):sha(path) for path in input_paths},
         'counts':dict(COUNTS,primary_failure_records=len(primary),auxiliary_failure_records=len(auxiliary),
                     frozen_physical_controls=len(records),large_slope_controls=6,old_only_physical_records=2,
                     archived_configurations_reproduced=18,phase_period_pairs=18,
                     primary_zero_phase_failures=zero_phase_failures),
         'primary_failure_roles':by_role,'all_primary_failures_have_eight_distinct_speeds':True,
         'auxiliary_failures_are_repeated_speed':True,
         'phase_period_controls':phase_period,'large_slope_controls':large,
         'old_only_comparison':{'new':new,'old':{'time':old['time'],'minimum':old['minimum'],
                    'seventh_phase':old['phases'][-1]},
                    'meaning':'Different selected times; rejected new selector does not imply absent loneliness.'},
         'repeated_core_controls':[{'row':r['row'],'pair':r['pair'],'distinct_speeds':r['distinct_speeds'],
                                    'minimum':r['minimum']} for r in records[-4:]],
         'auxiliary_control_row_6_2':{'pair':records[36]['pair'],'time':records[36]['time'],
                                     'seventh_phase':records[36]['phases'][-1]},
         'ambient_fallback_failure':ambient,
         'conditional_outside_R':'NOT_TRIGGERED' if not outside else 'COMPLETED',
         'limits':'Derived finite failure certificates and frozen controls; universal classification relies separately on the proved finite reduction. No external human/formal certification.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
