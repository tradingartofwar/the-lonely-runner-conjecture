"""Standalone exact diagnostics for the September 25 overlap review.

Run from the repository root:
  python reviews/2026-09-25-ultra/overlap_check.py

Does not import project code or modify project files. Enumerates one prescribed
configuration, rational boundary cells, and the 16 labelled trees via Prufer codes.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

DELTA = Q(1, 8)
CORE = (1, 4, 5)
EXTRAS = (6, 7, 11, 16)
J = (Q(9, 32), Q(3, 8))


def safe(speeds, t):
    return all(DELTA <= (w * t) % 1 <= 1 - DELTA for w in speeds)


def prufer_edges(sequence):
    degree = {v: 1 + sequence.count(v) for v in EXTRAS}
    edges = []
    for v in sequence:
        leaf = min(x for x in EXTRAS if degree[x] == 1)
        edges.append(tuple(sorted((leaf, v))))
        degree[leaf] -= 1
        degree[v] -= 1
    a, b = (v for v in EXTRAS if degree[v] == 1)
    return tuple(sorted((*edges, tuple(sorted((a, b))))))


cuts = {*J}
for w in (*CORE, *EXTRAS):
    for j in range(w + 1):
        for sign in (-1, 1):
            t = (j + sign * DELTA) / w
            if J[0] < t < J[1]:
                cuts.add(t)
cuts = sorted(cuts)
statuses = defaultdict(Q)
good_cells = []
for a, b in zip(cuts, cuts[1:]):
    t = (a + b) / 2
    assert safe(CORE, t)
    active = tuple(w for w in EXTRAS if not safe((w,), t))
    statuses[active] += b - a
    if not active:
        good_cells.append((a, b))
good_points = [t for t in cuts if safe((*CORE, *EXTRAS), t)]
assert good_cells == [(Q(17, 56), Q(39, 128))]
assert good_points == [Q(17, 56), Q(39, 128)]
assert safe((*CORE, *EXTRAS), sum(good_cells[0]) / 2)


def margins(distribution):
    individual = {w: sum(m for s, m in distribution.items() if w in s) for w in EXTRAS}
    pairs = {e: sum(m for s, m in distribution.items() if set(e) <= set(s))
             for e in combinations(EXTRAS, 2)}
    return individual, pairs


individual, pairs = margins(statuses)
excess = sum(individual.values()) - (J[1] - J[0])
trees = {prufer_edges(list(s)) for s in product(EXTRAS, repeat=2)}
assert len(trees) == 16
weights = {t: sum(pairs[e] for e in t) for t in trees}
maximum = max(weights.values())
winners = sorted(t for t, w in weights.items() if w == maximum)
assert winners == [((6, 16), (7, 11), (11, 16))]
assert maximum == Q(13, 704)
assert excess == Q(569, 29568)
assert maximum - excess == -Q(23, 29568)
assert statuses[()] == Q(1, 896)

# Produce another nonnegative event distribution with the SAME first/second
# moments but no uncovered measure. This is an event-data obstruction, not
# another physical runner configuration.
theta = statuses[()]
alternative = defaultdict(Q, statuses)
alternative[()] -= theta
for e in ((6, 11), (6, 16), (11, 16)):
    alternative[e] -= theta
for v in (6, 11, 16):
    alternative[(v,)] += theta
alternative[(6, 11, 16)] += theta
assert all(m >= 0 for m in alternative.values())
assert sum(alternative.values()) == sum(statuses.values()) == J[1] - J[0]
assert margins(alternative) == (individual, pairs)
assert alternative[()] == 0

result = {
    'speeds': (0, *CORE, *EXTRAS), 'J': J,
    'clear_interval': good_cells[0], 'clear_duration': statuses[()],
    'individual_durations': individual,
    'pair_overlaps': [{'pair': e, 'duration': m} for e, m in pairs.items()],
    'excess': excess, 'maximum_tree': winners[0], 'maximum_tree_weight': maximum,
    'best_tree_bound': maximum - excess,
    'tree_gap': statuses[()] - (maximum - excess),
    'status_distribution': [{'active': s, 'duration': m} for s, m in sorted(statuses.items())],
    'alternative_zero_clear_distribution': [{'active': s, 'duration': m}
                                            for s, m in sorted(alternative.items())],
    'checks': 'Exact complete boundary partition, all 16 Prufer trees, and matching first/second moments passed.'
}
print(json.dumps(result, indent=2, default=str))
