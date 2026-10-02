# Exact physical optimum cross-check

Date: 2026-09-29. Frozen candidate commit specified by the review protocol:
`8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Result: no discrepancy in the assigned physical checks.** A freshly authored
opposing-contact implementation recovers the archived maximum and **complete
set of maximizing times** for every prescribed integer `q=2,...,25`. All six
prescribed large inputs `q=100002,...,100007` pass exact actual-phase witness
checks, covering every residue modulo six. Those six checks establish the stated
lower bounds only; no large-input exhaustive optimum calculation was performed.

This is bounded exact reproduction by a separately tasked internal AI reviewer.
It is not external human review, a formal proof certificate, or a proof of the
unbounded spectrum formula. The universal geometric and symbolic arguments
belong to the other review assignments.

## Scope and implementation separation

For seven speeds relative to selected reference 0,

\[
V(q)=(1,q,q+1,q+2,q+3,2q+3,2q+5),\qquad
f_q(t)=\min_{v\in V(q)}\|vt\|,\quad 0\le t\le1,
\]

`physical_check.py` evaluates the actual physical phases `vt-floor(vt)` using
Python's standard-library `fractions.Fraction`. It imports no project
mathematical code. It uses neither ambient coordinates nor the fixed-cell
selector, and it does not partition the time axis at runner breakpoints or
enumerate affine-line intersections within such a partition.

I read the displayed candidate theorem and the protocol, then wrote and ran the
fresh checker before opening archived `verification.json`. The first completed
checker, before the comparison adapter, had SHA-256
`93e2282eb42f611be5e70f9c61028d3a6f8ce0cd7d9ab6e7e3bfe0d981e1234a`.
Only afterward was an archive-format adapter added. In every current run,
the archive is read after all fresh small-case calculations and large witnesses
have finished. It supplies no candidates, bounds, arithmetic, or stopping rule.
The original `verify.py`, `ambient.py`, and `audit.py` were never read or imported
by this reviewer. This is not a blinded review: the formula, scope, and exceptional
cases were known from the candidate note.

The implementations still share Python integer arithmetic and
`fractions.Fraction`. A defect in that arithmetic dependency could affect both.
Separate program structure and reviewer assignment do not create independent
human authorship or formal verification. AI materially authored this derivation,
checker, comparison, and report.

The mounted snapshot has no `.git` metadata. The coordinator separately reports
checking the frozen GitHub HEAD, the candidate note's Git blob, and all nine
archived manifest hashes. This review records hashes of its own checker,
protocol, candidate note, and comparison archive in `physical_check.json`; it
does not claim to have independently repeated the coordinator's remote check.

## Completeness of the candidate set

The following argument applies directly to any finite list of positive integer
speeds, so it includes every case in the assigned family.

1. Each tent `d_v(t)=||vt||` is continuous, with slope `+v` when its phase is
   strictly between 0 and 1/2, and slope `-v` when its phase is strictly between
   1/2 and 1. Its upward corners have value zero and its downward corners have
   value 1/2. The continuous minimum of finitely many tents attains its maximum.
2. That maximum is positive: at `t=1/(4 max(V))`, every phase lies in `(0,1/4]`.
   Thus no maximizing time can have an active tent trough, and neither endpoint
   0 nor 1 can maximize. The code nevertheless includes both endpoints.
3. If an active tent is at its peak, the time is
   `t=(2j+1)/(2v)` for some `j=0,...,v-1`. The code explicitly enumerates **every
   individual runner peak**, independently of the contact calculation. Omitting
   this branch would leave a completeness gap for general integer-speed inputs,
   including a maximum of 1/2.
4. Otherwise every active tent is locally affine with nonzero slope. Inactive
   tents have a strictly positive gap above the minimum; finiteness and
   continuity keep them inactive in a sufficiently small neighborhood. If all
   active slopes were positive, moving slightly right would increase the
   minimum. If all were negative, moving slightly left would increase it. At an
   interior maximum there must therefore be an active rising tent with speed
   `v` and an active falling tent with distinct speed `w`.
5. At such a contact the two phases are `z` and `1-z`, where
   `0<z<1/2`. Adding their physical phase equations gives
   `(v+w)t=N` for an integer `N`. Since the time is interior,
   `N=1,...,v+w-1` exhausts the possibilities. For every unordered speed pair the
   code generates exactly these rational times, checks the actual two phases,
   and retains either strict opposing orientation. Phase-zero contacts are
   correctly excluded by positivity; phase-1/2 contacts are already covered by
   the individual peak branch.

Consequently **every** maximizing time lies in the finite union of the retained
opposing contacts, all individual peaks, and the endpoints. At each candidate,
the program computes all seven actual distances and takes their exact minimum.
Taking the largest value and retaining every tied candidate recovers the
complete maximum and maximizing-time set. This also rules out a missed flat
interval of maximizers: every point of such an interval would have to lie in
the same finite candidate set. No grid resolution, tolerance, proposed formula,
or ambient certificate enters this conclusion.

This deliberately speed-dependent algorithm is an audit oracle, not an
alternative claim of a bounded-operation witness selector.

## Small-input results

All entries agree exactly with archived `verification.json`. Times are in the
closed period `[0,1]`; no symmetry reduction is used in the calculation.

| q | Maximum | All maximizing times |
| --- | --- | --- |
| 2 | 1/6 | 1/6, 5/6 |
| 3 | 1/7 | 1/7, 2/7, 3/7, 4/7, 5/7, 6/7 |
| 4 | 1/8 | 1/8, 3/8, 5/8, 7/8 |
| 5 | 3/20 | 9/20, 11/20 |
| 6 | 2/13 | 4/13, 9/13 |
| 7 | 1/6 | 1/6, 5/6 |
| 8 | 1/6 | 1/6, 5/6 |
| 9 | 3/19 | 6/19, 13/19 |
| 10 | 1/7 | 1/7, 2/7, 3/7, 17/35, 18/35, 4/7, 5/7, 6/7 |
| 11 | 3/19 | 9/19, 10/19 |
| 12 | 4/25 | 8/25, 17/25 |
| 13 | 1/6 | 1/6, 5/6 |
| 14 | 1/6 | 1/6, 5/6 |
| 15 | 5/31 | 10/31, 21/31 |
| 16 | 5/33 | 10/33, 23/33 |
| 17 | 9/56 | 27/56, 29/56 |
| 18 | 6/37 | 12/37, 25/37 |
| 19 | 1/6 | 1/6, 5/6 |
| 20 | 1/6 | 1/6, 5/6 |
| 21 | 7/43 | 14/43, 29/43 |
| 22 | 7/45 | 14/45, 31/45 |
| 23 | 6/37 | 18/37, 19/37 |
| 24 | 8/49 | 16/49, 33/49 |
| 25 | 1/6 | 1/6, 5/6 |

The 24 cases contain 60 maximizing-time occurrences. In particular, the six-way
tie at q=3, the eight-way tie at q=10, and the four isolated maximizing times at
q=4 are all preserved. Since the q=4 maximum equals 1/8, those four times are
also its complete 1/8-safe set. No continuum of equality witnesses was lost.

Across these cases, the checker processes 17,208 speed-sum integer candidates
with pair multiplicity, retains 16,824 strict opposing-contact occurrences,
adds 2,952 individual peak occurrences, and evaluates 12,042 distinct
candidate-time occurrences including endpoints. These are processing counts;
they are not independent samples or independent replications. Full exact
phases, distances, physical lap labels, active speeds, and candidate origins
are retained at every maximizing time in the JSON output.

## Six large witness controls

For each row, the checker evaluates only the displayed time, verifies all seven
actual phases lie in `[z,1-z]`, and verifies that their minimum distance is
exactly `z`. It does not enumerate contacts, peaks, time cells, or alternative
times for any large input.

| q | q mod 6 | Witness t | Exact actual minimum z |
| --- | --- | --- | --- |
| 100002 | 0 | 66668/200005 | 33334/200005 |
| 100003 | 1 | 1/6 | 1/6 |
| 100004 | 2 | 1/6 | 1/6 |
| 100005 | 3 | 66670/200011 | 33335/200011 |
| 100006 | 4 | 66670/200013 | 33335/200013 |
| 100007 | 5 | 75006/150013 | 25002/150013 |

The two pre-existing large controls, q=100003 and 100004, also match the archived
witness times, claimed values, and all seven distances. The other four controls
exercise the nonconstant branches missing from the original large-input check.
Agreement with a proposed optimum at one time verifies attainability, not the
matching global upper bound.

## Reproduction and limits

From the repository root:

```bash
python3 reviews/2026-09-29-ltcm-ultra-review/physical_check.py
```

The command writes only `physical_check.json` in the new review directory.
The final run passed all formula, full maximizing-set, reflection, and witness
comparisons. No other physical q values, speed families, reference runners,
existing checker tests, or broad searches were evaluated. Original proof files
and continuity files were not modified, and no publication or merge was made.

No adverse mathematical finding arose in this assigned computation. The
remaining material limitation is the distinction between these exact finite
cross-checks and the unbounded theorem: only the separately reviewed symbolic
argument can establish the spectrum for every integer q>=2.
