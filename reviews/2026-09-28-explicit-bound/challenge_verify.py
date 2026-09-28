#!/usr/bin/env python3
"""Independent exact piecewise-polynomial check of the frozen convolution fixtures.

No primary implementation is imported. The finite domain is protocol.json:
9 fixtures, 144 per-train convolution values, and 81 kernel sample values.
"""
from bisect import bisect_right
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
EXPECTED_PROTOCOL_SHA = "63d509f00dd73cfc54094030ed942d0e929215213a5e20604305dc4e99192d06"


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def value(p, x):
    ans = F(0)
    for c in reversed(p):
        ans = ans * x + c
    return ans


def shifted(p, delta):
    """Coefficients of p(x+delta), expanded by the binomial theorem."""
    out = [F(0)] * len(p)
    for k, c in enumerate(p):
        for j in range(k + 1):
            out[j] += c * comb(k, j) * delta ** (k-j)
    return trim(out)


def subtract(p, q, divisor):
    out = [F(0)] * max(len(p), len(q))
    for k, c in enumerate(p):
        out[k] += c
    for k, c in enumerate(q):
        out[k] -= c
    return trim(c / divisor for c in out)


class Piecewise:
    """Polynomial pieces on the real line, with rational breakpoints."""

    def __init__(self, breaks, cells):
        assert len(cells) == len(breaks) + 1
        self.breaks, self.cells = [], [trim(cells[0])]
        for b, p in zip(breaks, cells[1:]):
            p = trim(p)
            if p != self.cells[-1]:
                self.breaks.append(b)
                self.cells.append(p)

    def coefficients_at(self, x):
        return self.cells[bisect_right(self.breaks, x)]

    def at(self, x):
        return value(self.coefficients_at(x), x)

    def antiderivative(self):
        assert self.cells[0] == (F(0),), "Only compact left support is used"
        pieces = [(F(0),)]
        previous = pieces[0]
        for b, p in zip(self.breaks, self.cells[1:]):
            integrated = [F(0)] + [c / (k+1) for k, c in enumerate(p)]
            integrated[0] = value(previous, b) - value(integrated, b)
            previous = trim(integrated)
            pieces.append(previous)
        return Piecewise(self.breaks, pieces)

    def box_convolution(self, period):
        """U_period*f = (F(x)-F(x-period))/period, F'=f."""
        primitive = self.antiderivative()
        breaks = sorted(set(primitive.breaks +
                            [b + period for b in primitive.breaks]))
        samples = [breaks[0] - 1]
        samples += [(a+b)/2 for a, b in zip(breaks, breaks[1:])]
        samples += [breaks[-1] + 1]
        cells = []
        for x in samples:
            first = primitive.coefficients_at(x)
            second = shifted(primitive.coefficients_at(x-period), -period)
            cells.append(subtract(first, second, period))
        return Piecewise(breaks, cells)


def periodic_indicator(period, start, left, right):
    """The exact periodic train cropped to the declared needed input window."""
    events = {left: 0, right: 0}
    first = (left-start) // period - 2
    last = (right-start) // period + 2
    for m in range(first, last+1):
        l = max(left, start+m*period)
        r = min(right, start+(F(m)+F(1, 4))*period)
        if l < r:
            events[l] = events.get(l, 0) + 1
            events[r] = events.get(r, 0) - 1
    breaks = sorted(events)
    count = 0
    cells = [(F(0),)]
    for b in breaks:
        count += events[b]
        cells.append((F(count),))
    assert count == 0
    return Piecewise(breaks, cells)


def run():
    protocol_bytes = (HERE / "protocol.json").read_bytes()
    protocol_sha = sha256(protocol_bytes).hexdigest()
    assert protocol_sha == EXPECTED_PROTOCOL_SHA
    protocol = json.loads(protocol_bytes)
    records = []
    indicator_count = total_count = kernel_interior_count = kernel_endpoint_count = 0
    for template in protocol["tiles"]:
        for perturbation in protocol["perturbations"]:
            periods = [F(p) for p in template["periods"]]
            starts = [F(s) for s in template["starts"]]
            if perturbation["field"] is not None:
                target = periods if perturbation["field"] == "periods" else starts
                target[perturbation["runner"]] += F(perturbation["delta"])
            S = sum(periods, F(0))
            xs = [F(0), F(1, 7), S, S + F(1, 7)]
            # Every value uses only [x-S,x], safely inside this crop.
            crop_left, crop_right = min(xs)-S-1, max(xs)+1
            per_train = []
            piece_counts = []
            for period, start in zip(periods, starts):
                function = periodic_indicator(period, start, crop_left, crop_right)
                for averaging_period in periods:
                    function = function.box_convolution(averaging_period)
                values = [function.at(x) for x in xs]
                assert all(v == F(1, 4) for v in values)
                indicator_count += len(values)
                per_train.append(values)
                piece_counts.append(len(function.cells))

            kernel = Piecewise([F(0), periods[0]],
                               [(F(0),), (1/periods[0],), (F(0),)])
            for period in periods[1:]:
                kernel = kernel.box_convolution(period)
            kernel_records = []
            for j in protocol["kernel_samples"]["interior_j"]:
                argument = S*F(j, 8)
                result = kernel.at(argument)
                assert result > 0
                kernel_interior_count += 1
                kernel_records.append({"kind": "interior", "j": j,
                                       "argument": str(argument), "value": str(result)})
            for argument in [F(0), S]:
                result = kernel.at(argument)
                assert result == 0
                kernel_endpoint_count += 1
                kernel_records.append({"kind": "endpoint", "argument": str(argument),
                                       "value": str(result)})
            kernel_mass = kernel.antiderivative().cells[-1]
            assert kernel_mass == (F(1),)

            samples = []
            for position, x in enumerate(xs):
                label_values = [values[position] for values in per_train]
                total = sum(label_values, F(0))
                assert total == 1
                total_count += 1
                samples.append({"x": str(x), "trains": [str(v) for v in label_values],
                                "total": str(total)})
            records.append({"id": template["id"]+":"+perturbation["id"],
                            "periods": [str(p) for p in periods],
                            "starts": [str(s) for s in starts], "S": str(S),
                            "samples": samples, "kernel_samples": kernel_records,
                            "kernel_mass": str(kernel_mass[0]),
                            "final_piece_counts": piece_counts})
    counts = {"fixtures": len(records), "per_train_integrals": indicator_count,
              "totals": total_count, "kernel_interior": kernel_interior_count,
              "kernel_endpoints": kernel_endpoint_count}
    assert counts == {"fixtures": 9, "per_train_integrals": 144, "totals": 36,
                      "kernel_interior": 63, "kernel_endpoints": 18}
    output = {"protocol_sha256": protocol_sha, "status": "all exact checks passed",
              "method": "rational piecewise-polynomial integration; four box-convolution antiderivative differences; no alternating-subset formula and no primary import",
              "counts": counts, "fixtures": records}
    (HERE / "challenge_verification.json").write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"status": output["status"], "counts": counts}, sort_keys=True))


if __name__ == "__main__":
    run()
