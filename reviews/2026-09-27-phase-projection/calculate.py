"""Exact pushforward/prefix-integral profiles for two prescribed speed lists.

No project imports, no grid sampling, no new speed configurations. The finite
phase partition is generated algebraically from projected closed endpoints.
--write creates the archive; default/--check replays without writing.
"""
from bisect import bisect_right
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results.json'
PROTOCOL_HASH = '8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17'
PRIOR_PATH = 'reviews/2026-09-27-fastest-laps/phase_results.json'
PRIOR_HASH = '612cd4320fc3083476b352f8ce058e345cf2f88a418a36e87228cdbad29c8692'
DELTA = F(1, 8)
CHOSEN = 11


def merge(pieces):
    """Union flagged intervals; do not fill a missing touching point."""
    out = []
    for a, b, ac, bc in sorted(pieces):
        if a > b or (a == b and not (ac and bc)):
            continue
        if not out or a > out[-1][1] or (a == out[-1][1] and not (ac or out[-1][3])):
            out.append([a, b, ac, bc])
            continue
        p = out[-1]
        if a == p[0]:
            p[2] = p[2] or ac
        if b > p[1]:
            p[1], p[3] = b, bc
        elif b == p[1]:
            p[3] = p[3] or bc
    return out


def member(p, t):
    a, b, ac, bc = p
    return a < t < b or (t == a and ac) or (t == b and bc)


def intersection(a, b):
    out = []
    for p in a:
        for q in b:
            lo, hi = max(p[0], q[0]), min(p[1], q[1])
            lc, rc = member(p, lo) and member(q, lo), member(p, hi) and member(q, hi)
            if lo < hi or (lo == hi and lc and rc):
                out.append([lo, hi, lc, rc])
    return merge(out)


def encode(pieces):
    return [[str(a), str(b), ac, bc] for a, b, ac, bc in pieces]


def closed_encode(pieces):
    assert all(ac and bc for a, b, ac, bc in pieces)
    return [[str(a), str(b)] for a, b, _, _ in pieces]


def length(pieces):
    return sum((b - a for a, b, _, _ in pieces), F(0))


def unchanged_safe(speeds):
    allowed = [[F(0), F(1), True, True]]
    for v in speeds:
        safe = [[F(8 * j + 1, 8 * v), F(8 * j + 7, 8 * v), True, True] for j in range(v)]
        allowed = intersection(allowed, safe)
    return allowed


def phase_safe(theta):
    a = (DELTA - theta) % 1
    b = a + 1 - 2 * DELTA
    if b < 1:
        return [[a, b, True, True]]
    if b == 1:
        return [[F(0), F(0), True, True], [a, F(1), True, False]]
    return [[F(0), b - 1, True, True], [a, F(1), True, False]]


def preimages(A, x):
    return [F(j + x, CHOSEN) for j in range(CHOSEN)
            if any(member(p, F(j + x, CHOSEN)) for p in A)]


def cut_set(events, point_mask, cell_mask):
    pieces = [[x, x, True, True] for x, keep in zip(events, point_mask) if keep]
    ends = events[1:] + [F(1)]
    pieces += [[a, b, False, False] for a, b, keep in zip(events, ends, cell_mask) if keep]
    return merge(pieces)


def metrics(pieces):
    assert pieces
    gaps = []
    for i, p in enumerate(pieces):
        next_left = pieces[(i + 1) % len(pieces)][0]
        lifted_left = next_left + (1 if i + 1 == len(pieces) else 0)
        gap = lifted_left - p[1]
        assert gap >= 0
        if gap:
            gaps.append((p[1] % 1, next_left, gap))
    maximum = max((g for _, _, g in gaps), default=F(0))
    return {'measure': str(length(pieces)), 'maximum_circular_gap': str(maximum),
            'minimum_covering_arc_length': str(1 - maximum),
            'maximal_gap_arcs': [[str(a), str(b), str(g)] for a, b, g in sorted(gaps) if g == maximum]}


class PeriodicPrefix:
    def __init__(self, events, counts):
        self.events = events
        self.ends = events[1:] + [F(1)]
        self.counts = counts
        self.prefix = [F(0)]
        for a, b, n in zip(events, self.ends, counts):
            self.prefix.append(self.prefix[-1] + (b - a) * n)
        self.mass = self.prefix[-1]

    def at(self, t):
        whole = t.numerator // t.denominator
        x = t - whole
        i = bisect_right(self.events, x) - 1
        return whole * self.mass + self.prefix[i] + (x - self.events[i]) * self.counts[i]

    def count(self, x):
        return self.counts[bisect_right(self.events, x % 1) - 1]

    def duration(self, theta):
        return (self.at(1 - DELTA - theta) - self.at(DELTA - theta)) / CHOSEN


def branch_images(A):
    branches = {}
    for j in range(CHOSEN):
        images = [[CHOSEN * a - j, CHOSEN * b - j, ac, bc] for a, b, ac, bc in A]
        branches[j] = intersection(images, [[F(0), F(1), True, False]])
    return branches


def pullback_allowed(branches, theta):
    safe = phase_safe(theta)
    pieces = []
    for j, source in branches.items():
        for a, b, ac, bc in intersection(source, safe):
            pieces.append([(a + j) / CHOSEN, (b + j) / CHOSEN, ac, bc])
    return merge(pieces)


def profile_status(A, P, theta, duration):
    if duration > 0:
        return 'strict', None
    image = intersection(P, phase_safe(theta))
    assert length(image) == 0
    times = sorted({t for x, y, _, _ in image for t in preimages(A, x)})
    assert all(a == b for a, b, _, _ in image)
    return ('contacts' if times else 'empty'), list(map(str, times))


def extrema(events, values, slopes):
    minimum, maximum = min(values), max(values)
    result = {'minimum': str(minimum), 'maximum': str(maximum)}
    for target, name in [(minimum, 'minimizer_set'), (maximum, 'maximizer_set')]:
        result[name] = encode(cut_set(events, [v == target for v in values],
                                     [s == 0 and v == target for s, v in zip(slopes, values)]))
    return result


def run_case(case, prior):
    velocities = case['velocities']
    V = velocities[7]
    unchanged = [v for i, v in enumerate(velocities) if i not in (0, 6)]
    assert velocities == [0, 1, 4, 5, 6, 7, 11, V]
    A = unchanged_safe(unchanged)
    branches = branch_images(A)
    events = sorted({F(0)} | {(CHOSEN * x) % 1 for a, b, _, _ in A for x in (a, b)})
    ends = events[1:] + [F(1)]
    phase_points = [{'x': str(x), 'count': len(preimages(A, x)),
                     'preimages': list(map(str, preimages(A, x)))} for x in events]
    phase_cells = []
    for a, b in zip(events, ends):
        mid = (a + b) / 2
        js = [j for j in range(CHOSEN) if any(member(p, mid) for p in branches[j])]
        assert [F(j + mid, CHOSEN) for j in js] == preimages(A, mid)
        phase_cells.append({'left': str(a), 'right': str(b), 'count': len(js), 'preimage_branches': js})
    counts = [c['count'] for c in phase_cells]
    point_counts = [p['count'] for p in phase_points]
    occupied = [n > 0 for n in counts]
    P = cut_set(events, [n > 0 for n in point_counts], occupied)
    bulk_points = [occupied[i] or occupied[i - 1] for i in range(len(events))]
    B = cut_set(events, bulk_points, occupied)
    extra = [str(x) for x, n, bulk in zip(events, point_counts, bulk_points) if n > 0 and not bulk]
    weighted = PeriodicPrefix(events, counts)
    support = PeriodicPrefix(events, list(map(int, occupied)))
    assert weighted.mass == CHOSEN * length(A)
    critical = sorted({F(0)} | {(edge - x) % 1 for x in events for edge in (DELTA, 1 - DELTA)})
    critical_ends = critical[1:] + [F(1)]
    theta_points, theta_cells = [], []
    values, estimates, slopes, support_slopes = [], [], [], []
    for theta in critical:
        duration, estimate = weighted.duration(theta), support.duration(theta)
        assert 0 <= estimate <= duration <= length(A)
        status, contacts = profile_status(A, P, theta, duration)
        theta_points.append({'theta': str(theta), 'duration': str(duration), 'support_estimate': str(estimate),
                             'status': status, 'contact_times': contacts})
        values.append(duration)
        estimates.append(estimate)
    for i, (a, b) in enumerate(zip(critical, critical_ends)):
        mid = (a + b) / 2
        # No generated event lies inside this cell. These two counts are
        # therefore constant throughout it, which proves the affine slope.
        slope = F(weighted.count(DELTA - mid) - weighted.count(1 - DELTA - mid), CHOSEN)
        sslope = F(support.count(DELTA - mid) - support.count(1 - DELTA - mid), CHOSEN)
        intercept, sintercept = values[i] - slope * a, estimates[i] - sslope * a
        assert slope * b + intercept == values[(i + 1) % len(values)]
        assert sslope * b + sintercept == estimates[(i + 1) % len(estimates)]
        assert slope * mid + intercept == weighted.duration(mid)
        assert sslope * mid + sintercept == support.duration(mid)
        status, contacts = profile_status(A, P, mid, weighted.duration(mid))
        if contacts is not None:
            assert slope == 0 and intercept == 0
        theta_cells.append({'left': str(a), 'right': str(b), 'slope': str(slope), 'intercept': str(intercept),
                            'support_slope': str(sslope), 'support_intercept': str(sintercept),
                            'status': status, 'contact_times': contacts})
        slopes.append(slope)
        support_slopes.append(sslope)
    plateau_values = sorted({v for v, slope in zip(values, slopes) if slope == 0})
    plateaus = []
    for value in plateau_values:
        active_cells = [slope == 0 and v == value for slope, v in zip(slopes, values)]
        # Include just endpoints incident to a positive-length plateau.
        active_points = [values[i] == value and (active_cells[i] or active_cells[i - 1])
                         for i in range(len(critical))]
        plateaus.append({'value': str(value), 'phase_components': encode(cut_set(critical, active_points, active_cells))})
    statuses = {name: encode(cut_set(critical, [p['status'] == name for p in theta_points],
                                     [c['status'] == name for c in theta_cells]))
                for name in ('strict', 'contacts', 'empty')}
    prior_checks = []
    assert prior['id'] == case['id'] and len(prior['offsets']) == V
    for offset in prior['offsets']:
        s = offset['s']
        theta = F(CHOSEN * s, V) % 1
        allowed = pullback_allowed(branches, theta)
        duration = weighted.duration(theta)
        assert duration == length(allowed) == F(offset['total_t_duration'])
        actual_status = 'strict' if duration > 0 else ('contacts' if allowed else 'empty')
        mapped_status = {'positive_duration': 'strict', 'contacts_only': 'contacts', 'empty': 'empty'}[offset['global_status']]
        isolated = [str(a) for a, b, _, _ in allowed if a == b]
        assert str(theta) == offset['phase11']
        assert closed_encode(allowed) == offset['full_allowed_t']
        assert isolated == offset['contacts_t'] and actual_status == mapped_status
        prior_checks.append({'s': s, 'theta': str(theta), 'duration': str(duration), 'status': actual_status,
                             'isolated_times': isolated, 'full_allowed_components': closed_encode(allowed)})
    result = {
        'id': case['id'], 'velocities': velocities, 'V': V, 'unchanged_speeds': unchanged,
        'A_components': closed_encode(A), 'A_duration': str(length(A)),
        'A_isolated_times': [str(a) for a, b, _, _ in A if a == b],
        'phase_events': list(map(str, events)), 'phase_points': phase_points, 'phase_cells': phase_cells,
        'P_components': encode(P), 'B_components': encode(B), 'extra_isolated_projection_points': extra,
        'P_metrics': metrics(P), 'B_metrics': metrics(B), 'multiplicity_integral': str(weighted.mass),
        'maximum_point_multiplicity': max(point_counts), 'maximum_bulk_multiplicity': max(counts),
        'critical_phases': list(map(str, critical)), 'theta_points': theta_points, 'theta_cells': theta_cells,
        'duration_extrema': extrema(critical, values, slopes),
        'support_estimate_extrema': extrema(critical, estimates, support_slopes),
        'underestimate_extrema': extrema(critical, [v - e for v, e in zip(values, estimates)],
                                        [s - ss for s, ss in zip(slopes, support_slopes)]),
        'duration_plateaus': plateaus, 'phase_status_sets': statuses, 'prior_phase_checks': prior_checks,
    }
    result['case_sha256'] = sha256((json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n').encode()).hexdigest()
    print(case['id'], 'A', result['A_duration'], 'phase events', len(events), 'theta cells', len(critical),
          'Dmin', result['duration_extrema']['minimum'], 'Dmax', result['duration_extrema']['maximum'],
          'maxN', max(point_counts), 'extra projected points', extra, flush=True)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = ap.parse_args()
    raw = (HERE / 'protocol.json').read_bytes()
    assert sha256(raw).hexdigest() == PROTOCOL_HASH, 'Frozen protocol changed'
    protocol = json.loads(raw)
    prior_raw = (HERE.parents[1] / PRIOR_PATH).read_bytes()
    assert sha256(prior_raw).hexdigest() == PRIOR_HASH, 'Pinned prior archive changed'
    prior = json.loads(prior_raw)
    result = {'schema_version': 1,
              'status': 'OBSERVED exact profiles for two fixed shifted-start families; theta0 is common-start',
              'protocol_sha256': PROTOCOL_HASH, 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'prior_archive': {'path': PRIOR_PATH, 'sha256': PRIOR_HASH},
              'cases': [run_case(c, p) for c, p in zip(protocol['cases'], prior['cases'])]}
    if args.write:
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    else:
        assert result == json.loads(OUT.read_text()), 'Archive drift'
    print('PASS: two exact pushforward profiles, finite algebraic partitions, point fibers, '
          'all extrema/status sets and29 pinned phase checks; ' + ('written' if args.write else 'replayed read-only'))


if __name__ == '__main__':
    main()
