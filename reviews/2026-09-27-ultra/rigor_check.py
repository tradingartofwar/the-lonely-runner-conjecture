"""Independent exact review checks; standard library, no project imports.

Run from any directory: python -B /absolute/path/to/rigor_check.py --check
--check replays the mathematics read-only and verifies this script's hash.
Default mode writes only this review's rigor_check.json, preserving recorded
baseline input hashes. Historical archives are read-only.
The residue enumeration is finite evidence supporting the derivations in rigor.md.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import gcd, lcm
from collections import defaultdict, Counter
from pathlib import Path
import json
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
A, B, DELTA = Q(9, 32), Q(3, 8), Q(1, 8)
J = [(A, B)]


def intersect(left, right):
    """Sorted interval intersection; preserve singleton closed safe cells."""
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        lo = max(left[i][0], right[j][0])
        hi = min(left[i][1], right[j][1])
        if lo <= hi:
            if out and lo <= out[-1][1]:
                out[-1] = (out[-1][0], max(out[-1][1], hi))
            else:
                out.append((lo, hi))
        if left[i][1] < right[j][1]:
            i += 1
        else:
            j += 1
    return out


def one_runner(v, safe=False):
    out = []
    for k in range((v*A).__floor__()-1, (v*B).__floor__()+2):
        raw = [((k+DELTA)/v, (k+1-DELTA)/v)] if safe else [((k-DELTA)/v, (k+DELTA)/v)]
        out += intersect(J, raw)
    return out


def measure(intervals):
    return sum((b-a for a, b in intervals), Q(0))


def moments_and_cells(fixed, y):
    extras = (*fixed, y)
    blocked = [one_runner(v) for v in extras]
    regions = [J]
    for mask in range(1, 16):
        bit = mask & -mask
        regions.append(intersect(regions[mask ^ bit], blocked[bit.bit_length()-1]))
    moments = list(map(measure, regions))
    # Boolean-lattice inversion, independent of midpoint state enumeration.
    states = [sum(((-1)**((s ^ mask).bit_count())*moments[s]
                   for s in range(16) if s & mask == mask), Q(0)) for mask in range(16)]
    assert min(states) >= 0 and sum(states) == B-A
    safe = J
    for v in (1, 4, 5, *extras):
        safe = intersect(safe, one_runner(v, safe=True))
    assert measure(safe) == states[0]
    return {"moments": moments, "states": states, "cells": safe,
            "gcds": [gcd(v, w) for v, w in combinations((1, 4, 5, *extras), 2)]}


def normalized_primitive(z):
    """Integral from 0 to z: count initial/final blocked portions of a lap.

    This differs by a constant from the reviewed shifted primitive.
    """
    n = z.__floor__()
    r = z-n
    return Q(n, 4)+min(r, DELTA)+max(Q(0), r-(1-DELTA))


def correction(z):
    return normalized_primitive(z)-z/4


def integrate(v, intervals):
    return sum(((normalized_primitive(v*b)-normalized_primitive(v*a))/v
                for a, b in intervals), Q(0))


def one_congruence(multiplier, residue, modulus):
    d = gcd(multiplier, modulus)
    if residue % d:
        return None
    m = modulus//d
    return ((residue//d)*pow(multiplier//d, -1, m) % m, m)


def crt(left, right):
    if left is None or right is None:
        return None
    a, p = left
    b, q = right
    d = gcd(p, q)
    if (b-a) % d:
        return None
    n = ((b-a)//d)*pow(p//d, -1, q//d) % (q//d)
    return ((a+p*n) % lcm(p, q), lcm(p, q))


def classify(fixed, period, archive_name):
    archive = json.loads((ROOT / 'reviews/2026-09-27-lr2' / archive_name).read_text())
    regions = [J]+[one_runner(v) for v in fixed]
    opening = J
    for v in fixed:
        opening = intersect(opening, one_runner(v, safe=True))
    # Build using rational primitive differences at actual rational endpoints.
    coefficients, groups, zeros = {}, defaultdict(list), []
    for r in range(period):
        row = tuple(sum((correction(r*b)-correction(r*a) for a, b in region), Q(0))
                    for region in regions)
        coefficients[r] = row
        index = next((i for i, x in enumerate(row) if x), None)
        if index is None:
            zeros.append(r)
        else:
            pivot = abs(row[index])
            groups[tuple(x/pivot for x in row)].append(r)
    families = []
    counts = Counter()
    for group in groups.values():
        for r, s in combinations(group, 2):
            counts['same_ray_pairs'] += 1
            x, z = coefficients[r], coefficients[s]
            idx = next(i for i, q in enumerate(x) if q)
            ratio = x[idx]/z[idx]
            a, b = ratio.numerator, ratio.denominator
            if a == b:
                continue
            solution = crt(one_congruence(a, r, period), one_congruence(b, s, period))
            if solution is None:
                continue
            k, mod = solution
            assert mod == period and k != 0
            if a > b:
                r, s, a, b = s, r, b, a
            first = k
            while a*first in (1, 4, 5, *fixed) or b*first in (1, 4, 5, *fixed):
                first += period
            row = {'residues': [r, s], 'multipliers': [a, b], 'k_residue': k,
                   'k_modulus': period, 'first_admissible_k': first,
                   'first_speeds': [a*first, b*first]}
            if fixed == (6, 7, 11):
                cy = sum((correction(r*v)-correction(r*u) for u, v in opening), Q(0))
                cz = sum((correction(s*v)-correction(s*u) for u, v in opening), Q(0))
                change = cy/a-cz/b
                same_gcd = all(gcd(r, v) == gcd(s, v) for v in fixed)
                row.update(U_z_minus_U_y_times_k=change, same_blocker_pair_gcds=same_gcd)
                counts['different_duration'] += bool(change)
                counts['same_blocker_gcds'] += same_gcd
                counts['same_blocker_gcds_different_duration'] += bool(change) and same_gcd
            else:
                assert (r % 8 == 0) == (s % 8 == 0)
                row['outcome'] = 'empty' if r % 8 == 0 else 'singleton at 3/8'
                counts[row['outcome']] += 1
            families.append(row)
    families.sort(key=lambda row: (max(row['first_speeds']), row['first_speeds']))
    assert json.loads(json.dumps(families, default=str)) == archive['collision_families']
    assert len(groups) == archive['nonzero_ray_count']
    assert zeros == [r[0] for r in archive['zero_coefficient_rows']]
    assert counts['same_ray_pairs'] == archive['same_ray_residue_pairs']
    return {'period': period, 'nonzero_rays': len(groups), 'zeros': zeros,
            'families': len(families), 'counts': dict(counts),
            'minimum_pair': families[0]['first_speeds'], 'archive_families_match': True}


def main():
    assert sys.argv[1:] in ([], ['--check']), 'Only --check is supported'
    check = sys.argv[1:] == ['--check']
    archive_path = HERE/'rigor_check.json'
    archived = json.loads(archive_path.read_text()) if archive_path.exists() else None
    assert not check or archived is not None, 'Missing review archive'
    results = {'baseline_supplied_by_parent': 'e94a87f650264826569cae63412c43a5175f5ae4',
               'method': 'Own rational interval intersections and unshifted primitive; separate linear-congruence/CRT classification; no project imports.'}
    cases = {}
    for fixed, ys in [((6, 7, 11), (3, 10, 13, 26, 45, 90, 266, 532, 336, 1344, 3696, 7392)),
                      ((3, 10, 28), (1680, 3360, 5040, 6720)),
                      ((6, 7, 3), (2, 8, 10, 24, 48, 144, 95, 190, 336, 672, 673)),
                      ((6, 7, 2), (23, 69, 25, 75)), ((6, 7, 8), (25, 75)),
                      ((6, 7, 21), (25, 75))]:
        for y in ys:
            cases[(*fixed, y)] = moments_and_cells(fixed, y)
    for a, b in ((45, 90), (266, 532), (336, 1344), (3696, 7392)):
        x, y = cases[(6, 7, 11, a)], cases[(6, 7, 11, b)]
        assert all(x['moments'][s] == y['moments'][s] for s in range(16) if s.bit_count() <= 2)
    assert [cases[(6, 7, 11, y)]['states'][0] for y in (45, 90, 266, 532)] == [Q(1, 210), Q(31, 5040), Q(13, 2128), Q(1, 152)]
    for h in range(1, 5):
        c = cases[(3, 10, 28, 1680*h)]
        base = cases[(3, 10, 28, 1680)]
        assert c['moments'] == base['moments'] and c['states'] == base['states'] and c['gcds'] == base['gcds']
        assert c['cells'] == ([(A, A)] if h % 2 else [])
        assert all(c['moments'][8+i] == c['moments'][i]/4 for i in range(8))
        assert all(c['states'][8+i] == c['states'][i]/3 for i in range(8))
    for fixed, a, b, full in (((6, 7, 2), 23, 69, True), ((6, 7, 2), 25, 75, True),
                               ((6, 7, 8), 25, 75, True), ((6, 7, 21), 25, 75, False)):
        x, y = cases[(*fixed, a)], cases[(*fixed, b)]
        assert (x['moments'] == y['moments']) == full
        assert all(x['moments'][s] == y['moments'][s] for s in range(16) if s.bit_count() <= 2)
        assert x['states'][0] == y['states'][0] and x['cells'] != y['cells']
    # Independently compare every archived concrete case of both latest notes.
    rc = json.loads((ROOT/'reviews/2026-09-27-lr2/residue_collisions.json').read_text())
    cc = json.loads((ROOT/'reviews/2026-09-27-lr2/contact_moments.json').read_text())
    listed = [(tuple((6,7,11)), row) for pair in rc['physical_controls'] for row in pair['cases']]
    listed += [(tuple((6,7,11)), row) for row in rc['zero_duration_cases']]
    listed += [(tuple(row['fixed_blockers']), row) for row in cc['physical_controls']+cc['constructive_boundary_family']['controls']]
    for fixed, row in listed:
        ours = cases[(*fixed, row['y'])]
        assert ours['moments'] == list(map(Q, row['moments_by_mask']))
        assert ours['states'] == list(map(Q, row['state_durations_by_mask']))
        assert ours['cells'] == [tuple(map(Q, pair)) for pair in row['components']]
    results['physical_cases'] = [{'fixed': key[:3], 'y': key[3], **value} for key, value in cases.items()]
    results['archived_cases_compared'] = len(listed)
    # Rebuild the original bounded collision search using interval intersections,
    # not its periodic-integral signature implementation.
    domain = [v for v in range(1,81) if v not in (1,4,5,6,7)]
    blocked = {v: one_runner(v) for v in (*domain,6,7)}
    sig_groups = defaultdict(list)
    for x, y in combinations(domain,2):
        sig = (measure(blocked[x]), measure(blocked[y]),
               measure(intersect(blocked[6],blocked[x])), measure(intersect(blocked[6],blocked[y])),
               measure(intersect(blocked[7],blocked[x])), measure(intersect(blocked[7],blocked[y])),
               measure(intersect(blocked[x],blocked[y])))
        sig_groups[sig].append([x,y])
    collisions = [group for group in sig_groups.values() if len(group)>1]
    assert len(sig_groups) == 2771
    assert collisions == [[[2,23],[2,69]], [[2,25],[2,75]], [[8,25],[8,75]], [[21,25],[21,75]]]
    results['original_audit_search'] = {'inputs':len(domain)*(len(domain)-1)//2,
                                       'unique_signatures':len(sig_groups), 'collisions':collisions}
    results['classifications'] = [classify((6,7,11), 7392, 'residue_collisions.json'),
                                  classify((6,7,3), 672, 'contact_moments.json')]
    # Bounded adversarial checks supplement, rather than replace, 2-adic proof.
    denominator_failures = [y for y in range(1, 8193) if (integrate(y, J).denominator % 64 == 0) != (y % 8 == 0)]
    assert not denominator_failures
    results['denominator_bounded_check'] = {'range': [1,8192], 'failures': denominator_failures}
    results['fixed_partition_endpoint_phases'] = sorted({(1680*t) % 1 for v in (3,10,28) for I in one_runner(v) for t in I})
    assert results['fixed_partition_endpoint_phases'] == [Q(0), Q(1,2)]
    sources = ['AGENTS.md','README.md','CLAIM_STATUS.md','CONTRIBUTING.md','HANDOFF.md',
               'notes/DISTINCTION_AUDIT_2026_09_25.md','notes/RESIDUE_COLLISIONS_2026_09_27.md',
               'notes/CONTACT_MOMENTS_2026_09_27.md',
               'reviews/2026-09-25-lr2/check_distinction_audit.py',
               'reviews/2026-09-25-lr2/distinction_audit.json',
               'reviews/2026-09-27-lr2/check_residue_collisions.py',
               'reviews/2026-09-27-lr2/check_contact_moments.py',
               'reviews/2026-09-27-lr2/crosscheck_residue_controls.py',
               'reviews/2026-09-27-lr2/crosscheck_contact_moments.py',
               'reviews/2026-09-27-lr2/residue_collisions.json',
               'reviews/2026-09-27-lr2/contact_moments.json']
    # These are provenance of the reviewed snapshot, not freshness assertions
    # about governance files that may legitimately change after the review.
    results['input_sha256'] = (archived['input_sha256'] if archived is not None else
                              {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources})
    results['review_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    encoded = json.dumps(results, indent=2, default=str)+'\n'
    if check:
        assert archived['review_script_sha256'] == results['review_script_sha256'], 'Review script hash mismatch'
        assert json.loads(encoded) == archived, 'Recomputed mathematical evidence differs from archive'
    else:
        archive_path.write_text(encoded)
    print(json.dumps({'physical_cases': len(cases), 'archived_cases_compared': len(listed),
                      'classifications': results['classifications'],
                      'denominator_speeds':8192, 'status':'PASS'}, indent=2))


if __name__ == '__main__':
    main()
