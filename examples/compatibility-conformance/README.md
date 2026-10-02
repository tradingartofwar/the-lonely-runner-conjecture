# Compatibility conformance: an inspectable human–AI research example

This small teaching and regression kit extracts useful failures from the Lonely Runner investigation and applies the same preservation question to an existing symbolic-math tool. It asks: **does the translated model still answer the question we started with?**

Open [index.html](index.html) in a browser for the offline viewer. The page displays saved exact results and their evidence; it does not run a symbolic solver in the browser. Exact fractions and endpoint flags are authoritative; plotted positions are illustrative. No account, server, network connection or external fonts are needed to view it.

## What is here

| Artifact | What it demonstrates | What it does not establish |
| --- | --- | --- |
| Five archived mathematical regressions | Separate marginal successes, incomplete orbit relations, missing clock lifts, dropped isolated points and an overcompressed source menu can change a requested answer | Five defects in third-party software, fresh transfer evidence, or superiority to a competent exact baseline |
| Ten-case SymPy periodic-set adapter | Solve each supported periodic predicate, restore its integer translates across the requested finite horizon, then intersect at the same time with exact endpoint semantics | A SymPy bug, arbitrary symbolic inequality solving, industrial scheduling benefit, or comparative speed advantage |
| Offline viewer and exact records | A reader can inspect a query, the omitted distinction, a counterexample and a recoverable result | Measured learning gains or a controlled human–AI productivity comparison |

These are development examples selected with their mechanisms in mind. They are not a random sample or held-out test. The two collections have different purposes and must not be combined into an external-success rate.

## Run the exact checks

From a checkout of the repository:

```bash
python examples/compatibility-conformance/check.py
```

The five-case checker uses only Python's standard library and rational arithmetic. It checks the pinned source bytes, resolves the declared source records, checks the mathematical fixture fields against those records, and compares direct physical-time calculations with archived answers. The point-time reference imports no old lattice or clock-recovery code. Explicit guards remain active under `python -O`.

**Source dependency:** the three archived files named in `fixtures.json` must accompany this directory at their pinned bytes. Copying only this example directory is insufficient to rerun its source verification. The offline viewer is self-contained for inspection; it is not a substitute for rerunning the checks.

For the SymPy example, create a local Python environment and install the pinned dependencies:

```bash
python -m pip install -r examples/compatibility-conformance/sympy_periodic/requirements.txt
timeout 120 python examples/compatibility-conformance/sympy_periodic/demo.py
```

The external `timeout` wrapper supplies the two-minute limit used in the recorded runs. See [the adapter README](sympy_periodic/README.md) for its exact structured-input contract, provenance and development correction. The implementation supports a narrow affine sine/cosine fragment with exact rational data. Unsupported input and execution failure are not mathematical emptiness.

To refresh the viewer after intentionally updating and checking records:

```bash
python examples/compatibility-conformance/build_demo.py
```

## Keep each query precise

The same-point fixture retains the archived segment and fixed third phase. The incomplete-relation fixture asks whether the archived false-hit **point** belongs to the actual orbit; it specializes the source edge query. The clock-lift fixture asks for the archived **exact phase triple**, which is stronger than the source's safe-band request. Both adaptations are explicit in the machine-readable source records. The two interval fixtures preserve the complete closed 1/8 safe-time query for their fixed inputs.

The five faulty rules in `check.py` are intentional teaching mutations. The direct-time baseline answers all five correctly. A false positive rejects the proposed model or witness, not the original underlying physical problem; an exhausted candidate subset does not prove full infeasibility.

The SymPy comparison uses its [documented periodic-output contract](https://docs.sympy.org/latest/guides/solving/reduce-inequalities-algebraically.html#not-all-results-are-returned-for-periodic-functions). The principal-period output is sufficient seed information when used with its period. Displaying it beside the lifted result illustrates a caller's scope obligation. It is not a competing complete solver that SymPy has failed to implement.

## What the collaboration produced

A human set the research direction and insisted that omitted information be investigated. AI-assisted work developed exact examples, tried compressed representations, preserved failures, compared established frameworks, built executable checks and reviewed the implementation. The resulting public artifact lets another person replay and challenge those steps. It demonstrates this bounded process; comparative claims about human–AI superiority require a different study.

The [team assessment](../../notes/ULTRA_VALUE_REVIEW_2026_10_02.md) separates this working artifact from the narrow mathematical proof candidate, the prior null handoff results, and applications still requiring a real consumer. Existing repository licenses apply: MIT for code, CC BY 4.0 for research writing/data.
