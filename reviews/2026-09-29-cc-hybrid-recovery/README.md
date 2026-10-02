# Contact-first hybrid recovery

Frozen development repair for the known (54,26) phase-screen omissions.
See [research note](../../notes/CC_HYBRID_RECOVERY_2026_09_29.md),
[protocol](PROTOCOL.md) and [summary](summary.json).

The hybrid retains the original screen and three-segment menu, then searches
the 36 supplied source segments only for its three uncovered primitive
directions. It recovers one point for each in 11 source visits and three
new-runner phase tests. Preflight work is explicitly charged. This recovers
the complete declared family at 1/8 under the internally reviewed finite
reduction and source-relative completeness argument.

Files:

- `INPUTS.json`: seven source pins and frozen protocol hash.
- `REVIEW_INPUTS.json`: one supplementary review-only parent-geometry pin
  for checking the retained original edge parameter against its actual vertices.
- `hybrid.py`: exact standard-library implementation and bounded benchmark.
- `hybrid.json`: unchanged screen certificate, preflight, visited traces and
  direction-specific point records.
- `audit.json`: archived-certificate regressions, full-candidate membership,
  47 residual physical dispatches, 24 physical controls, open-source
  diagnostic, zero budget and four synthetic kernel fixtures.
- `summary.json`: exact results and cost counts.
- `timing.json`: one recorded eleven-pair benchmark, environment and scope;
  not a byte-reproducible mathematical output.
- `geometry_review.*`, `physical_review.*`, `proof_review.md`: separately
  structured AI reviews, without external/human/formal certification.
- `reproduce.py`, `REPRODUCTION.json`: deterministic-output reproduction.
- `EXECUTION_RECORD.md`, `MANIFEST.json`: provenance, correction history
  and hashes.

From the repository root, reproduce exact outputs without repeating timing:

```sh
python3 reviews/2026-09-29-cc-hybrid-recovery/reproduce.py
```

The exploratory benchmark can be run deliberately with `hybrid.py --benchmark`;
it overwrites timing.json and is not part of deterministic reproduction.
General claims remain HYPOTHESIS / internally reviewed proof candidates.
No new target transfer, new threshold, full-safe-set or optimum computation.
