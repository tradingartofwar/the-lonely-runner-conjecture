"""Prospective two-stage continuation for the frozen four-weight first-escape rule.

Cohorts are matched by smallest-weight band. Selection uses the divisibility profile
only. Wrap work is conditional on the cohort result and never alters the original
one-output score. An independent verifier can replay the same seed and audit the
certificates runner by runner. Run with --help for the command-line interface.
"""
import argparse
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments/subset-sum-prediction"))
sys.path.insert(0, str(ROOT / "experiments/one-time-prediction"))
from predictor import choose_time
from observatory.escape_trial.rule import predict
from observatory.study.candidate import predict as direct_predict
from observatory.study.panel import SCALES, draw_weights

Q = range(2, 17)
TARGET = Fraction(1, 16)
PROTOCOL = "four-weight-multiple-colliders-v1"
COHORT_QUOTA, COHORT_CAP = 4, 256
WRAP_QUOTA, WRAP_CAP = 32, 512

SCOPE = (
    "Stationary reference, 16 common-start runners, inclusive 1/16; primitive "
    "stretch_middle generator. Band-matched arms are drawn separately. "
    "Unconditioned means no filtering on divisibility, predictor or outcome. "
    "The conditioned arm has a collider at every q=2..16 and at least five at "
    "q=3, matching the opened motivating anchor. Counts of colliders at q=3 "
    "range over 3,4,5,7,15 for the 81 four-weight residue signatures. "
    "Both are finite selected cohorts; keep raw arm denominators "
    "and report all skipped draws and empty cells. Wrap is an endpoint scan "
    "only on first-arc abstentions, with a separate conditional denominator."
)


def physical(weights):
    return sorted(sum(c) for k in range(1, 5) for c in combinations(weights, k))


def published_exclusions():
    prior = json.loads((HERE / "exclusions.json").read_bytes())
    opened = json.loads((HERE / "reveal/panel.json").read_bytes())
    return set(map(tuple, prior)).union(tuple(row["weights"]) for row in opened["instances"])


def stream(seed, arm, band):
    domain = f"{PROTOCOL}|{arm}|{band[0]}-{band[1]}|".encode()
    return random.Random(int.from_bytes(hashlib.sha256(domain + seed).digest(), "big"))


def eligible(weights, arm):
    if arm == "unconditioned":
        return True
    speeds = physical(weights)
    counts = [sum(v % q == 0 for v in speeds) for q in Q]
    if not all(counts):
        return False
    return arm == "wrap_screen" or counts[1] >= 5


def sample(seed, arm, seen):
    """Select all inputs for an arm before evaluating any returns or distances."""
    quota, cap = (WRAP_QUOTA, WRAP_CAP) if arm == "wrap_screen" else (COHORT_QUOTA, COHORT_CAP)
    cells, rows = [], []
    for band in SCALES:
        rng = stream(seed, arm, band)
        rejected = Counter()
        accepted = 0
        for attempt in range(1, cap + 1):
            weights = draw_weights(rng, band, "stretch_middle")
            if math.gcd(*weights) != 1:
                rejected["nonprimitive"] += 1
            elif weights in seen:
                rejected["excluded_or_duplicate"] += 1
            elif not eligible(weights, arm):
                rejected["divisibility"] += 1
            else:
                seen.add(weights)
                accepted += 1
                rows.append({"arm": arm, "band": list(band), "weights": list(weights)})
                if accepted == quota:
                    break
        cells.append(dict(arm=arm, band=list(band), quota=quota, cap=cap, attempts=attempt,
                          accepted=accepted, shortfall=quota - accepted, rejected=dict(rejected)))
    return cells, rows


def score(speeds, q, time):
    if time is None:
        return dict(q=None, time=None, status="abstain", clearance=None, limiting_speeds=[])
    p, d = time.as_integer_ratio()
    values = [(min((v*p) % d, (-v*p) % d), v) for v in speeds]
    least = min(n for n, _ in values)
    return dict(q=q, time=str(time), status="safe" if 16 * least >= d else "unsafe",
                clearance=str(Fraction(least, d)), limiting_speeds=[v for n, v in values if n == least])


def assess(row):
    w = row["weights"]
    speeds = physical(w)
    escape, direct = predict(w), direct_predict(w)
    q, earlier, _ = choose_time(speeds)
    if escape:
        den = escape["q"]
        result = score(speeds, den, escape["time"])
        result.update(sign=escape["sign"], h=str(escape["escape"]),
                      room=str(escape["room"]) if escape["room"] is not None else None,
                      colliders=[v for v in speeds if v % den == 0], edge_speeds=list(escape["room_speeds"]))
    else:
        result = dict(score(speeds, None, None), sign=None, h=None, room=None, colliders=[], edge_speeds=[])
    return {**row, "q3_colliders": sum(v % 3 == 0 for v in speeds),
            "clear_anchor_count": sum(all(v % q for v in speeds) for q in Q),
            "escape": result, "direct": score(speeds, direct.denominator if direct else None, direct),
            "earlier": score(speeds, q, earlier)}


def wrap_diagnostic(weights):
    """Test full membership at the 30 preregistered endpoints of one abstention."""
    speeds = physical(weights)
    first_safe = first_unsafe = None
    tested = safe_count = 0
    for q in Q:
        hits = [v for v in speeds if v % q == 0]
        if not hits:
            raise ValueError("Wrap diagnostic requires a collider at every anchor")
        m = min(hits)
        d = 16 * m * q
        for sign in (1, -1):
            # Reflect a backward trajectory. All directed phases now increase.
            # Each runner remains in the calculation, including interior class members.
            lifted = [(16*m*((sign*v) % q) + v*q, v) for v in speeds]
            outside = [v for n, v in lifted if not d <= 16*n <= 15*d]
            if not outside:
                raise ValueError("The frozen rule should have certified this direction")
            distances = [(min(n % d, (-n) % d), v) for n, v in lifted]
            least = min(n for n, _ in distances)
            safe = 16 * least >= d
            tested += 1
            safe_count += safe
            if (safe and first_safe is None) or (not safe and first_unsafe is None):
                case = dict(q=q, sign=sign, time=str(Fraction(16*m + sign*q, d)),
                            clearance=str(Fraction(least, d)), limiting_speeds=[v for n, v in distances if n == least],
                            colliders=hits, outside_first_arc=outside)
                if safe:
                    first_safe = case
                else:
                    first_unsafe = case
    return dict(tested=tested, safe_count=safe_count, first_safe=first_safe, first_unsafe=first_unsafe)


def tally(rows):
    counts = dict.fromkeys(("rows", "escape_safe", "earlier_safe", "direct_safe", "abstentions",
                           "multi_safe", "gain_over_direct", "gain_over_earlier", "earlier_only",
                           "unique_gain", "multi_unique_gain", "different_safe_times",
                           "wrap_evaluated", "wrap_recovered"), 0)
    histogram = Counter()
    for row in rows:
        e, d, h = (row[name]["status"] == "safe" for name in ("escape", "direct", "earlier"))
        colliders = len(row["escape"]["colliders"])
        unique = e and not d and not h
        counts["rows"] += 1
        counts["escape_safe"] += e
        counts["direct_safe"] += d
        counts["earlier_safe"] += h
        counts["abstentions"] += row["escape"]["status"] == "abstain"
        counts["multi_safe"] += e and colliders >= 2
        counts["gain_over_direct"] += e and not d
        counts["gain_over_earlier"] += e and not h
        counts["earlier_only"] += h and not e
        counts["unique_gain"] += unique
        counts["multi_unique_gain"] += unique and colliders >= 2
        counts["different_safe_times"] += e and h and row["escape"]["time"] != row["earlier"]["time"]
        if e:
            histogram[str(colliders)] += 1
        if "wrap" in row:
            counts["wrap_evaluated"] += 1
            counts["wrap_recovered"] += row["wrap"]["safe_count"] > 0
    return dict(counts, collision_histogram=dict(sorted(histogram.items())))


def arm_counts(rows, arms):
    return {arm: tally([row for row in rows if row["arm"] == arm]) for arm in arms}


def branch(rows):
    if any(r["escape"]["status"] == "unsafe" for r in rows):
        return "unsafe"
    if any(r["escape"]["status"] == "abstain" for r in rows):
        return "cohort_abstentions"
    if any(r["escape"]["status"] == "safe" and len(r["escape"]["colliders"]) >= 2 for r in rows):
        return "new_screen"
    return "defer"


def focus_example(rows):
    """Give a replayable ordinary/failed example even when the forecast misses."""
    for qualifies in (
        lambda r: r["escape"]["status"] == "unsafe",
        lambda r: len(r["escape"]["colliders"]) >= 2 and r["earlier"]["status"] != "safe",
        lambda r: len(r["escape"]["colliders"]) >= 2,
        lambda r: r["escape"]["status"] == "abstain",
        lambda r: True,
    ):
        for row in rows:
            if qualifies(row):
                return row
    return None


def run(seed, stage, role):
    seen = published_exclusions()
    known = len(seen)
    arms = ("unconditioned", "conditioned")
    cells, inputs = [], []
    for arm in arms:
        arm_cells, arm_rows = sample(seed, arm, seen)
        cells.extend(arm_cells)
        inputs.extend(arm_rows)
    cohorts = [assess(r) for r in inputs]
    counts = arm_counts(cohorts, arms)
    trigger = branch(cohorts)
    evidence = dict(protocol=PROTOCOL, seed=seed.hex(), stage=stage, exclusions=known, scope=SCOPE,
                    primary_question="Does the frozen selector choose any safe shift with at least two colliders? "
                                     "Score and interpret each arm independently. A zero count is a miss for that arm.",
                    unique_gain_definition="A safe frozen return on a row where direct and earlier both miss. "
                                           "Different safe times on the same row are counted separately.",
                    historical_fresh_trial=dict(rows=12, escape_safe=12, direct_safe=11,
                                                earlier_safe=11, unique_gain=1, multi_unique_gain=0),
                    cohort_counts=counts, cohort_cells=cells, trigger=trigger)
    if stage == "cohorts":
        rows = cohorts
        evidence.update(cells=cells, counts=counts, focus=focus_example(rows))
        summaries = []
        for arm, c in counts.items():
            summaries.append(f"{arm}: {c['multi_safe']}/{c['rows']} safe multi-collider selections, "
                             f"{c['multi_unique_gain']} missed by both baselines, "
                             f"{c['earlier_only']} earlier-only, {c['abstentions']} abstentions")
        summary = ". ".join(summaries) + "."
        focus = evidence["focus"]
        if focus:
            chosen = focus["escape"]
            if chosen["time"] is not None:
                summary += (f" At {focus['weights']}, q={chosen['q']}, t={chosen['time']}, "
                            f"clearance {chosen['clearance']} at {chosen['limiting_speeds']}.")
            else:
                old = focus["earlier"]
                summary += (f" At {focus['weights']} the frozen rule abstained; earlier t={old['time']} "
                            f"had clearance {old['clearance']} at {old['limiting_speeds']}.")
        followup = {
            "cohort_abstentions": "Do any first-arc abstentions on these cohorts have a safe signed endpoint after re-entry?",
            "new_screen": "On a fresh bounded no-clear screen, does full endpoint membership recover any first-arc abstentions?",
        }
        if trigger in followup:
            action = {"next_question": followup[trigger]}
        else:
            action = {"decision": "Review the unsafe return before extending the rule." if trigger == "unsafe"
                      else "The cohort produced neither a safe multiple-collider selection nor an abstention. "
                           "Choose whether to change the pre-outcome stratification in a new protocol."}
    else:
        wrap_cells = []
        if trigger == "new_screen":
            wrap_cells, fresh_inputs = sample(seed, "wrap_screen", seen)
            rows = [assess(r) for r in fresh_inputs]
            active_arms = ("wrap_screen",)
        elif trigger == "cohort_abstentions":
            rows, active_arms = cohorts, arms
        else:
            rows, active_arms = [], ()
        for row in rows:
            if row["escape"]["status"] == "abstain":
                row["wrap"] = wrap_diagnostic(row["weights"])
        wrap_rows = [r for r in rows if "wrap" in r]
        successes = [r for r in wrap_rows if r["wrap"]["safe_count"]]
        focus = next(iter(successes or wrap_rows), None)
        evidence.update(cells=wrap_cells if trigger == "new_screen" else (cells if rows else []),
                        counts=arm_counts(rows, active_arms), focus=focus or focus_example(rows))
        summary = f"Wrap trigger {trigger}. {len(wrap_rows)} first-arc abstentions among {len(rows)} screened rows. "
        if wrap_rows:
            summary += f"Recovered {len(successes)} after checking {30 * len(wrap_rows)} signed endpoints."
        else:
            summary += "No endpoint sweep was eligible."
        if successes:
            e = focus["wrap"]["first_safe"]
            summary += (f" At {focus['weights']}, q={e['q']}, sign={e['sign']:+}, "
                        f"t={e['time']}, clearance {e['clearance']} at {e['limiting_speeds']}.")
            decision = "Select whether to test a cheaper one-output within-residue re-entry certificate against this full-membership benchmark."
        elif wrap_rows:
            decision = "No abstention had a safe endpoint in the 30 signed choices. Decide whether to enlarge the anchor family in a separate protocol."
        elif trigger in ("unsafe", "defer"):
            decision = "The cohort branch deferred the endpoint stage. Review the first-stage evidence before authorizing another comparison."
        else:
            decision = "There were zero first-arc abstentions in this bounded screen. A population claim about re-entry gains remains open."
        action = {"decision": decision}

    evidence["rows"] = rows
    if role == "verifier":
        from observatory.escape_trial.continuation_check import verify_ledger
        if stage == "wrap" and trigger != "cohort_abstentions":
            verify_ledger(dict(stage="cohorts", trigger=trigger, counts=counts, rows=cohorts))
        verify_ledger(evidence)
    return dict(summary=summary, evidence=evidence, **action)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, help="Deterministic hexadecimal seed, an even number of digits")
    parser.add_argument("--stage", required=True, choices=("cohorts", "wrap"))
    parser.add_argument("--role", required=True, choices=("researcher", "verifier"))
    parser.add_argument("--json", action="store_true", help="Print the full row and arm ledger")
    args = parser.parse_args()
    if not re.fullmatch(r"(?:[0-9a-fA-F]{2})+", args.seed):
        parser.error("--seed requires hexadecimal byte pairs")
    result = run(bytes.fromhex(args.seed), args.stage, args.role)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")) if args.json else result["summary"])


if __name__ == "__main__":
    main()
