# Eight explicit cores: two components still suffice, with an anchor caveat

October 17, 2026. **OBSERVED:** with the widest component required, the exact
minimum is one for the consecutive core and two for the other seven cores.
All eight lie outside the specified p,q template. No natural residual-cover,
no-cover or budget outcome occurred. This broadens the tested inputs but does
not establish a general two-component theorem.

**A consequential limitation:** all eight selected cores happen to admit
t=1/10. Six of the seven nonempty leader-exception lists are also repaired at
that same time. The test removed one structural restriction while retaining
another. This retrospective finding is preserved, not presented as a frozen
prediction. The powers-of-two case supplies a boundary to that explanation:
its exception r=10 blocks t=1/10, while t=11/80 repairs its entire exception list.

Execution freeze: `e72faca03468bb2e4a5aa284b098a6dfe15791f9`, with 18 pinned
files. Source: `12ef6a5daa07f37176744ef866830507393ea4e4`.
[Protocol](PROTOCOL.md), [inputs](config.json), [runner](run.py),
[alternate verifier](verify.py), [manifest](manifest.json).

## Scope and exact outcomes

Every row has stationary reference 0, eight distinct positive integer core
speeds of gcd one, common start and d=1/10. Adding a positive integer speed
r absent from the core gives n=10. No other-reference or general LRC claim is
made. Ordered p,q candidates from each input set give 64 exhaustive template
checks per core; none matches the earlier coefficient construction. This
excludes that exact template, not every symmetry or earlier appearance.

| Core | Eight speeds | Complete components | Finite cutoff R | Finite cases | Minimum with leader |
|---|---|---:|---:|---:|---:|
| Consecutive | 1,2,3,4,5,6,7,8 | 8 | 16 | 7 | 1 |
| Odd | 1,3,5,7,9,11,13,15 | 13 | 4 | 1 | 2 |
| Primes | 2,3,5,7,11,13,17,19 | 20 | 12 | 6 | 2 |
| Squares | 1,4,9,16,25,36,49,64 | 40 | 18 | 13 | 2 |
| Powers of two | 1,2,4,8,16,32,64,128 | 72 | 37 | 30 | 2 |
| Fibonacci | 1,2,3,5,8,13,21,34 | 22 | 16 | 9 | 2 |
| Clustered | 11,12,13,17,19,23,29,31 | 30 | 11 | 10 | 2 |
| Irregular | 3,8,14,27,35,46,62,89 | 58 | 37 | 31 | 2 |

Components include closed intervals and singletons. R=ceil(2d/leader width);
the finite cases are exactly admissible 1<=r<R. All 107 complete child sets
are nonempty. The width argument supplies r>=R, including equality. Combined
all-r conclusions remain **same-author proof candidates awaiting independent
review**. No minimum among menus that omit the required leader was computed.

IDs index the complete core in increasing time. Each selected menu matches
the full reference minimum and its lexicographic tie-break.

| Core | Leader ID | Leader interval | Leader failures | Selected IDs | Optional common repair time |
|---|---:|---|---|---|---|
| Consecutive | 0 | [1/10,9/80] | none | [0] | not attempted |
| Odd | 6 | [71/150,79/150] | 2 | [0,6] | 1/10 |
| Primes | 6 | [41/170,49/190] | 4,8 | [0,6] | 11/170 |
| Squares | 18 | [41/90,299/640] | 2,13 | [0,18] | 1/10 |
| Powers of two | 1 | [131/1280,69/640] | 9,10,19 | [1,3] | 11/80 |
| Fibonacci | 5 | [91/340,59/210] | 11 | [0,5] | 1/10 |
| Clustered | 0 | [1/110,9/310] | 1,2,3 | [0,2] | 1/10 |
| Irregular | 15 | [121/460,239/890] | 4,15 | [0,15] | 11/270 |

The selected repairs for odd, squares and clustered are the singleton
{1/10}. Dropping isolated components would remove those selected witnesses.
This is not a claim that all alternative menus need a singleton: every finite
child has some positive-width source contact in the saved reference table.
The complete cores contain 22 isolated and 241 positive-width components.

## What the anchor view adds

At t=1/10, an integer speed v has phase (v mod 10)/10. At d=1/10 it is safe
exactly when 10 does not divide v; residues 1 and 9 count by equality. Every
chosen core satisfies this condition, which was not a selection criterion.

Once the full finite leader-failure list F is known, a core-safe time 1/10
repairs F exactly when no member of F is divisible by 10. That criterion holds
for odd, primes, squares, Fibonacci, clustered and irregular. It also holds
vacuously for the consecutive core, whose leader already suffices. It fails
for powers of two because 10 belongs to F. The different point 11/80 works
there, as the frozen construction and verification establish.

For primes and irregular, the component containing 1/10 has ID 1 and 6,
respectively, whereas the constructor chooses the earlier component 0. Thus
the anchor gives a simpler explanation of sufficient coverage without claiming
to reproduce the lexicographically selected menu. Four of the seven actual
repair points equal 1/10; six exception lists could instead use that time.

[inspect_anchor.py](inspect_anchor.py) and its
[source-bound diagnostic](results/ANCHOR_DIAGNOSTIC.json) were added **after
outcomes**. They read the saved geometry, compare source membership with exact
physical phases, and check the residue condition. They run no new core or
contact search and are not part of the 18-file execution freeze. This is a
retrospective interpretation, not held-out validation of a newly tuned rule.
It reuses the ordinary rational-anchor viewpoint developed in the earlier
[placement study](../placement/RESULTS.md); no new language or novelty claim.

This is an example of productive representation choice: component incidence
finds a small menu, while residues expose a common reason for several
successes and a limitation in the input selection. Neither view alone retains
the complete geometry or supports arbitrary changes of constraints.

## Work and verification

| Core | Leader contacts | Lazy contacts | Constructor total | Full reference contacts |
|---|---:|---:|---:|---:|
| Consecutive | 7 | 0 | 7 | 56 |
| Odd | 1 | 1 | 2 | 13 |
| Primes | 6 | 2 | 8 | 120 |
| Squares | 13 | 2 | 15 | 520 |
| Powers of two | 30 | 6 | 36 | 2160 |
| Fibonacci | 9 | 1 | 10 | 198 |
| Clustered | 10 | 4 | 14 | 300 |
| Irregular | 31 | 2 | 33 | 1798 |
| **Total** | **107** | **18** | **125** | **5165** |

These are first-pass operation counts, not timings or total project work.
Complete core construction uses 1,162 input bands and yields 263 components;
the reference reconstructs those cores and all 107 complete child sets. No
constructor residual contacts, cache reuses or DP searches were needed. The
full reference DP performs 885 transitions, with peak states per case
1,2,3,4,6,2,4,4. These DP counters are execution instrumentation.

Optional common searches use 14 point probes, all at the selected component's
left endpoint; no gap jumps occur. Certificates store 14 exception witnesses.
Dispatch emits 107 finite and 31 tail-control witnesses, using 93 and 31 fresh
leader-contact calls respectively. All 16 invalid-query guards reject. Tail
controls are spot checks; the width argument, not large tested speeds,
supports the infinite extension.

[Alternate verification](results/VERIFICATION.json) passes 8 complete cores,
107 complete child sets, 5,165 reference contacts, 125 constructor contacts,
383 physical witness records, 256 minimum-search subsets and 7 complete
optional common sets. It reconstructs geometry with threshold events and
minimum menus with subset enumeration, importing neither the primary checker
nor constructor. Shared prior verifier helpers and the same AI author limit
independence; this is not human or formal proof review.

[Replay](results/REPLAY.json) is byte-identical on Python 3.12.14. No frozen
source changed, execution discrepancy, timeout, or budget stop occurred.
The earlier seven supplied-interval semantic controls were not rerun; their
existing frozen evidence remains in the source study. No fresh physical case
exercised three-component fallback or separate-versus-common repair failure.

## Reproduction and artifacts

From repository root, using fresh output/checkpoint paths:

```sh
timeout 240s python experiments/runner-addition/outside-template/run.py --freeze e72faca03468bb2e4a5aa284b098a6dfe15791f9 --output /tmp/outside-results.json --checkpoint-dir /tmp/outside-checkpoints
timeout 240s python experiments/runner-addition/outside-template/verify.py --input /tmp/outside-results.json --output /tmp/outside-verification.json
timeout 240s python experiments/runner-addition/outside-template/run.py --freeze e72faca03468bb2e4a5aa284b098a6dfe15791f9 --output /tmp/outside-replay.json --checkpoint-dir /tmp/outside-replay-checkpoints
cmp /tmp/outside-results.json /tmp/outside-replay.json
python experiments/runner-addition/outside-template/inspect_anchor.py --input /tmp/outside-results.json --output /tmp/outside-anchor.json
```

[Complete results](results/RESULTS.json), 766,526 bytes, SHA-256:
`021dc797d191b5b5d2d5c40004b0944d45872c6878058d9af45a35c7a8d46f4c`.
[Certificates](results/CERTIFICATES.json) are a post-verification extraction
bound to that source hash. Completed per-case checkpoints were retained during
execution; the committed aggregate contains every case in order.

**Next proposed:** freeze a small paired test that deliberately removes the
shared time 1/10 by including a speed divisible by 10, while retaining distinct
primitive cores outside the old template. Specify the pairing using input
arithmetic before geometry. Compare leader failures, required-leader minima,
repair locations and full geometry; retain any unresolved or larger-menu
outcome. This tests dependence on the observed anchor, not all possible
rational anchors. No such new input set has been selected or evaluated.
