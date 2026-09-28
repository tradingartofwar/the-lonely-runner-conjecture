#!/usr/bin/env python3
"""Post-protocol analytic counterexamples, including one common-start lift.

No searches or threshold enumeration: direct22/23projection traces and a
seven-open-interval covering certificate. Exact rational arithmetic only.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
D=F(1,8)
ORDER=[0,1,2,3,2,3,1,2,3,2,3,0,1,2,3,2,3,1,2,3,2,3]


def dist(x):
    p=x%1
    return min(p,1-p)


def project(v,alpha,t):
    x=v*t+alpha-1+D
    m=-((-x.numerator)//x.denominator)
    out=max(t,(m+D-alpha)/v)
    assert 0<=out-t<2*D/v and dist(v*out+alpha)>=D
    return out


def case_record(name,speeds,phases,anchor,local_phases,core=()):
    a,b,c,d=speeds
    L=anchor+(-D-local_phases[0])/a
    R=anchor+(1+D-local_phases[3])/d
    for v,alpha,p in zip(speeds,phases,local_phases):
        assert (v*anchor+alpha)%1==p
    t=L
    trace=[]
    for idx in ORDER:
        old=t
        t=project(speeds[idx],phases[idx],t)
        trace.append({'runner':idx,'input':str(old),'output':str(t)})
    assert t==R
    margins=[dist(v*t+alpha)-D for v,alpha in zip(speeds,phases)]
    assert margins[0]<0 and all(m>=0 for m in margins[1:])
    # These exact open intervals cover the whole CLOSED supplied window.
    chain=[]
    for idx,k in ((2,0),(0,0),(3,0),(1,1),(2,1),(3,1),(0,1)):
        v=speeds[idx]
        lo=anchor+(k-D-local_phases[idx])/v
        hi=anchor+(k+D-local_phases[idx])/v
        assert dist(v*lo+phases[idx])==dist(v*hi+phases[idx])==D
        assert dist(v*(lo+hi)/2+phases[idx])==0
        chain.append({'runner':idx,'relative_meeting_label':k,'left':str(lo),'right':str(hi)})
    assert F(chain[0]['left'])<L
    assert F(chain[-1]['right'])>R
    overlaps=[]
    for u,v in zip(chain,chain[1:]):
        assert F(u['left'])<F(v['left'])
        overlap=min(F(u['right']),F(v['right']))-max(F(u['left']),F(v['left']))
        assert overlap>0
        overlaps.append(str(overlap))
    later=project(a,phases[0],t)
    assert later>R
    assert later==F(chain[-1]['right'])
    later_distances=[dist(v*later+alpha) for v,alpha in zip(speeds,phases)]
    assert min(later_distances)>=D
    core_cert=[]
    for v in core:
        mid=v*(L+later)/2
        lap=mid.numerator//mid.denominator
        p,q=v*L-lap,v*later-lap
        assert D<p<=q<1-D
        core_cert.append({'speed':v,'lap':lap,'phase_left':str(p),'phase_later':str(q)})
    s=anchor+(D-local_phases[0])/a
    assert R-s>F(3,4)/a
    condition_bound=F(1,4)/b+F(1,2)/c+1/d
    assert condition_bound>F(3,4)/a
    return {'id':name,'speeds':list(map(str,speeds)),'phases':list(map(str,phases)),
            'anchor':str(anchor),'anchor_phases':list(map(str,local_phases)),
            'core':list(core),'window':[str(L),str(R)],'trace':trace,
            'final_time':str(t),'final_safe':False,'final_margins':list(map(str,margins)),
            'condition_bound':str(condition_bound),'slow_safe_width':str(F(3,4)/a),
            'fresh_slow_safe_entry':str(s),'last_triple_wait':str(R-s),
            'window_verdict':'empty_by_open_cover','cover_chain':chain,
            'adjacent_strict_overlaps':overlaps,'later_witness_step23':str(later),
            'extended_window':[str(L),str(later)],'extended_window_has_witness':True,
            'later_residual_distances':list(map(str,later_distances)),
            'core_safe_through_later_witness':core_cert}


def calculate():
    common_tail=[F(925,1056),F(127,220),F(1,8)]
    eq_v=[F(1),F(1),F(6,5),F(33,20)]
    eq_ph=[F(97,352)]+common_tail
    eq=case_record('aux_equal',eq_v,eq_ph,F(0),eq_ph)
    v=[F(127,128),F(1),F(6,5),F(33,20)]
    ph=[F(12363,45056)]+common_tail
    distinct=case_record('aux_distinct',v,ph,F(0),ph)
    M,P=675840,225281
    N=640*M*10**6
    inverse=pow(P,-1,M)
    assert all((M*x).denominator==1 for x in ph)
    residues=[int(M*x)*inverse%M for x in ph]
    assert all((N*x).denominator==1 for x in v)
    U=[int(N*x)+r for x,r in zip(v,residues)]
    assert len(set([0,1,4,5]+U))==8 and U==sorted(U)
    anchor=F(P,M)
    lifted=case_record('common_start_lift',list(map(F,U)),[F(0)]*4,anchor,ph,(1,4,5))
    assert F(9,32)<F(lifted['window'][0])<F(lifted['later_witness_step23'])<F(3,8)
    return {'status':'pass','provenance':'post-protocol analytic constructions; no scan',
            'construction':{'M':M,'P':P,'N':N,'residues':residues,
                            'integer_full_configuration':[0,1,4,5]+U},
            'cases':[eq,distinct,lifted],
            'meaning':'Unconditional22projection completeness fails, including one common-start eight-runner input. The conditional theorem and guarded diagnostic are intact.'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    result=calculate()
    target=HERE/'follow_on.json'
    if args.check:
        assert json.loads(target.read_text())==result
    else:
        target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','fixed_constructions':len(result['cases']),
                      'common_start_velocities':result['construction']['integer_full_configuration'],
                      'all22step_results_unsafe':True,'all_windows_covered':True,
                      'all_step23_witnesses_safe':True}))


if __name__=='__main__':
    main()
