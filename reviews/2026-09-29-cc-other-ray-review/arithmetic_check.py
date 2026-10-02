#!/usr/bin/env python3
"""Fresh exact arithmetic countercheck of the V(q,1) ray, 2026-09-29.

Authored before reading any original mathematical implementation or JSON output.
Inputs: the two written OTHER_RAY notes, especially the stated peak/edge table.
The completeness of that fixed geometry is a premise, not reconstructed here.
No project imports, no physical parameter scan, no floating point arithmetic.
Run from any directory: python3 /path/to/arithmetic_check.py > arithmetic_check.json
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json


class P:
    """A rational polynomial, with coefficients in increasing degree order."""
    def __init__(self, *coeff):
        if len(coeff) == 1 and isinstance(coeff[0], P):
            coeff = coeff[0].c
        coeff = list(map(F, coeff or (0,)))
        while len(coeff) > 1 and coeff[-1] == 0:
            coeff.pop()
        self.c = tuple(coeff)

    def __add__(self, other):
        other = P(other)
        size = max(len(self.c), len(other.c))
        return P(*(sum(v[i] if i < len(v) else F(0) for v in (self.c, other.c))
                   for i in range(size)))

    __radd__ = __add__

    def __neg__(self):
        return P(*(-a for a in self.c))

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) - self

    def __mul__(self, other):
        other = P(other)
        c = [F(0)] * (len(self.c) + len(other.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                c[i+j] += a*b
        return P(*c)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.c == P(other).c

    def at(self, x):
        return sum(a * F(x)**i for i, a in enumerate(self.c))

    def shifted(self, start):
        return [sum(self.c[j]*comb(j, i)*F(start)**(j-i)
                    for j in range(i, len(self.c))) for i in range(len(self.c))]

    def nonnegative(self, start, strict=False):
        shifted = self.shifted(start)
        return all(a >= 0 for a in shifted) and (not strict or shifted[0] > 0)

    def out(self):
        return [str(a) for a in self.c]


class Rat:
    """Rational functions; identities checked by polynomial cross products."""
    def __init__(self, num, den=1):
        self.n, self.d = P(num), P(den)
        assert self.d != 0

    @staticmethod
    def cast(value):
        return value if isinstance(value, Rat) else Rat(value)

    def __add__(self, other):
        other = Rat.cast(other)
        return Rat(self.n*other.d + other.n*self.d, self.d*other.d)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.n, self.d)

    def __sub__(self, other):
        return self + -Rat.cast(other)

    def __rsub__(self, other):
        return Rat.cast(other) - self

    def __mul__(self, other):
        other = Rat.cast(other)
        return Rat(self.n*other.n, self.d*other.d)

    __rmul__ = __mul__

    def __eq__(self, other):
        other = Rat.cast(other)
        return self.n*other.d == other.n*self.d


ROWS = [(1,0), (0,1), (1,1), (2,1), (3,1), (3,2), (5,2)]
PERM = [1,0,2,3,4,5,6]
PEAKS = {
    'A': ((F(1,6), F(1,6)), [(-1,2), (F(1,5),-1), (1,-1)]),
    'B': ((F(1,6), F(1,3)), [(-1,1), (-1,4), (1,-2)]),
    'C': ((F(1,2), F(1,6)), [(-3,5), (0,-1), (0,F(1,2))]),
    'D': ((F(1,2), F(1,3)), [(-1,2), (0,F(-1,2)), (0,1)]),
    'E': ((F(1,3), F(5,6)), [(-2,1), (0,1), (1,-2)]),
    'F': ((F(1,2), F(2,3)), [(-1,2), (0,-1), (0,F(1,2))]),
    'G': ((F(1,2), F(5,6)), [(F(-3,5),1), (0,F(-1,2)), (0,1)]),
}
QMIN = {0:6, 1:7, 2:2, 3:3, 4:4, 5:5}
KMIN = {r:(q-r)//6 for r,q in QMIN.items()}
WINNER_CLAIMS = {0:('B',1), 2:('C',0), 5:('F',0)}
# Entries are SIX TIMES the loss; each denominator is [constant, q coefficient].
TABLE = {
    'A': {0:(1,P(1,2)), 2:(1,P(1,1)), 5:(2,P(1,2))},
    'B': {0:(1,P(1,4)), 2:(3,P(1,4)), 5:(3,P(1,4))},
    'C': {0:(3,P(3,5)), 2:(1,P(3,5)), 5:(4,P(3,5))},
    'D': {0:(3,P(1,2)), 2:(2,P(0,1)), 5:(2,P(0,1))},
    'E': {0:(2,P(2,1)), 2:(2,P(1,2)), 5:(1,P(2,1))},
    'F': {0:(3,P(1,2)), 2:(1,P(1,2)), 5:(1,P(1,2))},
    'G': {0:(15,P(3,5)), 2:(2,P(0,1)), 5:(10,P(3,5))},
}


def rank(rows):
    rows = [list(map(F, row)) for row in rows]
    pivot = 0
    for col in range(3):
        pos = next((j for j in range(pivot,len(rows)) if rows[j][col]),None)
        if pos is None:
            continue
        rows[pivot],rows[pos] = rows[pos],rows[pivot]
        fac = rows[pivot][col]
        rows[pivot] = [a/fac for a in rows[pivot]]
        for j in range(len(rows)):
            if j != pivot:
                fac = rows[j][col]
                rows[j] = [a-fac*b for a,b in zip(rows[j],rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def bands(point, laps):
    x,y,z = point
    # All inequalities written n . (x,y,z) >= b.
    constraints = [((0,0,1), F(1,8)), ((-1,0,0), F(-1,2))]
    for (a,b),m in zip(ROWS,laps):
        constraints += [((a,b,-1), F(m)), ((-a,-b,-1), F(-m-1))]
    active = []
    for normal, bound in constraints:
        value = sum(a*b for a,b in zip(normal,(x,y,z)))
        assert value >= bound
        if value == bound:
            active.append(normal)
    return active


def loss_compare(candidate, target, qmin):
    # c.n/c.d - t.n/t.d; all denominators separately proved positive.
    diff = P(candidate['n'])*target['d'] - P(target['n'])*candidate['d']
    assert len(diff.c) <= 2
    assert diff.nonnegative(qmin)
    return {'cross_product_coefficients':diff.out(),
            'at_domain_minimum':str(diff.at(qmin)),
            'strict_on_domain':diff.nonnegative(qmin,strict=True)}


def audit():
    result = {'scope':'Exact symbolic AI arithmetic countercheck; fixed geometry completeness assumed',
              'frozen_head':'12d08824ead7b772032ba240d0e858250fbd183c',
              'original_mathematical_code_or_output_read':[],
              'coefficient_order':ROWS, 'q_domain_minima':QMIN,
              'polynomial_encoding':'coefficients in increasing degree order; exact fraction strings'}
    root = Path(__file__).resolve().parents[2]
    # Historical README/HANDOFF read provenance is in arithmetic_review.md;
    # current handoff updates must not change this mathematical output.
    inputs = ['AGENTS.md','CLAIM_STATUS.md','CONTRIBUTING.md',
              'reviews/2026-09-29-cc-other-ray-review/PROTOCOL.md',
              'notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md',
              'notes/LTCM_OTHER_RAY_RECOVERY_2026_09_29.md']
    result['input_sha256'] = {name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                              for name in inputs}
    congruences, edges, losses, endpoints = {}, [], {}, []
    for r in range(6):
        congruences[r] = [name for name,((x,y),_) in PEAKS.items()
                          if (x-r*y).denominator == 1]
    assert congruences == {0:[],1:['A'],2:[],3:['C','G'],4:['E'],5:[]}
    result['compatible_peaks'] = congruences
    for name,((x,y),directions) in PEAKS.items():
        laps = [int(a*x+b*y) for a,b in ROWS]
        peak_active = bands((x,y,F(1,6)),laps)
        assert rank(peak_active) == 3
        for j,(alpha,beta) in enumerate(directions):
            d = P(alpha,-beta)
            sign = 1 if d.at(2) > 0 else -1
            absd = d*sign
            assert absd.nonnegative(2,strict=True)  # no zero projection for q>=2
            emax = F(1,42) if (name,j)==('E',0) else F(1,24)
            end = (x+alpha*emax,y+beta*emax,F(1,6)-emax)
            end_active = bands(end,laps)
            assert rank(end_active) == 3
            common = [a for a in peak_active if a in end_active]
            assert rank(common) == 2
            edge = {'peak':name,'direction_index':j,'direction':[str(alpha),str(beta)],
                    'projection_coefficients':d.out(),'projection_sign':sign,
                    'absolute_projection_at_q2':str(absd.at(2)),
                    'maximum_e':str(emax),'endpoint':list(map(str,end)),
                    'ambient_laps':laps,'common_active_rank':2}
            edges.append(edge)
            for r in (0,2,5):
                h = x-r*y
                rho = h - h.numerator//h.denominator
                assert 0 < rho < 1
                gap = rho if sign < 0 else 1-rho
                # Six times loss, so comparison coefficients remain concise.
                loss = {'peak':name,'direction_index':j,'r':r,'n':6*gap,'d':absd}
                losses[r,name,j] = loss
                assert absd.c[1] > 0
                threshold = (gap/emax-absd.c[0])/absd.c[1]
                steps = (threshold-QMIN[r])/6
                ceiling = -((-steps.numerator)//steps.denominator)
                first_q = QMIN[r]+6*max(0,ceiling)
                assert gap/absd.at(first_q) <= emax
                assert first_q==QMIN[r] or gap/absd.at(first_q-6)>emax
                endpoints.append({'peak':name,'direction_index':j,'r':r,
                                  'rho':str(rho),'gap_in_directed_H':str(gap),
                                  'six_loss_numerator':str(6*gap),
                                  'six_loss_denominator_coefficients':absd.out(),
                                  'first_hit_within_edge_from_q':first_q,
                                  'first_domain_q':QMIN[r]})
    result['edges'] = edges
    result['directed_losses'] = endpoints
    comparisons, table_comparisons, winners = [], [], {}
    for r in (0,2,5):
        candidates = [v for (rr,_,_),v in losses.items() if rr==r]
        # Derive the universal winner, without using WINNER_CLAIMS for selection.
        winning = []
        for target in candidates:
            diffs = [P(c['n'])*target['d']-P(target['n'])*c['d'] for c in candidates]
            if all(d.nonnegative(QMIN[r]) for d in diffs):
                winning.append(target)
        assert len(winning) == 1
        win = winning[0]
        assert (win['peak'],win['direction_index']) == WINNER_CLAIMS[r]
        winners[r] = {'peak':win['peak'],'direction_index':win['direction_index'],
                      'six_loss_numerator':str(win['n']),
                      'six_loss_denominator_coefficients':win['d'].out()}
        for c in candidates:
            proof = loss_compare(c,win,QMIN[r])
            is_winner = c is win
            assert proof['strict_on_domain'] != is_winner
            comparisons.append({'r':r,'peak':c['peak'],'direction_index':c['direction_index'],
                                'is_winner':is_winner,**proof})
            n,d = TABLE[c['peak']][r]
            target = {'n':F(n),'d':d}
            assert d.nonnegative(QMIN[r],strict=True)
            proof = loss_compare(c,target,QMIN[r])
            table_comparisons.append({'r':r,'peak':c['peak'],
                                     'direction_index':c['direction_index'],**proof})
        for name in PEAKS:
            n,d = TABLE[name][r]
            assert any(P(losses[r,name,j]['n'])*d == P(n)*losses[r,name,j]['d']
                       for j in range(3))
    assert len(comparisons)==63 and len(table_comparisons)==63
    result['derived_winners']=winners
    result['global_comparisons']=comparisons
    result['within_peak_table_comparisons']=table_comparisons

    k = P(0,1)
    raw = {
        0:(8*k+1,24*k+1,4*k,[0,2*k,2*k,4*k,6*k,6*k+1,10*k+1],
           [8*k+1,4*k,12*k+1,16*k+1,20*k+1,4*k+1,12*k+1]),
        2:(5*k+3,30*k+13,5*k+2,[0,k,k,2*k+1,3*k+1,3*k+1,5*k+2],
           [5*k+3,15*k+6,20*k+9,5*k+2,20*k+8,25*k+11,25*k+10]),
        5:(12*k+10,36*k+33,6*k+5,[0,2*k+1,2*k+1,4*k+3,6*k+4,6*k+5,10*k+8],
           [12*k+10,18*k+17,30*k+27,12*k+11,30*k+28,6*k+5,6*k+6]),
        1:(P(1),P(6),P(1),[0,k,k,2*k,3*k,3*k,5*k+1],[1,1,2,3,4,5,1]),
        3:(P(1),P(6),P(1),[0,k,k,2*k+1,3*k+1,3*k+1,5*k+2],[1,3,4,1,4,5,5]),
        4:(P(1),P(6),P(1),[0,k,k,2*k+1,3*k+2,3*k+2,5*k+3],[1,4,5,3,1,2,4]),
    }
    witness_rows, safety, phase_identities, transfer = [], [], [], []
    for r in range(6):
        q = 6*k+r
        N,D,A,ell,R = raw[r]
        ell,R = list(map(P,ell)),list(map(P,R))
        speeds = [P(1),q,q+1,2*q+1,3*q+1,3*q+2,5*q+2]
        assert A.nonnegative(KMIN[r],strict=True)
        assert D.nonnegative(KMIN[r],strict=True)
        assert (7*A-D).nonnegative(KMIN[r],strict=True)  # F > 1/7
        assert N.nonnegative(KMIN[r],strict=True)
        assert (D-2*N).nonnegative(KMIN[r],strict=True)  # 0<t<1/2
        for i,v in enumerate(speeds):
            assert v*N == ell[i]*D+R[i]
            phase_identities.append({'r':r,'coordinate':i,'identity_difference':(v*N-ell[i]*D-R[i]).out()})
            for side,margin in [('lower',R[i]-A),('upper',D-A-R[i])]:
                assert margin.nonnegative(KMIN[r])
                safety.append({'r':r,'coordinate':i,'side':side,'coefficients':margin.out(),
                               'at_domain_minimum':str(margin.at(KMIN[r]))})
        contacts = [i for i in range(7) if R[i]==A or R[i]==D-A]
        assert contacts
        if r in (0,2,5):
            win = losses[r,*WINNER_CLAIMS[r]]
            denq = P(win['d'].at(r),win['d'].c[1]*6)
            e = Rat(P(win['n']/6),denq)
            name,j = WINNER_CLAIMS[r]
            alpha,beta = PEAKS[name][1][j]
            # Winner losses are monotone decreasing on their whole q domains.
            maxe = (win['n']/6)/win['d'].at(QMIN[r])
            assert maxe < F(1,42) < F(1,24)
            assert Rat(F(1,6))-e == Rat(A,D)
        else:
            name,j = {1:('A',None),3:('C',None),4:('E',None)}[r]
            alpha,beta = 0,0
            e = Rat(0)
            maxe=F(0)
        x0,y0 = PEAKS[name][0]
        x,y = Rat(x0)+alpha*e,Rat(y0)+beta*e
        H = x-y*q
        # Obtain H as an affine polynomial from its exact values at k=0,1;
        # then prove the identity, rather than relying on interpolation.
        h0 = H.n.at(0)/H.d.at(0)
        h1 = H.n.at(1)/H.d.at(1)
        hp = P(h0,h1-h0)
        assert H == hp and all(a.denominator==1 for a in hp.c)
        reflected = r in (4,5)
        t = 1-y if reflected else y
        assert t == Rat(N,D)
        ambient = [int(a*x0+b*y0) for a,b in ROWS]
        folded_laps = [P(m)-a*hp for (a,b),m in zip(ROWS,ambient)]
        unpermuted_speeds=[a*q+b for a,b in ROWS]
        physical = [v-1-l if reflected else l
                    for v,l in zip(unpermuted_speeds,folded_laps)]
        physical = [physical[i] for i in PERM]
        assert physical == ell
        for i,((a,b),m,v) in enumerate(zip(ROWS,ambient,unpermuted_speeds)):
            ambient_phase = x*a+y*b-m
            physical_phase = t*v-physical[PERM.index(i)]
            assert physical_phase == (1-ambient_phase if reflected else ambient_phase)
            transfer.append({'r':r,'unpermuted_coordinate':i,'identity_verified':True})
        reflected_laps = [v-1-l for v,l in zip(speeds,ell)]
        for v,l,rr in zip(speeds,reflected_laps,R):
            assert v*(D-N)-l*D == D-rr
        witness_rows.append({'r':r,'k_min':KMIN[r],'q_min':QMIN[r],
                             'peak':name,'reflected_to_selected_time':reflected,
                             'H_coefficients_in_k':hp.out(),'ambient_laps':ambient,
                             'derived_physical_laps':[p.out() for p in physical],
                             'N':N.out(),'D':D.out(),'A':A.out(),
                             'contact_coordinates':contacts,'largest_winning_loss':str(maxe)})
    assert len(phase_identities)==42 and len(safety)==84 and len(transfer)==42
    result['physical_witnesses']=witness_rows
    result['phase_identities']=phase_identities
    result['safe_band_inequalities']=safety
    result['physical_transfer_identities']=transfer
    result['summary']={'peak_directions':21,'nonzero_projection_certificates':21,
                       'directed_losses':63,'global_comparisons':63,
                       'strict_nonwinner_comparisons':60,'within_peak_comparisons':63,
                       'phase_identities':42,'safe_band_inequalities':84,
                       'physical_lap_transfers':42,'reflected_phase_identities':42,
                       'result':'PASS',
                       'remaining_premises':['fixed-cell completeness and ambient height classification',
                                             'slice-vertex reduction and optimizer-face argument reviewed separately']}
    return result


if __name__ == '__main__':
    print(json.dumps(audit(),indent=2,sort_keys=True))
