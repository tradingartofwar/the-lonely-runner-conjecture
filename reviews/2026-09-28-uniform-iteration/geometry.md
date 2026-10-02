# Geometry route to a qualitative uniform bound

September 28, 2026. Pinned baseline and scope: `TEAM_BRIEF.md`.

**Status: HYPOTHESIS / proof candidate, pending independent external review.**
Material AI derivation. No speed or phase scan was used. This note makes no
novelty or full Lonely Runner claim. The primary physical scope is four
positive common-start integer residual speeds at threshold `1/8`; the proposed
argument actually treats the stronger auxiliary scope of four positive real
speeds with arbitrary phases. Equality remains safe.

## 1. Proposed result and remaining quantitative limitation

There is an absolute finite bound on the number of distinct intervals in any
strict, right-endpoint-increasing blocking chain of four such runners.
Consequently there is an absolute finite bound on advancing next-safe moves,
and on rounds of the stipulated eleven-call selector. The proof below is
qualitative in the comparable-speed regime: it does **not** give a numerical
universal bound there. In the regime `d >= 4a`, it gives at most **175 advancing
moves**, conservatively.

The proposed proof has two parts:

1. An unavoidable overlap with the fastest train bounds repetitions of the
   slowest occurrence when `d >= 4a`.
2. In the compact regime `a <= b <= c <= d <= 4a`, unbounded chains would limit
   to an exact periodic tiling. A strict cover near such a tiling cannot contain
   a whole tiling cycle beginning at the runner with largest perturbed cycle
   period. This gives a contradiction.

The compactness step is an existence proof of an absolute constant, not an
algorithm for computing the constant or a small practical stopping rule.

## 2. Definitions and the inherited excess budget

For runner `i`, put `p_i=1/v_i`; its blocking intervals have period `p_i` and
width `w_i=p_i/4`. Write them as

`I_(i,m) = (beta_i + m*p_i, beta_i + m*p_i + p_i/4)`.

This is just a translated version of the centered occurrence convention.
Let `M(t)` be the number of blocking intervals containing `t`. The inherited
continuous primitive has

`H'(t)=M(t)-1`, and `osc(H) <= B = (3/16) sum_i p_i`.

On the open union `U` of a strict connected selected chain,

`integral_U (M-1) <= B`.

Each selected interval is contained in `U`, selected occurrences are distinct,
and occurrences of the same runner are disjoint. All these statements concern
the whole selected occurrences, including any part to the left of the
algorithm's starting time. This avoids a truncated-first-occurrence issue.

## 3. At most seven selected occurrences when one runner is omitted

A pair of ordered runners `c <= d` cannot have two selected `c` occurrences in
one strict chain. The intervening `c`-safe gap has width `3/(4c)`, while a
single `d` occurrence has width `1/(4d)`; distinct `d` occurrences cannot join
one another. Thus the pair has at most one selected `c`, with at most one `d`
before and one after: at most three intervals, and span at most

`1/(4c) + 1/(2d)`.

If two `b` occurrences belonged to a strict chain on `b <= c <= d`, the
`c,d` blocking union would have to cover the entire intervening closed
`b`-safe gap, of width `3/(4b)`. Its connected component has span strictly less
than `1/(4c)+1/(2d) <= 3/(4b)`: strict overlap makes the span strictly less than
the sum of the at most three interval widths. This is impossible. Therefore
the triple has at most one selected `b`. Removing it leaves at most two pair
subchains, each with at most three selected intervals. Hence the total is at
most seven; the label bounds are `1,2,4`.

This argument also covers a chain with no `b`: it is then a pair chain.
It uses geometry, not the prescribed order of projection calls.

If a four-runner chain selects `N_a` occurrences of `a`, its selected word has
at most `N_a+1` runs omitting `a`. Each such run is itself a strict triple
chain. Consequently

`N <= N_a + 7*(N_a+1) = 8*N_a+7`.                 (1)

## 4. A numerical bound when `d >= 4a`

Every full `a` occurrence has length `ell=1/(4a)`. In a window of that length,
the least possible measure occupied by the `d` blocking train is

`[floor(x)/4 + max(0, frac(x)-3/4)]/d`, where `x=d*ell`.

To see this, split the window into `floor(x)` complete periods and one
remainder; a remainder of fractional length `r` can avoid at most `3/4` of a
period. This formula is valid for every phase and all real positive speeds.

For `x>=1`, this expression is at least `x/(7d)=1/(28a)`. On each interval
`x=n+r`, `n>=1`, the ratio is smallest at `r=3/4`, where

`(n/4)/(n+3/4) >= 1/7`.

On a selected `a` interval, every point blocked also by `d` contributes at
least one to `M-1`. The selected `a` occurrences are pairwise disjoint.
Therefore

`N_a/(28a) <= B <= 3/(4a)`, so `N_a<=21`.

Together with (1), this gives

`N <= 175` whenever `d>=4a`.                    (2)

No integer endpoint lattice or lower bound on an individual selected overlap
is used here. Additional overlaps can only strengthen the charge.

## 5. Compactness reduction for `d/a <= 4`

Suppose, for contradiction, that strict selected chains in this regime have
unbounded lengths. Rescale time so `a=1`, and shift the left endpoint of each
chain union to `0`. The four speeds belong to the compact set

`1 = a <= b <= c <= d <= 4`,

and the four phases belong to the compact four-torus. Pass to a convergent
subsequence of these parameters.

Unbounded selected counts force unbounded union spans: an interval of length
`T` can intersect at most `v_i*T+2 <= 4*T+2` occurrences of runner `i`, so a
chain whose union has length `T` contains at most `16*T+8` selected
occurrences. Every approximating chain strictly covers `(0,T)`. By continuity
of phase distance and finiteness of the four labels, the limiting **closed**
blocking sets cover `[0,infinity)`.

The limit need not strictly cover: isolated equality contacts are precisely
the important case.

## 6. A limiting closed cover is an exact tiling

For the limiting parameters, the closed cover gives `M(t)>=1` away from
threshold endpoints. Hence `H` is nondecreasing on `[0,infinity)`.

There are arbitrarily large `T_j` for which all four phases
`v_i*T_j mod 1` tend to zero. One elementary justification is simultaneous
Dirichlet pigeonholing: either the resulting approximating integer times are
unbounded, or a bounded repeated time gives an exact common period and its
multiples. Since `H` is continuous in those phases,

`H(T_j) -> H(0)`.

A nondecreasing function with these returns is constant. Thus `M=1` almost
everywhere on the halfline. No two blocking interiors can overlap at a positive
time, since such an overlap is open and would force a strict increase of `H`.

Two periodic interval trains with irrational period ratio necessarily have
an interior overlap at arbitrarily large positive times: the centers of one
train modulo the other's period are dense. Therefore every pair of limiting
periods has rational ratio.

For a rational pair write `p_i=q_i*g`, `p_j=q_j*g`, with coprime positive
integers `q_i,q_j`. Differences between centers range through one residue
class modulo `g`. Its closest representative to zero has absolute value at
most `g/2`. Interior disjointness requires that distance to be at least half
the sum of the two interval widths:

`(p_i+p_j)/8 <= g/2`, or `q_i+q_j<=4`.

The only possibilities are period ratios `1`, `2`, or `3` and their
reciprocals. Because the slowest normalized speed is `1`, every limiting
speed is in `{1,2,3}`. Speeds `2` and `3` cannot both occur, since their pair
would require coprime period integers summing to five.

In particular every limiting train has common period `P=1`, and the
halfline tiling extends periodically to the full line. The occurrence
interiors are disjoint, the closed intervals cover, and adjacent occurrences
meet exactly at endpoints. This common-period conclusion is all the next
step needs. A finer multiplicity classification gives the familiar types
`(1,1,1,1)`, `(1,1,2,2)`, and `(1,1,1,3)`, but that classification is not
required for the compactness proof.

## 7. No nearby strict cover across two complete tiling cycles

The following local argument applies to any periodic exact tiling with four
trains, each of duty `1/4`. Let its common period be `P`, with runner `i`
appearing `q_i=P/p_i` times per period. For nearby parameters, use primes and
put

`s_i=q_i*p_i'`.

Choose a runner `i` maximizing `s_i`. In the unperturbed tiling choose one of
its occurrence starts in `[P,2P)`. The next occurrence of the same runner with
the same position in the period is `q_i` occurrences later, in `[2P,3P)`.
The tiling sequence from the first start to this latter start includes exactly
`q_j` complete occurrences of every runner `j`.

For all sufficiently nearby parameters, a strict cover of `[0,4P]` forces
strict overlap at every adjacency in this finite sequence. Here is the
endpoint justification. Around each of its finitely many original contacts,
choose a small open neighborhood whose closure lies inside `(0,4P)` and
meets no unperturbed occurrence except the two adjacent ones. This is
possible because every interval width is positive and a tiling contact has
exactly one interval on either side. The remaining occurrences are separated
from each chosen contact by positive distance. On the bounded horizon only
finitely many occurrence labels can enter, and endpoints depend continuously
on parameters. Thus the exclusions and the left/right order persist in a
small parameter neighborhood. If the perturbed left interval ends before
the right interval starts, a gap remains. If they merely touch, the contact
is in neither open blocking interval and is safe. Therefore strict coverage
forces `right(left)>left(right)` at each contact. Possible changes to the
selector's own itinerary are irrelevant: this concerns the entire blocking
union, with all occurrences available.

Write the perturbed consecutive starts in this sequence as `l_0,...,l_m`;
the corresponding widths before the final start are `w_0',...,w_(m-1)'`.
Adding the forced strict overlap inequalities gives

`l_m-l_0 < sum_(r=0)^(m-1) w_r'`.

The left side is `q_i*p_i'=s_i`. The right side is

`sum_j q_j*p_j'/4 = (s_1+s_2+s_3+s_4)/4 <= s_i`.

This is impossible. There are only four possible choices of maximizing
runner; take the intersection of the four finite contact-preserving
neighborhoods, so the argument is uniform over that choice.

For our normalized limits `P=1`, every exact tiling therefore has a
parameter neighborhood in which no strict cover of `[0,4]` exists. The
approximating chains from Section 5 eventually lie in this neighborhood and
have spans exceeding four, contradicting their strict coverage of `(0,T)`.
To avoid the left endpoint at zero entirely, apply the same finite contact
argument on `[1,5]`, or shift the displayed horizon slightly into `(0,T)`;
the contacts used above are already in its interior.

This closes the contradiction: selected chain length is uniformly bounded in
the compact-ratio regime. Together with (2), the proposed absolute bound
exists for all positive speed ratios and phases.

## 8. Cost and scope checks

- This controls advancing scalar moves. The prescribed eleven-call round is
  fair with a fixed delay, so every completed unsafe round has at least one
  advance. One final all-stationary round is enough to certify safety, giving
  a uniform round and call bound once the qualitative move constant is fixed.
- The proof does not produce that constant for `d/a<4`, nor an efficient way
  to find it. It therefore must not be described as a numerical replacement
  for the disproven 22-call bound.
- Strict overlaps and open blocking sets are essential. Exact tilings have
  equality-safe contacts; they are limits, not counterexamples to termination.
- A chain count does not count skipped lap labels or arithmetic bit cost.
- The conclusion is auxiliary phase-robust and so includes common-start
  positive integer residual speeds. It does not force the resulting witness
  into a supplied core-safe window, select a globally successful core, or
  solve the eight-runner conjecture.
- The recurrence, pair-disjointness lemma, and local adjacency forcing merit
  separate line-by-line review. No external literature or novelty audit was
  attempted in this assigned geometric subtask.
