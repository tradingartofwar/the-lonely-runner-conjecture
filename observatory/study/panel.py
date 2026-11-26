"""Seal or replay the twelve-input blind comparison. Never evaluate a time here."""
import argparse
import hashlib
import itertools
import json
import math
import random
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPERIMENTS = ROOT / "experiments"
GENERATOR = EXPERIMENTS / "subset-sum-prediction" / "generate.py"
sys.path.insert(0, str(GENERATOR.parent))
from generate import SCALES, draw_weights

RECIPE = {
    "generator": "experiments/subset-sum-prediction/generate.py:draw_weights",
    "pattern": "stretch_middle",
    "ordered_bands": [list(scale) for scale in SCALES],
    "accept_per_band": 3,
    "rng": "CPython random.Random(int.from_bytes(raw_32_byte_seed, 'big')), one stream",
    "reject": ["gcd of weights exceeds one", "weights in exclusions.json", "repeat accepted weights"],
    "panel_encoding": "sorted keys, compact JSON, UTF-8, trailing LF; arrays retain draw order",
    "exclusion_scope": "Versioned 60-case panel, both complement controls, 15 three-prefix "
                       "controls, consecutive-speed control. Also check speed sets in the "
                       "240-case one-time panel, 2048 count-invariant random lineups for "
                       "n=16, and integer arrays in prior experiment JSON; retain four-weight "
                       "decompositions only when all 15 physical speeds coincide.",
}


def canonical(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def physical(weights):
    return sorted(sum(s) for size in range(1, 5) for s in itertools.combinations(weights, size))


def recover_weights(values):
    """Invert a superincreasing subset-sum lineup, if it is one."""
    values = sorted(v for v in values if v != 0)
    if len(values) != 15 or values[0] <= 0 or len(set(values)) != 15:
        return None
    partial = {0}
    weights = []
    for value in values:
        if value not in partial:
            if len(weights) == 4 or value <= sum(weights):
                return None
            weights.append(value)
            partial.update(s + value for s in tuple(partial))
    if len(weights) == 4 and sorted(partial) == [0, *values]:
        return tuple(weights)
    return None


def arrays(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from arrays(item)
    if isinstance(value, list):
        if len(value) in (15, 16) and all(type(n) is int for n in value):
            yield value
        else:
            for item in value:
                yield from arrays(item)


def exclusions():
    opened = json.loads((GENERATOR.parent / "panel.json").read_bytes())
    weights = {tuple(row["weights"]) for row in opened["instances"]}
    weights.update({(1, 2, 4, 8), (1, 6, 11, math.lcm(*range(1, 33)) - 18),
                    (114, 139, 359, 1100)})
    for total in (112, 128, 144, 160, 16 * 10**9):
        for prefix in ((1, 2, 13), (1, 3, 8), (1, 4, 6)):
            weights.add((*prefix, total - sum(prefix)))

    def collect(lineups):
        for lineup in lineups:
            candidate = recover_weights(lineup)
            if candidate is not None:
                weights.add(candidate)

    with tempfile.TemporaryDirectory() as temp:
        archived = Path(temp) / "one-time.json"
        subprocess.run([sys.executable, str(EXPERIMENTS / "one-time-prediction/generate.py"),
                        str(archived)], stdout=subprocess.DEVNULL, check=True)
        collect(row["speeds"] for row in json.loads(archived.read_bytes()))
    sys.path.insert(0, str(EXPERIMENTS / "count-invariants"))
    from test_second_time import draw
    for panel in range(4):
        rng = random.Random(2026112400 + 160 + panel)
        collect(draw(16, panel, rng) for _ in range(256))
    for maximum in (1024, 1031, 1050, 1260):
        rng = random.Random(202611241600 + maximum)
        collect([maximum, *rng.sample(range(1, maximum), 14)] for _ in range(256))
    for file in EXPERIMENTS.rglob("*.json"):
        collect(arrays(json.loads(file.read_bytes())))
    return sorted(weights)


def draw_panel(seed, excluded):
    if len(seed) != 32:
        raise ValueError("expected 32 seed bytes")
    rng = random.Random(int.from_bytes(seed, "big"))
    seen = set(map(tuple, excluded))
    rows = []
    for scale in SCALES:
        count = 0
        while count < 3:
            weights = draw_weights(rng, scale, "stretch_middle")
            if math.gcd(*weights) != 1 or weights in seen:
                continue
            seen.add(weights)
            rows.append({"scale": list(scale), "weights": list(weights), "pattern": "stretch_middle"})
            count += 1
    return {"instances": rows}


def commitment(seed, panel, excluded):
    return {
        "schema_version": 1,
        "raw_seed_sha256": digest(seed),
        "panel_sha256": digest(canonical(panel)),
        "recipe": RECIPE,
        "recipe_sha256": digest(canonical(RECIPE)),
        "sampling_code_sha256": digest(Path(__file__).read_bytes()),
        "original_generator_sha256": digest(GENERATOR.read_bytes()),
        "exclusions_sha256": digest(canonical(excluded)),
        "excluded_lineups": len(excluded),
    }


def verify(reveal_dir):
    seed = bytes.fromhex((reveal_dir / "seed.hex").read_text().strip())
    excluded = json.loads((HERE / "exclusions.json").read_bytes())
    if canonical(exclusions()) != canonical(excluded):
        raise ValueError("archived exclusions changed")
    panel = draw_panel(seed, excluded)
    if canonical(panel) != (reveal_dir / "panel.json").read_bytes():
        raise ValueError("panel does not regenerate")
    expected = json.loads((HERE / "commitment.json").read_bytes())
    if commitment(seed, panel, excluded) != expected:
        raise ValueError("commitment mismatch")
    return panel


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["seal", "verify"])
    parser.add_argument("reveal_dir", type=Path)
    args = parser.parse_args()
    directory = args.reveal_dir.resolve()
    if args.operation == "verify":
        verify(directory)
        print("Verified inputs, seed, exclusions, recipe and generator hashes.")
        return
    if directory == ROOT or ROOT in directory.parents:
        raise ValueError("private seal directory must be outside the repository")
    if (HERE / "commitment.json").exists():
        raise ValueError("commitment already exists")
    directory.mkdir(mode=0o700, exist_ok=False)
    excluded = exclusions()
    seed = secrets.token_bytes(32)
    panel = draw_panel(seed, excluded)
    (directory / "seed.hex").write_text(seed.hex() + "\n")
    (directory / "panel.json").write_bytes(canonical(panel))
    (HERE / "exclusions.json").write_bytes(canonical(excluded))
    (HERE / "commitment.json").write_text(json.dumps(commitment(seed, panel, excluded), indent=2) + "\n")
    print("Sealed 12 inputs. Reveal material stays in the private directory.")


if __name__ == "__main__":
    main()
