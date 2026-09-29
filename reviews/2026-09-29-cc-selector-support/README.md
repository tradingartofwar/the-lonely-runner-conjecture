# Actual selector support and exact coefficient decision

September 29, 2026. The argument is in
[CC_SELECTOR_SUPPORT_2026_09_29.md](../../notes/CC_SELECTOR_SUPPORT_2026_09_29.md).

Result: the actual support is countable and closed, with one accumulation
point, yet T=T_all=R for positive integer seventh-row coefficients. The
whole-L-plus-C test accepts exactly the same 42 classes as uniform success
of the fixed first-integer selector. T excludes p=q; T_all includes that
auxiliary. Every rejection for T supplies an eight-distinct-speed failure
of this selector, with no claim that the configuration lacks other witnesses.

The large-slope argument proves |A−2B|≤13 is necessary; a safe-tail argument
reduces the remaining direction checks to M=Q+2P≤91. The complete reduction
has 216 residue cells and 1,275 primitive directions. There are 387 unique
leader points including the auxiliary, 386 after its removal. The 174
rejected cells retain physical failure certificates. All 54 old progression
controls reproduce. No outside-R class was found, so the conditional new
positive controls were not triggered.

| File | Purpose |
| --- | --- |
| PROTOCOL.md | Questions, prospective bounds, fixed controls and review scope |
| INPUTS.json | Source head, SHA-256 and Git blob identities |
| selector.py | Residue-form support, full reduced classification and Bezout recovery |
| support.json | Every bounded primitive direction and selected point |
| classification.json | All 216 verdicts, including failure counts and phase-vector hashes |
| witnesses.json | 174 derived negative certificates and 54 archived reproductions |
| support_review.md | Separate support/topology, large-slope and tail proof review |
| classification_review.py / .json / .md | Direct interval selection, coordinate recovery, full independent calculation and comparison |
| EXECUTION_RECORD.md | Timing, shared findings, correction and scope |
| reproduce.py / REPRODUCTION.json | Four byte-for-byte output reproductions |
| MANIFEST.json | File identities for this package and main note |

From the repository root, use Python 3 and the standard library, without `-O`:

```sh
python3 reviews/2026-09-29-cc-selector-support/reproduce.py
```

This verifies pinned inputs, runs selector.py, then the reviewer's independent
calculations and comparisons. It overwrites the same deterministic outputs
and requires all four to reproduce byte-for-byte. Comparison covers 7,650
support fields, 1,944 classification fields, 4,332 physical fields and 972
archive fields. The reviewer reads coordinator JSON only after computing its
own results; it imports no coordinator code. The support reviewer performs
no new enumeration or physical trial. Reviews are parallel, with findings
shared; no blind, human or formal certification is claimed.

The 11-direction rejection summary in the note was extracted after the
complete run; it is not a newly frozen or minimal test menu. All earlier
packages and visual work remain unchanged. The universal argument remains
an internally reviewed proof candidate, and exact-certificate novelty stays open.
