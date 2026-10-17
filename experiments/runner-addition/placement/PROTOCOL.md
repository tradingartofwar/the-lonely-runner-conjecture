# Placement validation v1

Selected after rule commit `8ecfaae521f80eca72fb137549d67f019452fbd2`.
Freeze this protocol, configuration, code and dependency hashes before execution.
No further added-runner query or new core construction has run at this freeze.

## Questions and selection

1. Does the midpoint obstruction reproduce all 1,888 saved component contacts?
   These are development regressions from the prior study, not new validation.
2. Do the three predicted rational anchors fit their prior 1/10 leaders, satisfy
   their entire cores, and generate correct physical witnesses? Construct the
   full finite set of individual core speeds permitted by each anchor's residue
   inequalities; this certifies arbitrary eight-element subsets conditionally
   on the rational-anchor proof, without enumerating those subsets.
3. On the next two even-q pairs (1,8),(1,10) at 1/10, which complete core
   components can handle every added positive integer speed? Which admit the
   sufficient rational-anchor rule? Preserve the distinction if answers differ.

The two additional pairs are chosen for a structural boundary, not promising
observed outputs. At q=10 the maximum core speed 83 exceeds the anchor rule's
bound 80. At q=8, speed 67 forces anchor denominator v>=9, while core speeds 9
and 10 exclude both possible denominators 9 and 10. Thus **no anchor is expected
for either core**, by the frozen rule, before computing their complete geometry.
This does not predict whether any other interval or full core succeeds.

These are newly specified inputs for this study; earlier repository scans may
have exposed them. No globally held-out sample or statistical validation claim.
Do not add pairs or alter the anchor rule after seeing the outcomes.

## Primary evaluation

Use exact Fraction arithmetic and the unchanged complete-core interval checker.
For each core component, store endpoints and all constant laps. For positive
width w compute R=ceil(2d/w), then check admissible r in increasing order below R
until the first blocker or the cap r<=128. A first blocker suffices to reject
that component's universal coverage; it does not reject the complete core.
If all r<R have passed, label UNIVERSAL_CANDIDATE. If no blocker is found but
some required r exceed the cap, label UNKNOWN_BUDGET. For a singleton u/v, use
the exact blocking speed v. No floating-point tolerance is permitted.

The sufficient-rule search examines every reduced u/v in [0,1], v<=floor(1/d),
and both directions, selecting the first fitting J by (v,u,direction), where
-1 precedes +1. Absence of such J means only NO_ANCHOR_IN_CLASS.

For each of the three declared development anchors, check r=1..32 plus v*10^6,
v*10^6+1, v*10^18 and v*10^18+1. These include repeated core speeds as predicate
controls, not as new ten-distinct-runner configurations. Record phases/laps for
the eight original core speeds and added r. Palette membership is checked over
1<=s<=floor(v*(1-2d)/d); larger speeds are excluded by the proved width condition.

For the two new cores, also inspect complete child-safe sets at every distinct
blocking speed found during component classification. This answers whether
the demonstrated component losses are repaired elsewhere. It does not establish
complete all-r core coverage if all individual components fail.

## Alternate verification and controls

Write a verifier importing neither the primary script nor the existing checker.
Reconstruct complete cores and selected child-safe sets using threshold-event
decomposition. Check placement hits using exact safe-band intersection in the
original clock; verify the entire ordered finite remainder or the first blocker.
Enumerate anchors by direct constant-lap endpoint safety, not the residue rule.
Verify palettes the same way and all saved witnesses directly in physical time.

Controls: exact-width equality [7/8,9/8], d=1/8, r=1 succeeds; singleton 1/8,
r=8 fails; [1/10,1/9], d=1/10, r=9 succeeds at an endpoint; the same-width
interval [0,1/90], d=1/10, r=1 fails; [9/10,11/10] has safe endpoints for
speed 1 at d=1/10 but is not wholly safe (its lap changes).

Same AI author, differently structured code; no independent human or formal
proof certification. Run once, verify, and perform one byte-identical primary
replay. Preserve any defect and require a new version before changing frozen
code. Commands have a 60-second limit. Core speed sums<=600; components<=600;
denominators<=10; finite added-speed cap128. A budget stop stays UNKNOWN.

Stop after this domain, the three symbolic anchor families, and the comparison.
No optimization benchmark, minimum multi-component cover, general q scan,
all-reference claim, or novelty assertion. Results and interpretation go in
separate files; the frozen source documents remain unchanged.
