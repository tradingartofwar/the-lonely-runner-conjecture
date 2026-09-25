# Early-family proof review

Reviewed working source corresponding to PR #3 commit `ea482f54edae4775621bc69c1fb7359291f31ddd`, September 25, 2026. The parent reviewer independently matched the substantive working files to that live Git tree; local HEAD was not used to establish currency. This is an AI review, not formal verification or an external mathematical referee report. No repository file was edited and no experiment output was regenerated in place.

## Conclusion and severity-ranked findings

**No correctness defect or missing unbounded case was found in the one-variable family, the two-variable family, or the fixed 6-to-12 replacement classification.** The endpoint distinctions and finite-remainder coverage are sound. The foundational interval-overlap identities and the eight prescribed blocking-chain certificates also survived independent exact reconstruction.

- **Critical/high:** none found in this scope.
- **Medium:** none found in this scope.
- **Low, exposition only — make the continuity step explicit in the replacement classification.** `notes/TIGHT_CASES_4_8_12.md:91–100` correctly obtains `6|w` and `w<=15`, hence `w=12`. Strictly speaking, tightness forces `||wt||<=1/8` on the *interior* of `J1`, because the retained core is strictly safe there. Continuity then forces the same inequality on its closure. Stating that one sentence would distinguish this upper-bound problem from the later nonexistence reductions, which require a closed allowed interval to be covered by *open* blocking sets. The proof's conclusion is unaffected.
- **Low, consolidation only — use the explicit one-variable formula as the main proof.** `notes/VARIABLE_SPEED_FAMILY.md:66–90` supplies a shorter complete argument than its preceding width reduction: the modulo-8 test, the modulo-7 test, and the escape time already exhaust the domain. Retaining the width proof as motivation/comparison is useful, but it is not an additional required verification step. This is not a defect.

No novelty determination is made. The Fibonacci plateau formula and limit are known results, explicitly identified as such in the repository and independently matched to the primary sources during this review.

## Audit of the unbounded arguments

### One variable speed

Scope: `{0,1,4,5,6,7,11,w}`, distinct positive integer moving speeds; selected reference 0; threshold 1/8.

The interval phase certificate at `VARIABLE_SPEED_FAMILY.md:22–40` is correct. For the fixed six, every phase stays in one integer cell and in `[1/8,7/8]` throughout `[17/56,5/16]`; every phase is strict in its interior. The piecewise witness at lines 84–88 is exhaustive:

1. `8` not dividing `w`: `t=1/8` works by nonzero residues modulo 8.
2. `8|w` but `56` not dividing `w`: at `17/56`, the moving phase is `17m/7`; its nonzero residue has distance at least `1/7>1/8`.
3. `56|w`: `t=17/56+1/(8w)` lies strictly inside the core interval because the delay is at most `1/448<1/112`, and the new runner has phase exactly `1/8`.

The earlier finite reduction also works independently: a connected closed interval contained in a union of disjoint open single-runner windows must lie wholly in one window, so its length is strictly less than `1/(4w)`. This leaves only 8,16,24 after the modular restriction. No implicit finite scan or uniform fixed-time assumption remains.

### Two variable speeds

Scope and ordering at `TWO_VARIABLE_SPEEDS.md:9–16` are precise and do not change the original count when constraints are temporarily removed.

The local duration inequality at lines 57–65 is valid for every starting phase, including a residual arc that wraps around the blocking interval's period. An arc shorter than one period sees at most the full blocked measure `1/4` in phase units, and at most its own length `r`, hence `min(r,1/4)`. Thus the `3/(16v)` error is justified; it is not a mistaken assumption that every local interval is one-quarter blocked. In fact the constant is sharp uniformly over interval phase and remainder length: take `r=1/4` aligned with a blocking arc.

At `x,y>=34`, the clear-duration lower bound is exactly `1/7616>0`. Positive measure guarantees a witness and, here, even strict times away from the finitely many boundaries. No explicit fast-case witness formula is required for the existence conclusion.

The remaining strips are exhaustively covered. I independently checked all 28 displayed `x` values are exactly the admissible positive integers below 34, verified every `J_x` by affine rational inequalities, recomputed every strict cap on `y`, imposed `y>x`, core exclusions and `8|x or 8|y`, and recovered exactly the listed eight pairs. All eight supplied point witnesses meet the recorded minimum and strictly exceed 1/8. Integer caps use the correct strict inequality even when the rational cap is integral. The tight `(11,13)` control is consistent with, and does not contradict, the strict witnesses for the residual pairs.

### The fixed 6-to-12 replacement

At `TIGHT_CASES_4_8_12.md:76–100`, independent threshold-boundary reconstruction returned precisely the stated four singleton points and the two closed intervals for core `{1,2,3,4,5,7}`. Its interior is strictly safe. At `t=1/6`, an integer replacement can prevent improvement only if `6|w`. The closed weak blocking neighborhood centered at this collision must reach `7/40`; its right extension is `1/120`, giving `w<=15`. Distinct faster admissible replacements are `w>7`, so 12 is the unique possibility. Direct endpoint phase inequalities verify it covers both openings while the four old equality times survive.

The fixed-case conclusion does not depend on the cited broader Goddyn–Wong acceleration criterion. That general criterion was not independently audited here; attempts to reopen the cited survey/S8 URLs failed. This retrieval limitation does not undermine the self-contained fixed-case proof.

## Foundational overlap and chain arguments

`BLOCKING_OVERLAPS.md:9–32`: the signed facing-endpoint gap is correctly `(n(aq-bp)-(a+b))/(nab)`. Its sign detects overlap even under containment; the note correctly avoids treating its negative value as intersection length in that case.

`BLOCKING_OVERLAPS.md:50–62`: the necessary `n|(a+b)` condition at an exact threshold maximum is sound for `n>=3`. Active distance curves are locally affine because the maximum is strictly between 0 and 1/2. Some active slope must increase and some decrease; otherwise moving in one direction raises every active curve while inactive ones retain positive margins. The associated facing endpoints give the divisibility. This is necessary only; it supplies neither the desired lower bound nor a tightness classification.

`BLOCKING_OVERLAPS.md:64–80`: `R=(n-2)/n+U` follows directly by integrating `M=1_{M>0}+(M-1)_+`. It uses the original competitor count, with multiplicity if equal absolute constraints arise. As used in these cases, all seven relative speeds are distinct. The separation of measure-zero safe contacts from empty feasibility is correct.

`BLOCKING_CHAINS.md:87–129`: strict overlap is the right edge relation, and monotonic advancement of the right endpoint makes the graph acyclic. The standard greedy exchange argument remains valid for open intervals because eligibility is strict after the first step. Windows cannot bridge separate blocked components across allowed endpoints, so componentwise minima sum to the stated global minimum cover. I independently rebuilt the full allowed sets and used breadth-first graph reachability to recover all 46 component minima across the eight prescribed cases, rather than invoking the repository's greedy/DAG routines. The 21 sole-blocker witnesses are valid strict witnesses for all other constraints.

The `13→8` example really blocks every rational denominator at most 8, since a present speed is divisible by every such denominator, while `4/13` remains valid. This is a sound counterexample to reliance on the old small-denominator witnesses, not evidence that all configurations with that divisibility pattern are safe.

## Fibonacci: known formula versus reconstructed explanation

The status distinction in `FIBONACCI_CHECK.md:7` and `FIBONACCI_RECURRENCE.md:5–7,171–175` is correct. Directly retrieved:

- Victoria Zhuravleva, *Diophantine approximations with Fibonacci numbers*, arXiv:1112.6142v1, PDF Theorem 1 and Corollary 1, printed page 3: https://arxiv.org/pdf/1112.6142 . For largest Fibonacci index `N`, let the paper's stage be `h=floor((N-2)/4)`. The maximum is `F_(2h+1)/(F_(2h+2)+F_(2h+4))`; putting repository `m=h+1` gives `F_(2m-1)/L_(2m+1)` and the claimed four-index plateaus. Theorem 2 gives the stated limiting witness.
- Ram Krishna Pandey, *On Some Magnified Fibonacci Numbers Modulo a Lucas Number*, Journal of Integer Sequences 16 (2013), Article 13.1.7, Theorem 5, printed page 6: https://cs.uwaterloo.ca/journals/JIS/VOL16/Pandey/pandey7.pdf . This supplies the modular witness, not by itself optimality. The repository correctly notes the endpoint-order error: modulo 11, the speed-3 product is 9 and the speed-8 product is 2, reversing the stated “respectively.”

The repository's upper-bound subset and recurrence reconstruction remain its explanatory derivation of a known formula. I read the induction and witness logic and found no immediate contradiction; the assigned scope here was primarily known-versus-candidate classification, so this report does **not** claim a complete independent audit of every Fibonacci recurrence identity or either published proof. The original bounded note's unresolved statements are expressly superseded by its opening update; they should not be cited in isolation as current status.

## Reproduction and coverage limits

Independent verifier: `reviews/2026-09-25-ultra/early_check.py`.

Run:

```bash
python reviews/2026-09-25-ultra/early_check.py
```

Result: PASS. It imports no repository checker or experiment helper and writes no tracked data. It checks 28 affine intervals, exact enumeration of the eight residual pairs, eight residual witnesses, fast-bound arithmetic, nine one-variable diagnostic witnesses including the large integer, the replacement core's complete allowed set, eight chain cases/46 component minima/21 sole blockers, and all seven overlap schedules and aggregate accounting identities. Full allowed sets are reconstructed from all exact threshold-status boundaries and their open cells, retaining singleton boundaries.

This bounded verifier checks certificates; the written modular, connectedness and periodic-duration arguments supply the unbounded logic. This review is selected-reference only, does not re-audit the general rational/integer reduction, does not certify the full 179-case experiment or all historical maxima/all-reference tables, does not examine later overlap/tiling families, and is not a broad literature or novelty search.

## Common mechanism worth preserving

The strongest early result is a compact, complete finite-reduction pattern: a positive-width core opening prevents a sufficiently fast single blocker from covering it; with two blockers, a local periodic measure estimate first forces one to be slow, then each slow value restores a one-blocker width bound. Modular witnesses reduce the finite residue set further. Exact endpoint handling distinguishes existence at equality from strict positive-duration survival.

This mechanism is mathematically sufficient for these families, and the separate phase certificates make the finite remainder inspectable without trusting the search that originally selected it. The useful next editorial step would be to extract two general elementary lemmas—one-runner connected-interval coverage and local periodic blocking measure—and present these families as concise applications. No additional search is needed to support the audited conclusions.
