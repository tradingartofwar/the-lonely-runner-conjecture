"""Read-only replay of the bounded September 27 Ultra review evidence.

Run from any directory. Optional positional names select groups. These checks
verify exact finite evidence, not every symbolic argument or any novelty claim.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECKS = {
    "arithmetic": ("arithmetic_check.py", "arithmetic_check.json"),
    "geometry": ("geometry_check.py", "geometry_check.json"),
    "optimization": ("optimization_check.py", None),
    "rigor": ("rigor_check.py", None),
    "strategy": ("strategy_check.py", None),
    "root": ("root_check.py", None),
}

# Capture the two writers rather than changing their independently supplied
# scripts. Each script runs in a separate interpreter with assertions enabled.
BOOTSTRAP = r'''
import json, runpy, sys
from pathlib import Path
script = Path(sys.argv[1]).resolve()
expected = script.parent / sys.argv[2]
captured = {}
def capture(self, data, *args, **kwargs):
    path = self.resolve()
    if path != expected:
        raise RuntimeError("Unexpected write: " + str(path))
    captured[path] = data
    return len(data)
Path.write_text = capture
sys.argv = [str(script)]
runpy.run_path(str(script), run_name="__main__")
assert set(captured) == {expected}, "Expected one archived output"
assert json.loads(captured[expected]) == json.loads(expected.read_text()), "Archive drift"
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checks", nargs="*")
    args = parser.parse_args()
    names = args.checks or list(CHECKS)
    for name in names:
        if name not in CHECKS:
            parser.error("Unknown group: " + name)
        script, archive = CHECKS[name]
        cmd = ([sys.executable, "-B", "-c", BOOTSTRAP, str(HERE/script), archive]
               if archive else [sys.executable, "-B", str(HERE/script), "--check"])
        print("Checking " + name + "...", flush=True)
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if result.returncode:
            print(result.stdout, end="")
            print(result.stderr, file=sys.stderr, end="")
            raise SystemExit(result.returncode)
        print("PASS: " + name, flush=True)
    print(f"PASS: {len(names)} bounded review groups; no archived outputs rewritten.")


if __name__ == "__main__":
    main()
