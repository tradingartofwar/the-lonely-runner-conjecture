"""Exact sheet criterion. Inherited geometry/recovery; new residue counting.

The Euclidean floor-sum primitive is standard (AtCoder Library math docs).
This Python implementation uses unbounded integers, including signed a,b.
See DERIVATION.md for the translation and its distinct proof obligations.
"""
from collections import Counter
from fractions import Fraction as F
from importlib.util import spec_from_file_location, module_from_spec
from math import ceil, floor, gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_module(name, relative):
    spec = spec_from_file_location(name, ROOT / relative)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load_module("rank_three_geometry", "reviews/2026-09-30-cc-three-parameter/discover.py")
COUNTS = Counter()


def floor_sum(n, m, a, b):
    """sum floor((a*j+b)/m), 0<=j<n; Euclidean reciprocity."""
    assert n >= 0 and m > 0
    COUNTS["floor_sum_calls"] += 1
    total = 0
    while True:
        COUNTS["euclidean_iterations"] += 1
        qa, a = divmod(a, m)
        qb, b = divmod(b, m)
        total += qa * n * (n - 1) // 2 + qb * n
        top = a * n + b
        if top < m:
            return total
        n, b = divmod(top, m)
        m, a = a, m


def residue_count(n, m, a, b, lower, upper):
    """Count inclusive residue hits; no scan over j."""
    assert n >= 0 and m > 0 and 0 <= lower <= upper < m
    COUNTS["residue_count_calls"] += 1
    return (floor_sum(n, m, a, b + m - lower)
            - floor_sum(n, m, a, b + m - upper - 1))


def first_residue(n, m, a, b, lower, upper):
    count = residue_count(n, m, a, b, lower, upper)
    if count == 0:
        return None, count
    left, right = 0, n - 1
    while left < right:
        middle = (left + right) // 2
        if residue_count(middle + 1, m, a, b, lower, upper):
            right = middle
        else:
            left = middle + 1
    return left, count


def contact(obj, lat):
    """Exact necessary/sufficient criterion for S x [1/8,7/8]."""
    COUNTS["contacts"] += 1
    if COUNTS["contacts"] > 100000:
        raise RuntimeError("SCOPE_LIMIT: contact calls")
    assert obj["z_range"] == [F(1, 8), F(7, 8)]
    p0, p1 = obj["endpoints"]
    Q, P, d = lat["Q"], lat["P"], lat["d"]
    a, b, C = lat["a"], lat["b"], lat["normalized"][2]
    h0, h1 = (Q*x-P*y for x, y in (p0, p1))
    w0, w1 = (a*x+b*y for x, y in (p0, p1))
    lower_h, upper_h = ceil(min(h0, h1)), floor(max(h0, h1))
    detail = {"h_range": [h0, h1], "integer_h_bounds": [lower_h, upper_h],
              "d": d, "vertical_n_width": F(3*d, 4)}
    if lower_h > upper_h:
        return {**detail, "reason": "NO_INTEGER_H", "hit": None}
    if h0 == h1:
        # The connected rectangle maps onto the complete n interval.
        choices = sorted((C*w-d*z, s, z) for s, w in ((F(0), w0), (F(1), w1))
                         for z in obj["z_range"])
        low, high = choices[0], choices[-1]
        high = next(item for item in choices if item[0] == high[0])
        n = ceil(low[0])
        detail["n_range"] = [low[0], high[0]]
        if n > high[0]:
            return {**detail, "reason": "CONSTANT_H_NO_INTEGER_N", "hit": None}
        u = F(0) if high[0] == low[0] else (n-low[0])/(high[0]-low[0])
        s, z = (low[k]+u*(high[k]-low[k]) for k in (1, 2))
        hit = {"point": old.at(obj, s, z), "s": s, "H1": int(h0), "H2": n}
        return {**detail, "reason": "CONSTANT_H_INTERVAL", "hit": hit}

    if d >= 2:
        h = lower_h
        detail["admissible_h_count"] = upper_h-lower_h+1
        reason = "VERTICAL_WIDTH_GUARANTEE"
    else:
        alpha = C*(w1-w0)/(h1-h0)
        beta = C*w0-alpha*h0
        modulus = lcm(alpha.denominator, beta.denominator)
        step, offset = int(alpha*modulus), int(beta*modulus)
        # Reduce the common representation, including the constant sequence.
        divisor = gcd(modulus, step, offset)
        modulus, step, offset = modulus//divisor, step//divisor, offset//divisor
        lo, hi = ceil(F(modulus, 8)), floor(F(7*modulus, 8))
        detail["residue"] = {"modulus": modulus, "step": step, "offset": offset,
                             "inclusive_safe_bounds": [lo, hi]}
        length = upper_h-lower_h+1
        if lo > hi:
            index, count = None, 0
        else:
            index, count = first_residue(length, modulus, step,
                                         step*lower_h+offset, lo, hi)
        detail["admissible_h_count"] = count
        if index is None:
            return {**detail, "reason": "RESIDUE_OBSTRUCTION", "hit": None}
        h = lower_h+index
        reason = "RESIDUE_CONTACT"
    s = (h-h0)/(h1-h0)
    w = w0+s*(w1-w0)
    n = ceil(C*w-F(7*d, 8))
    z = (C*w-n)/d
    assert F(1, 8) <= z <= F(7, 8)
    return {**detail, "reason": reason,
            "hit": {"point": old.at(obj, s, z), "s": s, "H1": h, "H2": n}}


def greedy(rows, cap=8):
    remaining = set(range(len(rows)))
    menu, trace = [], []
    while remaining and len(menu) < cap:
        gains = [sum(rows[j]["bits"][i] == "1" for j in remaining) for i in range(36)]
        best = max(gains)
        if best == 0:
            break
        chosen = gains.index(best)
        covered = sorted(j for j in remaining if rows[j]["bits"][chosen] == "1")
        menu.append(chosen)
        remaining.difference_update(covered)
        trace.append({"source": chosen, "gain": best, "covered_rows": covered})
    return {"indices": menu, "trace": trace, "uncovered_rows": sorted(remaining), "cap": cap}
