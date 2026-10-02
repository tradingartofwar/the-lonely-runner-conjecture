"""Transfer overlap accounting across fixed cores and retain equality times.

Run: python -m scripts.analyze_core_transfer
Eleven prescribed decompositions (ten distinct full speed sets), twenty
core/residual profiles, and a zero-phase-area local control. Exact arithmetic.
General implications are proof candidates; see CORE_TRANSFER.md.
"""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

from lonely_runner.checker import circular_distance, feasible_intervals
from scripts.analyze_blocking_overlaps import blocking_intervals
from scripts.analyze_local_overlap import duration, intersect, measure
from scripts.analyze_overlap_placement import primitive as blocking_primitive
from scripts.analyze_phase_discrepancy import primitive as phase_primitive
from scripts.analyze_two_variable_speeds import phase_certificate


ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "a5bddc35a9e74b5397e11cb762642bd4b0ab68c5"
D = Q(1, 8)
CORES = ((1, 4, 5), (1, 3, 5), (1, 4, 8), (2, 3, 5), (1, 2, 4), (1, 6, 7))


def floor(z):
    return z.numerator // z.denominator


def slice_width(t, r):
    return min(D, max(Q(0), (3 * D - circular_distance(r * t)) / 2))


def phase_pieces(region, r):
    """Affine lower/upper fast-phase endpoints on any rational region."""
    assert isinstance(r, int) and r > 0
    rows = []
    for left, right in region:
        if left == right:
            continue
        cuts = {left, right}
        for m in range(floor(r * left) - 1, floor(r * right) + 2):
            for offset in (-3 * D, -D, D, 3 * D):
                t = (m + offset) / r
                if left < t < right:
                    cuts.add(t)
        cuts = sorted(cuts)
        for a, b in zip(cuts, cuts[1:]):
            t = (a + b) / 2
            if slice_width(t, r) == 0:
                continue
            m = floor(r * t + Q(1, 2))
            lower = max(((Q(0), -D), (-Q(r, 2), (m - D) / 2)), key=lambda h: h[0] * t + h[1])
            upper = min(((Q(0), D), (-Q(r, 2), (m + D) / 2)), key=lambda h: h[0] * t + h[1])
            slope, offset = upper[0] - lower[0], upper[1] - lower[1]
            area = slope * (b * b - a * a) / 2 + offset * (b - a)
            for z in (a, t, b):
                assert slope * z + offset == slice_width(z, r)
            assert area == (b - a) * (slice_width(a, r) + slice_width(b, r)) / 2 > 0
            rows.append({"interval": (a, b), "lower": lower, "upper": upper, "phase_area": area})
    return rows


def endpoint_correction(q, affine, interval):
    slope, offset = affine
    c = q - slope
    a, b = interval
    return (phase_primitive(c * b - offset) - phase_primitive(c * a - offset)) / c


def pair_on_region(q, r, region):
    rows = phase_pieces(region, r)
    area = sum((row["phase_area"] for row in rows), Q(0))
    correction = sum((endpoint_correction(q, row["upper"], row["interval"]) -
                      endpoint_correction(q, row["lower"], row["interval"]) for row in rows), Q(0))
    direct = duration(intersect(intersect(blocking_intervals(q), blocking_intervals(2 * q + r)), region))
    assert direct == area + correction
    error = sum((Q(1, 8) / (q - row["lower"][0]) +
                 Q(1, 8) / (q - row["upper"][0]) for row in rows), Q(0))
    assert abs(correction) <= error <= Q(len(rows), 4 * q)
    return {"q": q, "r": r, "phase_area": area, "endpoint_correction": correction,
        "actual_overlap": direct, "error_bound": error, "piece_count": len(rows)}


def merged(intervals):
    result = []
    for a, b in sorted(intervals):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(b, result[-1][1]))
        else:
            result.append((a, b))
    return tuple(result)


def boundary_certificate(speeds):
    """Reconstruct both open cells and valid boundary points independently."""
    cuts = sorted({Q(0), Q(1), *(t for w in speeds for ab in blocking_intervals(w) for t in ab)})
    good_cells = []
    for a, b in zip(cuts, cuts[1:]):
        if all(circular_distance(w * (a + b) / 2) >= D for w in speeds):
            good_cells.append((a, b))
    valid_points, contacts, rejected_contacts = [], [], []
    for t in cuts:
        outgoing = [w for w in speeds if w * t % 1 == D]
        incoming = [w for w in speeds if w * t % 1 == 1 - D]
        blocked = [w for w in speeds if circular_distance(w * t) < D]
        if not blocked:
            valid_points.append((t, t))
        if outgoing and incoming:
            pairs = []
            for a in outgoing:
                for b in incoming:
                    j, k = a * t - D, b * t + D
                    assert j.denominator == k.denominator == 1
                    assert a * k - b * j == Q(a + b, 8)
                    assert (a + b) % 8 == 0
                    pairs.append({"outgoing": a, "incoming": b, "integers": (j, k), "sum_over_8": Q(a + b, 8)})
            row = {"time": t, "blocking_ends": outgoing, "blocking_starts": incoming,
                   "strict_blockers": blocked, "pairs": pairs}
            (rejected_contacts if blocked else contacts).append(row)
    reconstructed = merged([*good_cells, *valid_points])
    expected = feasible_intervals(speeds, D)
    assert reconstructed == expected
    singletons = [a for a, b in expected if a == b]
    assert [row["time"] for row in contacts] == singletons
    return {"complete_allowed_set": reconstructed, "boundary_count": len(cuts),
        "positive_cell_count": len(good_cells), "isolated_contact_certificates": contacts,
        "rejected_contact_count": len(rejected_contacts),
        "rejected_old_odd_eighth_contacts": [x for x in rejected_contacts if 8 * x["time"] in (1, 3, 5, 7)]}


def profile(core, r):
    region = feasible_intervals(core, D)
    pieces = phase_pieces(region, r)
    area = sum((x["phase_area"] for x in pieces), Q(0))
    k = sum(a < b for a, b in region)
    m = len(pieces)
    M = max(core)
    length = duration(region)
    assert length >= Q(1, 4) + Q(1, 2 * M)
    assert area >= Q(1, 64 * M * M) > 0
    constant = Q(8 * m + 21 * k, 32)
    cutoff = floor(constant / area) + 1
    assert area - constant / cutoff > 0
    return {"core": core, "residual": r, "core_allowed": region, "core_allowed_duration": length,
        "core_duration_lower_bound": Q(1, 4) + Q(1, 2 * M),
        "positive_core_components_k": k, "phase_pieces_m": m, "pieces": pieces,
        "phase_area_I": area, "phase_area_lower_bound": Q(1, 64 * M * M),
        "uniform_error_constant": constant, "coarse_sufficient_q": cutoff,
        "scope": "Core and residual fixed; q and both other speeds grow with u,v>=q; all distinct. Cutoff is not sharp."}


def full_case(label, core, extra):
    q, B, u, v = extra
    r = B - 2 * q
    speeds = tuple(sorted((*core, *extra)))
    assert len(speeds) == len(set(speeds)) == 7
    region = feasible_intervals(core, D)
    accounting = measure(extra, region)
    pair = pair_on_region(q, r, region)
    for w in extra:
        endpoint_duration = sum(((blocking_primitive(w * b) - blocking_primitive(w * a)) / w
                                 for a, b in region), Q(0))
        assert endpoint_duration == accounting["individual_blocking"][str(w)]
    lower = pair["actual_overlap"] - accounting["excess_over_local_average_E"]
    assert accounting["clear_duration_U"] >= lower
    cert = boundary_certificate(speeds)
    assert cert["complete_allowed_set"] == accounting["allowed_intervals"]
    intervals = [ab for ab in cert["complete_allowed_set"] if ab[0] < ab[1]]
    result = {"label": label, "core": core, "extra": extra, "full_relative_speeds": speeds,
        "core_allowed": region, "core_allowed_duration": duration(region), "pair": pair,
        "T": accounting["total_individual_blocking_T"], "E": accounting["excess_over_local_average_E"],
        "R": accounting["redundant_blocking_R"], "U": accounting["clear_duration_U"],
        "one_pair_lower_bound": lower, "histogram": accounting["histogram"], "boundary_certificate": cert}
    if intervals:
        largest = max(intervals, key=lambda ab: ab[1] - ab[0])
        result["positive_interval_certificate"] = phase_certificate(speeds, largest)
        result["certified_interval"] = largest
    return result


def main():
    profiles = [profile(core, r) for core in CORES for r in (1, 2, 3)]
    profiles += [profile((2, 3, 5), r) for r in (5, 8)]
    # Prescribed pair-only checks cover every profile, including r beyond 1..3.
    profile_checks = [pair_on_region(56, row["residual"], row["core_allowed"]) for row in profiles]
    cases = [full_case(f"core_{'_'.join(map(str, core))}_{label}", core, extra)
        for core in CORES[:4]
        for label, extra in (("fast", (56, 113, 64, 72)), ("slow", (6, 13, 7, 11)))]
    cases += [full_case("consecutive_tight", (1, 2, 4), (3, 7, 5, 6)),
              full_case("consecutive_7_to_8", (1, 2, 4), (3, 8, 5, 6)),
              full_case("same_tight_set_regrouped", (1, 6, 7), (4, 11, 5, 13))]
    original, regrouped = cases[1], cases[-1]
    assert original["full_relative_speeds"] == regrouped["full_relative_speeds"]
    assert original["boundary_certificate"]["complete_allowed_set"] == regrouped["boundary_certificate"]["complete_allowed_set"]
    assert original["U"] == regrouped["U"] == cases[8]["U"] == 0
    assert original["E"] == original["R"] and regrouped["E"] == regrouped["R"]
    assert original["E"] != regrouped["E"]
    assert any(x["time"] == Q(3, 8) and 8 in x["strict_blockers"]
               for x in cases[5]["boundary_certificate"]["rejected_old_odd_eighth_contacts"])
    assert cases[3]["U"] == Q(199, 3432) and cases[5]["U"] == Q(1347, 16016)
    assert cases[7]["U"] == Q(111, 1144) and cases[9]["U"] == Q(9, 160)
    # A profile with two singleton core components demonstrates their removal
    # by fast blockers and their survival in the corresponding small case.
    core_points = [a for a, b in cases[2]["core_allowed"] if a == b]
    assert core_points == [Q(3, 8), Q(5, 8)]
    assert not cases[2]["boundary_certificate"]["isolated_contact_certificates"]
    assert all(any(x["time"] == t for x in cases[3]["boundary_certificate"]["isolated_contact_certificates"]) for t in core_points)
    local_region = ((Q(17, 40), Q(23, 40)),)
    assert local_region[0] in cases[2]["core_allowed"]
    local_pair = pair_on_region(56, 1, local_region)
    local_accounting = measure((56, 113, 64, 72), local_region)
    assert local_pair["phase_area"] == local_pair["actual_overlap"] == 0
    assert local_accounting["clear_duration_U"] > 0
    zero_duration = []
    for interval in ((Q(9, 32), Q(1, 3)), (Q(9, 32), Q(3, 8))):
        row = measure((6, 13, 7, 11), (interval,))
        assert row["clear_duration_U"] == 0
        assert row["redundant_blocking_R"] == row["excess_over_local_average_E"]
        zero_duration.append(row)
    assert zero_duration[0]["allowed_intervals"] == ()
    assert zero_duration[1]["allowed_intervals"] == ((Q(3, 8), Q(3, 8)),)
    source_paths = ("scripts/analyze_core_transfer.py", "scripts/analyze_phase_discrepancy.py",
        "scripts/analyze_overlap_placement.py", "scripts/analyze_local_overlap.py",
        "scripts/analyze_blocking_overlaps.py", "scripts/analyze_two_variable_speeds.py", "lonely_runner/checker.py")
    counts = {"core_residual_profiles": len(profiles), "profile_pair_checks": len(profile_checks),
        "full_decompositions": len(cases), "distinct_full_speed_sets": len({x["full_relative_speeds"] for x in cases}),
        "full_pair_endpoint_checks": len(cases), "full_individual_endpoint_checks": 4 * len(cases),
        "full_pair_duration_crosschecks": 6 * len(cases), "complete_allowed_set_reconstructions": len(cases),
        "additional_zero_phase_area_local_control": 1,
        "additional_zero_duration_endpoint_controls": 2,
        "positive_interval_certificates": sum("certified_interval" in x for x in cases),
        "isolated_contact_certificates": sum(len(x["boundary_certificate"]["isolated_contact_certificates"]) for x in cases)}
    data = {"date": "2026-09-24", "base_commit": BASE_COMMIT,
        "claim_status": {"finite_cases": "OBSERVED", "general_transfer_and_boundary_lemmas":
            "HYPOTHESIS: AI-generated complete arguments awaiting independent review", "arbitrary_seven_speeds": "OPEN"},
        "scope": "Eight common-start runners; reference 0; positive distinct integer relative speeds; threshold retained at 1/8 for every subgroup.",
        "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "profiles": profiles, "profile_pair_checks": profile_checks, "cases": cases, "verification_counts": counts,
        "zero_phase_area_local_control": {"core": (1, 3, 5), "region": local_region,
            "pair": local_pair, "accounting": local_accounting},
        "zero_duration_empty_versus_singleton": zero_duration,
        "general_candidate": "For any fixed positive integer core triple and fixed positive integer r, phase area I>0; U>=I-(8m+21k)/(32q) when the four extras are q,2q+r,u,v with u,v>=q and all speeds distinct. k counts positive core components, m their positive affine phase pieces.",
        "isolated_point_candidate": "At delta=1/8 a valid interior time is isolated exactly when some speed has fractional phase 1/8 and another has 7/8. All other constraints must still be checked.",
        "limitations": "No general existence proof for arbitrary seven speeds, no all-reference check, no independent mathematical review or novelty claim. Positive phase area is not finite-q occupancy. Durations do not determine singleton existence."}
    (ROOT / "experiments/core_transfer.json").write_text(json.dumps(data, indent=2, default=str) + "\n")
    print(json.dumps({"cases": [{"label": x["label"], "core_duration": x["core_allowed_duration"],
        "I": x["pair"]["phase_area"], "O": x["pair"]["actual_overlap"], "E": x["E"], "R": x["R"],
        "pair_bound": x["one_pair_lower_bound"], "U": x["U"],
        "singletons": [y["time"] for y in x["boundary_certificate"]["isolated_contact_certificates"]]} for x in cases],
        "counts": counts}, indent=2, default=str))


if __name__ == "__main__":
    main()
