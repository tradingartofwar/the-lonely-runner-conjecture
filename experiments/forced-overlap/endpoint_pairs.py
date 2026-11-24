"""Predict the fast-runner cutoff for a core of fourteen integer speeds."""
import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import gcd

from lonely_runner.checker import ComputationLimitError, feasible_intervals
from same_pass import can_trap_pair

TARGET = Fraction(1, 16)
STRONG = Fraction(1, 15)


@dataclass(frozen=True)
class PairBound:
    u: int
    w: int
    scaled_width: int

    @property
    def cutoff(self):
        return Fraction(2 * self.u * self.w, self.scaled_width)


def pair_bound(u, w):
    common = gcd(u, w)
    speed_sum = u + w
    # Round the required width up to the first attainable residue class.
    step_index = (speed_sum + 15 * common - 1) // (15 * common)
    return PairBound(u, w, 16 * common * step_index - speed_sum)


def core_bounds(core):
    core = tuple(core)
    if (len(core) != 14 or any(type(v) is not int or v <= 0 for v in core)
            or len(set(core)) != 14):
        raise ValueError("Supply fourteen distinct positive integer core speeds.")
    second, largest = sorted(core)[-2:]
    original = Fraction(30 * second * largest, second + largest)
    pairs = [pair_bound(u, w) for u, w in combinations(core, 2)]
    return original, max(p.cutoff for p in pairs), pairs


def strong_components(core):
    """All closed target components containing at least one stronger witness."""
    target = feasible_intervals(core, TARGET)
    strong = feasible_intervals(core, STRONG)
    components = []
    j = 0
    for left, right in target:
        while j < len(strong) and strong[j][1] < left:
            j += 1
        if j < len(strong) and left <= strong[j][0] <= right:
            components.append((left, right))
    return components


def witness_on_component(left, right, fastest):
    """Allow the left endpoint; if blocked, try the right edge of its blocking arc."""
    phase = fastest * left
    if TARGET <= phase % 1 <= 1 - TARGET:
        return left
    exit_time = (round(phase) + TARGET) / fastest
    if exit_time <= right:
        return exit_time
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("core", type=int, nargs=14, metavar="SPEED")
    parser.add_argument("--fastest", type=int, required=True)
    parser.add_argument("--same-pass", action="store_true",
                        help="require both endpoints to fit inside one blocking pass")
    parser.add_argument("--witness", action="store_true",
                        help="also search the retained intervals using the bounded exact solver")
    args = parser.parse_args()
    try:
        original, refined, pairs = core_bounds(args.core)
    except ValueError as e:
        parser.error(str(e))
    if args.fastest <= max(args.core):
        parser.error("--fastest must exceed every retained speed")
    candidates = [p for p in pairs if p.cutoff > args.fastest]
    report = {
        "two_endpoint_cutoff": str(original), "congruence_cutoff": str(refined),
        "prediction": "unresolved" if candidates else "certified under the 15-runner result",
        "pairs_setting_refined_cutoff": [[p.u, p.w] for p in pairs if p.cutoff == refined],
        "remaining_endpoint_pairs": [[p.u, p.w] for p in candidates],
    }
    if args.same_pass:
        compatible = [p for p in candidates if can_trap_pair(p, args.fastest)]
        report["same_pass_prediction"] = ("unresolved" if compatible else
                                          "certified under the 15-runner result")
        report["same_pass_pairs"] = [[p.u, p.w] for p in compatible]
    if args.witness:
        witness = None
        try:
            for left, right in strong_components(args.core):
                witness = witness_on_component(left, right, args.fastest)
                if witness is not None:
                    break
        except ComputationLimitError as e:
            # The prediction works even when interval enumeration exceeds its budget.
            report["witness_search_error"] = str(e)
        report["witness_from_strong_component"] = str(witness) if witness is not None else None
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
