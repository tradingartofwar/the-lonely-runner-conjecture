"""Search all triangle-free unsigned supports at seven prime clocks, up to 15 speeds."""

from itertools import combinations


def search(prime):
    m = (prime - 1) // 2
    full = (1 << m) - 1
    def folded(v):
        return min(v % prime, -v % prime)

    # If a,b have already been chosen, these third classes complete a signed triple.
    third = {}
    for a, b in combinations(range(1, m+1), 2):
        third[a, b] = sum(1 << (c-1) for c in {folded(a+b), folded(a-b)} - {a,b})
    blocked = {v: sum(1 << (j-1) for j in range(1,m+1) if 16*folded(v*j) < prime)
               for v in range(1,m+1)}
    covers = visited = largest = max_blocked = 0
    example = None
    def visit(speeds, allowed, times):
        nonlocal covers, visited, largest, max_blocked, example
        visited += 1
        largest = max(largest, len(speeds))
        max_blocked = max(max_blocked, times.bit_count())
        if times == full:
            covers += 1
            if example is None:
                example = speeds
        if len(speeds) == 15:
            return
        while allowed:
            bit = allowed & -allowed
            v = bit.bit_length()
            allowed ^= bit
            next_allowed = allowed
            for a in speeds:
                next_allowed &= ~third[a,v]
            visit(speeds + (v,), next_allowed, times | blocked[v])

    visit((), full, 0)
    return visited, largest, max_blocked, covers, example


if __name__ == "__main__":
    largest_by_prime = {37: 7, 41: 8, 43: 8, 47: 9, 53: 10, 59: 11, 61: 11}
    for p, expected_largest in largest_by_prime.items():
        result = search(p)
        assert result[1] == expected_largest and result[3] == 0
        print(p, result, flush=True)
