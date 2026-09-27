"""Exact all-speed collision reduction for extras (6,7,11,y) on J.

Standard library only; no project imports. The finite classification is backed
by the periodic-primitive derivation in notes/RESIDUE_COLLISIONS_2026_09_27.md.
It is not a speed scan. Independent phase partitions check the physical cases.
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
FIXED = (*CORE, 6, 7, 11)
I6 = (F(5, 16), F(17, 48))
I7 = (J[0], F(17, 56))
B11 = ((J[0], F(25, 88)), (F(31, 88), J[1]))
S = (F(17, 56), F(5, 16))
K6 = (F(31, 88), I6[1])
K7 = B11[0]
REGIONS = ((J,), (I6,), (I7,), B11, (S,), (K6,), (K7,))
P = lcm(*(q.denominator for region in REGIONS for I in region for q in I))
assert P == 7392


def floor(q):
    return q.numerator // q.denominator


def primitive(z):
    z += D
    n = floor(z)
    return F(n, 4) + min(z-n, F(1, 4))


def duration(v, region):
    return sum(((primitive(v*b)-primitive(v*a))/v for a, b in region), F(0))


def distance(z):
    q = z % 1
    return min(q, 1-q)


def snapshot(y):
    """Direct threshold-event partition, including valid isolated endpoints."""
    extras = (6, 7, 11, y)
    speeds = (*CORE, *extras)
    assert y > 0 and y not in FIXED
    points = set(J)
    for v in speeds:
        for m in range(floor(v*J[0])-1, floor(v*J[1])+2):
            for sign in (-1, 1):
                t = (m+sign*D)/v
                if J[0] < t < J[1]:
                    points.add(t)
    points = sorted(points)
    masses = [F(0)]*16
    pieces = []
    for a, b in zip(points, points[1:]):
        t = (a+b)/2
        assert all(distance(v*t) >= D for v in CORE)
        state = sum(1 << i for i, v in enumerate(extras) if distance(v*t) < D)
        masses[state] += b-a
        if state == 0:
            pieces.append((a, b))
    pieces.extend((t, t) for t in points if all(distance(v*t) >= D for v in speeds))
    components = []
    for a, b in sorted(pieces):
        if components and a <= components[-1][1]:
            components[-1] = (components[-1][0], max(b, components[-1][1]))
        else:
            components.append((a, b))
    moments = [sum(z for s, z in enumerate(masses) if s & mask == mask)
               for mask in range(16)]
    singles = [moments[1 << i] for i in range(4)]
    pairs = [moments[(1 << i) | (1 << j)] for i, j in combinations(range(4), 2)]
    triples = [moments[7], moments[11], moments[13], moments[14]]
    E = sum(singles)-(J[1]-J[0])
    R = sum(max(s.bit_count()-1, 0)*z for s, z in enumerate(masses))
    assert masses[0] == R-E == -E+sum(pairs)-sum(triples)+moments[15]
    assert masses[0] == sum((b-a for a, b in components), F(0))
    assert masses[0] == S[1]-S[0]-duration(y, (S,))
    assert (moments[8], moments[9], moments[10], moments[12]) == tuple(
        duration(y, region) for region in REGIONS[:4])
    assert (moments[13], moments[14]) == tuple(duration(y, region) for region in REGIONS[5:])
    assert moments[7] == moments[11] == moments[15] == 0
    contacts = [{"time": a, "controllers": [
        {"speed": v, "phase": (v*a) % 1,
         "direction": "enters safety" if (v*a) % 1 == D else "leaves safety"}
        for v in speeds if distance(v*a) == D]}
        for a, b in components if a == b]
    return {"y": y, "single_durations": singles, "pair_durations": pairs,
            "triple_durations": triples, "quadruple_duration": moments[15],
            "blocker_pair_gcds": [gcd(v, w) for v, w in combinations(extras, 2)],
            "moments_by_mask": moments, "state_durations_by_mask": masses,
            "E": E, "R": R, "clear_duration": masses[0], "components": components,
            "isolated_contacts": contacts}


def bezout(a, b):
    """a*u+b*v=1 for coprime positive multipliers."""
    r0, r1, u0, u1, v0, v1 = a, b, 1, 0, 0, 1
    while r1:
        q = r0//r1
        r0, r1 = r1, r0-q*r1
        u0, u1 = u1, u0-q*u1
        v0, v1 = v1, v0-q*v1
    assert r0 == a*u0+b*v0 == 1
    return u0, v0


def digest(obj):
    return hashlib.sha256(json.dumps(obj, default=str, separators=(",", ":")).encode()).hexdigest()


def main():
    # psi[k] = 4P*(C(k/P)-(k/P)/4). C(z)-z/4 is 1-periodic.
    psi = [((k+P//8)//P)*P + 4*min((k+P//8) % P, P//4)-k for k in range(P)]
    for k, q in enumerate(psi):
        assert F(q, 4*P) == primitive(F(k, P))-F(k, 4*P)
    lengths = [sum((b-a for a, b in region), F(0)) for region in REGIONS]
    grid = [tuple((int(a*P), int(b*P)) for a, b in region) for region in REGIONS]
    rays = defaultdict(list)
    zeros = []
    rows = []
    for r in range(P):
        e = tuple(sum(psi[(r*b) % P]-psi[(r*a) % P] for a, b in region) for region in grid)
        assert e[4] == e[0]-e[1]-e[2]-e[3]+e[5]+e[6]
        g = gcd(*e[:4])
        row = (r, g, e)
        rows.append(row)
        if g:
            rays[tuple(c//g for c in e[:4])].append(row)
        else:
            zeros.append(row)
        # All residue classes checked against rational endpoint integration.
        y = r+P
        assert all(duration(y, region) == length/4+F(c, 4*P*y)
                   for region, length, c in zip(REGIONS, lengths, e))
    assert [(r, e[4]) for r, g, e in zeros] == [(0, 0), (3696, 0)]
    assert len(rays) == 5186

    candidates = 0
    families = []
    for values in rays.values():
        for left, right in combinations(values, 2):
            candidates += 1
            r, g, e = left
            s, h, f = right
            d = gcd(g, h)
            a, b = g//d, h//d
            if a == b:
                # Distinct residues cannot represent equal speeds.
                assert r != s
                continue
            # Independent finite congruence countercheck: every possible k mod P.
            solutions = [k for k in range(P) if (a*k-r) % P == (b*k-s) % P == 0]
            compatible = (b*r-a*s) % P == 0
            assert bool(solutions) == compatible
            if not compatible:
                continue
            u, v = bezout(a, b)
            k0 = (u*r+v*s) % P
            assert solutions == [k0]
            if a > b:
                r, s, g, h, e, f, a, b = s, r, h, g, f, e, b, a
            assert 0 < k0 < P
            first_k = k0
            while a*first_k in FIXED or b*first_k in FIXED:
                first_k += P
            assert a*first_k >= 45
            gamma = (F(e[4], a)-F(f[4], b))/(4*P)
            for k in (first_k, first_k+P):
                y, z = a*k, b*k
                assert y % P == r and z % P == s
                assert all(duration(y, I) == duration(z, I) for I in REGIONS[:4])
                assert duration(y, (S,))-duration(z, (S,)) == gamma/k
            families.append({"residues": [r, s], "multipliers": [a, b],
                             "k_residue": k0, "k_modulus": P,
                             "first_admissible_k": first_k,
                             "first_speeds": [a*first_k, b*first_k],
                             "U_z_minus_U_y_times_k": gamma,
                             "same_blocker_pair_gcds": all(gcd(r, w) == gcd(s, w) for w in (6, 7, 11))})
    families.sort(key=lambda row: (max(row["first_speeds"]), row["first_speeds"]))
    assert candidates == 3240 and len(families) == 118
    assert sum(row["U_z_minus_U_y_times_k"] != 0 for row in families) == 62
    assert sum(row["same_blocker_pair_gcds"] for row in families) == 46
    assert sum(row["same_blocker_pair_gcds"] and row["U_z_minus_U_y_times_k"] != 0
               for row in families) == 8
    assert families[0]["first_speeds"] == [45, 90]
    assert families[0]["U_z_minus_U_y_times_k"] == F(1, 16)
    assert families[1]["first_speeds"] == [266, 532]
    assert families[1]["U_z_minus_U_y_times_k"] == F(1, 8)

    # For y>28, each connected blocked component has length 1/(4y)<|S|.
    # The connected interval S therefore has positive uncovered length.
    # Check the entire remaining finite range; these are old equality controls.
    small = [snapshot(y) for y in range(1, 29) if y not in FIXED]
    zero_duration = [row for row in small if row["clear_duration"] == 0]
    assert [row["y"] for row in zero_duration] == [3, 10, 13, 26]
    assert all(row["components"] for row in zero_duration)

    controls = []
    for y, z in ((45, 90), (266, 532), (336, 1344), (3696, 7392)):
        A, B = snapshot(y), snapshot(z)
        assert A["single_durations"] == B["single_durations"]
        assert A["pair_durations"] == B["pair_durations"]
        controls.append({"speeds": [y, z], "cases": [A, B],
                         "same_all_moments": A["moments_by_mask"] == B["moments_by_mask"]})
    A, B = controls[0]["cases"]
    assert [A["clear_duration"], B["clear_duration"]] == [F(1, 210), F(31, 5040)]
    assert A["triple_durations"] == [F(0), F(0), F(1, 720), F(0)]
    assert B["triple_durations"] == [F(0)]*4
    assert A["components"] == [(S[0], F(37, 120)), (J[1], J[1])]
    assert B["components"] == [(S[0], F(223, 720)), (S[1], S[1]), (J[1], J[1])]
    A, B = controls[1]["cases"]
    assert [A["clear_duration"], B["clear_duration"]] == [F(13, 2128), F(1, 152)]
    assert A["blocker_pair_gcds"] == B["blocker_pair_gcds"]
    assert B["clear_duration"]-A["clear_duration"] == F(1, 2128)
    for control in controls[2:]:
        assert all(row["clear_duration"] == F(3, 448) for row in control["cases"])

    result = {"date": "2026-09-27", "baseline_commit": "f4eecb08eeb790064536551b2bbd44706a7c4a38",
              "status": "Exact physical counterexamples and finite table; unbounded residue classification is a proof candidate awaiting independent review. No novelty claim.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "core": CORE, "fixed_blockers": [6, 7, 11], "window": J, "threshold": D,
              "variable_speed_domain": "Every positive integer y outside {1,4,5,6,7,11}; common start; reference 0.",
              "period": P, "regions": REGIONS, "region_lengths": lengths,
              "coefficient_rows_sha256": digest(rows), "nonzero_ray_count": len(rays),
              "ray_size_counts": dict(sorted(Counter(map(len, rays.values())).items())),
              "same_ray_residue_pairs": candidates, "zero_coefficient_rows": zeros,
              "zero_class": "All positive multiples of 3696 have the same single/pair summary and U=3/448.",
              "family_counts": {"all": 118, "different_duration": 62, "equal_duration": 56,
                                "same_blocker_gcds": 46, "same_blocker_gcds_different_duration": 8},
              "collision_families": families, "physical_controls": controls,
              "zero_duration_cases": zero_duration, "small_check_count": len(small),
              "limits": "Pair durations are local to J. Gcd matches refer to pairs among the four extra blockers, not every core pair or reduced ratios. All matched configurations have positive local duration. No matching empty/contact or positive/zero-duration pair is claimed. All-reference and general-conjecture questions remain separate."}
    encoded = json.dumps(result, indent=2, default=str)+"\n"
    if sys.argv[1:] == ["--check"]:
        assert json.loads(encoded) == json.loads(Path(__file__).with_name("residue_collisions.json").read_text())
        print("PASS: 7392 residue rows; 3240 candidate pairs; 118 nonzero collision families (62 change U); zero class; eight physical controls; 22 small equality checks.")
    else:
        assert not sys.argv[1:], "Only --check is supported"
        print(encoded, end="")


if __name__ == "__main__":
    main()
