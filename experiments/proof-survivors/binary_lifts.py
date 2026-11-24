"""Recount the binary lifts of individual residue classes, with exact arithmetic."""

from functools import lru_cache
from itertools import product


def safe_times(speed, denominator, runners):
    """Bits for the safe times h/denominator on a half-period, including equality."""
    last = denominator // 2
    bits = bytearray(last // 8 + 1)
    for h in range(1, last + 1):
        residue = h * speed % denominator
        if runners * min(residue, denominator - residue) >= denominator:
            bits[h // 8] |= 1 << (h % 8)
    return int.from_bytes(bits, "little")


def descendants(parents, old_denominator, runners):
    denominator = 2 * old_denominator
    all_times = (1 << (denominator // 2 + 1)) - 2

    @lru_cache(maxsize=None)
    def mask(speed):
        return safe_times(speed, denominator, runners)

    retained = []
    for parent in parents:
        def visit(prefix, times, odd_count):
            if len(prefix) == len(parent):
                # At a power-of-two level the common-divisor test discards
                # exactly the tuples with at most one odd coordinate.
                if not times and odd_count >= 2:
                    retained.append(prefix)
                return
            v = parent[len(prefix)]
            for speed in (v, v + old_denominator):
                visit(prefix + (speed,), times & mask(speed), odd_count + speed % 2)

        visit((), all_times, 0)
    return retained


def counts(seed, prime, last_level=32):
    runners = 1 + len(seed)
    times = (1 << (prime // 2 + 1)) - 2
    for v in seed:
        times &= safe_times(v, prime, runners)
    parents = [] if times else [tuple(seed)]
    level = 1
    history = [len(parents)]
    while level < last_level:
        parents = descendants(parents, level * prime, runners)
        level *= 2
        history.append(len(parents))
    return history


def cross_check():
    # Independently enumerate all times on a full period and both digit choices.
    for old_denominator, parent in [(11, (1, 2, 3, 4)), (22, (1, 13, 3, 15))]:
        d = 2 * old_denominator
        expected = set()
        for digits in product((0, 1), repeat=len(parent)):
            speeds = tuple(v + a * old_denominator for v, a in zip(parent, digits))
            has_witness = any(all(5 * min(h*v % d, (-h*v) % d) >= d
                                  for v in speeds) for h in range(d))
            if not has_witness and sum(v % 2 for v in speeds) >= 2:
                expected.add(speeds)
        assert expected == set(descendants([parent], old_denominator, 5))


def even_sets(runners, prime):
    """Parity rule for p = 2*n-1 prime, using representatives 1 through n-1."""
    k = runners - 1

    def bit(value):
        residue = value % prime
        return 1 << (min(residue, prime - residue) - 1)

    triples = [(bit(j), bit(2*j), bit(3*j)) for j in range(1, runners)]
    return {
        even for even in range(1, 1 << k)
        if even.bit_count() <= k - 2
        and all(not (even & a and even & c) or even & b for a, b, c in triples)
    }


def check_parity_rule():
    for n, p in [(7, 13), (9, 17), (10, 19), (12, 23), (15, 29), (16, 31)]:
        seed = tuple(range(1, n))
        lifted = descendants([seed], p, n)
        actual = {sum(1 << j for j, v in enumerate(w) if v % 2 == 0) for w in lifted}
        predicted = even_sets(n, p)
        assert actual == predicted and len(actual) == len(lifted)
        print(f"{n} runners, p={p}: {len(actual)} surviving parity assignments")


if __name__ == "__main__":
    cross_check()
    check_parity_rule()
    for p in (199, 251):
        cases = [(str(n), tuple(range(1, n))) for n in (13, 14, 15, 16)]
        cases.append(("14 doubled", (*range(1, 12), 13, 24)))
        for name, speeds in cases:
            print(p, name, counts(speeds, p), flush=True)
