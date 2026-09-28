# A uniform bound candidate from occurrence order and critical tilings

September 28, 2026. Baseline `5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.

**Result:** the coordinator and six agents supply a complete argument candidate
that an absolute finite bound exists on advancing next-safe moves for four
residual constraints at threshold `1/8`. The bound is independent of speeds,
phases and starting time. It applies to positive real speeds with arbitrary
phases, and hence includes the common-start integer inputs. **The argument
does not give a numerical value for the universal bound.** It gives the
explicit conservative bound 175 when the fastest speed is at least four
times the slowest.

All new general implications are **HYPOTHESIS / proof candidates**, materially
AI-derived and internally challenged, pending external mathematical review.
Finite exact calculations are **OBSERVED** only on their declared fixtures.
This is a candidate answer to the queued uniform-iteration question, not a
solution of the full Lonely Runner Conjecture or a novelty claim.

The most direct relational finding is a forbidden pattern: the sequence of
**advancing** runner labels cannot contain a nonempty word repeated immediately
twice. Repeated visits are possible, but an exact consecutive repetition of
their pattern is incompatible with the shared timing. Stationary projection
calls must be removed before applying this rule.

## 1. Scope, prior results, and attribution

The [preceding note](BLOCKING_CHAIN_TERMINATION_2026_09_28.md) gave a
speed-dependent bound using a finite excess-overlap allowance and the smallest
possible arithmetic overlap. The present question was whether arbitrarily
many advances could actually be required as the speeds vary.

Basic existence at this threshold is already established. Beck, Hoşten and
Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29,
[Theorem 4, printed page 12](https://math.colgate.edu/~integers/t29/t29.pdf),
gives arbitrary-phase existence at `1/(2k)` for k positive integer speeds,
crediting Schoenberg. The theorem and its elementary proof were inspected.
Here k=4. This must not be presented as newly proved existence.

An elementary consequence gives another speed-dependent benchmark. Put
`g=gcd(v_1,...,v_4)`. The cited result gives a joint-safe point within one
common period `1/g` of any start. Projections cannot overshoot its earliest
such point, and each advance lands on a new right endpoint. Counting the
endpoints in that period yields

\[
N\leq \sum_{i=1}^{4}v_i/g.
\]

This is our endpoint-count deduction, not an algorithm theorem quoted from
the source. The [literature audit](../reviews/2026-09-28-uniform-iteration/literature.md)
also identifies close chain-based precedent in Rifford,
[*On the time for a runner to get lonely*, v2, February 16, 2022](https://arxiv.org/html/2111.13688v2),
Sections 2.2 and 4.1. His irredundant-chain conditions cannot simply be assumed
for our actual projection sequence. A bounded search did not settle novelty;
no literature-wide claim of openness or originality follows.

## 2. The precise uniform statement

For four labels let `p_i=1/v_i>0` and write their open blocked occurrences as

\[
I_{i,m}=(s_i+m p_i,\ s_i+(m+1/4)p_i),\qquad m\in\mathbb Z.
\]

Their widths are `p_i/4`, each label's duty is `1/4`, and equality at an
endpoint is safe. A selected chain has strictly increasing right endpoints,
each of which lies strictly inside the next selected occurrence. Every
sequence of nonzero next-safe projections is such a chain.

**Proposed statement.** There exists a finite integer C such that every such
four-label selected chain has at most C occurrences, for all positive periods
and all shifts. No irredundancy assumption is made. Thus the statement bounds
the actual advancing sequence, not just a shortened cover certificate.

The argument below proves existence of C subject to review. It does not name
C, claim C=175 for all inputs, or repair the earlier failed 22-call guarantee
with another fitted number.

## 3. A chain cannot contain an immediately repeated label word

Suppose a chain contains `WW`, where W has length m and q_i occurrences of
label i. Choose a used label r maximizing `q_i p_i`. Match an occurrence of r
in the first copy to the corresponding occurrence m positions later. The m
destination intervals between them contain exactly q_i occurrences of each
label. The right endpoints of the q_r new r-occurrences advance by at least
`q_r p_r`; skipped laps only increase that displacement D.

For consecutive intervals let `g_j=R_{j-1}-L_j>0`. Their endpoint increments
satisfy `R_j-R_{j-1}=p_label(j)/4-g_j`. Telescoping over those m transitions
gives

\[
0<\sum_jg_j
=\frac14\sum_iq_i p_i-D
\leq\frac14\sum_iq_i p_i-\max_i(q_i p_i)
\leq0,
\]

a contradiction. There are at most four labels, which supplies the last
inequality. The g_j are positive facing-endpoint gaps; with containment they
need not equal full intersection lengths. The proof only uses their
positivity and the exact telescoping identity.

This is the square-free word rule. It is a configuration-level constraint on
which visits can follow which other visits. It gives no numerical length
bound by itself; the remaining geometry is necessary.

## 4. Large speed ratios: at most 175 advances

Order speeds `a<=b<=c<=d`. A strict chain using only c,d has at most one c
occurrence: a d-only subchain cannot bridge the c-safe gap of length
`3/(4c)` using a single d interval of width `1/(4d)`. There can be at most
one d on either side, so a pair chain has at most three intervals and span
less than `1/(4c)+1/(2d)` whenever that entire sum is needed.

Two b occurrences in a b,c,d chain would require a c,d subchain to cover the
closed b-safe gap of width at least `3/(4b)`. Its span is strictly less than
`1/(4c)+1/(2d)<=3/(4b)`, impossible. There is therefore at most one b, with
at most three selected intervals on either side: **a triple chain has at
most seven occurrences**. This concerns arbitrary selected chains, not just
the prior ten-call triple selector.

If N_a occurrences of a appear in a four-label chain, deleting their labels
leaves at most N_a+1 triple subchains. Hence

\[
N\leq N_a+7(N_a+1)=8N_a+7. \tag{1}
\]

Reuse the previously recorded centered primitive

\[
h(x)=\min(x,1/8)+\max(0,x-7/8)-x/4,
\quad H(t)=\sum_i h(\{v_it+\alpha_i\})/v_i.
\]

If M(t) is total blocked multiplicity, then `H'=M-1` away from thresholds.
On the whole union U of the selected occurrences,

\[
\int_U(M-1)\,dt\leq\frac3{16}\sum_i1/v_i\leq\frac3{4a}. \tag{2}
\]

Suppose `d>=4a`. In each whole a occurrence, length `1/(4a)`, the fastest
train must occupy at least `1/(28a)`. To verify the constant, put
`x=d/(4a)>=1`. In x normalized fastest periods the least blocked measure is

\[
f(x)=\frac{\lfloor x\rfloor}{4}
+\max(0,\{x\}-3/4)\geq x/7.
\]

For `x=n+r`, n>=1, the ratio is minimized at r=3/4, where it is
`n/(4n+3)>=1/7`. Dividing by d gives the claimed measure. Each overlap with
the fastest train contributes at least once to M-1, whether or not that
fast occurrence was selected. The selected a intervals are disjoint, so (2)
gives `N_a/(28a)<=3/(4a)` and `N_a<=21`. Equation (1) yields

\[
\boxed{d\geq4a\quad\Longrightarrow\quad N\leq175.} \tag{3}
\]

Using whole selected occurrences avoids clipping away the initial overlap.
This argument uses no integer lattice and permits arbitrary phases.

## 5. Comparable speeds: what an unbounded sequence would approach

Assume no bound exists when `d/a<=4`. Normalize a=1 and translate each
chain's union to `(0,T)`. The speeds lie in the compact set
`1=a<=b<=c<=d<=4`, and phases lie in a compact four-torus.

A union of length T contains at most `16T+8` selected occurrences: each
runner has at most `v_i T+2` relevant occurrences. Thus an unbounded sequence
of counts has T tending to infinity. Pass to convergent speeds and phases.
For each fixed positive time, continuity of phase distance says that at
least one limiting **closed** blocked interval contains it. Away from the
locally finite threshold set, the limiting multiplicity satisfies M>=1.
The limit's potential H is therefore nondecreasing on the positive half-line.

There are arbitrarily large simultaneous phase-return times t_j with
`v_i t_j mod1 ->0` for all four i. An elementary pigeonhole approximation
gives such integer times: either increasingly accurate choices are unbounded,
or a bounded repeated choice is an exact period and its multiples suffice.
Continuity gives `H(t_j)->H(0)`. A nondecreasing function with these returns
must be constant. Hence M=1 almost everywhere: the limiting closed cover is
an exact tiling by intervals with disjoint interiors.

This step deliberately retains equality. The next-safe map is discontinuous
at a block's left endpoint, so one cannot simply assert that the limiting
algorithm keeps advancing.

## 6. The limiting tiling is periodic

Two trains with periods p,q and starting offsets x,y overlap when

\[
(y-x)+\ell q-kp\in(-q/4,p/4).
\]

If p/q is irrational, these differences are dense, forcing an overlap.
Positive-time irrational rotation returns force such overlaps arbitrarily
far to the right as well. Disjoint interiors on a half-line therefore require
commensurable periods. Write `p=rg`, `q=sg` with coprime positive integers
r,s. The differences form a translate of `g Z`. Avoiding the indicated open
interval requires

\[
(p+q)/4\leq g,\qquad r+s\leq4.
\]

The only pair ratios are 1,2,3 or their reciprocals. In particular all four
limiting periods are commensurable, so the tiling has a common period P.
The half-line tiling extends to the full line by that period. The stronger
classification into speed types `(1,1,1,1)`, `(1,1,2,2)`, `(1,1,1,3)` is
independently derived in the review notes; the proof here needs only
periodicity.

## 7. A neighborhood of a tiling cannot maintain strict coverage

At each exact tiling contact exactly two occurrences meet, one ending and
one starting. A third positive-width interval would cause an interior
overlap. Choose a finite horizon containing several periods, with padding,
and small neighborhoods around its relevant contacts. Only those two
occurrences meet each neighborhood; all others are a positive distance away.

These exclusions persist for sufficiently nearby speeds and phases. Only
finitely many occurrence labels can enter the fixed horizon, and their
endpoints vary continuously. If the perturbed system openly covers each
whole contact neighborhood, the former left and right occurrences must
strictly overlap. A gap remains if they separate, and an uncovered equality
point remains if they merely touch. Coverage of the neighborhood, not just
the old contact point, is the requirement.

Let `q_i=P/p_i` be the limiting counts per period. For perturbed periods p'_i,
choose r maximizing `q_i p'_i`. The padded horizon contains a complete
tiling-word cycle anchored at r, with exactly q_i intervals of each label.
All its adjacent pairs must overlap strictly by the preceding paragraph.
Its start-to-start displacement is `q_r p'_r`, whereas its total interval
length is `sum_i q_i p'_i/4`. Summing the strict overlaps requires

\[
\max_i(q_i p'_i)=q_r p'_r
<\frac14\sum_iq_i p'_i
\leq\max_i(q_i p'_i),
\]

which is impossible. Prepare cycles for all four possible maximizing labels
before taking the finite parameter neighborhood. No assumption about which
occurrences the selector itself chooses is needed: full local coverage
forces these adjacency inequalities.

The hypothetical longer chains from Section 5 eventually lie in this
neighborhood and cover its whole fixed horizon, a contradiction. Thus a
finite comparable-speed constant C_comp exists. Together with (3),

\[
C=\max(175,C_{\rm comp})<\infty.
\]

This completes the proposed uniform-bound argument. Compactness establishes
existence, not a value for C_comp.

## 8. Exact checks, six-agent review, and their limits

The six assignments covered positive geometry, adversarial construction,
occurrence combinatorics, affine inequalities, primary-source literature,
and skeptical endpoint/compactness review. The coordinator synthesized and
checked the argument. Review notes are in
[the evidence directory](../reviews/2026-09-28-uniform-iteration/).

The [frozen protocol](../reviews/2026-09-28-uniform-iteration/protocol.json)
declares three auxiliary exact tilings, each with the exact version and four
specified perturbations, giving fifteen windows. These are shifted-phase
calibration examples, not new common-start physical configurations or
held-out tests. Four scalar occupancy fixtures check the numerical charge.

The primary affine/ceiling implementation and a separately tasked verifier
agree on 1489 compared fields, including all 99 scalar calls, 60 anchored
cycle identities, and all fifteen earliest times. The verifier checks 342
threshold points and 327 cells and retains every equality contact. The
occupancy inequality is attained at the declared `x=7/4` boundary fixture.

These fixtures have only nine advances in total and at most two in any case.
Their absence of repeated moving words is weak calibration, not a stress
test or proof of the square-free lemma. The general claims rest on the
arguments above. A separately labelled affine check replays the already
preserved 33-call auxiliary counterexample, with seven advances and final
time `38325/44704`; it does not add a physical input.

```bash
python reviews/2026-09-28-uniform-iteration/primary.py
python reviews/2026-09-28-uniform-iteration/verify.py
python reviews/2026-09-28-uniform-iteration/compare.py
python reviews/2026-09-28-uniform-iteration/affine_verify.py
```

Independent implementations and agreement among AI agents are internal
checks, not external proof certification. The proof's main review targets
are the actual-chain triple bound, recurrence at the weak limit, and the
finite contact-neighborhood argument. The reviewers found no defect under
the stated assumptions. No broad speed scan or all-reference campaign ran.

## 9. Meaning for the project and the next question

A fixed round visiting all four runners advances whenever it starts unsafe.
A uniform bound on advances therefore gives a uniform bound on those rounds
and on the prescribed eleven calls per round. It does not bound the bit cost
of arithmetic. The verified terminal time is still the earliest residual-safe
time; it may fall outside a supplied core-safe window.

For the full eight-runner system there are seven moving constraints, whose
total blocking duty at threshold 1/8 is 7/4. Both the critical potential
cancellation and the mean-versus-maximum cycle contradiction used here rely
on four duties summing to one. They do not prove the full conjecture.

The relational insight is precise: apparent freedom to overlap neighboring
windows is constrained by the occurrence counts and periods of an entire
cycle. The same parameter choices must make every handoff work, and the
summed inequalities can be contradictory even when isolated handoffs look
possible. This supplies structure that separate speed or pair-overlap totals
do not record.

**Next bounded milestone:** turn the comparable-speed compactness argument
into an explicit, auditable numerical bound, or identify a precise obstruction
to that extraction. Start from the finite occurrence inequalities and the
tiling neighborhoods already supplied; do not choose a step cap by fitting
the fixtures. External review and novelty comparison remain outstanding.
The arbitrary full-configuration core/window existence bridge is still open.
Hourly research remains paused.
