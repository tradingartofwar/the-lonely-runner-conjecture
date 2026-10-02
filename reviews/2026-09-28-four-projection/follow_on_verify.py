#!/usr/bin/env python3
"""Independent tiny-window event verification of3post-protocol constructions.

Reuses only the independent reviewer's threshold/phase routines, never primary
code or results. No scan: inputs are derived exactly from follow_on_protocol.
Default replay is read-only; --write creates the separate reviewer archive.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

from verify import allowed, frac, project_from_phase, safe, trace22

HERE = Path(__file__).resolve().parent
DELTA = F(1, 8)


def case_record(case_id, speeds, phases, lo, hi, core=(), anchor=F(0), metadata=None):
    assert len(speeds) == 4 and list(speeds) == sorted(speeds)
    final, trace = trace22(speeds, phases, DELTA, lo)
    assert final == hi
    final_flags = [safe(v, ph, final, DELTA) for v, ph in zip(speeds, phases)]
    assert final_flags == [False, True, True, True]
    later = project_from_phase(speeds[0], phases[0], DELTA, final)
    assert later > hi
    assert all(safe(v, ph, later, DELTA) for v, ph in zip(speeds, phases))

    # Independently inspect the whole short interval ending at the23rd step.
    # Huge absolute lap labels are permitted; the number of neighboring laps
    # is tiny because the interval width scales inversely with the speeds.
    all_speeds = tuple(map(F, core)) + tuple(speeds)
    all_phases = (F(0),) * len(core) + tuple(phases)
    full, event_count = allowed(all_speeds, all_phases, DELTA, lo, later)
    assert full == [(later, later)]
    old_window, old_count = allowed(all_speeds, all_phases, DELTA, lo, hi)
    assert old_window == []
    if core:
        core_result, _ = allowed(core, [F(0)] * len(core), DELTA, lo, later)
        assert core_result == [(lo, later)]

    # Independent direct cover proof. Lap labels below are relative to anchor.
    local_phases = [frac(v * anchor + ph) for v, ph in zip(speeds, phases)]
    chain = []
    for runner, lap in ((2, 0), (0, 0), (3, 0), (1, 1), (2, 1), (3, 1), (0, 1)):
        v, ph = speeds[runner], local_phases[runner]
        left = anchor + (lap - DELTA - ph) / v
        right = anchor + (lap + DELTA - ph) / v
        chain.append({"runner_index": runner, "relative_lap": lap,
                      "speed": str(v), "left": str(left), "right": str(right)})
    assert F(chain[0]["left"]) < lo < F(chain[0]["right"])
    assert F(chain[-1]["left"]) < hi < F(chain[-1]["right"])
    for previous, current in zip(chain, chain[1:]):
        assert max(F(previous["left"]), F(current["left"])) < min(F(previous["right"]), F(current["right"]))
    assert F(chain[-1]["right"]) == later
    a, b, c, d = speeds
    margin = 3 / (4 * a) - (1 / (4 * b) + 1 / (2 * c) + 1 / d)
    assert margin < 0
    return {
        "case_id": case_id, "speeds": list(map(str, speeds)),
        "phases": list(map(str, phases)), "core": list(core),
        "window": [str(lo), str(hi)], "anchor": str(anchor),
        "anchor_phases": list(map(str, local_phases)),
        "condition_margin": str(margin), "fixed22_trace": trace,
        "fixed22_final": str(final), "fixed22_safe_flags": final_flags,
        "fixed22_raw_verdict": "inconclusive", "window_is_empty": True,
        "first_witness_after_left": str(later), "step23": "P_a",
        "full_allowed_set_in_extended_window": [[str(later), str(later)]],
        "extended_window": [str(lo), str(later)],
        "oracle_threshold_events_original": old_count,
        "oracle_threshold_events_extended": event_count,
        "core_extended_window_certified": bool(core),
        "open_blocking_cover": chain,
        "metadata": metadata or {},
    }


def build():
    raw = (HERE / "follow_on_protocol.json").read_bytes()
    protocol = json.loads(raw)
    equal = protocol["auxiliary_equal"]
    distinct = protocol["auxiliary_distinct"]
    eq_speeds, eq_phases = tuple(map(F, equal["speeds"])), tuple(map(F, equal["phases"]))
    di_speeds, di_phases = tuple(map(F, distinct["speeds"])), tuple(map(F, distinct["phases"]))
    distinct_lo = (-DELTA - di_phases[0]) / di_speeds[0]
    cases = [
        case_record("auxiliary_equal", eq_speeds, eq_phases, F(equal["L"]), F(equal["R"])),
        case_record("auxiliary_distinct", di_speeds, di_phases, distinct_lo, F(distinct["R"])),
    ]
    lift = protocol["common_start_lift"]
    modulus, numerator = lift["M"], lift["P"]
    scale = 640 * modulus * 10**6
    anchor = F(numerator, modulus)
    inverse = pow(numerator, -1, modulus)
    residues = []
    for ph in di_phases:
        raw_residue = modulus * ph
        assert raw_residue.denominator == 1
        residues.append((raw_residue.numerator * inverse) % modulus)
    physical = tuple(scale * v + residue for v, residue in zip(di_speeds, residues))
    assert all(v.denominator == 1 for v in physical)
    assert len(set((F(0), F(1), F(4), F(5)) + physical)) == 8
    assert [frac(v * anchor) for v in physical] == list(di_phases)
    assert residues == [185445, 141440, 390144, 84480]
    assert list(physical) == [429158400185445, 432537600141440, 519045120390144, 713687040084480]
    lo = anchor + (-DELTA - di_phases[0]) / physical[0]
    hi = anchor + 1 / physical[-1]
    cases.append(case_record("common_start_lift", physical, (F(0),) * 4, lo, hi,
                             core=(1, 4, 5), anchor=anchor,
                             metadata={"M": modulus, "P": numerator, "N": scale,
                                       "residues": residues, "physical_n": 8,
                                       "reference": 0, "common_start": True}))
    assert cases[0]["first_witness_after_left"] == "299/352"
    assert cases[1]["first_witness_after_left"] == "38325/44704"
    assert cases[2]["first_witness_after_left"] == "163489640070647/490466743069080"
    assert all(c["oracle_threshold_events_extended"] < 30 for c in cases)
    # trace22 deliberately stores exact Fraction speed objects; normalize them
    # through a narrow scalar serializer while retaining all other field types.
    return json.loads(json.dumps({
        "status": "Independent exact3case verification passed",
        "provenance": "Post-protocol analytical constructions; frozen10case archive unchanged",
        "method": "Independent tiny-window threshold reconstruction plus open-interval cover and phase-case22trace",
        "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "case_count": len(cases), "cases": cases,
        "limits": "No full-period enumeration; no speed or phase scan; counterexample to fixed22 completeness, not LRC",
    }, default=lambda x: str(x) if isinstance(x, F) else (_ for _ in ()).throw(TypeError(type(x)))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    target = HERE / "follow_on_verification.json"
    if args.write:
        target.write_text(output)
    else:
        assert target.read_text() == output
    print(json.dumps({"case_count": result["case_count"],
                      "all22final_iterates_unsafe": True, "all_supplied_windows_empty": True,
                      "all23rd_projections_first_witness": True,
                      "extended_threshold_event_counts": [c["oracle_threshold_events_extended"] for c in result["cases"]],
                      "verification_sha256": hashlib.sha256(output.encode()).hexdigest()}))


if __name__ == "__main__":
    main()
