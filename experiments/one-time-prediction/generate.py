"""Generate the frozen 240-lineup panel; the reference runner has speed zero."""
import hashlib
import json
import random
import sys
from pathlib import Path

SEED = int("1697b9d0a71569b75fa633a2af42932fb2b2dd43d844aff1d3308426f4587964", 16)


def near_progression(rng):
    step = rng.randint(1, 12)
    removed = rng.randint(2, 4)
    progression = [step * i for i in range(1, 16)]
    kept = rng.sample(progression, 15 - removed)
    outliers = rng.sample(range(15 * step + 1, 35 * step + 1), removed)
    return kept + outliers


def residue_clusters(rng):
    modulus = rng.choice([5, 7, 9, 11])
    residues = rng.sample(range(modulus), 3)
    pool = [s for s in range(1, 251) if s % modulus in residues]
    while True:
        choices = rng.sample(pool, 15)
        if len({s % modulus for s in choices}) == 3:
            return choices


def uniform(rng):
    return rng.sample(range(1, 201), 15)


def two_scale(rng):
    start = rng.randint(120, 1000)
    return rng.sample(range(8, 71), 10) + rng.sample(range(start, start + 31), 5)


def main():
    rng = random.Random(SEED)
    rows = []
    seen = set()
    for name, generate in [
        ("near_progression", near_progression),
        ("residue_clusters", residue_clusters),
        ("uniform", uniform),
        ("two_scale", two_scale),
    ]:
        count = 0
        while count < 60:
            speeds = tuple(sorted(generate(rng)))
            assert len(speeds) == len(set(speeds)) == 15 and speeds[0] > 0
            if speeds in seen:
                continue
            seen.add(speeds)
            rows.append({"bucket": name, "speeds": speeds})
            count += 1
    output_path = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/lr_blind_panels.json")
    data = (json.dumps(rows, separators=(",", ":")) + "\n").encode("ascii")
    output_path.write_bytes(data)
    print(hashlib.sha256(data).hexdigest(), output_path)


if __name__ == "__main__":
    main()
