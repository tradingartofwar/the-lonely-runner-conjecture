#!/usr/bin/env python3
"""Independent contact-event verifier. No primary source/output imports.

Reconstruct core and final safe sets by direct predicates on rational time
thresholds and open time cells. Reconstruct speed bands from independently
generated endpoint-contact events and open speed cells.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "PROTOCOL.json"
EXPECTED_PROTOCOL = "660a3a7f27f6a1e7b2c0c68aeea22b42366c7a946d5612e967c6f355999d5aae"
EPS = Q(1, 8)
COUNTS = {"core_time_events": 0, "core_time_cells": 0,
          "speed_events_evaluated": 0, "speed_cells_evaluated": 0,
          "final_time_events": 0, "final_time_cells": 0,
          "diagnostic_reconstructions": 0}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -floor(-x)


def dist(x):
    x -= floor(x)
    return min(x, 1 - x)


def merge_closed(pieces):
    ans = []
    for lo, hi in sorted(pieces):
        if ans and lo <= ans[-1][1]:
            ans[-1] = (ans[-1][0], max(ans[-1][1], hi))
        else:
            ans.append((lo, hi))
    return ans


def threshold_events(v, phase=Q(0)):
    ans = set()
    # Deliberately generate a safe superset of integer laps and filter in t.
    for m in range(floor(phase) - 2, ceil(v + phase) + 3):
        for sign in (-1, 1):
            t = (Q(m) + sign * EPS - phase) / v
            if 0 <= t <= 1:
                ans.add(t)
    return ans


def reconstruct_time(speeds, d=None, phase=Q(0), count_kind="final"):
    events = {Q(0), Q(1)}
    for v in speeds:
        events.update(threshold_events(Q(v)))
    if d is not None:
        events.update(threshold_events(d, phase))
    events = sorted(events)

    def safe(t):
        return all(dist(Q(v) * t) >= EPS for v in speeds) and (
            d is None or dist(d * t + phase) >= EPS)

    pieces = [(t, t) for t in events if safe(t)]
    for l, r in zip(events, events[1:]):
        if safe((l + r) / 2):
            # All safe predicates are closed; a safe open cell has safe ends.
            assert safe(l) and safe(r)
            pieces.append((l, r))
    if count_kind == "core":
        COUNTS["core_time_events"] += len(events)
        COUNTS["core_time_cells"] += len(events) - 1
    else:
        COUNTS["final_time_events"] += len(events)
        COUNTS["final_time_cells"] += len(events) - 1
    return merge_closed(pieces)


def string_components(components):
    return [[str(l), str(r)] for l, r in components]


def component_summary(components):
    return {"components": string_components(components),
            "positive_components": string_components([(l, r) for l, r in components if l < r]),
            "singletons": [str(l) for l, r in components if l == r],
            "safe_measure": str(sum((r-l for l, r in components), Q(0)))}


def intersects(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def positive_intersection(a, b):
    return max(a[0], b[0]) < min(a[1], b[1])


def normalize_atoms(atoms):
    """Merge adjacent true speed cells iff their shared contact is included."""
    merged = []
    for l, r, lc, rc in sorted(atoms, key=lambda x: (x[0], x[1], not x[2], not x[3])):
        if merged and (l < merged[-1][1] or (
                l == merged[-1][1] and (merged[-1][3] or lc))):
            pl, pr, plc, prc = merged[-1]
            if r > pr:
                merged[-1] = (pl, r, plc, rc)
            elif r == pr:
                merged[-1] = (pl, pr, plc, prc or rc)
        else:
            merged.append((l, r, lc, rc))
    return [{"lower": str(l), "upper": str(r), "left_closed": lc,
             "right_closed": rc} for l, r, lc, rc in merged]


def integer_members(bands):
    ans = set()
    for b in bands:
        lo, hi = Q(b["lower"]), Q(b["upper"])
        a, z = ceil(lo), floor(hi)
        if not b["left_closed"] and Q(a) == lo:
            a += 1
        if not b["right_closed"] and Q(z) == hi:
            z -= 1
        ans.update(range(a, z + 1))
    return sorted(ans)


def phase_record(speeds, core, c, U, theta):
    mode_indices = {"F": list(range(len(core))),
                    "P": [i for i, (l, r) in enumerate(core) if l < r],
                    "Z": [i for i, (l, r) in enumerate(core) if l < r]}
    contacts = {c, U} if U > c else set()
    if U > c:
        for s in {t for comp in core for t in comp}:
            assert s > 0
            for m in range(floor(c*s+theta) - 2, ceil(U*s+theta) + 3):
                for sign in (-1, 1):
                    d = (Q(m) + sign * EPS - theta) / s
                    if c <= d <= U:
                        contacts.add(d)
    contacts = sorted(contacts)
    atoms = []
    for d in contacts:
        if d > c:
            atoms.append((d, d, True, True, d, "event"))
    for l, r in zip(contacts, contacts[1:]):
        atoms.append((l, r, False, False, (l+r)/2, "cell"))
    atoms.sort(key=lambda a: (a[0], a[1]))
    collected = {mode: {"full": [], "components": {i: [] for i in ids},
                        "prefix": {i: [] for i in ids}}
                 for mode, ids in mode_indices.items()}
    for l, r, lc, rc, sample, kind in atoms:
        safe_set = reconstruct_time(speeds, sample, theta)
        COUNTS["speed_events_evaluated" if kind == "event" else "speed_cells_evaluated"] += 1
        atom = (l, r, lc, rc)
        strict = {i: not any(intersects(core[i], s) for s in safe_set)
                  for i in range(len(core))}
        zero_duration = {i: not any(positive_intersection(core[i], s) for s in safe_set)
                         for i in range(len(core))}
        for mode, ids in mode_indices.items():
            truths = zero_duration if mode == "Z" else strict
            cumulative = True
            for i in ids:
                if truths[i]:
                    collected[mode]["components"][i].append(atom)
                cumulative = cumulative and truths[i]
                if cumulative:
                    collected[mode]["prefix"][i].append(atom)
            if cumulative:
                collected[mode]["full"].append(atom)
    modes = {}
    for mode, ids in mode_indices.items():
        bands = normalize_atoms(collected[mode]["full"])
        modes[mode] = {"bands": bands, "integers": integer_members(bands),
                       "component_bands": [{"component_index": i,
                         "bands": normalize_atoms(collected[mode]["components"][i])}
                                           for i in ids],
                       "prefix_bands": [{"component_index": i,
                         "bands": normalize_atoms(collected[mode]["prefix"][i])}
                                        for i in ids]}
    return {"phase": str(theta), "modes": modes}, {"phase": str(theta),
            "parameter_contact_count": len(contacts), "atom_count": len(atoms)}


def main():
    assert sha(PROTOCOL) == EXPECTED_PROTOCOL
    protocol = json.loads(PROTOCOL.read_text())
    records, event_counts = [], []
    for declared in protocol["cores"]:
        speeds = declared["speeds"]
        core = reconstruct_time(speeds, count_kind="core")
        widths = [r-l for l, r in core]
        w = max(widths)
        assert w > 0
        U, c = 1/(4*w), Q(max(speeds))
        record = {"id": declared["id"], "speeds": speeds,
                  **component_summary(core), "width": str(w),
                  "widest_ties": string_components([comp for comp in core if comp[1]-comp[0] == w]),
                  "cap_U": str(U),
                  "domain": {"lower": str(c), "upper": str(U),
                             "left_closed": False, "right_closed": True} if U > c else None,
                  "endpoint_slack_caps": []}
        for i, (l, r) in enumerate(core):
            if l < r:
                ql, qr = l.denominator, r.denominator
                assert ql % 8 == 0 and qr % 8 == 0
                record["endpoint_slack_caps"].append({"component_index": i,
                    "q_left": ql, "q_right": qr, "width": str(r-l),
                    "cap_integer": floor((Q(1,4)-Q(1,ql)-Q(1,qr))/(r-l))})
        record["phase_records"] = []
        for phase in protocol["final_phases"]:
            result, counts = phase_record(speeds, core, c, U, Q(phase))
            record["phase_records"].append(result)
            event_counts.append({"id": declared["id"], **counts})
        record["diagnostics"] = []
        for d in declared["diagnostic_final_speeds"]:
            result = reconstruct_time(speeds, Q(d), Q(0))
            record["diagnostics"].append({"speed": d, "phase": "0", **component_summary(result)})
            COUNTS["diagnostic_reconstructions"] += 1
        records.append(record)
        print("completed", declared["id"], flush=True)
    out = {"algorithm": "Independent rational contact events; direct modular time-threshold reconstruction",
           "protocol_sha256": sha(PROTOCOL), "source_sha256": sha(Path(__file__)),
           "records": records, "counts": COUNTS, "parameter_counts": event_counts,
           "independence": "Source and this output frozen before primary code/output access."}
    output = HERE / "independent_last_runner_results.json"
    output.write_text(json.dumps(out, indent=2)+"\n")
    manifest = {"protocol_sha256": sha(PROTOCOL), "source_sha256": sha(Path(__file__)),
                "output_sha256": sha(output), "primary_access_before_freeze": False,
                "files": [Path(__file__).name, output.name]}
    (HERE / "INDEPENDENT_FREEZE.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == "__main__":
    main()
