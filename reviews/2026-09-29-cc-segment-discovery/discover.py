"""Parent-only floor-edge discovery, fixed by PROTOCOL.md before execution.

Standard-library exact arithmetic. The only mathematical input file contains
six-form parents; no old selector, seven-form cells or optimum data are read.
"""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "PARENT_INPUT.json"
ADDED_ROW = (5, 2)


def ceil(x):
    return -((-x.numerator) // x.denominator)


def floor(x):
    return x.numerator // x.denominator


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def interpolate(a, b, t):
    return tuple(x + t * (y - x) for x, y in zip(a, b))


def phase(p, row):
    return sum(x * y for x, y in zip(p, row))


def candidates(data):
    z = F(data["threshold"])
    records, edge_count, lap_count = [], 0, 0
    for parent_index, parent in enumerate(data["parents"]):
        vertices = [tuple(map(F, v)) for v in parent["vertices"]]
        for i, j in sorted(parent["edges"]):
            if vertices[i][2] != z or vertices[j][2] != z:
                continue
            edge_count += 1
            a, b = vertices[i][:2], vertices[j][:2]
            sa, sb = phase(a, ADDED_ROW), phase(b, ADDED_ROW)
            ds = sb - sa
            # Exactly the laps whose closed phase band meets the edge range.
            k_min, k_max = ceil(min(sa, sb) - (1 - z)), floor(max(sa, sb) - z)
            for k in range(k_min, k_max + 1):
                lap_count += 1
                if ds:
                    u, v = sorted(((k + z - sa) / ds, (k + 1 - z - sa) / ds))
                    lo, hi = max(F(0), u), min(F(1), v)
                    if lo > hi:
                        continue
                elif k + z <= sa <= k + 1 - z:
                    lo, hi = F(0), F(1)
                else:
                    continue
                endpoints = sorted((interpolate(a, b, lo), interpolate(a, b, hi)))
                p, r = endpoints
                dx, dy = r[0] - p[0], r[1] - p[1]
                cutoff = max(2, ceil((1 + dy) / dx)) if dx > 0 else None
                records.append({"id": f"P{parent_index}:E{i}-{j}:K{k}",
                                "parent": parent_index, "edge": (i, j), "seventh_lap": k,
                                "labels": tuple(parent["labels"]) + (k,),
                                "endpoints": endpoints, "source_parameters": (lo, hi),
                                "dx": dx, "dy": dy, "tail_cutoff": cutoff})
    return records, {"floor_edges": edge_count, "edge_lap_pairs": lap_count}


def select_on(segment, q):
    p, r = segment["endpoints"]
    hp, hr = q * p[0] - p[1], q * r[0] - r[1]
    low, high = sorted((hp, hr))
    h = ceil(low)
    if h > high:
        return None
    parameter = F(0) if hp == hr else (h - hp) / (hr - hp)
    assert 0 <= parameter <= 1
    point = interpolate(p, r, parameter)
    return {"q": q, "segment": segment["id"], "h": h, "interval": (low, high),
            "parameter": parameter, "point": point, "time": point[0]}


def build_cover(records):
    eligible = [s for s in records if s["tail_cutoff"] is not None]
    if not eligible:
        return {"status": "NO CERTIFICATE: no nonvertical candidate"}
    # records already have the declared canonical provenance order.
    tail = min(eligible, key=lambda s: s["tail_cutoff"])
    cutoff = tail["tail_cutoff"]
    if cutoff > 26:
        return {"status": "SCOPE LIMIT", "tail": tail["id"], "cutoff": cutoff}
    prefix = list(range(2, cutoff))
    coverage = {s["id"]: [q for q in prefix if select_on(s, q) is not None] for s in records}
    chosen = [tail]
    uncovered = set(prefix) - set(coverage[tail["id"]])
    steps = []
    while uncovered:
        best = max(records, key=lambda s: len(uncovered.intersection(coverage[s["id"]])))
        covered = sorted(uncovered.intersection(coverage[best["id"]]))
        if not covered:
            return {"status": "NO CERTIFICATE: uncovered prefix", "uncovered": sorted(uncovered)}
        steps.append({"before": sorted(uncovered), "chosen": best["id"], "newly_covered": covered})
        chosen.append(best)
        uncovered.difference_update(covered)
    return {"status": "COMPLETE COVER CERTIFICATE", "tail": tail["id"], "cutoff": cutoff,
            "prefix": prefix, "coverage": coverage, "greedy_steps": steps,
            "chosen_ids": [s["id"] for s in chosen], "chosen_segments": chosen}


def witness(cover, q, rows):
    for attempt, segment in enumerate(cover["chosen_segments"], start=1):
        cert = select_on(segment, q)
        if cert is not None:
            cert["attempts"] = attempt
            cert["physical_laps"] = [m + b * cert["h"] for m, (_, b) in zip(segment["labels"], rows)]
            return cert
    raise ArithmeticError("input not covered")


def main():
    data = json.loads(INPUT.read_text())
    records, counts = candidates(data)
    rows = tuple(map(tuple, data["rows"])) + (ADDED_ROW,)
    z = F(data["threshold"])
    for s in records:
        for p in s["endpoints"]:
            assert z <= p[0] <= F(1, 2) and z <= p[1] <= 1-z
            assert all(z <= phase(p, row) - m <= 1-z for row, m in zip(rows, s["labels"]))
        if s["tail_cutoff"] is not None:
            assert s["tail_cutoff"] * s["dx"] - s["dy"] >= 1
    cover = build_cover(records)
    controls = []
    if cover["status"] == "COMPLETE COVER CERTIFICATE":
        for q in range(2, 26):
            cert = witness(cover, q, rows)
            speeds = [a+b*q for a, b in rows]
            time_checks = []
            for t in (cert["time"], 1-cert["time"]):
                positions = [v*t for v in speeds]
                laps = [floor(p) for p in positions]
                phases = [p-ell for p, ell in zip(positions, laps)]
                distances = [min(f, 1-f) for f in phases]
                assert min(distances) >= z
                time_checks.append({"time": t, "laps": laps, "phases": phases,
                                    "minimum": min(distances)})
            assert time_checks[0]["laps"] == cert["physical_laps"]
            assert time_checks[1]["laps"] == [v-1-ell for v, ell in zip(speeds, cert["physical_laps"])]
            controls.append({"certificate": cert, "physical": time_checks})
    out = {"status": cover["status"], "authorship": "coordinator; proof candidate, no independent review",
           "source_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
           "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "added_row": ADDED_ROW, "candidates": records, "cover": cover, "physical_controls": controls,
           "summary": {**counts, "candidate_records": len(records),
                       "point_records": sum(s["endpoints"][0] == s["endpoints"][1] for s in records),
                       "nonvertical_records": sum(s["dx"] > 0 for s in records),
                       "chosen_count": len(cover.get("chosen_ids", [])),
                       "cutoff": cover.get("cutoff"), "physical_q_count": len(controls),
                       "new_physical_q_values": 0}}
    print(json.dumps(encode(out), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
