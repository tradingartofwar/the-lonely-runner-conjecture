# Blocking-chain overlap budget and a speed-dependent termination bound

September 28, 2026. Internal AI mathematical review by the separately tasked
`chain_bound` agent. Baseline: `dd5b3bce9a7a3fb22474a724161438f24e35fb41`.

**Status:** HYPOTHESIS / supplied proof candidate, pending external review.
No novelty claim, full Lonely Runner result, or speed-independent bound is
asserted. This argument was derived analytically, without a speed or phase
scan. It complements rather than supersedes the preserved failure of the
unconditional 22-projection selector.

**Prior-work correction after the coordinator's audit:** the same periodic
primitive h and its `3/16` oscillation were already present in
`notes/OVERLAP_PLACEMENT.md`, Section 8. They are reused here. The added argument
connects that existing discrepancy identity to selected blocking occurrences
and a pairwise endpoint quantum to obtain a move bound. This review must not
be read as introducing the primitive or establishing literature novelty.

## 1. Exact potential at the critical blocking density

Use four residual runners with positive speeds `v_i`, arbitrary initial phases
`alpha_i`, and threshold `delta=1/8`. Their blocked occurrences are the open
intervals

`I_(i,k)=((k-1/8-alpha_i)/v_i,(k+1/8-alpha_i)/v_i)`.

Each runner is blocked for one quarter of every period. Let `M(t)` be the
number of blocked residual runners at t. Define the continuous periodic
function h by, for `0<=theta<=1`,

```
h(theta) = 3 theta/4                 if 0 <= theta <= 1/8,
           1/8 - theta/4             if 1/8 <= theta <= 7/8,
           3(theta-1)/4              if 7/8 <= theta <= 1.
```

The formulas agree at their joins and `h(0)=h(1)=0`. Set

`H(t)=sum_i h({v_i*t+alpha_i})/v_i`.

Away from the finitely many local threshold points,

`H'(t)=M(t)-1`.

Consequently, on a continuously blocked interval `[A,B]`,

`integral_A^B (M(t)-1) dt = H(B)-H(A)`.

The left side is the total excess multiplicity: time covered twice contributes
once, time covered three times contributes twice, and so on. It is not the
sum of all pairwise overlap measures, which would overcount a triple overlap.

Since `-3/32<=h<=3/32`,

`H(B)-H(A) <= (3/16) sum_i 1/v_i`.                    (1)

The phase-sensitive upper envelope is

`H_max=(3/32) sum_i 1/v_i`.

Thus a blocked chain can consume at most `H_max-H(L)` of excess multiplicity
after a specified starting time L. There is no assertion that the envelope
H_max is simultaneously attained by all phases.

The cancellation in `H'=M-1` is specific to four residual blockers at this
threshold. For fewer blockers, a continuously blocked interval also consumes
a positive amount of potential per unit of elapsed time. With four, its
length is not bounded by this identity alone: the relevant cost is overlap.

## 2. Every nonzero projection adds a connected blocking occurrence

Take any sequence of the next-safe projections P_i. Ignore stationary calls,
and write its successive strictly increasing times as

`t_0=L < t_1 < ... < t_N`.

The jth moving projection starts inside a blocked occurrence I_j and ends
at that occurrence's right endpoint t_j. The next moving projection starts
at t_j strictly inside a different blocked occurrence I_(j+1). Therefore
I_j and I_(j+1) overlap by positive length, not merely at an endpoint.
No occurrence can be selected twice, because its right endpoint has already
been passed or reached.

Their union is one open interval U. If every positive overlap between two
blocking occurrences has length at least eta>0, each newly selected interval
overlaps the previous union by at least eta. The elementary union identity
then gives

`sum_j |I_j| - |U| >= (N-1)*eta`.

This difference is exactly the selected intervals' excess multiplicity on U.
The full four-runner multiplicity is at least the selected multiplicity.
Applying (1) on the closure of U proves

`N <= floor(1 + (3/(16*eta))*sum_i 1/v_i)`.            (2)

There is no assumption in this argument that a later safe time already exists.
Every finite prefix of moving projections obeys the same bound. Hence an
infinite sequence of nonzero projections is impossible whenever eta exists.

Open blocking intervals are essential: a shared boundary is safe for both
of its adjacent blocked occurrences and cannot be used to continue a chain.

## 3. A pairwise arithmetic quantum for common-start integer speeds

For positive integer speeds and common phases zero, put

`Q = max_(i<j) lcm(v_i,v_j)`,   `eta=1/(8Q)`.

Two block endpoints from runners i,j differ by an integer multiple of
`1/(8*lcm(v_i,v_j))`. If their positive overlap is determined by one endpoint
from each runner, its length is therefore at least eta. If one interval
contains the other, the overlap is a whole interval, of length
`1/(4*v_i) >= 1/(4Q) > eta`. Occurrences of a single runner are disjoint.
Thus eta is a valid positive overlap quantum, and (2) becomes

`N <= K_global := floor(1+(3Q/2)*sum_i 1/v_i)`.        (3)

The bound depends on the speeds. It is deliberately conservative, and can be
very large for the existing common-start lifted example. It is not evidence
that that many steps are ever needed. It avoids presupposing a witness or
enumerating a common period, but is still a rational-arithmetic termination
bound, not a speed-independent complexity result.

Rational speeds and phases also admit an endpoint lattice after a suitable
common scaling/denominator choice; (2) applies using any proved positive
overlap quantum. The explicit pairwise Q formula above is only asserted for
the common-start integer case. For arbitrary real speeds/phases a uniform
positive endpoint-spacing quantum need not exist, so (3) must not be silently
extended to that setting.

## 4. Phase-sensitive version from the actual starting time

Let `m_L=M(L)`, with threshold equality counted as safe. Exactly m_L blocked
occurrences contain L. Among the selected I_j, at most m_L can contain L.
Every other selected occurrence starts at or after L and overlaps the previous
selected union, inside `[L,t_N]`, by at least eta. Integrating the selected
excess multiplicity only from L to t_N gives

`(N-m_L)*eta <= H(t_N)-H(L) <= H_max-H(L)`.

Therefore

`N <= K_phase := m_L + floor((H_max-H(L))/eta)`.       (4)

Use the smaller of (2) and (4). If all residual runners are safe at L, the
algorithm should return L immediately; the bound itself need not evaluate to
zero in that case. Formula (4) counts all possible initially containing
occurrences, even when some are never selected, and remains a conservative
bound. It uses the actual phases at L, not an independently adjustable phase
model in a physical common-start input.

## 5. Consequence for the repeated eleven-call map

At threshold 1/8, the prior proof candidate makes the ordered triple map
S_bcd an exact earliest joint-safe selector. The repeated map

`F = P_a followed by S_bcd`

has eleven scalar calls and visits every one of the four runners. A full round
starting from an unsafe time has at least one moving call; otherwise all four
would already be safe. With a safety test after every round, (3) or (4) thus
implies termination in at most K rounds, or 11K scalar calls, where
`K=min(K_global,K_phase)` in the common-start integer case.

This bound does not require the special triple waiting estimate: any fixed
round that visits every runner has the same termination argument, with its
own number of scalar calls per round. The triple map may still reduce the
actual number of rounds. With an arbitrary fair order but unbounded delays
between visits, the nonzero-move bound survives but a bound on all calls does
not follow without a fairness rate.

Every projection preserves all possible earlier joint witnesses as upper
bounds on its output. The safe terminal output is consequently the earliest
four-runner safe time at or after L. If an iterate passes the supplied window's
right endpoint R, that window is empty; otherwise continue until safety is
verified. A residual witness after R says nothing about the safety of the core
there, and this argument never forces a successful core-safe window for a full
arbitrary eight-runner configuration.

## Review scope

The derivation has no numerical search or fitted examples. The parent should
independently audit especially (a) the potential's coefficients; (b) strict
overlap rather than contact; (c) the interval-addition excess identity; and
(d) the distinction between nonzero moves, eleven-call rounds, and bit cost.
The bound does not settle whether a smaller speed-independent number of rounds
exists, nor whether long chains can be constructed with arbitrarily many
selected occurrences. Its concrete contribution is a finite termination
certificate and a phase-sensitive explanation of what continued chains spend.
