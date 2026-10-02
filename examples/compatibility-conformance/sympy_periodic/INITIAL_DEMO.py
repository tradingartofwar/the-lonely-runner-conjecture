#!/usr/bin/env python3
"""A bounded adapter for SymPy's documented principal-period inequality API."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys

import sympy as s
from sympy.calculus.util import periodicity

HERE = Path(__file__).resolve().parent
T = s.Symbol("t", real=True)
THRESHOLDS = {F(-1), F(-1, 2), F(0), F(1, 2), F(1)}
RELATIONS = {">": s.Gt, ">=": s.Ge, "<": s.Lt, "<=": s.Le}


class Unsupported(ValueError):
    """Outside the explicitly supported input/result contract."""


def rational(text):
    if not isinstance(text, str) or not re.fullmatch(r"-?\d+(?:/[1-9]\d*)?", text):
        raise Unsupported("rational inputs must be integer or fraction strings; floats unsupported")
    q = F(text)
    if q.denominator > 64 or abs(q) > 100:
        raise Unsupported("input rationals require denominator <=64 and absolute value <=100")
    return q


def sr(q):
    return s.Rational(q.numerator, q.denominator)


def ff(q):
    if not isinstance(q, s.Rational):
        raise Unsupported(f"nonrational endpoint or period: {q}")
    return F(int(q.p), int(q.q))


def validate(case):
    h = case["horizon"]
    lo, hi = rational(h["lo"]), rational(h["hi"])
    if lo >= hi or any(type(h[k]) is not bool for k in ("left_open", "right_open")):
        raise Unsupported("horizon must have increasing rational ends and Boolean endpoint flags")
    if not 1 <= len(case["atoms"]) <= 8:
        raise Unsupported("one to eight atoms required")
    for a in case["atoms"]:
        if a["function"] not in ("sin", "cos") or a["relation"] not in RELATIONS:
            raise Unsupported("unsupported function or relation")
        frequency = rational(a["frequency"])
        rational(a["phase"])
        if frequency <= 0 or rational(a["threshold"]) not in THRESHOLDS:
            raise Unsupported("positive frequency and listed threshold required")
        if (hi - lo) * frequency / 2 > 100:
            raise Unsupported("at most 100 periods per atom within the horizon")


def expression(atom):
    angle = s.pi * (sr(F(atom["frequency"])) * T + sr(F(atom["phase"])))
    lhs = (s.sin if atom["function"] == "sin" else s.cos)(angle)
    return RELATIONS[atom["relation"]](lhs, sr(F(atom["threshold"])))


def horizon_set(h):
    return s.Interval(sr(F(h["lo"])), sr(F(h["hi"])), h["left_open"], h["right_open"])


def components(solution):
    """Read only exact, fully evaluated finite unions from SymPy."""
    if solution is s.S.EmptySet:
        return []
    if isinstance(solution, s.Union):
        result = [part for arg in solution.args for part in components(arg)]
    elif isinstance(solution, s.Interval):
        result = [(ff(solution.start), ff(solution.end), not bool(solution.left_open),
                   not bool(solution.right_open))]
    elif isinstance(solution, s.FiniteSet):
        result = [(ff(x), ff(x), True, True) for x in solution]
    else:
        raise Unsupported(f"unsupported solved set: {solution}")
    return sorted(result)


def to_set(parts):
    return s.Union(*(s.Interval(sr(lo), sr(hi), not lc, not rc)
                     for lo, hi, lc, rc in parts))


def serialize(parts):
    return [{"lo": str(lo), "hi": str(hi), "left_closed": lc, "right_closed": rc}
            for lo, hi, lc, rc in parts]


def adapter(case):
    """Solve each atom alone, restore its own shifts, then compose."""
    h = case["horizon"]
    lo, hi = F(h["lo"]), F(h["hi"])
    horizon = horizon_set(h)
    joint = horizon
    principal_only = horizon
    records = []
    for atom in case["atoms"]:
        expr = expression(atom)
        period = ff(periodicity(expr.lhs - expr.rhs, T))
        if period <= 0 or period != 2 / F(atom["frequency"]):
            raise Unsupported("unexpected period for declared trig fragment")
        raw = s.solve_univariate_inequality(expr, T, relational=False)
        seed = raw.intersect(s.Interval.Ropen(0, sr(period)))
        parts = components(seed)
        # Seed lies in [0, period), so these bounds include every possible lift.
        first = lo // period - 1
        last = -((-hi) // period) + 1
        if last - first + 1 > 104:
            raise Unsupported("period enumeration exceeds finite budget")
        expanded = to_set([(a + k * period, b + k * period, lc, rc)
                           for k in range(first, last + 1)
                           for a, b, lc, rc in parts]).intersect(horizon)
        joint = joint.intersect(expanded)
        principal_only = principal_only.intersect(seed)
        records.append({"expression": str(expr), "period": str(period),
                        "principal_seed": serialize(parts),
                        "lift_range": [first, last]})
    return components(joint), components(principal_only), records


# Independent phase-event oracle. Angles below are measured in units of pi.
ROOTS = {
    F(-1): (F(3, 2),), F(-1, 2): (F(7, 6), F(11, 6)),
    F(0): (F(0), F(1)), F(1, 2): (F(1, 6), F(5, 6)),
    F(1): (F(1, 2),),
}


def phase_truth(atom, time):
    p = (F(atom["frequency"]) * time + F(atom["phase"])
         + (F(1, 2) if atom["function"] == "cos" else F(0))) % 2
    threshold = F(atom["threshold"])
    if threshold == -1:
        ge = True
    elif threshold == F(-1, 2):
        ge = p <= F(7, 6) or p >= F(11, 6)
    elif threshold == 0:
        ge = p <= 1
    elif threshold == F(1, 2):
        ge = F(1, 6) <= p <= F(5, 6)
    else:
        ge = p == F(1, 2)
    equal = p in ROOTS[threshold]
    return {">=": ge, ">": ge and not equal,
            "<": not ge, "<=": not ge or equal}[atom["relation"]]


def in_horizon(h, time):
    lo, hi = F(h["lo"]), F(h["hi"])
    return (lo < time or (lo == time and not h["left_open"])) and (
        time < hi or (time == hi and not h["right_open"]))


def oracle_truth(case, time):
    return in_horizon(case["horizon"], time) and all(
        phase_truth(a, time) for a in case["atoms"])


def merge_parts(parts):
    result = []
    for lo, hi, lc, rc in sorted(parts):
        if result and (lo < result[-1][1] or
                       (lo == result[-1][1] and (lc or result[-1][3]))):
            a, b, ac, bc = result.pop()
            if lo == a:
                ac = ac or lc
            if hi > b:
                b, bc = hi, rc
            elif hi == b:
                bc = bc or rc
            result.append((a, b, ac, bc))
        else:
            result.append((lo, hi, lc, rc))
    return result


def oracle(case):
    h = case["horizon"]
    lo, hi = F(h["lo"]), F(h["hi"])
    events = {lo, hi}
    for atom in case["atoms"]:
        a = F(atom["frequency"])
        b = F(atom["phase"]) + (F(1, 2) if atom["function"] == "cos" else F(0))
        for root in ROOTS[F(atom["threshold"])]:
            # Solve a*t+b = root+2*k directly from the original input.
            first = (a * lo + b - root) // 2 - 1
            last = -((-(a * hi + b - root)) // 2) + 1
            for k in range(first, last + 1):
                event = (root + 2 * k - b) / a
                if lo <= event <= hi:
                    events.add(event)
    events = sorted(events)
    if len(events) > 1000:
        raise Unsupported("event budget exceeded")
    parts = [(p, p, True, True) for p in events if oracle_truth(case, p)]
    probes = list(events)
    for a, b in zip(events, events[1:]):
        middle = (a + b) / 2
        probes.append(middle)
        if oracle_truth(case, middle):
            parts.append((a, b, False, False))
    return merge_parts(parts), sorted(probes), len(events)


def parts_contain(parts, value):
    return any((a < value or (a == value and lc)) and
               (value < b or (value == b and rc)) for a, b, lc, rc in parts)


def original_truth(case, time):
    answers = []
    for atom in case["atoms"]:
        value = s.simplify(expression(atom).subs(T, sr(time)))
        if value is not s.S.true and value is not s.S.false:
            raise Unsupported(f"exact original substitution undecided at {time}: {value}")
        answers.append(value is s.S.true)
    return in_horizon(case["horizon"], time) and all(answers)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def provenance():
    import sympy.calculus.util
    import sympy.solvers.inequalities
    import sympy.sets.sets
    modules = [sympy.calculus.util, sympy.solvers.inequalities, sympy.sets.sets]
    package_pins = {}
    for name in ("sympy", "mpmath"):
        dist = importlib.metadata.distribution(name)
        record = next(p for p in dist.files if str(p).endswith(".dist-info/RECORD"))
        package_pins[name] = {"version": dist.version,
                              "record_sha256": sha(dist.locate_file(record))}
    return {"repository_baseline": "29e54d32e2ff5349bdb0c3db56fab753a0e44c94",
            "package_pins": package_pins,
            "module_sha256": {m.__name__: sha(m.__file__) for m in modules},
            "artifact_sha256": {n: sha(HERE / n) for n in
                                ("PROTOCOL.md", "cases.json", "requirements.txt", "demo.py")}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "report.json")
    args = parser.parse_args()
    if s.__version__ != "1.14.0":
        raise Unsupported("this recorded demonstration requires SymPy 1.14.0")
    cases = json.loads((HERE / "cases.json").read_text())
    if len(cases) != 10:
        raise Unsupported("the frozen demonstration has exactly ten cases")
    records = []
    for case in cases:
        try:
            validate(case)
            expected, probes, event_count = oracle(case)
            actual, principal, atom_records = adapter(case)
            substitutions = [original_truth(case, p) == oracle_truth(case, p)
                             == parts_contain(actual, p) for p in probes]
            set_agreement = actual == expected
            success = set_agreement and all(substitutions)
            records.append({"id": case["id"], "status": "PASS" if success else "DISAGREEMENT",
                            "horizon": case["horizon"], "atoms": case["atoms"],
                            "verdict": "NONEMPTY" if actual else "EMPTY",
                            "complete_intervals": serialize(actual),
                            "oracle_intervals": serialize(expected),
                            "singleton_count": sum(a == b for a, b, _, _ in actual),
                            "principal_only_intervals": serialize(principal),
                            "principal_only_matches_complete": actual == principal,
                            "principal_only_scope": "documented limited result; not a competitor",
                            "checks": {"exact_set_agreement": set_agreement,
                                       "exact_substitution_agreement": all(substitutions),
                                       "event_count": event_count, "probe_count": len(probes)},
                            "atom_sources": atom_records})
        except Unsupported as exc:
            records.append({"id": case["id"], "status": "UNSUPPORTED", "reason": str(exc)})
        except Exception as exc:
            records.append({"id": case["id"], "status": "ERROR",
                            "error_type": type(exc).__name__, "reason": str(exc)})
    passed = sum(r["status"] == "PASS" for r in records)
    report = {"schema_version": 1, "claim_status": "OBSERVED development regression",
              "method": "ordinary per-atom periodic lifting followed by exact set intersection",
              "provenance": provenance(), "cases": records,
              "summary": {"cases": len(records), "passed": passed,
                          "unsupported": sum(r["status"] == "UNSUPPORTED" for r in records),
                          "errors": sum(r["status"] == "ERROR" for r in records),
                          "all_passed": passed == len(records)}}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["summary"], sort_keys=True))
    return 0 if report["summary"]["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
