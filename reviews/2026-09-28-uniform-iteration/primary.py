"""Constructed exact checks for the uniform-chain proof candidate.

No search and no fitted universal constant. Only protocol inputs are used.
Run from repo root: python reviews/2026-09-28-uniform-iteration/primary.py
"""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = 'f0ddb7b2f82af5e812d1b2c31a012e3119fe90e67d209bf664ea0f2e395f9fa2'


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def endpoint(label, occurrence, right=False):
    # Affine coefficients: four periods followed by four starting offsets.
    out = [F(0)]*8
    out[label] = F(occurrence) + (F(1,4) if right else 0)
    out[4+label] = F(1)
    return out


def cycle_records(tile, periods, starts):
    word, q = tile['word'], tile['q']
    counter = [0]*4
    sequence = []
    for label in word*3:
        sequence.append((label, counter[label]))
        counter[label] += 1
    rows = []
    for anchor in range(4):
        at = word.index(anchor)
        coefficients, gaps = [], []
        for pos in range(at+1, at+len(word)+1):
            a = endpoint(*sequence[pos-1], right=True)
            b = endpoint(*sequence[pos])
            coeff = [x-y for x,y in zip(a,b)]
            coefficients.append(coeff)
            gaps.append(sum((x*y for x,y in zip(coeff,periods+starts)), F(0)))
        total = [sum((c[j] for c in coefficients),F(0)) for j in range(8)]
        expected_coeff = [F(n,4) for n in q] + [F(0)]*4
        expected_coeff[anchor] -= q[anchor]
        assert total == expected_coeff
        expected = sum((F(q[i],4)*periods[i] for i in range(4)),F(0))-q[anchor]*periods[anchor]
        assert sum(gaps,F(0)) == expected
        rows.append(dict(anchor=anchor,q=q,gaps=gaps,sum=sum(gaps,F(0)),expected=expected,
            coefficients=total,identity_ok=True))
    anchor_max = max(range(4),key=lambda i:q[i]*periods[i])
    assert rows[anchor_max]['sum'] <= 0
    assert any(g<=0 for g in rows[anchor_max]['gaps'])
    return rows, anchor_max


def safe(period, start, t):
    phase = ((t-start)/period) % 1
    return not (0 < phase < F(1,4))


def squares(word):
    return [(j,k) for j in range(len(word)) for k in range(1,(len(word)-j)//2+1)
        if word[j:j+k] == word[j+k:j+2*k]]


def selector(periods, starts, L, R):
    order = sorted(range(4),key=lambda i:(-periods[i],i))
    round_order = [order[i] for i in [0,1,2,3,2,3,1,2,3,2,3]]
    trace, moving = [], []
    t, rounds = L, 0
    # Every advance inside [L,R] is a distinct right endpoint. The extra one
    # permits an exit past R; this guard does not assume the uniform theorem.
    local_cap = 11*(sum(ceil((R-L)/p) for p in periods)+5)
    while not all(safe(p,s,t) for p,s in zip(periods,starts)):
        rounds += 1
        for i in round_order:
            old = t
            lap = ceil((t-starts[i])/periods[i]-1)
            t = max(t,starts[i]+(lap+F(1,4))*periods[i])
            moved = t>old
            trace.append(dict(call=len(trace)+1,round=rounds,label=i,before=old,after=t,moved=moved))
            if moved:
                moving.append(i)
            assert len(trace)<=local_cap
            if t>R:
                break
        if t>R:
            break
    repeated = squares(moving)
    assert not repeated
    return order,dict(status='empty' if t>R else 'safe',time=t,calls=len(trace),rounds=rounds,
        trace=trace,moving_labels=moving,nonzero_trace=[x for x in trace if x['moved']],
        square_free=True,squares=repeated)


def main():
    raw=(HERE/'protocol.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==PROTOCOL_SHA
    protocol=json.loads(raw)
    cases=[]
    for tile in protocol['tiles']:
        for change in protocol['perturbations']:
            p=list(map(F,tile['periods']));s=list(map(F,tile['starts']))
            if change['field']:
                (p if change['field']=='periods' else s)[change['runner']]+=F(change['delta'])
            cycles,max_anchor=cycle_records(tile,p,s)
            order,sel=selector(p,s,*map(F,protocol['window']))
            cases.append(dict(tile=tile['id'],perturbation=change['id'],periods=p,starts=s,order=order,
                earliest=sel['time'] if sel['status']=='safe' else None,selector=sel,cycles=cycles,
                maximal_cycle_anchor=max_anchor))
    occupancy=[]
    for row in protocol['occupancy_fixtures']:
        x=F(row['x']);phase=F(row['phase']);m=floor(x);r=x-m
        f=F(m,4)+max(F(0),r-F(3,4))
        assert x>=1 and f>=x/7
        occupancy.append(dict(x=x,phase=phase,formula=f,x_over_7=x/7))
    data=dict(status='pass',protocol_sha256=PROTOCOL_SHA,
        primary_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases,occupancy=occupancy,
        counts=dict(auxiliary_cases=len(cases),formal_cycles=4*len(cases),
            scalar_calls=sum(x['selector']['calls'] for x in cases),
            nonzero_moves=sum(len(x['selector']['moving_labels']) for x in cases)),
        limits='Constructed finite algebra and endpoint checks, not proof of the compactness step or a numerical global step bound.')
    (HERE/'results.json').write_text(json.dumps(data,indent=2,default=str)+'\n')
    print(json.dumps({'status':'pass','counts':data['counts'],'cases':[
        {k:c[k] for k in ['tile','perturbation','earliest']}|{'calls':c['selector']['calls'],'moves':c['selector']['moving_labels']} for c in cases]},indent=2,default=str))


if __name__=='__main__':
    main()
