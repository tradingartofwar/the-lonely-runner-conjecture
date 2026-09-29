# Coefficient range of the fixed row-(3,8) selector

September 29, 2026. Main account:
[CC_ROW38_COEFFICIENT_RANGE_2026_09_29.md](../../notes/CC_ROW38_COEFFICIENT_RANGE_2026_09_29.md).

The complete reduction finds T=R with 205 classes under coefficient shift
(56,56). Including the p=q auxiliary gives T_all with 178 classes. Requiring
both entire primary segments gives W with 21 positive rows. The old and new
infinite coefficient sets have an exact intersection of 10 rows, including
four identically repeated core rows. Neither set contains the other.
The universal arguments remain internally reviewed proof candidates.

The finite reduction comprises 1,512 coefficient cells and 2,551 primitive
directions, including one auxiliary. All 1,307 primary rejections retain
genuine eight-distinct-speed failed outputs. The 27 auxiliary-only failures
are separately labelled. The complete old/new intersection uses a proved
finite bound and 422 positive cases, not unlike residue-class counts.

| File | Purpose |
| --- | --- |
| PROTOCOL.md / INPUTS.json | Frozen scope, algebraic proposals and seven pinned sources |
| classify.py | Exact complete reductions and physical recovery |
| support.json | Complete bounded support; infinite tail is proved separately |
| classification.json | Every residue-cell verdict, failure count and accepted table |
| whole_segments.json | Complete W cases and 21 accepted positive rows |
| comparison.json | Exact finite old/new intersection and exclusive progressions |
| failures/delta_*.json | First physical failure for all 1,307 rejected primary cells |
| auxiliary_failures.json | 27 failed repeated-speed auxiliary records |
| controls.json | Frozen physical controls, period lifts and ambient fallback example |
| support_review.md | Pre-enumeration support, topology, slope and tail derivations |
| arithmetic_review.py / .json / .md | Separate projection/forbidden-band reconstruction |
| physical_review.py / .json / .md | Separate coordinate-lap and direct physical review |
| EXECUTION_RECORD.md | Timing, count typo and review-harness corrections |
| reproduce.py / REPRODUCTION.json | Byte-for-byte reproduction of 35 exact outputs |
| MANIFEST.json | Package and main-note hashes, excluding the manifest itself |

From the repository root, using standard-library Python 3 without -O:

```sh
python3 reviews/2026-09-29-cc-row38-range/reproduce.py
```

The arithmetic review matches 32,810 shared fields. The physical review
matches 96,202 scalar fields across 1,400 records, including 18 archived
configurations reproduced, 18 phase-period pairs and six analytic large-slope
controls. Full rejection arrays are retained once in the coordinator shards;
the physical review checks all their fields and records input hashes.

The output arrays use compact JSON where useful; the note and reports give
the readable interpretation. Code imports and source hashes are explicit.
No changed compiler, new menu, broader scan or new literature/priority claim
is made. The support and period reductions, rather than finite tests alone,
carry the universal construction claim. Separate AI reviews are disclosed;
they are not external human or formal proof certificates.
