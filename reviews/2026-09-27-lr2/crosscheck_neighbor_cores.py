"""Independent standard-library audit of neighbor_cores.json.

Uses blocking-interval intersections and Boolean inversion for moments/states,
event vertices and cells for closed feasibility, and Kruskal for best trees.
No import from the experiment, LP helper, or project checker.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent;SOURCE=HERE/'neighbor_cores.json';D=Q(1,8)
EDGES=list(combinations(range(4),2));MASKS=[m for m in range(16) if m.bit_count()<=2]


def dist(x):
    p=x%1
    return min(p,1-p)


def blocks(v,a,b):
    low=(v*a-D).__ceil__();high=(v*b+D).__floor__()
    result=[]
    for lap in range(low,high+1):
        l=max(a,(lap-D)/v);r=min(b,(lap+D)/v)
        if l<r:result.append((l,r))
    return result


def overlap(a,b):
    # Independently use the Cartesian interval formula; cases are deliberately small.
    return sorted((max(l,u),min(r,v)) for l,r in a for u,v in b if max(l,u)<min(r,v))


def measure(a):return sum((r-l for l,r in a),Q(0))


def allowed(speeds):
    events={Q(0),Q(1)}
    for v in speeds:
        for lap in range(v+1):
            for sign in (-1,1):
                t=(lap+sign*D)/v
                if 0<=t<=1:events.add(t)
    events=sorted(events)
    pieces=[(t,t) for t in events if all(dist(v*t)>=D for v in speeds)]
    pieces.extend((a,b) for a,b in zip(events,events[1:]) if all(dist(v*(a+b)/2)>D for v in speeds))
    merged=[]
    for a,b in sorted(pieces):
        if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(merged[-1][1],b))
        else:merged.append((a,b))
    return merged


def kruskal(weights):
    parts=[{i} for i in range(4)];total=Q(0)
    for (i,j),w in sorted(zip(EDGES,weights),key=lambda p:-p[1]):
        a=next(s for s in parts if i in s);b=next(s for s in parts if j in s)
        if a is not b:parts.remove(a);parts.remove(b);parts.append(a|b);total+=w
    assert len(parts)==1
    return total


def decode(intervals):return [tuple(map(Q,ab)) for ab in intervals]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    data=json.loads(SOURCE.read_text());assert data['threshold']=='1/8' and data['pair_mask_order']==MASKS
    assert [c['y'] for c in data['cases']]==[44,45,46]
    assert data['source_sha256']==sha256((HERE/'check_neighbor_cores.py').read_bytes()).hexdigest()
    fixed=(1,4,5,6,7,11);rows=[];count=0;loss_windows=0
    for case in data['cases']:
        y=case['y'];speeds=(*fixed,y);full=allowed(speeds)
        assert full==decode(case['full_allowed']) and measure(full)==Q(case['global_duration'])
        t=Q(case['global_witness']);ds=[dist(v*t) for v in speeds]
        assert ds==list(map(Q,case['witness_distances'])) and min(ds)>D
        assert [tuple(c['core']) for c in case['cores']]==[(1,5,6),(1,4,6)]
        for core in case['cores']:
            expected=allowed(core['core']);assert expected==[tuple(map(Q,x['window'])) for x in core['components']]
            assert core['extras']==[v for v in speeds if v not in core['core']]
            for cell in core['components']:
                a,b=map(Q,cell['window']);bs=[blocks(v,a,b) for v in core['extras']]
                moments=[]
                for m in range(16):
                    pieces=[(a,b)]
                    for i in range(4):
                        if m>>i&1:pieces=overlap(pieces,bs[i])
                    moments.append(measure(pieces))
                assert moments==list(map(Q,cell['moments']))
                masses=[sum(((-1)**(m.bit_count()-s.bit_count())*moments[m] for m in range(16) if m&s==s),Q(0)) for s in range(16)]
                assert masses==list(map(Q,cell['state_masses'])) and min(masses)>=0
                clipped=[(max(a,l),min(b,r)) for l,r in full if max(a,l)<=min(b,r)]
                assert clipped==decode(cell['allowed_components'])
                assert measure(clipped)==masses[0]==Q(cell['actual_duration'])
                weights=[moments[(1<<i)|(1<<j)] for i,j in EDGES]
                tree=b-a-sum(moments[1<<i] for i in range(4))+kruskal(weights)
                assert tree==Q(cell['tree_bound'])
                cert=cell['pair_minimum'];p=list(map(Q,cert['primal']));d=list(map(Q,cert['dual']))
                assert cert['sense']=='min' and len(p)==16 and len(d)==11 and min(p)>=0
                for m in MASKS:assert sum(p[s] for s in range(16) if s&m==m)==moments[m]
                for s in range(16):assert sum(c*int(s&m==m) for c,m in zip(d,MASKS))<=int(s==0)
                bound=sum(c*moments[m] for c,m in zip(d,MASKS))
                assert bound==p[0]==Q(cert['value'])
                assert tree<=bound<=masses[0]
                loss_windows+=bool(masses[0]>0 and bound==0)
                if 'wing_spill' in cell:
                    ws=decode(data['geometry']['wing_intervals'])
                    pieces=[blocks(y,l,r) for l,r in ws]
                    assert pieces==[decode(z) for z in cell['wing_blocked']]
                    spill=sum((measure(z) for z in pieces),Q(0))
                    assert spill==Q(cell['wing_spill'])==masses[13]+masses[14]
                    assert bound==Q(cell['cycle_value'])==masses[0]-spill
                if 'exact_star_bound' in cell:
                    s=tuple(map(Q,data['geometry']['fixed_opening']))
                    assert blocks(y,*s)==decode(cell['blocked_in_opening'])
                    assert masses[0]==(s[1]-s[0])-measure(blocks(y,*s))==Q(cell['exact_star_bound'])
                    assert Q(cell['tail_lower_bound'])==Q(3,448)-Q(3,16*y)>0
                count+=1
            assert sum(Q(c['tree_bound'])>0 for c in core['components'])==core['positive_tree_windows']
            assert sum(Q(c['pair_minimum']['value'])>0 for c in core['components'])==core['positive_pair_windows']
            assert sum(Q(c['actual_duration'])>0 for c in core['components'])==core['positive_actual_windows']
        rows.append({'y':y,'global_duration':case['global_duration'],
                     'old_positive_tree_windows':case['cores'][0]['positive_tree_windows'],
                     'new_positive_tree_windows':case['cores'][1]['positive_tree_windows']})
    # Conditional Boolean identities for the symbolic explanation, independent
    # of numerical y. Here bits are old residuals (4,7,11,y).
    cycle=data['cycle_dual'];old_valid=0;new_valid=0
    for s in range(16):
        a,b,c,d=[(s>>i)&1 for i in range(4)]
        score=sum(k*int(s&m==m) for k,m in zip(cycle,MASKS))
        assert score<=int(s==0)
        if (not(a and b) or c) and (not c or a or b):
            assert int(s==0)-score==int(d and c and not(a and b));old_valid+=1
        # New residuals (5,7,11,y): 5 empty, 11 contained in 7.
        if a==0 and c<=b:
            star=1-a-b-c-d+a*b+b*c+b*d
            assert star==int(s==0);new_valid+=1
    assert old_valid==12 and new_valid==6
    # Periodic primitive correction is affine between these exact vertices.
    def primitive(z):
        whole=z.numerator//z.denominator;r=z-whole
        return Q(whole,4)+min(r,D)+max(Q(0),r-(1-D))
    vertices=(Q(0),D,1-D,Q(1))
    values=[primitive(z)-z/4 for z in vertices]
    assert values==[Q(0),Q(3,32),-Q(3,32),Q(0)]
    assert max(values)-min(values)==Q(3,16)
    assert count==48 and loss_windows==8
    result={'baseline':data['baseline'],'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'archive_sha256':sha256(SOURCE.read_bytes()).hexdigest(),
            'method':'Interval-intersection moments and Boolean inversion, event-cell closed components, Kruskal, rational primal/dual substitution',
            'components_checked':count,'exact_lp_certificates':count,'positive_actual_zero_pair_bound_windows':loss_windows,
            'conditional_old_states':old_valid,'conditional_new_states':new_valid,
            'primitive_vertices':list(map(str,vertices)),'primitive_corrections':list(map(str,values)),
            'cases':rows,'limits':'Three exact inputs, one reference, two cores. Boolean identities and primitive vertices support the separately written general argument; no generic selection theorem or novelty claim.'}
    out=HERE/'neighbor_cores_crosscheck.json';encoded=json.dumps(result,indent=2)+'\n'
    if args.write:out.write_text(encoded)
    else:assert json.loads(encoded)==json.loads(out.read_text())
    print('PASS: 48 components and exact LP optima; all full allowed sets; 8 genuine local pair-data failures; structural Boolean identities and primitive range.')


if __name__=='__main__':main()
