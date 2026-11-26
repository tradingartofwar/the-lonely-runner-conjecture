"""Select paired inputs without importing or calling either scored rule."""
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial import continuation as prior

PRIOR_SEED = bytes.fromhex("456475a077509b60f82776ad017e5b42")


def select(seed):
    seen = prior.published_exclusions()
    known = len(seen)
    for arm in ("unconditioned", "conditioned", "wrap_screen"):
        prior.sample(PRIOR_SEED, arm, seen)
    hosted = len(seen) - known
    membership = json.loads((HERE.parent/"membership_audit/panel.json").read_bytes())["rows"]
    seen.update(map(tuple,membership))
    # All other challenge-box examples have smallest weight >=257.
    seen.update(((260,264,1567,2101),(257,258,1543,2070),(258,261,522,1453),
                 (258,516,1032,2064),(257,271,720720,17*720720)))
    cells, rows = [], []
    exclusions = len(seen)
    assert tuple(prior.SCALES) == ((1, 4), (5, 16), (17, 64), (65, 256))
    for band in prior.SCALES:
        rng = prior.stream(seed, "anchor-swap-v1", band)
        cell = []
        for attempt in range(1, 4097):
            w = prior.draw_weights(rng, band, "stretch_middle")
            if w in seen or math.gcd(*w) != 1 or not prior.eligible(w, "wrap_screen"):
                continue
            cell.append(w)
            seen.add(w)
            if len(cell) == 256:
                break
        cells.append(dict(band=band, attempts=attempt, accepted=len(cell), shortfall=256-len(cell)))
        rows.extend(cell)
    return dict(archive_exclusions=known, prior_hosted_exclusions=hosted, additional_exclusions=exclusions-known-hosted, cells=cells, rows=rows)


if __name__ == "__main__":
    seed = Path(sys.argv[1]).read_bytes()
    assert hashlib.sha256(seed).hexdigest() == (HERE / "seed.sha256").read_text().strip()
    panel = select(seed)
    print(json.dumps(panel, separators=(",", ":")))
