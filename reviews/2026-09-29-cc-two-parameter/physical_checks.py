#!/usr/bin/env python3
"""Fixed physical controls; no parameter scan, optimizer, or imported checker."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import json

ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
TRIANGLE = ((1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 3), (3, 1))
CONTROLS = ((1, 6), (2, 5), (3, 2), (3, 4), (4, 3), (5, 2), (5, 7), (3, 5), (4, 6), (6, 10))
PAIRS = TRIANGLE + CONTROLS


def floor(z):
    return z.numerator // z.denominator


def ceil(z):
    return -floor(-z)


def frac(z):
    return z - floor(z)


def safe(phases):
    return all(F(1, 8) <= z <= F(7, 8) for z in phases)


def bezout(a, b):
    if b == 0:
        return a, 1, 0
    d, u, v = bezout(b, a % b)
    return d, v, u - (a // b) * v


def speed_list(p, q):
    # Deliberately independent of the coefficient-row list used for lap transfer.
    return (p, q, p + q, 2*p + q, 3*p + q, 3*p + 2*q, 5*p + 2*q)


def physical(speeds, time):
    products = [speed * time for speed in speeds]
    laps = [floor(z) for z in products]
    phases = [z - n for z, n in zip(products, laps)]
    distances = [min(z, 1-z) for z in phases]
    return {'time': time, 'laps': laps, 'phases': phases, 'distances': distances}


def choose(p, q):
    d = gcd(p, q)
    P, Q = p // d, q // d
    h = ceil(F(3*(Q-P), 8))
    if h <= F(4*Q-P, 8):
        segment, m = 'P3', (0, 0, 0, 1, 1, 1, 2)
        interval = (F(3*(Q-P), 8), F(4*Q-P, 8))
        x = F(8*h + 9*P, 8*(Q+2*P))
        y = F(9, 8) - 2*x
        assert F(3, 8) <= x <= F(1, 2)
    else:
        segment, m = 'P1', (0, 0, 0, 0, 0, 1, 1)
        interval = (F(Q-4*P, 8), F(5*Q-6*P, 24))
        h = ceil(interval[0])
        x = F(8*h + 7*P, 8*(Q+3*P))
        y = F(7, 8) - 3*x
        assert F(1, 8) <= x <= F(5, 24)
    assert interval[0] <= h <= interval[1]
    assert Q*x-P*y == h
    return d, P, Q, segment, interval, h, x, y, m


def case(p, q):
    d, P, Q, segment, interval, h, x, y, m = choose(p, q)
    divisor, r, s = bezout(P, Q)
    assert divisor == 1 and r*P+s*Q == 1
    T = r*x+s*y
    N = floor(T)
    tau = frac(T)
    t = tau / d
    assert 0 < t < F(1, d)
    speeds = speed_list(p, q)
    primitive_speeds = speed_list(P, Q)
    record = physical(speeds, t)
    # Direct geometric expressions, written without referring to ROWS.
    raw = (x, y, x+y, 2*x+y, 3*x+y, 3*x+2*y, 5*x+2*y)
    expected = [z-n for z, n in zip(raw, m)]
    assert record['phases'] == expected and safe(record['phases'])
    assert min(record['distances']) == F(1, 8)
    transferred_laps = [n+(-a*s+b*r)*h-v*N for n, (a,b), v in zip(m, ROWS, primitive_speeds)]
    assert record['laps'] == transferred_laps
    assert frac(p*t) == x and frac(q*t) == y

    # A separate coordinate-lap congruence reconstructs tau without r or s.
    # Q*floor(P*tau) = -h (mod P). The least nonnegative solution gives tau.
    coordinate_lap = 0 if P == 1 else (-h * pow(Q, -1, P)) % P
    congruence_tau = (x+coordinate_lap) / P
    assert 0 <= congruence_tau < 1 and congruence_tau == tau
    assert frac(Q*congruence_tau) == y

    reflected = physical(speeds, 1-t)
    assert safe(reflected['phases'])
    assert reflected['phases'] == [1-z for z in record['phases']]
    assert reflected['laps'] == [v-1-n for v, n in zip(speeds, record['laps'])]

    alternatives = []
    for k in (-3, 2):
        rr, ss = r+k*Q, s-k*P
        TT = rr*x+ss*y
        NN = floor(TT)
        alt_t = frac(TT)/d
        assert TT == T+k*h and NN == N+k*h and alt_t == t
        alt_laps = [n+(-a*ss+b*rr)*h-v*NN for n, (a,b), v in zip(m, ROWS, primitive_speeds)]
        alt_record = physical(speeds, alt_t)
        assert alt_laps == alt_record['laps'] == record['laps']
        assert alt_record['phases'] == expected and safe(alt_record['phases'])
        alternatives.append({'k': k, 'r': rr, 's': ss, 'T': TT, 'N': NN, 'time': alt_t, 'laps': alt_laps})

    wrong_clocks = {}
    for name, clock in (('x', x), ('y', y)):
        trial = physical(speeds, clock)
        failures = [{'index_1_based': i+1, 'speed': v, 'phase': z, 'distance': dist}
                    for i, (v, z, dist) in enumerate(zip(speeds, trial['phases'], trial['distances']))
                    if dist < F(1, 8)]
        wrong_clocks[name] = {'time': clock, 'safe': not failures,
                              'same_as_selected_time': clock == t,
                              'minimum_distance': min(trial['distances']), 'failures': failures}
    return {'p': p, 'q': q, 'd': d, 'P': P, 'Q': Q,
            'distinct_speed_configuration': p != q, 'segment': segment,
            'interval': interval, 'h': h, 'x': x, 'y': y, 'm': m,
            'r': r, 's': s, 'T': T, 'N': N, 'tau': tau,
            'speeds': speeds, 'selected': record, 'transferred_laps': transferred_laps,
            'congruence_coordinate_lap': coordinate_lap, 'congruence_tau': congruence_tau,
            'reflected': reflected, 'alternative_bezout': alternatives, 'wrong_clocks': wrong_clocks}


def negative_fixture(x, y):
    p, q, d = 2, 4, 2
    labels = (0, 0, 0, 1, 1, 1, 2)
    phases = [a*x+b*y-n for (a,b), n in zip(ROWS, labels)]
    raw_h = q*x-p*y
    primitive_h = raw_h/d
    assert y == F(9, 8)-2*x and safe(phases)
    # For any t with {2t}=x, {4t} must equal {2x}.
    forced_y = frac(2*x)
    assert forced_y != y
    return {'p': p, 'q': q, 'd': d, 'x': x, 'y': y, 'phases': phases,
            'raw_h': raw_h, 'primitive_h': primitive_h,
            'naive_integrality_passes': raw_h.denominator == 1,
            'true_compatibility_passes': primitive_h.denominator == 1,
            'forced_y_from_first_coordinate': forced_y,
            'physical_orbit_impossible': forced_y != y}


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    return obj


def main():
    cases = [case(*pair) for pair in PAIRS]
    failed_original = negative_fixture(F(7, 16), F(1, 4))
    replacement = negative_fixture(F(13, 32), F(5, 16))
    assert failed_original['raw_h'] == F(5, 4)
    assert not failed_original['naive_integrality_passes']
    assert replacement['raw_h'] == 1 and replacement['primitive_h'] == F(1, 2)
    assert replacement['naive_integrality_passes'] and not replacement['true_compatibility_passes']
    boundary_case = next(c for c in cases if (c['p'], c['q']) == (1, 4))
    assert boundary_case['segment'] == 'P1' and boundary_case['x'] == F(1, 8)
    assert boundary_case['interval'] == (F(0), F(7, 12))
    result = {
        'status': 'OBSERVED fixed exact physical controls; general claims remain proof candidates',
        'scope': 'Only the protocol 18 positive integer pairs; stationary reference; one selected time and reflection',
        'summary': {
            'pairs': len(cases), 'distinct_speed_configurations': sum(c['p'] != c['q'] for c in cases),
            'repeated_speed_auxiliaries': 1, 'selected_phase_checks': 7*len(cases),
            'reflected_phase_checks': 7*len(cases),
            'direct_selected_and_reflected_distance_checks': 14*len(cases),
            'selected_lap_formula_checks': 7*len(cases),
            'reflected_lap_formula_checks': 7*len(cases),
            'alternate_bezout_recoveries': 2*len(cases),
            'alternate_bezout_phase_and_lap_checks_each': 14*len(cases),
            'independent_congruence_time_recoveries': len(cases),
            'wrong_clock_distance_checks': 14*len(cases),
            'wrong_x_clock_failing_pairs': sum(not c['wrong_clocks']['x']['safe'] for c in cases),
            'wrong_y_clock_failing_pairs': sum(not c['wrong_clocks']['y']['safe'] for c in cases),
            'P3_cases': sum(c['segment'] == 'P3' for c in cases),
            'P1_cases': sum(c['segment'] == 'P1' for c in cases),
            'all_selected_minimum_distances': '1/8',
        },
        'cases': cases,
        'negative_fixtures': {
            'protocol_attempt_preserved': failed_original,
            'corrected_naive_integrality_counterexample': replacement,
        },
        'endpoint_failure': {'primitive_pair': [1, 4], 'closed_P1_interval': [F(0), F(7, 12)],
                             'only_integer': 0, 'open_interval_has_integer': False,
                             'lost_point': [F(1, 8), F(1, 2)]},
        'limits': ['No optimizer, broad scan, all-reference claim, optimality claim, or all-witness enumeration.',
                   'Alternative Bezout checks reuse each physical time; they are recovery invariance checks.',
                   'Separate AI implementation is not human, formal, or externally independent certification.'],
    }
    destination = Path(__file__).with_name('physical_checks.json')
    destination.write_text(json.dumps(encode(result), indent=2) + '\n')
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
