"""Exact coefficient decision for the fixed CC first-integer L/C selector.

Run: python3 -m lonely_runner.cc_coefficients A B [--p p --q q]
The universal classification is an internally reviewed proof candidate.
REJECTED means this selector fails on a supplied input, not failed loneliness.
No research-output files or third-party dependencies are needed at runtime.
"""
import argparse
from fractions import Fraction as F
from math import gcd
import json
import re

CORE = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2))
SMALL_FAILURE_DIRECTIONS = ((1, 2), (1, 3), (2, 1), (1, 4), (1, 5),
                            (2, 3), (1, 6), (3, 2), (2, 5), (4, 1), (1, 8))
PROOF_COMMIT = '57997d4220226b44b9a89d8d8139926f15cca90c'
PROOF_NOTE = 'notes/CC_SELECTOR_SUPPORT_2026_09_29.md'
SELECTOR_ID = 'CC-L-C-first-integer-v1'


def _positive_integer(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f'{name} must be a positive integer; booleans and coercions are not accepted.')
    return value


def _require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def _floor(x):
    return x.numerator // x.denominator


def _phase(x):
    return x - _floor(x)


def _safe(x):
    return F(1, 8) <= _phase(x) <= F(7, 8)


def _json_ready(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [_json_ready(v) for v in value]
    if isinstance(value, dict):
        return {k: _json_ready(v) for k, v in value.items()}
    return value


def _point(P, Q):
    M = Q + 2*P
    rho = (-P - 2*M) % 8
    h = (2*Q - 3*P + rho) // 8
    if rho <= M:
        x = F(1, 4) + F(rho, 8*M)
        y, role = F(7, 8) - 2*x, 'L'
    else:
        _require((P, Q) == (1, 2), 'Unexpected leader miss; no certificate returned.')
        x, y, h, role = F(1, 8), F(1, 4), 0, 'C'
    _require(Q*x - P*y == h, 'Orbit identity failed.')
    return x, y, h, role, M, rho


def _bezout(P, Q):
    a, b, r, r1, s, s1 = P, Q, 1, 0, 0, 1
    while b:
        quotient = a // b
        a, b = b, a - quotient*b
        r, r1 = r1, r - quotient*r1
        s, s1 = s1, s - quotient*s1
    _require(a == 1 and r*P + s*Q == 1, 'Primitive Bezout identity failed.')
    return r, s


def _domain(A, B):
    duplicate = [A, B] if (A, B) in CORE else None
    return dict(empty=duplicate is not None, identically_repeated_core_row=duplicate,
                conditions=dict(p_not_equal_q=True,
                    nonzero_linear_forms=[dict(core_row=[a, b], p_coefficient=A-a,
                                              q_coefficient=B-b) for a, b in CORE[2:]]))


def evaluate_selector(A, B, p, q):
    """Evaluate one labelled physical configuration, whether safe or unsafe.

    This does not require uniform acceptance of (A,B). Positive repeated-speed
    configurations are retained with distinct_speeds=False.
    All fractions in the returned JSON-ready record are exact strings.
    """
    for name, value in (('A', A), ('B', B), ('p', p), ('q', q)):
        _positive_integer(value, name)
    d = gcd(p, q)
    P, Q = p//d, q//d
    x, y, h, role, M, rho = _point(P, Q)
    r, s = _bezout(P, Q)
    T = r*x + s*y
    N = _floor(T)
    tau, t = T-N, (T-N)/d
    _require(0 < tau < 1 and _phase(P*tau) == x and _phase(Q*tau) == y,
             'Physical clock recovery failed.')
    rows = CORE + ((A, B),)
    speeds = [a*p + b*q for a, b in rows]
    raw = [a*x + b*y for a, b in rows]
    torus_laps = [_floor(v) for v in raw]
    phases = [_phase(v) for v in raw]
    physical_laps = [m + (-a*s+b*r)*h - (a*P+b*Q)*N
                     for (a, b), m in zip(rows, torus_laps)]
    _require(phases == [_phase(v*t) for v in speeds], 'Direct physical phases disagree.')
    _require(physical_laps == [_floor(v*t) for v in speeds], 'Direct physical laps disagree.')
    core_safe = all(F(1, 8) <= f <= F(7, 8) for f in phases[:6])
    _require(core_safe, 'The fixed six-core witness is unsafe; no certificate returned.')
    distances = [min(f, 1-f) for f in phases]
    reflected_time = 1-t
    reflected_phases = [_phase(v*reflected_time) for v in speeds]
    reflected_laps = [_floor(v*reflected_time) for v in speeds]
    _require(reflected_phases == [1-f if f else F(0) for f in phases], 'Reflection phases disagree.')
    _require(reflected_laps == [v-m-int(bool(f)) for v, m, f in zip(speeds, physical_laps, phases)],
             'Reflection laps disagree.')
    distinct = len(set([0]+speeds)) == 8
    collisions = [[a, b] for a, b in CORE[2:] if (A-a)*p + (B-b)*q == 0]
    _require(distinct == (p != q and not collisions), 'Distinctness checks disagree.')
    return _json_ready(dict(row=[A, B], pair=[p, q], gcd=d, primitive=[P, Q],
        selector=SELECTOR_ID, role=role, point=[x, y], h=h, M=M, rho=rho,
        bezout=[r, s], N=N, primitive_time=tau, time=t, speeds=speeds,
        torus_laps=torus_laps, physical_laps=physical_laps, phases=phases,
        distances=distances, minimum=min(distances), core_safe=core_safe,
        seventh_safe=distances[6] >= F(1, 8),
        failed_runner_indices=[i+1 for i, distance in enumerate(distances) if distance < F(1, 8)],
        distinct_speeds=distinct, repeated_initial_speeds=p == q,
        seventh_core_collisions=collisions, reflected_time=reflected_time,
        reflected_phases=reflected_phases, reflected_laps=reflected_laps))


def check_coefficients(A, B):
    """Return ACCEPTED with a uniform guarantee, or REJECTED with a failure.

    ValueError means invalid input. ArithmeticError means an internal
    inconsistency and must not be interpreted as mathematical rejection.
    The proof source is an internally reviewed candidate, not a formal proof.
    """
    _positive_integer(A, 'A')
    _positive_integer(B, 'B')
    u, v, w = 2*A+3*B, 3*A+B, A+2*B
    delta, a = A-2*B, u % 8
    D = abs(delta)
    m, c_lap = min(u, v)//8, w//8
    leader_safe = 8*m+1 <= min(u, v) <= max(u, v) <= 8*m+7
    c_safe = w % 8 != 0
    result = dict(schema='cc-coefficient-decision-v1', row=[A, B], delta=delta,
        B_mod8=B % 8, threshold='1/8', selector=SELECTOR_ID,
        proof=dict(status='internally reviewed proof candidate', commit=PROOF_COMMIT, note=PROOF_NOTE),
        distinct_speed_domain=_domain(A, B),
        scope='Uniform safety of this fixed selector; rejection does not imply absence of other lonely times.')
    if leader_safe and c_safe:
        result.update(status='ACCEPTED', guarantee=dict(
            quantifier='Every positive integer p,q has a labelled safe selected time; eight-distinct-speed use requires the stated domain.',
            leader=dict(endpoints=[[F(1, 4), F(3, 8)], [F(3, 8), F(1, 8)]],
                        seventh_values=[F(u, 8), F(v, 8)], seventh_lap=m,
                        safe_band=[F(8*m+1, 8), F(8*m+7, 8)]),
            fallback=dict(point=[F(1, 8), F(1, 4)], seventh_value=F(w, 8),
                          seventh_lap=c_lap, seventh_phase=F(w % 8, 8)),
            recovery='d=gcd(p,q), P=p/d, Q=q/d; rP+sQ=1; tau={rx+sy}; t=tau/d; recompute every row lap.',
            minimum_selected_distance='1/8'))
        return _json_ready(result)
    construction = dict(left_phase=F(a, 8), absolute_delta=D)
    if not c_safe:
        pair, reason = (1, 2), 'FALLBACK_COLLISION'
    elif a == 0:
        pair, reason = (2, 3), 'LEADER_START_COLLISION'
    elif (delta > 0 and a == 7) or (delta < 0 and a == 1):
        j = max(2, (7*D)//8+1)
        _require(F(0) < F(7*D, 32*j) < F(1, 4), 'Outward-boundary construction failed.')
        pair, reason = (1, 4*j-2), 'OUTWARD_BOUNDARY'
        construction.update(j=j, drift_magnitude=F(7*D, 32*j))
    elif D >= 14:
        c = 7-a if delta > 0 else a-1
        _require(1 <= c <= 6, 'Invalid first-forbidden-band parameter.')
        lower, upper = F(7*D, 4*(c+2)), F(7*D, 4*c)
        j = _floor(lower)+1
        _require(lower < j < upper and j >= 2, 'Strict integer interval construction failed.')
        pair, reason = (1, 4*j-2), 'LARGE_SLOPE'
        construction.update(c=c, j=j, open_j_interval=[lower, upper],
                            drift_magnitude=F(7*D, 32*j))
    else:
        attempts, pair = [], None
        for P, Q in SMALL_FAILURE_DIRECTIONS:
            x, y, _, _, _, _ = _point(P, Q)
            value = A*x+B*y
            attempts.append(dict(pair=[P, Q], seventh_phase=_phase(value)))
            if not _safe(value):
                pair = (P, Q)
                break
        _require(pair is not None, 'Bounded rejection certificate missing; no mathematical verdict returned.')
        reason = 'BOUNDED_DIRECTION'
        construction.update(attempts=attempts, contact_tests=len(attempts))
    failed = evaluate_selector(A, B, *pair)
    _require(failed['core_safe'] and not failed['seventh_safe'] and failed['distinct_speeds']
             and failed['failed_runner_indices'] == [7], 'Invalid physical rejection certificate.')
    result.update(status='REJECTED', reason=reason, construction=construction,
                  counterexample=failed)
    return _json_ready(result)


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def _cli_integer(text, name):
    if not re.fullmatch(r'[+-]?[0-9]+', text):
        raise ValueError(f'{name} must be decimal integer text.')
    return _positive_integer(int(text), name)


def main(argv=None):
    parser = _Parser(description='Exact coefficient decision for the fixed CC L/C selector; proof-candidate scope.')
    parser.add_argument('A')
    parser.add_argument('B')
    parser.add_argument('--p', help='Optional positive physical parameter; requires --q.')
    parser.add_argument('--q', help='Optional positive physical parameter; requires --p.')
    try:
        args = parser.parse_args(argv)
        A, B = _cli_integer(args.A, 'A'), _cli_integer(args.B, 'B')
        if (args.p is None) != (args.q is None):
            raise ValueError('--p and --q must be supplied together.')
        pair = None if args.p is None else (_cli_integer(args.p, 'p'), _cli_integer(args.q, 'q'))
    except ValueError as exc:
        print(json.dumps(dict(status='INVALID_INPUT', error=str(exc)), sort_keys=True))
        return 2
    result = check_coefficients(A, B)
    if pair is not None:
        result['requested_evaluation'] = evaluate_selector(A, B, *pair)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
