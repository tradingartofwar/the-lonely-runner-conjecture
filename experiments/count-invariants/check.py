"""Compare the exact requirements for blocking the 2n time grid across counts."""

from fractions import Fraction
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "proof-survivors"))
from binary_lifts import descendants, even_sets


def prime_divisors(value):
    primes = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            primes.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        primes.append(value)
    return primes


def required_classes(n):
    d = 2 * n
    units = {v for v in range(1, n) if gcd(v, d) == 1}
    divisors = {d // p for p in prime_divisors(d)}
    return units, divisors


def predicted_blocked(speeds, n):
    d = 2 * n
    if any(v % d == 0 for v in speeds):
        return True
    units, divisors = required_classes(n)
    unsigned = {min(v % d, -v % d) for v in speeds}
    return units <= unsigned and all(any(v % q == 0 for v in speeds)
                                     for q in divisors)


def direct_blocked(speeds, n, d):
    return all(any(n * min(h*v % d, -h*v % d) < d for v in speeds)
               for h in range(1, d))


def check_rule():
    checked = 0
    for n in range(2, 17):
        d = 2 * n
        units, divisors = required_classes(n)
        minimal = sorted(units | divisors)
        assert predicted_blocked(minimal, n) and direct_blocked(minimal, n, d)
        for v in minimal:
            reduced = [r for r in minimal if r != v]
            assert not predicted_blocked(reduced, n) and not direct_blocked(reduced, n, d)
        # Every subset of unsigned residues for the small grids, zero included.
        if n <= 8:
            for size in range(n + 2):
                for subset in combinations(range(n + 1), size):
                    assert predicted_blocked(subset, n) == direct_blocked(subset, n, d)
                    checked += 1
        print(f"{n:2} runners, {len(units):2} unit classes, "
              f"maximal proper divisors {sorted(divisors)}, minimum {len(minimal)}")
    print(f"Exhaustive small-grid subsets checked: {checked}")


def check_prime_lifts(n):
    """Join a known surviving parity label at 2p to an actual lift modulo 2n."""
    p, d = 2 * n - 1, 2 * n
    lifts = descendants([tuple(range(1, n))], p, n)
    masks = {sum(1 << j for j, v in enumerate(speeds) if v % 2 == 0)
             for speeds in lifts}
    assert masks == even_sets(n, p)
    units, divisors = required_classes(n)
    minimal = sorted(units | divisors)
    targets = {bit: [v for v in minimal if v % 2 == bit] for bit in (0, 1)}
    compatible = 0
    for speeds in lifts:
        if any(sum(v % 2 == bit for v in speeds) < len(targets[bit])
               for bit in (0, 1)):
            continue
        pending = {bit: targets[bit].copy() for bit in (0, 1)}
        joint = []
        for speed in speeds:
            bit = speed % 2
            want = pending[bit].pop() if pending[bit] else (1 if bit else 2)
            # The two moduli have gcd 2, so matching parity gives a solution.
            joined = next(speed + j * 2 * p for j in range(n)
                          if (speed + j * 2 * p) % d == want)
            joint.append(joined)
        assert all(v % d for v in joint)
        assert direct_blocked(joint, n, d) and direct_blocked(joint, n, 2*p)
        compatible += 1
    return len(lifts), compatible


def clearance(speeds, a, d):
    return Fraction(min(min(a*v % d, -a*v % d) for v in speeds), d)


def check_controls():
    a = sorted(set(range(1, 17)) - {15})
    b = sorted(set(range(1, 17)) - {8})
    assert clearance(a, 15, 32) == Fraction(1, 16)
    assert direct_blocked(b, 16, 32)
    assert clearance(b, 3, 25) == Fraction(2, 25)

    # Any finite bank of rational clocks can fail, even on a solvable tuple.
    m = lcm(*range(1, 33))
    speeds = [*range(1, 15), m]
    assert all(direct_blocked(speeds, 16, d) for d in range(2, 33))
    t = Fraction(1, 15) + Fraction(1, 2*m)
    assert clearance(speeds, t.numerator, t.denominator) >= Fraction(1, 16)


if __name__ == "__main__":
    check_rule()
    for n in range(4, 17):
        p = 2*n - 1
        if prime_divisors(p) == [p]:
            total, compatible = check_prime_lifts(n)
            print(f"{n:2} runners: {total} parity patterns, {compatible} compatible "
                  f"without a multiple of {2*n}, {total - compatible} force one")
    check_controls()
    print("All controls passed.")
