"""Five source-bound regression examples. Standard-library exact arithmetic only.

The direct-time reference imports no archived lattice or recovery code.
Intentionally broken rules are diagnostic mutations, never solver competitors.
"""
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASELINE = '29e54d32e2ff5349bdb0c3db56fab753a0e44c94'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def phases(rates, t):
    return [(v*t) % 1 for v in rates]


def point_times(rates, point):
    """All times in [0,1): exhaust one exact phase's integer laps."""
    point = list(map(F, point))
    candidates = [(j+point[0])/rates[0] for j in range(rates[0])]
    return [t for t in candidates if phases(rates, t) == point], candidates


def segment_parameter(point, segment):
    A, B = [list(map(F, x)) for x in segment]
    for axis in range(2):
        if B[axis] != A[axis]:
            s = (point[axis]-A[axis])/(B[axis]-A[axis])
            return s if 0 <= s <= 1 and point == [a+s*(b-a) for a,b in zip(A,B)] else None
    return F(0) if point == A else None


def segment_times(case):
    rates = case['rates']; z = F(case['z'])
    candidates = [(j+z)/rates[2] for j in range(rates[2])]
    return [t for t in candidates if segment_parameter(phases(rates,t)[:2],case['segment']) is not None], candidates


def relation_contacts(case):
    """Solve each affine integrality condition in the SAME segment parameter."""
    A, B = [list(map(F, x))+[F(case['z'])] for x in case['segment']]
    sets = []; traces = []
    for row in case['relations']:
        start = sum(a*x for a,x in zip(row,A)); end = sum(a*x for a,x in zip(row,B))
        if start == end:
            hits = None if start.denominator == 1 else set()
        else:
            hits = {(F(k)-start)/(end-start) for k in range(ceil(min(start,end)),floor(max(start,end))+1)}
        sets.append(hits)
        traces.append({'relation':row,'range':[start,end],'parameters':'ALL' if hits is None else sorted(hits)})
    finite = [s for s in sets if s is not None]
    common = set.intersection(*finite) if finite else None
    return all(s is None or bool(s) for s in sets), common, traces


def merge(pieces):
    result=[]
    for l,u in sorted(pieces):
        if result and l <= result[-1][1]:
            result[-1][1]=max(result[-1][1],u)
        else:
            result.append([l,u])
    return result


def safe_set(rates, delta):
    """Exhaust all rational band-boundary events, including singleton points."""
    require(sum(rates) <= 1000, 'Example budget exceeded')
    events = sorted({F(0),F(1)} | {(j+a)/v for v in rates for j in range(v) for a in (delta,1-delta)})
    def safe(t):
        return all(delta <= x <= 1-delta for x in phases(rates,t))
    pieces = [[t,t] for t in events if safe(t)]
    pieces += [[l,u] for l,u in zip(events,events[1:]) if safe((l+u)/2)]
    return merge(pieces), len(events)*2-1


def intersect_band(interval, rate, delta):
    l,u=map(F,interval)
    return merge([[max(l,(k+delta)/rate),min(u,(k+1-delta)/rate)]
                  for k in range(rate) if max(l,(k+delta)/rate) <= min(u,(k+1-delta)/rate)])


def run_case(case):
    detail={}; mutation=case['mutant']; rates=case['rates']
    require(all(type(v) is int and 0 < v <= 100 for v in rates), 'Rates outside fixture contract')
    if case['query_kind']=='fixed_z_segment':
        times,candidates=segment_times(case)
        marginal,common,traces=relation_contacts(case)
        actual=bool(times); wrong=marginal
        require(common is not None and bool(common)==actual,'Joint relation/reference mismatch')
        detail={'physical_candidates':candidates,'relation_parameter_sets':traces,'joint_parameters':sorted(common)}
    elif case['query_kind']=='phase_point':
        times,candidates=point_times(rates,case['point']); actual=bool(times)
        detail={'physical_candidates':[{'time':t,'phases':phases(rates,t)} for t in candidates]}
        if mutation=='incomplete_relations':
            point=list(map(F,case['point']))
            values=lambda rows:[sum(a*x for a,x in zip(row,point)) for row in rows]
            raw=values(case['raw_relations']); complete=values(case['complete_relations'])
            wrong=all(x.denominator==1 for x in raw)
            require(all(x.denominator==1 for x in complete)==actual,'Complete relation/reference mismatch')
            detail.update(raw_relation_values=raw,complete_relation_values=complete)
        else:
            t=F(case['canonical_time']);wrong=phases(rates,t)==list(map(F,case['point']))
            detail['discarded_alternative']={'canonical_time':t,'canonical_phases':phases(rates,t)}
    else:
        delta=F(case['delta']); intervals,checks=safe_set(rates,delta)
        require(intervals==[[F(x) for x in pair] for pair in case['expected_intervals']], 'Archived full-set disagreement')
        actual=bool(intervals);times=[intervals[0][0]] if actual else []
        if mutation=='drop_singletons':
            retained=[pair for pair in intervals if pair[0]<pair[1]]
        else:
            l,u=map(F,case['primary_interval'])
            # Verify the stored primary component is actually core-safe before r is added.
            core,_=safe_set(rates[:-1],delta)
            require([l,u] in core,'Primary is not a complete core component')
            retained=intersect_band([l,u],rates[-1],delta)
        wrong=bool(retained)
        detail={'complete_intervals':intervals,'mutant_retained_intervals':retained,'exact_event_predicates':checks,'total_safe_duration':sum(u-l for l,u in intervals)}
    if 'expected_times' in case:
        require(times==list(map(F,case['expected_times'])),'Archived physical-time disagreement')
    require(actual != wrong,'Intended failure no longer reached')
    return {'id':case['id'],'title':case['title'],'question':case['question'],'lesson':case['lesson'],
            'reference_status':'SAT' if actual else 'UNSAT','mutant_status':'SAT' if wrong else 'UNSAT',
            'diagnostic':'FALSE_POSITIVE' if wrong else 'FALSE_NEGATIVE','mutant':mutation,
            'witnesses':[{'time':t,'phases':phases(rates,t)} for t in times],
            'evidence':detail,'source':case['source']}


def encode(x):
    if isinstance(x,F):return str(x)
    raise TypeError(type(x).__name__)


def validate_source_links(data):
    """Resolve the five declared source selections, not only file digests.

    Two point queries intentionally specialize archived edge/band diagnostics.
    Their provenance must not be described as the full original source query.
    """
    old_path='reviews/2026-09-30-cc-three-parameter/discovery.json'
    new_path='reviews/2026-10-02-cc-orbit-intervals/run/RESULTS.json'
    check_path='reviews/2026-10-02-cc-orbit-intervals/run/VERIFICATION.json'
    old=json.loads((ROOT/old_path).read_text())['diagnostics']
    new=json.loads((ROOT/new_path).read_text())
    verification=json.loads((ROOT/check_path).read_text())
    expected={}
    f=old['false_marginal'];u=old['unsaturated_false_point'];l=old['lost_clock_lift']
    expected['same_point']={'query_kind':'fixed_z_segment','rates':f['pqr'],
        'segment':f['object']['endpoints'],'z':f['object']['z_range'][0],
        'relations':f['relations'],'expected_times':[],'mutant':'independent_marginals',
        'source':{'path':old_path,'selector':'diagnostics.false_marginal',
                  'adaptation':'The exact archived segment with its fixed z coordinate.'}}
    expected['complete_relations']={'query_kind':'phase_point','rates':u['pqr'],
        'point':u['raw_hit']['point'],'raw_relations':u['raw_relations'],
        'complete_relations':u['saturated_relations'],'expected_times':[],
        'mutant':'incomplete_relations','source':{'path':old_path,'selector':'diagnostics.unsaturated_false_point',
        'adaptation':'Point-membership specialization of the archived false hit on an edge; not the whole edge query.'}}
    expected['clock_lifts']={'query_kind':'phase_point','rates':l['pqr'],
        'point':l['recovered']['point'],'canonical_time':l['canonical_time'],
        'expected_times':[l['recovered']['time']],'mutant':'first_clock_only',
        'source':{'path':old_path,'selector':'diagnostics.lost_clock_lift',
        'adaptation':'Exact recovered-phase-point query, stronger than the archived safe-band recovery request.'}}
    for cid,triple,mutation in [('isolated_points',[1,4,13],'drop_singletons'),('widest_only',[1,6,13],'widest_only')]:
        row=next(c for c in new['cases'] if c['pqr']==triple)
        core=new['cores'][row['core_key']];p,q,r=triple
        union=next(c['full8_intervals'] for c in verification['compression_failure_unions'] if c['pqr']==triple)
        expected[cid]={'query_kind':'closed_phase_bands','rates':[p,q,p+q,2*p+q,3*p+q,3*p+2*q,6*p+2*q,3*p+8*q,r],
            'pqr':triple,'delta':'1/8','primary_interval':core['components'][core['primary']]['interval'],
            'expected_intervals':union,'mutant':mutation,'source':{'path':new_path,
            'selector':'cases[pqr='+','.join(map(str,triple))+']',
            'adaptation':'Archived complete closed 1/8 safe-time query for this fixed input.'}}
    require(len(data['cases'])==len(expected),'Unexpected case count')
    require({c['id'] for c in data['cases']}==set(expected),'Unexpected or duplicated case IDs')
    for case in data['cases']:
        contract=expected[case['id']]
        for key,value in contract.items():
            require(case.get(key)==value,'Source-binding mismatch: '+case['id']+'.'+key)


def run(out):
    fixture_raw=(HERE/'fixtures.json').read_bytes(); data=json.loads(fixture_raw)
    require(data.get('schema')=='compatibility-conformance/v1','Unsupported schema')
    require(data.get('source_commit')==BASELINE,'Wrong source commit')
    require(set(data.get('source_sha256',{}))=={
        'reviews/2026-09-30-cc-three-parameter/discovery.json',
        'reviews/2026-10-02-cc-orbit-intervals/run/RESULTS.json',
        'reviews/2026-10-02-cc-orbit-intervals/run/VERIFICATION.json'},'Missing or unexpected source pins')
    for path,digest in data['source_sha256'].items():
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'Source changed: '+path)
    validate_source_links(data)
    results=[run_case(c) for c in data['cases']]
    payload={'status':'PASS_DEVELOPMENT_REGRESSIONS','fixture_sha256':hashlib.sha256(fixture_raw).hexdigest(),
             'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'source_commit':data['source_commit'],'cases':results,
             'limits':data['scope'],'counts':{'cases':len(results),'injected_false_positives':sum(x['diagnostic']=='FALSE_POSITIVE' for x in results),'injected_false_negatives':sum(x['diagnostic']=='FALSE_NEGATIVE' for x in results)}}
    out.write_text(json.dumps(payload,default=encode,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':payload['status'],'counts':payload['counts']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=HERE/'results.json')
    run(parser.parse_args().out)
