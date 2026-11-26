"""Replay fresh selection without invoking a last-anchor arm.

Default output is the committed selected.json, regenerated from its recorded seed.
Use --seed-file only for the verifier's initial generation.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial import continuation as prior
from observatory.escape_trial.anchor_swap.select_panel import PRIOR_SEED
from observatory.escape_trial.reentry_membership import classes_at, inspect
from observatory.escape_trial.rule import predict


def archive():
    seen = prior.published_exclusions()
    for arm in ("unconditioned", "conditioned", "wrap_screen"):
        prior.sample(PRIOR_SEED, arm, seen)
    for directory in ("membership_audit", "anchor_swap"):
        panel = json.loads((HERE.parent / directory / "panel.json").read_bytes())
        seen.update(map(tuple, panel["rows"]))
    seen.update(((260,264,1567,2101), (257,258,1543,2070), (258,261,522,1453),
                 (258,516,1032,2064), (257,271,720720,17*720720)))
    return seen


def first_arc_fails(weights):
    """Exact first-arc gate by integer cross multiplication on every speed."""
    speeds = [0]
    for w in weights:
        speeds += [s+w for s in speeds]
    speeds = speeds[1:]
    for q in range(16, 1, -1):
        residues = [v % q for v in speeds]
        colliders = [v for v,r in zip(speeds,residues) if r == 0]
        if not colliders:
            return False
        m = min(colliders)
        if max(colliders) > 15*m:
            continue
        forward, backward = True, True
        for v,r in zip(speeds, residues):
            if r:
                forward = forward and q*v <= m*(15*q-16*r)
                backward = backward and q*v <= m*(16*r-q)
                if not forward and not backward:
                    break
        if forward or backward:
            return False
    return True


def shared_fail(weights):
    for q in (3,5):
        groups = classes_at(weights,q)
        if any(inspect(groups,q,sign)[0] is not None for sign in (1,-1)):
            return False
    return True


def select(seed):
    known = archive()
    # Historical inputs serve only as controls on the equivalent faster gate.
    assert all(first_arc_fails(w) == (predict(w) is None) for w in known)
    excluded = set(known)
    ordinary, conditional = [], []
    for band in prior.SCALES:
        rng = prior.stream(seed, "last-anchor-ordinary-v1", band)
        primitive = abstentions = eligible = 0
        for _ in range(8192):
            w = prior.draw_weights(rng, band, "stretch_middle")
            excluded.add(w)
            if math.gcd(*w) != 1:
                continue
            primitive += 1
            if first_arc_fails(w):
                assert predict(w) is None
                abstentions += 1
                eligible += shared_fail(w)
        ordinary.append(dict(band=band, raw=8192, primitive=primitive,
                             first_arc_abstentions=abstentions, eligible=eligible))
    for band in prior.SCALES:
        rng = prior.stream(seed, "last-anchor-conditional-v1", band)
        rows = []
        for draws in range(1, 131073):
            w = prior.draw_weights(rng, band, "stretch_middle")
            if w in excluded or math.gcd(*w) != 1:
                continue
            excluded.add(w)
            if first_arc_fails(w) and shared_fail(w):
                assert predict(w) is None
                rows.append(w)
                if len(rows) == 32:
                    break
        conditional.append(dict(band=band, raw=draws, shortfall=32-len(rows), rows=rows))
    return dict(seed_hex=seed.hex(), historical_controls=len(known),
                ordinary=ordinary, conditional=conditional)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-file", type=Path)
    args = parser.parse_args()
    seed = (args.seed_file.read_bytes() if args.seed_file else
            bytes.fromhex(json.loads((HERE/"selected.json").read_bytes())["seed_hex"]))
    assert len(seed) == 32 and hashlib.sha256(seed).hexdigest() == (HERE/"seed.sha256").read_text().strip()
    print(json.dumps(select(seed), separators=(",",":")))
