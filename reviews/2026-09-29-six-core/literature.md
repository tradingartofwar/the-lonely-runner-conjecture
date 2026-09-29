# Literature audit: six-core margin and the last fast runner

Date: 2026-09-29. Role: six_literature. Parent: da05361310a6e0d5607fdd7565ad226f637c8305.

This is a source and applicability audit, not an independent verification of the complete cited proofs. No executable mathematics, tuple search, or external communication was performed.

## Established seven-total-runner input

**KNOWN:** J. Barajas and O. Serra, *The lonely runner with seven runners*, Electronic Journal of Combinatorics 15(1), R48 (2008), DOI [10.37236/772](https://doi.org/10.37236/772).

- [Published PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v15i1r48/pdf).
- [Journal record](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v15i1r48).
- [arXiv:0710.4495v1](https://arxiv.org/abs/0710.4495v1), submitted 2007-10-24.

The abstract and introduction establish the seven-total-runner case. Page 2 explicitly translates to six positive integer frequencies, selected reference speed zero, common start, and distance at least 1/7. The normalized formulation assumes gcd(D)=1. Our D={1,4,5,a,b,c} contains 1, so it meets that assumption automatically. Rational rescaling is unnecessary here.

The main conclusion is presented through the introduction and Sections 4–6, rather than a numbered main theorem. Lemma 2 and Corollary 3 provide prime filtering; Section 4 organizes the remaining modulo-7 cases. This does not establish an arbitrary-phase version.

Read limit: formulation, Lemma 2 and its proof, Corollary 3, and the Section 4 proof roadmap inspected; later detailed casework not independently audited. The published PDF says March 18, 2008; journal metadata says March 20. Cite 2008 without silently choosing between these dates.

## Exact fast-runner precedent

**KNOWN:** Noah Kravitz, *Barely lonely runners and very lonely runners: a refined approach to the Lonely Runner Problem*, Combinatorial Theory 1 (2021), #17, published 2021-12-15, DOI [10.5070/C61055383](https://doi.org/10.5070/C61055383).

[Published PDF](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf), Proposition 6.1, printed pages 12–13, states that a lower bound ML(v_1,...,v_{n-1})>=L yields ML(v_1,...,v_n)>=L-epsilon when

\[
v_n\ge \frac{L-\epsilon}{\epsilon}v_{n-1},\qquad 0<\epsilon<L.
\]

Its proof expands a witness time to a closed interval of radius epsilon/v_{n-1}. I read this proposition and its complete proof and checked PDF screenshots: text extraction incorrectly displays several non-strict inequalities as strict.

Applying it with L=1/7, epsilon=1/56, v_{n-1}=c, and v_n=d gives exactly **d>=7c**, including equality. The corresponding six-core closed 1/8-safe interval has width 1/(28c), with strict safety in its interior. This is a standard literature consequence, not a new perturbation lemma. In this paper n counts moving frequencies, unlike our total-runner n.

## Established six-total-runner input

**KNOWN:** Tom Bohman, Ron Holzman and Dan Kleitman, *Six Lonely Runners*, Electronic Journal of Combinatorics 8(2), R3 (2001), DOI [10.37236/1602](https://doi.org/10.37236/1602).

- [Author-hosted published PDF](https://holzman.technion.ac.il/files/2012/09/runners.pdf).
- [Journal record](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v8i2r3), dated 2001-02-06.

Theorem 2, printed page 3, gives distance at least 1/6 for five positive real frequencies, covering {1,4,5,a,b} without a gcd hypothesis. The introduction, theorem statements, and Section 2 through Lemma 4/Corollary 5 were inspected; the complete proof was not independently verified. Lemma 4's two-block argument is relevant precedent.

## Application arithmetic and additional review lead

The following deductions are internal proof candidates using the credited inputs.

Let M=max(5,b). The margin 1/6-1/8 gives width 1/(12M). The inherited pair span T2<3/(4c) certifies c>=9M, leaving c<=422 and d<=2953 when b<=47.

**Further lead sent for internal review:** a quarter-duty adaptation of the cited two-block argument gives span<1/(2c), improving the sufficient condition to c>=6M and the remaining limits to c<=281, d<=1966. The detailed adaptation belongs in the coordinator's mathematical note after review. No novelty or external certification is claimed.

## Scope and current-literature guardrail

The repository already records later eight-and-more-runner literature. I also inspected Rosenfeld's [arXiv:2509.14111v2](https://arxiv.org/abs/2509.14111v2), revised 2025-10-16, [PDF](https://arxiv.org/pdf/2509.14111v2): Theorem 1 states the eight-total-runner conclusion, and Section 4 uses a product bound plus computer-verified divisibility conditions. I did not reproduce its computational component. This continuation concerns an explicit structural certificate in the repository's framework; it must not present the fixed eight-runner family's existence question as newly open or newly solved. No broad frontier audit or novelty claim was attempted.

## Retrieval pointers for the coordinator

These identifiers are session retrieval pointers, not enduring bibliographic identifiers. The URLs above are the durable citations.

- Published seven-runner PDF: turn31view1. Journal metadata: turn26view0. arXiv statement and normalization: turn21view1; roadmap: turn23view0.
- Kravitz published PDF: turn27view0; proposition extraction: turn28view3; inequality screenshots: turn29view0 and turn29view1.
- Six-runner author PDF, Theorem 2 and Lemma 4: turn33view1. Journal metadata: turn33view0.
- Rosenfeld version: turn22view2; Theorem 1 and proof framework: turn22view4.

The coordinator should open the underlying sources independently before citing these retrieval references in a user-facing answer.
