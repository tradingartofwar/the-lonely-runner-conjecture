"""Independent exact review. No imports from the reviewed repository; no writes there.

Maximum oracle: a positive local maximum of a minimum of nonconstant triangular
curves occurs at opposite-slope equality, hence at t=n/(v+w), allowing v=w.
Boundary oracle: certify all threshold cells and points using affine phases.
Only stored cases, exhaustive specified finite remainders, and prescribed
auxiliary profiles are checked; this is not an unbounded search.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product, combinations
from pathlib import Path
from collections import Counter
import hashlib, json

ROOT=Path(__file__).resolve().parents[2]
D=F(1,8)
COUNTS=Counter()
FULL_CACHE={}
MAX_CACHE={}

def norm(t):
    r=t%1
    return min(r,1-r)

def distance(v,t):
    return norm(v*t)

def merge(seq):
    out=[]
    for a,b in sorted(seq):
        if out and a<=out[-1][1]: out[-1]=(out[-1][0],max(out[-1][1],b))
        else: out.append((a,b))
    return tuple(out)

def union(terms):
    # Each term is signed integer slope + exact intercept. Safe sets are closed.
    cuts={F(0),F(1)}
    for v,c in terms:
        l,h=sorted((c,c+v))
        for j in range(l.numerator//l.denominator-1,h.numerator//h.denominator+2):
            for sign in (-1,1):
                t=(j+sign*D-c)/v
                if 0<=t<=1: cuts.add(t)
    cuts=sorted(cuts)
    def good(t): return all(norm(v*t+c)>=D for v,c in terms)
    out=[(t,t) for t in cuts if good(t)]
    out.extend((a,b) for a,b in zip(cuts,cuts[1:]) if good((a+b)/2))
    return merge(out)

def actual_union(vs):
    key=tuple(vs)
    if key not in FULL_CACHE: FULL_CACHE[key]=union([(v,F(0)) for v in vs])
    return FULL_CACHE[key]

def maximum(vs):
    key=tuple(sorted(vs))
    if key in MAX_CACHE: return MAX_CACHE[key]
    numer,denom=0,1
    peaks=set()
    for den in sorted({a+b for a,b in combinations_with_replacement(vs,2)}):
        for num in range(1,den):
            residues=[num*v%den for v in vs]
            lower=min(min(r,den-r) for r in residues)
            comparison=lower*denom-numer*den
            if comparison>0:
                numer,denom=lower,den
                peaks={F(num,den)}
            elif comparison==0: peaks.add(F(num,den))
    result=(F(numer,denom),tuple(sorted(peaks)))
    MAX_CACHE[key]=result
    return result

def check_max(row,vs):
    result=maximum(vs)
    assert result==(F(row['maximum']),tuple(map(F,row['all_maximizing_times']))), (vs,result)
    COUNTS['complete_maximum_and_peak_records']+=1

def check_summary(vs, summary):
    result=actual_union(vs)
    expected_hash=summary.get('sha256_json_string_endpoints')
    if expected_hash:
        actual=hashlib.sha256(json.dumps(result,default=str).encode()).hexdigest()
        assert actual==expected_hash,(vs,actual,expected_hash)
    duration=sum((b-a for a,b in result),F(0))
    if 'clear_duration' in summary: assert duration==F(summary['clear_duration'])
    if 'duration' in summary: assert duration==F(summary['duration'])
    if 'components' in summary: assert len(result)==summary['components']
    if 'positive_components' in summary: assert sum(a<b for a,b in result)==summary['positive_components']
    for key in ('isolated','isolated_components'):
        if key in summary: assert sum(a==b for a,b in result)==summary[key]
    COUNTS['full_allowed_union_records']+=1
    return result

def strict(vs, time, interval, stated_distances):
    t=F(time); a,b=map(F,interval)
    assert 0<a<t<b<1
    assert min(distance(v,t) for v in vs)>D
    assert {str(v):str(distance(v,t)) for v in vs}==stated_distances
    for v in vs:
        left,right=v*a,v*b
        integer=left.numerator//left.denominator
        assert integer==right.numerator//right.denominator
        assert D<left-integer<right-integer<1-D
    COUNTS['strict_point_and_interval_records']+=1

def check_grids(q,vs,rows):
    for g in rows:
        x=F(g['core_phase']); threshold=F(g.get('threshold','1/8'))
        times=[(x+j)/q for j in range(q)]
        bad=[[j for j,t in enumerate(times) if distance(v,t)<threshold] for v in vs[-4:]]
        if 'runners' in g:
            extras=vs[-2:]
            bad=[[j for j,t in enumerate(times) if distance(v,t)<threshold] for v in extras]
            assert bad==[r['blocked_indices'] for r in g['runners']]
        else:
            expected=g.get('blocked_indices',g.get('blocked_indices_by_runner'))
            assert bad==expected
        good=[j for j,t in enumerate(times) if min(distance(v,t) for v in vs)>=threshold]
        assert good==g.get('survivors',g.get('surviving_indices'))
        strict_indices=[j for j,t in enumerate(times) if min(distance(v,t) for v in vs)>threshold]
        assert strict_indices==g.get('strict_survivors',g.get('strict_surviving_indices'))
        COUNTS['actual_grid_records']+=1
        COUNTS['actual_grid_choices']+=q

def read(name): return json.loads((ROOT/'experiments'/f'{name}.json').read_text())

scaled=read('scaled_perturbation')
for c in scaled['cases']:
    vs=c['relative_speeds']; q,s=c['q'],c['s']
    assert vs==list(range(q,7*q,q))+[7*q+s]
    check_max(c,vs); full=check_summary(vs,c['allowed_summary'])
    for classification,times in c['old_touch_classification'].items():
        for ts in times:
            t=F(ts)
            segment=next(((a,b) for a,b in full if a<=t<=b),None)
            actual='blocked' if segment is None else 'isolated' if segment[0]==segment[1] else 'opens_right' if segment[0]==t else 'opens_left' if segment[1]==t else 'interior'
            assert actual==classification
            COUNTS['old_touch_classifications']+=1
    old={F(8*j+r,8*q) for j in range(q) for r in (1,3,5,7)}
    new=sorted(a for a,b in full if a==b and a not in old)
    assert new==[F(r['time']) for r in c['new_isolated_contacts']]
    if 'strict_witness' in c:
        w=c['strict_witness']; strict(vs,w['time'],w['interval'],w['distances'])

for name in ('two_perturbations','four_perturbations'):
    d=read(name)
    for c in d['cases']:
        vs=c['relative_speeds']
        check_max(c,vs);check_summary(vs,c['allowed_summary'])
        check_grids(c['q'],vs,c['grids'])
        if 'strict_witness' in c:
            w=c['strict_witness'];strict(vs,w['time'],w['interval'],w['distances'])
    if name=='four_perturbations':
        keys={(c['q'],tuple(c['signs'])) for c in d['cases'] if c['q']<7}
        assert keys==set(product(range(3,7),product((-1,1),repeat=4)))
        COUNTS['four_unit_remainder_cases']=len(keys)
        c=d['unchanged_control'];vs=c['speeds']
        assert actual_union(vs)==tuple(tuple(map(F,ab)) for ab in c['complete_allowed_set'])
        assert maximum(vs)[0]==D
        COUNTS['full_allowed_union_records']+=1
        COUNTS['complete_maximum_and_peak_records']+=1
        for p in d['phase_profiles']:
            x=F(p['core_phase']); terms=[(s,k*x) for k,s in zip(range(4,8),p['signs'])]
            assert union(terms)==tuple(tuple(map(F,ab)) for ab in p['allowed_phases'])
            COUNTS['complete_auxiliary_profile_records']+=1

for name,start,double_count,profile_key,expected_counts in (
    ('unequal_perturbations',4,1,'profiles',{3:8,4:32,5:12,6:8,7:2,9:2}),
    ('two_doubled_offsets',5,2,'families',{4:28,5:32,6:32,9:4})):
    d=read(name); rows=d[profile_key]
    vectors={tuple(s*(2 if k in doubled else 1) for k,s in zip(range(4,8),signs))
             for doubled in combinations(range(4,8),double_count) for signs in product((-1,1),repeat=4)}
    assert len(rows)==len(vectors) and {tuple(r['offsets']) for r in rows}==vectors
    assert Counter(r['sufficient_q'] for r in rows)==expected_counts
    expected_remainder={(q,tuple(r['offsets'])) for r in rows for q in range(start,r['sufficient_q'])}
    actual_remainder={(c['q'],tuple(c['offsets'])) for c in d['cases'] if c['finite_remainder']}
    assert actual_remainder==expected_remainder
    COUNTS[name+'_exhaustive_remainder_cases']=len(expected_remainder)
    for r in rows:
        offsets=r['offsets']; pp=r['profiles']
        for p in pp:
            x=F(p['core_phase']); terms=[(a,k*x) for k,a in zip(range(4,8),offsets)]
            complete=union(terms)
            assert complete==tuple(tuple(map(F,ab)) for ab in p['geometry']['allowed_phases'])
            lo,hi=map(F,p['chosen_interval']);w=hi-lo
            assert (lo,hi) in complete and w==max(b-a for a,b in complete)>0
            assert w==F(p['width']) and (lo+hi)/2==F(p['midpoint'])
            assert p['sufficient_q']==(1/w).numerator//(1/w).denominator+1
            # Independent signed affine interval proof.
            for a,c in terms:
                z0,z1=a*lo+c,a*hi+c;integer=z0.numerator//z0.denominator
                assert integer==z1.numerator//z1.denominator
                assert D<=min(z0,z1)-integer<=max(z0,z1)-integer<=1-D
            COUNTS['certified_phase_width_profiles']+=1
            COUNTS['complete_auxiliary_profile_records']+=1
        chosen=min(pp,key=lambda p:(p['sufficient_q'],F(p['core_phase'])))
        assert chosen['core_phase']==r['selected_phase'] and chosen['sufficient_q']==r['sufficient_q']
        if name=='two_doubled_offsets':
            unit=[(1 if a>0 else -1)*k for k,a in zip(range(4,8),offsets) if abs(a)==1]
            delta=unit[1]-unit[0]
            candidates={F(2*j+1,2*abs(delta)) for j in range(abs(delta))}
            records=r['tiling_candidate_check']['checks']
            assert len(records)==len(candidates) and {F(c['core_phase']) for c in records}==candidates
            for c in records:
                x=F(c['core_phase']); u=union([(a,k*x) for k,a in zip(range(4,8),offsets)])
                length=sum((b-a for a,b in u),F(0))
                assert length==F(c['clear_phase_length'])>0
                COUNTS['necessary_tiling_candidate_profiles']+=1
    assert len({(c['q'],tuple(c['offsets'])) for c in d['cases']})==len(d['cases'])
    for c in d['cases']:
        q,offsets=c['q'],c['offsets'];vs=c['speeds']
        assert vs==[q,2*q,3*q]+[k*q+a for k,a in zip(range(4,8),offsets)]
        if name=='unequal_perturbations':
            strict(vs,c['witness'],c['strict_interval'],c['distances'])
            summary=c.get('full_allowed_summary')
        else:
            w=c['certificate'];strict(vs,w['time'],w['strict_interval'],w['distances'])
            assert q*F(w['time'])%1==F(c['witness_core_phase'])
            summary=c.get('complete_allowed_summary')
        if summary: check_summary(vs,summary)
        check_grids(q,vs,c['grids'])
        if 'maximum' in c:check_max(c,vs)
    if name=='two_doubled_offsets':
        c=d['changed_coefficient_control'];vs=c['speeds']
        check_max(c,vs)
        w=c['certificate'];strict(vs,w['time'],w['strict_interval'],w['distances'])
        # Source stores no full control-union hash; verify exact witness is inside full union.
        full=actual_union(vs);assert any(a<=F(w['time'])<=b for a,b in full)
        COUNTS['full_allowed_union_records']+=1
        for p in c['profiles']:
            x=F(p['core_phase']);g=p['geometry']
            assert union([(b,a*x) for b,a in c['terms_b_a']])==tuple(tuple(map(F,ab)) for ab in g['allowed_phases'])
            COUNTS['complete_auxiliary_profile_records']+=1

print(json.dumps({'status':'PASS','counts':COUNTS,'unique_maximum_inputs':len(MAX_CACHE),'unique_actual_union_inputs':len(FULL_CACHE)},indent=2))
