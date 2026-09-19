"""Exact interval feasibility and an independent piecewise-linear maximum.

All certification uses Fraction. There is no sampled-time search here.
Methods A and B share input validation and exact arithmetic, but Method B
does not call the interval-intersection algorithm to find its maximum.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import gcd, lcm
import re

Q = Fraction
Interval = tuple[Q, Q]
MAX_INTERVALS = 20_000
MAX_CROSSING_WORK = 2_000_000


class ComputationLimitError(ValueError):
    """The small reference implementation's work limit was exceeded."""


def rational(value) -> Q:
    """Accept integers, Fractions, or integer/fraction strings, never floats."""
    if isinstance(value, bool):
        raise ValueError("Use exact integers or fractions, not booleans.")
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r"[+-]?\d+(?:/[+-]?\d+)?", value.strip()):
        parts = value.strip().split("/")
        try:
            return Q(int(parts[0]), int(parts[1]) if len(parts) == 2 else 1)
        except ZeroDivisionError as exc:
            raise ValueError("A fraction denominator cannot be zero.") from exc
    raise ValueError("Use exact integers or fraction strings such as '3/2'; floats are rejected.")


@dataclass(frozen=True)
class Normalized:
    original: tuple[Q, ...]
    reference: int
    relative: tuple[Q, ...]
    denominator_lcm: int
    integer_gcd: int
    signed_integer_speeds: tuple[int, ...]
    speeds: tuple[int, ...]
    time_scale: Q  # original t = normalized tau * time_scale

    @property
    def n(self) -> int:
        return len(self.original)

    @property
    def threshold(self) -> Q:
        return Q(1, self.n)


def normalize(velocities, reference=0) -> Normalized:
    original = tuple(rational(v) for v in velocities)
    if len(original) < 2:
        raise ValueError("At least two runners are required.")
    if len(set(original)) != len(original):
        raise ValueError("Original velocities must be distinct.")
    if type(reference) is not int or not 0 <= reference < len(original):
        raise ValueError("Reference must be a zero-based runner index in range.")
    relative = tuple(v - original[reference] for i, v in enumerate(original) if i != reference)
    denominator = lcm(*(v.denominator for v in relative))
    integers = tuple(int(v * denominator) for v in relative)
    divisor = gcd(*integers)
    signed = tuple(v // divisor for v in integers)
    return Normalized(
        original, reference, relative, denominator, divisor, signed,
        tuple(sorted({abs(v) for v in signed})), Q(denominator, divisor),
    )


def _speeds(values) -> tuple[int, ...]:
    raw = tuple(values)
    if not raw or any(type(v) is not int or v <= 0 for v in raw):
        raise ValueError("Normalized constraint speeds must be positive integers.")
    return tuple(sorted(set(raw)))


def circular_distance(value) -> Q:
    """Distance to the nearest integer; signed positions are supported."""
    x = rational(value)
    phase = x % 1
    return min(phase, 1 - phase)


def _intersect(left: tuple[Interval, ...], right: tuple[Interval, ...]) -> tuple[Interval, ...]:
    """Intersect sorted disjoint closed intervals, preserving singleton points."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        start = max(left[i][0], right[j][0])
        end = min(left[i][1], right[j][1])
        if start <= end:
            result.append((start, end))
        if left[i][1] < right[j][1]:
            i += 1
        else:
            j += 1
    return tuple(result)


def feasible_intervals(speeds, threshold) -> tuple[Interval, ...]:
    """Method A: all allowed normalized times in [0, 1], including endpoints.

    Positive thresholds greater than 1/2 return the mathematically empty set.
    A work-limit exception is not an infeasibility certificate.
    """
    speeds = _speeds(speeds)
    delta = rational(threshold)
    if delta <= 0:
        raise ValueError("Threshold must be positive.")
    if delta > Q(1, 2):
        return ()
    if sum(speeds) > MAX_INTERVALS:
        raise ComputationLimitError("Interval work limit exceeded; use smaller normalized speeds.")
    allowed = ((Q(0), Q(1)),)
    for v in speeds:
        current = tuple(((Q(j) + delta) / v, (Q(j + 1) - delta) / v) for j in range(v))
        allowed = _intersect(allowed, current)
        if not allowed:
            break
    return allowed


@dataclass(frozen=True)
class Maximum:
    value: Q
    times: tuple[Q, ...]
    candidate_count: int


def exact_maximum(speeds) -> Maximum:
    """Method B: inspect all corners and pairwise affine crossings exactly.

    Each distance curve is affine between m/(2v) corners. Its lower envelope
    can change slope only at corners or crossings, so this candidate set is
    complete. Every affine piece has nonzero slope; there are no flat maxima.
    This naive method is intentionally limited to small cases.
    """
    speeds = _speeds(speeds)
    k = len(speeds)
    work_bound = 2 * sum(speeds) * (1 + k * (k - 1) // 2)
    if sum(speeds) > MAX_INTERVALS or work_bound > MAX_CROSSING_WORK:
        raise ComputationLimitError("Maximum work limit exceeded; use --feasibility-only or smaller speeds.")
    corners = sorted({Q(m, 2 * v) for v in speeds for m in range(2 * v + 1)})
    candidates = set(corners)
    for left, right in zip(corners, corners[1:]):
        middle = (left + right) / 2
        lines = []
        for v in speeds:
            position = v * middle
            whole = position.numerator // position.denominator
            if position - whole < Q(1, 2):
                lines.append((v, Q(-whole)))
            else:
                lines.append((-v, Q(whole + 1)))
        for (slope_a, intercept_a), (slope_b, intercept_b) in combinations(lines, 2):
            if slope_a != slope_b:
                crossing = (intercept_b - intercept_a) / (slope_a - slope_b)
                if left < crossing < right:
                    candidates.add(crossing)
    best = Q(-1)
    times = []
    for t in sorted(candidates):
        # Directly evaluate distances, independent of the affine construction.
        value = min(circular_distance(v * t) for v in speeds)
        if value > best:
            best, times = value, [t]
        elif value == best:
            times.append(t)
    return Maximum(best, tuple(times), len(candidates))


def _interval_strings(intervals, scale=Q(1)):
    return [[str(a * scale), str(b * scale)] for a, b in intervals]


def check(velocities, reference=0, *, threshold=None, compute_maximum=True) -> dict:
    """Check one runner. JSON-ready output stores every rational as a string.

    All original-time intervals cover one period of this reference runner's
    *relative distances*. Absolute track positions need not repeat then.
    """
    config = normalize(velocities, reference)
    delta = config.threshold if threshold is None else rational(threshold)
    allowed = feasible_intervals(config.speeds, delta)
    result = {
        "velocities": [str(v) for v in config.original],
        "reference_index": reference,
        "reference_velocity": str(config.original[reference]),
        "n": config.n,
        "conjecture_threshold": str(config.threshold),
        "threshold": str(delta),
        "normalization": {
            "relative_velocities": [str(v) for v in config.relative],
            "denominator_lcm": config.denominator_lcm,
            "integer_gcd": config.integer_gcd,
            "signed_integer_speeds": list(config.signed_integer_speeds),
            "constraint_speeds": list(config.speeds),
            "original_time_per_normalized_unit": str(config.time_scale),
        },
        "period_original": str(config.time_scale),
        "feasible": bool(allowed),
        "intervals_normalized": _interval_strings(allowed),
        "intervals_original": _interval_strings(allowed, config.time_scale),
        "witness_original": str(allowed[0][0] * config.time_scale) if allowed else None,
        "maximum": None,
    }
    if compute_maximum:
        maximum = exact_maximum(config.speeds)
        peak_intervals = feasible_intervals(config.speeds, maximum.value)
        expected_peaks = tuple((t, t) for t in maximum.times)
        # This checks all maximizers, not just one passing witness.
        if peak_intervals != expected_peaks or bool(allowed) != (maximum.value >= delta):
            raise ArithmeticError("Independent methods disagree; no checked result is returned.")
        details = []
        for tau in maximum.times:
            t = tau * config.time_scale
            distances = [
                {"runner_index": i, "distance": str(circular_distance((v - config.original[reference]) * t))}
                for i, v in enumerate(config.original) if i != reference
            ]
            details.append({
                "time_original": str(t),
                "distances": distances,
                "limiting_runner_indices": [d["runner_index"] for d in distances if Q(d["distance"]) == maximum.value],
            })
        result["maximum"] = {
            "separation": str(maximum.value),
            "excess_over_conjecture_threshold": str(maximum.value - config.threshold),
            "tight": maximum.value == config.threshold,
            "times_normalized": [str(t) for t in maximum.times],
            "times_original": [str(t * config.time_scale) for t in maximum.times],
            "witness_details": details,
            "candidate_count": maximum.candidate_count,
            "crosschecked_with_intervals": True,
        }
    return result
