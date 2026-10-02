# SymPy finite-horizon periodic inequality demonstration

Prepared 2026-10-02 against repository `29e54d32e2ff5349bdb0c3db56fab753a0e44c94`.
This is an exposed development regression demonstration, not a blinded validation set,
industrial workload, solver defect report, or comparative performance experiment.

## Supported question and fragment

Return the complete solution set of a conjunction of atoms on a bounded rational
time interval with explicit open/closed ends. An atom is
`sin(pi*(a*t+b)) op c` or `cos(pi*(a*t+b)) op c`, where `a` is a positive rational,
`b` is rational, `op` is one of `<`, `<=`, `>`, `>=`, and
`c` is one of `-1`, `-1/2`, `0`, `1/2`, `1`. Time is normalized by pi, so every
boundary in this fragment is rational. The input is structured JSON; there is no
arbitrary-expression parser. Unsupported input raises an error, never `UNSAT`.
Inputs use integer/fraction strings; floating-point values are unsupported.
Each input rational has denominator at most 64 and absolute value at most 100;
each case has at most eight atoms, at most 100 periods of each atom in its
horizon, and at most 1,000 compiled phase events. These are implementation limits,
not mathematical impossibility results.

The pinned dependency is SymPy 1.14.0. Its documented principal-period inequality
result is a compressed source, not the answer for an arbitrary finite horizon.
The candidate obtains each atom's result and period from SymPy, retains endpoint
flags and isolated points, shifts that source through every relevant period,
clips to the horizon, then intersects all atoms at the same time. A complete
empty intersection alone supports the bounded negative verdict.

## Frozen development cases

`cases.json` contains ten selected cases, chosen before the first candidate run:
the documentation example `2*cos(x)<1`; mixed periods; incompatible strict
inequalities; an equality-only conjunction; offsets; rational frequency;
negative time; a closed horizon end; an extremal singleton; and a query entirely
beyond the principal period. These are informed examples, not ten independent
external demands or fresh holdouts. No rates, thresholds or cases will be added
in response to outcomes. Implementation corrections, if needed, will be recorded.

## Three checks and a limited diagnostic

1. The adapter lifts each independently solved atom before joint intersection.
2. A separately structured `Fraction` oracle enumerates all original phase
   boundary events, decides each endpoint and open cell by elementary sine phase
   arcs, and assembles the complete set. It does not read SymPy's solved sets or
   call its inequality solver or set operations.
3. At every oracle event and every intervening cell midpoint, exact SymPy
   substitution in the original trig expressions must agree with the oracle and
   adapter. The finite partition is complete for the stated fragment; these are
   event cells, not a dense numerical sample.

The unlifted principal-period intersection is printed solely to show the changed
query obligation. It deliberately has narrower scope and is not a fair baseline,
a failure of SymPy, or evidence of CC superiority. The fair ordinary method is
standard period expansion and interval/set intersection, which is what this
adapter implements. A named CC layer is not necessary to implement it.

## Budget, outputs and success/stop criteria

One process, ten cases, no optimization, no network or live devices during the
run. Stop the run if it exceeds two minutes or an unsupported symbolic result is
encountered. Record source/dependency hashes, exact normalized outputs, empty vs
nonempty verdicts, singleton counts, and the two agreement checks. Re-run once
and require identical deterministic JSON. Timing is not an outcome measure.

Success is ten exact set agreements and all exact substitutions agreeing, with
the provenance contract readable and reproducible. This establishes bounded
adapter correctness and an example of how to honor the existing API's scope.
It does not establish a new solver, advantage over conventional exact methods,
external adoption, operational benefit, or general symbolic completeness.
Any discrepancy stops positive reporting until classified and preserved. If
everything passes, stop at this small artifact; do not launch a larger benchmark
without a real downstream use or a separately justified question.

## Primary source

SymPy 1.14.0 guide, last updated April 27, 2025, read October 2, 2026:
https://docs.sympy.org/latest/guides/solving/reduce-inequalities-algebraically.html#not-all-results-are-returned-for-periodic-functions
The documentation explicitly instructs restoration by integer period shifts.
The source code of the installed pinned wheel is also hashed by this package.
The source SHA256 authenticates the tested bytes, not their correctness.
