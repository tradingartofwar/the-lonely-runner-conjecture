#!/usr/bin/env python3
"""Independent frozen boundary-phase screen geometry audit. No production imports."""
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


def stage_a_parents(z):
    data=json.loads(SOURCE.read_text())
    out=[]
    for p in data['parents']:
        vs=[tuple(map(F,v)) for v in p['vertices']]
        constraints=[]
        for _,coeff,bound in p['constraints']:
            a,b,c=map(F,coeff)
            constraints.append((a,b,F(bound)-c*z))
        out.append(dict(labels=p['labels'],vertices=[v[:2] for v in vs],
                        edges=[tuple(e) for e in sorted(p['edges']) if vs[e[0]][2]==vs[e[1]][2]==z],
                        constraints=constraints))
    return out,dict(source='pinned floor edges',parents=len(out),floor_edges=sum(len(p['edges']) for p in out))


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


def diagnose(parents,z,certificate):
    if certificate['status']!='UNCOVERED_PRIMITIVE_PAIRS' or not certificate['primary_uncovered']:
        return dict(status='NOT_TRIGGERED')
    P,Q=certificate['primary_uncovered'][0]
    ranges=[]
    for a,b in ROWS[-3:]:
        ranges.append(range(ceil((a+b)*z-(1-z)),floor(F(a,2)+b*(1-z)-z)+1))
    H_range=range(ceil(Q*z-P*(1-z)),floor(F(Q,2)-P*z)+1)
    bound=len(parents)*len(ranges[0])*len(ranges[1])*len(ranges[2])*len(H_range)
    out=dict(pair=[P,Q],maximum_sections=bound,section_budget=100000,
             orbit_range=[H_range.start,H_range.stop-1])
    if bound>100000: return dict(out,status='DIAGNOSTIC_SCOPE_LIMIT',examined=0)
    sections=[]
    for pi,parent in enumerate(parents):
        for seventh,eighth,ninth,H in itertools.product(*ranges,H_range):
            labels=tuple(parent['labels'])+(seventh,eighth,ninth)
            constraints=parent['constraints']+band_constraints(labels,z,ROWS)
            interval=(z,F(1,2))
            for a,b,c in constraints:
                interval=restrict(interval,a+b*F(Q,P),-b*F(H,P),c)
            lo,hi=interval
            section=dict(parent=pi,seventh_lap=seventh,eighth_lap=eighth,ninth_lap=ninth,
                         added_laps=[seventh,eighth,ninth],H=H,
                         x_interval=interval,nonempty=lo<=hi)
            sections.append(section)
            if lo<=hi:
                x=(lo+hi)/2
                y=F(Q,P)*x-F(H,P)
                need(all(a*x+b*y<=c for a,b,c in constraints),'diagnosed point')
                return dict(out,status='RESTORED_PARENT_WITNESS',sections=sections,examined=len(sections),
                            parent=pi,labels=labels,point=[x,y],h=H)
    return dict(out,status='NO_WITNESS_IN_RESTORED_INPUT',sections=sections,examined=len(sections))


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


def compare_classes(restricted,full,screen):
    full_by_id={r['id']:r for r in full['candidates']}
    subset_fields=0
    for r in restricted['candidates']:
        need(r['id'] in full_by_id,'screen is not a full subset')
        subset_fields+=compare(encode(r),encode(full_by_id[r['id']]))
    union=sorted(set(restricted.get('residual_pairs',[]))|set(full.get('residual_pairs',[])))
    need(len(union)<=800,'union bound')
    exhaustive=all('contact_matrix' in c for c in (restricted,full))
    records=[];lost=[]
    for pair in union:
        row=dict(pair=pair,primary=primary(*pair))
        for name,c in (('restricted',restricted),('full',full)):
            hits=[dict(id=r['id'],contact=contact(r,*pair)) for r in c['candidates'] if contact(r,*pair)['hit']]
            row[name]=dict(hit=bool(hits),contact_ids=[r['id'] for r in hits],first_contact=hits[0] if hits else None)
        if row['primary'] and not row['restricted']['hit'] and row['full']['hit']: lost.append(row)
        records.append(row)
    witness=None
    if lost:
        selected=lost[0]
        first=selected['full']['first_contact']
        source_id=first['id'].rsplit(':M',1)[0]
        decision=next(d for d in screen['decisions'] if d['source_id']==source_id)
        need(decision['status']=='NO_SCREEN_CERTIFICATE','lost witness source not omitted')
        witness=dict(pair=selected['pair'],full_contact=first,source_id=source_id,screen_decision=decision)
    return dict(scope='GLOBAL_POSITIVE_PRIMITIVE_COMPARISON' if exhaustive else 'BOUNDED_COMPARISON',
                subset_scalar_fields_checked=subset_fields,union_pairs=union,records=records,
                lost_primary_pairs=[r['pair'] for r in lost],first_lost_witness=witness)


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


def compare_production(out):
    results={}
    def check(name,expected,actual=None):
        path=HERE/(name+'.json')
        if actual is None: actual=json.loads(path.read_text())
        results[name]=dict(scalar_fields_compared=compare(encode(expected),actual,name),sha256=digest(path))
    output_screen=screen_for_output(out['screen'])
    check('screen',output_screen)
    for name in ('restricted','full'):
        actual=json.loads((HERE/(name+'.json')).read_text())
        expected=dict(certificate=certificate_for_output(out[name],ROWS[-1]),
                      primary_status='PRIMARY_COMPLETE' if out[name]['primary_status']=='PRIMARY_COMPLETE' else 'NO_PRIMARY_GUARANTEE')
        check(name,expected,{k:v for k,v in actual.items() if k!='controls'})
    check('full_clipping',out['full_clipping'])
    check('diagnostic',out['diagnostic'])
    own=out['comparison'];rows=[]
    for r in own['records']:
        row=dict(pair=r['pair'],primary=r['primary'])
        for branch in ('restricted','full'):
            first=r[branch]['first_contact']
            row[branch]=dict(r[branch])
            if first: row[branch]['first_contact']=dict(candidate_id=first['id'],contact=first['contact'])
        rows.append(row)
    lost_aux=[r['pair'] for r in rows if not r['primary'] and not r['restricted']['hit'] and r['full']['hit']]
    both_miss=[r['pair'] for r in rows if not r['restricted']['hit'] and not r['full']['hit']]
    lost=own['first_lost_witness']
    geometry_witness=None
    actual=json.loads((HERE/'comparison.json').read_text())
    if lost:
        decision=next(d for d in output_screen['decisions'] if d['source_id']==lost['source_id'])
        first=lost['full_contact']
        rec=next(r for r in out['full']['candidates'] if r['id']==first['id'])
        geometry_witness=dict(status='OMITTED_SOURCE_WITNESS',pair=lost['pair'],source_id=lost['source_id'],
                              failed_screen_decision=decision,
                              witness=dict(segment=first['id'],contact=first['contact'],point=first['contact']['point'],
                                           h=first['contact']['first_integer'],torus_laps=rec['labels']))
        actual['lost_primary_witness']['witness']={k:v for k,v in actual['lost_primary_witness']['witness'].items()
                                                  if k in geometry_witness['witness']}
    expected=dict(all_subset_checks_pass=True,subset_checks=[dict(id=r['id'],identical_full_candidate=True) for r in out['restricted']['candidates']],
                  complete_reduction_prerequisites=own['scope']=='GLOBAL_POSITIVE_PRIMITIVE_COMPARISON',
                  scope='ALL_POSITIVE_PRIMITIVE_DIRECTIONS' if own['scope']=='GLOBAL_POSITIVE_PRIMITIVE_COMPARISON' else 'BOUNDED_COMPARISON',
                  scope_note='Outside the union, both leaders have width at least one only when both full finite reductions were reached.',
                  union_pairs=own['union_pairs'],rows=rows,lost_primary_pairs=own['lost_primary_pairs'],lost_auxiliary_pairs=lost_aux,
                  both_miss_pairs=both_miss,lost_primary_witness=geometry_witness)
    check('comparison',expected,actual)
    return dict(status='PASS',files=results,total_scalar_fields=sum(r['scalar_fields_compared'] for r in results.values()),
                scope='all screen fields, both full coverage certificates/statuses, clipping trace, subset and union contacts, geometric lost witness, diagnostic status; physical recovery reviewed separately')


def main():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    need(digest(HERE/'PROTOCOL.md')==pins['protocol_sha256'],'protocol changed')
    for path,pin in pins['files'].items(): need(digest(ROOT/path)==pin['sha256'],'input changed '+path)
    raw=json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())['certificate']['candidates']
    sources=decode_source(raw)
    regression_candidates,regression_counts=append_full(sources,(38,18))
    regression=coverage(regression_candidates,F(1,8))
    archive=json.loads((ROOT/'reviews/2026-09-29-cc-ten-runner/stage8.json').read_text())['certificate']
    regression_fields=compare(encode(certificate_for_output(regression,(38,18))),archive)
    screen=screen_sources(sources)
    restricted=coverage(screen['candidates'],F(1,8))
    full_records,full_counts=append_full(sources,ROWS[-1])
    full=coverage(full_records,F(1,8)) if full_counts['status']=='PASS' else dict(status=full_counts['status'],primary_status='INCOMPLETE',candidates=[])
    classes=compare_classes(restricted,full,screen)
    parents,_=stage_a_parents(F(1,8))
    diagnostic=diagnose(parents,F(1,8),full)
    out=dict(status='AWAITING_PRODUCTION_COMPARISON',protocol_sha256=pins['protocol_sha256'],
             script_sha256=digest(Path(__file__)),
             method='independent two-coordinate coefficient identities, whole-record screen, all-band sequential clipping, direct integer contacts',
             regression=dict(status='PASS',scalar_fields_compared=regression_fields,counts=regression_counts),
             screen=screen,restricted=restricted,full=full,full_clipping=full_counts,
             comparison=classes,diagnostic=diagnostic)
    if all((HERE/(name+'.json')).exists() for name in ('screen','restricted','full','full_clipping','comparison','diagnostic')):
        out['production_comparison']=compare_production(out)
        out['status']='PASS'
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__=='__main__': main()
