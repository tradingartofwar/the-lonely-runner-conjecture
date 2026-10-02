# Sheet coverage: the missing time matters more than the menu ranking

October 2, 2026 UTC. Completed frozen comparison and exact constructed counterexample. AI-derived general arguments remain proof candidates awaiting independent review.

**The main finding:** all 36 inherited sheets fail for (p,q,r)=(1,2,40), even though t=25/152 is physically 1/8-safe. The sheets offer only the three pair-contact times 1/8, 7/40 and 3/8; speed 40 puts the new runner at phase zero at every one. Thus keeping more of these same sources cannot yield uniform coverage. The [full report](../reviews/2026-10-02-cc-sheet-coverage/RESULTS_REPORT.md) preserves the complete exact diagnosis, finite test and limits.

This resolves a more specific question than Lonely Runner: whether the supplied certificate class can retain the times needed after an independently chosen runner is added. It cannot do so uniformly. This does not establish failure of other sheets, necessity of a three-dimensional cell, or a physical counterexample.

## Exact coverage criterion

The [derivation](../reviews/2026-10-02-cc-sheet-coverage/DERIVATION.md) retains the existing saturated orbit relation and inverse physical clock. After primitive normalization, let d be the gcd of the first two speeds. A nonconstant first integer contact fixes a point in the base segment. Its second projected range has width 3d/4.

- If d>=2, that width guarantees a second integer contact. A first contact is still required.
- If d=1, the third runner's fractional phase must fall in [1/8,7/8]. An exact modular-count formula decides this and recovers a contact using standard Euclidean floor sums.
- Constant first projection uses its full second-coordinate interval, including point and equality cases.

All eight old menu misses fall into the coprime phase-obstruction case, with other selected sheets lacking first contacts. The new kernel matches all 14,652 archived sheet bits. This changes the decision procedure, not the underlying source coverage. No runtime advantage or novelty is claimed.

## Fresh finite comparison

Freeze `afc11e6aae4dad703aac7a587311790572268752` was published and fetched before testing. All 407 earlier primitive triples in [1,9]^3 became development data. The fresh domain contains all 643 admissible primitive triples in [1,12]^3 outside that old box.

| Source selection | Development | Fresh |
| --- | ---: | ---: |
| Original four sheets | 399/407 | 639/643 |
| Revised four-sheet prefix | 401/407 | 640/643 |
| Revised seven sheets | 407/407 | 641/643 |
| All 36 sheets | 407/407 | 643/643 |

The seven-sheet menu fits all development cases but does not transfer completely. It misses (1,6,10), recovered by an omitted source at t=3/16, and (4,1,11), recovered at t=33/104. The latter is a new loss relative to the old four-sheet menu. Keep both; do not repair this holdout and call the repair transfer success. Seven versus four also changes the realized budget.

The alternate physical-time checker agrees on all 23,148 fresh sheet bits, checks 1,301 saved witnesses and 576 source endpoint bands. All three output files reproduce byte for byte. The arithmetic implementations and analysis share an AI author; separate-agent, human and formal review remain open. Finite-box coverage does not override the constructed all-36 failure outside the box.

## An interval survives the source-class failure

For p=1,q=2, the first eight moving speeds are safe throughout

\[
I=[25/152,7/40],\qquad |I|=1/95.
\]

The general argument extends the source failure to r=40k, k>=1: every inherited contact is a zero phase for the new runner. But the largest unsafe time gap of that runner is 1/(160k), shorter than I. The explicit formula in the derivation recovers a safe time inside I for every such k. Its unbounded conclusion remains a proof candidate; the k=1 counterexample and witness are exactly checked by both the sheet and physical-time paths.

A direction-aligned base segment {(t,2t):t in I}, crossed with the safe third-coordinate interval, retains these needed choices. It is still a sheet, but it holds a continuous interval of actual-orbit contact. It was not added to the frozen comparison. This distinguishes inadequate source selection from inadequate source geometry.

**Next:** develop that parameter-dependent source construction, with a clear split between positive-duration and isolated-only core-safe sets. Start from the r=40k obstruction and the two new compact-menu misses as development evidence. Freeze a new domain and budget before comparing it against full physical-time recovery. Do not launch another ranking adjustment of the same 36 sources as if it could solve the structural limitation.

The richer source and recovery map are the pinned full physical safe intervals and their lap bands; the current short record supports one verified time from a supplied sheet. It omits the complete safe xy region, arbitrary mixed-r constraints, other reference runners and optimization/all-witness questions. These remain separate obligations.
