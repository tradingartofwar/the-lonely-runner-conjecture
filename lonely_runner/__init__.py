"""Small exact-rational tools for the common-start Lonely Runner problem."""

from .checker import (
    ComputationLimitError,
    check,
    circular_distance,
    exact_maximum,
    feasible_intervals,
    normalize,
)

__all__ = [
    "ComputationLimitError", "check", "circular_distance", "exact_maximum",
    "feasible_intervals", "normalize",
]
