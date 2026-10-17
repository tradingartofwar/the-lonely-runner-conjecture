# Select a repair component by escaping unsafe gaps

October 17, 2026. Rule freeze before choosing a new validation domain.
Development source: `35f70163baf88e7f1a127cc59469567f822e2d86`, especially
[the two-menu study](../menu-views/RESULTS.md). Same-author AI derivation;
unbounded implications are proof candidates, with no novelty claim.

## Supported question

Given the complete closed core-safe components at a fixed threshold d, can we
select a sufficient menu containing the predetermined widest component without
first constructing the complete component-by-added-speed incidence matrix?
All speeds are positive integers relative to reference 0, with a common start.
An admissible added speed is absent from the core. Period is [0,1]. Require a
positive-width leader; otherwise return UNSUPPORTED_ZERO_WIDTH, not nonexistence.
Break widest-width ties by earliest left endpoint. Component IDs follow time.

## Rule: one common repair point

1. Construct the complete core once. For leader L=[a,b], let
   `R=ceil(2*d/(b-a))` and let D contain every admissible integer 1<=r<R.
2. Use the exact center/half-width predicate to find all leader failures
   `F={r in D: distance(r*c, integers)+r*h < d}`. Retain the blocking integer
   and its open time gap `((m-d)/r,(m+d)/r)` for every such r.
3. If F is empty, return the one-component menu {L}.
4. Otherwise search the core in increasing time for the earliest point safe
   for every r in F simultaneously. Start at each component's left endpoint.
   Test F in increasing speed order. If r is unsafe at t, t lies strictly
   inside one unsafe gap. Jump to that gap's right endpoint and restart F.
   If the jump leaves the component, advance to the next component. Preserve
   equality; touching unsafe gaps do not license removing their shared endpoint.
5. On finding t*, select the component J containing it and return {L,J} plus
   t*. If the complete search finds none, return NO_COMMON_REPAIR_POINT.
   A budget stop is UNKNOWN_BUDGET. Do not silently fall back inside this rule.

Dispatch: if r is in F, use t*; otherwise use the existing first-contact formula
on L. For r>=R the leader's width guarantees contact; below R the complete
failure classification decides. Store physical phases and laps for witnesses.

## Why a returned certificate works; what a failure means

Each jump skips only times known unsafe for its triggering speed. The right
endpoint itself is safe for that speed and must be tested against the others.
Scanning all components therefore finds the earliest common repair point if
one exists, subject to budget. Threshold events are finite for finite F.
Its component is core-safe; t* handles all leader failures and L handles the
rest. If F is nonempty, the forced leader alone fails and a returned two-menu
is minimum within the leader-containing class. An empty F gives minimum one.

This rule asks the stronger question `exists t for all r in F`. A two-component
menu needs only `for all r in F, exists t in J`. Therefore a failed common-point
search need not mean failure of two components, full-core coverage, or LRC.
The previously published disjoint-survival examples motivate checking exactly
this distinction. No minimum claim about menus omitting the leader follows.

## Comparators and accounting

Use three explicitly different operations on the same complete core:

- Gap rule above: exact leader classification, then point probes and certified
  jumps. No access to the complete incidence matrix during selection.
- Lazy two-component selector: same finite leader failures, then try components
  in ID order, testing first contact against F in speed order and rejecting a
  component on its first miss. Return the first component covering F. Otherwise
  report NO_TWO_COMPONENT_MENU; retain the exact minimum-cover result separately.
  This is a competent conventional baseline and permits different times for r.
- Exact minimum cover: build complete finite component contacts, then compute
  the minimum menu containing L using the pinned dynamic program and tie rule.
  This supplies an optimality reference, not an efficiency strawman.

Record core construction size, leader tests, gap point tests/jumps/components
visited, lazy interval tests/components visited, full matrix contacts, and DP
states/transitions separately. Also count first-contact calls to recover one
witness per finite r: gap-rule failures use the saved t*, other r use L; lazy
uses L or its repair component; exact cover tests each selected component and
chooses the earliest successful contact. Report witness storage separately.
Counts of different primitives are not automatically comparable runtime costs.
Complete-set certification and alternate verification are charged separately;
their research cost is not part of the selector's online operation.

## Representation record and failure test

Retain original speeds, threshold, core IDs/endpoints, leader, full finite
domain, F, gap/jump trace, t*, selected menu and physical recovery. Selection
summaries omit other witnesses and optimal loneliness; recover from full
geometry and original predicates before changing the question or constraints.
This is ordinary exact interval and modular reasoning, compatible with the
existing CC model record, not a new LTCM or binary encoding proposal.

Concrete semantic controls must include a shared safe endpoint between two
open unsafe gaps, and an interval with separate witnesses for two speeds but
no common point. The latter must yield common-point failure while the lazy
interval selector succeeds. Preserve every validation failure and all budgets.

Freeze a bounded configuration, code and hashes after this rule is committed
and before computing new core geometry or leader failures. Use an alternate
event-based construction to verify complete sets, the earliest common point,
all returned witnesses, and the exact minimum via subset enumeration. Run once
plus one byte-identical replay. No general advantage or family extension may
be inferred from a few successful configurations.
