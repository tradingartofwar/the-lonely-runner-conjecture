# Recovery scope — September 29, 2026

The user requested preservation of the unsaved continuation. The live research
branch starts at `908a089ac39f9af796d6261d22f8b37009b1eb53`. The original candidate
and Ultra review already exist there. Their family is V(1,q), whereas the recent
continuation's displayed speeds are V(q,1), after permutation.

Freeze the continuation's four-row optimum candidate and witness formulas
without fitting replacements. Reproduce exactly q=2,...,150 (149 integer cases),
the range claimed in the continuation. No larger scan or new parameter family
is part of this save task. Two original-ray controls at q=2 and q=4 distinguish
the families. Preserve any failure rather than adjusting the candidate silently.

Use exact opposing-contact/individual-peak enumeration, with reflection to
halve the time range. Candidates must not depend on the proposed optimum or
witness. Recover physical phases/laps at each proposed time. Also check the
explicit affine polynomial witness charts for all six residue classes: exact
identities and affine sign certificates apply to whole unbounded k domains.

This is a reconstruction run, not recovered evidence of the earlier claimed
execution. The formulas were already visible before this protocol; it is not a
blind discovery experiment. The archived Ultra physical checker was inspected
before writing this script. No independent-author review is claimed.

Do not upgrade bounded optimum agreement into a universal upper bound. The
original ray's Ultra verdict and upper-bound comparisons do not automatically
transfer to this different ray. No literature novelty claim is being made.

Reproduce from the repository root (standard-library Python only):

```bash
python3 reviews/2026-09-29-ltcm-other-ray/verify.py > /tmp/ltcm-other-ray-verification.json
```

The saved `verification.json` records every case, selected witness, full
maximizing-time set, candidate count, symbolic identity, and inequality.
