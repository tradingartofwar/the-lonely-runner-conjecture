# Exact menus from only the leader's exceptions

October 17, 2026. Source: `353531ad1035010a4acdb78994614753d36977d1`.
Ordinary exact interval contacts, memoization and finite set cover; no new
language or novelty claim. AI-generated arguments remain proof candidates.

## Input contract and algorithm

The finite constructor takes sorted disjoint closed intervals, a required
leader ID, a finite sorted positive-integer query domain D, and 0<d<1/2.
Intervals may be singletons. A component covers r when it contains a time with
distance(rt,integers)>=d. Different r may use different times.

1. Query the leader for every r in D, retaining exact first contact and hit.
   Let F be its failures. If F is empty, return the leader alone.
2. Try other components in ID order against F in speed order; reject each
   component on its first miss. The first component covering F gives the
   lexicographically first minimum two-menu containing the leader.
3. If none works, fill the remaining component-by-F contact entries. Reuse
   cached entries; never compute the same (component,r) contact twice.
4. If some r in F has no covering component, return NO_SUFFICIENT_MENU with
   its speed. Otherwise run exact dynamic programming on the residual masks,
   minimizing number of components and breaking ties lexicographically.
5. Retain one cached first-contact witness per exception, using the smallest
   selected component ID that hits. Dispatch other inputs through the leader.

For any menu containing the leader, coverage of D is equivalent to coverage
of F by the other components. Removing already-covered columns therefore
preserves the feasible menus, minimum size and tie rule. The DP recurrence
retains the shortest, lexicographically first subset for each accumulated mask;
adding future components preserves that ordering. This is a complete finite
procedure subject to explicit budgets, not a guarantee that a cover exists.

If two components suffice, optionally search the selected repair interval
for one time safe for all F using the pinned gap-jump routine. A found point
is an extra certificate and may replace per-exception recovery. A missing
point or optional-search budget stop **cannot invalidate the selected menu**.
For one or more than two components, no common-point search is attempted.

## Family extension

For an actual eight-speed core at d=1/10 with stationary reference 0, construct
the complete safe set, choose its widest positive component, and set
R=ceil(2d/width). Let D be every admissible positive integer r<R. The width
tail covers r>=R, so a finite certificate extends to all admissible added
speeds. Attach the core speeds, reference, threshold, physical clock and cutoff
to the certificate. Reject repeated, nonpositive or out-of-domain requests.

Core safety, a complete finite domain and the tail argument are necessary
obligations. A supplied-interval fixture has only a finite-domain guarantee;
it must not be presented as a ten-runner configuration or all-r theorem.
No minimum among menus omitting the required leader is claimed.

## Representation and accounting

The certificate retains selected intervals, leader, exact threshold, domain,
exception-to-witness table, optional common point and (when justified) family
context. The audit retains every computed contact, masks and source geometry.
Unqueried component/speed entries stay absent; an absent entry is not a miss.
Recover the full geometry for complete-set, optimum or changed-input questions.

Count unique first-contact evaluations by stage (leader, lazy, residual fill),
cache reuse, DP states/transitions, optional point probes, certificate size and
dispatcher calls separately. Core construction and full reference verification
remain charged. Cached exceptions cost no new first-contact evaluation at
dispatch, but their discovery, storage and physical checking are not free.

This adapts the previous lazy selector by adding cached residual completion,
exact fallback, explicit failure/budget statuses and a guarded dispatcher.
The inherited first-contact/tail arguments remain under their original
hypotheses. Prove and verify the new cache, fallback, tie and dispatch obligations
against complete event geometry and cardinality-ordered subset enumeration.
