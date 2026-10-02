# Focused primary-source review: which geometry retains the lost contacts?

Reviewed September 27, 2026 against the supplied snapshot pinned to `e94a87f650264826569cae63412c43a5175f5ae4`. This is a literature/mechanism review, not a general bibliography or independent audit of the cited papers. Material AI involvement: source retrieval, mathematical synthesis, exact small calculations, and writing. Read AGENTS, README, CLAIM_STATUS, CONTRIBUTING, current HANDOFF, SOURCES, DOMAIN_CONNECTIONS, CONTACT_MOMENTS, and RESIDUE_COLLISIONS. No shared research notes were edited.

## Principal conclusion

**The closed lap-polyhedron, restricted to the actual time window, is the most direct established framework for this particular missing distinction.** The most useful less-direct lead is the spectrum literature's combination of rational extremal contacts, one-sided slopes, and residue-dependent approximation errors. Orbit dimension alone, a duration distribution at one threshold, or an unlocalized covering radius omits essential data.

The examples are counterexamples to specified summaries. They do not contradict lattice, spectrum, Fourier, or modular approaches that retain more information. In particular, matching all duration moments at one threshold is not matching the distribution of the continuous function `min_i ||v_i t||` at every threshold.

## 1. The precise polyhedral translation

Beck–Hoşten–Schymura [L1], Section 2, equation (5) and Proposition 1, identify global loneliness with an integer point in `R v - [δ,1-δ]^k`. Their closed cubes already retain equality, including zero-width feasible cells. Read printed pp. 2–4, including the elementary derivation; checked the displayed equivalence, not the paper's other results.

The following is our direct restriction of that formulation, not a theorem attributed verbatim to the paper. Put

`P_J(v,δ) = { t v - s : t in J, s in [δ,1-δ]^k }`.

This is a bounded rational zonotope when `J` and `δ` are rational. Exactly:

`F_J(v,δ) is nonempty  iff  P_J(v,δ) intersects Z^k`.

For an integer point `m`, its complete time fiber is

`J intersect [max_i (m_i+δ)/v_i, min_i (m_i+1-δ)/v_i]`.

Thus the existing safe-lap certificate is already an explicit integer-point certificate. The 1680 example has a feasible singleton fiber; 3360 has none. The bounded formulation retains the location of J. Projecting away the velocity direction in the usual global zonotope construction retains global existence but does not, by itself, retain which time window contains a witness.

This translation supplies no small candidate-selection theorem: listing all integer points or all event cells can simply recreate the current checker. The meaningful target remains a selection or exclusion argument with an explicit complexity bound.

## 2. Common-start central distance is not arbitrary-phase covering radius

Blanco–Criado–Santos [L2], Proposition 1.7 and Section 2.1, distinguish the first central minimum `κ(Z)` from covering radius `μ(Z)`: the unshifted maximum gap is `(1-κ(Z))/2`, whereas the worst shifted maximum gap is `(1-μ(Z))/2`. Read definitions and the stated equivalences; checked the elementary distance identity in Lemma 1.4. The broader proof and shifted counterexamples were not audited.

**Consequence for this project:** a generic covering-radius target silently strengthens the problem to all starting phases. Retain the designated center/coset, and retain J for a local question. Their shifted counterexamples are not common-start counterexamples.

Malikiosis–Santos–Schymura [L3], Section 1.2 and Corollary 2.3, give the global LR-zonotope construction and `|Z intersect Z^(k-1)| = sum_S gcd(v_i:i in S)`, with the empty contribution zero. Singleton terms are the speeds themselves. The 1680/3360 pair therefore does not match this lattice-point invariant. In fact, all gcds of subsets containing at least two speeds agree here, because every fixed speed divides 1680; only the variable singleton term changes. Consequently the cited lattice-point counts differ by exactly 1680. This is an elementary deduction from the formula, not a computed zonotope census. The full geometry-of-numbers proof was not audited.

## 3. A closer precedent than a generic orbit-closure analogy

Jain–Kravitz [L4], Section 2.3, Lemmas 2.4–2.5, treat a rational piecewise-linear function sampled on a shifted rational grid. They separate an interval of minimizers from finitely many isolated minimizers; the latter are described using their rational positions and left/right slopes. Eventually, the grid minimum differs from the true minimum by a residue-dependent constant divided by the grid denominator. Read these lemmas and their proofs, and Proposition 2.6's statement. Also inspected Section 7's contact locus and Proposition 7.1 statement. No full-paper audit.

**Why this is pertinent:** the repository's primitive `ψ` identifies accumulated amounts; equal values of `ψ` need not preserve the indicator at a contact. The spectrum construction retains precisely contact location, slopes, and residue errors. Its setting is global subtori, so a local-J application needs a derivation rather than a citation alone.

The source's Section 1.2 explains how one-dimensional subtori can converge to a larger subtorus. For integer speed vectors all individual orbit closures remain one-dimensional: counting that dimension cannot distinguish the matched cases. The actual embedded orbit and its target contact locus can.

## 4. Contact selection and finite groups: useful precedents, explicit limits

Kravitz [L5], Proposition 2.1, printed pp. 4–5, puts local maxima among the rational times `m/(v_i+v_j)` from opposite-side active runners. Its surrounding discussion already proposes grouping candidate times by pairs. Section 3 also explicitly constructs fast runners that hit the origin at slower runners' equality times. Read that discussion and Theorem 3.1's proof; no audit of the paper as a whole.

Therefore pair-contact candidate generation and destroying earlier equality contacts have clear precedents. The team's condition `n divides (u+v)/gcd(u,v)` is an elementary exact-threshold refinement consistent with this picture; this review establishes no novelty for it. A surviving candidate still needs every remaining runner checked.

Allikvere [L6], Section 2, Definition 2.1, uses an exact rational-grid witness, supplemented by a common-divisor alternative and complete lifting. Section 4.1 describes covering individual finite-grid times. I read these definitions, the short prime-divisibility argument, and the covering-search statement; did not audit the computational proof, certificates, or implementations.

For the present anchor, the single contact `9/32` is already a finite-group test: `1680 mod 32=16`, `3360 mod 32=0`, and multiplication by 9 gives half-phase versus zero-phase. That arithmetic retains what duration averaging loses. But a fixed modulus or fixed list of rational times is not a general selection theorem. The prime/lifting literature uses additional completeness arguments, not the assumption that a chosen grid contains every needed contact.

## 5. One concrete falsifiable experiment, with initial exact checks

**Experiment:** derive the local maximum and the first nonzero part of the threshold-response function for the existing family, instead of increasing moment order at the same threshold. Let

`G_J(y)=max_{t in J} min_{v in {1,3,4,5,10,28,y}} ||vt||`,

`W_y(epsilon)=measure{t in J: every ||vt|| >= 1/8-epsilon}`.

The testable candidate for `y=1680h` is

* odd h: `G_J(y)=1/8`, and `W_y(epsilon)=epsilon/28` for all sufficiently small positive epsilon;
* even h: `G_J(y)=y/[8(y+3)]`, with maximizing time `3/8-1/[8(y+3)]`, and `W_y(epsilon)=0` for `0<epsilon<3/[8(y+3)]`.

The odd-branch slope comes from runner 28 immediately to the right of `9/32`. The even-branch candidate is the crossing of runners 3 and y immediately to the left of `3/8`; all other constraints must be certified there and competing peaks excluded. Those global exclusions within J, including the quantitative cutoff for the linear germ, are the actual remaining work. This is a bounded experiment proposal, not an unbounded result or novelty claim.

An exact check during this review enumerated all pair-sum candidate times in J plus both endpoints. The complete minimum over all seven runners was evaluated at each candidate:

| h | G_J found | One maximizing time |
| --- | --- | --- |
| 1 | 1/8 | 9/32 |
| 2 | 140/1121 | 1261/3363 |
| 3 | 1/8 | 9/32 |
| 4 | 280/2241 | 2521/6723 |

Separately, the existing closed-interval checker at `epsilon=1/1000000`, clipped to J, returned `[9/32,7875001/28000000]` for h=1,3 (length `1/28000000`) and the empty set for h=2,4. These are OBSERVED checks on four cases, not a family proof. Reproduction is included below; no checker code was changed.

The general logical limit is elementary. For a continuous distance function on a compact positive-length J, existence at δ is equivalent to positive allowed duration at every smaller threshold sufficiently close to δ. A point at level δ has a positive neighborhood at any lower threshold; if no point reaches δ, compactness gives a strictly smaller maximum. Thus the current examples defeat the *fixed-threshold* summary, not every measure-based approach. A finite threshold menu still needs a proved margin: the conjectured even-family deficit tends to zero as y grows.

## 6. Current-source check and novelty limits

The primary arXiv record for Allikvere [L6] was reopened on September 27. It currently reports version 2, revised September 24, 2026 at 11:58:42 UTC, with the title *Fourteen and fifteen lonely runners* and a theorem claiming both cases. The version history shown lists v1 and v2. A system1 recency search was also performed; some exact-ID queries had poor retrieval. This is a refreshed statement/version check, not independent reproduction, peer-review verification, or an exhaustive claim about all subsequent work.

The earlier Cordella lead [L7] remains a retrieval limitation: current search returned its primary arXiv abstract, but direct versioned abstract/HTML opens failed. I do not promote its six-speed classifications to proof-checked facts. They concern the global spectrum, not the present local eight-runner contact example.

Targeted searches for LRC moments, isolated equality, polyhedra, finite-group covering, and spectrum mechanisms did not locate an exact published counterpart of the physical matched-moment construction. That is not a novelty certificate. The underlying measure-zero distinction, closed-cube geometry, pair-sum maxima, rational-grid residues, and equality-destroying fast runners are established precedents. The physically realized collision may be a useful explanatory example without being a new general obstruction to solving LRC.

## Sources and exact reading scope

Web retrieval identifiers and version metadata are also in `literature_sources.json` for the coordinating reviewer to reopen before citing.

* **[L1]** Matthias Beck, Serkan Hoşten, Matthias Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29, published June 3, 2019. [Journal PDF](https://math.colgate.edu/~integers/t29/t29.pdf). Section 2, printed pp. 2–4, equation (5), Proposition 1. Elementary equivalence checked; remaining paper not audited.
* **[L2]** Mónica Blanco, Francisco Criado, Francisco Santos, *Coloopless zonotopes and counterexamples to the Shifted Lonely Runner Conjecture*, arXiv:2603.24784v2, April 27, 2026. [Versioned HTML](https://arxiv.org/html/2603.24784v2). Abstract, definitions in Section 1, Lemma 1.4, Proposition 1.7, Proposition 1.11, Corollary 1.14, Sections 2.1–2.2 definitions. Statements and elementary distance identity inspected; no full proof audit.
* **[L3]** Romanos Diogenes Malikiosis, Francisco Santos, Matthias Schymura, *Linearly exponential checking is enough for the lonely runner conjecture and some of its variants*, Forum of Mathematics, Sigma 13 (2025), e164, published online October 1, 2025. [Publisher](https://doi.org/10.1017/fms.2025.10107). Section 1.2, Section 2.1 and Corollary 2.3. Formula and construction inspected; finite-reduction proof not audited.
* **[L4]** Vanshika Jain, Noah Kravitz, *Relative Lonely Runner spectra*, arXiv:2411.12684v2, December 9, 2024; published Combinatorial Theory 6(1) (2026), paper 1. [Versioned HTML](https://arxiv.org/html/2411.12684v2). Read Sections 1.1–1.2, Section 2.3 Lemmas 2.4–2.5 including proofs, Proposition 2.6 statement, Section 7 opening and Proposition 7.1 statement. Local adaptation is our inference; no full-paper audit.
* **[L5]** Noah Kravitz, *Barely lonely runners and very lonely runners: a refined approach to the Lonely Runner Problem*, Combinatorial Theory 1 (2021), paper 17, December 15, 2021. [Published PDF](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf). Section 2, Proposition 2.1, printed pp. 4–5; Section 3 opening and Theorem 3.1 proof, pp. 5–6. No full-paper audit.
* **[L6]** Jaan Allikvere, *Fourteen and fifteen lonely runners*, arXiv:2609.02604v2, September 24, 2026. [Abstract/history](https://arxiv.org/abs/2609.02604v2), [HTML](https://arxiv.org/html/2609.02604v2). Abstract/history, Section 1 and Theorem 1.1, Section 2 definitions and Lemma 2.2 argument, Section 4.1 statement. No computation, implementation, or full proof audited.
* **[L7]** Francesco Cordella, *Odd denominators in the Lonely Runner spectrum for six speeds*, arXiv:2609.03444, September 3, 2026. [Primary record](https://arxiv.org/abs/2609.03444). Primary abstract returned in search; direct v1 pages failed. Lead only.

## Reproduce the bounded spectrum/profile check

Run from the repository root:

```bash
python -B - <<'PY'
from fractions import Fraction as Q
from itertools import combinations
from lonely_runner.checker import feasible_intervals
J = (Q(9,32), Q(3,8))
def dist(x):
    r = x - x.numerator // x.denominator
    return min(r, 1-r)
for h in range(1,5):
    v = (1,3,4,5,10,28,1680*h)
    candidates = set(J)
    for u,w in combinations(v,2):
        d = u+w
        lo, hi = (J[0]*d).__ceil__(), (J[1]*d).__floor__()
        candidates.update(Q(m,d) for m in range(lo,hi+1))
    peak = max((min(dist(t*x) for x in v),t) for t in candidates)
    eps = Q(1,10**6)
    whole = feasible_intervals(v,Q(1,8)-eps)
    local = [(max(a,J[0]),min(b,J[1])) for a,b in whole
             if max(a,J[0]) <= min(b,J[1])]
    print(h, tuple(map(str,peak)),
          [(str(a),str(b)) for a,b in local],
          str(sum((b-a for a,b in local),Q(0))))
PY
```
