"""Six-endpoint q=4 swap. Run directly to reproduce the motivating opened case."""
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from observatory.escape_trial.reentry_membership import classes_at, inspect, rescue


def swapped(weights):
    for q in (3, 5, 4):
        groups = classes_at(weights, q)
        for sign in (1, -1):
            time, _ = inspect(groups, q, sign)
            if time is not None:
                return q, sign, time
    return None


if __name__ == "__main__":
    weights = (59, 112, 540, 745)
    assert rescue(weights) is None
    assert swapped(weights) == (4, -1, Fraction(447, 1792))
    print(weights, swapped(weights))
