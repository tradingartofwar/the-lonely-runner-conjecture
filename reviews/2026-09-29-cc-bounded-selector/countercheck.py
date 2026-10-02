"""Physical-time polynomial check without importing selector or atlas code.

All coefficients are integers. On q=8a+r the proposed time is N(a)/D(a),
and candidate physical laps are integer affine polynomials. Compute v*N-lap*D,
then certify both closed band inequalities on the entire residue domain.
This is a second structure, not a second author or independent review.
"""

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def add(p, q):
    return tuple((p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q))))


def scale(c, p):
    return tuple(c * v for v in p)


def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return tuple(out)


def affine_certificate(p, a_min):
    assert all(v == 0 for v in p[2:]), p
    constant, slope = p[0], (p[1] if len(p) > 1 else 0)
    assert slope >= 0 and constant + slope * a_min >= 0, (p, a_min)
    return {"constant": constant, "slope": slope, "a_min": a_min,
            "minimum": constant + slope * a_min}


def main():
    records = []
    for r in range(8):
        e = 1 if r >= 5 else 0
        a_min = 1 if r in (0, 1, 5) else 0
        numerator, denominator = (8 * e + 7, 8), (8 * r + 24, 64)
        speeds = ((1,), (r, 8), (r + 1, 8), (r + 2, 8), (r + 3, 8),
                  (2 * r + 3, 16), (2 * r + 5, 16))
        h = (e, 1)
        laps = ((0,), h, h, h, h, (2 * e + 1, 2), (2 * e + 1, 2))
        assert denominator[0] + denominator[1] * a_min > 0
        assert numerator[0] + numerator[1] * a_min > 0
        folded = affine_certificate(add(denominator, scale(-2, numerator)), a_min)
        rows = []
        for speed, lap in zip(speeds, laps):
            phase = add(mul(speed, numerator), scale(-1, mul(lap, denominator)))
            lower = add(scale(8, phase), scale(-1, denominator))
            upper = add(scale(7, denominator), scale(-8, phase))
            rows.append({"speed": speed, "lap": lap, "phase_numerator": phase,
                         "lower_certificate": affine_certificate(lower, a_min),
                         "upper_certificate": affine_certificate(upper, a_min)})
        # The fifth physical phase is identically 7/8, not just >=1/8-safe.
        assert all(v == 0 for v in add(scale(8, rows[4]["phase_numerator"]), scale(-7, denominator)))
        records.append({"r": r, "a_min": a_min, "time_numerator": numerator,
                        "time_denominator": denominator, "folded_time": folded, "rows": rows})
    # Exactly one q>=2 falls outside the eight primary domains: q=5.
    # This is checked by comparing their starts, not by scanning q.
    omitted = []
    for r, record in enumerate(records):
        base_start = 1 if r in (0, 1) else 0
        omitted.extend(8 * a + r for a in range(base_start, record["a_min"]))
    assert omitted == [5]
    q, t = 5, F(25, 56)
    speeds = (1, q, q + 1, q + 2, q + 3, 2 * q + 3, 2 * q + 5)
    laps = tuple((v * t).numerator // (v * t).denominator for v in speeds)
    phases = tuple(v * t - ell for v, ell in zip(speeds, laps))
    assert laps == (0, 2, 2, 3, 3, 5, 6)
    assert all(F(1, 8) <= phase <= F(7, 8) for phase in phases)
    assert min(min(phase, 1 - phase) for phase in phases) == F(1, 8)
    controls = []
    for q in range(2, 26):
        a, r = divmod(q, 8)
        e = int(r >= 5)
        time = F(25, 56) if q == 5 else F(8 * (a + e) + 7, 8 * (q + 3))
        velocities = (1, q, q + 1, q + 2, q + 3, 2 * q + 3, 2 * q + 5)
        distances = []
        for v in velocities:
            pos = v * time
            phase = pos - pos.numerator // pos.denominator
            distances.append(min(phase, 1 - phase))
        assert min(distances) == F(1, 8)
        controls.append({"q": q, "time": str(time), "minimum_distance": str(min(distances))})
    out = {"status": "PASS: direct physical polynomial certificate",
           "authorship": "Same coordinator; no imports from selector, geometry or optimum code",
           "coefficient_order": "constant, a, a^2; trailing zero coefficients retained",
           "unbounded_primary_domains": records, "primary_omitted_q": omitted,
           "fallback": {"q": 5, "time": str(t), "laps": laps, "phases": list(map(str, phases))},
           "controls": controls,
           "summary": {"unbounded_residue_domains": 8, "physical_band_inequalities": 112,
                       "fallback_q": 5, "physical_control_count": 24},
           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
