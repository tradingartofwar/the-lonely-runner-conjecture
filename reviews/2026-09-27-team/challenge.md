# Hostile review: the transfer test has acquired a structural explanation

September 27, 2026 protocol; reviewed September 28 UTC. Scope: the six frozen
inputs, reference 0, threshold 1/8. Material AI involvement: mathematical
challenge, exact diagnostics, and writing. No added speed configurations,
all-reference calculation, external contact, or novelty claim.

**Principal finding:** the strongest challenge is now to the interpretation of
the experiment, rather than to its arithmetic. The fastest-core argument in
[the candidate note](../../notes/FASTEST_CORE_CERTIFICATES_2026_09_27.md) supplies
a complete explanation of the some-core tree hypothesis. I independently
reviewed its interval lemma, endpoints, and quantifiers and found no gap in the
stated scope. It remains a **HYPOTHESIS / proof candidate** under repository
rules. The six-case calculations are **OBSERVED** finite evidence and an
implementation check; they cannot promote that argument by repetition.

The unresolved LRC step is existence itself. Showing that an existing strict
lonely time has a tree certificate is conditional certificate completeness,
not an argument forcing a lonely time.

## 1. Independent review of the fastest-core argument

Write V for the greatest absolute relative speed and delta for the threshold,
with 0<delta<1/2. A complete safe component W of any core containing a V label
lies in one safe lap of V, and therefore

`|W| <= (1-2delta)/V <= (1-2delta)/v`

for each residual speed v. The last expression is the closed safe gap between
two successive strict blocking intervals of that residual runner. If W met
both intervals, its width would be *strictly greater* than the intervening gap:
the gap endpoints themselves are safe. Thus every residual blocker on W is
one interval or empty. At delta=1/8 the width is **3/(4v)**, not 7/(8v).

For intervals ordered by left endpoint, join each interval after the first to
an earlier interval with greatest right endpoint. Its intersection with the
previous union has the same length as its intersection with this one parent:
every earlier left endpoint lies to the left of the new interval's left
endpoint. The resulting parent edges form a tree, and incremental union
lengths telescope to the tree expression. This tree attains actual uncovered
duration; no tree can exceed it. Empty intervals attach with zero weights.

The potential objections do not break this argument:

- Time is a line. The protocol does not join the endpoints of [0,1], so there
  is no circular interval graph hidden in the construction.
- Equal absolute relative speeds preserve the claim; their runner labels and
  original threshold remain unchanged. Negative relative velocities may be
  replaced by their absolute values for the distance constraints.
- Endpoint flags affect existence at zero duration, but not the interval
  union length identity. Singleton W has actual duration and tree bound zero.
- Shortening or splitting a fastest safe lap by additional core constraints
  preserves the necessary width bound.

Consequently each of the 15 three-label cores containing the unique fastest
runner has exact bounds on every component in each frozen row. If the global
allowed set has positive duration, every one of these cores has a positive
component. A core consisting of the fastest runner alone also works, with six
residual vertices. Three core constraints are not essential to exactness.

Under this argument, a strict failure across all 35 cores cannot be a physical
counterexample. A reported failure would first demand checking enumeration,
strict endpoints, normalization, or the implementation of the tree optimum.
The original falsifier was legitimate before the argument; it is no longer a
reason to launch a larger campaign while leaving this proof candidate unreviewed.

## 2. A sharp local obstruction and the exact slack identity

Let m_S be the time in W with exactly residual subset S active, and c_T(S) the
number of connected components of the induced tree on S. At a nonempty state,
the induced forest has `|S|-c_T(S)` edges. Hence

`U - Q_T = sum_(S nonempty) m_S (c_T(S)-1)`.

The empty state contributes zero slack: both the uncovered indicator and the
tree integrand equal one. Optimizing gives

`U - Q_opt = min_T sum_(S nonempty) m_S (c_T(S)-1)`.

This proves the requested identity and gives an exact interpretation: one
fixed tree must connect every active subset that carries positive duration.
Separate states cannot choose different trees when evaluating a certificate.
The checker exhaustively verifies the pointwise identity on **286 tree/state
combinations** for one through four vertices; the derivation is not based on
that finite check.

A useful geometric necessary condition follows from the interval lemma. If
`U>Q_opt`, at least one **retained** blocker must have two or more interval
pieces. For such a blocker v,

`|W| > 3/(4v)`, so `v > 3/(4|W|) >= max(core speeds)`.

Thus every missed positive window must retain a runner faster than every core
runner whose blocking state leaves and returns inside W. This is a directly
falsifiable diagnostic, stronger than merely observing pair overlap. Multiple
pieces are necessary for nonzero slack, not sufficient: the near_pairs winner
has repeated pieces but an exact tree.

For an incomplete collection of cores, the state formulation sharpens this
diagnostic without adding physical examples:

- With at most two retained blockers, slack is always zero.
- With three, slack is exactly the minimum of the three exclusive pair-state
  durations. A positive window is missed precisely when each of those three
  durations is at least U.
- With four labels R, a fixed tree has slack

  `sum_(ij not an edge of T) m_{i,j}`

  `+ sum_(i in R) (degree_T(i)-1) m_(R minus {i})`.

  Therefore zero slack is possible exactly when there is a tree containing
  every positive-mass exclusive pair edge, with every label omitted by a
  positive-mass triple being a leaf. A positive pair cycle already rules out
  zero slack. The *weights* still determine whether the slack defeats U.
  Averaging all 16 trees shows optimal slack is at most `(M2+M3)/2`, where Ms
  is the total mass in states of size s. Tree failure with U>0 requires
  `M2+M3 >= 2U`.

These conditions concern durations. An incompatible state at a single event
point carries no mass and cannot create positive slack.

## 3. What passing these cases does and does not measure

The protocol is correctly described as fixed internally before this
calculation, not externally preregistered, random, or representative. The six
case names describe arithmetic constructions, not six independent populations.
Reflection duplicates and overlapping cores further preclude treating 15,696
components as independent evidence for an unbounded statement.

Excluding t=1/8 does not remove simple strict witnesses. Direct substitution
at t=1/6 works for **prime_mix, near_pairs, squares, prime_powers, and
perturbed_chain**, with minimum distance at least 1/6>1/8: none of their speeds
is divisible by 6. Fibonacci is the sole row without a witness 1/d for
2<=d<=7. This bounded diagnostic neither changes the inputs nor enters Q's
selection keys. Failure of this small denominator list does not establish
that Fibonacci is intrinsically hard.

The experiment can still show how the quantitative selector chooses wider
windows, which state patterns create slack, and whether independent exact
implementations agree. It supplies no probability of universal validity and
no new existence coverage from five cases already certified at 1/6. The
conditional fastest-core explanation now matters more than the pass rate.

The observed 210/210 successful cores also does not revive the stronger
every-core conjecture. The earlier `{1,5,6}` core in
`{0,1,4,5,6,7,11,45}` remains an exact counterexample to that conjecture. It
omits the fastest runner, exactly as the present argument requires.

## 4. Containment, invariance, and endpoint blindness

Removing a strictly contained blocker preserves the allowed set pointwise;
removing a merely almost-everywhere contained blocker need not preserve an
endpoint. Separately, the optimal tree value is unchanged by containment:
if B_i is contained in B_j, then `O_ij=D_i` and `O_ik<=O_jk`. An optimum can
include i--j; contracting it leaves the optimum after deleting i. The added
edge weight D_i cancels its single duration. Empty sets and equality classes
follow as limiting cases of the same elementary argument.

This means reduction simplifies the certificate; it does not strengthen an
already optimized tree inequality. Reducing to at most two blockers suffices
for exactness, but does not force positive duration. Conversely, neither
positive bounds nor exactness require nonempty containment.

There is a reporting trap in `positive_bound_without_reduction=198`: this
counts positive windows whose map removes nothing. It does **not** mean only
198 windows had a positive bound before reduction. All **7,953** positive
reduced bounds are positive full bounds, by the checked equality. Likewise,
the 6,064 positive windows without nonempty proper containment describe
certificate structure, not the gain from withholding or applying a method.

The interval-tree identity does not recover equality points from durations.
The earlier contact-moment examples remain valid demonstrations that even
every-order local durations can fail to decide local nonemptiness. Here the
strict interval structure adds a route to exact *duration*, not a license to
discard strict blocker flags.

The all-core endpoint fallback has a stronger consequence than the frozen
protocol claims. If the full allowed set F in [0,1] is nonempty, let a=min F.
Common start and positive threshold give a>0. At least one runner begins a
safe lap at a, since otherwise all runners would also be safe just before a.
Any core containing that runner is safe at a and has a complete component
beginning at a. Thus any collection of cores covering all labels contains a
passing endpoint. All 35 cores, and the 15 fastest-containing cores, do so.

This supplies a **proof candidate for fallback completeness**, unlike the
earlier two-core procedure. Keep the frozen protocol unchanged and label this
as a later deduction. A fallback success is not a positive-tree success, and
even a complete finite decision method does not prove the answer is always
nonempty for arbitrary speeds.

## 5. Audit of the primary outputs

The small checker reads the primary archive; it is **not** an independent
reconstruction of all 15,696 components. It verifies the promised fastest-core
consequences in the archived per-core summaries, independently recalculates
each selected tree from its state masses and moments, checks selection among
the per-core winners, and directly substitutes all 12 global/selected witnesses.
No error was found within that audit scope.

All **8,800** components of the 90 fastest-containing cores have exact bounds,
zero slack, and no positive-duration misses. All six Q winners omit the
fastest runner. This is consistent: the selector maximizes unnormalized
duration over complete windows, and a wider component may beat every exact
fastest-core window while retaining slack.

| Case | Selected core speeds | Retained blockers | Selected slack U-Q |
| --- | --- | ---: | ---: |
| prime_mix | 8,11,29 | 2 | 0 |
| near_pairs | 15,16,17 | 4 | 0 |
| fibonacci | 8,13,21 | 4 | 27/24208 |
| squares | 8,9,25 | 4 | 13991/3312738 |
| prime_powers | 16,25,27 | 4 | 3189/3136000 |
| perturbed_chain | 7,23,38 | 1 | 0 |

Two concrete mechanisms are especially useful:

- **near_pairs:** all four blockers remain, none vanishes, and there is no
  nonempty containment. The only positive pair-only states are 31/33 and
  47/49. A tree containing those two edges is exact; its connecting edge has
  zero overlap. This is direct physical evidence that containment and
  single-piece blockers are each unnecessary for tree exactness.
- **fibonacci:** the selected tree is a star centered at 144. Its entire
  slack is the exclusive 34/89 state, of duration 27/24208. The positive
  exclusive edges 34/89, 34/144, and 89/144 form a triangle, so no tree can
  represent all three without a missing pair edge. This makes the loss
  concrete instead of attributing it vaguely to high-order overlap.

The 18 positive-duration component misses are compatible with all 210 cores
succeeding elsewhere. None is an all-core failure, and the conditional
stronger-pair follow-up authorized only after an all-core failure is not
triggered.

Reproduction:

```bash
python -B reviews/2026-09-27-team/challenge_check.py --check
```

[challenge_checks.json](challenge_checks.json) pins this checker, protocol,
and inspected primary archive by SHA-256. The unbounded deductions above
remain supplied arguments pending the repository's required further review;
the exact six-input and Boolean-state calculations have only their stated
finite scope.
