"""Exact streaming center selection. No complete safe-set construction/import."""
from fractions import Fraction as F
import heapq
from math import ceil, floor


class Budget(Exception):
    pass


def validate(speeds, d):
    if not speeds or any(type(s) is not int or s <= 0 for s in speeds):
        raise ValueError('nonempty positive integer core required')
    if len(set(speeds)) != len(speeds) or not isinstance(d, F) or not 0 < d < F(1, 2):
        raise ValueError('distinct speeds and rational 0<d<1/2 required')


def norm(x):
    f = x % 1
    return min(f, 1-f)


def required(c, d, cap):
    best, critical = F(0), None
    for r in range(1, min(c.denominator, cap)+1):
        value = max(F(0), d-norm(r*c))/r
        if value > best:
            best, critical = value, r
        reason = ('DENOMINATOR' if r == c.denominator else
                  'TAIL_BOUND' if best > 0 and d/(r+1) <= best else None)
        if reason:
            return dict(status='EXACT', H=best, critical=critical, terms=r, stop=reason)
    return dict(status='UNKNOWN_H', lower=best, critical=critical,
                terms=min(c.denominator, cap))


def event_stream(speeds, d, counts, cap):
    # For speed s: opening, closing, opening, closing, ... are sorted.
    def at(s, idx):
        k, side = divmod(idx, 2)
        return (k+d)/s if side == 0 else (k+1-d)/s
    heap = [(at(s, 0), s, 0) for s in speeds]
    heapq.heapify(heap)
    counts['heap_peak'] = len(heap)
    previous = F(0)
    yield previous
    while heap:
        if counts['raw_events'] >= cap:
            raise Budget('UNKNOWN_EVENTS')
        t, s, idx = heapq.heappop(heap)
        counts['raw_events'] += 1
        if idx+1 < 2*s:
            heapq.heappush(heap, (at(s, idx+1), s, idx+1))
        if t != previous:
            counts['distinct_events'] += 1
            previous = t
            yield t
    yield F(1)


def select(speeds, d, caps):
    validate(speeds, d)
    B, V = sum(speeds), max(speeds)
    counts = dict(raw_events=0, distinct_events=0, heap_peak=0,
                  candidates=0, core_predicates=0, H_terms=0)
    out = dict(status=None, counts=counts, safe_candidates=[],
               bounds=dict(raw_events=2*B, candidates=2*B+1,
                           denominator=2*d.denominator*V*V))
    if B > caps['speed_sum']:
        out['status'] = 'UNKNOWN_PREFLIGHT'
        return out
    try:
        events = event_stream(sorted(speeds), d, counts, caps['events'])
        left = next(events)
        for right in events:
            if counts['candidates'] >= caps['candidates']:
                raise Budget('UNKNOWN_CANDIDATES')
            counts['candidates'] += 1
            c = (left+right)/2
            margins = [(norm(s*c)-d)/s for s in speeds]
            counts['core_predicates'] += len(speeds)
            G = min(margins)
            assert c.denominator <= out['bounds']['denominator']
            if G > 0:
                assert G == (right-left)/2
                result = required(c, d, caps['H_terms'])
                counts['H_terms'] += result['terms']
                record = dict(center=c, G=G, interval=[left, right], **result)
                out['safe_candidates'].append(record)
                if result['status'] != 'EXACT':
                    raise Budget('UNKNOWN_H')
                H, r = result['H'], result['critical']
                record['M'] = G-H
                if H <= G:
                    record['decision'] = 'YES'
                    out.update(status='YES', selected=record, exhausted=False)
                    return out
                record['decision'] = 'BLOCKED'
                integer = floor(r*c+F(1, 2))
                assert r not in speeds and r*right-d < integer < r*left+d
                record['blocker'] = dict(r=r, integer=integer)
            left = right
        out.update(status='NO', exhausted=True)
    except Budget as exc:
        out.update(status=str(exc), exhausted=False)
    return out


def witness(interval, r, speeds, d):
    left, right = interval
    k = ceil(r*left-(1-d))
    t = max(left, (k+d)/r)
    assert left <= t <= right
    phases = [(s*t) % 1 for s in speeds+[r]]
    assert all(d <= phase <= 1-d for phase in phases)
    return dict(r=r, t=t, phases=phases, laps=[floor(s*t) for s in speeds+[r]])
