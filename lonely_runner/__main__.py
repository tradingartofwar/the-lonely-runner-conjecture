"""Run with python -m lonely_runner --velocities 0 1 2."""

import argparse
import json
from .checker import check


def main(argv=None):
    parser = argparse.ArgumentParser(description="Exact common-start Lonely Runner checker (Python 3.10+).")
    parser.add_argument("--velocities", nargs="+", required=True, help="Integer or p/q speeds, separated by spaces or commas. For negative fractions use --velocities=-1/2,0,1/2.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--reference", type=int, default=0, help="Zero-based runner index; default 0.")
    group.add_argument("--all-references", action="store_true", help="Check every runner separately.")
    parser.add_argument("--threshold", help="Optional positive p/q threshold; default 1/n.")
    parser.add_argument("--feasibility-only", action="store_true", help="Skip the more expensive maximum calculation.")
    parser.add_argument("--json", action="store_true", help="Machine-readable exact output.")
    args = parser.parse_args(argv)
    velocities = [v for token in args.velocities for v in token.split(",")]
    refs = range(len(velocities)) if args.all_references else [args.reference]
    try:
        results = [check(velocities, r, threshold=args.threshold, compute_maximum=not args.feasibility_only) for r in refs]
    except (ValueError, ArithmeticError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(results if args.all_references else results[0], indent=2))
        return
    for result in results:
        print(f"Velocities: ({', '.join(result['velocities'])}); reference #{result['reference_index']} (speed {result['reference_velocity']})")
        print(f"Runners: {result['n']}; threshold: {result['threshold']}; feasible: {result['feasible']}")
        print(f"Relative-distance period: {result['period_original']}; original t = normalized tau × {result['period_original']}")
        print("Allowed original times (closed intervals; [a,a] is a valid instant):")
        print("  " + (", ".join(f"[{a}, {b}]" for a, b in result['intervals_original']) or "none"))
        if result["maximum"]:
            maximum = result["maximum"]
            print(f"Exact maximum: {maximum['separation']}; attaining times: {', '.join(maximum['times_original'])}")
            print("Independent interval / piecewise-linear crosscheck: passed")
        print()


if __name__ == "__main__":
    main()
