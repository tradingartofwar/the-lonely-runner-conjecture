# The fastest runner makes the local tree certificate exact

September 27, 2026 (Pacific research date). Baseline `910a26b044d6ea093a0d22aa678304a02e7e2642`. This arose during the authorized [six-agent transfer experiment](../reviews/2026-09-27-team/protocol.json), following the [relationship-selector study](RELATIONSHIP_SELECTOR_2026_09_27.md).

**Main finding:** a supplied general argument explains the previously open some-core tree-certificate hypothesis. Choose a core containing a fastest runner relative to the selected reference. Each complete core-safe window is short enough that each residual blocker is a single interval or empty. For a finite family of intervals on a line, the optimal tree bound equals the actual uncovered duration.

Consequently, if strict lonely time exists, every such core has a positive tree certificate somewhere. A core consisting of the fastest runner alone already has this property; three core runners are not essential. This is a statement about representing and detecting existing strict lonely time. It does not establish that lonely time always exists.

**Status:** HYPOTHESIS / proof candidate with a complete supplied argument, separate AI mathematical reviews, and separately implemented finite checks recorded in the companion [team report](TEAM_TRANSFER_2026_09_27.md). No novelty or full Lonely Runner proof is claimed. AI materially contributed the argument, review, calculations, and writing; model agreement is not itself proof certification.

## Definitions and scope

Fix a reference runner and let `v_i` be the absolute values of its nonzero relative velocities. Distinct original velocities can give equal absolute values; keep their runner labels and the original threshold. Put `V=max_i v_i` and choose a threshold `0<delta<1/2`. For Lonely Runner, `delta=1/n` with n the total number of runners (the two-runner endpoint case delta=1/2 is outside this formulation).

Define the strict blocking set `B_i={t: ||v_i t||<delta}`. Its complement is closed and includes equality. A core C is any nonempty collection of nonreference labels that includes a label with speed V. Let W be a complete connected component of the times when all core runners are safe, optionally intersected with a fixed closed observation interval. We work on the time line, not with time endpoints identified. The local argument applies to real relative speeds; the accompanying finite experiment uses positive integers and the full period `[0,1]`.

For residual labels R, let `D_i=|B_i intersect W|` and `O_ij=|B_i intersect B_j intersect W|`, where bars denote length. The optimal tree certificate is

\[
Q_C(W)=|W|-\sum_{i\in R}D_i+
\max_{T\text{ spanning }R}\sum_{ij\in T}O_{ij}.
\]

With zero residual labels this is `|W|`; with one it is `|W|-D_i`.

## 1. A fastest-core window prevents repeated blocking pieces

A safe lap of speed v is

\[
[(m+\delta)/v,(m+1-\delta)/v],
\]

of length `(1-2delta)/v`. Since W is contained in one safe lap of V,

\[
|W|\le (1-2\delta)/V\le (1-2\delta)/v_i.
\]

The rightmost quantity is also the length of the closed safe gap between consecutive strict blocking intervals of runner i. If W met two such blocking intervals, two of its points would lie strictly beyond the two ends of that safe gap. Their separation would exceed the gap length, contradicting the bound on `|W|`.

Thus each `B_i intersect W` is one interval or empty. Its ends may be open or closed relative to W. At equality of window and gap lengths, the gap endpoints remain safe, so they cannot supply a second blocked piece. At threshold 1/8 the relevant length is **3/(4v)**. An initial informal message used 7/(8v); review corrected that arithmetic before the written argument and checks.

## 2. The tree formula is exact for intervals

Consider any finite family of nonempty intervals `I_1,...,I_r` on a line. Sort them by their left endpoints, breaking ties arbitrarily. For each `j>1`, choose a preceding interval `I_p(j)` with largest right endpoint. Then, up to endpoints,

\[
I_j\cap\bigcup_{i<j}I_i=I_j\cap I_{p(j)}.
\]

Indeed, all preceding left endpoints are no greater than the left endpoint of `I_j`. Among the portions reaching into `I_j`, the interval with the greatest right endpoint contains every other such portion. If no preceding interval reaches it, both intersections are empty.

Each edge `j--p(j)` points to an earlier index, so the r-1 edges form a tree. Adding intervals one at a time gives

\[
\left|\bigcup_{j=1}^{r} I_j\right|
=\sum_{j=1}^{r}|I_j|
-\sum_{j=2}^{r}|I_j\cap I_{p(j)}|.
\]

Empty intervals can be attached by zero-weight edges. Endpoint flags do not change these duration identities. The usual tree inequality is a lower bound on uncovered duration for every spanning tree: at a point with a nonempty active set S, the induced forest has at most `|S|-1` edges. The tree just constructed attains the actual uncovered duration, so the maximum over all trees attains it as well.

This uses the existing graph-based union-bound framework of D. Hunter, *An upper bound for the probability of a union*, Journal of Applied Probability 13(3), 597–603 (1976), [DOI 10.2307/3212481](https://doi.org/10.2307/3212481). The targeted literature review documents its reading limits; that citation supports the general tree-bound framework, not a novelty or priority claim for this particular fastest-runner application.

## 3. Consequences and limits

Combining the two steps yields the proposed identity

\[
Q_C(W)=\left|W\setminus\bigcup_{i\in R}B_i\right|
\]

for every complete fastest-core window. Other core constraints can shorten or split the fastest runner's safe lap; they do not invalidate the length bound.

- **Conditional certificate completeness.** A strict lonely instant has a neighborhood satisfying every constraint strictly. Without observation clipping, or inside a nondegenerate observation interval containing that instant, its fastest-core component has positive actual duration and hence positive Q. A degenerate observation interval consisting only of that instant does not have positive duration. For seven distinct positive relative speeds, each of the 15 three-runner cores containing the unique fastest label works in this conditional sense.
- **The some-core hypothesis no longer needs a larger numerical campaign as its principal test.** The argument supplies a structural explanation. Finite calculations check implementations and consequences within their scope; they cannot prove the unbounded statement by accumulation.
- **One core runner is enough for exactness.** Using only the fastest runner leaves more residual vertices but still yields interval blockers. More core constraints may help certificate size or expose relations. Those are separate optimization questions.
- **A larger Q need not come from a fastest core.** Other, wider components can collect more clear duration. Exactness and maximizing the numerical lower bound are different objectives.
- **Containment is not necessary.** The interval-tree construction permits crossing intervals; it does not require each discarded blocker to lie inside another. Conditional containment remains a useful simplification.
- **Existence remains the missing step.** Exactness says Q equals the available room. It does not force any room to be positive, nor does it settle an equality-only configuration. A universal LRC argument must still preclude complete blocking or establish a valid boundary contact.

## Equality and the endpoint fallback

A zero tree value can accompany an empty allowed set or isolated valid instants. The duration identity does not erase that distinction. Any reconstruction of the full allowed set must preserve strict blocking and closed safety endpoints.

There is also a supplied completeness argument for the experiment's fallback. For positive integer speeds on `[0,1]`, if the global allowed set F is nonempty, its earliest point `a=min F` is greater than zero. At least one runner begins a safe lap at a; otherwise every runner would also be safe slightly before a. Any core containing that runner is safe at a and has a component whose left endpoint is a. Therefore a collection of cores covering every runner label includes a passing core endpoint. All 35 cores meet that condition; the 15 cores containing a fastest label also do.

This strengthens the earlier two-core procedure, which did not cover all labels and had no completeness guarantee. It remains separate from positivity of a tree certificate. The frozen protocol conservatively calls endpoint failure inconclusive; its wording is preserved, while this later argument is recorded as a proof candidate.

## What information became visible

Our earlier pair summaries could lose decisive information on wide windows. Conditioning on the fastest runner controls a feature those summaries did not record: **a residual runner cannot leave and re-enter its blocking state inside the window**. That interval structure makes the tree duration formula exact.

This is a concrete example of improving a representation by choosing its context. It does not make arbitrary pair summaries sufficient, reconstruct the placement of every interval from durations, or settle boundary-only feasibility. The next mathematical task is to exploit arithmetic relations between the fastest runner's different safe laps to rule out their collective complete coverage, with endpoint contacts retained.
