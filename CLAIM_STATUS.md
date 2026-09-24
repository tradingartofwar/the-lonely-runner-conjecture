# Claim status vocabulary

This project uses explicit status labels to prevent an interesting idea from quietly becoming an accepted fact through repetition.

Use the strongest label the evidence actually earns — never the label you hope it will earn.

## KNOWN

An established mathematical result supported by a cited source that we have identified clearly enough for readers to locate and inspect.

Use **KNOWN** for literature results, not merely because a claim is familiar or widely repeated.

Record:
- source and version/date;
- theorem/proposition/section when practical;
- notation differences that matter;
- whether we inspected only a statement or also checked the proof.

## REPRODUCED

A result that has been independently recovered here within a stated scope.

Examples:
- our checker matches a published fixed case;
- an exact computation reproduces a reported value;
- a known formula is reconstructed and checked on explicit inputs.

**REPRODUCED** does not imply novelty and does not mean we have independently verified an entire paper.

Record:
- exact input or domain;
- code revision or derivation;
- command or certificate;
- comparison target;
- any remaining verification limit.

## OBSERVED

A bounded pattern or exact fact established for the explicitly tested cases.

Examples:
- a finite family shares a spacing pattern;
- a search over a stated box produces no counterexample;
- several exact cases exhibit the same limiting runner.

An **OBSERVED** pattern is not a theorem outside its stated domain.

Record:
- the complete tested scope;
- exact arithmetic or search method;
- nearby counterchecks when available.

## HYPOTHESIS

A proposed explanation, mechanism, generalization, or conjectured pattern that can fail.

Good hypotheses state what evidence would count against them.

Record:
- the precise statement;
- why it was suggested;
- known supporting observations;
- known counterpressure or exceptions;
- a useful falsification test.

## OPEN

A question or unresolved distinction.

Use **OPEN** when we do not yet know which of several possibilities is correct, when an argument is incomplete, or when a literature/novelty check remains unfinished.

An open question is not evidence for any preferred answer.

## DISPROVEN

A sufficiently specific proposed statement for which a valid counterexample, contradiction, or failed necessary condition has been established.

Preserve disproven ideas when they are instructive. State exactly what failed rather than erasing the path that led there.

Record:
- the original statement;
- the counterexample or contradiction;
- whether a narrower version may remain open.

## Proof candidates

A proof candidate is not a seventh evidence category. It is a **HYPOTHESIS** or **OPEN** item with a proposed complete argument that has not yet earned promotion to **KNOWN**.

For this repository, an internally generated proof candidate should receive:
- line-by-line mathematical review;
- explicit assumption and endpoint checks;
- attempts to produce counterexamples;
- literature/novelty comparison;
- independent human or independently structured review when feasible.

AI generation or agreement is never itself independent review.

## Changing status

A status change should be visible in Git history and justified in the note or pull request that changes it.

Examples:

- HYPOTHESIS -> DISPROVEN after a counterexample.
- OBSERVED -> KNOWN after locating the existing theorem.
- HYPOTHESIS -> KNOWN only after a valid proof is established and the novelty/literature status is clear.
- OPEN -> REPRODUCED when the question was whether we could independently recover an existing result.

Corrections are progress.
