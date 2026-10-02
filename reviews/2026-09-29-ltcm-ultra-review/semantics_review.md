# Witness, equality, and LTCM scope review

Date: 2026-09-29. Candidate: `8a967b30fcd73abd814e4c8f7f53f216c4b3f61e`.

**Verdict: no defect found in the actual-time lower witnesses, physical lap
reconstruction, exceptional safe set, or stated restricted scope.** The
positive-duration and unique-tightness conclusions follow without assuming
the proposed global upper bounds for the other parameters. Exact optimality
on those other branches remains dependent on the separately assigned
fixed-cell, slice, and upper-bound reviews. This is an internally tasked AI
review, not independent human review, formal verification, or a novelty
determination.

The reviewed sources were `AGENTS.md`, `README.md`, the current `HANDOFF.md`
and research-queue entries, `CLAIM_STATUS.md`, `CONTRIBUTING.md`, the new
review protocol, the spectrum note, its original protocol and prevalidation
derivation, and its `audit.py`. The mathematical-baseline path linked by
`AGENTS.md` is absent from this supplied snapshot; the operative conventions
are explicit in the other files. The snapshot lacks `.git`; the coordinator
separately verified the remote candidate commit and the note/manifest hashes.
No original proof file or continuity file was changed.

## 1. Assumptions and the actual orbit

For every integer `q >= 2`,

`0 < 1 < q < q+1 < q+2 < q+3 < 2q+3 < 2q+5`.

Thus the displayed configuration has eight distinct runners, with seven
positive velocities relative to the selected stationary reference. In this
display the initial `0 < 1` includes the reference speed zero; no additional
coprimality hypothesis is needed. Common starting position is essential.

Integrality supplies period one and the reflection identity
`||v(1-t)|| = ||vt||`. These justify restricting the full optimization first
to `[0,1]`, then to `[0,1/2]`. An arbitrary real `q` would invalidate the
stated period/reflection and residue analysis. No such extension is claimed.

The coefficient representation is exact: the seven velocities are
`v_i(q)=a_i+b_i*q`. If an ambient safe point has
`q*x-y=h` integral, setting **`t=x`** gives

`v_i(q)*t = a_i*x + b_i*y + b_i*h`.

Consequently an ambient phase `a_i*x+b_i*y-m_i` transfers to physical lap
`ell_i=m_i+b_i*h`. Since all safe phases lie in `[z,1-z]`, with `z>=1/8`,
they lie strictly between zero and one. These labels are the actual floors,
not merely congruence representatives. Conversely, any physical time reduced
modulo one satisfies the integer equation. The reduction therefore retains
the actual trajectory in both directions; it does not infer a physical
witness merely from two-dimensional feasibility.

The lower witnesses below also discharge the apparent ordering issue in
using only the ambient region `z>=1/8`: that restriction captures a global
maximum because a physical witness at least that high is independently
supplied for every allowed `q`.

## 2. Lower phase tables and their sharp endpoint restrictions

I independently expanded both affine charts directly from the seven rows.
Every displayed phase in Section 4 of the note is correct. A fresh exact
script, `semantics_check.py`, compares the full affine identities and the
lower/upper safety slacks at both endpoints. Because every slack is affine
in `e`, this checks the entire stated error interval, not a sample of it.

For E, the phases equal

`(1/3-2e, 5/6+e, 1/6-e, 1/2-3e, 5/6-5e, 2/3-4e, 1/3-8e)`.

The last lower slack is `1/6-7e`; hence `e<=1/42` is essential. The third
phase equals `z`, and the second equals `1-z`, so the physical minimum at
the proposed witness is **exactly** `z`, not only bounded below by it.

For C, the phases equal

`(1/2-3e, 1/6+5e, 2/3+2e, 1/6-e, 2/3-4e, 5/6+e, 5/6-5e)`.

Every safety slack is nonnegative on `[0,1/24]`. The fourth phase equals
`z`, and the sixth equals `1-z`. The upper endpoint also enforces the
baseline `z>=1/8`; the physical witness in this branch uses a smaller `e`.

The domain and common-time calculations are:

| Branch | Error and domain check | Integral `h=q*x-y` | Time |
| --- | --- | --- | --- |
| `3 divides q`, `q>=3` | `e=1/[6(2q+1)] <= 1/42`, equivalent to `q>=3` | `q/3-1` | `x=2z` |
| `q=4 mod 6`, `q>=10` | `e=1/[2(2q+1)] <= 1/42`, equivalent to `q>=10` | `(q-4)/3` | `x=2z` |
| `q=5 mod 6`, `q>=5` | `e=1/[3(3q+5)] <= 1/60 < 1/24` | `(q-1)/2` | `x=3z` |

For E, `q*x-y=q/3-5/6-(2q+1)e`; for C,
`q*x-y=q/2-1/6-(3q+5)e`. Substitution gives precisely the table.
All denominators are positive on the allowed domains.

At `q=1 mod 6` the least allowed `q` is 7; at `q=2 mod 6` it is 2.
At `t=1/6` their respective numerator lists modulo six are exactly
`(1,1,2,3,4,5,1)` and `(1,2,3,4,5,1,3)`. Both have minimum distance `1/6`.
The five branches are disjoint and exhaustive: residues 0 and 3 form the
first E branch; residue 4 splits into `q=4` and `q>=10`.

For additional transparency, the generic physical labels are:

| Chart | Ambient labels | Physical labels |
| --- | --- | --- |
| E | `(0,0,1,1,1,2,3)` | `(0,h,h+1,h+1,h+1,2h+2,2h+3)` |
| C | `(0,0,0,1,1,1,2)` | `(0,h,h,h+1,h+1,2h+1,2h+2)` |
| A, `q=6r+1` | `(0,0,0,0,0,0,1)` | `(0,r,r,r,r,2r,2r+1)` |
| B, `q=6r+2` | `(0,0,0,0,0,1,1)` | `(0,r,r,r,r,2r+1,2r+1)` |

Here the E/C values of `h` are given above. They are all nonnegative, so
there is no hidden negative-lap or wraparound exception.

## 3. Exceptional safe set and the earlier widening obstruction

For `q=4`, I reconstructed the closed safe set independently of all ambient
files. For each physical speed `v`, its safe set at threshold `1/8` is the
union of the `v` closed bands

`[(j+1/8)/v, (j+7/8)/v]`, `j=0,...,v-1`.

Successive exact intersections for `(1,4,5,6,7,11,13)` leave precisely

`{1/8,3/8,5/8,7/8}`.

Every endpoint is retained by the `lo<=hi` condition. The complete
intermediate unions and physical phases are in `semantics_check.json`.
Each of these four points has minimum distance exactly `1/8`, so this
also establishes `M(4)=1/8` directly. It does not rely on deducing equality
from zero duration alone.

The fixed-cell argument is consistent with this independent result.
Direct substitution into the stated vertex table confirms all ten
`4x-y` ranges. Only cell 2 reaches integer zero, at its unique minimizing
vertex `(1/8,1/2,1/8)`, and cell 5 is the singleton with integer value one.
Reflection produces four different times; no midpoint or period endpoint
is duplicated or omitted.

The conceptual counterexample to widening old stronger-safe cells is also
valid, and can be seen without another search. Delete speed 5. At `t=1/8`
the retained speed-1/speed-7 lap labels require, at threshold `r`,
`t>=r` and `t<=(1-r)/7`. Their feasibility forces `r<=1/8`. At `t=3/8`,
the retained speed-11/speed-13 labels require
`t>=(4+r)/11` and `t<=(5-r)/13`; feasibility again forces `r<=1/8`.
Reflection treats the other two points. These opposing pairs also isolate
the points already in the retained system at threshold `1/8`.

Thus none of the four necessary full-system witness label cells is
feasible at threshold `1/7`. Uniqueness of the retained labels at these
strictly nonintegral phases rules out recovering the same points from
another old label cell. Nevertheless, the retained six speeds have
minimum distance `1/5` at `t=1/5`. The failure concerns that proposed lift,
not lower-runner existence. A complete cell-based extension must admit
new lap cells.

## 4. Unique tightness, positive duration, and what uses upper bounds

Let `L(q)` denote the candidate value attained by the verified witness.
For `q!=4`, subtraction of `1/7` gives:

| Branch | `L(q)-1/7` |
| --- | --- |
| `3 divides q` | `(q-3)/[21(2q+1)]` |
| `q=1,2 mod 6` | `1/42` |
| `q=4 mod 6`, `q>=10` | `(q-10)/[21(2q+1)]` |
| `q=5 mod 6` | `(q-3)/[14(3q+5)]` |

Every entry is nonnegative on its stated domain, and only the first at
`q=3` and the third at `q=10` vanish. Hence **`M(q)>=1/7` for every
`q!=4`** follows from the lower witnesses alone. Together with the direct
exceptional calculation, this proves that `q=4` is the only member whose
selected-reference maximum is `1/8`. Claiming that the actual maximum is
exactly `1/7` at `q=3,10`, rather than that those witnesses attain `1/7`,
does additionally require the reviewed global upper bound.

Positive safe duration follows from continuity, with an explicit check
available. The function `f_q(t)=min_v ||vt||` is `(2q+5)`-Lipschitz. At
each nonexceptional witness it is at least `1/7`. Therefore

`|s| < 1/[56(2q+5)]` implies `f_q(t+s)>1/8`.

These witness neighborhoods are inside `[0,1]` and have positive length.
The shrinking radius depends on `q`; the note does not assert a uniform
positive duration over the infinite family. At `q=4` there is exactly zero
safe duration while all four equality witnesses survive. The inference
from margin to duration is sound; adding the continuity sentence would
make the original exposition more explicit, but it is not a substantive
missing lemma.

## 5. What the LTCM test demonstrates

Subject to the other proof components, this passes the original bounded
test: a fixed arrangement plus actual-orbit arithmetic selects a witness
and its exact optimal separation throughout an unbounded parameter ray.
It supplies more than an ambient safe point, a sampled pattern, or a
conditional test for an externally supplied window. The family formulas
meet the stated tiny-language roles: closed labeled cells, a genuine
time-transfer identity, and a selector with a coverage argument.

The statement about a fixed number of operations is appropriately narrow.
There are finitely many residue cases and rational operations; physical
lap magnitudes grow with `q` and their representation/bit cost does not
stay constant. The note explicitly acknowledges this distinction.

The demonstrated mechanism is an application of the credited fixed-lap
polyhedral and relative-spectrum frameworks. This review does not assess
whether the exact appended-coordinate spectrum was previously published;
the separately assigned primary-source review must address that question.
An internally successful calculation does not create novelty for the
representation, integer rounding, or residue splitting.

The remaining generalization gap is concrete. All seven speeds here obey
the same fixed coefficient matrix, the runner count is eight, the initial
phases are zero, and the reference is fixed. A general additive triple
does not constrain the other relative speeds to these rows or establish
that their actual common-time trajectory hits a safe cell. No argument
here bounds arbitrary coefficient complexity, supplies arbitrary-
configuration cell selection, preserves every equality case under runner
addition, or proves a threshold-preserving induction. Changing reference
also changes the relative-speed list, so this spectrum does not classify
the optima of the other seven runners.

Thus the valid next *question*, after the current proof/prior-art audit,
is which explicit additional hypotheses could support a uniform
actual-orbit selection theorem while retaining new-cell and singleton
cases. Merely finding another safe point in a relaxed phase space or
renaming an existing geometric construction would not answer it. No
family extension or new search was performed for this review.

## Reproduction and limits

Before execution I declared to the coordinator the narrow calculation:
two symbolic affine charts and the `q=4` threshold-safe-set reconstruction.
Run from the repository root:

```bash
python3 reviews/2026-09-29-ltcm-ultra-review/semantics_check.py
```

Result: `PASS`, 56 affine endpoint inequalities, and precisely the four
exceptional safe points. Standard-library rational arithmetic only; no
original checker imports. The script does not recalculate any other
physical `q`, any global optimum outside `q=4`, any new family, other
reference, or phase offset. Large witness controls belong to the separate
direct-check review. The analytical parameter identities above concern
the already authorized family and do not derive an extended theorem.
