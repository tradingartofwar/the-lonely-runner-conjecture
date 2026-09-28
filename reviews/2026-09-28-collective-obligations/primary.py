"""Exact primary study for the frozen collective-obligation protocol.

The 16 nonnegative variables are exact-state masses for four abstract events.
Only total, singleton, and pair moments are retained.  This is an abstract
event-measure calculation: no primal distribution is asserted to be realizable
by common-start runners.

``--write`` may use SciPy only to propose bases and dual multipliers.  Every
candidate is accepted with exact Fraction arithmetic before being serialized.
``--check`` is read-only and uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "protocol.json"
OUT = HERE / "results.json"
MASKS = list(range(16))
SINGLES = [1 << i for i in range(4)]
PAIRS = [sum(1 << i for i in ij) for ij in combinations(range(4), 2)]
TRIPLES = [sum(1 << i for i in ijk) for ijk in combinations(range(4), 3)]
MOMENT_MASKS = [0] + SINGLES + PAIRS


def incidence(mask: int) -> list[int]:
    """Inclusive moment row; mask 0 denotes total mass."""
    return [int(mask == 0 or state & mask == mask) for state in MASKS]


EMPTY = [int(state == 0) for state in MASKS]
H_ROW = [1 if state.bit_count() == 3 else 3 if state == 15 else 0 for state in MASKS]
SUM_TRIPLES_ROW = [sum(incidence(t)[state] for t in TRIPLES) for state in MASKS]
Q_ROW = incidence(15)


def q(value) -> F:
    return value if isinstance(value, F) else F(value)


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(v) for v in value]
    return value


def solve_linear(rows, rhs):
    """Solve a full-column-rank exact system, allowing redundant rows."""
    if not rows or not rows[0]:
        return []
    aug = [[q(x) for x in row] + [q(b)] for row, b in zip(rows, rhs)]
    n = len(rows[0])
    pivot_row = 0
    pivots = []
    for column in range(n):
        pivot = next((r for r in range(pivot_row, len(aug)) if aug[r][column]), None)
        if pivot is None:
            continue
        aug[pivot_row], aug[pivot] = aug[pivot], aug[pivot_row]
        d = aug[pivot_row][column]
        aug[pivot_row] = [x / d for x in aug[pivot_row]]
        for r in range(len(aug)):
            if r != pivot_row and aug[r][column]:
                d = aug[r][column]
                aug[r] = [x - d * y for x, y in zip(aug[r], aug[pivot_row])]
        pivots.append(column)
        pivot_row += 1
    assert all(any(row[:-1]) or not row[-1] for row in aug), "inconsistent basis"
    assert len(pivots) == n, (len(pivots), n)
    result = [F(0)] * n
    for r, column in enumerate(pivots):
        result[column] = aug[r][-1]
    return result


def moments_for(case: str) -> dict[int, F]:
    if case == "symmetric_collective":
        return {0: F(1), **{m: F(3, 7) for m in SINGLES}, **{m: F(1, 7) for m in PAIRS}}
    if case == "zero_burden_partition":
        return {0: F(1), **{m: F(1, 4) for m in SINGLES}, **{m: F(0) for m in PAIRS}}
    if case == "quadruple_correction":
        # x_1234=1/4 and x_i=3/16 for i=1..4.
        return {0: F(1), **{m: F(7, 16) for m in SINGLES}, **{m: F(1, 4) for m in PAIRS}}
    raise KeyError(case)


def make_spec(moments, objective, *, cover=False, h_upper=None, label=""):
    spec = {
        "label": label,
        "objective": list(objective),
        "eq_rows": [incidence(m) for m in MOMENT_MASKS],
        "eq_rhs": [moments[m] for m in MOMENT_MASKS],
        "eq_labels": ["total" if m == 0 else f"moment_{m}" for m in MOMENT_MASKS],
        "le_rows": [],
        "le_rhs": [],
        "le_labels": [],
    }
    if cover:
        spec["eq_rows"].append(EMPTY)
        spec["eq_rhs"].append(F(0))
        spec["eq_labels"].append("empty_mass_zero")
    if h_upper is not None:
        spec["le_rows"].append(H_ROW)
        spec["le_rhs"].append(q(h_upper))
        spec["le_labels"].append("collective_H_upper")
    return spec


def verify_certificate(cert):
    primal = list(map(q, cert["primal"]))
    dual_eq = list(map(q, cert["dual_eq"]))
    dual_le = list(map(q, cert["dual_le"]))
    eq_rows = cert["eq_rows"]
    eq_rhs = list(map(q, cert["eq_rhs"]))
    le_rows = cert["le_rows"]
    le_rhs = list(map(q, cert["le_rhs"]))
    objective = list(map(q, cert["objective"]))
    assert len(primal) == 16
    assert len(dual_eq) == len(eq_rows) == len(eq_rhs)
    assert len(dual_le) == len(le_rows) == len(le_rhs)
    assert all(x >= 0 for x in primal)
    assert all(z <= 0 for z in dual_le)
    assert all(sum(a * x for a, x in zip(row, primal)) == b for row, b in zip(eq_rows, eq_rhs))
    assert all(sum(a * x for a, x in zip(row, primal)) <= b for row, b in zip(le_rows, le_rhs))
    for state in MASKS:
        lhs = sum(y * row[state] for y, row in zip(dual_eq, eq_rows))
        lhs += sum(z * row[state] for z, row in zip(dual_le, le_rows))
        assert lhs <= objective[state], (cert["label"], state, lhs, objective[state])
    primal_value = sum(c * x for c, x in zip(objective, primal))
    dual_value = sum(y * b for y, b in zip(dual_eq, eq_rhs))
    dual_value += sum(z * b for z, b in zip(dual_le, le_rhs))
    assert primal_value == dual_value == q(cert["value"]), cert["label"]


def propose_certificate(spec):
    """Use floating LP only for discovery, then accept a rational certificate."""
    import numpy as np
    from scipy.optimize import linprog

    aeq = np.array(spec["eq_rows"], dtype=float)
    beq = np.array(spec["eq_rhs"], dtype=float)
    aub = np.array(spec["le_rows"], dtype=float) if spec["le_rows"] else None
    bub = np.array(spec["le_rhs"], dtype=float) if spec["le_rhs"] else None
    result = linprog(
        np.array(spec["objective"], dtype=float),
        A_eq=aeq,
        b_eq=beq,
        A_ub=aub,
        b_ub=bub,
        bounds=(0, None),
        method="highs",
    )
    assert result.success, result.message
    support = [i for i, x in enumerate(result.x) if x > 1e-9]
    active = [i for i, x in enumerate(result.ineqlin.residual) if abs(x) < 1e-9]
    rows = spec["eq_rows"] + [spec["le_rows"][i] for i in active]
    rhs = spec["eq_rhs"] + [spec["le_rhs"][i] for i in active]
    values = solve_linear([[row[i] for i in support] for row in rows], rhs)
    primal = [F(0)] * 16
    for i, value in zip(support, values):
        primal[i] = value
    dual_eq = [F(float(x)).limit_denominator(10**6) for x in result.eqlin.marginals]
    dual_le = [F(float(x)).limit_denominator(10**6) for x in result.ineqlin.marginals]
    cert = {
        **spec,
        "primal": primal,
        "dual_eq": dual_eq,
        "dual_le": dual_le,
        "value": sum(c * x for c, x in zip(spec["objective"], primal)),
    }
    verify_certificate(cert)
    return serialize(cert)


def moment_vector(distribution):
    values = list(map(q, distribution))
    return {m: sum(a * x for a, x in zip(incidence(m), values)) for m in MOMENT_MASKS}


def diagnostics(distribution):
    values = list(map(q, distribution))
    triples = {t: sum(a * x for a, x in zip(incidence(t), values)) for t in TRIPLES}
    sum_triples = sum(triples.values(), F(0))
    q4 = values[15]
    h = sum(a * x for a, x in zip(H_ROW, values))
    return {
        "U": values[0],
        "triples": triples,
        "sum_triples": sum_triples,
        "Q": q4,
        "H": h,
        "identity_check_sumT_minus_Q": sum_triples - q4,
    }


def canonical_main_cover(active_triple):
    """Transparent symmetric cover with only ``active_triple`` positive.

    If d is the omitted label, assign 1/7 to the triple, the three exact
    pairs {d,i}, and the three singleton states {i}, i in active_triple.
    """
    assert active_triple in TRIPLES
    omitted = 15 ^ active_triple
    distribution = [F(0)] * 16
    distribution[active_triple] = F(1, 7)
    for singleton in SINGLES:
        if singleton & active_triple:
            distribution[singleton] = F(1, 7)
            distribution[singleton | omitted] = F(1, 7)
    return distribution


def check_case(record, archived=None):
    name = record["name"]
    moments = moments_for(name)
    lp_count = 0

    def solve(spec, old=None):
        nonlocal lp_count
        lp_count += 1
        if old is None:
            return propose_certificate(spec)
        expected = serialize(spec)
        assert {k: old[k] for k in expected} == expected
        verify_certificate(old)
        return old

    old = archived or {}
    baseline = solve(make_spec(moments, EMPTY, label=f"{name}:baseline_U"), old.get("baseline"))
    triple_minima = []
    for index, triple in enumerate(TRIPLES):
        old_cert = old.get("cover_triple_minima", [{}] * 4)[index].get("certificate") if archived else None
        cert = solve(
            make_spec(moments, incidence(triple), cover=True, label=f"{name}:cover_T_{triple}"),
            old_cert,
        )
        triple_minima.append({"mask": triple, "certificate": cert})
    h_minimum = solve(make_spec(moments, H_ROW, cover=True, label=f"{name}:cover_H"), old.get("cover_H_minimum"))

    c_value = moments[0] - sum(moments[m] for m in SINGLES) + sum(moments[m] for m in PAIRS)
    cover_models = [entry["certificate"]["primal"] for entry in triple_minima]
    record_out = {
        "name": name,
        "moments": moments,
        "C": c_value,
        "baseline": baseline,
        "cover_triple_minima": triple_minima,
        "cover_H_minimum": h_minimum,
        "cover_models": cover_models,
        "cover_model_diagnostics": [diagnostics(model) for model in cover_models],
        "cost": {"lp_solves": lp_count, "logical_states_per_lp": 16},
    }
    assert all(moment_vector(model) == moments for model in cover_models)
    assert all(q(model[0]) == 0 for model in cover_models)
    assert all(q(entry["certificate"]["value"]) == diagnostics(model)["triples"][entry["mask"]]
               for entry, model in zip(triple_minima, cover_models))
    # Mobius/inclusion-exclusion identity, checked on each explicit optimizer.
    for model in [baseline["primal"], *cover_models, h_minimum["primal"]]:
        d = diagnostics(model)
        assert d["U"] + d["H"] == c_value
        assert d["H"] == d["sum_triples"] - d["Q"]
    result = serialize(record_out)
    if archived is not None:
        assert result == archived
    return result


def build_or_check(data=None):
    protocol = json.loads(PROTOCOL.read_text())
    names = [control["name"] for control in protocol["prescribed_controls"]]
    assert names == ["symmetric_collective", "zero_burden_partition", "quadruple_correction"]
    records = []
    for i, name in enumerate(names):
        records.append(check_case({"name": name}, data["cases"][i] if data else None))

    main = records[0]
    main_moments = moments_for("symmetric_collective")
    repair_spec = make_spec(main_moments, EMPTY, h_upper=F(0), label="symmetric_collective:H_le_0_repair")
    if data is None:
        repair = propose_certificate(repair_spec)
    else:
        repair = data["main_H_zero_repair"]
        expected = serialize(repair_spec)
        assert {k: repair[k] for k in expected} == expected
        verify_certificate(repair)
    open_model = repair["primal"]
    assert moment_vector(open_model) == main_moments
    open_diag = diagnostics(open_model)
    assert open_diag["U"] == F(1, 7) and open_diag["H"] == 0

    canonical_covers = [canonical_main_cover(triple) for triple in TRIPLES]
    for triple, model in zip(TRIPLES, canonical_covers):
        assert moment_vector(model) == main_moments
        d = diagnostics(model)
        assert d["U"] == 0 and d["H"] == F(1, 7) and d["Q"] == 0
        assert d["triples"][triple] == F(1, 7)
        assert all(value == 0 for mask, value in d["triples"].items() if mask != triple)

    # The main pair is explicit and exact: four covered models (one per omitted
    # triple) and one open model have identical retained moments.
    for i, entry in enumerate(main["cover_triple_minima"]):
        assert q(entry["certificate"]["value"]) == 0
        assert q(main["cover_models"][i][0]) == 0
    assert q(main["cover_H_minimum"]["value"]) == F(1, 7)

    zero = records[1]
    assert q(zero["cover_H_minimum"]["value"]) == 0
    quad = records[2]
    assert q(quad["cover_H_minimum"]["value"]) == F(3, 4)
    supplied_quad = [F(0)] * 16
    supplied_quad[15] = F(1, 4)
    for state in SINGLES:
        supplied_quad[state] = F(3, 16)
    assert moment_vector(supplied_quad) == moments_for("quadruple_correction")
    supplied_quad_diag = diagnostics(supplied_quad)
    assert supplied_quad_diag["sum_triples"] == 1
    assert supplied_quad_diag["Q"] == F(1, 4)
    assert supplied_quad_diag["H"] == F(3, 4)

    totals = {
        "lp_solves": sum(r["cost"]["lp_solves"] for r in records) + 1,
        "baseline_lp_solves": 3,
        "cover_triple_lp_solves": 12,
        "cover_H_lp_solves": 3,
        "repair_lp_solves": 1,
        "logical_states_per_lp": 16,
        "rational_certificates": 19,
    }
    out = {
        "baseline": protocol["baseline"],
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "primary_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "representation": "16 exact-state masses; retained total, four singles, six pairs",
        "certificate_convention": "min c.x with Aeq.x=b, Ale.x<=h, x>=0; dual y free,z<=0; Aeq^T.y+Ale^T.z<=c; exact equal objectives",
        "cases": records,
        "main_H_zero_repair": repair,
        "main_open_model": open_model,
        "main_open_model_diagnostics": open_diag,
        "main_canonical_cover_models": canonical_covers,
        "main_canonical_cover_diagnostics": [diagnostics(model) for model in canonical_covers],
        "quadruple_supplied_model": supplied_quad,
        "quadruple_supplied_diagnostics": supplied_quad_diag,
        "total_cost": totals,
        "scope_warning": "Abstract event-measure models only; no physical runner realizability or speed-search claim.",
    }
    result = serialize(out)
    if data is not None:
        assert result == data
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    assert args.write ^ args.check, "choose exactly one of --write or --check"
    if args.write:
        data = build_or_check()
        OUT.write_text(json.dumps(data, indent=2) + "\n")
    else:
        data = json.loads(OUT.read_text())
        build_or_check(data)
    main_case = data["cases"][0]
    print("main baseline U", main_case["baseline"]["value"])
    print("main cover triple minima", [x["certificate"]["value"] for x in main_case["cover_triple_minima"]])
    print("main cover H minimum", main_case["cover_H_minimum"]["value"])
    print("main H<=0 repaired U", data["main_H_zero_repair"]["value"])
    print("zero-burden cover H minimum", data["cases"][1]["cover_H_minimum"]["value"])
    print("quadruple sumT,Q,H", data["quadruple_supplied_diagnostics"]["sum_triples"], data["quadruple_supplied_diagnostics"]["Q"], data["quadruple_supplied_diagnostics"]["H"])
    print("cost", data["total_cost"])
    print("PASS: 19 exact primal/dual certificates and all paired-model identities verified.")


if __name__ == "__main__":
    main()
