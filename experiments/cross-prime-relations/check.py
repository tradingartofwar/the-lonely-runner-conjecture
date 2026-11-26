"""Exact cross-prime alignment experiment. Run with Python 3.11 or later."""

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import isqrt
from random import Random


def allowed_relation(h):
    k = len(h)
    return (sum(h) % 2 == 1 and sum(map(abs, h)) <= 2 * k + 3
            and (k - 1) * sum(x * x for x in h) <= 4 * (k + 1) ** 2)


def first_row_relations(k, max_norm):
    """List all relations on row (1,...,k) within the given 1-norm and both bounds."""
    squared_limit = 4 * (k + 1) ** 2 // (k - 1)
    relations = []

    def visit(pos, remaining, squared, dot, terms):
        # The first nonzero entry is positive to identify h with -h.
        if pos > k or remaining == 0:
            if dot == 0 and sum(value for _, value in terms) % 2:
                relations.append(tuple(terms))
            return
        visit(pos + 1, remaining, squared, dot, terms)
        bound = min(remaining, isqrt(squared_limit - squared))
        for size in range(1, bound + 1):
            for value in ((size, -size) if terms else (size,)):
                visit(pos + 1, remaining - size, squared + size * size,
                      dot + pos * value, terms + [(pos - 1, value)])

    visit(1, min(max_norm, 2 * k + 3), 0, 0, [])
    return sorted(relations, key=lambda r: sum(abs(v) for _, v in r))


def physical_lift(first, second, p, q):
    """Least positive CRT representatives with the given labelled residues."""
    inv = pow(p, -1, q)
    return tuple(a + p * ((b - a) * inv % q) for a, b in zip(first, second))


def clearance_numerator(speeds, j, denominator):
    return min(min(j*v % denominator, -j*v % denominator) for v in speeds)


def first_witness(speeds, denominator):
    n = len(speeds) + 1
    for j in range(1, denominator // 2 + 1):
        if n * clearance_numerator(speeds, j, denominator) >= denominator:
            return j
    return None


def small_alignments(k):
    for perm in permutations(range(1, k + 1)):
        for signs in product((1, -1), repeat=k):
            yield tuple(value * sign for value, sign in zip(perm, signs))


def random_alignments(k, count):
    rng = Random(20261124)
    for _ in range(count):
        perm = list(range(1, k + 1))
        rng.shuffle(perm)
        yield tuple(-value if rng.getrandbits(1) else value for value in perm)


def evaluate(n, p, q, rows, max_norm):
    k = n - 1
    first = tuple(range(1, n))
    # For every allowed h, neither dot product can wrap to a nonzero multiple.
    assert min(p, q) > k * (2*k + 3)
    assert first_witness(first, p) is None and first_witness(first, q) is None
    relations = first_row_relations(k, max_norm)
    tally = Counter()
    for second in rows:
        assert sorted(map(abs, second)) == list(first)
        candidate = next((r for r in relations if sum(second[j]*v for j,v in r) == 0), None)
        if candidate:
            coeff = [0]*k
            for j, v in candidate:
                coeff[j] = v
            assert allowed_relation(coeff)
            assert sum(a*v for a,v in zip(coeff, first)) % p == 0
            assert sum(a*v for a,v in zip(coeff, second)) % q == 0
            result = "compatible"
        elif max_norm >= 2*k+3 or second == first[::-1]:
            result = "excluded"
        else:
            result = "undecided"
        speeds = physical_lift(first, second, p, q)
        numerator = first_witness(speeds, p*q)
        if numerator is not None:
            time = Fraction(numerator, p*q)
            assert all(min(v*time % 1, -v*time % 1) >= Fraction(1,n) for v in speeds)
        tally[result, numerator is not None] += 1
    return tally


def check_five_by_box():
    first = (1, 2, 3, 4)
    # The squared-norm bound is 100/3, so every coordinate belongs to [-5, 5].
    all_h = [h for h in product(range(-5, 6), repeat=4)
             if allowed_relation(h) and sum(a*b for a,b in zip(h, first)) % 47 == 0]
    sparse = first_row_relations(4, 11)
    for second in small_alignments(4):
        direct = any(sum(a*b for a,b in zip(h, second)) % 53 == 0 for h in all_h)
        listed = any(sum(second[j]*v for j,v in r) == 0 for r in sparse)
        assert listed == direct


def controls(n, p, q):
    first = tuple(range(1, n))
    rev = first[::-1]
    speeds = physical_lift(first, rev, p, q)
    # Round p/(2n), q/(2n) to the nearest integers by integer arithmetic.
    a, b = ((prime + n) // (2*n) for prime in (p, q))
    time = Fraction(a, p) + Fraction(b, q)
    gap = Fraction(clearance_numerator(speeds, time.numerator, time.denominator), time.denominator)
    assert gap >= Fraction(1,2) - Fraction(n, 2*min(p,q))
    assert all((w-i) % p == 0 and (w-(n-i)) % q == 0 for i,w in enumerate(speeds, 1))
    # The same residues under BOTH clocks can represent very different real lineups.
    odd = tuple(v if v%2 else v + p*q for v in first)
    assert all((x-y) % (p*q) == 0 for x,y in zip(odd,first))
    assert clearance_numerator(odd, 1, 2) == 1 and first_witness(first, p*q) is None
    print(f"n={n}, reverse time {time}, clearance {gap}; identical-row all-odd control 1/2.")


if __name__ == "__main__":
    check_five_by_box()
    small = evaluate(5, 47, 53, small_alignments(4), 11)
    assert small == {("compatible", False): 2, ("compatible", True): 258, ("excluded", True): 124}
    print("5 runners, exhaustive:", sorted(small.items()))
    controls(5,47,53)
    first = tuple(range(1,16))
    planted = evaluate(16, 503, 509, [first, first[::-1]], 5)
    sample = evaluate(16, 503, 509, random_alignments(15, 256), 5)
    assert planted == {("compatible", False): 1, ("excluded", True): 1}
    assert sample == {("compatible", True): 256}
    print("16 runners, two controls:", sorted(planted.items()))
    print("16 runners, sampled:", sorted(sample.items()))
    controls(16,503,509)
