# Ultra review of the LTCM exact spectrum candidate

September 29, 2026. Reviewed source commit: `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Verdict: the five-branch spectrum formula survives this internal adversarial review.** No result-level mathematical defect was found. Six separately tasked Ultra reviewers examined the geometry, upper bound, selector, direct physical calculation, equality/witness semantics, and prior art. This strengthens the proof candidate; it is not formal verification, independent human certification, or a novelty determination.

The reviewed statement concerns eight common-start runners, reference 0, and moving speeds
\[
(1,q,q+1,q+2,q+3,2q+3,2q+5),\qquad q\in\mathbb Z,\ q\ge2.
\]
The exact optimum and attaining-time formulas in [the frozen candidate](LTCM_EXACT_SPECTRUM_2026_09_29.md) remain unchanged. In particular, q=4 is the sole case with optimum 1/8; every other member has optimum at least 1/7. This is a selected-reference result for this family, not a solution of the general conjecture.

## What survived the challenges

| Target | Independent task and evidence | Outcome |
| --- | --- | --- |
| Fixed geometry | Fresh exact three-dimensional clipping, plus separately implemented exhaustive boundary intersections | Same 10 cells, 33 vertices, and 45 edges; all three singleton cells retained |
| Universal upper bound | Rebuilt edge adjacency from printed vertices and inequalities; checked all 21 peak directions and 84 symbolic comparisons | All four unbounded residue-domain comparisons hold; no zero-projection or endpoint exception missed |
| Selector completeness | Minimal-face proof, signed rounding, empty ranges, constant projections, horizontal edges, and lower-dimensional cells | Maximum and one attaining witness can be selected within 33 vertex checks plus 45 edge selections |
| Physical optimum | Newly authored opposing-contact and individual-peak enumeration, without the original implementation | Exact maxima and complete maximizer sets agree for q=2,...,25; 60 maximizing times in total |
| Large witnesses | Direct actual-phase evaluations at q=100002,...,100007 | All six residue classes pass; these are witness checks, not exhaustive large-q maxima |
| Equality and transfer | Actual physical lap reconstruction; 56 affine endpoint inequalities; direct closed-safe-band intersection at q=4 | Exactly four q=4 safe times: 1/8,3/8,5/8,7/8; no positive interval silently substituted for equality |

The finite controls do not prove an infinite statement by extrapolation. The universal claim rests on fixed-cell completeness, the slice argument, symbolic inequalities on entire residue domains, and explicit physical witnesses. The direct physical calculations provide a different way for the argument to fail.

## Precision corrections

The original upper-bound sentence “Any slice maximum ... must lie” should be read as an existence statement: **if a slice has optimum above 1/7, an optimizer can be chosen at a peak vertex or on an edge incident to a peak.** It need not describe every maximizing point of a general polytope slice.

A dimension-independent justification replaces informal facet counting. Choose an optimizing vertex p of the slice and let F be its minimal face in the original polytope. The point p lies in the relative interior of F. If F had dimension at least two, a nonzero direction in F would preserve the slicing equation, giving a segment through p inside the slice and contradicting extremality. Hence F is a vertex or an edge. This also handles lower-dimensional cells and a slicing plane containing an entire face.

The bound **33+45** counts vertex checks and edge selections needed to find the optimum and at least one witness. It is not a bound on the number of all optimal times and is not a constant bit-time assertion. A robust edge implementation computes both rounded endpoint bounds, tests whether an integer exists between them, and selects the endpoint integer favored by the objective slope. The original implementation already does this correctly.

These are exposition and scope clarifications. They require no change to the five formulas. The original proof package and its recorded hashes have been preserved; this review supplies the clarification.

## Literature finding that changes the context

Jain and Kravitz's *Relative Lonely Runner spectra* is now published in *Combinatorial Theory* 6(1), #1 (April 20, 2026), DOI [10.5070/C66165688](https://doi.org/10.5070/C66165688). Its fixed-torus framework and §6 example already supply the first six coordinate forms of our model. Both arXiv v2 and the published §6 also identify an additional progression in the sector 0<=A<=B with (A,B) congruent to (1,0) modulo 6. [Published paper](https://escholarship.org/content/qt3mx8w3js/qt3mx8w3js.pdf).

The review additionally located Francesco Cordella's *Odd denominators in the Lonely Runner spectrum for six speeds*, [arXiv:2609.03444v2](https://arxiv.org/html/2609.03444v2), September 8, 2026. Section 5 reports a complete exact analysis of the same six-coordinate torus for coprime parameters A,B. Our first six speeds correspond to A=1,B=q. Its computational certificate was not independently reproduced in this review; it is credited as a preprint result, not imported as a verified premise of our proof.

Neither inspected treatment supplies our complete appended seventh-coordinate formula. That does not establish novelty. It does establish that fixed geometry, integer-orbit compatibility, finite arithmetic selection, and residue structure have strong existing precedents. Beck–Hoşten–Schymura's [*Lonely Runner Polyhedra*](https://math.colgate.edu/~integers/t29/t29.pdf), §2 and Proposition 1, remains the fixed-lap polyhedral precedent.

## What this says about LTCM

The successful part is concrete: one representation retains safety constraints, equality cases, and actual-time compatibility while supporting a bounded witness-selection operation. The number of physical laps grows with q, while the geometric model and selection budget remain fixed.

The special structure is equally concrete: seven speeds are generated from just two coordinates with fixed small coefficients. This review does not show that arbitrary runner configurations admit comparably small models, that a newly added constraint preserves a useful selector, or that equality-safe cells can always be discovered with a universal bound. The earlier failure of widening old stronger-safe cells remains intact.

The next focused research question is to isolate exactly how the appended seventh constraint changes the known six-coordinate model's winning witnesses and exceptional cases. A transferable rule for that change would advance the language beyond another family calculation. That investigation has not been executed as part of this review.

## Reproduction and provenance

Detailed reports, exact code, outputs, and the preregistered review scope are in [reviews/2026-09-29-ltcm-ultra-review](../reviews/2026-09-29-ltcm-ultra-review/). Reproduce the new mathematical checks from the repository root:

```bash
python3 reviews/2026-09-29-ltcm-ultra-review/geometry_check.py
python3 reviews/2026-09-29-ltcm-ultra-review/upper_check.py
python3 reviews/2026-09-29-ltcm-ultra-review/physical_check.py
python3 reviews/2026-09-29-ltcm-ultra-review/semantics_check.py
```

Reviewers were given the theorem and shared coefficient data. Some read original code after constructing their checks; each report states its dependencies. Separately authored AI calculations are useful counterchecks, not external certification. The coordinator inspected the source and new checks, reconciled results, verified all nine original manifest hashes, and matched the local proof note to its live GitHub blob at the frozen commit.

No broader physical family, other reference runner, or exhaustive large-q scan was evaluated. Hourly research remains paused. No outside contact, paid compute, unattended run, or main merge occurred.
