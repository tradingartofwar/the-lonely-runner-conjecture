# Final mathematical challenge of the overlap bound and robust lift

September 28, 2026. Internal AI audit by `chain_bound`, requested after the
initial derivation. No further computations or scans were performed. This
checks the arguments, not external proof certification or novelty.

## Bound: challenged points and verdict

**Selected-union versus full multiplicity.** On the union U of selected
blocking intervals, selected multiplicity is at least one almost everywhere.
Full multiplicity is at least selected multiplicity, so integrating
`M_full-1 >= M_selected-1` on U is legitimate. Outside U is not included.
Because every next moving interval contains the preceding right endpoint
strictly, U is a single open interval. Integrating on its closure changes no
measure. The primitive identity therefore supplies exactly the needed bound,
without an assumption that other blocking intervals are absent.

**A new interval can extend the union to the left.** This does not damage the
global proof. The identity for adjoining a set gives the increment of excess
as the measure of its intersection with the previous union. That intersection
contains its positive intersection with the immediately preceding selected
interval, hence has measure at least eta. Monotonicity of selected left
endpoints was never required; only the right endpoints strictly increase.

**Phase bound when a selected left endpoint equals L.** An occurrence beginning
at L does not contain L, since blocking is open. It is correctly counted among
the intervals that must consume eta inside `[L,t_N]`. When selected, its right
endpoint exceeds the preceding right endpoint, and the latter lies strictly
inside this new occurrence. Their full positive intersection starts at or
after L and is included in the clipped previous union. Its length is at least
eta. The same reasoning covers every selected occurrence starting after L.
All other selected occurrences have left endpoint below L and right endpoint
above L, so contain L and number at most M(L). No occurrence can be selected
twice. Thus `(N-M(L))*eta <= H(t_N)-H(L)` is valid, including equality at the
starting threshold. If L is already safe for all four, return L immediately.

**Pairwise quantum.** If a positive overlap is not a full contained interval,
its length is a difference of endpoints with denominators `8*v_i` and
`8*v_j`. It is a positive multiple of `1/(8*lcm(v_i,v_j))`, hence at least
`1/(8Q)`. A whole contained blocked interval has length `1/(4*v_i)`, which is
also larger than this quantum because Q is at least every speed. Q need not
be a common multiple of all four speeds; its role is a maximum of pairwise
lcm values, and only pairwise lower bounds are used.

**K rounds versus K moves.** Every complete eleven-call round that starts
unsafe has at least one moving call: otherwise each of the four runners was
tested at the unchanged input time and all were safe, a contradiction. If the
algorithm were still unsafe after K such rounds, another round would force
at least K+1 moves. This contradicts the bound on every finite moving prefix.
Consequently K rounds suffice. This counts up to 11K scalar calls, not K
calls; it does not bound bit cost. Testing for safety after each round is
required. With an unbounded-delay fair order, only the moving-call count is
bounded, not the total stationary calls.

**Endpoint and window conclusions.** A pair of open blocks merely touching
does not continue a connected cover. An iterate at the right window endpoint
must still pass all safety checks; equality in time alone is insufficient.
Any iterate strictly beyond that endpoint excludes an earlier joint witness
by projection preservation, even if the iterate is not itself feasible.
Global residual termination does not keep the core safe outside its supplied
window and cannot establish a full-configuration lonely moment there.

No defect was found in these challenged steps. The argument remains a proof
candidate under repository governance.

## Audit of structural.md: explicit robust common-start lift

The stated constants and restrictions are sufficient for its finite strict
endpoint-certificate scope:

- `M=72*D_alpha` and `P=24*D_alpha+1` satisfy `gcd(P,M)=1`: a common divisor
  divides 3, while P is 1 modulo 3.
- Since N is a multiple of `M*D_v`, each `N*v_i` is an integer multiple of M.
  The selected residues therefore give `{U_i*tau}=alpha_i` exactly, rather
  than approximately.
- `N>M/Delta` preserves strict speed order because a residue difference has
  absolute value strictly below M. `N>5/v_min` makes all residual speeds
  larger than the fixed core's largest speed 5.
- In the local coordinate, `w_i=v_i+r_i/N>=v_i`, so
  `|e'-e|=|e|*r_i/(N*w_i)<T*M/(N*v_min)<mu/4`.
  Two distinct endpoints separated by at least mu remain separated by more
  than mu/2. Same-endpoint identities, including a runner's own projected
  safe boundary, remain identities.
- Since `|e'|<=|e|<=T`, the endpoint perturbation does not enlarge the selected
  local time range. For `M>=72`, the anchor
  `tau=1/3+1/M` is at distance at least `1/36` from both endpoints of
  `J=[9/32,3/8]`. Thus `N>36*T` puts all selected physical endpoints strictly
  inside J, where the core runners 1,4,5 are strictly safe.

The equality exclusions are necessary. Two equal coordinates belonging to
different runners need not remain equal after the independent speed residue
perturbations. The lift preserves a finite certificate expressed entirely by
strict cross-runner endpoint comparisons, together with genuine identities
of the same labelled endpoint. An isolated equality witness is outside this
robust statement. A projection itinerary also requires that every comparison
that determines it actually appears in the finite certificate; preserving a
subset of cover inequalities alone would not certify the entire trace.

The proof assumes the local certificate's anchors/boundaries are among its
selected endpoints. If a future construction introduces an additional fixed
local point, its strict distances from the selected endpoints must also be
included in the margin data; the present endpoint-only wording should not be
extended silently. The current statement and archived construction use
endpoint certificates, so this is a scope reminder rather than a defect.

No defect was found in the explicit lift within its stated scope. It transfers
a finite robust construction if supplied; it does not construct an arbitrarily
long chain or establish that one exists.

## Prior primitive and remaining question

The coordinator located the same periodic primitive and `3/16` oscillation in
`notes/OVERLAP_PLACEMENT.md`, Section 8. The bound review now credits that prior
work. The additional deduction concerns chain excess, the arithmetic overlap
quantum, and projection termination. A speed-independent iteration bound and
a family with unbounded iteration counts both remain unresolved here.
