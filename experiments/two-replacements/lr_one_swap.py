"""Exact one-replacement comparison, with the root stationary and speeds 1..4 retained.

For each n, remove k from 1,...,n-1 with 5 <= k <= n-1 and adjoin an
arbitrary integer v >= n. Verify strict clearance > 1/n by interval tests,
or check the equality times explicitly. Run with Python 3.11 or later.
"""

from fractions import Fraction
from math import ceil, floor


def strict_windows(speeds, n):
    """Components on [0,1] outside the union of the closed blocking intervals."""
    blocks = sorted(
        (max(Fraction(0), Fraction(n*j - 1, n*v)),
         min(Fraction(1), Fraction(n*j + 1, n*v)))
        for v in speeds for j in range(v + 1)
    )
    right = Fraction(0)
    windows = []
    for left, end in blocks:
        if left > right:
            windows.append((right, left))
        right = max(right, end)
    return windows


def single_speed_leaves_window(windows, speed, delta):
    """An open window (l,r) is covered iff an integer belongs to [vr-d,vl+d]."""
    return any(ceil(speed*r - delta) > floor(speed*l + delta) for l, r in windows)


def equality_times(speeds, n):
    """Complete endpoint test for instances already known to have no strict time."""
    candidates = {
        Fraction(n*j + sign, n*v)
        for v in speeds for j in range(v + 1) for sign in (-1, 1)
        if 0 < n*j + sign < n*v
    }
    result = []
    for t in sorted(candidates):
        p, q = t.as_integer_ratio()
        if all(n * min(v*p % q, -v*p % q) >= q for v in speeds):
            result.append(t)
    return result


def experiment(n, minimum_removed=5):
    delta = Fraction(1, n)
    rows = []
    for k in range(minimum_removed, n):
        retained = [s for s in range(1, n) if s != k]
        windows = strict_windows(retained, n)
        assert windows, "This tail argument requires a positive-width window"
        longest = max(r-l for l, r in windows)
        # A single blocking arc for speed v has width 2*delta/v. If this is
        # shorter than our longest open window, some strict time survives.
        last = floor(2 * delta / longest)
        strict = 0
        tight = []
        below = []
        for v in range(n, last + 1):
            if single_speed_leaves_window(windows, v, delta):
                strict += 1
            elif equality_times([*retained, v], n):
                tight.append(v)
            else:
                below.append(v)
        rows.append((k, longest, last, strict, tight, below))
    return rows


def main():
    print("n   removed   finite tested   tight (k,v)   below   largest tail cutoff")
    for n in range(6, 21):
        rows = experiment(n)
        tight = [(k, v) for k, _, _, _, equal, _ in rows for v in equal]
        below = [(k, v) for k, _, _, _, _, small in rows for v in small]
        tested = sum(max(0, last - n + 1) for _, _, last, _, _, _ in rows)
        assert tested == sum(s for _, _, _, s, _, _ in rows) + len(tight) + len(below)
        expected = [(n - 2, 2 * (n - 2))] if n % 6 == 2 else []
        assert tight == expected and not below
        upper = max(last for _, _, last, _, _, _ in rows)
        print(f"{n:2d}  {len(rows):4d}  {tested:8d}   {tight}   {below}   {upper}")
        if n == 16:
            print("    n=16 cutoffs by omitted speed:",
                  [(k, last) for k, _, last, _, _, _ in rows])
    # A positive equality control outside the retained-1..4 experiment.
    assert equality_times([1, 3, 4, 7], 5) and not strict_windows([1, 3, 4, 7], 5)
    # At 16 the strict conclusion also covers deletions of the first four speeds.
    assert not any(tight or below for _, _, _, _, tight, below in experiment(16, 1))


if __name__ == "__main__":
    main()
