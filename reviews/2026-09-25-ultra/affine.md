# Review of the fixed-core affine and fast-cluster arguments

Reviewer: a fresh AI mathematical reviewer, separate from the generating work. Date: September 25, 2026. This is substantive adversarial review, not human verification, formal verification, or a novelty certificate.

Reviewed research snapshot: `ea482f54edae4775621bc69c1fb7359291f31ddd`, as verified by the parent reviewer against the live repository. The local checkout's Git HEAD/index is stale; the parent independently confirmed that the working mathematical files match that commit. No repository file was changed and nothing was published.

**Verdict:** I found no mathematical gap or counterexample to the stated fixed-core affine proposition. Steps A–D are valid under their stated hypotheses. The exact quarter-arc argument in FAST_CLUSTER Sections 2–5 is also valid. The finite evidence is consistent with the claims; it is not the reason the infinite implication holds. Several stronger consequences and one elementary alternate proof deserve consideration. The scope remains asymptotic with fixed coefficients, and novelty remains unresolved.

## Findings by severity

| Severity | Location | Finding |
|---|---|---|
| Critical / major | REVIEW_AFFINE_FAMILY Section 2; FAST_CLUSTER Sections 3–4, 8–9 | None found after checking the main implication, endpoints, negative offsets, quantifiers, and distinctness. |
| Minor evidence limitation | REVIEW_AFFINE_FAMILY Section 3; analyze_affine_family `main` | The archived profiles use nonnegative offsets and minimum winding 1. The note explicitly discloses the first limitation. The written proof does cover negative offsets, zero offsets, and minimum winding greater than 1. Four independent bounded profiles below check these cases successfully. |
| Exposition / useful simplification | REVIEW_AFFINE_FAMILY Step D, formula (3) | The component-distance condition is only needed to insist on the chosen interval J. Strict core safety already follows from the core-margin term. For a maximal strict core component, its eta term is dominated by the core-margin term. |
| Valuable unrecorded consequence | FAST_CLUSTER Section 6 scope sentence; REVIEW_AFFINE_FAMILY Section 1 | Reference changes give eventual strict loneliness for every runner in the fixed four-runner block. In the equal-winding two-block family, all eight references are eventually strictly lonely. This needs an explicit corollary with repeated absolute-speed handling; it is not an error in the narrower claim. |
| Valuable extension | REVIEW_AFFINE_FAMILY Steps A–D | The same argument works for balanced fixed-core/affine blocks at arbitrary even runner count, with an easier odd-count version for the selected reference. This is not arbitrary-speed coverage. |

## Detailed mathematical audit

### Core opening and strictness

Each nonzero integer core coordinate is uniformly distributed over its circle during a unit period in the elementary measure-preserving sense. Its unsafe set at threshold 1/8 has measure 1/4. Three such sets cannot cover the period. Removing all finitely many equality times leaves a positive-measure open set and hence a nonempty open interval J. There is no hidden genericity assumption here. In fact, three distinct core speeds are stronger than necessary: repeated absolute speeds or fewer than three constraints are harmless for this argument.

The chosen rational t0 can avoid the finite cancellation set because every nonempty open interval contains infinitely many rationals. At that rational t0, all phase boundaries are rational; positive clear measure contains a cell with nonzero width, so a rational x0 with strict inequalities exists. The finite endpoint set is precisely why positive measure can be upgraded to strict inequalities here. Equality-only phase sets are retained in the controls and are not used as strict auxiliary points.

### Fourier calculation

For the convention in the note, a direct calculation gives, when k=l*b_i with l nonzero,

\[
\widehat{1_{B_i(t)}}(k)=
 e^{2\pi i l a_i t}\frac{\sin(\pi l/4)}{\pi l}.
\]

For b_i not dividing k the coefficient is zero. At k=b_* the only contributors have b_i=b_*, and l=1, so the sign, the absence of an extra b_i factor, and the constant sqrt(2)/(2*pi) in Step B are all correct. This remains true if b_*>1.

The integral of the four indicators is exactly 1. If their union has full measure, the integer-valued multiplicity M is at least 1 almost everywhere and has integral 1, so M=1 almost everywhere. A nonzero Fourier coefficient rules this out. The Laurent polynomial P is not identically zero because P(0) equals its positive number of terms. Multiplying by a monomial handles every negative a_i. Its zeros on the unit circle, and therefore its zeros modulo one in t, are finite. No distinct-exponent assumption is needed for this nonvanishing argument, although equal minimum winding already gives distinct a_i under the proposition's pair-distinctness hypothesis.

FAST_CLUSTER formula (12) also checks out: with mean multiplicity 1, the integral of excess multiplicity equals the measure with multiplicity zero, and the L1 distance to 1 is twice that quantity. Consequently formula (14) is valid. A canceled lowest-frequency coefficient alone does not characterize tiling; the archived countercontrol correctly demonstrates this.

### Actual-time realization and distinctness

Nearest-integer rounding gives |t_q-t0|<=1/(2q), including the half-integer tie case. Because b_i is integer, b_i*m_q drops out exactly. The remaining error is |a_i|/(2q), not (b_i*q+|a_i|)/(2q). Negative offsets are fully handled by A=max|a_i|.

The speed conditions in formula (3) are sufficient:

- b_i*q+a_i >= q-A > M, so every extra speed is positive and above the core.
- For different b_i,b_j, |(b_i-b_j)q+(a_i-a_j)| >= q-2A > 0.
- Equal b_i have different a_i by hypothesis.

All bounds are strict, so Q=1+floor(maximum bound) is the correct sufficient integer cutoff, including an integral right-hand side. The case A=0 is harmless: its fast-drift term is zero, and distinct pairs then force distinct b_i. Continuity converts the strict witness into an open interval. Rational witnesses follow from the rational t0,x0 and integer q. No equidistribution assumption or changed starting phases enters the construction.

The explicit Section 3 example is correct: the stated t0,x0 give core margin 3/16, fast margin 115/512, eta=3/64, and dominant bound 1792/115, hence Q=16. The actual witness and minimum distance independently check exactly.

### Equal-winding geometry

FAST_CLUSTER's formula G(t)=sum max(g_j-1/4,0) is correct even when centers coincide: zero cyclic gaps account for repetitions. G=0 implies each gap is at most 1/4, and their sum 1 forces all four to equal 1/4. Since offset 0 is present, such a tiling implies 4*a_1*t is integer. The finite exceptional grid argument and rounded-time transfer therefore work. The scripted adjustment away from a grid midpoint cannot land on another grid point: it shifts by a positive amount no greater than half one grid spacing.

## Simpler or stronger formulations worth retaining

These are reviewer-derived consequences, not literature novelty claims. They should receive a separate check before expanding the public theorem statement.

### An elementary alternative to the Fourier step

At an exact tiling, the individual open blocked arcs have disjoint interiors and form a cyclic chain, with each right endpoint contacting the next left endpoint. The endpoints of an arc from coordinate i move with velocity -a_i/b_i as slow time varies.

If every a_i/b_i is equal to r, every B_i contains x=-r*t and the sets overlap in positive length, so a tiling is impossible. Otherwise, in a cyclic tiling there must be an adjacent contact joining arcs with different boundary velocities. On suitable lifts that contact has equation

\[
(j+\delta-a_i t)/b_i=(k-\delta-a_j t)/b_j+\ell,
\qquad\delta=1/8.
\]

Because a_i/b_i differs from a_j/b_j, this determines one rational t. Over t in [0,1], there are only finitely many relevant endpoint labels and lifts. Hence exact tilings can occur only at finitely many rational times. This gives the opening lemma directly and identifies a sharper fact about actual tiling times. The Fourier proof is already correct and is arguably cleaner to generalize quantitatively.

### Explicit convergence to the auxiliary optimum

Set

\[
L_U=\max_{(t,x)\in(\mathbb R/\mathbb Z)^2}
\min\bigl(\|c_jt\|,\|b_ix+a_it\|\bigr),
\qquad K=\max(M,A).
\]

Let L(q) be the actual maximum for the seven relative speeds. Since the actual orbit lies in U, L(q)<=L_U. Rounding an auxiliary maximizer exactly as in Step D gives the reverse estimate

\[
L_U-\frac{K}{2q}\le L(q)\le L_U.
\]

This is a direct finite-q estimate, not an appeal to a limiting theorem. It explains precisely what the strict auxiliary gap buys and why the zero-margin case needs a different argument. Periodicity handles a rounded time outside the chosen representative period. The eta term is unnecessary for this global formulation.

### Reference changes within the slow block; all references for equal winding

For a reference r in S={0,c1,c2,c3}, the fixed relative constraints are |s-r| for s in S minus r, and the fast coordinates are b_i*q+(a_i-r). There are at most three distinct fixed absolute constraints. The proof works unchanged with repetitions removed; alternatively pad to three fixed constraints, preserving the original threshold 1/8. Thus each of the four slow references has eventual strictness, and taking the maximum of their four finite cutoffs gives one cutoff for all four.

If all b_i=b, a reference b*q+a_r in the fast block sees three fixed offset differences |a_i-a_r| and four opposite-sign slow differences. After sign reversal these latter constraints are b*q+(a_r-s), s in S. Their offsets are distinct. The same argument applies. Taking the maximum of eight finite cutoffs proves eventual strict loneliness for all eight runners in the equal-winding two-block family. The times may differ between references. Repeated absolute fixed differences do not change n or the threshold.

An additional special case: if one fast b_i is unique among the fast slopes, that fast reference also has eventual strictness. At auxiliary t=0, the four slow runners give one repeated constraint |b_i*x|, while the other fast runners give at most three nonzero slope constraints |(b_j-b_i)x|. At most four blocked sets have total measure at most 1, and they all overlap around x=0, so a strict phase gap exists. Choose x in (0,1/2) in such a gap and use actual t=x/q; all offset errors tend to zero. In particular pairwise-distinct fast slopes give eventual strictness for all references. No conclusion here settles the remaining mixed multiplicity patterns (2+2, 3+1, 2+1+1) for every fast reference.

### Balanced-block extension beyond eight runners

For n=2m, m>=2, take m-1 fixed nonzero integer core speeds and m affine fast speeds with fixed positive integer b_i. At threshold 1/(2m), the core blocks measure at most (m-1)/m<1, while the fast blocked measures sum to 1. The same lowest-frequency argument has nonzero coefficient sin(pi/m)/pi and goes through unchanged. This gives eventual strictness for the selected reference. With two equal-winding blocks of m runners each, the reference-change argument gives eventual strictness for all 2m runners.

For n=2m+1, m>=1, take m fixed core speeds and m affine fast speeds. Both blocking sums are 2m/(2m+1)<1. A strict phase gap exists at every slow time without Fourier analysis, and rounding proves eventual strictness for the selected reference.

Do not automatically claim all-reference strictness for odd blocks of sizes m and m+1: a reference in the smaller block sees m+1 fast constraints, whose total blocked measure exceeds 1. Also exclude m=1 from the even strict theorem: two runners cannot exceed distance 1/2. These extensions keep the coefficients fixed while q tends to infinity and do not cover arbitrary configurations by choosing an arbitrary small q.

## Computational review and its limits

I read both analysis scripts fully and inspected their supporting boundary-certificate and interval-certificate routines. Every recorded source SHA-256 in both archived JSON files matches the current research files. The scripts distinguish direct interval intersection from independently structured boundary-cell reconstruction but share primitive rational-distance routines; this is useful internal crosschecking, not fully independent proof certification. I did not rerun their main functions because those overwrite repository evidence, and reproduction is not needed to assess the symbolic implication.

Independent reviewer code imports no repository code and is saved as `affine_checks.py`; its exact output is `affine_checks.json`, both beside this report. It verified:

- All 12 affine and all 20 fast-cluster archived rational witnesses, their exact minimum distances, and their positive-width strict interval certificates.
- The three mixed-winding phase controls, including clear lengths 0, 1/40, 1/8 and the six isolated tiling phases.
- Four additional fixed profiles at Q, Q+1, and 2Q: negative offsets with a tied minimum winding; A=0 with minimum winding 2; all-negative offsets; and mixed offsets. All 12 new witnesses passed exact distance and distinctness checks.

| Added profile, core | Four (b,a) pairs | t0 | x0 | Sufficient Q |
|---|---|---|---|---:|
| Negative tied minimum, (1,4,5) | (2,-9),(2,-4),(3,0),(5,7) | 21/64 | 215/256 | 31 |
| Zero offsets, (1,4,5) | (2,0),(3,0),(4,0),(5,0) | 21/64 | 19/160 | 14 |
| All negative, (1,4,5) | (1,-100),(2,-7),(3,-2),(4,-1) | 21/64 | 671/1536 | 227 |
| Mixed offsets, (2,3,5) | (2,-5),(2,-3),(3,4),(4,7) | 13/100 | 1503/1600 | 34 |

For example, the first added profile at q=31 has speeds (1,4,5,53,58,93,162), time 2519/7936, and minimum distance 1405/7936>1/8. This directly exercises the signed-offset case missing from the archive. These are bounded diagnostics, not evidence for the unbounded proposition independently of the proof.

I did not independently reconstruct all large positive-duration allowed unions, audit every imported analysis module, assess other candidate families, rerun the 25 checker tests, or search the full literature. Those scopes are separate from this mathematical review.

## Literature and package interpretation

I opened the primary source [Jain–Kravitz, Relative Lonely Runner spectra, arXiv:2411.12684v2, December 9, 2024](https://arxiv.org/html/2411.12684v2), reading the relevant introductory definitions, Theorem 1.1, the comparison with very fast runners, and the proof outline; I also inspected the statement of Proposition 2.6. Its two-dimensional-subtorus framework and finite phase-grid approximation are direct context for this work. The repository's ambient dimension seven, common-start orbit x=qt, and conversion strict loneliness>1/8 iff D<3/8 are correct. The mapping has rank two, and no coordinate is constant. The source's theorem does not by itself supply this note's elementary proof that the auxiliary U has a strict 1/8 opening. I have not established whether a prior result already implies the full restricted statement or the balanced-block corollary.

The useful next step is to present the sound core proposition with this explicit review scope, decide whether to append the elementary alternate proof or balanced-block/reference-change corollaries, and ask a human specialist to evaluate correctness and prior art. No upgrade to an established or novel result follows merely from this AI review.
