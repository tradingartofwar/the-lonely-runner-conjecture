"""Exact pair-only repair of the single failed strict core in the named controls.

No project imports or optimizer required. The optimum was discovered using the
existing Ultra LP helper, then preserved as a rational primal/dual certificate.
This script independently partitions the eight core components and checks it.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
CORE=(1,5,6);EXTRAS=(4,7,11,45);D=F(1,8)
MOMENT_MASKS=[m for m in range(16) if m.bit_count()<=2]
DUAL=[1,-1,-1,0,-1,1,1,-1,1,1,-1]
PRIMAL=list(map(F,['1/1260','61/1980','62/3465','0','0','1/154','1/352','79/10080',
                  '41/5040','1/180','1/630','0','0','0','0','1/180']))
EXPECTED_WINDOWS=[('1/8','7/48'),('9/40','5/16'),('17/48','3/8'),('17/40','23/48'),
                  ('25/48','23/40'),('5/8','31/48'),('11/16','31/40'),('41/48','7/8')]


def dist(x):
    p=x%1
    return min(p,1-p)


def points(speeds,a,b):
    cuts={a,b}
    for v in speeds:
        for j in range(v):
            for phase in (D,1-D):
                t=(j+phase)/v
                if a<=t<=b:cuts.add(t)
    return sorted(cuts)


def windows():
    cuts=points(CORE,F(0),F(1));pieces=[]
    pieces.extend((t,t) for t in cuts if all(dist(v*t)>=D for v in CORE))
    pieces.extend((a,b) for a,b in zip(cuts,cuts[1:]) if all(dist(v*(a+b)/2)>D for v in CORE))
    result=[]
    for a,b in sorted(pieces):
        if result and a<=result[-1][1]:result[-1]=(result[-1][0],max(result[-1][1],b))
        else:result.append((a,b))
    assert result==[tuple(map(F,w)) for w in EXPECTED_WINDOWS]
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    # Universal validity: the affine combination of pair indicators lies below
    # the uncovered indicator in each of the 16 possible Boolean states.
    for s in range(16):
        assert sum(c*int(s&m==m) for c,m in zip(DUAL,MOMENT_MASKS))<=int(s==0)
    records=[];edges=list(combinations(range(4),2));trees=[]
    for chosen in combinations(edges,3):
        reached={0}
        for _ in range(4):
            for i,j in chosen:
                if i in reached or j in reached:reached.update((i,j))
        if len(reached)==4:trees.append(chosen)
    assert len(trees)==16
    for a,b in windows():
        cuts=points(EXTRAS,a,b);masses=[F(0)]*16
        for lo,hi in zip(cuts,cuts[1:]):
            t=(lo+hi)/2;s=sum(1<<i for i,v in enumerate(EXTRAS) if dist(v*t)<D)
            masses[s]+=hi-lo
        moments=[sum(masses[s] for s in range(16) if s&m==m) for m in range(16)]
        tree=(b-a)-sum(moments[1<<i] for i in range(4))+max(sum(moments[(1<<i)|(1<<j)] for i,j in tr) for tr in trees)
        record={'window':list(map(str,(a,b))),'tree_bound':str(tree),'actual_duration':str(masses[0]),
                'state_masses':list(map(str,masses)),'moments':list(map(str,moments))}
        if masses[0]:
            value=sum(c*moments[m] for c,m in zip(DUAL,MOMENT_MASKS))
            assert value==F(1,1260) and tree==-F(1,1260) and masses[0]==F(1,210)
            assert min(PRIMAL)>=0
            for m in MOMENT_MASKS:assert sum(PRIMAL[s] for s in range(16) if s&m==m)==moments[m]
            assert PRIMAL[0]==value
            record.update(pair_minimum=str(value),primal=list(map(str,PRIMAL)),dual=DUAL)
        else:assert tree==0
        records.append(record)
    archive=json.loads((HERE/'core_selection/moment45.json').read_text())
    r=archive['references'][0]
    row=next(row for c,row in zip(archive['core_order'],r['core_rows']) if [r['absolute_speeds'][i] for i in c]==list(CORE))
    digest=sha256()
    for rec in records:
        digest.update((','.join([*rec['window'],rec['tree_bound'],rec['actual_duration']])+'\n').encode())
    assert digest.hexdigest()==row[8]
    # An explicit successful changed-core certificate and strict witness.
    best=r['best_certificate']
    assert best['core_absolute_speeds']==[1,4,6] and best['bound']=='1/210'
    assert best['window']==['9/32','5/16'] and best['witness']=='257/840'
    assert min(dist(v*F(best['witness'])) for v in (*CORE,*EXTRAS))>D
    out={'baseline':'5c6e7dee3fd096101e5ce759b4a0c84838d0a932','status':'OBSERVED exact fixed control; no novelty claim',
         'velocities':[0,1,4,5,6,7,11,45],'reference':0,'core':CORE,'extras':EXTRAS,'threshold':str(D),
         'moment_mask_order':MOMENT_MASKS,
         'inequality':'U >= L - D4 - D7 - D11 - D45 + O4,11 + O7,11 + O4,45 + O7,45 - O11,45',
         'proof':'16 Boolean inequalities establish the dual lower bound. A nonnegative 16-state primal matches every single/pair moment and attains it, proving optimality in the abstract moment relaxation.',
         'physical_realizability_limit':'The optimizer primal is an abstract event-mass distribution, not a claimed second constant-speed runner realization.',
         'components':records,'changed_core_certificate':best,
         'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':sha256((HERE/'core_selection/moment45.json').read_bytes()).hexdigest()}
    encoded=json.dumps(out,indent=2)+'\n';dest=HERE/'core_selection_repair.json'
    if args.write:dest.write_text(encoded)
    else:assert json.loads(encoded)==json.loads(dest.read_text())
    print('PASS: eight failed-core components; two exact positive pair-only optima; all 16 Boolean dual checks; rational primal; changed-core witness.')


if __name__=='__main__':main()
