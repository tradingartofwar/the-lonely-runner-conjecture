#!/usr/bin/env python3
"""Separate exact audit of the frozen CC coefficient-checker outputs.

No production imports: intervals and coordinate congruences reconstruct the
mathematics. The audit reads serialized production outputs only after deriving
the expected values. Its fixed input scope is the accompanying PROTOCOL.md.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import gcd
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CORE = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2))
MENU = ((1, 2), (1, 3), (2, 1), (1, 4), (1, 5), (2, 3),
        (1, 6), (3, 2), (2, 5), (4, 1), (1, 8))


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def frac(x):
    return x - floor(x)


def safe(x):
    return F(1, 8) <= frac(x) <= F(7, 8)


def band(A, B):
    """Common integer lap = intersection of endpoint lap intervals."""
    ends = (A*F(1, 4) + B*F(3, 8), A*F(3, 8) + B*F(1, 8))
    lower = max(ceil(z-F(7, 8)) for z in ends)
    upper = min(floor(z-F(1, 8)) for z in ends)
    return {"leader_safe": lower <= upper, "lap_interval": [lower, upper],
            "endpoints": ends, "C_raw": A*F(1, 8)+B*F(1, 4),
            "accepted": lower <= upper and safe(A*F(1, 8)+B*F(1, 4))}


def recover(A, B, p, q):
    """Direct interval contact followed by coordinate congruence recovery."""
    d = gcd(p, q)
    P, Q = p//d, q//d
    left, right = Q*F(1, 4)-P*F(3, 8), Q*F(3, 8)-P*F(1, 8)
    h = ceil(left)
    if h <= right:
        x = (F(h)+P*F(7, 8))/(Q+2*P)
        y = F(7, 8)-2*x
        role = "L"
    else:
        if (P, Q) != (1, 2):
            raise ValueError("Unexpected leader miss outside sole fallback direction")
        x, y, h, role = F(1, 8), F(1, 4), 0, "C"
    i = (-h*pow(Q, -1, P)) % P if P > 1 else 0
    if (Q*i+h) % P:
        raise ValueError("Coordinate congruence has no integral second lap")
    j = (Q*i+h)//P
    tau = (x+i)/P
    t = tau/d
    if Q*tau != y+j or not 0 <= tau < 1:
        raise ValueError("Coordinate lift failed")
    rows = CORE+((A, B),)
    speeds = [a*p+b*q for a, b in rows]
    torus = [a*x+b*y for a, b in rows]
    raw = [v*t for v in speeds]
    phases = [frac(z) for z in raw]
    laps = [floor(z) for z in raw]
    torus_laps = [floor(z) for z in torus]
    if phases != [frac(z) for z in torus]:
        raise ValueError("Torus and physical phases disagree")
    if laps != [m+a*i+b*j for m, (a, b) in zip(torus_laps, rows)]:
        raise ValueError("Coordinate lap recovery disagrees with direct product")
    reflected = [v*(1-t) for v in speeds]
    distances = [min(z, 1-z) for z in phases]
    return {
        "row": [A, B], "pair": [p, q], "primitive": [P, Q], "gcd": d,
        "point": [str(x), str(y)], "h": h, "role": role,
        "coordinate_laps": [i, j], "primitive_time": str(tau), "time": str(t),
        "speeds": speeds, "phases": [str(z) for z in phases],
        "physical_laps": laps, "torus_laps": torus_laps,
        "distances": [str(z) for z in distances], "minimum": str(min(distances)),
        "safe": all(z >= F(1, 8) for z in distances),
        "six_core_safe": all(z >= F(1, 8) for z in distances[:6]),
        "distinct_speeds": len(set([0]+speeds)) == 8,
        "reflected_time": str(1-t),
        "reflected_phases": [str(frac(z)) for z in reflected],
        "reflected_laps": [floor(z) for z in reflected],
        "empty_distinct_speed_domain": (A, B) in CORE,
    }


def rejection(A, B):
    """Independently reconstruct the protocol's deterministic branch order."""
    if band(A, B)["accepted"]:
        return None
    delta = A-2*B
    D = abs(delta)
    a = (2*A+3*B) % 8
    evidence = {}
    if (A+2*B) % 8 == 0:
        pair, branch = (1, 2), "C_collision"
    elif a == 0:
        pair, branch = (2, 3), "left_collision"
    elif (delta > 0 and a == 7) or (delta < 0 and a == 1):
        j = max(2, floor(F(7*D, 8))+1)
        drift = F(7*D, 32*j)
        if not 0 < drift < F(1, 4):
            raise ValueError("Outward branch does not strictly enter forbidden band")
        pair, branch = (1, 4*j-2), "outward_boundary"
        evidence = {"j": j, "drift": str(drift)}
    elif D >= 14:
        c = 7-a if delta > 0 else a-1
        if not 1 <= c <= 6:
            raise ValueError("Large-slope margin outside derived range")
        lower, upper = F(7*D, 4*(c+2)), F(7*D, 4*c)
        j = floor(lower)+1
        if not lower < j < upper or j < 2:
            raise ValueError("Rounded large-slope direction outside strict interval")
        drift = F(7*D, 32*j)
        if not F(c, 8) < drift < F(c+2, 8):
            raise ValueError("Large-slope drift outside strict forbidden band")
        pair, branch = (1, 4*j-2), "large_slope"
        evidence = {"j": j, "c": c, "strict_interval": [str(lower), str(upper)],
                    "drift": str(drift)}
    else:
        if D > 13:
            raise ValueError("Unclassified slope")
        pair = next((pair for pair in MENU if not recover(A, B, *pair)["safe"]), None)
        if pair is None:
            raise ValueError("Frozen eleven-direction menu supplied no rejection")
        branch = "finite_menu"
    witness = recover(A, B, *pair)
    if witness["safe"] or not witness["six_core_safe"] or not witness["distinct_speeds"]:
        raise ValueError("Derived rejection does not meet physical failure contract")
    if pair[0] == pair[1]:
        raise ValueError("Rejection used excluded diagonal input")
    return {"branch": branch, "pair": list(pair), "evidence": evidence, "witness": witness}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


CHECKS = Counter()


def equal(actual, expected, label):
    CHECKS[label.split(".")[0]] += 1
    if actual != expected:
        raise ValueError(f"{label}: expected {expected!r}; found {actual!r}")


def check_physical(actual, A, B, p, q):
    expected = recover(A, B, p, q)
    fields = ("row", "pair", "primitive", "gcd", "point", "h", "role",
              "primitive_time", "time", "speeds", "phases", "physical_laps",
              "torus_laps", "distances", "minimum", "distinct_speeds",
              "reflected_time", "reflected_phases", "reflected_laps")
    for name in fields:
        equal(actual[name], expected[name], f"physical.{name}")
    P, Q = expected["primitive"]
    x, y = map(F, expected["point"])
    rho = 8*ceil(F(2*Q-3*P, 8))-(2*Q-3*P)
    for name, value in {
        "M": Q+2*P, "rho": rho, "core_safe": expected["six_core_safe"],
        "seventh_safe": expected["safe"], "repeated_initial_speeds": p == q,
        "failed_runner_indices": [i+1 for i, z in enumerate(expected["distances"]) if F(z) < F(1, 8)],
        "seventh_core_collisions": [[a, b] for a, b in CORE[2:] if (A-a)*p+(B-b)*q == 0],
        "selector": "CC-L-C-first-integer-v1",
    }.items():
        equal(actual[name], value, f"physical.{name}")
    r, s = actual["bezout"]
    equal(r*P+s*Q, 1, "physical.bezout_identity")
    N = floor(r*x+s*y)
    equal(actual["N"], N, "physical.bezout_floor")
    equal(frac(r*x+s*y), F(expected["primitive_time"]), "physical.bezout_clock")
    equal(actual["physical_laps"], [m+(-a*s+b*r)*actual["h"]-(a*P+b*Q)*N
          for m, (a, b) in zip(actual["torus_laps"], CORE+((A, B),))], "physical.bezout_lap_map")
    return expected


def check_decision(actual, A, B):
    derived = band(A, B)
    for name, value in {
        "row": [A, B], "delta": A-2*B, "B_mod8": B % 8, "threshold": "1/8",
        "status": "ACCEPTED" if derived["accepted"] else "REJECTED",
        "schema": "cc-coefficient-decision-v1", "selector": "CC-L-C-first-integer-v1",
        "proof": {"status": "internally reviewed proof candidate",
                  "commit": "57997d4220226b44b9a89d8d8139926f15cca90c",
                  "note": "notes/CC_SELECTOR_SUPPORT_2026_09_29.md"},
        "distinct_speed_domain": {
            "empty": (A, B) in CORE,
            "identically_repeated_core_row": [A, B] if (A, B) in CORE else None,
            "conditions": {"p_not_equal_q": True, "nonzero_linear_forms": [
                {"core_row": [a, b], "p_coefficient": A-a, "q_coefficient": B-b}
                for a, b in CORE[2:]]}},
    }.items():
        equal(actual[name], value, f"decision.{name}")
    if derived["accepted"]:
        lap = derived["lap_interval"][0]
        equal(derived["lap_interval"][1], lap, "acceptance.unique_lap")
        leader = actual["guarantee"]["leader"]
        for name, value in {"endpoints": [["1/4", "3/8"], ["3/8", "1/8"]],
                            "seventh_values": list(map(str, derived["endpoints"])),
                            "seventh_lap": lap,
                            "safe_band": [str(lap+F(1, 8)), str(lap+F(7, 8))]}.items():
            equal(leader[name], value, f"acceptance.leader_{name}")
        C = derived["C_raw"]
        fallback = actual["guarantee"]["fallback"]
        for name, value in {"point": ["1/8", "1/4"], "seventh_value": str(C),
                            "seventh_lap": floor(C), "seventh_phase": str(frac(C))}.items():
            equal(fallback[name], value, f"acceptance.fallback_{name}")
        equal(actual["guarantee"]["minimum_selected_distance"], "1/8", "acceptance.minimum")
        return None
    expected = rejection(A, B)
    reasons = {"C_collision": "FALLBACK_COLLISION", "left_collision": "LEADER_START_COLLISION",
               "outward_boundary": "OUTWARD_BOUNDARY", "large_slope": "LARGE_SLOPE",
               "finite_menu": "BOUNDED_DIRECTION"}
    equal(actual["reason"], reasons[expected["branch"]], "rejection.branch")
    equal(actual["counterexample"]["pair"], expected["pair"], "rejection.pair")
    construction = actual["construction"]
    equal(construction["left_phase"], str(frac(A*F(1, 4)+B*F(3, 8))), "rejection.left_phase")
    equal(construction["absolute_delta"], abs(A-2*B), "rejection.absolute_delta")
    for name, production_name in {"j": "j", "c": "c", "drift": "drift_magnitude",
                                  "strict_interval": "open_j_interval"}.items():
        if name in expected["evidence"]:
            equal(construction[production_name], expected["evidence"][name], f"rejection.{name}")
    if expected["branch"] == "finite_menu":
        attempts = []
        for pair in MENU:
            physical = recover(A, B, *pair)
            attempts.append({"pair": list(pair), "seventh_phase": physical["phases"][-1]})
            if not physical["safe"]:
                break
        equal(construction["attempts"], attempts, "rejection.menu_attempts")
        equal(construction["contact_tests"], len(attempts), "rejection.menu_count")
    check_physical(actual["counterexample"], A, B, *expected["pair"])
    return expected


def run():
    validation = json.loads((HERE/"validation.json").read_text())
    previous = ROOT/"reviews/2026-09-29-cc-selector-support/classification.json"
    archive_cells = json.loads(previous.read_text())["cells"]
    physical_archive = ROOT/"reviews/2026-09-29-cc-coefficient-range/witnesses.json"
    archive_physical = json.loads(physical_archive.read_text())["progression_controls"]
    K = 10**20
    expected_rows = {
        "baseline": [(2*(b+8)+delta, b+8) for delta in range(-13, 14) for b in range(8)],
        "period_shift": [(2*(b+8)+delta+16*K, b+8+8*K)
                         for delta in range(-13, 14) for b in range(8)],
        "large": [],
    }
    for delta in (-15, -14, 14, 15, -(10**40+14), 10**40+14):
        for b in range(8):
            B = 8*(abs(delta)//8+2)+b
            expected_rows["large"].append((2*B+delta, B))
    groups = {group: {} for group in expected_rows}
    branches = Counter()
    for case in validation["coefficient_cases"]:
        actual = case["result"]
        row = tuple(actual["row"])
        group = case["group"]
        if row in groups[group]:
            raise ValueError("Duplicate coefficient record")
        groups[group][row] = actual
        expected = check_decision(actual, *row)
        branches["ACCEPTED" if expected is None else expected["branch"]] += 1
    for group, rows in expected_rows.items():
        equal(sorted(groups[group]), sorted(rows), f"scope.{group}_rows")

    changed_directions = []
    baseline_counts = Counter()
    for cell in archive_cells:
        A, B = cell["representative"]
        actual = groups["baseline"][(A, B)]
        equal(actual["status"] == "ACCEPTED", cell["T"], "archive.decision")
        if actual["status"] == "REJECTED":
            baseline_counts[actual["reason"]] += 1
            now_pair = actual["counterexample"]["pair"]
            if now_pair != cell["first_failure_pair"]:
                changed_directions.append({"row": [A, B], "old_pair": cell["first_failure_pair"],
                                           "new_pair": now_pair, "new_reason": actual["reason"]})
        shifted = groups["period_shift"][(A+16*K, B+8*K)]
        equal(shifted["status"], actual["status"], "periodicity.status")
        if actual["status"] == "ACCEPTED":
            old, new = actual["guarantee"], shifted["guarantee"]
            for component, increment in (("leader", 7*K), ("fallback", 4*K)):
                equal(new[component]["seventh_lap"]-old[component]["seventh_lap"], increment,
                      f"periodicity.{component}_lap")
            equal(new["fallback"]["seventh_phase"], old["fallback"]["seventh_phase"], "periodicity.C_phase")
            equal([F(v)-F(u) for u, v in zip(old["leader"]["seventh_values"], new["leader"]["seventh_values"])],
                  [7*K, 7*K], "periodicity.leader_values")
        else:
            old, new = actual["counterexample"], shifted["counterexample"]
            equal(shifted["reason"], actual["reason"], "periodicity.branch")
            equal(shifted["construction"], actual["construction"], "periodicity.construction")
            for name in ("pair", "point", "role", "time", "primitive_time", "phases", "distances",
                         "minimum", "reflected_time", "reflected_phases"):
                equal(new[name], old[name], f"periodicity.{name}")
            torus_increment = 7*K if old["role"] == "L" else 4*K
            equal(new["torus_laps"][-1]-old["torus_laps"][-1], torus_increment, "periodicity.torus_lap")
            p, q = old["pair"]
            physical_increment = 8*K*(2*p+q)*F(old["time"])
            equal(physical_increment.denominator, 1, "periodicity.integer_physical_increment")
            equal(new["physical_laps"][-1]-old["physical_laps"][-1], physical_increment,
                  "periodicity.physical_lap")
            equal(new["reflected_laps"][-1]-old["reflected_laps"][-1],
                  8*K*(2*p+q)-physical_increment, "periodicity.reflected_lap")
            for name in ("speeds", "physical_laps", "torus_laps", "reflected_laps"):
                equal(new[name][:6], old[name][:6], f"periodicity.core_{name}")
    equal(len(changed_directions), 40, "archive.changed_direction_count")

    archive_lookup = {(tuple(r["row"]), tuple(r["pair"])): r for r in archive_physical}
    named_inputs = [((A, B), (2, 3)) for A, B in ((1, 1), (2, 1), (3, 1), (3, 2), (4, 5), (23, 12))]
    named_inputs += [((4, 2), (1, 2)), ((5, 2), (2, 3))]
    physical_seen = {"archived": [], "named": []}
    for case in validation["physical_cases"]:
        record = case["record"]
        A, B = record["row"]
        p, q = record["pair"]
        expected = check_physical(record, A, B, p, q)
        key = ((A, B), (p, q))
        physical_seen[case["group"]].append(key)
        if case["group"] == "archived":
            archived = archive_lookup[key]
            for name in record.keys() & archived.keys():
                equal(record[name], archived[name], f"archive.physical_{name}")
        if "decision" in case:
            check_decision(case["decision"], A, B)
            if case["decision"]["status"] == "ACCEPTED":
                equal(expected["safe"], True, "acceptance.requested_safe")
    equal(sorted(physical_seen["archived"]), sorted(archive_lookup), "scope.archived_physical")
    equal(sorted(physical_seen["named"]), sorted(named_inputs), "scope.named_physical")

    invalid_coefficients = [(0, 2), (-1, 2), (6, 0), (6, -2), (True, 2),
                            (6, False), (6.0, 2), (6, "2"), (None, 2)]
    invalid_physical = [(0, 3), (2, 0), (-1, 3), (2, -3), (True, 3), (2, 3.0)]
    expected_invalid = [("check_coefficients", repr(pair)) for pair in invalid_coefficients]
    expected_invalid += [("evaluate_selector", repr((6, 2)+pair)) for pair in invalid_physical]
    equal(sorted((r["function"], r["input_repr"]) for r in validation["invalid_api"]),
          sorted(expected_invalid), "scope.invalid_api")
    for record in validation["invalid_api"]:
        equal(record["error_type"], "ValueError", "invalid.error_type")

    cli_argv = [["6", "2"], ["5", "2"], ["6", "2", "--p", "4", "--q", "6"],
                ["1", "1", "--p", "2", "--q", "3"], ["5", "2", "--p", "1", "--q", "3"],
                ["6", "2", "--p", "2"], ["6", "two"], ["6.0", "2"], ["-1", "2"]]
    cli_seen = {False: {}, True: {}}
    for case in validation["cli_cases"]:
        argv, output = case["argv"], case["output"]
        cli_seen[case["optimized"]][tuple(argv)] = case
        valid = argv in cli_argv[:5]
        equal(case["exit_code"], 0 if valid else 2, "cli.exit_code")
        if valid:
            A, B = map(int, argv[:2])
            check_decision(output, A, B)
            if "--p" in argv:
                p, q = int(argv[argv.index("--p")+1]), int(argv[argv.index("--q")+1])
                check_physical(output["requested_evaluation"], A, B, p, q)
        else:
            equal(output["status"], "INVALID_INPUT", "cli.invalid_status")
    for optimized in (False, True):
        equal(sorted(cli_seen[optimized]), sorted(map(tuple, cli_argv)), f"scope.cli_{optimized}")
    for argv in map(tuple, cli_argv):
        equal(cli_seen[False][argv]["output"], cli_seen[True][argv]["output"], "cli.optimized_output")

    result = {
        "status": "PASS", "method": "Independent interval and coordinate-congruence audit; no production imports",
        "scope": {"coefficient_cases": 480, "baseline": 216, "period_shift": 216, "large": 48,
                  "archived_physical": 54, "named_physical": 8, "invalid_api": 15, "cli": 18},
        "decision_counts": {"accepted": branches["ACCEPTED"], "rejected": 480-branches["ACCEPTED"]},
        "branch_counts": dict(sorted(branches.items())), "baseline_rejection_counts": dict(sorted(baseline_counts.items())),
        "field_comparisons": dict(sorted(CHECKS.items())), "total_field_comparisons": sum(CHECKS.values()),
        "changed_archive_rejection_directions": changed_directions,
        "provenance": {str(p.relative_to(ROOT)): digest(p) for p in
            (HERE/"PROTOCOL.md", HERE/"audit.py", HERE/"validation.json", previous, physical_archive)},
        "claim_limit": "Internal AI review and bounded implementation controls of the existing proof candidate; no new mathematical classification or changed construction",
    }
    (HERE/"audit.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "scope", "decision_counts", "branch_counts", "total_field_comparisons")}, indent=2))


if __name__ == "__main__":
    run()
