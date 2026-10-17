"""Full closed-band oracle; imports no primary selector or H/G implementation."""
import argparse
from fractions import Fraction as Q
from math import ceil, floor, gcd
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def dump(x):
    return json.dumps(x,sort_keys=True,indent=2,
                     default=lambda z:str(z) if isinstance(z,Q) else z)+'\n'


def full_set(speeds,d,counts):
    current=[(Q(0),Q(1))]
    for s in sorted(speeds):
        bands=[((k+d)/s,(k+1-d)/s) for k in range(s)]
        counts['input_bands']+=s
        i=j=0; result=[]
        while i<len(current) and j<len(bands):
            counts['intersection_pairs']+=1
            a,b=current[i]; u,v=bands[j]
            lo,hi=max(a,u),min(b,v)
            if lo<=hi:
                if result and lo<=result[-1][1]:
                    result[-1]=(result[-1][0],max(hi,result[-1][1]))
                else: result.append((lo,hi))
            if b<v: i+=1
            elif v<b: j+=1
            else: i+=1; j+=1
        current=result
    return current


def contact(interval,r,d,counts):
    a,b=interval
    counts['contact_queries']+=1
    # A safe band [ (k+d)/r, (k+1-d)/r ] intersects [a,b] iff
    # r*a-(1-d) <= k <= r*b-d has an integer solution.
    low,high=ceil(r*a-(1-d)),floor(r*b-d)
    return low<=high


def classify(interval,d,cap,counts):
    a,b=interval
    if a==b:
        return dict(status='BLOCKED',r=a.denominator,singleton=True)
    R=ceil(2*d/(b-a))
    for r in range(1,min(R-1,cap)+1):
        if not contact(interval,r,d,counts):
            return dict(status='BLOCKED',r=r,cutoff=R)
    return dict(status='YES' if R-1<=cap else 'UNKNOWN_CONTACTS',cutoff=R)


def safe_point(t,S,d):
    return all(d <= s*t-floor(s*t) <= 1-d for s in S)


def core_interval(interval,S,d):
    a,b=interval
    for s in S:
        k=floor(s*a)
        assert (k+d)/s<=a<=b<=(k+1-d)/s


def independent_G(c,S,d):
    bounds=[]
    for s in S:
        k=floor(s*c)
        bounds.append(min(c-(k+d)/s,(k+1-d)/s-c))
    return min(bounds)


def verify_trace(primary,S,d,components,cap,counts):
    records=primary['safe_candidates']
    positive=[x for x in components if x[0]<x[1]]
    assert len(records)<=len(positive)
    for rec,component in zip(records,positive):
        interval=tuple(map(Q,rec['interval'])); assert interval==component
        c,G=Q(rec['center']),Q(rec['G'])
        assert c==sum(interval)/2 and G==(interval[1]-interval[0])/2
        assert G==independent_G(c,S,d)
        assert c.denominator<=2*d.denominator*max(S)**2
        core_interval(interval,S,d)
        if rec['status']!='EXACT': continue
        H=Q(rec['H']); r=rec['critical']; q=r*c; k=floor(q+Q(1,2))
        assert H>0 and abs(q-k)+r*H==d
        assert classify((c-H,c+H),d,cap,counts)['status']=='YES'
        assert Q(rec['M'])==G-H
        assert rec['terms']<=c.denominator
        if rec['stop']=='DENOMINATOR': assert rec['terms']==c.denominator
        else: assert d/(rec['terms']+1)<=H
        if rec['decision']=='YES': assert H<=G
        else:
            assert H>G and r not in S
            assert abs(q-k)+r*G<d
            assert rec['blocker']==dict(r=r,integer=k)
        counts['H_certificates']+=1
    if primary['status']=='NO':
        assert primary['exhausted'] and len(records)==len(positive)
        assert primary['counts']['raw_events']==2*sum(S)
        # Independently enumerate raw event values for coverage accounting only.
        events={Q(0),Q(1)}
        for s in S:
            for k in range(s): events.update(((k+d)/s,(k+1-d)/s))
        assert primary['counts']['candidates']==len(events)-1
        assert primary['counts']['distinct_events']==len(events)-2
    counts['safe_candidate_records']+=len(records)


def verify_grid(row,S,d,cap,counts):
    found=None
    for v in range(2,len(S)+3):
        for u in range(1,v):
            if gcd(u,v)!=1: continue
            c=Q(u,v); G=independent_G(c,S,d)
            if G<=0: continue
            decision=classify((c-G,c+G),d,cap,counts)
            assert decision['status']!='UNKNOWN_CONTACTS'
            if decision['status']=='YES': found=c; break
        if found is not None: break
    if found is None: assert row['status']=='NO_GRID_CENTER'
    else:
        assert row['status']=='FOUND' and Q(row['center'])==found
        h,g=Q(row['H']),Q(row['G'])
        core_interval((found-g,found+g),S,d)
        assert 0<h<=g and classify((found-h,found+h),d,cap,counts)['status']=='YES'


def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--output',required=True)
    p.add_argument('--checkpoint-dir',required=True); a=p.parse_args()
    raw=Path(a.input).read_bytes(); source=json.loads(raw)
    rel='experiments/runner-addition/center-selection/'
    manifest=HERE/'manifest.json'
    assert manifest.read_bytes()==subprocess.check_output(['git','show',source['freeze']+':'+rel+'manifest.json'],cwd=ROOT)
    for path,digest in json.loads(manifest.read_text())['sha256'].items():
        content=(ROOT/path).read_bytes()
        assert hashlib.sha256(content).hexdigest()==digest
        assert content==subprocess.check_output(['git','show',source['freeze']+':'+path],cwd=ROOT)
    cfg=json.loads((HERE/'config.json').read_text()); cap=cfg['caps']['contacts']
    assert [r['case'] for r in source['cases']]==cfg['cases']
    checkpoint=Path(a.checkpoint_dir); checkpoint.mkdir(parents=True,exist_ok=True)
    counts=dict(contact_queries=0,H_certificates=0,safe_candidate_records=0,witnesses=0)
    out=dict(status='PASS',freeze=source['freeze'],primary_sha256=hashlib.sha256(raw).hexdigest(),cases=[],verification_work=counts)
    for row in source['cases']:
        case=row['case']; S,d=case['speeds'],Q(case['d'])
        geometry=dict(input_bands=0,intersection_pairs=0)
        C=full_set(S,d,geometry)
        oracle_work=dict(contact_queries=0)
        diagnostic_work=dict(contact_queries=0)
        classified=[]; first=None; unknown=False
        for I in C:
            checks=oracle_work if first is None else diagnostic_work
            verdict=classify(I,d,cap,checks)
            classified.append(dict(interval=I,**verdict))
            if verdict['status']=='YES' and first is None: first=I
            if verdict['status'].startswith('UNKNOWN'): unknown=True
            if verdict['status']=='BLOCKED':
                r=verdict['r']; m=floor(r*(I[0]+I[1])/2+Q(1,2))
                assert r not in S and r*I[1]-d<m<r*I[0]+d
        status='YES' if first else 'UNKNOWN' if unknown else 'NO'
        primary=row['primary']
        if primary['status'] in ('YES','NO'):
            assert primary['status']==status,(case['id'],primary['status'],status)
        else: out['status']='INCOMPLETE'
        if status=='UNKNOWN': out['status']='INCOMPLETE'
        if primary['status']=='YES': assert tuple(map(Q,primary['selected']['interval']))==first
        if 'expected' in case: assert status==case['expected']
        verify_trace(primary,S,d,C,cap,counts)
        verify_grid(row['heuristic'],S,d,cap,counts)
        for witness in row['witnesses']:
            r,t=witness['r'],Q(witness['t'])
            assert r not in S and first[0]<=t<=first[1] and safe_point(t,S+[r],d)
            assert list(map(Q,witness['phases']))==[s*t-floor(s*t) for s in S+[r]]
            assert witness['laps']==[floor(s*t) for s in S+[r]]
            counts['witnesses']+=1
        blockers={v['r'] for v in classified if v['status']=='BLOCKED'}
        blockers.update(x['blocker']['r'] for x in primary['safe_candidates'] if x.get('decision')=='BLOCKED')
        children=[]; child_work=dict(input_bands=0,intersection_pairs=0)
        for r in sorted(blockers):
            if r>cfg['caps']['child_speed']:
                children.append(dict(r=r,status='UNKNOWN_CHILD')); out['status']='INCOMPLETE'; continue
            child=full_set(S+[r],d,child_work)
            t=child[0][0] if child else None
            if t is not None: assert safe_point(t,S+[r],d)
            children.append(dict(r=r,status='NONEMPTY' if child else 'EMPTY',witness=t,
                                 components=len(child),sha256=hashlib.sha256(dump(child).encode()).hexdigest()))
        item=dict(id=case['id'],arm=case['arm'],status=status,components=classified,
                  first_universal=first,geometry_work=geometry,decision_contact_work=oracle_work,
                  extra_component_diagnostics=diagnostic_work,child_work=child_work,children=children,
                  grid_miss=status=='YES' and row['heuristic']['status']=='NO_GRID_CENTER')
        out['cases'].append(item)
        (checkpoint/(case['id']+'.json')).write_text(dump(item))
    budgets=source['budget_controls']
    for key,expected in [('events','UNKNOWN_EVENTS'),('candidates','UNKNOWN_CANDIDATES'),
                         ('speed_sum','UNKNOWN_PREFLIGHT'),('H_terms','UNKNOWN_H')]:
        assert budgets[key]['status']==expected and not budgets[key].get('exhausted',False)
    assert budgets['specified_center']['status']=='UNKNOWN_H'
    out['budget_controls']='PASS'
    # Explicit counterexample to boundary-only centers: singleton core speed 1.
    assert independent_G(Q(1,3),[1],Q(1,3))==0
    assert independent_G(Q(2,3),[1],Q(1,3))==0
    assert classify((Q(1,3),Q(2,3)),Q(1,3),cap,counts)['status']=='YES'
    out['boundary_only_counterexample']=dict(S=[1],d='1/3',boundaries=['1/3','2/3'],
                                             selected_center='1/2',H='1/6',G='1/6',M='0')
    Path(a.output).write_text(dump(out))
    print(dump(dict(status=out['status'],cases=len(out['cases']),verification_work=counts,
                    grid_misses=[x['id'] for x in out['cases'] if x['grid_miss']])))

if __name__=='__main__': main()
