# Phase projections, multiplicity, and two-time certificates

September 27, 2026 (Pacific research date; completed September 28 UTC). Baseline `0d67b3077af417f8b3e365b18bb2a6cb92b76189`. Material AI involvement: coordinating synthesis and six workers supplied calculations, separate verification, mathematical review, and writing. This continues [fastest-lap alignment](FASTEST_LAP_ALIGNMENT_2026_09_27.md) and [restricted phase robustness](PHASE_ROBUSTNESS_2026_09_27.md).

**The complete study separates existence, duration, and the locations of surviving times. It also reduces all-phase existence at our threshold to a two-time certificate.** The exact phase profiles for the two existing controls are independently reproduced. General geometric implications remain HYPOTHESIS / proof candidates under [the evidence rules](../CLAIM_STATUS.md); no novelty or general Lonely Runner proof is claimed.

## Scope and plan executed

The [frozen protocol](../reviews/2026-09-27-phase-projection/protocol.json), SHA256 `8eba9a06595a2014095f84cc22c6b91d65d6f9fd71771912e0af368293bdff17`, fixes only

\[
\{0,1,4,5,6,7,11,13\},\qquad
\{0,1,4,5,6,7,11,16\}.
\]

Reference 0, total runner count n=8, and threshold delta=1/8 are retained. Only runner 11 may start at phase theta; all other runners remain common-start. **Theta=0 is the original conjecture's input. Other phases are a separately labeled experiment.** The period is `[0,1]`, and the phase circle identifies 0 with 1.

The six assignments were: primary phase projection; independent time-domain reconstruction; challenge and endpoint review; arithmetic certificates; representation limits; and exact verification of the two prescribed time pairs. The time pairs were fixed before the new profile calculation: `{1/8,7/8}` for V=13 and `{7/15,8/15}` for V=16. One abstract time-set countermodel was permitted. No new speed lists or arbitrary phase grid were added.

## What the representation retains

Let A be all times when the six unchanged speeds `1,4,5,6,7,V` are at distance at least 1/8. Define

\[
P=\{11t\bmod1:t\in A\},\quad
N(x)=\#\{t\in A:11t\bmod1=x\}.
\]

Let B be the closure of the positive-length interval pieces of P. Isolated phase points belong to P but can be absent from B. Runner 11 blocks the open phase arc `O_theta={x: ||x+theta||<1/8}`; let its closed safe complement be S_theta. Then

\[
D(\theta)=\frac1{11}\int_{S_\theta}N(x)\,dx.
\]

The factor 1/11 converts phase length to time length on each preimage branch. Equality points contribute valid instants but no duration.

| Information retained | Question it answers | Information still missing |
| --- | --- | --- |
| Full P, including isolated points and boundaries | Is there any valid time? Is the outcome empty, contact-only, or strict? | Exact duration and actual time preimages |
| B | Is the duration positive? What is the support-only estimate `E=|B intersect S_theta|/11`? | Isolated phase witnesses and multiplicity |
| N almost everywhere | What is the exact duration profile D? | Exceptional endpoint counts and time identities |
| Pointwise N | Also all phasewise statuses and the number of contacts when D=0 | Which time branches supply the counts |
| Full fibers, with branch identities and event-point preimages | The entire surviving time set, including isolated contacts | No time-set information is lost |

In this finite-union setting B is recoverable from P, so full P alone already decides positive duration. Exact fibers remain necessary for locating times and resolving how branches meet. A count at an endpoint does not identify its contributing time branches. See [representation.md](../reviews/2026-09-27-phase-projection/representation.md) for precise assumptions and the distinction between almost-everywhere and endpoint data.

## Exact results over the whole phase circle

The primary method pushes A into phase space and integrates multiplicities. The independent verifier instead intersects A directly with runner 11's moving safe intervals in time. It derives the complete breakpoint set from boundary-equality equations, so the continuum conclusion does not rest on phase sampling.

| Quantity | V=13 | V=16 |
| --- | --- | --- |
| Unchanged safe-time duration `|A|` | 115/2184 | 7/96 |
| Phase-support measure `|P|=|B|` | 1/4 | 151/448 |
| Shortest containing arc c(P) | 3/4 | 45/64 |
| Shortest containing arc c(B) | 1/4 | 45/64 |
| Largest bulk multiplicity | 3 | 4 |
| Minimum clear duration D | 0 | 39/4928 |
| Phases attaining the minimum | 0 only | Circular interval `[-1/48,1/48]` |
| Maximum clear duration D | 115/2184 | 7/96 |
| Phases attaining the maximum | `[1/4,3/4]` | `[61/128,67/128]` |
| Status over all phases | Contact-only at 0; strict everywhere else | Strict everywhere |

Intervals in this table include their endpoints, with circular wrap understood. At theta=0 the tight configuration retains exactly the four odd eighths. The strict configuration retains its previously known four intervals with total duration 39/4928.

The complete projections, written on the circle, are

\[
P_{13}=[-1/8,1/8]\cup\{3/8,5/8\},\qquad B_{13}=[-1/8,1/8],
\]

\[
P_{16}=B_{16}=[-5/32,5/32]
\cup[19/56,45/128]\cup[83/128,37/56].
\]

For V=13, the two isolated phase points change the covering-arc length and preserve additional contacts. **They are not necessary for all-phase nonemptiness in this particular control:** the closed bulk arc itself has length 1/4 and already protects its endpoints when its interior is blocked. Dropping the extra points loses two contacts at phase zero, rather than turning a feasible phase into an empty one.

For V=16, the complete support improves the preceding lower bound `1/176` to

\[
D_{16}(\theta)\ge\frac{|B_{16}|-1/4}{11}
=\frac{39}{4928}.
\]

The profile attains this bound, so it is the exact minimum over every runner-11 phase. The improvement is 1/448, contributed by the two extra outer phase arcs. This gives a useful qualification: multiplicity is not needed for every quantitative conclusion. Here support measure alone determines the exact worst-phase duration, once attainment is checked.

## An exact collision in the support-based estimate

At phases 0 and 1/32 in the same V=16 configuration, the support-only estimate E is identical, but the actual durations differ:

| Phase theta | Support-only estimate E | Actual duration D | D minus E |
| --- | --- | --- | --- |
| 0 | 39/4928 | 39/4928 | 0 |
| 1/32 | 39/4928 | 131/14784 | 1/1056 |

Both phases are algebraic events in the frozen exact calculation. This is a collision of one scalar summary, not identical phase placements or identical runner configurations. The missing quantity is exactly

\[
D(\theta)-E(\theta)=\frac1{11}
\int_{B\cap S_\theta}(N(x)-1)\,dx.
\]

The support-only minimum plateau extends to `[-1/32,1/32]`; the true minimum plateau extends only to `[-1/48,1/48]`. Multiple safe times can project to the same surviving phase, and counting that phase once loses their additional duration.

A stronger representation counterexample uses the one permitted **abstract, nonphysical** pair:

\[
A_1=[1/44,1/22],\qquad
A_2=A_1\cup[5/44,3/22].
\]

Both project under `11t mod1` to exactly `[1/4,1/2]`. At phase 0 their durations are 1/44 and 1/22. At phase 5/8 they retain respectively two and four isolated endpoint times. Thus even identical complete P does not determine duration or contact count. These sets are not asserted to arise from runner configurations; their role is to prove what the projection operation discards.

## Covering arcs and two-time certificates

For a nonempty compact phase set K, write c(K) for its shortest containing closed circular arc. For our finite unions it equals one minus the largest circular gap. The endpoint distinction gives

\[
\begin{aligned}
\text{valid time for every phase}&\iff c(P)\ge1/4,\\
\text{positive duration for every phase}&\iff c(B)>1/4.
\end{aligned}
\]

The first uses an open blocker; the second must exclude containment of bulk support in its closure. Empty sets are handled separately. These statements explain why equality can preserve an instant while permitting zero duration.

The [two-time note](TWO_TIME_CERTIFICATES_2026_09_27.md) supplies a smaller certificate. If every unchanged runner is at distance at least c at both times and the selected runner's two phases are separated by circular distance d, one time gives all distances at least `min(c,d/2)` after any phase shift. The circle triangle inequality proves the claim.

| Control | Two prescribed times | Minimum unchanged distance c | Selected phase separation d | Best full margin within this pair, every phase |
| --- | --- | --- | --- | --- |
| V=13 | 1/8, 7/8 | 1/8 | 1/4 | Exactly 1/8 |
| V=16 | 7/15, 8/15 | 2/15 | 4/15 | Exactly 2/15 |

For V=16 this gives strict excess 1/120 above threshold without constructing all of A. Direct time-Lipschitz bounds give duration at least 1/660; a one-sided interval refinement in [arithmetic.md](../reviews/2026-09-27-phase-projection/arithmetic.md) improves this compact-only bound to 1/352. Both are weaker than the complete projection's exact minimum. For V=13 the fixed pair remains at equality even when other times provide positive duration. Certificate performance is distinct from total available duration.

General review sharpens sufficiency to **conditional completeness**. For a compact circle set and `0<a<=1/3`, `c(P)>=a` holds exactly when some two points have circular separation at least a. At `a=1/4`, every all-phase nonempty configuration therefore admits a two-time certificate. With positive bulk support and the finite nonzero-speed assumptions, all-phase positive duration similarly admits two times strictly safe for every unchanged runner, with selected-runner phase separation greater than 1/4. The selected runner need not be safe at both times at any given phase. The strict argument requires `a<1/3`. Complete proofs and endpoint checks are in the two-time note and the challenge/arithmetic reviews.

This does not prove all-phase robustness for arbitrary speeds, nor provide a speed-based procedure finding the pair. Original common-start Lonely Runner requires only the prescribed phase. Requiring robustness to every phase is a stronger auxiliary target and must be justified if used in a general proof strategy.

## Verification and review limits

All six commands passed in read-only mode:

```bash
python -B reviews/2026-09-27-phase-projection/calculate.py --check
python -B reviews/2026-09-27-phase-projection/verify_independent.py --check
python -B reviews/2026-09-27-phase-projection/certificates.py --check
python -B reviews/2026-09-27-phase-projection/arithmetic_check.py --check
python -B reviews/2026-09-27-phase-projection/challenge_check.py --check
python -B reviews/2026-09-27-phase-projection/representation_check.py
```

The principal independent reconstruction matches every case field and digest, all phase fibers, 43 algebraically generated open phase cells, 45 endpoint evaluations including periodic closure, all extrema and plateaus, and all 29 previously archived offsets with their full allowed-time sets. Its author did not read or import the primary implementation. The challenge calculation separately checks the complete event partition and affine formulas through direct time intersections. The compact arithmetic and abstract-set checks have their own narrower scopes.

All six scripts use Python's standard library. The prior phase archive is pinned by SHA256 `612cd4320fc3083476b352f8ce058e345cf2f88a418a36e87228cdbad29c8692`. New primary results have SHA256 `daf8cadcb6f06bda538c9231f053e37c85fdaeba5fbd4167ca96d442ddc5ba34`. [schema.md](../reviews/2026-09-27-phase-projection/schema.md) defines event and boundary conventions; [manifest.json](../reviews/2026-09-27-phase-projection/manifest.json) records files and dependency hashes.

These are separately structured exact computational checks and internal mathematical reviews, not independent human review, formal proof-assistant verification, or a novelty audit. Historical checkers and archives remain unchanged.

## The next bounded investigation

The most useful next move is **arithmetic transfer of the two fixed time templates**, rather than another complete profile calculation. In the existing family `{0,1,4,5,6,7,11,V}`, derive exactly which admissible integer V make each prescribed pair a threshold or strict certificate. Here admissible means a positive integer outside `{1,4,5,6,7,11}`, preserving eight distinct speeds. The unchanged constraints at rational times become integer residue inequalities, so a finite congruence classification can describe an unbounded family without enumerating its full safe sets.

Freeze that classification task before additional computations. Preserve the residue classes neither template certifies. A failure of these particular templates is not failure of every pair, failure of phase robustness, or failure of common-start loneliness. Compare its coverage with existing family results so a better explanation is not mislabeled new existence coverage. Any further test of failed classes should have a small, declared set of representatives and a separately reconstructed check.

This next investigation is proposed, not executed here. It tests how far the two already-chosen templates certify the family without first solving its entire joint safe sets; it is not yet a general method for finding a pair. The general guarantee remains OPEN; the +7/+9 direction remains parked.
