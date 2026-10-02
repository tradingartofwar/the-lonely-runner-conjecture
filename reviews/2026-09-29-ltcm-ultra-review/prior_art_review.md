# Primary-source and novelty-scope review

Date: 2026-09-29. Assigned frozen candidate: `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Verdict: the mathematical framework is established; the exact seven-coordinate formula was not located in the inspected sources. Novelty remains OPEN.** The candidate is an explicit fixed-family calculation within existing relative-spectrum and polyhedral methods. Its five cases, witness times, finite exception and certificate counts may be useful concrete output, but do not constitute a new general selection principle. This review does not certify the mathematical candidate or re-audit the literature's computational proofs.

## Sources, dates and reading scope

1. Vanshika Jain and Noah Kravitz, *Relative Lonely Runner spectra*, [arXiv:2411.12684v2](https://arxiv.org/html/2411.12684v2), revised December 9, 2024 (v1: November 19, 2024). Read the definitions, Theorem 1.1, the strategy in Section 2.1, Lemma 2.5, Proposition 2.6 and the relevant Section 6 formulas and tables. Also inspected the [published PDF](https://escholarship.org/content/qt3mx8w3js/qt3mx8w3js.pdf), *Combinatorial Theory* 6(1), #1, DOI [10.5070/C66165688](https://doi.org/10.5070/C66165688), published April 20, 2026; submitted January 10, 2025, accepted July 8, 2025. Checked publication metadata and the corresponding Section 6, Tables 6.1-6.2, pp. 40-44. The publisher's [landing page](https://escholarship.org/uc/item/3mx8w3js) was initially nearly empty in extraction; the PDF was accessible. No complete version diff or full-paper proof audit.

2. Francesco Cordella, *Odd denominators in the Lonely Runner spectrum for six speeds*, [arXiv:2609.03444v2](https://arxiv.org/html/2609.03444v2), September 8, 2026. The targeted search first surfaced v1, September 3; the [abstract/version record](https://arxiv.org/abs/2609.03444) identified v2, which was then inspected. Read Theorem B, Section 5's parameterization, Lemmas 5.1-5.2, far-region and strip mechanisms, Theorem 5.3, and the relevant reproducibility description; checked the corresponding portions in v2 after initially reading v1. This is a preprint whose reported exact computations were **not** downloaded or rerun. No claim of independent verification of its classification or exhaustive calculations.

3. Matthias Beck, Serkan Hosten and Matthias Schymura, [*Lonely Runner Polyhedra*](https://math.colgate.edu/~integers/t29/t29.pdf), *Integers* 19 (2019), #A29. Received September 14, 2018; accepted April 19, 2019; published June 3, 2019. Read Section 2, especially the translated cube, cones, formulas (1)-(5), and Proposition 1 on pp. 3-4. No audit of the paper's later family results.

## What the precedents actually establish

Jain-Kravitz Theorem 1.1 gives finite reciprocal-progression structure. Proposition 2.6 gives eventual residue/sector formulas of the form `D(U)+kappa/(E A+F B)`, with finite exceptional behavior requiring care. Section 6's generators are exactly the candidate's first six rows. Its detailed progression calculation primarily uses `A=6, B=5 mod 6`; its final paragraph also identifies a progression in the sector `0<=A<=B`, class `(A,B)=(1,0) mod 6`. The published version retains this scope. Neither inspected version displays the candidate's seven-coordinate five-branch formula. The paper's `U^7` is an example label for a torus in six coordinates, not a seven-coordinate object.

Cordella's Section 5 studies that same six-coordinate torus for all admissible coprime parameters. The source reports an exact completion using fixed component geometry, modulus 6, explicit thresholds, finitely many cones, strips, and finite residual checks. This is a material additional precedent missing from the original note's references. Theorem B/5.3 states its resulting restrictions on the six-speed values; the text does not state the appended seven-speed formula under review. These are source claims, not results reproduced in this review.

Beck-Hosten-Schymura Proposition 1 equates loneliness with membership in a fixed-lap cone, an integer point in the associated polyhedron, or a projected-lattice point in a zonotope. Section 2 already retains the actual line through the velocity vector and closed cube inequalities. Consequently, fixed lap labels, common-time compatibility and endpoint retention are established ingredients. Optimizing a variable threshold adds an elementary linear coordinate; it does not turn this representation into a new theory.

## Exact mapping and independent comparison

The candidate has total runner count `n=8` and `k=7` relative speeds. The sources normally count moving speeds instead. Set

```
u  = (1,0,1,2,3,3),   v  = (0,1,1,1,1,2),
u' = (1,0,1,2,3,3,5), v' = (0,1,1,1,1,2,2).
```

Then the first six speeds are `u+q v`, i.e. the specialization `(A,B)=(1,q)`; the full candidate is `u'+q v'`. Coprimality is automatic. Since the first two coordinates are the parameter coordinates, both embeddings retain the parameter lattice directly. The actual time orbit is `(x,y)=(t,qt) mod 1`, hence `qx-y` is integral. The objective conversion is `D=1/2-M`.

The following is algebra on the **candidate's** displayed formulas, not an assertion copied from a source:

| Candidate domain | Equivalent distance-to-center value |
| --- | --- |
| `q=4` | `3/8` |
| `3` divides `q` | `1/3 + 1/[6(2q+1)]` |
| `q=1,2 mod 6` | `1/3` |
| `q=4 mod 6`, `q>=10` | `1/3 + 1/[2(2q+1)]` |
| `q=5 mod 6` | `1/3 + 1/[3(3q+5)]` |

This is the expected reciprocal-affine/residue pattern for a fixed two-dimensional rational torus. Applying the general structural theorem to the seven-coordinate embedding predicts this *kind* of eventual behavior; it does not supply the displayed constants, the modulus, validity at every `q>=2`, or the exceptional value merely by substitution.

The appended coordinate is not redundant. At the single ambient point `(x,y)=(1/3,1/6)`, the first six reduced phases are

```
(1/3, 1/6, 1/2, 5/6, 1/6, 1/3),
```

all at least `1/6` from an integer, whereas `5x+2y=2` collides. This hand calculation is a logical scope check, not a new physical-family scan. It shows why a six-coordinate optimum cannot simply be declared unchanged when the seventh coordinate is appended. It does not show whether the extra coordinate changes the optimum on any particular physical `q`.

The candidate's `33` vertex checks and `45` edge selections are explicit constants for its supplied finite geometry. The reduction of a linear slice optimum to vertices/edges and nearest feasible integer levels is an elementary finite-polytope specialization. The source comparison supports crediting this as an auditable implementation of established geometry and arithmetic. It does not support claiming a novel complexity result from a fixed template, or an algorithm for arbitrary coefficient systems with those same constants.

## Search limits and disposition

This was a finite, targeted source check. Queries covered the named paper and its 2026 publication, plus the textual fragments `"lonely runner" "2q+5"`, `"lonely runner" "q+3" "2q+3"`, and `"lonely runner" "5,2" "spectrum"`. Exact-fragment results were poor or irrelevant; title searching identified Cordella's directly relevant preprint. Only primary papers were relied on. No broad literature census, citation-network exhaustion, supplemental-code execution, new-family calculation, external correspondence or paid computation was performed.

The defensible status is **an explicitly evaluated seven-coordinate ray inside an established framework, with exact-formula novelty unresolved**. Absence from these sections or from notation-sensitive searches is not evidence of worldwide absence. Conversely, a general algorithm capable of producing the answer does not prove that this exact formula has already been written down.

The next useful comparison, if separately authorized, is a source-level specialization of the six-coordinate formulas to `(1,q)`, followed by an explicit account of which optimizers the seventh form removes. It should compare claimed outputs, thresholds and finite exceptions; it should not rebrand the established residue-sector mechanism. No such supplemental computation was performed here.

This report was written by a separately tasked AI reviewer. The original proof package and continuity files were not modified. The supplied snapshot has no readable Git repository metadata at this path, so the commit identifier above is the review protocol's frozen identifier rather than an independently resolved HEAD.
