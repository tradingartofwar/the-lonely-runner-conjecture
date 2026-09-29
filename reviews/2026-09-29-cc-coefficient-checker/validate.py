#!/usr/bin/env python3
"""Run the frozen unittest scope and retain exact runtime outputs for review."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:
        raise RuntimeError('Run this review harness without -O; runtime optimization is tested separately.')
    spec = importlib.util.spec_from_file_location('cc_frozen_tests', ROOT/'tests/test_cc_coefficients.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(module.CoefficientCheckerTests)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    records = module.CoefficientCheckerTests.records
    counts = dict(coefficient_cases=len(records['coefficient_cases']),
        coefficient_groups=dict(Counter(v['group'] for v in records['coefficient_cases'])),
        decisions=dict(Counter(v['result']['status'] for v in records['coefficient_cases'])),
        rejection_branches=dict(Counter(v['result'].get('reason') for v in records['coefficient_cases'] if v['result']['status']=='REJECTED')),
        physical_cases=len(records['physical_cases']), invalid_api_cases=len(records['invalid_api']),
        cli_cases=len(records['cli_cases']), unittest_methods=result.testsRun)
    files = ['lonely_runner/cc_coefficients.py', 'tests/test_cc_coefficients.py',
             'reviews/2026-09-29-cc-selector-support/classification.json',
             'reviews/2026-09-29-cc-selector-support/witnesses.json',
             str((HERE/'PROTOCOL.md').relative_to(ROOT)), str(Path(__file__).relative_to(ROOT))]
    output = dict(status='PASS', counts=counts,
                  provenance={name:digest(ROOT/name) for name in files}, **records)
    (HERE/'validation.json').write_text(json.dumps(output, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps(dict(status='PASS', counts=counts), sort_keys=True))


if __name__ == '__main__':
    main()
