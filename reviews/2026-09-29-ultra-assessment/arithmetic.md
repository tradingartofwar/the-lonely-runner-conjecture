# Arithmetic assessment: contact denominators, resonances, and descent

September 29, 2026. Assessment against the coordinator's pinned head
`7b0101376e00dbb71537d3a62e39ec75cee113cc` and the supplied local snapshot.
The snapshot has no Git metadata; that pin is supplied provenance, not a
locally verified checkout identity. No mathematical executable calculation,
scan, or frozen-output modification was performed. Materially AI-assisted
derivations below are **HYPOTHESIS / proof candidates**, except where an
existing literature result or an archived observation is explicitly credited.
There is no novelty claim.

Conventions: `n` total common-start runners, `k=n-1` nonzero relative
constraints, threshold `delta=1/n`; replace signed relative speeds by their
absolute values for this selected-reference analysis. Coincident absolute
constraints may be removed from the function, but do not silently change
the original threshold. Equality is safe. The statements involving opposing
threshold sides assume `n>=3`.

## Assessment

**Most consequential assessment correction:** strict feasibility of the
proposed two-additional-relation torus is already implied by known
lower-runner existence. Section 6 gives a short rational-polytope reduction,
independently checked by the coordinator. With seven phase coordinates
and a three-dimensional relaxed torus, it supplies gap at least `1/6`,
strictly above `1/8`. Therefore P2 positivity is not the missing new
existence lemma; useful explicit certificates or quantitative mass bounds
are the remaining potential contribution of that proposal.

The useful arithmetic progress is the conversion of complete blocking into
simultaneous integer obligations: endpoint residues, one lap label per
positive interval, and relations between those labels. The last-runner
report's narrow-core contradiction is substantially stronger than a width
test because it retains those obligations. It is a useful mechanism within
already covered families.

The general gap remains a **selection/existence theorem**. The record does
not show that arbitrary speeds have a core with an arithmetically protected
collection of openings. Nor does it give a decreasing operation carrying
every hypothetical counterexample to a simpler counterexample. Contact
denominators alone do neither. The fixed core `{1,4,5}` is a substantial
restriction, not a normalization of an arbitrary eight-runner instance.

## 1. The exact contact restriction is stronger than divisibility of a sum

Let `u,v` be positive integer speeds, `g=gcd(u,v)`, `U=u/g`, `V=v/g`.
They have opposite threshold contacts

`u*t = 1/n (mod 1)`, `v*t = -1/n (mod 1)`

if and only if

`n | U+V = (u+v)/g`.

For necessity, write `u*t=m+1/n`, `v*t=l-1/n`. Eliminating `t` and
dividing by `g` gives `n*(U*l-V*m)=U+V`. Conversely, the divisibility
implies `gcd(U,n)=1`, since a common divisor would also divide `V`.
For `r=U^{-1} mod n`, all contacts of this orientation in `[0,1)` are

`t=(r+n*j)/(n*g)`, `j=0,...,g-1`.

The reverse orientation uses `-r mod n`. These are two distinct classes
when `n>=3`, giving **exactly `2g` contacts for the pair**, before checking
other runners. The supplied geometry reviewer independently obtained and
checked the same formula. Their subsequent archive search found the
normalized divisibility criterion already recorded in HANDOFF.md; this is
a retained/rederived restriction, not a newly claimed project result.

The weaker condition `n | u+v` is necessary but insufficient. At `n=8`,
the pair `(4,12)` has sum 16, but normalized sum 4. It has no opposing
`1/8` contacts. This is a hand countercheck of the weakened formulation,
not a counterexample to loneliness.

Every isolated point of the full closed safe set has at least one active
constraint entering safety and another leaving it. With positive absolute
speeds, these are precisely opposite threshold sides. Thus every isolated
witness belongs to one of the eligible pair grids above. A candidate on a
grid remains a witness only if **all** constraints are safe there. If no
pair is eligible, nonempty safety implies positive duration; it does not
prove that safety is nonempty.

### The same arithmetic at an arbitrary local maximum

Write `f(t)=min_i ||v_i*t||`. Suppose `t0` is a local maximum with
`0<f(t0)=p/q<1/2`, in lowest terms. At least one active branch has positive
slope and one has negative slope: otherwise a sufficiently small time
perturbation increases every active minimum, while inactive constraints
retain their positive slack. Consequently there is an opposite active pair
`u,v`, and

`q | (u+v)/gcd(u,v)`.

The proof above replaces `1/n` by `p/q`, using `gcd(p,q)=1`.
If `t0=A/B` is reduced, the individual active equation also implies
`B=q*h`; every active speed is divisible by `h`, and, after division by
`h`, its residue modulo `q` is one of

`p*A^{-1}` and `-p*A^{-1}`.

For opposite active speeds, `B | u+v`. The normalized-pair condition is
stronger than just this last divisibility.

The pair-sum candidate-time principle is established precedent: Kravitz
(2021), Proposition 2.1, places local maxima on times `m/(u+v)`.
The published Section 2 and adjoining discussion on printed pages 4–5
were inspected for this assessment. This report's elementary derivation
spells out the reduced denominator and gcd information.

**Crucial quantifier:** `n` enters the contact divisor only after the value
has been shown to be exactly `1/n`. A hypothetical counterexample has a
global maximum `p/q<1/n`; its active normalized sums must be divisible by
`q`, not by `n`. Applying the threshold divisibility to all global maxima
would assume away the central issue. Threshold contacts, local maxima,
and globally tight instances are three different hypotheses.

## 2. A direct restriction on a minimal counterexample from pre-jumps

Here is a genuine conditional structural restriction, independent of
the fixed `{1,4,5}` core. It uses lower-runner existence explicitly.

Let a core `C` consist of `r` of the `k` speeds, all divisible by an integer
`h>=2`; let the other `s=k-r` speeds be `w_1,...,w_s`. Suppose the core has
a time `t0` with every core distance at least `1/n`. Put

`g_j=gcd(h,w_j)`, `q_j=h/g_j`.

Then a full safe time exists among `t0+l/h`, `l=0,...,h-1`, provided

`sum_j g_j*ceil(2*q_j/n) < h`.                         (P)

Proof: each jump fixes every core phase. The phases of `w_j` form a
translated `q_j`-point uniform grid, each point repeated `g_j` times.
An open unsafe arc of length `2/n` contains at most `ceil(2*q_j/n)`
grid points. If (P) holds, the union of the strictly blocked jump labels
has cardinality below `h`. A surviving label gives a closed-safe time.
Open arcs are essential: points exactly at distance `1/n` are retained.
This conclusion need not give positive duration for the full configuration.

For a hypothetical first counterexample in runner number, the core
assumption follows from LRC for `r+1<n` total runners, which gives margin
at least `1/(r+1)>1/n`. Therefore **every** choice of such a core in a
minimal-counterexample tuple must violate (P). This is a necessary
restriction; it is not an induction step because that violation may occur.

When all residuals are coprime to `h`, it becomes

`s*ceil(2*h/n) >= h`                                  (necessary).

If `2s<n`, the strict opposite is guaranteed by
`h>=n*s/(n-2s)`: indeed `ceil(x)<x+1` gives
`s*ceil(2h/n)<2sh/n+s<=h`. More generally replace `s` in the additive
error by `sum_j g_j`. A sparse exceptional set can therefore exclude a
large common divisor among a majority core.

This is standard pre-jump/counting reasoning made explicit, not a new
existence theorem. Kravitz Section 2, printed p.5, supplies the established
core-preserving time-jump precedent. At a maximum `p/q` the preceding
denominator factor `h=B/q` divides all active speeds; if enough of those
speeds form a majority core, (P) constrains the remaining gcds. However,
there is **no reason all tight instances should have many active speeds**:
at `t=1/n` the canonical tight tuple `1,...,n-1` has just two active speeds
when `n>3`. Thus this restriction does not become universal merely by
calling the core “the active set.”

## 3. Several runners can jointly defeat an otherwise reasonable pair grid

Kravitz's three-speed pair-grid argument cannot be generalized by only
requiring that no residual speed annihilate the entire grid.

Hand counterexample to that proposed extension: take `n=5` and speeds
`{1,2,3,5}`. Use the pair `(1,5)`, with sum 6. Its `1/5`-safe grid points
are `m/6` for `m=2,3,4`. Speed 3 collides at `m=2,4`; speed 2 collides at
`m=3`. Neither residual is divisible by 6, yet together they block the
whole pair-safe grid. The actual point `t=1/4` is safe for all four speeds.

Thus a useful extension must constrain a **joint residue cover**, not just
one residual's divisibility. This is the fastest falsifier of the natural
“every pair grid has a single annihilating runner” explanation. It also
illustrates why finding local pair candidates is much easier than proving
one survives all other runners.

## 4. Short relations: the necessary refinement and its present weakness

Beck–Everett, *Lonely Runner Relations*, arXiv:2609.06259v2 (September 23,
2026; manuscript September 22), Theorems 1.1 and 2.1, imply that a tight
instance or counterexample with `k=n-1` speeds has an integer relation of
1-norm at most `2n+1` whose coefficient sum is odd. The statement and
Section 2's Fourier setup/proof were inspected; no full independent proof
audit or current-frontier claim is made.

That condition already holds throughout the fixed-core family:
`1+4-5=0` has norm 3 and odd coefficient sum. Applying the theorem to
these inputs without more information supplies **no constraint on
`a,b,c,d`**.

A standard relative Fourier argument can force a relation involving a
residual. For completeness, the following coarse version is derived here;
the duality reviewer independently obtained a much stronger weighted
version, which should be preferred in any integrated report.

For any fixed integer core `c_1,...,c_r`, put
`rho=1/2-1/n`, and let

`phi(x)=max(1-||x-1/2||/rho,0)`.

It is positive exactly for strict threshold safety. Suppose

`mu=integral_0^1 product_i phi(c_i*t) dt > 0`.

Its Fourier coefficients are `rho*(-1)^m*sinc(pi*m*rho)^2`; their
absolute values sum to 1, their zeroth coefficient is `rho`, and the
absolute tail beyond `R` is at most `2/(pi^2*rho*R)`. For an extension by
`s` residual speeds, the terms whose residual coefficients vanish sum to
`mu*rho^s`. If no relation involving a residual has every coefficient of
absolute value at most `R`, all other surviving terms lie in the product
tail, whose absolute mass is at most `2k/(pi^2*rho*R)`. Therefore

`R > 2k/(pi^2*mu*rho^(s+1))`

forces a mixed relation whenever the full tuple has no strict lonely time.
All rearrangements are justified by absolute summability. This addresses
strict safety only: zero weighted integral includes valid equality-only
instances.

This is a resonance mechanism, but its initial constants are not useful
pruning. For `{1,4,5}` at `n=8`, the interval of radius `1/96` around
`1/3` gives `mu >= (1/48)*(5/12)^3 =125/82944`. The resulting coefficient
cutoff is very large. More decisively, once the existing work has bounded
`a<=34`, the elementary relation `a*1-a=0` already involves a residual and
has norm at most 35. A large-coefficient mixed-relation conclusion then
says nothing beyond what the tuple itself plainly supplies. The better
duality bound also faces this issue. An odd-sum version can combine this
with the odd core relation when needed; it does not repair the weakness.

The worthwhile refinement is a relation **outside the entire lattice of
relations on the already bounded core**, with a coefficient bound small
enough to impose a new restriction on the still free speeds. The general
relative formulation compares the weighted mass on that core's torus with
the tail of relations outside its lattice. It is a sound way to organize
resonances, but it does not by itself prove that the next resonance stratum
still meets the target box. At the final one-dimensional stratum that is
the original problem again.

## 5. Why an unqualified speed-perturbation descent is invalid

A fixed rational tuple has a finite set of maxima in one period. Small
changes to speeds preserve its finite-time pieces for a while. They do
not preserve its full-period coverage, because the perturbed tuple can
have a much longer period, or an irrational orbit closure.

There is an elementary hand example. The two-speed tuple `(1,2)` has
maximum `1/3`. For even integer `N`, perturb it to `(1,2+1/N)`.
At time `t=N/2+1/2`, the two distances are `1/2` and
`1/2-1/(2N)`. Thus arbitrarily small rational speed perturbations introduce
late near-half-lap witnesses. The relevant time grows with `N`, and the
period after normalization grows too.

A proposed minimal-counterexample descent must therefore state an integer
complexity that decreases and prove that **all times in the new period**
remain blocked. Active gradients in the old period do not provide that
implication. Likewise, dividing only an active gcd changes the other
speeds and is not an invariance. Common scaling of every speed is the
valid normalization.

## 6. A lower-runner reduction already settles relaxed-torus existence

This hand deduction is important when assessing a proposed independent-
relation induction. Let `Lambda` be a saturated integer relation module,
let `K=Lambda^perp` be its rational real nullspace, and suppose `K` has
dimension `d>=2` and contains a strictly positive speed vector. The relaxed
phase torus is `H=K/(K intersect Z^k)` modulo `Z^k`.

The polyhedron `P={w in K : w_i>=1 for every i}` is nonempty. Minimize
`sum_i w_i` on it: an appropriate sublevel is nonempty and compact because
all coordinates are positive and bounded above by the sum. Take a vertex
of the compact minimizing face. It is a rational vertex of P. At least
`d` coordinate inequalities must have independent restrictions active at
that vertex; otherwise a nonzero direction in K preserves all active
equalities, and sufficiently small movement in both directions preserves
the other inequalities, contradicting extremality. Thus at least `d`
coordinates of this rational w equal 1, and every coordinate is positive.

Merge these duplicate constraints and clear denominators. There are at
most `k-d+1` distinct positive moving speeds. **Assuming LRC for that
smaller number of constraints**, the corresponding orbit has a point with
every coordinate distance at least `1/(k-d+2)`. Because `w in K`, this
point belongs to H. Its distance is strictly above `1/(k+1)`.

For the duality report's proposed two-additional-relation torus over
`{1,4,5}`, there are `k=7` phase coordinates, total relation rank 4, and
`d=3`. Known six-total-runner existence therefore already supplies a point
in that relaxed torus with distance at least `1/6>1/8`. With three added
independent relations, `d=2`, and known seven-total-runner existence
supplies at least `1/7>1/8`. The one-additional-relation case has an even
smaller effective runner count.

This is the familiar rational-dimension reduction philosophy, here given
a direct rational-polytope proof candidate. The 2025 survey's Section 2
describes the established lower-runner reduction context; this particular
vertex derivation is supplied for internal audit, without a novelty claim.
Consequently **P2's bare strict-existence conclusion is already implied
by known lower-runner results**. Its potentially useful output would be
an explicit efficient phase certificate or a useful quantitative Haar
mass bound. Positivity alone should not be presented as the new missing
existence theorem. This correction was sent immediately to the coordinator
and duality reviewer. The coordinator independently checked the vertex
reduction; this remains internal AI review, not external certification.
The earlier P2 proposal should remain in the history with this explicit
correction.

## 7. Highest-value next lemma and quickest falsification

The arithmetic direction worth testing is a **useful independent-relation
bound**, rather than another denominator census, the already vacuous first
mixed relation, or relaxed-torus existence alone. Section 6 shifts the
value of a two-relation study to controlled certificates and quantitative
mass estimates.

A concrete, deliberately unproved target in the present family is:

> For every admissible common-start integer tuple
> `V=(1,4,5,a,b,c,d)` with `a<b<c<d`, if `max_t min_i ||V_i*t||<=1/8`,
> then some integer relation `m dot V=0` has `sum |m_i|<=17`, odd
> coefficient sum, and `(m_c,m_d)!=(0,0)`.

This is a proposed **relative strengthening** of the existing
Beck–Everett bound, not something established by that theorem or by the
Fourier-tail argument. It would place the remaining speeds in finitely
many explicit strips `h_c*c+h_d*d=-(h_1+4h_4+5h_5+h_a*a+h_b*b)` with a
small coefficient budget; that is real residual arithmetic information.
It would not complete the proof, because such strips can contain
unbounded or many integer pairs. There is presently no evidence here
that the coefficient 17 is valid for this refinement.

**Quickest falsification:** before any new search, use archived globally
tight cases only, and try to prove that every norm-at-most-17 harmful
relation involving either of the last two speeds is absent. A single
such tight instance refutes the target. This is a relation-feasibility
problem; it does not require rebuilding safe-time schedules. Conversely,
checking several successes would not justify the universal target. No
executable check was authorized or run in this review. For the inherited
tight `(1,4,5,6,7,11,13)`, obvious relations `11-5-6=0` and `13-6-7=0`
already pass, so that case supplies no meaningful positive evidence.

**Recommended next action:** first compare this relative target with
existing relation/finite-reduction literature and audit whether a
projected version of the weighted Fourier argument can actually preserve
the small coefficient bound. If not, stop this route before turning a
huge but ineffective bound into another finite project. For the existing
window program, retain the normalized contact grids and endpoint/lap
relations, but require the next claimed advance to force a compatible
certificate for an unbounded class of cores.

## Source and reading limits

- [Kravitz, published 2021 paper](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf):
  Section 2, Proposition 2.1 and pre-jump discussion, printed pp.4–5;
  the displayed pair-grid statement in Lemma 5.1 was also inspected.
- [Beck–Everett v2](https://arxiv.org/html/2609.06259v2): Theorems 1.1,
  2.1 and Section 2's Fourier argument, read for the relation mechanism.
  The role of the supplied fixed core is this report's own assessment.
- [Cordella primary record](https://arxiv.org/abs/2609.03444): abstract
  retrieved; its claimed near-threshold spectral classification is a
  relevant follow-up, not an input to any deduction here. A search
  surfaced v2 but its full text did not retrieve in this review.
- [Perarnau–Serra survey v3](https://arxiv.org/html/2409.20160v3): Section 2
  was read for the rational-dimension/lower-runner reduction context;
  no current-frontier assertion is taken from its 2025 snapshot.
- Local readings: governance files, current README/HANDOFF/LR2 entries,
  recent six-core and last-runner arithmetic reports, source notes and
  DOMAIN_CONNECTIONS. Several older note paths named by governance are
  absent from this partial snapshot; no claim to a full-history audit.

All arithmetic counterchecks and formulas above were reasoned by hand.
No independent human certification, novelty review, full-conjecture
coverage, new all-reference result, or executed finite exhaustion is claimed.
