"""Test whether a faster integer runner preserves clearance for 16 or 17 total runners."""
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
    total: int = 16

    @property
    def cutoff(self):
        return Fraction(2 * self.u * self.w, self.scaled_width)


def pair_bound(u, w, total=16):
    common = gcd(u, w)
    speed_sum = u + w
    # Round the required width up to the first attainable residue class.
    slack_modulus = (total - 1) * common
    step_index = (speed_sum + slack_modulus - 1) // slack_modulus
    return PairBound(u, w, total * common * step_index - speed_sum, total)


def core_bounds(core, total=16):
    core = tuple(core)
    if (len(core) != total - 2 or any(type(v) is not int or v <= 0 for v in core)
            or len(set(core)) != total - 2):
        raise ValueError(f"Supply {total - 2} distinct positive integer core speeds.")
    second, largest = sorted(core)[-2:]
    original = Fraction(2 * (total - 1) * second * largest, second + largest)
    pairs = [pair_bound(u, w, total) for u, w in combinations(core, 2)]
    return original, max(p.cutoff for p in pairs), pairs


def strong_components(core, total=16, strong=None):
    """All closed target components containing at least one stronger witness."""
    target = feasible_intervals(core, Fraction(1, total))
    if strong is None:
        strong = feasible_intervals(core, Fraction(1, total - 1))
    components = []
    j = 0
    for left, right in target:
        while j < len(strong) and strong[j][1] < left:
            j += 1
        if j < len(strong) and left <= strong[j][0] <= right:
            components.append((left, right))
    return components


def witness_on_component(left, right, fastest, target=TARGET):
    """Allow the left endpoint; if blocked, try the right edge of its blocking arc."""
    phase = fastest * left
    if target <= phase % 1 <= 1 - target:
        return left
    exit_time = (round(phase) + target) / fastest
    if exit_time <= right:
        return exit_time
    return None


def component_at_strong_time(core, time, total):
    """Recover the physical target component in one pass over the retained speeds."""
    slack_level = Fraction(1, total - 1)
    target = Fraction(1, total)
    left, right = Fraction(0), Fraction(1)
    time %= 1
    for v in core:
        lap, phase = divmod(v * time, 1)
        if not slack_level <= phase <= 1 - slack_level:
            raise ValueError(f"Core speed {v} fails the 1/{total - 1} premise at {time}.")
        left = max(left, (lap + target) / v)
        right = min(right, (lap + 1 - target) / v)
    return left, right


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("core", type=int, nargs="+", metavar="SPEED")
    parser.add_argument("--runners", type=int, choices=(16, 17), default=16,
                        help="total runners including the stationary reference")
    parser.add_argument("--fastest", type=int, required=True)
    parser.add_argument("--core-time", type=Fraction,
                        help="verify this exact time for the stronger retained core")
    parser.add_argument("--same-pass", action="store_true",
                        help="require both endpoints to fit inside one blocking pass")
    parser.add_argument("--witness", action="store_true",
                        help="search retained components for an exact full witness")
    args = parser.parse_args()
    n = args.runners
    try:
        original, refined, pairs = core_bounds(args.core, n)
    except ValueError as e:
        parser.error(str(e))
    if args.fastest <= max(args.core):
        parser.error("--fastest must exceed every retained speed")
    candidates = [p for p in pairs if p.cutoff > args.fastest]
    report = {}
    success = "certified under the 15-runner result"
    core_time = args.core_time
    if n == 17:
        success = "conditional on a 1/16 core witness"
        if core_time is None:
            try:
                strong = feasible_intervals(args.core, Fraction(1, 16))
                if strong:
                    core_time = strong[0][0]
                else:
                    success = "inapplicable: the core has no 1/16 witness"
            except ComputationLimitError as e:
                report["core_search_error"] = str(e)
    component = None
    if core_time is not None:
        try:
            component = component_at_strong_time(args.core, core_time, n)
        except ValueError as e:
            parser.error(str(e))
        report["verified_core_time"] = str(core_time % 1)
        success = f"certified from the verified 1/{n - 1} core time"
    report.update({
        "two_endpoint_cutoff": str(original), "congruence_cutoff": str(refined),
        "prediction": "unresolved" if candidates else success,
        "pairs_setting_refined_cutoff": [[p.u, p.w] for p in pairs if p.cutoff == refined],
        "remaining_endpoint_pairs": [[p.u, p.w] for p in candidates],
    })
    if args.same_pass:
        compatible = [p for p in candidates if can_trap_pair(p, args.fastest)]
        report["same_pass_prediction"] = "unresolved" if compatible else success
        report["same_pass_pairs"] = [[p.u, p.w] for p in compatible]
    if args.witness:
        target = Fraction(1, n)
        witness = (witness_on_component(*component, args.fastest, target)
                   if component is not None else None)
        if witness is None:
            try:
                for left, right in strong_components(args.core, n):
                    witness = witness_on_component(left, right, args.fastest, target)
                    if witness is not None:
                        break
            except ComputationLimitError as e:
                report["witness_search_error"] = str(e)
        report["witness_from_strong_component"] = str(witness) if witness is not None else None
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
