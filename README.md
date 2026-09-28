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
| [CLAIM_STATUS.md](CLAIM_STATUS.md) | Evidence/status vocabulary used throughout the project |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to investigate, challenge, reproduce, and submit work |
| [notes/MATHEMATICAL_BASELINE.md](notes/MATHEMATICAL_BASELINE.md) | Definitions, exact checks, normalization, and test fixtures |
| [notes/SOURCES.md](notes/SOURCES.md) | Dated literature starting points and verification limits |
| [AGENTS.md](AGENTS.md) | Instructions for AI collaborators |

## Current state — September 27, 2026

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
