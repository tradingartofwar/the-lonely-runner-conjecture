"""Independently verify the fixed-family certificate using only the Python standard library."""
import csv
import json
from fractions import Fraction as Q
from math import ceil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXED = (0, 11, 13, 16, 17, 20, 28, 38, 39, 42, 43, 52, 56, 60, 63, 70)
DELTA = Q(1, 17)


def check_time(reference, speeds, t, clearance):
    for speed in speeds:
        if speed != reference:
            phase = ((speed - reference) * t) % 1
            assert clearance <= phase <= 1 - clearance, (reference, speed, t)


def verify():
    cert = json.loads((ROOT / "seventeen_family_results.json").read_text())
    assert tuple(cert["fixed"]) == FIXED
    assert [row["reference"] for row in cert["core_certificates"]] == list(FIXED)
    m = max(FIXED)
    direct_tail = max(m+1, ceil(Q(16*m, 15)))
    for row in cert["core_certificates"]:
        r = row["reference"]
        a, b = map(Q, row["strong_component"])
        strong_time = Q(row["strong_time"])
        assert 0 <= a < strong_time < b <= 1
        check_time(r, FIXED, strong_time, Q(1, 16))
        for u in {abs(s-r) for s in FIXED if s != r}:
            lap = (u*a) // 1
            assert lap + DELTA <= u*a <= u*b <= lap + 1 - DELTA
        direct_tail = max(direct_tail, r + ceil(2 * DELTA / (b-a)))
    # For V >= direct_tail every stored interval is too wide for one open
    # blocking pass of V-r. The added runner uses t=1/(2V-m).
    assert direct_tail <= cert["tail_from"]
    expected = [v for v in range(1, cert["tail_from"]) if v not in FIXED]
    with (ROOT / "seventeen_family_witnesses.csv").open(newline="") as file:
        reader = csv.reader(file)
        assert next(reader) == ["added_speed", *(f"reference_{s}" for s in FIXED), "reference_added"]
        seen = []
        for entry in reader:
            v = int(entry[0])
            speeds = (*FIXED, v)
            times = tuple(map(Q, entry[1:]))
            assert len(times) == len(speeds)
            for r, t in zip(speeds, times):
                check_time(r, speeds, t, DELTA)
            seen.append(v)
    assert seen == expected
    assert len(seen) == cert["finite_additions"]
    assert 17*len(seen) == cert["finite_verified_roles"]
    print(f"All 17 references verified for {len(seen)} finite additions.")
    print(f"The stored interval widths cover every added integer V >= {direct_tail}.")


if __name__ == "__main__":
    verify()
