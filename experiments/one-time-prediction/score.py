"""Replay the frozen rule and score every prediction after it has been generated.

From the repo root run PYTHONPATH=. python experiments/one-time-prediction/score.py PANEL.json
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import sys

from lonely_runner.checker import feasible_intervals
from predictor import choose_time


def clearance(speeds, t):
    p, q = t.as_integer_ratio()
    return Fraction(min(min(p*v % q, -p*v % q) for v in speeds), q)


def main():
    data = Path(sys.argv[1]).read_bytes()
    assert sha256(data).hexdigest() == "252b6097cb35188e0fc16de321b64aaa172714390f0dc64b9660c97ac438a167"
    panel = json.loads(data)
    predictions = [choose_time(row["speeds"]) for row in panel]
    threshold = Fraction(1, 16)
    grid = [Fraction(a, q) for q in range(2, 33)
            for a in range(1, q // 2 + 1) if gcd(a, q) == 1]
    counts = defaultdict(Counter)
    wins = []
    for i, (row, (q, prediction, forward)) in enumerate(zip(panel, predictions)):
        speeds = row["speeds"]
        anchor = Fraction(1, q)
        anchored = clearance(speeds, anchor) >= threshold
        predicted = clearance(speeds, prediction) >= threshold
        forward_ok = clearance(speeds, forward) >= threshold
        grid_ok = any(clearance(speeds, t) >= threshold for t in grid)
        exact = bool(feasible_intervals(speeds, threshold))
        assert exact or not (anchored or predicted or forward_ok or grid_ok)
        for bucket in (row["bucket"], "total"):
            counts[bucket].update(dict(trials=1, anchor=anchored, shifted=(prediction != anchor),
                                       predicted=predicted, forward=forward_ok, prediction_only=predicted and not forward_ok,
                                       forward_only=forward_ok and not predicted, grid=grid_ok,
                                       beats_grid=predicted and not grid_ok, exact=exact))
        if predicted and (not forward_ok or not grid_ok):
            wins.append((i, speeds, anchor, prediction, clearance(speeds, prediction), forward_ok, grid_ok))
    for bucket, row in counts.items():
        print(bucket, dict(row))
    print("Cases where direction or the larger grid mattered:", wins)


if __name__ == "__main__":
    main()

