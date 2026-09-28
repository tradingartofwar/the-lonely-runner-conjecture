# Independent exact verification of the frozen fixtures

2026-09-28. Agent 5. Status: **OBSERVED**, limited to the frozen auxiliary
fixtures. Material AI involvement includes implementation and review writing.
The protocol was received after the analytic candidate and before this
computation. Neither `primary.py` nor `results.json` was read in preparing this
implementation or report.

## Scope and result

All prescribed checks pass:

- 15 window cases: the three specified tile profiles times the five specified
  perturbations, on exactly `[0,3]`.
- Complete classification of 342 threshold points and 327 open partition cells.
- 15 agreements between the first safe point from the complete partition and
  the independently reconstructed next-safe iteration.
- 60 anchored cycle checks, each checking both the evaluated identity and the
  exact eight affine coefficients (four periods, four starts).
- Four explicit clipped-interval occupancy checks, including equality at
  `x=7/4`.
- 15 moving words containing no adjacent repeated nonempty block.

These are constructed arbitrary-phase auxiliary trains. No additional physical
common-start configuration, speed scan, phase scan, or new fixture was used.

## Independent method

`verify.py` uses only Python's standard library and exact `fractions.Fraction`.
For each label it enumerates all open intervals
`(s_i+m*p_i, s_i+(m+1/4)*p_i)` meeting `[0,3]`, retaining enough neighboring
occurrences to check either endpoint. Its partition comprises every interval
boundary in the window plus both window endpoints. It evaluates strict
containment at every partition point and at a midpoint of every open cell.
It then merges adjacent safe pieces into complete closed safe components,
including singleton equality witnesses.

The selector sorts the labels by actual speed `1/p_i`, with original label as
the tie-breaker, and applies the prescribed eleven positions
`a,b,c,d,c,d,b,c,d,c,d`. Each scalar projection is reconstructed by finding the
explicit interval that strictly contains its current time and jumping to that
interval's right endpoint. The implementation does not use the ceiling formula
for the next-safe map. Joint safety is tested initially and after complete
rounds. An overshoot beyond R returns `empty`; none occurred in these fixtures.
Every selected occurrence is recorded and checked not to recur. The occurrence
list supplies a finite execution guard; no universal move bound is assumed.

For each tile word and each anchor label, the verifier rotates the prescribed
word from that label's first occurrence and appends its `q_anchor`-th successor.
It builds each signed contact gap from the two explicit endpoints. It also
constructs endpoint coefficient vectors independently of the expected formula.
The numeric sum and coefficients agree with
`sum_i(q_i*p_i/4)-q_anchor*p_anchor`; every start coefficient cancels.
The supplied q-vector is checked against the actual word counts. Signed
contact gaps are recorded even when zero or negative: an identity is not a
claim that a perturbed inherited word remains a strict chain.

The scalar occupancy calculation explicitly clips intervals
`(m-phase-1/8,m-phase+1/8)` to `[0,x]` and adds their lengths. It compares that
measurement with the formula supplied in the protocol; no optimization over
phases or deduction of the minimum property is performed by this code.

## Exact observations

All actual speed orders in these fixtures are `[0,1,2,3]`.

| Perturbation, in each of the three profiles | First safe time | Advancing labels | Calls | Rounds |
|---|---:|---|---:|---:|
| exact | 0 | empty | 0 | 0 |
| period_first_up | 0 | empty | 0 | 0 |
| period_last_down | 1/4 | 3,0 | 22 | 2 |
| start_first_up | 0 | empty | 0 | 0 |
| start_first_down | 249/1000 | 0 | 11 | 1 |

| Profile | Safe-component counts, in the five protocol perturbation orders |
|---|---|
| equal | 13,10,10,10,9 |
| two_levels | 19,16,13,16,15 |
| one_fast | 19,16,10,16,15 |

There are 207 safe components in total, with no implication that overlapping
or related cases are independent replications. All components and every
threshold classification are retained in `verification.json`.

| x | Measured blocked duration | x/7 | Equality? |
|---:|---:|---:|---|
| 1 | 1/4 | 1/7 | no |
| 7/4 | 1/4 | 1/4 | yes |
| 2 | 1/2 | 2/7 | no |
| 11/4 | 1/2 | 11/28 | no |

## What these checks do not establish

The maximum observed moving-word length is only two. Nine words are empty,
three are `[0]`, and three are `[3,0]`. Their square-free checks are therefore
weak boundary diagnostics, not substantial evidence about long words or a proof
of square exclusion. No more fixtures were added to strengthen that test.

The cycle coefficient cancellations are finite exact algebraic checks on three
declared words. They do not prove that all possible tilings have been classified,
that the claimed compactness argument is valid, that arbitrary real-speed
limits preserve the needed occurrence structure, or that every prescribed
selector has a uniform iteration bound. The occupancy fixtures verify four
scalar evaluations, not the continuum minimum or its inequality for all x.

The iteration/partition agreement is an independently structured calculation
inside this verifier. A comparison with the coordinator's output is a separate
step; no such primary-output comparison is claimed by this note.

## Reproduction and provenance

Run from any directory:

```sh
python /workspace/scratch/4b594c29a5a8/lr-uniform-iteration/reviews/2026-09-28-uniform-iteration/verify.py
```

This rewrites only `verification.json` and prints the summary. It raises an
error for a failed assertion or failed check. Source files read: `protocol.json`
and the verifier's own source for the hash. Repository mathematical helpers
and the primary implementation are not imported.

Protocol SHA-256:
`f0ddb7b2f82af5e812d1b2c31a012e3119fe90e67d209bf664ea0f2e395f9fa2`.

Verifier SHA-256:
`f4696d6ce1aefdaa2d0deb3cc6dc6cccf1f54bc97090728947c3ac34a97e9d6a`.

Pinned research baseline:
`5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.
