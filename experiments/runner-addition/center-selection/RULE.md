# Complete rational-center selection from threshold events

October 17, 2026. Version 1. **HYPOTHESIS / proof candidate**, with a
self-contained derivation. Commit before selecting new comparison inputs.
AI-assisted internal reconstruction; external human/formal review remains open.
No novelty claim. Source: center-width RULE.md at
`dd972d3e7566a1adff1f480e7b934756c14b790f`.

## 1. Question, assumptions and fresh audit of H and G

Let S be a nonempty finite set of distinct positive integers, and let d=a/b
be rational in lowest terms, 0<d<1/2. All starts are at 0; time is in [0,1]
and reference speed is 0. A center c=u/v is rational, reduced, 0<c<1.

    H(c) = max_{1<=j<=v} (d-||jc||)_+ / j
    G(c) = min_{s in S} (||sc||-d) / s
    M(c) = G(c)-H(c).

The requested decision is whether some rational c has M(c)>=0. For the LRC
application n=|S|+2, d=1/n; added speed r is positive integer and r not in S.
General rational-threshold controls do not silently become n-runner claims.

Fresh derivation, starting from bands instead of the previous implementation:

* The unsafe sets for r are the open intervals ((m-d)/r,(m+d)/r).
  A closed connected I=[c-h,c+h] has no safe point exactly when it is
  strictly contained in one such gap: |rc-m|+rh<d. If this holds, m is a
  nearest integer since d<1/2. Conversely ||rc||+rh<d places I in that gap.
  Thus safe contact is exactly ||rc||+rh>=d, including equality. The score
  is a contact test, NOT an identity for the maximum circular distance when
  the phase interval crosses a triangular peak.
* For rational c=u/v, the deficit repeats modulo v. In each positive residue
  class, division by r makes its least positive representative the largest
  required half-width. Therefore H equals sup over ALL positive integers r
  of (d-||rc||)_+/r. The r=v term gives H>=d/v>0. A maximizing r blocks any
  h<H; at h=H it attains the safe equality boundary.
* The safe bands for s are [(k+d)/s,(k+1-d)/s]. If c is safe, its radius to
  the nearer edge of its containing band is (||sc||-d)/s. If c is unsafe,
  that expression is negative and no h>=0 works. Thus I is wholly safe for
  the core iff h<=G, and the combined condition is H<=h<=G. A valid core-safe
  interval cannot cross integer times, so containment in (0,1) follows.
* Requiring all positive r adds no obligation for r in S once core safety
  holds. A blocker for a core-safe interval is necessarily admissible. The
  time may vary with r; no fixed time is asserted to work for every r.

No defect was found in the original symbolic derivation under those
hypotheses. Rationality of d is an ADDITIONAL assumption for the selection
reduction below; the original supplied-center criterion allows real d.
Boundary strictness, nonempty S and common start are essential to this audit.
This is an independently structured internal argument, not independent authorship.

## 2. Why margin is maximized at component midpoints

For rational x,y, each function f_r(c)=(d-||rc||)_+/r is 1-Lipschitz:
distance to the integers is 1-Lipschitz and the positive-part map is too.
Using the supremum identity above, even when denominators change,

    |H(x)-H(y)| <= |x-y|.

Let C be the complete core-safe set, used for this proof only. It is a finite
union of closed intervals with rational endpoints. On a maximal positive
component [L,R],

    G(c)=min(c-L,R-c).

Indeed each core band containing this component has a left and right endpoint;
their maximum left endpoint is L and minimum right endpoint R. Writing
m=(L+R)/2 and w=(R-L)/2 gives G(c)=w-|c-m|. Consequently

    M(m)-M(c) = |c-m| + H(c)-H(m) >= 0.

This proves more than monotonicity under interval enlargement: the midpoint
dominates every rational center in its component for the actual margin M.
The maximum need not be unique. If M(c)>=0 anywhere, c is strictly core-safe
because H(c)>0, belongs to a positive component, and its rational midpoint
also satisfies M>=0. A singleton core component has G=0<H and cannot be a
universal source. Its possible role as an ordinary LRC witness is unaffected.

Thus checking all positive-component midpoints is a complete decision,
conditional on this proof. We still need to generate a superset without first
constructing C.

## 3. A finite candidate set from the input constraints alone

Generate the threshold events

    E = {0,1} union {(k+d)/s, (k+1-d)/s : s in S, 0<=k<s}.

Deduplicate equal rational values and order them e_0<...<e_q. Generate

    K = {(e_i+e_(i+1))/2 : 0<=i<q}.

Every maximal positive core-safe component has consecutive endpoints in E.
Its endpoints must be constraint boundaries. There cannot be another event
in its interior: at any threshold event for a positive speed and 0<d<1/2,
one adjacent open side is unsafe for that speed. That would contradict the
component's safety. This also shows that a candidate with G>0 has
G=(e_(i+1)-e_i)/2. No core-safe geometry is needed to generate K.

Therefore

    exists rational c in (0,1) with M(c)>=0
        iff exists c in K with G(c)>=H(c).

Let B=sum(S), V=max(S). At most 2B raw events plus two sentinels give at most
2B+1 candidate cells. Any midpoint of two boundaries has reduced denominator
at most 2*b*V^2, since a boundary has denominator dividing b*s and the
midpoint of boundaries from speeds s,t has denominator dividing 2*b*s*t.
Sentinels satisfy the same bound. A loose complete bound is thus
(2B+1)*2*b*V^2 H terms, plus (2B+1)*|S| core predicates and event processing.
These are finite input-dependent bounds, not a fixed bound for all cores,
and not a polynomial bound in the bit-length of binary-encoded speeds.

An even larger complete set is midpoints of every pair of input boundaries.
Adjacency removes unnecessary pairs. Testing the boundary points themselves
is inadequate: at every actual event, some core margin is zero, hence
G<=0<H. A raw-boundary-only search ALWAYS rejects, including successful cores.
This shortcut is analytically disproven once a successful control is supplied.
Unjustified denominator caps or selected single-runner phase peaks likewise
remain heuristic unless a separate completeness proof is supplied.

## 4. Streaming exact algorithm and decision statuses

Merge each speed's already sorted stream of 2s events with a min-heap,
retaining one pending event per speed, the previous distinct event and sentinels.
For each consecutive pair, evaluate its midpoint against ALL core constraints.
If G<=0 discard it. Otherwise calculate the established H exactly, with
optional early stopping when d/(j+1)<=the positive running maximum.

* If H<=G, return YES with c,H,G,M and interval [c-G,c+G]. Equality M=0 is YES.
* If H>G, retain the maximizing r and strict gap as a rejection certificate.
* Return NO only after exhausting every cell without a success or unresolved H.
* A resource cap before completeness returns UNKNOWN; a found positive witness
  may still prove YES. The implementation may stop immediately on a cap.

The production selector does not construct, merge or store C. It can terminate
on the first success and uses O(|S|) streaming event storage apart from output
and exact-number bit sizes. For complete rejection it may visit all boundaries
and classify all cells: it is still an interval-boundary method. Avoiding an
up-front full safe-set object is NOT avoiding all geometry or demonstrating
an efficiency advantage. An ordinary event-sweep baseline could share much of
this work. Recording a full diagnostic trace costs additional storage.

For a returned I=[A,B] and any admissible r, let

    k = ceil(r*A-(1-d)), t=max(A,(k+d)/r).

Contact guarantees t<=B; all core and added phases are checked at this SAME t.
The rule answers a connected-source existence question. It does not enumerate
all qualifying centers or maximize M over every point outside the safe set.

## 5. Independent full-geometry comparison to freeze separately

Use a separately written repeated intersection of the unions of closed safe
bands to construct complete C, preserving zero-width components. For each
positive component of length L, check direct contact with added-speed safe
bands for 1<=r<ceil(2d/L); r>=ceil(2d/L) follows from unsafe-gap length 2d/r<=L.
If a singleton is encountered, its reduced denominator blocks it. The baseline
must not call H, G, the streaming event generator or the new selector.

Compare existential decisions, first successful component in chronological
order, complete negative classifications and physical witnesses. For a
negative source, reconstruct its full blocker child to check whether witnesses
survive elsewhere. Do not turn a per-component blocker into a whole-core
blocker. Full comparison and trace verification occur AFTER primary selection.

Freeze new arithmetic input families, semantic equality/singleton/empty controls,
budgets and stop rules after this rule is committed and before running them.
Expose development controls separately. Preserve discrepancies rather than
repairing frozen sources silently. Charge streaming events, core predicates,
H terms, full band/intersection work, contact queries, verification and replay.

## 6. Representation and review limits

Question/output: complete existence decision for a rational center with M>=0,
one successful interval and per-r physical recovery, or exhaustive rejection.
Retained: S,d, positive integer domain, consecutive boundary identity, joint
core margins, rational H certificate, strict blockers, closed equality and
decision-completion status. Omitted: complete C as a prerequisite/object in
the primary algorithm; all qualifying centers, other references, optimum
loneliness, multiple simultaneously added constraints and minimum menus.
Recovery: pin input and code; build full C by closed-band intersections and
recheck the desired stronger question. The old center-width source is pinned
above; full comparison outputs will supply the richer validation record.
Failure test: any oracle disagreement, a qualifying noncandidate center whose
component midpoint fails, lost equality, or NO returned before exhaustion.

The transferable structure is a distance-to-boundary allowance minus a
1-Lipschitz demand: moving to an interval midpoint cannot lower the margin.
That abstract observation is not specific to runner speeds. Its application
still needs the stated allowance identity, rationality and candidate coverage.
This proof candidate establishes no universal successful center, general LRC
proof, novelty or runtime superiority. No external proof review is claimed.
