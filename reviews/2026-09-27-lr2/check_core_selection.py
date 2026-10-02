"""Exhaust all 35 labelled cores on eleven prescribed eight-runner controls.

Exact integer interval intersections and prefix integrals; no project imports.
--write generates per-configuration archives. Default/--check replays them.
The separate crosscheck_core_selection.py uses a threshold-event state sweep.
"""
from bisect import bisect_right
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = HERE / 'core_selection'
BASELINE = '5c6e7dee3fd096101e5ce759b4a0c84838d0a932'
CASES = [
    ('tree16', (0,1,4,5,6,7,11,16)),
    ('contact13', (0,1,4,5,6,7,11,13)),
    ('moment45', (0,1,4,5,6,7,11,45)),
    ('moment90', (0,1,4,5,6,7,11,90)),
    ('gcd266', (0,1,4,5,6,7,11,266)),
    ('gcd532', (0,1,4,5,6,7,11,532)),
    ('cycle112', (0,1,4,5,56,64,72,112)),
    ('cycle113', (0,1,4,5,56,64,72,113)),
    ('local1680', (0,1,3,4,5,10,28,1680)),
    ('local3360', (0,1,3,4,5,10,28,3360)),
    ('consecutive', tuple(range(8))),
]
CORES = list(combinations(range(7),3))
EDGES = list(combinations(range(4),2))


def trees():
    answer=[]
    for chosen in combinations(range(6),3):
        seen={0}
        for _ in range(4):
            for e in chosen:
                i,j=EDGES[e]
                if i in seen or j in seen: seen.update((i,j))
        if len(seen)==4: answer.append(chosen)
    assert len(answer)==16
    return answer


TREES = trees()


def intersect(a,b):
    result=[];i=j=0
    while i<len(a) and j<len(b):
        lo=max(a[i][0],b[j][0]);hi=min(a[i][1],b[j][1])
        if lo<=hi: result.append((lo,hi))
        if a[i][1]<b[j][1]:i+=1
        elif b[j][1]<a[i][1]:j+=1
        else:i+=1;j+=1
    return result


class Integral:
    def __init__(self,pieces):
        self.pieces=[(a,b) for a,b in pieces if a<b]
        self.starts=[a for a,b in self.pieces]
        self.prefix=[0]
        for a,b in self.pieces:self.prefix.append(self.prefix[-1]+b-a)
    def at(self,t):
        i=bisect_right(self.starts,t)-1
        if i<0:return 0
        a,b=self.pieces[i]
        return self.prefix[i]+min(t,b)-a
    def on(self,a,b):return self.at(b)-self.at(a)


def q(x,d):return str(F(x,d))


def distance(v,t,d):
    p=v*t%d
    return min(p,d-p)


def digest_row(hasher,a,b,bound,actual,d):
    hasher.update((','.join(q(x,d) for x in (a,b,bound,actual))+'\n').encode())


def run_reference(velocities,ref):
    labels=[i for i in range(8) if i!=ref]
    speeds=[abs(velocities[i]-velocities[ref]) for i in labels]
    assert gcd(*speeds)==1  # All prescribed configurations contain adjacent 0,1.
    L=lcm(*speeds);d=8*L
    safe={};blocks={};single={}
    for v in set(speeds):
        unit=L//v
        safe[v]=[((8*j+1)*unit,(8*j+7)*unit) for j in range(v)]
        blocks[v]=[(0,unit)]+[((8*j-1)*unit,(8*j+1)*unit) for j in range(1,v)]+[((8*v-1)*unit,d)]
        single[v]=Integral(blocks[v])
    pair={}
    for i,j in combinations(range(7),2):
        a,b=sorted((speeds[i],speeds[j]))
        if (a,b) not in pair:pair[a,b]=Integral(intersect(blocks[a],blocks[b]))
    full=[(0,d)]
    for v in sorted(set(speeds)):full=intersect(full,safe[v])
    actual=Integral(full)
    full_duration=actual.prefix[-1]
    assert full, 'An empty result needs independent investigation, never silent acceptance.'
    strict=[ab for ab in full if ab[0]<ab[1]]
    global_piece=max(strict,key=lambda ab:ab[1]-ab[0]) if strict else full[0]
    t=F(sum(global_piece),2*d)
    distances=[min(v*t%1,1-v*t%1) for v in speeds]
    assert min(distances)>=F(1,8)
    assert (min(distances)>F(1,8))==bool(strict)
    core_rows=[];winner=None
    total_components=total_positive=positive_cores=0
    for core in CORES:
        windows=[(0,d)]
        for i in sorted(core,key=lambda i:speeds[i]): windows=intersect(windows,safe[speeds[i]])
        extras=[i for i in range(7) if i not in core]
        vs=[speeds[i] for i in extras]
        integrals=[pair[tuple(sorted((vs[i],vs[j])))] for i,j in EDGES]
        rows=[];digest=sha256();best=None;smallest=None
        positive=positive_actual=isolated=0;actual_sum=0
        for a,b in windows:
            ds=[single[v].on(a,b) for v in vs]
            os=[obj.on(a,b) for obj in integrals]
            weights=[sum(os[e] for e in tree) for tree in TREES]
            ti=max(range(16),key=lambda t:weights[t])
            bound=b-a-sum(ds)+weights[ti]
            u=actual.on(a,b)
            assert bound<=u
            if a==b:assert bound==u==0
            positive+=bound>0;positive_actual+=u>0;isolated+=a==b;actual_sum+=u
            digest_row(digest,a,b,bound,u,d)
            if smallest is None or bound<smallest:smallest=bound
            if best is None or bound>best['bound']:
                best=dict(window=(a,b),bound=bound,actual=u,singles=ds,pairs=os,tree=ti)
        assert actual_sum==full_duration
        assert best is not None
        total_components+=len(windows);total_positive+=positive;positive_cores+=positive>0
        core_rows.append([len(windows),isolated,positive,positive_actual,q(smallest,d),q(best['bound'],d),
                          [q(x,d) for x in best['window']],best['tree'],digest.hexdigest()])
        if winner is None or best['bound']>winner['bound']:
            winner={**best,'core':core,'extras':extras}
    assert len(core_rows)==35
    a,b=winner['window']
    cert={'core_runner_indices':[labels[i] for i in winner['core']],
          'core_absolute_speeds':[speeds[i] for i in winner['core']],
          'extra_runner_indices':[labels[i] for i in winner['extras']],
          'extra_absolute_speeds':[speeds[i] for i in winner['extras']],
          'window':[q(a,d),q(b,d)],'bound':q(winner['bound'],d),'actual_duration':q(winner['actual'],d),
          'single_durations':[q(x,d) for x in winner['singles']],
          'pair_durations':[q(x,d) for x in winner['pairs']],
          'tree_edge_indices':list(TREES[winner['tree']])}
    if winner['bound']>0:
        surviving=intersect([(a,b)],full)
        piece=max(surviving,key=lambda ab:ab[1]-ab[0])
        wt=F(sum(piece),2*d)
        wd=[min(v*wt%1,1-v*wt%1) for v in speeds]
        assert min(wd)>F(1,8)
        cert.update(witness=str(wt),witness_distances=list(map(str,wd)))
    return {'reference_index':ref,'reference_velocity':velocities[ref],
            'constraint_runner_indices':labels,'absolute_speeds':speeds,
            'distinct_absolute_speeds':len(set(speeds)),
            'full_duration':q(full_duration,d),'full_positive_components':len(strict),
            'full_singletons':[q(a,d) for a,b in full if a==b],
            'full_components_sha256':sha256(json.dumps([[q(a,d),q(b,d)] for a,b in full],separators=(',',':')).encode()).hexdigest(),
            'global_witness':str(t),'global_witness_distances':list(map(str,distances)),
            'core_component_count':total_components,'positive_certificate_components':total_positive,
            'successful_cores':positive_cores,'strict_all_core_failure':bool(strict) and winner['bound']<=0,
            'best_certificate':cert,'core_rows':core_rows}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true')
    ap.add_argument('--case',choices=[x[0] for x in CASES]);args=ap.parse_args()
    if args.write:DEST.mkdir(exist_ok=True)
    selected=[x for x in CASES if args.case is None or x[0]==args.case]
    for name,velocities in selected:
        references=[]
        for ref in range(8):
            row=run_reference(velocities,ref);references.append(row)
            print(name,ref,'distinct',row['distinct_absolute_speeds'],'U',row['full_duration'],
                  'cores',row['successful_cores'],'best',row['best_certificate']['bound'],flush=True)
        result={'case':name,'velocities':velocities,'baseline':BASELINE,'n':8,'threshold':'1/8',
                'scope':'All eight labelled references; all 35 labelled three-runner cores; every complete core-safe component on [0,1]. Duplicate absolute constraints retained; no speed normalization needed.',
                'status':'OBSERVED exact finite experiment; no general selection theorem or novelty claim',
                'core_order':CORES,'extra_edge_order':EDGES,'tree_order':TREES,
                'core_row_columns':['component_count','singleton_count','positive_bound_count','positive_actual_count','minimum_bound','maximum_bound','first_maximizing_window','first_maximizing_tree_index','component_digest'],
                'digest_format':'Increasing components, each line reduced fractions a,b,best_tree_bound,actual_duration followed by newline.',
                'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'references':references}
        dest=DEST/(name+'.json');encoded=json.dumps(result,indent=2)+'\n'
        if args.write:dest.write_text(encoded)
        else:assert json.loads(encoded)==json.loads(dest.read_text()),name+' archive drift'
    print('PASS:',len(selected),'prescribed configurations; archive '+('written' if args.write else 'replayed read-only'))


if __name__=='__main__':main()
