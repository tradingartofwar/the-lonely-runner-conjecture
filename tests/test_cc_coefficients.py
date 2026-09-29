"""Frozen exact checker validation; see the dated protocol for complete scope."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import subprocess
import sys
import unittest

from lonely_runner.cc_coefficients import check_coefficients, evaluate_selector, CORE, PROOF_COMMIT

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT/'reviews/2026-09-29-cc-selector-support'


class CoefficientCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = dict(coefficient_cases=[], physical_cases=[], invalid_api=[], cli_cases=[])

    def check_physical(self, out):
        A, B = out['row']
        p, q = out['pair']
        speeds = [a*p+b*q for a, b in CORE+((A, B),)]
        self.assertEqual(out['speeds'], speeds)
        t = F(out['time'])
        raw = [v*t for v in speeds]
        phases = [v % 1 for v in raw]
        laps = [v.numerator//v.denominator for v in raw]
        self.assertEqual(out['phases'], list(map(str, phases)))
        self.assertEqual(out['physical_laps'], laps)
        self.assertTrue(all(F(1, 8) <= f <= F(7, 8) for f in phases[:6]))
        self.assertEqual(out['seventh_safe'], F(1, 8) <= phases[6] <= F(7, 8))
        self.assertEqual(out['distinct_speeds'], len(set([0]+speeds)) == 8)
        self.assertEqual(out['minimum'], str(min(min(f, 1-f) for f in phases)))
        reflected = [v*(1-t) for v in speeds]
        self.assertEqual(out['reflected_time'], str(1-t))
        self.assertEqual(out['reflected_phases'], [str(v % 1) for v in reflected])
        self.assertEqual(out['reflected_laps'], [v.numerator//v.denominator for v in reflected])

    def check_decision(self, out):
        self.assertEqual(out['proof']['commit'], PROOF_COMMIT)
        self.assertEqual(out['threshold'], '1/8')
        A, B = out['row']
        self.assertEqual(out['distinct_speed_domain']['empty'], (A, B) in CORE)
        if out['status'] == 'ACCEPTED':
            leader = out['guarantee']['leader']
            m = leader['seventh_lap']
            for point, value in zip(leader['endpoints'], leader['seventh_values']):
                x, y = map(F, point)
                self.assertEqual(F(value), A*x+B*y)
                self.assertTrue(F(1, 8) <= F(value)-m <= F(7, 8))
            c = out['guarantee']['fallback']
            self.assertEqual(F(c['seventh_value']), F(A+2*B, 8))
            self.assertEqual(F(c['seventh_value'])-c['seventh_lap'], F(c['seventh_phase']))
            self.assertTrue(F(1, 8) <= F(c['seventh_phase']) <= F(7, 8))
        else:
            self.assertEqual(out['status'], 'REJECTED')
            failed = out['counterexample']
            self.check_physical(failed)
            self.assertTrue(failed['distinct_speeds'])
            self.assertFalse(failed['seventh_safe'])
            self.assertEqual(failed['failed_runner_indices'], [7])
            self.assertLess(F(failed['minimum']), F(1, 8))
            if out['reason'] == 'LARGE_SLOPE':
                c = out['construction']
                lo, hi = map(F, c['open_j_interval'])
                self.assertTrue(lo < c['j'] < hi)
            if out['reason'] == 'BOUNDED_DIRECTION':
                self.assertLessEqual(out['construction']['contact_tests'], 11)

    def test_residue_decisions_and_periodicity(self):
        old = json.loads((OLD/'classification.json').read_text())['cells']
        K = 10**20
        for cell in old:
            A, B = cell['representative']
            before = check_coefficients(A, B)
            after = check_coefficients(A+16*K, B+8*K)
            expected = 'ACCEPTED' if cell['T'] else 'REJECTED'
            for group, out in [('baseline', before), ('period_shift', after)]:
                with self.subTest(group=group, row=out['row']):
                    self.assertEqual(out['status'], expected)
                    self.check_decision(out)
                    self.records['coefficient_cases'].append(dict(group=group, result=out))
            if expected == 'REJECTED':
                a, b = before['counterexample'], after['counterexample']
                self.assertEqual(before['reason'], after['reason'])
                self.assertEqual(a['pair'], b['pair'])
                self.assertEqual(a['time'], b['time'])
                self.assertEqual(a['phases'], b['phases'])
                self.assertNotEqual(a['physical_laps'][6], b['physical_laps'][6])
                self.assertEqual(b['physical_laps'][6]-a['physical_laps'][6],
                                 F((16*K*a['pair'][0]+8*K*a['pair'][1]))*F(a['time']))
            else:
                self.assertEqual(after['guarantee']['leader']['seventh_lap']-
                                 before['guarantee']['leader']['seventh_lap'], 7*K)
                self.assertEqual(after['guarantee']['fallback']['seventh_lap']-
                                 before['guarantee']['fallback']['seventh_lap'], 4*K)

    def test_analytic_rejection_branches(self):
        for delta in (-15, -14, 14, 15, -(10**40+14), 10**40+14):
            for b in range(8):
                B = 8*(abs(delta)//8+2)+b
                A = 2*B+delta
                with self.subTest(delta=delta, b=b):
                    out = check_coefficients(A, B)
                    self.assertEqual(out['status'], 'REJECTED')
                    self.check_decision(out)
                    self.records['coefficient_cases'].append(dict(group='large', result=out))

    def test_archived_physical_outputs_and_named_domains(self):
        archive = json.loads((OLD/'witnesses.json').read_text())['progression_controls']
        keys = ('row', 'pair', 'gcd', 'primitive', 'role', 'point', 'h', 'time', 'primitive_time',
                'speeds', 'torus_laps', 'physical_laps', 'phases', 'minimum', 'distinct_speeds',
                'reflected_time', 'reflected_phases', 'reflected_laps')
        for old in archive:
            out = evaluate_selector(*old['row'], *old['pair'])
            self.check_physical(out)
            for key in keys:
                self.assertEqual(out[key], old[key], (old['row'], old['pair'], key))
            self.records['physical_cases'].append(dict(group='archived', record=out))
        for A, B in ((1, 1), (2, 1), (3, 1), (3, 2), (4, 5), (23, 12)):
            decision = check_coefficients(A, B)
            self.check_decision(decision)
            self.assertEqual(decision['status'], 'ACCEPTED')
            out = evaluate_selector(A, B, 2, 3)
            self.check_physical(out)
            self.assertEqual(out['distinct_speeds'], (A, B) not in CORE)
            self.records['physical_cases'].append(dict(group='named', record=out, decision=decision))
        for A, B, p, q in ((4, 2, 1, 2), (5, 2, 2, 3)):
            out = evaluate_selector(A, B, p, q)
            self.check_physical(out)
            self.assertEqual((out['time'], out['phases'][6]), ('1/8', '0'))
            self.records['physical_cases'].append(dict(group='named', record=out))

    def test_invalid_api_inputs(self):
        coefficient_cases = [(0, 2), (-1, 2), (6, 0), (6, -2), (True, 2),
                             (6, False), (6.0, 2), (6, '2'), (None, 2)]
        pair_cases = [(0, 3), (2, 0), (-1, 3), (2, -3), (True, 3), (2, 3.0)]
        cases = [('check_coefficients', check_coefficients, v) for v in coefficient_cases]
        cases += [('evaluate_selector', evaluate_selector, (6, 2)+v) for v in pair_cases]
        for name, fn, args in cases:
            with self.subTest(function=name, args=args):
                with self.assertRaises(ValueError) as cm:
                    fn(*args)
                self.records['invalid_api'].append(dict(function=name, input_repr=repr(args),
                    error_type=type(cm.exception).__name__, message=str(cm.exception)))

    def test_cli_and_optimized_mode(self):
        cases = [(['6', '2'], 'ACCEPTED', 0), (['5', '2'], 'REJECTED', 0),
            (['6', '2', '--p', '4', '--q', '6'], 'ACCEPTED', 0),
            (['1', '1', '--p', '2', '--q', '3'], 'ACCEPTED', 0),
            (['5', '2', '--p', '1', '--q', '3'], 'REJECTED', 0),
            (['6', '2', '--p', '2'], 'INVALID_INPUT', 2),
            (['6', 'two'], 'INVALID_INPUT', 2), (['6.0', '2'], 'INVALID_INPUT', 2),
            (['-1', '2'], 'INVALID_INPUT', 2)]
        for args, status, code in cases:
            outputs = []
            for optimized in (False, True):
                command = [sys.executable]+(['-O'] if optimized else [])
                command += ['-m', 'lonely_runner.cc_coefficients']+args
                run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(run.returncode, code, run.stderr)
                out = json.loads(run.stdout)
                self.assertEqual(out['status'], status)
                if status != 'INVALID_INPUT':
                    self.check_decision(out)
                    if 'requested_evaluation' in out:
                        self.check_physical(out['requested_evaluation'])
                if args == ['5', '2', '--p', '1', '--q', '3']:
                    self.assertTrue(out['requested_evaluation']['seventh_safe'])
                    self.assertFalse(out['counterexample']['seventh_safe'])
                if args == ['1', '1', '--p', '2', '--q', '3']:
                    self.assertTrue(out['distinct_speed_domain']['empty'])
                    self.assertFalse(out['requested_evaluation']['distinct_speeds'])
                self.records['cli_cases'].append(dict(argv=args, optimized=optimized,
                                                     exit_code=run.returncode, output=out))
                outputs.append(out)
            self.assertEqual(outputs[0], outputs[1])


if __name__ == '__main__':
    unittest.main()
