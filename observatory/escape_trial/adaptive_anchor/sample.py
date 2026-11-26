"""Select the preregistered fresh conditional panel without calling either final arm."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial.last_anchor.select_cases import archive, first_arc_fails, shared_fail, prior


def exclusions():
    previous = json.loads((HERE.parent / 'last_anchor/selected.json').read_bytes())
    old_seed = bytes.fromhex(previous['seed_hex'])
    seen = archive()
    for cell in previous['conditional']:
        seen.update(map(tuple, cell['rows']))
    for band in prior.SCALES:
        rng = prior.stream(old_seed, 'last-anchor-ordinary-v1', band)
        seen.update(prior.draw_weights(rng, band, 'stretch_middle') for _ in range(8192))
    return seen


def sample(seed):
    seen = exclusions()
    excluded = len(seen)
    cells = []
    for band in prior.SCALES:
        rng = prior.stream(seed, 'adaptive-anchor-v1', band)
        rows = []
        for draws in range(1, 131073):
            weights = prior.draw_weights(rng, band, 'stretch_middle')
            if weights in seen or math.gcd(*weights) != 1:
                continue
            seen.add(weights)
            if first_arc_fails(weights) and shared_fail(weights):
                rows.append(weights)
                if len(rows) == 32:
                    break
        cells.append(dict(band=band, draws=draws, shortfall=32-len(rows), rows=rows))
    return dict(seed_hex=seed.hex(), excluded=excluded, cells=cells)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed-file', type=Path)
    args = parser.parse_args()
    seed = (args.seed_file.read_bytes() if args.seed_file
            else bytes.fromhex(json.loads((HERE/'panel.json').read_bytes())['seed_hex']))
    assert len(seed) == 32 and hashlib.sha256(seed).hexdigest() == (HERE/'seed.sha256').read_text().strip()
    print(json.dumps(sample(seed), separators=(',',':')))
