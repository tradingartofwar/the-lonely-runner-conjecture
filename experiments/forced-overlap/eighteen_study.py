"""Frozen 18-runner transfer panels; run with PYTHONPATH=. from the repository root."""
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from math import gcd

from lonely_runner.checker import feasible_intervals
from seventeen_study import check_core, pair_oracle


def panels():
    sparse, challenge = [], []
    mandatory = {11, 13, 16, 17, 60, 63, 70, 90}
    for j in range(8):
        sparse.append(tuple(5*i + 1 + hashlib.sha256(f"eighteen/sparse/{j}/{i}".encode())
                            .digest()[0] % 5 for i in range(16)))
        ranking = sorted(set(range(1, 96)) - mandatory,
                         key=lambda v: (hashlib.sha256(f"eighteen/challenge/{j}/{v}".encode())
                                        .digest(), v))
        challenge.append(tuple(sorted(mandatory.union(ranking[:8]))))
    return {"sparse": sparse, "challenge": challenge}


def main():
    oracle = pair_oracle(18)
    times = [Q(k, 18) for k in range(1, 18) if gcd(k, 18) == 1]
    assert feasible_intervals(range(1, 18), Q(1,18)) == tuple((t,t) for t in times)
    report = {"oracle_triples": oracle, "consecutive_control": list(map(str, times)), "panels": {}}
    for label, cores in panels().items():
        rows = [check_core(c, 18) for c in cores]
        totals = Counter()
        for row in rows:
            totals.update(row["counts"])
        report["panels"][label] = {"counts": dict(totals), "rows": rows}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
