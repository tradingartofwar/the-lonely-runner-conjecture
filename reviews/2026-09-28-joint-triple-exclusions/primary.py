"""Frozen joint-triple exclusion lattice: 52 exact-certified optimizations.

Numerical LP is solely a certificate proposer in --write. --check is read-only,
uses standard-library rational arithmetic, and verifies all primal/dual pairs,
geometry, preserved cover countermodels, subset minimality and reflection.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys

sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/'protocol.json'
OUT=HERE/'results.json'
FROZEN_SHA='ad4746abe0a7b34ff0e4c63a1a3f1b18fab9ddbdb06a42da702e7a75b9f5db78'
LP_SOURCE=ROOT/'reviews/2026-09-28-collective-obligations/primary.py'
spec=importlib.util.spec_from_file_location('prior_exact_lp_helper',LP_SOURCE)
lp=importlib.util.module_from_spec(spec);spec.loader.exec_module(lp)
TRIPLES=[7,11,13,14]
SUBSETS=[tuple(c) for k in range(5) for c in combinations(TRIPLES,k)]
DELTA=F(1,8)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def intersect(first,second):
    i=j=0;out=[]
    while i<len(first) and j<len(second):
        a=max(first[i][0],second[j][0]);b=min(first[i][1],second[j][1])
        if a<b:
            out.append((a,b))
        if first[i][1]<second[j][1]:
            i+=1
        elif second[j][1]<first[i][1]:
            j+=1
        else:
            i+=1;j+=1
    return out


def geometry(speeds,window):
    a,b=map(F,window);blocks=[]
    for v in speeds:
        pieces=[]
        for j in range(int(v*a)-1,int(v*b)+2):
            left=max(a,(F(j)-DELTA)/v);right=min(b,(F(j)+DELTA)/v)
            if left<right:
                pieces.append((left,right))
        blocks.append(pieces)
    moments=[];intersection_pieces=[]
    for mask in range(16):
        pieces=[(a,b)]
        for i in range(4):
            if mask>>i&1:
                pieces=intersect(pieces,blocks[i])
        moments.append(sum((y-x for x,y in pieces),F(0)))
        intersection_pieces.append(pieces)
    atoms=moments[:]
    for bit in range(4):
        for mask in range(16):
            if not mask>>bit&1:
                atoms[mask]-=atoms[mask|(1<<bit)]
    assert all(x>=0 for x in atoms) and sum(atoms)==b-a
    C=moments[0]-sum(moments[1<<i] for i in range(4))+sum(moments[m] for m in range(16) if m.bit_count()==2)
    H=sum(moments[m] for m in TRIPLES)-moments[15]
    assert atoms[0]+H==C
    return dict(window=[a,b],speeds=speeds,moments=moments,atoms=atoms,blocks=blocks,
        intersection_pieces=intersection_pieces,triples=[moments[m] for m in TRIPLES],Q=moments[15],H=H,C=C,U=atoms[0])


def solve(spec,old=None):
    if old is None:
        return lp.propose_certificate(spec)
    expected=lp.serialize(spec)
    assert {k:old[k] for k in expected}==expected
    lp.verify_certificate(old)
    return old


def triple_speeds(mask,speeds):
    return [v for i,v in enumerate(speeds) if mask>>i&1]


def evaluate(name,physical,old=None):
    moments={m:physical['moments'][m] for m in lp.MOMENT_MASKS}
    speeds=physical['speeds'];chosen_subsets=SUBSETS if name!='doubling_112' else [()]
    assert chosen_subsets==sorted(chosen_subsets,key=lambda s:(len(s),[triple_speeds(m,speeds) for m in s]))
    entries=[]
    for index,subset in enumerate(chosen_subsets):
        s=lp.make_spec(moments,lp.EMPTY,label=name+':triples:'+','.join(map(str,subset)))
        s['le_rows']=[lp.incidence(m) for m in subset]
        s['le_rhs']=[physical['moments'][m] for m in subset]
        s['le_labels']=['inclusive_triple_'+str(m)+'_upper' for m in subset]
        c=solve(s,old['coordinate_subsets'][index]['certificate'] if old else None)
        value=F(c['value'])
        assert F(0)<=value<=physical['U']
        # Verify the real schedule satisfies every offered bound; it provides
        # an exact upper control for the minimum, without entering the LP.
        p=physical['atoms']
        assert all(sum(F(x)*a for x,a in zip(row,p))==rhs for row,rhs in zip(s['eq_rows'],s['eq_rhs']))
        assert all(sum(F(x)*a for x,a in zip(row,p))<=rhs for row,rhs in zip(s['le_rows'],s['le_rhs']))
        proper=[e for e in entries if set(e['masks'])<set(subset)]
        if any(e['positive'] for e in proper):
            assert value>0
        entries.append(dict(masks=list(subset),triples=[triple_speeds(m,speeds) for m in subset],
            ranking_key=[len(subset),[triple_speeds(m,speeds) for m in subset]],
            bounds=[physical['moments'][m] for m in subset],certificate=c,positive=value>0,
            inclusion_minimal=value>0 and all(not e['positive'] for e in proper),
            cover_countermodel=c['primal'] if value==0 else None))
    successful=[e for e in entries if e['positive']]
    minimal=[e['masks'] for e in entries if e['inclusion_minimal']]
    selected=successful[0]['masks'] if successful else None
    collective=None
    if name!='doubling_112':
        s=lp.make_spec(moments,lp.EMPTY,h_upper=physical['H'],label=name+':collective_H')
        collective=solve(s,old['collective'] if old else None)
        assert F(collective['value'])==physical['U']==physical['C']-physical['H']
    out=lp.serialize(dict(name=name,physical=physical,coordinate_subsets=entries,
        inclusion_minimal_successful_subsets=minimal,selected=selected,collective=collective,
        subset_order='Cardinality, then lexicographic list of physical speed triples; never numeric subset-bitmask order',
        counts=dict(coordinate_lps=len(entries),collective_lps=int(collective is not None),
            positive_subsets=len(successful),zero_subsets=len(entries)-len(successful)),
        collective_input_cost=None if collective is None else dict(supplied_scalar_bounds=1,
            present_exact_derivation_inclusive_triples=4,present_exact_derivation_four_way=1,
            new_cheap_geometric_derivation=False)))
    if old is not None:
        assert out==old
    return out


def endpoint_tight():
    t=F(3,8);speeds=[1,4,5,6,7,11,13]
    phases={v:(v*t)%1 for v in speeds}
    distances={v:min(p,1-p) for v,p in phases.items()}
    left=[v for v,p in phases.items() if p==DELTA]
    right=[v for v,p in phases.items() if p==1-DELTA]
    assert all(d>=DELTA for d in distances.values()) and left and right
    return dict(time=t,distances=distances,valid=True,left_neighborhood_blockers=left,
        right_neighborhood_blockers=right,isolated=True)


def abstract_comparison(data):
    source=data['cases'][0];moments={int(m):F(v) for m,v in source['moments'].items()}
    covers=data['main_canonical_cover_models'];diagnostics=[]
    for subset in SUBSETS[:-1]:
        active=next(m for m in TRIPLES if m not in subset)
        p=list(map(F,covers[TRIPLES.index(active)]))
        assert p[0]==0 and all(x>=0 for x in p)
        assert all(sum(a*x for a,x in zip(lp.incidence(m),p))==v for m,v in moments.items())
        assert all(sum(a*x for a,x in zip(lp.incidence(m),p))==0 for m in subset)
        diagnostics.append(dict(zero_triples=list(subset),active_triple=active,
            archived_cover_index=TRIPLES.index(active)))
    return dict(status='Prior abstract comparison, no new optimization or runner-realizability claim',
        proper_zero_subsets=len(diagnostics),witness_references=diagnostics)


def build(old=None):
    assert sha(PROTOCOL)==FROZEN_SHA
    protocol=json.loads(PROTOCOL.read_text());contract=protocol['source_contract'];sources={}
    for key in ('target_results','control_results','abstract_collective_results'):
        path=ROOT/contract[key];assert sha(path)==contract[key+'_sha256'];sources[key]=json.loads(path.read_text())
    target=protocol['target'];physical=geometry(target['residual_speeds'],target['window'])
    assert physical['U']==F(target['actual_uncovered_duration'])
    assert physical['C']==F(target['pair_constant_C']) and physical['H']==F(target['physical_collective_H'])
    assert physical['Q']==F(target['physical_four_way_duration'])
    assert physical['triples']==[F(t['value']) for t in target['physical_inclusive_triple_upper_bounds']]
    archived=next(r for r in sources['target_results']['cases'] if r['id']=='perturbed_chain:1,2,4:4')
    assert physical['moments']==list(map(F,archived['moments'])) and physical['atoms']==list(map(F,archived['atoms']))
    a,b=map(F,target['window']);reflected=geometry(target['residual_speeds'],[1-b,1-a])
    assert reflected['moments']==physical['moments'] and reflected['atoms']==physical['atoms']
    for pieces,ref in zip(physical['intersection_pieces'],reflected['intersection_pieces']):
        assert [(1-b,1-a) for a,b in reversed(pieces)]==ref
    cases={'target':evaluate('target',physical,old['cases']['target'] if old else None)}
    control_records={r['name']:r for r in sources['control_results']['cases']}
    for control in protocol['controls']:
        name=control['name'];p=geometry(control['speeds'],['9/32','3/8'])
        archive=control_records[name]
        assert all(p['moments'][int(m)]==F(v) for m,v in archive['moments'].items())
        cases[name]=evaluate(name,p,old['cases'][name] if old else None)
    assert F(cases['doubling_112']['coordinate_subsets'][0]['certificate']['value'])>0
    assert all(not e['positive'] for e in cases['tight_13']['coordinate_subsets'])
    # U+H=C is an identity on all 16 exact-state columns, not a sampled claim.
    rhs=[sum((1 if m==0 or m.bit_count()==2 else -1)*lp.incidence(m)[state]
             for m in lp.MOMENT_MASKS) for state in range(16)]
    lhs=[lp.EMPTY[state]+lp.H_ROW[state] for state in range(16)]
    assert lhs==rhs
    coordinate_count=sum(c['counts']['coordinate_lps'] for c in cases.values())
    collective_count=sum(c['counts']['collective_lps'] for c in cases.values())
    assert coordinate_count==49 and collective_count==3
    out=lp.serialize(dict(baseline=protocol['baseline'],protocol_sha256=FROZEN_SHA,
        primary_sha256=sha(Path(__file__)),lp_helper_sha256=sha(LP_SOURCE),source_contract=contract,
        cases=cases,target_reflection=reflected,tight_endpoint=endpoint_tight(),
        collective_identity=dict(lhs_U_plus_H_columns=lhs,rhs_C_columns=rhs,
            retained_moment_masks=lp.MOMENT_MASKS,
            retained_moment_coefficients=[1 if m==0 or m.bit_count()==2 else -1 for m in lp.MOMENT_MASKS]),
        prior_abstract_comparison=abstract_comparison(sources['abstract_collective_results']),
        counts=dict(coordinate_lps=coordinate_count,collective_lps=collective_count,total_lps=52,
            logical_states_per_lp=16,physical_windows_reconstructed=5,
            zero_optimum_coordinate_countermodels=sum(c['counts']['zero_subsets'] for c in cases.values())),
        scope='Three subset lattices on existing windows, one pair-only control, target reflection geometry, three collective comparisons; no general selection, novelty, independent validation or runner-realizable cover claim'))
    if old is not None:
        assert out==old
    return out


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');a=p.parse_args()
    data=build(None if a.write else json.loads(OUT.read_text()))
    if a.write:
        OUT.write_text(json.dumps(data,indent=2)+'\n')
    for name,c in data['cases'].items():
        print(name,'minimal',c['inclusion_minimal_successful_subsets'],'selected',c['selected'])
        print('subset optima',[(e['masks'],e['certificate']['value']) for e in c['coordinate_subsets']])
        print('collective',c['collective']['value'] if c['collective'] else None)
    print('PASS',data['counts'])


if __name__=='__main__':
    main()
