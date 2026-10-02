# Mathematical mechanisms: transferable-value review

Date: 2026-09-30. Research baseline: `52c4912a89e4c314201e66e7fa94da7fa3366964`, repository `tradingartofwar/the-lonely-runner-conjecture`. This is the mathematical track of the requested review, not a new experiment, external certification, novelty finding, or completed application. The review agent used the inherited model configuration; no separate “Ultra” model identity was established. It read common project sources, used the GitHub connector for pinned files, inspected local source/output text, and browsed primary literature. It did not execute the research programs, enumerate target inputs, benchmark, contact anyone, or publish Git changes.

## Assessment

The most portable mathematical object is older than the recent compact-menu experiments: the critical-duty averaging argument and its endpoint-jump consequence. Four periodic open blackout intervals, each occupying one quarter of its own period, have a candidate bound of 23 advancing jumps before a joint-safe point. Its stated theorem already allows arbitrary positive real periods and arbitrary phases; common start and integer speeds are not needed. A narrow exact periodic-feasibility library could use it as a stopping certificate. The theorem remains an internally reviewed proof candidate, and the present review demonstrates neither external demand nor a performance gain.

The strongest application objection is substantive: the safe point can be isolated. A scheduling job needs time to execute; a physical trigger normally needs timing margin; ordinary outage calendars often include their starting endpoint. All three changes can invalidate the proposed guarantee. The repository's own equality fixture exposes this immediately. The useful next step is a small semantic-conformance test, not a larger speed search or a broad application claim.

The two-window last-runner argument is a second compact tool: retain two actual openings, their widths and separation, and prove that one additional periodic blackout cannot cover both at any phase. Its strict version supplies positive duration, but no prescribed minimum duration. It is a useful geometric certificate under supplied-window assumptions, not a general scheduling algorithm.

## Ranked candidates in this track

| Rank | Candidate and concrete destination | What is supported | Novelty and practical assessment |
| --- | --- | --- | --- |
| 1 | Critical-duty averaging plus exact endpoint jumps for an earliest simultaneous **instant** query against four periodic threshold constraints | Complete argument candidate, exact archived kernel calibrations, existing projection traces; arbitrary phases/real periods in the mathematics | Best standalone mathematical extraction. Novelty of mixed kernel/23 bound unresolved. External utility a supported hypothesis, strongly conditional on endpoint semantics. |
| 2 | Two-window protection against one additional periodic outage of unknown phase | Explicit inequality certificate, including separate existence and positive-duration forms; inspected underlying proof | Small useful sufficient check if the windows already exist. Elementary interval geometry; no novelty or external use demonstrated. |
| 3 | Exact midpoint/width margin for a supplied time window | Exact formula, with open/closed and zero-speed cases; proof read directly | Established distance-to-set/Lipschitz reasoning made exact for an affine phase. Useful implementation and teaching example, not a new mathematical framework. |

Ranks describe this track's evidence, not a claim to displace the other reviewers' algorithmic or representation candidates. No named open problem qualifies as a serious transfer target on this evidence.

## Transfer record 1: certified periodic point availability

| Field | Record |
| --- | --- |
| Origin | `notes/SHORT_KERNEL_BOUND_2026_09_28.md`, §§1–4 (mixed kernel, span, 23 advances, window condition); §6 for the larger critical-duty model. `notes/EXPLICIT_CHAIN_BOUND_2026_09_28.md`, §§2–5 supplies the simpler 39-move predecessor. `notes/DIRECT_LAP_PROJECTION_2026_09_28.md`, §§1–3 defines the arithmetic projection and earliestness. Status: HYPOTHESIS / proof candidates. Archived rational computations are OBSERVED within their declared fixtures. |
| Mechanism | For open trains `B_i=union_m(s_i+mp_i,s_i+(m+1/4)p_i)`, choose a largest period `P`; average over one uniform `[0,P]` variable and three independent four-point quarter-period grids. The resulting density is positive on `(0,H)`, `H=P+3(sum other p_i)/4`, and its average of total multiplicity is exactly one. A continuously blocked strict chain spanning H would give strictly positive weighted excess, a contradiction. Whole-occurrence counting plus the long-three-label restriction bounds an actual increasing-endpoint chain by 23. |
| Destination | An exact calendar primitive answering: for four prescribed periodic **open threshold-violation intervals**, find the earliest time in closed `[L,R]` when all predicates hold, or certify no such time exists there. A synthetic synchronized-sampling admission check is a concrete candidate use. No deployed customer task has been identified. |
| Translation | Periods become repetition periods; shifts become blackout origins; runner lap becomes blackout occurrence index; weak phase safety becomes admissible point time. A violated predicate advances the candidate to the right endpoint of its current open blackout. A shared scalar time is retained throughout. Only the earliest point and trace are requested; total available duration, later components, best margin, throughput, resource contention and job sequencing are discarded. |
| Inherited guarantees | Under the exact open-interval, one-quarter duty, fixed-period, four-train hypotheses, the mathematical candidate carries over unchanged: at most 23 advances; earliestness; safe point inside every closed interval of length H. An iterate above R certifies only that supplied window is empty. The existing implementation is rational; real-period mathematics does not supply exact computation for arbitrary irrational inputs. |
| New obligations | Establish that the destination really uses open violation intervals and admits a zero-duration answer. Prove the adapter's period/phase/endpoint conversion, range and occurrence arithmetic. Independently review the 23 proof before relying on the bound. Any dwell time, clock error, asymmetric duty, multiple blackout pieces per period, variable periods or scheduling resource constraints needs a fresh argument. A maximum number of arithmetic operations is not a bound on bit cost. |
| Existing approach | Exact event partition/intersection is a transparent comparator, already implemented in the repository's separate verifiers. Beck–Hoşten–Schymura (2019), Theorem 4 and its proof, supplies known arbitrary-phase **integer-speed** existence at `1/(2k)`, credited to Schoenberg; it does not state this actual-trace 23 bound. Rifford's 2022 author preprint, Definition 5 and Proposition 4, uses minimal interval covering chains with an extra nonadjacent-order condition. That condition cannot be silently imposed on arbitrary projection traces. No priority determination was reached for the averaging/count result. |
| Added value | Potentially a small auditable stopping certificate and direct occurrence jumps, without materializing every lap or a long rational common period. Already useful internally as an explanation of termination and a replacement for a discredited fixed cap. No external speedup or broad solver advantage is established. A generic event sweep may remain simpler and fast enough on real inputs. |
| Failure test | The archived equal-period tiling below has isolated admissible points but no positive dwell interval. With half-open outages it has no admissible point at all. Any adapter that returns the point as a feasible job slot, or applies the 23 guarantee to that half-open calendar, fails. Separately, one valid open-quarter-duty exact trace with over 23 advances would refute the bound. |
| Smallest useful test | The four-record unrun protocol below; compare endpoint jumps with exact event partition, freeze the adapter before running, preserve unsupported cases explicitly, and do not time it. |
| Assessment | Supported mathematical transfer under exact hypotheses; practical usefulness unvalidated. An interesting theorem candidate and a possible verification primitive, not a demonstrated engineering application or general solution of scheduling. |

### What the proof actually retains

This proof does not rely on a source atlas or low-rank coefficient family. It retains one physical clock, each interval occurrence, strictly increasing endpoints and equality-safe boundaries. It handles containment and skipped occurrence indices; it does not replace the actual trace by a minimal cover. The continuous uniform component matters: the discrete quarter-period average is zero, rather than one quarter, at its exceptional threshold grid. Continuous averaging removes these measure-zero exceptions from the integral while the solver still preserves their point semantics.

The historical progression should not be compressed into “the new average worked better.” The speed-dependent bound was enormously loose on the seven-advance counterexample. The qualitative compactness proof then gave existence of a uniform bound; full-period averaging supplied 39; the mixed kernel and long-triple argument supplied 23. The archived twelve-window comparison says both old S and shorter H certify exactly the same five windows. No newly certified window in that diagnostic set was obtained. Neither 23 nor 39 is demonstrated sharp; the earlier seven-advance trace reached its answer at raw call 23, which is a different count.

## An explicit unrun semantic-conformance test

This test is **not executed** and is not presented as fresh validation. Inputs intentionally reuse frozen source fixtures, so a pass would validate the adapter's handling of known examples, not external generalization. Freeze these records and the endpoint interpretation before implementing. Let all times use a declared synthetic time unit.

| Record | Fixed input and requested output | Required distinction |
| --- | --- | --- |
| A: isolated point | Four periods `4/13`; starts `0,1/13,2/13,3/13`; open intervals `(s+mp,s+mp+p/4)`; query `[1/26,1]`; dwell 0 | Earliest admissible point is `1/13`. In the archived `[0,1]` fixture, the entire safe set is `{j/13:0<=j<=13}` and duration is 0. |
| B: positive dwell | Same periods, starts, openness and query; require the whole interval `[t,t+1/1000]` admissible and within the query | No such interval exists. The point theorem is insufficient for this query; do not silently reuse its witness or its move bound for expanded blackouts. |
| C: calendar boundary | Same periods, starts and query, but each blackout is `[s+mp,s+mp+p/4)`; dwell 0 | The four calendars cover every time. The open-blackout theorem is inapplicable; exact event logic must return no point, or the specialized solver must reject the unsupported model before dispatch. |
| D: positive opening control | Periods `(1/6,1/7,1/11,1/16)`; starts `(-1/48,-1/56,-1/88,-1/128)`; open quarter-period blackouts; query `[9/32,3/8]`; ask separately for dwell 0 and dwell `1/1000` | Archived first safe interval `[17/56,39/128]` has width `1/896`, so both queries have earliest start `17/56`. The dwell guarantee follows from this supplied interval, not from the critical-duty point theorem. |

Comparator: a separately implemented rational threshold-event partition preserving point membership and interval endpoint flags. For a positive dwell query, inspect complete safe components and contract each right endpoint by the requested dwell, carrying flags. Do not decide positive duration from an isolated earliest component.

Budget: exactly these four calendars, five query records (D has two), no random inputs, no search over periods/phases, no benchmark, at most 10,000 generated threshold events per record, and 23 advancing jumps only for the theorem-eligible point queries. Reaching a resource cap is INCOMPLETE, never mathematical infeasibility. For a declared non-eligible model the specialized theorem must not be dispatched. Freeze the protocol and source hashes before a future execution.

Success measure: exact agreement of point feasibility, earliest time, dwell feasibility and applicability classification; a trace showing every advance skipped only an open forbidden interval. Failure interpretation: a disagreement locates a semantic or implementation error; >23 valid advancing moves challenges the proof; a pass supplies conformance evidence only. No runtime success criterion is declared.

The phase-origin map in D is `s_i=-1/(8v_i)`, `p_i=1/v_i`; this matches the original open interval around each integral phase. It is easy to lose this shift when converting the symmetric runner condition to a one-sided calendar interval.

The adversarial reviewer sharpened the dwell objection: requiring `[t,t+tau]` to avoid an open blackout `(a,b)` forbids start times in `(a-tau,b)`. Before any wrapping/merging, the per-period forbidden width becomes `p_i/4+tau`, so duty becomes `1/4+tau/p_i` and aggregate duty exceeds one. The exact point solver cannot inherit its critical-duty stopping bound after this transformation. Clock uncertainty likewise requires a fresh margin argument. This is a semantic failure of the proposed extension, not a defect alleged in the original open-point theorem.

## Transfer record 2: two openings resilient to one unknown-phase blackout

| Field | Record |
| --- | --- |
| Origin | `notes/LAST_RUNNER_COMPATIBILITY_2026_09_29.md`, §1. Two supplied closed positive core-safe intervals I and K. The exact source example is `I=[25/56,29/64]`, `K=[89/192,15/32]`. Status: internally reviewed proof candidate; finite core computations observed. |
| Mechanism | Put hull length D, intervening gap G, largest individual width w. A quarter-duty train of speed d can strictly cover both intervals only in the same occurrence, requiring `dD<1/4`, or different occurrences, requiring `dG>3/4`; either requires `dw<1/4`. Hence `G<=3w` and `d>=1/(4D)` exclude complete blocking at every phase. With both inequalities strict, the argument with closed blockers excludes zero residual duration. |
| Destination | Verify that two already-approved service opportunities cannot both be eliminated by one periodic quarter-duty disturbance with unknown phase. This is a robust opportunity check, not construction of a schedule or optimization of jobs. |
| Translation | Approved windows map to I,K; disturbance period to `1/d`; unknown offset to final phase. Retain widths, gap and hull, plus endpoint semantics and actual window membership in the pre-existing feasible set. Discard internal origin of those windows only after membership has been certified. |
| Inherited/new obligations | Source example has `D=5/224`, `G=1/96`, `w=3/448`, so all real `d>=56/5` leave a point and all `d>56/5` leave positive duration. No common start or integer final speed is required for this pair argument. The window supplier, the disturbance model, any required minimum dwell and robustness to clock error require separate certification. Positive duration alone does not quantify an operationally useful minimum. |
| Existing approach | Direct interval containment and a same-occurrence/different-occurrence case split; the closest inspected primary geometric precedent is Rifford's occurrence-labelled covering-chain formulation, not a claimed original scheduling theorem. Standard exact interval intersection remains the practical baseline. |
| Added value | A constant-size, phase-uniform sufficient certificate whose failure can be explained with the two incompatible occurrence requirements. Width alone loses this placement information. It may be a useful precheck or teaching example; no evidence it beats established scheduling tools. |
| Failure test | Any phase at an eligible d that covers both complete windows would refute the statement. A job longer than the remaining interval refutes a careless “positive duration means job fits” application, not the point certificate. |
| Smallest useful test | Keep this pair and one final speed `d=12` fixed; compare the symbolic same/different-occurrence exclusion with an exact phase-event partition, preserving endpoint contacts. Budget one pair and at most 1,000 phase events, no speed or phase sampling. This is an alternative future test, not an additional recommended project and not executed. |
| Assessment | Supported conditional transfer of a short geometric certificate; no demonstrated external application. The mathematics may be useful even if familiar. |

## Exact interval margins and negative findings worth keeping

For a supplied interval with center m and half-width h,

`inf dist(vt+alpha,Z) = max(dist(vm+alpha,Z)-|v|h,0)`.

The proof in `EXACT_INTERVAL_CRITERION`, §1, directly uses the distance function's Lipschitz inequality and a nearest integer to attain the lower bound. For positive threshold delta, nonnegative `dist(vm+alpha,Z)-|v|h-delta` exactly decides weak safety of the whole interval. This is more than testing the midpoint, but it still assumes the interval was supplied. It is an exact robust-time-window check for a fixed affine phase; arbitrary nonlinear trajectories do not inherit exactness from a Lipschitz bound. An open endpoint can make the infimum unattained without changing the weak-containment verdict.

Three instructive failures have practical interpretive value:

1. `SHORT_KERNEL` §5 and `windows_results.json`: in strict16, a safe interval of width `1/896` exists, but every translated/truncated nonnegative mixture of sufficiently wide boxes has positive signed excess. Failure of that weighted summary to detect an opening does not mean none exists. The claim is about that stated kernel class, not every possible local certificate.
2. `LAST_RUNNER` §§2–3: full strict coverage F, strict coverage of only positive components P, and zero-duration coverage Z differ. At d=13 all positive core components are strictly covered while four isolated witnesses survive. A duration-only scheduling representation is adequate for positive jobs but inadequate for point existence; conversely point existence is inadequate for jobs.
3. `DIRECT_LAP_PROJECTION` §4: the `(840,5880)` control's first safe component is a singleton, with positive components later. Earliest-point output does not answer whether the full window has positive duration. A consumer must request the correct output or recover the richer safe-set representation.

## Assumptions that survive or break

| Change | Consequence for this track |
| --- | --- |
| Remove common start | Kernel, pair/triple projection and two-window geometry already allow arbitrary phases; the fixed-core arithmetic and reflection reductions do not all survive. |
| Remove integer speeds | Kernel and two-window proof statements still apply to positive real periods/speeds. Exact supplied programs use rationals; endpoint residue and common-period simplifications need new treatment. |
| Change quarter duty or add a fifth quarter-duty train | The particular zero-excess identity and 23 count cannot be inherited. Total duty becomes greater than one for five quarter-duty trains. Four equal-duty `1/4` intervals have special discrete translates; arbitrary shapes or duties are not covered by the mixed-kernel proof. |
| Change open blackouts to half-open/closed | Isolated safe contacts can disappear entirely. Tiling fixture C is an explicit failure. |
| Require duration, margin or jitter tolerance | Existence can survive while useful duration is zero. Expanding each blacklist to encode a dwell or uncertainty changes duties and hypotheses; dispatch must be re-justified. |
| Remove supplied windows | The two-window and local exact-margin tests no longer provide discovery or an existence theorem. |
| Replace actual shared time by separate feasible phases | The conjunction is relaxed. No guarantee of a common physical time follows. |
| Increase m in the equal-duty `1/m` model | The source gives a conditional `m!-1` advance corollary for m>=4. It is not polynomial scalability or the full Lonely Runner model, whose aggregate duty exceeds one. |

## Primary literature and rejected leads

All web retrievals below were made on 2026-09-30. No complete literature census was performed.

| Source/version | Inspected material | What it licenses and what it does not |
| --- | --- | --- |
| Matthias Beck, Serkan Hoşten, Matthias Schymura, *Lonely Runner Polyhedra*, Integers 19 (2019), A29; published 2019-06-03. https://math.colgate.edu/~integers/t29/t29.pdf | Bibliographic front matter; Proposition 1 context; printed p12, Theorem 4 and its full elementary proof | Known arbitrary-phase integer-speed existence at the weaker `1/(2k)` threshold, credited to Schoenberg 1976. Do not label that existence new. Original Schoenberg paper not inspected here. No determination of priority for the mixed kernel or 23 bound. |
| Ludovic Rifford, *On the time for a runner to get lonely*, author PDF dated 2022-02-21. https://math.univ-cotedazur.fr/u/rifford/Papiers_en_ligne/LR_Rifford.pdf ; journal DOI https://doi.org/10.1007/s10440-022-00515-9 | Abstract/introduction and §2.2, printed pp12–14, Definition 5, Proposition 4, Proposition 5 and its proof | Direct chain/occurrence precedent. Definition 5 has minimal-cover conditions including strict separation of nonadjacent intervals. Our actual projection traces need not satisfy them. Full paper and §4 exhaustive chain classification were not independently checked. The arXiv HTML v2 open failed, so this review pins the dated author PDF instead. |
| Hiroshi Fujiwara, Kota Miyagi, Katsuhisa Ouchi, *Pinwheel Scheduling with Real Periods*, arXiv:2510.24068v1, 2025-10-28. https://arxiv.org/html/2510.24068v1 | Abstract and §1 definitions, Theorem 1, Conjecture 2, Theorem 2, through the failed identification example in §1.1.1 | Integer `5/6` pinwheel density was already settled by Kawamura, and this primary paper poses a real-period extension. Pinwheel asks for a discrete perpetual assignment with recurrent deadlines, not a common free point in fixed periodic calendars. No reduction from our kernel or two-window certificate to its schedule synthesis was found. We do not make a current-status claim for the real-period conjecture or propose it as a transfer target. |

The primary PNAS DOI page for Kawamura's 2026 version, https://www.pnas.org/doi/10.1073/pnas.2530214123, redirected to a cookie wall; its proof was not read. The newer pinwheel paper above explicitly states the integer theorem. Search results about maintenance scheduling were leads only; their abstracts do not establish that the current mechanisms solve those job-sequencing models. No empirical scheduling literature is used as evidence of utility.

Quantum, gravitational, distributed-intelligence or broad “synergy” claims have no mechanism-to-output bridge here. `DOMAIN_CONNECTIONS.md` itself carefully distinguishes phase notation and coordinate translation from quantum advantage, interaction, or a measured information-theoretic quantity. A shared scalar clock plus modular phases is mathematics already; a new name does not create an application.

## Coverage and provenance ledger

Every repository statement above is tied to baseline commit `52c4912a89e4c314201e66e7fa94da7fa3366964`. Canonical source URL pattern: `https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/52c4912a89e4c314201e66e7fa94da7fa3366964/<path>`. Pinned GitHub fetches report the Git blob SHAs below; they are provenance identities, not assertions that this reviewer reran hash audits or mathematical computation. Local snapshot parsing is inspection, not reproduction.

| Cluster/artifact | Direct coverage and limits |
| --- | --- |
| Governance/trajectory | AGENTS, review brief, CLAIM_STATUS and CONTRIBUTING read; README introductory/current summaries, research-plan queue, CC representation-rule opening/obligations, and HANDOFF relevant chain/kernel/last-runner entries inspected. These very large living overview files were not independently checked end to end. |
| Chain development | `BLOCKING_CHAIN_TERMINATION`, `UNIFORM_CHAIN_BOUND`, `EXPLICIT_CHAIN_BOUND`, `SHORT_KERNEL_BOUND` read in full, including underlying proof arguments and declared limits. Separate six-agent review files and historical computation packages were not all re-reviewed. |
| Short-kernel code/evidence | `protocol.json` read; `primary.py` and verifier's substantive primitives/kernel/event/equality functions read directly; `manifest.json` and `comparison.json` inspected. `results.json` counts and complete equality fixture inspected, not all 144 integral records individually. `windows_results.json` complete 12-case records and strict16 signed-event table inspected. No program rerun. |
| Exact selection | `EXACT_INTERVAL_CRITERION` read in full; `DIRECT_LAP_PROJECTION` §§1–4 and start of §5 read directly. Exact interval audit output and direct-projection programs were not rechecked in this track. |
| Last-runner | `LAST_RUNNER_COMPATIBILITY` read in full, including pair proof, F/P/Z, symmetry and scope. `PROTOCOL.json`, `primary_last_runner.py` and manifest inspected; primary interval/endpoint-band implementation read. Full primary/independent JSON and independent code not reviewed here. Pair numeric certificate checked by reading arithmetic in the note, without a new computation. |
| Core-window reductions | `CORE_WINDOW_REDUCTION` §§1–5 and start of §6 read directly: width/measure/component bounds and integer/common-start dependencies. Six-core reduction and final finite-box exhaustiveness not re-reviewed. |
| Original cross-domain work | `DOMAIN_CONNECTIONS` inspected as an historical translation/scope document, with proofs/code in its linked Fibonacci, graph and phase packages not checked. |
| Recent exact-spectrum/CC compilers/rank-three | Seen through prerequisite current summaries and other team members' assignments; this track makes no independent review claim for them. |
| Fresh testing | None. Explicit test design only. No new target inputs were executed, no benchmark or broad scan, no external application validation. |

Selected immutable Git blob identities:

| Path | Git blob SHA |
| --- | --- |
| `notes/BLOCKING_CHAIN_TERMINATION_2026_09_28.md` | `b9b166e0fd63a51bed7f7a5024c675096666d5f5` |
| `notes/UNIFORM_CHAIN_BOUND_2026_09_28.md` | `1fecf4c92bec921405f2d1d802ef55eed241ceff` |
| `notes/EXPLICIT_CHAIN_BOUND_2026_09_28.md` | `877fc865d593bc3b6af2c27a1ed6ea051315f78e` |
| `notes/SHORT_KERNEL_BOUND_2026_09_28.md` | `24f17a64fe58677d944795d4f4b40eba2fc99e0b` |
| `notes/EXACT_INTERVAL_CRITERION_2026_09_28.md` | `6c2507ebb501b217cfa8a622bf5fbed235364d42` |
| `notes/DIRECT_LAP_PROJECTION_2026_09_28.md` | `e74aa4b1257d2cd5a0f6da3bf563f63d25bd1ea3` |
| `notes/LAST_RUNNER_COMPATIBILITY_2026_09_29.md` | `5d39e7ffdb39e92db95cdc96096991a8437b951c` |
| `notes/CORE_WINDOW_REDUCTION_2026_09_29.md` | `e6e1c9e42ba47a4dd41c4e86e334ac3a30354edf` |
| `reviews/2026-09-28-short-kernel/protocol.json` | `9485517bd17b7567932a0a1eaf8ed6fef9259a9c` |
| `reviews/2026-09-28-short-kernel/primary.py` | `b941df656f72b2e261054038f1697bcf10ed47b9` |
| `reviews/2026-09-28-short-kernel/verify.py` | `40a710b87fd6889c36b0d638592da45b3ffda0e7` |
| `reviews/2026-09-28-short-kernel/results.json` | `e3bdd82811d49d7b5f3f4ec75312e321d52483fc` |
| `reviews/2026-09-28-short-kernel/windows_results.json` | `4398b7dd03503c7f2f0c5ac017ac70417e0d8ba1` |
| `reviews/2026-09-28-short-kernel/comparison.json` | `3267632b6bed7dcfc3eea847676ad6af4eb09213` |
| `reviews/2026-09-29-last-runner/primary_last_runner.py` | `71c192d3dd672bc1d83ad7f5e67928a76c4db12a` |
| `reviews/2026-09-29-last-runner/PROTOCOL.json` | `e16e281ddf41697381010536d4ce6a76832d270b` |

## Recommendation and strongest reason it may fail

If the overall review selects an external mathematical test, do only the four-record semantic adapter test above before extending the research. It asks whether the reusable unit has an honest input/output contract. The strongest reason to stop afterward is that real desired tasks need half-open calendar semantics, minimum dwell and jitter tolerance; the exact critical-duty point guarantee supplies none of them. A pass would still leave that demand question unanswered.

Keep the mixed-kernel derivation and the two-window certificate as small standalone mathematical candidates, with external proof/priority review explicitly pending. Simplify application language to periodic interval feasibility and exact interval geometry. The useful contribution may be a proof-bound primitive and clear counterexamples that teach consumers what an existence witness does and does not buy.
