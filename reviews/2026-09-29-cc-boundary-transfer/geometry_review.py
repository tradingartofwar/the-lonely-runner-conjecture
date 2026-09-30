#!/usr/bin/env python3
"""Different-boundary audit using pinned independent review primitives only."""
import importlib.util
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PRIOR='reviews/2026-09-29-cc-hybrid-transfer/'
REVIEW=PRIOR+'geometry_review.py'
OLD=(102,50)
TARGET=(78,50)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads((ROOT/path).read_text())
def need(value,label):
    if not value: raise ArithmeticError(label)


def load_review():
    spec=importlib.util.spec_from_file_location('pinned_independent_transfer_review',ROOT/REVIEW)
    t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
    return t,t.load_reviewer()


def controls(t,g,compact,recovery,full):
    return [dict(pair=pair,primary=g.primary(*pair),hybrid=t.hybrid_dispatch(g,compact,recovery,pair),
                 full=t.full_dispatch(g,full,pair)) for pair in g.CONTROLS]


def controls_geometry(t,raw):
    return [dict(pair=r['pair'],primary=r['primary'],hybrid=t.retain_geometry(r['hybrid']),
                 full=t.retain_geometry(r['full'])) for r in raw]


def target_audit(t,g,sources,hybrid,compact,full):
    rec=hybrid['recovery']
    union=sorted(set(compact['residual_pairs'])|set(full['residual_pairs']))
    need(len(union)<=800,'residual union cap')
    records=[]
    for pair in union:
        full_hits=[r['id'] for r in full['candidates'] if g.contact(r,*pair)['hit']]
        screen_hits=[r['id'] for r in compact['candidates'] if g.contact(r,*pair)['hit']]
        dispatch=t.hybrid_dispatch(g,compact,rec,pair)
        records.append(dict(pair=pair,primary=g.primary(*pair),hybrid=dispatch,
                            full_class_hit=bool(full_hits),full_contact_ids=full_hits,
                            screen_class_hit=bool(screen_hits),screen_contact_ids=screen_hits,
                            dispatch_coverage_equal=bool(full_hits)))
    full_by_id={r['id']:r for r in full['candidates']}
    subset=[]
    for r in compact['candidates']:
        need(g.encode(r)==g.encode(full_by_id[r['id']]),'screen-full candidate mismatch')
        subset.append(dict(id=r['id'],identical_full_member=True))
    # The independently obtained screen is complete, so there is no recovered
    # point or missing-direction diagnostic to construct in this reached run.
    need(compact['status']=='COMPLETE_COVER_CERTIFICATE' and not rec['exceptions'],'screen did not complete')
    opened=g.recover(sources,compact['uncovered'],opened=True)
    zero=g.preflight(sources,compact['uncovered'],budget=0)
    need(not opened['queries'] and not opened['exceptions'] and not zero['rows'],'empty diagnostics did work')
    return dict(status='PASS',comparison_scope='ALL_POSITIVE_PRIMITIVE_DIRECTIONS',union_pairs=union,
                comparison=records,dispatch_coverage_mismatches=[r['pair'] for r in records if not r['dispatch_coverage_equal']],
                screen_class_lost_pairs=[r['pair'] for r in records if r['full_class_hit'] and not r['screen_class_hit']],
                screen_subset=subset,exception_membership=[],controls=controls(t,g,compact,rec,full),
                open_source_diagnostic=opened,zero_budget={k:v for k,v in zero.items() if k!='rows'},
                full_source_diagnostic=dict(status='NOT_TRIGGERED'))


def main():
    pins=json.loads((HERE/'INPUTS.json').read_text())
    need(digest(HERE/'PROTOCOL.md')==pins['protocol_sha256'],'protocol changed')
    for path,pin in pins['files'].items(): need(digest(ROOT/path)==pin['sha256'],'input changed '+path)
    t,g=load_review()
    sources=g.decode_source(read('reviews/2026-09-29-cc-nine-runner/stage8.json')['certificate']['candidates'])
    fields={}
    old_binding=t.bind_reviewer(g,OLD)
    old_hybrid,old_full,old_compact,old_full_core=t.construct(g,sources)
    fields['old_hybrid']=g.compare(g.encode(old_hybrid),read(PRIOR+'hybrid.json'),'old hybrid')
    fields['old_full']=g.compare(g.encode(old_full),read(PRIOR+'full.json'),'old full record')
    old_controls=controls(t,g,old_compact,old_hybrid['recovery'],old_full_core)
    archive_controls=read(PRIOR+'audit.json')['controls']
    fields['old_control_geometry']=g.compare(g.encode(old_controls),controls_geometry(t,archive_controls),'old control geometry')
    hashes=t.source_hashes();base=g.ROWS[:-1]
    static_adapter=t.validate_adapter_ast()
    old_adapter=t.adapter_record(base,(54,26),(38,18),OLD,hashes)
    regression=dict(status='PASS',adapter=old_adapter,hybrid_scalar_fields=fields['old_hybrid'],
                    full_scalar_fields=fields['old_full'],control_scalar_fields=t.leaf_count(archive_controls),
                    controls_per_method=len(old_controls),scope='Previous target exact regression; no prior timing or new coefficient scan')
    fields['regression']=g.compare(g.encode(regression),json.loads((HERE/'regression.json').read_text()),'regression metadata')
    new_binding=t.bind_reviewer(g,TARGET)
    fields['adapter']=g.compare(g.encode(t.adapter_record(base,OLD,OLD,TARGET,hashes)),json.loads((HERE/'adapter.json').read_text()),'new adapter')
    hybrid,full,compact,full_core=t.construct(g,sources)
    fields['hybrid']=g.compare(g.encode(hybrid),json.loads((HERE/'hybrid.json').read_text()),'target hybrid')
    fields['full']=g.compare(g.encode(full),json.loads((HERE/'full.json').read_text()),'target full')
    screened=g.screen_for_output(g.screen_sources(sources))
    fields['screen']=g.compare(g.encode(screened),json.loads((HERE/'screen.json').read_text()),'screen decisions')
    audit=target_audit(t,g,sources,hybrid,compact,full_core)
    actual_audit=json.loads((HERE/'audit.json').read_text())
    for r in actual_audit['comparison']: r['hybrid']=t.retain_geometry(r['hybrid'])
    actual_audit['controls']=controls_geometry(t,actual_audit['controls'])
    fields['audit_geometry']=g.compare(g.encode(audit),actual_audit,'audit geometry')
    rec=hybrid['recovery']
    summary=dict(protocol_sha256=pins['protocol_sha256'],target=TARGET,threshold=g.Z,relations=screened['relations'],
      hybrid_status=hybrid['status'],screen_status=compact['status'],full_status=full_core['status'],full_clipping_status=full['clipping']['status'],
      screen_counts=hybrid['screen_counts'],screen_compiler_counts=compact['counts'],screen_leader=compact['leader'],
      exception_pairs=compact['uncovered'],recovered=rec['exceptions'],recovery_counts=rec['counts'],
      preflight={k:v for k,v in rec['preflight'].items() if k!='rows'},full_compiler_counts=full_core['counts'],
      full_leader=full_core['leader'],full_clipping_counts={k:v for k,v in full['clipping'].items() if k!='trace'},
      comparison_scope=audit['comparison_scope'],union_pairs=len(audit['union_pairs']),
      dispatch_coverage_mismatches=audit['dispatch_coverage_mismatches'],screen_class_lost_pairs=audit['screen_class_lost_pairs'],
      controls_per_method=len(g.CONTROLS),hybrid_control_hits=len(g.CONTROLS),full_control_hits=len(g.CONTROLS),
      open_source_status=audit['open_source_diagnostic']['status'],full_source_diagnostic_status=audit['full_source_diagnostic']['status'],
      source_validation_endpoint_band_checks_per_method=hybrid['source_validation_endpoint_band_checks'],
      evidence='Informed different-boundary transfer; universal arguments remain internally reviewed proof candidates')
    fields['summary']=g.compare(g.encode(summary),json.loads((HERE/'summary.json').read_text()),'summary')
    by_id={r['id']:r for r in compact['candidates']}
    report=dict(status='PASS',protocol_sha256=pins['protocol_sha256'],script_sha256=digest(Path(__file__)),
      inherited_reviewers={path:pins['files'][path]['sha256'] for path in (REVIEW,t.GEO)},
      independent_old_binding=old_binding,independent_new_binding=new_binding,
      production_adapter_verification=static_adapter,field_counts=fields,total_scalar_fields_compared=sum(fields.values()),
      compared_sha256={name:digest(HERE/(name+'.json')) for name in ('regression','adapter','hybrid','full','screen','audit','summary')},
      relations=screened['relations'],screen_counts=hybrid['screen_counts'],screen_compiler_counts=compact['counts'],
      screen_leader=compact['leader'],leader_record=by_id[compact['leader']['id']],chosen_ids=compact['chosen_ids'],
      preflight=summary['preflight'],recovery_counts=rec['counts'],exceptions=rec['exceptions'],
      full_counts=full_core['counts'],full_clipping_counts=summary['full_clipping_counts'],union_pairs=len(audit['union_pairs']),
      dispatch_coverage_mismatches=audit['dispatch_coverage_mismatches'],screen_class_lost_pairs=audit['screen_class_lost_pairs'],
      open_diagnostic=dict(raw_status=audit['open_source_diagnostic']['status'],pair_count=0,query_count=0,
                           interpretation='VACUOUS_EMPTY_DOMAIN; no target open-source contact was tested'),
      zero_budget=audit['zero_budget'],scope='Pinned independent primitives with disclosed data/default binding; no production imports, benchmarks, new targets or new fixtures. Physical recovery fields reviewed separately.')
    print(json.dumps(g.encode(report),indent=2,sort_keys=True))


if __name__=='__main__': main()
