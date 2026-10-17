# Center-selection comparison, version 1

Selected after rule commit `15af72d70ab1486f13869b30ac3b1201fb5c047e`.
Freeze this file, explicit config, both implementations and dependency hashes
before evaluating the new arithmetic inputs. They were selected by recipes,
without calculating their answers. This is a prospective stress test, not a
random sample or a claim that no equal tuple occurs anywhere in repository history.

## Inputs and scope

Twenty-four arithmetic cases: m=4,6,8 core speeds; j=1,...,m; eight recipes
j+4, j+9, 2j, 2j+3, j^2+2, j^2+j+2, 3j+(j mod 2),
and j+10*floor((j-1)/2). Use n=m+2 and d=1/n. Retain nonprimitive cores and
do not normalize by gcd: the domain of added integer speeds is fixed.
All starts are 0, reference is 0, and admissible added r is positive and absent
from the core. Explicit lists are in config.json. No input is removed or
replaced because its answer is uninteresting or unresolved.

Seven separately labelled exposed/semantic controls:

* S={1}, d=1/3: YES exactly at M=0, center 1/2, H=G=1/6.
* S={1}, d=33/100 and 101/300: below/above equality, expected YES/NO.
* S={1,2}, d=1/3: core is exactly two isolated points, expected NO for a
  universal interval although ordinary core feasibility is nonempty.
* S={1,2}, d=2/5: empty core, expected NO; artificial threshold, not LRC failure.
* Exposed original eight-speed success and primes-derived failure from the
  prior studies: regression controls only, not fresh generalization evidence.

The tiny pre-freeze checks in DEVELOPMENT_CHECKS.json use only three of those
analytic controls and the exposed specified-center one-term UNKNOWN. No
arithmetic input has run at this stage.

## Primary, reference and diagnostics

The primary merges constraint events, checks candidate G directly from core
speeds and uses exact rational H. It stops at the first chronological success,
or exhausts the stream for NO, or reports UNKNOWN at a cap. It does not import
or construct the complete safe set. A diagnostic trace retains only the
core-safe candidates visited before stopping; this output storage is distinct
from the O(m) streaming state.

The alternate script independently intersects complete safe-band unions,
including singleton components. Direct integer-range band contact plus a
width tail classifies each component without calling H, G or the selector.
Compare existential decisions and first successful components. After the
first success, further component checks are diagnostic work, separately counted.
No result-dependent selection of extra cores is allowed.

Verify each primary H by all-r contact of its critical-width interval and
the tight critical gap; verify strict blockers, endpoint core bands, midpoint
coverage and exact equality. For NO, check every positive full component has
its corresponding primary record and independently count all threshold cells.
Preserve isolated components in the reference and give their denominator blocker.

For each YES save physical witnesses for every admissible r below the selected
interval's width cutoff plus cutoff, cutoff+1, 10^6+1 and 10^18+1, bumping
past excluded speeds and deduplicating. The width argument, not these sample
tail witnesses, supplies the infinite conclusion. For every distinct blocker
from either complete reference classification or the primary trace, build
the full child set, retain its hash/count and an actual witness or EMPTY.
Empty artificial-threshold controls are not LRC counterexamples. A blocked
source whose child is nonempty explicitly preserves the distinction.

Two shortcut diagnostics are subordinate to the complete method. The raw
constraint-boundary center rule analytically always rejects because G<=0<H;
the equality control is its counterexample. Separately try reduced centers
with denominator <=m+2 in increasing denominator/numerator order. This is a
heuristic candidate restriction, not a completeness claim. Verify its answers
with independent direct contact, and retain every miss without changing its cap.

## Budgets and failure rules

Caps per case: sum of speeds 2,000; raw events 4,000; candidate cells 4,001;
H terms 4,096 per center; alternate contact queries 4,096 per interval; child
speed at most 8,192. A cap is UNKNOWN, not NO. Set each primary cap to zero
in turn on the exposed original positive core to test UNKNOWN separation;
also retain a one-term H query at c=159/1330,d=1/10. No large scan or unattended
job is authorized by this protocol.

Limit primary, alternate verification and one primary replay to 240 seconds
each, with per-case checkpoint files. Before each command compare every
dependency and manifest to the execution-freeze Git commit. Any discrepancy
stops the comparison; save its evidence and version a fix rather than altering
frozen sources silently. Unexpected unresolved cases are INCOMPLETE, not PASS
for a completed full-domain comparison. Stop after this domain and one replay.

Report false positives/negatives, unknowns, exact-zero margins, shortcut misses,
component/singleton counts, child outcomes and costs. Charge event generation,
core predicates and H terms separately from complete band construction,
intersection comparisons, contact checks, verification, child diagnostics and
replay. These are different operations, not a runtime comparison.

The symbolic completeness argument is input-general within its rational domain;
the numerical evidence is bounded to these cases. Both implementations and
the fresh derivation are AI-authored in this continuation. This supplies
separately structured internal checks, not external proof review. General
claims remain proof candidates; no novelty, efficiency advantage, arbitrary-core
single-source theorem, other-reference result or general LRC proof follows.
