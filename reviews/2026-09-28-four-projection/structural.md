# Structural challenge: the unconditional 22-step selector fails

Date: September 28, 2026. This is explicitly **post-protocol analytical
follow-on work**. It preserves the original condition and archived controls.
Material AI involvement: the structural challenger derived the interval-chain
counterexamples; the coordinator derived the common-start lift; the structural
challenger checked that lift with exact rational arithmetic. A separately tasked
reviewer checked the auxiliary construction. None of this is external review or
a literature novelty assessment.

**Outcome:** an explicit four-constraint auxiliary example disproves the
unconditional claim that `P_a,S_bcd,P_a,S_bcd` always returns a feasible point at
threshold 1/8. A second, directly constructed example establishes the same
failure for eight distinct integer-speed, common-start runners, with a supplied
core-safe window. The speed-conditioned sufficient theorem is not contradicted.
Lonely Runner is not contradicted: the next projection supplies a valid lonely
moment in these examples.

## 1. A bad-interval chain defeats the hoped-for waiting bound

Safety means `||v*t+alpha||>=1/8`; each open bad interval is
`((m-1/8-alpha)/v,(m+1/8-alpha)/v)`.
Use the following ordered residual triple:

| Runner | Speed | Phase | Selected bad intervals |
| --- | --- | --- | --- |
| b | 1 | 925/1056 | (-1,263)/1056 |
| c | 6/5 | 127/220 | (262,482)/1056 |
| d | 33/20 | 1/8 | (-160,0)/1056 and (480,640)/1056 |

In their temporal order d,b,c,d, consecutive intervals strictly overlap.
They therefore cover the whole open interval

`(-160/1056,640/1056)=(-5/33,20/33)`.

Both outer endpoints are safe for all three runners. Its length is `25/33`,
strictly larger than `3/(4b)=3/4`. Starting at `t0=-159/1056=-53/352`,
the earliest triple-safe time is `T=640/1056=20/33`; the wait `799/1056`
is larger than 3/4. Thus the proposed uniform waiting bound cannot repair the
fourth-runner proof.

This is a direct interval construction, not a parameter scan. The faster
runner contributes two different blocking occurrences, connected by the
other two runners. Counting only one occurrence of each runner would miss the
long blocked component.

An earlier analytical construction had speeds `(1,1,8/5)` and phases
`(113/128,41/64,1/8)`, with the open chain
`(-20,0),(-1,31),(30,62),(60,80)` divided by 128. That already refuted
the proposed 3/4 waiting bound, but by itself did not defeat 22 steps: the
preceding safe gap was too large. The present chain was derived specifically
to close that remaining step. These constructions must not be counted as
independent held-out data.

## 2. A fourth runner makes 22 projections end at an unsafe time

First use the simple auxiliary case

`(a,b,c,d)=(1,1,6/5,33/20)`

with phases `(97/352,925/1056,127/220,1/8)`.
Runner a has a fresh safe lap beginning at `t0=-159/1056` and ending at
`633/1056`. Its preceding safe lap ends at `L=-423/1056=-141/352`.
Take this L as the input to the proposed composition.

Runner c's preceding bad interval is `(-618,-398)/1056`; it contains L.
The other two triple runners are safe at its right endpoint. Consequently:

| Operation | Output | Reason |
| --- | --- | --- |
| First P_a | -423/1056 | L is the included a-safe endpoint |
| First S_bcd | -398/1056 | Earliest triple safety, at the prior c-bad exit |
| Second P_a | -159/1056 | First triple output lies inside a's bad interval |
| Second S_bcd | 640/1056 | Triple chain from section 1 |

The last output exceeds the end of a's fresh safe lap by `7/1056`.
Its four phases are

`(931/1056,509/1056,67/220,1/8)`.

The first exceeds 7/8, so the 22-step output is infeasible. This defeats the
actual composition, rather than only defeating a proposed bound used to prove
it. The ten-step triple selector remains correct in both calls.

The supplied closed window `W=[L,20/33]` is empty. This follows from an open
cover: the preceding c-bad interval, the preceding a-bad interval, the long
triple-bad component, and the next a-bad interval overlap successively and cover
every time from L until `299/352`. At `299/352` all four constraints are safe.
Thus `299/352` is the actual earliest joint safe time after L.

Merely testing `T<=R` after 22 operations would give a false positive on this
window. Checking final feasibility correctly reports the unsafe output as
inconclusive. An output past R remains an emptiness certificate because every
projection preserves the lower-bound property, even without a termination
guarantee.

## 3. Distinct speeds do not remove the auxiliary failure

Keep b,c,d and t0 unchanged. Set

`a=127/128`, `alpha_a=1/8-a*t0=12363/45056`,

`L=t0-1/(4a)=-17995/44704`.

This L still lies inside the same preceding c-bad interval, and the outputs of
the two triple calls remain `-199/528` and `20/33`. The new a-safe width is
`96/127`, less than `799/1056`. The final a-phase is
`118369/135168`, exceeding 7/8 by `97/135168`.
The earliest actual joint-safe time is `38325/44704`.
These are four distinct rational speeds, with arbitrary initial phases; this
section alone is not a common-start Lonely Runner configuration.

`structural_check.py` exactly checks both selected auxiliary cases. It imports
neither the primary selector nor saved results. This is the structural author's
own check of an algebraic derivation, not independent verification.

## 4. Coordinator follow-on: a single common-start lift

After the auxiliary construction was fixed, the coordinator proposed the
following algebraic conversion. It is a **new constructed physical example**,
separate from all frozen archived controls, not a speed scan or held-out test.

Let the four distinct speeds and phases from section 3 be v_i and alpha_i.
Choose

`M=lcm(phase denominators)=675840`, `P=M/3+1=225281`,

`tau=P/M`, `N=640*M*10^6=432537600000000`.

Since P is invertible modulo M, select

`r_i=(M*alpha_i)*P^(-1) mod M`, `U_i=N*v_i+r_i`.

Here N*v_i is an integer multiple of M. The residues are
`(185445,141440,390144,84480)`, and the resulting integer speeds are

`(429158400185445,432537600141440,519045120390144,713687040084480)`.

Their common-start phases at tau equal the four prescribed alpha_i exactly.
The scaled local speeds U_i/N differ from v_i by less than 1/(640*10^6).
The magnitude N was chosen once to protect strict margins; it was not tuned by
search. More importantly, the certificate below checks actual exact interval
inequalities, so no unverified perturbation estimate is needed for the claim.

The complete eight-runner configuration is `{0,1,4,5,U_1,U_2,U_3,U_4}`,
with all initial phases zero and selected reference zero. All speeds are
distinct, and the configuration has overall gcd one.
Set

`L=tau+(-1/8-alpha_a)/U_a`

` =1144427480494519/3433267201483560`,

`R=tau+(9/8-alpha_d)/U_d`

` =1903173888225289/5709496320675840`.

The 22-step output equals R. Its first residual phase is
`47618157730181/54376155435008`, which exceeds 7/8 by the positive amount
`39021724549/54376155435008`. The other three residuals are safe there.

The exact lifted bad intervals repeat the covering pattern of sections 1–3;
they cover the entire supplied closed window. The next first-runner projection
returns

`U=163489640070647/490466743069080`.

The cover proves no joint witness exists in `[L,U)`, and U is safe for every
moving runner. The core speeds 1,4,5 remain safe throughout `[L,U]`, verified by
single lifted-lap inequalities. Thus U is the actual earliest selected-reference
lonely moment after L. The 22-step counterexample is compatible with loneliness.

`common_start_lift_check.py` computes this one construction and checks both the
projection trace and the separate open-interval cover, using exact fractions
only. It does not enumerate the enormous number of prior laps.

## 5. Scope and next implication

The unconditional 22-step claim is **DISPROVEN** by these exact counterexamples,
including a common-start integer configuration. The conditional waiting-bound
argument is unaffected; its failed premise and the algorithm's actual failure
remain distinct findings. The failure also does not rule out a different
bounded projection order, a larger justified bound, or a phase-aware repair.

These examples need only one additional a projection, but that is a fact about
these constructed inputs. It is not evidence that 23 steps solve every case.
Any next repair needs a termination argument that controls chained blocking
occurrences, together with preservation of endpoint safety. The wider problem
of forcing a successful core-safe window remains separate.

Reproduction from the checkout root:

```bash
python -B reviews/2026-09-28-four-projection/structural_check.py
python -B reviews/2026-09-28-four-projection/common_start_lift_check.py
```

No hourly research restart, broad scan, all-reference campaign, paid compute,
outside outreach, main merge, or parked +7/+9 work was performed here.
