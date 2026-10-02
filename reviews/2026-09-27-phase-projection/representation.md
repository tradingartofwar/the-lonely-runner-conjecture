# What each phase representation determines

September 27, 2026 Pacific research date; written September 28 UTC. Scope: `protocol.json`, SHA256 `8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17`; the two fixed controls; and its one permitted abstract time-set pair. Materially AI-assisted. No literature search, extra runner configuration, or phase grid was added. General implications below are supplied proof candidates under `CLAIM_STATUS.md`.

**The full phase projection determines existence and strict-versus-contact-only status, but not duration or the identities of the surviving times.** Multiplicity restores duration. Exact fibers restore the times themselves. Endpoint values must remain distinct from almost-everywhere data.

## Exact definitions and decision rules

Let A be the complete closed safe-time set of the unchanged six runners on `[0,1]`, a finite union of closed intervals and isolated points. Put `f(t)=11t mod1`, and define

\[
P=f(A),\qquad F(x)=\{t\in A:f(t)=x\},\qquad N(x)=|F(x)|.
\]

Let B be the closure of the occupied positive-length phase cells. In this finite-union setting,

\[
B=\overline{\operatorname{int}P}.
\]

Thus B is recoverable from full P; it is not an extra datum needed to decide strictness when full P is retained. B can omit isolated projection points of P. Conversely, an isolated *time* may project inside B, so `P minus B` does not list every isolated safe time.

For phase theta, let `O_theta={x: ||x+theta||<1/8}` be runner 11's open blocking arc, and let `S_theta` be its closed complement. Directly:

\[
\begin{aligned}
\text{some allowed time exists}
 &\iff P\cap S_\theta\ne\varnothing
 \iff P\not\subset O_\theta,\\
D(\theta)
 &=\frac1{11}\int_{S_\theta}N(x)\,dx,\\
D(\theta)>0
 &\iff |B\cap S_\theta|>0
 \iff B\not\subset\overline{O_\theta}.
\end{aligned}
\]

The factor `1/11` comes from each affine preimage branch `t=(j+x)/11`; integrating counts every branch once. For these nonzero-speed runner constraints, positive duration is equivalent to existence of a fully strict time: only finitely many times have an equality constraint. Contact-only status is exactly `P not subset O_theta` together with `B subset closure(O_theta)`.

The final strictness equivalence uses B's definition as the closure of its positive-length interval pieces. It is not asserted for arbitrary closed sets with different measure-theoretic structure.

## The sufficient-statistic hierarchy

| Retained object | What it determines exactly | What it omits |
| --- | --- | --- |
| Full P, with isolated points and circle endpoints | Phasewise empty/contact-only/strict classification, since it also determines B | Multiplicity, exact duration, safe-time locations, and contact counts |
| Full B | Phasewise positive-duration versus zero-duration classification; the unweighted estimate `|B intersect S_theta|/11` | Extra equality witnesses from `P minus B`; multiplicity |
| Support measure `|P|=|B|` | Some sufficient bounds, including `D(theta)>=(|B|-1/4)/11` when the right side is positive | Placement around the circle, precise statuses, and multiplicity |
| Minimum covering-arc length of P and of B | All-phase existence and all-phase strictness, using the distinct inequalities below | Which individual phases are exceptional; exact duration |
| N almost everywhere | The entire exact duration profile D, hence strictness; also `|A|=(1/11) integral N` | Isolated phase images and exceptional endpoint counts |
| Pointwise N, including every event value | Also P, all phasewise statuses, and total contact count when D=0 | Which time branches supply those counts |
| Full fibers F(x), encoded by affine branches on cells and exact event lists | The complete allowed-time set for every phase, witnesses, interval endpoints, and all isolated times | No time-set information is lost by this encoding |

When D=0, `P intersect S_theta` is finite and the contact count is `sum_x N(x)` over those phases. Almost-everywhere N cannot supply this sum. If positive intervals coexist with isolated times, even a pointwise count can obscure which left and right phase branches join at the same time; fiber identities resolve that distinction. Counts and lifts should not be conflated.

The unweighted estimate is a lower bound because `N>=1` almost everywhere on B. It is not another runner realization. Its difference from D is exactly

\[
D(\theta)-\frac{|B\cap S_\theta|}{11}
 =\frac1{11}\int_{B\cap S_\theta}(N(x)-1)\,dx.
\]

A useful conservation identity is

\[
\int_0^1D(\theta)\,d\theta=\frac34|A|.
\]

Each fixed time is safe for runner 11 during exactly three quarters of its possible initial phases. This mean does not determine the phase profile. Nor should the full function N be called a uniquely recoverable or minimal representation of D: the formula supplies weighted moving-arc integrals, which are the data D actually uses.

## Covering length: the endpoint distinction is decisive

For a nonempty compact circle set K, let c(K) be the length of its shortest containing closed circular arc. For these finite unions, `c(K)=1-g(K)`, where g is the largest complementary circular-gap length. A singleton has c=0; the full circle has c=1. Empty sets are handled separately.

The exact criteria are

\[
\begin{array}{ll}
\text{an allowed time exists for every phase} &\iff c(P)\ge1/4,\\
\text{positive duration exists for every phase} &\iff c(B)>1/4.
\end{array}
\]

For the first statement, complete blocking requires P to fit inside an **open** arc of length 1/4. Compactness gives room at both ends, so this occurs exactly when `c(P)<1/4`. At equality, extreme points cannot both fit strictly inside the blocking arc: equality witnesses are protected.

For the second, zero duration occurs when B fits inside the **closed** blocking arc of length 1/4. At equality its surviving boundary points have zero measure, so all-phase positivity requires a strict inequality. If B is empty, D is identically zero. Equivalent maximum-gap tests are `g(P)<=3/4` and `g(B)<3/4`, respectively.

These scalar criteria answer universal questions over *all* phase translations. Phasewise questions also need locations: the scalar maximum gap forgets where that gap lies. Similarly, support measure is not covering-arc length; measuring how much phase is occupied does not retain how far apart the occupied parts lie. No general existence claim follows merely from naming a set's maximum gap.

## The one permitted abstract countermodel

This is **not a pair of runner configurations**. It is an exact representation test for two finite closed time sets, using the same map `f(t)=11t mod1`:

\[
A_1=[1/44,1/22],\qquad
A_2=A_1\cup(A_1+1/11)
    =[1/44,1/22]\cup[5/44,3/22].
\]

Both have exactly

\[
P=B=[1/4,1/2].
\]

For x in that closed arc their fibers are

\[
F_1(x)=\{x/11\},\qquad
F_2(x)=\{x/11,(1+x)/11\},
\]

and are empty elsewhere. Thus their multiplicities are respectively 1 and 2 on the same projection.

| Phase of runner 11 | A1 allowed times | A2 allowed times | Difference |
| --- | --- | --- | --- |
| 0 | All of A1 | All of A2 | Durations `1/44` and `1/22` |
| `5/8` | `{1/44,1/22}` | `{1/44,1/22,5/44,3/22}` | Two versus four isolated contacts; both durations zero |

At phase `5/8`, the open blocked arc on the unshifted x circle is `(1/4,1/2)`, so exactly the projected endpoints survive. This same pair demonstrates both missing multiplicity in positive duration and missing contact counts, without introducing a second abstract example.

Reproduce the exact branch, interval, endpoint, and duration checks:

```bash
python -B reviews/2026-09-27-phase-projection/representation_check.py
```

## What the fixed two-time certificate earns

For V=16, the protocol fixed `t_-=7/15` and `t_+=8/15=1-t_-` before the phase profile calculation. Direct substitution gives the same unchanged-runner distances at both times:

| Speed | 1 | 4 | 5 | 6 | 7 | 16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Distance | `7/15` | `2/15` | `1/3` | `1/5` | `4/15` | `7/15` |

Runner 11's unshifted phases at these times are `2/15` and `13/15`, with circular separation `4/15`. For every common phase translation of this pair, at least one point has distance at least `2/15` from the origin: two points closer than that would fit in an open arc shorter than their separation. At the selected candidate all seven runners therefore have distance at least `2/15`, strictly above `1/8` by `1/120`.

This verifies all-phase strict existence for this fixed family using **two directly checked times**, without constructing the full unchanged safe set A. It additionally supplies a quantitative neighborhood: the smallest unchanged margin divided by speed is `1/480` (runner 4); runner 11's guaranteed margin divided by speed is `1/1320`. The closed radius-`1/1320` interval around the successful candidate is safe, with a strict interior. Hence this compact argument yields `D16(theta)>=1/660`. This is weaker than the earlier two-interval lower bound `1/176`, but uses a smaller certificate. It is not asserted optimal.

For V=13, the protocol's pair `1/8,7/8` has runner-11 phase separation exactly `1/4`. It guarantees a nonempty allowed set for every phase because the blocking arc is open. The unchanged speed-1 and speed-7 constraints leave these times isolated, so that pair alone supplies neither a strict witness nor positive duration. The earlier interval argument provides strictness for nonzero phase separately.

The compact certificate moves the burden from constructing all of A to verifying a small subset of A with useful phase separation and unchanged-runner margins. It does not show that arbitrary velocity lists admit such a pair or such margins. That selection/existence requirement remains the general gap; a successful fixed pair does not establish that missing universal statement.

## Fixed-control profile results

The exact [results](results.json) and [independent verification](verification.json) were inspected. The latter reconstructs time-domain intersections independently over all algebraically generated critical phases and all 43 intervening cells, with a completeness argument for the breakpoints. It also checks all 29 pinned prior offsets. The following values are **OBSERVED / independently REPRODUCED** in those two fixed phase families, not inferred from a phase grid.

| Quantity | V=13 | V=16 |
| --- | --- | --- |
| Unchanged safe-time duration `|A|` | `115/2184` | `7/96` |
| Projection/support measure `|P|=|B|` | `1/4` | `151/448` |
| Minimum covering-arc length c(P) | `3/4` | `45/64` |
| Minimum covering-arc length c(B) | `1/4` | `45/64` |
| Maximum bulk multiplicity | 3 | 4 |
| Exact minimum D | 0, only at phase 0 | `39/4928`, on the circular interval `[-1/48,1/48]` |
| Exact maximum D | `115/2184`, on `[1/4,3/4]` | `7/96`, on `[61/128,67/128]` |

Here

\[
P_{13}=[-1/8,1/8]\cup\{3/8,5/8\},\qquad
B_{13}=[-1/8,1/8]
\]

on the circle. Full P protects existence at every phase; B fits exactly in a closed blocking arc at phase zero, allowing only contacts then. Those are the two distinct covering-length inequalities in a single physical control.

For V=16, `P=B`, and its support measure alone yields

\[
D_{16}(\theta)\ge
\frac{151/448-1/4}{11}=\frac{39}{4928}.
\]

The archive shows this lower bound is attained, so it is the exact worst-phase duration. **Multiplicity is not required for every quantitative conclusion.** It is required to recover this family's full profile from its projection: the unweighted estimate has maximum `151/4928`, whereas D reaches `7/96`. Even its minimum plateau is different: the unweighted estimate stays minimal on `[-1/32,1/32]`, while the actual D stays minimal only on `[-1/48,1/48]`.

For V=13 the same distinction is substantial: the unweighted support estimate reaches only `1/44`, while the true maximum is `115/2184`. Projection geometry answers whether an opening exists; multiplicity measures how many separate time branches contribute to its duration. The [two-time certificate](certificates.md) answers a smaller existence question without reconstructing either complete profile.
