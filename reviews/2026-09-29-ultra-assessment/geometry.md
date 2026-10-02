# Geometry review: what the whole safe set adds, and what it cannot force

Date: 2026-09-29. Assigned review of the supplied snapshot at pinned head
`7b0101376e00dbb71537d3a62e39ec75cee113cc`.

**Status:** retained general arguments and the cluster extension below are
HYPOTHESIS / proof candidates under repository policy. Archived finite
facts retain their OBSERVED status. No mathematical program was executed.
This review used static reading, hand derivation, and a targeted primary
source reading. AI internal review is not external certification.

## Assessment

The best retained geometry is already quite complete **conditional on
having a useful core-safe set**. The TWO_TIME note characterizes
one-runner all-phase robustness by a pair for threshold 1/8. The latest
last-runner note preserves exact containment, isolated witnesses, and
reflection. Another representation of the same phase image will not
itself supply the missing arithmetic guarantee.

There are two concrete conclusions for the next research question:

1. A universal route through positive core windows alone is already
   disproved by the inherited tight13 control, even if arbitrarily many
   such windows are allowed.
2. The two-window *uniform speed-tail* criterion admits a useful cluster
   extension: a wide window bounds the possible blocker period, and a
   chain of sufficiently short intervening gaps propagates one shared
   lap label across a much longer hull. This is an elementary extension,
   not a new circle-geometry principle or a general existence proof.

The requested advance must therefore be a quantified **certificate
existence** statement, with an equality branch. It cannot be another
conditional completeness statement.

## 1. An exact no-go inside the active physical family

Use the archived core

\[
C=\{1,4,5,6,7,11\},\qquad d=13,\qquad\delta=1/8.
\]

Its four positive closed safe components are

\[
[17/56,5/16],\quad[41/88,15/32],\quad
[17/32,47/88],\quad[11/16,39/56].
\]

The archived last-runner calculation, also checked analytically in its
arithmetic review, says that speed13 at phase zero strictly blocks all
four entire components. The full safe set nevertheless consists of
the four isolated points

\[
1/8,\quad3/8,\quad5/8,\quad7/8.
\]

Consequently **no collection of positive core windows can certify a
surviving point for this input**: every such window is contained in the
four strictly blocked components. This refutes a universal
positive-window-only strategy, not only the particular sufficient
inequalities of the latest note. Allowing more positive windows cannot
repair it. The isolated-point branch is logically indispensable.

For this input all-phase robustness still holds: the isolated times
1/8 and7/8 are both core-safe, and their speed13 phases are5/8 and3/8,
separated by1/4. Thus the full-set two-time certificate succeeds exactly
where every positive-window-only certificate fails.

This does **not** disprove the proposed all-phase extension for every
admissible positive eight-runner configuration. No counterexample to that
particular stronger statement was derived here. The safe-set geometry
only makes its additional quantifier explicit.

## 2. Why larger witness collections do not remove the all-phase burden

Let n>=6, delta=1/n, and let S be a nonempty compact core-safe set. For a
selected speed d, let A=dS mod1. As already proved in TWO_TIME, with
2delta<=1/3,

\[
\begin{split}
&\text{for every phase }\theta\text{ some }t\in S
  \text{ satisfies }\|dt+\theta\|\ge\delta\\
&\qquad\Longleftrightarrow
\exists s,t\in S:\ \|d(s-t)\|\ge2\delta.
\end{split}
\]

The forward direction is the compact circular-arc diameter lemma; the
reverse is the circle triangle inequality. Thus, at these thresholds,
adding a bounded larger collection cannot create a weaker geometric
all-phase objective. If any collection protects against every phase,
some pair inside its phase image already suffices. A larger collection
may still make an arithmetic **selection argument** or a simultaneous
speed-range argument easier. That is where its value must be measured.

For an integer common-start core and integer d, the reflected full-period
phase image is symmetric. The archived reflection argument says that
all-phase feasibility is equivalent to feasibility at phases0 and1/2.
Common-start Lonely Runner asks only for phase0. Proving phase1/2 as well
is an extra requirement; geometry does not establish it automatically.
The positive-duration version must exclude isolated core points, exactly
as the last-runner note does.

These are retained results, not new claims of this review.

## 3. A window-cluster extension with arbitrary n

Here is a precise proposed extension of the current two-window
speed-tail certificate. It applies to supplied core-safe windows, not
necessarily complete maximal components.

**Cluster lemma.** Fix n>=3, delta=1/n, and finitely many ordered disjoint
positive closed core-safe intervals

\[
I_j=[l_j,r_j],\qquad r_j<l_{j+1}\quad(1\le j<q).
\]

Put

\[
w=\max_j(r_j-l_j),\quad D=r_q-l_1,\quad
G_j=l_{j+1}-r_j,\quad \alpha=2/n.
\]

If

\[
G_j\le\frac{1-\alpha}{\alpha}w=\frac{n-2}{2}w
\quad\text{for all }j,
\]

then every real final speed d>=alpha/D leaves a safe point in the union
at every final phase. If all displayed gap inequalities are strict and
d>alpha/D, it leaves positive safe duration.

**Proof of existence.** Suppose the final runner strictly blocks all
windows. Each connected window fits into one open blocking lap. Such a
lap has width alpha/d, while two consecutive laps have an intervening
safe gap of width (1-alpha)/d. The widest window forces dw<alpha.
Consequently

\[
dG_j\le\frac{1-\alpha}{\alpha}dw<1-\alpha.
\]

Two neighboring windows therefore cannot occupy different blocking
laps: their intervening time gap would have to exceed
(1-alpha)/d. All windows must occupy the same lap, which requires
dD<alpha, contradicting d>=alpha/D.

**Proof of positive duration.** If final safe duration on the windows
is zero, each positive closed window lies in a closed blocker. Otherwise
a point of strict final safety has a one-sided or two-sided safe
neighborhood inside the window. Closed containment gives dw<=alpha.
The strict gap assumptions still give dG_j<1-alpha, forcing one common
closed lap and dD<=alpha, contrary to d>alpha/D.

For q=1 the gap assumptions are vacuous and this is the width bound.
For q=2 it is the existing two-window lemma. The extension propagates
the same lap constraint through a cluster; it has no new dependence on
integrality and no claim that arbitrary runner cores supply a cluster.

### It can improve the uniform tail without a successful old pair test

Consider the following **abstract interval fixture**, not an asserted
realization as a runner core:

\[
I_1=[1/16,3/16],\quad
I_2=[7/16,15/32],\quad
I_3=[23/32,3/4].
\]

At n=8, w=1/8, both gaps are1/4<3w, and D=11/16.
The cluster lemma gives positive duration for every d>4/11, at every
phase. The old two-window criterion applied to I1,I2 starts only at
d>=8/13. The pairs I1,I3 and I2,I3 fail its gap/width condition:
their gaps are17/32>3/8 and1/4>3/32 respectively. Thus, for example,
the cluster uniformly covers the range4/11<d<8/13 that none of those
three pair formulas covers.

At each fixed d in that range the old two-time *existence* theorem
still guarantees a suitable pair of points. There is no contradiction:
the gain is in a simple certificate valid for an entire speed tail,
not in the minimum size of a fixed-d phase witness.

The tight13 no-go remains untouched. Its positive components are
actually blocked, so they cannot satisfy this lemma at d13.

## 4. The equality route is already arithmetic, and already in the record

For common-start positive integer absolute relative speeds and n>=3,
an isolated safe time must have an entering and an exiting equality
controller. Otherwise a small movement in at least one direction keeps
every constraint safe. For one orientation the two controllers a,b
satisfy

\[
at\equiv1/n,\qquad bt\equiv-1/n\pmod1.
\]

Write g=gcd(a,b), A=a/g, B=b/g. Such opposed contacts exist exactly when

\[
n\mid A+B=\frac{a+b}{\gcd(a,b)}.
\]

Indeed, writing at=m+1/n and bt=k-1/n gives
n(Bm-Ak)=-(A+B), proving necessity. Conversely, when n divides A+B,
gcd(A,n)=1. If r is the inverse of A modulo n, all contacts of this
orientation in [0,1) are exactly

\[
t=\frac{r+n\ell}{ng},\qquad \ell=0,\ldots,g-1.
\]

The reverse orientation uses -r modulo n. For n>=3 these are disjoint,
so there are exactly2g pair-contact candidates before the other runner
constraints are checked. This candidate count is unbounded as pair gcds
grow; it is not a constant-time global selector. Merely requiring
n|(a+b) is weaker and insufficient: n8, a4,b12 has reduced sum4.

For tight13, (1,7) supplies1/8 and7/8; (5,11) supplies3/8 and5/8.
Every remaining speed must still be checked at each point.

**Prior-art correction during this review:** this precise gcd condition
and conditional complete contact selector were found in HANDOFF's
September27 Ultra summary. They must not be presented as a new advance.
The exact grid above was independently reconstructed here and separately
checked by the arithmetic reviewer. HANDOFF also warns that matching
all opposed-contact times and controller labels does not determine
which candidates survive the other runners.

The literature precedent is also explicit: Kravitz,
*Barely lonely runners and very lonely runners* (2021), Proposition2.1
and adjacent discussion on printed pages4–5, describe local maxima at
pair-sum denominators and grouping candidate times by controller pairs.
Those pages were inspected in the [published PDF](https://escholarship.org/content/qt3wx931fh/qt3wx931fh.pdf)
for this review. No full-paper or novelty audit was performed.

## 5. A falsifiable next target

The correct original-phase target has the following form:

> For every admissible common-start integer core C in the intended
> family and every admissible final integer d, either a supplied
> core window or cluster forces a final-safe point at phase0, or an
> eligible opposed-contact grid contains a point satisfying every
> runner constraint.

That statement is not established. With unrestricted certificate
selection it is another formulation of the desired existence result;
it becomes useful only after specifying arithmetic hypotheses or a
selector which force one branch. In particular, “otherwise check
all contact points” does not prove the equality branch succeeds.

**Smallest next test, requiring a separately approved diagnostic if
executed:** on the already frozen27 six-core decompositions, retain each
maximal component and isolated point unchanged. For each positive
component chosen as a largest-width anchor, merge neighboring components
while every intervening gap is at most3 times that anchor width. Record
only the resulting hull D and the sufficient speed cutoff1/(4D), and
compare against the existing width cutoffs and any already archived
two-window cutoffs. A cluster
containing a wider component may use its larger w. Declare in advance
that no improvement is a negative result about this sufficient test,
not a reason to enlarge the speed domain. No such test was run here.

The quickest algebraic falsifier of the lemma itself would be three
closed intervals meeting its inequalities and an actual single
periodic blocking schedule containing them all. The shared-lap proof
explains why such a fixture should be impossible. Equality cases must
use open blockers for existence and closed blockers for duration.

The more important long-term test is whether endpoint arithmetic forces
clusters or a surviving contact without first reconstructing the full
safe set. Nothing in the current geometry answers that question.

## Source and access limits

Read AGENTS, README, CONTRIBUTING, CLAIM_STATUS, current HANDOFF/LR2
entries, the Ultra brief, TWO_TIME, ADAPTIVE_REFLECTED_PAIR,
LAST_RUNNER_COMPATIBILITY and its supplied reviews, EXACT_INTERVAL,
FASTEST_CORE, DOMAIN_CONNECTIONS, and relevant SOURCES entries.
Some older linked notes are absent from the supplied local snapshot;
their HANDOFF summaries were used only as explicit prior-work warnings.
The snapshot directory has no local .git metadata, so its live branch
could not be independently inspected; the pinned head is inherited from
the team brief. No frozen output was changed, no scan was run, and no
claim is made about arbitrary eight-runner configurations from the
special fixed1,4,5 family.
