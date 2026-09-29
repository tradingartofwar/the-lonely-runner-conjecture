#!/usr/bin/env python3
"""Separately authored B-ray physical checker; no discovery/selector imports.

Input endpoints and claims are read only from the frozen transfer.json. Uses
exact Fractions and elementary polynomial arithmetic. Physical evaluations
are confined to archived q=2,...,25 and their reflections.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "transfer.json"
ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
ORDER = (1, 0, 2, 3, 4, 5, 6)
Z = F(1, 8)


def ceil(x):
    return -((-x.numerator) // x.denominator)


def polyadd(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def scale(a, x):
    return [v*x for v in a]


def sub(a, b):
    return polyadd(a, scale(b, -1))


def mul(a, b):
    out = [F(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return polyadd(out, [F(0)])


def shift(a, start):
    """Coefficients of p(start+s), ascending powers of nonnegative s."""
    out = [F(0)]
    for c in reversed(a):
        out = polyadd(mul(out, [F(start), F(1)]), [c])
    return out


def physical(q, time):
    speeds = (1, q, q+1, 2*q+1, 3*q+1, 3*q+2, 5*q+2)
    products = [v*time for v in speeds]
    laps = [p.numerator // p.denominator for p in products]
    phases = [p-l for p, l in zip(products, laps)]
    distances = [min(p, 1-p) for p in phases]
    return {"time": time, "speeds": speeds, "laps": laps,
            "phases": phases, "distances": distances,
            "minimum": min(distances)}


def own_select(segments, q):
    """Integer hit and interpolation, using supplied segments as claims only."""
    attempts = []
    for record in segments:
        p0, p1 = [[F(c) for c in p] for p in record["endpoints"]]
        g0, g1 = q*p0[0]-p0[1], q*p1[0]-p1[1]
        lo, hi = min(g0, g1), max(g0, g1)
        g = ceil(lo)
        attempts.append({"segment": record["id"], "interval": [lo, hi],
                         "first_integer": g, "hit": g <= hi})
        if g > hi:
            continue
        if g0 == g1:
            lam = F(0)
        else:
            lam = (g-g0)/(g1-g0)
        assert 0 <= lam <= 1
        u, v = [a+lam*(b-a) for a, b in zip(p0, p1)]
        assert q*u-v == g
        return record, g, lam, (u, v), attempts
    raise AssertionError(("supplied segments do not cover", q))


def endpoint_proof(segments):
    certificates = []
    for record in segments:
        p0, p1 = [[F(c) for c in p] for p in record["endpoints"]]
        rows = []
        for (a, b), m in zip(ROWS, record["labels"]):
            phases = [a*v+b*u-m for u, v in (p0, p1)]
            lower = [p-Z for p in phases]
            upper = [1-Z-p for p in phases]
            assert min(lower+upper) >= 0
            rows.append({"original_row": [a, b], "local_lap": m,
                         "endpoint_phases": phases,
                         "lower_margins": lower, "upper_margins": upper})
        certificates.append({"segment": record["id"], "rows": rows,
            "argument": "Each phase and each margin is affine in lambda in [0,1]; endpoint nonnegativity proves the entire segment safe."})
    return certificates


def derive_clock_formulas(segments):
    out = []
    for record in segments:
        (u0,v0),(u1,v1) = [[F(c) for c in p] for p in record["endpoints"]]
        alpha = (v1-v0)/(u1-u0)
        beta = v0-alpha*u0
        assert v1 == alpha*u1+beta
        out.append({"segment":record["id"],"v_equals_alpha_u_plus_beta":{
           "alpha":alpha,"beta":beta},
           "orbit_elimination":"g=q*u-v=(q-alpha)*u-beta, so t=u=(g+beta)/(q-alpha)",
           "positive_denominator_for_all_q_ge_2":2-alpha > 0})
    assert out[0]["v_equals_alpha_u_plus_beta"] == {"alpha":F(-1,3),"beta":F(7,24)}
    assert out[1]["v_equals_alpha_u_plus_beta"] == {"alpha":F(-1,2),"beta":F(9,16)}
    assert all(r["positive_denominator_for_all_q_ge_2"] for r in out)
    return out


def residue_proof(primary):
    """Direct physical-time proof on four infinite domains; no samples."""
    assert primary["id"] == "P1:E1-3:K1"
    certificates = []
    for r, amin in ((0, 1), (1, 1), (2, 1), (3, 0)):
        # q=4*a+r and g=ceil(q/4); every domain here has q>=3.
        q = [F(r), F(4)]
        g = [F(int(r != 0)), F(1)]
        numerator = polyadd(scale(g, 24), [F(7)])
        denominator = scale(polyadd(scale(q, 3), [F(1)]), 8)
        assert all(x >= 0 for x in shift(denominator, amin))
        assert shift(denominator, amin)[0] > 0
        records = []
        for a, b, m in [(a, b, m) for (a, b), m in zip(ROWS, primary["labels"])]:
            speed = polyadd(scale(q, a), [F(b)])
            lap = polyadd(scale(g, a), [F(m)])
            phase_numerator = sub(mul(speed, numerator), mul(lap, denominator))
            lower = sub(scale(phase_numerator, 8), denominator)
            upper = sub(scale(denominator, 7), scale(phase_numerator, 8))
            lower_shift = shift(lower, amin)
            upper_shift = shift(upper, amin)
            assert all(c >= 0 for c in lower_shift+upper_shift)
            records.append({"original_row": [a, b], "speed_coefficients": speed,
                "lap_coefficients": lap, "phase_numerator_coefficients": phase_numerator,
                "eight_times_lower_margin_numerator_at_a_min_plus_s": lower_shift,
                "eight_times_upper_margin_numerator_at_a_min_plus_s": upper_shift})
        certificates.append({"residue_mod_4": r, "a_min": amin,
             "q": "4*a+r", "g_coefficients": g, "time_numerator": numerator,
             "time_denominator": denominator,
             "coefficient_order": "ascending powers of a; margin checks use s=a-a_min>=0",
             "rows": records})
    return certificates


def run():
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    segments = source["cover"]["chosen_segments"]
    assert [s["id"] for s in segments] == ["P1:E1-3:K1", "P3:E0-1:K2"]
    assert source["display_order"] == list(ORDER)
    endpoints = endpoint_proof(segments)
    clocks = derive_clock_formulas(segments)
    residues = residue_proof(segments[0])
    controls = []
    wrong_clock_failures = []
    wrong_lap_failures = []
    by_q = {item["certificate"]["q"]: item for item in source["physical_controls"]}
    assert sorted(by_q) == list(range(2, 26))
    for q in range(2, 26):
        segment, g, lam, (u, v), attempts = own_select(segments, q)
        expected = by_q[q]["certificate"]
        assert u == F(expected["time"])
        assert (u, v) == tuple(F(x) for x in expected["point"])
        assert lam == F(expected["parameter"])
        assert g == expected["g"] == -expected["H"]
        assert segment["id"] == expected["segment"]
        assert len(attempts) == expected["attempts"]
        assert 0 < u < 1 and 0 < v <= F(1, 2)
        assert (q*u).numerator // (q*u).denominator == g
        own = physical(q, u)
        reflected = physical(q, 1-u)
        assert own["minimum"] == reflected["minimum"] == Z
        native_phases = [a*v+b*u-m for (a,b),m in zip(ROWS, segment["labels"])]
        native_laps = [m+a*g for (a,b),m in zip(ROWS, segment["labels"])]
        native_wrong_laps = [m+b*g for (a,b),m in zip(ROWS, segment["labels"])]
        phases = [native_phases[i] for i in ORDER]
        laps = [native_laps[i] for i in ORDER]
        wrong_laps = [native_wrong_laps[i] for i in ORDER]
        assert phases == own["phases"] and laps == own["laps"]
        assert laps == expected["display_laps"]
        assert [1-p for p in phases] == reflected["phases"]
        assert [s-1-l for s,l in zip(own["speeds"], laps)] == reflected["laps"]
        gr = q-1-g
        reflected_native_laps = [a+b-1-m+a*gr for (a,b),m in zip(ROWS,segment["labels"])]
        assert [reflected_native_laps[i] for i in ORDER] == reflected["laps"]
        for fresh, old in zip((own, reflected), by_q[q]["physical"]):
            assert fresh["time"] == F(old["time"])
            assert fresh["laps"] == old["laps"]
            assert fresh["phases"] == [F(x) for x in old["phases"]]
            assert fresh["distances"] == [F(x) for x in old["distances"]]
        wrong_clock = physical(q, v)
        if wrong_clock["minimum"] < Z:
            bad = [{"speed": s, "phase": p, "distance": d}
                   for s,p,d in zip(wrong_clock["speeds"],wrong_clock["phases"],wrong_clock["distances"]) if d < Z]
            wrong_clock_failures.append({"q":q, "wrong_time_x":v,
                 "correct_time_y":u, "minimum": wrong_clock["minimum"], "unsafe_runners":bad})
        if wrong_laps != laps:
            bad = [{"speed":s,"wrong_lap":wl,"actual_lap":l,
                    "phase_from_wrong_lap":s*u-wl}
                   for s,wl,l in zip(own["speeds"],wrong_laps,laps) if wl != l]
            wrong_lap_failures.append({"q":q,"time":u,"g":g,"mismatches":bad})
        controls.append({"q":q,"segment":segment["id"],"g":g,"parameter":lam,
             "native_point_x_y":[v,u],"attempts":attempts,
             "selected":own,"reflected":reflected})
    assert controls[0]["selected"]["time"] == F(9,40)
    assert all(c["segment"] == segments[0]["id"] for c in controls[1:])
    assert wrong_clock_failures and wrong_lap_failures
    return {
       "status":"PASS: separately authored internal AI physical check",
       "source_sha256":hashlib.sha256(source_bytes).hexdigest(),
       "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       "read_order":"Governance and protocol; generic physical derivation saved; coordinator freeze notification; transfer.json claims; no transfer.py/discovery imports or old B optimum witness files.",
       "scope":"One B-ray 1/8-safe witness, q integer>=2; direct physical controls only q=2,...,25 and reflections.",
       "summary":{"q_controls":24,"physical_times":48,"direct_phase_checks":336,
           "endpoint_band_inequalities":56,"infinite_residue_domains":4,
           "symbolic_band_inequalities":56,"wrong_clock_failure_count":len(wrong_clock_failures),
           "wrong_lap_failure_count":len(wrong_lap_failures)},
       "universal_physical_identity":{
           "identity":"(a*q+b)*u - (m+a*(q*u-v)) = a*v+b*u-m",
           "assumptions":"q and g=q*u-v integers; local phase in [1/8,7/8]",
           "conclusion":"m+a*g is the actual physical floor; t=u=y",
           "reflection":"phase'=1-phase; ell'=speed-1-ell; g'=q-1-g",
           "clock_warning":"v=x<=1/2 does not imply u=t<=1/2"},
       "coverage_argument":{
           "primary_interval":"[(6q-5)/24,(4q-1)/8]",
           "primary_width":"(3q+1)/12 >=1 for q>=4",
           "primary_integer":"ceil((6q-5)/24)=ceil(q/4)",
           "small_prefix":"q=3 hits g=1; q=2 primary misses and fallback hits g=0",
           "primary_time":"(24*g+7)/(8*(3*q+1))",
           "fallback_at_2":"t=9/40; g=0; native (x,y)=(9/20,9/40)"},
       "endpoint_certificates":endpoints,"independently_derived_clock_formulas":clocks,
       "unbounded_physical_residue_certificates":residues,
       "controls":controls,"wrong_clock_failures":wrong_clock_failures,
       "wrong_lap_failures":wrong_lap_failures,
       "limits":"Not an optimum proof, all-witness enumeration, new-family result, formal verification, novelty assessment, independent human review, or blind study."}


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k:encode(v) for k,v in obj.items()}
    if isinstance(obj, (tuple,list)):
        return [encode(v) for v in obj]
    return obj


if __name__ == "__main__":
    output = run()
    (HERE / "physical_review.json").write_text(json.dumps(encode(output),indent=2,sort_keys=True)+"\n")
    print(json.dumps(output["summary"],sort_keys=True))
