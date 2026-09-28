# An isolated tight alignment and an opening that survives every phase

September 27, 2026 (Pacific). Baseline `f362f54b8f5077f12579076e815d505bf81cf9a6`. Companion to the [fastest-lap alignment experiment](FASTEST_LAP_ALIGNMENT_2026_09_27.md). Material AI contribution: derivation, separate mathematical review, exact checking, and writing.

**Result supplied for review:** in the fixed speed-13 control, the common-start alignment is the only phase of runner 11 with zero positive lonely duration. In the fixed speed-16 control, positive duration survives every phase of runner 11, with a uniform lower bound. These statements follow from the explicit arguments below, rather than extrapolation from the finite phase experiment.

**Status: HYPOTHESIS / proof candidates.** Separate internal reviews and exact endpoint checks support the arguments. No novelty, outside acceptance, or general Lonely Runner proof is asserted.

## The precise variation

Keep reference runner 0 fixed, total runner count n=8, and threshold 1/8. The other velocities are `1,4,5,6,7,11,V`, with V either 13 or 16. All runners except speed 11 start at the reference position. Give speed 11 initial phase `theta` modulo 1, so its position is `11t+theta` modulo 1. Write `D_V(theta)` for the total allowed duration over `[0,1]`.

Only `theta=0` is the original common-start configuration. The other phases belong to an explicitly shifted-start comparison. Conclusions for this phase family must not be substituted for the common-start conjecture at arbitrary velocities.

For every fixed theta, the constraints have finitely many threshold events in `[0,1]`. Positive allowed duration therefore supplies a time when all seven distances are strictly greater than 1/8. Isolated equality contacts are recorded separately.

## 1. Speed 13: only the original phase is tight

The proposed quantitative bound is

\[
D_{13}(\theta)\ge
\frac{\min\{\|\theta\|,1/4\}}{11},
\qquad 0\le\theta<1,
\]

where `||theta||=min(theta,1-theta)`. At theta=0, exact reconstruction gives only the four valid points `1/8,3/8,5/8,7/8`, so `D13(0)=0`. Every nonzero phase has a positive lower bound.

The unchanged runners `1,4,5,6,7,13` are safe throughout

\[
K_-=[17/48,3/8],\qquad K_+=[5/8,31/48]=1-K_-.
\]

Their safe-lap integers on K_minus are `0,1,1,2,2,4`, respectively. Endpoint checking puts each entire interval inside its corresponding safe lap; all six constraints are strict in the interior. In particular, speed 6 controls the left endpoint 17/48, while speeds 5 and 13 reach their upper safety boundary together at 3/8.

Map these two safe intervals to runner 11's phase circle before adding theta. Their images are

\[
11K_-\pmod1=[-5/48,1/8],\qquad
11K_+\pmod1=[-1/8,5/48].
\]

Their union is exactly `[-1/8,1/8]`, an arc of length 1/4. At theta=0, this coincides with the closure of runner 11's blocking arc. A nonzero phase displaces the blocking arc by circular distance `d=||theta||`. Two arcs of length 1/4 overlap in length `1/4-d` when `d<=1/4`, and have zero overlap measure when `d>=1/4`. Thus at least `min(d,1/4)` of the fixed phase union is safe. Each image map is injective and has slope 11, so its preimages in K_minus/K_plus supply at least `min(d,1/4)/11` clear time. Overlap of the two images increases preimage multiplicity and cannot weaken this bound.

There is also a direct one-sided witness construction. For `0<theta<=1/2`, put `d=min(1/48,theta/11)`. If `t=3/8-h` with `0<=h<=d`, then

\[
11t+\theta=4+\left(\frac18+\theta-11h\right).
\]

The phase in parentheses is between 1/8 and 5/8, so speed 11 is safe. The entire interval `[3/8-d,3/8]` survives, and its interior is strict. Its length is d.

For `1/2<=theta<1`, reflect time by `t -> 1-t` and phase by `theta -> 1-theta`. This preserves circular distances because all velocities are integers. The reflected interval starts at 5/8 and has length `min(1/48,(1-theta)/11)`. This gives the additional explicit witness bound `min(1/48,||theta||/11)`; the phase-union argument above gives the stronger displayed duration bound. At theta=0 use the independently reconstructed original allowed set.

The arithmetic source of the pinch is visible at the odd-eighth contacts. Modulo eight, `13=5` while `11=-5`. At 3/8, speeds 5 and 13 leave safety as speed 11 enters it; at 5/8 the directions reverse. Changing speed 11's phase separates these coincident boundary events and opens one side. The proof uses the full safety of every unchanged runner on K_minus/K_plus, not just a pair of controlling equalities.

At least one isolated contact also survives every phase: times 1/8 and 7/8 remain isolated under the unchanged speed-1/speed-7 constraints, and runner 11's phases there are separated by one quarter of the circle. Its strict blocking arc has length one quarter and cannot contain both points. Thus the appearance of a positive interval need not eliminate all isolated contacts.

We can also describe the complete phase projection for this control. Let A13 be the full allowed set for the unchanged six speeds `1,4,5,6,7,13`. Then

\[
\{11t\pmod1:t\in A_{13}\}
=[-1/8,1/8]\ \cup\ \{3/8,5/8\}
\quad\text{on the phase circle}.
\]

The K intervals prove inclusion of the whole arc. Every projected phase outside that closed arc would be safe for speed 11 at theta=0, and hence come from the already computed full tight allowed set, the four odd eighths. Their images add only 3/8 and 5/8 outside the arc, and both are attained. This derivation explicitly uses the known tight result; it is not an independent proof of global existence. At the original phase, the two arc endpoints and the two isolated projected points explain four contacts of different geometric origins. The projection alone does not specify the multiplicity of safe-time preimages, needed for exact duration.

## 2. Speed 16: a uniform positive margin for every phase

The proposed uniform bound is

\[
D_{16}(\theta)\ge\frac1{176}
\quad\text{for every }\theta\in\mathbb R/\mathbb Z.
\]

The unchanged runners `1,4,5,6,7,16` are safe throughout the two disjoint intervals

\[
J=[25/56,15/32],\qquad 1-J=[17/32,31/56].
\]

For J, their safe-lap integers are `0,1,2,2,3,7`, respectively. These are direct closed-interval inclusions, with strict safety in the interiors. Each interval has length 5/224.

Map these two intervals to runner 11's phase circle before adding theta. Their images can be written as arcs

\[
11J\pmod1=[-5/56,5/32],\qquad
11(1-J)\pmod1=[-5/32,5/56].
\]

They overlap, and their union is the arc `[-5/32,5/32]` of length 5/16. A phase shift of runner 11 moves its blocking arc, but that arc always has length 1/4. It therefore leaves at least `5/16-1/4=1/16` of this union safe, for every theta.

The phase map has slope 11 and is injective on each of J and 1-J. Every surviving phase has at least one preimage in their union. Pulling back the remaining phase measure therefore leaves time measure at least `(1/16)/11=1/176`. Overlapping image portions can have two preimages, which can only increase that lower bound. Endpoint inclusion does not affect the positive duration conclusion.

This argument uses the union of the two phase-image arcs, retaining their placement. It does not add their lengths as though the images were disjoint. At theta=0 the actual full duration is `39/4928`, larger than the uniform bound; sharpness of the bound is not asserted.

## What these arguments distinguish

The speed-13 configuration has an exact alignment at which interval openings disappear while equality contacts survive. Within this particular phase family, any nonzero phase change creates positive duration, with a lower bound tending to zero as the phase approaches the original alignment.

The speed-16 configuration has enough phase-image spread across two safe time intervals that one blocker of width 1/4 cannot cover both images. This guarantees positive duration independently of speed 11's phase. It is a geometric robustness certificate for this fixed family.

Both arguments depend on specific safe intervals supplied by the other runners. They do not prove that arbitrary configurations have intervals with these properties. That remaining existence requirement is the limit of transfer to the general conjecture.

The [arithmetic review](../reviews/2026-09-27-fastest-laps/arithmetic.md) and [challenge review](../reviews/2026-09-27-fastest-laps/challenge.md) record exact interval checks, phase-image identities, separate reviews, and the distinction between the continuous arguments and the finite 29-offset experiment. The source protocol and reproducible artifacts are linked from the [main report](FASTEST_LAP_ALIGNMENT_2026_09_27.md).
