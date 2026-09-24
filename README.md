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
| [RESEARCH_PLAN.md](RESEARCH_PLAN.md) | Strategy and research method |
| [CLAIM_STATUS.md](CLAIM_STATUS.md) | Evidence/status vocabulary used throughout the project |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to investigate, challenge, reproduce, and submit work |
| [notes/MATHEMATICAL_BASELINE.md](notes/MATHEMATICAL_BASELINE.md) | Definitions, exact checks, normalization, and test fixtures |
| [notes/SOURCES.md](notes/SOURCES.md) | Dated literature starting points and verification limits |
| [AGENTS.md](AGENTS.md) | Instructions for AI collaborators |

## Current state — September 24, 2026

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
