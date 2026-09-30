# Frozen contact-first hybrid transfer

Target (102,50), informed by failure of the previous hybrid time9/40 at(5,1).
See [research note](../../notes/CC_HYBRID_TRANSFER_2026_09_29.md),
[protocol](PROTOCOL.md) and [summary](summary.json).

The data-only adapter preserves the prior function bodies, captured target
defaults and physical row bindings. It reproduces the old result before
constructing the new hybrid. The new search rejects the old point and recovers
31/136 from a later source; all three exceptions are repaired with14 source
visits and four phase tests. Full discovery yields89 candidates. Both methods
pass24 controls and the complete47-direction coverage comparison agrees.

Artifacts:

- `PROTOCOL.md`, `INPUTS.json`: pre-computation freeze and14 source pins.
- `transfer.py`, `adapter.json`, `adapter_regression.json`: explicit data
  bindings, unchanged-function evidence and exact old-result regression.
- `hybrid.json`, `full.json`: full reached construction certificates/traces.
- `audit.json`, `summary.json`: candidate-class comparison, physical controls,
  old-time failure, source maps, open-source/budget diagnostics and costs.
- `timing.json`: one bounded eleven-pair benchmark, environment and scope;
  retained as measured data, excluded from byte-for-byte reproduction.
- `geometry_review.*`, `physical_review.*`, `proof_review.md`: separate
  internally structured AI reviews; inherited independent primitives disclosed.
- `reproduce.py`, `REPRODUCTION.json`, `EXECUTION_RECORD.md`, `MANIFEST.json`:
  reproduction, provenance, correction history and artifact hashes.

From the repository root:

```sh
python3 reviews/2026-09-29-cc-hybrid-transfer/reproduce.py
```

That command repeats only frozen deterministic outputs and reviews, with
serialized production dispatch checks. It does not rerun timing or choose a
further target. Deliberately running `transfer.py --benchmark` replaces the
saved timing measurement and is outside deterministic reproduction.

This is one within-progression stress transfer, not arbitrary-row portability,
optimality, novelty or a general runtime bound. Universal claims remain
internally reviewed proof candidates. A different allowed phase-identity
family, changing the supporting boundary, is proposed but unrun.
