"""Exact orbit-map controls; fixed protocol inputs, no parameter search.

Run from any directory: python orbit_checks.py
Writes orbit_checks.json beside this file. The infinite claim is proved in
orbit_review.md; these finite controls are implementation/sign checks only.
"""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
CONTROLS = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1),
            (2, 3), (3, 1), (1, 6), (2, 5), (3, 2), (3, 4),
            (4, 3), (5, 2), (5, 7), (3, 5), (4, 6), (6, 10))


def floor(v):
    return v.numerator // v.denominator


def ceil(v):
    return -floor(-v)


def bezout(a, b):
    old_r, rem = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    divisions = 0
    while rem:
        q = old_r // rem
        old_r, rem = rem, old_r - q * rem
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        divisions += 1
    assert old_r == 1 and old_s * a + old_t * b == 1
    return old_s, old_t, divisions


def point(P, Q):
    h = ceil(F(3 * (Q-P), 8))
    if h <= F(4 * Q-P, 8):
        x = F(8 * h + 9 * P, 8 * (Q+2*P))
        y = F(9, 8) - 2*x
        return "P3", h, x, y, (0, 0, 0, 1, 1, 1, 2)
    h = ceil(F(Q-4*P, 8))
    assert h <= F(5*Q-6*P, 24)
    x = F(8*h+7*P, 8*(Q+3*P))
    y = F(7, 8)-3*x
    return "P1", h, x, y, (0, 0, 0, 0, 0, 1, 1)


def recover(P, Q, x, y, labels, r, s):
    h = Q*x-P*y
    assert h.denominator == 1
    T = r*x+s*y
    N = floor(T)
    tau = T-N
    Lp, Lq = -s*h-P*N, r*h-Q*N
    assert P*tau == x+Lp and Q*tau == y+Lq
    assert Lp == floor(P*tau) and Lq == floor(Q*tau)
    laps = tuple(m+(-a*s+b*r)*h-(a*P+b*Q)*N
                 for (a, b), m in zip(ROWS, labels))
    return T, N, tau, laps, Lp, Lq


def control(p, q):
    d = gcd(p, q)
    P, Q = p//d, q//d
    name, h, x, y, labels = point(P, Q)
    assert h == Q*x-P*y
    r, s, divisions = bezout(P, Q)
    T, N, tau, laps, Lp, Lq = recover(P, Q, x, y, labels, r, s)
    alt = recover(P, Q, x, y, labels, r+Q, s-P)
    assert alt[0] == T+h and alt[1] == N+h
    assert alt[2:] == (tau, laps, Lp, Lq)
    time = tau/d
    assert 0 < time < F(1, d)
    phases = tuple(a*x+b*y-m for (a, b), m in zip(ROWS, labels))
    speeds = tuple(a*p+b*q for a, b in ROWS)
    reflected_laps = tuple(v-1-ell for v, ell in zip(speeds, laps))
    for v, ell, ell_reflected, f in zip(speeds, laps, reflected_laps, phases):
        assert v*time-ell == f
        assert floor(v*time) == ell
        assert F(1, 8) <= f <= F(7, 8)
        assert v*(1-time)-ell_reflected == 1-f
        assert floor(v*(1-time)) == ell_reflected
    wrong_clock_results = {}
    for name_clock, clock in (("x", x), ("y", y)):
        clock_phases = tuple(v*clock-floor(v*clock) for v in speeds)
        wrong_clock_results[name_clock] = {
            "time": clock,
            "recovers_same_torus_point": (
                p*clock-floor(p*clock) == x and
                q*clock-floor(q*clock) == y),
            "safe": all(F(1, 8) <= f <= F(7, 8) for f in clock_phases),
            "minimum_distance": min(min(f, 1-f) for f in clock_phases),
        }
    return {"p": p, "q": q, "d": d, "P": P, "Q": Q,
            "repeated_speed_auxiliary": p == q, "segment": name,
            "x": x, "y": y, "h": h, "raw_orbit": q*x-p*y,
            "bezout": [r, s], "extended_euclid_divisions": divisions,
            "T": T, "N": N, "primitive_time": tau, "physical_time": time,
            "physical_laps": laps, "phases": phases,
            "reflected_time": 1-time, "reflected_laps": reflected_laps,
            "alternative_bezout_matches": True,
            "wrong_clocks": wrong_clock_results}


def negative_record(x, y):
    p, q, d = 2, 4, 2
    labels = (0, 0, 0, 1, 1, 1, 2)
    phases = tuple(a*x+b*y-m for (a, b), m in zip(ROWS, labels))
    assert y == F(9, 8)-2*x and F(3, 8) <= x <= F(1, 2)
    assert all(F(1, 8) <= f <= F(7, 8) for f in phases)
    raw = q*x-p*y
    return {"p": p, "q": q, "x": x, "y": y, "phases": phases,
            "raw_orbit": raw, "primitive_orbit": raw/d,
            "raw_integer": raw.denominator == 1,
            "raw_in_dZ": (raw/d).denominator == 1}


def clean(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {k: clean(w) for k, w in v.items()}
    if isinstance(v, (tuple, list)):
        return [clean(w) for w in v]
    return v


def main():
    records = [control(p, q) for p, q in CONTROLS]
    failed = negative_record(F(7, 16), F(1, 4))
    replacement = negative_record(F(13, 32), F(5, 16))
    assert failed["raw_orbit"] == F(5, 4) and not failed["raw_integer"]
    assert replacement["raw_orbit"] == 1
    assert replacement["raw_integer"] and not replacement["raw_in_dZ"]
    summary = {
        "controls": len(records), "distinct_speed_controls": 17,
        "phase_and_lap_checks": 7*len(records),
        "reflected_phase_and_lap_checks": 7*len(records),
        "alternative_bezout_controls": len(records),
        "wrong_clock_unsafe_counts": {
            clock: sum(not v["wrong_clocks"][clock]["safe"] for v in records)
            for clock in ("x", "y")},
        "wrong_clock_wrong_point_counts": {
            clock: sum(not v["wrong_clocks"][clock]["recovers_same_torus_point"]
                       for v in records) for clock in ("x", "y")},
        "all_declared_positive_checks_pass": True,
    }
    output = {"scope": "18 frozen controls only; no parameter search",
              "summary": summary,
              "failed_original_negative_fixture": failed,
              "replacement_negative_fixture": replacement,
              "records": records}
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(clean(output), indent=2, sort_keys=True)+"\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
