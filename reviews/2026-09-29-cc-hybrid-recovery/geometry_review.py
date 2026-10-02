#!/usr/bin/env python3
"""Independent frozen contact-first hybrid recovery geometry audit. No production imports."""
import hashlib
import itertools
import json
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CORE=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2))
ROWS=CORE+((6,2),(3,8),(54,26))
SOURCE=ROOT/'reviews/2026-09-29-cc-segment-discovery/PARENT_INPUT.json'


def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [encode(x) for x in v]
    return v


def need(value,label):
    if not value: raise ArithmeticError(label)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def primary(p,q): return p!=q and p!=2*q


def restrict(interval,slope,constant,bound):
    lo,hi=interval
    if slope>0: hi=min(hi,(bound-constant)/slope)
    elif slope<0: lo=max(lo,(bound-constant)/slope)
    elif constant>bound: return F(1),F(0)
    return lo,hi


def band_constraints(labels,z,rows=CORE):
    out=[(-F(1),F(0),-z),(F(1),F(0),F(1,2)),
         (F(0),-F(1),-z),(F(0),F(1),1-z)]
    for (a,b),m in zip(rows,labels):
        out.extend([(F(a),F(b),m+1-z),(-F(a),-F(b),-m-z)])
    return out


def contact(record,P,Q):
    p0,p1=record['endpoints']
    h0,h1=Q*p0[0]-P*p0[1],Q*p1[0]-P*p1[1]
    low,high=sorted((h0,h1))
    integers=range(ceil(low),floor(high)+1)
    out=dict(interval=[low,high],first_integer=ceil(low),hit=bool(integers))
    if integers:
        u=F(0) if h0==h1 else (integers[0]-h0)/(h1-h0)
        point=tuple(a+u*(b-a) for a,b in zip(p0,p1))
        need(0<=u<=1 and Q*point[0]-P*point[1]==integers[0],'contact')
        out.update(parameter=u,point=point)
    return out


def coverage(records,z):
    ranking=[]
    for r in records:
        (x0,y0),(x1,y1)=r['endpoints']
        dx,dy=x1-x0,y0-y1
        if dx>0 and dy>0:
            pm,qm=ceil(1/dy)-1,ceil(1/dx)-1
            ranking.append(dict(id=r['id'],alpha=dx,beta=dy,P_max=pm,Q_max=qm,rectangle_pairs=pm*qm))
    ranking.sort(key=lambda v:v['rectangle_pairs'])
    out=dict(candidates=records,ranking=ranking,budget=400)
    if not ranking: return dict(out,status='NO_DESCENDING_SEGMENT',primary_status='INCOMPLETE')
    lead=ranking[0]
    out['leader']=lead
    if lead['rectangle_pairs']>400:
        return dict(out,status='SCOPE_LIMIT',primary_status='INCOMPLETE',enumerated_rectangle_pairs=0)
    residual=[(p,q) for p in range(1,lead['P_max']+1) for q in range(1,lead['Q_max']+1)
              if gcd(p,q)==1 and p*lead['beta']+q*lead['alpha']<1]
    matrix=[dict(id=r['id'],contacts=[dict(pair=pair,**contact(r,*pair)) for pair in residual]) for r in records]
    hits={r['id']:{tuple(c['pair']) for c in r['contacts'] if c['hit']} for r in matrix}
    menu=[lead['id']]
    missed=set(residual)-hits[lead['id']]
    steps=[]
    while missed:
        gains=[(len(missed&hits[r['id']]),r['id']) for r in records]
        most=max(n for n,_ in gains)
        if not most: break
        best=next(identity for n,identity in gains if n==most)
        gained=sorted(missed&hits[best])
        steps.append(dict(before=sorted(missed),chosen=best,newly_covered=gained))
        menu.append(best)
        missed-=set(gained)
    primary_misses=sorted(pair for pair in missed if primary(*pair))
    out.update(status='UNCOVERED_PRIMITIVE_PAIRS' if missed else 'COMPLETE_COVER_CERTIFICATE',
               primary_status='INCOMPLETE' if primary_misses else 'PRIMARY_COMPLETE',
               primary_uncovered=primary_misses,auxiliary_uncovered=sorted(set(missed)-set(primary_misses)),
               chosen_ids=menu,residual_pairs=residual,contact_matrix=matrix,
               uncovered=sorted(missed),greedy_steps=steps,
               counts=dict(candidates=len(records),descending=len(ranking),rectangle_pairs=lead['rectangle_pairs'],
                           residual_pairs=len(residual),contacts=len(records)*len(residual),chosen=len(menu)))
    return out


def compare(expected,actual,path=''):
    need(type(expected)==type(actual),'type mismatch '+path)
    if isinstance(expected,dict):
        need(expected.keys()==actual.keys(),'keys mismatch '+path)
        return sum(compare(v,actual[k],path+'/'+k) for k,v in expected.items())
    if isinstance(expected,list):
        need(len(expected)==len(actual),'length mismatch '+path)
        return sum(compare(v,actual[i],path+'/'+str(i)) for i,v in enumerate(expected))
    need(expected==actual,'value mismatch '+path)
    return 1


def decode_source(raw):
    out=[]
    for r in raw:
        d=dict(r)
        d['endpoints']=[tuple(map(F,p)) for p in r['endpoints']]
        d['source_parameters']=tuple(map(F,r['source_parameters']))
        out.append(d)
    return out


def candidate(source,row,lap,local):
    a,b=source['endpoints']
    s0,s1=source['source_parameters']
    endpoints=sorted(tuple(x+t*(y-x) for x,y in zip(a,b)) for t in local)
    labels=list(source['labels'])+[lap]
    for point in endpoints:
        need(all(F(1,8)<=dot(v,point)-m<=F(7,8) for v,m in zip(ROWS[:-1]+(row,),labels)),
             'new candidate endpoint band')
    return dict(id=source['id']+f':M{lap}',parent=source['parent'],edge=source['edge'],
                seventh_lap=source['seventh_lap'],eighth_lap=source['eighth_lap'],ninth_lap=lap,
                added_laps=[source['seventh_lap'],source['eighth_lap'],lap],labels=labels,
                endpoints=endpoints,source_parameters=[s0+t*(s1-s0) for t in local])


def append_full(sources,row):
    jobs=[]
    for source in sources:
        values=sorted(dot(row,p) for p in source['endpoints'])
        laps=range(ceil(values[0]-F(7,8)),floor(values[1]-F(1,8))+1)
        jobs.append((source,laps))
    attempts=sum(len(laps) for _,laps in jobs)
    counts=dict(source_records=len(sources),source_lap_attempts=attempts,budget=256)
    if attempts>256: return [],dict(counts,status='CLIPPING_SCOPE_LIMIT',enumerated=0)
    records=[];trace=[]
    for source,laps in jobs:
        a,b=source['endpoints']
        direction=tuple(y-x for x,y in zip(a,b))
        for lap in laps:
            interval=(F(0),F(1))
            # Rebuild all nine bands, not only the appended row's band.
            for (x,y),m in zip(ROWS[:-1]+(row,),source['labels']+[lap]):
                slope=x*direction[0]+y*direction[1]
                constant=x*a[0]+y*a[1]
                interval=restrict(interval,slope,constant,m+F(7,8))
                interval=restrict(interval,-slope,-constant,-m-F(1,8))
            nonempty=interval[0]<=interval[1]
            entry=dict(source_id=source['id'],ninth_lap=lap,local_interval=interval,nonempty=nonempty)
            if nonempty:
                record=candidate(source,row,lap,interval)
                records.append(record)
                entry.update(candidate_id=record['id'],original_interval=record['source_parameters'])
            trace.append(entry)
    counts.update(status='PASS',candidate_records=len(records),
                  point_records=sum(r['endpoints'][0]==r['endpoints'][1] for r in records))
    counts['trace']=trace
    return records,counts


def screen_sources(sources):
    row=ROWS[-1]
    checks=[];relations=[]
    for vi,v in enumerate(ROWS[:-1]):
        for ci,c in enumerate(CORE):
            delta=tuple(a-b for a,b in zip(row,v))
            possible=[];compatible=True
            for difference,coefficient in zip(delta,c):
                if coefficient==0:
                    if difference!=0: compatible=False
                else: possible.append(F(difference,8*coefficient))
            match=compatible and len(set(possible))==1 and possible[0].denominator==1 and possible[0]!=0
            k=int(possible[0]) if match else None
            check=dict(v_index=vi,c_index=ci,v=v,c=c,difference=delta,match=match,k=k)
            checks.append(check)
            if match: relations.append(dict(v_index=vi,c_index=ci,v=v,c=c,k=k))
    decisions=[];records=[]
    for source in sources:
        reasons=[];tests=[]
        for relation in relations:
            vi,ci,k=relation['v_index'],relation['c_index'],relation['k']
            c=relation['c']
            raw=[dot(c,p) for p in source['endpoints']]
            mc,mv=source['labels'][ci],source['labels'][vi]
            eps=raw[0]-mc
            constant=raw[0]==raw[1]
            boundary=eps in (F(1,8),F(7,8))
            accepted=constant and boundary
            tests.append(dict(v_index=vi,c_index=ci,k=k,raw_values=raw,core_lap=mc,
                              constant=constant,boundary=boundary,accepted=accepted))
            if accepted:
                lap=mv+8*k*mc+int(8*k*eps)
                reasons.append(dict(v_index=vi,c_index=ci,k=k,epsilon=eps,ninth_lap=lap,
                                    core_lap=mc,source_lap=mv,raw_difference=8*k*raw[0]))
        reasons.sort(key=lambda r:(r['v_index'],r['c_index'],r['k'],r['epsilon']))
        if reasons:
            need(len({r['ninth_lap'] for r in reasons})==1,'inconsistent screening laps')
            records.append(candidate(source,row,reasons[0]['ninth_lap'],(F(0),F(1))))
        decisions.append(dict(source_id=source['id'],status='SCREEN_CERTIFICATE' if reasons else 'NO_SCREEN_CERTIFICATE',
                              relation_checks=tests,reasons=reasons))
    return dict(coefficient_checks=checks,relations=relations,decisions=decisions,candidates=records,
                counts=dict(coefficient_checks=len(checks),relations=len(relations),source_records=len(sources),
                            relation_segment_checks=len(relations)*len(sources),candidate_records=len(records),
                            point_records=sum(r['endpoints'][0]==r['endpoints'][1] for r in records)))


def certificate_for_output(c,row):
    out={k:v for k,v in c.items() if k not in ('primary_status','primary_uncovered','auxiliary_uncovered')}
    out.update(schema='cc-positive-coverage-v1',rows=ROWS[:-1]+(row,),threshold=F(1,8),
               domain='positive integer p,q; ten distinct speeds iff p!=q and p!=2q; full labelled compilation includes auxiliaries')
    return out


def screen_for_output(screen):
    checks=[]
    for r in screen['coefficient_checks']:
        quotient=next(F(d,8*c) for d,c in zip(r['difference'],r['c']) if c)
        checks.append(dict(v_index=r['v_index'],c_index=r['c_index'],difference=r['difference'],
                           match=r['match'],quotient=quotient))
    relations=[dict(v_index=r['v_index'],c_index=r['c_index'],safe_row=r['v'],core_row=r['c'],k=r['k'])
               for r in screen['relations']]
    decisions=[]
    for d in screen['decisions']:
        reasons=[dict(v_index=r['v_index'],c_index=r['c_index'],k=r['k'],epsilon=r['epsilon'],
                      core_lap=r['core_lap'],ninth_lap=r['ninth_lap'],raw_shift=int(r['raw_difference']))
                 for r in d['reasons']]
        tests=[dict(v_index=r['v_index'],c_index=r['c_index'],k=r['k'],core_lap=r['core_lap'],
                    raw_values=r['raw_values'],matching_boundaries=[r['raw_values'][0]-r['core_lap']] if r['accepted'] else [])
               for r in d['relation_checks']]
        entry=dict(source_id=d['source_id'],status='ACCEPTED_WHOLE' if reasons else 'NO_SCREEN_CERTIFICATE',
                   tests=tests,reasons=reasons)
        if reasons: entry['candidate_id']=d['source_id']+':M'+str(reasons[0]['ninth_lap'])
        decisions.append(entry)
    c=screen['counts']
    counts=dict(source_records=c['source_records'],coefficient_pair_tests=c['coefficient_checks'],relations=c['relations'],
                boundary_checks=c['relation_segment_checks'],accepted_sources=c['candidate_records'],
                omitted_sources=c['source_records']-c['candidate_records'],point_records=c['point_records'],new_row_lap_attempts=0)
    return dict(status='PASS',target=ROWS[-1],coefficient_checks=checks,relations=relations,
                decisions=decisions,candidates=screen['candidates'],counts=counts)


Z=F(1,8)
CONTROLS=((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
          (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
          (2,2),(4,2),(1,20),(2,40),(5,1),(10,2))


def provenance(source):
    return source['parent'],*source['edge'],source['seventh_lap'],source['eighth_lap']


def point_at(source,u):
    a,b=source['endpoints']
    return tuple(x+u*(y-x) for x,y in zip(a,b))


def source_bounds(source,pair,row=ROWS[-1]):
    p,q=pair
    hs=[q*x-p*y for x,y in source['endpoints']]
    raw=sorted(dot(row,p) for p in source['endpoints'])
    hr=(ceil(min(hs)),floor(max(hs)))
    mr=(ceil(raw[0]-(1-Z)),floor(raw[1]-Z))
    hc=max(0,hr[1]-hr[0]+1)
    return dict(source_id=source['id'],pair=pair,projection=hs,raw_range=raw,h_range=hr,
                lap_range=mr,h_count=hc,work_bound=hc*max(1,mr[1]-mr[0]+1))


def preflight(sources,pairs,budget=4096):
    entries=[source_bounds(s,p) for p in pairs for s in sorted(sources,key=provenance)]
    work=sum(r['work_bound'] for r in entries)
    return dict(status='PASS' if work<=budget else 'RECOVERY_SCOPE_LIMIT',budget=budget,
                work_bound=work,rows=entries,source_pair_projections=len(entries),
                new_row_raw_ranges=len(entries),integer_h_bound=sum(r['h_count'] for r in entries))


def full_band_contacts(source,pair,row,opened):
    """Independent oracle: clip new bands first, then intersect integer orbits."""
    if opened and source['endpoints'][0]==source['endpoints'][1]: return []
    meta=source_bounds(source,pair,row)
    h0,h1=meta['projection'];dh=h1-h0
    r0,r1=(dot(row,p) for p in source['endpoints']);dr=r1-r0
    contacts=[]
    for m in range(meta['lap_range'][0],meta['lap_range'][1]+1):
        interval=(F(0),F(1))
        interval=restrict(interval,dr,r0,m+1-Z)
        interval=restrict(interval,-dr,-r0,-m-Z)
        lo,hi=interval
        if lo>hi or (opened and (hi<=0 or lo>=1)): continue
        ends=(h0+lo*dh,h0+hi*dh)
        for h in range(ceil(min(ends)),floor(max(ends))+1):
            if dh:
                u=(h-h0)/dh
                if opened and not 0<u<1: continue
            else:
                u=(lo+hi)/2 if opened and lo==0 else lo
            need(lo<=u<=hi and (not opened or 0<u<1),'oracle parameter')
            contacts.append(dict(h=h,parameter=u,point=point_at(source,u),ninth_lap=m))
    contacts.sort(key=lambda c:(c['h'],c['ninth_lap'],c['parameter']))
    return contacts


def query(source,pair,row=ROWS[-1],opened=False):
    meta=source_bounds(source,pair,row)
    h0,h1=meta['projection'];dh=h1-h0
    trace=[]
    counts=dict(h_tests=0,point_phase_tests=0,parallel_band_tests=0)
    oracle=full_band_contacts(source,pair,row,opened)
    witness=None
    if not (opened and source['endpoints'][0]==source['endpoints'][1]):
        for h in range(meta['h_range'][0],meta['h_range'][1]+1):
            counts['h_tests']+=1
            if dh:
                u=(h-h0)/dh
                point=point_at(source,u)
                raw=dot(row,point);lap=floor(raw);phase=raw-lap
                accepted=Z<=phase<=1-Z and (not opened or 0<u<1)
                counts['point_phase_tests']+=1
                trace.append(dict(h=h,branch='POINT',parameter=u,raw=raw,lap=lap,phase=phase,accepted=accepted))
                if accepted: witness=dict(h=h,parameter=u,point=point,ninth_lap=lap)
            else:
                r0,r1=(dot(row,p) for p in source['endpoints']);dr=r1-r0
                for lap in range(meta['lap_range'][0],meta['lap_range'][1]+1):
                    counts['parallel_band_tests']+=1
                    interval=(F(0),F(1))
                    interval=restrict(interval,dr,r0,lap+1-Z)
                    interval=restrict(interval,-dr,-r0,-lap-Z)
                    lo,hi=interval
                    accepted=lo<=hi and (not opened or (hi>0 and lo<1))
                    trace.append(dict(h=h,branch='PARALLEL',lap=lap,interval=interval,accepted=accepted))
                    if accepted:
                        u=(lo+hi)/2 if opened and lo==0 else lo
                        witness=dict(h=h,parameter=u,point=point_at(source,u),ninth_lap=lap)
                        break
            if witness: break
    need(encode(witness)==encode(oracle[0] if oracle else None),'contact-first versus band-first canonical witness')
    return dict(status='HIT' if witness else 'NO_SOURCE_CONTACT',trace=trace,counts=counts,witness=witness)


def recover(sources,pairs,budget=4096,opened=False):
    check=preflight(sources,pairs,budget)
    out=dict(status=check['status'],preflight=check,queries=[],exceptions=[],uncovered=[],
             counts=dict(source_visits=0,h_tests=0,point_phase_tests=0,parallel_band_tests=0))
    if check['status']!='PASS': return out
    for pair in pairs:
        found=False
        for source in sorted(sources,key=provenance):
            result=query(source,pair,opened=opened)
            out['queries'].append(dict(pair=pair,source_id=source['id'],**result))
            out['counts']['source_visits']+=1
            for k,v in result['counts'].items(): out['counts'][k]+=v
            if result['witness']:
                w=result['witness'];s0,s1=source['source_parameters']
                out['exceptions'].append(dict(pair=pair,source_id=source['id'],parent=source['parent'],edge=source['edge'],
                    local_parameter=w['parameter'],original_parameter=s0+w['parameter']*(s1-s0),point=w['point'],h=w['h'],
                    labels=source['labels']+[w['ninth_lap']],ninth_lap=w['ninth_lap'],source_endpoint=w['point'] in source['endpoints']))
                found=True;break
        if not found: out['uncovered'].append(pair)
    out['status']='COMPLETE_EXCEPTION_RECOVERY' if not out['uncovered'] else 'NO_SOURCE_CONTACT'
    return out


def fixtures():
    cases=(('nonconstant_unsafe_then_safe',((0,0),(3,1))),
           ('constant_integer_band',((0,0),(1,1))),
           ('constant_noninteger',((0,F(1,2)),(1,F(3,2)))),
           ('singleton',((F(1,4),F(1,4)),(F(1,4),F(1,4)))))
    out=[]
    for name,ends in cases:
        result=query(dict(id=name,endpoints=[tuple(map(F,p)) for p in ends]),(1,1),(1,0))
        out.append(dict(name=name,endpoints=ends,target=(1,0),result=result))
    return dict(status='PASS',cases=out,scope='Kernel fixtures only; not physical runner targets')


def dispatch(certificate,recovery,p,q):
    d=gcd(p,q);pair=(p//d,q//d)
    exception=next((r for r in recovery['exceptions'] if tuple(r['pair'])==pair),None)
    if exception:
        r=exception
        hit=dict(hit=True,point=r['point'],first_integer=r['h'],parameter=r['local_parameter'])
        return dict(pair=[p,q],route='EXCEPTION_POINT',source_id=r['source_id'],
                    witness=dict(segment='EXCEPTION:'+r['source_id']+f':M{r["ninth_lap"]}',contact=hit,
                                 point=r['point'],h=r['h'],torus_laps=r['labels'],primitive=pair))
    by_id={r['id']:r for r in certificate['candidates']}
    for identity in certificate['chosen_ids']:
        record=by_id[identity];hit=contact(record,*pair)
        if hit['hit']:
            return dict(pair=[p,q],route='SCREEN_MENU',witness=dict(segment=identity,contact=hit,point=hit['point'],
                        h=hit['first_integer'],torus_laps=record['labels'],primitive=pair))
    raise ArithmeticError('dispatch missed a declared covered direction')


def project_dispatch(actual):
    wanted=('segment','contact','point','h','torus_laps','primitive')
    return [dict({k:v for k,v in r.items() if k!='witness'},witness={k:v for k,v in r['witness'].items() if k in wanted}) for r in actual]


def main():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    need(digest(HERE/'PROTOCOL.md')==pins['protocol_sha256'],'protocol changed')
    for path,pin in pins['files'].items(): need(digest(ROOT/path)==pin['sha256'],'input changed '+path)
    raw=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())['certificate']['candidates']
    sources=decode_source(raw)
    validated=0
    for source in sources:
        need(len(source['labels'])==8 and all(type(m) is int for m in source['labels']),'source labels')
        for point in source['endpoints']:
            need(all(0<=x<1 for x in point),'source fundamental square')
            for row,m in zip(ROWS[:-1],source['labels']):
                need(Z<=dot(row,point)-m<=1-Z,'source band validation');validated+=1
    screen=screen_sources(sources)
    compact=coverage(screen['candidates'],Z)
    recovered=recover(sources,compact['uncovered'])
    expected_hybrid=dict(status='COMPLETE_HYBRID_CERTIFICATE',screen_counts=screen_for_output(screen)['counts'],
                         screen_certificate=certificate_for_output(compact,ROWS[-1]),recovery=recovered,
                         source_validation_endpoint_band_checks=validated)
    actual_hybrid=json.loads((HERE/'hybrid.json').read_text())
    counts={'hybrid':compare(encode(expected_hybrid),actual_hybrid,'hybrid')}
    # Only now read the archived answers, after independent construction.
    archived_restricted=json.loads((ROOT/'reviews/2026-09-29-cc-phase-screen/restricted.json').read_text())['certificate']
    counts['archived_restricted']=compare(encode(expected_hybrid['screen_certificate']),archived_restricted,'archived restricted')
    full_records,full_clipping=append_full(sources,ROWS[-1])
    full=coverage(full_records,Z)
    archived_full=json.loads((ROOT/'reviews/2026-09-29-cc-phase-screen/full.json').read_text())['certificate']
    counts['archived_full']=compare(encode(certificate_for_output(full,ROWS[-1])),archived_full,'archived full')
    membership=[]
    for e in recovered['exceptions']:
        rec=next(r for r in full_records if r['id']==e['source_id']+f':M{e["ninth_lap"]}')
        need(rec['labels']==e['labels'],'inherited and new labels')
        lo,hi=rec['source_parameters']
        need(lo<=e['original_parameter']<=hi,'recovered full membership')
        membership.append(dict(pair=e['pair'],candidate_id=rec['id'],original_parameter=e['original_parameter'],
                               full_parameter_interval=(lo,hi),labels_equal=True))
    opened=recover(sources,compact['uncovered'],opened=True)
    zero=recover(sources,compact['uncovered'],budget=0)
    need(not zero['queries'] and not zero['exceptions'] and all(v==0 for v in zero['counts'].values()),'zero cap queried source')
    residual=[dispatch(compact,recovered,*pair) for pair in compact['residual_pairs']]
    controls=[dispatch(compact,recovered,*pair) for pair in CONTROLS]
    kernel=fixtures()
    actual_audit=json.loads((HERE/'audit.json').read_text())
    expected_audit=dict(status='PASS',archived_restricted_certificate_equal=True,archived_full_certificate_equal=True,
                        exception_membership=membership,residual_dispatch=residual,physical_controls=controls,
                        open_source_diagnostic=opened,zero_budget=dict(status=zero['status'],work_bound=zero['preflight']['work_bound']),
                        kernel=kernel)
    actual_audit['residual_dispatch']=project_dispatch(actual_audit['residual_dispatch'])
    actual_audit['physical_controls']=project_dispatch(actual_audit['physical_controls'])
    counts['audit_geometry']=compare(encode(expected_audit),actual_audit,'audit geometry')
    expected_summary=dict(protocol_sha256=pins['protocol_sha256'],status=expected_hybrid['status'],target=ROWS[-1],threshold=Z,
        screen_counts=expected_hybrid['screen_counts'],screen_compiler_counts=compact['counts'],leader=compact['leader'],
        exception_pairs=compact['uncovered'],recovered=recovered['exceptions'],recovery_counts=recovered['counts'],
        preflight={k:v for k,v in recovered['preflight'].items() if k!='rows'},full_compiler_counts=full['counts'],
        full_clipping_counts={k:v for k,v in full_clipping.items() if k!='trace'},physical_controls=len(CONTROLS),
        residual_dispatch_checks=len(residual),open_source_status=opened['status'],open_source_uncovered=opened['uncovered'],
        primary_controls=sum(primary(*pair) for pair in CONTROLS),source_validation_endpoint_band_checks_per_method=validated,
        evidence='Exact development repair; general completeness/coverage remains internally reviewed proof candidate')
    counts['summary']=compare(encode(expected_summary),json.loads((HERE/'summary.json').read_text()),'summary')
    report=dict(status='PASS',protocol_sha256=pins['protocol_sha256'],script_sha256=digest(Path(__file__)),
                source_sha256=pins['files']['reviews/2026-09-29-cc-nine-runner/stage8.json']['sha256'],
                compared_sha256={name:digest(HERE/(name+'.json')) for name in ('hybrid','audit','summary')},
                method='independent screen/compile reconstruction, band-first contact oracle plus exact trace reconstruction; no production imports',
                field_counts=counts,total_scalar_fields_compared=sum(counts.values()),
                preflight={k:v for k,v in recovered['preflight'].items() if k!='rows'},
                recovery_counts=recovered['counts'],exceptions=recovered['exceptions'],
                open_recovery_counts=opened['counts'],open_exceptions=opened['exceptions'],
                kernel=kernel,zero_budget=dict(status=zero['status'],source_visits=zero['counts']['source_visits']),
                dispatch_checks=dict(residual_directions=len(residual),declared_controls=len(controls)),
                timing='Not rerun or used as correctness evidence; no additional targets')
    print(json.dumps(encode(report),indent=2,sort_keys=True))


if __name__=='__main__': main()
