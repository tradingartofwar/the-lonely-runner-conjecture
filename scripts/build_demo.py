"""Regenerate the three-case demo: python -m scripts.build_demo [--check]."""

import argparse
import json
from pathlib import Path

from lonely_runner import check

ROOT = Path(__file__).resolve().parents[1]


def build():
    cases = []
    for third_speed in [2, 3, 4]:
        velocities = [0, 1, third_speed]
        cases.append({
            "key": str(third_speed),
            "velocities": [str(v) for v in velocities],
            "references": [check(velocities, r) for r in range(3)],
        })
    data = {"schema": 1, "cases": cases}
    fragment = (ROOT / "demo/fragment.html").read_text().replace(
        "__RUNNER_DATA__", json.dumps(data, separators=(",", ":")),
    )
    page = (ROOT / "demo/page.html").read_text().replace("__FRAGMENT__", fragment)
    return {"demo/cases.json": json.dumps(data, indent=2) + "\n", "demo/index.html": page}, fragment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed generated files differ from current code/templates.")
    parser.add_argument("--inline-output", type=Path, help="Optional conversation fragment destination, e.g. /workspace/lonely-runner-first-cases.html.")
    args = parser.parse_args()
    outputs, fragment = build()
    for relative, content in outputs.items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_text() != content:
                parser.exit(1, f"Out of date: {relative}; run python -m scripts.build_demo\n")
        else:
            path.write_text(content)
    if args.inline_output:
        args.inline_output.write_text(fragment)
    print("Demo matches exact checker and templates." if args.check else "Built three cases, all nine reference-runner checks, and standalone demo.")


if __name__ == "__main__":
    main()
