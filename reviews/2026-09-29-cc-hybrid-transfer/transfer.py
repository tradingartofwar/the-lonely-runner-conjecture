#!/usr/bin/env python3
"""Frozen (102,50) stress transfer through explicit data-only module bindings."""
import argparse
import hashlib
import importlib.util
import inspect
import json
from fractions import Fraction as F
from math import floor, gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=(54,26)
TARGET=(102,50)
Z=F(1,8)
PREFIX='reviews/2026-09-29-cc-hybrid-recovery/'


def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [encode(x) for x in v]
    return v


def save(name,value): (HERE/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(path): return json.loads((ROOT/path).read_text())


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


def setup():
    pin=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==pin['protocol_sha256']
    for path,identity in pin['files'].items(): assert digest(ROOT/path)==identity['sha256'],path
    h=module('transfer_hybrid',PREFIX+'hybrid.py')
    phase=module('transfer_phase','reviews/2026-09-29-cc-phase-screen/compare.py')
    api=module('transfer_compiler','reviews/2026-09-29-cc-coverage-compiler/compiler.py')
    physical=module('transfer_physical','reviews/2026-09-29-cc-ten-runner/transfer.py')
    api.key=phase.key
    sources=read('reviews/2026-09-29-cc-nine-runner/stage8.json')['certificate']['candidates']
    assert len(sources)==36
    return pin,h,phase,api,physical,sources


def bindings(h,physical):
    return {'hybrid.TARGET':h.TARGET,'hybrid.ROWS':h.ROWS,
            'bounds.__defaults__':h.bounds.__defaults__,'query.__defaults__':h.query.__defaults__,
            'physical.ROWS':physical.ROWS,'physical.ADDED':physical.ADDED}


def bind(h,phase,api,physical,target):
    functions={**{'hybrid.'+name:getattr(h,name) for name in
        ('bounds','preflight','query','recovery','validate_sources','build_hybrid','build_full','select','benchmark')},
        'phase.screen':phase.screen,'phase.full_clip':phase.full_clip,
        'compiler.compile_records':api.compile_records,'compiler.contact':api.contact,'physical.recover':physical.recover}
    bodies={name:fn.__code__ for name,fn in functions.items()}
    before_hashes={name:hashlib.sha256(inspect.getsource(fn).encode()).hexdigest() for name,fn in functions.items()}
    before=bindings(h,physical)
    h.TARGET=tuple(target);h.ROWS=h.BASE+(tuple(target),)
    h.bounds.__defaults__=(tuple(target),)
    h.query.__defaults__=(tuple(target),False,None)
    physical.ROWS=h.ROWS;physical.ADDED=h.ROWS[6:]
    assert h.bounds.__defaults__[0]==h.query.__defaults__[0]==h.TARGET==physical.ROWS[-1]
    assert physical.ADDED==h.ROWS[6:]
    assert all(fn.__code__ is bodies[name] for name,fn in functions.items())
    after_hashes={name:hashlib.sha256(inspect.getsource(fn).encode()).hexdigest() for name,fn in functions.items()}
    assert before_hashes==after_hashes
    return dict(target=target,before=before,after=bindings(h,physical),function_code_identity_unchanged=True,
                function_source_sha256_before=before_hashes,function_source_sha256_after=after_hashes,
                inherited_adapter='compiler.key = phase.key; unchanged numeric provenance ordering',
                unused_old_binding='phase.TARGET remains old; screen/full_clip receive target explicitly')


def fields(value):
    if isinstance(value,dict): return sum(fields(x) for x in value.values())
    if isinstance(value,list): return sum(fields(x) for x in value)
    return 1


def regression(h,phase,api,physical,sources):
    adapter=bind(h,phase,api,physical,OLD)
    hybrid=h.build_hybrid(phase,api,sources);archived=read(PREFIX+'hybrid.json')
    assert encode(hybrid)==archived
    full=h.build_full(phase,api,sources)['certificate']
    archived_full=read('reviews/2026-09-29-cc-phase-screen/full.json')['certificate']
    assert encode(full)==archived_full
    old_audit=read(PREFIX+'audit.json')
    records=[dict(pair=r['pair'],**h.select(api,physical,hybrid,*r['pair'])) for r in old_audit['physical_controls']]
    assert encode(records)==old_audit['physical_controls']
    kernel=h.fixtures();assert encode(kernel)==old_audit['kernel']
    return dict(status='PASS',adapter=adapter,hybrid_scalar_fields=fields(archived),
                full_certificate_scalar_fields=fields(archived_full),physical_controls=len(records),
                physical_scalar_fields=fields(old_audit['physical_controls']),kernel_fixtures=len(kernel['cases']),
                scope='Exact old-row adapter regression; no old benchmark or added targets')


def hybrid_select(h,api,physical,hybrid,p,q):
    if hybrid.get('recovery') is None:
        return dict(status='NO_OUTPUT_CERTIFICATE',reason=hybrid['status'])
    try: return dict(status='HIT',**h.select(api,physical,hybrid,p,q))
    except ArithmeticError:
        return dict(status='NO_CERTIFIED_CONTACT',reason=hybrid['status'])


def full_select(h,api,physical,full,p,q):
    cert=full['certificate'];records=cert.get('candidates',[])
    if cert['status']=='COMPLETE_COVER_CERTIFICATE':
        byid={s['id']:s for s in records};records=[byid[i] for i in cert['chosen_ids']]
    d=gcd(p,q);P,Q=p//d,q//d
    for record in records:
        hit=api.contact(record,P,Q)
        if hit['hit']: return dict(status='HIT',witness=physical.recover(api,record,hit,p,q,Z))
    return dict(status='NO_CERTIFIED_CONTACT',reason=full['clipping']['status'] if full['clipping']['status']!='PASS' else cert['status'])


def audit(h,phase,api,physical,hybrid,full,sources):
    screen=hybrid['screen_certificate'];fc=full['certificate']
    reduced=lambda c:c['status'] in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS') and 'residual_pairs' in c
    global_scope=reduced(screen) and reduced(fc) and full['clipping']['status']=='PASS' and hybrid.get('recovery') is not None and hybrid['recovery']['status']!='RECOVERY_SCOPE_LIMIT'
    union=sorted({tuple(p) for c in (screen,fc) for p in c.get('residual_pairs',[])})
    assert len(union)<=800
    comparison=[]
    for pair in union:
        hits=[s['id'] for s in fc.get('candidates',[]) if api.contact(s,*pair)['hit']]
        selected=hybrid_select(h,api,physical,hybrid,*pair)
        comparison.append(dict(pair=pair,primary=physical.primary(*pair),hybrid=selected,
                               full_class_hit=bool(hits),full_contact_ids=hits,
                               coverage_equal=(selected['status']=='HIT')==bool(hits)))
    subset=[];full_byid={s['id']:s for s in fc.get('candidates',[])}
    for source in screen.get('candidates',[]):
        same=encode(source)==encode(full_byid.get(source['id']))
        subset.append(dict(id=source['id'],identical_full_member=same))
        if full['clipping']['status']=='PASS': assert same
    membership=[]
    for r in (hybrid.get('recovery') or {}).get('exceptions',[]):
        candidate_id=r['source_id']+f':M{r["ninth_lap"]}'
        s=full_byid.get(candidate_id)
        if s is None:
            membership.append(dict(pair=r['pair'],status='NO_FULL_COMPARISON_RECORD'));continue
        a,b=map(F,s['source_parameters']);t=F(r['original_parameter'])
        assert a<=t<=b and tuple(r['labels'])==tuple(s['labels'])
        membership.append(dict(pair=r['pair'],candidate_id=candidate_id,original_parameter=t,
                               full_parameter_interval=(a,b),labels_equal=True))
    controls=[dict(pair=pair,primary=physical.primary(*pair),hybrid=hybrid_select(h,api,physical,hybrid,*pair),
                   full=full_select(h,api,physical,full,*pair)) for pair in physical.PAIRS+((5,1),(10,2))]
    exceptions=screen.get('uncovered',[])
    opened=h.recovery(sources,exceptions,opened=True) if reduced(screen) else dict(status='NOT_TRIGGERED')
    zero=h.preflight(sources,exceptions,budget=0) if reduced(screen) else dict(status='NOT_TRIGGERED')
    old_time=F(9,40);speed=TARGET[0]*5+TARGET[1];raw=speed*old_time
    old_failure=dict(pair=(5,1),old_time=old_time,new_speed=speed,raw=raw,phase=raw-floor(raw),safe=Z<=raw-floor(raw)<=1-Z)
    assert not old_failure['safe'] and raw==126
    return dict(status='PASS',comparison_scope='ALL_POSITIVE_PRIMITIVE_DIRECTIONS' if global_scope else 'REACHED_FINITE_UNION_ONLY',
                union_pairs=union,comparison=comparison,coverage_mismatches=[r['pair'] for r in comparison if not r['coverage_equal']],
                screen_subset=subset,exception_membership=membership,controls=controls,
                open_source_diagnostic=opened,zero_budget={k:v for k,v in zero.items() if k!='rows'},old_time_failure=old_failure)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--benchmark',action='store_true');args=parser.parse_args()
    pin,h,phase,api,physical,sources=setup()
    reg=regression(h,phase,api,physical,sources);save('adapter_regression.json',reg)
    adapter=bind(h,phase,api,physical,TARGET);save('adapter.json',adapter)
    hybrid=h.build_hybrid(phase,api,sources);save('hybrid.json',hybrid)
    full=h.build_full(phase,api,sources);save('full.json',full)
    checks=audit(h,phase,api,physical,hybrid,full,sources);save('audit.json',checks)
    rec=hybrid.get('recovery') or {};screen=hybrid['screen_certificate']
    summary=dict(protocol_sha256=pin['protocol_sha256'],target=TARGET,threshold=Z,
        hybrid_status=hybrid['status'],full_status=full['certificate']['status'],full_clipping_status=full['clipping']['status'],
        screen_counts=hybrid['screen_counts'],screen_compiler_counts=screen.get('counts'),screen_leader=screen.get('leader'),
        exception_pairs=screen.get('uncovered'),recovered=rec.get('exceptions'),recovery_counts=rec.get('counts'),
        preflight={k:v for k,v in rec.get('preflight',{}).items() if k!='rows'},
        full_compiler_counts=full['certificate'].get('counts'),full_leader=full['certificate'].get('leader'),
        full_clipping_counts={k:v for k,v in full['clipping'].items() if k!='trace'},
        comparison_scope=checks['comparison_scope'],union_pairs=len(checks['union_pairs']),coverage_mismatches=checks['coverage_mismatches'],
        hybrid_control_hits=sum(r['hybrid']['status']=='HIT' for r in checks['controls']),
        full_control_hits=sum(r['full']['status']=='HIT' for r in checks['controls']),physical_controls=len(checks['controls']),
        open_source_status=checks['open_source_diagnostic']['status'],old_time_failure=checks['old_time_failure'],
        source_validation_endpoint_band_checks_per_method=hybrid['source_validation_endpoint_band_checks'],
        evidence='Informed within-progression stress transfer; general arguments remain internally reviewed proof candidates')
    save('summary.json',summary)
    if args.benchmark:
        if hybrid['status']=='COMPLETE_HYBRID_CERTIFICATE' and full['certificate']['status']=='COMPLETE_COVER_CERTIFICATE' and full['clipping']['status']=='PASS':
            timing=h.benchmark(phase,api,sources)
        else: timing=dict(status='NOT_TRIGGERED',reason='Both complete new certificates required',hybrid_status=hybrid['status'],full_status=full['certificate']['status'],clipping_status=full['clipping']['status'])
        save('timing.json',timing)
    print(json.dumps(encode(summary),sort_keys=True))


if __name__=='__main__': main()
