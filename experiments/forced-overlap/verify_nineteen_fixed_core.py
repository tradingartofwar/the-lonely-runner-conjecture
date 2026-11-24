"""Check the fixed 18-speed core and the finite cases of its 19-runner extension."""

from math import gcd

BASE = (*range(15), 105, 420, 480)
N = len(BASE) + 1
DIAMETER = max(BASE) - min(BASE)
TAIL_START = N * DIAMETER


def clears(difference, p, q, count):
    residue = (difference * p) % q
    return q <= count * residue <= (count - 1) * q


def verify_witness(group, runner, p, q, count):
    for opponent in group:
        if opponent == runner:
            continue
        residue = (p * abs(opponent - runner)) % q
        if count * min(residue, q - residue) < q:
            raise ValueError(f"Collision or insufficient clearance at {p}/{q}: {runner}, {opponent}")


def check():
    base_denominators = (17, 14, 13, 12, 11, 11, 10, 8, 9, 10, 11, 12, 14, 14, 15, 18, 25, 21)
    for runner, q in zip(BASE, base_denominators, strict=True):
        verify_witness(BASE, runner, 1, q, len(BASE))

    times = [
        (p, q)
        for q in range(2, 41)
        for p in range(1, q // 2 + 1)
        if gcd(p, q) == 1
    ]
    fixed_times = {
        runner: [
            (p, q) for p, q in times
            if all(clears(s - runner, p, q, N) for s in BASE if s != runner)
        ]
        for runner in BASE
    }
    groups_checked = roles_checked = 0
    for added in range(1, TAIL_START):
        if added in BASE:
            continue
        group = (*BASE, added)
        for runner in BASE:
            candidates = fixed_times[runner]
            witness = next(((p, q) for p, q in candidates if clears(added - runner, p, q, N)), None)
            if witness is None:
                raise ValueError(f"Missing fixed-runner witness: added={added}, runner={runner}")
            verify_witness(group, runner, *witness, N)
            roles_checked += 1

        if (N - 2) * added >= N * DIAMETER:
            witness = (1, 2 * added)
        else:
            witness = next(((p, q) for p, q in times if all(clears(s - added, p, q, N) for s in BASE)), None)
            if witness is None:
                raise ValueError(f"Missing newcomer witness: added={added}")
        verify_witness(group, added, *witness, N)
        roles_checked += 1
        groups_checked += 1

    if (groups_checked, roles_checked) != (9102, 172938):
        raise ValueError(f"Incomplete finite range: {groups_checked} groups, {roles_checked} roles")
    print(f"{len(BASE)} base witnesses, {groups_checked} added speeds, {roles_checked} runner checks passed.")


if __name__ == "__main__":
    check()
