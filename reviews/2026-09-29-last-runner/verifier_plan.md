# Independent verification plan: the last-runner speed parameter

Date: 2026-09-29. Research parent: f3c26e709fa1cd8945968dcd585bd012430c7243.

Status: **HYPOTHESIS / proof candidate** for the general criterion and its
finite event reduction. No executable mathematical evaluation has occurred
in preparing this plan. The verifier has not read primary code or outputs.
Only a root-frozen, explicitly bounded protocol will authorize evaluation.

## Independent construction

For each declared integer six-core, construct its safe set on [0,1] by
collecting every rational threshold (8j+1)/(8v), (8j+7)/(8v), together with
0 and 1. Evaluate the original modular distance condition separately at
every event and every open-cell midpoint. Reconstruct maximal closed safe
components, retaining all isolated points. Do not import the primary
component generator or read its results.

Let the largest positive component width be w. Complete coverage by the
last runner is impossible for d >= U=1/(4w), including equality. A connected
closed interval covered by the disjoint open d-blockers must lie inside
one such blocker, which has width 1/(4d). Therefore only the declared
bounded parameter domain c<d<U can require examination; if U<=c it is empty.

Construct all parameter contact events in the closed bounded domain:

    d=(m+1/8)/s or d=(m-1/8)/s,

for every positive core-component endpoint or isolated point s and every
integer m that puts the event inside the domain. Also include the declared
domain endpoints. This construction does not use allowable-band endpoints
from the primary calculation.

At every event d and rational midpoint of adjacent events, independently
reconstruct the full safe time set from the original seven modular
inequalities. Generate the core and d thresholds in t, evaluate endpoints
and open cells, and merge the resulting closed pieces. Each reconstruction
retains isolated equality witnesses. Repeat the coverage classification
with isolated core points excluded if the frozen protocol requests that
contrast. No floating-point tests are needed.

## Why these events suffice

For one positive closed core interval I=[l,r], complete strict blocking
means its continuous phase image [dl,dr] lies in a single open interval
(m-1/8,m+1/8). Thus it is equivalent to

    dr-1/8 < m < dl+1/8.

The truth value can change only at dl=m+1/8 or dr=m-1/8, both present in
the larger contact-event list above. A singleton s is covered exactly
when |ds-m|<1/8 for some integer m, with the same type of contact events.
The conjunction across all components is consequently constant on every
open parameter cell. Direct time-set reconstruction at one midpoint is
therefore sufficient for that cell. Contact events must be evaluated
separately because equality is safe, not blocked.

This argument also establishes the midpoint formulation without a hidden
wraparound assumption. With x=d(l+r)/2 and h=d(r-l)/2, existence of m with
|x-m|+h<1/8 is equivalent to ||x||+h<1/8. The inequality itself forces
h<1/8 and therefore a non-wrapping image inside one block. It is a
criterion for **complete blocking**; it is not a global formula for the
maximum circular distance when the inequality fails.

## Equality and scope alternatives

- No final safe point: all closed components and every isolated core point
  are strictly blocked.
- Only equality witnesses: the final safe set is nonempty but has zero
  duration. This must remain distinct from complete blocking.
- A positive final interval: the final safe set has positive duration.
- Positive components completely blocked but an isolated core point survives:
  this is another possible equality-only mechanism and must not be discarded.
- Positive components may leave only their own endpoints. Omitting isolated
  core points alone does not distinguish that mechanism; preserve the exact
  reconstructed final safe set at requested diagnostic speeds.

For a separate exact duration criterion, the final safe set has zero
positive duration if and only if each positive core component lies in one
**closed** d-block. Its lap criterion is

    dr-1/8 <= m <= dl+1/8,

or equivalently ||d(l+r)/2||+d(r-l)/2<=1/8. If a positive component is
not contained in one closed block, the open complement of the locally
finite closed blockers meets its interior and supplies positive safe
duration. Conversely, containment leaves at most block-boundary points.
Isolated core points do not affect duration. This criterion concerns zero
duration, and cannot replace the strict no-witness criterion.

Real d calculations concern the fixed time interval [0,1]. They are not
full-period conclusions for noninteger d. Integer d makes the unit-period
scope complete. Reflected core components will be retained even when an
integer-d argument could remove them, since real-d coverage need not be
reflection symmetric.

## Freeze and comparison discipline

After receiving the root protocol, write a standalone verifier from this
plan using exact fractions. Freeze the verifier source and independently
computed output before reading any primary code/output. Compare normalized
exact components, parameter cells/events or their equivalent maximal open
coverage bands, integer classifications, and requested diagnostic final
safe sets. Report any representation-only difference separately from a
mathematical disagreement. The bounded computation cannot establish a
universal statement beyond its frozen cases, and separate AI agreement is
not independent external proof certification.
