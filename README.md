# The Lonely Runner Conjecture

An open, curiosity-led investigation of the Lonely Runner Conjecture using exact mathematics, reproducible computation, visualization, and human–AI collaboration.

This project began as an exploration by Vance and an AI partner. It is being prepared as a first open inquiry in the **EXTRA ORDINARY** independent-science model: open to unusual questions and contributors, strict about evidence, and explicit about what is known versus what is only suggested.

A breakthrough is an aspiration, not an expectation or a claimed result.

## The question

Start `n` runners together on a circular track of circumference 1, with distinct constant velocities. Does each runner eventually have a moment when every other runner is at least `1/n` of the track away? The moments can differ between runners.

Our current guiding question is:

> **What prevents the runners from collectively blocking every possible moment?**

## Research discipline

This repository deliberately separates different levels of evidence. See [CLAIM_STATUS.md](CLAIM_STATUS.md).

- **KNOWN** — established result supported by cited literature.
- **REPRODUCED** — an established or stated result independently reproduced here within a documented scope.
- **OBSERVED** — exact or computational pattern in a stated finite scope.
- **HYPOTHESIS** — proposed explanation or extension that can fail.
- **OPEN** — unresolved question.
- **DISPROVEN** — a proposed statement for which a counterexample or contradiction has been established.

No animation, sampled plot, optimizer output, large finite search, or language-model agreement is treated as a proof.

## Start here

| File | Purpose |
| --- | --- |
| [HANDOFF.md](HANDOFF.md) | Detailed current research state, evidence pointers, and next questions |
| [Broader inquiries](notes/inquiries/README.md) | Reflections, thought experiments, and possible connections to other problems |
| [RESEARCH_PLAN.md](RESEARCH_PLAN.md) | Strategy and research method |
| [CC representation rules](notes/CC_REPRESENTATION_RULES.md) | Supported questions, information loss, recovery and framework adaptation |
| [CLAIM_STATUS.md](CLAIM_STATUS.md) | Evidence/status vocabulary used throughout the project |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to investigate, challenge, reproduce, and submit work |
| [notes/MATHEMATICAL_BASELINE.md](notes/MATHEMATICAL_BASELINE.md) | Definitions, exact checks, normalization, and test fixtures |
| [notes/SOURCES.md](notes/SOURCES.md) | Dated literature starting points and verification limits |
| [AGENTS.md](AGENTS.md) | Instructions for AI collaborators |

## Current state — September 29, 2026 UTC

**Visual companion:** [From cap to clock](visuals/compatibility-calculus/README.md)
is the first interactive CC slice, backed by the exact fixed-cell certificates.
Open its self-contained `presentation.html` to follow a B-ray cap section to
an integer orbit contact and a physical runner witness. The data and browser
checks pass; the full deck and research explorer remain in progress.

**Language name — September 29, 2026:** The language we are developing is **Compatibility Calculus (CC)**. Use this name for current discussion and new work. Historical LTCM terminology and filenames remain in the preserved research record.

**CC working rules — September 29, 2026:** [Representation and transfer rules](notes/CC_REPRESENTATION_RULES.md) now require an explicit supported question and next operation, retained/omitted information, a richer source and recovery map, and evidence plus a failure test. The note supplies records for full cells, B-ray caps and A-ray conditional intervals. Existing frameworks, including other authors' LTCMs, may be reused, modified, combined or replaced whenever useful; preserve attribution, the exact changes and the applicability of inherited results. Apply the same scrutiny to CC itself. These rules are also in AGENTS.md. The bounded one-witness selection target now has the two-segment proof candidate below; its compact representation record is included in the working rules.

**Latest — two segments cover the positive two-parameter family.** [CC_TWO_PARAMETER_WITNESS_2026_09_29.md](notes/CC_TWO_PARAMETER_WITNESS_2026_09_29.md) gives a complete proof candidate for one stationary-reference 1/8-safe time for every positive integer p!=q in V(p,q)=(p,q,p+q,2p+q,3p+q,3p+2q,5p+2q). With d=gcd(p,q), P=p/d, Q=q/d, P3 covers Q+2P>=8 and all but (1,2),(1,4) in the complete primitive complement; P1 covers those two, retaining the equality endpoint.

The actual-orbit condition is Qx-Py in Z, equivalently qx-py in dZ. For rP+sQ=1, recover tau={rx+sy} and t=tau/d, with the explicit physical lap map in the note. An ambient-safe point with raw integer orbit value outside dZ exposes the loss from omitting normalization. Neither coordinate nor the stored fold supplies the general physical clock. The cost is at most two segment tests plus gcd/Bezout arithmetic, whose iteration count is not constant.

Three separately tasked AI reviewers found no result-level defect. All four exact outputs reproduce byte-for-byte; three implementations agree on 18 declared pairs (17 distinct-speed configurations and one repeated-speed auxiliary), including physical phases/laps and reflection. The independent physical check also recovers all 18 times through a coordinate congruence. The 56 endpoint inequalities and complete eight-pair primitive triangle support the written infinite argument; no broad parameter scan or optimizer was run.

Status remains HYPOTHESIS / internally reviewed complete proof candidate. The selected minimum is exactly 1/8; this does not settle optimum values, all witnesses, other reference runners or general LRC. The frozen A/B discovery and visual packages remain unchanged. **Next proposed:** compare this precise two-parameter family and elementary certificate against existing literature, keeping novelty OPEN and the selected-reference scope explicit. External mathematical review remains open.

### Prior B-ray discovery transfer — preserved

**Latest — frozen discovery transfers to B; review finds a one-segment certificate.** [CC_B_RAY_TRANSFER_2026_09_29.md](notes/CC_B_RAY_TRANSFER_2026_09_29.md) records the unchanged rule with an explicit coordinate adapter: u=y, v=x, g=qu-v=-H, t=u, physical laps m+a*g, and original fold v<=1/2. The same 27 candidates yield a cutoff of 4: P1 covers q>=3 and P3 handles q=2 at t=9/40. No ranking or exception rule was retuned. Three separately tasked AI reviewers found no result-level defect; this remains an internally reviewed proof candidate, not external certification or new physical family coverage.

The separate discovery implementation matches all 27 candidates, 54 prefix entries and 24 recovered controls. Direct selected/reflected checks cover only archived q=2,...,25, with 56 physical polynomial inequalities on unbounded residue domains. Wrong-clock recovery at q=2 produces distance 1/10<1/8; wrong laps, sign and fold also have preserved counterchecks. Safe geometry alone is insufficient unless its physical map stays attached.

After the frozen comparison, a reviewer noticed P3 already covers both prefix inputs as well as every q>=4. Its single-segment formula is g=floor((q+3)/8), t=(16g+9)/(8(2q+1)), for every q>=2. A separate, explicitly post-protocol supplement checks this simplification without altering the frozen two-segment run. All selected separations remain exactly 1/8; optimum values, all maximizing times and the complete safe set are outside this carrier's scope.

**Next proposed:** derive the actual-orbit and physical recovery map for a general primitive (p,q) substitution in the same seven-form model, then determine which directions these segments cover. Do not transfer t=x or t=y when both parameters vary. This extension has not been performed; no wider physical scan, new reference, external contact, main merge or unattended work was run.

### Prior A-ray discovery — preserved

**Latest — parent-only discovery recovers the two-segment certificate.** [CC_SEGMENT_DISCOVERY_2026_09_29.md](notes/CC_SEGMENT_DISCOVERY_2026_09_29.md) records a fixed procedure using only six-form parent geometry and the seventh band. The 24 floor edges yield 27 labelled clipping records. A projected-width cutoff selects P3 for every q>=6; it also handles q=3,5. One greedy addition, P1, fills q=2,4. Online selection still uses at most two rounding/tests. This is the same pair in a discovery-selected order, not new family coverage.

The useful reduction is conditional and exact: with a nonvertical safe segment, one can cover an unbounded q tail and decide coverage by the full candidate list on a finite prefix. Here all 108 candidate/prefix entries pass reconstruction. A separate two-dimensional halfspace calculation recovers every candidate, tail cutoff and choice. The archived q=2,...,25 physical controls and reflections pass; no optimizer or wider scan was run. Removing endpoints loses every candidate witness at q=4. Both programs and the review are by the same coordinator; independent review remains open.

The prior two-segment proof was audited without finding a result-level defect, and both old checker outputs reproduce exactly. The procedure was designed with that example already known, so it is a development result, not a blind or held-out test. CC now retains discovery inputs, tail/prefix coverage, choice provenance and preprocessing cost in addition to the compact witness model. Historical packages are unchanged.

**Next proposed:** transfer the frozen rule to the already studied B ray, explicitly translating its actual orbit x-qy and physical clock t=y, and reuse archived controls. This transfer has not been run. No new family/reference, external contact, main merge or unattended work occurred in this step.

### Prior two-segment derivation — preserved

**Latest — two parent segments give a bounded A-ray witness selector.** [CC_BOUNDED_SELECTOR_2026_09_29.md](notes/CC_BOUNDED_SELECTOR_2026_09_29.md) supplies a self-contained proof candidate selecting one physical 1/8-safe time for every integer q>=2 in A_q=V(1,q), with the stationary reference fixed. One edge of parent P1 works for all q except 5; an edge of P3 handles q=5 at t=25/56. At most two integer roundings and closed interval tests suffice. The q=4 equality witness t=1/8 and q=6 endpoint t=5/24 survive. Every selected separation is exactly 1/8; optimality and complete witness enumeration are outside this selector's claim.

The proof uses seven affine phase bands on the two parent edges and the actual-orbit relation qx-y in Z. Interval width covers all q>=9; seven small cases and the fallback complete the argument. Exact checks certify 56 endpoint inequalities and eight unbounded residue domains; a separately structured physical polynomial check certifies 112 band inequalities. Only the archived q=2,...,25 receive direct physical checks, including reflection (336 exact distances). The known seven-form optimum is comparison data, not a premise. Both programs are coordinator-authored, not independent review or formal verification.

The information-loss checkpoint supports a smaller CC representation for this specific output: two compatible segments with rounding and recovery. It deliberately omits other safe points, optimum values and all-maximizer data. The richer atlas and earlier proof/review packages remain unchanged. Standard affine and integer-interval methods suffice; no new language or novelty claim is needed.

**Next proposed:** review this small certificate, then investigate how a sufficient segment collection can be discovered from parent data. The supplied-segment lemma does not force suitable segments in another family. No wider scan, new reference, external contact, main merge or unattended work was performed.

### Prior six-to-seven transfer — preserved

**Latest — CC six-to-seven transfer exposes consequential information loss.** [CC_SIX_SEVEN_TRANSFER_2026_09_29.md](notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md) completes the same-threshold parent-child atlas for the original A ray V(1,q). Eight six-form tetrahedra (32 vertices, 48 edges) become the existing ten seven-form cells (33 vertices, 45 edges), including all three singletons. Of the child edges, nine are new cuts inside old parent faces. Exact clipping and a separate 34-plane reconstruction agree; all children match the frozen certificate.

Only q=3,4,10 and their six-form prefixes were physically checked. Both exact physical methods reproduce every optimum and maximizer. All old six-coordinate global maximizing times fail final 1/8 safety in these controls. At q=4, adding speed 13 removes all four positive safe intervals while preserving four isolated witnesses. At q=10, final maximizers 17/35 and 18/35 lie inside old parent faces and are missed by simply retaining points on old edges or each parent slice's old optimum. This does not refute their sufficiency for selecting one different optimizer.

Separate orbit and seventh-phase ranges also give a false positive in a declared q=4 parent. The exact transfer instead retains the seventh-phase interval conditional on the same integer orbit value h=qx-y. A closed band intersection plus the inverse coordinate map recovers physical time and laps, including equality. The distinction between one witness, every maximizer and the complete safe set is now supported by explicit counterexamples. Status remains exact bounded reproduction plus a transfer proof candidate; no novelty or general forcing theorem is claimed.

**Next proposed:** derive a bounded selection certificate from the parent conditional intervals, including support changes and integer rounding, without using the already known seven-form spectrum as the proof. Earlier proof/review packages remain unchanged. This was a coordinator continuation, not a new team review; no wider q scan, other reference runner, external contact, main merge or unattended work was performed.

### Prior other-ray adversarial review — preserved

**Latest — CC other-ray adversarial review completed.** [CC_OTHER_RAY_REVIEW_2026_09_29.md](notes/CC_OTHER_RAY_REVIEW_2026_09_29.md) records five separately tasked AI reviews of the completed B_q=V(q,1) candidate, with its first two coordinates permuted. No result-level defect was found; all four value branches and the exactly-two-maximizer conclusion remain unchanged. Status is HYPOTHESIS / internally reviewed complete proof candidate, with independent mathematical assessment and novelty still open.

Fresh exact halfspace clipping reproduces all 10 cells, 33 vertices, 45 edges and 3 singleton cells. A fresh arithmetic checker confirms all 63 unbounded global comparisons, including 60 strict nonwinners, plus symbolic witness/lap recovery. A different physical-time optimizer recovers every maximum and all 48 maximizing-time occurrences for q=2,...,25; closed-band intersection agrees. Six large inputs q=100002,...,100007 receive witness-only checks. The coordinator reproduced all three outputs exactly.

Two quantifier clarifications distinguish slice vertices from arbitrary high points, and global optimizers from local slice maxima. Exact counterexamples to the overbroad readings are preserved. A simpler cap formulation projects each triangular section through H=x-qy to an interval: 14 extremal directions suffice for this B-ray upper bound. Full cells and equality cases remain stored; the smaller representation does not cover the original ray's tight q=4 case.

**Next proposed:** a same-threshold (z>=1/8) parent-child comparison of the first six forms with the appended seventh constraint 5x+2y, retaining the A-ray orbit qx-y in Z, lap labels and isolated equality witnesses. Begin with archived controls, including q=4, and test what parent information is sufficient to recover the children. This investigation was not executed in the review. The original proof packages remain frozen; no main merge, outside contact, novelty sweep or unattended work was performed.

### Prior other-ray upper-bound derivation — preserved

**Latest — matching upper bound completes the other-ray proof candidate.** [LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md](notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md) closes the open upper-bound step for B_q=V(q,1), with its first two coordinates permuted. The four-row mod-6 spectrum and physical witness formulas now have a complete argument for every integer q>=2, conditional on the exact fixed-cell lemma. Status remains HYPOTHESIS / complete proof candidate, awaiting independent review; no novelty claim.

The corrected actual-orbit equation x-qy in Z selects peak B's (-1,4) edge in residue 0, C's (-3,5) edge in residue 2, and F's (-1,2) edge in residue 5. Their minimum losses from 1/6 are 1/[6(4q+1)], 1/[6(5q+3)], and 1/[6(2q+1)]. Residues 1,3,4 reach an ambient peak. All competing edges have strictly greater loss in the nonconstant branches; exactly two maximizing times survive in every case, t(q) and 1-t(q).

A fresh exact 48-plane reconstruction matches all ten cells, 33 vertices and 45 edges. The audit certifies 63 global upper comparisons on unbounded residue domains, the explanatory loss table, and symbolic witness transfer. The fixed-cell selector agrees with all 149 previously frozen physical maxima and full maximizer sets for q=2,...,150. No new physical q values or reference runners were added. The original V(1,q) proof and Ultra review, and the earlier recovery's historical files, remain unchanged.

Next: independent adversarial review of this completed other-ray argument, particularly folded-coordinate transfer, slice-vertex completeness and the two-maximizer conclusion. No new team review, external contact, main merge, or recurring work has been performed.

### Prior continuation recovery — preserved

**Latest — continuation recovered; two parameter rays separated.** The unsaved mod-6 rule concerns B_q=(1,q,q+1,2q+1,3q+1,3q+2,5q+2), which is V(q,1) after permutation. It was incorrectly called the p=1 ray in the continuation. The original A_q=V(1,q) spectrum and its Ultra review were already saved and already contain a matching upper-bound candidate. Their claims remain unchanged.

[The recovery note](notes/LTCM_OTHER_RAY_RECOVERY_2026_09_29.md) preserves the newer formulas, contact pairs, physical laps, and symbolic lower-bound certificates. A fresh exact reproduction matches all 149 optima for q=2,...,150, with 42 polynomial phase identities and 84 safe-band inequalities on whole residue domains. These checks apply to B_q; its universal upper bound remains OPEN and has not received the original ray's Ultra review. Small controls q=2,4 confirm the two rays have different optima.

Resume with these scopes explicit: the original ray's proposed next question is six-to-seven-coordinate transfer; the newer ray's unfinished task is a matching upper bound. No new upper-bound derivation or broader investigation was performed as part of preservation.

### Prior Ultra spectrum review — preserved

The [Ultra spectrum review](notes/LTCM_ULTRA_REVIEW_2026_09_29.md) found no result-level defect in the five-branch exact spectrum candidate. Six separately tasked AI reviewers reconstructed the ten-cell geometry, checked all 84 universal upper-bound comparisons, proved selector completeness, and recovered all 24 small-q maxima with every maximizing time using a fresh physical algorithm. Six large witness checks cover every residue; q=4 retains exactly four isolated safe times.

The review clarifies that the selector finds an optimum and one witness within 33+45 candidate checks, not every optimizer or constant bit-time. Cordella's September 8, 2026 preprint completes the first-six-coordinate model and is now credited alongside published Jain–Kravitz. The appended seventh-coordinate formula's novelty remains unresolved. Status remains an internally reviewed proof candidate, not external certification or a general Lonely Runner proof.

Next proposed, not executed: isolate how the appended seventh constraint changes the known six-coordinate model and seek a transferable rule. Hourly remains paused.

### Prior spectrum candidate — preserved

The [LTCM spectrum test](notes/LTCM_EXACT_SPECTRUM_2026_09_29.md) gives a complete proof candidate for the exact selected-reference maximum of (1,q,q+1,q+2,q+3,2q+3,2q+5), every integer q>=2. A five-branch rule supplies both the optimum and an attaining time. q4 is the only tight1/8 case; every other member has maximum>=1/7.

A fixed ten-cell geometry and the actual-orbit condition qx-y in Z replace growing lap enumeration. Separate exact constructions recover33 vertices;84 symbolic comparisons support the universal upper bound;24 declared small-q maxima and two large witness checks agree. This is an internally checked candidate with a finite polyhedral certificate, not independent human review or established novelty. The existing relative-spectrum and polyhedral frameworks are credited.

Next: independent proof and prior-art review before extending the parameter family. Hourly remains paused.

### Prior Ultra assessment — preserved

The [Ultra assessment](notes/ULTRA_ASSESSMENT_2026_09_29.md) found no fatal defect in the assigned proof spine, but identified the missing general step: our supplied-window and arithmetic certificates do not yet force witnesses for arbitrary configurations. The finite fixed-family remainder is unchanged and unexhausted. Tight13 rules out any universal strategy using only positive openings; isolated equality witnesses are essential.

The review also ruled out a proposed detour: proper rational phase-space relaxations already have strict safe points by lower-runner theory. The hard part is transferring safety to the actual one-dimensional runner trajectory. A new relative short-relation bound adds no pruning to our present remainder.

Next: an explicitly quantified, equality-preserving extension for a parameterized additive core p,q,p+q, retaining the original common-time trajectory. This is an open research target, not a promised lemma or novelty claim. General deductions remain internally reviewed proof candidates. No new mathematical computation was run; hourly remains paused.

### Prior last-runner snapshot — preserved

The [last-runner continuation](notes/LAST_RUNNER_COMPATIBILITY_2026_09_29.md) identifies a concrete placement constraint. For two core-safe windows with hull span D, gap G and larger width w, G<=3w prevents simultaneous blocking once d>=1/(4D), at every final-runner phase. Strict inequalities give positive duration. For core {1,3,4,5,7,24}, this covers every admissible d>24, including the auxiliary real-speed/arbitrary-phase setting.

The exact calculation distinguishes full strict coverage, coverage of positive components only, and zero duration. The tight d13 control preserves four isolated lonely moments after every positive opening is blocked. Two separately structured implementations agree on all declared records for three frozen inherited cores, including3162 numerical fields. General deductions remain internally reviewed proof candidates; no novelty or new eight-runner existence claim is made.

Next: show that a useful window pair or bounded collection must exist, using the core's arithmetic and retaining equality witnesses. The previous finite parameter region remains unexhausted. No broad tuple scan is authorized; hourly research stays paused.

### Prior six-core-window snapshot — preserved

The [six-core continuation](notes/SIX_CORE_WINDOW_2026_09_29.md) supplies a direct proof candidate that every common-start integer core1,4,5,a,b,c has a positive1/8-safe window. Short-chain bounds reduce the work to a frozen27-triple domain; explicit arithmetic certificates close it, and two exact implementations agree on2495 numerical fields. All50 isolated points are retained alongside190 positive components.

The last speed is now bounded too. The direct route gives a finite remainder; separately crediting established six- and seven-runner results sharpens it to **a<=34,b<=47,c<=281,d<=1268** in the fixed family{0,1,4,5,a,b,c,d}. This remaining region has not been exhaustively checked. The existence conclusions are already implied by established lower-runner/eight-runner results; our focus is an explicit structural argument. External review of our derivation and novelty assessment remain pending.

Next: identify the simultaneous containment conditions for the final runner's blocking intervals across the full six-core safe set. No broad tuple scan is authorized; hourly research stays paused.

### Prior three-speed-bound snapshot — preserved

The [core-window candidate](notes/CORE_WINDOW_REDUCTION_2026_09_29.md) bounds three residual speeds in the fixed common-start integer family {0,1,4,5,a,b,c,d}, with a<b<c<d and selected reference0. The five-constraint core1,4,5,a,b retains at least1/24 of a period as safe time. Combining this with short blocking-chain bounds leaves only **a<=34, b<=47, c<=1565** uncertified by these sufficient tests; d remains unbounded. These are internally reviewed proof candidates, not a proof of the full conjecture. External mathematical and novelty assessment remain pending.

Two exact implementations match all31 declared four-core cases across1932 numerical fields, preserving348 positive components and20 isolated points. The calculation checks twelve arithmetic values used in the universal core-measure argument. A separate translated-grid certificate handles residual gcd>=7. No broad tuple or all-reference scan was run.

Next is a direct six-constraint core-window argument, with the final equality cases preserved. Hourly research stays paused.

### Prior23-move snapshot — preserved

The [short-kernel candidate](notes/SHORT_KERNEL_BOUND_2026_09_28.md) improves the explicit universal bound to **23 advancing moves** for four quarter-duty trains, independent of positive periods and phases. A mixed continuous/discrete average shortens the covered-span bound, and a long-triple restriction sharpens the count. Six-agent internal review and exact kernel checks support the candidate; external mathematical and novelty review remain pending.

A closed core-safe window W succeeds if H=3(sum periods)/4+max(period)/4<=width(W). Integer residual speeds>=35 suffice for core1,4,5's J=[9/32,3/8]. A general auxiliary critical-duty corollary gives m!-1 moves for m>=4, with threshold1/(2m); full core-window existence and the full conjecture remain unresolved. The strict16 control proves that simple translated-box truncation can miss positive clear time.

Two exact implementations agree on1943 numerical fields; one declared auxiliary equality window retains14 isolated safe points. Twelve inherited width checks gain no newly certified row. The current next step is a structural core-window guarantee where the sufficient length condition fails. Hourly research stays paused.

### Prior39-move snapshot — preserved

The [explicit chain-bound candidate](notes/EXPLICIT_CHAIN_BOUND_2026_09_28.md) supplies a short period-averaging argument for at most **39 advancing moves** for four quarter-duty trains, independent of positive periods and phases. Six agents and the coordinator checked the span argument, strict endpoints and count. The result remains **HYPOTHESIS / proof candidate pending external review**; novelty is not claimed.

A connected strict blocking chain spans less than the sum S of the four periods. This also guarantees a common-safe point in every closed window of length S: for a supplied core-safe W, S<=width(W) suffices. On core1,4,5's J=[9/32,3/8], both the112 and113 controls meet the condition; residual integer speeds>=43 suffice. This is a selected-reference sufficient condition, not a proof of the full conjecture.

Two exact implementations match on459 numerical fields for nine inherited auxiliary fixtures. A capped selector reproduces twelve earlier windows,199 calls and32 moves against the independently archived threshold oracle. Empty and isolated-equality cases are preserved. The next question is the core/window obstruction when the sufficient width test is inconclusive. Hourly research stays paused.

### Prior qualitative-bound snapshot — preserved

The [uniform-chain candidate](notes/UNIFORM_CHAIN_BOUND_2026_09_28.md) now supplies an internally reviewed argument that an absolute bound exists on four-residual advancing moves at threshold 1/8, independent of speeds and phases. The general constant is not yet numerical;175 is established by the supplied argument only in the d>=4a regime. A forbidden immediate repetition of moving-label words and a strict-cover obstruction near periodic tilings provide the relational mechanism. Fifteen auxiliary calibration windows and a separate inherited trace pass exact checks; no new physical scan or full conjecture result. Known critical-threshold existence and close chain literature are explicitly credited. The next milestone is an auditable numerical bound for the comparable-speed regime. Hourly research stays paused. Earlier summaries below are historical.

The [blocking-chain continuation](notes/BLOCKING_CHAIN_TERMINATION_2026_09_28.md) supplies a speed-dependent termination proof candidate for the repeated four-residual selector at threshold 1/8. Strict overlaps consume a finite excess-coverage allowance, with an arithmetic lower bound on each positive overlap. Twelve reused windows agree under separately structured exact checks, preserving the small-gcd opening, tight equality and clipped-window failure. The bounds can be very loose; no speed-independent guarantee, new family existence result or full conjecture proof is claimed. The next question is whether occurrence compatibility forces a uniform bound or permits an explicit unbounded itinerary. Hourly research stays paused. Earlier summaries below are historical.

The [fourth-runner limit](notes/FOUR_RUNNER_PROJECTION_LIMIT_2026_09_28.md) now separates a valid conditional 22-projection theorem from a false universal extension. All eight archived controls pass the raw selector despite failing its conservative speed condition. A new, explicitly post-protocol common-start integer configuration makes step 22 stop unsafe, with the actual earliest lonely time reached at step 23. Exact open covers and separate threshold reconstruction verify the failure and preserve equality. This refutes that fixed step guarantee, not Lonely Runner or every possible bounded method. The next question concerns connected blocking occurrences and a justified termination bound. Hourly research remains paused; earlier summaries below are historical.

The [direct lap selector](notes/DIRECT_LAP_PROJECTION_2026_09_28.md) now computes the earliest safe time in a supplied core-safe window using at most four arithmetic projections for two residual runners, or ten nested projections for three, at threshold 1/8. Separate exact reconstruction agrees on all 20 bounded pair cases, a huge symbolic example, and endpoint/scope controls. The triple argument is a marked post-protocol deduction with one reused diagnostic. These proof candidates select compatible later laps without enumerating skipped laps; they do not force a successful window for arbitrary full configurations or add family existence coverage. Hourly research stays paused. Earlier summaries below are historical.

The [finite-anchor obstruction](notes/FINITE_ANCHOR_OBSTRUCTION_2026_09_28.md) now shows why the first-safe-lap rule can fail at every small-denominator anchor while a lonely interval survives. For {0,1,4,5,6,7,840,6720}, all 44 choices fail; a later fast lap repairs the existing anchor 3/8. Independent exact implementations agree on 308 first intervals, both positive certificates and an equality control. A supplied proof candidate extends the obstruction to every prescribed finite rational menu with a fixed early-lap budget. This identifies a certificate limitation and the need to select compatible lap occurrences; it adds no new family coverage or general Lonely Runner proof. Hourly research remains paused. Earlier summaries below are historical.

The [relational-information brief](notes/inquiries/2026-09-28-configuration-relational-information.md) now guides an [explicit common-displacement certificate](notes/COMMON_DISPLACEMENT_CERTIFICATES_2026_09_28.md): after a rational anchor, an opening is forced if the last runner enters safety before the first leaves it. A general residue formula and sufficient speed inequalities are supplied; exact checks on four old controls preserve positive intervals, a tight equality, and failed first-safe-lap itineraries. This does not establish that suitable anchors must exist. Hourly research remains paused.

The [exact interval criterion and consolidation](notes/EXACT_INTERVAL_CRITERION_2026_09_28.md) completes the midpoint/width argument: its corrected sign exactly decides supplied component containment, including omitted endpoints. Forty existing pair records (62 components) pass exact reconstruction, including multi-component successes and failures. This verifies a supplied local relationship; it does not force a successful pair or window to exist. The next structural milestone concerns cross-window arithmetic that forces useful certificates. Hourly research is paused at the maintainer's request. Earlier summaries below are historical.

The [one-pair selection test](notes/ONE_PAIR_SELECTION_2026_09_28.md) now compares a frozen information budget on six existing controls. Four individual durations guide one overlap query, with a separate endpoint fallback. It certifies three positive pair bounds, retains a tight contact, and obtains another interval from an endpoint. The final speed-16 control defeats the rule; archived best-pair bounds show that changing the pair cannot fix this selected window. A cap test can sometimes detect that certificate-class limitation before any overlap query. Exact verification and cost records distinguish selection failure from failed loneliness. These known controls add no new existence coverage or general guarantee.

The [adaptive reflected-pair argument](notes/ADAPTIVE_REFLECTED_PAIR_2026_09_28.md) now supplies a lonely instant for every admissible V and every initial phase of runner 11 in the fixed family {0,1,4,5,6,7,11,V}. It uses the old speed-dependent time and its reflection. The pair itself reaches exactly 1/8, while directed endpoint information gives a positive interval of length at least 1/(56V) whenever 8 divides V. This closes all three former fixed-menu failure classes. Original common-start family coverage was already available; general implications remain proof candidates, with exact finite checks and separate internal review. Next proposed: the preserved small-gcd certificate-selection question on existing controls. Earlier next-step statements below are historical.

The [fixed-time-template classification](notes/TIME_TEMPLATE_CLASSIFICATION_2026_09_27.md) now gives exact arithmetic coverage in `{0,1,4,5,6,7,11,V}`. The two prescribed pairs certify every phase of runner11 in117 of120 fixed-time residue classes; these counts concern this particular certificate and family. The missed classes are0,32,88mod120. Their least admissible representatives120,32,88 nevertheless have positive duration at every phase, verified by separate exact reconstructions. The earlier variable-speed work already explains why no finite fixed rational menu can cover every V: a denominator multiple collides at every listed time. Next proposed: test the old V-dependent common-start witness together with its reflection as an adaptive pair. Original common-start family coverage was already available; this round adds compact phase-robust certificates and preserves their failures, with no general Lonely Runner or novelty claim.

The [phase-projection study](notes/PHASE_PROJECTION_2026_09_27.md) completes both controls' exact phase sets, safe-time multiplicities, and full duration profiles. Separate implementations agree on 43 algebraic phase cells and all 29 prior offsets. The speed-16 control's exact worst-phase duration is 39/4928; support measure already gives this sharp bound, while multiplicity changes the rest of the profile. A [two-time certificate](notes/TWO_TIME_CERTIFICATES_2026_09_27.md) verifies all-phase strictness from just 7/15 and 8/15, with distance at least 2/15. A supplied circle argument makes some two-time certificate complete for one-runner all-phase robustness at threshold 1/8. This is conditional completeness for a stronger auxiliary question, not a guarantee for arbitrary speeds or a general Lonely Runner proof. Next proposed: derive the exact arithmetic coverage and failures of the two fixed time templates in the existing one-parameter family. Earlier next-step statements below are historical.

The [fastest-lap alignment study](notes/FASTEST_LAP_ALIGNMENT_2026_09_27.md) completes all 29 one-runner-core laps for the existing speed-13 and speed-16 controls. An endpoint-aware phase rearrangement preserves each runner's individual pattern inventory but changes clear duration and local existence. Separate implementations agree on all 29 original laps and all 29 shifted-start arrangements (425 lap records). New [restricted phase-robustness proof candidates](notes/PHASE_ROBUSTNESS_2026_09_27.md) explain the outcomes: speed13 has zero duration only at the original speed11 phase, while speed16 retains at least 1/176 clear time at every speed11 phase. The distinction is an available phase arc that exactly fits one blocker versus a phase union that is wider. These are fixed-family explanations, not a general existence or novelty claim.

The [six-agent transfer study](notes/TEAM_TRANSFER_2026_09_27.md) checks six frozen configurations, 210 cores, and 15,696 complete windows with two separately structured exact implementations. Its main result is a [fastest-core proof candidate](notes/FASTEST_CORE_CERTIFICATES_2026_09_27.md): a core containing the fastest absolute relative speed makes each residual blocker a single interval, so the optimal tree certificate equals actual clear duration. All 8,800 such windows in the batch agree. Even a one-runner fastest core suffices in the argument. This explains conditional certificate selection; it does not prove lonely-time existence. The next proposed task compares interval-cover chains across the fastest laps of the existing tight speed-13 and strict speed-16 controls.

The [relationship-selector experiment](notes/RELATIONSHIP_SELECTOR_2026_09_27.md) tests the proposed map on 80 windows from five existing configurations. The same nontrivial containment map can accompany an empty window or a positive opening. Choosing the fewest remaining constraints fails throughout this batch; adding retained single/pair durations selects strict certificates in all four strict cases, with an endpoint fallback retaining the tight control. The countercontrol also reveals a different useful containment: B19 is contained in B45 on the chosen J. These are bounded mechanism and selection results, with separate exact reconstruction and no new family-coverage claim.

The [fixed-window containment classification](notes/FIXED_WINDOW_CONTAINMENT_2026_09_27.md) finds 30 distinct-speed replacements for 11 that preserve the exact tree on the selected opening. A two-coordinate integer-lattice certificate bounds the search by 84; the largest feasible replacement is 73. Separate exact implementations retain all endpoint contacts and check 35 local certificates. The supplied all-parameter argument gives the same positive bound for y>=29, while a countercontrol shows that containment is sufficient but not necessary for a successful tree.

The [44/45/46 follow-up](notes/CORE_EXCHANGE_NEIGHBORS_2026_09_27.md) identifies why a core exchange works: one residual blocker disappears and another is contained in a third on the selected window. The resulting tree is exact, with a proposed uniform positive bound for the existing family's variable speed y>=29. Exact finite calculations and a separate reconstruction accompany the argument.

The [all-core selection experiment](notes/ALL_CORE_SELECTION_2026_09_27.md) checks eleven named configurations at every reference. Every strict reference has a successful tree certificate somewhere. One core fails across all its windows but is repaired by a stronger inequality using the same pair data. This is a bounded result, independently reconstructed, with equality-only controls retained.

The [September 27 Ultra review](notes/ULTRA_REVIEW_2026_09_27.md) assesses the distinction audit through six separate mathematical and literature scopes. It preserves exact examples of information lost by overlap summaries, a conditional contact selector, and threshold-response and global-witness deductions. Its unbounded implications remain proof candidates; the next question is how to select a useful certificate for a configuration.

The repository contains:

- an exact rational checker using independently structured methods;
- regression tests and bounded crosschecks;
- an offline interactive visual demonstration;
- exact studies of tight configurations and reference-runner roles;
- interval-cover, blocking-chain, overlap, and local-duration analyses;
- Fibonacci experiments followed by a literature correction identifying already-known results;
- one-variable and two-variable integer-family arguments for a selected reference runner;
- structured speed-ratio and local-overlap investigations;
- explicit counterexamples to several tempting but overbroad explanations.

Several arguments in the newer notes are **proof candidates or restricted-family arguments awaiting independent review**. They are not claims that the full Lonely Runner Conjecture has been solved, and novelty is not asserted unless the literature record supports it.

For the detailed live state, read [HANDOFF.md](HANDOFF.md).

## Try the exact checker

Python 3.10 or later; no third-party Python packages are required.

```bash
python -m lonely_runner --velocities 0 1 2
python -m lonely_runner --velocities 0 1 4 --all-references
python -m lonely_runner --velocities=-1/2,0,1/2 --reference 1 --json
python -m unittest discover -s tests -v
```

Inputs are exact integers or fractions such as `3/2`; floats and decimal strings are rejected. Large normalized inputs fail explicitly rather than being reported as mathematical counterexamples.

## Visual demonstration

Open [demo/index.html](demo/index.html) locally after cloning or downloading the repository. It works offline and uses exact precomputed cases for its verified peak labels.

```bash
python -m scripts.build_demo
python -m scripts.build_demo --check
```

The visual layer is explanatory. Exact claims live in the checker, experiment outputs, written derivations, and cited literature.

## Participate

You do not need write access to contribute.

When this repository is public, the normal path is:

1. fork the repository;
2. create a branch in your fork;
3. reproduce or challenge the relevant result;
4. state the evidence level of your contribution;
5. submit a pull request.

A pull request is a proposal, not a change to the canonical record. See [CONTRIBUTING.md](CONTRIBUTING.md) for the research and reproducibility expectations.

Especially welcome:

- counterexamples;
- independent proof review;
- simpler derivations;
- reproduction of computational claims;
- literature connections we missed;
- alternative representations that generate testable consequences;
- corrections to our terminology, assumptions, or scope.

## Canonical record

`main` is intended to represent the best current organized research record, not an assertion that every idea in the repository is correct. Failed approaches, corrections, and counterexamples are part of the scientific history and should be preserved when they remain informative.

> **Anyone may question. Anyone may investigate. Anyone may contribute. Canonical claims change only when the evidence earns the change.**


## License

Code and software are licensed under the [MIT License](LICENSE-CODE).
Research writing, notes, figures, diagrams, and data are licensed under
[Creative Commons Attribution 4.0 International](LICENSE-CONTENT.md) unless
otherwise noted. See [LICENSE](LICENSE) for the repository-wide licensing
boundary and third-party-material notice.
