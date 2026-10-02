"""Replay only the twelve frozen inherited windows under the candidate cap39.

Run from repository root. Optional --reference-root locates the pinned older
independent threshold results in a separate working directory. The solver
does not read that oracle; a later comparison does.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL_SHA = '563cefe2f0d36df46795a598e11a0c73dde1ff1e24e38b0481a9fb2d97b5ac5b'


def ceil(x):
    return -((-x.numerator) // x.denominator)


def safe(v, t):
    return F(1, 8) <= (v*t) % 1 <= F(7, 8)


def solve(case, order):
    speeds = case['speeds']
    assert speeds == sorted(speeds) and len(speeds) == 4
    left, right = map(F, case['window'])
    assert left <= right
    t, rounds = left, 0
    trace, intervals = [], []
    while t <= right and not all(safe(v, t) for v in speeds):
        assert rounds < 39, 'Candidate bound violated: unsafe after39 rounds'
        rounds += 1
        for i in order:
            v, old = speeds[i], t
            meeting = ceil(v*t-F(7, 8))
            t = max(t, (meeting+F(1, 8))/v)
            trace.append(dict(runner=i, input=old, output=t))
            if t > old:
                a, b = (meeting-F(1, 8))/v, (meeting+F(1, 8))/v
                assert a < old < b and t == b
                if intervals:
                    assert a < intervals[-1]['right'] < b
                intervals.append(dict(runner=i, occurrence=meeting, left=a, right=b))
                assert len(intervals) <= 39, 'Candidate move bound violated'
            if t > right:
                break
    assert len(trace) <= 429
    periods = [F(1, v) for v in speeds]
    period_sum = sum(periods, F(0))
    span = None
    if intervals:
        span = [min(x['left'] for x in intervals), intervals[-1]['right']]
        assert span[1]-span[0] < period_sum
    slow_count = sum(x['runner'] == 0 for x in intervals)
    assert slow_count <= 4
    gaps, run = [], 0
    for x in intervals:
        if x['runner'] == 0:
            gaps.append(run)
            run = 0
        else:
            run += 1
    gaps.append(run)
    assert max(gaps) <= 7 and len(intervals) <= 8*slow_count+7
    core = []
    for v in case['core']:
        lap = (v*left).numerator // (v*left).denominator
        a, b = v*left-lap, v*right-lap
        assert F(1, 8) <= a <= b <= F(7, 8)
        core.append(dict(speed=v, lap=lap, phase_left=a, phase_right=b))
    width_guarantee = period_sum <= right-left
    feasible = t <= right
    if width_guarantee:
        assert feasible
    if feasible:
        assert all(safe(v, t) for v in speeds+case['core'])
    return dict(id=case['id'], kind=case['kind'], speeds=speeds,
        window=[left, right], verdict='earliest' if feasible else 'empty',
        earliest=t if feasible else None, final_time=t, trace=trace,
        calls=len(trace), started_rounds=rounds, nonzero_moves=len(intervals),
        selected_intervals=intervals, union_span=span, reciprocal_sum=period_sum,
        slow_count=slow_count, three_label_runs=gaps,
        window_width=right-left, width_guarantee=width_guarantee,
        core_certificate=core)


def stringify(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: stringify(v) for k, v in x.items()}
    if isinstance(x, list):
        return [stringify(v) for v in x]
    return x


def main():
    args = argparse.ArgumentParser()
    args.add_argument('--reference-root', type=Path, default=ROOT)
    options = args.parse_args()
    raw = (HERE/'replay_protocol.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PROTOCOL_SHA
    protocol = json.loads(raw)
    rows = stringify([solve(c, protocol['algorithm']['round_order']) for c in protocol['cases']])
    # Independent archived threshold oracle is used only after solving all cases.
    reference_path = options.reference_root/'reviews/2026-09-28-chain-termination/verification.json'
    reference_raw = reference_path.read_bytes()
    reference = {c['id']: c for c in json.loads(reference_raw)['cases']}
    fields = ['trace', 'earliest', 'final_time', 'calls', 'nonzero_moves',
              'selected_intervals', 'union_span']
    comparisons = 0
    for row in rows:
        old = reference[row['id']]
        for field in fields:
            assert row[field] == old[field], (row['id'], field)
            comparisons += 1
        assert (row['verdict'] == 'earliest') == (old['earliest'] is not None)
        comparisons += 1
    result = dict(status='pass', claim_status='OBSERVED for these twelve recycled diagnostics only; general cap39 is a proof candidate',
        protocol_sha256=PROTOCOL_SHA,
        replay_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        independent_reference='reviews/2026-09-28-chain-termination/verification.json',
        independent_reference_sha256=hashlib.sha256(reference_raw).hexdigest(),
        counts=dict(cases=len(rows), calls=sum(r['calls'] for r in rows),
            nonzero_moves=sum(r['nonzero_moves'] for r in rows),
            maximum_moves=max(r['nonzero_moves'] for r in rows),
            width_guaranteed_cases=sum(r['width_guarantee'] for r in rows),
            exact_top_level_comparisons=comparisons), cases=rows)
    (HERE/'replay_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['counts'], indent=2))


if __name__ == '__main__':
    main()
