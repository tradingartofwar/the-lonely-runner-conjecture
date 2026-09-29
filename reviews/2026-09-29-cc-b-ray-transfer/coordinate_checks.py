"""Internal coordinate audit, using frozen discovery functions, not B adapter.

This is not a separately implemented candidate enumeration. The coordinate
translation, symbolic coefficient tests and direct physical checks are local.
"""
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "2026-09-29-cc-segment-discovery"


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def swap_data(source):
    out = copy.deepcopy(source)
    out["rows"] = [[b, a] for a, b in source["rows"]]
    for p in out["parents"]:
        p["vertices"] = [[v, u, z] for u, v, z in p["vertices"]]
        p["constraints"] = [[name, [b, a, c], rhs]
                                for name, (a, b, c), rhs in p["constraints"]]
    return out


def physical(t, speeds):
    positions = [s*t for s in speeds]
    laps = [p.numerator // p.denominator for p in positions]
    phases = [p-ell for p, ell in zip(positions, laps)]
    return {"time": t, "laps": laps, "phases": phases,
            "minimum": min(min(f, 1-f) for f in phases)}


def main():
    original = json.loads((SOURCE / "PARENT_INPUT.json").read_text())
    swapped = swap_data(original)
    assert swap_data(swapped) == original
    original_rows = [tuple(r) for r in original["rows"]] + [(5, 2)]
    rows = [tuple(r) for r in swapped["rows"]] + [(2, 5)]
    assert rows == [(b, a) for a, b in original_rows]
    vertex_constraints = 0
    for parent, old in zip(swapped["parents"], original["parents"]):
        assert parent["labels"] == old["labels"]
        assert parent["edges"] == old["edges"]
        assert next(c for c in parent["constraints"] if c[0] == "fold")[1:] == [["0", "1", "0"], "1/2"]
        for vertex in parent["vertices"]:
            for _, normal, rhs in parent["constraints"]:
                assert sum(F(a)*F(v) for a, v in zip(normal, vertex)) <= F(rhs)
                vertex_constraints += 1
    spec = importlib.util.spec_from_file_location("frozen_discovery_coordinate_audit", SOURCE / "discover.py")
    frozen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(frozen)
    frozen.ADDED_ROW = (5, 2)
    a_records, a_counts = frozen.candidates(original)
    frozen.ADDED_ROW = (2, 5)
    b_records, b_counts = frozen.candidates(swapped)
    assert a_counts == b_counts
    assert len(a_records) == len(b_records)
    endpoint_bands = 0
    for old, new in zip(a_records, b_records):
        for key in ("id", "parent", "edge", "seventh_lap", "labels", "source_parameters"):
            assert old[key] == new[key]
        assert sorted(old["endpoints"]) == sorted((v, u) for u, v in new["endpoints"])
        for u, v in new["endpoints"]:
            assert F(1, 8) <= u <= F(7, 8)
            assert F(1, 8) <= v <= F(1, 2)
            for row, lap in zip(rows, new["labels"]):
                phase = row[0]*u + row[1]*v - lap
                assert F(1, 8) <= phase <= F(7, 8)
                endpoint_bands += 1
        if new["tail_cutoff"] is not None:
            assert new["tail_cutoff"]*new["dx"]-new["dy"] >= 1
            assert new["dx"] > 0
    cover = frozen.build_cover(b_records)
    assert cover["status"] == "COMPLETE COVER CERTIFICATE"
    # This identity, valid for every u,v,g with qu=v+g, is the universal
    # physical certificate: (aq+b)u - (m+ag) = bu+av-m.
    symbolic_coefficient_checks = []
    for (a, b), new in zip(original_rows, rows):
        assert new == (b, a)
        symbolic_coefficient_checks.append({"native_row": (a, b), "swapped_row": new,
                                           "phase_coefficients_u_v_g": (b, a, 0),
                                           "physical_lap_g_coefficient": a})
    controls, wrong_clock, wrong_lap, wrong_sign, beyond_half = [], [], [], [], []
    display_order = [1, 0, 2, 3, 4, 5, 6]
    for q in range(2, 26):
        cert = frozen.witness(cover, q, rows)
        u, v = cert["point"]
        g = cert["h"]
        assert q*u-v == g and g == (q*u).__floor__()
        assert cert["time"] == u
        speeds = [a*q+b for a, b in original_rows]
        s = next(s for s in b_records if s["id"] == cert["segment"])
        ell = [m+a*g for m, (a, b) in zip(s["labels"], original_rows)]
        assert ell == cert["physical_laps"]
        direct = physical(u, speeds)
        reflected = physical(1-u, speeds)
        assert direct["minimum"] >= F(1, 8) and reflected["minimum"] >= F(1, 8)
        assert direct["laps"] == ell
        assert reflected["laps"] == [speed-1-lap for speed, lap in zip(speeds, ell)]
        assert q*(1-u)-(1-v) == q-1-g
        assert [speeds[i] for i in display_order] == [1,q,q+1,2*q+1,3*q+1,3*q+2,5*q+2]
        wrong_t = physical(v, speeds)
        if wrong_t["minimum"] < F(1, 8):
            wrong_clock.append({"q": q, "correct_time": u, "wrong_time": v, "wrong_minimum": wrong_t["minimum"]})
        for results, incorrect in ((wrong_lap, [m+b*g for m, (a,b) in zip(s["labels"], original_rows)]),
                                   (wrong_sign, [m-a*g for m, (a,b) in zip(s["labels"], original_rows)])):
            if incorrect != ell:
                index = next(i for i in range(7) if incorrect[i] != ell[i])
                results.append({"q": q, "native_index": index, "speed": speeds[index],
                                "correct_lap": ell[index], "wrong_lap": incorrect[index],
                                "wrong_phase": speeds[index]*u-incorrect[index]})
        if u > F(1,2):
            beyond_half.append({"q":q,"time":u,"folded_v":v})
        controls.append({"q":q,"segment":cert["segment"],"g":g,"point":(u,v),
                         "native":direct,"reflection":reflected})
    # A same-q candidate demonstrates why u<=1/2 is an extra restriction,
    # although the two selected segments happen to keep u<=1/2 themselves.
    fold_candidate = next(s for s in b_records if s['id'] == 'P6:E0-1:K3')
    fold_control = frozen.select_on(fold_candidate, 2)
    assert fold_control['point'] == (F(41,56), F(13,28))
    assert fold_control['point'][0] > F(1,2) >= fold_control['point'][1]
    assert 2*fold_control['point'][0]-fold_control['point'][1] == 1
    out = {"status":"PASS", "authorship":"b_coordinate_review, internal AI mathematical and implementation audit",
           "dependencies":{"input_sha256":hashlib.sha256((SOURCE/'PARENT_INPUT.json').read_bytes()).hexdigest(),
                           "frozen_discovery_sha256":hashlib.sha256((SOURCE/'discover.py').read_bytes()).hexdigest()},
           "summary":{"parent_vertex_constraint_checks":vertex_constraints,"candidates":len(b_records),
                      "candidate_endpoint_band_checks":endpoint_bands,"cutoff":cover["cutoff"],
                      "selected_ids":cover["chosen_ids"],"controls":len(controls),"new_physical_q_values":0},
           "selected":cover["chosen_segments"],"prefix_coverage":cover["coverage"],
           "symbolic_coefficients":symbolic_coefficient_checks,
           "first_wrong_clock_failure":wrong_clock[:1],"first_wrong_lap_failure":wrong_lap[:1],
           "first_wrong_sign_failure":wrong_sign[:1],"selected_times_beyond_one_half":beyond_half,
           "wrong_fold_excluded_safe_candidate":fold_control,
           "physical_controls":controls}
    print(json.dumps(encode(out),indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
