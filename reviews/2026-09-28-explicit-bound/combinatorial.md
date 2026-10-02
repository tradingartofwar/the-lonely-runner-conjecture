# An explicit finite-state bound from strict return inequalities

**Completion note:** Sections 1–6 preserve the independently derived weaker
bound. The stronger current candidate is 39, audited in Section 8; Section 9
checks the sufficient core-window corollary.

Date: 2026-09-28. Pinned live baseline supplied by the coordinator:
`99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / proof candidate, materially AI-derived, pending
independent mathematical review.** No word enumeration, speed/phase scan,
new physical fixture, executable check, or novelty claim is used here.
The proof below is analytic. It applies to four arbitrary shifted positive
periodic trains of duty `1/4`, including equal periods. Its conclusion is
about the actual selected chain, without an irredundancy assumption.

**Independent combinatorial fallback:** every strictly overlapping chain with strictly
increasing right endpoints has at most **2,923 selected occurrences**.
This applies globally, hence also to the requested comparable regime
`p_i in [1/4,1]`. The previously derived bound 175 remains sharper when the
largest/smallest period ratio is at least four.

**Subsequent team result:** the period-averaging argument in `geometry.md`
gives the stronger global constant **39**. Sections 8–9 below audit its
combinatorial conversion and the requested sufficient core-window
corollary. The independent finite-state proof is retained in full because
it uses a different mechanism. Neither constant is asserted sharp.

The key additional constraint beyond square-freeness is local and weighted:
between consecutive occurrences of label i, the sum of the intervening
periods must exceed `3 p_i`. Once every label recurs within eight positions,
these constraints define a finite directed graph. Its cycles are impossible
by summing four strict inequalities. Therefore a valid chain cannot repeat
a state of seven trailing labels.

## 1. Definitions and the strict return inequality

Write the occurrence intervals as

`I_(i,m) = (s_i + m p_i, s_i + (m+1/4) p_i)`, with `p_i > 0`.

Let a chain have labels `w_1,...,w_N`, left endpoints `L_j`, and right
endpoints `R_j`, satisfying, for every `2 <= j <= N`,

`L_j < R_(j-1) < R_j`.

Its endpoint increment consequently satisfies

`0 < R_j - R_(j-1) < p_(w_j)/4`.                         (1)

Consecutive selected occurrences of the same label cannot be adjacent in
the word: two distinct occurrences have right endpoints at least one whole
period apart, whereas (1) would give a separation below a quarter period.
Thus every adjacent pair of word labels is different.

Suppose positions u and v, with `u < v`, are consecutive appearances of
label i in the selected word. They need not be consecutive occurrences of
that periodic train: skipping laps is allowed. In either case

`R_v - R_u >= p_i`.

Telescoping (1) gives

`p_i <= R_v-R_u < (p_i + sum_(u<j<v) p_(w_j))/4`,

and hence

`sum_(u<j<v) p_(w_j) > 3 p_i`.                           (2)

This is a necessary inequality, not a claim of sufficiency for realizing
the word. Its strictness follows from strict overlaps. Endpoints that merely
touch do not satisfy it.

## 2. Every eight-label factor contains all four labels

For completeness, the prior three-label bound has the following direct
proof for the actual selected chain.

For a chain using two labels with periods `p >= q`, label p can occur at
most once. Otherwise take two consecutive selected p occurrences. Their
safe gap between the right endpoint of the first and the left endpoint of
the next has length at least `3p/4`. The intervening q-only subchain has at
most one occurrence, of width `q/4 <= p/4`, and cannot bridge that gap.
There is at most one q occurrence on either side of the unique p occurrence.
Thus a two-label chain has at most three selected occurrences, and its
union has length at most `p/4 + q/2`.

For a chain using three labels with periods `p >= q >= r`, suppose p occurs
twice, and take consecutive selected p occurrences. Their safe gap has
length at least `3p/4`. The intervening q,r chain has at most one q and two r
occurrences, so its union has length at most

`q/4 + r/2 <= 3p/4`.

In order to bridge the two p occurrences strictly, that union would contain
both endpoints of the p-safe gap in its interior and hence have length
strictly greater than the gap. This is impossible. Thus p appears at most
once, with a two-label subchain of length at most three on each side. Every
three-label chain has at most seven occurrences.

Every contiguous factor of a selected chain is itself a selected chain.
Therefore, for `N >= 8`,

**Every contiguous block of eight selected labels contains all four labels.** (3)

In particular, after position 8 every newly appended label has a previous
appearance at distance at most eight. This upper bound counts positions,
not elapsed time.

## 3. The seven-letter directed graph

Fix the four positive periods for the remainder of the argument. Consider
the directed graph whose vertices are seven-letter words over the four
labels with no equal adjacent labels. There are exactly

`4 * 3^6 = 2916`                                             (4)

such vertices. We allow a directed edge

`s_1...s_7  ->  s_2...s_7 x`

only if the target is also a vertex and both following conditions hold:

1. The eight-letter word `s_1...s_7 x` contains all four labels.
2. Let B be the suffix of `s_1...s_7` strictly after its last x, if x occurs
   in that word; if x is absent, put `B=s_1...s_7`. Require

   `sum_(b in B) p_b > 3 p_x`.                              (5)

The sum in (5) counts letters with multiplicity. This graph is only a
necessary-condition graph. Extra edges or vertices that cannot correspond
to actual chains cause no problem for the upper-bound argument.

An actual chain with `N >= 8` yields a graph walk through the states

`S_n = w_(n-6)...w_n`, for `n=8,...,N`.                     (6)

Each is a vertex. For the edge from `S_n` to `S_(n+1)`, condition 1 follows
from (3). For condition 2, if x occurs in `S_n`, its last appearance there
is its previous appearance in the chain. If x does not occur in `S_n`,
the eight-letter window ending at n contains x by (3), so its previous
appearance is exactly at position `n-7`. In both cases B is precisely the
intervening word between consecutive x appearances. Equation (2) gives
condition 2. Starting the state list at n=8 ensures this preceding
appearance exists even when x is absent from the seven-letter state.

## 4. The directed graph has no directed cycle

Suppose a directed cycle exists. Follow it periodically in both directions,
reading the appended labels. The seven-letter suffix states match under
each shift, so this gives a periodic bi-infinite word satisfying the two
edge conditions at every position. This construction also covers cycles
shorter than seven edges: equality of the suffix states supplies precisely
the required wraparound consistency.

Every eight-letter factor contains all four labels, so all four labels
occur in a period and the distance between consecutive appearances of any
label is at most eight. Condition 2 is therefore exactly inequality (2)
for every consecutive pair in this periodic word. When x is absent from a
state, its preceding appearance is exactly eight positions before the
appended x, just as in Section 3.

Let `q_i >= 1` count the appearances of label i in one period. Fix i and
sum (2) over its `q_i` consecutive return gaps around that period, including
the wraparound gap. Each occurrence of every other label j belongs to
exactly one such gap. Consequently

`sum_(j != i) q_j p_j > 3 q_i p_i`.                        (7)

There are four strict inequalities (7), one for each i. Summing them gives

`3 sum_i q_i p_i > 3 sum_i q_i p_i`,

which is impossible. Hence the graph has no directed cycle. The same
argument rules out a positive-length directed closed walk, whether or not
its vertices are all distinct.

This is the step stronger than square-freeness: the forbidden repetition
is any repeated trailing state that respects all intervening weighted
return constraints. It need not be an adjacent square in the original
moving word.

## 5. Explicit count and scope

The actual walk (6) has `N-7` vertices. It cannot revisit a vertex, since a
revisit would give a directed closed walk. Combining with (4),

`N - 7 <= 2916`, and therefore **`N <= 2923`**.              (8)

If `N < 8`, (8) holds trivially. This is a deliberately coarse finite-state
count, derived before any word enumeration. No compactness, tiling
classification, phase recurrence, Diophantine approximation, or distance
from a critical tiling is required.

The argument does not use comparable periods; it gives the same explicit
number for all positive periods and shifts. Combining it with the prior
large-ratio result gives the piecewise candidate

- largest/smallest period ratio at least four: `N <= 175`;
- all other ratios: `N <= 2923`.

Both count selected occurrences/advancing moves, not stationary scalar
calls. A conversion to a specified repeated projection schedule must be
stated separately. These four-train assertions do not settle the full
eight-runner core/window problem or the full Lonely Runner Conjecture.

## 6. A redundant eight-state version for indexing review

A less economical proof can retain the last eight labels, all four of
which are present. Each next-label return inequality then depends on the
state and appended label without the absent-letter case. Repeated states
again give the impossible periodic schedule from Section 4. There are

`4^8 - 4*3^8 + 6*2^8 - 4 = 40824`

eight-letter words containing all four labels, by inclusion-exclusion.
The state list at positions 8 through N again has `N-7` members, yielding
the independently indexed, weaker candidate `N <= 40831`.

This alternative is included to make the seven-state edge convention
auditable. It is an analytic crosscheck, not an independent external proof
review and not evidence that either constant is sharp.

## 7. Review targets and provenance

The substantive review targets are the strict gap-bridging proof of the
three-label bound, the absent-letter case in the seven-state transition,
and the cyclic counting identity (7). The argument preserves skipped
occurrences, equality-safe endpoints, and arbitrary choices of the next
overlapping occurrence. It uses only necessary constraints, so it does not
accidentally identify all graph walks with realizable trajectories.

I read the team's pinned brief, repository evidence/contribution rules,
the previous main uniform-chain proof, and the occurrence/affine reviews.
The isolated task checkout did not contain its own README or HANDOFF;
the brief explicitly directed the prior handoff in `lr-uniform-iteration`.
No files outside this report were edited and nothing was published.

## 8. Audit of the stronger 39 bound

I read the completed geometry report and checked its period-average argument:
conditioning on the uniform variable of period p_i gives exactly the duty
`1/4` for train i, and the convolution density is positive on the whole
interior of its support of length `S=sum_i p_i`. On an openly covered
interval the integrand `M-1` is nonnegative, while a strict overlap gives
a positive-length interval where it is positive. A support interval of
length S can be placed inside a chain union of length at least S, with
that overlap in its interior, including the case of equality of lengths.
This contradicts the period average. Hence the strict chain union has
length `T<S`.

The subsequent combinatorial conversion is valid. Choose a label of
maximum period `p_max`, and let a be its selected occurrence count. If
`a>=1`, the first and last of its whole intervals have union-span lower
bound

`T >= (a-1)p_max + p_max/4 = (a-3/4)p_max`.

Since `T<S<=4p_max`, it follows that `a<=4`. (The geometry report's weaker
lower bound `(a-1)p_max<T` also suffices.) Deleting the a occurrences
leaves at most `a+1` contiguous three-label pieces, each of length at most
seven by Section 2, so

`N <= a + 7(a+1) = 8a+7 <= 39`.

The case `a=0` gives `N<=7` directly. This argument counts the actual
selected chain and permits containment, skipped laps, equal periods, and
arbitrary shifts. No unproved assumption about a minimal cover enters it.
At the coordinator's request, no optional constant-tightening was pursued
after this audit.

## 9. Sufficient core-window corollary, including equality

Subject to the period-span proof candidate, **every closed interval of
length `S=sum_i p_i` contains a point safe for all four residual trains**.
To check the endpoint case, suppose the whole closed interval `[a,a+S]`
were blocked. The locally finite open blocked intervals would give a
finite open cover of it. Starting with an interval containing a and
successively choosing an interval containing the current right endpoint
with a larger right endpoint gives a strict increasing-endpoint chain
reaching past `a+S`. Such an interval exists at each step before reaching
past the endpoint because every point of the closed window is openly
covered. Its union starts strictly before a and ends strictly after
`a+S`, so its length exceeds S, contradicting the span bound. This proof
also shows explicitly why equality at the safe thresholds causes no gap
in the corollary.

Thus if a prescribed **closed core-safe window** W has width at least S,
it contains a point safe for all four residuals as well as for the core.
For common-start core speeds `{1,4,5}` at threshold `1/8`, the window

`J=[9/32,3/8]`

is core-safe, including its endpoints: the fractional parts for speeds
1, 4, and 5 range respectively in `[9/32,3/8]`, `[1/8,1/2]`, and
`[13/32,7/8]`, all contained in `[1/8,7/8]`. Its width is `3/32`.
Consequently the sufficient residual condition is

`sum_(i=1)^4 1/v_i <= 3/32`.

In particular, `min_i v_i >= 128/3` is sufficient, since each reciprocal
is then at most `3/128`. For positive integer residual speeds,
`min_i v_i >= 43` suffices; indeed `4/43 < 3/32`. Distinctness of the
physical speeds can be retained and is not needed in this auxiliary
window argument. This is a sufficient subclass, not a necessary
criterion and not the remaining full core/window existence theorem.
