# Six-case structural and constructive review

Scope: the six fixed configurations in `protocol.json`, selected reference 0,
eight total runners, threshold 1/8, time interval [0,1]. No added configurations
or reference changes. This report is materially AI-generated and remains a
bounded diagnostic, not a theorem or novelty claim.

## Additional diagnostic fixed before its calculation

This is a **retrospective diagnostic**, additional to the primary experiment;
it does not change any primary selection key or outcome. Before inspecting
the six outcomes, fix the following small constructive candidate list on each
input: `1/(2*v_min)` and `1/(v_i+v_j)` for every unordered pair of its seven
nonreference speeds (at most 22 distinct times). Evaluate all seven distances
exactly at every candidate. Report the counts with minimum distance at least
1/8 and strictly above 1/8, and select the earliest strict candidate if one
exists. Do not add candidate types after seeing the answers.

For a selected strict candidate t, compute
`r=min_i ((dist(v_i*t,Z)-1/8)/v_i)` and give the closed interval
`[t-r/2,t+r/2]`. The distance functions are v_i-Lipschitz, so this interval is
strictly safe for every runner. This elementary interval is deliberately a
local diagnostic; it is not substituted for a complete core component.

Structural comparisons will use the primary rule's selected certificates and
the exact identity between tree slack and integrated active-subgraph
fragmentation. The complete-window restriction will be retained throughout.

## Constructive diagnostic outcome

**OBSERVED:** five of the six cases have a strict witness in the frozen small
candidate list. The squares case has no weak or strict witness there. The
single candidate `1/(2*v_min)` fails even weak safety in all six cases. Thus
failure of the common time 1/8 should not be described as making these inputs
hard, while the failed squares diagnostic prevents claiming this particular
shortcut covers the whole batch.

| Case | Distinct candidates | Strict candidates | Earliest strict t | Minimum distance at t | Certified local interval width |
| --- | ---: | ---: | --- | --- | --- |
| prime_mix | 18 | 4 | 1/60 | 2/15 | 1/960 |
| near_pairs | 18 | 9 | 1/96 | 5/32 | 1/480 |
| fibonacci | 22 | 1 | 1/63 | 8/63 | 1/27720 |
| squares | 21 | 0 | — | — | — |
| prime_powers | 22 | 3 | 1/108 | 4/27 | 7/27000 |
| perturbed_chain | 22 | 2 | 1/46 | 7/46 | 9/18400 |

The prime-mix witness is especially easy to inspect: at t=1/60 the seven
distances are `(8,11,17,23,29,23,17)/60`, all above 1/8. The Fibonacci witness
has the smaller positive margin `8/63-1/8=1/504`. No additional candidate
types were tried after seeing the squares failure. Repeated pair sums explain
why some lists have fewer than 22 distinct times; these are not independent
tests.

The five exact closed strict neighborhoods are, respectively,
`[31/1920,11/640]`, `[3/320,11/960]`,
`[293/18480,881/55440]`, `[493/54000,169/18000]`, and
`[791/36800,809/36800]`. Their endpoint-to-integer minima are checked
independently of the Lipschitz construction, including whether an integer
lies between the endpoints. The full distance lists and every failed
candidate remain in `structure.json`.

## What tree slack measures

Let S(t) be the active residual blockers in a complete core-safe component W,
and let T be one fixed tree on the residual labels. If S is nonempty, its
induced graph is a forest, so it has `|S|-c_T(S)` edges. Therefore

`U(W)-Q_T(W) = integral over {S(t) nonempty} of (c_T(S(t))-1) dt`.

This is the supplied forest-counting argument behind the existing slack
identity; general mathematical promotion still follows the repository's
proof-review rules. The finite checks below have status OBSERVED. Tree
optimization minimizes this integrated fragmentation. A pattern with two
active connected components costs its duration; three components cost twice
its duration. A disconnected active pattern confined to isolated event
vertices does not cost duration. Exactness requires connected active sets
almost everywhere, not one active blocker, and not containment.

This separates three tasks: containment removes redundant labels without
changing the optimal Q; selecting edges reduces fragmentation; selecting W
changes both actual room U and fragmentation. A positive Q only requires
actual room to exceed fragmentation. Maximizing Q need not pick an exact
tree or the smallest residual description.

## Six selected certificates

These are the primary frozen Q choices, reconstructed here from exact
residual threshold events. The independent local reconstruction compares all
16 active-state masses, enumerates all 16 labelled full trees, and checks the
integrated-fragmentation identity. It agrees on every selected certificate.
Indices in the primary archive are translated to speeds below.

| Case | Core speeds | Complete selected W | Q | U-Q | Retained residual speeds |
| --- | --- | --- | ---: | ---: | --- |
| prime_mix | 8,11,29 | [33/232,39/232] | 865/46139 | 0 | 37,43 |
| near_pairs | 15,16,17 | [1/120,7/136] | 1357451/66752455 | 0 | 31,33,47,49 |
| fibonacci | 8,13,21 | [41/104,71/168] | 306451/67104576 | 27/24208 | 34,55,89,144 |
| squares | 8,9,25 | [33/200,39/200] | 2053/200772 | 13991/3312738 | 49,81,121,169 |
| prime_powers | 16,25,27 | [97/216,19/40] | 35029/4704000 | 3189/3136000 | 49,64,81,125 |
| perturbed_chain | 7,23,38 | [41/184,71/304] | 2827/426512 | 0 | 61 |

The exact cases display three distinct sufficient mechanisms:

- **prime_mix:** speeds 17 and 23 vanish. With only 37 and 43 retained,
  one pair edge makes inclusion-exclusion exact, even though blocker 43 has
  two components on W.
- **near_pairs:** all four blockers remain, none vanishes, and no nonempty
  containment holds. The only positive-duration coactive pairs are
  `{31,33}` and `{47,49}`, with durations `2/341` and `18/2303`.
  Tree edges `31-33`, `31-47`, `47-49` capture both; the middle edge has
  zero overlap. Every nonempty active state is connected in that tree.
  Speeds 47 and 49 each have two blocker components. This is an exact
  physical counterexample to necessity of containment, reduction, or
  single-interval blockers for tree exactness.
- **perturbed_chain:** speeds 8 and 15 vanish, while
  `B100=(183/800,37/160)` is strictly contained in
  `B61=(111/488,113/488)`. Only 61 remains. This reproduces the previous
  containment mechanism without making it a necessary explanation.

For the other three selected windows, all four blockers remain with no
nonempty containment. Their slack has a short exact description:

| Case | Chosen full tree edges | Disconnected active patterns and duration |
| --- | --- | --- |
| fibonacci | 34-144, 55-144, 89-144 | `{34,89}`: 27/24208 |
| squares | 49-81, 49-121, 121-169 | `{49,81,169}`: 29/54756; `{49,169}`: 31/39204; `{81,121}`: 73/39204; `{81,169}`: 19/18252 |
| prime_powers | 49-64, 49-81, 81-125 | `{49,125}`: 23/24500; `{64,125}`: 1/12800 |

Each displayed pattern has exactly two induced components, so the durations
sum directly to U-Q. For example, the Fibonacci tree's center 144 is safe
while 34 and 89 both block throughout the open cell
`(295/712,113/272)`, whose width is exactly `27/24208`. This pinpoints the
lost information rather than attributing the slack to the case's recurrence
label. The squares case has blocker-component counts 2,2,4,6; its positive Q
survives four disconnected patterns. The prime-powers case has counts
2,2,2,3. These counts explain why the interval sufficient condition is
unavailable on these broad windows, but counts alone do not determine Q.

Across the whole primary archive, 18 positive-duration windows are missed by
trees: eight Fibonacci, four squares, two prime-powers, four perturbed-chain.
The other two cases have no missed positive window. All 35 cores in every
case have a positive certificate somewhere. These overlapping window counts
are bounded observations, not independent trials or an every-core theorem.

## Why arbitrary local cells would make the question trivial

A strict witness has an open neighborhood on which all seven constraints are
safe. On a sufficiently small closed subinterval there, every residual blocker
vanishes and Q equals the interval's positive width, for every core. The five
local intervals above demonstrate exactly this elementary certificate. They
are not substitutions for the protocol's complete core components: allowing
outcome-tailored subdivisions would make conditional existence of a positive
tree certificate automatic by the definition of strict loneliness.

The useful complete-window comparison is therefore whether a broad W offers
more certified duration despite fragmented residual patterns, and whether
choosing a core gives structural control of those patterns.

## Fastest-core mechanism: a stronger structural explanation

The concurrent mathematical review supplies a further proof candidate. Let
V be the largest absolute nonreference speed and use any core containing it.
Each complete core component lies inside one V-safe interval and hence has
length at most `(1-2*delta)/V`. For a residual speed v with `|v|<=V`, two
consecutive strict blocker intervals are separated by a closed safe gap of
length `(1-2*delta)/|v|`, at least as long as W. Consequently its blocker on W
is a single interval or empty. Equality at the threshold cannot add blocked
endpoints to defeat this conclusion.

For a finite family of intervals, sort by left endpoint and attach each new
interval to an earlier interval with greatest right endpoint. Its intersection
with the entire preceding union has the same measure as its intersection
with that parent. If they are disjoint the chosen edge contributes zero.
Summing these incremental union lengths gives an exact tree expression.
Thus an optimal tree has Q=U on every fastest-core window. Containment is one
possible simplification, but it is not needed for this interval argument.

If accepted after the required review, this supplies conditional some-core
success whenever a strict lonely time already exists. Even a core consisting
only of the fastest constraint would suffice for the exact-duration identity;
three core runners are not essential to that argument. It does not establish
that any such component has positive U, and hence does not prove Lonely
Runner. The six-case success rate would then check the implementation of an
explained mechanism, rather than supply independent evidence for a difficult
unbounded some-core selection hypothesis.

The distinction from the arbitrary-local-cell observation matters: fastest
safe windows are chosen from the input before knowing the full allowed set.
They create a useful interval representation by controlling length, without
assuming a known strict witness. Their number and detailed endpoints still
depend on speeds; this is not a speed-independent complexity bound.

The primary per-core records corroborate this explanation on all 8,800
components belonging to the 90 fastest-containing three-cores: every one has
Q=U, and every such core has at least one positive component. This aggregation
uses primary summaries; this review independently reconstructs only the six
Q winners, while the dedicated independent verifier covers the entire
primary enumeration.

Nevertheless, none of the six Q winners contains the fastest runner. Every
selected W is wider than a single fastest-runner safe interval, and its Q
strictly exceeds the best Q among the 15 fastest-containing three-cores:

| Case | Selected Q | Best fastest-containing three-core Q |
| --- | ---: | ---: |
| prime_mix | 865/46139 | 26/1591 |
| near_pairs | 1357451/66752455 | 1/105 |
| fibonacci | 306451/67104576 | 287/102528 |
| squares | 2053/200772 | 3/676 |
| prime_powers | 35029/4704000 | 7/1500 |
| perturbed_chain | 2827/426512 | 279/48800 |

This is a concrete role for the broader quantitative search: it can collect
more certified duration into one complete component, tolerating fragmentation
in three cases. It is not required merely to obtain conditional some-core
success. The comparison is specifically to fastest-containing three-cores;
no singleton-fastest-core experiment was run here.

## A focused next experiment

Further success counts would add little to the conditional some-core claim.
The remaining useful target is an arithmetic reason that at least one
fastest-safe lap escapes complete coverage. A bounded next mechanism study
could use only the existing squares input: decompose the 169 fastest-safe
laps using the singleton fastest core, record the greedy interval-cover
chains of the six residual blockers, and compare chains that reach the
right endpoint with those that leave a gap. The concrete question is whether
a repeated integer-lap endpoint relation explains a forced gap across laps,
rather than only certifying a gap after it is found. This is proposed work,
not performed here; the singleton core differs from the frozen primary
three-core protocol. Failure to find such a relation should leave the
positivity question open, not prompt a retuned list of speed configurations.

## Reproduction and limits

`python -B reviews/2026-09-27-team/structure_check.py --check` regenerates the
reciprocal-time diagnostic and six selected-certificate reconstructions using
Python rational arithmetic and no project imports, comparing against
`structure.json` without modifying it. `--write --include-primary` overwrites
that owned diagnostic archive. Protocol, primary result, and checker hashes
are recorded. `protocol.json` supplies
the exact scope and declared baseline; the local workspace did not expose a
Git repository from which to verify a live HEAD.

No new configurations, references, retuned inputs, extra candidate types,
broader search, external publication, or claim of novelty were added.
