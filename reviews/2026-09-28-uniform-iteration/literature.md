# Bounded literature audit: critical density and projection termination

2026-09-28. Agent 5; material AI-assisted literature inspection and deductions.
Pinned task baseline: `5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.
Repository convention: `k` moving constraints relative to one reference; here
`k=4`, threshold `delta=1/(2k)=1/8`. Equality is safe.

**Result:** the integer-speed, arbitrary-phase existence statement at this
threshold is **KNOWN** (Schoenberg's theorem, with an elementary proof reproduced
by Beck–Hoşten–Schymura). A straightforward endpoint-counting deduction proves
next-safe termination and gives another speed-dependent bound. That deduction is
recorded below as a **HYPOTHESIS / proof candidate** pending independent review.
This audit did not establish an existing answer to the particular uniform
scalar-move or prescribed-round question. That is a limit of this bounded audit,
not a claim that the question is new or open in the literature.

## 1. Primary sources and precise inspection limits

### A. The shifted critical threshold, with a complete elementary proof

Matthias Beck, Serkan Hoşten, Matthias Schymura, *Lonely Runner Polyhedra*,
Integers 19 (2019), A29. Published 2019-06-03; arXiv v4 dated 2019-03-05.

- Official journal PDF: <https://math.colgate.edu/~integers/t29/t29.pdf>
- Version metadata: <https://arxiv.org/abs/1606.01783v4>
- Inspected: Section 6, printed pp. 11–12; Theorem 4 and its complete proof on
  p. 12; PDF p. 12 also visually checked. Metadata and relevant references read.

Theorem 4, attributed there to Schoenberg (1976), says: for positive integers
`n_1,...,n_k` and arbitrary real `s_1,...,s_k`, some real `t` satisfies
`||s_j+t n_j|| >= 1/(2k)` for every j. Repeated speeds are allowed. The proof uses
the union bound for smaller thresholds and compactness at equality; periodicity
allows `t in [0,1]`. Equal unit speeds with equally spaced phases prove sharpness
in that scope. Here the paper's `n_j` are our `v_j`, and its `k` is our `k`.

The p. 11 question concerns bounded **physical laps**, not projection calls.
Schoenberg's original article was not inspected: *Extremum problems for the
motions of a billiard ball. II. The L-infinity norm*, Indag. Math. 38 (1976),
263–279. We cite the inspected theorem/proof rather than pretend to have checked
that original article.

### B. Covering-language exposition of the familiar threshold

Terence Tao, *Some remarks on the lonely runner conjecture*, author exposition,
2017-01-10.

- <https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/>
- Associated paper metadata: <https://arxiv.org/abs/1701.02048v4>, v4 dated
  2017-11-02; Contributions to Discrete Mathematics 13(2) (2018), 1–31.
- Inspected: exposition's definitions, Proposition 2 and proof, and the ensuing
  overlap/multiplicity discussion; associated paper's metadata/abstract only.

The exposition defines periodic Bohr blockers, each of measure `2 delta`, and
obtains the standard lower bound `1/(2n)` by the union bound. Its `n` counts
nonzero relative velocities, so translate it to our `k`. It also discusses
near-equality in the union bound through the coverage multiplicity and higher
intersections. This supplies context for excess-coverage accounting; it does
not supply the local potential formula or an iteration-count theorem.

### C. Directly relevant prior art on compatible interval chains

Ludovic Rifford, *On the time for a runner to get lonely*,
arXiv:2111.13688v2, 2022-02-16.

- <https://arxiv.org/html/2111.13688v2>
- <https://arxiv.org/abs/2111.13688v2>
- Inspected: introduction/Theorems 1–2/Proposition 1; Section 2.2,
  Definitions 4–6 and Propositions 4–5, including proofs; Section 3.3's Lemmas
  1–2; Section 4.1's weak-chain definitions, Lemmas 6–12 statements and portions
  of their proofs; Section 6 Proposition 9 statement. Computer enumerations
  were not reproduced and the full paper was not audited.

Definition 5 requires an irredundant chain with separated nonadjacent intervals.
Proposition 5 forbids equal adjacent labels and requires the middle speed of
an `ABA` subchain to be smaller. Section 4.1 studies compatible successive weak
subchains at threshold `1/6`. His `d` is dimension after normalizing a slowest
runner; there are `d+1` moving constraints, not `d`.

Proposition 1 gives common-start loneliness at least `1/(2m-1)` within one lap
of the slowest of `m` moving runners. These are physical laps, not selector
rounds. The inspected results do not state a bound for our prescribed
next-safe iteration.

### D. Scope check: finite verification is a different kind of bound

Romanos Diogenes Malikiosis, Francisco Santos, Matthias Schymura,
*Linearly-exponential checking is enough for the Lonely Runner Conjecture and
some of its variants*, arXiv:2411.06903v2, 2025-06-21;
Forum of Mathematics, Sigma 13 (2025), e164.

- <https://arxiv.org/html/2411.06903v2>
- <https://arxiv.org/abs/2411.06903v2>
- <https://doi.org/10.1017/fms.2025.10107>
- Inspected: introduction through the shifted formulation and main finite-check
  statements; relevant bibliography. Proofs of finite reduction not audited.

Their `n` is our `k`. The introduction explicitly identifies `1/(2n)` as the
optimal shifted bound when equal speeds are permitted, and points to source A,
Theorem 4. Their bounded-speed reduction concerns existence of counterexamples
to loneliness assertions. It is not a bound on the number of projections taken
by an arbitrary input's specified algorithm. Their shifted finite-reduction
claim carries a stated Lonely Vector Problem hypothesis; no unconditional
algorithmic consequence is extracted here.

## 2. Elementary termination consequence and a simpler baseline

The following is our deduction, not a quotation or theorem attributed to any
source. Fix positive integer speeds `v_1,...,v_k`, real phases `alpha_i`, an
arbitrary starting time L, and threshold `delta=1/(2k)`. Put

```
g = gcd(v_1,...,v_k),     P = 1/g,
S = {t : ||v_i t + alpha_i|| >= delta for all i}.
```

Apply source A to integer speeds `v_i/g` and shifted phases `alpha_i+v_i L`.
There exists a joint-safe time in `[L,L+P]`. Since S is closed, its first member
T at or after L exists and also lies in that interval.

Define `P_i(t)` as the least time at least t safe for constraint i. If
`t <= T`, then `t <= P_i(t) <= T`; hence any sequence of such projections never
overshoots T. Every advancing move ends at a right blocking endpoint

```
r_(i,m) = (m + delta - alpha_i)/v_i.
```

The endpoints of type i form an arithmetic progression of spacing `1/v_i`.
Exactly `v_i/g` of them lie in any half-open interval `(L,L+P]`. Consecutive
advancing moves have strictly increasing endpoint times, so no endpoint time
is revisited. Counting endpoints with multiplicity is a valid upper bound.
Consequently the total number N of advancing moves satisfies

```
N <= sum_i v_i/g.
```

A repeated finite schedule visiting every constraint cannot remain at an unsafe
point without advancing: a visit to a currently blocking constraint moves.
Thus a schedule testing joint safety after each round terminates after at most
`sum_i v_i/g` rounds that begin unsafe. For the prescribed eleven-call round,
this gives at most `11 sum_i v_i/g` calls from an unsafe start. If the start is
already jointly safe, return immediately. Rational speeds reduce to this case
by a common time rescaling; arbitrary real phases need no rationality.

This deduction explains why termination in the physical integer-speed scope
already follows elementarily from a known threshold theorem. The earlier
potential/overlap-quantum argument can still provide a different bound and
local accounting; this note makes no novelty claim for either argument. Both
bounds depend on the input speeds. In a supplied core-safe window `[L,R]`, the
iteration must still check whether its first residual-safe time exceeds R.
The known global existence theorem says nothing about remaining inside that
particular window.

## 3. What does and does not transfer to uniform iteration

Rifford's chain framework is a close structural precedent and deserves explicit
credit whenever compatible occurrence words or transitions are studied here.
Its irredundancy condition is stronger than the selected chain of advancing
projections: the latter can retain redundant blockers. Removing intervals may
shorten a geometric covering chain without shortening the actual algorithm's
itinerary. A proof about the actual selector therefore needs its own charging
or simulation argument before importing irredundant-chain restrictions.

An elementary version of the local `ABA` geometry is worth retaining as a
proof candidate: if one B-blocker bridges the safe gap between distinct
A-blockers, then `2 delta/v_B > (1-2 delta)/v_A`. At `delta=1/8` this requires
`v_A > 3 v_B`. This inequality does not by itself bound a long word containing
three or four labels.

Neither a uniform physical-time bound nor a finite reduction to bounded
counterexample velocities bounds how many endpoints a specific next-safe
algorithm can visit. A time interval of controlled length may contain many
fast-runner endpoints. Conversely, a uniform call theorem would be stronger
algorithmic information than merely proving a witness exists in that time.
This audit found no inspected statement resolving that distinction for the
specific four-constraint schedule. No conclusion about novelty or global
literature status follows from that nonfinding.

## 4. Audit budget and reproducibility

Six targeted queries were used, followed by primary-source opens/finds:

1. `"shifted lonely runner" "1/(2"`
2. `"lonely runner" "algorithm" "jump"`
3. `shifted lonely runner union bound 2n trivial bound`
4. `lonely runner next safe time algorithm intervals covering chasing`
5. `"lonely runner" "algorithm" "intervals"`
6. `"periodic" "interval" "covering" "density" lonely runner`

Queries 1 and 6 had poor precision. No further broad searches, novelty sweep,
frontier-status sweep, external outreach, or numerical scan was undertaken.
Search snippets from other papers were not treated as established results.
Four substantive primary source documents/expositions were inspected (A–D);
Tao's linked paper was opened only for metadata. Failed arXiv HTML/PDF opens for
source A were replaced by its official journal PDF. Historical statements of
conjecture status were not promoted to claims about the present frontier.
