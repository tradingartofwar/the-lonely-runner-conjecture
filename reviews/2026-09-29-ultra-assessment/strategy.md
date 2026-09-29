# Strategy review: exact proof distance and a stopping rule

Date: 2026-09-29. Assigned scope: logical distance from the strongest fixed-core results to arbitrary-runner LRC, equality witnesses, allocation, and research gates. The root supplied a connector snapshot pinned to `7b0101376e00dbb71537d3a62e39ec75cee113cc`; the local copy has no `.git` directory. This review used static reading, hand deductions, and primary-source reading. No executable mathematical calculation or scan was performed. General deductions below retain **HYPOTHESIS / proof-candidate** status; proposed targets are **OPEN**, and no novelty is asserted.

## Assessment

We have a useful, increasingly explicit mechanism for supplying and checking witnesses in a special family. We do not yet have a mechanism that forces such witnesses for arbitrary speed vectors. The missing implication is structural, and contains the difficult part of LRC; it is not a final constant adjustment or one more finite diagnostic.

There are two different destinations. Completing an explicit proof for the family `{0,1,4,5,a,b,c,d}` would be a legitimate explanatory result. It would recover an existence conclusion already covered by the credited eight-runner literature. A proof for arbitrary `n` must additionally remove the privileged `1:4:5` core, preserve the threshold as the runner count grows, and handle boundary-only witnesses. Nothing in the present finite remainder provides those implications.

## What should be retained

The strongest concise mechanism is the last-runner certificate: two supplied core-safe intervals with hull span `D`, gap `G`, and larger width `w` cannot both be strictly blocked when `G<=3w` and `d>=1/(4D)`. Strict inequalities yield positive duration. For `{1,3,4,5,7,24}`, the exact pair has `D=5/224`, `G=1/96`, `w=3/448`; therefore every real `d>56/5` succeeds at every final phase with positive duration. This is a genuine quantified auxiliary extension, conditional on an explicitly verified core.

The most broadly parameterized result is the critical-duty chain argument: `m` arbitrary-phase trains at duty `1/m` have support bound

`H_m=Pmax+((m-1)/m) sum(other periods)`

and the supplied induction gives `m!-1` advancing moves for `m>=4`. Its usefulness is an explicit bound and a witness procedure on a sufficiently long supplied window. The underlying shifted-existence conclusion is already credited in the repository; novelty of the refinement remains unassessed.

The endpoint-sensitive `F/P/Z` separation is essential, not bookkeeping. It cleanly distinguishes full strict coverage, strict coverage of positive core components, and zero final duration. It should be part of any future theorem statement, data contract, or proof certificate.

## The implication ladder

| Desired implication | Present position | Character of the missing work |
| --- | --- | --- |
| Supplied windows or points imply a valid witness | Several exact sufficient criteria and internally reviewed proofs exist. | Audit and exposition; mathematical review is still needed. |
| Every admissible fixed `1,4,5,a,b,c` core has a positive `1/8`-safe interval | Direct proof candidate supplied; known lower-runner theory also implies this. | Primarily verification and attribution. |
| One final runner cannot strictly cover that entire core | Exact lap-band representation and several inherited cores are closed; no universal fixed-family structural exclusion supplied. | Substantive certificate-existence or exception-classification problem. |
| The unexhausted finite fixed-family remainder is covered | Credited sufficient reductions leave `a<=34,b<=47,c<=281,d<=1268`. | A finite task in principle, but unexecuted and unauthorized as a scan. It is not arbitrary eight-runner coverage. |
| Every arbitrary eight-runner vector has a suitable privileged core | No such reduction. Translation, scaling, signs, and reference changes do not force the ratios `1:4:5`. | A new structural theorem, not normalization. |
| The construction scales to arbitrary `n` at threshold `1/n` | The auxiliary train count scales, but its duty and its supplied-window premise do not solve the full problem. | A threshold-preserving structural extension or reduction; this is the central research gap. |

The all-reference issue should be stated accurately. A theorem for *every* nonzero relative-speed vector would apply after selecting each reference, taking absolute relative speeds, and retaining the original runner count if absolute values coincide. A theorem for the displayed fixed core does not have that quantifier. Running more references on the same few configurations would not repair the missing universal vector theorem.

## Why the scalable auxiliary theorem stops short

For total runner count `n`, a single blocker has duty `2/n`. All `n-1` blockers have total duty `2(n-1)/n>1` for `n>2`. Thus the averaging contradiction used at critical total duty one cannot simply be applied to the full system.

For even `n=2m`, the current chain theorem can handle `m` residual runners only after a window has been made safe for the other `m-1` relative constraints. More generally, choosing at most `floor(n/2)` residuals leaves at least `ceil(n/2)-1` core constraints. The hard question is whether those constraints can be selected and their windows placed so that the remaining residuals cannot cover them. Merely proving that the core has some positive interval is insufficient.

Even an inductive lower-runner theorem does not close this. Assuming LRC for `n-1` total runners, a core of `n-2` frequencies with maximum speed `c` has a witness at level `1/(n-1)`. The margin to `1/n` is `1/[n(n-1)]`, so Lipschitz continuity supplies a closed interval of length `2/[n(n-1)c]`. A final blocker has width `2/(nd)`. Therefore `d>=(n-1)c` is a sufficient fast-runner condition, including equality. This reproduces the standard fast-runner perturbation pattern credited to Kravitz. It leaves the comparable-speed regime. Proving that an additional configuration-dependent choice always resolves that regime is substantive new content.

A factorial move count is not the current bottleneck: reducing `23` again would not make a missing core window appear. No present evidence shows that such constant improvement would resolve a structurally new case.

## Equality already falsifies a tempting next step

For `C={1,4,5,6,7,11}` and `d=13`, the archived exact interval

`P=(220/17,196/15)`

contains `13`. Every positive **closed** core component is therefore strictly covered. The final safe set nevertheless consists of `1/8,3/8,5/8,7/8`.

Consequently, no theorem using only two positive windows can cover every admissible core. Neither can a larger collection made solely of positive components or subwindows: even the entire positive part fails on this example. A universal result must explicitly permit isolated core points and final threshold contacts. Adding more positive windows does not repair this obstruction.

The right branch structure is:

1. Disprove strict containment of at least one positive closed component, preserving endpoint-only survivors.
2. If all positive components are strictly covered, find a surviving isolated core point.

The second branch is not optional and cannot be represented by a positive integral. Tight configurations also prevent a universal positive-duration theorem for the full problem. Conversely, a zero integral or zero duration is not evidence against LRC.

There is a second quantifier trap. Two-time and two-window certificates can guarantee every phase of the final runner, while LRC only asks for the actual common-start phase. A universal all-phase assertion is stronger and requires its own proof. Certificate completeness for all-phase robustness is a characterization of that stronger property, not a proof that every common-start instance has it. Even without a counterexample to the stronger statement, adding it as a required bridge imposes an unearned burden.

## Manageable lemmas versus the original hard problem in new notation

The general-threshold form of the pair criterion is a manageable lemma. For every `n>2`, any two supplied positive core-safe intervals with parameters `D,G,w`, and every `d>0`,

`G<=((n-2)/2)w` and `d>=2/(nD)`

exclude strict blocking of both at every phase. Strict inequalities imply positive duration. One lap requires `dD<2/n`; different laps require `dG>(n-2)/n`; the wider interval requires `dw<2/n`. The two contradictions are exactly the existing `n=8` proof with its constants exposed. This is worth recording for portability, but it does not constitute a new bridge toward universal existence.

By contrast, let `S_C` be the full `1/n`-safe set of `n-2` arbitrary relative integer speeds, and let `d` be the omitted largest speed. The assertion

`for every C and d, S_C is not contained in the open blockers of d at phase zero`

is simply the selected-reference `n`-runner LRC expressed as a core-cover statement. Calling it a compatibility lemma does not make it easier. A meaningful intermediate theorem must impose a independently checkable structural condition and prove that condition in a broader class, or supply a genuine dimension reduction.

Likewise, “there is a bounded certificate” is weak without a discovery rule: one rational lonely time is already a small verifiable certificate whenever a witness exists. The contribution would be an arithmetic way to select it or a theorem forcing a specified certificate shape, not the existence of a short written witness by itself.

## Recommended allocation and a precise scalable target

First package the present mechanism into a compact, self-contained account: (i) averaging support and chain count, (ii) supplied-core window consequences, and (iii) final-runner lap compatibility with equality branches. Preserve the frozen computational record as evidence and avoid another succession of near-identical verification campaigns. Independent human mathematical review would be useful before promotion of any claim; this review does not authorize outreach.

Then shift the principal research question from a fixed numerical core to **arithmetic relation classes**. The fixed triple `1,4,5` already satisfies the low-complexity relation `1+4=5`. It is reasonable to ask what survives for `p,q,p+q` before claiming anything about arbitrary cores.

A precise candidate research target is:

> **Additive-core extension target — OPEN, not asserted novel.** For every total `n>=6`, assume LRC for `n-1` total runners. For every collection of `n-1` distinct positive integer relative speeds containing three speeds `p,q,p+q`, produce a `1/n`-safe time by an explicit lift from lower-dimensional data, allowing equality witnesses. The argument must be uniform in `p,q` and the other speed magnitudes.

This is an ambitious restricted induction statement, not a routine lemma. Its value would be a theorem uniform in `n` and in the core ratio. It would still leave relation classes other than the additive triple. A first proof attempt should isolate the proposed lifting step and attack that step, rather than “test the conjecture” on examples known to be lonely. No new calculation is requested by this recommendation.

The literature provides a sensible organizing principle, but not the desired lift. Beck–Everett's versioned abstract reports that a counterexample or tight instance with `k=n-1` frequencies must admit a nonzero integer relation of bounded `l1` norm, in particular at most `2k+3=2n+1`. This makes bounded relation types a motivated search space. Merely finding such a relation cannot finish the proof: the hard part is what each relation permits at the threshold. The full statement and proof must be audited before using that recent preprint as a theorem input.

A second alternative is contact geometry: classify how rational threshold contacts survive when a fast or exceptional speed changes. This matches the current equality-sensitive strengths and connects to established relative-spectrum methods. It should be pursued as a parameterized family or reduction theorem, not as a new visual language alone.

## Gates and abandonment criteria

| Gate | Required output | Stop or redirect when |
| --- | --- | --- |
| Package gate | One self-contained claim per result; exact quantifiers, equality handling, known inputs, and certificate records separated. | The supposed claim is only an already-known existence result with another finite check. Preserve it as exposition, not a breakthrough. |
| Necessity gate for any universal certificate | An explicit branch handling tight `13`, plus survival of strict `16` and the finite-anchor/lap obstruction. | It requires positive duration, finitely many input-independent anchors with bounded early laps, or only positive components. These are already refuted. |
| Scope gate | A statement permitting arbitrary core ratio or arbitrary `n`, with no hidden fixed `1:4:5` normalization. | A derivation still fixes the same old core and merely lowers a cutoff. Finish only if it materially simplifies the packaged proof. |
| Relation-class gate | A written, threshold-preserving lift or contraction for one declared relation type, including endpoints. | The argument stops at “there is a short relation”, or needs the very `n`-runner assertion it aims to prove. |
| First research-cycle exit | Either a complete restricted theorem, a concrete counterexample to its proposed lifting step, or a precise obstruction with a useful narrower replacement. | After one focused derivation/challenge cycle, progress consists only of renamed invariants, more examples, or a new fitted selector. Archive the obstruction and choose another relation or method. |
| Computation gate | A root-approved small protocol with a prediction that can distinguish two mathematical possibilities. | The run can only reconfirm known existence or increase agreement counts. Do not execute it. |
| Global-proof gate | An actual induction or exhaustive classification covering all permitted relative vectors, with equality and the standard real-speed/reference reductions stated. | A fixed-family finite reduction is being treated as a reduction of all LRC inputs. |

The fastest available falsifiers require no new computation: tight `13` eliminates positive-component completeness; strict `16` eliminates the specified coarse truncated-kernel route; the `q,8Bq` construction eliminates fixed rational menus with a fixed early-lap budget. Any replacement should explain explicitly which assumption it changes. Adding exceptions one by one without a theorem predicting them is a reason to stop that approach.

The fixed-family finite remainder should be kept as a possible later certification project, not the default mission. Published general finite-reduction theorems already show that finiteness alone is not the conceptual breakthrough. Exhausting this much smaller special-family box could complete a clean elementary account, but its scientific goal would need to be named in those terms.

## Sources and reading limits

Repository items read: `AGENTS.md`, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, `README.md`, current `HANDOFF.md` and `LR2_HANDOFF.md` entries, `RESEARCH_PLAN.md`, and the core-window, six-core, last-runner, short-kernel, two-time, finite-anchor-obstruction, and domain-connection notes. Exact counts above are taken from the archived notes, not independently recomputed here.

- Beck and Everett, *Lonely Runner Relations*, [arXiv:2609.06259v1](https://arxiv.org/abs/2609.06259v1), September 5, 2026: reopened and read the versioned abstract. Its HTML proof retrieval failed in this session. The relation bound is used only as a reported research lead here; no independent proof audit.
- Malikiosis, Santos, Schymura, *Linearly exponential checking is enough for the lonely runner conjecture and some of its variants*, [published article](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/linearly-exponential-checking-is-enough-for-the-lonely-runner-conjecture-and-some-of-its-variants/A51A991DE89B8C9C2E2FF13FBD4501DA), 2025, and [arXiv:2411.06903v1](https://arxiv.org/html/2411.06903v1): inspected the abstract and published finite-checking discussion; full reduction proof not audited. The general finite-checking precedent, rather than its constants, is the point used here.
- Jain and Kravitz, *Relative Lonely Runner spectra*, [arXiv:2411.12684v2](https://arxiv.org/html/2411.12684v2), December 9, 2024: read Theorem 1.1, Sections 1.4–1.6 and 2.1's proof outline. They provide structured parameterized spectra and rational-contact methodology; no claim is made that their theorem proves the proposed additive-core target. Frontier statements in the older introduction are not used as current status.
- The repository's September 29 six-core literature audit supplies the specifically credited lower-runner and Kravitz inputs. This strategy report did not independently re-audit their full proofs or the current maximum runner-count frontier.

Recommended next action: finish the compact mechanism package, then conduct one tightly bounded, noncomputational derivation/challenge cycle on a declared parameterized relation-class lifting step. Make equality handling and removal of the fixed core the acceptance criteria. Do not resume broad scans or constant polishing by default.

## Correction record

2026-09-29, root review: corrected the newly generalized pair criterion from `G<=(n-2)w` to `G<=((n-2)/2)w`. The safe gap has width `(n-2)/(nd)` and a blocking interval has width `2/(nd)`, so their ratio is `(n-2)/2`. At `n=8` this recovers the existing correct condition `G<=3w`; the earlier fixed-core theorem and its constants are unchanged. The initial generalization had a factor-of-two error.

The Beck–Everett v1 reading limit above records this reviewer's own inspection. The integrated team literature assessment additionally checks v2; consult that report for the updated source assessment.

### Late team finding: relaxed-torus existence is not the next open target

The arithmetic review supplies the following reduction, independently checked by the root. Let a rational relation nullspace `K` have dimension `ell>=2` and contain a positive speed vector with `k` coordinates. A rational vertex of `{w in K : w_i>=1}`, obtained by minimizing the coordinate sum on a compact sublevel, has at least `ell` coordinates equal to one. Merging repeated coordinates and clearing denominators leaves at most `k-ell+1` distinct positive speeds. The corresponding lower-runner theorem therefore gives a point in the relaxed torus with margin at least `1/(k-ell+2)`, strictly above `1/(k+1)`.

In particular, the team's P2 relaxation with `k=7` and `ell=3` has a `1/6` witness from the known six-runner case. Mere positivity or existence in this relaxed torus is consequently not an open primary research target. The literature review identifies explicit precedent in Allikvere v2, Lemma 3.3, crediting Giri–Kravitz; consult the team arithmetic and literature reports for the argument and source scope. Quantitative certificates or usable Haar-measure bounds may still help, but they require a stated application. The principal recommendation remains an actual-orbit-preserving lift, such as the declared additive-core extension target, with equality retained.
