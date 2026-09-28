"""Frozen audit of archived positive windows missed by their optimal tree.

The source archive stores per-core summaries and component digests, not every
component record. Reconstruct only its five cores reporting a positive miss;
recheck their full digests, and retain precisely the 18 prescribed records.
Only those 18 receive LPs or diagnostic higher-order reconstruction.
--write uses floating LP proposals, accepted solely by exact primal/dual checks.
--check is read-only, requires only the standard library, and makes no LP calls.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from math import lcm
import argparse, hashlib, importlib.util, json, sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / 'protocol.json'
OUT = HERE / 'results.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = ROOT / 'reviews/2026-09-27-team/calculate.py'
LP_SOURCE = ROOT / 'reviews/2026-09-28-collective-obligations/primary.py'
CONTROL_SOURCE = ROOT / 'reviews/2026-09-28-cover-obligations/primary.py'
src = load_module('archived_component_geometry', SOURCE)
lp = load_module('archived_exact_lp', LP_SOURCE)


def reconstruct_selected(archive):
    """Reconstruct locator digests using only singleton/pair geometry.

    Source labels (indices into velocities) are retained; they are not silently
    replaced by their physical speeds. Strict endpoint membership is essential
    for reproducing vanished/containment fields in the historical digest.
    """
    selected, locators = [], []
    for case in archive['cases']:
        flagged = [c for c in case['cores'] if c['summary']['positive_actual_tree_misses']]
        if not flagged:
            continue
        velocities = case['velocities']
        speeds = {i: abs(velocities[i]-velocities[0]) for i in range(1, 8)}
        den = 8*lcm(*speeds.values())
        assert den == case['integer_denominator']
        safe, blocks, point_blocks = {}, {}, {}
        for i,v in speeds.items():
            unit = den//(8*v)
            safe[i] = [((8*j+1)*unit,(8*j+7)*unit) for j in range(v)]
            pieces = [(0,unit,True,False)]
            pieces += [((8*j-1)*unit,(8*j+1)*unit,False,False) for j in range(1,v)]
            pieces += [((8*v-1)*unit,den,False,True)]
            point_blocks[i] = src.PointSet(pieces)
            blocks[i] = [(a,b) for a,b,_,_ in pieces]
        full = [(int(F(a)*den),int(F(b)*den)) for a,b in case['full_allowed_components']]
        assert all(F(x)*den == int(F(x)*den) for p in case['full_allowed_components'] for x in p)
        actual_integral = src.Integral(full)
        for core_record in flagged:
            core = tuple(core_record['core']); residual = tuple(core_record['residual'])
            windows = [(0,den)]
            for i in sorted(core,key=lambda i:speeds[i]):
                windows = src.intersect(windows,safe[i])
            ints = {():src.Integral([(0,den)])}
            for i in residual:
                ints[i,] = src.Integral(blocks[i])
            for i,j in combinations(residual,2):
                ints[i,j] = src.Integral(src.intersect(blocks[i],blocks[j]))
            violations = {(i,j):src.PointSet(src.strict_intersect(point_blocks[i].pieces,
                [(a,b,True,True) for a,b in safe[j]]))
                for i in residual for j in residual if i!=j}
            sha = hashlib.sha256(); misses = 0; positive = 0
            for index,(a,b) in enumerate(windows):
                singles = {i:ints[i,].on(a,b) for i in residual}
                pairs = {(i,j):ints[i,j].on(a,b) for i,j in combinations(residual,2)}
                vanished = tuple(i for i in residual if not point_blocks[i].nonempty_on(a,b))
                edges = tuple((i,j) for i in residual for j in residual if i!=j and not violations[i,j].nonempty_on(a,b))
                edge_set = set(edges); nonempty = tuple(i for i in residual if i not in vanished)
                proper = tuple((i,j) for i,j in edges if i in nonempty and j in nonempty and (j,i) not in edge_set)
                classes=[]; ungrouped=set(nonempty)
                while ungrouped:
                    i=min(ungrouped)
                    group=tuple(j for j in nonempty if j==i or ((i,j) in edge_set and (j,i) in edge_set))
                    classes.append(group); ungrouped.difference_update(group)
                retained=tuple(g[0] for g in classes if not any((g[0],j) in proper for j in nonempty))
                full_weight,_=src.optimal_tree(residual,pairs)
                reduced_weight,tree=src.optimal_tree(retained,pairs)
                bound=b-a-sum(singles[i] for i in retained)+reduced_weight
                assert bound == b-a-sum(singles.values())+full_weight
                actual=actual_integral.on(a,b); positive += actual>0
                row=[src.rational(a,den),src.rational(b,den),src.rational(bound,den),
                     src.rational(actual,den),vanished,edges,retained]
                sha.update((json.dumps(row,separators=(',',':'))+'\n').encode())
                if actual<=0 or bound>0:
                    continue
                misses += 1
                # Diagnostic full moments are calculated only after the fixed
                # archive-derived positive/tree-missed predicate selects a row.
                moments=[]
                for mask in range(16):
                    pieces=[(a,b)]
                    for bit,i in enumerate(residual):
                        if mask>>bit&1:
                            pieces=src.intersect(pieces,blocks[i])
                    moments.append(F(sum(y-x for x,y in pieces),den))
                atoms=moments[:]
                for bit in range(4):
                    for mask in range(16):
                        if not mask>>bit&1:
                            atoms[mask]-=atoms[mask|(1<<bit)]
                assert all(x>=0 for x in atoms) and atoms[0]==F(actual,den)
                assert moments[0]==F(b-a,den)
                for bit,i in enumerate(residual):
                    assert moments[1<<bit]==F(singles[i],den)
                for first,second in combinations(range(4),2):
                    assert moments[(1<<first)|(1<<second)]==F(pairs[residual[first],residual[second]],den)
                ident=f"{case['id']}:{','.join(map(str,core))}:{index}"
                selected.append(dict(id=ident,case_id=case['id'],velocities=velocities,
                    reference_index=0,core_labels=list(core),core_speeds=[speeds[i] for i in core],
                    residual_labels=list(residual),residual_speeds=[speeds[i] for i in residual],
                    component_index=index,window=[F(a,den),F(b,den)],
                    reduced_tree_bound=F(bound,den),reduced_tree_edges=tree,retained=retained,
                    archived_actual_duration=F(actual,den),moments=moments,atoms=atoms))
            assert sha.hexdigest()==core_record['component_sha256'],core
            assert len(windows)==core_record['summary']['components']
            assert misses==core_record['summary']['positive_actual_tree_misses']
            assert positive==core_record['summary']['positive_actual_components']
            locators.append(dict(case_id=case['id'],core_labels=list(core),
                components_reconstructed=len(windows),positive_components=positive,
                selected_misses=misses,component_sha256=sha.hexdigest()))
    assert len(selected)==18 and len(locators)==5
    assert len({r['id'] for r in selected})==18
    return selected,locators


def evaluate(record,old=None):
    moments={m:record['moments'][m] for m in lp.MOMENT_MASKS}
    def solve(spec,cert=None):
        if cert is None:
            return lp.propose_certificate(spec)
        expected=lp.serialize(spec)
        assert {k:cert[k] for k in expected}==expected
        lp.verify_certificate(cert)
        return cert
    base=solve(lp.make_spec(moments,lp.EMPTY,label=record['id']+':U'),old['baseline'] if old else None)
    minima=[]
    if F(base['value'])==0:
        for index,mask in enumerate(lp.TRIPLES):
            c=solve(lp.make_spec(moments,lp.incidence(mask),cover=True,label=record['id']+':T'+str(mask)),
                old['cover_triple_minima'][index]['certificate'] if old else None)
            minima.append(dict(mask=mask,speeds=[v for i,v in enumerate(record['residual_speeds']) if mask>>i&1],certificate=c))
    counterpart=F(base['value'])==0 and all(F(t['certificate']['value'])==0 for t in minima)
    out={**record,'baseline':base,'cover_triple_minima':minima,'collective_only_counterpart':counterpart,
         'diagnostic_only':{'actual_triples':{m:record['moments'][m] for m in lp.TRIPLES},
          'actual_four_way':record['moments'][15],
          'actual_H':sum(record['moments'][m] for m in lp.TRIPLES)-record['moments'][15]},
         'lp_count':1+len(minima)}
    out=lp.serialize(out)
    if old is not None:
        assert out==old
    return out


def verify_controls(protocol):
    control=load_module('archived_controls',CONTROL_SOURCE)
    path=ROOT/protocol['controls']['source']; data=json.loads(path.read_text())
    assert digest(CONTROL_SOURCE)==data['primary_sha256']
    cp=json.loads(control.PROTOCOL.read_text())
    assert digest(control.PROTOCOL)==data['protocol_sha256']
    assert [c['name'] for c in data['cases']]==protocol['controls']['names']
    result=[]
    for c,p in zip(data['cases'],cp['controls']):
        control.run_case(p,c)  # Exact archived certs; no optimization and no writes.
        result.append(dict(name=c['name'],baseline=c['baseline']['value'],
            cover_triple_minima=[t['certificate']['value'] for t in c['cover_triples']],
            outcome=c['outcome']))
    return {'archive_sha256':digest(path),'primary_sha256':digest(CONTROL_SOURCE),'cases':result}


def build(old=None):
    protocol=json.loads(PROTOCOL.read_text()); contract=protocol['source_contract']
    for key in ('archive','reconstruction','source_protocol'):
        assert digest(ROOT/contract[key])==contract[key+'_sha256']
    archive=json.loads((ROOT/contract['archive']).read_text())
    assert archive['totals']['positive_actual_tree_misses']==18
    selected,locators=reconstruct_selected(archive)
    records=[evaluate(r,old['cases'][i] if old else None) for i,r in enumerate(selected)]
    grouped={}
    for r in records:
        key=(r['case_id'],*r['window'])
        grouped.setdefault(key,[]).append(r['id'])
    duplicates=[ids for ids in grouped.values() if len(ids)>1]
    # Reflection repeats are retained in the frozen domain, but not presented
    # as separate physical mechanisms or independent samples.
    reflection_groups=[]; seen=set()
    for r in records:
        if r['id'] in seen:
            continue
        a,b=map(F,r['window'])
        peers=[s for s in records if s['case_id']==r['case_id']
               and s['core_labels']==r['core_labels']
               and list(map(F,s['window']))==[1-b,1-a]]
        assert len(peers)==1 and peers[0]['id']!=r['id']
        peer=peers[0]
        assert r['moments']==peer['moments'] and r['atoms']==peer['atoms']
        assert r['collective_only_counterpart']==peer['collective_only_counterpart']
        ids=[r['id'],peer['id']]; seen.update(ids)
        reflection_groups.append(dict(record_ids=ids,collective_only_counterpart=r['collective_only_counterpart']))
    assert len(reflection_groups)==9 and len(seen)==18
    out=dict(baseline=protocol['baseline'],protocol_sha256=digest(PROTOCOL),primary_sha256=digest(Path(__file__)),
        source_contract=contract,lp_helper_sha256=digest(LP_SOURCE),locator_checks=locators,cases=records,
        controls=verify_controls(protocol),
        summary=dict(records=len(records),distinct_configuration_window_pairs=len(grouped),
            duplicate_configuration_window_groups=duplicates,
            reflection_pair_count=len(reflection_groups),reflection_groups=reflection_groups,
            collective_only_reflection_pair_count=sum(g['collective_only_counterpart'] for g in reflection_groups),
            pair_only_positive=sum(F(r['baseline']['value'])>0 for r in records),
            pair_only_zero=sum(F(r['baseline']['value'])==0 for r in records),
            collective_only_counterparts=sum(r['collective_only_counterpart'] for r in records),
            baseline_lp_count=len(records),cover_triple_lp_count=sum(len(r['cover_triple_minima']) for r in records),
            lp_count=sum(r['lp_count'] for r in records),logical_states_per_lp=16,
            locator_component_count=sum(x['components_reconstructed'] for x in locators)),
        scope='18 labelled archived positive tree-missed records at reference0; no new windows or speed search; physical higher moments are diagnostic only; abstract LP covers need not be runner-realizable')
    out=lp.serialize(out)
    if old is not None:
        assert out==old
    return out


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');a=p.parse_args()
    data=build(None if a.write else json.loads(OUT.read_text()))
    if a.write:
        OUT.write_text(json.dumps(data,indent=2)+'\n')
    for r in data['cases']:
        print(r['id'],r['window'],'U',r['baseline']['value'],'T minima',
            [t['certificate']['value'] for t in r['cover_triple_minima']],
            'counterpart',r['collective_only_counterpart'])
    print('PASS',data['summary'])


if __name__=='__main__':
    main()
