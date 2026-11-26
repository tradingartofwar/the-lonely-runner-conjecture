"""Generate the four-weight subset-sum panel without evaluating clock times."""
import argparse
import hashlib
import itertools
import json
import math
import random
import secrets
from pathlib import Path


SCALES = ((1, 4), (5, 16), (17, 64), (65, 256))
PATTERNS = ("boundary", "balanced", "stretch_first", "stretch_middle", "stretch_last")
DRAWS_PER_CELL = 3


def ceil16(n):
    return (n + 15) // 16


def draw_weights(rng, scale, pattern):
    a = rng.randint(*scale)
    if pattern == "boundary":
        x = y = 1
        k = 0
    elif pattern == "balanced":
        x = rng.randint(a, 2 * a)
        y = rng.randint(a, 2 * a)
        k = rng.randint(a // 16, ceil16(2 * a))
    elif pattern == "stretch_first":
        x = rng.randint(4 * a, 8 * a)
        y = rng.randint(1, a)
        k = rng.randint(0, ceil16(a))
    elif pattern == "stretch_middle":
        x = rng.randint(1, a)
        y = rng.randint(4 * a, 8 * a)
        k = rng.randint(0, ceil16(a))
    elif pattern == "stretch_last":
        x = rng.randint(1, a)
        y = rng.randint(1, a)
        k = rng.randint(ceil16(4 * a), ceil16(8 * a))
    else:
        raise ValueError(pattern)
    b = a + x
    c = a + b + y
    partial_sum = a + b + c
    min_gap = 1 + ((-2 * partial_sum - 1) % 16)
    d = partial_sum + min_gap + 16 * k
    return (a, b, c, d)


def generate(seed_hex):
    rng = random.Random(int(seed_hex, 16))
    rows = []
    seen = set()
    for scale in SCALES:
        for pattern in PATTERNS:
            drawn = 0
            while drawn < DRAWS_PER_CELL:
                weights = draw_weights(rng, scale, pattern)
                if weights in seen or math.gcd(*weights) != 1:
                    continue
                seen.add(weights)
                speeds = sorted(sum(s) for n in range(1, 5)
                                for s in itertools.combinations(weights, n))
                assert len(set(speeds)) == 15 and speeds[-1] % 16 == 0
                rows.append({"pattern": pattern, "scale": list(scale),
                             "weights": list(weights), "speeds": speeds})
                drawn += 1
    assert len(rows) == 60
    return {"family": "superincreasing-four-weight-subset-sums-v1",
            "sampling": "uniform inclusive random integers by stated stratum; primitive, distinct",
            "seed_hex": seed_hex, "instance_count": len(rows), "instances": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed-hex", default=None)
    args = parser.parse_args()
    seed = secrets.token_hex(32) if args.seed_hex is None else args.seed_hex
    if len(seed) != 64:
        raise ValueError("Expected a 256-bit hexadecimal seed.")
    panel = generate(seed)
    data = (json.dumps(panel, sort_keys=True, separators=(",", ":")) + "\n").encode()
    args.output.write_bytes(data)
    print("panel_sha256", hashlib.sha256(data).hexdigest())
    print("seed_sha256", hashlib.sha256(bytes.fromhex(seed)).hexdigest())


if __name__ == "__main__":
    main()
