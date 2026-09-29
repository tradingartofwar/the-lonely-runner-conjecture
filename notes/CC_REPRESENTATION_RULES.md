# Compatibility Calculus: representation and transfer rules

Adopted September 29, 2026, following the six-to-seven transfer at commit
`a3be4b53111fc173c55c453de6e2bb28ebd7c389`.

This is the current working specification for how CC carries, compresses and
transfers models. It implements the maintainer's direction to check information
loss and model adequacy periodically and to consider adapting other authors'
languages or frameworks whenever that could help. Historical LTCM names and
proof packages remain part of the record. These are research requirements;
they do not establish a new theorem or a complete formal language.

## 1. Adequacy belongs to a question and an operation

A representation must say which question it supports, under which assumptions,
and which next operation it is being asked to support. Successful use for one
question does not automatically establish adequacy for another.

Keep these outputs distinct:

| Intended output | Required conclusion |
| --- | --- |
| Existence | At least one compatible physical point exists in the stated domain. |
| Optimal value | A matching lower and upper bound identifies the maximum. |
| One witness | A recoverable physical point attains the stated threshold or value. |
| Every maximizer | The complete optimizer set is recovered, including ties and boundaries. |
| Complete safe set | Every feasible time or point at the chosen threshold is represented, including isolated points. |
| Transfer to another model | The stated operation preserves or reconstructs the required relation and output; its new assumptions are checked. |

These are separate obligations. For example, an optimum selector does not
automatically enumerate all maximizers, and a representation of feasibility
does not itself give an efficient selection rule or force existence.

## 2. The minimum representation record

For a substantive new model, compressed object, or transfer, include this short
record in its research note. Reuse an existing record by reference when its
question, scope and operation have not changed. The point is to preserve
consequential distinctions, not to repeat paperwork at every turn.

```text
Representation and version:
Question and requested output:
Domain, assumptions and next operation:
Information retained, including joint relations and equality cases:
Information omitted; what can and cannot be reconstructed from this record:
Richer source and explicit recovery/translation map:
Evidence, dependencies and limits of the adequacy claim:
Failure test or trigger for enrichment, replacement or rechecking:
```

Use the repository's existing claim-status vocabulary. Identify whether support
comes from an exact identity, a proof candidate, a bounded check, or an open
assumption. A list of successful cases supports its stated domain, not an
unstated universal adequacy claim. A failed record remains preserved with the
particular question or operation that defeated it.

For runner work, the domain normally includes total and moving runner counts,
selected reference, common-start assumption, parameter ray, coordinate order,
threshold, and closed/strict boundary convention. The recovery map includes
the actual-orbit condition, physical clock, lap labels and reflection where
needed. Include only fields that matter to the claim, but do not silently
identify different rays, clocks, references or quantifiers.

## 3. Rules for compression and transfer

**Declare the intended loss.** State which information is deliberately omitted
and why it cannot change the present answer, or mark that justification open.
Keeping a source file elsewhere does not make a compressed object intrinsically
lossless; it provides a recovery route that must be used when needed.

**Preserve joint compatibility.** Conditions that must hold at the same point,
time, label or configuration remain linked. Separate marginal feasibility
does not establish simultaneous feasibility. A projection may be adequate for
a value question while requiring extremizer identities and an inverse map to
recover witnesses.

**Preserve relevant equality and lower alternatives.** Closed endpoints, ties,
singleton cells and lower-valued configurations remain available when a later
constraint may remove today's best points. A smaller record may omit them only
within a justified question-specific scope, with its limits explicit.

**Recheck before a material change of use.** Adding a constraint, changing the
parameter ray or reference, lowering a threshold, changing coordinates, or
asking for all witnesses instead of one changes the obligation. Establish that
the current record supports that operation before relying on its answer.

**Recover, enrich or switch when necessary.** Return to the pinned richer
source, retain the missing relationship, or use another representation. Then
test the revised record against the example that exposed the loss. Preserve
the old failure and the mapping between versions. The old representation may
remain valid and useful for its original question.

**Reassess at meaningful checkpoints.** Use these rules after substantial
derivations, compression or translation, before conclusions and handoffs, and
when exceptions or stalled progress suggest a mismatch. Ask whether a smaller
adequate model is now possible as well as whether more information is needed.

## 4. Adapting existing frameworks is an ordinary research option

Consider existing mathematical languages, models and frameworks, including
another author's LTCM, during formulation, method selection, simplification,
transfer and review. There is no need to wait until our current approach fails
or to exhaust an approach merely because we built it. Consider unchanged reuse,
targeted modification, combination and replacement on their merits. CC itself
is subject to the same scrutiny.

For a substantive adaptation, record:

| Item | What to preserve |
| --- | --- |
| Source | Author, original name, version/date, and the definitions or results actually inspected. |
| Reason | The concrete question, missing distinction, cost or counterexample motivating the change. |
| Modification | The exact changed variables, assumptions, constraints, operations or inference rules. |
| Translation | How objects and claims map between the original framework and the adapted one; what is lost or added. |
| Inherited claims | Which source results still apply with their hypotheses checked, and which require a new argument. |
| Evidence and limits | A reproducible example or counterexample, relevant endpoint checks, claim status and unresolved obligations. |

Credit the source and distinguish our changes from its established content.
A successful adaptation does not establish novelty; a cited theorem does not
automatically cover altered assumptions. Describe an untested change as a
proposal. Compare the modified framework against both the original and the
present alternative on the concrete task. Prefer the smallest adequate
representation, regardless of its origin.

Use this compact extension to the representation record when adapting a source:

```text
Original framework, author and pinned source:
Specific modification and reason:
Translation and information changes:
Source guarantees retained, re-proved, or no longer applicable:
Comparison case, result and unresolved obligation:
```

## 5. Applied records for the current CC work

### Full fixed-cell representation

- **Question/output:** represent closed feasibility and recover physical points
  at z>=1/8 for the stated six/seven coefficient forms and integer parameter
  ray; support exact addition of the seventh band.
- **Retained:** full inequalities, labels, vertices, incidence and dimensions,
  including singletons; the chosen A- or B-ray orbit/clock/lap map stays explicit.
- **Omitted/limits:** the continuum need not be listed point by point because
  the inequalities or convex hull recover it. Geometry alone does not assert
  actual-orbit feasibility, cheap selection, or applicability to other forms.
- **Source/recovery:** [the original cell certificate](LTCM_EXACT_SPECTRUM_2026_09_29.md)
  and [six-to-seven parent-child atlas](CC_SIX_SEVEN_TRANSFER_2026_09_29.md).
  Reconstruct each labelled polytope, impose its exact integer orbit and use
  the appropriate physical recovery map.
- **Evidence/trigger:** fixed exact constructions and stated proof candidates.
  Changing coefficients, the floor, or the ray requires rechecking the affected
  geometry or orbit map. More runner coordinates need not stay in this model's
  fixed scope.

### Seven-cap representation for the B-ray upper bound

- **Question/output:** determine the B-ray optimum and, with strict supporting
  directions and reflection bookkeeping, its complete maximizing-time set.
- **Domain/operation:** B_q=V(q,1) after the first-two-coordinate permutation,
  integer q>=2, selected stationary reference among eight common-start runners;
  use the lower-bound argument F_B(q)>1/7 supplied by the current proof candidate.
- **Retained:** seven peak caps, the projected H=x-qy interval at each height,
  extremizing direction identities, congruences, strict comparisons and recovery.
- **Omitted/limits:** geometry below 1/7, the singleton cells and the complete
  1/8-safe set. Numerical interval endpoints alone do not retain witness identity.
- **Source/recovery:** [the B-ray review](CC_OTHER_RAY_REVIEW_2026_09_29.md) and
  its full-cell dependencies. Recover the full cells before using a lower
  threshold or a constraint-addition operation that this cap record does not cover.
- **Evidence/trigger:** internally reviewed proof candidate, supported by exact
  finite geometry and unbounded symbolic comparisons. A change that removes
  the F_B>1/7 premise invalidates this reduction; the A-ray q=4 case is a known
  control against incorrectly reusing it at 1/8.

### Conditional intervals for A-ray six-to-seven transfer

- **Question/output:** decide same-slice survival and recover every compatible
  point from the complete family of closed conditional intervals, or select
  one point from a specified nonempty intersection.
- **Domain/operation:** A_q=V(1,q), q>=2, x={t}, y={qt}, h=qx-y integral;
  the same floor z>=1/8 before and after adding S=5x+2y.
- **Retained:** parent label m, integer h, height z, the joint conditional
  interval J_{m,h}(z), seventh lap k, and inverse time/lap map. Each interval
  comes from the same parent and the same h; distinct parents remain distinct.
- **Omitted/limits:** a single evaluated interval omits other h and z values
  and their support changes. The exact representation supplies neither a bound
  on the number of slices to inspect nor a rule forcing a nonempty intersection.
- **Source/recovery:** [the transfer note and certificate](CC_SIX_SEVEN_TRANSFER_2026_09_29.md).
  Intersect J with [k+z,k+1-z], then recover
  x=(S+2h)/(2q+5), y=(qS-5h)/(2q+5), t=x and physical laps.
- **Evidence/trigger:** exact reconstruction, controls q=3,4,10 and a transfer
  proof candidate. Use the archived q=4 marginal-range false positive and
  equality witnesses, and q=10 new-face contacts, when assessing a proposed
  compression. Adapt the check to the question: missing one maximizer refutes
  complete enumeration, not necessarily selection of a different witness.

## 6. Selection target and completed two-segment candidate

**Requested output:** a certificate selecting one physical 1/8-safe witness for
each integer q>=2 in the A ray from six-form parent information plus the added
seventh band. Exact optimization and enumeration of every maximizing time are
separate obligations and are not silently included in this next target.

**Retained inputs:** the same-threshold parent facets, conditional intervals,
support changes, integer compatibility, closed boundaries and recovery maps.
The q=4 isolated points remain necessary for the existence control. The q=10 new-face
example distinguishes the selected-witness task from a stronger all-maximizers
claim. Separate marginal ranges remain invalid as a joint-feasibility test.

**Cost target and source boundary:** seek a q-independent bound on the number
of rational selection operations, with bit lengths allowed to grow with q.
No such bound follows merely from storing conditional intervals. Derive the
selection argument from the parent data; use the already known seven-form
spectrum as a comparison target, not as the premise establishing success.

**Evidence status:** the [two-segment selector](CC_BOUNDED_SELECTOR_2026_09_29.md)
now supplies a complete proof candidate for this target. Two parent edges and
integer interval coverage suffice for all q>=2, with at most two roundings and
tests. The self-contained derivation, exact unbounded arithmetic checks and
archived physical controls are recorded there; independent review remains open.

**Failure conditions:** A missed admissible input,
an unsupported equality exclusion, an unproved nonempty slice, or a number of
steps that grows with q defeats the corresponding requested claim. Reuse the
existing controls before considering additional bounded checks. A finite pass
alone will not establish the all-q result. Existing frameworks are candidates
for reuse or adaptation during this step, with the source/change record above.

### Applied record: two compatible segments for one A-ray witness

- **Question/output:** one physical 1/8-safe witness for every integer q>=2,
  with the stationary reference fixed among eight common-start runners.
- **Retained/operation:** parent P1 and P3 edge equations, closed endpoints,
  all seven joint bands and laps, h=qx-y, integer rounding, coverage and the
  inverse time/lap map. The primary edge misses only q=5; the second covers it.
- **Omitted/limits:** other safe points, the complete safe set, optimum values
  and maximizing-time sets cannot be recovered from these two segments alone.
  Every selected separation is exactly 1/8. This is not a lossless atlas.
- **Source/recovery:** the [full record](CC_BOUNDED_SELECTOR_2026_09_29.md)
  pins the richer parent/child atlas and gives the recovery map. Recover that
  richer model before changing to optimization or all-witness questions.
- **Evidence/trigger:** complete proof candidate using endpoint affinity and
  integer-interval coverage; exact certificates and archived q=2,...,25 checks.
  Any failed band, uncovered integer, physical-map defect or equality loss
  defeats its respective claim. A change of ray, reference, coefficients,
  threshold or output requires rechecking.
- **Framework assessment:** elementary affine convexity and integer rounding
  provide the needed operation within CC. No external theorem is newly
  imported or modified, and no novelty is claimed. Alternative frameworks
  remain available under section 4.

The requirements themselves did not establish this result: the subsequent
linked derivation and checks supply the new evidence. Historical certificates
and their recorded claim statuses remain preserved. The next bounded question
is review and discovery of sufficient compatible segment collections, not an
unproved extension of this selector to new families.
