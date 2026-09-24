# Contributing

Thank you for helping investigate the Lonely Runner Conjecture.

The project welcomes professional mathematicians, students, programmers, independent researchers, curious outsiders, and AI-assisted teams. Credentials are not a prerequisite. Evidence is.

## The normal contribution path

Once the repository is public:

1. Fork the repository.
2. Create a branch in your fork.
3. Make a small, inspectable change.
4. Run or reproduce the relevant checks.
5. Open a pull request against `main`.

You do not need direct write access to the canonical repository.

## Before proposing a result

Read:
- [README.md](README.md)
- [CLAIM_STATUS.md](CLAIM_STATUS.md)
- [HANDOFF.md](HANDOFF.md) for the current detailed state
- [notes/SOURCES.md](notes/SOURCES.md) when novelty or literature status matters

Then ask:

- What exactly am I claiming?
- What is the claim's current status?
- What assumptions and runner-count conventions am I using?
- Can another person reproduce the calculation or inspect the proof?
- What would falsify this?
- Is the result already known?

## Good contributions

Especially useful contributions include:

- a counterexample to one of our hypotheses;
- independent review of a proof candidate;
- a simpler or more general derivation;
- reproduction of an experiment using different code;
- a bug report with a minimal failing case;
- a literature reference that changes novelty or context;
- an exact computation that tests a stated open question;
- a new representation that produces a testable consequence;
- a correction to terminology, notation, scope, or attribution.

Negative results are welcome when they are informative and reproducible.

## Mathematical conventions

Unless explicitly stated otherwise:

- `n` is the total number of runners;
- selecting a reference runner leaves `k=n-1` relative speeds;
- all runners begin at the same point;
- equality at distance `1/n` counts;
- rational test cases should be certified with exact arithmetic when practical.

If a cited paper uses another convention, translate it explicitly.

## Computational contributions

Please include:

- the exact input/domain;
- code revision;
- command used;
- whether arithmetic is exact or numerical;
- resource/search bounds;
- output or certificate;
- at least one countercheck when practical.

A large finite search is evidence only for the searched domain unless paired with a proved finite reduction.

Do not report resource failure or numerical instability as a mathematical counterexample.

## Proof and proof-review contributions

A proof proposal should make every assumption visible and separate:

1. definitions;
2. lemmas;
3. the main implication;
4. endpoint/equality cases;
5. dependence on integrality, positivity, ordering, or a selected reference runner.

Reviewers are encouraged to attack the argument rather than merely confirm it.

If the proof was materially generated or reconstructed with AI, say so. That does not invalidate it; it makes provenance clear and increases the importance of independent review.

## Literature and novelty

Do not label a result "new" solely because we did not know it.

For possible novelty claims:
- search the relevant literature;
- cite exact sources and versions;
- note terminology differences;
- state how much of each source was actually inspected.

Finding that an idea is already known is a successful research outcome and should be preserved.

## Pull-request expectations

A useful PR answers:

- **Question:** what are you investigating?
- **Status:** KNOWN / REPRODUCED / OBSERVED / HYPOTHESIS / OPEN / DISPROVEN
- **Claim:** what exactly changes?
- **Scope:** for which runners/speeds/parameters?
- **Evidence:** proof, certificate, computation, source, or counterexample
- **Reproduction:** how can someone check it?
- **Counterchecks:** what did you try that could have broken it?
- **Uncertainty:** what remains unresolved?

Small PRs are easier to review than mixed bundles.

## Respectful scientific disagreement

Challenge claims aggressively; treat contributors respectfully.

Prefer:
- "This step assumes X, which is not established"
over:
- "This is nonsense."

Prefer:
- a counterexample
over:
- authority or status.

Prefer:
- "I don't know"
over:
- filling a gap with confidence.

## Privacy and repository scope

Do not add:
- credentials or secrets;
- private conversations;
- personal identifiers;
- family, business, clinical, health, or financial records;
- unrelated research that belongs elsewhere.

The public repository is a scientific record, not a general conversation archive.

## Canonical record

A pull request is a proposal. Maintainers decide what enters `main`.

Rejected or revised contributions may still be scientifically useful. The goal is not consensus at all costs; it is a correctable record that stays in contact with the evidence.
