"""Audit a continuation ledger from physical trajectories, using exact arithmetic."""

import argparse
import json
from fractions import Fraction
from pathlib import Path

DELTA = Fraction(1, 16)
DENOMINATORS = range(2, 17)


def physical(weights):
    if len(weights) != 4 or any(type(w) is not int or w <= 0 for w in weights):
        raise ValueError("Expected four positive integer weights")
    sums = [0]
    for weight in weights:
        sums += [value + weight for value in sums]
    speeds = sorted(sums[1:])
    if len(set(speeds)) != 15:
        raise ValueError("Expected fifteen distinct physical speeds")
    return speeds


def score(speeds, q=None, time=None):
    if time is None:
        return dict(q=None, time=None, clearance=None, limiting_speeds=[], status="abstain")
    distances = {}
    for v in speeds:
        position = v * time
        distances[v] = abs(position - round(position))
    least = min(distances.values())
    return dict(q=q, time=str(time), clearance=str(least),
                limiting_speeds=[v for v, distance in distances.items() if distance == least],
                status="safe" if least >= DELTA else "unsafe")


def first_edge(speeds, q, sign):
    """Time from the anchor to any noncollider's outgoing boundary."""
    arrivals = {}
    for v in speeds:
        phase = Fraction(sign * v, q) % 1
        if phase:
            arrivals[v] = (1 - DELTA - phase) / v
    if not arrivals:
        return None, []
    earliest = min(arrivals.values())
    return earliest, [v for v, arrival in arrivals.items() if arrival == earliest]


def outside(speeds, q, sign, h):
    """Keep the lift on its initial lap, orienting each trajectory toward +1."""
    result = []
    for v in speeds:
        phase = Fraction(sign * v, q) % 1
        lifted = phase + v * h
        if lifted < DELTA or lifted > 1 - DELTA:
            result.append(v)
    return result


def direct_and_escape(speeds, colliders):
    no_shift = dict(sign=None, colliders=[], h=None, room=None, edge_speeds=[])
    for q, hits in colliders.items():
        if not hits:
            direct = score(speeds, q, Fraction(1, q))
            return direct, {**direct, **no_shift, "sign": 0, "h": "0"}

    abstention = score(speeds)
    for q, hits in colliders.items():
        h = DELTA / min(hits)
        for sign in (1, -1):
            # Individual first-lap endpoints, independent of extrema and headroom tests.
            if outside(speeds, q, sign, h):
                continue
            room, edges = first_edge(speeds, q, sign)
            selected = score(speeds, q, Fraction(1, q) + sign * h)
            return abstention, dict(**selected, sign=sign, colliders=hits, h=str(h),
                                    room=None if room is None else str(room), edge_speeds=edges)
    return abstention, {**abstention, **no_shift}


def earlier_score(speeds, colliders):
    fewest = min(len(hits) for hits in colliders.values())
    tied = [q for q, hits in colliders.items() if len(hits) == fewest]
    if fewest == 0:
        q = min(tied)
        return score(speeds, q, Fraction(1, q))
    largest_minimum = max(min(colliders[q]) for q in tied)
    q = min(q for q in tied if min(colliders[q]) == largest_minimum)
    h = DELTA / largest_minimum
    forward, _ = first_edge(speeds, q, 1)
    backward, _ = first_edge(speeds, q, -1)
    sign = 1 if forward is None or forward >= backward else -1
    return score(speeds, q, Fraction(1, q) + sign * h)


def wrap_diagnostics(speeds, colliders):
    result = dict(tested=0, safe_count=0, first_safe=None, first_unsafe=None)
    for q, hits in colliders.items():
        if not hits:
            raise ValueError("Wrap diagnostic is defined only after a first-arc abstention")
        h = DELTA / min(hits)
        for sign in (1, -1):
            endpoint = score(speeds, q, Fraction(1, q) + sign * h)
            safe = endpoint.pop("status") == "safe"
            result["tested"] += 1
            result["safe_count"] += safe
            key = "first_safe" if safe else "first_unsafe"
            if result[key] is None:
                result[key] = dict(**endpoint, sign=sign, colliders=hits,
                                   outside_first_arc=outside(speeds, q, sign, h))
    return result


def expected_row(weights, with_wrap):
    speeds = physical(weights)
    colliders = {q: [v for v in speeds if v % q == 0] for q in DENOMINATORS}
    direct, escape = direct_and_escape(speeds, colliders)
    result = dict(weights=list(weights), escape=escape, direct=direct,
                  earlier=earlier_score(speeds, colliders))
    if with_wrap:
        if escape["status"] != "abstain":
            raise ValueError("Wrap diagnostics supplied on a first-arc return")
        result["wrap"] = wrap_diagnostics(speeds, colliders)
    return result


def compare(expected, reported, location):
    """Compare required fields, allowing unrelated provenance on their parent records."""
    if isinstance(expected, dict):
        if not isinstance(reported, dict):
            raise ValueError(f"{location}: expected an object")
        for key, value in expected.items():
            if key not in reported:
                raise ValueError(f"{location}: missing field {key}")
            compare(value, reported[key], f"{location}.{key}")
    elif type(expected) is not type(reported) or expected != reported:
        raise ValueError(f"{location}: expected {expected!r}, received {reported!r}")


def verify_row(weights, record):
    """Reconstruct selections, distances, limiting speeds and optional wrap diagnostics."""
    expected = expected_row(weights, "wrap" in record)
    location = f"weights={tuple(weights)}"
    compare(expected, record, location)
    if "q3_colliders" in record or "clear_anchor_count" in record or record.get("arm") in {"conditioned", "wrap_screen"}:
        speeds = physical(weights)
        q3 = sum(v % 3 == 0 for v in speeds)
        clear = sum(all(v % q for v in speeds) for q in DENOMINATORS)
        if "q3_colliders" in record:
            compare(q3, record["q3_colliders"], location + ".q3_colliders")
        if "clear_anchor_count" in record:
            compare(clear, record["clear_anchor_count"], location + ".clear_anchor_count")
        arm = record.get("arm")
        if (arm in {"conditioned", "wrap_screen"} and clear) or (arm == "conditioned" and q3 < 5):
            raise ValueError(f"{location}: ineligible for {arm} cohort")


def verify_ledger(evidence):
    """Check every row, the wrap inspection policy, and the per-arm summary totals."""
    rows = evidence["rows"]
    stage, trigger = evidence["stage"], evidence["trigger"]
    declared = evidence["counts"]
    arms = set(declared)
    if stage == "wrap" and trigger in {"defer", "unsafe"}:
        if rows or declared:
            raise ValueError(f"Expected empty evidence for wrap/{trigger}")
        return
    if stage == "cohorts" or (stage == "wrap" and trigger == "cohort_abstentions"):
        expected_arms = {"unconditioned", "conditioned"}
    elif stage == "wrap" and trigger == "new_screen":
        expected_arms = {"wrap_screen"}
    else:
        raise ValueError(f"Unrecognized continuation stage or trigger: {stage}/{trigger}")
    if arms != expected_arms:
        raise ValueError(f"Unexpected study arms: {sorted(arms)}")
    fields = ("rows escape_safe earlier_safe direct_safe abstentions multi_safe gain_over_direct "
              "gain_over_earlier earlier_only unique_gain multi_unique_gain different_safe_times "
              "wrap_evaluated wrap_recovered").split()
    calculated = {arm: {**dict.fromkeys(fields, 0), "collision_histogram": {}} for arm in arms}
    for row in rows:
        arm = row["arm"]
        totals = calculated[arm]
        weights = row["weights"]
        verify_row(weights, row)
        selected, direct, earlier = row["escape"], row["direct"], row["earlier"]
        safe = selected["status"] == "safe"
        direct_safe = direct["status"] == "safe"
        earlier_safe = earlier["status"] == "safe"
        should_sweep = stage == "wrap" and selected["status"] == "abstain"
        if ("wrap" in row) != should_sweep:
            raise ValueError(f"weights={weights}: wrap diagnostic inclusion mismatch")
        multi = safe and len(selected["colliders"]) >= 2
        unique = safe and not direct_safe and not earlier_safe
        outcomes = dict(rows=1, escape_safe=safe, direct_safe=direct_safe, earlier_safe=earlier_safe,
                        abstentions=selected["status"] == "abstain", multi_safe=multi,
                        gain_over_direct=safe and not direct_safe, gain_over_earlier=safe and not earlier_safe,
                        earlier_only=earlier_safe and not safe, unique_gain=unique,
                        multi_unique_gain=multi and unique, different_safe_times=safe and earlier_safe
                        and selected["time"] != earlier["time"], wrap_evaluated=should_sweep,
                        wrap_recovered=should_sweep and row["wrap"]["safe_count"] > 0)
        for key, value in outcomes.items():
            totals[key] += value
        if safe:
            bucket = str(len(selected["colliders"]))
            histogram = totals["collision_histogram"]
            histogram[bucket] = histogram.get(bucket, 0) + 1
    for arm, totals in calculated.items():
        if declared[arm]["collision_histogram"] != totals["collision_histogram"]:
            raise ValueError(f"{arm}: collision histogram mismatch")
        compare(totals, declared[arm], f"counts.{arm}")


def self_test():
    # Opened controls: direct, signed gain, unsafe historical return, and re-entry.
    record = expected_row((2, 3, 17, 42), False)
    assert record["direct"]["time"] == "1/12"
    assert record["direct"]["limiting_speeds"] == [47, 59, 61]
    shifted = expected_row((14, 17, 103, 154), False)
    assert shifted["earlier"]["time"] == "289/4608"
    assert shifted["earlier"]["clearance"] == "17/4608"
    assert shifted["escape"]["time"] == "625/1872"
    assert shifted["escape"]["room"] == "13/12336"
    assert shifted["escape"]["edge_speeds"] == [257]
    missed = (260, 264, 1567, 2101)
    diagnostic = expected_row(missed, True)
    assert diagnostic["escape"]["status"] == "abstain"
    assert diagnostic["wrap"]["tested"] == 30
    assert diagnostic["wrap"]["safe_count"] == 5
    first = diagnostic["wrap"]["first_safe"]
    assert (first["time"], first["clearance"], first["limiting_speeds"]) == ("1409/4224", "1/16", [264])
    assert first["outside_first_arc"] == [3668, 3928, 3932, 4192]
    verify_row(missed, diagnostic)
    diagnostic["arm"] = "wrap_screen"
    counts = dict(rows=1, escape_safe=0, earlier_safe=0, direct_safe=0, abstentions=1,
                  multi_safe=0, gain_over_direct=0, gain_over_earlier=0, earlier_only=0,
                  unique_gain=0, multi_unique_gain=0, different_safe_times=0,
                  wrap_evaluated=1, wrap_recovered=1, collision_histogram={})
    ledger = dict(rows=[diagnostic], counts={"wrap_screen": counts},
                  stage="wrap", trigger="new_screen")
    verify_ledger(ledger)
    counts["wrap_recovered"] = 0
    try:
        verify_ledger(ledger)
    except ValueError as error:
        assert "counts.wrap_screen.wrap_recovered" in str(error)
    else:
        raise AssertionError("A fabricated recovery count passed")
    first["limiting_speeds"] = []
    try:
        verify_row(missed, diagnostic)
    except ValueError as error:
        assert "wrap.first_safe.limiting_speeds" in str(error)
    else:
        raise AssertionError("A fabricated limiting-speed list passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, nargs="?", help="researcher JSON bundle to audit")
    parser.add_argument("--self-test", action="store_true", help="exercise only opened controls")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("Opened controls and corrupted-record rejection passed.")
    if args.ledger:
        data = json.loads(args.ledger.read_bytes())
        evidence = data["evidence"]
        verify_ledger(evidence)
        print(f"Verified {len(evidence['rows'])} physical row records and all arm counts.")
    if not args.self_test and not args.ledger:
        parser.error("supply a researcher ledger or --self-test")


if __name__ == "__main__":
    main()
