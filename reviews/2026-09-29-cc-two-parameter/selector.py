#!/usr/bin/env python3
"""Two fixed segments, primitive compatibility, and exact physical recovery.

Run from any directory; JSON goes to stdout. No optimizer or parameter scan.
The proof of universal coverage is in the companion note, not this control run.
"""
from fractions import Fraction as F
from math import gcd, floor, ceil
import json

ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))
CONTROLS = ((1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
            (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10))

def bezout(a,b):
    """Return r,s with ra+sb=gcd(a,b), charging every Euclid division."""
    old_r,r,old_s,s,old_t,t,steps = a,b,1,0,0,1,0
    while r:
        k=old_r//r
        old_r,r=r,old_r-k*r
        old_s,s=s,old_s-k*s
        old_t,t=t,old_t-k*t
        steps+=1
    return old_s,old_t,steps

def phases(speeds,t):
    return [v*t-floor(v*t) for v in speeds]

def select(p,q):
    if not isinstance(p,int) or not isinstance(q,int) or p<=0 or q<=0:
        raise ValueError('p,q must be positive integers')
    d=gcd(p,q)
    P,Q=p//d,q//d
    lower,upper=F(3*(Q-P),8),F(4*Q-P,8)
    h=ceil(lower)
    segment='P3'; tests=1
    if h<=upper:
        x=F(8*h+9*P,8*(Q+2*P)); y=F(9,8)-2*x
        m=(0,0,0,1,1,1,2)
        assert F(3,8)<=x<=F(1,2)
    else:
        segment='P1'; tests=2
        assert (P,Q) in ((1,2),(1,4))
        lower,upper=F(Q-4*P,8),F(5*Q-6*P,24)
        h=ceil(lower)
        assert h<=upper
        x=F(8*h+7*P,8*(Q+3*P)); y=F(7,8)-3*x
        m=(0,0,0,0,0,1,1)
        assert F(1,8)<=x<=F(5,24)
    assert Q*x-P*y==h
    r,s,steps=bezout(P,Q)
    assert r*P+s*Q==1
    T=r*x+s*y; N=floor(T); tau=T-N; t=tau/d
    speeds=[a*p+b*q for a,b in ROWS]
    fractional=phases(speeds,t)
    laps=[mi+(-a*s+b*r)*h-(a*P+b*Q)*N for (a,b),mi in zip(ROWS,m)]
    ambient=[a*x+b*y-mi for (a,b),mi in zip(ROWS,m)]
    assert 0<t<F(1,d)
    assert all(F(1,8)<=f<=F(7,8) for f in fractional)
    assert min(min(f,1-f) for f in fractional)==F(1,8)
    assert fractional==ambient
    assert laps==[floor(v*t) for v in speeds]
    alternate_T=(r+Q)*x+(s-P)*y
    assert alternate_T-floor(alternate_T)==tau
    reflected=phases(speeds,1-t)
    assert reflected==[1-f for f in fractional]
    assert [floor(v*(1-t)) for v in speeds]==[v-1-ell for v,ell in zip(speeds,laps)]
    return dict(p=p,q=q,gcd=d,primitive=[P,Q],distinct_speeds=p!=q,
                segment=segment,tests=tests,interval=[lower,upper],h=h,
                point=[x,y],torus_laps=m,bezout=[r,s],euclid_divisions=steps,
                unwrapped_clock=T,N=N,primitive_time=tau,time=t,speeds=speeds,
                phases=fractional,physical_laps=laps,reflected_time=1-t,
                reflected_phases=reflected)

def main():
    records=[select(p,q) for p,q in CONTROLS]
    negatives=[]
    for name,x,y in [('failed_protocol_fixture',F(7,16),F(1,4)),
                     ('corrected_nonprimitive_fixture',F(13,32),F(5,16))]:
        raw=4*x-2*y; normalized=2*x-y
        fs=[a*x+b*y-mi for (a,b),mi in zip(ROWS,(0,0,0,1,1,1,2))]
        assert all(F(1,8)<=f<=F(7,8) for f in fs)
        negatives.append(dict(name=name,p=2,q=4,point=[x,y],raw_orbit=raw,
                              primitive_orbit=normalized,phases=fs,
                              raw_integral=raw.denominator==1,
                              actual_orbit=normalized.denominator==1))
    assert negatives[0]['raw_integral'] is False
    assert negatives[1]['raw_integral'] is True
    assert negatives[1]['actual_orbit'] is False
    wrong={}
    for j,label in enumerate(('x','y')):
        failures=[]
        for rec in records:
            bad=phases(rec['speeds'],rec['point'][j])
            minimum=min(min(f,1-f) for f in bad)
            if minimum<F(1,8):
                failures.append(dict(pair=[rec['p'],rec['q']],wrong_time=rec['point'][j],minimum=minimum))
        wrong[label]=failures
    report=dict(status='PASS',scope='18 fixed pairs; 17 distinct-speed configurations and one repeated-speed auxiliary',
                records=records,negative_controls=negatives,wrong_clock_failures=wrong,
                counts=dict(controls=len(records),direct_phase_checks=7*len(records),
                            reflected_phase_checks=7*len(records),alternate_bezout_checks=len(records)),
                limit='Universal coverage follows from the accompanying proof candidate, not these finite controls.')
    print(json.dumps(report,default=lambda o:str(o) if isinstance(o,F) else o,indent=2)+'\n',end='')

if __name__=='__main__':
    main()
