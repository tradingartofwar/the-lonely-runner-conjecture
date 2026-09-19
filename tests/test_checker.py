"""Run: python -m unittest discover -s tests -v. No third-party packages."""

from fractions import Fraction as Q
from itertools import combinations, permutations
import json
import random
import subprocess
import sys
import unittest

from lonely_runner.checker import (
    ComputationLimitError, check, circular_distance, exact_maximum,
    feasible_intervals, normalize,
)


class ExactFixtures(unittest.TestCase):
    def test_planned_maxima(self):
        for speeds, expected in [((1,), Q(1, 2)), ((1, 2), Q(1, 3)), ((1, 3), Q(1, 2)),
                                 ((1, 2, 3), Q(1, 4)), ((1, 3, 4, 7), Q(1, 5)), ((2, 4), Q(1, 3))]:
            with self.subTest(speeds=speeds):
                peak = exact_maximum(speeds)
                self.assertEqual(peak.value, expected)
                self.assertEqual(feasible_intervals(speeds, expected), tuple((t, t) for t in peak.times))

    def test_equality_instants_are_not_lost(self):
        self.assertEqual(feasible_intervals([1, 2], Q(1, 3)), ((Q(1, 3), Q(1, 3)), (Q(2, 3), Q(2, 3))))

    def test_full_nonzero_intervals(self):
        self.assertEqual(feasible_intervals([1, 3], Q(1, 3)), ((Q(4, 9), Q(5, 9)),))

    def test_artificial_impossible_threshold(self):
        self.assertEqual(feasible_intervals([1, 2], Q(2, 5)), ())
        result = check([0, 1, 2], threshold="2/5")
        self.assertFalse(result["feasible"])
        self.assertIsNone(result["witness_original"])
        self.assertEqual(result["conjecture_threshold"], "1/3")

    def test_half_track_and_above(self):
        self.assertEqual(feasible_intervals([1, 3], Q(1, 2)), ((Q(1, 2), Q(1, 2)),))
        self.assertEqual(feasible_intervals([1, 2], Q(1, 2)), ())
        self.assertEqual(feasible_intervals([1, 3], Q(51, 100)), ())

    def test_direct_signed_distances(self):
        self.assertEqual(circular_distance(Q(-7, 3)), Q(1, 3))
        self.assertEqual(circular_distance(Q(9, 2)), Q(1, 2))
        self.assertEqual(circular_distance(-10), 0)

    def test_three_starting_cases(self):
        expected = [(2, "1/3", "1/3"), (3, "1/2", "1/2"), (4, "2/5", "2/5")]
        for speed, separation, first_peak in expected:
            result = check([0, 1, speed])
            self.assertEqual(result["maximum"]["separation"], separation)
            self.assertEqual(result["maximum"]["times_original"][0], first_peak)
            for ref in range(3):
                self.assertTrue(check([0, 1, speed], ref)["feasible"])


class NormalizationTests(unittest.TestCase):
    def test_opposite_speeds_keep_original_runner_count(self):
        result = check([0, 1, 2], reference=1)
        self.assertEqual(result["normalization"]["constraint_speeds"], [1])
        self.assertEqual(result["n"], 3)
        self.assertEqual(result["threshold"], "1/3")
        self.assertEqual(result["intervals_original"], [["1/3", "2/3"]])
        self.assertEqual(result["maximum"]["separation"], "1/2")

    def test_gcd_scaling_back_to_original_time(self):
        result = check([0, 2, 4])
        self.assertEqual(result["period_original"], "1/2")
        self.assertEqual(result["witness_original"], "1/6")
        self.assertEqual(result["maximum"]["times_original"], ["1/6", "1/3"])

    def test_rational_denominator_and_gcd_both_survive(self):
        result = check([Q(1, 3), Q(5, 3), 3])
        self.assertEqual(result["normalization"]["denominator_lcm"], 3)
        self.assertEqual(result["normalization"]["integer_gcd"], 4)
        self.assertEqual(result["period_original"], "3/4")
        self.assertEqual(result["maximum"]["times_original"], ["1/4", "1/2"])

    def test_translation_reflection_and_permutation(self):
        original = [0, 1, 3, 4, 7]
        baseline = check(original)
        for transformed in [[v + Q(2, 7) for v in original], [-v for v in original], [7, 0, 4, 1, 3]]:
            ref = 1 if transformed == [7, 0, 4, 1, 3] else 0
            result = check(transformed, ref)
            self.assertEqual(result["maximum"]["separation"], baseline["maximum"]["separation"])
            self.assertEqual(result["intervals_original"], baseline["intervals_original"])

    def test_gcd_one_need_not_begin_with_one(self):
        self.assertEqual(normalize([0, 2, 3]).speeds, (2, 3))
        self.assertEqual(check([0, 2, 3])["maximum"]["separation"], "2/5")

    def test_scale_changes_times_not_maximum(self):
        baseline = check([0, 1, 4])
        for scale in [Q(2, 3), Q(-5, 2), Q(9)]:
            result = check([0, scale, 4 * scale])
            self.assertEqual(result["maximum"]["separation"], baseline["maximum"]["separation"])
            self.assertEqual([Q(t) for t in result["maximum"]["times_original"]],
                             [Q(t) / abs(scale) for t in baseline["maximum"]["times_original"]])

    def test_original_coordinates_at_all_reference_witnesses(self):
        # Seeded, bounded regression cases, not a research atlas or theorem.
        rng = random.Random(19092026)
        for _ in range(20):
            values = [Q(v, 3) for v in rng.sample(range(-8, 9), 4)]
            for ref in range(len(values)):
                result = check(values, ref)
                self.assertTrue(result["feasible"])
                t = Q(result["witness_original"])
                self.assertTrue(all(circular_distance((v - values[ref]) * t) >= Q(1, len(values))
                                    for i, v in enumerate(values) if i != ref))
                for detail in result["maximum"]["witness_details"]:
                    distances = [Q(d["distance"]) for d in detail["distances"]]
                    self.assertEqual(min(distances), Q(result["maximum"]["separation"]))
                    self.assertTrue(detail["limiting_runner_indices"])


class IndependentMethods(unittest.TestCase):
    def test_bounded_crosscheck_at_below_and_above_maximum(self):
        cases = 0
        for k in range(1, 5):
            for speeds in combinations(range(1, 9), k):
                with self.subTest(speeds=speeds):
                    peak = exact_maximum(speeds)
                    self.assertEqual(feasible_intervals(speeds, peak.value), tuple((t, t) for t in peak.times))
                    self.assertTrue(feasible_intervals(speeds, peak.value - Q(1, 1000)))
                    self.assertEqual(feasible_intervals(speeds, peak.value + Q(1, 1000)), ())
                    cases += 1
        self.assertEqual(cases, 162)

    def test_constraint_permutations_and_duplicates(self):
        baseline = exact_maximum([1, 3, 4])
        for speeds in permutations([1, 3, 4]):
            self.assertEqual(exact_maximum(speeds), baseline)
        self.assertEqual(exact_maximum([1, 1, 3, 4]), baseline)


class RejectionsAndCLI(unittest.TestCase):
    def test_invalid_original_inputs(self):
        for values in [[], [1], [0, 0], [0, "1/0"], [0, 0.1], [0, True], [0, "0.5"], [0, "nan"], [0, "1/2", Q(1, 2)]]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                check(values)

    def test_invalid_reference(self):
        for ref in [-1, 3, True, "0", 0.0]:
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                check([0, 1, 2], ref)

    def test_invalid_normalized_constraints(self):
        for speeds in [[], [0], [-1], [1.0], [True]]:
            for method in [lambda v: feasible_intervals(v, Q(1, 3)), exact_maximum]:
                with self.subTest(speeds=speeds), self.assertRaises(ValueError):
                    method(speeds)

    def test_invalid_threshold(self):
        for delta in [0, -1, 0.3, "1/0"]:
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                check([0, 1, 2], threshold=delta)

    def test_resource_limits_are_errors_not_failed_conjectures(self):
        with self.assertRaises(ComputationLimitError):
            feasible_intervals([1, 20001], Q(1, 3))
        with self.assertRaises(ComputationLimitError):
            exact_maximum([1, 1000001])

    def test_feasibility_only_reports_no_maximum(self):
        result = check([0, 1, 2], compute_maximum=False)
        self.assertIsNone(result["maximum"])
        self.assertTrue(result["feasible"])

    def test_cli_json_all_references(self):
        proc = subprocess.run([sys.executable, "-m", "lonely_runner", "--velocities", "0", "1", "2", "--all-references", "--json"], capture_output=True, text=True, check=True)
        results = json.loads(proc.stdout)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r["feasible"] for r in results))

    def test_cli_negative_fractions(self):
        proc = subprocess.run([sys.executable, "-m", "lonely_runner", "--velocities=-1/2,0,1/2", "--json"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(proc.stdout)["witness_original"], "2/3")

    def test_cli_invalid_input_is_nonzero_exit(self):
        proc = subprocess.run([sys.executable, "-m", "lonely_runner", "--velocities", "0", "0"], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "")
        self.assertIn("distinct", proc.stderr)


if __name__ == "__main__":
    unittest.main()
