"""Replay issued times, independently audit every switched obstruction, and aggregate costs."""
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial.adaptive_anchor.choose import adaptive
from observatory.escape_trial.last_anchor.arms import first_issue
from observatory.escape_trial.last_anchor.score import physical_trial
from observatory.escape_trial.rule import predict

PANEL = 'f12acb9e634c9839b74ea8cdb60b66227856da844570275e88a2f7030133864d'


def audit(weights):
    assert predict(weights) is None and all(first_issue(weights, q) is None for q in (3, 5))
    speeds = [sum(v for bit, v in enumerate(weights) if mask & (1 << bit)) for mask in range(1, 16)]
    q, sign, time, probes, attempts = adaptive(weights)
    records = {}
    safe = {}
    for anchor in (4, 7):
        trials = [physical_trial(speeds, anchor, direction) for direction in (1, -1)]
        issue = first_issue(weights, anchor)
        if issue:
            returned_sign, returned_time = issue
            trial = next(t for t in trials if t['sign'] == returned_sign)
            assert str(returned_time) == trial['time']
        if anchor == q:
            assert issue == ((sign, time) if sign else None)
        records[anchor] = dict(trials=trials, issued=issue and issue[0])
        safe[anchor] = bool(issue and trial['safe'])

    # Direct paired physical check: the switch is invalid if even one 4 endpoint is safe.
    switch = q == 7
    policy = safe[q]
    fixed = safe[4]
    outcome = ('neither','adaptive_only','fixed4_only','shared')[2*fixed+policy]
    assert 1 <= probes <= 15 and attempts == (1 if sign == 1 else 2)
    counts = Counter(cases=1, switches=int(switch), probes=probes, attempts_adaptive=attempts,
                     attempts_fixed4=1 if records[4]['issued']==1 else 2,
                     attempts_fixed7=1 if records[7]['issued']==1 else 2,
                     adaptive=int(policy), fixed4=int(fixed), fixed7=int(safe[7]),
                     seven_only=int(safe[7] and not fixed),
                     seven_only_missed=int(safe[7] and not fixed and not policy),
                     invalid_switch=int(switch and any(t['safe'] for t in records[4]['trials'])),
                     unsafe_issued=sum(records[a]['issued'] is not None and not safe[a] for a in (4,7)))
    counts[outcome] += 1
    return dict(weights=weights, chosen=q, probes=probes, attempts=attempts, outcome=outcome,
                endpoints=records), counts


def score():
    raw = (HERE/'panel.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PANEL
    total = Counter()
    cells, cases = [], []
    for cell in json.loads(raw)['cells']:
        band_counts = Counter()
        for w in cell['rows']:
            record, counts = audit(w)
            band_counts.update(counts)
            cases.append(record)
        total.update(band_counts)
        cells.append(dict(band=cell['band'], draws=cell['draws'], shortfall=cell['shortfall'],
                          counts=dict(band_counts)))
    return dict(panel_sha256=PANEL, total=dict(total), cells=cells, cases=cases)


if __name__ == '__main__':
    print(json.dumps(score(), separators=(',',':')))
