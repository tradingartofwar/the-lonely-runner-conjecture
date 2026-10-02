"""Independent small checks of the frozen conformance example; no root edits."""
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from copy import deepcopy
from contextlib import redirect_stdout
from fractions import Fraction as F
import io
import json
import hashlib
import tempfile
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TARGET = ROOT / 'examples/compatibility-conformance/check.py'
FIXTURE = ROOT / 'examples/compatibility-conformance/fixtures.json'


def load(path, name):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    checker = load(TARGET, 'review_conformance')
    archived = load(ROOT / 'reviews/2026-09-30-cc-three-parameter/verify.py', 'review_old_physical')
    data = json.loads(FIXTURE.read_text())
    source_checks = []
    for path, digest in data['source_sha256'].items():
        pinned = subprocess.check_output(['git', 'show', data['source_commit'] + ':' + path], cwd=ROOT)
        local = (ROOT / path).read_bytes()
        require(local == pinned and hashlib.sha256(pinned).hexdigest() == digest, 'Source does not match pinned commit: ' + path)
        source_checks.append({'path': path, 'sha256': digest, 'local_equals_git_blob': True})
    comparisons = []
    for case in data['cases']:
        if case['query_kind'] == 'closed_phase_bands':
            event_union, _ = checker.safe_set(case['rates'], F(case['delta']))
            band_union = archived.safe_intervals(case['rates'], F(case['delta']))
            require(event_union == band_union, case['id'] + ': event/band disagreement')
            comparisons.append({'case': case['id'], 'method': 'successive exact band intersection versus event decomposition', 'equal': True, 'complete_set': event_union})
    cases = {c['id']: c for c in data['cases']}
    point = cases['complete_relations']
    # The alternative candidate enumeration uses the third phase, not the first.
    p = list(map(F, point['point']))
    times = [(F(j) + p[2]) / point['rates'][2] for j in range(point['rates'][2])]
    surviving = [t for t in times if [(v*t) % 1 for v in point['rates']] == p]
    require(surviving == [], 'independent point exclusion failed')
    comparisons.append({'case': point['id'], 'method': 'third-coordinate lap enumeration', 'candidates': times, 'surviving': surviving})
    clock = cases['clock_lifts']
    p = list(map(F, clock['point']))
    times = [(F(j) + p[2]) / clock['rates'][2] for j in range(clock['rates'][2])]
    surviving = [t for t in times if [(v*t) % 1 for v in clock['rates']] == p]
    require(surviving == [F(11, 16)], 'independent clock recovery failed')
    comparisons.append({'case': clock['id'], 'method': 'third-coordinate lap enumeration', 'candidates': times, 'surviving': surviving})

    mutations = []
    def probe(name, alter, should_reject):
        mutated = deepcopy(data)
        alter(mutated)
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / 'fixtures.json').write_text(json.dumps(mutated))
            checker.HERE = folder
            checker.ROOT = ROOT
            try:
                with redirect_stdout(io.StringIO()):
                    checker.run(folder / 'result.json')
                accepted = True
                error = None
            except Exception as exc:
                accepted = False
                error = type(exc).__name__ + ': ' + str(exc)
            mutations.append({'mutation': name, 'accepted': accepted, 'desired_for_strict_source_contract': 'reject' if should_reject else 'accept', 'error': error})

    probe('wrong expected source digest', lambda d: d['source_sha256'].__setitem__(next(iter(d['source_sha256'])), '0'*64), True)
    probe('wrong clock expected time', lambda d: d['cases'][2].__setitem__('expected_times', ['3/16']), True)
    probe('removed isolated point from expected full set', lambda d: d['cases'][3]['expected_intervals'].pop(), True)
    probe('wrong source selector', lambda d: d['cases'][0]['source'].__setitem__('selector', 'diagnostics.DOES_NOT_EXIST'), True)
    probe('wrong claimed source commit', lambda d: d.__setitem__('source_commit', '0'*40), True)
    probe('changed same-point physical rates without source update', lambda d: d['cases'][0].__setitem__('rates', [1, 2, 7]), True)
    probe('unknown query kind accepted through else branch', lambda d: d['cases'][3].__setitem__('query_kind', 'UNKNOWN_QUERY_KIND'), True)
    probe('replace widest primary by a different safe core singleton', lambda d: d['cases'][4].__setitem__('primary_interval', ['11/24', '11/24']), True)
    probe('wrong mutant label', lambda d: d['cases'][4].__setitem__('mutant', 'UNKNOWN_MUTANT'), True)
    probe('missing source pin', lambda d: d['source_sha256'].pop(next(iter(d['source_sha256']))), True)
    probe('duplicated case identity', lambda d: d['cases'][4].__setitem__('id', d['cases'][3]['id']), True)
    result = {
        'reviewed_checker_sha256': hashlib.sha256(TARGET.read_bytes()).hexdigest(),
        'reviewed_fixture_sha256': hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        'source_checks': source_checks,
        'arithmetic_comparisons': comparisons,
        'mutation_checks': mutations,
        'limits': 'Audit controls for this frozen fixture, not independent human certification, a parser security audit, or external solver defect evidence.'
    }
    (HERE / 'conformance_review_checks.json').write_text(json.dumps(result, default=lambda x: str(x) if isinstance(x, F) else None, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'arithmetic_comparisons': len(comparisons), 'mutations': len(mutations), 'accepted_mutations': [x['mutation'] for x in mutations if x['accepted']]}))


if __name__ == '__main__':
    main()
