# Exact contact and finite family reduction

October 17, 2026. Elementary derivations adapted from the existing orbit-interval
work. These are proof candidates under repository governance, with no novelty
claim. All times use the original physical clock on [0,1]; p=1 ensures gcd 1.

Let 0<d<1/2, and let I=[a,b] be a complete connected component of the safe set
for the eight fixed positive integer speeds. An added positive integer speed r
is safe exactly on bands [(j+d)/r,(j+1-d)/r], j integer.

## First contact, including equality

The first band whose right endpoint reaches a has

`j = ceil(r*a - (1-d))`.

Its earliest possible common time is `t=max(a,(j+d)/r)`. The band's right
endpoint is at least a, so this t belongs to the band. Thus I survives exactly
when t<=b. Earlier bands end before a, and later bands start no earlier. This
is also valid when a=b. A miss means this component is blocked throughout.

## Tail guarantee

Each connected unsafe time gap is open and has width 2d/r. A closed interval
of width w=b-a>=2d/r cannot be wholly contained in such an open gap. Therefore
it meets a closed safe band. A leader of positive width consequently succeeds
for every integer r>=ceil(2d/w); equality in the width bound is sufficient.
The same first-contact formula constructs the witness without scanning laps.

## Exact finite set-cover problem

Fix the leader before evaluating r. At each admissible r below its cutoff,
each component supplies a Boolean exact-contact entry. A menu containing the
leader is sufficient for every r precisely when it covers all these finite
exceptions. The leader handles the infinite tail. Additional finite comparisons
above a threshold's own cutoff cannot alter this conclusion because the leader
already succeeds there.

An exhaustive finite minimum with the leader forced is an exact minimum within
that class. It says nothing about menus omitting the leader, disconnected unions
counted as single objects, input-dependent sources, alternative encodings, or
general algorithmic complexity.

## How a changed threshold changes the problem

At a fixed ten-runner input, any 1/8 witness is strictly 1/10-safe. Continuity
then supplies a positive 1/10-safe neighborhood. Thus an isolated 1/8 witness
need not remain isolated at 1/10. This is a direct deduction, not an empirical
discovery to be credited to the matched comparison. The comparison asks the
additional operational question: which reusable source menus and exceptions
change when the cores are reconstructed at the weaker threshold?

## Verification obligation

The tail argument needs an actually core-safe interval. Verify all core laps
are constant on it and endpoint phases lie in [d,1-d]; affine motion then
establishes safety throughout. Complete-source claims additionally need the
independent event decomposition. Universal family claims depend jointly on
these facts, exact finite coverage and the first-contact/tail arguments.
