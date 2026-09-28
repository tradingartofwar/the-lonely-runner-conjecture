# Adversarial review: what a forced-overlap query can establish

September 28, 2026 UTC. Baseline `c1e88837c8d48954b0de217d857d0bd6ac9cbccf`. Frozen scope: `protocol.json` in this directory, three supplied controls, reference 0, eight common-start runners, threshold 1/8, core {1,4,5}, J=[9/32,3/8]. AI-assisted mathematical and prior-coverage review, not independent human certification. No new speed input, alternate window, external literature search, or remote write was performed by this reviewer.

## Quantifiers and certificate validity

Let P be the nonnegative 16-state mass polytope with the supplied total, four singles, and six pair moments. It is a relaxation of runner geometry. Its compactness follows from nonnegative masses with fixed finite total. Let F be its face x_empty=0. A feasible point in F represents complete coverage **up to measure zero**; it does not settle whether isolated safe times survive.

If minimizing x_empty over P gives zero with an exact primal certificate, F is nonempty. For a triple A, minimize its inclusive intersection mass T_A over F. An exact primal and dual certificate for a strictly positive optimum m_A establishes that EVERY compatible abstract zero-duration cover has T_A >= m_A. A physically derived upper bound T_A <= h < m_A therefore rules out all of F, not merely a displayed artificial countermodel. The physical state table remains feasible in the constrained P; by compactness its minimum empty mass must be positive. A further exact optimum certificate supplies the quantitative bound.

The inclusive triple counts the four-way state. It must not be confused with the exact-three state. If h=m_A, no contradiction follows. If all m_A are zero, each triple can separately be avoided by some cover, but different triples may require different covers. The quantifiers do not imply a single cover avoids all triples. Collective quantitative obligations remain possible. None of these implications assumes abstract tables are realized by common-start runners.

## Direct strict16 algebra

Write a=6,b=7,c=11,d=16 and C=L-sum D+sum O. The supplied zero pairs O_ab=O_bd=0 imply, by nonnegative masses, that every state containing ab or bd has zero mass. Consequently all triples except acd are zero, and the four-way mass is zero. Inclusion-exclusion reduces identically on the entire pair-compatible polytope to

    x_empty = C - T_acd.

The archived data give C=1/896. Thus every point of F has T_6,11,16=1/896. The other three triple minima are zero; choosing the largest positive minimum has a unique candidate. This supplies a simple universal explanation for the selected query independent of LP basis discovery.

Geometry supplies the already-known exclusion. On J, simultaneous blocking by 6 and 11 has endpoints 31/88 and 17/48. Multiplying their closed span by 16 gives phase in [7/11,2/3], wholly within (1/8,7/8). Runner 16 cannot block there, even at the endpoints. Hence T_6,11,16=0 and x_empty=1/896 for every compatible table respecting this bound. The physical positive interval was already known. The rule's outcome is a reproduced explanation and explicit selection trace.

## Tight13 and doubling112 guard against false extensions

For tight13, the zero pairs are 6/7 and 11/13. Every triple contains one of these pairs, so all triples and Q are already zero from pair information. The archived C is zero, so the pair polytope fixes x_empty=0. No physically valid higher-duration restriction can force a positive duration for this physical control. At t=3/8, the seven distances for speeds 1,4,5,6,7,11,13 are respectively 3/8,1/2,1/8,1/4,3/8,1/8,1/8. The endpoint is valid and isolated: speed 11 blocks immediately to its left, speed 5 immediately to its right. The direct endpoint check is a separate information channel.

For doubling112, the archived pair optimum is already 761/32256>0. Escalating to geometry would violate the frozen early-stop rule. The archived physical four-way duration is 1/896 and every triple has positive duration. Those facts must remain visible as diagnostics, because replacing all higher intersections by zero would be false. This control validates a pair-only success path; it does not test the higher-order query selector.

## Prior coverage and remaining weakness

The September 25 sparse selector already chooses useful compatibility graphs from two triple tests in the fixed 6/7/11/w family. The two-speed transfer adds a prescribed J/H dispatch. The four-blocker cycle note already permits quantitative higher-intersection upper bounds and records genuine nonzero triple/four-way overlap for doubling112.

More strongly, `reviews/2026-09-27-ultra/optimization.md`, sections 2–3, already describes the 16-state relaxation, the strict16 single-exclusion repair, its exact value, and a complete two-coordinate formula when blockers 6 and 7 are disjoint. It also records pair optima for all three present controls. The present bounded increment is a frozen prequery decision process based on obligations across the whole zero-duration-cover face, accompanied by a cost and certificate trace. It is not a new repair, pair-optimization method, family-coverage result, or novelty claim.

The three controls do not test ranking among multiple strictly positive triple obligations. They do not test a selected triple with positive physical duration, nor a physically strict pair-feasible control in which every individual triple minimum is zero. In strict16 the only positive candidate is forced by pair support. Thus these outcomes cannot support a general guarantee for the maximum-forced-mass ranking or its cost effectiveness. A large forced mass need not be easier to bound geometrically than a smaller one; without querying geometry, the ranking does not know the useful gap m_A-h_A.

A coherent next bounded algebraic investigation would freeze an abstract pair-compatible zero-duration-cover polytope in which every triple can separately have zero mass but their sum has a positive minimum. A symmetric moment construction with Q=0, nonnegative exact-state constraints, and alternative allocations of fixed positive triple mass is a candidate route. This is a proposed investigation only, not a newly calculated control or claim of physical runner realizability. It would test individual versus collective obligations before any new physical speed search.

## Review scope

Read the repository governance and current handoff/queue, the frozen protocol, sparse and two-speed selectors, cycle corrections, one-pair policy, September 25 obstruction and September 27 optimization analysis. The direct arguments above check the quantifiers, strict16 forced intersection, tight13 endpoint channel, and proper prior attribution. Computational result/code review is recorded below after those artifacts become available.

### Completed computational and manuscript review

Reviewed `primary.py`, `verify.py`, `results.json`, `verification.json`, and the draft `notes/COVER_OBLIGATION_SELECTION_2026_09_28.md`. Ran both read-only commands successfully:

```bash
python -B reviews/2026-09-28-cover-obligations/primary.py --check
python -B reviews/2026-09-28-cover-obligations/verify.py --check
```

The primary's equality and inequality sign conventions are sound: for a minimization, inequality multipliers are nonpositive and the dual weighted columns lie below the objective. All twelve archived optima have exact feasible primals, exact dual inequalities, and equal objectives. Floating-point support selection is only proposal machinery and fails closed under exact reconstruction. No optimizer is used by either check command.

The selection uses only the supplied pair moments and cover minimizers. It does not inspect triple durations before choosing mask 13 in strict16. The primary stores the individual and pair interval lists used to calculate its supplied summaries; those are real computation costs, not free inputs. Its selected geometry check then intersects only one chosen pair list with the third blocker. The independent verifier reconstructs all sixteen state masses from 74 exact threshold cells on the three authorized windows and checks the cover-face values independently using zero-pair algebra. This is a separately structured computation, not independent human validation.

Observed decisions match the direct arguments above: strict16 baseline 0, selected mandatory triple 1/896, actual triple 0, repaired minimum 1/896; doubling112 pair-only minimum 761/32256 with no escalation; tight13 all four compulsory triple minima zero and a valid isolated endpoint. The diagnostic doubling112 moments retain four positive inclusive triples and Q=1/896. The aggregate primary record charges twelve LP certificates/solves at generation, eighteen pair queries, seventy-five candidate laps, forty-two individual interval pieces, 107 pair intersection comparisons, one selected triple query with two comparisons, and one endpoint query. Read-only replay checks these decision and cost records without calling a solver.

No fatal defect was found within this frozen scope. The draft note appropriately identifies the repair as prior work, distinguishes measure from equality points, and preserves the untested ranking and collective-obligation limitations. A zero pair optimum is not itself a statement that physical duration is zero; only tight13's extra zero-pair algebra makes that stronger conclusion here. No claim beyond the three named configurations has been numerically tested in this round.
