"""Frozen ordinary-lineup sampler and paired timing harness."""

import argparse
import hashlib
import json
import math
import os
import platform
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from time import perf_counter_ns, process_time_ns

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))

from observatory.escape_trial.adaptive_anchor.choose import adaptive
from observatory.escape_trial.adaptive_anchor.sample import exclusions, prior
from observatory.escape_trial.continuation_check import physical
from observatory.escape_trial.last_anchor.arms import first_issue
from observatory.escape_trial.rule import predict

RAW_PER_BAND = 65_536
DOMAIN = "ordinary-adoption-v1"
KINDS = ("fixed4", "adaptive")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def fingerprint(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def panel_rows(seed):
    seen = exclusions()
    older = json.loads((HERE.parent / "adaptive_anchor/panel.json").read_bytes())
    seen.update(tuple(w) for cell in older["cells"] for w in cell["rows"])
    manifest = {"seed_hex": seed.hex(), "raw_per_band": RAW_PER_BAND, "opened_exclusions": len(seen), "cells": []}
    bands = []
    for band in prior.SCALES:
        rng = prior.stream(seed, DOMAIN, band)
        rows = []
        nonprimitive = excluded = 0
        for _ in range(RAW_PER_BAND):
            weights = prior.draw_weights(rng, band, "stretch_middle")
            if math.gcd(*weights) != 1:
                nonprimitive += 1
            elif weights in seen:
                excluded += 1
            else:
                rows.append(weights)
        manifest["cells"].append(dict(band=list(band), ordinary=len(rows), nonprimitive=nonprimitive,
                                      opened_excluded=excluded, repeats=len(rows)-len(set(rows)),
                                      ordered_rows_sha256=fingerprint(rows)))
        bands.append(rows)
    return manifest, bands


def regen(seed):
    if len(seed) != 32 or hashlib.sha256(seed).hexdigest() != (HERE / "seed.sha256").read_text().strip():
        raise ValueError("Seed does not match the separate commitment")
    return panel_rows(seed)


def load_panel():
    raw = (HERE / "panel.json").read_bytes()
    manifest, bands = regen(bytes.fromhex(json.loads(raw)["seed_hex"]))
    if raw != encoded(manifest):
        raise ValueError("Regenerated inputs differ from the sealed manifest")
    return hashlib.sha256(raw).hexdigest(), bands


def prefix(weights):
    first = predict(weights)
    if first is not None:
        return first["time"]
    for q in (3, 5):
        issued = first_issue(weights, q)
        if issued is not None:
            return issued[1]
    return None


def fixed_final(weights):
    issued = first_issue(weights, 4)
    return (4, issued[1] if issued else None)


def adaptive_final(weights):
    q, _sign, time, _probes, _attempts = adaptive(weights)
    return (q, time)


def full_policy(weights, final):
    time = prefix(weights)
    if time is not None:
        return time
    return final(weights)[1]


def modular_clearance(speeds, time):
    if time is None:
        return None
    q = time.denominator
    return min(min(r, q-r) for r in ((v*time.numerator) % q for v in speeds)), q


def safe_clearance(clearance):
    return clearance is not None and 16*clearance[0] >= clearance[1]


def paired_record(weights, issued, final_q, speeds, check):
    times = [check(speeds, t) for t in issued]
    # A canonical record stores exact distances as reduced rational strings.
    return dict(weights=weights, final_q=final_q, times=[str(t) if t is not None else None for t in issued],
                minima=[str(Fraction(*c)) if c is not None else None for c in times],
                safe=[safe_clearance(c) for c in times])


def summarize(bands, compare):
    cells = []
    total = Counter()
    final_rows = []
    for scale, weights_in_band in zip(prior.SCALES, bands, strict=True):
        counts = Counter({key: 0 for key in ("ordinary", "eligible", "switches", "fixed4_safe", "adaptive_safe",
                                             "gains", "losses", "unsafe_fixed4", "unsafe_adaptive", "both_abstain")})
        all_pairs = hashlib.sha256()
        for weights in weights_in_band:
            pair = compare(weights)
            all_pairs.update(encoded(pair))
            fixed, candidate = pair["safe"]
            a, b = pair["times"]
            counts.update(ordinary=1, eligible=pair["final_q"] is not None, switches=pair["final_q"] == 7,
                          fixed4_safe=fixed, adaptive_safe=candidate, gains=candidate and not fixed,
                          losses=fixed and not candidate, unsafe_fixed4=a is not None and not fixed,
                          unsafe_adaptive=b is not None and not candidate, both_abstain=a is None and b is None)
            if pair["final_q"] is not None:
                final_rows.append(pair)
        cells.append(dict(band=list(scale), counts=dict(counts), ordered_pairs_sha256=all_pairs.hexdigest()))
        total.update(counts)
    return dict(cells=cells, total=dict(total), eligible=final_rows)


def compare(weights):
    t = prefix(weights)
    speeds = physical(weights)
    if t is not None:
        return paired_record(weights, (t, t), None, speeds, modular_clearance)
    q, alternate = adaptive_final(weights)
    return paired_record(weights, (fixed_final(weights)[1], alternate), q, speeds, modular_clearance)


def clock_batch(rows, final, repeat, whole):
    call = (lambda weights: full_policy(weights, final)) if whole else final
    wall = perf_counter_ns()
    cpu = process_time_ns()
    for _ in range(repeat):
        for weights in rows:
            call(weights)
    cpu_used = process_time_ns() - cpu
    return {"wall_ns": perf_counter_ns()-wall, "cpu_ns": cpu_used}


def benchmark(bands, eligible):
    cpus = os.sched_getaffinity(0)
    pinned = min(cpus)
    os.sched_setaffinity(0, {pinned})
    try:
        arms = {"fixed4":fixed_final, "adaptive":adaptive_final}
        ordinary = [w for band in bands for w in band]
        modes = benchmark_modes(ordinary, eligible, arms)
    finally:
        os.sched_setaffinity(0, cpus)
    return dict(python=platform.python_version(), os=platform.system(), architecture=platform.machine(),
                processor=pinned, modes=modes)


def benchmark_modes(ordinary, eligible, arms):
    def trial(rows, reps, whole, order):
        return {arm: clock_batch(rows, arms[arm], reps, whole) for arm in order}

    for f in arms.values():
        for w in ordinary[:2048]:
            full_policy(w, f)
        for w in eligible:
            f(w)
    records = []
    for round_id in range(3):
        for start in range(0, len(ordinary), 4096):
            rows = ordinary[start:start+4096]
            order = KINDS if (round_id + start//4096)%2 == 0 else KINDS[::-1]
            records.append(dict(round=round_id, start=start, rows=len(rows), order=order,
                                **trial(rows, 1, True, order)))
    final = []
    if eligible:
        for i in range(9):
            order = KINDS if i%2 == 0 else KINDS[::-1]
            final.append(dict(round=i, rows=len(eligible), repetitions=32, order=order,
                              **trial(eligible, 32, False, order)))
    return {"ordinary": records, "eligible": final}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("seal", "score", "time"))
    parser.add_argument("--seed-file", type=Path)
    args = parser.parse_args()
    if args.stage == "seal":
        manifest, _ = regen(args.seed_file.read_bytes())
        sys.stdout.buffer.write(encoded(manifest))
        return
    panel_hash, bands = load_panel()
    results = dict(panel_sha256=panel_hash, **summarize(bands, compare)) if args.stage == "score" else None
    if args.stage == "time":
        result = json.loads((HERE / "results.json").read_bytes())
        if result["panel_sha256"] != panel_hash:
            raise ValueError("Score belongs to another panel")
        eligible = [tuple(row["weights"]) for row in result["eligible"]]
        results = dict(panel_sha256=panel_hash, **benchmark(bands, eligible))
    sys.stdout.buffer.write(encoded(results))


if __name__ == "__main__":
    main()
