# LTCM test: an exact spectrum for a variable-ratio family

September 29, 2026. Base commit: 4c4d370d0bb9b97e47eca9e9260d64beac1502ef.

**Status: HYPOTHESIS / complete proof candidate with exact finite polyhedral certificates.** The construction, symbolic comparisons, and prescribed finite controls have been checked by separately structured programs written in this session. This is not independent human review or a novelty determination. AI materially supplied derivation, implementation, checking, source comparison, and writing.

## Result and scope

For eight common-start runners, select reference 0 and let
\[
V(q)=(1,q,q+1,q+2,q+3,2q+3,2q+5),\qquad q\in\mathbb Z,\quad q\ge2.
\]
Define
\[
M(q)=\max_{0\le t\le1}\min_{v\in V(q)}\|vt\|.
\]
The proposed exact answer and one attaining time are:

| Parameter | \(M(q)\) | \(t(q)\) |
| --- | --- | --- |
| \(q=4\) | \(1/8\) | \(1/8\) |
| \(q\equiv0\pmod3\) | \(\dfrac{q}{3(2q+1)}\) | \(2M(q)\) |
| \(q\equiv1,2\pmod6\) | \(1/6\) | \(1/6\) |
| \(q\equiv4\pmod6,\ q\ge10\) | \(\dfrac{q-1}{3(2q+1)}\) | \(2M(q)\) |
| \(q\equiv5\pmod6\) | \(\dfrac{q+1}{2(3q+5)}\) | \(3M(q)\) |

These five branches cover every integer \(q\ge2\). The special input \(q=4\) is the archived tight13 configuration. It is the **only** member of this ray with \(M=1/8\). Every other member has \(M\ge1/7\), with equality at \(q=3,10\); hence it has positive \(1/8\)-safe duration. At \(q=4\), the complete safe set is exactly
\[
\{1/8,3/8,5/8,7/8\}.
\]

This classifies the optimal separation of the selected reference, not the optimal separation of every reference runner. It does not establish the full conjecture, arbitrary eight-runner reduction, arbitrary real \(q\), or the full two-parameter family.

The rule uses a fixed number of rational operations and residue tests. No list of \(q\)-many laps is needed to select its witness. Arithmetic bit lengths still grow with the input.

## Why this is the intended language test

The preceding LTCM review distinguished faithful representation from useful selection. It also ruled out a tempting induction: remove speed \(5=1+4\) from tight13, then widen every retained safe cell from threshold \(1/7\) to \(1/8\). None contains any full-system witness. Each of the four full witnesses remains isolated already in the retained system, controlled by opposing pairs 1/7 or 11/13, and its particular lap cell is empty at the stronger threshold. The smaller system does have stronger witnesses, for example \(t=1/5\). A complete method must therefore permit new lap cells.

The present test supplies those labels from arithmetic. A cell carries closed safety constraints; a transfer carries the common-time equation; a selection rule carries a coverage argument. The final formulas select actual witnesses across an unbounded family and have matching upper bounds.

The mechanism is established polyhedral and relative-spectrum mathematics applied to this explicit family. It is not evidence that a new mathematical discipline has been created.

## 1. A fixed geometric model with the actual orbit retained

Put \(x=t\bmod1\), \(y=qt\bmod1\). The seven phases are the reductions modulo one of
\[
x,\quad y,\quad x+y,\quad2x+y,\quad3x+y,\quad3x+2y,\quad5x+2y.
\]
Let the corresponding coefficient rows be
\[
\mathcal A=((1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2)).
\]

The physical orbit is still required to satisfy
\[
qx-y=h,\qquad h\in\mathbb Z. \tag{1}
\]
An arbitrary safe point in the two-dimensional square is insufficient.

Because all speeds are integers, reflection \(t\mapsto1-t\) preserves distances. We may restrict \(x\) to \([0,1/2]\). For an optimum at least \(1/8\), \(x,y\) lie in
\[
1/8\le x\le1/2,\qquad1/8\le y\le7/8.
\]
For a fixed ambient lap vector \(m\), attach a separation coordinate \(z\) and impose
\[
z\ge1/8,\quad x\le1/2,\qquad
m_i+z\le a_i x+b_i y\le m_i+1-z. \tag{2}
\]
These define a bounded rational polytope. The bounds on \(x,y,z\) follow from the first two forms. Relevant labels satisfy \(0\le m_i<a_i+b_i\); the first two labels are zero.

The model has fixed size because \(\mathcal A\) is fixed. Dependence on \(q\) occurs only in the integer-plane condition (1).

### Fixed-cell lemma

There are exactly ten nonempty polytopes (2): three singletons, six tetrahedra, and one six-vertex polytope. Together they have 33 vertex occurrences and 45 edge occurrences. The maximum \(z\) is \(1/6\); every vertex below \(1/6\) has \(z\le1/7\).

Here is the complete vertex certificate. A triple means \((x,y,z)\); labels follow the order of \(\mathcal A\).

| Cell | Ambient lap vector \(m\) | Vertices |
| --- | --- | --- |
| 0 | \((0,0,0,0,0,0,0)\) | \((1/8,1/8,1/8)\) |
| 1 | \((0,0,0,0,0,0,1)\) | \((1/8,1/4,1/8),(1/6,1/6,1/6),(7/40,1/8,1/8),(5/24,1/8,1/8)\) |
| 2 | \((0,0,0,0,0,1,1)\) | \((1/8,3/8,1/8),(1/8,1/2,1/8),(1/6,1/3,1/6),(5/24,1/4,1/8)\) |
| 3 | \((0,0,0,0,1,1,2)\) | \((3/8,1/8,1/8)\) |
| 4 | \((0,0,0,1,1,1,2)\) | \((3/8,3/8,1/8),(1/2,1/8,1/8),(1/2,1/6,1/6),(1/2,3/16,1/8)\) |
| 5 | \((0,0,0,1,1,2,2)\) | \((3/8,1/2,1/8)\) |
| 6 | \((0,0,0,1,1,2,3)\) | \((11/24,5/12,1/8),(1/2,5/16,1/8),(1/2,1/3,1/6),(1/2,3/8,1/8)\) |
| 7 | \((0,0,1,1,1,2,3)\) | \((11/40,7/8,1/8),(2/7,6/7,1/7),(7/24,5/6,1/8),(1/3,5/6,1/6),(1/3,7/8,1/8),(3/8,3/4,1/8)\) |
| 8 | \((0,0,1,1,2,2,3)\) | \((11/24,3/4,1/8),(1/2,5/8,1/8),(1/2,2/3,1/6),(1/2,11/16,1/8)\) |
| 9 | \((0,0,1,1,2,3,4)\) | \((19/40,7/8,1/8),(1/2,13/16,1/8),(1/2,5/6,1/6),(1/2,7/8,1/8)\) |

**Finite verification and completeness.** The first construction successively clips the baseline square by each permitted lap band, then enumerates all triple intersections of the facets in (2). The second constructs all 48 possible boundary planes globally, solves their 17,296 triples by a separate Gaussian-elimination implementation, and retains exactly the points satisfying the seven modular safety constraints. Grouping those points by their uniquely determined labels gives the same ten cells and all 33 vertices.

Every nonempty bounded polytope has a vertex. Every vertex is determined by three linearly independent active planes from this exhaustive list, including lower-dimensional cells. Thus the second construction is a finite certificate of completeness, not a sample of the square. Rational arithmetic is exact throughout. This fixed finite lemma is the computational part of the proof candidate.

## 2. A finite selection rule, before simplification

Intersect a polytope (2) with any physical plane (1). Maximizing \(z\) on the slice reaches a vertex of that slice. Such a vertex is either an original vertex or lies on an original edge: at least two independent original facet constraints are active, in addition to the slicing plane, unless the point was already a vertex.

On an edge joining \(P\) to \(Q\), both \(z\) and \(H=qx-y\) are affine. If \(H\) varies, \(z\) is affine as a function of \(H\). Among the integers between \(H(P)\) and \(H(Q)\), an extremal feasible integer therefore attains the largest \(z\) on that edge. It is selected by one floor or ceiling. If \(H\) is constant, the edge either misses all integer planes or lies in one; then an endpoint with maximal \(z\) suffices. Original vertices are checked separately.

Consequently, at most 33 vertex checks and 45 edge selections suffice, independently of \(q\). This is a complete selector for safety at least \(1/8\), once the lower witness construction below guarantees that this threshold is attainable. This is a bounded number of candidates in a fixed ambient geometry, not an enumeration of the physical schedule.

The five-branch result is a further simplification of this selector.

## 3. The matching upper bound

Any slice maximum strictly above \(1/7\) must lie at a \(z=1/6\) vertex or on an edge incident to one: all other vertices and edges have height at most \(1/7\).

Write an incident edge as
\[
(x,y,z)=(x_0+\alpha e,\ y_0+\beta e,\ 1/6-e),\qquad e\ge0.
\]
Its physical condition is
\[
h=h_0+(q\alpha-\beta)e,\qquad h_0=qx_0-y_0. \tag{3}
\]
If \(\rho=\{h_0\}>0\), reaching an integer requires a loss of at least
\[
e\ge
\begin{cases}
\rho/|q\alpha-\beta|,&q\alpha-\beta<0,\\
(1-\rho)/|q\alpha-\beta|,&q\alpha-\beta>0.
\end{cases} \tag{4}
\]
When \(\rho=0\), the peak itself is on the actual orbit. Dropping the finite length of an edge enlarges the permitted set, so (4) remains a valid upper-bound device.

The complete peak-edge data are:

| Peak | \((x_0,y_0)\) | Outward directions \((\alpha,\beta)\) |
| --- | --- | --- |
| A | \((1/6,1/6)\) | \((-1,2),(1/5,-1),(1,-1)\) |
| B | \((1/6,1/3)\) | \((-1,1),(-1,4),(1,-2)\) |
| C | \((1/2,1/6)\) | \((-3,5),(0,-1),(0,1/2)\) |
| D | \((1/2,1/3)\) | \((-1,2),(0,-1/2),(0,1)\) |
| E | \((1/3,5/6)\) | \((-2,1),(0,1),(1,-2)\) |
| F | \((1/2,2/3)\) | \((-1,2),(0,-1),(0,1/2)\) |
| G | \((1/2,5/6)\) | \((-3/5,1),(0,-1/2),(0,1)\) |

All these edges allow \(0\le e\le1/24\), except E's \((-2,1)\) edge, which allows \(0\le e\le1/42\).

For \(q\equiv1,2\pmod6\), A or B is attained and the ambient bound \(M\le1/6\) is sharp. In the remaining residues, the smallest losses among the relevant directions reduce to the following table. C dominates D, F and G; their vertical alternatives cannot improve a maximum above \(1/7\).

| Residue and domain | A loss | B loss | C loss | E loss | Minimum |
| --- | --- | --- | --- | --- | --- |
| \(q\equiv0\pmod6,\ q\ge6\) | \(\frac1{6(q+1)}\) | \(\frac1{3(q+2)}\) | \(\frac5{6(3q+5)}\) | \(\frac1{6(2q+1)}\) | E |
| \(q\equiv3\pmod6,\ q\ge3\) | \(\frac1{3(q+2)}\) | \(\frac1{6(q+4)}\) | \(\frac1{3(3q+5)}\) | \(\frac1{6(2q+1)}\) | E |
| \(q\equiv4\pmod6,\ q\ge10\) | \(\frac1{2(q+2)}\) | \(\frac1{3(q+4)}\) | \(\frac5{6(3q+5)}\) | \(\frac1{2(2q+1)}\) | E |
| \(q\equiv5\pmod6,\ q\ge5\) | \(\frac1{3(q+1)}\) | \(\frac1{2(q+4)}\) | \(\frac1{3(3q+5)}\) | \(\frac1{6(q+2)}\) | C |

These are rational comparisons, not empirical selections. After multiplying positive denominators, each is a linear inequality in \(q\). For example, in residue 4, comparing E with B gives \(q-10\ge0\), and comparing E with C gives \(2(q-10)\ge0\). The audit checks the winning loss against **all 21 original directions**, giving 84 linear certificates over the four unbounded residue domains. Each certificate records a nonnegative slope and a nonnegative value at its smallest allowed \(q\).

Subtracting the minimum loss from \(1/6\) yields the stated formulas for every \(q\ne4\). Each proposed value is at least \(1/7\). If a larger actual maximum existed, it would lie above \(1/7\) and contradict (4) and the comparisons. This also handles equality at \(q=3,10\).

### Exceptional \(q=4\)

Here an argument restricted to heights above \(1/7\) is insufficient. The full fixed-cell table gives these ranges of \(H=4x-y\):

| Cell | Range |
| --- | --- |
| 0 | \(\{3/8\}\) |
| 1 | \([1/4,17/24]\) |
| 2 | \([0,7/12]\) |
| 3 | \(\{11/8\}\) |
| 4 | \([9/8,15/8]\) |
| 5 | \(\{1\}\) |
| 6 | \([17/12,27/16]\) |
| 7 | \([9/40,3/4]\) |
| 8 | \([13/12,11/8]\) |
| 9 | \([41/40,19/16]\) |

Only cells 2 and 5 meet an integer plane. In cell 2, \(H=0\) is achieved only at \((1/8,1/2,1/8)\); cell 5 is the singleton \((3/8,1/2,1/8)\). Thus the only half-period witnesses are \(1/8,3/8\), both at height \(1/8\). Reflection gives the four complete witnesses and proves the exceptional upper bound.

## 4. Actual-time witnesses and lap reconstruction

For the E branches put
\[
x=1/3-2e,\qquad y=5/6+e,\qquad z=1/6-e.
\]
The phases after subtracting ambient labels \((0,0,1,1,1,2,3)\) are
\[
1/3-2e,\quad5/6+e,\quad1/6-e,\quad
1/2-3e,\quad5/6-5e,\quad2/3-4e,\quad1/3-8e.
\]
All lie in \([z,1-z]\) for \(0\le e\le1/42\). In particular, the last phase satisfies the lower bound exactly when \(e\le1/42\).

- If \(3\mid q\), take \(e=1/[6(2q+1)]\). Then \(qx-y=q/3-1\) is integral and \(t=x=2M(q)\).
- If \(q\equiv4\pmod6,\ q\ge10\), take \(e=1/[2(2q+1)]\). Then \(qx-y=(q-4)/3\) is integral and again \(t=x=2M(q)\).

For the C branch put
\[
x=1/2-3e,\qquad y=1/6+5e,\qquad z=1/6-e.
\]
With ambient labels \((0,0,0,1,1,1,2)\), the phases are
\[
1/2-3e,\quad1/6+5e,\quad2/3+2e,\quad
1/6-e,\quad2/3-4e,\quad5/6+e,\quad5/6-5e.
\]
All are safe for \(0\le e\le1/24\). For \(q\equiv5\pmod6\), set \(e=1/[3(3q+5)]\). Then \(qx-y=(q-1)/2\) is integral and \(t=x=3M(q)\).

For residues 1 and 2, \(t=1/6\) gives, respectively, phase numerators
\[
(1,1,2,3,4,5,1),\qquad(1,2,3,4,5,1,3)
\]
over denominator 6. The exceptional \(q=4,t=1/8\) is already certified.

If \(m\) is an ambient label vector and \(h=qx-y\), the **physical** lap labels are
\[
\ell_i=m_i+b_i h.
\]
Indeed, \(v_i(q)t=a_i x+b_i y+b_i h\). This is the explicit witness transfer. The labels may grow with \(q\), but their construction does not enumerate earlier laps.

## 5. Verification record

The protocol was saved before the ambient construction. The five-branch symbolic candidate, directions, and intended upper-bound proof were saved before evaluating any physical \(q\)-case.

- The primary fixed-cell construction and a global-boundary-plane reconstruction agree on all ten cells and 33 vertices.
- The audit supplies 84 symbolic comparisons valid on unbounded residue domains, and affine endpoint certificates for both witness charts. These certify linear inequalities throughout the declared error intervals.
- For exactly \(q=2,\ldots,25\), a direct one-dimensional lower-envelope method agrees with the ambient selector and the formula. It partitions time at every runner's tent breakpoint, then checks every affine-line intersection inside each time cell.
- The 24 direct calculations use 5,456 time knots and 9,376 line-pair crossing occurrences. These are processing counts, not independent samples.
- The direct calculation recovers all four tight13 maximizing times. It also retains ties at \(q=3,10\).
- The two predeclared large inputs \(q=100003,100004\) pass witness-only checks. Both lie in the \(1/6\) branches; no large-\(q\) exhaustive optimality check is claimed.
- No other physical family, phase grid, reference runner, or broad parameter scan was evaluated. Existing project tests and previous research scripts were not rerun.
- The scripts share only standard-library rational arithmetic and the declared coefficient data. They were written by the same AI coordinator, so separately structured checks are not independent authorship or external review.

Reproduction, from the repository root:
~~~bash
python3 reviews/2026-09-29-ltcm-spectrum/ambient.py
python3 reviews/2026-09-29-ltcm-spectrum/verify.py
python3 reviews/2026-09-29-ltcm-spectrum/audit.py
~~~

The manifest records the source and output hashes, protocol, and pre-validation derivation.

## 6. Precedents and remaining limits

Jain and Kravitz's *Relative Lonely Runner spectra*, arXiv:2411.12684v2 (December 9, 2024), §6 studies a two-dimensional torus with generators
\[
(1,0,1,2,3,3),\qquad(0,1,1,1,1,2).
\]
These are exactly our first six coefficient rows. The seventh row here is \((5,2)\). Their framework already explains how actual one-dimensional subtori can be treated through arithmetic and fixed geometric data. Our \(M\) equals \(1/2-D\) in their distance-to-center convention.

The source's §6 generators and parameterization were inspected directly. Earlier design review also identified the exact fixed-lap cone construction in Beck–Hoşten–Schymura, *Lonely Runner Polyhedra*, §2 and Proposition 1. No novelty is claimed for phase lifting, polytopes, slice-edge optimization, integer rounding, or residue case analysis.

A targeted text search did not establish whether this exact appended-coordinate formula has appeared elsewhere; notation-sensitive search results were insufficient for a novelty conclusion. Ordinary eight-runner existence was already credited in the preceding research review. This package's substantive target is the exact optimum and explicit bounded selector for the displayed ray.

Primary source: https://arxiv.org/html/2411.12684v2#S6  
Polyhedral precedent: https://math.colgate.edu/~integers/t29/t29.pdf

The next useful step is independent review of the fixed-cell certificate, slice-edge argument, and residue comparisons, together with a focused prior-art comparison. Only after that should the variable-\(p\) family or a broader coefficient class be considered. The present result does not imply a threshold-preserving induction for arbitrary runner count.

Hourly research remains paused. No agents were newly delegated in this continuation, no outside researchers contacted, no main merge performed, and no paid or unattended computation launched.

