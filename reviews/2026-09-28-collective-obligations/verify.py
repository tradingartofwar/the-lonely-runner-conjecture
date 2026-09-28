#!/usr/bin/env python3
"""Independent exact verification of the collective-obligation study.

This checker does not import the primary implementation and does not use an
optimizer.  It verifies every archived rational primal/dual certificate, then
derives the three controls by Mobius inversion and an explicit parameterization
of the main cover face.  ``--check`` is read-only and standard-library only.
"""

import argparse
from fractions import Fraction as F
import hashlib
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "protocol.json"
PRIMARY = HERE / "primary.py"
RESULTS = HERE / "results.json"
OUT = HERE / "verification.json"
REPORT = HERE / "verification.md"

STATES = list(range(16))
SINGLES = [1 << i for i in range(4)]
PAIRS = [sum(1 << i for i in pair) for pair in combinations(range(4), 2)]
TRIPLES = [sum(1 << i for i in triple) for triple in combinations(range(4), 3)]
MOMENT_MASKS = [0] + SINGLES + PAIRS
EMPTY = [int(state == 0) for state in STATES]


def q(value):
    return value if isinstance(value, F) else F(value)


def incidence(mask):
    return [int(mask == 0 or state & mask == mask) for state in STATES]


H_ROW = [1 if state.bit_count() == 3 else 3 if state == 15 else 0 for state in STATES]
SUM_T_ROW = [sum(incidence(mask)[state] for mask in TRIPLES) for state in STATES]
Q_ROW = incidence(15)


def dot(left, right):
    return sum((q(a) * q(b) for a, b in zip(left, right)), F(0))


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def expected_moments(name):
    if name == "symmetric_collective":
        return {0: F(1), **{m: F(3, 7) for m in SINGLES}, **{m: F(1, 7) for m in PAIRS}}
    if name == "zero_burden_partition":
        return {0: F(1), **{m: F(1, 4) for m in SINGLES}, **{m: F(0) for m in PAIRS}}
    if name == "quadruple_correction":
        return {0: F(1), **{m: F(7, 16) for m in SINGLES}, **{m: F(1, 4) for m in PAIRS}}
    raise KeyError(name)


def moments(distribution):
    x = list(map(q, distribution))
    return {mask: dot(incidence(mask), x) for mask in MOMENT_MASKS}


def diagnostics(distribution):
    x = list(map(q, distribution))
    triples = {mask: dot(incidence(mask), x) for mask in TRIPLES}
    sum_t = sum(triples.values(), F(0))
    q4 = x[15]
    h = dot(H_ROW, x)
    assert h == sum_t - q4
    return {
        "U": x[0],
        "triples": triples,
        "sum_triples": sum_t,
        "Q": q4,
        "H": h,
    }


def archived_diagnostics(distribution):
    result = diagnostics(distribution)
    return {**result, "identity_check_sumT_minus_Q": result["H"]}


def expected_spec(moment_data, objective, *, cover=False, h_upper=None):
    rows = [incidence(mask) for mask in MOMENT_MASKS]
    rhs = [moment_data[mask] for mask in MOMENT_MASKS]
    if cover:
        rows.append(EMPTY)
        rhs.append(F(0))
    le_rows, le_rhs = [], []
    if h_upper is not None:
        le_rows.append(H_ROW)
        le_rhs.append(q(h_upper))
    return list(map(q, objective)), rows, rhs, le_rows, le_rhs


def check_certificate(cert, moment_data, objective, *, cover=False, h_upper=None):
    c, eq_rows, eq_rhs, le_rows, le_rhs = expected_spec(
        moment_data, objective, cover=cover, h_upper=h_upper
    )
    assert list(map(q, cert["objective"])) == c
    assert [list(map(q, row)) for row in cert["eq_rows"]] == [list(map(q, row)) for row in eq_rows]
    assert list(map(q, cert["eq_rhs"])) == eq_rhs
    assert [list(map(q, row)) for row in cert["le_rows"]] == [list(map(q, row)) for row in le_rows]
    assert list(map(q, cert["le_rhs"])) == le_rhs

    x = list(map(q, cert["primal"]))
    y = list(map(q, cert["dual_eq"]))
    z = list(map(q, cert["dual_le"]))
    assert len(x) == 16 and all(value >= 0 for value in x)
    assert len(y) == len(eq_rows) and len(z) == len(le_rows)
    assert all(value <= 0 for value in z)
    assert all(dot(row, x) == rhs for row, rhs in zip(eq_rows, eq_rhs))
    assert all(dot(row, x) <= rhs for row, rhs in zip(le_rows, le_rhs))

    reduced = []
    for state in STATES:
        dual_column = sum((y[i] * q(eq_rows[i][state]) for i in range(len(y))), F(0))
        dual_column += sum((z[i] * q(le_rows[i][state]) for i in range(len(z))), F(0))
        reduced.append(c[state] - dual_column)
    assert all(value >= 0 for value in reduced)
    primal_value = dot(c, x)
    dual_value = dot(y, eq_rhs) + dot(z, le_rhs)
    value = q(cert["value"])
    assert primal_value == dual_value == value
    return {
        "label": cert["label"],
        "value": value,
        "positive_primal_states": [state for state, mass in enumerate(x) if mass],
        "primal_dual_equal": True,
        "reduced_costs_nonnegative": True,
    }


def main_distribution(u, y, q4):
    """Mobius reconstruction for the symmetric main moments.

    ``y[i]`` is the exact-three mass on the state missing event i.  The
    retained moments are met exactly iff u + sum(y) + 3*q4 = 1/7.
    """
    u, q4 = q(u), q(q4)
    y = list(map(q, y))
    assert len(y) == 4
    assert u + sum(y, F(0)) + 3 * q4 == F(1, 7)
    assert min([u, q4, *y]) >= 0
    x = [F(0)] * 16
    x[0], x[15] = u, q4
    for i in range(4):
        x[15 ^ (1 << i)] = y[i]
        x[1 << i] = sum((y[j] for j in range(4) if j != i), F(0)) + 2 * q4
    for i, j in combinations(range(4), 2):
        x[(1 << i) | (1 << j)] = u + y[i] + y[j] + 2 * q4
    assert min(x) >= 0
    assert moments(x) == expected_moments("symmetric_collective")
    return x


def main_parameters(distribution):
    x = list(map(q, distribution))
    y = [x[15 ^ (1 << i)] for i in range(4)]
    u, q4 = x[0], x[15]
    rebuilt = main_distribution(u, y, q4)
    assert rebuilt == x
    return {"u": u, "y_missing_event": y, "q": q4, "face_equation": u + sum(y, F(0)) + 3 * q4}


def canonical_main_models():
    c = F(1, 7)
    open_model = main_distribution(c, [0, 0, 0, 0], 0)
    individual_zero_covers = {}
    concentrated_proper_subset_covers = {}
    for target in TRIPLES:
        missing = next(i for i in range(4) if target == 15 ^ (1 << i))
        y = [F(1, 21)] * 4
        y[missing] = F(0)
        model = main_distribution(0, y, 0)
        assert diagnostics(model)["triples"][target] == 0
        individual_zero_covers[target] = model

        # Concentrating all exact-three mass on target makes every other
        # inclusive triple vanish.  Hence any fixed proper subset of the four
        # triple queries can vanish simultaneously by choosing an omitted one.
        y = [F(0)] * 4
        y[missing] = c
        concentrated = main_distribution(0, y, 0)
        diag = diagnostics(concentrated)
        assert diag["triples"][target] == c
        assert all(diag["triples"][other] == 0 for other in TRIPLES if other != target)
        concentrated_proper_subset_covers[target] = concentrated
    return open_model, individual_zero_covers, concentrated_proper_subset_covers


def analytic_controls(data):
    main = data["cases"][0]
    zero = data["cases"][1]
    quad = data["cases"][2]

    # Every archived main primal is independently inverted into (u,y,q).
    main_primal_parameters = []
    main_certs = [main["baseline"]]
    main_certs += [entry["certificate"] for entry in main["cover_triple_minima"]]
    main_certs += [main["cover_H_minimum"], data["main_H_zero_repair"]]
    for cert in main_certs:
        main_primal_parameters.append({"label": cert["label"], **main_parameters(cert["primal"])})

    open_model, individual_zero, concentrated = canonical_main_models()
    open_diag = diagnostics(open_model)
    assert open_diag == {"U": F(1, 7), "triples": {m: F(0) for m in TRIPLES},
                         "sum_triples": F(0), "Q": F(0), "H": F(0)}
    assert list(map(q, data["main_open_model"])) == open_model
    assert serialize(archived_diagnostics(open_model)) == data["main_open_model_diagnostics"]
    primary_canonical = [list(map(q, model)) for model in data["main_canonical_cover_models"]]
    expected_canonical = [concentrated[mask] for mask in TRIPLES]
    assert primary_canonical == expected_canonical
    assert [serialize(archived_diagnostics(model)) for model in expected_canonical] == data["main_canonical_cover_diagnostics"]

    # The zero-burden moments have C=0. Pair moments zero exclude every state
    # of size >=2; cover then fixes the four singleton masses to 1/4.
    zero_unique = [F(0)] * 16
    for mask in SINGLES:
        zero_unique[mask] = F(1, 4)
    assert moments(zero_unique) == expected_moments("zero_burden_partition")
    assert diagnostics(zero_unique)["H"] == 0
    for model in zero["cover_models"]:
        assert list(map(q, model)) == zero_unique

    # For the quadruple control, on the cover face H=C=3/4. If y is total
    # exact-three mass and q is four-way mass, H=y+3q. Summing the six
    # pair-only masses gives -3/4+3q >= 0, while y>=0 gives q<=1/4.
    # Thus q=1/4 and y=0 uniquely; inversion gives four singleton masses 3/16.
    quad_unique = [F(0)] * 16
    for mask in SINGLES:
        quad_unique[mask] = F(3, 16)
    quad_unique[15] = F(1, 4)
    assert moments(quad_unique) == expected_moments("quadruple_correction")
    quad_diag = diagnostics(quad_unique)
    assert quad_diag["sum_triples"] == 1
    assert quad_diag["Q"] == F(1, 4)
    assert quad_diag["H"] == F(3, 4)
    for model in quad["cover_models"]:
        assert list(map(q, model)) == quad_unique
    assert list(map(q, data["quadruple_supplied_model"])) == quad_unique
    assert serialize(archived_diagnostics(quad_unique)) == data["quadruple_supplied_diagnostics"]

    return {
        "main_cover_face": {
            "parameterization": "u=x_empty, q=x_1234, y_i=x_[4]\\{i}; u+sum(y_i)+3q=1/7; all parameters nonnegative",
            "reconstruction": {
                "singleton_i": "sum_{j!=i} y_j + 2q",
                "pair_ij": "u + y_i + y_j + 2q",
                "triple_missing_i": "y_i",
            },
            "archived_primal_parameters": main_primal_parameters,
            "individual_minima": {mask: F(0) for mask in TRIPLES},
            "sum_of_individual_minima": F(0),
            "minimum_collective_H": F(1, 7),
            "open_model": open_model,
            "individual_zero_cover_models": individual_zero,
            "proper_subset_concentrated_covers": concentrated,
            "proper_subset_limitation": "For any proper subset of the four inclusive triples, concentrate y=1/7 on an omitted triple: every queried triple is zero while U=0.",
            "H_zero_repair": "H=sum(y_i)+3q<=0 forces y_i=q=0, hence u=1/7.",
        },
        "zero_burden": {
            "C": F(0),
            "unique_cover": zero_unique,
            "individual_triple_minima": {mask: F(0) for mask in TRIPLES},
            "minimum_H": F(0),
        },
        "quadruple_correction": {
            "C": F(3, 4),
            "unique_cover": quad_unique,
            "pair_only_mass_sum_on_cover": "-3/4+3q>=0 and sum(y)>=0 force q=1/4",
            "inclusive_triples": {mask: F(1, 4) for mask in TRIPLES},
            "sum_triples": F(1),
            "Q": F(1, 4),
            "H_equals_sumT_minus_Q": F(3, 4),
        },
    }


def markdown_report(output):
    return """# Independent verification: collective higher-order obligations

September 28, 2026 UTC. This verifier is separately structured from the primary calculation: it uses exact rational primal/dual replay plus direct Möbius inversion and face parameterization. It imports no primary functions and uses no optimizer. AI agreement is not independent human mathematical validation.

## Result

All **19 exact LP certificates** pass: three baseline minima, twelve cover-constrained individual-triple minima, three cover-constrained collective minima, and the main `H <= 0` repair. Every primal meets the frozen moments and side constraints; every dual is feasible; exact primal and dual values agree.

For the symmetric main moments, write `u=x_empty`, `q=x_1234`, and `y_i` for exact-three mass on the state missing event `i`. Möbius inversion gives the complete feasible-face parameterization

`u + sum_i y_i + 3q = 1/7`, with all six parameters nonnegative,

and reconstructs the lower states as `x_i=sum_(j!=i)y_j+2q` and `x_ij=u+y_i+y_j+2q`. Therefore on the cover face `u=0`, every individual inclusive triple can have minimum zero, while

`H = sum_K T_K - Q = sum_i y_i + 3q = 1/7`.

This is a real distinction between `sum(min T_K)=0` and `min(sum T_K-Q)=1/7`; the separate minima occur at different covers. In fact, any fixed **proper subset** of the four triple queries can vanish simultaneously: place all `1/7` exact-three mass on an omitted triple. Thus this abstract control genuinely requires a collective all-four statistic under the frozen query language.

The same retained moments also admit the explicit open model `x_empty=1/7` and `x_ij=1/7` for all six exact-pair states, with all other masses zero. Imposing `H<=0` forces this form and repairs the minimum empty mass to `1/7`.

The controls behave as intended. The zero-burden partition is uniquely the four singleton states of mass `1/4`, so all triple and collective minima are zero. In the quadruple control, nonnegative pair-only mass and exact-three mass force `q=1/4` and all exact-three masses to zero. Hence each inclusive triple is `1/4`, raw `sum T=1`, but `H=sum T-Q=3/4`; omitting the `Q` correction would overcount.

## Scope

These are exact finite facts about three prescribed abstract four-event moment models. They do not show that the distributions are realizable by common-start runners, provide a speed-derived upper bound on `H`, or establish a general Lonely Runner selector. The proper-subset limitation is specific to the frozen inclusive-triple query language.

Reproduce read-only with:

```bash
python -B reviews/2026-09-28-collective-obligations/verify.py --check
```
"""


def build():
    protocol_raw = PROTOCOL.read_bytes()
    primary_raw = PRIMARY.read_bytes()
    results_raw = RESULTS.read_bytes()
    protocol = json.loads(protocol_raw)
    data = json.loads(results_raw)
    assert protocol["frozen_before_calculation"] is True
    assert data["protocol_sha256"] == hashlib.sha256(protocol_raw).hexdigest()
    assert data["primary_sha256"] == hashlib.sha256(primary_raw).hexdigest()
    names = [entry["name"] for entry in protocol["prescribed_controls"]]
    assert names == [record["name"] for record in data["cases"]]

    checked = []
    for record in data["cases"]:
        name = record["name"]
        moment_data = expected_moments(name)
        assert {str(mask): str(value) for mask, value in moment_data.items()} == record["moments"]
        c_value = moment_data[0] - sum((moment_data[m] for m in SINGLES), F(0)) + sum(
            (moment_data[m] for m in PAIRS), F(0)
        )
        assert q(record["C"]) == c_value
        checked.append(check_certificate(record["baseline"], moment_data, EMPTY))
        assert [entry["mask"] for entry in record["cover_triple_minima"]] == TRIPLES
        for entry in record["cover_triple_minima"]:
            checked.append(check_certificate(
                entry["certificate"], moment_data, incidence(entry["mask"]), cover=True
            ))
        checked.append(check_certificate(record["cover_H_minimum"], moment_data, H_ROW, cover=True))
        for cert in [record["baseline"], *[entry["certificate"] for entry in record["cover_triple_minima"]], record["cover_H_minimum"]]:
            diag = diagnostics(cert["primal"])
            assert diag["U"] + diag["H"] == c_value

    main_moments = expected_moments("symmetric_collective")
    checked.append(check_certificate(
        data["main_H_zero_repair"], main_moments, EMPTY, h_upper=F(0)
    ))
    assert len(checked) == 19
    analytic = analytic_controls(data)

    assert [q(item["value"]) for item in checked[:6]] == [F(0), F(0), F(0), F(0), F(0), F(1, 7)]
    assert q(data["main_H_zero_repair"]["value"]) == F(1, 7)
    output = {
        "protocol_sha256": hashlib.sha256(protocol_raw).hexdigest(),
        "primary_sha256": hashlib.sha256(primary_raw).hexdigest(),
        "results_sha256": hashlib.sha256(results_raw).hexdigest(),
        "method": "independent Mobius inversion and exact rational primal/dual replay; no primary imports or optimizer",
        "certificates_checked": len(checked),
        "certificates": checked,
        "analytic_verification": analytic,
        "scope": "three frozen abstract four-event controls; no runner realizability inference",
    }
    return serialize(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = build()
    expected_json = json.dumps(output, indent=2, sort_keys=True) + "\n"
    expected_report = markdown_report(output)
    if args.check:
        assert OUT.read_text() == expected_json, "verification.json differs"
        assert REPORT.read_text() == expected_report, "verification.md differs"
        print("PASS: 19 exact certificates, Mobius face, paired models, and controls")
    else:
        OUT.write_text(expected_json)
        REPORT.write_text(expected_report)
        print("Wrote", OUT)
        print("Wrote", REPORT)


if __name__ == "__main__":
    main()
