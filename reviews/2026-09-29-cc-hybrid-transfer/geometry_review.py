#!/usr/bin/env python3
"""Data-adapted independent hybrid reviewer; imports only the pinned old reviewer."""
import ast
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from math import floor,gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=(54,26)
TARGET=(102,50)
PRIOR='reviews/2026-09-29-cc-hybrid-recovery/'
GEO=PRIOR+'geometry_review.py'


def read(path): return json.loads((ROOT/path).read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def need(value,label):
    if not value: raise ArithmeticError(label)


def load_reviewer():
    spec=importlib.util.spec_from_file_location('pinned_independent_geometry',ROOT/GEO)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bind_reviewer(g,target):
    before=dict(rows=g.ROWS,source_bounds_defaults=g.source_bounds.__defaults__,query_defaults=g.query.__defaults__)
    bodies={name:getattr(g,name).__code__ for name in ('source_bounds','query','recover','screen_sources','append_full','coverage')}
    g.ROWS=g.ROWS[:-1]+(target,)
    g.source_bounds.__defaults__=(target,)
    g.query.__defaults__=(target,False)
    need(all(getattr(g,name).__code__ is body for name,body in bodies.items()),'reviewer bodies changed')
    return dict(before=before,after=dict(rows=g.ROWS,source_bounds_defaults=g.source_bounds.__defaults__,query_defaults=g.query.__defaults__),
                bodies_unchanged=True)


def source_hashes():
    groups={
      'hybrid':(PRIOR+'hybrid.py',('bounds','preflight','query','recovery','validate_sources','build_hybrid','build_full','select','benchmark')),
      'phase':('reviews/2026-09-29-cc-phase-screen/compare.py',('screen','full_clip')),
      'compiler':('reviews/2026-09-29-cc-coverage-compiler/compiler.py',('compile_records','contact')),
      'physical':('reviews/2026-09-29-cc-ten-runner/transfer.py',('recover',))}
    out={}
    for prefix,(path,names) in groups.items():
        source=(ROOT/path).read_text();lines=source.splitlines(keepends=True)
        nodes={n.name:n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        for name in names:
            node=nodes[name]
            text=''.join(lines[node.lineno-1:node.end_lineno])
            out[prefix+'.'+name]=hashlib.sha256(text.encode()).hexdigest()
    return out


def production_bindings(base,target,physical_target):
    return {'hybrid.TARGET':target,'hybrid.ROWS':base+(target,),
            'bounds.__defaults__':(target,),'query.__defaults__':(target,False,None),
            'physical.ROWS':base+(physical_target,), 'physical.ADDED':base[6:]+(physical_target,)}


def adapter_record(base,before_target,before_physical,target,hashes):
    return dict(target=target,before=production_bindings(base,before_target,before_physical),
                after=production_bindings(base,target,target),function_code_identity_unchanged=True,
                function_source_sha256_before=hashes,function_source_sha256_after=hashes,
                inherited_adapter='compiler.key = phase.key; unchanged numeric provenance ordering',
                unused_old_binding='phase.TARGET remains old; screen/full_clip receive target explicitly')


def validate_adapter_ast():
    source=(HERE/'transfer.py').read_text()
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='bind')
    attr_targets=[]
    for n in ast.walk(node):
        if isinstance(n,ast.Assign):
            for target in n.targets:
                if isinstance(target,ast.Attribute): attr_targets.append(ast.unparse(target))
    expected=['h.TARGET','h.ROWS','h.bounds.__defaults__','h.query.__defaults__','physical.ROWS','physical.ADDED']
    need(attr_targets==expected,'production adapter mutates unexpected attribute')
    return dict(attribute_assignments=attr_targets,scope='static source/binding verification; production modules were not imported')


def construct(g,sources):
    validated=0
    for source in sources:
        need(len(source['labels'])==8 and all(type(m) is int for m in source['labels']),'source labels')
        for point in source['endpoints']:
            need(all(0<=x<1 for x in point),'source square')
            for row,m in zip(g.ROWS[:-1],source['labels']):
                need(g.Z<=g.dot(row,point)-m<=1-g.Z,'source safety');validated+=1
    screen=g.screen_sources(sources)
    compact=g.coverage(screen['candidates'],g.Z)
    recovery=g.recover(sources,compact['uncovered'])
    hybrid=dict(screen_counts=g.screen_for_output(screen)['counts'],screen_certificate=g.certificate_for_output(compact,g.ROWS[-1]),
                source_validation_endpoint_band_checks=validated,status='COMPLETE_HYBRID_CERTIFICATE',recovery=recovery)
    full_records,clipping=g.append_full(sources,g.ROWS[-1])
    full_core=g.coverage(full_records,g.Z)
    full=dict(certificate=g.certificate_for_output(full_core,g.ROWS[-1]),clipping=clipping,
              source_validation_endpoint_band_checks=validated)
    return hybrid,full,compact,full_core


def leaf_count(v):
    if isinstance(v,dict): return sum(leaf_count(x) for x in v.values())
    if isinstance(v,list): return sum(leaf_count(x) for x in v)
    return 1


def hybrid_dispatch(g,compact,recovery,pair):
    result=g.dispatch(compact,recovery,*pair)
    del result['pair']
    return dict(status='HIT',**result)


def full_dispatch(g,full,pair):
    p,q=pair;d=gcd(p,q);primitive=(p//d,q//d)
    by_id={r['id']:r for r in full['candidates']}
    for identity in full['chosen_ids']:
        record=by_id[identity];hit=g.contact(record,*primitive)
        if hit['hit']:
            return dict(status='HIT',witness=dict(segment=identity,contact=hit,point=hit['point'],h=hit['first_integer'],
                                                 torus_laps=record['labels'],primitive=primitive))
    raise ArithmeticError('full menu misses a declared control')


def retain_geometry(selection):
    result=dict(selection)
    if 'witness' in result:
        keep=('segment','contact','point','h','torus_laps','primitive')
        result['witness']={k:v for k,v in result['witness'].items() if k in keep}
    return result


def target_audit(g,sources,hybrid,compact,full):
    recovery=hybrid['recovery']
    union=sorted(set(compact['residual_pairs'])|set(full['residual_pairs']))
    need(len(union)<=800,'union cap')
    comparison=[]
    for pair in union:
        hit_ids=[r['id'] for r in full['candidates'] if g.contact(r,*pair)['hit']]
        selected=hybrid_dispatch(g,compact,recovery,pair)
        comparison.append(dict(pair=pair,primary=g.primary(*pair),hybrid=selected,
                               full_class_hit=bool(hit_ids),full_contact_ids=hit_ids,coverage_equal=bool(hit_ids)))
    by_id={r['id']:r for r in full['candidates']}
    subset=[]
    for r in compact['candidates']:
        need(g.encode(r)==g.encode(by_id[r['id']]),'screen subset')
        subset.append(dict(id=r['id'],identical_full_member=True))
    membership=[]
    for e in recovery['exceptions']:
        candidate_id=e['source_id']+f':M{e["ninth_lap"]}'
        r=by_id[candidate_id];lo,hi=r['source_parameters']
        need(lo<=e['original_parameter']<=hi and r['labels']==e['labels'],'exception membership')
        membership.append(dict(pair=e['pair'],candidate_id=candidate_id,original_parameter=e['original_parameter'],
                               full_parameter_interval=(lo,hi),labels_equal=True))
    controls=[dict(pair=pair,primary=g.primary(*pair),hybrid=hybrid_dispatch(g,compact,recovery,pair),
                   full=full_dispatch(g,full,pair)) for pair in g.CONTROLS]
    opened=g.recover(sources,compact['uncovered'],opened=True)
    zero=g.preflight(sources,compact['uncovered'],budget=0)
    speed=g.ROWS[-1][0]*5+g.ROWS[-1][1]
    old_time=F(9,40);raw=speed*old_time;phase=raw-floor(raw)
    failure=dict(pair=(5,1),old_time=old_time,new_speed=speed,raw=raw,phase=phase,safe=g.Z<=phase<=1-g.Z)
    need(raw==126 and not failure['safe'],'old-time failure')
    return dict(status='PASS',comparison_scope='ALL_POSITIVE_PRIMITIVE_DIRECTIONS',union_pairs=union,
                comparison=comparison,coverage_mismatches=[r['pair'] for r in comparison if not r['coverage_equal']],
                screen_subset=subset,exception_membership=membership,controls=controls,
                open_source_diagnostic=opened,zero_budget={k:v for k,v in zero.items() if k!='rows'},old_time_failure=failure)


def main():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    need(digest(HERE/'PROTOCOL.md')==pins['protocol_sha256'],'protocol changed')
    for path,pin in pins['files'].items(): need(digest(ROOT/path)==pin['sha256'],'input changed '+path)
    g=load_reviewer()
    sources=g.decode_source(read('reviews/2026-09-29-cc-nine-runner/stage8.json')['certificate']['candidates'])
    fields={}
    bind_old=bind_reviewer(g,OLD)
    old_hybrid,old_full,old_compact,_=construct(g,sources)
    fields['old_hybrid']=g.compare(g.encode(old_hybrid),read(PRIOR+'hybrid.json'),'old hybrid')
    fields['old_full']=g.compare(g.encode(old_full['certificate']),read('reviews/2026-09-29-cc-phase-screen/full.json')['certificate'],'old full')
    old_audit=read(PRIOR+'audit.json')
    old_controls=[g.dispatch(old_compact,old_hybrid['recovery'],*pair) for pair in g.CONTROLS]
    fields['old_dispatch_geometry']=g.compare(g.encode(old_controls),g.project_dispatch(old_audit['physical_controls']),'old dispatch')
    fields['old_kernel']=g.compare(g.encode(g.fixtures()),old_audit['kernel'],'old kernels')
    hashes=source_hashes();base=g.ROWS[:-1]
    static_adapter=validate_adapter_ast()
    adapter_old=adapter_record(base,OLD,(38,18),OLD,hashes)
    expected_regression=dict(status='PASS',adapter=adapter_old,hybrid_scalar_fields=fields['old_hybrid'],
        full_certificate_scalar_fields=fields['old_full'],physical_controls=len(old_controls),
        physical_scalar_fields=leaf_count(old_audit['physical_controls']),kernel_fixtures=4,
        scope='Exact old-row adapter regression; no old benchmark or added targets')
    fields['adapter_regression']=g.compare(g.encode(expected_regression),json.loads((HERE/'adapter_regression.json').read_text()),'adapter regression')
    bind_new=bind_reviewer(g,TARGET)
    fields['adapter']=g.compare(g.encode(adapter_record(base,OLD,OLD,TARGET,hashes)),json.loads((HERE/'adapter.json').read_text()),'adapter')
    hybrid,full,compact,full_core=construct(g,sources)
    fields['hybrid']=g.compare(g.encode(hybrid),json.loads((HERE/'hybrid.json').read_text()),'hybrid')
    fields['full']=g.compare(g.encode(full),json.loads((HERE/'full.json').read_text()),'full')
    audit=target_audit(g,sources,hybrid,compact,full_core)
    actual=json.loads((HERE/'audit.json').read_text())
    for r in actual['comparison']: r['hybrid']=retain_geometry(r['hybrid'])
    for r in actual['controls']:
        r['hybrid']=retain_geometry(r['hybrid']);r['full']=retain_geometry(r['full'])
    fields['audit_geometry']=g.compare(g.encode(audit),actual,'audit geometry')
    recovery=hybrid['recovery']
    summary=dict(protocol_sha256=pins['protocol_sha256'],target=TARGET,threshold=g.Z,
      hybrid_status=hybrid['status'],full_status=full_core['status'],full_clipping_status=full['clipping']['status'],
      screen_counts=hybrid['screen_counts'],screen_compiler_counts=compact['counts'],screen_leader=compact['leader'],
      exception_pairs=compact['uncovered'],recovered=recovery['exceptions'],recovery_counts=recovery['counts'],
      preflight={k:v for k,v in recovery['preflight'].items() if k!='rows'},full_compiler_counts=full_core['counts'],
      full_leader=full_core['leader'],full_clipping_counts={k:v for k,v in full['clipping'].items() if k!='trace'},
      comparison_scope=audit['comparison_scope'],union_pairs=len(audit['union_pairs']),coverage_mismatches=audit['coverage_mismatches'],
      hybrid_control_hits=len(g.CONTROLS),full_control_hits=len(g.CONTROLS),physical_controls=len(g.CONTROLS),
      open_source_status=audit['open_source_diagnostic']['status'],old_time_failure=audit['old_time_failure'],
      source_validation_endpoint_band_checks_per_method=hybrid['source_validation_endpoint_band_checks'],
      evidence='Informed within-progression stress transfer; general arguments remain internally reviewed proof candidates')
    fields['summary']=g.compare(g.encode(summary),json.loads((HERE/'summary.json').read_text()),'summary')
    report=dict(status='PASS',protocol_sha256=pins['protocol_sha256'],script_sha256=digest(Path(__file__)),
      inherited_reviewer=dict(path=GEO,sha256=pins['files'][GEO]['sha256'],old_binding=bind_old,new_binding=bind_new),
      production_adapter_verification=static_adapter,field_counts=fields,total_scalar_fields_compared=sum(fields.values()),
      compared_sha256={name:digest(HERE/(name+'.json')) for name in ('adapter_regression','adapter','hybrid','full','audit','summary')},
      preflight=summary['preflight'],recovery_counts=recovery['counts'],exceptions=recovery['exceptions'],
      open_recovery_counts=audit['open_source_diagnostic']['counts'],old_time_failure=audit['old_time_failure'],
      comparison_scope=audit['comparison_scope'],union_pairs=len(audit['union_pairs']),coverage_mismatches=audit['coverage_mismatches'],
      full_counts=full_core['counts'],full_clipping_counts=summary['full_clipping_counts'],
      scope='No production imports; pinned prior independent reviewer reused with disclosed data/default bindings. All geometry/traces/dispatch choices checked; physical recovery fields reviewed separately. No benchmark rerun or additional targets.')
    print(json.dumps(g.encode(report),indent=2,sort_keys=True))


if __name__=='__main__': main()
