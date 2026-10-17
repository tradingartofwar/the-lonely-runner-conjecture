# Removing the required leader: exact decision and scope

October 17, 2026. Same-author proof candidates; independent review remains
required. Adapted from the repository's existing placement and width arguments.

Let S be one of the six specified eight-speed cores, d=1/10, and C its complete
safe set in [0,1] for stationary reference 0. Write its maximal connected closed
components as I_i=[a_i,b_i], allowing a_i=b_i. An admissible added speed is a
positive integer r not in S. A component works for r when some t in it has
distance(rt,integers)>=d. Times may differ between different r.

For a positive-width I=[a,b], let c=(a+b)/2, h=(b-a)/2. The previously derived
criterion is

    I is blocked by r iff distance(r*c,integers)+r*h < d.

Equality is safe. In the blocked case the entire closed interval lies strictly
inside one open unsafe gap ((m-d)/r,(m+d)/r). The exact integer certificate is

    r*b-d < m < r*a+d.

All bad gaps on the time line have width 2d/r. Consequently, with
R_i=ceil(2d/(b_i-a_i)), every r>=R_i has a safe contact in I_i, including
equality. Checking all admissible 1<=r<R_i therefore suffices for this
component alone. The widest component's cutoff cannot be substituted here.

For a singleton t=u/v in lowest terms, r=v gives phase zero. Since this point
is core-safe with d>0, v cannot already be in S: otherwise that core speed
would have phase zero. Thus v is an admissible exact blocker. This singleton
decision is analytic; the positive-width search cap does not apply to it.

Apply the unchanged placement classifier to every component. A found blocker
rejects that component alone. No blocker below an incomplete search cap yields
UNKNOWN, not a covering interval. Exhausting a component's own finite domain
without a blocker, together with the tail, gives a universal single-component
candidate. This study disables the classifier's optional rational-anchor
search (max_denominator=0); an absent anchor field means unsearched, not that
no rational explanation exists.

If any component is universal, the minimum number of fixed connected core-safe
source components is one. If every complete component has an admissible blocker,
no connected core-safe subinterval can be universal either: it is contained in
one maximal component and inherits its blocker. The pinned prior two-component
certificate supplies an upper bound, so the unrestricted minimum is two.
If some components remain UNKNOWN and none is certified universal, keep [1,2].

This minimum belongs to a particular representation class. A disconnected
union can be named as one set, and an algorithm may choose a time directly
from r; neither is ruled out by a two-component lower bound. The obstruction
quantifiers are: for every fixed component there exists a blocker. They are
not: there exists one r blocking the entire complete core. Full child sets
and physical witnesses at the recorded blockers keep that distinction visible.

Retain all source endpoints, equality cases, local IDs and thresholds. Recover
the pinned complete geometry for complete-set, changed-core, different-reference
or optimum-distance questions. No intrinsic incompressibility, all-reference,
novelty or general LRC implication follows.
