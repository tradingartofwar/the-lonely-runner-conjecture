#!/usr/bin/env python3
"""Frozen sufficient phase screen versus complete supplied-edge clipping."""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CORE=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2))
BASE=CORE+((6,2),(3,8))
TARGET=(54,26)
ROWS=BASE+(TARGET,)
Z=F(1,8)
DOMAIN='positive integer p,q; ten distinct speeds iff p!=q and p!=2q; full labelled compilation includes auxiliaries'


def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [encode(x) for x in v]
    return v


def save(name,v): (HERE/name).write_text(json.dumps(encode(v),indent=2,sort_keys=True)+'\n')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def key(s): return s['parent'],*s['edge'],*s['added_laps']
def source_key(s): return s['parent'],*s['edge'],s['seventh_lap'],s['eighth_lap']
def primary(p,q): return p!=q and p!=2*q
def dot(row,p): return sum(a*x for a,x in zip(row,p))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


def inputs():
    d=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==d['protocol_sha256']
    for path,pin in d['files'].items(): assert digest(ROOT/path)==pin['sha256'],path
    return d


def child(source,lap,endpoints,parameters):
    k,l=source['seventh_lap'],source['eighth_lap']
    return dict(id=source['id']+f':M{lap}',parent=source['parent'],edge=tuple(source['edge']),
                seventh_lap=k,eighth_lap=l,ninth_lap=lap,added_laps=(k,l,lap),
                labels=tuple(source['labels'])+(lap,),endpoints=endpoints,source_parameters=parameters)


def full_clip(sources,u):
    jobs=[]
    for s in sorted(sources,key=source_key):
        a,b=[tuple(map(F,p)) for p in s['endpoints']];sa,sb=dot(u,a),dot(u,b)
        laps=range(ceil(min(sa,sb)-(1-Z)),floor(max(sa,sb)-Z)+1)
        jobs.append((s,a,b,sa,sb,laps))
    attempts=sum(len(job[-1]) for job in jobs)
    counts=dict(source_records=len(sources),source_lap_attempts=attempts,budget=256)
    if attempts>256: return [],dict(counts,status='CLIPPING_SCOPE_LIMIT',enumerated=0)
    records=[];trace=[]
    for s,a,b,sa,sb,laps in jobs:
        for m in laps:
            lo,hi=F(0),F(1);ds=sb-sa
            if ds:
                u0,u1=sorted(((m+Z-sa)/ds,(m+1-Z-sa)/ds));lo=max(lo,u0);hi=min(hi,u1)
            elif not m+Z<=sa<=m+1-Z: lo,hi=F(1),F(0)
            item=dict(source_id=s['id'],ninth_lap=m,local_interval=(lo,hi),nonempty=lo<=hi)
            if lo<=hi:
                endpoints=sorted(tuple(x+t*(y-x) for x,y in zip(a,b)) for t in (lo,hi))
                s0,s1=map(F,s['source_parameters']);parameters=tuple(s0+t*(s1-s0) for t in (lo,hi))
                record=child(s,m,endpoints,parameters);records.append(record)
                item.update(candidate_id=record['id'],original_interval=parameters)
            trace.append(item)
    return sorted(records,key=key),dict(counts,status='PASS',candidate_records=len(records),
        point_records=sum(r['endpoints'][0]==r['endpoints'][1] for r in records),trace=trace)


def screen(sources,u):
    checks=[];relations=[]
    for vi,v in enumerate(BASE):
        diff=tuple(a-b for a,b in zip(u,v))
        for ci,c in enumerate(CORE):
            axis=next(i for i,a in enumerate(c) if a)
            quotient=F(diff[axis],8*c[axis])
            match=quotient.denominator==1 and quotient!=0 and all(d==8*quotient*a for d,a in zip(diff,c))
            checks.append(dict(v_index=vi,c_index=ci,difference=diff,quotient=quotient,match=match))
            if match: relations.append(dict(v_index=vi,c_index=ci,k=int(quotient),safe_row=v,core_row=c))
    records=[];decisions=[];boundary_checks=0
    for s in sorted(sources,key=source_key):
        endpoints=[tuple(map(F,p)) for p in s['endpoints']];tests=[];reasons=[]
        for relation in relations:
            vi,ci,k=relation['v_index'],relation['c_index'],relation['k']
            raw=[dot(CORE[ci],p) for p in endpoints];m=s['labels'][ci]
            boundaries=[epsilon for epsilon in (Z,1-Z) if raw[0]==raw[1]==m+epsilon]
            tests.append(dict(v_index=vi,c_index=ci,k=k,raw_values=raw,core_lap=m,
                              matching_boundaries=boundaries));boundary_checks+=1
            for epsilon in boundaries:
                shift=8*k*m+(k if epsilon==Z else 7*k)
                reasons.append(dict(v_index=vi,c_index=ci,k=k,epsilon=epsilon,
                                    core_lap=m,raw_shift=shift,ninth_lap=s['labels'][vi]+shift))
        reasons.sort(key=lambda r:(r['v_index'],r['c_index'],r['k'],r['epsilon']))
        decision=dict(source_id=s['id'],tests=tests,reasons=reasons,
                      status='ACCEPTED_WHOLE' if reasons else 'NO_SCREEN_CERTIFICATE')
        if reasons:
            lap=reasons[0]['ninth_lap'];assert all(r['ninth_lap']==lap for r in reasons)
            record=child(s,lap,endpoints,tuple(map(F,s['source_parameters'])))
            assert all(Z<=dot(row,p)-m<=1-Z for row,m in zip(BASE+(u,),record['labels']) for p in endpoints)
            decision['candidate_id']=record['id'];records.append(record)
        decisions.append(decision)
    return dict(status='PASS',target=u,coefficient_checks=checks,relations=relations,decisions=decisions,
                candidates=sorted(records,key=key),counts=dict(coefficient_pair_tests=len(checks),
                relations=len(relations),source_records=len(sources),boundary_checks=boundary_checks,
                accepted_sources=len(records),omitted_sources=len(sources)-len(records),
                new_row_lap_attempts=0,point_records=sum(r['endpoints'][0]==r['endpoints'][1] for r in records)))


def compile_branch(api,ten,prior,records,clip_status='PASS'):
    if clip_status=='PASS':
        cert=api.compile_records(records,rows=ROWS,threshold=Z,budget=400);cert['domain']=DOMAIN
    else: cert={'status':clip_status,'candidates':[]}
    primary_complete=cert['status']=='COMPLETE_COVER_CERTIFICATE' or (
        cert['status']=='UNCOVERED_PRIMITIVE_PAIRS' and not any(primary(*p) for p in cert['uncovered']))
    return dict(certificate=cert,primary_status='PRIMARY_COMPLETE' if primary_complete else 'NO_PRIMARY_GUARANTEE',
                controls=ten.controls(api,prior,cert,Z,primary_complete))


def all_contacts(api,records,pair):
    found=[(r,api.contact(r,*pair)) for r in records]
    found=[(r,h) for r,h in found if h['hit']]
    return dict(hit=bool(found),contact_ids=[r['id'] for r,h in found],
                first_contact=dict(candidate_id=found[0][0]['id'],contact=found[0][1]) if found else None)


def compare(api,ten,screen_record,restricted,full):
    rc,fc=restricted['certificate'],full['certificate']
    reduced=lambda c:c['status'] in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS') and 'residual_pairs' in c
    global_scope=reduced(rc) and reduced(fc)
    pairs=sorted({tuple(p) for c in (rc,fc) for p in c.get('residual_pairs',[])})
    assert len(pairs)<=800
    full_by_id={r['id']:r for r in fc.get('candidates',[])};subset=[]
    for s in rc.get('candidates',[]):
        match=s['id'] in full_by_id and encode(s)==encode(full_by_id[s['id']])
        subset.append(dict(id=s['id'],identical_full_candidate=match))
        if full['certificate']['status']!='CLIPPING_SCOPE_LIMIT': assert match,s['id']
    rows=[]
    for pair in pairs:
        rows.append(dict(pair=pair,primary=primary(*pair),
            restricted=all_contacts(api,rc.get('candidates',[]),pair),
            full=all_contacts(api,fc.get('candidates',[]),pair)))
    lost=[r for r in rows if not r['restricted']['hit'] and r['full']['hit']]
    primary_lost=[r for r in lost if r['primary']]
    recovered={'status':'NOT_TRIGGERED'}
    if primary_lost:
        row=primary_lost[0];first=row['full']['first_contact'];s=full_by_id[first['candidate_id']]
        source_id=s['id'].rsplit(':M',1)[0]
        decision=next(d for d in screen_record['decisions'] if d['source_id']==source_id)
        assert decision['status']=='NO_SCREEN_CERTIFICATE'
        recovered=dict(status='OMITTED_SOURCE_WITNESS',pair=row['pair'],source_id=source_id,
                       failed_screen_decision=decision,witness=ten.recover(api,s,first['contact'],*row['pair'],Z))
    return dict(scope='ALL_POSITIVE_PRIMITIVE_DIRECTIONS' if global_scope else 'REACHED_FINITE_UNION_ONLY',
        complete_reduction_prerequisites=global_scope,union_pairs=pairs,rows=rows,
        subset_checks=subset,all_subset_checks_pass=all(x['identical_full_candidate'] for x in subset),
        lost_primary_pairs=[r['pair'] for r in primary_lost],
        lost_auxiliary_pairs=[r['pair'] for r in lost if not r['primary']],
        both_miss_pairs=[r['pair'] for r in rows if not r['restricted']['hit'] and not r['full']['hit']],
        lost_primary_witness=recovered,
        scope_note='Outside the union, both leaders have width at least one only when both full finite reductions were reached.')


def main():
    pins=inputs()
    api=load('phase_compiler','reviews/2026-09-29-cc-coverage-compiler/compiler.py');api.key=key
    prior=load('phase_open_contacts','reviews/2026-09-29-cc-coefficient-transfer/transfer.py')
    ten=load('phase_ten_recovery','reviews/2026-09-29-cc-ten-runner/transfer.py')
    source=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())
    sources=source['certificate']['candidates'];assert len(sources)==36
    assert tuple(map(tuple,source['certificate']['rows']))==BASE
    assert F(source['certificate']['threshold'])==Z
    old_records,old_counts=full_clip(sources,(38,18));assert old_counts['status']=='PASS'
    old=api.compile_records(old_records,rows=BASE+((38,18),),threshold=Z,budget=400);old['domain']=DOMAIN
    archived=json.loads((ROOT/'reviews/2026-09-29-cc-ten-runner/stage8.json').read_text())['certificate']
    assert encode(old)==archived
    save('regression.json',dict(status='PASS',row=(38,18),all_certificate_fields_exact=True,
         source_lap_attempts=old_counts['source_lap_attempts'],candidate_records=len(old_records),
         scope='Sequential append clip reproduces prior simultaneous-clip coverage certificate; no old physical rerun.'))
    ten.ROWS=ROWS;ten.ADDED=ROWS[6:]
    screened=screen(sources,TARGET);save('screen.json',screened)
    restricted=compile_branch(api,ten,prior,screened['candidates']);save('restricted.json',restricted)
    full_records,full_counts=full_clip(sources,TARGET);save('full_clipping.json',full_counts)
    full=compile_branch(api,ten,prior,full_records,full_counts['status']);save('full.json',full)
    comparison=compare(api,ten,screened,restricted,full);save('comparison.json',comparison)
    parent=json.loads((ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json').read_text())
    diagnostic=ten.diagnostic(api,parent,full['certificate'],Z);save('diagnostic.json',diagnostic)
    summary=dict(protocol_sha256=pins['protocol_sha256'],target=TARGET,threshold=Z,
        restricted=dict(status=restricted['certificate']['status'],primary_status=restricted['primary_status'],
                        counts=restricted['certificate'].get('counts'),screen_counts=screened['counts']),
        full=dict(status=full['certificate']['status'],primary_status=full['primary_status'],
                  counts=full['certificate'].get('counts'),clip_counts={k:v for k,v in full_counts.items() if k!='trace'}),
        comparison_scope=comparison['scope'],union_pairs=len(comparison['union_pairs']),
        lost_primary_pairs=comparison['lost_primary_pairs'],lost_auxiliary_pairs=comparison['lost_auxiliary_pairs'],
        both_miss_pairs=comparison['both_miss_pairs'],diagnostic_status=diagnostic['status'])
    save('summary.json',summary);print(json.dumps(encode(summary),sort_keys=True))


if __name__=='__main__': main()
