"""Verify the three published runner-addition families using Python 3.11 or later."""
import argparse
import csv
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
STUDY = Path("experiments/forced-overlap")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panels", action="store_true", help="replay both endpoint panels")
    parser.add_argument("--regenerate", action="store_true", help="rebuild all three certificates")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error("Python 3.11 or newer is required")
    if not __debug__:
        parser.error("verification requires Python assertions")
    root = next(p for p in (HERE, *HERE.parents) if (p / STUDY / "verify_seventeen_family.py").is_file())
    study = root / STUDY
    manifest = HERE / "SHA256SUMS"
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            expected, filename = line.split("  ", 1)
            if hashlib.sha256((HERE / filename).read_bytes()).hexdigest() != expected:
                raise SystemExit(f"Archive integrity check failed for {filename}")
        print("Archive checksums passed.", flush=True)

    env = {**os.environ, "PYTHONPATH": str(root), "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("PYTHONOPTIMIZE", None)

    def run(script, *arguments, capture=False):
        result = subprocess.run([sys.executable, str(study / script), *map(str, arguments)],
                                cwd=root, env=env, stdout=subprocess.PIPE if capture else None,
                                check=True)
        return result.stdout

    run("verify_seventeen_family.py")
    run("verify_eighteen_family.py")
    run("verify_eighteen_family.py", "--transfer")
    if args.panels:
        for name in ("seventeen", "eighteen"):
            actual = json.loads(run(f"{name}_study.py", capture=True))
            expected = json.loads((study / f"{name}_results.json").read_bytes())
            if actual != expected:
                raise SystemExit(f"{name} panel differs from its full archived result")
            print(f"{name.capitalize()} endpoint panel matches the archived result.", flush=True)

    if args.regenerate:
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            ledger = folder / "seventeen.csv"
            summary = json.loads(run("seventeen_family.py", "--certificates", ledger, capture=True))
            if summary != json.loads((study / "seventeen_family_results.json").read_bytes()):
                raise SystemExit("17-runner family summary differs")
            with ledger.open(newline="") as left, (study / "seventeen_family_witnesses.csv").open(newline="") as right:
                if list(csv.reader(left)) != list(csv.reader(right)):
                    raise SystemExit("17-runner witness ledger differs")
            for filename, options in (("eighteen_family.json.xz", []),
                                      ("eighteen_transfer.json.xz", ["--transfer"])):
                generated = folder / filename
                run("eighteen_family.py", *options, "--out", generated)
                with lzma.open(generated) as actual, lzma.open(study / filename) as expected:
                    if json.load(actual) != json.load(expected):
                        raise SystemExit(f"Generated certificate differs from {filename}")
            print("All three regenerated certificates match.", flush=True)


if __name__ == "__main__":
    main()
