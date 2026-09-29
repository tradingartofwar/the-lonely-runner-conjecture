#!/usr/bin/env python3
"""Post-protocol P3-only B-ray simplification; original outputs untouched."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = ((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2))
ORDER = (1,0,2,3,4,5,6)
Z = F(1,8)


def ceil(value):
    return -((-value.numerator)//value.denominator)


def physical(speeds, time):
    products = [v*time for v in speeds]
    laps = [p.numerator//p.denominator for p in products]
    phases = [p-l for p,l in zip(products,laps)]
    distances = [min(p,1-p) for p in phases]
    assert min(distances) == Z
    return {"time":time,"laps":laps,"phases":phases,
            "distances":distances,"minimum":min(distances)}


def encode(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,dict):
        return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [encode(v) for v in value]
    return value


def run():
    old_names = ("transfer.json","physical_review.py","physical_review.json","physical_review.md")
    old_hashes = {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in old_names}
    frozen = json.loads((HERE/"transfer.json").read_bytes())
    candidate = next(c for c in frozen["cover"]["chosen_segments"] if c["id"] == "P3:E0-1:K2")
    p0,p1 = [[F(v) for v in p] for p in candidate["endpoints"]]
    labels = candidate["labels"]
    # Derive v=alpha*u+beta, then solve g=qu-v for u=t.
    alpha = (p1[1]-p0[1])/(p1[0]-p0[0])
    beta = p0[1]-alpha*p0[0]
    assert alpha == F(-1,2) and beta == F(9,16)
    assert p0 == [F(1,8),F(1,2)] and p1 == [F(3,8),F(3,8)]
    assert labels == [0,0,0,1,1,1,2]
    endpoint_records = []
    for (a,b),m in zip(ROWS,labels):
        phases = [a*v+b*u-m for u,v in (p0,p1)]
        lower = [p-Z for p in phases]
        upper = [1-Z-p for p in phases]
        assert min(lower+upper) >= 0
        endpoint_records.append({"row":[a,b],"lap":m,"phases":phases,
                                 "lower_margins":lower,"upper_margins":upper})
    assert endpoint_records[3]["phases"] == [Z,Z]
    # Prove floor((q+3)/8)=ceil((q-4)/8) on every integer residue.
    rounding = []
    for residue in range(8):
        epsilon = (residue+3)//8
        margin = 8*epsilon-residue+4
        assert 0 <= margin < 8
        rounding.append({"q_mod_8":residue,"g_minus_floor_q_over_8":epsilon,
                         "eight_g_minus_q_plus_4":margin})
    # Universal tail: width=(2q+1)/8, positive slope, >=1 at q=4.
    width_at_4, slope = F(9,8), F(1,4)
    assert width_at_4 >= 1 and slope > 0
    prefix = []
    for q in (2,3):
        lo,hi = F(q-4,8),F(3*(q-1),8)
        g = (q+3)//8
        assert lo <= g <= hi
        prefix.append({"q":q,"interval":[lo,hi],"g":g})
    controls = []
    for q in range(2,26):
        speeds = (1,q,q+1,2*q+1,3*q+1,3*q+2,5*q+2)
        g = (q+3)//8
        time = F(16*g+9,8*(2*q+1))
        lo,hi = F(q-4,8),F(3*(q-1),8)
        assert g == ceil(lo) and g <= hi
        # Separately interpolate the frozen endpoints by their orbit values.
        g0,g1 = q*p0[0]-p0[1],q*p1[0]-p1[1]
        assert (g0,g1) == (lo,hi)
        lam = F(g-g0,g1-g0)
        u,v = [a+lam*(b-a) for a,b in zip(p0,p1)]
        assert u == time == (g+beta)/(q-alpha)
        assert q*time-v == g and 0 <= lam <= 1
        assert F(1,8) <= u <= F(3,8) and F(3,8) <= v <= F(1,2)
        direct, reflected = physical(speeds,time),physical(speeds,1-time)
        laps = [m+a*g for (a,b),m in zip(ROWS,labels)]
        phases = [a*v+b*u-m for (a,b),m in zip(ROWS,labels)]
        assert direct["laps"] == [laps[i] for i in ORDER]
        assert direct["phases"] == [phases[i] for i in ORDER]
        assert reflected["laps"] == [s-1-l for s,l in zip(speeds,direct["laps"])]
        assert reflected["phases"] == [1-p for p in direct["phases"]]
        controls.append({"q":q,"g":g,"interval":[lo,hi],"parameter":lam,
             "native_point_x_y":[v,u],"speeds":speeds,"selected":direct,"reflected":reflected})
    assert all(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==old_hashes[name] for name in old_names)
    return {"status":"PASS: post-protocol one-segment simplification",
       "authorship":"Separate internal AI physical reviewer; no discovery or earlier checker imports",
       "chronology":"Requested after frozen two-segment transfer/review; no retuning of discovery rule",
       "summary":{"candidate_segments":1,"q_controls":24,"selected_and_reflected_pairs":24,
           "additional_physical_times":48,"additional_exact_distances":336,
           "endpoint_inequalities":28,"rounding_residues":8,"tail_cutoff":4,
           "new_physical_q_values":0,"original_output_files_unchanged":True},
       "original_file_sha256":old_hashes,
       "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       "protocol_sha256":hashlib.sha256((HERE/"POST_PROTOCOL_SIMPLIFICATION.md").read_bytes()).hexdigest(),
       "candidate":candidate,
       "formula":{"g":"floor((q+3)/8)","t":"(16*g+9)/(8*(2*q+1))",
           "v_equals_alpha_u_plus_beta":{"alpha":alpha,"beta":beta},
           "physical_laps":"ell=m+a*g for original row (a,b)",
           "physical_identity":"(a*q+b)*u - (m+a*(q*u-v)) = a*v+b*u-m"},
       "rounding_certificate":rounding,"endpoint_certificates":endpoint_records,
       "unbounded_coverage":{"lower":"(q-4)/8","upper":"3(q-1)/8",
           "width":"(2q+1)/8","width_at_4":width_at_4,"width_slope":slope,
           "argument":"For q>=4 the closed interval has width>=1; ceil(lower)<=upper. Exact prefix handles q=2,3."},
       "universal_safety":"Every segment phase is affine and in [1/8,7/8] at both endpoints; physical identity transfers the entire segment on integer orbits. Fourth phase is identically 1/8.",
       "prefix":prefix,"controls":controls,
       "limits":"One physical witness only; post-protocol simplification not discovered by frozen ranking; no optimality, all-witness, novelty, formal verification or independent human-review claim."}


if __name__ == "__main__":
    result = run()
    (HERE/"single_segment.json").write_text(json.dumps(encode(result),indent=2,sort_keys=True)+"\n")
    print(json.dumps(result["summary"],sort_keys=True))
