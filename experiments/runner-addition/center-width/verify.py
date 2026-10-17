"""Alternate band/event check; does not import the H evaluator or primary checker."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import ceil, floor
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('prior_event_verifier', HERE.parent/'verify.py')
events = importlib.util.module_from_spec(spec)
spec.loader.exec_module(events)


def check(ok, message):
    if not ok:
        raise ValueError(message)


def pairs(rows):
    return [tuple(map(F, row)) for row in rows]


def band_pieces(interval, r, d):
    a, b = interval
    pieces = []
    for j in range(floor(r*a)-1, floor(r*b)+2):
        left, right = max(a, (j+d)/r), min(b, (j+1-d)/r)
        if left <= right:
            pieces.append((left, right))
    return pieces


def band_margin(c, speeds, d):
    margins = []
    for s in speeds:
        lap = floor(s*c)
        margins.append(min(c-(lap+d)/s, (lap+1-d)/s-c))
    return min(margins)


def verify(path):
    raw = path.read_bytes()
    result = json.loads(raw)
    cfg = json.loads((HERE/'config.json').read_text())
    freeze = result['freeze_commit']
    manifest = json.loads((HERE/'manifest.json').read_text())
    check((HERE/'manifest.json').read_bytes() == subprocess.check_output(
        ['git', 'show', freeze+':experiments/runner-addition/center-width/manifest.json'], cwd=ROOT),
        'Manifest freeze mismatch')
    for name, expected in manifest['sha256'].items():
        data = (ROOT/name).read_bytes()
        check(hashlib.sha256(data).hexdigest() == expected and data == subprocess.check_output(
            ['git', 'show', freeze+':'+name], cwd=ROOT), 'Dependency freeze mismatch: '+name)
    check(result['study'] == cfg['study'] and result['rule_commit'] == cfg['rule_commit'],
          'Study identity')
    check((HERE/'RULE.md').read_bytes() == subprocess.check_output(
        ['git', 'show', cfg['rule_commit']+':experiments/runner-addition/center-width/RULE.md'], cwd=ROOT),
        'Preselection rule changed')
    counts = Counter()
    independent = []

    def h_certificate(c, d, record, cap=None, intentional=False):
        cap = cfg['max_terms'] if cap is None else cap
        terms = record['terms']
        check(1 <= terms <= min(c.denominator, cap), 'Term count domain')
        # Reproduce only bookkeeping/stop claims here. The mathematical value
        # is checked below by safe-band contact plus a tight critical gap.
        best, critical = F(0), None
        for j in range(1, terms+1):
            m = floor(j*c+F(1, 2))
            needed = max(F(0), (d-abs(j*c-m))/j)
            if needed > best:
                best, critical = needed, j
            stopped = j == c.denominator or (best > 0 and d/(j+1) <= best)
            if j < terms:
                check(not stopped, 'Evaluation continued beyond its frozen stop')
        check(record['critical_speed'] == critical, 'First critical-speed bookkeeping')
        counts['H_terms_audited'] += terms
        if record['status'] == 'UNKNOWN_BUDGET':
            check(not stopped and terms == cap and F(record['lower_bound']) == best,
                  'Invalid unknown H result')
            if not intentional:
                counts['unknowns'] += 1
            return None
        check(record['status'] == 'EXACT' and stopped, 'Unjustified exact status')
        H = F(record['H'])
        check(H == best > 0, 'H bookkeeping value')
        check(record['stop'] == ('DENOMINATOR' if terms == c.denominator else 'BOUND'),
              'Wrong stopping reason')
        r = record['critical_speed']
        m = floor(r*c+F(1, 2))
        check(abs(r*c-m) < d and abs(r*c-m)+r*H == d, 'Critical tight unsafe gap')
        critical_interval = (c-H, c+H)
        cutoff = ceil(d/H)
        check(cutoff-1 <= cfg['max_band_queries'], 'H validation exceeds band budget')
        for speed in range(1, cutoff):
            check(bool(band_pieces(critical_interval, speed, d)), 'Critical width not universal')
            counts['H_band_queries'] += 1
        check(2*H >= 2*d/cutoff, 'Critical-width tail condition')
        counts['H_certificates'] += 1
        return H

    def physical(w, interval, speeds, d):
        r, t = w['r'], F(w['time'])
        check(isinstance(r, int) and r > 0 and r not in speeds, 'Witness admissibility')
        check(interval[0] <= t <= interval[1], 'Witness leaves interval')
        events.verify_witness(w, speeds+[r], d)
        check(t == events.phase_first(interval[0], r, d), 'First-contact discrepancy')
        counts['physical_witnesses'] += 1

    def candidate(row, speeds, d, H):
        a, b = map(F, row['interval'])
        c, h = (a+b)/2, (b-a)/2
        check(F(row['center']) == c and F(row['halfwidth']) == h and 0 < a <= b < 1,
              'Candidate coordinates')
        G = band_margin(c, speeds, d)
        check(F(row['G']) == G >= h, 'Core band containment or G mismatch')
        for s in speeds:
            lap = floor(s*a)
            check((lap+d)/s <= a <= b <= (lap+1-d)/s, 'Core interval crosses unsafe gap')
        counts['candidate_intervals'] += 1
        if H is None:
            check(row['decision'] == 'UNKNOWN_H_BUDGET', 'H unknown promoted')
            return
        expected = 'UNIVERSAL_CANDIDATE' if h >= H else 'BLOCKED'
        check(row['decision'] == expected, 'H comparison decision')
        if h == 0:
            blocker = a.denominator
            check(blocker not in speeds and not band_pieces((a, b), blocker, d),
                  'Singleton denominator did not block')
            alternate = 'BLOCKED'
            counts['candidate_band_queries'] += 1
        else:
            R = ceil(d/h)
            alternate = None
            for r in range(1, min(R-1, cfg['max_band_queries'])+1):
                if r in speeds:
                    continue
                counts['candidate_band_queries'] += 1
                if not band_pieces((a, b), r, d):
                    alternate = 'BLOCKED'
                    break
            if alternate is None:
                alternate = 'UNIVERSAL_CANDIDATE' if R-1 <= cfg['max_band_queries'] else 'UNKNOWN'
        if alternate == 'UNKNOWN':
            counts['unknowns'] += 1
        else:
            check(alternate == row['decision'], 'FALSE POSITIVE/NEGATIVE against exact bands')
            counts['decision_agreements'] += 1
        if row['decision'] == 'BLOCKED':
            r, m = row['blocker']['r'], row['blocker']['integer']
            check(r > 0 and r not in speeds and (m-d)/r < a <= b < (m+d)/r,
                  'Strict blocker gap mismatch')
            counts['strict_blockers'] += 1
            return
        check(row['cutoff'] == R and 2*h >= 2*d/R, 'Actual interval tail')
        if R-1 > cfg['max_band_queries']:
            check(row['recovery_status'] == 'UNKNOWN_RECOVERY_BUDGET', 'Recovery budget')
            counts['unknowns'] += 1
            return
        check(row['recovery_status'] == 'COMPLETE', 'Incomplete recovery')
        domain = [r for r in range(1, R) if r not in speeds]
        check([w['r'] for w in row['finite_witnesses']] == domain, 'Finite witness domain')
        tail = []
        for r in (R, R+1, 10**6+1, 10**18+1):
            while r in speeds:
                r += 1
            if r not in tail:
                tail.append(r)
        check([w['r'] for w in row['tail_witnesses']] == tail, 'Tail controls')
        for w in row['finite_witnesses']+row['tail_witnesses']:
            physical(w, (a, b), speeds, d)

    def children(rows, candidates, speeds, d):
        expected = sorted({x['blocker']['r'] for x in candidates if x['decision'] == 'BLOCKED'})
        check([x['r'] for x in rows] == expected, 'Blocker child list')
        for row in rows:
            r = row['r']
            if r > cfg['max_child_speed']:
                check(row['status'] == 'UNKNOWN_CHILD_BUDGET', 'Child cap')
                counts['unknowns'] += 1
                continue
            full, event_count = events.event_set(speeds+[r], d)
            check(full == pairs(row['safe_set']), 'Full child set mismatch')
            check(row['status'] == ('NONEMPTY' if full else 'EMPTY'), 'Child feasibility status')
            if full:
                physical(row['witness'], full[0], speeds, d)
                check(F(row['witness']['time']) == full[0][0], 'Child earliest witness')
            else:
                check(row['witness'] is None, 'Empty child has witness')
                counts['empty_children'] += 1
            counts['child_sets'] += 1
            counts['threshold_events'] += event_count

    controls = result['controls']
    check([x['name'] for x in controls] == ['equality', 'term_budget'], 'Controls')
    check(h_certificate(F(1, 4), F(1, 10), controls[0]['result']) == F(1, 40), 'Equality H')
    physical(controls[0]['witness'], (F(9, 40), F(11, 40)), [1], F(1, 10))
    check(F(controls[0]['witness']['time']) == F(9, 40), 'Closed equality contact')
    check(h_certificate(F(159, 1330), F(1, 10), controls[1]['result'], 1, True) is None,
          'Expected control unknown')
    counts['controls'] = 2

    expected_keys = [(F(c), n) for c in cfg['palette_centers'] for n in cfg['palette_n']]
    check([(F(x['center']), x['n']) for x in result['constructed']] == expected_keys, 'Constructed domain')
    for row in result['constructed']:
        c, n, d = F(row['center']), row['n'], F(row['threshold'])
        check(d == F(1, n), 'Constructed threshold')
        H = h_certificate(c, d, row['H_certificate'])
        if H is None:
            check(row['status'] == 'UNKNOWN_H_BUDGET' and not row['cores'], 'Unknown palette')
            continue
        bound = floor((F(1, 2)-d)/H)
        palette = []
        for s in range(1, bound+1):
            lap = floor(s*(c-H))
            if (lap+d)/s <= c-H <= c+H <= (lap+1-d)/s:
                palette.append(s)
            counts['palette_band_checks'] += 1
        check(row['palette_bound'] == bound and row['palette'] == palette, 'Palette discrepancy')
        check(F(row['shortcut_halfwidth']) == d/c.denominator and
              row['shortcut_matches'] == (H == d/c.denominator), 'Shortcut result')
        counts['palette_rows'] += 1
        if len(palette) < n-2:
            check(row['status'] == 'INSUFFICIENT_PALETTE' and not row['cores'], 'Insufficient palette')
            counts['insufficient_palettes'] += 1
            continue
        check(row['status'] == 'READY' and
              [x['selection'] for x in row['cores']] == cfg['palette_selections'], 'Core selections')
        for core in row['cores']:
            speeds = palette[:n-2] if core['selection'] == 'smallest' else palette[-(n-2):]
            check(core['speeds'] == speeds and len(set(speeds)) == n-2, 'Constructed core')
            if sum(speeds) > cfg['max_core_sum']:
                check(core['status'] == 'UNKNOWN_CORE_BUDGET', 'Constructed core budget')
                counts['unknowns'] += 1
                continue
            check(core['status'] == 'COMPLETE', 'Constructed status')
            widths = [('critical', H), ('half', H/2), ('denominator_only', d/c.denominator)]
            check([x['name'] for x in core['candidates']] == [x[0] for x in widths], 'Candidate labels')
            for actual, (_, h) in zip(core['candidates'], widths):
                check(tuple(map(F, actual['interval'])) == (c-h, c+h), 'Candidate width')
                candidate(actual, speeds, d, H)
            children(core['children'], core['candidates'], speeds, d)
            counts['constructed_cores'] += 1

    check([x['name'] for x in result['challenge']] ==
          [x['name'] for x in cfg['challenge_cores']], 'Challenge list')
    for row, spec in zip(result['challenge'], cfg['challenge_cores']):
        check(all(row[k] == value for k, value in spec.items()), 'Challenge input changed')
        speeds, d = row['speeds'], F(row['threshold'])
        check(d == F(1, row['n']) and len(set(speeds)) == row['n']-2, 'Challenge n/d')
        if sum(speeds) > cfg['max_core_sum']:
            check(row['status'] == 'UNKNOWN_CORE_BUDGET', 'Challenge input cap')
            counts['unknowns'] += 1
            continue
        core, event_count = events.event_set(speeds, d)
        check(core == pairs(row['core']) and row['core_input_bands'] == sum(speeds), 'Complete challenge core')
        counts['core_sets'] += 1
        counts['threshold_events'] += event_count
        if len(core) > cfg['max_components']:
            check(row['status'] == 'UNKNOWN_CORE_BUDGET', 'Component cap')
            counts['unknowns'] += 1
            continue
        check(row['status'] == ('COMPLETE' if core else 'EMPTY_CORE'), 'Challenge status')
        check(len(row['components']) == len(core), 'Missing component')
        tally = Counter()
        for i, (actual, interval) in enumerate(zip(row['components'], core)):
            check(actual['id'] == i and tuple(map(F, actual['interval'])) == interval, 'Component ID/geometry')
            c = sum(interval)/2
            H = h_certificate(c, d, actual['H_certificate'])
            candidate(actual, speeds, d, H)
            check(F(actual['G']) == (interval[1]-interval[0])/2, 'Maximal component G')
            tally[actual['decision']] += 1
        children(row['children'], row['components'], speeds, d)
        independent.append({'name': row['name'], 'components': len(core), 'decisions': dict(tally)})
    return {'status': 'PASS' if not counts['unknowns'] else 'PARTIAL',
            'freeze_commit': freeze, 'rule_commit': cfg['rule_commit'],
            'source_results_sha256': hashlib.sha256(raw).hexdigest(),
            'counts': dict(sorted(counts.items())), 'challenge': independent,
            'false_positives': 0, 'false_negatives': 0,
            'limits': 'Same-author alternate verification; universal implications remain proof candidates.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE/'results/RESULTS.json')
    parser.add_argument('--output', type=Path, default=HERE/'results/VERIFICATION.json')
    args = parser.parse_args()
    report = verify(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(report['status'], json.dumps(report['counts'], sort_keys=True))
