# Frozen independent third-parameter test

See the [research note](../../notes/CC_THREE_PARAMETER_TEST_2026_09_30.md).

Replacing the ninth moving speed by free r gives a coefficient family of
rank three. Four discovered sheets cover all 89 training cases and 310/318
held-out cases. The frozen compact transfer fails on eight cases. The full
36-sheet class covers all 407, with exact physical 1/8 witnesses. The 72
tested boundary edges cover only 90. These are finite, reproduced results;
there is no claimed infinite-family coverage or general Lonely Runner proof.

Files:

- PROTOCOL.md and INPUTS.json: pre-execution rules, domains, budgets and eight
  input pins. Protocol and code were frozen in Git at d744b08.
- discover.py: exact shared-point integer-contact solver and training-only
  greedy compiler for the two declared object classes.
- discovery.json: sources, object identities, both menus and selection traces,
  all 45,252 contact bits, exact selected/class-fallback witnesses, and three
  information-loss counterexamples. `hits` strings align with object indices.
- summary.json: compact discovery counts and raw outcome distinctions.
- verify.py: alternate physical-time contact checks and complete physical
  safe-band intersections, with no production imports.
- verification.json: exact physical interval unions and first failure/repair
  examples; verification_summary.json: aggregate check counts.
- reproduce.py and REPRODUCTION.json: clean exact replay of four output files.
- EXECUTION_RECORD.md and MANIFEST.json: chronology, identities and scope.

From the repository root:

```sh
python3 reviews/2026-09-30-cc-three-parameter/reproduce.py
```

The two implementations share an author. This is structured internal checking,
not blind, independent human, separate-agent or formal verification. General
orbit/recovery arguments remain proof candidates. The four-sheet menu is not
silently enlarged with its holdout diagnostics. The conditional weaker-threshold
and negative-result branches were unexecuted and are not validated by this run.
