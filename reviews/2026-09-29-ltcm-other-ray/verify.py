#!/usr/bin/env python3
"""Recover the unsaved V(q,1) formulas with exact, explicitly bounded checks.

Default: verify q=2,...,150 and print a JSON record to stdout; no file writes.
No project imports or third-party packages. The opposing-contact approach was
read in the archived Ultra physical checker; this is not independent review.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

BASE_COMMIT = "908a089ac39f9af796d6261d22f8b37009b1eb53"
Q_VALUES = range(2, 151)


def speeds(q):
    return (1, q, q + 1, 2*q + 1, 3*q + 1, 3*q + 2, 5*q + 2)


def proposed(q):
    residue = q % 6
    if residue == 0:
        return F(2*q, 3*(4*q+1)), F(4*q//3 + 1, 4*q+1)
    if residue == 2:
        return F(5*q+2, 6*(5*q+3)), F(5*q+8, 6*(5*q+3))
    if residue == 5:
        return F(q, 3*(2*q+1)), F(2*q, 3*(2*q+1))
    return F(1, 6), F(1, 6)


def certificate(vs, t):
    n, d = t.numerator, t.denominator
    remainders = [v*n % d for v in vs]
    distances = [F(min(r, d-r), d) for r in remainders]
    value = min(distances)
    return {
        "time": t,
        "laps": [v*n//d for v in vs],
        "phases": [F(r, d) for r in remainders],
        "distances": distances,
        "minimum": value,
        "active_speeds": [v for v, x in zip(vs, distances) if x == value],
    }


def exact_maximum(vs):
    """Exhaust opposing contacts and tent peaks on the reflection half-period.

    A positive local maximum is an individual tent peak or a meeting of active
    positive and negative slopes. The latter has (v+w)t integral. We include
    every such integer time, even those that fail the opposing-phase test.
    The proposed formula/witness is never used to generate or prune candidates.
    """
    times = {F(0), F(1, 2)}
    for v, w in combinations(vs, 2):
        denominator = v + w
        times.update(F(n, denominator) for n in range(1, denominator//2 + 1))
    for v in vs:
        times.update(F(n, 2*v) for n in range(1, v + 1, 2))
    best_n, best_d, winners = 0, 1, []
    for t in sorted(times):
        n, d = t.numerator, t.denominator
        remainders = [v*n % d for v in vs]
        value_n = min(min(r, d-r) for r in remainders)
        difference = value_n*best_d - best_n*d
        if difference > 0:
            best_n, best_d, winners = value_n, d, [t]
        elif difference == 0:
            winners.append(t)
    return F(best_n, best_d), sorted(set(winners + [1-t for t in winners])), len(times)


# Polynomials use coefficients (constant, linear), i.e. b+a*k.
CHARTS = {
    0: dict(k_min=1, N=(1,8), D=(1,24), A=(0,4),
            laps=((0,0),(0,2),(0,2),(0,4),(0,6),(1,6),(1,10)),
            remainders=((1,8),(0,4),(1,12),(1,16),(1,20),(1,4),(1,12))),
    1: dict(k_min=1, N=(1,0), D=(6,0), A=(1,0),
            laps=((0,0),(0,1),(0,1),(0,2),(0,3),(0,3),(1,5)),
            remainders=tuple((r,0) for r in (1,1,2,3,4,5,1))),
    2: dict(k_min=0, N=(3,5), D=(13,30), A=(2,5),
            laps=((0,0),(0,1),(0,1),(1,2),(1,3),(1,3),(2,5)),
            remainders=((3,5),(6,15),(9,20),(2,5),(8,20),(11,25),(10,25))),
    3: dict(k_min=0, N=(1,0), D=(6,0), A=(1,0),
            laps=((0,0),(0,1),(0,1),(1,2),(1,3),(1,3),(2,5)),
            remainders=tuple((r,0) for r in (1,3,4,1,4,5,5))),
    4: dict(k_min=0, N=(1,0), D=(6,0), A=(1,0),
            laps=((0,0),(0,1),(0,1),(1,2),(2,3),(2,3),(3,5)),
            remainders=tuple((r,0) for r in (1,4,5,3,1,2,4))),
    5: dict(k_min=0, N=(10,12), D=(33,36), A=(5,6),
            laps=((0,0),(1,2),(1,2),(3,4),(4,6),(5,6),(8,10)),
            remainders=((10,12),(17,18),(27,30),(11,12),(28,30),(5,6),(6,6))),
}


def multiply(a, b):
    return (a[0]*b[0], a[0]*b[1] + a[1]*b[0], a[1]*b[1])


def at(poly, k):
    return sum(c*k**i for i, c in enumerate(poly))


def nonnegative(poly, k_min):
    assert len(poly) == 2
    assert poly[1] >= 0 and at(poly, k_min) >= 0, (poly, k_min)
    return {"coefficients": poly, "slope": poly[1], "value_at_k_min": at(poly, k_min)}


def symbolic_witnesses():
    """Polynomial identities and affine sign certificates on unbounded domains."""
    rows = []
    for residue, chart in CHARTS.items():
        lo, n, d, a = (chart[key] for key in ("k_min", "N", "D", "A"))
        assert d[1] >= 0 and at(d, lo) > 0
        assert a[1] >= 0 and at(a, lo) > 0
        v_polys = ((1,0),(residue,6),(residue+1,6),(2*residue+1,12),
                   (3*residue+1,18),(3*residue+2,18),(5*residue+2,30))
        coordinate_certificates = []
        for v, lap, rem in zip(v_polys, chart["laps"], chart["remainders"]):
            lhs, product = multiply(v, n), multiply(lap, d)
            rhs = (product[0]+rem[0], product[1]+rem[1], product[2])
            assert lhs == rhs, (residue, v, lap, rem)
            lower = tuple(rem[i]-a[i] for i in range(2))
            upper = tuple(d[i]-a[i]-rem[i] for i in range(2))
            coordinate_certificates.append({
                "speed_coefficients": v, "lap_coefficients": lap,
                "phase_numerator_coefficients": rem, "identity_vN_equals_lapD_plus_R": True,
                "R_minus_A": nonnegative(lower, lo),
                "D_minus_A_minus_R": nonnegative(upper, lo),
            })
        assert any(rem == a or tuple(d[i]-rem[i] for i in range(2)) == a
                   for rem in chart["remainders"])
        rows.append({"residue": residue, **chart, "coordinates": coordinate_certificates})
    return rows


def main():
    symbolic = symbolic_witnesses()
    cases = []
    for q in Q_VALUES:
        vs = speeds(q)
        maximum, times, count = exact_maximum(vs)
        expected, time = proposed(q)
        witness = certificate(vs, time)
        assert maximum == expected and time in times, (q, maximum, expected)
        assert witness["minimum"] == expected
        chart, k = CHARTS[q % 6], q//6
        assert time == F(at(chart["N"], k), at(chart["D"], k))
        assert expected == F(at(chart["A"], k), at(chart["D"], k))
        assert witness["laps"] == [at(m, k) for m in chart["laps"]]
        cases.append({"q": q, "speeds": vs, "maximum": maximum,
                      "maximizing_times": times, "candidate_times_in_half_period": count,
                      "formula_matches": True, "witness": witness})
    controls = []
    for q, original_expected in ((2, F(1,6)), (4, F(1,8))):
        original = (1, q, q+1, q+2, q+3, 2*q+3, 2*q+5)
        maximum, times, count = exact_maximum(original)
        other = cases[q-2]["maximum"]
        assert maximum == original_expected and maximum != other
        controls.append({"q": q, "original_ray_speeds": original,
                         "original_ray_maximum": maximum, "other_ray_maximum": other,
                         "different_objectives": True})
    result = {
        "base_commit": BASE_COMMIT,
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "bounded exact maximum checks; symbolic lower-bound certificates; upper bound open",
        "scope": {"q_min": 2, "q_max": 150, "case_count": len(cases),
                  "total_runners": 8, "selected_reference": 0,
                  "exact_maximum_mismatches": 0,
                  "candidate_times_in_half_period": sum(c["candidate_times_in_half_period"] for c in cases),
                  "symbolic_phase_identities": 42, "symbolic_safe_band_inequalities": 84},
        "symbolic_witness_charts": symbolic,
        "family_distinction_controls": controls,
        "cases": cases,
    }
    print(json.dumps(result, indent=2, default=lambda x: str(x) if isinstance(x, F) else x))


if __name__ == "__main__":
    main()
