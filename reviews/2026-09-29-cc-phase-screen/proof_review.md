# Separate proof review: sufficient phase screening loses coverage

September 29, 2026. This is a separately tasked internal AI proof review,
not blind replication, external human review or formal certification. I
reviewed the proposed rule and finite-comparison argument before target
enumeration, then inspected the frozen protocol and reached outputs. No
additional target trial or production-code import was used for this review.

Protocol SHA256, verified from disk:
`0cc8219fadcfb0f3ac5091a613692355b1c7e4ceb9a51b3b2eeba7fcf8875300`.
The pinned input head is `c7a9886bc49e73968deafd11f9da123a5916ff88`.
The declared target is u=(54,26), at fixed threshold1/8. The input choice
was informed by the preceding coefficient identity; it is not a blind test.

## 1. The screen is sound, but its converse was never established

Let v be an existing safe row and c a core row, with u-v=8k*c for a nonzero
integer k. On a source segment where c dot(x,y) is constantly m_c+epsilon,
epsilon equal to1/8 or7/8, define

    m_u=m_v+8k*m_c+k          if epsilon=1/8,
    m_u=m_v+8k*m_c+7k         if epsilon=7/8.

Then u dot(x,y)-m_u=v dot(x,y)-m_v throughout that segment. This proves
same-point safety and supplies the exact new integer lap. Endpoint equality
of an affine raw value proves constancy on the whole segment, including a
singleton. If several reasons apply, they must derive the same m_u: each
places the same raw value in the open unit interval(m_u,m_u+1), because the
retained safe phases lie in[1/8,7/8]. A different integer lap cannot do so.

These implications justify accepting each retained segment whole. They do
not justify rejecting a source as unsafe when the screen fails. A variable
core value, a different rational phase, or a nonidentical but safe ninth
phase can all occur on valid contacts omitted by this sufficient rule.

The48 frozen coefficient checks retain one relation:

    (54,26)-(6,2)=24*(2,1),  k=3.

The36 source/relation checks retain five records: four nondegenerate segments
and one point with duplicate geometric membership in a retained segment.
On 2x+y=7/8 the raw shift is21 and the retained lap becomes23; on
2x+y=9/8 the raw shift is27 and the retained lap becomes30. These raw/lap
differences are retained even though the corresponding fractional phases agree.

## 2. Source completeness, clipping and the subset relation

The pinned36 source records already represent every simultaneous safe
intersection of the first two added rows with the original24 floor edges.
Appending u by clipping every source against each possible ninth lap is
therefore equivalent, on that edge class, to imposing all three added bands
simultaneously. It is not a complete representation of parent interiors or
new edges created away from the original floor edges.

For a source's affine raw-value range[min,max], the possible new laps are
exactly within ceil(min-7/8) through floor(max-1/8). Intersecting the closed
band with the source's local parameter interval gives every allowed subsegment.
The source-local parameter must then be mapped back to the original edge by
s_original=s0+s_local*(s1-s0). The frozen regression checks this changed
input route against the entire previous simultaneous-clipping certificate.

Every screened source is already safe for u everywhere under its derived
label, so that exact whole source must occur in the full clipped branch with
the same new label. The recorded subset checks confirm all five identities,
including endpoints and original parameters. Thus any contact supplied by a
screened candidate is also a contact in the full class. Losing a screened
candidate during that mapping would be a correctness error, not screening
loss; no such error is reported.

## 3. Why the coverage comparison is global

For a descending segment with positive widths alpha=x1-x0 and beta=y0-y1,
the orbit projection H=Qx-Py has width alpha*Q+beta*P. Width at least1
guarantees a closed integer contact. Every miss therefore lies inside
P<=ceil(1/beta)-1, Q<=ceil(1/alpha)-1, with alpha*Q+beta*P<1.
This is the proved finite residual domain underlying the compiler.

Both branches reached full contact matrices and selected the same leader:

    y=7/8-2x, 33/104<=x<=3/8,
    I(P,Q)=[(33Q-25P)/104,(3Q-P)/8],
    width=3*(Q+2P)/52.

Thus every positive primitive pair with Q+2P>=18 is covered in both classes.
The entire possible difference lies among the47 primitive pairs with
Q+2P<=17, inside the136-pair rectangle P<=8,Q<=17. In general the union
of both reached residual domains would suffice; here those domains coincide.
The comparison checks all candidates, not just the greedy menus.

The complete comparison finds precisely three screened-class misses:

    (P,Q)=(1,2),(1,4),(5,1).

The full class hits all three, and both classes hit every other positive
primitive direction. No auxiliary direction is lost. This is an exhaustive
candidate-class comparison, not merely a pattern in22 physical controls.
Its physical parameter interpretation includes all positive integer multiples
of the three displayed directions. It is not a nonexistence claim about
physical witnesses for those parameters.

The restricted raw status is `UNCOVERED_PRIMITIVE_PAIRS`, and every miss is
primary, so `NO_PRIMARY_GUARANTEE` is correct. The full branch is
`COMPLETE_COVER_CERTIFICATE`, hence also `PRIMARY_COMPLETE`. The valid
general alternative of deducing primary completeness from auxiliary-only
misses does not apply to this restricted result.

## 4. Full construction and exact witness lost by the screen

The full menu uses the leader above and then:

| Order | Geometry | Ninth torus lap |
| --- | --- | --- |
| First fallback | y=7/8-2x, 1/4<=x<=31/104 | 23 |
| Second fallback | y=7/16-3x/2, 1/8<=x<=11/72 | 13 |
| Third fallback | x=1/8, 99/208<=y<=1/2 | 19 |
| Fourth fallback | y=9/16-3x/2, 1/8<=x<=3/20 | 16 |

The first eight rows are safe by the pinned source records. The ninth phases
on the leader and these four fallbacks are, respectively,

    2x-1/4; 2x-1/4; 15x-13/8; 26y-49/4; 15x-11/8.

Each lies in[1/8,7/8] at both endpoints, hence throughout its segment.
The first fallback covers six leader misses; the remaining fallbacks cover
two, two and one. Together they cover all11 leader misses in the complete
47-pair residual table. Each segment also retains a constant core phase
equal to1/8 or7/8, so the constructed minimum is exactly1/8. This is not
an optimality or minimum-menu claim.

The first lost primary direction is(1,2). The full candidate in provenance
order is P0:E0-1:K1:L2:M13, with x=1/8 and 51/208<=y<=1/4.
Its projected interval is[0,1/208], so the first integer H=0 selects

    (x,y)=(1/8,1/4),  t=1/8.

The moving speeds are1,2,3,4,5,7,10,19,106, and their phases are

    1/8,1/4,3/8,1/2,5/8,7/8,1/4,3/8,1/4.

The minimum is1/8, all ten total speeds are distinct, and the ninth physical
lap is13. The source P0:E0-1:K1:L2 was omitted because its core raw value
2x+y ranges from15/32 to1/2: it is not constant on either declared boundary.
Its failed screen result is therefore correctly `NO_SCREEN_CERTIFICATE`.

At the recovered point itself, 2x+y=1/2 and u-v=24*(2,1) gives an integer
raw difference12. Phase equality does hold there. The lost distinction is
between an identity certified along an entire specially chosen boundary and
an identity or ordinary safety at an actual compatible contact. The latter
was not expressible by this frozen whole-segment screen. This observation
does not retroactively broaden or rerun the rule.

## 5. Physical interpretation and scope

The new row dominates every previous moving row. Thus ten distinct total
speeds require exactly p!=q and p!=2q; the two auxiliary primitive directions
have nine distinct speeds. These restrictions are preserved explicitly.

For an integer contact h=Qx-Py and Bezout coefficients rP+sQ=1, put
N=floor(rx+sy), tau=rx+sy-N and t=tau/d, where d=gcd(p,q). A row(a,b)
with retained torus lap m has physical lap

    m+(-a*s+b*r)*h-(a*P+b*Q)*N.

This identity makes all nine phases occur at one physical time. Positive
safe coordinate phases give0<t<1/d. Reflected time1-t and alternative
Bezout recovery preserve the same safety claim. The full width-plus-residual
certificate therefore supplies the selected-reference1/8 witness for every
positive p,q in this fixed family, including labelled auxiliaries; on the
ten-distinct-speed domain it also implies1/10 safety.

Only the screen's claim to preserve full candidate coverage fails. Its
sufficient safety proof remains valid, and the full candidate class succeeds.
No full-parent diagnostic is triggered. Threshold1/10 was excluded by design,
not omitted after observing failure; no claim is made to have executed it.
No statement about arbitrary ten-runner families, every reference, optimum
or the complete physical safe set follows.

## 6. Costs, next operation and finding

The screen performs48 coefficient-pair tests and36 boundary checks, producing
five candidates and235 candidate/residual contacts. The full branch performs
61 source/lap attempts, producing61 candidates and2,867 contacts. Both use
the same47 residual pairs and136-pair rectangle; their greedy menus contain
three and five records respectively. The earlier generation of the36 source
records is supplied preprocessing. These counts measure different operations
and do not by themselves establish runtime or total computational savings.

The result supports treating the phase screen as a sufficient first stage
with explicitly recoverable exceptions. A proposed hybrid could retain its
infinite-tail certificate and consult richer candidates only on the three
remaining directions. That is a next study, not an implemented result here.
It needs its own frozen rule, exact coverage comparison and cost accounting;
the full61-candidate result used in this comparison cannot be treated as
unpaid work already available to a future discovery algorithm.

PASS for screen soundness, exact lap translation, subset mapping, finite
comparison proof, lost-witness interpretation and physical recovery. The
screen is demonstrably incomplete for preserving this full edge class's
coverage. The complete wider construction remains an internally reviewed
proof candidate. No new literature/frontier or originality conclusion was
drawn, and no rule expansion, alternate leader or repaired rerun occurred.
