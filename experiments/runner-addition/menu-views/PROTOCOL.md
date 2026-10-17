# Menu and representation comparison v1

Freeze protocol, exact inputs, code and dependency hashes before evaluation.
Parent/source commit: `a74bf46a4d96e554b50e71ea191cc8223253beb5`.
The proposal and transformation meanings are in MODEL.md.

## Domain and primary question

Use only the previously reconstructed cores (p,q)=(1,8),(1,10), threshold 1/10,
with common-start speeds (0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r).
Reference is 0; r is a positive integer absent from the eight moving core speeds.
These are exposed follow-ups. There is no held-out or statistical claim.

Copy all 26 and 34 complete components from the pinned placement result. Fix
the widest component, earliest left endpoint breaking ties. Its known cutoffs
are 21 and 23. Evaluate **every** admissible r below that core's cutoff.
No larger parameter box or additional threshold is permitted.

Reuse the unchanged prior primary evaluator for exact component contacts,
complete child sets, physical witnesses and minimum set cover containing the
fixed leader. Minimum ties use lexicographically sorted component IDs. Keep
NO_SUFFICIENT_MENU for a full-core miss and UNKNOWN for a budget stop. The leader
handles every r at or above its cutoff by the previously derived width argument.

Cross-stage corollary: if a size-two menu succeeds, the pinned placement study's
explicit blocker for every single component supplies the lower bound two even
when the leader requirement is removed. If more than two are selected, do not
claim unrestricted minimality without a separate argument/search.

## Explanatory views

1. Reconstruct exact component/speed bitmasks and their explicit axis labels.
2. For every contact compute center/half-width value, the blocking integer if
   any, and its open unsafe time gap. Require agreement with the contact bit.
3. For the selected menu record failure sets **within the leader remainder**,
   their intersection, and the unsafe gap centers m/r for leader failures.
4. Try the selected nonleader components' left endpoints, sorted by physical
   time and ID, as one fixed repair time for all leader misses. If one works,
   store it and the exact exception list. Otherwise keep per-case recovery;
   do not tune a new search after observing failure. This supplements the
   constructive first-contact rule and does not imply a speedup.
5. From the already computed surviving pieces, search lexicographically by
   (pair order, component ID, r, s), r<s, for one component where each added
   speed separately has a witness but their surviving pieces are disjoint.
   Return the first example per core, or NOT_FOUND_IN_DOMAIN. This is a
   composition diagnostic at the fixed threshold, not an eleven-runner LRC
   counterexample, an all-core nonexistence claim, or a new scan of velocities.

## One exact time-state case

Use the saved (p,q,r)=(1,8,3) failure/recovery example. Build the complete ordered
threshold events on [0,1] for the eight core speeds and r=3. Record each event
point separately, and each open cell between consecutive events, with a bit
for each runner's distance predicate. Include ordered speeds, exact endpoints
and a representative time. Bit strings list speed indices 0..8 left to right.

Decode the all-true records back into the complete safe set and compare with
the interval solver and saved placement result. Inspect the state immediately
before, at, and after four preselected boundaries: the old widest interval's
endpoints and the first saved child-safe interval's endpoints. Report which
runner conditions change; do not select a visually persuasive new example.

Semantic fixture: speeds (1,2), threshold 1/3 must retain the two isolated
all-true times {1/3,2/3}, even though no open cell is all true.

## Verification, budgets and stop rules

The alternate wrapper reuses prior event decomposition and cardinality-ordered
subset enumeration, importing neither the primary evaluator nor its checker.
Verify the complete cores/child sets, every contact, all witnesses, bit axes,
blocking gaps, minimum size/tie, fixed repair time and composition diagnostic.
For time states, verify each point by safe-band membership and each open cell
by whole-band containment or empty interior intersection, not by sampling a
second midpoint. Check event completeness and decode the full safe set.

Publish the execution freeze before running. Require all local and archived
dependency hashes to match. Run primary once, alternate verification, then one
byte-identical primary replay. Preserve any defect and version a fix separately.

Caps: core speed sum600, components600, cutoff128, DP100000 states/2000000
transitions, verifier1000000 subsets per core, composition100000 pair trials
per core, time trace2000 event points, each command60 seconds. UNKNOWN is not
failure of the mathematical conjecture. Stop if a discrepancy prevents claim
promotion; preserve results and diagnose rather than silently changing rules.

End after these two minimum-menu decisions, their placement explanations and
the single time-state case. A clearer argument, verified new distinction, or
working transfer operation counts as progress. No general representation
superiority, intrinsic incompressibility, novelty, or all-reference result.
