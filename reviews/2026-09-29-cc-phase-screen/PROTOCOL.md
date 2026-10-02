# Frozen boundary-phase screen comparison — September 29, 2026

Freeze before target screening, clipping, contact tables or physical controls.
Initial live source: c7a9886bc49e73968deafd11f9da123a5916ff88.

## Question and informed input

Can the sufficient boundary phase-identity rule guide candidate selection
without losing the full candidate class's coverage? Use the pinned 36 safe
segment records from the nine-runner stage8 certificate: core rows
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2), plus (6,2),(3,8).
Append u=(54,26), replacing the last trial's (38,18). This is the next k=3
after its k=2 in u=(6,2)+8k*(2,1). The input is deliberately informed by that
relationship, not blind or randomly held out; no target trial has run.

The total speeds are zero plus ap+bq for the nine moving rows. Positive
integer p,q give ten distinct speeds iff p!=q and p!=2q, since u dominates
every previous row. Common start, stationary reference, one witness and
closed threshold 1/8. Success implies 1/10; failure at 1/8 does not refute
that weaker target. This experiment keeps 1/8 fixed to test the selection
restriction. No 1/10 regeneration or other row is part of it.

## Exact sufficient screen

Enumerate the 8 existing safe rows v in source order and 6 core rows c in
source order: exactly 48 coefficient-pair tests. Retain all relations
u-v=8k*c for a nonzero integer k, solving the two coordinates exactly.
This is a finite algebraic check, not a search over possible k or u.

For every one of the 36 source records, test every retained relation. Accept
the entire record if c has the SAME raw value at both endpoints equal to
m_c+epsilon for epsilon=1/8 or 7/8, using its retained core lap m_c.
The ninth lap is m_v+8k*m_c+k for epsilon=1/8, or m_v+8k*m_c+7k for 7/8.
Keep every reason in lexicographic (v_index,c_index,k,epsilon) order. Use its
first reason to derive the label and verify all other reasons agree. Check
all nine bands at both endpoints. Retain singleton records and provenance
duplicates; points cannot serve as descending leaders. Never use a selected
control time or physical outcome to accept an edge.

The screen performs no new-row lap enumeration or partial clipping: each
source is accepted whole or omitted. Omission means NO_SCREEN_CERTIFICATE,
not unsafe. Save all 36 decisions and all coefficient checks. Lap shifts
and raw differences must survive phase equality.

## Full comparison branch and regression

Independently append u to ALL 36 source records by exact closed affine
clipping. For endpoint raw extrema enumerate laps
ceil(min(raw)-7/8) through floor(max(raw)-1/8). Preflight at most 256
source/lap attempts and emitted records. Record partial clips and points.
Map the local clip parameter back to each original parent-edge parameter:
s_original=s0+s_local*(s1-s0), with the source's pinned interval [s0,s1].
Numerical provenance key: (parent,edge_start,edge_end,seventh,eighth,ninth lap).
Candidate identity is the source id followed by :M<ninth_lap>. Both branches
use the same candidate field schema as the preceding ten-runner trial.

Before the target screen/full branch, run this sequential full clip with
the old row (38,18) and reproduce every field of its archived coverage
certificate exactly, including candidate endpoints, original parameters,
labels, ranking, all contacts and choices. This validates the changed input
path against the existing simultaneous clip; do not rerun old physical
controls. It is a regression, not another target or blind trial.

For both target branches import the old coverage compiler without edits,
replace only its module-local provenance key, and correct domain metadata.
Keep first descending leader, smallest exception rectangle then provenance,
400-pair rectangle budget, full positive primitive residual matrix, maximum
gain greedy fallback and provenance ties. No alternative leader, post-result
rule change, modified budget or repaired rerun. Preserve raw status and derive
PRIMARY_COMPLETE separately only if a complete matrix misses auxiliaries alone.

## Exhaustive candidate-class comparison and evidence recovery

If both runs reach their complete residual matrices, form the sorted union
of their residual pairs (at most 800 from the two rectangle bounds). Test
each pair against ALL candidates in each branch, retaining contact ids and
the first contact record. Outside this union both leaders have width at
least one, hence both classes hit; the comparison then exhausts possible
coverage differences over all positive primitive directions. Distinguish
primary P!=Q,P!=2Q and auxiliary directions. Use the same direct comparison
on any reached finite union after a stop, but label it bounded only if either
complete finite-reduction prerequisite is missing. Menus are not substitutes
for candidate classes in this comparison.

Verify every screened candidate equals a full candidate with the same id,
labels, endpoints and original parameters. For the lexicographically first
primary direction missed by all screened records but hit by a full record,
retain its first full contact in provenance order, recover a physical witness,
and identify its omitted source and exact failed screen predicate. Do not add
that witness to or rerun the restricted compiler. It is a diagnostic of loss.

Only if the FULL compiler reaches UNCOVERED_PRIMITIVE_PAIRS with a primary
miss: diagnose its first primary miss using all complete six-core parents,
three added lap bands and integer H=Qx-Py. Use the previous ten-runner
diagnostic's exact interval method with u changed as data. Global lap ranges
come from [1/8,1/2] x [1/8,7/8], H from [Q/8-7P/8,Q/2-P/8]. Preflight
100,000 parent/lap/lap/lap/H tuples. Visit numeric parent/laps/H order;
choose the midpoint or singleton of the first nonempty x interval. Keep
section trace and edge membership, or exact one-pair exhaustion, or scope
stop separately. No candidate enrichment or subsequent threshold change.
Independent physical review of this conditional pair may use full physical
band unions with sum-speeds cap10,000 and interval/band-test cap200,000.

## Controls, costs, review and scope

Use the same 22 pairs as the ten-runner protocol in each target branch:
(1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1),
(1,6),(2,5),(3,2),(3,4),(4,3),(5,2),(5,7),(3,5),(4,6),(6,10),
(2,2),(4,2),(1,20),(2,40).
On a complete primary domain use its menu for primary controls; on auxiliaries
use it only if full-complete; otherwise use every candidate in provenance
order. Record first witness or candidate miss, original gcd, direct cardinality,
all nine phases and laps, reflection1-t and alternative Bezout recovery.
Record open-contact results for emitted menus and all candidates separately.
Missing contacts and resource stops are not physical nonexistence certificates.

Cost record: existing 36-source input is supplied and its earlier generation
is not free work newly done by either branch. Report coefficient checks,
relation/segment checks, lap attempts, candidates, descending count, rectangle,
residuals, contacts and menu entries separately. These are unlike operations;
do not sum them into a runtime claim or infer speed from record counts alone.

Separate AI arithmetic, physical and proof reviews; independent arithmetic
and recovery do not import production code. Review reached fields, the subset
relation, union comparison and lost-witness diagnostic. Reproduce only frozen
outputs once; preserve corrections and their timing. Internal AI review is
not blind, external human or formal proof. Prior packages remain unchanged.

CC carries its supported question, same-point bands, all laps, boundaries,
domain and physical inverse map. Screening retains a sufficient phase-identity
proof but omits other safe configurations; full candidates are the immediate
recovery source and full parents the next source. Check what each source can
actually establish. Reuse the credited segment/physical-lap frameworks in the
pinned literature comparison; no new literature, priority or frontier claim.
Universal arguments remain HYPOTHESIS / internally reviewed proof candidates.
No broad scan, outside contact, main merge, paid compute or unattended task.
Save the full bounded comparison and any clean failure on the research branch.
