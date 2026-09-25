"""Fresh exact verifier. No repository imports and no repository writes.
Bounded scope: recorded local schedules/certificates plus 16 constructed
core-endpoint profiles at the claimed cutoffs; no coefficient-box search.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
D=F(1,8)
COUNTS={}
def count(key,n=1): COUNTS[key]=COUNTS.get(key,0)+n
def frac(x): return x%1
def dist(x): return min(frac(x),1-frac(x))
def fl(x): return x.numerator//x.denominator
def ce(x): return -fl(-x)
def rational_intervals(rows): return tuple((F(a),F(b)) for a,b in rows)
def merge(rows):
    result=[]
    for a,b in sorted(rows):
        if result and a<=result[-1][1]: result[-1]=(result[-1][0],max(b,result[-1][1]))
        else: result.append((a,b))
    return tuple(result)
def allowed_region(forms,lo=F(0),hi=F(1)):
    """Direct threshold partition of interval, preserving singleton contacts."""
    cuts={lo,hi}
    for slope,offset in forms:
        assert slope>0
        for m in range(fl(slope*lo+offset)-1,ce(slope*hi+offset)+2):
            for side in (-D,D):
                t=(m+side-offset)/slope
                if lo<=t<=hi: cuts.add(t)
    cuts=sorted(cuts)
    safe=lambda t: all(dist(slope*t+offset)>=D for slope,offset in forms)
    rows=[(t,t) for t in cuts if safe(t)]
    rows += [(a,b) for a,b in zip(cuts,cuts[1:]) if safe((a+b)/2)]
    return merge(rows)
def local_actual(speeds,q,x0,H):
    result=[]
    for j in range(q):
        result.extend(allowed_region([(v,F(0)) for v in speeds],(x0-H+j)/q,(x0+H+j)/q))
    return merge(result)
def certify_interval(speeds,row):
    lo,hi=map(F,row)
    assert lo<hi
    for v in speeds:
        m=fl(v*(lo+hi)/2)
        assert m+D<=v*lo<=v*hi<=m+1-D
        assert dist(v*(lo+hi)/2)>D
    count('stored_strict_interval_certificates')

for name in ('tiling_escape','local_tilings','signed_tilings'):
    data=json.loads((ROOT/'experiments'/f'{name}.json').read_text())
    for path,digest in data['source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,(name,path)
        count('source_hash_checks')
    profiles=data.get('profiles',[])
    if name=='tiling_escape':
        profiles=[{'x0':data['x0'],'H':data['neighborhood_radius'],'terms':[(1,4),(1,12),(2,10),(2,22)],
                   'actual_checks':data['cases'],'frozen_controls':[]}]
        for row in data['frozen_controls']:
            s,h=row['sign'],F(row['h']); f=row['profile']
            exact=allowed_region([(b,a*(F(data['x0'])+s*h)) for b,a in profiles[0]['terms']])
            assert exact==rational_intervals(f['allowed_phases'])
            count('frozen_phase_sets')
    for p in profiles:
        x0,H=F(p['x0']),F(p['H']); terms=[(F(b),F(a)) for b,a in p['terms']]
        for row in p['frozen_controls']:
            h=F(row['h']); s=row['sign']
            assert allowed_region([(b,a*(x0+s*h)) for b,a in terms])==rational_intervals(row['allowed'])
            count('frozen_phase_sets')
        for row in p['actual_checks']:
            q=row['q']; speeds=tuple(row['speeds'])
            complete=row.get('complete',row.get('complete_local_check',False))
            if complete:
                assert local_actual(speeds,q,x0,H)==rational_intervals(row['complete_local_allowed_intervals']),(name,p.get('name'),q)
                count('complete_local_schedule_checks')
            if name=='tiling_escape': certify_interval(speeds,row['closed_time_component'])
            else:
                for cert in row.get('strict_interval_certificates',row.get('certificates',[])):
                    certify_interval(speeds,cert['interval'])
            for c in row.get('classified_contacts',[]):
                t=F(c['contact']); radius=F(1,10**6)
                left=all(dist(v*(t-radius))>D for v in speeds)
                right=all(dist(v*(t+radius))>D for v in speeds)
                assert (left,right)=={'isolated':(False,False),'starts_interval':(False,True),'ends_interval':(True,False)}[c['kind']]
                count('stored_contact_types')

# Independently verify the exact cyclic contacts for new endpoint cases.
def contacts(coefficients,x0):
    b=(1,1,2,2)
    blocks=[]
    for i,(a,rate) in enumerate(zip(coefficients,b)):
        for m in range(rate):
            lo=frac((m-a*x0-D)/rate)
            blocks.append((lo,lo+2*D/rate,F(a,rate),i))
    blocks.sort()
    result=[]
    for k,left in enumerate(blocks):
        right=blocks[(k+1)%6]
        assert left[1]==right[0]+(k==5)
        result.append((frac(left[1]),left[2],right[2]))
    return result

def wedge(low,high,disp,H):
    assert low<high
    points={F(0),H}
    for slope in (low,high):
        if slope:
            h=disp/slope
            if 0<=h<=H: points.add(h)
    points=sorted(points)
    good=[(a,b) for a,b in zip(points,points[1:]) if low*(a+b)/2<disp<high*(a+b)/2]
    assert len(good)<=1
    return good[0] if good else None

core=((F(1,8),F(7,24)),(F(3,8),F(7,16)),(F(9,16),F(5,8)),(F(17,24),F(7,8)))
assert allowed_region([(1,F(0)),(2,F(0)),(3,F(0))])==core
assert min(b-a for a,b in core)==F(1,16)
new_examples=[]; endpoint_contacts=[]
for core_lo,core_hi in core:
    for x0,s in ((core_lo,1),(core_hi,-1)):
        numerator,d=x0.numerator,x0.denominator
        a0=5 if d==16 else 4
        c0=(3*d//8*pow(numerator,-1,d))%d
        c1=(5*d//8*pow(numerator,-1,d))%d
        base=(a0,a0+d//2,2*a0+c0,2*a0+c1)
        for signed in (False,True):
            A=base if not signed else (base[0],base[1]-2*d,base[2],base[3]-3*d)
            assert all(abs(a)>=4 for a in A)
            cs=contacts(A,x0)
            assert sum(L-R for c,L,R in cs)==0
            assert all(L!=R for c,L,R in cs)
            M=max(abs(F(a,b)) for a,b in zip(A,(1,1,2,2)))
            q=17 if signed else 8
            H=1/(16*M+1) if signed else 1/(8*M)
            assert H<core_hi-core_lo
            chosen=[]
            for c,L,R in cs:
                if (1 if L>R else -1)!=s: continue
                for r in (L,R):
                    if abs(r)!=M: continue
                    edge=-s*(r+F(1,q))
                    low,high=-s*(L+F(1,q)),-s*(R+F(1,q))
                    assert (edge==low and edge<0) or (edge==high and edge>0)
                    z=q*c-x0
                    j=fl(z)+1 if edge>0 else ce(z)-1
                    disp=(j-z)/q
                    hp=wedge(low,high,disp,H)
                    assert hp
                    h=(hp[0]+hp[1])/2
                    t=(x0+j+s*h)/q%1
                    speeds=(q,2*q,3*q,*(abs(a)*q+(1 if a>0 else -1)*b for a,b in zip(A,(1,1,2,2))))
                    assert min(dist(v*t) for v in speeds)>D
                    row={'A':A,'x0':x0,'direction':s,'q':q,'H':H,'contact':c,'h_interval':hp,'witness':t,'minimum':min(dist(v*t) for v in speeds)}
                    chosen.append(row)
            assert chosen,(A,x0)
            new_examples.append(chosen[0]);count('core_endpoint_extreme_witnesses')
            # Complete contact residues, one representative q>=17 each. Bounded by d.
            for residue in range(d):
                qc=residue+d*((17-residue+d-1)//d)
                speeds=(qc,2*qc,3*qc,*(abs(a)*qc+(1 if a>0 else -1)*b for a,b in zip(A,(1,1,2,2))))
                for c,L,R in cs:
                    if (qc*c-x0).denominator!=1: continue
                    assert all(dist(v*c)>=D for v in speeds)
                    active=[(v,frac(v*c)) for v in speeds if dist(v*c)==D]
                    assert len(active)==3
                    expected='starts_interval' if all(ph==D for v,ph in active) else 'ends_interval' if all(ph==1-D for v,ph in active) else 'isolated'
                    rad=F(1,1000*max(speeds))
                    near=allowed_region([(v,F(0)) for v in speeds],c-rad,c+rad)
                    wanted={'starts_interval':((c,c+rad),),'ends_interval':((c-rad,c),),'isolated':((c,c),)}[expected]
                    assert near==wanted
                    endpoint_contacts.append({'A':A,'x0':x0,'q':qc,'t':c,'kind':expected,'active':active,'radius':rad,'local_component':near})
                    count('core_endpoint_reachable_contact_classifications')

payload={'counts':COUNTS,'core_safe_set':core,'minimum_core_component_width':F(1,16),'core_endpoint_extreme_witnesses':new_examples,'core_endpoint_contacts':endpoint_contacts}
(OUT/'test_tilings_results.json').write_text(json.dumps(payload,indent=2,default=str)+'\n')
print(json.dumps(COUNTS,indent=2))
for kind in ('starts_interval','ends_interval','isolated'):
    print(kind,next((row for row in endpoint_contacts if row['kind']==kind),None))

# Check the affine cell certificates as continuum certificates, recomputing
# phases from input terms rather than trusting stored vertex phase arrays.
for name in ('tiling_escape','local_tilings','signed_tilings'):
    data=json.loads((ROOT/'experiments'/f'{name}.json').read_text())
    if name=='tiling_escape':
        entries=[(F(data['x0']),F(data['neighborhood_radius']),((1,4),(1,12),(2,10),(2,22)),data['chamber_certificates'])]
    else:
        entries=[(F(p['x0']),F(p['H']),p['terms'],p['chambers']) for p in data['profiles']]
    for x0,H,terms,chambers in entries:
        for chamber in chambers:
            s=chamber['sign']
            for cell in chamber['cells']:
                lines=[tuple(map(F,cell[k])) for k in ('left','right')]
                for h in (F(0),H): assert lines[0][0]+lines[0][1]*h<=lines[1][0]+lines[1][1]*h
                midtau=sum(c+v*H/2 for c,v in lines)/2
                records=cell.get('runner_vertex_certificates',cell.get('certificates'))
                for (b,a),row in zip(terms,records):
                    b,a=F(b),F(a)
                    values=[a*(x0+s*h)+b*(c+v*h) for h in (F(0),H) for c,v in lines]
                    low,high=map(F,row.get('bounds',(row.get('phase_lower_bound'),row.get('phase_upper_bound'))))
                    assert all(low<=v<=high for v in values)
                    assert values==[F(v) for v in row.get('vertices',row.get('vertex_phases'))]
                    blocked=dist(a*(x0+s*H/2)+b*midtau)<D
                    assert blocked==row.get('blocked',row.get('blocked_in_interior'))
                    count('affine_runner_cell_certificates')
                    count('recomputed_vertex_phase_checks',4)

# Check every symbolic winner comparison in the fixed family independently.
data=json.loads((ROOT/'experiments/tiling_escape.json').read_text())
x0=F(data['x0']); cs=contacts((4,12,10,22),x0)
for residue in range(8):
    q=next(q for q in range(5,13) if q%8==residue)
    options=[]
    for c,L,R in cs:
        s=1 if L>R else -1
        z=q*c-x0; j=fl(z) if s>0 else ce(z)
        rho=s*(z-j)
        assert 0<rho<1
        options.append((rho/(max(L,R)*q+1),c,s,rho,max(L,R),min(L,R)))
    winning=min(options)
    row=data['residue_certificates'][residue]['winner']
    assert (winning[1],winning[2],16*winning[3],winning[4],winning[5])==(F(row['contact']),row['sign'],row['mismatch_numerator'],row['A'],row['B'])
    _,c,s,rho,A,B=winning
    for other in options:
        if other==winning: continue
        slope=other[3]*A-rho*other[4]; constant=other[3]-rho
        assert slope>=0 and 5*slope+constant>0
        count('fixed_family_unbounded_winner_comparisons')
payload['counts']=COUNTS
(OUT/'test_tilings_results.json').write_text(json.dumps(payload,indent=2,default=str)+'\n')
print('Additional continuum and symbolic checks:',json.dumps(COUNTS,indent=2))

# Four named endpoint contacts, including a core constraint killing the
# auxiliary interval. Reconstruct each complete time schedule once.
selected=[((4,-8,11,-11),F(1,8),21,F(5,8)),
          ((5,-19,20,-32),F(7,16),23,F(1,16)),
          ((4,8,11,13),F(1,8),17,F(1,8)),
          ((4,-32,23,-55),F(7,24),35,F(5,24))]
full_examples=[]
for A,x0,q,t in selected:
    speeds=(q,2*q,3*q,*(abs(a)*q+(1 if a>0 else -1)*b for a,b in zip(A,(1,1,2,2))))
    complete=allowed_region([(v,F(0)) for v in speeds])
    component=next((a,b) for a,b in complete if a<=t<=b)
    full_examples.append({'A':A,'x0':x0,'q':q,'speeds':speeds,'contact':t,'complete_component':component})
    count('new_core_boundary_full_schedules')
payload['counts']=COUNTS;payload['core_boundary_full_examples']=full_examples
(OUT/'test_tilings_results.json').write_text(json.dumps(payload,indent=2,default=str)+'\n')
print('Complete endpoint examples:',json.dumps(full_examples,indent=2,default=str))
