# Center-width generalization test v1

Selected after rule freeze `6ea4ca25250d070380f174665d7ad9dfc7824e32`.
Freeze this protocol, config, run.py, verify.py and dependency manifest before
any new-family evaluation. The exposed original (1,2) example is development
evidence only. This is a prospectively selected mathematical stress test,
not a random sample or a claim of globally unseen inputs throughout history.

## Two separate arms

**Constructed families.** Use the six reduced centers
`2/11,3/13,5/17,7/19,9/23,11/29`, each at n=8,10,12 and d=1/n. These centers
span locations and denominators beyond the old rule's v<=n restriction. For
each, evaluate the frozen H rule, take h=H, and enumerate the entire finite
eligible-speed palette through floor((1/2-d)/H). If its size is at least n-2,
form two cores: the smallest n-2 and largest n-2 eligible speeds. Retain both
labels even if they coincide. Otherwise report INSUFFICIENT_PALETTE without
substitution. These are conditional families deliberately built to meet the
rule, not evidence about arbitrary cores.

For each constructed core, check its proposed critical interval h=H, the
smaller core-safe interval h=H/2, and the denominator-only shortcut h=d/v.
The critical interval should be universal; the half-size interval should have
the rule's exact critical blocker. The shortcut is a deliberately overbroad
hypothesis to falsify, not part of the theorem candidate. Report all outcomes.
Save finite-domain witnesses and tail controls R,R+1,10^6+1,10^18+1, adjusted
upward past duplicate core speeds and deduplicated. Reconstruct the complete
child set at each distinct blocker and preserve an actual witness elsewhere
when one exists; do not infer nonexistence from interval failure.

**Independent core selection.** Use j=1,...,8 and the following twelve explicit
speed lists, generated arithmetically in config.json without evaluating H,
palettes, safe sets or coverage:

- j+k for k=2,7,17;
- j^2+k for k=1,3,7;
- j^2+j+k for k=1,3,7;
- j^3+k for k=1,3,7.

All have stationary reference 0, common start, n=10 after one admissible
positive integer added speed, and d=1/10. Do not normalize speeds or discard
cores based on gcd, successful intervals, or observed answers. These differ
from the earlier p,q templates and the prior eight explicit/altered inputs;
no claim of statistical representativeness follows.

Construct each complete core with the unchanged exact interval checker.
For EVERY maximal component, use its rational midpoint, evaluate H with the
frozen early-stop rule, and compare its half-width with H. Also compute G and
check that G equals the component half-width. Keep singleton components;
their half-width zero is below positive H. A failure gives the first maximizing
critical speed, not necessarily the smallest speed blocking that component.
For universal components, save finite-domain and tail-control witnesses as
above. Check complete children at every distinct recorded blocker. A core
with no universal component is not a counterexample to the criterion or LRC.

## Alternate verification and failure criteria

The alternate script imports the existing threshold-event/phase helpers only,
not run.py, the H evaluator, or lonely_runner.checker. It must reconstruct all
twelve challenge cores and all saved blocker children. Verify palette membership
by constant-lap endpoint containment, including absence of eligible speeds
within the analytic bound; verify the bound itself.

For EACH computed H, independently certify the critical-width interval by
direct safe-band intersections for every positive r below its width cutoff,
plus the width tail. Check a critical-speed equality at H with positive deficit;
this proves that smaller half-widths fail. Do not merely recalculate the H
formula using the same code. Check reported evaluated-term counts and stopping
conditions using direct safe/unsafe geometry and the stated upper bound.

For each actual candidate interval, independently scan its complete finite
width domain until the first blocker or budget; compare to the primary decision.
For singletons, use the reduced time denominator. Verify G from containing
core-safe bands, all witness phases/laps, the alternate first-contact time,
scope/exclusions, and every strict blocker gap. Check whole-core witnesses at
blockers separately from the rejected source. Any implementation disagreement
is a discrepancy, not silently repaired validation. Preserve output and version
any necessary correction separately.

Two supplied controls exercise equality at c=1/4,d=1/10,h=1/40 (r=4), and
an intentional H-budget UNKNOWN at c=159/1330,d=1/10 with one term. These are
analytic semantics checks, not new n-runner families. The original (1,2)
example is not rerun as a fresh family in this study.

## Budgets, accounting and stop

- H evaluation: at most 4096 terms per center; a premature cap is UNKNOWN.
- Alternate band-domain scan: at most 4096 positive speeds per interval;
  premature exhaustion without a blocker is UNKNOWN, not success/failure.
- Core speed sum <=1500, complete components <=1200; exceeding either yields
  UNKNOWN_CORE_BUDGET, without selective replacement.
- Full child construction requires added speed <=8192; otherwise preserve the
  local blocker but report UNKNOWN_CHILD_BUDGET.
- Each primary, alternate and replay command is limited to 240 seconds. Save
  checkpoints after every constructed-center row and challenge core.
- Run primary once, alternate verification, and one identical primary replay.
  No additional case selection, fitted rule, or expanded domain after results.

Charge H terms, palette predicate checks, source geometry (input bands and
components), child construction and witness recovery separately. Verifier and
replay work are extra work actually performed. No runtime or asymptotic advantage
is claimed. End after this domain and report false positives, false negatives,
unknowns, shortcut counterexamples, and limits as well as confirming examples.

The analytic criterion ranges over rational centers, arbitrary positive integer
cores and 0<d<1/2. The new computations cover only the declared domain. Keep the
proof candidate, conditional constructed class, independent-core observations,
and earlier three successes distinct. Same-author alternate algorithms do not
constitute independent human/formal proof review. No general LRC or novelty claim.
