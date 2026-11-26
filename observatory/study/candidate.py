"""Direct denominator certificate from four weights, common start, reference zero."""
from fractions import Fraction

RULE_REVISION = "four-weight-direct-residues-v1"


def residue_mask(weights, q):
    """Set bit r when a nonempty subset of the weights sums to r modulo q."""
    mask = 0
    width = (1 << q) - 1
    for weight in weights:
        r = weight % q
        # Rotating old bits includes this weight with each old subset.
        translated = ((mask << r) | (mask >> (q - r))) & width
        mask |= translated | (1 << r)
    return mask


def predict(weights):
    """Return 1/q for the smallest clear q from 2 through 16, or abstain."""
    weights = tuple(weights)
    if len(weights) != 4 or any(type(w) is not int or w <= 0 for w in weights):
        raise ValueError("Expected four positive integer weights")
    for q in range(2, 17):
        if residue_mask(weights, q) & 1 == 0:
            return Fraction(1, q)
    return None


def check_opened():
    """Replay only the already-opened source panel. This is outside predict()."""
    import json
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2] / "experiments"
    sys.path.insert(0, str(root / "one-time-prediction"))
    sys.path.insert(0, str(root / "subset-sum-prediction"))
    from predictor import choose_time
    from predict import predict as archived_four_weight

    def clearance(speeds, t):
        p, q = t.as_integer_ratio()
        return Fraction(min(min(v*p % q, -v*p % q) for v in speeds), q)

    panel = json.loads((root / "subset-sum-prediction" / "panel.json").read_bytes())
    comparisons = direct_total = earlier_only_direct = earlier_only_shifted = 0
    middle = []
    for row in panel["instances"]:
        w, speeds = row["weights"], row["speeds"]
        clear = []
        for q in range(2, 17):
            physical = {v % q for v in speeds}
            assert residue_mask(w, q) == sum(1 << r for r in physical)
            comparisons += 1
            if all(v % q for v in speeds):
                clear.append(q)
        proposed = predict(w)
        expected = Fraction(1, clear[0]) if clear else None
        assert proposed == expected
        _, old_time, _ = choose_time(speeds)
        if proposed is not None:
            assert proposed == old_time
            assert clearance(speeds, proposed) >= Fraction(1, 16)
            direct_total += 1
        if row["pattern"] != "stretch_middle":
            continue
        _, four_time = archived_four_weight(w)
        old_distance = clearance(speeds, old_time)
        if four_time is None and old_distance >= Fraction(1, 16):
            earlier_only_direct += int(proposed is not None)
            earlier_only_shifted += int(proposed is None)
        middle.append(dict(weights=w, clear_denominators=clear,
                           time=str(proposed) if proposed else None,
                           earlier_time=str(old_time), earlier_clearance=str(old_distance)))
    assert (comparisons, direct_total, len(middle)) == (900, 45, 12)
    assert (earlier_only_direct, earlier_only_shifted) == (9, 1)
    denominator_tests = sum(Fraction(r["time"]).denominator - 1 if r["time"] else 15
                            for r in middle)
    return dict(rule=RULE_REVISION, opened_rows=len(panel["instances"]),
                residue_sets_checked=comparisons, direct_predictions=direct_total,
                earlier_only_direct=earlier_only_direct, earlier_only_shifted=earlier_only_shifted,
                middle_denominator_tests=denominator_tests, middle_mask_updates=4*denominator_tests,
                middle=middle)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("weights", nargs="*", type=int)
    parser.add_argument("--check-opened", action="store_true")
    args = parser.parse_args()
    if args.check_opened:
        if args.weights:
            parser.error("--check-opened uses only the archived panel")
        print(json.dumps(check_opened(), indent=2))
    elif len(args.weights) == 4:
        result = predict(args.weights)
        print(result if result is not None else "abstain")
    else:
        parser.error("supply four weights or --check-opened")
