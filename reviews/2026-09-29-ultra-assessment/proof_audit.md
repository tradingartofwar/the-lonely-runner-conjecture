# Adversarial audit of the current proof spine

Date: 2026-09-29. Pinned repository head supplied by the coordinator: `7b0101376e00dbb71537d3a62e39ec75cee113cc`.

**Status:** mathematical review of proof candidates, materially AI-assisted. This is not independent human certification, a novelty determination, or a promotion of claim status. No mathematical program, tuple scan, phase scan, or frozen protocol was executed. Only this new report was written. The workspace is a connector-backed snapshot rather than a local Git checkout; the coordinator verified the branch pin.

## Verdict

I found **no fatal mathematical gap** in the four assigned notes, including their inherited short-kernel dependency. Their strongest advertised implications survive this scoped line-by-line audit. The direct and literature-assisted finite reductions are logically valid conditional on their stated ingredients; neither is an exhausted finite domain.

The strongest broadly reusable result is the mixed averaging argument for arbitrary positive periods and phases: a strict four-train quarter-duty chain has span less than `H=P+3(q+r+s)/4`, and its actual selected occurrence count is at most 23. The fixed-core six-constraint positivity argument is also complete as written once its explicit arithmetic cases are included. Its existence conclusion is weaker than an established lower-runner theorem; its potential value is its explicit construction.

The remaining research gap is substantial and precise: there is no proved theorem forcing a usable final-runner certificate for every core in the remaining fixed-family parameter region. More importantly, there is no reduction of arbitrary configurations to the distinguished core `{1,4,5}`. Closing this region would complete this particular selected-reference route, not the full conjecture.

## 1. Short-kernel and chain audit

Read `SHORT_KERNEL_BOUND_2026_09_28.md` in full and the preceding `EXPLICIT_CHAIN_BOUND_2026_09_28.md`.

The mixed expectation identity is valid. A four-point quarter-period average has an endpoint exception, but conditioning on the continuously distributed full-period variable kills that countable exception. Each train therefore contributes exactly `1/4` for every translate. The proof does not assume rationally related periods or silently average over an unavailable common period.

The density really is positive on the entire open support. Successively translating an interval of positivity by steps at most `P/4` creates overlaps, so no internal hole appears. This property, rather than nonnegativity alone, is essential.

For a chain union `(A,B)` of length at least `H`, an overlap point `y` permits a translate with `a` in `[A,B-H] intersect (y-H,y)`. This intersection is nonempty, including at equality. The kernel then sees a nonnegative multiplicity excess everywhere and a strictly positive excess on an open set, contradicting its zero mean. Endpoint contacts alone do not yield that excess, as required.

Whole-occurrence counting is sound: `h` appearances of the largest period imply span at least `(h-3/4)P`; the strict span bound and `H<=13P/4` give `h<=3`. This counts selected occurrences even if laps are skipped or one interval contains another.

The long-triple lemma is also sound. A triple chain with at least six occurrences has one largest label and two pair pieces of combined length at least five. One pair piece is `s,r,s`, forcing `r>3s`. The two `r` occurrences force `q+2s>3r`; these imply `q+r+s<11q/7`. With three `P` occurrences the global span instead forces `q+r+s>5P/3`, an incompatibility because `q<=P`. This gives the stated 23 bound without empirical fitting.

The conversion to 23 rounds / 253 scalar calls requires the stated joint-safety checks at round boundaries and a round visiting every label. It is not a 23-raw-call theorem or a bit-complexity bound. The note states this correctly.

The auxiliary factorial induction is valid: at duty `1/m`, the largest label has at most `m-1` appearances; widening the remaining intervals leftwards to duty `1/(m-1)` preserves right endpoints and all strict transitions. It is legitimate to apply the smaller-label occurrence bound afterward. The base `m=1` is not incorrectly subjected to the strict-span lemma.

**Critical limitation:** the kernel applies where the total blocked duty is one. Applying it to all seven constraints at threshold `1/8` would instead give mean `7/4`; the sign contradiction disappears. The larger-number corollary does not repair this mismatch. No such invalid transfer is made in the current note.

The finite calibrations do not test a chain close to 23 occurrences, but this is an evidence limitation, not a gap in the symbolic argument. The proof stands or falls on the lemmas above.

## 2. Core-window measure and three-speed reduction

Read `CORE_WINDOW_REDUCTION_2026_09_29.md`, plus its arithmetic and scope reports. I checked the following dependencies and endpoints.

* The complete `{1,4,5}` safe set consists of the stated three first-half intervals and their reflections. Their measure is `3/8`.
* The periodic primitive of a quarter-duty indicator minus its mean has oscillation `3/(16v)`. Summing its one-interval bound over six components gives `Q(v)<=3/32+9/(8v)`. At `v>=16`, the bound is `21/128<1/6`.
* The twelve remaining values have explicit scaled intersections in the scope report. These cover all admissible smaller positive integers; there is no missing speed among them. Together they justify `Q(v)<=1/6`.
* The five-core lower bound `3/8-Q(a)-Q(b)>=1/24` is a union bound. It does not require independence or use an unknown five-core positivity conclusion circularly.
* The positive-component count `a+b+6` is conservative and sufficient. A single deleted open interval can create at most one extra positive component. The blocker pieces adjoining 0 and 1 do not create extra splits in this core, which is separated from those endpoints.
* The two- and three-label strict-chain budgets are independent elementary arguments. A closed safe interval of at least the budget cannot be completely covered by the open blockers. Equality therefore gives a point, although not necessarily positive duration.

The peeling argument for `b>=48` has no missing small-`a` regime: admissible `a<=10` are exactly `2,3,6,7,8,9,10`; `11<=a<=21` is covered by clipping; larger `a` is covered by `H`. The conclusion `c>=18(a+b+6)` and then `c>=1566` follows without scanning pairs or triples.

I also checked the separate residual-gcd argument. The grid-hitting proof handles `g=7,8,9,10` explicitly and `g>=11` by interval width. In the `g=9` case, three speed-1 blocked grid points force a shared middle point of all three blockers. The common-start excess identity on one residual period is valid, and integration over the `g` translates gives the asserted positive-measure transfer. This result does not depend on the 23-move theorem.

## 3. Direct six-core positivity and finite final-speed bounds

Read `SIX_CORE_WINDOW_2026_09_29.md`, its arithmetic and structure reports, and the displayed prior four-core windows.

The strict two-train lemma correctly switches to closed residual blockers. A positive four-core component has all four constraints strictly safe in its interior: a threshold crossing for any nonzero speed cannot lie in that interior. Failure of a closed cover leaves a relatively open set and hence an interior interval. Thus the step proves positive duration rather than merely an equality witness.

The reduction to eight `a` values and 36 pairs checks out. In particular, the full-lap clipping threshold is `a>=19`, since `3/(4a)<=3/64-1/(8a)` exactly when `a>=56/3`. For each exceptional row I checked the last admitted and first excluded `b` using the monotone budget `1/(4b)+1/(2(b+1))`. Rearranging failure gives exactly `c<=floor(2b/(4bw_a-1))`; its largest value is 62 at `(a,b)=(6,7)`.

The arithmetic closure is not circular with the 27-triple computation. The modulo-6 and modulo-7 strict anchors, the two directed eighth anchors, and the three-direction seventh selector are direct certificates. In the seventh selector, two nonzero residual residues veto at most two of the three choices, while fixed speeds `1,4,5` veto none. The displacement interval keeps every noncolliding phase below `7/8` and puts the colliding speed above `1/8`. The nine-pair pruning, shared window, and two `c=16` certificates then complete the remaining hand casework. The 27-triple computation is a separate, conservative check, not an unproved extrapolation used to supply the universal step.

The endpoint quantum is sound. Distinct controlling speeds `v,w` give a positive endpoint difference at least `1/(8*lcm(v,w))>=1/(8Mc)`, where `M=max(5,b)`. Same-speed endpoints also have adequate separation. Since `c>=6`, it really is the largest core speed even when `a=2,b=3`. Speed 1 excludes artificial domain endpoints 0 and 1. An open final blocker of width at most the closed component's width cannot cover that component, so `d>=2Mc` includes equality.

Consequently the direct residual box `a<=34,b<=47,c<=1565,d<=147109` follows. The smaller box follows from the separately credited lower-runner inputs: a five-core margin gives width `1/(12M)`; a six-core margin gives width `1/(28c)`; the two-train component refinement gives `c>=6M`; and the split at `c=27M/7` gives `d>=27M`. Thus `c<=281,d<=1268` is correct when `M<=47`.

There is no hidden use of eight-runner existence in either reduction. Nor is there an exhaustive check of either box. The smaller box deliberately imports six- and seven-total-runner theorems, so it should never be described as a wholly elementary reconstruction.

## 4. Last-runner compatibility and endpoint audit

Read `LAST_RUNNER_COMPATIBILITY_2026_09_29.md` in full.

The two-window certificate is valid at its exact endpoints. Strict coverage by one lap requires `dD<1/4`; coverage by different laps requires `dG>3/4`; either also requires `dw<1/4`. Thus weak hypotheses `G<=3w` and `d>=1/(4D)` suffice for a safe point. Zero duration uses closed blockers instead; the proof then needs both strict hypotheses shown in the note to rule it out. This is correctly separated from existence.

The supplied narrow core has `D=5/224`, `G=1/96`, and larger width `3/448`; the arithmetic yields threshold `56/5`. This is a strong explicit all-phase, real-speed certificate for that supplied core. It is not a universal statement about positive six-core safe sets.

The midpoint maximum formula, strict lap band, and the distinction `F subset P subset Z` are correct. The reduced denominator of a core threshold retains a factor of 8 because its numerator is odd. Endpoint residue conditions alone do not suffice; the additional small-width condition prevents endpoints lying in different blocking laps. The note includes that condition.

Reflection reduction to phases 0 and 1/2 is valid for a full integer-period core image under integer `d`, including its separate closed-arc version for zero duration. It would fail as an argument for arbitrary clipped windows or noninteger first-period images; the note excludes those extensions explicitly. The final paragraph's noninteger-speed global escape is also valid: for `beta=||d||>0`, its chosen integer `m` has `1/4<m beta<=1/2`, and the integer core repeats at `t0+m`.

I independently checked the exceptional image calculations using the four displayed tight-core components: at `d=13` their images join to `[-3/32,3/32]`, and at `d=18` their union is `[3/8,5/8]`. Their claimed zero-duration phase sets follow. No phase scan is needed for those deductions.

## 5. A decisive limitation of the proposed next milestone

The tight core at `d=13`, phase zero, has every positive closed component strictly blocked. Only the four isolated core points survive. Therefore:

> No universal theorem asserting that some collection of positive core windows has incompatible final blocking laps can hold, even if the collection size is unbounded.

This is stronger than the failure of a particular pair or width criterion. The full positive-component set is already compatibly covered in the existing example. The next theorem must have a genuine isolated-point alternative, not only mention that equality will be handled later.

Also, arbitrary phase robustness is a stronger goal than common-start existence. The fact that three inherited cores are phase-robust is not evidence that the full fixed family is. A future proof should state whether it seeks phase zero only or every phase before choosing its certificate language.

## 6. A concrete falsifiable next statement

An economical target is **sparse endpoint coverage below the width cutoff**, with the cutoff included explicitly to avoid the already proved finite-rational-menu obstruction.

For an admissible six-core `C`, let `E(C)` be all maximal safe-component endpoints, including isolated points, and let `w(C)>0` be its widest component. Ask whether there is an absolute constant `K`, independent of `a,b,c`, such that:

> For every admissible `C={1,4,5,a,b,c}`, one can select `E_*(C) subset E(C)` with `|E_*(C)|<=K` so that every integer `d>c` with `d<1/(4w(C))` satisfies `||dt||>=1/8` for at least one `t` in `E_*(C)`.

This is a proposed research statement, not an established deduction. It includes isolated points and permits the endpoint menu to depend on the whole core. Above the cutoff, the width theorem supplies the witness. Unlike an unrestricted fixed rational menu, it does not claim to cover arbitrarily large denominator-multiple speeds with those same endpoints. A common multiple of all core endpoint denominators is automatically outside this small-speed regime because the width is a positive multiple of the reciprocal common denominator.

The hypothesis requires a declared `K` before empirical testing. The quickest useful falsifier for any proposed small `K` is an exact set-cover obstruction on an already archived core: each admissible integer `d` below the width cutoff must be covered by at least one selected endpoint's safe residue class. One can inspect the existing last-runner records and component lists first, then request a narrowly declared diagnostic only if necessary. A failed small `K` would disprove that compression claim, not loneliness. No such diagnostic was run here, and no particular `K` is asserted plausible on the current evidence.

The immediate recommendation is to formulate and prove a structural endpoint-selection theorem, or establish a lower bound showing that sparse endpoint menus cannot suffice. That is more informative than another successful reconstruction of the same three final-runner examples. It also makes the isolated-point branch a first-class part of the proposed theorem.

## 7. Literature dependency check and review boundary

I retrieved primary sources on 2026-09-29 and inspected only the following relevant portions:

* Bohman–Holzman–Kleitman, *Six Lonely Runners* (2001), printed page 3: Theorem 2 and Lemma 4. The theorem gives the required five-frequency `1/6` witness; the interval-block argument is directly relevant to the two-train refinement. [Primary PDF](https://holzman.technion.ac.il/files/2012/09/runners.pdf).
* Barajas–Serra, *The lonely runner with seven runners* (2008), abstract and introduction, printed pages 1–2: the six-positive-integer formulation and stated seven-total-runner result. I did not re-audit its full proof. [Published PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v15i1r48/pdf/).
* Kravitz, *Barely lonely runners and very lonely runners*, Section 6.1, Proposition 6.1 and its proof on printed page 13. I inspected the rendered page because text extraction renders several weak inequalities incorrectly. The displayed proposition and proof retain the equality needed for `d>=7c`. [Primary PDF](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf).

The repository's newer frontier-status claims and eight-runner literature proof were outside this proof-spine review. I did not verify frozen output hashes, re-run either implementation, or inspect every historical proof package. Internal independent implementations and this audit support confidence in the stated finite arithmetic; they do not substitute for outside mathematical review or a novelty investigation.

## Addendum: static challenge of the relative/module Fourier proposal

At the coordinator's request, I audited Sections 2–4 of `duality.md`, taking its stated autocorrelation coefficient identities as analytic inputs. **No defect found** in the relative or full-module extraction, or in the one-cross-relation positive-Haar argument. No mathematical computation was executed.

The extraction correctly subtracts the entire retained module's Fourier contribution, not just its zero vector. A positive retained contribution `A_Lambda` forces outside odd-sum weight at least `A_Lambda` if the actual-orbit integral is zero. Its global second moment therefore yields the asserted norm bound by weighted averaging. Absolute convergence justifies the Fourier integration. The original-coordinate odd-sum condition need not descend to the quotient by the core relations; the argument does not require it to descend.

The saturation/connectedness distinction is handled correctly. `L(v)` is saturated in `Z^k`; hence saturation relative to `L(v)` agrees with ambient saturation for its subgroups. For saturated `Lambda`, its annihilator is a connected subtorus, and an integer vector outside `Lambda` is outside its real span. Thus the extracted outside relation really increases rank after saturation. These rank conclusions would not follow merely from a nonsaturated generating list.

For the distinguished core, the quotient map on characters is explicitly

`(m_1,m_4,m_5,r_a,r_b,r_c,r_d) -> (m_1+4m_4+5m_5,r_a,r_b,r_c,r_d)`.

Its kernel is the exact core relation module and it is onto `Z^5`. Consequently one independent saturated extension is represented by a primitive vector `(q,r)`. The condition that it annihilate `(1,a,b,c,d)` forces `r!=0`. If `||r||_1>=2`, the image of the open residual cube is an open real interval of length at least `3/2`, so it meets every required congruence class. If `||r||_1=1`, the equation fixes the affected residual phase to its actual positive integer-speed phase, and the existing four-core measure bound applies. In this case `q=0` would force that residual speed to be zero and is inadmissible. Thus a zero-coordinate exception does not invalidate the lemma.

More generally, no coordinate can be identically zero on this connected relaxed torus: that would put its unit character in `Lambda subset L(v)`, contradicting positivity of the corresponding speed. This observation alone does not establish simultaneous safety; the open-interval argument above is what establishes the one-relation result. A strict point supplies an open relative neighborhood and hence positive Haar mass.

For P2, projecting the rank-two module to its four residual coefficients preserves rank: a nonzero relation with residual coefficients zero would contradict its annihilation of `(1,a,b,c,d)`. Thus the asserted rank-two matrix `R` is justified. The closed zonotope membership and support-function criterion are correct. The open cube is required for strict safety, and neither area nor individual coordinate surjectivity can replace a simultaneous feasibility argument. At this stage I treated P2 as OPEN; **that assessment is superseded by the positive-collision correction below**. The earlier observation about positive first-module means over a finite bounded family supplied only a qualitative next coefficient bound, not a useful numerical estimate.

## Final integrated-note check

I statically reviewed an initial draft of `notes/ULTRA_ASSESSMENT_2026_09_29.md` after the preceding addendum. Its proof-distance assessment is candid, and its one-cross/P2 discussion correctly distinguishes relaxed phase feasibility from the actual runner trajectory. The connected-window coefficient `(n-2)/2` and hull speed cutoff `2/(nD)` are correct; the stated strict version follows by switching to closed blockers. My initial acceptance of P2 as the next analytical target is superseded by the late correction below. The additive-core lift remains a possible later scalability gate.

I recommended two explicit domain clarifications for readability: say `n>=3` and disjoint ordered positive windows in the general connected-window lemma; and repeat that P2 quantifies over saturated rank-two subgroups of `Z^5` annihilating some admissible `(1,a,b,c,d)` of distinct positive integers. These assumptions are already supplied by the intended context and the linked detailed report, but stating them inline prevents an overbroad reading. This final check introduced no new mathematical research or execution.

## Late correction: relaxed P2 existence follows from lower-runner theory

The arithmetic reviewer supplied a decisive correction after the initial integrated-note check. I independently audited the following argument and found it valid. **P2's relaxed strict-existence conclusion is supplied by known lower-runner results and should not remain the recommended open target.** This is a correction to my earlier assessment, not a proof of strict safety on the actual seven-speed trajectory.

Let `Lambda` be the retained saturated relation module, let `K=Lambda^perp` in `R^k`, and suppose `K` has dimension `d>=2` and contains the positive actual speed vector. The rational polyhedron

`P={w in K : w_i>=1 for all i}`

is nonempty after scaling that positive vector. Minimize `sum_i w_i`. A nonempty sublevel is compact, so the minimum is attained and its compact minimizing face has a vertex, which is also a vertex of `P`. At such a vertex the active coordinate functionals span `K*`: otherwise a nonzero direction in `K` vanishing on all active coordinates admits sufficiently small feasible perturbations of both signs, contradicting extremality. At least `d` coordinates therefore equal 1. Rationality of the defining linear constraints gives a rational vertex.

This produces a positive rational vector in `K` with at most `k-d+1` distinct coordinate values. Clear denominators and merge equal speeds. A known Lonely Runner theorem for those at most `k-d+1` moving frequencies gives a point of the relaxed torus at separation at least

`1/(k-d+2)>1/(k+1)`.

All repeated coordinates are safe together, and every retained relation annihilates the constructed vector, so the point is indeed in `H_Lambda`. The supplied stronger margin yields strict safety at the target threshold and hence positive Haar mean. This conclusion concerns the relaxed torus, not the original vector's orbit.

For P2, the two exact core relations and two additional independent relations leave `k=7,d=3`; the construction needs at most five distinct moving frequencies. The established six-total-runner theorem therefore gives margin at least `1/6`, strictly above `1/8`. Even the next relaxed rank, with `d=2`, is handled by the seven-total-runner theorem at margin `1/7`. The actual orbit is the remaining dimension-one stage, where this collision argument offers no reduction in the number of distinct speeds.

The recommendation must therefore shift from proving bare P2 relaxed existence to a genuinely additional quantitative, constructive, or actual-orbit implication. Rank growth and positive relaxed means by themselves still do not transfer the safe phase point to the original trajectory. No mathematical executable computation was used in this correction.
