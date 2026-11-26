"""Export a read-only board from one real, completed local verification run."""
import argparse
import json
from pathlib import Path
import shutil

from .runtime import ROOT, Store, default_db, revisions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="destination for static hosting")
    parser.add_argument("--db", type=Path, default=default_db())
    args = parser.parse_args()
    if not args.db.is_file():
        parser.error("Run python -m observatory run against this database first.")
    store = Store(args.db)
    store.import_journal()
    state = store.board(snapshot=True)
    verified = next((j for j in state["jobs"] if j["id"] == "verify"), None)
    if not verified or verified["state"] != "completed":
        parser.error("The independent verification replay must have completed.")
    if (verified["input_revision"], verified["code_revision"]) != revisions():
        parser.error("The checked revisions differ from this checkout. Replay in a fresh database.")
    # Publishing uses an explicit allowlist. The operational database stays on the worker host.
    destination = args.directory.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "app.js", "style.css"):
        shutil.copy2(ROOT / "observatory/web" / name, destination / name)
    shutil.copy2(ROOT / "observatory/study/results.json", destination / "results.json")
    (destination / "demo").mkdir(exist_ok=True)
    for name in ("index.html", "cases.json"):
        shutil.copy2(ROOT / "demo" / name, destination / "demo" / name)
    snapshot = destination / "snapshot.json"
    temporary = destination / ".snapshot.tmp"
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(snapshot)
    print(f"Exported {len(state['events'])} real events as of {state['generated_at']}")


if __name__ == "__main__":
    main()
