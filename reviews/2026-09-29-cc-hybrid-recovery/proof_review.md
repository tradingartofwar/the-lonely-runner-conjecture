# Separate proof review: contact-first exception recovery

September 29 maintainer date / September 30, 2026 UTC. This is a separately
tasked internal AI review, not blind replication, external human review or
formal certification. The preliminary argument below was written before
hybrid target computation or timing. It does not presume a successful run.
No target search or production-code import was performed for this review.

Frozen protocol SHA256, verified from disk:
`eb3a894b8d2c411b177ef26f3916a0138adad975f9848a590aaaf1ee11723ccf`.
The pinned source head is `54f9a2ea0a654afc9326668e4c3bc92e31f31567`.
The experiment repairs the known (54,26) screen failure; it is not a new
coefficient, runner count, threshold or held-out transfer.

## 1. Fixed-pair equivalence of the two operations

Let a pinned eight-row safe source be Z(s)=A+s(B-A), 0<=s<=1, at threshold
z=1/8. For one fixed positive primitive pair(P,Q), write

    H(s)=Q*x(s)-P*y(s),  U(s)=(54,26) dot Z(s).

Both full append clipping followed by orbit contact and contact-first
recovery seek exactly the set

    {s in[0,1]: H(s) is an integer and
                 m+z<=U(s)<=m+1-z for some integer m}.

The operation order changes enumeration and possibly the first witness;
it does not change this set or its nonemptiness. The two implementations
must not be required to choose the same point merely because both succeed.

If H is nonconstant, every integer between ceil(min H) and floor(max H)
has exactly one source parameter s. Testing these integers exhausts all
possible contacts, regardless of projection orientation. At each point the
only possible safe lap is floor(U(s)): since z>0, every safe phase lies
strictly inside its unit interval. Thus testing whether the fractional part
is in[1/8,7/8] is equivalent to testing all integer safe bands. An unsafe
first contact is not sufficient to reject the source; every later integer
must be tested until success or exhaustion.

If H is constant and noninteger, the source has no orbit contact. If H is
constant and integer, every parameter is compatible. The exhaustive new-lap
range is ceil(min U-7/8) through floor(max U-1/8). For each lap, its safe
intersection with[0,1] is a closed interval, a singleton or empty. The least
parameter of the first nonempty closed interval is a valid deterministic
witness. Constant U is included: either the entire source is safe for its
unique label or no band survives.

A point source A=B is covered by the same constant-H and constant-U cases.
Its parameter interval may be nontrivial, but it represents one geometric
point. Its relative interior in its affine hull is the singleton itself.
The protocol instead declares an open-source endpoint-deletion convention
that removes singleton sources entirely. For a nondegenerate source, open
diagnostics use0<s<1 and must not require an unattained least element of an
open interval. A rational interior choice, or an interior singleton when
permitted, suffices.

All inequalities are closed for the actual selector. Endpoint phases1/8
and7/8 and integer contacts at projected endpoints must remain admissible.

It follows source by source, and then over all36 sources, that contact-first
recovery succeeds if and only if some full appended candidate has an orbit
contact, provided exhaustive recovery completes. A budget stop establishes
neither side's emptiness. Exhaustion establishes only `NO_SOURCE_CONTACT`
in this supplied edge class, not physical nonexistence.

## 2. Preflight bound and provenance

For a source/pair combination let n_H be the count of projected integers
and n_m the count of whole-source possible new laps. If H is nonconstant,
the recovery performs at most n_H point-phase tests; this is bounded by
n_H*max(1,n_m). If H is constant and integer, n_H=1 and at most n_m band
tests occur. If H is constant and noninteger, n_H=0 and no contact is
tested. Thus the protocol's sum bounds the prescribed kernel work in all
cases, while intentionally overcounting some nonconstant-H work.

Preflight still evaluates every missing-pair/source combination's projection
and raw range, even if later first-success stopping avoids many source
visits. This work must be charged. The4,096 cap is a resource bound, not a
mathematical obstruction. A zero-budget test should therefore produce a
scope status rather than a fabricated missed physical witness.

If the selected local parameter is s, the original parent-edge parameter is
s0+s*(s1-s0), using the source's retained interval. This affine map also
handles endpoint and degenerate cases. The inherited eight laps, derived
ninth lap, source identity, H and both parameter descriptions must travel
with the witness. Subsequent comparison with a full clipped candidate checks
membership and identical labels, not an unproved equality of selection order.

## 3. Conditional uniform coverage from a finite dispatch table

The unchanged screen's descending leader gives a positive projection width
alpha*Q+beta*P. Width at least1 guarantees an integer contact; every possible
leader miss lies in the proved finite rectangle and strict residual domain.
Its completed greedy menu covers all residual pairs except the recorded
uncovered set E. This conclusion requires the completed matrix, not just a
partial or budget-limited run.

Suppose contact-first recovery succeeds for every(P,Q) in E. Store one
compatible safe point under that primitive pair, and dispatch to it only
after gcd normalization. For all other primitive pairs use the original
screen menu. Outside the residual domain the leader works; inside it the
menu works unless the pair belongs to E, where the stored point works.
This proves the conditional uniform guarantee without rerunning the compiler
or treating recovered points as a new globally ranked segment menu.

If any residual pair remains unresolved, the complete-family status must
remain false and dispatch on that pair must fail visibly. Successful queries
elsewhere may still be retained with their precise scope.

## 4. Physical recovery and the supported representation

For p=dP,q=dQ, an integral contact h=Qx-Py and Bezout coefficients rP+sQ=1,
put T=rx+sy, N=floor(T), tau=T-N and t=tau/d. A row(a,b) with torus lap m
has physical lap

    m+(-a*s+b*r)*h-(a*P+b*Q)*N.

The identities P*T=x-s*h and Q*T=y+r*h prove that every retained phase
occurs at this same t. Positive coordinate phases imply0<t<1/d. Scaling
an exception pair changes time by1/d while preserving torus phases, which
is why the dispatch key must be primitive. Physical laps, gcd and reflection
1-t still need their own exact checks.

Ten distinct speeds require p!=q and p!=2q, since the appended row dominates
all earlier rows. The full labelled construction may cover the two excluded
primitive directions as auxiliaries; these have nine distinct speeds.

The representation is designed to carry one selected witness for each
parameter input. A recovered point is not asserted to parameterize a full
safe interval, all witnesses or an optimum. The point could also contact
other primitive directions, but no such reuse or coverage is inferred here.
The richer supplied source segments remain the recovery route. Parent
interiors and other thresholds are outside this experiment.

## 5. Cost and evidence limits

The two methods share source validation and supplied preprocessing. Hybrid
screening, its residual matrix, recovery preflight and actual queries are
different operations from full lap clipping and full residual compilation.
Materializing fewer segments does not itself prove lower runtime. Earlier
generation of the36 sources is retained as supplied work, not erased.

The frozen paired timing can support a bounded claim about these two
implementations, this known input and this execution environment. It cannot
prove a complexity improvement, general speedup or a held-out benefit.
Imports, parsing, physical controls, comparison audits and file writes are
explicitly outside that timing. Native trace construction remains inside,
so the exact implemented workloads, not idealized abstract operations, are
being compared. Any elapsed-time stop must remain visible rather than be
replaced with extra favorable repetitions.

## Preliminary finding

PASS for fixed-pair equivalence, all affine degeneracies, closed equality,
the preflight bound, conditional global dispatch proof and declared scope.
The protocol correctly separates development repair from new transfer and
construction inputs from after-construction regression data. Reached results
and final review findings remain to be added after execution.

## 6. Final outcome review

After execution I inspected `hybrid.py`, `hybrid.json`, `audit.json`,
`summary.json` and `timing.json`, without rerunning the target or importing
production code. The first coordinator run required no correction. The
screen and its entire certificate remain equal to the archived restricted
certificate. Full clipping and compilation, performed after hybrid
construction, reproduce the archived full certificate exactly. Construction
does not consult those archived comparison results as a source-selection,
lap-selection or point-selection oracle.

The same leader covers every primitive direction with Q+2P>=18. The
complete47-pair residual domain leaves exactly the recorded exceptions
(1,2),(1,4),(5,1). All three are recovered in the frozen source order:

| Primitive direction | Recovered point | H | New torus lap | Primitive physical time |
| --- | --- | ---: | ---: | --- |
| (1,2) | (1/8,1/4) | 0 | 13 | 1/8 |
| (1,4) | (1/8,1/2) | 0 | 19 | 1/8 |
| (5,1) | (1/8,9/40) | -1 | 12 | 9/40 |

The first and third use source P0:E0-1:K1:L2; the second uses
P1:E0-1:K1:L4. Their local parameters are1,1,1/5 and original parent-edge
parameters1,1,4/5. The first two points are source endpoints; the third is
in its source's relative interior. In each case the integer orbit identity
holds and the appended phase is safe:1/4,3/4,3/5 respectively.

The membership audit locates each point in the full candidate of its source
and new lap, with identical inherited labels and original parameter mapping.
All47 residual dispatch checks succeed, including nonexception directions.
All24 declared physical controls succeed, including the added (5,1),(10,2)
pair and its scaling;20 controls have ten distinct speeds and four are
labelled auxiliaries. These checks complement, rather than replace, the
infinite-tail and complete-residual proof.

The final representation is the original three-segment screen menu plus a
three-entry primitive-direction point dispatch table. It is not a six-segment
menu, a newly optimized menu or a uniform geometric reuse of the recovered
points. The completed exception table satisfies the hypotheses in section3,
so `COMPLETE_HYBRID_CERTIFICATE` is justified as an internally reviewed
construction candidate for this fixed family.

## 7. Reached branches and the openness diagnostic

Closed recovery visits11 sources and performs three integer-H tests and
three point-phase tests. No constant-integer-H band branch is reached in
these actual target recoveries. The four predetermined synthetic fixtures
separately exercise an unsafe first point followed by a safe later contact,
a positive-length constant-integer-H safe band, constant noninteger H, and
a safe singleton. They are kernel evidence, not four additional physical
runner configurations. The zero-budget control returns
`RECOVERY_SCOPE_LIMIT` with required work bound33.

The open-source diagnostic also recovers all three directions, using:

| Primitive direction | Point in an open supplied source |
| --- | --- |
| (1,2) | (7/40,7/20) |
| (1,4) | (41/88,19/22) |
| (5,1) | (1/8,9/40) |

The first two therefore have alternative source-interior contacts despite
their closed rule selecting endpoints. This does not alter the closed
dispatch table. Opening the original supplied source removes its original
endpoints; opening every newly clipped candidate would also remove newly
created clipping endpoints. Those are different operations in general.
Moreover source-interior membership does not make every safety inequality
strict: an entire source edge can have a core phase fixed at1/8 or7/8.
Geometric relative interior, phase-band equality and physical openness must
remain distinct.

The open diagnostic uses47 source visits and eight integer/phase tests; it
is an audit rather than part of the timed closed construction. Neither the
target's three successful nonconstant projections nor these open results
alone validate all affine degeneracy cases. The proof and labelled synthetic
fixtures provide the separate support for those branches.

## 8. Observed costs and timing, with their limits

Preflight evaluates all108 exception/source projections and all108 new-row
raw ranges before first-success stopping. It counts17 potential integer-H
contacts and yields conservative work bound33 under the4,096 cap. These
evaluations remain real hybrid work despite only11 sources being queried
afterward.

| Quantity | Hybrid | Full baseline |
| --- | ---: | ---: |
| Source endpoint/band validation checks | 576 | 576 |
| Coefficient relation checks | 48 | Not used |
| Source boundary checks | 36 | Not used |
| Appended lap-enumeration attempts | 0 in actual closed recovery | 61 |
| Materialized safe segments/points from clipping or screening | 5 screened records | 61 clipped records |
| Residual contact-matrix entries | 235 | 2,867 |
| Recovery preflight projections / raw ranges | 108 / 108 | Not used |
| Actual recovery source visits / point-phase tests | 11 / 3 | Not used |
| Retained operational selector | 3 segments plus3 keyed points | 5-segment menu |

The hybrid still computes whole-source lap-count bounds during preflight;
zero actual parallel-band enumeration does not mean it did no new-row range
work. The unlike operations in this table must not be combined into a single
abstract speedup count.

All11 predeclared paired timing rounds completed after one warmup per method.
The full median was37,902,064ns, and the hybrid median was10,073,670ns.
The median of per-round full/hybrid ratios was approximately3.784. These are
different summaries: the ratio of medians is not asserted to equal the
median paired ratio. Timing included source validation and native traces,
and excluded discovery, imports, parsing, audits, physical controls and
writes as frozen. The recorded environment was Python3.12.14 on Linux with
default garbage collection. No extra repetitions or correction cycle was
used to improve the timing result.

This is evidence that this implementation of the development repair was
faster on this supplied, already known input in this environment. It is not
a general complexity or portability result. Earlier discovery of the36
source records remains supplied preprocessing; neither method eliminated it.

## Final finding and appropriate next question

PASS for the reached complete hybrid construction, recovered-point labels
and source membership, global dispatch argument, open-source interpretation
and bounded cost claim. A compact screen menu with direction-specific point
recovery is adequate for the declared one-witness task. It deliberately does
not preserve the full candidate geometry or every possible witness.

A separately frozen changed-row transfer is now an appropriate next test of
portability. Keep the same screening predicate, source order, contact kernel,
budgets, dispatch semantics and comparison rules, change only the declared
input through an explicit data adapter, and preserve any resulting scope stop
or uncovered direction. The present script contains fixed target bindings;
changing those bindings must be accounted for rather than described as an
already generic implementation. Predeclare the next input before its trial,
and label any informed input choice accurately. No new target is chosen or
run by this review. General mathematical statements remain internally reviewed
proof candidates, without a new existence, originality or frontier claim.
