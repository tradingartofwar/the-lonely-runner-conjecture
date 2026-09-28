# Core windows and the obstruction to truncating the mixed kernel

September 28, 2026. Baseline
`bcf959b45a35701f2fd710b1d86ca2cc3152e14c`.

**Status: HYPOTHESIS / proof candidate for the general implications below;
OBSERVED for the declared exact rational calculations.** This is an AI-derived
internal mathematical review, not independent human certification. The core
window corollary is conditional on the separately reviewed mixed-kernel span
lemma. No novelty, full Lonely Runner, or all-reference claim is made.

The main structural finding is negative but precise: **on the inherited
strict16 window, every nontrivial truncation of every translate of this mixed
kernel has positive signed multiplicity excess.** Thus merely truncating the
annihilating kernel and using the sign of its integral does not recover this
known positive window. The proof is an analytic all-translates statement, not
a numerical translation search.

## 1. Core-window corollary and the integer threshold

Let four open blocking trains have periods `p_i>0`, duty `1/4`, and arbitrary
phases. Write

`P=max_i p_i`, `S=sum_i p_i`, `H=(3/4)S+(1/4)P`.

Assume the mixed-kernel lemma that every strict selected chain has union span
less than H. Then every closed interval of length at least H has a common-safe
point. Otherwise its points are covered by the open blocked set. Starting with
an occurrence containing the left endpoint and continuing through strictly
overlapping occurrences gives a finite chain whose union begins before the
left endpoint and ends after the right endpoint. Local finiteness permits a
finite choice. Its span exceeds H, a contradiction. This argument includes
the equality `width=H`; endpoint safety is not discarded.

For the physical common-start case with selected reference 0, `n=8`, core
`{1,4,5}`, and threshold `1/8`, the whole interval

`J=[9/32,3/8]`, `|J|=3/32`

is core-safe. Its core phases range respectively through `[9/32,3/8]`,
`[1/8,1/2]`, and `[13/32,7/8]`. For residual positive speeds `v_i` and
`v_min=min_i v_i`,

`H=(3/4)sum_i(1/v_i)+(1/4)(1/v_min) <= 13/(4 v_min)`.

Consequently `v_min>=104/3` suffices, and **four integer residual speeds at
least 35 suffice**. This is a sufficient minimum-speed cutoff, not an asserted
optimal cutoff. Distinctness is not used in this upper estimate.

The remaining domain is not a finite speed box: failure of `v_min>=35` leaves
at least one small residual speed while the other speeds can be arbitrarily
large. Also, an arbitrary configuration need not supply the core `{1,4,5}`.
The result certifies the selected reference under this supplied core; it is
not the missing general core-selection or all-reference implication.

## 2. Exactly the twelve inherited windows

The protocol was written before implementation. The only calculations are
the twelve inherited `S,H,width` comparisons and a declared strict16 event
check in Section 4. Existing witness statuses below were read from the old
results, not obtained by a new selector run.

| Inherited input | H | Window width | H sufficient? | Archived earliest result |
| --- | --- | --- | --- | --- |
| doubling_112 | `251/5376` | `3/32` | yes | `145/512` |
| small_gcd_113 | `28327/607488` | `3/32` | yes | `129/448` |
| tight_13 | `4801/12012` | `3/32` | no | `3/8`, equality only |
| control_8_11 | `3221/7392` | `3/32` | no | `17/56` |
| affine_309 | `91126213/10037902080` | `3/32` | yes | `697/2472` |
| affine_310 | `3052387/336764160` | `3/32` | yes | `467/1656` |
| affine_320 | `259431/29434720` | `3/32` | yes | `721/2560` |
| strict_16 | `5749/14784` | `3/32` | no | `17/56` |
| aux_condition_strict | `53/32` | `13/40` | no | `73/64` |
| aux_condition_equality | `139/960` | `1/120` | no | `1/120`, equality |
| common_start_lift_clipped | `H_lift` | `w_c` | no | empty |
| common_start_lift_extended | `H_lift` | `w_e` | no | `163489640070647/490466743069080` |

For the last two rows the unchanged residual speeds are

`(429158400185445,432537600141440,519045120390144,713687040084480)`.

Writing these increasingly as `v_1,...,v_4`,

`H_lift=1/v_1+(3/4)(1/v_2+1/v_3+1/v_4)`,

`w_c=18138392386519/7778661291574374470615019520`,

`w_e=1/343326720148356`.

The full exact fraction for `H_lift` and every comparison difference are in
`windows_results.json`. **Both S and H certify the same five of these twelve
windows; H adds zero successful rows in this frozen set.** No row has
`H=width`. The threshold improvement and the equality case therefore rest on
the analytic argument, not an observed boundary fixture.

The huge lift has all residual speeds above 35, so the proposed corollary
guarantees success somewhere in the full core interval J. Its much narrower
clipped window is a different input and remains genuinely empty. A condition
on the speeds alone cannot justify replacing J by any arbitrarily narrow
subwindow of J.

## 3. A finite phase-sensitive truncation formula

Choose one largest-period label `j`, with `p_j=P`. Let the multiset of 64
offsets be

`D={sum_(i!=j) r_i p_i/4 : each r_i in {0,1,2,3}}`.

Multiplicity is retained when distinct choices give the same offset. Up to
irrelevant endpoint values, the mixed density is

`K(x)=(1/(64P)) sum_(d in D) 1_(d,d+P)(x)`.

For train `i` with blocked intervals
`(s_i+m p_i,s_i+(m+1/4)p_i)`, put

`z_i(t)=(t-s_i)/p_i`,

`A_i(t)=p_i [floor(z_i(t))/4 + min(frac(z_i(t)),1/4)]`,

`F(t)=sum_i A_i(t)-t`.

The floor convention works for negative arguments too, and `F'=M-1` almost
everywhere. For a supplied closed `W=[L,R]` and a supplied translate `a`,
define

`l_d=max(L,a+d)`, `u_d=min(R,a+d+P)`.

Then the exact truncated signed excess is

`E_W(a)=(1/(64P)) sum_(d: l_d<u_d) [F(u_d)-F(l_d)]`.

This takes at most 64 interval terms, each using four periodic primitives at
two endpoints: at most 512 individual primitive evaluations. No per-lap
endpoint enumeration, numerical quadrature, or common-period computation is
needed. Rational input produces exact rational arithmetic. This counts
arithmetic operations, not bit complexity. Choosing a useful translation is
a separate problem; this formula does not solve that selection problem.

If `E_W(a)<0`, there must be common-safe time of positive measure in W,
because `M-1>=0` wherever at least one train blocks. Thus this is a finite
sufficient certificate for some shorter windows. It is not complete. The
full convolution identity is

`E_W(a)=-integral_(real line outside W) K(t-a)(M(t)-1) dt`.

Once the support extends outside W, the unknown signed contribution outside
W cannot simply be discarded. Renormalizing the restricted density does not
restore any train's quarter-duty identity. A zero integral alone is also
inconclusive without further overlap or endpoint information.

This formula answers a limited computational question positively: a supplied
truncated certificate can be evaluated without a full endpoint scan. It does
not give a generally successful certificate or a forced phase-local choice.

## 4. Strict16 defeats every translate of this truncated kernel

Here residual speeds are `(6,7,11,16)` and `W=J`. Let `f=M-1` and
`G(t)=integral_(9/32)^t f(u) du`. Direct arithmetic from the six intersecting
blocked occurrences gives, ignoring endpoint values only for integration:

| Sign of f | Interval | Length |
| --- | --- | --- |
| +1 | `(9/32,25/88)` | `1/352` |
| -1 | `(17/56,39/128)` | `1/896` |
| +1 | `(5/16,41/128)` | `1/128` |
| +1 | `(31/88,17/48)` | `1/528` |
| +1 | `(47/128,3/8)` | `1/128` |

Elsewhere in J, f is zero almost everywhere. In particular, the common-safe
closed interval is exactly `[17/56,39/128]`, of positive length `1/896`.

The total signed excess is

`T=1/352-1/896+1/128+1/528+1/128=569/29568>0`.

The only decrease of G is `1/896`, occurring after G has already reached
`1/352`. Its value after that decrease is `17/9856>0`; every later nonzero
change is positive. The final positive interval reaches T only at `3/8`.
Therefore

`G(9/32)=0`, `G(3/8)=T`, and `0<G(t)<T` for every interior t in J.

Every positive-length prefix, suffix, or full copy of J consequently has
strictly positive signed excess.

**General box obstruction.** Suppose a window of width w has this strict
prefix/suffix property. A real interval of length at least w intersects the
window, up to endpoints, in either a prefix, a suffix, the full window, or
the empty set. Thus every such positive-length intersection has positive
signed excess. Any nonnegative mixture of these boxes has positive weighted
signed excess whenever it puts positive mass on the window.

For this mixed kernel, every box has width `P=1/6`, while `|J|=3/32<1/6`.
Applying the obstruction yields

`E_J(a)>0 whenever integral_J K(t-a) dt>0`, for **every real a**.

There is no useful exceptional translate. If the kernel puts zero mass on J,
its zero integral says nothing about J. In particular, positivity of clear
duration does not imply that a translate of this truncated annihilating
kernel detects it.

The declared exact check reconstructed only this strict16 event sequence,
independently of the displayed list, and verified the prefix and suffix
ranges `[0,569/29568]`. The strict interior inequalities and the all-translates
implication are analytic deductions. No translate was tested or searched.

This is a limitation of the sign certificate, not a failure of loneliness.
Additional exact overlap information could compensate the positive signed
excess; a shorter localized weight could isolate a gap; or the already
available bounded projection procedure can select the earliest safe point.
But forcing or selecting such local information is additional work, not a
consequence of truncating the original convolution identity. Choosing a
subwindow already known to lie in a safe gap would only repackage that known
witness, not supply its discovery.

## 5. Equality contacts and the clipped lift

For tight13, residual speeds `(6,7,11,13)` have a strict overlapping cover of
`[9/32,3/8)` supplied by the occurrences

`(15/56,17/56)`, `(31/104,33/104)`,
`(5/16,17/48)`, `(31/88,3/8)`.

These come respectively from speeds 7,13,6,11. Each starts before the
preceding occurrence ends, and the first contains `9/32`. At `3/8`, the
residual phases are `(1/4,5/8,1/8,7/8)`, all safe. Hence the window has only
the isolated safe endpoint `3/8`. Every nonnegative absolutely continuous
weighted signed excess is nonnegative because `M>=1` almost everywhere on
the whole window. An integral sign argument cannot see that singleton.
Endpoint-aware phase checks must remain separate.

The archived huge lift similarly distinguishes the two supplied windows.
The seven selected occurrences openly cover the clipped window; the next
safe time is

`t_*=163489640070647/490466743069080`.

The clipped right endpoint is strictly below `t_*`. Extending the right
endpoint exactly to `t_*` includes its first common-safe point and gives an
endpoint-only witness within that extended window. These are inherited
certificates, not new reconstructions. The clipped failure is real; a sound
local existence certificate must fail there. For the extended window, an
absolutely continuous integral again cannot detect the zero-measure witness.

Thus the remaining distinctions are precise: the width criterion is silent
on both tight/strict controls; tight13 needs equality awareness; strict16 has
positive safe duration but defeats all translations of the truncated mixed
kernel's sign test; and the clipped lift has no witness in the requested
window at all. None warrants fitting another cutoff or assuming that a
failed sufficient test proves emptiness.

## 6. Reproduction and limits

From this local project root:

```bash
python reviews/2026-09-28-short-kernel/windows.py
```

The frozen protocol is `windows_protocol.json`; exact results and source
hashes are in `windows_results.json`. The source files are the twelve-row
protocol and results under `reviews/2026-09-28-chain-termination/` in the
canonical repository. The script prefers those canonical paths and falls
back to the historical sibling-workspace paths recorded in the frozen
protocol only if the canonical files are absent. It asserts the full frozen
protocol hash and both source hashes before any evaluation. This path-only
portability revision preserves the protocol bytes and numerical scope; the
same frozen calculation was rerun afterward. The prior candidate note is
`notes/EXPLICIT_CHAIN_BOUND_2026_09_28.md` in the canonical repository.

There was no new selector execution, new speed input, other event
reconstruction, phase/translation search, full-configuration reconstruction,
or fitted rule. The general statements remain proof candidates requiring
independent review. The width audit does not depend on which improved
universal move bound the other reviews ultimately retain.
