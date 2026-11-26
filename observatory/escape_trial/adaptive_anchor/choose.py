"""Select a final denominator from residue classes before signed membership."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from observatory.escape_trial.reentry_membership import classes_at, inspect


def select(groups):
    """Input is the q=4 table, which both the old and new policies build."""
    m = groups[0][0]
    examined = 0
    for speed in groups[0]:
        examined += 1
        if 15*m < speed < 17*m:
            return 7, examined

    lower_seen, upper_seen = set(), set()
    for residue in (1, 3):
        for speed in groups.get(residue, ()):
            examined += 1
            if 3*m < speed < 5*m:
                lower_seen.add(residue)
            elif 11*m < speed < 13*m:
                upper_seen.add(residue)
            if len(lower_seen) == 2 or len(upper_seen) == 2:
                return 7, examined
    return 4, examined


def adaptive(weights):
    groups = classes_at(weights, 4)
    q, examined = select(groups)
    if q == 7:
        groups = classes_at(weights, 7)
    for attempts, sign in enumerate((1, -1), 1):
        time, _ = inspect(groups, q, sign)
        if time is not None:
            return q, sign, time, examined, attempts
    return q, None, None, examined, 2


if __name__ == "__main__":
    opened = json.loads((HERE.parent / "last_anchor/results.json").read_bytes())["cases"]
    switches = gains = losses = examined_total = 0
    for case in opened:
        q, sign, time, examined, _ = adaptive(case["weights"])
        assert sign == case[str(q)]["issued_sign"]
        switches += q == 7
        fixed = case["4"]["issued_sign"] is not None
        gains += time is not None and not fixed
        losses += time is None and fixed
        examined_total += examined
    print(f"{len(opened)} opened cases; {switches} switches; {gains} gains, {losses} losses; "
          f"{examined_total} speed-window probes.")
