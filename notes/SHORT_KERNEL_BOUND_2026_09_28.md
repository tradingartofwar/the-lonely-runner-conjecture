# Shorter averaging support and a 23-move bound

September 28, 2026. Pinned parent:
`bcf959b45a35701f2fd710b1d86ca2cc3152e14c`.

**Status: HYPOTHESIS / complete proof candidates, internally reviewed by six
AI agents and the coordinator; external mathematical and novelty review pending.**
The exact finite checks below are OBSERVED within their stated scopes.

The proposed universal bound for four quarter-duty blocking trains improves
from **39 to 23 advancing moves**. This counts the actual increasing-endpoint
chain, with arbitrary positive periods and phases, including containment and
skipped laps. The existing eleven-call round order consequently needs at most
23 rounds / 253 projection calls when joint safety is checked at round
boundaries. No sharpness or arithmetic bit-complexity claim is made.

The [39-move note](EXPLICIT_CHAIN_BOUND_2026_09_28.md) and its computations remain
unchanged. The improvement uses a shorter averaging support followed by a
constraint on long three-label pieces. The same proof also yields a
dimension-dependent bound in a precisely stated larger auxiliary model.

## 1. Shorter averaging support

Let the four open blocked trains have occurrences

`I_(i,m)=(s_i+m p_i, s_i+(m+1/4)p_i)`, with `p_i>0`.

Let M be their total multiplicity. Order their periods as `P>=q>=r>=s`,
retaining label identity even in a tie. Keep a uniform variable U on `[0,P]`
for one largest-period label. For each other label of period p, use an
independent four-point variable D uniform on

`{0,p/4,p/2,3p/4}`.

Put `X=U+D_q+D_r+D_s`. Its support length is

`H=P+3(q+r+s)/4 = 3(sum_i p_i)/4+P/4`.                        (1)

For every real a,

`E M(a+X)=1`.                                                  (2)

For the P label, condition on the discrete variables and average over its
whole period. For any other label i, its four grid translates have indicator
average exactly `1/4` off the countable grid `s_i+(p_i/4)Z`, and zero on that
grid, because blocking endpoints are open. After conditioning on the other
discrete variables, U gives that exceptional set probability zero. Thus each
label contributes exactly `1/4` to (2) for every a. The intermediate discrete
average is **not** pointwise equal to `1/4`; preserving this distinction is
essential at equality contacts.

The density K of X is a positive mixture of 64 translated uniform boxes of
length P, counting repeated offsets with multiplicity. It is positive
throughout `(0,H)`. One direct proof starts with the interval `(0,P)`.
Adding a four-point factor of spacing `p/4<=P/4` takes four translates of the
current positive interval; adjacent translates overlap, so their union is
the whole enlarged interval. Repeat for the other three factors. The support
endpoints themselves may be assigned density zero without affecting integrals.

## 2. Strict chains and whole-occurrence counting

A selected chain has strictly increasing right endpoints, and each previous
right endpoint lies strictly inside the next open occurrence. Its union is
an open interval `(A,B)`. For a one-occurrence chain, its width is below H.
For a longer chain, consecutive occurrences overlap on an open interval
where `M>=2`, while `M>=1` throughout the union.

If `B-A>=H`, choose an overlap point y and

`a in [A,B-H] intersect (y-H,y)`.

The intersection is nonempty, also when `B-A=H`. The support interior
`(a,a+H)` is covered, and its overlap near y has positive K-weight. This
makes `E[M(a+X)-1]>0`, contradicting (2). Therefore

**`B-A<H`.**                                                   (3)

If the P label occurs h times, its first and last right endpoints are
separated by at least `(h-1)P`. The union also contains the whole first
P occurrence, of width `P/4`. Hence

`B-A >= (h-3/4)P`, whereas `H<=13P/4`.

The strict upper bound (3) gives `h<4`, so **h<=3**. This uses whole
occurrences; merely bounding their right-endpoint span would lose the
improvement. Containment and skipped laps strengthen or preserve the lower
bound.

The elementary pair and triple bounds remain 3 and 7. To recall their proof,
each transition obeys

`0<R_next-R_old<p_destination/4`.                             (4)

In a pair of periods u>=v, a return to u could have only one intervening v
and would advance by less than `(u+v)/4<=u/2`, although it must advance by
at least u. Thus u occurs at most once, giving at most three occurrences.
In a triple u>=v>=w, the intervening pair has at most one v and two w;
a return to u would advance by less than `(u+v+2w)/4<=u`, again impossible.
Thus a triple has at most `1+3+3=7` occurrences. Equal periods are allowed.

Deleting the at most three P occurrences initially gives the intermediate
bound `N<=h+7(h+1)<=31`. This was the candidate when the exact kernel
protocol was frozen. The following additional count was derived analytically
after that freeze, with no change to the fixtures and no fitting to their
outputs.

## 3. A long-triple restriction gives 23

**Lemma.** If a q,r,s chain, with `q>=r>=s`, has at least six occurrences,
then

`r>3s`, `q+2s>3r`, and `q+r+s<11q/7`.                         (5)

The largest label q must appear exactly once: if absent, the chain is a
pair chain of length at most three. Its two r,s pieces have combined length
at least five and each has length at most three. Both therefore have length
at least two and contain exactly one r; one piece has length three and is
necessarily `s,r,s`. The return to s in that piece and (4) give

`s <= endpoint separation < (r+s)/4`, hence `r>3s`.

Between the two r occurrences lie q and at most two s occurrences: at most
one s after the first r and one before the second. Their return gives

`r <= endpoint separation < (q+r+2s)/4`, hence `q+2s>3r`.

Since `s<r/3`, these inequalities imply `r<3q/7`, then
`q+r+s<q+4r/3<11q/7`. This proves (5) without word enumeration.

Now split the four-label chain by its h occurrences of P.

- If `h<=2`, the triple bound gives `N<=h+7(h+1)<=23`.
- If `h=3`, whole-occurrence span gives `B-A>=9P/4`. Together with (1)
  and (3), this requires `q+r+s>5P/3`. A triple-only piece of length at
  least six would instead require `q+r+s<11q/7<=11P/7<5P/3` by (5).
  Thus each of the at most four triple-only pieces has length at most five,
  and `N<=3+4*5=23`.

Consequently **N<=23 for every actual four-label quarter-duty chain**.
The argument handles empty pieces, either orientation of a length-two pair,
tied periods and nonconsecutive selected laps. No example attaining 23 is
supplied, and no assertion of sharpness follows from these inequalities.

## 4. Projection calls and successful core windows

The existing repeated order is `a,b,c,d,c,d,b,c,d,c,d`, with increasing speeds.
Every round beginning unsafe makes an advancing call because it visits all
four labels. With initial and round-boundary joint-safety checks, the bound
is therefore **23 rounds / 253 scalar projection calls**. A convention that
requires one extra unchanged confirmation round gives 24 rounds / 264 calls.
The separate safety tests and arithmetic bit costs are not included in these
projection-call counts.

Earlier code and traces are preserved. In particular, the older failure of
unconditional22-call completeness still used seven advancing moves and first
reached safety on call23. Its call count neither attains nor verifies the
new23-move bound. This round does not rerun the archived selector or claim
that23 raw projection calls always suffice.

Every closed interval of length H contains a common-safe point. Otherwise
the locally finite open blockers covering it can be followed by a finite
strict increasing-endpoint chain from before its left endpoint to beyond
its right endpoint. That chain would span more than H, contradicting (3).
Thus a prescribed closed core-safe window W succeeds whenever

**`H<=width(W)`.**                                              (6)

The equality case is included; safe duration need not be positive. For the
physical common-start core `{1,4,5}` at threshold `1/8`,
`J=[9/32,3/8]` is closed-safe and has width `3/32`. Since

`H <= 13/(4 v_min)`,

residual speeds at least `104/3`, and in particular positive integer residual
speeds at least **35**, suffice for a selected-reference witness in J. This
is a convenient sufficient threshold, not an optimal or necessary one.
Failure of (6) remains inconclusive. Any failure of this sufficient test in
the integer setting has at least one residual speed at most34; the remaining
speeds may still be unbounded, so this is not a finite configuration reduction.

Exact arithmetic on the twelve inherited windows shows H smaller than the
old S in each, but **no newly certified window in that diagnostic set**: both
criteria certify the same five. In particular, both112 and113 controls pass,
while the tight13, strict16 and clipped-lift windows remain outside this
sufficient criterion. Their old feasible/empty outcomes are not changed.

## 5. A precise obstruction to truncating this average

For the inherited strict16 residuals `(6,7,11,16)` on J, put `f=M-1`.
Its nonzero open-cell values are:

| Cell | f |
| --- | --- |
| `(9/32,25/88)` | `+1` |
| `(17/56,39/128)` | `-1` |
| `(5/16,41/128)` | `+1` |
| `(31/88,17/48)` | `+1` |
| `(47/128,3/8)` | `+1` |

It is zero on the other open cells. Point values at thresholds are checked
separately when determining safety. The total signed excess is

`T=1/352-1/896+1/128+1/528+1/128=569/29568`.

Let `F(t)=integral_(9/32)^t f`. The only decrease has size `1/896`, after
an accumulated `1/352`, so its value remains positive. At every interior
point of J, `0<F(t)<T`. Therefore every positive-length prefix, suffix or
whole J has strictly positive signed excess.

Here `P=1/6>width(J)=3/32`. A box of width P can intersect J only in a
prefix, suffix, all of J, or the empty set, up to endpoints. Every translated
mixed kernel is a nonnegative mixture of such boxes. Hence

`integral_J K(t-a)[M(t)-1] dt > 0`

for every translate having positive kernel mass on J. This statement covers
all real translations analytically; no translate was scanned. In fact it
holds for every nonnegative mixture of boxes of width at least `width(J)`.

Yet the exact safe interval `[17/56,39/128]` has positive length `1/896`.
Thus simply restricting this average to J and asking for a negative signed
excess cannot certify even this positive-duration example. Isolated equality
witnesses, such as tight13, pose a separate obstacle to any negative-integral
certificate because they occupy zero measure.

This is a limitation of this specified certificate class. It does not exclude
other kernels, finer localization, joint occurrence constraints, or the
bounded projection selector. It directly identifies information still lost
by a coarse weighted summary despite the global averaging identity.

## 6. A larger-number auxiliary corollary

Let m>=2 trains each occupy exactly `1/m` of their own positive period, with
arbitrary phases. Use one continuous full-period variable for a largest
period P and m-point grids for the other labels. The same proof gives

`H_m=P+((m-1)/m)sum_(others) p_i`,

strict span below H_m and at most `m-1` selected occurrences of the largest
period. Deleting them leaves at most m chains on at most `m-1` labels, each
still at duty `1/m`. Enlarge their intervals leftwards to duty `1/(m-1)`
while keeping every right endpoint fixed. Strict transitions and endpoint
order are preserved. Thus occurrence bounds obey

`B_m + 1 <= m (B_(m-1) + 1)`.

Using `B_4=23` gives **`B_m<=m!-1` for m>=4**. A generic baseline `B_1=1`
instead gives `2m!-1`; the strict-span lemma is not asserted for m=1.
The widening and induction were separately challenged, including that base
case. These remain proof candidates, with no higher-dimensional experiment
or sharpness claim.

This is the critical-duty auxiliary model, corresponding to symmetric
distance threshold `1/(2m)`. For even total runner count `n=2m`, it can
serve as a residual subproblem after a window is already safe for `m-1`
core constraints. It does not supply that core window or an all-reference
guarantee. For the full `k=n-1` constraints at threshold `1/n`, total duty
is `2(n-1)/n>1` for n>2, so the averaging contradiction does not transfer
directly to the full Lonely Runner Conjecture.

## 7. Finite verification, review and reproduction

The [review directory](../reviews/2026-09-28-short-kernel/) records six
separate assignments, two frozen protocols, exact implementations and their
comparison. No broad speed, phase, word or all-reference scan was run.

The main protocol uses exactly nine inherited auxiliary fixtures. For each,
the primary integrates blocked intervals against64 translated boxes. A
separately written verifier uses periodic primitives and a signed-event
sweep for the density and CDF. Neither imports the other's implementation.
The frozen scope comprises144 train integrals,36 multiplicity totals,
219 density cells,210 interior breakpoints,18 support endpoints and54
discrete-boundary/interior checks. All pass; the implementations agree on
1,943 numerical, 14 Boolean and 82 text fields. These calibrate the kernel
identity and endpoint handling; they do not prove the general move bound.

One additional, explicitly auxiliary equality fixture is analytically
constructed: `p_i=4/13`, `s_i=i/13` for `i=0,1,2,3`, W=`[0,1]`.
It has `H=width(W)=1`, fourteen isolated safe points `j/13` for `j=0,...,13`,
and thirteen blocked open cells. Safe duration is zero. Both implementations
recover this exactly; it is not a new common-start physical configuration.

The second protocol computes S,H and width only for twelve inherited integer
windows, then reconstructs only strict16's already specified event sequence
to check the signed-prefix obstruction. It makes no translation scan and no
new projection run. The five old width certificates remain five. The
all-translates implication is analytical, based on the verified prefix and
suffix signs.

From repository root:

```bash
python reviews/2026-09-28-short-kernel/primary.py
python reviews/2026-09-28-short-kernel/verify.py
python reviews/2026-09-28-short-kernel/compare.py
python reviews/2026-09-28-short-kernel/windows.py
```

The manifest records the frozen hashes, sources, implementations and results.
The protocol's initial31 candidate remains preserved; the23 refinement came
from the long-triple inequalities after freezing, not from adapting the test
domain or observing a maximum trace length.

## 8. Prior art and next step

Basic shifted existence at threshold `1/(2m)` is already credited to
Schoenberg via Beck–Hoşten–Schymura,
[*Lonely Runner Polyhedra*](https://math.colgate.edu/~integers/t29/t29.pdf),
Integers19 (2019), Theorem4, printed page12. The latter statement and
elementary proof were inspected; the original1976 paper has not been
inspected here. The focused literature check does not determine priority
for the mixed kernel, span bound, finite move counts, or window corollary.
No novelty claim is made.

The next bounded mathematical target is a structural guarantee for a core-safe
window when (6) fails, starting with the inherited controls and the fact that
some residual integer speed is then at most34. Three other speeds can remain
unbounded. The strict16 result excludes the simple translated-box truncation
route as a complete solution. Preserve endpoint-sensitive occurrence data;
do not infer emptiness from failure of a sufficient condition.

Hourly research stays paused. No main merge, outreach, paid compute, broad
unattended computation or parked +7/+9 continuation was performed.
