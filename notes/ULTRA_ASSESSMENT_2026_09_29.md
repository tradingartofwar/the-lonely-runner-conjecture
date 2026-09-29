# Ultra assessment: proof distance and the next decisive question

Date: 2026-09-29. Reviewed checkpoint:
`7b0101376e00dbb71537d3a62e39ec75cee113cc`.
Research branch: `research/near-doubling-overlap-2026-09-24`.

Six Ultra reviewers and the coordinator examined the proof spine, strategy,
geometry, arithmetic, duality, and primary literature. This is materially
AI-assisted internal review, not independent human certification.
No mathematical program, new tuple scan, phase grid, or archived protocol
was run. Existing general deductions remain **HYPOTHESIS / proof
candidates**; prior finite exact records remain **OBSERVED**.

## 1. How close are we?

We have a useful collection of exact witness mechanisms and a substantially
clearer account of their limits. We do **not** yet have evidence that a
general proof is near. The missing implication is structural: why every
permitted speed configuration must provide one of the witnesses our methods
know how to certify.

The present work is further along as a focused methods and review package
than as a solution of arbitrary-runner Lonely Runner. Completing the
remaining fixed-family cases would explain a special family already covered
by the standard eight-runner theorem. It would not establish an arbitrary
eight-runner reduction, much less an induction for every runner count.

A numerical completion percentage would be misleading. Mathematical
distance is better stated by the missing implications:

| Question | Current position |
| --- | --- |
| Does a supplied interval, pair of openings, or endpoint witness work? | Several exact criteria and internally reviewed proofs. |
| Does every admissible core \(1,4,5,a,b,c\) have positive \(1/8\)-safe duration? | A complete direct proof candidate; established lower-runner theory also gives existence. |
| Can every final runner be excluded from covering that entire core? | Exact formulation and several families covered; no universal structural exclusion within our framework. |
| Is the finite remainder finished? | No. The literature-assisted bounds \(a\le34,b\le47,c\le281,d\le1268\) remain unexhausted. |
| Can arbitrary configurations be reduced to the special \(1:4:5\) core? | No such reduction. Scaling and changing the reference do not impose those ratios. |
| Does the method prove threshold \(1/n\) for arbitrary \(n\)? | No threshold-preserving general reduction or induction has been supplied. |

The current literature is already well beyond eight runners: Rosenfeld's
paper states the seven-relative-speed \(1/8\) theorem, and Allikvere's
September 24 revision reports fourteen and fifteen total runners.
We inspected the relevant primary statements, not the full computational
certificates. This reinforces that our potential contribution is an
explanatory mechanism or a scalable structural theorem, rather than a new
existence assertion for these eight-runner examples.
Sources and exact reading limits are in
[literature.md](../reviews/2026-09-29-ultra-assessment/literature.md).

## 2. What survived the audit

The adversarial reviewer found no fatal defect in the assigned four-note
proof spine:

- [Short-kernel bound](SHORT_KERNEL_BOUND_2026_09_28.md): the mixed average,
  strict chain-span contradiction, 23-occurrence count, and auxiliary
  factorial induction.
- [Core-window reduction](CORE_WINDOW_REDUCTION_2026_09_29.md): the
  restricted blocking-measure bound, positive five-core measure, and
  sufficient speed cutoffs.
- [Six-core window](SIX_CORE_WINDOW_2026_09_29.md): the arithmetic closure,
  endpoint width quantum, and the separate direct and literature-assisted
  finite reductions.
- [Last-runner compatibility](LAST_RUNNER_COMPATIBILITY_2026_09_29.md):
  open versus closed containment, the two-window certificate, reflection,
  and the exceptional final-phase classifications.

This is scoped confidence in the written arguments. It is not a claim that
every historical artifact was reviewed, that computations were rerun, that
novelty was established, or that the claim status should be promoted.

The most portable existing mechanism is the critical-duty averaging and
chain argument. The most compact geometric illustration is the narrow
core \(\{1,3,4,5,7,24\}\): two specified openings force positive duration
for every real final speed \(d>56/5\), at every final phase. Both retain
their stated scopes.

## 3. The limits that should change our next move

### Positive windows cannot be the entire certificate language

At common-start final speed \(13\), the tight core
\(\{1,4,5,6,7,11\}\) has **every positive closed component strictly
blocked**. Four isolated safe points survive.

This falsifies more than the hope for a universally useful pair:
**no collection consisting only of positive core windows, even the entire
positive part of the core, can yield a surviving point in this example.**

A complete final-runner argument needs a real disjunction:

1. A positive closed component is not strictly contained, possibly leaving
   only an endpoint.
2. If all positive components are strictly contained, an isolated core point
   survives.

A strictly positive duration lower bound cannot settle the second branch.
This does not invalidate a zero-average/strict-cover contradiction with
separate endpoint reasoning, such as the existing chain proof.

### The scalable train bound has the wrong duty for the full system

At threshold \(1/n\), each of \(n-1\) blockers occupies duty \(2/n\).
Their total is \(2(n-1)/n>1\). The critical-duty kernel instead obtains its
contradiction when the selected residual trains have total duty one.

For \(n=2m\), it can treat \(m\) residual runners after the other \(m-1\)
constraints have supplied a suitable window. **Supplying that window with
enough width or placement is the hard bridge.** A factorial move bound does
not make the window appear.

### All-phase robustness is an extra requirement

The physical problem has a common start. Many of our cleanest certificates
work at every phase of the final runner, which is stronger. The audit does
not prove that every admissible fixed core has that stronger property.
We should not make universal phase robustness a necessary intermediate goal
without a reason.

In the applicable small-arc regime, the existing two-time theorem already
compresses all-phase robustness to a pair of phase points. Merely allowing
larger witness collections does not remove that stronger quantifier.

### Some apparent new directions were rediscoveries

The condition for opposing threshold contacts
\[
 n\mid\frac{u+v}{\gcd(u,v)}
\]
was independently rederived during this review, but already appears in
the earlier project handoff. It is retained mathematics, not a new advance.
For \(n\ge3\), an eligible pair supplies exactly \(2\gcd(u,v)\) oriented
contact times in one period before the other runners are checked.
This enumeration is endpoint-complete for isolated witnesses, but can be
large and does not guarantee that any candidate survives.

Likewise, phase-space polyhedra, lap-labelled inequalities, short-relation
extraction, and pre-jumps have direct precedents. Finding another
representation is progress only if it yields a new usable restriction,
selection rule, or proof.

## 4. Alternative approaches examined in this review

### A. Connected openings: a modest geometric extension

For integer \(n\ge3\), the pair lemma extends to ordered disjoint positive core windows
\(I_1,\ldots,I_r\). Let \(w\) be their largest width, \(D\) their total
hull span, and \(G_j\) the adjacent gaps. At threshold \(1/n\), if
\[
 G_j\le\frac{n-2}{2}w\quad\hbox{for every }j,
 \qquad d\ge\frac{2}{nD},
\]
then the final runner cannot strictly block all of them, at any phase.
Strict gap and speed inequalities guarantee positive duration.

Indeed, full blocking forces \(dw<2/n\). The gap inequalities then make
every \(dG_j<(n-2)/n\), too short for different blocking laps. All windows
must occupy the same lap, contradicting the hull threshold. The closed
blocker version gives the strict-duration assertion.

This propagates one shared lap through a connected chain of openings.
It can strengthen a supplied-window certificate, but neither forces such
a chain to exist nor addresses tight \(13\)'s isolated-point branch.
The correct general coefficient is \((n-2)/2\); a factor-of-two error in
one draft review was caught and corrected before preservation.
See [geometry.md](../reviews/2026-09-29-ultra-assessment/geometry.md).

### B. Relations involving the remaining speeds

Beck–Everett's September 23 revision gives a necessary short odd-sum
integer relation when strict loneliness fails. Applied directly here,
it is satisfied by \(1+4-5=0\), regardless of \(a,b,c,d\).
That theorem alone cannot restrict the remaining speeds.

The team derived an explicit relative version using the paper's
nonnegative cosine-autocorrelation window. Let \(k=s+r\) be the number of
moving speeds, \(h=1/2-\delta\), and let the supplied \(s\)-speed core have
positive weighted safe mean \(A\). Write \(a_0=8h/\pi^2\).
If the full system has no strictly \(\delta\)-safe time, an odd-sum
integer relation involving at least one residual speed has
\[
 \|m\|_1\le\frac{k}{2h\sqrt{A a_0^r}}.
\]
The proof isolates the positive contribution of relations wholly inside
the core, then uses a Fourier second moment to bound a relation needed to
cancel it. This is a specialization of established inverse-Fourier
reasoning; Tao already supplies relative relation-extraction precedents.

For the live core, a hand bound gives
\[
 A\ge\frac{3}{320\pi^3},\qquad
 \|m\|_1\le\frac{28}{3}\sqrt{\frac{320\pi^{11}}{243}}.
\]
**This does not reduce today's remaining region.** When \(a\le34\), an
obvious odd-sum relation involving \(a\) already has norm at most \(38\),
far below that bound. A correct but ineffective bound must not be counted
as a practical advance toward finishing the conjecture.

The useful object is therefore the set of **independent relations already
imposed**, not a tally of short relations.

### C. A useful correction: relaxed phase-space existence is already supplied

The Fourier viewpoint suggests retaining the full module of independent
integer relations and studying the phase space compatible with them. The
team first showed that one relation added to the core cannot eliminate all
strictly safe phase choices, then proposed testing two added relations.

**That proposed next existence problem was resolved during the review.**
A stronger general observation shows why it is not the missing theorem.

Let \(K\subset\mathbb R^k\) be a rational subspace of dimension
\(\ell\ge2\), containing a vector with all coordinates positive. Consider
\[
 \{w\in K:w_i\ge1\text{ for every }i\}.
\]
It is nonempty by scaling that positive vector. Minimize \(\sum_i w_i\);
a compact sublevel gives an optimal vertex. At a vertex, at least \(\ell\)
independent coordinate inequalities are active, so at least \(\ell\)
coordinates equal one. The vertex is rational.

Clear denominators and merge equal coordinates. The resulting direction
has at most \(k-\ell+1\) distinct positive speeds. Assuming the
corresponding lower-runner result, some scalar multiple of that direction
has every coordinate at distance at least
\[
 \frac1{k-\ell+2}>\frac1{k+1}.
\]
Thus the relaxed torus supplied by \(K\) already has a strict safe point.

For the seven moving coordinates in our family:

| Independent relations added to the exact \(1,4,5\) core | Remaining dimension | Supplied relaxed-space margin |
| --- | ---: | ---: |
| One | 4 | At least \(1/5\) |
| Two | 3 | At least \(1/6\) |
| Three | 2 | At least \(1/7\) |
| Four: the full actual relation module | 1 | This argument needs the eight-runner conclusion itself. |

The positive-cone vertex proof was independently derived and challenged in
this review. The literature reviewer then identified an established,
more general conditional conclusion: Allikvere v2, Lemma 3.3, explicitly
attributes rational-subspace separation to Giri–Kravitz. We reopened the
statement and proof. The review therefore treats this as an alternate
derivation of a known mechanism, not a new existence theorem.

The crucial distinction is **direction**. The constructed rational vector
\(w\in K\) need not be proportional to the actual velocity vector \(v\).
A safe point on the trajectory of \(w\) is not a lonely time for \(v\).
The remaining obstruction is reaching the safe region along the actual
one-dimensional trajectory, or bounding the error of an explicit transfer
to it. Existing finite-reduction literature already uses such transfer and
rounding estimates.

The two-relation zonotope formulation remains an exact representation,
recorded in [duality.md](../reviews/2026-09-29-ultra-assessment/duality.md),
but its bare feasibility is no longer an open research priority here.
Only an improved constructive or quantitative transfer would add something.
This correction supersedes the initial P2 proposal in the individual
reports, which preserve its development and the subsequent correction.

### D. A wider core and an equality-preserving lift

A complementary scope test replaces \(1,4,5\) by \(p,q,p+q\).
The ambitious target is an explicit extension from an \((n-1)\)-runner
result to \(n\) runners whose relative speeds contain such a triple,
uniformly in the core ratio and the other speed magnitudes, preserving
equality.

The targeted literature search did not locate that exact lifting theorem.
This is not a novelty certificate. Deleting \(p+q\) and taking an arbitrary
old witness fails: \(pt\) and \(qt\) can be opposite safe phases while
\((p+q)t\) is integral. The research task is a justified witness choice
and a valid common-time extension, not the bare existence of an additive
relation.

This target would test whether the method can leave the fixed numeric
core. It is a major open bridge, not a promised routine lemma.

### E. Other ideas that need a nontrivial inequality first

Threshold continuation can recover equality points. If the maximum
separation is exactly \(1/n\), then for sufficiently small \(\epsilon>0\),
the safe duration at threshold \(1/n-\epsilon\) is
\[
 \epsilon\sum_j(1/p_j+1/q_j),
\]
where \(p_j,q_j\) are the two controlling one-sided slopes at each isolated
maximum. This is a useful endpoint-sensitive representation. Without an
independent lower bound, it restates existence rather than proving it.

A sparse endpoint menu below the known width cutoff is another precise
compression question. It must depend on the core and retain isolated
points. A fixed input-independent rational menu with bounded early laps
is already ruled out by the archived obstruction.

A fixed affine family \(v(q)=qA+B\) could instead be studied for its exact
global maximum, using relative-spectrum theory. That requires both lower
witnesses and upper bounds over every contact branch; another local
opening is insufficient. This is a legitimate alternative bounded project,
but not the principal route to arbitrary \(n\).

## 5. Recommended next research contract

Preserve the current mechanism package and stop treating new numerical
cutoffs or larger agreement counts as the default next step.

**First priority:** one analytical derivation-and-challenge cycle on an
**actual-trajectory-preserving extension** for a declared relation class,
starting with \(p,q,p+q\). State exactly how lower-dimensional information
chooses a valid time on the original runner trajectory, uniformly in the
parameters and with equality allowed.

The acceptance criterion is a complete restricted theorem, or a concrete
counterexample to the proposed lifting step with a precise explanation of
what failed. A witness for a different velocity vector, a safe point in a
larger torus, or the discovery of another short relation does not pass.

Begin by challenging the lift at the opposite-phase obstruction: a
lower-case witness can make \(pt+qt\) integral. Then ask whether an
arithmetic choice among witnesses or permitted time shifts can avoid that
obstruction without losing the other runners' margins. This is an
ambitious restricted induction target, not an assertion that the needed
choice always exists.

**Alternative quantitative route:** supply an explicit transfer from a
relaxed safe phase point to the actual trajectory with error smaller than
its safety margin. Compare the resulting bound against the existing
lattice/rounding literature before calling it an improvement. The mere
existence of the relaxed point is already accounted for.

**Scalability gate:** the result must free the fixed \(1:4:5\) ratio or
give a genuine threshold-preserving step in \(n\). Another supplied-window
criterion or a tighter cutoff for the same old family does not pass that
gate, though a substantial simplification may still help the methods
package.

**Equality gate:** every proposed universal route must accommodate tight
\(13\). A positive-component-only argument is already falsified. The
existing strict \(16\) and finite-anchor examples remain cheap analytical
checks against repeating ruled-out certificate classes.

A broad search is unnecessary for this first cycle. If computation becomes
useful, specify a small exact protocol that can falsify the proposed
structural statement before running it. A test whose only possible payoff
is another already-known lonely configuration should not be run.

The mission remains open. What would materially change the assessment is
a uniform selection, extension, or reduction theorem with these quantifiers
and equality cases intact—not simply another successful example.

## 6. Review provenance and continuity

Full individual reports:
[proof audit](../reviews/2026-09-29-ultra-assessment/proof_audit.md),
[strategy](../reviews/2026-09-29-ultra-assessment/strategy.md),
[geometry](../reviews/2026-09-29-ultra-assessment/geometry.md),
[arithmetic](../reviews/2026-09-29-ultra-assessment/arithmetic.md),
[duality](../reviews/2026-09-29-ultra-assessment/duality.md),
[literature](../reviews/2026-09-29-ultra-assessment/literature.md).

The reports preserve disagreements, rediscoveries, the corrected
general-threshold coefficient, source-reading limits, ineffective bounds,
and proposed falsifiers. The manifest hashes the final preserved review
artifacts. Prior frozen computations and proof notes remain unchanged.

Hourly research remains paused. No paid compute, broad scan, all-reference
campaign, outside outreach, +7/+9 restart, or main merge was performed.
