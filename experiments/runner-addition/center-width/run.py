"""Frozen center-width criterion evaluation; exact arithmetic, bounded domains."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import ceil, floor
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import feasible_intervals


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'),
                      default=lambda x: str(x) if isinstance(x, F) else x)+'\n'


def preflight(freeze):
    manifest = HERE/'manifest.json'
    require(manifest.read_bytes() == subprocess.check_output(
        ['git', 'show', freeze+':experiments/runner-addition/center-width/manifest.json'], cwd=ROOT),
        'Manifest differs from freeze')
    for path, expected in json.loads(manifest.read_text())['sha256'].items():
        raw = (ROOT/path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected, 'Modified dependency: '+path)
        require(raw == subprocess.check_output(['git', 'show', freeze+':'+path], cwd=ROOT),
                'Dependency differs from execution freeze: '+path)


def distance(x):
    f = x % 1
    return min(f, 1-f)


def required_halfwidth(c, d, cap):
    best, critical = F(0), None
    for j in range(1, min(c.denominator, cap)+1):
        value = max(F(0), d-distance(j*c))/j
        if value > best:
            best, critical = value, j
        reason = ('DENOMINATOR' if j == c.denominator else
                  'BOUND' if best > 0 and d/(j+1) <= best else None)
        if reason:
            return {'status': 'EXACT', 'H': best, 'critical_speed': critical,
                    'terms': j, 'stop': reason}
    return {'status': 'UNKNOWN_BUDGET', 'lower_bound': best,
            'critical_speed': critical, 'terms': min(c.denominator, cap)}


def permitted_halfwidth(c, speeds, d):
    return min((distance(s*c)-d)/s for s in speeds)


def witness(interval, r, speeds, d):
    a, b = interval
    lap = ceil(r*a-(1-d))
    t = max(a, (lap+d)/r)
    require(a <= t <= b, 'Recovery leaves source')
    phases = [s*t % 1 for s in speeds+[r]]
    require(all(d <= f <= 1-d for f in phases), 'Unsafe physical witness')
    return {'r': r, 'time': t, 'phases': phases,
            'laps': [floor(s*t) for s in speeds+[r]]}


def candidate(interval, speeds, d, H, cfg):
    a, b = interval
    c, h = (a+b)/2, (b-a)/2
    G = permitted_halfwidth(c, speeds, d)
    require(0 < a <= b < 1 and h <= G, 'Candidate is not wholly core-safe')
    out = {'interval': interval, 'center': c, 'halfwidth': h, 'G': G}
    if H['status'] != 'EXACT':
        return {**out, 'decision': 'UNKNOWN_H_BUDGET'}
    if h < H['H']:
        r = H['critical_speed']
        m = floor(r*c+F(1, 2))
        require(r not in speeds and r*b-d < m < r*a+d, 'Invalid critical blocker')
        return {**out, 'decision': 'BLOCKED', 'blocker': {'r': r, 'integer': m}}
    R = ceil(2*d/(b-a))
    out.update({'decision': 'UNIVERSAL_CANDIDATE', 'cutoff': R})
    if R-1 > cfg['max_band_queries']:
        return {**out, 'recovery_status': 'UNKNOWN_RECOVERY_BUDGET'}
    finite = [r for r in range(1, R) if r not in speeds]
    tail = []
    for seed in (R, R+1, 10**6+1, 10**18+1):
        while seed in speeds:
            seed += 1
        if seed not in tail:
            tail.append(seed)
    return {**out, 'recovery_status': 'COMPLETE',
            'finite_witnesses': [witness(interval, r, speeds, d) for r in finite],
            'tail_witnesses': [witness(interval, r, speeds, d) for r in tail]}


def children(candidates, speeds, d, cfg):
    rows = []
    for r in sorted({x['blocker']['r'] for x in candidates if x['decision'] == 'BLOCKED'}):
        if r > cfg['max_child_speed']:
            rows.append({'r': r, 'status': 'UNKNOWN_CHILD_BUDGET'})
            continue
        core = feasible_intervals(speeds+[r], d)
        rows.append({'r': r, 'status': 'NONEMPTY' if core else 'EMPTY', 'safe_set': core,
                     'witness': witness(core[0], r, speeds, d) if core else None})
    return rows


def run(freeze, checkpoint):
    preflight(freeze)
    cfg = json.loads((HERE/'config.json').read_text())
    require((HERE/'RULE.md').read_bytes() == subprocess.check_output(
        ['git', 'show', cfg['rule_commit']+':experiments/runner-addition/center-width/RULE.md'], cwd=ROOT),
        'Rule differs from preselection freeze')
    out = {'study': cfg['study'], 'freeze_commit': freeze, 'rule_commit': cfg['rule_commit'],
           'claim_status': 'same-author proof candidates; independent review pending',
           'controls': [], 'constructed': [], 'challenge': []}
    checkpoint.mkdir(parents=True, exist_ok=True)
    def save(label):
        (checkpoint/(label+'.json')).write_text(encoded(out))

    eq = required_halfwidth(F(1, 4), F(1, 10), cfg['max_terms'])
    require(eq['H'] == F(1, 40) and eq['critical_speed'] == 4, 'Equality control')
    eq_time = witness((F(9, 40), F(11, 40)), 4, [1], F(1, 10))
    unknown = required_halfwidth(F(159, 1330), F(1, 10), 1)
    require(unknown['status'] == 'UNKNOWN_BUDGET', 'Unknown control')
    out['controls'] = [{'name': 'equality', 'result': eq, 'witness': eq_time},
                       {'name': 'term_budget', 'result': unknown}]

    for center in cfg['palette_centers']:
        c = F(center)
        for n in cfg['palette_n']:
            d = F(1, n)
            H = required_halfwidth(c, d, cfg['max_terms'])
            row = {'center': c, 'n': n, 'threshold': d, 'H_certificate': H, 'cores': []}
            if H['status'] != 'EXACT':
                row['status'] = 'UNKNOWN_H_BUDGET'
            else:
                h = H['H']
                bound = floor((F(1, 2)-d)/h)
                palette = [s for s in range(1, bound+1) if distance(s*c) >= d+s*h]
                row.update({'palette_bound': bound, 'palette': palette,
                            'shortcut_halfwidth': d/c.denominator,
                            'shortcut_matches': h == d/c.denominator})
                row['status'] = 'READY' if len(palette) >= n-2 else 'INSUFFICIENT_PALETTE'
                if row['status'] == 'READY':
                    for selection in cfg['palette_selections']:
                        speeds = palette[:n-2] if selection == 'smallest' else palette[-(n-2):]
                        if sum(speeds) > cfg['max_core_sum']:
                            row['cores'].append({'selection': selection, 'speeds': speeds,
                                                 'status': 'UNKNOWN_CORE_BUDGET'})
                            continue
                        candidates = []
                        for name, width in [('critical', h), ('half', h/2),
                                            ('denominator_only', d/c.denominator)]:
                            candidates.append({'name': name, **candidate((c-width, c+width), speeds, d, H, cfg)})
                        row['cores'].append({'selection': selection, 'speeds': speeds, 'status': 'COMPLETE',
                                             'candidates': candidates,
                                             'children': children(candidates, speeds, d, cfg)})
            out['constructed'].append(row)
            save('constructed_'+str(len(out['constructed'])))

    for spec in cfg['challenge_cores']:
        speeds, d = spec['speeds'], F(1, spec['n'])
        require(len(set(speeds)) == 8 and min(speeds) > 0, 'Invalid challenge input')
        row = {**spec, 'threshold': d}
        if sum(speeds) > cfg['max_core_sum']:
            row['status'] = 'UNKNOWN_CORE_BUDGET'
        else:
            core = feasible_intervals(speeds, d)
            row.update({'core': core, 'core_input_bands': sum(speeds), 'components': []})
            if len(core) > cfg['max_components']:
                row['status'] = 'UNKNOWN_CORE_BUDGET'
            else:
                row['status'] = 'COMPLETE' if core else 'EMPTY_CORE'
                for i, interval in enumerate(core):
                    c = sum(interval)/2
                    H = required_halfwidth(c, d, cfg['max_terms'])
                    result = candidate(interval, speeds, d, H, cfg)
                    require(result['G'] == result['halfwidth'], 'Maximal component margin mismatch')
                    row['components'].append({'id': i, 'H_certificate': H, **result})
                row['children'] = children(row['components'], speeds, d, cfg)
        out['challenge'].append(row)
        save(spec['name'])
    preflight(freeze)
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', required=True)
    parser.add_argument('--output', type=Path, default=HERE/'results/RESULTS.json')
    parser.add_argument('--checkpoint-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run(args.freeze, args.checkpoint_dir)
    args.output.write_text(encoded(result))
    print('Completed', len(result['constructed']), 'constructed rows and',
          len(result['challenge']), 'challenge cores')
