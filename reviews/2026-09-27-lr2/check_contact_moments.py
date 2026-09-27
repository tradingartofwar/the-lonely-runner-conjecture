"""Exact duration-versus-contact audit for two fixed triples on J.

Standard library only. The note CONTACT_MOMENTS_2026_09_27.md proves the
denominator criterion and finite reduction; no bounded speed scan is used
to justify an unbounded conclusion.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import sys

D = F(1, 8)
J = (F(9, 32), F(3, 8))
CORE = (1, 4, 5)
FIXED = (*CORE, 6, 7, 3)
I6 = (F(5, 16), F(17, 48))
I7 = (J[0], F(17, 56))
I3 = (F(7, 24), J[1])
K = (I3[0], I7[1])
REGIONS = ((J,), (I6,), (I7,), (I3,))
FIXED_REGIONS = ((J,), (I6,), (I7,), (), (I3,), (I6,), (K,), ())
B10 = (F(23, 80), F(5, 16))
B28 = ((J[0], F(65, 224)), (F(71, 224), F(73, 224)), (F(79, 224), F(81, 224)))
ALT_REGIONS = ((J,), (I3,), (B10,), ((I3[0], B10[1]),), B28, B28[1:],
               ((B10[0], B28[0][1]),), ())
ALT_PERIOD = lcm(*(q.denominator for region in ALT_REGIONS for I in region for q in I))
assert ALT_PERIOD == 3360
P = lcm(*(q.denominator for region in REGIONS for I in region for q in I))
assert P == 672


def floor(q):
    return q.numerator//q.denominator


def primitive(z):
    z += D
    n = floor(z)
    return F(n, 4)+min(z-n, F(1, 4))


def duration(y, region):
    return sum(((primitive(y*b)-primitive(y*a))/y for a, b in region), F(0))


def length(region):
    return sum((b-a for a, b in region), F(0))


def distance(z):
    q = z % 1
    return min(q, 1-q)


def from_summary(M):
    Dy, O6y, O7y, O3y = M
    return [length(A) for A in FIXED_REGIONS] + [Dy, O6y, O7y, F(0), O3y, O6y, O7y+O3y-Dy, F(0)]


def all_moments(y):
    return [length(A) for A in FIXED_REGIONS]+[duration(y, A) for A in FIXED_REGIONS]


def snapshot(y, anchor=(6, 7, 3)):
    """Independently partition phase events and retain valid endpoints."""
    assert y > 0 and y not in (*CORE, *anchor)
    extras = (*anchor, y)
    speeds = (*CORE, *extras)
    points = set(J)
    for v in speeds:
        for m in range(floor(v*J[0])-1, floor(v*J[1])+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if J[0] < t < J[1]:
                    points.add(t)
    points = sorted(points)
    masses = [F(0)]*16
    for a, b in zip(points, points[1:]):
        t = (a+b)/2
        assert all(distance(v*t) >= D for v in CORE)
        state = sum(1 << i for i, v in enumerate(extras) if distance(v*t) < D)
        assert state & 7 in ((2, 4, 5, 6) if anchor == (6, 7, 3) else (1, 2, 3, 4, 5, 6))
        masses[state] += b-a
    components = [(t, t) for t in points if all(distance(v*t) >= D for v in speeds)]
    assert masses[0] == 0
    moments = [sum(z for s, z in enumerate(masses) if s & mask == mask) for mask in range(16)]
    M = tuple(moments[i] for i in (8, 9, 10, 12))
    if anchor == (6, 7, 3):
        assert components == ([] if y % 8 == 0 else [(J[1], J[1])])
        assert moments == all_moments(y) == from_summary(M)
    else:
        assert anchor == (3, 10, 28) and y % 1680 == 0
        assert components == ([(J[0], J[0])] if (y//1680) % 2 else [])
        assert moments == [length(A) for A in ALT_REGIONS]+[duration(y, A) for A in ALT_REGIONS]
        assert moments[8:] == [q/4 for q in moments[:8]]
    assert (M[0].denominator % 64 == 0) == (y % 8 == 0)
    return {"y": y, "fixed_blockers": anchor, "summary": M, "D_y_denominator": M[0].denominator,
            "moments_by_mask": moments, "state_durations_by_mask": masses,
            "clear_duration": masses[0], "components": components,
            "variable_endpoint_phases": [(y*t) % 1 for t in J],
            "all_nonzero_relative_pair_gcds": [gcd(v, w) for v, w in combinations(speeds, 2)],
            "contact_controllers": [
                {"time": t, "speed": v, "phase": (v*t) % 1,
                 "direction": "enters safety" if (v*t) % 1 == D else "leaves safety"}
                for t, _ in components for v in speeds if distance(v*t) == D]}


def safe_cell(y):
    speeds = (1, 3, 4, 5, 10, 28, y)
    t = J[0]
    rows = []
    for v in speeds:
        k = floor(v*t)
        a, b = (k+D)/v, (k+1-D)/v
        assert a <= t <= b
        rows.append({"speed": v, "lap": k, "lower": a, "upper": b})
    a = max(J[0], *(r["lower"] for r in rows))
    b = min(J[1], *(r["upper"] for r in rows))
    assert a == b == t
    assert [r["speed"] for r in rows if r["lower"] == a] == [4]
    assert [r["speed"] for r in rows if r["upper"] == b] == [28]
    return {"speeds": speeds, "rows": rows, "cell": [a, b], "width": b-a,
            "lower_controller": 4, "upper_controller": 28}


def bezout(a, b):
    r0, r1, u0, u1, v0, v1 = a, b, 1, 0, 0, 1
    while r1:
        q = r0//r1
        r0, r1 = r1, r0-q*r1
        u0, u1 = u1, u0-q*u1
        v0, v1 = v1, v0-q*v1
    assert r0 == a*u0+b*v0 == 1
    return u0, v0


def psi_grid(period):
    result = [((k+period//8)//period)*period + 4*min((k+period//8) % period, period//4)-k
              for k in range(period)]
    assert all(F(q, 4*period) == primitive(F(k, period))-F(k, 4*period)
               for k, q in enumerate(result))
    return result


def main():
    # A 32-residue congruence certificate for the all-y denominator argument.
    # D_y=(3y+c[r])/(128y), r=y mod 32. Adding 32 to y adds 96 to the numerator.
    p32 = psi_grid(32)
    denominator_rows = []
    for r in range(32):
        c = p32[(12*r) % 32]-p32[(9*r) % 32]
        if r % 16 == 0:
            assert c == 0
            conclusion = "D_y=3/128; denominator has exactly seven factors of 2"
        elif r % 8 == 0:
            assert c == (-8 if r == 8 else 8)
            assert (3*r+c) % 32 == 16 and 96 % 32 == 0
            conclusion = "denominator has exactly six factors of 2"
        else:
            v = gcd(r, 8)  # 1,2,4: the entire 2-power dividing y in this class
            assert (3*r+c) % (4*v) == 0 and 96 % (4*v) == 0
            conclusion = "denominator has at most five factors of 2"
        y = r+32
        assert duration(y, (J,)) == F(3*y+c, 128*y)
        denominator_rows.append({"residue": r, "coefficient": c, "conclusion": conclusion})

    # All duration moments are determined by the four variable single/pair entries.
    psi = psi_grid(P)
    grid = [tuple((int(a*P), int(b*P)) for a, b in region) for region in REGIONS]
    rows = []
    groups = defaultdict(list)
    zeros = []
    for r in range(P):
        e = tuple(sum(psi[(r*b) % P]-psi[(r*a) % P] for a, b in region) for region in grid)
        g = gcd(*e)
        row = (r, g, e)
        rows.append(row)
        if g:
            groups[tuple(c//g for c in e)].append(row)
        else:
            zeros.append(row)
        y = r+P
        M = tuple(duration(y, A) for A in REGIONS)
        assert M == tuple(length(A)/4+F(c, 4*P*y) for A, c in zip(REGIONS, e))
        assert from_summary(M) == all_moments(y)
        assert (M[0].denominator % 64 == 0) == (y % 8 == 0)
    assert [r for r, g, e in zeros] == [0, 336]
    assert len(groups) == 534
    # Even before enforcing speed congruences, no positive proportionality
    # class of complete summaries mixes the two endpoint outcomes.
    assert all(len({r % 8 == 0 for r, g, e in group}) == 1 for group in groups.values())

    families = []
    candidates = 0
    for group in groups.values():
        for (r, g, e), (s, h, f) in combinations(group, 2):
            candidates += 1
            d = gcd(g, h)
            a, b = g//d, h//d
            if a == b:
                continue
            solutions = [k for k in range(P) if (a*k-r) % P == (b*k-s) % P == 0]
            assert bool(solutions) == ((b*r-a*s) % P == 0)
            if not solutions:
                continue
            u, v = bezout(a, b)
            k0 = (u*r+v*s) % P
            assert solutions == [k0] and k0 > 0
            if a > b:
                r, s, a, b = s, r, b, a
            first = k0
            while a*first in FIXED or b*first in FIXED:
                first += P
            for k in (first, first+P):
                y, z = a*k, b*k
                assert all_moments(y) == all_moments(z)
                assert (y % 8 == 0) == (z % 8 == 0)
            families.append({"residues": [r, s], "multipliers": [a, b], "k_residue": k0,
                             "k_modulus": P, "first_admissible_k": first,
                             "first_speeds": [a*first, b*first],
                             "outcome": "empty" if r % 8 == 0 else "singleton at 3/8"})
    families.sort(key=lambda row: (max(row["first_speeds"]), row["first_speeds"]))
    assert candidates == 168 and len(families) == 34
    assert Counter(row["outcome"] for row in families) == {"empty": 12, "singleton at 3/8": 22}
    assert families[0]["first_speeds"] == [48, 144]
    assert families[1]["first_speeds"] == [95, 190]

    controls = [snapshot(y) for y in (2, 8, 10, 24, 48, 144, 95, 190, 336, 672, 673)]
    by_y = {row["y"]: row for row in controls}
    for y, z in ((48, 144), (95, 190), (336, 672)):
        assert by_y[y]["moments_by_mask"] == by_y[z]["moments_by_mask"]
        assert by_y[y]["components"] == by_y[z]["components"]
    # Partial-summary failures: a single pair overlap, or two other pairs,
    # can match across opposite outcomes. D_y is the decisive single statistic.
    assert by_y[2]["summary"][1:3] == by_y[8]["summary"][1:3] == (F(0), F(0))
    assert by_y[10]["summary"][3] == by_y[24]["summary"][3] == F(1, 48)

    # All moments approach an empty configuration's vector along contact cases.
    # Formula checks only for large m; no large-speed phase enumeration.
    proximity = []
    for m in (1, 10**6, 10**20):
        y, z = P*m, P*m+1
        A, B = all_moments(y), all_moments(z)
        assert A[:8] == B[:8]
        assert all(B[i] == A[i]*(1-F(1, z)) for i in range(8, 16))
        error = max(abs(a-b) for a, b in zip(A, B))
        assert error == F(3, 128*z)
        assert y % 8 == 0 and z % 8 != 0
        proximity.append({"m": m, "speeds": [y, z], "empty_D_y": A[8],
                          "contact_D_z": B[8], "maximum_moment_difference": error})

    # The first anchor masks a real loss at the LEFT endpoint: these have
    # identical full moments, but y=336 is safe there and y=672 blocks there.
    assert by_y[336]["variable_endpoint_phases"][0] == F(1, 2)
    assert by_y[672]["variable_endpoint_phases"][0] == 0
    assert distance(7*J[0]) < D  # fixed runner 7 makes that distinction irrelevant here

    # Make that lost left-endpoint distinction decisive with a second fixed triple.
    # Three overlapping blocking intervals cover the entire open J. Both ends
    # remain safe for the fixed runners; the other B28 occurrences are redundant.
    assert J[0] < B10[0] < B28[0][1] < I3[0] < B10[1] < J[1]
    assert all(distance(v*t) >= D for v in (*CORE, 3, 10, 28) for t in J)
    endpoint_grid = sorted({t for A in ALT_REGIONS for I in A for t in I})
    endpoint_rows = []
    for t in endpoint_grid:
        assert (2*1680*t).denominator == 1
        phase = (1680*t) % 1
        assert phase in (F(0), F(1, 2))
        assert primitive(phase)-phase/4 == D
        endpoint_rows.append({"time": t, "phase_for_1680": phase, "periodic_correction": D})
    boundary_controls = [snapshot(1680*h, (3, 10, 28)) for h in (1, 2, 3, 4)]
    for A, B in zip(boundary_controls, boundary_controls[1:]):
        assert A["moments_by_mask"] == B["moments_by_mask"]
        assert A["state_durations_by_mask"] == B["state_durations_by_mask"]
        assert A["all_nonzero_relative_pair_gcds"] == B["all_nonzero_relative_pair_gcds"]
        assert A["components"] != B["components"]
    cells = [safe_cell(1680), safe_cell(5040)]
    outside_witnesses = []
    for y in (1680, 3360):
        t = F(11, 64)
        clearance = min(distance(v*t) for v in (*CORE, 3, 10, 28, y))
        assert clearance == F(9, 64) > D
        outside_witnesses.append({"y": y, "time": t, "minimum_distance": clearance, "margin": clearance-D})

    result = {"date": "2026-09-27", "baseline_commit": "8a4b1415aff92a53473237183b18076cdc2d8537",
              "status": "Exact physical empty/contact counterexample and scoped residue classification; unbounded arguments are proof candidates awaiting independent review. No novelty claim.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "core": CORE, "fixed_blockers": [6, 7, 3], "window": J, "threshold": D,
              "variable_domain": "Positive integer y outside {1,3,4,5,6,7}; reference 0; common start.",
              "endpoint_rule": "F_J is empty iff 8 divides y, otherwise F_J={3/8}; U=0 always.",
              "denominator_rule": "For reduced D_y=p/q, F_J is empty iff 64 divides q; q=1 when D_y=0.",
              "denominator_certificate": denominator_rows, "period": P,
              "fixed_regions_by_mask": FIXED_REGIONS,
              "coefficient_rows_sha256": hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest(),
              "nonzero_ray_count": len(groups), "ray_size_counts": dict(sorted(Counter(map(len, groups.values())).items())),
              "zero_coefficient_rows": zeros, "zero_class": "All positive multiples of 336; all have empty J and identical complete moments.",
              "same_ray_residue_pairs": candidates,
              "family_counts": {"all": 34, "empty": 12, "singleton": 22, "mixed_outcome": 0},
              "collision_families": families, "physical_controls": controls, "closeness_controls": proximity,
              "constructive_boundary_family": {"fixed_blockers": [3, 10, 28], "period": ALT_PERIOD,
                  "fixed_regions_by_mask": ALT_REGIONS, "endpoint_certificate": endpoint_rows,
                  "variable_speeds": "y=1680h for every positive integer h",
                  "statement": "All joint duration moments and all pair gcds among the seven nonzero relative speeds are constant. F_J={9/32} for odd h and is empty for even h.",
                  "controls": boundary_controls, "closed_safe_cells": cells,
                  "strict_witnesses_outside_J": outside_witnesses},
              "limits": "The first anchor excludes exact complete-moment empty/contact matches. The second anchor supplies them physically on the same J and threshold. This is local, selected-reference information loss, not a counterexample to Lonely Runner. Right-endpoint status is encoded by single-duration denominators; left-endpoint status need not be. Full chronology, reduced ratios, and speeds are not matched."}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("contact_moments.json").read_text())
        print("PASS: denominator certificate; 672 residues and 34 same-outcome matches in first anchor; closeness controls; four second-anchor controls with identical full moments and opposite local existence; two closed safe cells.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
