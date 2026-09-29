# Separate physical review of the row38 coefficient range

September 29, 2026. Status: **PASS** for the exact records described below.
Materially AI-generated, separately tasked internal review. This is neither
external human review nor a formal proof certificate. Findings were shared
with the coordinator; no blind replication is claimed.

## Scope and method

I read the pinned row-(3,8) transfer and the preceding coefficient-range and
selector-support notes, together with AGENTS.md and the repository evidence
rules. Before the new protocol was frozen, I checked the general distinct-speed
domain, coordinate-lap recovery, zero-phase reflection and the operational
period. No new coefficient enumeration or physical trial was run before the
protocol freeze. The review script imports only Python standard-library
modules; it imports no coordinator, compiler, selector or coefficient checker.

For each specified physical pair, the reviewer projects the three preserved
segments under Qx-Py, takes the first contained integer on the first segment
with a contact, and reconstructs the contact by affine interpolation. This is
separate from the coordinator's residue formula and fallback table. Seventh
torus laps are recomputed as floor(Ax+By), rather than copied from (3,8).

For p=dP,q=dQ, solve Q*i=-h modulo P with 0<=i<P, set j=(Q*i+h)/P,
and recover tau=(x+i)/P and t=tau/d. Direct physical multiplication checks
all seven phases and floor(v*t) values. Independently,

    physical_lap = torus_lap + a*i + b*j

is verified for every row. Two different Bezout representatives also recover
the same time and integer laps. Reflection uses the declared convention 1-t.
A zero phase stays zero and has reflected lap v-lap; a nonzero phase becomes
1-phase and has reflected lap v-1-lap. This distinction is exercised by the
rejected records, including the repeated-speed auxiliary failures.

## Reviewed records and exact agreement

The deterministic JSON output records **96,202 scalar field comparisons** and
**1,400 physical records**:

| Category | Records |
| --- | ---: |
| First failed pair of every rejected primary residue cell | 1,307 |
| Auxiliary failures of primary-accepted cells | 27 |
| Frozen positive/comparison and repeated-core controls | 58 |
| Analytic large-slope controls, both signs | 6 |
| New failure and old witness for the old-only row (38,18) | 2 |

There are 9,800 checks in each of the selected phase, selected lap, reflected
phase and reflected lap categories, plus 2,800 alternative Bezout recoveries.
All 1,307 primary failures are checked against their declared coefficient
cell and first-failure pair in classification.json. Their roles are 863 leader,
138 first fallback and 306 second fallback. All have eight distinct speeds.
Exactly 357 primary failures have seventh phase zero. All 27 auxiliary
failures occur at (1,1), have seventh phase zero and are explicitly labelled
repeated-speed configurations.

All 18 original (3,8) configurations reproduce the archived common physical
fields. The 18 lifted (59,64) configurations have the same times and fractional
phases. Their seventh torus laps increase by 63,29,27,14 according to leader,
first fallback, second fallback or auxiliary role. Physical seventh laps have
the additional change 56(i+j). Thus phase preservation does not preserve
integer laps. Both scaled-pair controls are checked for all three frozen rows.
The four identically repeated core rows remain safe but do not have eight
distinct speeds. Row (6,2) is safe on the 17 primary controls and fails at the
auxiliary (1,1), as required by the distinct contracts.

For all six analytic large-slope controls the reviewer reconstructs the open
interval for j, verifies strict interior membership, recovers (1,4j), and
checks the failed seventh phase. This includes coefficients of size 10^12.
These are six frozen controls of the analytic construction, not a scan of
large coefficients or a substitute for its separately reviewed proof.

For (38,18) at (p,q)=(1,20), the new selector chooses t=7/24 and minimum
1/12; the old selector chooses t=47/176 and minimum 1/8. Both are recovered
independently from their respective segments. This explicitly exhibits two
different selected times. Failure of the new selector does not imply absence
of another lonely time.

The declared ambient fallback example is also reconstructed directly: for
(59,64), the first integer in the raw image of the whole fallback segment is
29, attained strictly inside it at (43/133,165/1064). All six core phases are
safe and the seventh phase is zero. This refutes whole-segment safety for that
row. It is ambient evidence and is not claimed to be an actual selected
physical failure. The conditional outside-R physical controls were not
triggered because the complete classification contains no such accepted cell.

## Corrections, reproduction and limits

Before the first complete review output, a harness path assumption used
zero-padded shard filenames such as delta_m09.json; the coordinator's actual
filenames are unpadded, such as delta_m9.json. The loader was corrected. No
trial, coefficient predicate, physical calculation or coordinator output
changed. Two metadata assertions were then added, and the same frozen
records were rerun. No physical or arithmetic discrepancy was found.

Run from the repository root:

```sh
python3 reviews/2026-09-29-cc-row38-range/physical_review.py
```

The script emits deterministic JSON, including its own SHA256 and hashes of
all input artifacts. The detailed coordinator failure shards remain the
complete certificates; this review does not duplicate them. The physical
checks establish exact agreement for these records. Universal coefficient
classification additionally depends on the separate support, large-slope,
tail and exhaustive residue arguments. Those universal results retain the
status of internally reviewed proof candidates. No new literature, priority,
external-review or optimal-time claim is made here.
