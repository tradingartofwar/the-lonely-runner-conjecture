# Exact interval safety, consolidated findings, and the existence milestone

September 28, 2026. Baseline `9aa72796ac0f77af52edff876c154ca05b910d45`, draft PR #3.

**Status.** A complete elementary argument is supplied below; under this repository's governance it remains an AI-assisted proof candidate pending independent review. The archived numerical checks are REPRODUCED/OBSERVED within their stated scope. One coordinating AI wrote this consolidation and the two algorithm structures used for its check. No separate agents or independent human review participated in this increment. No novelty or new Lonely Runner existence coverage is claimed.

**Research decision.** Hourly continuation is paused at the maintainer's request. This increment finishes the interval argument and consolidates the accumulated findings. The next milestone concerns arithmetic that forces a useful certificate to exist; it is not another ranking refinement on the same successful windows.

## 1. The exact interval identity

Write `d(x)=dist(x,Z)`. Let `I` be any nonempty bounded interval with closure `[m-h,m+h]`, `h>=0`. For a singleton take `h=0`; an empty interval is handled separately. Let `v` and `alpha` be real, and put `rho=|v|h`. Then

\[
\inf_{t\in I}d(vt+\alpha)
=\min_{t\in\overline I}d(vt+\alpha)
=\max\{d(vm+\alpha)-|v|h,0\}. \tag{1}
\]

For an open or half-open interval the infimum need not be attained. This is why the first expression is an infimum, not necessarily a minimum.

**Proof.** The image of the closed interval is `[x-rho,x+rho]`, where `x=vm+alpha`. The 1-Lipschitz inequality for distance to a set gives the lower bound `max(d(x)-rho,0)` everywhere on that image. Choose a nearest integer `k` to `x`. If `rho>=d(x)`, the image contains `k`, attaining zero. If `rho<d(x)`, move a distance `rho` from `x` toward `k`. The resulting endpoint is distance `d(x)-rho` from `k`, so it attains the lower bound. This includes `v=0`. Finally, continuity and density of a positive interval in its closure make its infimum equal the closed minimum. The singleton case is direct. This proves (1).

For any **positive** threshold `delta`, define

\[
S(v,I)=d(vm+\alpha)-|v|h-\delta.
\]

Since `delta>0`, equation (1) gives the equivalence

\[
\boxed{S(v,I)\ge0\quad\Longleftrightarrow\quad
       d(vt+\alpha)\ge\delta\text{ for every }t\in I.} \tag{2}
\]

If `S<0`, the closed minimum is strictly below `delta`. If its minimizer is an omitted endpoint of a positive interval, continuity supplies nearby interior points that are also strictly below `delta`. Thus removing an endpoint cannot rescue this failed weak-safety test.

Two boundaries matter:

- A zero score may still give strict safety everywhere in an **open** interval: `(1/8,7/8)` at speed 1 is an example. Equation (2) concerns weak safety, with equality allowed, and does not equate zero score with an attained equality point.
- The unclipped score is not always the numerical minimum margin. That minimum is `max(d(vm+alpha)-|v|h,0)-delta`. Their signs agree for positive `delta`; their values can differ when the interval crosses an integer.

The phase and signed-speed notation only state the scalar lemma generally. All physical archival checks below retain common start, positive relative speeds, selected reference 0, eight total runners and `delta=1/8`.

## 2. Unions and the precise correction to the earlier note

For a finite union of positive intervals, apply (2) on every component and to every complementary runner. The compound containment holds exactly when the minimum of all component scores is nonnegative. The empty union is vacuously contained. Any separately supplied isolated points must be checked directly; they cannot be discarded using duration information.

For the strict blocking sets `B_a,B_b` restricted to a positive closed window, their intersection is relatively open in that window. It cannot have an isolated component: any point satisfying both strict inequalities has a one-sided or two-sided neighborhood satisfying them. Thus its positive components exhaust the actual base intersection. This fact does not remove isolated points from the **full safe set**, which uses weak inequalities.

The earlier [Lipschitz note](LIPSCHITZ_COMPONENT_MARGIN_2026_09_28.md) froze a sufficient-only interpretation and explicitly queued this stronger argument. Its historical calculation remains unchanged. The current interpretation is now:

> A negative corrected score proves that this particular compound containment fails. It remains inconclusive about lonely time, the success of another pair, or another window.

This conclusion follows from the argument, not from counting successful examples.

## 3. Exact audit on existing records

The scope was written in [protocol.json](../reviews/2026-09-28-exact-interval/protocol.json) before this calculation. The input is the pinned selector-transfer archive, SHA256 `bc6c3c87803057632e80d85f74af40a6a7f83bebce27b19f0dc3fce9e4e11615`. This is an archival proof audit, not prospective selector validation.

The checker reconstructs base components by intersecting rational lap intervals and computes the new scores before consulting archived containment answers. A separately structured threshold-event sweep then tests the entire containment on open cells and endpoints. Endpoint/integer enumeration independently checks each scalar exact-minimum formula. Both implementations are by the same author.

| Audited item | Result |
| --- | ---: |
| Previously selected minimum-component pairs | 10/10 remain containing |
| Eligible archival pairs, including rejected alternatives | 38 |
| Existing strict16 calibration pairs | 2 |
| Positive base components across those 40 pair records | 62 |
| Exact scalar minimum comparisons | 124, all agree |
| Containing / noncontaining pair records | 22 / 18 |
| Multi-component pair records | 20: 4 contain, 16 fail |
| Archived query comparisons | 39, all agree; the second strict16 pair is checked directly |
| Named elementary boundary fixtures | 8, all agree |

All ten selected archival pairs still have exactly one component. The already archived alternatives supply the multi-component test; no new speeds or windows were introduced. Reflections remain dependent symmetry checks. These counts overlap; they are not independent replications.

`doubling_112` retains its earlier pair-only exit `761/32256`. `tight_13` retains its isolated valid time `3/8`, with opposing one-sided blockers. No duration is inferred from that point.

Reproduce from the repository root:

```bash
python -S -B reviews/2026-09-28-exact-interval/check.py --check
```

The deterministic output, including every score and an exact event witness for each failed containment, is [results.json](../reviews/2026-09-28-exact-interval/results.json). The scalar fixtures include open equality endpoints, an excluded strictly failed endpoint, an integer crossing, a half-integer cusp, an interval spanning multiple laps, a negative speed with phase, and zero speed. They are lemma fixtures, not new runner configurations.

## 4. What the overnight sequence established

| Consequential distinction | Evidence and current limit |
| --- | --- |
| Separately avoidable overlaps can be jointly unavoidable under full coverage | [Collective window](COLLECTIVE_WINDOW_AUDIT_2026_09_28.md) and [joint restrictions](JOINT_TRIPLE_EXCLUSIONS_2026_09_28.md): an actual runner window has duration `1/600`; no single triple upper bound eliminates every summary-compatible cover, but two simultaneous bounds do. The alternative covers are abstract state distributions, not alternative runner realizations. |
| One shared occurrence can certify two restrictions | [Shared pair](SHARED_PAIR_CONTAINMENT_2026_09_28.md): one base intersection is safe for both complements. It still contains two safety predicates and assumes a supplied pair/window. |
| Fewer components and larger potential slack are different ranking signals | [Selector transfer](SELECTOR_TRANSFER_AUDIT_2026_09_28.md): component count alone does not distinguish a tied success and failure; lexicographic choice matters. The finite successes do not force future success. |
| Midpoint safety alone loses motion inside the interval | [Midpoint failure](TIE_MIDPOINT_DISCRIMINATOR_2026_09_28.md), corrected by (1)-(2): midpoint, width and speed exactly decide containment once the base components are known. |
| Efficient representation is distinct from an existence argument | [Floor sums](FLOOR_SUM_COMPONENT_COUNT_2026_09_28.md) avoid per-lap counting but establish no runtime advantage on the active small cases. Exact interval checking still requires base-component information. |

The central joint-restriction example was also independently reconstructed in the preceding interactive review: 17 exact threshold cells reproduce `U=1/600`, the two zero triples, and lower bounds `49/524400` and `13/22800`. That review also reran both pinned Lipschitz implementations successfully. Those are supporting reproductions, not new cases or external certification.

There are now three different tasks:

1. **Verify a supplied containment:** equation (2) settles this exactly after base components are known.
2. **Find a useful certificate:** ranking pairs, choosing cores/windows and obtaining component endpoints still cost information and computation; no general successful selector follows.
3. **Force a useful certificate to exist:** the common-start arithmetic must prevent every relevant window from failing. This is the remaining structural milestone.

## 5. A concrete algebraic interface for the next milestone

For positive speeds `a,b` and a core-safe window `J=[L,R]`, a base blocking occurrence with integer lap labels `p,q` has endpoints

\[
\ell=\max\{L,(p-\delta)/a,(q-\delta)/b\},\qquad
r=\min\{R,(p+\delta)/a,(q+\delta)/b\}.
\]

Only `ell<r` contributes a positive component. For a positive complement speed `v`, the equivalent safe-lap condition is

\[
\exists z\in\mathbb Z:\quad z+\delta\le v\ell,
\quad vr\le z+1-\delta,
\]

or, without an existential integer search,

\[
\left\lceil vr-1+\delta\right\rceil
\le\left\lfloor v\ell-\delta\right\rfloor. \tag{3}
\]

For `0<delta<=1/2`, the connected lifted interval must fit in one closed safe lap. This proves (3)'s equivalence to containment. The same lap labels and speed relations govern every occurrence; they cannot be chosen independently in different windows. Equations (2)-(3) supply a precise place to seek arithmetic forcing, but writing them down does not force their feasibility.

For four residual blockers `a,b,c,d`, the existing five-edge inequality also requires positive slack

\[
C_0-O_{cd}>0,\qquad C_0=|J|-\sum_vD_v+\sum_{u<v}O_{uv}.
\]

If every `a,b` component satisfies (3) for both `c,d`, the two corresponding triple intersections vanish, and `U_J>=C_0-O_cd`. Therefore **placement and positive slack must be forced together**. A containment by itself is insufficient, as the tight control already shows.

## 6. Next milestone and stopping rule

**Question:** What explicit speed relationship forces at least one useful window and compatible local certificate, without first reconstructing the complete lonely-time set?

The next manually directed increment should target linked coverage requirements across windows, rather than optimize scores inside already successful windows:

1. Audit the existing [fastest-lap alignment](FASTEST_LAP_ALIGNMENT_2026_09_27.md), [core transfer](CORE_TRANSFER.md), [uniform triangle](UNIFORM_TRIANGLE_CERTIFICATE.md), and [affine review](REVIEW_AFFINE_FAMILY.md). Fixed-core transfer, restricted small-gcd coverage and exact fastest-core duration are prior results; do not relabel them as new coverage.
2. Use the already available tight13 and strict16 fastest-lap records as development controls. Choose non-reflected windows when testing independent restrictions. Express hypothetical complete-cover chains with their actual shared lap labels. Ask whether covering two or more windows forces inconsistent integer/residue requirements under a stated speed relation.
3. Seek one parameterized proposition: explicit arithmetic hypotheses force a positive-slack certificate somewhere, or force a valid equality contact with its endpoint conditions. Derive it before evaluating the full answer. If the hypotheses only recover a known family, record that fact and identify the unresolved extension.
4. Accept either a proof candidate with a clearly broader structural scope, or an exact compatible-cover/counterexample showing why the proposed cross-window requirement is insufficient. Further score refinements on this same archive are not the default continuation.

This is a research target, not a claim that the shared-pair certificate is universally complete or that all strict lonely configurations admit its particular five-edge form. A negative local score, zero duration, absence of a selected certificate and absence of every valid lonely time remain different statements.

No broad speed search, all-reference scan, paid compute, external outreach, merge to main, or parked `+7/+9` campaign is part of this increment. Hourly research remains paused until explicitly resumed. General Lonely Runner existence and the novelty of restricted arguments remain unresolved by this work.
