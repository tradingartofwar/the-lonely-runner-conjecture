# CC two-parameter coverage compiler — September 29, 2026

**Result:** the frozen rule assembles a sufficient two-segment certificate from
the preserved parent-edge geometry. The complete finite reduction, physical
recovery, separate AI reconstruction and four failure controls pass. This is
a development example with a known answer; the underlying universal argument
remains an internally reviewed proof candidate. No external/formal verification,
new existence coverage, optimization result or originality claim follows.

Start with [the synthesis](../../notes/CC_COVERAGE_COMPILER_2026_09_29.md).
The input branch is `17b2fca8541540af52cd6c5bf2b09c26c646d240`; earlier proof
packages are read-only. This package contains:

| File | Purpose |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Frozen input, deterministic ranking, bounds, controls and scope |
| [INPUTS.json](INPUTS.json) | Exact input hashes and read boundary |
| [CORRECTIONS.md](CORRECTIONS.md) | Review clarification: completed uncovered-pair evidence excludes every supplied candidate |
| [compiler.py](compiler.py) | Candidate generation, coverage assembly and serialized-record evaluation |
| [certificate.json](certificate.json) | 27 candidates, 10 descending ranks, 8 residual pairs, 216 contacts and selected menu |
| [run.json](run.json) | 18 prior physical controls, four failure statuses and endpoint-loss control |
| [coverage_review.md](coverage_review.md) | Separate line/band reconstruction and conditional coverage review |
| [coverage_review.py](coverage_review.py) / [output](coverage_review.json) | Exact geometric/contact checks; isolated production-failure checks |
| [physical_review.md](physical_review.md) | Separate coordinate-lap reconstruction and representation review |
| [physical_review.py](physical_review.py) / [output](physical_review.json) | Exact physical checks without compiler/selector imports |
| [reproduce.py](reproduce.py) / [REPRODUCTION.json](REPRODUCTION.json) | Four exact output reproductions and post-run comparison to archived witnesses |
| [MANIFEST.json](MANIFEST.json) | Final file hashes, excluding the manifest itself |

From the repository root, using standard-library Python without `-O`:

```sh
python3 reviews/2026-09-29-cc-coverage-compiler/reproduce.py
```

This reruns the compiler, verifies its two outputs byte-for-byte, reruns the
two review programs and compares their stdout to the archived JSON, then
checks six physical output fields for each of the 18 prior selector records.
It writes REPRODUCTION.json. There is no enlarged parameter scan or optimizer.

The compiler writes certificate.json and run.json. The two review programs
print JSON without rewriting their own archived reports. Their reconstruction
uses pinned local inputs, so retain the referenced predecessor packages when
copying this directory. The full source boundary and hashes are explicit.

The online evaluator checks its selected segment and recovered witness. It is
not a full validator for arbitrary untrusted certificates; the separate
coverage reconstruction checks the emitted global record in this fixed scope.
Missing geometry, invalid input, a resource bound and a named uncovered pair
must remain distinct outcomes. None establishes failed loneliness.
