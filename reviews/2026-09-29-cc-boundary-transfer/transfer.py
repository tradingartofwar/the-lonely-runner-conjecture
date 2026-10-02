#!/usr/bin/env python3
"""One frozen supporting-boundary transfer; inherited algorithms and explicit data."""
import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=(102,50)
TARGET=(78,50)
Z=F(1,8)
PREVIOUS='reviews/2026-09-29-cc-hybrid-transfer/'


def encode(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):encode(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [encode(x) for x in v]
    return v


def save(name,value): (HERE/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads((ROOT/path).read_text())


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


def setup():
    pin=json.loads((HERE/'INPUTS.json').read_text())
    assert digest(HERE/'PROTOCOL.md')==pin['protocol_sha256']
    for path,identity in pin['files'].items(): assert digest(ROOT/path)==identity['sha256'],path
    h=module('boundary_hybrid','reviews/2026-09-29-cc-hybrid-recovery/hybrid.py')
    t=module('boundary_adapter',PREVIOUS+'transfer.py')
    phase=module('boundary_phase','reviews/2026-09-29-cc-phase-screen/compare.py')
    api=module('boundary_compiler','reviews/2026-09-29-cc-coverage-compiler/compiler.py')
    physical=module('boundary_physical','reviews/2026-09-29-cc-ten-runner/transfer.py')
    api.key=phase.key
    sources=read('reviews/2026-09-29-cc-nine-runner/stage8.json')['certificate']['candidates']
    assert len(sources)==36
    return pin,h,t,phase,api,physical,sources


def fields(value):
    if isinstance(value,dict): return sum(fields(x) for x in value.values())
    if isinstance(value,(list,tuple)): return sum(fields(x) for x in value)
    return 1


def regression(h,t,phase,api,physical,sources):
    adapter=t.bind(h,phase,api,physical,OLD)
    hybrid=h.build_hybrid(phase,api,sources);full=h.build_full(phase,api,sources)
    old_hybrid=read(PREVIOUS+'hybrid.json');old_full=read(PREVIOUS+'full.json')
    assert encode(hybrid)==old_hybrid
    assert encode(full)==old_full
    controls=read(PREVIOUS+'audit.json')['controls'];rebuilt=[]
    for r in controls:
        rebuilt.append(dict(pair=r['pair'],primary=physical.primary(*r['pair']),
            hybrid=t.hybrid_select(h,api,physical,hybrid,*r['pair']),
            full=t.full_select(h,api,physical,full,*r['pair'])))
    assert encode(rebuilt)==controls
    return dict(status='PASS',adapter=adapter,hybrid_scalar_fields=fields(old_hybrid),
                full_scalar_fields=fields(old_full),control_scalar_fields=fields(controls),
                controls_per_method=len(controls),scope='Previous target exact regression; no prior timing or new coefficient scan')


def reduced(cert):
    return cert['status'] in ('COMPLETE_COVER_CERTIFICATE','UNCOVERED_PRIMITIVE_PAIRS') and 'residual_pairs' in cert


def audit(h,t,phase,api,physical,screened,hybrid,full,sources):
    sc=hybrid['screen_certificate'];fc=full['certificate'];rec=hybrid.get('recovery')
    global_scope=reduced(sc) and reduced(fc) and full['clipping']['status']=='PASS' and rec is not None and rec['status'] in ('COMPLETE_EXCEPTION_RECOVERY','NO_SOURCE_CONTACT')
    union=sorted({tuple(p) for c in (sc,fc) for p in c.get('residual_pairs',[])})
    assert len(union)<=800
    assert encode(screened['candidates'])==encode(sc.get('candidates',[]))
    rows=[]
    for pair in union:
        full_hits=[s['id'] for s in fc.get('candidates',[]) if api.contact(s,*pair)['hit']]
        screen_hits=[s['id'] for s in sc.get('candidates',[]) if api.contact(s,*pair)['hit']]
        selected=t.hybrid_select(h,api,physical,hybrid,*pair)
        rows.append(dict(pair=pair,primary=physical.primary(*pair),hybrid=selected,
            full_class_hit=bool(full_hits),full_contact_ids=full_hits,
            screen_class_hit=bool(screen_hits),screen_contact_ids=screen_hits,
            dispatch_coverage_equal=(selected['status']=='HIT')==bool(full_hits)))
    full_byid={s['id']:s for s in fc.get('candidates',[])};subset=[];membership=[]
    source_byid={s['id']:s for s in sources}
    for s in sc.get('candidates',[]):
        same=encode(s)==encode(full_byid.get(s['id']))
        if full['clipping']['status']=='PASS': assert same
        subset.append(dict(id=s['id'],identical_full_member=same))
    for r in (rec or {}).get('exceptions',[]):
        ident=r['source_id']+f':M{r["ninth_lap"]}';full_member=full_byid.get(ident)
        source=source_byid[r['source_id']];a,b=h.ends(source)
        assert h.at(a,b,F(r['local_parameter']))==tuple(map(F,r['point']))
        s0,s1=map(F,source['source_parameters'])
        assert s0+F(r['local_parameter'])*(s1-s0)==F(r['original_parameter'])
        if full_member is None:
            membership.append(dict(pair=r['pair'],status='NO_FULL_COMPARISON_RECORD'));continue
        lo,hi=map(F,full_member['source_parameters']);orig=F(r['original_parameter'])
        assert lo<=orig<=hi and tuple(r['labels'])==tuple(full_member['labels'])
        membership.append(dict(pair=r['pair'],candidate_id=ident,original_parameter=orig,
                               full_parameter_interval=(lo,hi),labels_equal=True))
    controls=[dict(pair=pair,primary=physical.primary(*pair),hybrid=t.hybrid_select(h,api,physical,hybrid,*pair),
                    full=t.full_select(h,api,physical,full,*pair)) for pair in physical.PAIRS+((5,1),(10,2))]
    opened=h.recovery(sources,sc.get('uncovered',[]),opened=True) if reduced(sc) else dict(status='NOT_TRIGGERED')
    zero=h.preflight(sources,sc.get('uncovered',[]),budget=0) if reduced(sc) else dict(status='NOT_TRIGGERED')
    missed=[r for r in rows if r['primary'] and r['full_class_hit'] and r['hybrid']['status']!='HIT']
    diagnostic=dict(status='NOT_TRIGGERED')
    if missed:
        row=missed[0];s=full_byid[row['full_contact_ids'][0]];hit=api.contact(s,*row['pair'])
        diagnostic=dict(status='FULL_SOURCE_WITNESS',pair=row['pair'],hybrid_status=hybrid['status'],
                        witness=physical.recover(api,s,hit,*row['pair'],Z),fed_back_into_hybrid=False)
    return dict(status='PASS',comparison_scope='ALL_POSITIVE_PRIMITIVE_DIRECTIONS' if global_scope else 'REACHED_FINITE_UNION_ONLY',
        union_pairs=union,comparison=rows,dispatch_coverage_mismatches=[r['pair'] for r in rows if not r['dispatch_coverage_equal']],
        screen_class_lost_pairs=[r['pair'] for r in rows if r['full_class_hit'] and not r['screen_class_hit']],
        screen_subset=subset,exception_membership=membership,controls=controls,
        open_source_diagnostic=opened,zero_budget={k:v for k,v in zero.items() if k!='rows'},full_source_diagnostic=diagnostic)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--benchmark',action='store_true');args=parser.parse_args()
    pin,h,t,phase,api,physical,sources=setup()
    save('regression.json',regression(h,t,phase,api,physical,sources))
    save('adapter.json',t.bind(h,phase,api,physical,TARGET))
    hybrid=h.build_hybrid(phase,api,sources);save('hybrid.json',hybrid)
    full=h.build_full(phase,api,sources);save('full.json',full)
    screened=phase.screen(sources,TARGET);save('screen.json',screened)
    checks=audit(h,t,phase,api,physical,screened,hybrid,full,sources);save('audit.json',checks)
    sc=hybrid['screen_certificate'];fc=full['certificate'];rec=hybrid.get('recovery') or {}
    summary=dict(protocol_sha256=pin['protocol_sha256'],target=TARGET,threshold=Z,relations=screened['relations'],
        hybrid_status=hybrid['status'],screen_status=sc['status'],full_status=fc['status'],full_clipping_status=full['clipping']['status'],
        screen_counts=hybrid['screen_counts'],screen_compiler_counts=sc.get('counts'),screen_leader=sc.get('leader'),
        exception_pairs=sc.get('uncovered'),recovered=rec.get('exceptions'),recovery_counts=rec.get('counts'),
        preflight={k:v for k,v in rec.get('preflight',{}).items() if k!='rows'},
        full_compiler_counts=fc.get('counts'),full_leader=fc.get('leader'),full_clipping_counts={k:v for k,v in full['clipping'].items() if k!='trace'},
        comparison_scope=checks['comparison_scope'],union_pairs=len(checks['union_pairs']),
        dispatch_coverage_mismatches=checks['dispatch_coverage_mismatches'],screen_class_lost_pairs=checks['screen_class_lost_pairs'],
        controls_per_method=len(checks['controls']),hybrid_control_hits=sum(r['hybrid']['status']=='HIT' for r in checks['controls']),
        full_control_hits=sum(r['full']['status']=='HIT' for r in checks['controls']),
        open_source_status=checks['open_source_diagnostic']['status'],full_source_diagnostic_status=checks['full_source_diagnostic']['status'],
        source_validation_endpoint_band_checks_per_method=hybrid['source_validation_endpoint_band_checks'],
        evidence='Informed different-boundary transfer; universal arguments remain internally reviewed proof candidates')
    save('summary.json',summary)
    if args.benchmark:
        if hybrid['status']=='COMPLETE_HYBRID_CERTIFICATE' and fc['status']=='COMPLETE_COVER_CERTIFICATE' and full['clipping']['status']=='PASS':
            timing=h.benchmark(phase,api,sources)
        else: timing=dict(status='NOT_TRIGGERED',reason='Both complete new certificates required',hybrid_status=hybrid['status'],full_status=fc['status'],clipping_status=full['clipping']['status'])
        save('timing.json',timing)
    print(json.dumps(encode(summary),sort_keys=True))


if __name__=='__main__': main()
