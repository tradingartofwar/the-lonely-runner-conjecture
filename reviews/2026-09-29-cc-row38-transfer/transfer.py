#!/usr/bin/env python3
"""Frozen row-(3,8) trial using unchanged clipping and compilation functions."""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(3,8))
CONTROLS = ((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
            (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10))
Z = F(1,8)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,dict):
        return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [encode(v) for v in value]
    return value


def save(name,value):
    (HERE/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs():
    record=json.loads((HERE/'INPUTS.json').read_text())
    for path,identity in record['files'].items():
        if digest(ROOT/path)!=identity['sha256']:
            raise ValueError('Pinned input mismatch: '+path)
    if digest(HERE/'PROTOCOL.md')!=record['protocol_sha256']:
        raise ValueError('Frozen protocol mismatch')
    return record


def regress(api,prior,data):
    cases=[]
    for row,path,omit in (
        ((5,2),'reviews/2026-09-29-cc-coverage-compiler/certificate.json','provenance'),
        ((6,2),'reviews/2026-09-29-cc-coefficient-transfer/certificate.json','transfer_provenance')):
        records,counts=prior.clip_candidates(data,row)
        assert counts['status']=='PASS'
        generated=api.compile_records(records,rows=ROWS[:-1]+(row,),threshold=Z,budget=400)
        archived=json.loads((ROOT/path).read_text())
        expected={k:v for k,v in archived.items() if k!=omit}
        assert encode(generated)==expected, row
        cases.append(dict(row=row,status='PASS',candidate_records=len(records),
                          all_coverage_fields_exact=True,compared_fields=sorted(expected),
                          archived_certificate_sha256=digest(ROOT/path)))
    return dict(status='PASS',cases=cases,scope='Two archived certificate regressions; no old physical reruns.')


def recover(api,record,hit,p,q):
    d=gcd(p,q);P,Q=p//d,q//d
    x,y=hit['point'];h=hit['first_integer']
    r,s,steps=api.bezout(P,Q)
    T=r*x+s*y;N=floor(T);tau=T-N;t=tau/d
    laps=[m+(-a*s+b*r)*h-(a*P+b*Q)*N for (a,b),m in zip(ROWS,record['labels'])]
    phases=[a*x+b*y-m for (a,b),m in zip(ROWS,record['labels'])]
    speeds=[a*p+b*q for a,b in ROWS]
    assert 0<t<F(1,d) and all(Z<=f<=1-Z for f in phases)
    assert all(v*t==ell+f for v,ell,f in zip(speeds,laps,phases))
    return dict(pair=[p,q],primitive=[P,Q],gcd=d,distinct_speeds=p!=q,
                segment=record['id'],contact=hit,point=[x,y],h=h,
                torus_laps=record['labels'],bezout=[r,s],euclid_divisions=steps,
                unwrapped_clock=T,N=N,primitive_time=tau,time=t,speeds=speeds,
                phases=phases,physical_laps=laps,minimum=min(min(f,1-f) for f in phases))


def controls(api,prior,certificate):
    records=certificate.get('candidates',[])
    by_id={r['id']:r for r in records}
    complete=certificate['status']=='COMPLETE_COVER_CERTIFICATE'
    menu=[by_id[i] for i in certificate['chosen_ids']] if complete else None
    chosen=menu if complete else records
    witnesses=[];misses=[];endpoint_checks=[]
    for p,q in CONTROLS:
        d=gcd(p,q);P,Q=p//d,q//d
        if complete:
            w=api.select(certificate,p,q)
        else:
            w=None
            for tests,record in enumerate(chosen,1):
                hit=prior.first_contact(record,P,Q)
                if hit:
                    w=recover(api,record,hit,p,q)
                    w['segment_tests']=tests
                    break
        if w:
            witnesses.append(prior.augment_physical(w))
        else:
            misses.append([p,q])
        entry=dict(pair=[p,q])
        for name,scope in [('all_candidates',records),('chosen_menu',menu)]:
            if scope is None:
                entry[name]=None
                continue
            closed=next((r['id'] for r in scope if prior.first_contact(r,P,Q)),None)
            opened=next((r['id'] for r in scope if prior.first_contact(r,P,Q,True)),None)
            entry[name]=dict(closed_hit=closed is not None,open_hit=opened is not None,
                             first_closed_candidate=closed,first_open_candidate=opened)
        endpoint_checks.append(entry)
    return dict(controls=witnesses,uncovered_controls=misses,endpoint_checks=endpoint_checks,
                selection_scope='complete chosen menu' if complete else 'all supplied candidates, actual contacts only',
                counts=dict(parameter_pairs=18,physical_witnesses=len(witnesses),
                            selected_phase_checks=7*len(witnesses),reflected_phase_checks=7*len(witnesses),
                            alternate_bezout_checks=len(witnesses)),
                scope='Frozen parameter list; newly evaluated row-(3,8) configurations.')


def diagnose(api,prior,data,certificate):
    if certificate['status']!='UNCOVERED_PRIMITIVE_PAIRS':
        return dict(status='NOT_TRIGGERED')
    pairs=sorted(tuple(p) for p in certificate['uncovered'])
    P,Q=next((pair for pair in pairs if pair[0]!=pair[1]),pairs[0])
    lower,upper=ceil(F(Q-7*P,8)),floor(F(4*Q-P,8))
    maximum=8*8*max(0,upper-lower+1)
    report=dict(pair=[P,Q],distinct_speeds=P!=Q,orbit_range=[lower,upper],
                seventh_laps=list(range(1,9)),section_budget=10000,maximum_sections=maximum)
    if maximum>10000:
        return dict(report,status='DIAGNOSTIC_SCOPE_LIMIT',examined=0)
    examined=[]
    for index,parent in enumerate(data['parents']):
        for lap in range(1,9):
            labels=parent['labels']+[lap]
            for H in range(lower,upper+1):
                lo,hi=F(0),F(1,2)
                for (a,b),m in zip(ROWS,labels):
                    slope=a+F(b*Q,P)
                    lo=max(lo,(m+Z+F(b*H,P))/slope)
                    hi=min(hi,(m+1-Z+F(b*H,P))/slope)
                section=dict(parent=index,seventh_lap=lap,H=H,x_interval=[lo,hi],nonempty=lo<=hi)
                examined.append(section)
                if lo<=hi:
                    x=(lo+hi)/2;y=(Q*x-H)/P
                    checks=[]
                    for name,normal,rhs in parent['constraints']:
                        lhs=sum(F(a)*v for a,v in zip(normal,(x,y,Z)))
                        assert lhs<=F(rhs),(name,lhs,rhs)
                        checks.append(dict(constraint=name,lhs=lhs,rhs=F(rhs),passed=True))
                    rec=dict(id=f'P{index}:FULL:K{lap}:H{H}',labels=labels)
                    hit=dict(point=(x,y),first_integer=H)
                    witness=prior.augment_physical(recover(api,rec,hit,P,Q))
                    membership=prior.on_old_floor_edges(data,(x,y))
                    assert not membership,'A missed edge contact contradicts the diagnostic'
                    return dict(report,status='RESTORED_PARENT_WITNESS',sections=examined,
                                examined=len(examined),witness=witness,parent_halfspace_checks=checks,
                                original_floor_edge_memberships=membership)
    return dict(report,status='NO_WITNESS_IN_RESTORED_INPUT',sections=examined,examined=len(examined))


def main():
    if not __debug__:
        raise RuntimeError('Run without -O; inherited research checks use assertions')
    frozen=inputs()
    api=load('row38_pinned_compiler','reviews/2026-09-29-cc-coverage-compiler/compiler.py')
    prior=load('row38_pinned_clipper','reviews/2026-09-29-cc-coefficient-transfer/transfer.py')
    checker=load('row38_pinned_selector','lonely_runner/cc_coefficients.py')
    data=json.loads((ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json').read_text())
    assert tuple(map(tuple,data['rows']))==ROWS[:-1] and F(data['threshold'])==Z
    save('regression.json',regress(api,prior,data))
    old=checker.check_coefficients(3,8)
    assert old['status']=='REJECTED'
    assert old['counterexample']['pair']==[1,4]
    assert old['counterexample']['time']=='5/16' and old['counterexample']['distances'][6]=='1/16'
    records,counts=prior.clip_candidates(data,(3,8))
    if counts['status']!='PASS':
        certificate=dict(status=counts['status'],clipping=counts)
    else:
        assert counts['edge_lap_attempts']<=192
        assert all(1<=s['seventh_lap']<=8 for s in records)
        certificate=api.compile_records(records,rows=ROWS,threshold=Z,budget=400)
    certificate['transfer_provenance']=dict(source_commit=frozen['source_commit'],added_row=(3,8),
        selection_rule_changed=False,clipper_changed=False,protocol_sha256=frozen['protocol_sha256'],
        input_record_sha256=digest(HERE/'INPUTS.json'),transfer_script_sha256=digest(Path(__file__)),
        regression_sha256=digest(HERE/'regression.json'),clipping_counts=counts)
    save('certificate.json',certificate)
    restored=json.loads((HERE/'certificate.json').read_text())
    run=controls(api,prior,restored)
    repaired=next((w for w in run['controls'] if w['pair']==[1,4]),None)
    run.update(status='PASS' if restored['status']=='COMPLETE_COVER_CERTIFICATE' else 'BOUNDED_OUTCOME',
               certificate_status=restored['status'],certificate_sha256=digest(HERE/'certificate.json'),
               fixed_selector_comparison=dict(old_decision=old,new_witness_at_known_failure=repaired,
                   repaired_at_pair=repaired is not None,uniform_compiler_repair=restored['status']=='COMPLETE_COVER_CERTIFICATE'),
               diagnostic=diagnose(api,prior,data,restored))
    save('run.json',run)
    print(json.dumps(dict(status=certificate['status'],clipping=counts,coverage_counts=certificate.get('counts'),
        chosen_ids=certificate.get('chosen_ids'),uncovered=certificate.get('uncovered'),
        repaired_known_pair=repaired is not None,diagnostic=run['diagnostic']['status'])))


if __name__=='__main__':
    main()
