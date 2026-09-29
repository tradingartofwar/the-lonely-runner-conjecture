#!/usr/bin/env python3
"""Frozen exact speed-band audit. Run from any working directory."""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / 'PROTOCOL.json'
EXPECTED = '660a3a7f27f6a1e7b2c0c68aeea22b42366c7a946d5612e967c6f355999d5aae'
DELTA = Q(1, 8)


def floor(x):
    return x.numerator // x.denominator


def valid(i):
    return i[0] < i[1] or (i[0] == i[1] and i[2] and i[3])


def intersection(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    lc = (a[2] if a[0] == lo else True) and (b[2] if b[0] == lo else True)
    rc = (a[3] if a[1] == hi else True) and (b[3] if b[1] == hi else True)
    i = (lo, hi, lc, rc)
    return i if valid(i) else None


def merge(items):
    items = sorted((i for i in items if valid(i)), key=lambda i: (i[0], not i[2], i[1], not i[3]))
    out = []
    for i in items:
        if not out or i[0] > out[-1][1] or (i[0] == out[-1][1] and not(i[2] or out[-1][3])):
            out.append(i)
        else:
            a = out[-1]
            lo, lc = a[0], a[2] or (i[0] == a[0] and i[2])
            hi = max(a[1], i[1])
            rc = (a[3] if a[1] == hi else False) or (i[3] if i[1] == hi else False)
            out[-1] = (lo, hi, lc, rc)
    return out


def meet(a, b):
    return merge([i for x in a for y in b if (i := intersection(x, y)) is not None])


def band_json(i):
    return {'lower': str(i[0]), 'upper': str(i[1]), 'left_closed': i[2], 'right_closed': i[3]}


def bands_json(items):
    return [band_json(i) for i in items]


def time_json(items):
    return [[str(i[0]), str(i[1])] for i in items]


def time_summary(items):
    return {
        'components': time_json(items),
        'positive_components': time_json([i for i in items if i[0] < i[1]]),
        'singletons': [str(i[0]) for i in items if i[0] == i[1]],
        'safe_measure': str(sum((i[1]-i[0] for i in items), Q(0)))
    }


def safe_laps(v):
    return [(Q(8*j+1, 8*v), Q(8*j+7, 8*v), True, True) for j in range(v)]


def core_components(speeds):
    safe = [(Q(0), Q(1), True, True)]
    for v in speeds:
        safe = meet(safe, safe_laps(v))
    return safe


def integer_points(items):
    out = []
    for lo, hi, lc, rc in items:
        first = -floor(-lo)
        if not lc and Q(first) == lo:
            first += 1
        last = floor(hi)
        if not rc and Q(last) == hi:
            last -= 1
        out.extend(range(first, last+1))
    return sorted(set(out))


def component_bands(comp, theta, domain, closed):
    if domain is None:
        return [], []
    lo, hi = comp[:2]
    U = domain[1]
    labelled = []
    for m in range(floor(U + theta + DELTA) + 1):
        trial = ((Q(m)-theta-DELTA)/lo, (Q(m)-theta+DELTA)/hi, closed, closed)
        if valid(trial):
            part = intersection(trial, domain)
            if part is not None:
                labelled.append((part, m))
    return merge([i for i, m in labelled]), labelled


def run():
    raw = PROTOCOL.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED, 'frozen protocol changed'
    protocol = json.loads(raw)
    records = []
    provenance = []
    for spec in protocol['cores']:
        components = core_components(spec['speeds'])
        positive = [i for i in components if i[0] < i[1]]
        w = max(i[1]-i[0] for i in positive)
        U = 1/(4*w)
        c = max(spec['speeds'])
        domain = (Q(c), U, False, True) if U > c else None
        record = {'id': spec['id'], 'speeds': spec['speeds'], **time_summary(components),
                  'width': str(w), 'widest_ties': time_json([i for i in positive if i[1]-i[0] == w]),
                  'cap_U': str(U), 'domain': band_json(domain) if domain else None,
                  'endpoint_slack_caps': [], 'phase_records': [], 'diagnostics': []}
        for index, i in enumerate(components):
            if i[0] == i[1]:
                continue
            ql, qr = i[0].denominator, i[1].denominator
            cap = floor((Q(1,4)-Q(1,ql)-Q(1,qr))/(i[1]-i[0]))
            record['endpoint_slack_caps'].append({'component_index': index, 'q_left': ql,
                'q_right': qr, 'width': str(i[1]-i[0]), 'cap_integer': cap})
        for theta_text in protocol['final_phases']:
            theta = Q(theta_text)
            phase = {'phase': theta_text, 'modes': {}}
            for mode in ('F', 'P', 'Z'):
                selected = [(j, i) for j, i in enumerate(components) if mode == 'F' or i[0] < i[1]]
                current = [domain] if domain else []
                per_component, prefixes = [], []
                for j, i in selected:
                    allowed, labelled = component_bands(i, theta, domain, mode == 'Z')
                    per_component.append({'component_index': j, 'bands': bands_json(allowed)})
                    provenance.append({'id': spec['id'], 'phase': theta_text, 'mode': mode,
                        'component_index': j, 'labelled_bands': [dict(band_json(b), lap=m) for b, m in labelled]})
                    current = meet(current, allowed)
                    prefixes.append({'component_index': j, 'bands': bands_json(current)})
                phase['modes'][mode] = {'bands': bands_json(current), 'integers': integer_points(current),
                    'component_bands': per_component, 'prefix_bands': prefixes}
            record['phase_records'].append(phase)
        for d in spec['diagnostic_final_speeds']:
            final = meet(components, safe_laps(d))
            record['diagnostics'].append({'speed': d, 'phase': '0', **time_summary(final)})
        records.append(record)
    result = {
        'status': 'OBSERVED exact frozen-domain computation; general implications remain proof candidates',
        'protocol_sha256': EXPECTED,
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'method': 'Exact closed safe-band intersections and rational open/closed speed-band intersections',
        'arithmetic': 'fractions.Fraction',
        'records': records,
        'lap_label_provenance': provenance
    }
    target = HERE / 'primary_last_runner.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'output': target.name, 'sha256': sha256(target.read_bytes()).hexdigest(),
                      'core_count': len(records), 'phase_count': len(protocol['final_phases']),
                      'diagnostic_count': sum(len(r['diagnostics']) for r in records)}))


if __name__ == '__main__':
    run()
