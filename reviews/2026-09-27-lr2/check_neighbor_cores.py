"""Exact 44/45/46 comparison of cores (1,5,6) and (1,4,6).

--write uses the archived Ultra LP helper/SciPy to discover rational bases.
Default/--check requires only the standard library and checks exact archived
primal/dual certificates, physical states, complete components, and geometry.
"""
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=HERE/'neighbor_cores.json'
HELPER=ROOT/'reviews/2026-09-27-ultra/optimization_check.py'
BASELINE='af6d0d6f83cfcf3c15e2573ccedd8d023040384a'
D=F(1,8);YS=(44,45,46);FIXED=(1,4,5,6,7,11)
CORES=((1,5,6),(1,4,6));EDGES=list(combinations(range(4),2))
PAIR_MASKS=[m for m in range(16) if m.bit_count()<=2]
I=(F(9,40),F(5,16));J=(F(9,32),F(5,16));S=(F(17,56),F(5,16))
WINGS=((F(23,88),F(15,56)),(F(9,32),F(25,88)))
CYCLE=[1,-1,-1,0,-1,1,1,-1,1,1,-1]


def distance(x):
    p=x%1
    return min(p,1-p)


def intersect(a,b):
    out=[];i=j=0
    while i<len(a) and j<len(b):
        lo=max(a[i][0],b[j][0]);hi=min(a[i][1],b[j][1])
        if lo<=hi:out.append((lo,hi))
        if a[i][1]<b[j][1]:i+=1
        elif b[j][1]<a[i][1]:j+=1
        else:i+=1;j+=1
    return out


def safe(v):return [((j+D)/v,(j+1-D)/v) for j in range(v)]


def allowed(speeds,window=(F(0),F(1))):
    result=[window]
    for v in speeds:result=intersect(result,safe(v))
    return result


def blocks(v,window):
    a,b=window
    return [(max(a,(j-D)/v),min(b,(j+D)/v)) for j in range(v+1)
            if max(a,(j-D)/v)<min(b,(j+D)/v)]


def length(intervals):return sum((b-a for a,b in intervals),F(0))


def physical(speeds,window):
    a,b=window;cuts={a,b}
    for v in speeds:
        for j in range(v):
            for phase in (D,1-D):
                t=(j+phase)/v
                if a<t<b:cuts.add(t)
    cuts=sorted(cuts);masses=[F(0)]*16
    for lo,hi in zip(cuts,cuts[1:]):
        t=(lo+hi)/2
        state=sum(1<<i for i,v in enumerate(speeds) if distance(v*t)<D)
        masses[state]+=hi-lo
    moments=[sum(masses[s] for s in range(16) if s&m==m) for m in range(16)]
    return masses,moments


def all_trees():
    out=[]
    for es in combinations(range(6),3):
        reached={0}
        for _ in range(4):
            for e in es:
                i,j=EDGES[e]
                if i in reached or j in reached:reached.update((i,j))
        if len(reached)==4:out.append(es)
    assert len(out)==16
    return out


TREES=all_trees()


def pair_spec(moments):
    return {'rows':[[F(int(s&m==m)) for s in range(16)] for m in PAIR_MASKS],
            'rhs':[moments[m] for m in PAIR_MASKS],'forbidden':[]}


def verify_lp(moments,cert):
    primal=list(map(F,cert['primal']));dual=list(map(F,cert['dual']))
    assert cert['sense']=='min' and len(primal)==16 and len(dual)==11 and min(primal)>=0
    for m in PAIR_MASKS:assert sum(primal[s] for s in range(16) if s&m==m)==moments[m]
    for s in range(16):assert sum(c*int(s&m==m) for c,m in zip(dual,PAIR_MASKS))<=int(s==0)
    value=sum(c*moments[m] for c,m in zip(dual,PAIR_MASKS))
    assert value==primal[0]==F(cert['value'])


def geometry():
    a=blocks(4,I);b=blocks(7,I);c=blocks(11,I)
    assert a==[(I[0],F(9,32))] and b==[(F(15,56),F(17,56))]
    assert c==[(F(23,88),F(25,88))]
    ab=intersect(a,b)
    assert ab==[(F(15,56),F(9,32))] and intersect(ab,c)==ab
    assert c[0][0]>=a[0][0] and c[0][1]<=b[0][1] and a[0][1]>=b[0][0]
    assert allowed(FIXED,I)==[S]
    # On the replacement-core window, speed 5 never blocks and 11 is dominated by 7.
    assert J in allowed(CORES[1])
    assert blocks(5,J)==[]
    assert blocks(11,J)==[(J[0],F(25,88))]
    assert blocks(7,J)==[(J[0],S[0])]
    assert intersect(blocks(11,J),blocks(7,J))==blocks(11,J)
    assert allowed(FIXED,J)==[S]
    costs=[int(s==0)-sum(c*int(s&m==m) for c,m in zip(CYCLE,PAIR_MASKS)) for s in range(16)]
    assert all(x>=0 for x in costs)
    assert [(s,x) for s,x in enumerate(costs) if x]==[(3,1),(12,2),(13,1),(14,1)]
    return {'old_window':I,'new_window':J,'fixed_opening':S,'wing_intervals':WINGS,
            'old_fixed_blocks':{'4':a,'7':b,'11':c},'old_AB_intersection':ab,
            'new_fixed_blocks':{str(v):blocks(v,J) for v in (5,7,11)},
            'cycle_slack_by_state':costs,
            'general_identity':'For every admissible positive integer y, the maximum tree bound on J equals U_J=1/112-|B_y intersect S|.',
            'tail_bound':'U_J >= 3/448 - 3/(16*y) > 0 for every integer y>=29.',
            'tail_status':'HYPOTHESIS/proof candidate supported by the containment and primitive-range derivation in the note; not extrapolated from these three controls.'}


def encode(obj):
    if isinstance(obj,F):return str(obj)
    if isinstance(obj,dict):return {k:encode(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [encode(v) for v in obj]
    return obj


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    archived=None;opt=None
    if args.write:
        spec=spec_from_file_location('ultra_pair_lp',HELPER);opt=module_from_spec(spec);spec.loader.exec_module(opt)
    else:archived=json.loads(OUT.read_text())
    geo=geometry();records=[];count=0
    for yi,y in enumerate(YS):
        full=allowed((*FIXED,y));strict=[ab for ab in full if ab[0]<ab[1]]
        assert strict
        ab=max(strict,key=lambda ab:ab[1]-ab[0]);t=sum(ab)/2
        distances=[distance(v*t) for v in (*FIXED,y)];assert min(distances)>D
        row={'y':y,'velocities':[0,*FIXED,y],'reference':0,'full_allowed':full,'global_duration':length(full),
             'global_witness':t,'witness_distances':distances,'cores':[]}
        for ci,core in enumerate(CORES):
            extra=tuple(v for v in (*FIXED,y) if v not in core);windows=allowed(core);local=[]
            assert len(windows)==8
            for wi,window in enumerate(windows):
                masses,mom=physical(extra,window);pair=[mom[(1<<i)|(1<<j)] for i,j in EDGES]
                scores=[sum(pair[e] for e in tr) for tr in TREES];ti=max(range(16),key=lambda i:scores[i])
                tree=mom[0]-sum(mom[1<<i] for i in range(4))+scores[ti]
                cert=opt.certify(pair_spec(mom)) if args.write else archived['cases'][yi]['cores'][ci]['components'][wi]['pair_minimum']
                verify_lp(mom,cert);count+=1
                true=allowed((*FIXED,y),window);assert length(true)==masses[0]
                assert tree<=F(cert['value'])<=masses[0]
                item={'window':window,'state_masses':masses,'moments':mom,'tree_bound':tree,
                      'tree_edges':[EDGES[e] for e in TREES[ti]],'pair_minimum':cert,
                      'actual_duration':masses[0],'allowed_components':true}
                if core==CORES[0] and window==I:
                    cycle=sum(F(c)*mom[m] for c,m in zip(CYCLE,PAIR_MASKS))
                    spill=sum((length(blocks(y,w)) for w in WINGS),F(0))
                    assert cycle==F(cert['value'])==masses[0]-spill
                    assert masses[3]==masses[12]==0
                    assert spill==masses[13]+masses[14]
                    item.update(cycle_value=cycle,wing_spill=spill,wing_blocked=[blocks(y,w) for w in WINGS])
                if core==CORES[1] and window==J:
                    # Star rooted at residual speed 7: edges 5--7, 7--11, 7--y.
                    star=mom[0]-sum(mom[1<<i] for i in range(4))+mom[3]+mom[6]+mom[10]
                    assert star==tree==F(cert['value'])==masses[0]==F(1,112)-length(blocks(y,S))
                    lower=F(3,448)-F(3,16*y);assert 0<lower<=star
                    item.update(exact_star_bound=star,remaining_opening=S,blocked_in_opening=blocks(y,S),tail_lower_bound=lower)
                local.append(item)
            row['cores'].append({'core':core,'extras':extra,'components':local,
                                 'positive_tree_windows':sum(x['tree_bound']>0 for x in local),
                                 'positive_pair_windows':sum(F(x['pair_minimum']['value'])>0 for x in local),
                                 'positive_actual_windows':sum(x['actual_duration']>0 for x in local)})
        records.append(row)
        old=next(x for x in row['cores'][0]['components'] if x['window']==I)
        new=next(x for x in row['cores'][1]['components'] if x['window']==J)
        print(y,'old tree',old['tree_bound'],'old pair',old['pair_minimum']['value'],
              'new exact tree',new['tree_bound'],'wing spill',old['wing_spill'],flush=True)
    result={'baseline':BASELINE,'threshold':D,'scope':'Three fixed inputs y=44,45,46; reference 0; two prescribed cores; all 48 complete core components; no all-reference or additional-speed scan.',
            'status':'OBSERVED / REPRODUCED finite exact evidence; general structural corollary remains a proof candidate; no novelty claim',
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'discovery_helper_sha256':sha256(HELPER.read_bytes()).hexdigest(),
            'pair_mask_order':PAIR_MASKS,'cycle_dual':CYCLE,'geometry':geo,'cases':records,'exact_lp_certificates':count}
    encoded=json.dumps(encode(result),indent=2)+'\n'
    if args.write:OUT.write_text(encoded)
    else:assert json.loads(encoded)==archived
    print('PASS:',count,'exact pair optima; complete physical components; cycle slack; exact replacement-core tree.')


if __name__=='__main__':main()
