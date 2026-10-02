# Structural challenge: long chains remain unresolved

September 28, 2026. Baseline `dd5b3bce9a7a3fb22474a724161438f24e35fb41`.
Material AI involvement: a separately tasked structural challenger derived the
arguments below after reading the preceding four-runner counterexample. No
parameter scan or additional physical control was run. This is internal
mathematical challenge, not external review or a literature novelty claim.

**Outcome:** no parameterized counterexample to every uniform iteration bound
was established in this round. The existing 22-step failure therefore remains
evidence against that specific composition only. The failed construction idea
and a common-start transfer argument are preserved below. The unbounded
statements with supplied arguments are **HYPOTHESIS / proof candidates** pending
review.

## 1. Why simply repeating four nearly equal intervals fails

At threshold `delta=1/8`, runner v has open blocked intervals of width
`1/(4v)` and period `1/v`. Order four positive speeds
`a<=b<=c<=d`.

A proposed chain that advances through one whole a period using exactly one
blocked occurrence of each runner has total interval length

`(1/a+1/b+1/c+1/d)/4 <= 1/a`.

It cannot cover a full a period by a connected chain with strict overlaps:
strict overlaps make the union strictly shorter than the sum of interval
lengths. Equivalently, to connect consecutive a-blocked occurrences, the
intervening closed a-safe lap has width `3/(4a)`. One occurrence apiece of
b,c,d has total length at most that width and cannot cover the lap by a
strictly connected open chain. Some residual runner must contribute another
occurrence.

This rules out a tempting construction that perturbs a quarter-period tiling
and repeats the same four-interval pattern. It does not rule out more
complicated changes of lap labels. The archived counterexample already uses
the required extra occurrence: its local triple chain has order d,b,c,d.

The overlap-budget argument derived separately in this round gives another
necessary consideration: a long chain must fit many positive overlaps into
a bounded excess-coverage budget. Tiny overlaps are arithmetically possible
when the speed denominators grow. That observation neither supplies a chain
nor proves that chains of arbitrary length are possible.

## 2. Finite robust rational chains admit a common-start lift

Common-start constraints are an essential physical condition. A finite
auxiliary construction with arbitrary phases must not be silently called a
Lonely Runner input. Nevertheless, the preceding numerical lift has a general
form that can be supplied analytically.

Assume four **distinct positive rational** auxiliary speeds `v_i`, rational
phases `alpha_i` in `[0,1)`, and a finite local endpoint certificate. Selected
bad-interval endpoints have the form

`e=(k +/- 1/8-alpha_i)/v_i`.

Assume the certificate is expressed through strict inequalities between
distinct selected endpoints: for example strict consecutive overlaps in a
finite chain, or strict containment of an endpoint of one runner in another
runner's bad interval. Necessary identities involving the same endpoint are
retained as identities. Cross-runner endpoint ties are excluded from this
robust version; an isolated equality witness needs a separate argument.

Choose constants:

- `D_alpha`: a common multiple of the phase denominators;
- `D_v`: a common multiple of the speed denominators;
- `M=72*D_alpha`, `P=M/3+1`, and `tau=P/M`;
- `v_min=min_i v_i` and `Delta=min_{i!=j}|v_i-v_j|>0`;
- `T>=1` bounding the absolute values of the selected endpoints;
- `mu>0` no greater than the distance between any two distinct selected
  endpoint coordinates used in the certificate.

Then `gcd(P,M)=1`: writing `M=72*D_alpha`, any common divisor of
`24*D_alpha+1` and `72*D_alpha` divides 3, while the former is 1 modulo 3.
For each runner set

`r_i=(M*alpha_i)*P^(-1) mod M`, with `0<=r_i<M`.

Choose N to be a positive integer multiple of `M*D_v`, strictly exceeding

`max(4*T*M/(v_min*mu), M/Delta, 36*T, 5/v_min)`.

Define the integer physical speeds `U_i=N*v_i+r_i`. They are distinct,
positive, larger than 5, and have the same order as the auxiliary speeds.
All eight runners in

`{0,1,4,5,U_1,U_2,U_3,U_4}`

therefore have distinct integer speeds and start together. Because
`N*v_i` is an integer multiple of M,

`{U_i*tau}=alpha_i`.

At physical time `t=tau+u/N`, the four residual phase functions are exactly

`alpha_i+w_i*u mod 1`, where `w_i=U_i/N=v_i+r_i/N`.

The endpoint corresponding to e becomes

`e'=e*v_i/w_i`

in the local coordinate u. Hence

`|e'-e| <= T*M/(N*v_min) < mu/4`.

Every strict endpoint ordering in the finite certificate is preserved.
Every selected interval keeps its runner and integer occurrence label. Thus
strict covering chains and strict containment failures survive the lift.
If a proposed projection trace is determined by these strict endpoint
comparisons, its occurrence itinerary survives as well. This last statement
does not excuse checking that the finite certificate actually contains every
comparison needed by the trace.

The old core-safe interval is `J=[9/32,3/8]`. The selected anchor tau lies
at distance at least `1/36` from both ends of J. The condition `N>36*T`
therefore keeps the whole selected local interval inside J. The three core
speeds 1,4,5 are strictly safe in its interior, so they do not spoil the
lifted residual obstruction.

This is an existence construction for a finite robust certificate, with an
explicit sufficient scale. It is not a new computed physical case. It is
also not a proof that a desired long auxiliary chain exists. If a future
rational construction supplies a strict chain for every parameter value,
the formula can be applied separately at each value to obtain one full
common-start integer configuration for that value. The required scale may
grow with the parameter.

## 3. Boundaries of the negative conclusion

- No unbounded family of iteration failures has been established here.
- The preceding 22-step counterexample is preserved and remains valid.
- A speed-dependent finite bound does not decide whether a speed-independent
  bound exists.
- Growing speed magnitudes or tiny overlap lengths do not themselves imply
  that many iterations are necessary.
- A phase-shifted auxiliary chain is not automatically a physical input; the
  finite robust lift explains precisely when this conversion is available.
- Strict-overlap preservation does not preserve arbitrary equality ties.
  Endpoint equality still counts as safety and requires its own check.

The next useful obstruction attempt needs an explicit sequence of occurrence
labels and strict endpoint inequalities that remain compatible as its length
increases. Merely shrinking existing overlaps, enlarging all speeds, or
repeating the archived seven-interval chain does not provide that result.
