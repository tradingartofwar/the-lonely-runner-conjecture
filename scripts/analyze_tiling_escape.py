"""Exact local escape from the common-start tiling at core phase 3/16.

Run: python -m scripts.analyze_tiling_escape [--figure]
Two parametric chambers, eight residue classes, 16 complete small cases,
and eight large-q direct certificates. No sampled-time or speed-box search.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_affine_family import frozen_phase
from scripts.analyze_core_transfer import boundary_certificate, merged
from scripts.analyze_local_overlap import duration, intersect
from scripts.analyze_two_variable_speeds import phase_certificate
from scripts.analyze_two_doubled_offsets import CONTROL_TERMS as TERMS
from scripts.analyze_two_doubled_offsets import DEPENDENCIES as PRIOR_DEPENDENCIES

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "cc916b8dfd0c83c766376c96459d22a9a27c68ad"
DEPENDENCIES = (*PRIOR_DEPENDENCIES, "scripts/analyze_two_doubled_offsets.py")
D, X0, H = Q(1,8), Q(3,16), Q(1,56)
# At x=X0+s*h, each gap is between c-s*A*h and c-s*B*h,
# sorted by position. A>B; A is the boundary first reached by the grid.
GAPS = (
    {"label":"P0", "sign":1, "contact":Q(0), "A":11, "B":5},
    {"label":"P1", "sign":1, "contact":Q(1,8), "A":5, "B":4},
    {"label":"P4", "sign":1, "contact":Q(1,2), "A":11, "B":5},
    {"label":"P7", "sign":1, "contact":Q(7,8), "A":12, "B":11},
    {"label":"M3", "sign":-1, "contact":Q(3,8), "A":11, "B":4},
    {"label":"M5", "sign":-1, "contact":Q(5,8), "A":12, "B":5},
)
WINNERS = (5,2,1,4,3,5,3,2)
NUMERATORS = (3,5,1,1,5,1,1,5)


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def value(line,h):
    return line[0] + line[1]*h


def gap_lines(g):
    c,s,A,B = g["contact"],g["sign"],g["A"],g["B"]
    return ((c,-Q(A)),(c,-Q(B))) if s==1 else ((c,Q(B)),(c,Q(A)))


def geometry_certificate(sign):
    lines=[]
    for b,a in TERMS:
        for m in range(floor(a*X0)-1,floor(a*X0)+b+2):
            for side in (-1,1):
                c=(m+side*D-a*X0)/b
                if 0<=c<1:
                    lines.append((c,-Q(sign*a,b)))
    assert len(lines)==12
    lines.sort(key=lambda line:value(line,H/2))
    cells=[]
    for i,left in enumerate(lines):
        right=lines[i+1] if i+1<len(lines) else (lines[0][0]+1,lines[0][1])
        assert all(value(left,h)<=value(right,h) for h in (Q(0),H))
        assert value(left,H/2)<value(right,H/2)
        midtau=(value(left,H/2)+value(right,H/2))/2
        vertices=[(h,value(line,h)) for h in (Q(0),H) for line in (left,right)]
        runner_rows=[];blocked=[]
        for i,(b,a) in enumerate(TERMS):
            middle=a*(X0+sign*H/2)+b*midtau
            bad=circular_distance(middle)<D
            integer=floor(middle+Q(1,2)) if bad else floor(middle)
            low,high=(integer-D,integer+D) if bad else (integer+D,integer+1-D)
            phases=[a*(X0+sign*h)+b*t for h,t in vertices]
            assert all(low<=p<=high for p in phases)
            if bad:blocked.append(i)
            runner_rows.append({"term":(b,a),"blocked_in_interior":bad,
                "phase_lower_bound":low,"phase_upper_bound":high,"vertex_phases":phases})
        cells.append({"left":left,"right":right,"blocked_runners":blocked,
                      "runner_vertex_certificates":runner_rows})
    good=[(tuple(c["left"]),tuple(c["right"])) for c in cells if not c["blocked_runners"]]
    expected=[gap_lines(g) for g in GAPS if g["sign"]==sign]
    assert sorted(good)==sorted(expected)
    widths=[(r[0]-l[0],r[1]-l[1]) for l,r in good]
    assert sum(w[0] for w in widths)==0 and sum(w[1] for w in widths)==14
    core_rows=[]
    for k in (1,2,3):
        p=[k*(X0+sign*h) for h in (Q(0),H)]
        assert all(D<z<1-D for z in p)
        core_rows.append({"k":k,"endpoint_phases":p})
    return {"sign":sign,"h_domain":(Q(0),H),"boundary_lines":lines,
            "cells":cells,"core_endpoint_certificates":core_rows,
            "clear_length_slope":14,"positive_gap_count":len(good)}


def phase_model(sign,h):
    if h==0:
        return tuple((t,t) for t in (Q(0),Q(1,8),Q(3,8),Q(1,2),Q(5,8),Q(7,8),Q(1)))
    result=[]
    for g in GAPS:
        if g["sign"]!=sign:continue
        l,r=gap_lines(g);a,b=value(l,h),value(r,h)
        for shift in (-1,0,1):
            lo,hi=max(Q(0),a+shift),min(Q(1),b+shift)
            if lo<=hi:result.append((lo,hi))
    return merged(result)


def candidate(q,g):
    z=q*g["contact"]-X0
    j=floor(z) if g["sign"]==1 else ceil(z)
    mismatch=z-j if g["sign"]==1 else j-z
    assert 0<mismatch<1 and (16*mismatch).denominator==1
    return {"label":g["label"],"sign":g["sign"],"contact":g["contact"],
            "A":g["A"],"B":g["B"],"mismatch_numerator":int(16*mismatch),
            "j":j%q,"entry_h":mismatch/(g["A"]*q+1),
            "exit_h":mismatch/(g["B"]*q+1)}


def residue_certificates():
    rows=[]
    for r in range(8):
        q=next(q for q in range(5,13) if q%8==r)
        cc=[candidate(q,g) for g in GAPS]
        win=cc[WINNERS[r]]
        assert win==min(cc,key=lambda c:c["entry_h"])
        assert win["mismatch_numerator"]==NUMERATORS[r]
        n,A=win["mismatch_numerator"],win["A"]
        comparisons=[]
        for c in cc:
            if c is win:continue
            nn,AA=c["mismatch_numerator"],c["A"]
            slope,constant=nn*A-n*AA,nn-n
            assert slope>=0 and 5*slope+constant>0
            comparisons.append({"other":c["label"],"cross_product_slope":slope,
                                "cross_product_constant":constant,"positive_at_q5":5*slope+constant})
        rows.append({"q_mod8":r,"representative_q":q,"winner":win,
                     "six_candidates":cc,"all_q_comparison_certificates":comparisons})
    assert Q(5,16*(4*5+1))<H
    return rows


def model_actual(q):
    result=[]
    for g in GAPS:
        s=g["sign"];c=g["contact"] or Q(1)
        for j in range(q):
            mismatch=s*(q*c-X0-j)
            if mismatch<=0:continue
            lo=max(Q(0),mismatch/(g["A"]*q+1))
            hi=min(H,mismatch/(g["B"]*q+1))
            if lo<=hi:
                result.append(tuple(sorted(((X0+s*lo+j)/q,(X0+s*hi+j)/q))))
    return merged(result)


def check_q(q,complete):
    cc=[candidate(q,g) for g in GAPS]
    row=min(cc,key=lambda c:c["entry_h"])
    assert row["label"]==GAPS[WINNERS[q%8]]["label"]
    assert row["mismatch_numerator"]==NUMERATORS[q%8]
    s,j,h0,h1=row["sign"],row["j"],row["entry_h"],row["exit_h"]
    assert 0<h0<h1<H
    speeds=(q,2*q,3*q,*(a*q+b for b,a in TERMS))
    assert len(set(speeds))==7
    t0,t1=(X0+s*h0+j)/q,(X0+s*h1+j)/q
    interval=tuple(sorted((t0,t1)))
    midpoint=sum(interval)/2
    lo,hi=interval
    inner=((3*lo+hi)/4,(lo+3*hi)/4)
    endpoints={"entry":{str(v):circular_distance(v*t0) for v in speeds},
               "exit":{str(v):circular_distance(v*t1) for v in speeds}}
    assert min(endpoints["entry"].values())==min(endpoints["exit"].values())==D
    assert all(min(circular_distance(v*t) for v in speeds)>D for t in (*inner,midpoint))
    cert=phase_certificate(speeds,inner)
    fullcert=phase_certificate(speeds,interval)
    width=(row["A"]-row["B"])*h0
    assert q*width<1
    # The entry is valid in a gap narrower than the sufficient width-only bound.
    assert abs(t0-(X0+j)/q)==h0/q
    assert hi-lo==(h1-h0)/q
    result={"q":q,"complete_local_check":complete,"six_entry_candidates":cc,
        "selected":row,"speeds":speeds,"entry_time":t0,"exit_time":t1,
        "closed_time_component":interval,"entry_exit_distances":endpoints,
        "strict_midpoint":midpoint,"strict_midpoint_minimum":min(circular_distance(v*midpoint) for v in speeds),
        "strict_inner_interval":inner,"strict_interval_certificate":cert,
        "closed_component_certificate":fullcert,"entry_gap_width":width,
        "gap_width_over_grid_spacing":q*width,"time_displacement_from_blocked_branch":h0/q}
    if complete:
        full=feasible_intervals(speeds,D)
        assert full==boundary_certificate(speeds)["complete_allowed_set"]
        windows=tuple(((X0-H+j)/q,(X0+H+j)/q) for j in range(q))
        local=intersect(full,windows)
        assert local==model_actual(q)
        assert interval in full
        distances=[]
        for jj,w in enumerate(windows):
            for a,b in intersect(full,(w,)):
                da,db=q*a-jj-X0,q*b-jj-X0
                assert da*db>0
                distances.extend((abs(da),abs(db)))
        assert min(distances)==h0
        result["complete_local_allowed_intervals"]=local
        result["full_allowed_summary"]={"components":len(full),"duration":duration(full),
            "sha256_json_string_endpoints":hashlib.sha256(json.dumps(full,default=str).encode()).hexdigest()}
    return result


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"svg.hashsalt":"tiling-escape","font.size":10})
    fig,(left,right)=plt.subplots(1,2,figsize=(12,5.3))
    left.plot([-float(H),0,float(H)],[.25,0,.25],color="#247c66",linewidth=2.5)
    left.axvspan(-float(H),0,color="#5d8eb5",alpha=.10)
    left.axvspan(0,float(H),color="#c09348",alpha=.10)
    left.text(-float(H)/2,.23,"2 openings",ha="center")
    left.text(float(H)/2,.23,"4 openings",ha="center")
    left.text(0,.14,r"Total clear length $G=14|\varepsilon|$",ha="center",fontsize=10)
    left.set_xticks([-float(H),0,float(H)],["-1/56","0","1/56"])
    left.set_yticks([0,.125,.25],["0","1/8","1/4"])
    left.set_xlabel("Core phase change epsilon from 3/16")
    left.set_ylabel("Total auxiliary clear length")
    left.set_title("Same total room; different pieces",loc="left",fontweight="bold")
    # Exact affine lines for the q=6 P7 gap; axis rescales h by first entry.
    q=6;g=GAPS[3];c=candidate(q,g);entry,exit=c["entry_h"],c["exit_h"]
    end=Q(3,2)*entry
    hs=(Q(0),end)
    xx=[float(h/entry) for h in hs]
    lower=[float(-12*h) for h in hs];upper=[float(-11*h) for h in hs]
    right.fill_between(xx,lower,upper,color="#96c5a7",alpha=.7,label="Opening")
    grid=[float(-Q(1,96)+h/q) for h in hs]
    right.plot(xx,grid,color="#37434f",linewidth=2,label="One actual-time branch")
    right.plot([1,float(exit/entry)],[float(-Q(1,96)+entry/q),float(-Q(1,96)+exit/q)],color="#177440",linewidth=4)
    right.scatter([1,float(exit/entry)],[float(-Q(1,96)+entry/q),float(-Q(1,96)+exit/q)],color="#177440",s=24,zorder=5)
    right.annotate("Entry: h = 1/1168",xy=(1,float(-Q(1,96)+entry/q)),xytext=(.25,-.004),
                   arrowprops={"arrowstyle":"->","color":"#37434f"},fontsize=9)
    right.annotate("Exit: h = 1/1072",xy=(float(exit/entry),float(-Q(1,96)+exit/q)),xytext=(.35,-.014),
                   arrowprops={"arrowstyle":"->","color":"#37434f"},fontsize=9)
    right.set_xlim(0,1.5)
    right.set_xlabel("h / first-entry displacement")
    right.set_ylabel("Auxiliary phase relative to 7/8")
    right.set_title("A narrow opening is reached (q = 6)",loc="left",fontweight="bold")
    right.legend(loc="upper right",frameon=False,fontsize=9)
    for ax in (left,right):
        ax.grid(alpha=.15)
        ax.spines["top"].set_visible(False);ax.spines["right"].set_visible(False)
    fig.suptitle("Escaping a perfect tiling: width and alignment",x=.08,ha="left",fontsize=15)
    fig.text(.08,.025,"At first entry, the q = 6 gap is only 3/584 of the grid spacing (about 0.51%). Equality counts; its interior gives strict separation.",fontsize=9)
    fig.subplots_adjust(left=.08,right=.98,top=.83,bottom=.19,wspace=.33)
    fig.savefig(ROOT/"figures/tiling_escape.svg",metadata={"Date":None})
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--figure",action="store_true");args=parser.parse_args()
    chambers=[geometry_certificate(s) for s in (-1,1)]
    residues=residue_certificates()
    frozen=[]
    for s in (-1,1):
        for h in (Q(0),H/2,H):
            p=frozen_phase(TERMS,X0+s*h)
            assert p["allowed_phases"]==phase_model(s,h)
            assert p["clear_phase_duration"]==14*h
            frozen.append({"sign":s,"h":h,"profile":p})
    beyond=frozen_phase(TERMS,X0+Q(1,55))
    assert beyond["clear_phase_duration"]==Q(1,4)!=Q(14,55)
    cases=[check_q(q,True) for q in range(5,21)]
    print("q=5..20: all sixteen complete local reconstructions pass",flush=True)
    cases.extend(check_q(1_000_000+r,False) for r in range(8))
    print("eight large-q residue representatives: direct exact certificates pass",flush=True)
    six=next(c for c in cases if c["q"]==6)
    assert six["entry_time"]==Q(505,584) and six["exit_time"]==Q(927,1072)
    assert six["gap_width_over_grid_spacing"]==Q(3,584)
    five=next(c for c in cases if c["q"]==5)
    assert five["closed_time_component"]==(Q(265,416),Q(311,488))
    counts={"parametric_chambers":2,"certified_boundary_cells":24,
            "runner_cell_vertex_certificates":96,"vertex_phase_checks":384,
            "residue_classes":8,"all_q_winner_comparisons":40,
            "frozen_phase_controls":6,"beyond_neighborhood_controls":1,
            "complete_actual_boundary_reconstructions":16,
            "complete_local_interval_model_comparisons":16,
            "exact_nearest_phase_comparisons":16,
            "direct_large_q_certificates":8,"strict_point_and_inner_interval_certificates":24,
            "closed_component_certificates":24}
    paths=("scripts/analyze_tiling_escape.py",*DEPENDENCIES)
    data={"date_utc":"2026-09-25","base_commit":BASE_COMMIT,
          "scope":"Eight common-start runners, reference 0; 0,q,2q,3q,4q+1,12q+1,10q+2,22q+2; integer q>=5. Local core phase x=3/16+epsilon with |epsilon|<=1/56.",
          "selection":"Two chambers cover a continuum via affine vertex inequalities. Eight residue classes cover unbounded q via linear cross-product comparisons. q=5..20 supplies two representatives of each residue with full allowed-set reconstruction; eight million-scale representatives use direct certificates without grid enumeration.",
          "claim_status":{"finite_checks":"OBSERVED, exact rational","parametric_and_all_q_claims":"HYPOTHESIS/proof candidates awaiting independent review","novelty":"Unestablished; known pre-jump context S15; no wider novelty audit"},
          "source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
          "x0":X0,"neighborhood_radius":H,"gap_branches":GAPS,"chamber_certificates":chambers,
          "residue_certificates":residues,"frozen_controls":frozen,
          "beyond_neighborhood_control":{"epsilon":Q(1,55),"profile":beyond,"incorrect_linear_extrapolation":Q(14,55)},
          "cases":cases,"verification_counts":counts,
          "limits":"Nearest means core-phase displacement from x0, not the first lonely time of the race or a global maximum. The exact contact has distance 1/8; strictness holds inside its certified time component. Local linear growth is not extrapolated beyond the certified neighborhood. Existing helpers unchanged; broader regression suite not rerun; no independent proof review or novelty claim."}
    (ROOT/"experiments/tiling_escape.json").write_text(json.dumps(data,indent=2,default=str)+"\n")
    if args.figure:figure()
    print(json.dumps(counts,indent=2))


if __name__=="__main__":
    main()
