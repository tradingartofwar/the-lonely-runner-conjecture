# Adversarial review: physical windows and collective cover obligations

September 28, 2026 UTC. Baseline `60f1665e92b54c3117fd73f5b83542c424dc9f21`. AI-assisted review of the frozen protocol in this directory; not independent human mathematical validation. This reviewer owns only this report. No new speeds, windows, subdivisions, all-reference search, remote writes, or external literature claims are authorized by this review.

## Frozen question and quantifiers

For a selected physical window, let P be its nonnegative sixteen-state mass polytope with total, single and pair moments fixed, and let F be the face U=0. The test requires actual physical U>0, a pair-only optimum of zero (so F is nonempty), and, separately for every inclusive triple K, min over F of T_K equal to zero.

The four minimizing covers may differ. Four zero minima mean “for every K there exists a compatible cover avoiding K,” not “one cover avoids all K.” An exact nonnegative primal attains each zero; a nonnegative objective supplies the corresponding lower bound, or the archived exact dual can certify it. Inclusive triples contain the four-way state; exact-three atom masses are different coordinates.

The collective interpretation does not require another optimization. Write H=sum of inclusive triples minus Q. Equivalently H is the sum of exact-three atom masses plus 3Q, hence H>=0. Inclusion-exclusion gives C=U+H, with C determined by pair data. Actual U>0 implies C>0. On every compatible cover, H=C>0. Thus a qualifying row would have a compulsory collective burden and no individually compulsory triple, exactly as requested.

A “physical counterpart” here would supply one actual common-start runner window with positive duration and an abstract compatible cover family with the stated minima. It would not supply a second physically realized runner configuration having the same summary and zero duration. The optimization never imposes integer-speed realizability, shared-clock interval order, or common-start phase equations on its alternative mass tables.

## Archive selection and counting

The source study fixes six speed configurations, reference 0, thirty-five labelled three-runner cores per configuration, and complete closed core-safe components in [0,1]. The eighteen records are components with actual duration positive and the archived reduced optimal-tree bound nonpositive. The archived full and reduced bounds agree throughout that study. Since any valid tree bound is a consequence of the same full pair moments, a positive tree bound precludes a zero pair-only optimum. This makes the retained misses an appropriate finite domain for the proposed obstruction; it does not make these configurations representative of arbitrary speeds.

The source archive contains per-core summaries and component digests rather than a full list of every missed component. The implementation must therefore document the archival reconstruction needed to identify those records, not imply that reading eighteen existing explicit rows was sufficient. Replayed source records must match the pinned algorithm/archive, and the selected identities and counts must match the protocol. Reconstructing candidate rows for identification must be separated from the number of new LP inputs.

Eighteen labelled core/component records are not eighteen independent physical examples. Distinct cores may select the same closed time interval of the same configuration and may leave different residual labels or moment models. Reflected intervals are linked by common-start symmetry. Report records, repeated (configuration, window) identities, and any reflection grouping separately; preserve all eighteen records under the protocol's no-deduplication rule. Do not turn repeated certificates into evidence of a higher success frequency.

## Endpoints and finite scope

The target requires strictly positive actual duration, so singleton-only windows cannot qualify and may not be smuggled into the search as successes. Zero optimum means a cover in measure, not the absence of every valid time. The separate tight13 control must retain its valid isolated endpoint 3/8. Strict blocking uses distance <1/8 and safety uses >=1/8. Threshold-cell interiors recover duration, but endpoint validity requires a separate exact check when stated.

A negative result would establish only that the specified eighteen archived records fail this conjunction. It would not rule out collective-only physical counterparts in other windows, speed inputs, references, or numbers of blockers, and it would not prove completeness of a mandatory-single-triple selector. Conversely, a positive forced triple minimum alone would not prove that measuring this triple repairs an actual window: that requires a physical upper bound strictly below the minimum. The frozen experiment does not select or test such repairs after inspecting outcomes.

## Prior coverage

The prior collective-obligation note already supplies an abstract symmetric example with separate zero triple minima and positive collective burden. This run tests its occurrence in an existing physical archive; the abstract distinction and inclusion-exclusion identity are not new discoveries.

The sparse-overlap selector already uses two speed-derived triple exclusions in the fixed 6/7/11/w family. The two-speed transfer already provides its alternate-window route, and the cover-obligation study already identifies the strict16 forced triple and known zero-overlap repair. The doubling112 control already has a positive pair-only optimum while genuine triple and four-way overlaps occur. Replaying these three controls calibrates the implementation and guards interpretation; it adds no new physical configurations and does not count toward the eighteen-window search.

## Completed calculation and independent-verifier review

Reviewed the frozen protocol, current collective-obligation note, team-transfer note, source reconstruction/archival organization, current `primary.py`, its exact LP helper, `results.json`, `verify.py`, and `verification.json`. Ran both read-only commands successfully:

```bash
python -S -B reviews/2026-09-28-collective-window-audit/primary.py --check
python -S -B reviews/2026-09-28-collective-window-audit/verify.py --check
```

The locator work is explicit and matches the archive: five flagged cores, 209 reconstructed components, all five historical component digests equal, exactly eighteen selected records. The five cores contribute 8, 2, 2, 2, and 4 misses respectively: Fibonacci indices [1,2,4]; Squares [1,2,5] and [1,3,4]; Prime powers [2,3,4]; Perturbed chain [1,2,4]. The other source cores were not subjected to new LPs. No new core, speed, or window was introduced.

The primary uses interval geometry from the pinned source and the existing exact acceptance routine for LP proposals. The separately structured verifier imports neither primary nor its LP helper: it locates source components by rational threshold events, computes maximum spanning trees with Kruskal, and solves every new optimum with an exact two-phase simplex. It generates its own rational primal and dual certificates and checks the primary certificates. All fifty-eight new-case optima agree: eighteen pair baselines and forty cover-triple minima. Eleven additional control optima are independently solved; the archived strict16 repair certificate is separately replayed. The three controls remain outside the search count.

The independent source locator uses 1,505 threshold cells over the 209 archived components. Its full-state verification uses 262 cells on the eighteen selected windows only. State masses, all sixteen moments, actual positive durations, core/component identities, tree bounds, and every claimed optimum agree. All exact certificates have feasible nonnegative primals, valid dual column inequalities, and equal objectives. Numerical optimization is not used by either read-only check; the independent verifier instead performs exact LP optimization.

Eight of the eighteen records have a positive pair-only optimum, so no individual-triple optimization is performed for those records. Ten have pair-only minimum zero. Eight of those ten have at least one positive forced triple minimum; the remaining two have all four minima zero. A positive forced minimum in those eight rows is a cover obligation only: this run does not select a triple or test a geometric repair for them.

## Accepted positive counterpart, and its precise consequence

The two qualifying records are the same reflected mechanism in the existing configuration

    {0,7,8,15,23,38,61,100}.

The core is {7,8,23}, leaving residual speeds {15,38,61,100}. The windows are [33/184,39/184] and [145/184,151/184], exchanged by t -> 1-t. Their labelled moment vectors agree. Each has actual uncovered duration 1/600, pair-only optimum zero, and four separately attained zero cover-triple minima. There are eighteen distinct (configuration, window) identities and no duplicated interval under different cores in this particular result, but all eighteen records form nine reflection pairs. Thus the two successes are one reflection class, not independent discoveries.

This is a physical counterexample to completeness of a selector limited to asking for a strictly positive individually compulsory triple. More sharply, no physically valid upper bound on just one inclusive triple can eliminate every abstract cover compatible with these pair moments: that triple has a compatible cover attaining zero, which satisfies any nonnegative upper bound. The proof uses the archived zero-minimum primal for each possible triple and does not require another geometry query.

That last conclusion concerns a single **upper-bound** restriction. It does not address an exact equality to a measured positive triple duration, a lower bound, multiple simultaneous restrictions, pointwise endpoint facts, or another time window. The underlying full configuration was already known to have lonely intervals; this diagnostic adds neither existence coverage nor an LRC counterexample. It exposes a physically realized failure of this particular compressed inference method.

The actual triples and Q are retained solely as diagnostics on the selected windows. Their already-defined combination H=sum T-Q may be used to explain the inclusion-exclusion identity, but must not be presented as a newly added selection statistic, extra optimization, or performed repair. No collective LP or combined-statistic query was run. Computing H exactly would merely reconstruct C-U and would not establish a cheap general way to discover the opening.

No fatal mathematical or computational defect was found within the frozen scope. Acceptance here means reproducible bounded AI-assisted evidence with separately structured exact calculations, not independent human certification, novelty, a general geometric exclusion theorem, or an all-reference conclusion.
