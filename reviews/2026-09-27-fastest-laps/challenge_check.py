"""Independent small challenge checks on the frozen two speed lists only.

Closed safe-interval intersection checks every authorized phase arrangement.
This does not reconstruct primary blocker maps, cover scans, or tree optima.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELTA = F(1, 8)


def meet(first, second):
    return sorted(set((max(a, c), min(b, d)) for a, b in first
                      for c, d in second if max(a, c) <= min(b, d)))


def safe(speed, phase=F(0)):
    phase %= 1
    return [(max(F(0), (F(k)+DELTA-phase)/speed),
             min(F(1), (F(k)+1-DELTA-phase)/speed))
            for k in range(-1, speed+1)
            if max(F(0), (F(k)+DELTA-phase)/speed)
            <= min(F(1), (F(k)+1-DELTA-phase)/speed)]


def conjunction(speeds):
    result = [(F(0), F(1))]
    for speed in speeds:
        result = meet(result, safe(speed))
    return result


def length(intervals):
    return sum((b-a for a, b in intervals), F(0))


def encode(intervals):
    return [[str(a), str(b)] for a, b in intervals]


def distance(speed, time, phase=F(0)):
    z = (speed*time+phase) % 1
    return min(z, 1-z)


def build():
    protocol = json.loads((HERE/'protocol.json').read_text())
    assert protocol['residual_speeds'] == [1, 4, 5, 6, 7, 11]
    phase_archive = json.loads((HERE/'phase_results.json').read_text())
    a5 = conjunction([1, 4, 5, 6, 7])
    a6 = meet(a5, safe(11))
    rows = []
    for frozen, published in zip(protocol['cases'], phase_archive['cases']):
        assert frozen['id'] == published['id']
        V = frozen['velocities'][-1]
        fastest_safe = safe(V)
        base_without_11 = meet(a5, fastest_safe)
        offsets = []
        assert len(published['offsets']) == V
        for s, other in enumerate(published['offsets']):
            phase = F((11*s) % V, V)
            allowed = meet(base_without_11, safe(11, phase))
            duration = length(allowed)
            contacts = [str(a) for a, b in allowed if a == b]
            status = 'positive_duration' if duration else 'contacts_only' if allowed else 'empty'
            assert encode(allowed) == other['full_allowed_t']
            assert str(duration) == other['total_t_duration']
            assert contacts == other['contacts_t']
            assert status == other['global_status']
            assert str(phase) == other['phase11']
            assert duration == F(published['offsets'][(-s) % V]['total_t_duration'])
            reflected = [(1-b, 1-a) for a, b in reversed(allowed)]
            assert encode(reflected) == published['offsets'][(-s) % V]['full_allowed_t']
            for a, b in allowed:
                for t in (a, (a+b)/2, b):
                    ds = [distance(v, t, phase if v == 11 else F(0))
                          for v in frozen['velocities'][1:]]
                    assert min(ds) >= DELTA
                    if a < t < b:
                        assert min(ds) > DELTA
            if V == 13:
                assert duration == 0 if s == 0 else duration > 0
                assert duration >= min(phase, 1-phase, F(1, 4))/11
                # The two fixed 1/7 contacts cannot both be blocked by11.
                assert any(distance(11, t, phase) >= DELTA
                           for t in (F(1, 8), F(7, 8)))
                assert sum(distance(11, F(j, 8), phase) >= DELTA
                           for j in (1, 3, 5, 7)) >= 3
            else:
                assert V == 16 and duration >= F(1, 176)
            offsets.append(dict(s=s, phase11=str(phase), duration=str(duration),
                                contacts=contacts, allowed=encode(allowed), status=status))
        pair_examples = []
        for s in (0, 1):
            phase = F((11*s) % V, V)
            safe1 = meet(fastest_safe, safe(1))
            safe11 = meet(fastest_safe, safe(11, phase))
            both_safe = meet(safe1, safe(11, phase))
            overlap = (length(fastest_safe)-length(safe1)-length(safe11)
                       + length(both_safe))
            pair_examples.append(dict(s=s, D1=str(length(fastest_safe)-length(safe1)),
                                      D11=str(length(fastest_safe)-length(safe11)),
                                      O1_11=str(overlap)))
        assert pair_examples[0]['D1'] == pair_examples[1]['D1']
        assert pair_examples[0]['D11'] == pair_examples[1]['D11']
        assert pair_examples[0]['O1_11'] != pair_examples[1]['O1_11']
        rows.append(dict(id=frozen['id'], V=V, unchanged_safe_without_11=encode(base_without_11),
                         offsets=offsets, pair_preservation_countercheck=pair_examples))

    # Exact geometry supporting the separately written continuous-phase arguments.
    left13 = [(F(17, 48), F(3, 8))]
    right13 = [(F(5, 8), F(31, 48))]
    assert meet(meet(a5, safe(13)), left13) == left13
    assert meet(meet(a5, safe(13)), right13) == right13
    images13 = [(11*left13[0][0]-4, 11*left13[0][1]-4),
                (11*right13[0][0]-7, 11*right13[0][1]-7)]
    assert images13 == [(F(-5, 48), F(1, 8)), (F(-1, 8), F(5, 48))]
    assert max(b for a, b in images13)-min(a for a, b in images13) == F(1, 4)
    pair16 = [(F(25, 56), F(15, 32)), (F(17, 32), F(31, 56))]
    assert meet(meet(a5, safe(16)), pair16) == pair16
    images = [(11*a-5, 11*b-5) for a, b in pair16[:1]]
    images += [(11*a-6, 11*b-6) for a, b in pair16[1:]]
    assert images == [(F(-5, 56), F(5, 32)), (F(-5, 32), F(5, 56))]
    image_width = max(b for a, b in images)-min(a for a, b in images)
    assert image_width == F(5, 16)
    assert (image_width-F(1, 4))/11 == F(1, 176)

    primary_path = HERE/'results.json'
    primary_audit = None
    if primary_path.exists():
        primary = json.loads(primary_path.read_text())
        assert primary['fixed_safe_components'] == encode(a6)
        count = touches = 0
        for case, row in zip(primary['cases'], rows):
            assert case['id'] == row['id']
            assert case['full_allowed_components'] == row['offsets'][0]['allowed']
            for lap in case['laps']:
                a, b = map(F, lap['window'])
                local = meet(a6, [(a, b)])
                assert lap['allowed_components'] == encode(local)
                assert F(lap['actual_duration']) == length(local)
                assert F(lap['tree_bound']) == length(local)
                for scan in lap['coverage_scan']:
                    if scan['junction'] == 'touch':
                        assert scan['touch_survives'] is True
                        touches += 1
                count += 1
        assert count == 29
        primary_audit = dict(results_sha256=sha256(primary_path.read_bytes()).hexdigest(),
                             lap_allowed_sets_checked=count, surviving_envelope_touches=touches)
    return dict(status='OBSERVED exact finite checks; continuous-phase arguments remain proof candidates',
                protocol_sha256=sha256((HERE/'protocol.json').read_bytes()).hexdigest(),
                script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                phase_results_sha256=sha256((HERE/'phase_results.json').read_bytes()).hexdigest(),
                fixed_five_safe=encode(a5), fixed_six_safe=encode(a6), cases=rows,
                continuous_phase_supporting_geometry=dict(
                    V13_one_sided_intervals=encode(left13+right13),
                    V13_phase_images=encode(images13), V13_phase_image_union_width='1/4',
                    V13_clear_duration_lower_bound='min(||theta||,1/4)/11',
                    V16_unchanged_safe_intervals=encode(pair16),
                    V16_phase_images=encode(images), V16_phase_image_union_width=str(image_width),
                    V16_clear_duration_lower_bound='1/176'),
                primary_audit=primary_audit)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE/'challenge_checks.json'
    if args.write:
        path.write_text(json.dumps(result, indent=2)+'\n')
    else:
        assert result == json.loads(path.read_text()), 'challenge_checks.json differs'
    print(json.dumps(dict(status='PASS', shifted_arrangements=sum(len(c['offsets']) for c in result['cases']),
                         primary_audit=result['primary_audit']), indent=2))


if __name__ == '__main__':
    main()
