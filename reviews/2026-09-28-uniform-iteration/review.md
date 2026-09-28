# Coordinator review and six-agent contribution record

September 28, 2026. Baseline `5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.

**Outcome:** a complete internal proof candidate for existence of a uniform
bound on advancing four-residual moves at threshold 1/8. There is no numerical
global bound yet. General statements stay **HYPOTHESIS** pending external
review. Finite calculations below are **OBSERVED**, not the proof.

## Independent assignments and resulting contributions

| Assignment | Contribution and recorded limit |
| --- | --- |
| Geometry | Actual-chain triple bound 7; explicit 175 advances for d>=4a; compactness and the local maximal-cycle contradiction. No number for the compact regime. |
| Adversarial construction | Attempted repeated itineraries fail by summed inequalities; no unbounded family found. Supplies independent periodicity/contact arguments. |
| Occurrence combinatorics | Disjoint-train commensurability, local adjacency stability, and square-free advancing-label words, including skipped laps. |
| Affine representation | Necessary and sufficient linear inequalities for a supplied full trace; exact word exclusions, local tiling-neighborhood bounds, and an alternative degeneration argument. |
| Literature / independent verifier | Known shifted threshold and chain precedents identified; later independently reconstructed the frozen auxiliary cases from protocol inputs. |
| Skeptical challenge | Independently checked recurrence, limiting equality contacts, the actual-chain175 bound, square-free lemma, and local-to-global compactness bridge. |

The agents communicated their results during the mathematical synthesis.
They are not six isolated proof certifications. The separately tasked
verifier did not read primary.py or results.json before completing its output.
The coordinator wrote the primary implementation, inspected the verifier and
proof notes, compared outputs, and assembled the final proof. All material
AI involvement is disclosed; no external reviewer has certified the result.

## Coordinator's mathematical checks

The proof bounds the actual selected intervals. It never silently replaces
them with an irredundant subcover. Removing occurrences of the slowest label
splits the selected word into strict subchains of the remaining labels, which
is the valid use of the triple bound.

The large-ratio overlap charge integrates over whole selected slow
occurrences, which are disjoint. It includes all fastest-runner blocking,
not only selected fast occurrences. The ratio f(x)/x is at least1/7 for
x>=1, with equality at x=7/4. The inherited potential allowance then gives
21 slow occurrences and175 total. This is conservative, not asserted sharp.

The compactness proof takes weak coverage at the limit, not continuity of
the projection algorithm. The potential is continuous on the phase torus
and has arbitrarily large simultaneous return times. Its monotonicity under
weak half-line coverage therefore forces multiplicity one almost everywhere.
Disjoint periodic trains have commensurable periods, giving a periodic tiling.

Only finitely many occurrence indices can enter a fixed padded horizon when
speeds remain in a compact positive range. Around each tiling contact, every
other occurrence is a positive distance away. A nearby **open cover of the
entire contact neighborhood** therefore forces strict overlap of the two
incident occurrences. Covering just the original contact point would not
suffice. All four candidate cycle anchors are included before choosing the
runner maximizing q_i*p_i'. That makes the mean-versus-maximum contradiction
valid despite the maximizing runner depending on the perturbation.

For square-freeness, q_r distinct new occurrences imply endpoint displacement
at least q_r*p_r. The summed facing-endpoint gaps are all positive and
telescope to at most mean(q_i*p_i)-max(q_i*p_i). These gaps need not equal
intersection lengths when intervals contain one another; only their
positivity is used. No common-start or integrality assumption is smuggled
into this auxiliary-phase lemma.

The full argument supplies an existential constant. It does not supply an
explicit global step cap, a bit-complexity bound, a successful core window,
or full-conjecture coverage. All seven full-system blockers at 1/8 have duty
sum7/4, so the critical four-blocker reasoning does not directly apply.

## Frozen exact checks

Protocol SHA-256:
`f0ddb7b2f82af5e812d1b2c31a012e3119fe90e67d209bf664ea0f2e395f9fa2`.

The protocol was frozen after the analytical candidate and before its new
coordinator/verifier calculations. It contains three canonical auxiliary
tilings and four prescribed perturbations per tiling, with the exact version
retained:15 windows. These are constructed calibration fixtures, not a
random or held-out sample. No new physical common-start configuration was
introduced.

| Comparison | Result |
| --- | --- |
| Auxiliary windows | 15/15 agree on the earliest safe time |
| All scalar calls | 99 agree, with9 advancing calls |
| Anchored affine cycle identities | 60 agree in both coefficients and evaluated signed gaps |
| Scalar occupancy fixtures | 4 agree; equality at x=7/4 |
| Compared fields | 1489 |
| Full threshold partition | 342 points,327 open cells,207 safe components |
| Exact tiling contacts | All retained as isolated safe points |
| Longest moving word in these fixtures | Two letters; this is not a stress test of the general square-free claim |

The cycle gaps are signed predictions for the inherited tiling order.
They are not all positive, and are not being represented as realizable
strict chains. A nonpositive gap at a maximal-cycle anchor is the intended
obstruction. Full safe sets come from the independent verifier, not from
assuming those signed cycles are the actual selector itinerary.

The affine agent also chose an ancillary check before running its own script:
the three exact tilings and the previously preserved distinct auxiliary
33-call trace. It reproduces seven moves with word C,A,D,B,C,D,A and final
time38325/44704. The coordinator reran this script and checked that the
seven-letter word has no immediate repeated block. This is separate from
the fifteen-case frozen protocol and adds no physical input.

## Literature and preservation

The bounded audit inspected primary sources only. It credits the known
arbitrary-phase1/(2k) existence statement and Rifford's compatible periodic
chain framework. The latter's irredundant chains are not automatically the
same as the actual selected chain. No paper inspected in this bounded audit
was found to state the exact uniform projection-count result; this does not
establish novelty or literature-wide openness.

The previous speed-dependent result is preserved, with its historical
uniform-bound question answered only at proof-candidate level by this note.
The next milestone is explicit extraction in the comparable-speed regime,
with external mathematical review and novelty comparison still outstanding.
Hourly research remains paused; no broad scan, paid compute, outreach,
all-reference campaign, main merge or parked+7/+9 continuation occurred.
