"""Exact orbit-aligned sources, built from p,q before any r is used."""
from collections import Counter
from fractions import Fraction as F
from math import ceil, floor, gcd

BASE=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(6,2),(3,8))
D=F(1,8)
COUNTS=Counter()


def speeds(p,q):return [a*p+b*q for a,b in BASE]


def encode(value):
    if isinstance(value,F):return str(value)
    raise TypeError(type(value).__name__)


def safe(vs,t):
    COUNTS['direct_phase_predicates']+=1
    return all(D<=(v*t)%1<=1-D for v in vs)


def source_core(P,Q):
    """Complete core set via boundary events and exact midpoint predicates."""
    assert gcd(P,Q)==1 and min(P,Q)>0
    vs=speeds(P,Q)
    assert len(set([0]+vs))==9
    if sum(vs)>600:raise RuntimeError('SCOPE_LIMIT: core phase events')
    events=sorted({F(0),F(1)}|{(F(j)+x)/v for v in vs for j in range(v) for x in (D,1-D)})
    if len(events)>1202:raise RuntimeError('SCOPE_LIMIT: distinct events')
    COUNTS['core_builds']+=1;COUNTS['core_events']+=len(events)
    pieces=[[t,t] for t in events if safe(vs,t)]
    pieces += [[l,u] for l,u in zip(events,events[1:]) if safe(vs,(l+u)/2)]
    union=[]
    for l,u in sorted(pieces):
        if union and l<=union[-1][1]:union[-1][1]=max(union[-1][1],u)
        else:union.append([l,u])
    if len(union)>600:raise RuntimeError('SCOPE_LIMIT: core components')
    components=[]
    for i,(l,u) in enumerate(union):
        midpoint=(l+u)/2
        physical_laps=[floor(v*midpoint) for v in vs]
        pair_laps=[floor(P*midpoint),floor(Q*midpoint)]
        endpoints=[[P*t-pair_laps[0],Q*t-pair_laps[1]] for t in (l,u)]
        torus_laps=[lap-a*pair_laps[0]-b*pair_laps[1] for (a,b),lap in zip(BASE,physical_laps)]
        for t in (l,u):
            assert all(D<=v*t-lap<=1-D for v,lap in zip(vs,physical_laps))
        for x,y in endpoints:
            assert all(D<=a*x+b*y-lap<=1-D for (a,b),lap in zip(BASE,torus_laps))
        components.append({'id':i,'interval':[l,u],'width':u-l,'dimension':0 if l==u else 1,
            'xy_endpoints':endpoints,'pair_laps':pair_laps,'core_physical_laps':physical_laps,
            'torus_laps':torus_laps})
    order=sorted(range(len(components)),key=lambda i:(-components[i]['width'],components[i]['interval'][0]))
    positive=sum(c['width']>0 for c in components)
    kind=('EMPTY' if not components else 'ISOLATED_ONLY' if positive==0
          else 'POSITIVE_ONLY' if positive==len(components) else 'MIXED')
    return {'pair':[P,Q],'classification':kind,'components':components,'order':order,
            'primary':order[0] if order else None,'event_count':len(events)}


def clock(v):
    g=gcd(*v);A,B,C=(x//g for x in v);d=gcd(A,B)
    return {'g':g,'A':A,'B':B,'C':C,'d':d,'P':A//d,'Q':B//d}


def first_band(L,U,C):
    """Earliest point of [L,U] in any closed C-safe band, or None."""
    assert L<=U and C>0
    band=ceil(C*L-(1-D))
    tau=max(L,(band+D)/C)
    if tau>U:return None
    assert tau<=(band+1-D)/C
    return tau,band


def component_hit(v,core,index):
    """First safe band in each physical clock lift; includes singleton input."""
    c=clock(v);assert core['pair']==[c['P'],c['Q']]
    component=core['components'][index];l,u=component['interval']
    COUNTS['component_queries']+=1
    for lift in range(c['d']):
        COUNTS['lift_queries']+=1
        if COUNTS['lift_queries']>1000000:raise RuntimeError('SCOPE_LIMIT: total lift queries')
        L,U=(l+lift)/c['d'],(u+lift)/c['d']
        hit=first_band(L,U,c['C'])
        if hit is None:continue
        tau,band=hit
        t=tau/c['g'];s=c['d']*tau-lift
        vs=speeds(v[0],v[1])+[v[2]]
        phases=[(speed*t)%1 for speed in vs]
        assert all(D<=phase<=1-D for phase in phases)
        xy=[c['P']*s-component['pair_laps'][0],c['Q']*s-component['pair_laps'][1]]
        assert phases[:2]==xy and l<=s<=u
        return {'component':index,'lift':lift,'core_clock':s,'tau':tau,'time':t,
                'r_band':band,'xy':xy,'phases':phases,
                'physical_laps':[floor(speed*t) for speed in vs],
                'guarantee':('MULTIPLE_LIFTS' if c['d']>=2 else
                             'INTERVAL_WIDTH' if c['C']*(u-l)>=F(1,4) else 'EXACT_CONTACT')}
    return None


def evaluate(v,core):
    results={i:component_hit(v,core,i) for i in core['order']}
    primary=core['primary']
    chosen={'widest':primary if primary is not None and results[primary] else None,
            'all_components':next((i for i in core['order'] if results[i]),None),
            'positive_only':next((i for i in core['order'] if core['components'][i]['width']>0 and results[i]),None)}
    c=clock(v)
    if primary is not None:
        width=core['components'][primary]['width']
        if c['d']>=2 or c['C']*width>=F(1,4):assert chosen['widest'] is not None
    return {'pqr':list(v),'clock':c,'core_class':core['classification'],
            'component_bits':''.join('1' if results[i] else '0' for i in range(len(results))),
            'selected':chosen,'witnesses':{str(i):results[i] for i in sorted({i for i in chosen.values() if i is not None})}}
