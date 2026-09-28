# Challenge review: alignment changes strictness, but these controls cannot lose all solutions

September 28 UTC, for the September 27 Pacific protocol. Scope: only
`{0,1,4,5,6,7,11,13}`, `{0,1,4,5,6,7,11,16}`, and the 29 explicitly authorized
shifts of runner 11. Material AI involvement: exact calculations, mathematical
review, and writing. No new speed list or numerical phase scan was added.

**The finite thought experiment demonstrates loss of alignment information
about duration and strictness, not about global nonemptiness.** Every shifted
arrangement remains nonempty. In fact, supplied continuous-phase arguments
explain a stronger limitation of these controls: for V=13 every nonzero phase
of 11 gives positive duration, while phase zero retains four contacts; for
V=16 every phase has positive duration bounded below by 1/176. These are
**HYPOTHESIS / proof candidates**, not extrapolations from the 29 calculations.
The exact finite comparisons are **OBSERVED** and independently reconstructed
within the checker scope stated below.

## 1. The smallest exact distinction is already visible before the fastest-lap decomposition

Let A be the complete safe set of residual speeds 1,4,5,6,7,11 at threshold
1/8. Exact closed intersections give four isolated points

`1/8, 3/8, 5/8, 7/8`

and four positive components: the intervals

`J1=[17/56,5/16]`, `J2=[41/88,15/32]`

and their reflections under t -> 1-t.

Speed 13 strictly blocks both J1 and J2, and therefore their reflections.
For example their images lie respectively inside the strict blocking laps
around integers 4 and 6. It is safe at all four isolated points. Thus the
complete answer for V=13 consists exactly of those four contacts.

Speed 16 instead collides at all four isolated points. On J1 its safety leaves
`[17/56,39/128]`, of length 1/896; it is safe throughout J2, of length 1/352.
The reflected intervals also survive. Total duration is

`2/896+2/352 = 39/4928`.

The positive endpoint differences have integer numerators one:

`7*39-16*17=1`, `11*15-4*41=1`.

These equations explain the two exact widths after the other constraints have
been checked. A positive endpoint difference alone does not establish safety
for the remaining runners.

This factorization is a useful explanation, but cannot be presented as a new
universal no-cover mechanism: constructing A already solves the full
six-residual conjunction. Writing the answer as `A intersect safe(V)` does
not bypass the existence problem. Fastest laps organize that same geometry
into intervals where the tree expression is exact.

## 2. The phase operation has a precise, limited preservation claim

In normalized lap coordinates `t=(m+u)/V`, replacing runner 11's pattern by
the pattern from `(m+s) mod V` changes its phase to `11s/V mod 1`. Both
gcd(11,13) and gcd(11,16) equal one, so only s=0 has zero phase. The other
unchanged runners include speed 1, hence there is no alternative time when
all runners in a nonzero-shift arrangement share a common start: speed 1
would require integer time, at which runner 11's nonzero phase remains.

The operation preserves every runner's multiset of normalized lap patterns,
including its individual durations, but not the alignment of different
runners. It is an actual shifted-start comparison. It is not an LRC
counterexample, a common-start deformation, or a preservation theorem for
pair statistics.

The latter limitation occurs already at the first shift. Over the union of
all fastest safe laps, exact durations are:

| V | Quantity | s=0 | s=1 |
| ---: | --- | ---: | ---: |
| 13 | Single duration D1 | 5/26 | 5/26 |
| 13 | Single duration D11 | 27/143 | 27/143 |
| 13 | Pair overlap O1,11 | 5/143 | 6/143 |
| 16 | Single duration D1 | 3/16 | 3/16 |
| 16 | Single duration D11 | 3/16 | 3/16 |
| 16 | Pair overlap O1,11 | 37/704 | 5/128 |

Thus any claimed information loss must identify the retained information as
individual inventories; claiming that the same pair moments have different
answers would be false for these exhibited comparisons.

Shifting all residual patterns together is a different operation: it is the
global time translation t -> t+s/V, under which fastest safety is unchanged.
The control's invariant totals and permuted local records are required
consistency checks, not independent evidence that arbitrary rearrangements
preserve answers.

## 3. Strong negative result: no phase can eliminate all solutions in either control

Write theta in [0,1) for an arbitrary initial phase of speed 11, with all other
speeds unchanged. The following supplied arguments use only the two fixed
speed lists; no further numerical phases are tested.

**V=13: theta=0 is the unique zero-duration phase.** The unchanged runners are
safe throughout

`Kleft=[17/48,3/8]`, `Kright=[5/8,31/48]`.

Their 11-phase images, with convenient integer lifts, are

`[-5/48,1/8]`, `[-1/8,5/48]`.

Their union is exactly the closed arc `[-1/8,1/8]`, of length 1/4. A shifted
blocking arc of the same length, separated by `d=||theta||` on the circle,
overlaps this arc in measure `max(1/4-d,0)`. At least `min(d,1/4)` of phase
measure survives. Pulling back, with multiplicity at least one, gives

`D13(theta) >= min(||theta||,1/4)/11`.

This strengthens the earlier one-sided neighborhood argument, whose plateau
was 1/48 rather than 1/44. That direct argument remains a valid witness
construction: for `0<theta<=1/2` use an interval ending at 3/8 of length
`min(1/48,theta/11)`; for the other half of phases reflect to one beginning
at 5/8. Speeds 5 and 13 are upper-threshold controllers at the first contact
and lower-threshold controllers at the second.

The known phase-zero geometry above gives D13(0)=0 with four valid points.
This explains all twelve nonzero prescribed shifts becoming strict. It does
not show that arbitrary shifted-start configurations remain feasible.

There is also a simpler contact obstruction to global emptiness. At t=1/8
and 7/8, the unchanged pair 1/7 supplies isolated contacts and every other
unchanged runner is safe. The two phases of runner 11 differ by 1/4 modulo
one, so its strict blocking arc of width 1/4 cannot remove both. At least one
isolated contact survives every theta. All four odd eighths are unchanged-safe
and quarter-spaced in runner 11's phase; at least three remain feasible points,
though some can join positive intervals after the phase change.

**V=16: a uniform positive bound holds at every phase.** The unchanged five
slow runners and speed 16 are safe throughout

`J=[25/56,15/32]`, `1-J=[17/32,31/56]`.

Under multiplication by 11, choose phase lifts for these intervals as

`[-5/56,5/32]`, `[-5/32,5/56]`.

Their union is `[-5/32,5/32]`, of phase length 5/16. A shifted strict blocker
of runner 11 occupies only 1/4 of the phase circle, so at least 1/16 of this
union remains safe. Pulling back gives at least `1/(16*11)=1/176` of allowed
time across J and its reflection. Overlapping phase images only increase
preimage multiplicity; they do not invalidate this lower bound.

The comparison is now particularly concrete: the selected V=13 phase union
exactly fits an arc of blocking width 1/4 at phase zero, whereas the V=16
union is too wide by 1/16. This is an explanation for these two certified
regions, not a theorem that an analogous wide phase union always exists.

The V=16 bound is attained on this restricted pair of intervals at theta=0. It is
not claimed sharp for the full schedule, whose phase-zero duration is the
larger value 39/4928.

One can also identify the full phase projection of the V=13 unchanged-safe
set as `[-1/8,1/8] union {3/8,5/8}` modulo one. The selected K intervals
already supply the closed arc. Any additional phase outside that arc would
survive runner 11 at phase zero; the already computed four-point global
answer restricts such phases to 3/8 and 5/8, both attained. This inference
uses the known tight answer; it must not be advertised as an independent
universal proof of that answer.

The measured outcomes therefore have a narrow interpretation:

- V=13: s=0 has contacts only; every s=1,...,12 has positive duration.
- V=16: every s=0,...,15 has positive duration.
- Neither inventory-preserving experiment changes global nonemptiness.

The earliest shift changes duration and local statuses in both cases. V=13
also changes global strictness and contact counts; V=16 does not change its
global strict status or its zero isolated-contact count. The absence of a
global emptiness change is substantive counterpressure against claiming that
this particular experiment demonstrates loss of global feasibility.

## 4. Contact arithmetic is necessary information, not a global sufficiency theorem

For integer speeds a,b and g=gcd(a,b), oppositely oriented threshold contacts
exist exactly when `(a+b)/g` is divisible by 8. For example

`b(8p+1)=a(8q+7)`

is solvable exactly when `8g` divides `7a-b`, equivalently a+b. Same-oriented
contacts instead require `|a-b|/g` divisible by 8. These equivalences are
sound pairwise arithmetic statements; they do not assert that other runners
are safe at the resulting time.

The fixed controls themselves provide the required counterpressure. Pair
1/7 gives the opposing contacts 1/8 and 7/8, and pair 5/11 gives 3/8 and 5/8.
All four are destroyed by the exact collisions of speed 16. Speed 13 joins
speed 5 in the same safe direction at 3/8 and 5/8 because 13-5=8. These facts
explain controllers, but the divisibility conditions alone cannot certify a
surviving contact.

Likewise, the shared residues obey `r_v(m)=vm mod V` and therefore
`r_v(m)-v*r_1(m)=0 mod V`. Shifting only 11 changes the latter difference to
11s modulo V, whereas a simultaneous shift preserves it. This distinguishes
a common time origin from misalignment. No supplied inequality derives the
existence of a gap or contact from this congruence alone. The exact duration
is a cyclic correlation of the fixed-runner safe pattern with the 11 pattern,
not a function of the separate pattern inventories.

## 5. Full-envelope touches differ from arbitrary pair touches

An arbitrary pair of blocker endpoints can touch while a third blocker
covers that time. A touch of the **full sorted-union frontier** used by this
protocol cannot be hidden that way on these nondegenerate laps. Earlier
intervals end no later than the frontier; later intervals start no earlier
than the touching point. Interior endpoints of the strict blocker intervals
exclude that point. Hence every genuine full-envelope touch survives.

Both recorded internal envelope touches survive: 1/8 and 7/8 for V=13.
Its other two contacts, 3/8 and 5/8, are fastest-lap boundary contacts. Thus
counting only internal chain touches misses half of the equality solutions.
Strict endpoint flags at the boundaries remain necessary.

For interval blockers, complete coverage requires boundary coverage and an
advancing chain with genuine overlaps rather than uncovered gaps or surviving
touches. Coverage almost everywhere permits those contacts. Tree equality
recovers duration exactly but cannot distinguish these two notions when its
value is zero. A cross-lap proof would still have to rule out complete coverage
on every lap; redescribing each lap as a chain does not accomplish that step.

## 6. Primary output audit and scope of independent checking

The primary archive has 29 exact-tree laps: 21 covered, four contact-only,
and four strict. There are 21 declared qualitative-signature groups, four
with status collisions. Those four are two reflection-paired mechanisms:
contact versus covered, and covered versus strict. They are not four
independent experiments.

The signature intentionally omits window geometry, flags, and comparisons
between one blocker's right end and another's left end. The collisions
disprove sufficiency of that precise compression within the 29-lap domain.
They do not strengthen the older matched-map claim to identical exact windows
or show failure after restoring the omitted geometry.

The separate [challenge checker](challenge_check.py) imports no project or
other review implementation. Closed-safe interval intersections reconstruct:

- A for the six residual runners and the analogous five-runner set;
- every authorized phase arrangement's complete allowed set, isolated
  points, duration, status, reflection symmetry, and direct endpoint/midpoint
  safety;
- all 29 original lap allowed sets, compared with the primary output;
- the displayed pair-overlap counterchecks and exact interval geometry used
  in the continuous-phase candidate arguments.

It finds no discrepancy in that scope. It checks the primary tree bound
against independently reconstructed duration but does not itself recompute
the spanning-tree optimum, blocker maps, or coverage-scan construction; the
dedicated independent verifier owns those broader comparisons.

```bash
python -B reviews/2026-09-27-fastest-laps/challenge_check.py --check
```

[challenge_checks.json](challenge_checks.json) pins its protocol, source, and
inspected primary/phase archives. The supplied continuous-phase arguments
remain proof candidates under repository rules; neither these finite checks
nor agreement among AI reviewers establishes a general common-start theorem.
