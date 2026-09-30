#!/usr/bin/env python3
"""Frozen screen + direction-specific contact-first recovery. Exact arithmetic."""
import argparse
import hashlib
import importlib.util
import json
import platform
import statistics
import sys
import time
from fractions import Fraction as F
from math import ceil, floor, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
Z = F(1, 8)
TARGET = (54, 26)
BASE = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8))
ROWS = BASE + (TARGET,)
DOMAIN = 'positive integer p,q; ten distinct speeds iff p!=q and p!=2q; full labelled compilation includes auxiliaries'


def encode(v):
    if isinstance(v, F): return str(v)
    if isinstance(v, dict): return {str(k): encode(x) for k,x in v.items()}
    if isinstance(v, (tuple,list)): return [encode(x) for x in v]
    return v


def save(name, value):
    (HERE/name).write_text(json.dumps(encode(value), indent=2, sort_keys=True)+'\n')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def setup():
    pins = json.loads((HERE/'INPUTS.json').read_text())
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(HERE/'PROTOCOL.md') == pins['protocol_sha256']
    for p, pin in pins['files'].items(): assert sha(ROOT/p) == pin['sha256'], p
    phase = load_module('hybrid_phase', 'reviews/2026-09-29-cc-phase-screen/compare.py')
    api = load_module('hybrid_compiler', 'reviews/2026-09-29-cc-coverage-compiler/compiler.py')
    ten = load_module('hybrid_physical', 'reviews/2026-09-29-cc-ten-runner/transfer.py')
    api.key = phase.key
    ten.ROWS = ROWS; ten.ADDED = ROWS[6:]
    data = json.loads((ROOT/'reviews/2026-09-29-cc-nine-runner/stage8.json').read_text())
    assert tuple(map(tuple, data['certificate']['rows'])) == BASE
    sources = data['certificate']['candidates']; assert len(sources) == 36
    return pins, phase, api, ten, sources


def dot(row, p): return sum(a*x for a,x in zip(row,p))
def source_key(s): return s['parent'], *s['edge'], s['seventh_lap'], s['eighth_lap']
def ends(s): return [tuple(map(F,p)) for p in s['endpoints']]
def at(a,b,t): return tuple(x+t*(y-x) for x,y in zip(a,b))


def bounds(source, pair, target=TARGET):
    a,b = ends(source); P,Q = pair
    ha,hb = Q*a[0]-P*a[1], Q*b[0]-P*b[1]
    ra,rb = dot(target,a),dot(target,b)
    h0,h1 = ceil(min(ha,hb)),floor(max(ha,hb))
    m0,m1 = ceil(min(ra,rb)-(1-Z)),floor(max(ra,rb)-Z)
    return dict(source_id=source['id'], pair=pair, projection=(ha,hb),
                raw_range=tuple(sorted((ra,rb))), h_range=(h0,h1),
                lap_range=(m0,m1), h_count=max(0,h1-h0+1),
                work_bound=max(0,h1-h0+1)*max(1,m1-m0+1))


def preflight(sources, pairs, budget=4096):
    rows = [bounds(s,p) for p in pairs for s in sorted(sources,key=source_key)]
    total = sum(r['work_bound'] for r in rows)
    return dict(status='PASS' if total<=budget else 'RECOVERY_SCOPE_LIMIT',
                budget=budget, work_bound=total, rows=rows,
                source_pair_projections=len(rows), new_row_raw_ranges=len(rows),
                integer_h_bound=sum(r['h_count'] for r in rows))


def query(source, pair, target=TARGET, opened=False, prepared=None):
    """Exhaust one supplied segment's integer contacts; never call full clipping."""
    a,b = ends(source); meta = prepared or bounds(source,pair,target)
    ha,hb = meta['projection']; trace=[]
    counts = dict(h_tests=0, point_phase_tests=0, parallel_band_tests=0)
    if opened and a==b:
        return dict(status='NO_SOURCE_CONTACT', trace=trace, counts=counts, witness=None)
    for h in range(meta['h_range'][0],meta['h_range'][1]+1):
        counts['h_tests'] += 1
        if ha != hb:
            t = (h-ha)/(hb-ha); point = at(a,b,t)
            raw = dot(target,point); m = floor(raw); phase = raw-m
            safe = Z<=phase<=1-Z and (not opened or 0<t<1)
            counts['point_phase_tests'] += 1
            trace.append(dict(h=h, branch='POINT', parameter=t, raw=raw, lap=m,
                              phase=phase, accepted=safe))
            if safe:
                return dict(status='HIT', trace=trace, counts=counts,
                            witness=dict(h=h,parameter=t,point=point,ninth_lap=m))
        else:
            ra,rb = dot(target,a),dot(target,b); dr=rb-ra
            for m in range(meta['lap_range'][0],meta['lap_range'][1]+1):
                counts['parallel_band_tests'] += 1
                lo,hi = F(0),F(1)
                if dr:
                    c,d=sorted(((m+Z-ra)/dr,(m+1-Z-ra)/dr))
                    lo,hi=max(lo,c),min(hi,d)
                elif not m+Z<=ra<=m+1-Z: lo,hi=F(1),F(0)
                safe = lo<=hi and (not opened or (hi>0 and lo<1))
                trace.append(dict(h=h,branch='PARALLEL',lap=m,interval=(lo,hi),accepted=safe))
                if safe:
                    t=(lo+hi)/2 if opened and lo==0 else lo
                    assert not opened or 0<t<1
                    return dict(status='HIT',trace=trace,counts=counts,
                                witness=dict(h=h,parameter=t,point=at(a,b,t),ninth_lap=m))
    return dict(status='NO_SOURCE_CONTACT', trace=trace, counts=counts, witness=None)


def recovery(sources, pairs, budget=4096, opened=False):
    check = preflight(sources,pairs,budget)
    result=dict(status=check['status'],preflight=check,queries=[],exceptions=[],uncovered=[],
                counts=dict(source_visits=0,h_tests=0,point_phase_tests=0,parallel_band_tests=0))
    if check['status'] != 'PASS': return result
    metadata={(tuple(r['pair']),r['source_id']):r for r in check['rows']}
    for pair in pairs:
        chosen=None
        for source in sorted(sources,key=source_key):
            r=query(source,pair,opened=opened,prepared=metadata[(tuple(pair),source['id'])])
            result['queries'].append(dict(pair=pair,source_id=source['id'],**r))
            result['counts']['source_visits']+=1
            for k,v in r['counts'].items(): result['counts'][k]+=v
            if r['status']=='HIT':
                w=r['witness']; local=w['parameter']; s0,s1=map(F,source['source_parameters'])
                chosen=dict(pair=pair,source_id=source['id'],parent=source['parent'],edge=source['edge'],
                    local_parameter=local,original_parameter=s0+local*(s1-s0),
                    point=w['point'],h=w['h'],labels=tuple(source['labels'])+(w['ninth_lap'],),
                    ninth_lap=w['ninth_lap'],source_endpoint=w['point'] in ends(source))
                result['exceptions'].append(chosen); break
        if chosen is None: result['uncovered'].append(pair)
    result['status']='COMPLETE_EXCEPTION_RECOVERY' if not result['uncovered'] else 'NO_SOURCE_CONTACT'
    return result


def validate_sources(api,sources):
    for s in sources: api.checked_record(s,BASE,Z)


def build_hybrid(phase,api,sources):
    validate_sources(api,sources)
    screened=phase.screen(sources,TARGET)
    cert=api.compile_records(screened['candidates'],rows=ROWS,threshold=Z,budget=400)
    cert['domain']=DOMAIN
    result=dict(screen_counts=screened['counts'],screen_certificate=cert,
                source_validation_endpoint_band_checks=36*2*8)
    if cert['status'] not in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS'):
        return dict(result,status=cert['status'],recovery=None)
    rec=recovery(sources,cert['uncovered'])
    complete=rec['status']=='COMPLETE_EXCEPTION_RECOVERY'
    return dict(result,status='COMPLETE_HYBRID_CERTIFICATE' if complete else rec['status'],recovery=rec)


def build_full(phase,api,sources):
    validate_sources(api,sources)
    records,clipping=phase.full_clip(sources,TARGET)
    cert=api.compile_records(records,rows=ROWS,threshold=Z,budget=400)
    cert['domain']=DOMAIN
    return dict(certificate=cert,clipping=clipping,source_validation_endpoint_band_checks=36*2*8)


def select(api,ten,hybrid,p,q):
    if type(p) is not int or type(q) is not int or p<=0 or q<=0:
        raise ValueError('positive integer parameters required')
    d=gcd(p,q); pair=(p//d,q//d); cert=hybrid['screen_certificate']
    exception=next((r for r in hybrid['recovery']['exceptions'] if tuple(r['pair'])==pair),None)
    if exception:
        r=exception
        record={'id':'EXCEPTION:'+r['source_id']+f':M{r["ninth_lap"]}', 'labels':r['labels']}
        hit=dict(hit=True,point=tuple(map(F,r['point'])),first_integer=r['h'],
                 parameter=F(r['local_parameter']))
        witness=ten.recover(api,record,hit,p,q,Z)
        return dict(route='EXCEPTION_POINT',witness=witness,source_id=r['source_id'])
    byid={s['id']:s for s in cert['candidates']}
    for identity in cert['chosen_ids']:
        s=byid[identity]; hit=api.contact(s,*pair)
        if hit['hit']: return dict(route='SCREEN_MENU',witness=ten.recover(api,s,hit,p,q,Z))
    raise ArithmeticError('No certified contact for this primitive direction')


def fixtures():
    cases=[
      ('nonconstant_unsafe_then_safe',((0,0),(3,1)),(1,0),'HIT',F(1,2)),
      ('constant_integer_band',((0,0),(1,1)),(1,0),'HIT',Z),
      ('constant_noninteger',((0,F(1,2)),(1,F(3,2))),(1,0),'NO_SOURCE_CONTACT',None),
      ('singleton',((F(1,4),F(1,4)),(F(1,4),F(1,4))),(1,0),'HIT',F(0))]
    out=[]
    for name,endpoints,target,status,t in cases:
        r=query({'id':name,'endpoints':endpoints},(1,1),target)
        assert r['status']==status
        if t is not None: assert r['witness']['parameter']==t
        out.append(dict(name=name,endpoints=endpoints,target=target,result=r))
    return dict(status='PASS',cases=out,scope='Kernel fixtures only; not physical runner targets')


def audits(api,ten,hybrid,full,sources):
    # Archived full/restricted outputs first become available here, after construction.
    restricted=json.loads((ROOT/'reviews/2026-09-29-cc-phase-screen/restricted.json').read_text())['certificate']
    archived=json.loads((ROOT/'reviews/2026-09-29-cc-phase-screen/full.json').read_text())['certificate']
    assert encode(hybrid['screen_certificate'])==restricted
    assert encode(full['certificate'])==archived
    bysource={s['id']:s for s in sources}; membership=[]
    for r in hybrid['recovery']['exceptions']:
        match=next(s for s in full['certificate']['candidates']
                   if s['id']==r['source_id']+f':M{r["ninth_lap"]}')
        assert tuple(match['labels'])==tuple(r['labels'])
        lo,hi=map(F,match['source_parameters']); orig=F(r['original_parameter'])
        assert lo<=orig<=hi
        source=bysource[r['source_id']]; a,b=ends(source)
        assert at(a,b,F(r['local_parameter']))==tuple(map(F,r['point']))
        membership.append(dict(pair=r['pair'],candidate_id=match['id'],original_parameter=orig,
                               full_parameter_interval=(lo,hi),labels_equal=True))
    residual=[dict(pair=pair,**select(api,ten,hybrid,*pair))
              for pair in hybrid['screen_certificate']['residual_pairs']]
    physical=[dict(pair=pair,**select(api,ten,hybrid,*pair))
              for pair in ten.PAIRS+((5,1),(10,2))]
    opened=recovery(sources,hybrid['screen_certificate']['uncovered'],opened=True)
    zero=preflight(sources,hybrid['screen_certificate']['uncovered'],budget=0)
    assert zero['status']=='RECOVERY_SCOPE_LIMIT'
    return dict(status='PASS',archived_restricted_certificate_equal=True,archived_full_certificate_equal=True,
                exception_membership=membership,residual_dispatch=residual,physical_controls=physical,
                open_source_diagnostic=opened,zero_budget=dict(status=zero['status'],work_bound=zero['work_bound']),
                kernel=fixtures())


def benchmark(phase,api,sources):
    fns={'hybrid':lambda:build_hybrid(phase,api,sources),'full':lambda:build_full(phase,api,sources)}
    for fn in fns.values(): fn()
    start=time.perf_counter_ns(); rounds=[]
    for i in range(11):
        if (time.perf_counter_ns()-start)>30_000_000_000: break
        order=('hybrid','full') if i%2==0 else ('full','hybrid'); values={}
        for name in order:
            t=time.perf_counter_ns(); result=fns[name](); values[name]=time.perf_counter_ns()-t
            status=result['status'] if name=='hybrid' else result['certificate']['status']
            assert status in ('COMPLETE_HYBRID_CERTIFICATE','COMPLETE_COVER_CERTIFICATE')
        rounds.append(dict(round=i,order=order,nanoseconds=values,
                           full_over_hybrid=values['full']/values['hybrid']))
    med={k:statistics.median(r['nanoseconds'][k] for r in rounds) for k in fns} if rounds else {}
    return dict(status='COMPLETE' if len(rounds)==11 else 'TIMING_SCOPE_LIMIT',rounds=rounds,
                medians_ns=med,median_paired_full_over_hybrid=statistics.median(r['full_over_hybrid'] for r in rounds) if rounds else None,
                python=sys.version,platform=platform.platform(),clock='perf_counter_ns',gc='default',
                warmups_per_method=1,budget_seconds=30,
                scope='Compute from supplied parsed sources including validation/traces; excludes earlier discovery, imports, parsing, audits, physical controls and writes. Environment-specific, not complexity evidence.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--benchmark',action='store_true');args=parser.parse_args()
    pins,phase,api,ten,sources=setup()
    hybrid=build_hybrid(phase,api,sources);save('hybrid.json',hybrid)
    full=build_full(phase,api,sources)
    audit=audits(api,ten,hybrid,full,sources);save('audit.json',audit)
    summary=dict(protocol_sha256=pins['protocol_sha256'],status=hybrid['status'],target=TARGET,threshold=Z,
        screen_counts=hybrid['screen_counts'],screen_compiler_counts=hybrid['screen_certificate']['counts'],
        leader=hybrid['screen_certificate']['leader'],exception_pairs=hybrid['screen_certificate']['uncovered'],
        recovered=hybrid['recovery']['exceptions'],recovery_counts=hybrid['recovery']['counts'],
        preflight={k:v for k,v in hybrid['recovery']['preflight'].items() if k!='rows'},
        full_compiler_counts=full['certificate']['counts'],full_clipping_counts={k:v for k,v in full['clipping'].items() if k!='trace'},
        physical_controls=len(audit['physical_controls']),residual_dispatch_checks=len(audit['residual_dispatch']),
        open_source_status=audit['open_source_diagnostic']['status'],open_source_uncovered=audit['open_source_diagnostic']['uncovered'],
        primary_controls=sum(r['witness']['distinct_speeds'] for r in audit['physical_controls']),
        source_validation_endpoint_band_checks_per_method=hybrid['source_validation_endpoint_band_checks'],
        evidence='Exact development repair; general completeness/coverage remains internally reviewed proof candidate')
    save('summary.json',summary)
    if args.benchmark: save('timing.json',benchmark(phase,api,sources))
    print(json.dumps(encode(summary),sort_keys=True))


if __name__=='__main__': main()
