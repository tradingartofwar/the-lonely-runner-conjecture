#!/usr/bin/env python3
"""Fresh exact fixed-cell reconstruction by incremental convex-hull clipping.

Authoring order: written inequalities -> this reconstruction -> initial output
-> archived ambient.json (optional comparison added only after that first run).
No original mathematical module is imported. All arithmetic is Fraction.
"""

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


ROWS = ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (5, 2))
FROZEN_HEAD = "12d08824ead7b772032ba240d0e858250fbd183c"
ROOT = Path(__file__).resolve().parents[2]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def rank(rows):
    a = [list(map(Q, row)) for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        divisor = a[r][c]
        a[r] = [v / divisor for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                scale = a[i][c]
                a[i] = [v - scale * w for v, w in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def dimension(vertices):
    if not vertices:
        return -1
    origin = next(iter(vertices))
    return rank([tuple(v[i] - origin[i] for i in range(3)) for v in vertices])


def constraint(name, normal, bound):
    return (name, tuple(map(Q, normal)), Q(bound))


def slack(c, v):
    return c[2] - dot(c[1], v)


def active(constraints, v):
    return tuple(i for i, c in enumerate(constraints) if not slack(c, v))


def clip(vertices, constraints, cut):
    """Intersect conv(vertices) with cut, including all boundary equalities.

    Every new vertex is an old vertex or lies on an old edge cut by the new
    plane. We deliberately intersect *all* opposite-side vertex pairs, so no
    adjacency oracle enters reconstruction. Nonvertices are then removed by
    the exact full active-normal rank criterion for bounded 3D H-polytopes.
    This criterion remains valid when the result has dimension 0, 1, or 2.
    """
    updated = constraints + (cut,)
    values = {v: slack(cut, v) for v in vertices}
    candidates = {v for v in vertices if values[v] >= 0}
    for u, v in itertools.combinations(vertices, 2):
        su, sv = values[u], values[v]
        if su * sv < 0:
            t = su / (su - sv)
            candidates.add(tuple(u[i] + t * (v[i] - u[i]) for i in range(3)))
    kept = set()
    for v in candidates:
        assert all(slack(c, v) >= 0 for c in updated)
        if rank([updated[i][1] for i in active(updated, v)]) == 3:
            kept.add(v)
    return tuple(sorted(kept)), updated


def seed():
    """The first two zero-lap bands, z >= 1/8, and x <= 1/2.

    At each height z in [1/8, 1/2], the cross-section is the rectangle
    [z, 1/2] x [z, 1-z]. Its four corners vary affinely towards the common
    apex at z=1/2. Thus the set is exactly the following rectangular pyramid.
    """
    constraints = (
        constraint("floor", (0, 0, -1), -Q(1, 8)),
        constraint("fold", (1, 0, 0), Q(1, 2)),
        constraint("0.lower", (-1, 0, 1), 0),
        constraint("0.upper", (1, 0, 1), 1),
        constraint("1.lower", (0, -1, 1), 0),
        constraint("1.upper", (0, 1, 1), 1),
    )
    vertices = tuple(sorted(
        [(x, y, Q(1, 8)) for x in (Q(1, 8), Q(1, 2))
         for y in (Q(1, 8), Q(7, 8))]
        + [(Q(1, 2), Q(1, 2), Q(1, 2))]
    ))
    assert all(all(slack(c, v) >= 0 for c in constraints) for v in vertices)
    assert all(rank([constraints[i][1] for i in active(constraints, v)]) == 3
               for v in vertices)
    return vertices, constraints


def equality_controls():
    """Exercise face collapse, singleton retention, emptiness, and interior-pair rejection."""
    v, c = seed()
    records = []
    v, c = clip(v, c, constraint("make_face", (1, 0, -1), 0))
    assert (dimension(v), len(v)) == (2, 3)
    records.append({"case": "seed restricted to x=z", "dimension": 2, "vertices": 3})
    v, c = clip(v, c, constraint("make_edge", (0, 1, -1), 0))
    assert (dimension(v), len(v)) == (1, 2)
    records.append({"case": "also y=z", "dimension": 1, "vertices": 2})
    v, c = clip(v, c, constraint("make_point", (0, 0, -1), -Q(1, 2)))
    assert v == ((Q(1, 2), Q(1, 2), Q(1, 2)),)
    records.append({"case": "also z>=1/2", "dimension": 0, "vertices": 1})
    v, c = clip(v, c, constraint("make_empty", (0, 0, -1), -Q(3, 4)))
    assert not v
    records.append({"case": "also z>=3/4", "dimension": -1, "vertices": 0})
    v, c = seed()
    v, c = clip(v, c, constraint("truncate", (0, 0, 1), Q(1, 3)))
    assert (dimension(v), len(v)) == (3, 8)
    records.append({"case": "seed truncated at z=1/3", "dimension": 3, "vertices": 8})
    return records


def face_edges(vertices, constraints):
    """Find one-dimensional faces by their entire vertex set.

    The minimal face containing u and v is cut out by every inequality active
    at both. The pair is an edge precisely when that face has exactly these
    two vertices. This avoids using common-normal rank two as the edge oracle.
    """
    signatures = [set(active(constraints, v)) for v in vertices]
    result = []
    for i, j in itertools.combinations(range(len(vertices)), 2):
        common = signatures[i] & signatures[j]
        face = [k for k, sig in enumerate(signatures) if common <= sig]
        if face == [i, j]:
            result.append((i, j))
    return result


def reconstruct():
    vertices, constraints = seed()
    branches = [((0, 0), vertices, constraints)]
    stages = []
    for i, (a, b) in enumerate(ROWS[2:], start=2):
        new_branches = []
        rejected_after_lower = 0
        rejected_after_upper = 0
        for labels, old_vertices, old_constraints in branches:
            for m in range(a + b):
                vertices, constraints = clip(
                    old_vertices, old_constraints,
                    constraint(f"{i}.lower", (-a, -b, 1), -m))
                if not vertices:
                    rejected_after_lower += 1
                    continue
                vertices, constraints = clip(
                    vertices, constraints,
                    constraint(f"{i}.upper", (a, b, 1), m + 1))
                if not vertices:
                    rejected_after_upper += 1
                    continue
                new_branches.append((labels + (m,), vertices, constraints))
        stages.append({
            "form_index": i,
            "coefficient": [a, b],
            "lap_range": [0, a + b - 1],
            "incoming_branches": len(branches),
            "attempted_branches": len(branches) * (a + b),
            "rejected_after_lower": rejected_after_lower,
            "rejected_after_upper": rejected_after_upper,
            "nonempty_after_both": len(new_branches),
            "dimension_counts": dict(sorted(Counter(dimension(v) for _, v, _ in new_branches).items())),
        })
        branches = new_branches
    cells = []
    for labels, vertices, constraints in branches:
        edges = face_edges(vertices, constraints)
        # Post-construction checks, never used as a source for any vertex.
        for v in vertices:
            assert all(slack(c, v) >= 0 for c in constraints)
            assert rank([constraints[i][1] for i in active(constraints, v)]) == 3
        for i, j in edges:
            common = set(active(constraints, vertices[i])) & set(active(constraints, vertices[j]))
            assert rank([constraints[k][1] for k in common]) == 2
        peaks = [i for i, v in enumerate(vertices) if v[2] == Q(1, 6)]
        peak_edges = []
        for p in peaks:
            for i, j in edges:
                if p not in (i, j):
                    continue
                k = j if i == p else i
                loss = vertices[p][2] - vertices[k][2]
                assert loss > 0
                alpha, beta = ((vertices[k][d] - vertices[p][d]) / loss for d in (0, 1))
                peak_edges.append({"peak_index": p, "endpoint_index": k,
                                   "alpha": alpha, "beta": beta, "max_loss": loss})
        cells.append({
            "labels": labels,
            "dimension": dimension(vertices),
            "vertices": vertices,
            "active_constraints": [[constraints[j][0] for j in active(constraints, v)] for v in vertices],
            "edges": edges,
            "peak_indices": peaks,
            "peak_edges": peak_edges,
        })
    return cells, stages


def check_statement(cells):
    vertices = [v for c in cells for v in c["vertices"]]
    edges = [e for c in cells for e in c["edges"]]
    peaks = [(c, p) for c in cells for p in c["peak_indices"]]
    other = [v for v in vertices if v[2] != Q(1, 6)]
    assert len(cells) == 10
    assert len(vertices) == 33
    assert len(set(vertices)) == 33
    assert len(edges) == 45
    assert Counter(c["dimension"] for c in cells) == Counter({0: 3, 3: 7})
    assert max(v[2] for v in vertices) == Q(1, 6)
    assert max(v[2] for v in other) == Q(1, 7)
    assert len(peaks) == 7
    assert all(len(c["peak_indices"]) == (1 if c["dimension"] == 3 else 0) for c in cells)
    assert sum(len(c["peak_edges"]) for c in cells) == 21

    written = {
        (Q(1, 6), Q(1, 6)): {(-Q(1), Q(2)), (Q(1, 5), -Q(1)), (Q(1), -Q(1))},
        (Q(1, 6), Q(1, 3)): {(-Q(1), Q(1)), (-Q(1), Q(4)), (Q(1), -Q(2))},
        (Q(1, 2), Q(1, 6)): {(-Q(3), Q(5)), (Q(0), -Q(1)), (Q(0), Q(1, 2))},
        (Q(1, 2), Q(1, 3)): {(-Q(1), Q(2)), (Q(0), -Q(1, 2)), (Q(0), Q(1))},
        (Q(1, 3), Q(5, 6)): {(-Q(2), Q(1)), (Q(0), Q(1)), (Q(1), -Q(2))},
        (Q(1, 2), Q(2, 3)): {(-Q(1), Q(2)), (Q(0), -Q(1)), (Q(0), Q(1, 2))},
        (Q(1, 2), Q(5, 6)): {(-Q(3, 5), Q(1)), (Q(0), -Q(1, 2)), (Q(0), Q(1))},
    }
    found = {}
    for c, p in peaks:
        key = c["vertices"][p][:2]
        found[key] = {(e["alpha"], e["beta"]) for e in c["peak_edges"]}
        for e in c["peak_edges"]:
            expected_length = Q(1, 42) if key == (Q(1, 3), Q(5, 6)) and e["alpha"] == -2 else Q(1, 24)
            assert e["max_loss"] == expected_length
    assert found == written
    return {
        "nonempty_cells": len(cells),
        "vertex_occurrences": len(vertices),
        "distinct_vertices": len(set(vertices)),
        "edge_occurrences": len(edges),
        "cell_dimension_counts": dict(sorted(Counter(c["dimension"] for c in cells).items())),
        "singleton_points": [c["vertices"][0] for c in cells if c["dimension"] == 0],
        "ambient_maximum": max(v[2] for v in vertices),
        "largest_nonpeak_vertex_height": max(v[2] for v in other),
        "peak_vertices": len(peaks),
        "peak_edges": 21,
        "written_directions_and_lengths_match": True,
    }


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_archive(cells):
    """Comparison only: called after the fresh reconstruction and assertions."""
    path = ROOT / "reviews/2026-09-29-ltcm-spectrum/ambient.json"
    archived = json.loads(path.read_text())
    old = {tuple(c["m"]): c for c in archived}
    assert len(old) == len(archived) == len(cells)
    assert set(old) == {c["labels"] for c in cells}
    checks = []
    for c in cells:
        o = old[c["labels"]]
        ov = [tuple(map(Q, v)) for v in o["vertices"]]
        nv = c["vertices"]
        assert len(set(ov)) == len(ov)
        assert set(ov) == set(nv)
        oe = {tuple(sorted((ov[i], ov[j]))) for i, j in o["edges"]}
        ne = {tuple(sorted((nv[i], nv[j]))) for i, j in c["edges"]}
        assert len(oe) == len(o["edges"])
        assert oe == ne
        ob = {tuple(map(Q, v)) for v in o["base"]}
        nb = {v[:2] for v in nv if v[2] == Q(1, 8)}
        assert ob == nb
        checks.append({"labels": c["labels"], "vertices_match": True,
                       "edges_match": True, "base_vertices_match": True})
    return {"path": str(path.relative_to(ROOT)), "sha256": sha256(path),
            "read_after_fresh_reconstruction": True, "all_cells_match": True,
            "cell_comparisons": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-archive", action="store_true",
                        help="compare saved ambient.json only after reconstruction")
    args = parser.parse_args()
    controls = equality_controls()
    cells, stages = reconstruct()
    summary = check_statement(cells)
    body = {"coefficient_rows": ROWS, "stages": stages, "cells": cells, "summary": summary}
    canonical = json.dumps(encode(body), sort_keys=True, separators=(",", ":")).encode()
    result = {
        "status": "PASS: fixed-cell statement reproduced by exact halfspace clipping",
        "frozen_research_head_from_protocol": FROZEN_HEAD,
        "method": "lap-branch incremental convex-hull clipping; no boundary-plane triple enumeration",
        "arithmetic": "Python standard-library fractions.Fraction",
        "original_mathematical_code_read_or_imported": [],
        "reconstruction_sha256": hashlib.sha256(canonical).hexdigest(),
        "source_sha256": {
            "notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md": sha256(ROOT / "notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md"),
            "geometry_check.py": sha256(Path(__file__).resolve()),
        },
        "equality_controls": controls,
        "archive_comparison": compare_archive(cells) if args.compare_archive else "not read in this run",
        **body,
    }
    print(json.dumps(encode(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
