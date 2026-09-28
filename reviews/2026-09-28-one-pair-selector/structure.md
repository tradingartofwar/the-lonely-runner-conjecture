# Information and cost audit of the frozen one-pair selector

This report reviews only the policy in `protocol.json`, SHA256
`36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e`,
at declared baseline `539dd899ac8ceea5b50d46b72c0fa28cec7a354e`.
It adds no cases, experimental computations, reranking, or alternative policy. Material
AI involvement includes this review. Finite outcomes are bounded observations;
general arguments retain the repository's proof-candidate limits.

## The opening is selected before the residual evidence

The input includes a prescribed three-speed core. The policy constructs its
complete closed safe components, keeps singleton components in that record,
and chooses the widest positive-length component with earliest-left tie
breaking. It does not choose the core. A claim that this solves core selection
would exceed the input contract.

Core component discovery is real work even though it does not use the four
residual runners. The number of safe laps and threshold events can grow with
the supplied core speeds. The fixed small cores in these controls do not
establish a speed-independent discovery bound. Reusing a repeated core could
amortize discovery, but only an implementation that actually reuses it may
count that saving; cold and cached costs should not be silently interchanged.

After the window is frozen, none of its endpoints, the core, or the residual
pair order may change in response to a failed certificate. In particular,
choosing another complete component after inspecting overlaps would be a
different policy, even if no full seven-runner allowed set were consulted.

## What is known before the overlap query

For the fixed window J, the four individual endpoint integrals determine
`E=sum(D_i)-|J|` and the six scalar caps `C_ij=min(D_i,D_j)`. The following
inferences are sound without measuring any pair overlap:

- If `E<0`, the single-runner union bound already gives positive allowed
  duration at least `-E`. A pair query is unnecessary.
- If `E>=0` and `max C_ij<=E`, every one-pair lower bound is nonpositive,
  because `O_ij<=C_ij<=E`. This excludes the whole one-pair certificate class
  on this chosen window, not physical existence.
- If `max C_ij>E`, a positive one-pair certificate remains possible. Selecting
  the greatest cap prioritizes an upper bound on potential overlap. It is
  neither a prediction nor a lower bound on actual overlap.

The caps are derived from the same four singles; they do not constitute six
new overlap measurements. They retain local blocking concentration but
discard relative placement, lap alignment, simultaneous occupancy, and
containment. Two large blocking sets can have little or no intersection.

If the single durations are ordered `D_(1)>=D_(2)>=D_(3)>=D_(4)`, the largest
cap is simply `D_(2)`. The best one-pair lower bound is therefore at most
`D_(2)-E=|J|-D_(1)-D_(3)-D_(4)`. This optimistic ceiling behaves as if the
second-largest blocker were completely contained in the largest. The
selector has not established that containment; it uses the ceiling only to
prioritize the query or to rule out the certificate class.

The selected pair's low-order description `b=h*a+r` is chosen only after
pair ranking. Its signed-residual strips are an exact evaluation method;
they do not supply a prior eligibility gate or cause reranking. A zero
eligible region must return zero overlap if that pair is selected. It must
not trigger an undeclared second pair query.

## Three distinct failure and recovery stages

The archive must keep these outcomes distinct:

1. **Cap exclusion:** no positive one-pair bound can exist on this J from
   the actual pair overlaps, since all are bounded above by E.
2. **Selected-query failure:** the one queried overlap satisfies `O-E<=0`.
   This says nothing about unqueried pairs unless cap exclusion already held.
3. **Endpoint fallback:** only J's right endpoint is tested against all
   seven constraints. A valid endpoint introduces new joint point information;
   its success does not repair the earlier pair certificate.

For a valid endpoint, intersect the seven closed safe laps containing it.
This recovers the complete connected allowed component containing that
particular endpoint. It is a permitted local calculation, not a reconstruction
of every allowed time. A positive interval has strict interior; a singleton
requires opposing threshold directions, with one runner blocking immediately
before and another immediately after. Contact labels cannot be inferred
from duration alone.

An invalid right endpoint makes this frozen policy uncertified. It does not
prove the window empty or the configuration non-lonely. The ordered campaign
must stop there, and any later prescribed cases must be marked unexecuted
without even evaluating their selector outcomes. Looking at another endpoint,
another pair, a tree, or another window would change the frozen policy.

## Cost contract and what one query does not establish

The report must separate core construction, four single-duration integrals
(eight primitive endpoint evaluations), six scalar caps, an optional exact
pair evaluation, and an optional seven-runner endpoint/lap calculation.
Pair-query count alone is insufficient: signed-residual strip construction,
clipping, and every primitive evaluation belong to that one query's cost.
The number of strips can depend on the residual and window length; a fixed
number of reported overlaps is not a fixed arithmetic-work guarantee.

Rational operand bit sizes are a separate dimension from the number of
calls. A small call count on these fixed controls does not establish an
empirical runtime speedup, an asymptotic complexity improvement, or a cheap
general selector. Independent verification uses a different algorithm and
its work should not be mixed into the generator's policy cost.

## Observed policy outcomes

The following records come from `results.json`, SHA256
`07de386d85fbd27cfbba45ce53f4006a7d2ac9c08249d2050b616ed598faf2ba`.
There are three positive queried-pair bounds, one endpoint interval, one
endpoint contact, and one final uncertified case. The failure is the last
prescribed case, so the stop rule leaves no unrun cases. No singles-only
positive branch is exercised.

| Control | Frozen J | Queried pair | Pair bound O-E | Fallback and final outcome |
| --- | --- | --- | --- | --- |
| fast_113 | [9/32,3/8] | 56,113 | 1223/911232 | Not called; positive duration |
| changed_core | [17/40,23/40] | 56,72 | 2169/202496 | Not called; positive duration |
| doubling_112 | [9/32,3/8] | 56,64 | 59/16128 | Not called; positive duration |
| tight_13 | [9/32,3/8] | 6,11 | -421/32032 | Contact at 3/8 |
| one_pair_ceiling | [9/32,7/16] | None | No pair evaluated | Interval [17/40,7/16], width 1/80 |
| strict_16 | [9/32,3/8] | 6,11 | -171/9856 | Speed16 blocks 3/8; uncertified and stop |

For `one_pair_ceiling`, the greatest cap and E are both 1/20. The
pre-query ceiling for every pair score is therefore zero. The stored
`duration_lower_bound=-1/20` is the singles-only bound -E, not that optimistic
cap-adjusted ceiling. The endpoint calculation independently recovers a
positive interval; speed2 has the sole equality controller and enters safety
leftward. This success does not make the one-pair class successful.

For `tight_13`, the valid endpoint's equality controllers are speed5
leftward, speed11 rightward, and speed13 leftward. The seven containing
safe laps intersect in exactly {3/8}. It is a contact certificate, with no
positive duration. For `strict_16`, speed16 has distance zero at the same
endpoint, so no containing safe laps are constructed and no second point is
tried.

All five queried overlaps are strictly positive. Two are nevertheless too
small to exceed E. Thus this finite campaign demonstrates neither a general
zero-overlap avoidance rule nor that positive overlap suffices for a useful
certificate. The negative signed residual r=-1 is exercised for 6/11; h=1
and h=2 are both exercised. An r=0 selected query is not exercised: the
doubling input selects 56/64, not 56/112.

## Observed discovery and evaluation cost

These are sums and transcriptions of the declared counters, not runtime
measurements. Each row independently reconstructs its core components.
Repeated core145 inputs receive no cache credit. Every row also pays four
single integrals, eight C calls, and six caps.

| Control | Core laps / event vertices / components / intersection iterations | Pair queries | Candidate strips / examined cells / positive cells | P calls | Endpoint distances / safe laps |
| --- | --- | --- | --- | --- | --- |
| fast_113 | 10 / 22 / 6 / 13 | 1 | 3 / 3 / 1 | 4 | 0 / 0 |
| changed_core | 9 / 18 / 7 / 11 | 1 | 5 / 12 / 6 | 24 | 0 / 0 |
| doubling_112 | 10 / 22 / 6 / 13 | 1 | 3 / 4 / 1 | 4 | 0 / 0 |
| tight_13 | 10 / 22 / 6 / 13 | 1 | 3 / 3 / 1 | 4 | 7 / 7 |
| one_pair_ceiling | 7 / 16 / 4 / 8 | 0 | 0 / 0 / 0 | 0 | 7 / 7 |
| strict_16 | 10 / 22 / 6 / 13 | 1 | 3 / 3 / 1 | 4 | 7 / 0 |
| Total | 56 / 122 / 35 / 71 | 5 | 17 / 25 / 10 | 40 | 21 / 14 |

The totals include 24 single integrals, 48 C calls, 36 caps, 68 candidate
residual events before filtering, and 20 W calls. The changed-core query
alone uses six positive strip cells and 24 P calls, compared with one cell
and four P calls for each other query. Calling all five queries one unit of
work would hide this difference. Positive cells count evaluator pieces,
not full physical overlap components or independently discovered witnesses.

Across the recorded primitive arguments, the greatest C numerator and
denominator bit counts are 12 and 6; the corresponding P counts are 11 and
7. Across all reported fraction strings, they are 21 and 24. These maxima
are separate and need not occur in the same fraction. They are not bounds
on every transient rational arithmetic operation, sorting comparison, or
memory allocation. The counters describe this implementation's work on
the fixed controls; they do not establish a speedup over an alternative.

## Information-flow inspection

Source inspection of `select.py` finds the prescribed dependency order:
the complete supplied-core safe set and J are computed before residual
durations; caps use only those four durations; exactly the first ranked
pair enters the signed-strip evaluator when its gate permits; fallback
uses only the chosen right endpoint. A nonpositive bound never triggers
another pair or another opening. The case loop breaks at `uncertified`.

The generator imports standard-library modules and reads the protocol,
its own source bytes for provenance, and its own saved output only after
regenerating the campaign in check mode. It does not read benchmark
durations, all-pair archives, full seven-runner allowed sets, or the
independent verifier. The separation between semantic hashes and
evaluation/cost records makes this distinction inspectable. This is a
source/dependency audit; it does not substitute for the separate arithmetic
verifier.

The chosen endpoint does introduce joint seven-runner information, but
only after the scalar/one-pair stages fail and at the single allowed point.
The seven safe laps are constructed only when that point is valid. A
benchmark's knowledge that an untested endpoint is invalid must not be
counted as a primary endpoint query.

## Post-selection comparison and retained failure

`benchmarks.json` supplies separately attributed archive fields after
selection. These are comparison targets, never selector inputs. The
changed-core choice agrees with the archived best pair. The other two
positive pair certificates are sufficient without being best: fast_113's
archived best pair is 72/113, while doubling_112's is 56/112. Its exact
doubling relation supplies no priority under the frozen cap/numerical tie
rule. No retrospective promotion of that relation is warranted.

The endpoint interval of `one_pair_ceiling` has width 1/80, whereas the
archived entire clear duration on J is 11/480. The fallback certifies only
its containing component. `tight_13` has archived clear duration zero on
J and the retained contact at 3/8.

Most decisively, `strict_16` has archived clear duration 1/896 on this very
J. Its archived best pair bound is still negative, -169/14784, and its
best tree bound is -23/29568. Merely reranking the pair cannot repair the
frozen opening. The previously known triple-exclusion certificate supplies
the missing joint-placement information and attains 1/896; alternative
openings are also known. Neither mechanism is added to this policy.
The useful question left by this failure is what limited information could
choose a stronger certificate or another opening, while accounting for
the cost of discovering that information. This campaign does not answer
that question by increasing its budget after failure.

## Existing limits that the interpretation must preserve

The core135 central component `[17/40,23/40]` already shows that the relation
`113-2*56=1` can have zero eligible phase area on a useful opening. Actual
overlap 56/72, rather than that relation, supplied the prior local certificate.
The frozen concentration ranking selects 56/72 there and succeeds without
querying 56/113. This is the observed consequence of its different scalar
ranking, not a retrospective drift gate or a general exclusion of zero
eligible overlap.

The tight 6/7/11/13 input retains isolated threshold contacts, so an endpoint
success cannot be labelled positive duration. The core124, extras3/5/6/8
control has a positive opening even though its best single-pair bound is
negative; it remains a check against calling one-pair failure physical
infeasibility. The older 45/90 and 266/532 physical collisions show that
even all local singles/pairs need not determine exact duration. They do not
invalidate a sound positive lower bound obtained from fewer quantities.

Finally, the previous qualitative containment selector chose a sole blocker
that covered its whole selected window. Few residual labels are not enough.
This experiment asks whether local concentration can guide one restricted
query more effectively, not whether any such compressed information must
always select a successful opening.
