# Instructions for AI collaborators

AI systems are welcome as research collaborators in this repository. They are not treated as authorities or independent proof certificates.

## Begin and resume

Read [README.md](README.md), [HANDOFF.md](HANDOFF.md), [CLAIM_STATUS.md](CLAIM_STATUS.md), and [CONTRIBUTING.md](CONTRIBUTING.md). Then consult [RESEARCH_PLAN.md](RESEARCH_PLAN.md), [the mathematical baseline](notes/MATHEMATICAL_BASELINE.md), and [sources](notes/SOURCES.md) as needed.

Inspect the live branch and relevant files before proposing changes. The current human maintainer's direction and the repository's evidence rules govern publication.

## Research partnership

- Human intuition, direction, skepticism, and recognition of interesting structure are legitimate inputs to inquiry.
- AI may contribute mathematical explanation, alternative representations, literature checking, implementation, testing, counterexamples, and continuity.
- Convert intuitions into statements that can fail.
- Preserve both promising patterns and the evidence that corrects them.
- Prefer concrete examples, exact calculations, and explicit assumptions over confident prose.
- Carry routine technical detail when useful, but report the result and uncertainty plainly.

## Evidence discipline

Use the vocabulary in [CLAIM_STATUS.md](CLAIM_STATUS.md).

- Distinguish literature result, reproduced computation, bounded observation, hypothesis, proof candidate, and established proof.
- Use `n` for total runners and `k=n-1` for the other runners relative to a selected reference unless explicitly translating another source's convention.
- Start all runners at the same position unless a different problem is clearly labeled.
- Animation, dense time samples, optimizer output, and language-model agreement are not proof certificates.
- Prefer exact rational arithmetic when certifying rational cases.
- Check suspected failures with a separately structured method where practical.
- A finite search supports only its stated finite scope unless accompanied by a proved finite reduction and exhaustive coverage.
- Do not call a result new until checking relevant literature and known symmetries.
- A proof candidate generated or reconstructed with AI requires independent review before being promoted to an established result.
- Cite source versions and dates. Literature-status notes are snapshots, not permanent claims about the frontier.

## Public-repository boundaries

Do not add credentials, private conversations, family information, business records, clinical information, financial records, personal identifiers, or unrelated private research.

Do not contact outside researchers, spend money, purchase compute, launch broad unattended computation, or publish claims outside this repository without explicit human authorization.

Keep changes small and inspectable. Preserve counterexamples and corrections rather than silently rewriting history.

## Contributions

For an external contribution, prefer a fork and pull request. In the PR:

1. identify the question;
2. declare the claim status;
3. state assumptions and scope;
4. provide a reproducible command, derivation, or certificate when applicable;
5. identify counterchecks;
6. cite related literature;
7. say what remains uncertain.

AI-assisted contributions should disclose material AI involvement when it affected reasoning, code, literature synthesis, or proof generation. The human submitter remains responsible for what is proposed for the canonical record.

At a meaningful research pause, update [HANDOFF.md](HANDOFF.md) only when the change materially affects the live research state.
