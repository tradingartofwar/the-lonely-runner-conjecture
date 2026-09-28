# An explicit 39-move bound from period averaging

September 28, 2026. Baseline `99a4e77a369ff0dd520138605b0339deb263ae39`.

**Status: HYPOTHESIS / complete proof candidate, internally challenged by six
AI agents and the coordinator; external mathematical review and novelty review
remain pending.** The bounded rational calculations below are OBSERVED only for
their declared inputs. AI agreement is not an external proof certificate.

The proposed result is now explicit: **four periodic blocking trains, each
occupying one quarter of its own period, admit at most 39 advancing next-safe
moves**, independently of their positive periods, phases, and starting time.
It applies to actual selected chains, including containment and skipped laps.
The constant is conservative; no sharpness is claimed.

This replaces the need for the compactness/critical-tiling argument in the
[preceding candidate](UNIFORM_CHAIN_BOUND_2026_09_28.md). That earlier argument,
its conditional 175 bound, and its verification history are retained. The new
proof uses an exact average over a finite interval and the elementary
three-label bound of seven.

## 1. Scope and notation

Fix four positive periods `p_i` and arbitrary real shifts `s_i`. Their open
blocked intervals are

`I_(i,m)=(s_i+m p_i, s_i+(m+1/4)p_i)`, with `m` integer.

Let `B_i` be train i, `M(t)=sum_i 1_(B_i)(t)`, and `S=sum_i p_i`.
Endpoints are safe for their own train. A selected chain has occurrences
`I_1,...,I_N`, increasing right endpoints `R_1<...<R_N`, and

`L_(j+1)<R_j<R_(j+1)`.

Its union is the open interval `U=(A,B)`, with
`A=min_j L_j` and `B=R_N`. Consecutive intervals overlap on a positive-length
interval. Every advancing call of the next-safe algorithm selects exactly one
such occurrence; stationary calls are removed when forming its chain.

For the physical problem, keep the original runner convention: `n=8`, a
selected stationary reference, and `k=7` other relative speeds. Three of them
form the core; the remaining four are the residual constraints at threshold
`1/8`. Since a blocked arc has length `1/4`, their periods are `p_i=1/v_i`.
Arbitrary phases and equal periods belong to the explicitly broader auxiliary
theorem; the physical fixtures retain common start and distinct integer speeds.

## 2. The joint averaging identity

Let `X_i` be independent uniform variables on `[0,p_i]`, and put
`X=X_1+X_2+X_3+X_4`. For every real `a`,

`E[M(a+X)]=1`.                                                   (1)

For label i, condition on all variables except `X_i`. Averaging its indicator
over the remaining full period gives exactly `1/4`, whatever the conditioned
shift. Sum the four expectations. Endpoint values have measure zero.

The density `K` of X is the convolution of the four normalized interval
indicators. It is supported on `[0,S]` and strictly positive on `(0,S)`.
For positivity, if two densities are positive on `(0,u)` and `(0,v)`, their
convolution at any `x` in `(0,u+v)` integrates a positive function over the
nonempty interval `(0,u) intersect (x-v,x)`. Induct on the four factors.
Thus (1) becomes

`integral_0^S K(x)[M(a+x)-1] dx=0` for every `a`.                 (2)

Equivalently, convolution with K annihilates `M-1`: every mean-zero summand
`1_(B_i)-1/4` is killed by averaging over its own period. No common period,
integer-speed assumption, recurrence, limiting process, or tiling
classification is used.

## 3. A strict chain has span below S

**Lemma.** `B-A<S` for every selected chain.

For one occurrence its width is `p_i/4<S`. Otherwise choose y in a positive
overlap of two consecutive selected intervals. Then `M>=2` on a neighborhood
of y. Suppose `B-A>=S`. Choose

`a in [A,B-S] intersect (y-S,y)`.

Such an a exists because `A<y<B`; when `B-A=S`, take `a=A`.
The interior `(a,a+S)` lies in U and contains y. Consequently `M-1>=0`
throughout this interior and is at least one on a nonempty open subinterval.
The density K is positive there, contradicting (2). This excludes equality
`B-A=S` as well. Uncovered boundary points of U do not affect the integral.

Mere endpoint contacts do not supply positive overlap. In particular, exact
quarter-duty tilings remain compatible with (2): their multiplicity is one
almost everywhere, and their contact points are safe. This is why the lemma
preserves isolated equality witnesses.

## 4. Convert span into an occurrence bound

At each transition,

`0<R_(j+1)-R_j<p_(label(j+1))/4`.                               (3)

A one-label chain has at most one occurrence. For two labels with periods
`p>=q`, two consecutive selected p occurrences would have endpoint separation
at least p. Their intervening q-only chain has at most one occurrence, so (3)
would make that separation less than `(p+q)/4<=p/2`. Hence the p label appears
at most once and the q label at most twice: a two-label chain has at most three
occurrences.

For three labels `p>=q>=r`, two consecutive selected p occurrences have between
them a q,r chain with at most one q and two r occurrences. Equation (3) would
give their separation strictly below `(p+q+2r)/4<=p`, again impossible.
Thus a three-label chain has at most one p occurrence and two pair-only pieces,
for at most `1+3+3=7` occurrences. Strictness handles tied periods too.

Now choose a largest-period label `p_max`. If it occurs h times, its selected
right endpoints are at least `p_max` apart, even if occurrence indices skip
laps. Their span is strictly below the whole union span. Therefore

`(h-1)p_max < B-A < S <= 4p_max`, so `h<=4`.

If the label is absent, the chain already has at most seven occurrences.
Otherwise delete its h appearances. The remaining at most `h+1` contiguous
pieces use three labels and each has length at most seven. Hence

**`N<=h+7(h+1)=8h+7<=39`.**                                     (4)

No minimal-cover or irredundancy assumption is hidden in this count. The proof
also permits nested selected intervals and arbitrary choices of the next
strictly overlapping occurrence. An independent, weaker finite-state bound
of 2,923 is preserved in the combinatorial review; it is not needed for (4).

## 5. Algorithm and core-window implications

The existing repeated eleven-call order is
`a,b,c,d,c,d,b,c,d,c,d`, with speeds sorted increasingly. Every round that
starts unsafe makes at least one advancing call, since it visits every label.
With a joint-safety test at each round boundary, at most **39 rounds / 429 scalar
projection calls** suffice. A convention requiring an extra unchanged round
for confirmation instead has the conservative cap **40 rounds / 440 calls**.
Neither is an arithmetic bit-complexity claim.

Each projection is monotone and cannot pass a common-safe point lying ahead:
it moves only through one open blocked interval to its right endpoint. Thus
iteration on a supplied closed window `[L,R]` either returns its earliest
common-safe point or exits above R and certifies that the window is empty.
The frozen replay retains the latter outcome for the clipped 22-call
counterexample. The bound is on advancing moves, not a claim that 39 raw calls
suffice or that a particular core window must succeed.

There is also a sufficient window-length condition:

**Every closed interval of length S contains a point safe for all four trains.**

If such an interval were openly covered, choose a blocking occurrence
containing its left endpoint, then an occurrence containing the current right
endpoint until passing the window's right endpoint. Local finiteness and full
coverage produce a finite strict chain whose union starts before the window
and ends after it. Its span exceeds S, contradicting Section 3. Equality-safe
contacts are included in this reasoning.

Therefore, if a closed window W is safe for the core and

`sum_(residual i) 1/v_i <= width(W)`,                            (5)

it contains a witness safe for the core and all four residuals. This is a
sufficient condition, not a necessary one.

For the common-start core `{1,4,5}` at `1/8`, take `J=[9/32,3/8]`.
Its three phase ranges are `[9/32,3/8]`, `[1/8,1/2]`, and `[13/32,7/8]`, so
the whole closed interval is core-safe and has width `3/32`. Condition (5)
holds, in particular, for four residual speeds at least `128/3`; distinct
positive integer residual speeds at least **43** suffice. This proves the
selected reference's witness under the candidate lemma; it does not establish
every reference runner's claim in a full configuration.

| Inherited residual control | S | Comparison with `3/32` | Earliest witness from exact replay |
| --- | --- | --- | --- |
| `(56,64,72,112)` | `227/4032` | smaller; sufficient criterion passes | `145/512` |
| `(56,64,72,113)` | `25615/455616` | smaller; sufficient criterion passes | `129/448` |
| `(6,7,11,13)` | `2867/6006` | larger; criterion is silent | `3/8`, equality witness |
| `(6,7,11,16)` | `1711/3696` | larger; criterion is silent | `17/56` |

The 112 and 113 controls now share a phase-uniform sufficient reason to leave
a moment in J despite their different arithmetic overlap behavior. Their
earliest witnesses still differ. The tight cases show why failure of the width
criterion must not be reported as empty time.

## 6. Declared exact checks and reproduction

The [review directory](../reviews/2026-09-28-explicit-bound/) contains six
separate mathematical investigations, the primary calculation, a separately
structured verifier, and the bounded inherited-window replay.

The convolution protocol was frozen before implementation: exactly three
inherited tiling templates times the exact, first-period-plus-1/1000, and
first-start-minus-1/1000 variants. At four stated x values, an inclusion-exclusion
quartic CDF calculation evaluates each train against K. The independent checker
uses rational piecewise-polynomial antiderivatives and successive interval
averages; it imports no primary code or subset CDF formula.

Both produce 144 exact train integrals equal to `1/4`, 36 totals equal to one,
63 positive interior kernel samples and 18 zero endpoint samples. They agree
on 459 numerical fields, with ten metadata comparisons recorded separately. These are
nine constructed algebra/boundary calibrations, not a finite substitute for the
general positivity or chain proof.

The second frozen protocol reuses exactly the twelve older integer/common-start
windows: nine physical configurations (one with two windows) and two auxiliary
inputs. The capped selector reproduces the independently archived threshold
oracle across **199 calls, 32 advancing moves and 96 compound-field comparisons**.
The largest observed move count remains seven; no fixture demonstrates
sharpness of 39. Five windows satisfy (5). The clipped empty window and the
extended singleton equality witness retain their previous outcomes. None of
these twelve windows has `S=width(W)`; equality in the sufficient window test
is established analytically, not by this replay.

From repository root:

```bash
python reviews/2026-09-28-explicit-bound/primary.py
python reviews/2026-09-28-explicit-bound/challenge_verify.py
python reviews/2026-09-28-explicit-bound/compare.py
python reviews/2026-09-28-explicit-bound/replay.py
```

Protocols, implementations, outputs, source provenance and their hashes are
recorded in the manifest. There is no speed, phase, or word scan and no new
physical speed configuration.

## 7. Relation to the configuration-information question

The joint object here is the whole multiplicity function M together with the
period-dependent positive averaging kernel K. The exact identity (2) constrains
where excess overlap can occur relative to a continuously covered interval.
Under a purported cover, the integrand has one sign; a strict overlap forces
that sign to be positive somewhere, which the joint identity forbids over its
full support. Separate duty fractions and pair-overlap totals do not express
this placement condition by themselves.

This gives a direct mathematical instance of the retained relational question.
No physical theorem or analogy enters the proof. The result does not claim that
one scalar identifies every tight configuration or predicts clear duration.

## 8. Prior art, limits and next question

Basic arbitrary-phase existence at threshold `1/(2r)` for r moving constraints
is already credited to Schoenberg in Beck–Hoşten–Schymura,
[*Lonely Runner Polyhedra*](https://math.colgate.edu/~integers/t29/t29.pdf),
Integers 19 (2019), Theorem 4, printed page 12. Its statement and elementary
union-bound/compactness proof have been inspected. Schoenberg's original 1976
paper has not been inspected here. Rifford,
[*On the time for a runner to get lonely*](https://arxiv.org/html/2111.13688v2),
v2, February 16, 2022, Sections 2.2 and 4.1, provides nearby compatible-chain
and finite-inequality context. Its irredundant-chain convention must be
distinguished from an arbitrary actual projection trace.

The focused literature check does not establish novelty of the finite averaging
identity, the span bound, the 39 corollary or the sufficient window condition.
Review those exact statements against prior work before making a novelty claim.

This remains a four-residual theorem candidate at total duty one. For all seven
relative constraints of `n=8` at threshold `1/8`, total duty is `7/4`, so the
zero-average sign contradiction used here no longer follows. General core/window
existence, all-reference guarantees, sharp constants and the full conjecture
are not settled.

The next bounded question is to characterize the configurations/windows left
unresolved by (5), starting from the already preserved tight and clipped-window
controls. Use their exact 39-move certificates to identify a structural
obstruction or a sufficient core-window rule; do not fit a rule to those cases.
Hourly research remains paused. No broad scan, +7/+9 restart, paid compute,
outreach or main-branch merge was performed.
