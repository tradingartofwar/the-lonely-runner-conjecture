"""Standalone root checks of consequential Ultra-review findings.

Standard library only; imports no project checker or research helper.
Run: python verify_review_findings.py
"""
from fractions import Fraction as F
from itertools import combinations
import json

D = F(1, 8)


def distance(x):
    p = x % 1
    return min(p, 1-p)


def partition(speeds, lo, hi, threshold=D):
    points = {lo, hi}
    for v in speeds:
        for j in range(v):
            for offset in (threshold, 1-threshold):
                t = (j+offset)/v
                if lo < t < hi:
                    points.add(t)
    return sorted(points)


def allowed_components(speeds, lo, hi, threshold=D):
    points = partition(speeds, lo, hi, threshold)
    pieces = [(t, t) for t in points
              if all(distance(v*t) >= threshold for v in speeds)]
    for a, b in zip(points, points[1:]):
        if all(distance(v*(a+b)/2) > threshold for v in speeds):
            pieces.append((a, b))
    result = []
    for a, b in sorted(pieces):
        if result and a <= result[-1][1]:
            result[-1] = (result[-1][0], max(b, result[-1][1]))
        else:
            result.append((a, b))
    return result


def core_check():
    expected = [(F(1,8), F(7,24)), (F(3,8), F(7,16)),
                (F(9,16), F(5,8)), (F(17,24), F(7,8))]
    actual = allowed_components((1,2,3), F(0), F(1))
    assert actual == expected
    assert min(b-a for a,b in actual) == F(1,16)
    for a,b in actual:
        for x in (a,b):
            assert sum(distance(k*x) == D for k in (1,2,3)) == 1
    return {"allowed_core": actual, "minimum_component_width": F(1,16),
            "active_constraints_per_endpoint": 1}


def tree_check():
    extras = (6,7,11,16)
    lo,hi = F(9,32), F(3,8)
    assert all(distance(k*(lo+hi)/2) > D for k in (1,4,5))
    cuts = partition(extras, lo, hi)
    atoms = {mask:F(0) for mask in range(16)}
    for a,b in zip(cuts,cuts[1:]):
        mask = sum(1<<i for i,v in enumerate(extras)
                   if distance(v*(a+b)/2) < D)
        atoms[mask] += b-a
    singles = [sum(m for mask,m in atoms.items() if mask & (1<<i)) for i in range(4)]
    edges = list(combinations(range(4),2))
    pairs = {edge:sum(m for mask,m in atoms.items()
                     if all(mask & (1<<i) for i in edge)) for edge in edges}
    trees = []
    for chosen in combinations(edges,3):
        reached = {0}
        for _ in range(4):
            for i,j in chosen:
                if i in reached or j in reached:
                    reached.update((i,j))
        if len(reached) == 4:
            trees.append((sum(pairs[e] for e in chosen),chosen))
    assert len(trees) == 16
    weight, best = max(trees)
    bound = hi-lo-sum(singles)+weight
    assert singles == [F(1,24),F(5,224),F(9,352),F(3,128)]
    assert weight == F(13,704) and bound == -F(23,29568)
    actual = allowed_components((1,4,5,*extras),lo,hi)
    assert actual == [(F(17,56),F(39,128))]
    theta = actual[0][1]-actual[0][0]
    assert theta == atoms[0] == F(1,896)

    # An abstract event model with identical first/second intersection moments
    # but no uncovered measure. This is not another runner speed configuration.
    alternate = atoms.copy()
    for mask in (0,5,9,12):
        alternate[mask] -= theta
    for mask in (1,4,8,13):
        alternate[mask] += theta
    assert min(alternate.values()) >= 0 and alternate[0] == 0
    assert sum(alternate.values()) == sum(atoms.values()) == hi-lo
    for i in range(4):
        assert sum(m for mask,m in alternate.items() if mask & (1<<i)) == singles[i]
    for edge,value in pairs.items():
        assert sum(m for mask,m in alternate.items()
                   if all(mask & (1<<i) for i in edge)) == value
    return {"core": (1,4,5), "extras": extras, "window": (lo,hi),
            "single_block_durations": singles,
            "pair_overlaps": {str(tuple(extras[i] for i in e)):v for e,v in pairs.items()},
            "trees_checked": len(trees),
            "best_edges": [tuple(extras[i] for i in e) for e in best],
            "tree_bound": bound, "actual_allowed": actual, "actual_duration": theta,
            "actual_atom_durations": atoms, "abstract_alternative_atoms": alternate,
            "same_single_and_pair_moments": True}


def all_core_windows_check():
    """Post-review discussion: local certificate failure is not global failure."""
    core, extras = (1,4,5), (6,7,11,16)
    edges = list(combinations(range(4),2))
    trees = []
    for chosen in combinations(edges,3):
        reached = {0}
        for _ in range(4):
            for i,j in chosen:
                if i in reached or j in reached:
                    reached.update((i,j))
        if len(reached) == 4:
            trees.append(chosen)
    assert len(trees) == 16
    result = []
    for lo,hi in allowed_components(core,F(0),F(1)):
        assert lo < hi
        cuts = partition(extras,lo,hi)
        atoms = {mask:F(0) for mask in range(16)}
        for a,b in zip(cuts,cuts[1:]):
            mask = sum(1<<i for i,v in enumerate(extras)
                       if distance(v*(a+b)/2) < D)
            atoms[mask] += b-a
        singles = sum(mask.bit_count()*length for mask,length in atoms.items())
        pairs = {e:sum(length for mask,length in atoms.items()
                       if all(mask & (1<<i) for i in e)) for e in edges}
        triples = sum(len(list(combinations(range(mask.bit_count()),3)))*length
                      for mask,length in atoms.items())
        quad = atoms[15]
        bound = hi-lo-singles+max(sum(pairs[e] for e in t) for t in trees)
        actual = allowed_components((*core,*extras),lo,hi)
        clear = sum((b-a for a,b in actual),F(0))
        assert clear == atoms[0] == hi-lo-singles+sum(pairs.values())-triples+quad
        result.append({"window":(lo,hi),"tree_bound":bound,"actual_allowed":actual,
                       "clear_duration":clear,"triple_sum":triples,"quadruple":quad})
    assert len(result) == 6
    assert [r["tree_bound"] for r in result] == [F(0),-F(23,29568),F(1,352),F(1,352),-F(23,29568),F(0)]
    assert result[2]["actual_allowed"] == [(F(41,88),F(15,32))]
    assert result[3]["actual_allowed"] == [(F(17,32),F(47,88))]
    # The only positive triangle in the missed window is 6,11,16.
    # Their triple overlap is excluded by exact affine phase bounds.
    common = (max((F(2)-D)/6,(F(4)-D)/11),
              min((F(2)+D)/6,(F(4)+D)/11))
    assert common == (F(31,88),F(17,48))
    assert (F(3)+D)/11 < (F(2)-D)/6
    phases = tuple(16*t-5 for t in common)
    assert phases == (F(7,11),F(2,3)) and D < min(phases) <= max(phases) < 1-D
    assert result[1]["triple_sum"] == result[1]["quadruple"] == 0
    return {"core":core,"extras":extras,"windows":result,
            "positive_tree_windows":2,"missed_window_triangle_pair_interval":common,
            "speed16_phases_on_pair_interval":phases}


def boundary_contacts_check():
    examples = [((4,-8,11,-11),21,F(5,8),"starts"),
                ((5,-19,20,-32),23,F(1,16),"ends"),
                ((4,8,11,13),17,F(1,8),"isolated"),
                ((4,-32,23,-55),35,F(5,24),"isolated")]
    result = []
    for coefficients,q,t,kind in examples:
        speeds = (q,2*q,3*q,*(abs(a)*q+(b if a>0 else -b)
                              for a,b in zip(coefficients,(1,1,2,2))))
        active = [v for v in speeds if distance(v*t) == D]
        assert len(active) == 3 and min(distance(v*t) for v in speeds) == D
        phases = {v*t % 1 for v in active}
        assert phases == ({D} if kind=="starts" else {1-D} if kind=="ends" else {D,1-D})
        result.append({"speeds": speeds, "q": q, "time": t, "active": active, "kind": kind})
    return result


def ten_runner_witness():
    # One exact diagnostic beyond the eight-runner development examples.
    # It is not the proof of the proposed arbitrary-count corollary.
    core=(1,2,3,4)
    offsets=(0,1,3,7,11)
    rates=(1,2,3,4,5)
    t0,x0=F(1,5),F(1,4)
    target=F(1,10)
    mc=min(distance(c*t0) for c in core)-target
    mf=min(distance(b*x0+a*t0) for a,b in zip(offsets,rates))-target
    assert mc==F(1,10) and mf==F(3,20)
    q=50
    z=q*t0-x0+F(1,2)
    m=z.numerator//z.denominator
    t=(m+x0)/q
    speeds=(*core,*(b*q+a for b,a in zip(rates,offsets)))
    assert len(set(speeds))==9
    minimum=min(distance(v*t) for v in speeds)
    assert minimum>target
    assert minimum >= min(target+mc-F(max(core),2*q),
                          target+mf-F(max(offsets),2*q))
    return {"total_runners": 10,"q":q,"speeds_including_reference":(0,*speeds),
            "time":t,"minimum":minimum,"target":target}


if __name__ == "__main__":
    print(json.dumps({"core_partition":core_check(),"tree_limitation":tree_check(),
                      "post_review_all_core_windows":all_core_windows_check(),
                      "core_boundary_contacts":boundary_contacts_check(),
                      "ten_runner_witness":ten_runner_witness()},indent=2,default=str))
