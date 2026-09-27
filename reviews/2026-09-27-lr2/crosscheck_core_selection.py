"""Independent reconstruction of all archived core-selection components.

No imports from the primary script or checker. Uses event-state sweeps on a
product-denominator grid, 16-state duration accumulators, and Kruskal trees.
--write saves a compact comparison record; default/--check replays read-only.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import prod
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
NAMES=['tree16','contact13','moment45','moment90','gcd266','gcd532',
       'cycle112','cycle113','local1680','local3360','consecutive']
CORES=list(combinations(range(7),3))
MASKS=[sum(1<<i for i in core) for core in CORES]
EXTRAS=[[i for i in range(7) if i not in core] for core in CORES]
EDGES=list(combinations(range(4),2))
ACTIVE=[[c for c,m in enumerate(MASKS) if not state&m] for state in range(128)]
RESIDUAL=[[sum(((state>>i)&1)<<j for j,i in enumerate(extra)) for state in range(128)] for extra in EXTRAS]


def kruskal(weights):
    roots=list(range(4));answer=0;used=[]
    def root(i):
        while roots[i]!=i:i=roots[i]
        return i
    for e in sorted(range(6),key=lambda e:(-weights[e],e)):
        a,b=EDGES[e];ra,rb=root(a),root(b)
        if ra!=rb:
            roots[ra]=rb;answer+=weights[e];used.append(e)
    assert len(used)==3
    return answer


def serial_fraction(x,d):return str(Q(x,d))


def check_reference(velocities,record):
    ref=record['reference_index']
    labels=[i for i in range(8) if i!=ref]
    speeds=[abs(velocities[i]-velocities[ref]) for i in labels]
    assert labels==record['constraint_runner_indices'] and speeds==record['absolute_speeds']
    assert len(set(speeds))==record['distinct_absolute_speeds']
    # Product rather than lcm grid: same rational instants, different integer coordinates.
    scale=8*prod(set(speeds));events={0:[0,0],scale:[0,0]}
    for i,v in enumerate(speeds):
        unit=scale//(8*v)
        for j in range(v):
            events.setdefault((8*j+1)*unit,[0,0])[0]|=1<<i
            events.setdefault((8*j+7)*unit,[0,0])[1]|=1<<i
    times=sorted(events)
    accum=[[0]*16 for _ in CORES];starts=[None]*35
    stats=[dict(count=0,points=0,positive=0,actual_positive=0,minimum=None,maximum=None,
                digest=sha256(),clear_sum=0,best=None) for _ in CORES]
    full=[];full_start=None
    winner=None

    def finish(c,a,b,masses):
        nonlocal winner
        s=stats[c];length=b-a
        assert sum(masses)==length
        singles=[sum(masses[m] for m in range(16) if m>>i&1) for i in range(4)]
        pairs=[sum(masses[m] for m in range(16) if m>>i&1 and m>>j&1) for i,j in EDGES]
        bound=length-sum(singles)+kruskal(pairs);actual=masses[0]
        assert bound<=actual
        s['digest'].update((','.join(serial_fraction(x,scale) for x in (a,b,bound,actual))+'\n').encode())
        s['count']+=1;s['points']+=a==b;s['positive']+=bound>0;s['actual_positive']+=actual>0;s['clear_sum']+=actual
        if s['minimum'] is None or bound<s['minimum']:s['minimum']=bound
        if s['maximum'] is None or bound>s['maximum']:
            s['maximum']=bound;s['best']=(a,b,singles,pairs,actual)

    before=127
    for idx,t in enumerate(times):
        low,high=events[t]
        point=before&~(low|high)
        after=(before&~low)|high
        # Reconstruct the complete full allowed set, retaining boundary atoms.
        if before==0 and after!=0:
            assert full_start is not None;full.append((full_start,t));full_start=None
        elif before!=0 and after==0:full_start=t
        elif before!=0 and after!=0 and point==0:full.append((t,t))
        for c,mask in enumerate(MASKS):
            was_safe=not before&mask;will_safe=not after&mask
            if was_safe and not will_safe:
                assert starts[c] is not None
                finish(c,starts[c],t,accum[c]);starts[c]=None;accum[c]=[0]*16
            elif not was_safe and will_safe:
                assert starts[c] is None;starts[c]=t
            elif not was_safe and not will_safe and not point&mask:
                finish(c,t,t,[0]*16)
        if idx+1<len(times):
            width=times[idx+1]-t
            for c in ACTIVE[after]:accum[c][RESIDUAL[c][after]]+=width
        before=after
    assert all(x is None for x in starts) and full_start is None
    encoded_full=[[serial_fraction(a,scale),serial_fraction(b,scale)] for a,b in full]
    assert sha256(json.dumps(encoded_full,separators=(',',':')).encode()).hexdigest()==record['full_components_sha256']
    duration=sum(b-a for a,b in full)
    assert serial_fraction(duration,scale)==record['full_duration']
    assert sum(a<b for a,b in full)==record['full_positive_components']
    assert [serial_fraction(a,scale) for a,b in full if a==b]==record['full_singletons']
    for c,s in enumerate(stats):
        r=record['core_rows'][c];a,b,singles,pairs,actual=s['best']
        assert [s['count'],s['points'],s['positive'],s['actual_positive']]==r[:4]
        assert [serial_fraction(s['minimum'],scale),serial_fraction(s['maximum'],scale)]==r[4:6]
        assert [serial_fraction(a,scale),serial_fraction(b,scale)]==r[6]
        assert s['digest'].hexdigest()==r[8],('component mismatch',ref,CORES[c])
        assert s['clear_sum']==duration
        if winner is None or s['maximum']>stats[winner]['maximum']:winner=c
    cert=record['best_certificate'];s=stats[winner];a,b,ds,ps,u=s['best']
    assert cert['core_runner_indices']==[labels[i] for i in CORES[winner]]
    assert cert['core_absolute_speeds']==[speeds[i] for i in CORES[winner]]
    assert cert['extra_runner_indices']==[labels[i] for i in EXTRAS[winner]]
    assert cert['extra_absolute_speeds']==[speeds[i] for i in EXTRAS[winner]]
    assert cert['window']==[serial_fraction(a,scale),serial_fraction(b,scale)]
    assert cert['bound']==serial_fraction(s['maximum'],scale)
    assert cert['actual_duration']==serial_fraction(u,scale)
    assert cert['single_durations']==[serial_fraction(x,scale) for x in ds]
    assert cert['pair_durations']==[serial_fraction(x,scale) for x in ps]
    chosen=cert['tree_edge_indices'];seen={0}
    for _ in range(4):
        for e in chosen:
            i,j=EDGES[e]
            if i in seen or j in seen:seen.update((i,j))
    assert len(set(chosen))==3 and len(seen)==4
    assert sum(ps[e] for e in chosen)==kruskal(ps)
    for obj,key,dk in ((record,'global_witness','global_witness_distances'),(cert,'witness','witness_distances')):
        if key not in obj:continue
        t=Q(obj[key]);ds=[min(((velocities[i]-velocities[ref])*t)%1,1-((velocities[i]-velocities[ref])*t)%1) for i in labels]
        assert list(map(str,ds))==obj[dk]
        assert min(ds)>=Q(1,8)
        if duration or obj is cert:assert min(ds)>Q(1,8)
    total=sum(s['count'] for s in stats);success=sum(s['positive']>0 for s in stats)
    assert total==record['core_component_count']
    assert success==record['successful_cores']
    assert sum(s['positive'] for s in stats)==record['positive_certificate_components']
    assert record['strict_all_core_failure']==bool(duration and not success)
    return {'reference':ref,'components':total,'successful_cores':success,'strict':bool(duration),
            'all_distinct':len(set(speeds))==7,'strict_failure':record['strict_all_core_failure']}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    records=[];hashes={}
    for name in NAMES:
        path=HERE/'core_selection'/(name+'.json');data=json.loads(path.read_text())
        assert data['n']==8 and data['threshold']=='1/8'
        assert data['core_order']==[list(c) for c in CORES]
        assert len(data['references'])==8
        assert sorted(r['reference_index'] for r in data['references'])==list(range(8))
        assert len(data['velocities'])==len(set(data['velocities']))==8
        hashes[str(path.relative_to(HERE))]=sha256(path.read_bytes()).hexdigest()
        rows=[check_reference(data['velocities'],r) for r in data['references']]
        records.append({'case':name,'references':rows})
        print('PASS:',name,'all eight references, all 280 labelled cores',flush=True)
    rows=[r for c in records for r in c['references']]
    out={'baseline':'5c6e7dee3fd096101e5ce759b4a0c84838d0a932',
         'method':'Independent threshold-event state sweep; product grid; 16-state masses; Kruskal trees; direct signed-velocity witness checks',
         'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':hashes,
         'configurations':len(records),'references':len(rows),'labelled_cores':35*len(rows),
         'core_components':sum(r['components'] for r in rows),
         'strict_references':sum(r['strict'] for r in rows),
         'all_distinct_references':sum(r['all_distinct'] for r in rows),
         'strict_all_core_failures':sum(r['strict_failure'] for r in rows),
         'successful_core_choices':sum(r['successful_cores'] for r in rows),'cases':records}
    dest=HERE/'core_selection_crosscheck.json';encoded=json.dumps(out,indent=2)+'\n'
    if args.write:dest.write_text(encoded)
    else:assert json.loads(encoded)==json.loads(dest.read_text())
    print(json.dumps({k:v for k,v in out.items() if k not in ('cases','input_sha256')},indent=2))


if __name__=='__main__':main()
