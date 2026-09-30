# Compatibility Calculus: the boundary-phase shortcut and its exact limit

September 29, 2026. Source c7a9886bc49e73968deafd11f9da123a5916ff88.

**Result:** the phase-identity rule is sound but does not preserve complete
coverage. On the new row (54,26), it retains five safe candidates and misses
exactly three positive primitive directions: **(1,2), (1,4), (5,1)**. Full
discovery on the same supplied source produces 61 candidates and a complete
five-segment certificate at 1/8. Both methods choose the same leading segment.
The lost information is fallback geometry, rather than a different leader.

This comparison covers all positive primitive directions through a proved
finite reduction, not just the physical controls. For original positive
parameters, the restricted class misses exactly the three rays q=2p, q=4p
and p=5q. All are in the ten-distinct-speed primary domain. No auxiliary
direction is lost. These are failures of the restricted candidate class,
not failures of loneliness.

**Status:** exact finite outputs are OBSERVED / REPRODUCED. The universal
coverage and exact-loss arguments remain HYPOTHESIS / internally reviewed
proof candidates. AI assistance includes implementation, derivation and
separate reviews; these are not blind, human, external or formal certification.
No general ten-runner, optimum, all-reference or originality claim is made.
The claim that this restriction preserves full candidate-class coverage is
DISPROVEN by the explicit lost witness; the sufficient safety implication
remains valid.

## Fixed question and informed input

The family is

\[
(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,54p+26q).
\]

All runners start together; the selected reference is stationary. Positive
integer p,q give ten distinct speeds iff p!=q and p!=2q. The last row strictly
dominates every earlier moving row. We seek one shared safe time at the fixed
closed threshold 1/8, which implies the ten-runner target 1/10 when successful.
No threshold change or 1/10 geometry was part of this comparison.

The new row is the next k=3 in (6,2)+8k(2,1), after the previous trial's
k=2 row (38,18). This is an informed arithmetic transfer, not a blind or
randomly held-out test. The input consists of all 36 pinned nine-runner safe
segments, already clipped for (6,2),(3,8), not only its chosen menu. Their
earlier discovery is supplied work, not a cost newly eliminated here.

The [protocol](../reviews/2026-09-29-cc-phase-screen/PROTOCOL.md) was frozen
before target screening or clipping, SHA256
`0cc8219fadcfb0f3ac5091a613692355b1c7e4ceb9a51b3b2eeba7fcf8875300`.
Eight source hashes matched the live tree. A sequential clipping regression
for the earlier row (38,18) reproduces its entire archived coverage certificate,
including the original parent-edge parameters. Old physical controls were
not rerun as part of that regression.

## The sufficient rule and the distinction it carries

Let u be the new row, v an already safe row and c a core row. If

\[
u-v=8kc,\qquad c\cdot(x,y)=m_c+\epsilon,
\qquad \epsilon\in\{1/8,7/8\},
\]

throughout a source segment, then the raw difference is an integer:
8km_c+k on the lower boundary or 8km_c+7k on the upper boundary. Set the new
lap to the old v lap plus that integer. The new and old fractional phases
are equal at every point of the segment. This is a sufficient whole-segment
certificate; failure to find such a relation does not prove unsafety.

The implementation checks all 48 existing-row/core-row pairs. It finds only

\[
(54,26)-(6,2)=24(2,1).
\]

It then checks the constant boundary predicate on all 36 source records.
Five pass, including one point record. The other 31 are labelled
NO_SCREEN_CERTIFICATE, rather than unsafe. All five retained candidates
appear identically in the full output, including labels and original edge
parameters. Different raw values and lap counts are preserved even when
fractional phases coincide.

The full branch instead clips every source segment against all possible
new-row lap bands. It admits partial segments and retains alternatives the
whole-segment rule cannot certify. Both branches use the same imported
coverage algorithm, numeric provenance ordering, first-leader rule,
400-pair rectangle budget and maximum-gain greedy fallback. No reranking,
changed screen or repaired restricted run followed the result.

## Exact costs and outcomes

| Quantity | Phase screen | Full append clipping |
| --- | ---: | ---: |
| Supplied source records | 36 | 36 |
| Coefficient-pair tests | 48 | not used |
| Relation/source boundary checks | 36 | not used |
| New-row lap attempts | 0 | 61 |
| Emitted candidate records | 5 | 61 |
| Point records, with provenance | 1 | 5 |
| Descending candidates | 4 | 33 |
| Leader rectangle | 136 | 136 |
| Residual primitive directions | 47 | 47 |
| Candidate/contact entries | 235 | 2,867 |
| Greedy menu entries | 3 | 5 |
| Uncovered primary primitive directions | 3 | 0 |

The screen reduces the number of records and contact checks, but it adds
coefficient and boundary checks. These operations are different; the counts
do not establish a runtime or total-work improvement. The full branch's 61
lap attempts are within its frozen 256 cap. Neither compiler hits its budget.

## Why the coverage comparison is global

Both branches choose P2:E0-3:K2:L2:M23, whose segment is

\[
y=7/8-2x,\qquad 33/104\le x\le3/8.
\]

For primitive positive P=p/gcd(p,q), Q=q/gcd(p,q), its integer-orbit
projection H=Qx-Py has interval

\[
[(33Q-25P)/104,(3Q-P)/8],
\qquad\text{width}=3(Q+2P)/52.
\]

Thus every Q+2P>=18 is covered by both leaders. The complete remaining domain
has 47 coprime pairs with Q+2P<=17 inside the declared rectangle. In general
the two residual domains would be united; here they coincide. Comparing
ALL candidates over this union exhausts all possible coverage differences.
The result is exactly the three lost primary directions stated above.

The three restricted menu entries are:

1. P2:E0-3:K2:L2:M23;
2. P2:E0-3:K2:L3:M23;
3. P3:E0-1:K3:L2:M30.

The first fallback gains six of the leader's eleven misses; the second gains
two, leaving (1,2),(1,4),(5,1). Every restricted candidate misses those three,
so this is not merely an unfortunate greedy selection.

The full menu is:

1. P2:E0-3:K2:L2:M23;
2. P2:E0-3:K2:L3:M23;
3. P0:E1-3:K1:L2:M13;
4. P1:E0-1:K1:L4:M19;
5. P1:E0-3:K1:L3:M16.

Its fallback gains are 6,2,2,1 and leave no uncovered labelled direction.
The larger menu is not claimed minimal. Fixed labels and endpoint safety
give whole-segment safety; integer orbit contacts and the retained gcd/Bezout
map recover one shared physical time for all nine moving rows.

## A concrete lost witness

The frozen diagnostic chooses the first lost primary direction, (P,Q)=(1,2).
The first full candidate contact in provenance order is
P0:E0-1:K1:L2:M13 at (x,y)=(1/8,1/4), H=0, giving t=1/8. Its ten speeds are

\[
(0,1,2,3,4,5,7,10,19,106),
\]

and its nine phases are

\[
(1,2,3,4,5,7,2,3,2)/8.
\]

The minimum is 1/8. The new runner's phase is 1/4. The omitted source is
P0:E0-1:K1:L2, on which the core raw value 2x+y varies from 15/32 to 1/2.
It is neither constant nor the required boundary value. Therefore the
sufficient screen cannot certify that entire source.

At the actual contact, however, 2x+y=1/2 and the raw difference is
24(2x+y)=12, so equal phases hold there. A relation valid at a needed contact
can survive even when the whole-segment predicate fails. This pinpoints the
extra obligation imposed by the shortcut. The diagnostic witness is distinct
in provenance from the full greedy menu's witness at the same physical point;
that menu uses P0:E1-3:K1:L2:M13. Both records remain preserved.

No witness was fed back into the restricted compiler. The full-parent
diagnostic was NOT_TRIGGERED because the full edge class already supplied
a complete certificate. This is recovery from the immediate richer source,
not an executed parent-interior search.

## Controls, review and reproduction

The restricted branch supplies 20 witnesses among the 22 fixed controls and
misses (1,2),(1,4); its third lost primitive direction (5,1) occurs in the
complete residual comparison, not in that control list. The full branch
passes all 22. All emitted witness minima are 1/8. Primary and auxiliary
counts, gcd scaling, phases, both lap systems, reflection and open endpoints
are checked separately in the review package.

Opening the restricted menu or all restricted candidates loses three further
closed-hit controls: (1,3),(2,3),(4,6), representing two primitive directions.
Opening the full chosen menu loses (1,2),(1,3),(1,4),(3,1); opening all full
candidates loses none of the 22. These are different representations and
finite control statements, not full physical safe-set conclusions.

Independent geometry reconstruction matches 25,843 target scalar fields,
plus 17,890 fields in the earlier-row regression. Physical review independently
checks all 3,102 candidate contacts in the comparison union, both control
sets, the subset mapping and the recovered lost witness. The proof review
passes. All ten exact output files reproduce byte-for-byte against eight
pinned inputs. Review/reproduction completed September 30 UTC (September 29
in the maintainer's local timezone); the protocol and package retain their
September 29 freeze date.

The package contains independent geometry and physical reconstruction, a
separate proof review, exact reproduction, an execution record and a manifest.
From the repository root:

```sh
python3 reviews/2026-09-29-cc-phase-screen/reproduce.py
```

## CC checkpoint and next limit

The boundary-phase record is adequate to prove the new row safe on each
accepted whole segment. It is inadequate as a complete discovery rule: it
omits safe partial segments and individual contacts needed on three rays.
Its failure is clean and recoverable because omitted records, exact reasons,
all shared labels and the full candidate source remain available.

No replacement of CC is required by this result. The model must distinguish
a sufficient local certificate, uniform family coverage and completeness
of discovery. The inherited segment/physical-lap frameworks remain useful
and credited in the pinned literature comparison. This informed transfer
does not establish general portability, necessity of the screen or novelty.

**Next proposed:** test a hybrid compiler that first uses the phase screen
for its infinite tail and covered finite directions, then consults the full
source only for its uncovered primitive directions. Here that would mean
recovering three directions. Freeze the recovery rule and costs before
testing; do not assume it is cheaper or inherits completeness automatically.
No hybrid implementation, enlarged screen or further target trial was run.
