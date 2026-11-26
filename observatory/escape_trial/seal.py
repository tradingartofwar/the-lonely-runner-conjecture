"""Sample fresh middle-gap lineups without computing any return or clearance."""
import argparse
import json
import secrets
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent / "study"
sys.path.insert(0, str(STUDY))
import panel as previous

ROOT = previous.ROOT
RECIPE = {
    **previous.RECIPE,
    "exclusion_scope": (
        "All exclusions in observatory/study/exclusions.json, every lineup in its "
        "revealed 12-row panel and every four-weight control in its results.json."
    ),
}


def published_weights(record):
    if isinstance(record, dict):
        if "weights" in record:
            yield tuple(record["weights"])
        for value in record.values():
            yield from published_weights(value)
    elif isinstance(record, list):
        for value in record:
            yield from published_weights(value)


def exclusions():
    old = json.loads((STUDY / "exclusions.json").read_bytes())
    groups = [json.loads((STUDY / name).read_bytes())
              for name in ("reveal/panel.json", "results.json")]
    return sorted(set(map(tuple, old)).union(*(published_weights(g) for g in groups)))


def record(seed, inputs, excluded):
    return {
        "schema_version": 1,
        "raw_seed_sha256": previous.digest(seed),
        "panel_sha256": previous.digest(previous.canonical(inputs)),
        "recipe": RECIPE,
        "exclusions_sha256": previous.digest(previous.canonical(excluded)),
        "excluded_lineups": len(excluded),
        "source_sha256": {
            str(file.relative_to(ROOT)): previous.digest(file.read_bytes())
            for file in (Path(__file__), STUDY / "panel.py", previous.GENERATOR,
                         STUDY / "exclusions.json", STUDY / "reveal/panel.json",
                         STUDY / "results.json")
        },
    }


def verify(directory):
    seed = bytes.fromhex((directory / "seed.hex").read_text().strip())
    excluded = exclusions()
    inputs = previous.draw_panel(seed, excluded)
    checks = (
        (HERE / "exclusions.json", previous.canonical(excluded)),
        (directory / "panel.json", previous.canonical(inputs)),
        (HERE / "commitment.json", (json.dumps(record(seed, inputs, excluded), indent=2) + "\n").encode()),
    )
    for path, expected in checks:
        if path.read_bytes() != expected:
            raise ValueError(f"Commitment mismatch for {path.name}")
    return inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("seal", "verify"))
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if args.action == "verify":
        verify(directory)
        print("Reproduced the exclusions, seed, draw, input bytes and source commitment.")
        return
    if directory.is_relative_to(ROOT) or (HERE / "commitment.json").exists():
        raise ValueError("Seal once in a new directory outside the repository.")
    directory.mkdir(mode=0o700, exist_ok=False)
    seed = secrets.token_bytes(32)
    excluded = exclusions()
    inputs = previous.draw_panel(seed, excluded)
    (directory / "seed.hex").write_text(seed.hex() + "\n")
    (directory / "panel.json").write_bytes(previous.canonical(inputs))
    (HERE / "exclusions.json").write_bytes(previous.canonical(excluded))
    (HERE / "commitment.json").write_text(json.dumps(record(seed, inputs, excluded), indent=2) + "\n")
    verify(directory)
    print(f"Sealed 12 draws with {len(excluded)} excluded lineups.")


if __name__ == "__main__":
    main()
