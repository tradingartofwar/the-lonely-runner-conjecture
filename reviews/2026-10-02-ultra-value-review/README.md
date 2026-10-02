# Ultra value review — October 2, 2026

Baseline: `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`. Five main AI review tracks plus implementation and delegated code checks. Review coverage is scoped in each report; neither every historical computation nor all possible model languages were exhaustively audited. No external messages, deployments or outside-user experiment occurred.

Start with the [synthesis](../../notes/ULTRA_VALUE_REVIEW_2026_10_02.md) and the [working demonstration](../../examples/compatibility-conformance/index.html). The [example README](../../examples/compatibility-conformance/README.md) gives exact reproduction commands and limits.

| Track | Report | Actual additional work |
| --- | --- | --- |
| Mathematics | [math_audit.md](math_audit.md) | Independently structured small exact checker; minimum-two component-source deduction; no broad scan |
| Framework alternatives | [frameworks.md](frameworks.md) | Nine framework families and primary-source comparisons; offline viewer built subsequently |
| External applications | [external_value.md](external_value.md) | Ten-case SymPy adapter, independent rational oracle, exact substitution checks and reproduction |
| Information/evidence | [information_value.md](information_value.md) | Review of physical information loss, handoff nulls and mature conventional baselines |
| Adversarial value | [value_redteam.md](value_redteam.md) | Static code review, protocol correction identified, final SymPy replay |
| Conformance code review | [conformance_review.md](conformance_review.md) | Source-field binding repairs, eleven corruption controls, independent physical checks and optimized-Python reproduction |

The top-level result is a reusable teaching/conformance artifact and a narrower mathematical proof candidate. There is no demonstrated third-party bug, novelty, operational adoption, comparative performance or CC advantage. Deliberately faulty rules are explicit controls. The fifteen examples belong to two separate development collections, not fifteen independent external successes.

## Preserved evidence

- `math_audit_check.py` and `math_audit_checks.json`: exact core, small-r, equality, tail and clock controls.
- `conformance_review_checks.py` and corresponding JSON: final source/semantic corruption checks, plus initial records and normal/optimized outputs. The initial source-binding defects remain documented.
- `examples/compatibility-conformance/sympy_periodic/`: frozen initial protocol/code hashes, initial implementation and successful outputs, the postfreeze dormant-path correction, final outputs and reproduction. Final source is not mislabeled as unchanged from the initial freeze.
- `UI_VERIFICATION.json`: renderer/interactions and presentation checks when completed by the coordinator. These verify the viewer, not mathematical truth.
- `MANIFEST.json`: final file hashes, including the review reports, example package and synthesis. A hash establishes byte identity relative to the pin, not proof or authenticity.

Older frozen packages are left unchanged. Current README/HANDOFF/plan updates are tracked by the containing result commit. The standalone demo has no network requirement; rerunning source-bound examples requires the repository source files, and the SymPy adapter requires its pinned dependencies.
