"""Independent bounded verification for the early-family Ultra review.
Run from any directory; imports no repository checker or experiment helpers.
"""
from fractions import Fraction as F
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
D=F(1,8)
def read(s): return json.loads((R/'experiments'/f'{s}.json').read_text())
def dist(v,t):
    z=(v*t)%1
    return min(z,1-z)
def point(V,t): return min(dist(v,t) for v in V)
def interval(V,a,b):
    assert a<b
    for v in V:
        j=(v*a).__floor__()
        assert j+D<=v*a<v*b<=j+1-D

def allowed(V):
    # Independent complete status-boundary partition; singleton boundaries retained.
    cuts=sorted({F(0),F(1)}|{(F(j)+s*D)/v for v in V for j in range(v+1) for s in (-1,1) if 0<=(F(j)+s*D)/v<=1})
    bits=[(x,x) for x in cuts if point(V,x)>=D]
    bits += [(a,b) for a,b in zip(cuts,cuts[1:]) if point(V,(a+b)/2)>=D]
    merged=[]
    for a,b in sorted(bits):
        if merged and a<=merged[-1][1]: merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else: merged.append((a,b))
    return merged

def decode(rows): return [(F(a),F(b)) for a,b in rows]
T=read('two_variable_speeds'); core=tuple(T['scope']['fixed_speeds'])
assert [r['x'] for r in T['slow_speed_table']]==[x for x in range(1,34) if x not in core]
res=[]
for row in T['slow_speed_table']:
    x=row['x']; a,b=map(F,row['interval']); interval((*core,x),a,b)
    cap=F(1,4)/(b-a)
    assert cap==F(row['strict_upper_bound_on_y'])
    ys=[y for y in range(x+1,(cap.numerator-1)//cap.denominator+1) if y not in core and (x%8==0 or y%8==0)]
    assert ys==row['candidate_y']; res.extend((x,y) for y in ys)
assert res==[(r['x'],r['y']) for r in T['residual_pairs']]
for row in T['residual_pairs']:
    V=(*core,row['x'],row['y']); t=F(row['witness']['time'])
    assert point(V,t)==F(row['witness']['minimum'])>D
assert F(T['fast_case']['clear_duration_lower_bound'])==F(5,448)-F(3,16)*(F(1,34)+F(1,34))>0
assert allowed((*core,11,13))==[(F(j,8),F(j,8)) for j in (1,3,5,7)]
V=read('variable_speed_family'); core1=tuple(V['scope']['core_relative_speeds'])
a,b=F(V['certified_interval']['left']),F(V['certified_interval']['right']); interval(core1,a,b)
for row in V['prescribed_examples']:
    w=row['w']; t=F(1,8) if w%8 else a if w%56 else a+F(1,8*w)
    assert t==F(row['time']) and point((*core1,w),t)==D
E=read('eight_runner_replacement')
assert allowed(E['core_relative_speeds'])==decode(E['core_closed_allowed_intervals'])
B=read('blocking_chains')
for case in B['cases']:
    speeds=case['relative_speeds']; A=allowed(speeds)
    assert A==decode(case['allowed_intervals'])
    count=0
    for comp in case['components']:
        left,right=map(F,comp['blocked_component'])
        windows=[((F(j)-D)/v,(F(j)+D)/v) for v in speeds for j in range(2*v+1) if (F(j)+D)/v>left and (F(j)-D)/v<right]
        # Breadth-first reachability of windows, rather than greedy selection or DAG order.
        layer={i for i,(a,b) in enumerate(windows) if a==left}
        seen=set(layer); length=1
        while not any(windows[i][1]==right for i in layer):
            nxt={j for i in layer for j,(a,b) in enumerate(windows) if a<windows[i][1]<b}-seen
            assert nxt
            seen|=nxt; layer=nxt; length+=1
        assert length==comp['minimum_chain_length']; count+=length
        chain=comp['chain']; prev=left
        for idx,w in enumerate(chain):
            a,b=map(F,w['open_interval'])
            assert a==(F(w['meeting'])-D)/w['speed'] and b==(F(w['meeting'])+D)/w['speed']
            assert a==left if idx==0 else a<prev
            assert b>prev; prev=b
        assert prev==right
    assert count==case['minimum_cover_windows']
    for row in case['sole_blocker_witnesses']:
        t=F(row['time']); omitted=row['omitted_speed']
        assert dist(omitted,t)<D<point([v for v in speeds if v!=omitted],t)
O=read('blocking_overlaps')
for case in O['cases']:
    speeds=case['relative_speeds']
    assert allowed(speeds)==decode(case['allowed_intervals'])
    hist={i:F(0) for i in range(8)}
    cuts=sorted({F(0),F(1)}|{(F(j)+s*D)/v for v in speeds for j in range(v+1) for s in (-1,1) if 0<(F(j)+s*D)/v<1})
    pairtotal=F(0)
    for a,b in zip(cuts,cuts[1:]):
        n=sum(dist(v,(a+b)/2)<D for v in speeds); hist[n]+=b-a; pairtotal+=(b-a)*n*(n-1)/2
    assert hist[0]==F(case['safe_duration'])
    assert sum(max(i-1,0)*d for i,d in hist.items())==F(case['extra_blocking_duration'])==F(3,4)+hist[0]
    assert pairtotal==F(case['summed_pair_overlap'])
print('PASS: 28 affine interval certificates; exact residual set of 8 pairs; all 8 direct residual witnesses; fast-bound arithmetic; 9 one-variable witnesses including large w; replacement core full allowed set; 8 chain cases, 46 component minima, 21 sole blockers; 7 full blocking schedules/accounting identities. No repository checker imported; no tracked files written.')
