# Bounded shifted-start alignment experiment

This review owns only `phase_experiment.py`, `phase_results.json`, and this
report. It implements the thought experiment frozen in `protocol.json`
(SHA256 `f1d4772133a47a3090c5f9f5f3aa6389b378917c0744a80e3df728790e397d7d`).
There are eight runners, reference 0, threshold 1/8, residual speeds
1,4,5,6,7,11, and fastest speed V=13 or V=16. Only offset s=0 has the original
common start. Other offsets change speed 11's starting phase to
`11*s/V mod 1`; they are a different, explicitly shifted-start problem.

## Definitions fixed before computing outcomes

For each m=0,...,V-1, use normalized u in [1/8,7/8]. The unchanged residual
patterns come from lap m; speed 11's pattern comes from `(m+s) mod V`.
All s=0,...,V-1 are evaluated. Blockers are strict, with endpoint membership
preserved after clipping to this closed normalized window. A local allowed
set is labelled `empty`, `contacts_only`, or `positive_duration`; isolated
points remain separate from positive intervals. Global status uses the same
three labels after collecting all laps. Actual time is t=(m+u)/V, so actual
duration is normalized duration divided by V.

The reported earliest changes always mean the least s>0 relative to s=0:
total duration; the vector of local empty/nonempty truth values; the vector
of local three-way statuses; global empty/nonempty; global three-way status;
and isolated-contact count. A missing change is explicitly null. These
diagnostics are not selected after inspecting which offset looks interesting.

For the control, shift all six residual patterns together by the same s,
reconstruct each local allowed set, and compare it to original lap `(m+s)
mod V`. Require exact equality of normalized allowed components, local
status, duration, and contacts, and invariant total duration/contact count.
For every speed, compare the entire multiset of normalized blockers and
their endpoint flags before and after each shift. No pair-moment invariance
is asserted by this preservation check.

## Outcome

**OBSERVED, bounded:** the complete per-runner pattern inventories do not
determine their joint allowed duration or local existence. They also do not
determine whether the full allowed set has positive duration: for V=13 the
common-start input has only four isolated contacts, while every nonzero
offset has positive duration. All 29 arrangements have some allowed time,
so this experiment does **not** separate global existence from nonexistence.

The first nonzero offset s=1 already changes total duration and local
empty/nonempty status in both cases. It changes global three-way status and
contact count only for V=13. For V=16 every offset has positive duration and
no isolated contacts; there is no offset changing those global statuses.
These negative results remain explicit nulls in the archive.

| Case | Offset and speed-11 phase | Actual allowed duration | Isolated contacts | Global status |
| --- | --- | ---: | ---: | --- |
| tight13 | s=0, phase 0 | 0 | 4 | contacts_only |
| tight13 | s=1, phase 11/13 | 1517/48048 | 3 | positive_duration |
| strict16 | s=0, phase 0 | 39/4928 | 0 | positive_duration |
| strict16 | s=1, phase 11/16 | 193/2688 | 0 | positive_duration |

The original V=13 contacts are exactly `{1/8,3/8,5/8,7/8}`. At s=1 the
three isolated contacts are `{1/8,57/104,7/8}`. A directly checked strict
witness for that shifted-start case is `t=4945/13728`; its minimum distance
is `369/2288>1/8`. A corresponding V=16, s=1 witness is `t=277/768`, with
minimum distance `21/128>1/8`. The archive records all seven distances for
each local witness and each isolated contact, evaluated with the shifted
starting phase included.

All outcomes appear below. Apart from V=13 at s=0, every row has positive
duration. Every V=16 row has zero isolated contacts.

| s | V=13 actual duration | V=13 isolated contacts | V=16 actual duration |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 4 | 39/4928 |
| 1 | 1517/48048 | 3 | 193/2688 |
| 2 | 115/2184 | 1 | 193/2688 |
| 3 | 115/2184 | 1 | 251/14784 |
| 4 | 115/2184 | 1 | 2039/29568 |
| 5 | 1223/24024 | 2 | 193/2688 |
| 6 | 761/48048 | 2 | 101/2688 |
| 7 | 761/48048 | 2 | 215/3696 |
| 8 | 1223/24024 | 2 | 7/96 |
| 9 | 115/2184 | 1 | 215/3696 |
| 10 | 115/2184 | 1 | 101/2688 |
| 11 | 115/2184 | 1 | 193/2688 |
| 12 | 1517/48048 | 3 | 2039/29568 |
| 13 | — | — | 251/14784 |
| 14 | — | — | 193/2688 |
| 15 | — | — | 193/2688 |

## Exact local changes and what is preserved

For V=13, lap m=5, the first five residual speeds leave exactly
`[45/56,7/8]` in normalized u. At s=0 speed 11's blocker is
`(67/88,7/8]`, which covers that entire interval. At s=1, the imported
speed-11 pattern comes from original lap 6 and is empty. The allowed set
therefore changes from empty to `[45/56,7/8]`, or
`[25/56,47/104]` in actual time. The exact actual duration of this new
opening is `1/182`. The removed blocker pattern is still present elsewhere
in the offset arrangement; its inventory has not been deleted or shortened.

The same shift can also close a previously successful lap. For V=16, m=4,
the original allowed normalized interval is `[6/7,7/8]`. The original
speed-11 blocker `(2/11,6/11)` misses it; the imported blocker from lap 5 is
`(7/11,7/8]`, which covers it completely. Thus this lap changes from positive
duration to empty. Original lap 5, conversely, becomes positive when the
empty speed-11 pattern from lap 6 moves there. For V=13, m=7, a previously
empty lap gains only the point `u=1/8`, illustrating why endpoint membership
and the third status `contacts_only` must be retained.

For each runner separately, s merely permutes its normalized pattern list;
for the five unchanged residual speeds the permutation is the identity.
The full multiset, including empties, interval endpoints, and endpoint
inclusion flags, agrees exactly over all V laps. Consequently all
single-runner normalized duration inventories and their totals agree too.
What changes is which patterns meet in the same lap. This is a counterexample
to sufficiency of the **unlabelled per-runner inventories** for recovering
joint duration or local existence, not a pair-moment collision. No pair
preservation was checked or claimed for these phase rearrangements.

## All-runner shift control

All 29 all-residual-shift controls pass: every normalized local allowed set,
duration, isolated-contact list, and status equals the original record at
`(m+s) mod V`. The total actual duration remains 0 with four isolated contacts
for V=13, and `39/4928` with none for V=16.

The reason is visible in the phase equations. A common residual shift adds
`v*s/V` to every residual phase, exactly as the common time translation
`t -> t+s/V` does. The fastest phase changes by the integer s and is
unchanged modulo 1. Thus a common shift moves complete lap arrangements
together; shifting only speed 11 changes relative alignment. The calculation
checks this identity on every declared lap and offset, rather than assuming
the control totals alone establish it.

## Reproduction and boundaries

`python -B reviews/2026-09-27-fastest-laps/phase_experiment.py --check`
reconstructs the archive read-only. `--write` creates `phase_results.json`.
The code imports no project helpers, constructs strict blocker intervals
from collision integers, clips with endpoint flags, reconstructs the closed
complement from event vertices/cells, and substitutes all recorded witnesses
directly into the shifted phase equations. Protocol and script hashes are
recorded. There are 29 partial-shift outcomes and 425 local lap calculations,
plus 29 all-shift controls with 425 local comparisons. These overlapping
objects are not independent statistical trials.

The separate `verify_independent.py` implementation uses direct shifted phase
threshold events and reads/imports none of this experiment's code. It agrees
on all 29 offsets, 425 local records, endpoint-aware patterns and source maps,
inventory hashes, full allowed sets, witnesses, contacts, earliest changes,
and all 29 all-shift controls. Its write/check runs passed against
`phase_results.json` SHA256
`612cd4320fc3083476b352f8ce058e345cf2f88a418a36e87228cdbad29c8692`.
This is an independently structured AI computation, not independent human
review or promotion to a general theorem.

This AI-generated review adds no speed configurations or references and
makes no claim about arbitrary initial phases, a common-start counterexample,
general Lonely Runner existence, or novelty. It isolates one precise loss of
information: per-runner inventories discard the shared lap alignment needed
to recover joint coverage.
