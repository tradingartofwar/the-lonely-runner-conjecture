# Fastest-runner conditioning and common-lap certificates

September 28, 2026. Scope: the six configurations fixed in `protocol.json`,
selected reference 0, eight common-start runners, threshold 1/8. AI materially
contributed the calculations and argument review. No extra speed configuration,
all-reference scan, literature review, publication, or novelty claim is made.

The useful geometric finding is a supplied **HYPOTHESIS / proof candidate**:
conditioning on safety of a fastest runner makes every remaining blocking set
an interval on each complete core-safe component. The optimal tree bound is
then exact. This would establish the experiment's *conditional certificate
selection* hypothesis; it does not establish that any lonely time exists.
The argument below received an internal mathematical attack/review, which is
not independent human review or promotion to an established result.

## Review of the fastest-runner argument

Write the relative speeds from the chosen reference as `r_i`, and put
`u_i=|r_i|`, `V=max_i u_i>0`. Using absolute values preserves every circular
distance. Equal absolute speeds retain their original labels and do not alter
the argument. Keep the original runner count and threshold `h=1/n`; removing
a condition locally does not change h. For the six cases, h=1/8.

Choose any nonempty core containing a runner of absolute speed V. The core
can consist of that runner alone. Let W be a complete closed connected
component of the core-safe set on the real interval [0,1]. Each such W lies
within one fastest-runner safe lap,

\[
[(m+h)/V,(m+1-h)/V],\qquad |W|\le(1-2h)/V.
\]

For a residual speed u>0, successive strict blocking intervals

\[
((j-h)/u,(j+h)/u)
\]

are separated by a closed safe gap of length `(1-2h)/u`. Since u<=V, that gap
is at least |W|. If W met two strict blocking intervals nontrivially, two
points of W in those intervals would be separated by **strictly more** than
the intervening safe-gap length. This contradicts the bound on |W|. Therefore
`B_u intersect W` is empty or a single interval, with its actual endpoint
flags retained. A zero relative speed, if allowed in an extension with repeated
original velocities, simply blocks all of W and is also an interval.

The strictness matters at equality: when |W| equals the safe gap, the two gap
endpoints are safe, so they do not supply two blocking pieces. The correct
constant at h=1/8 is **6/(8V)=3/(4V)** for the fastest safe-lap width and
**6/(8u)** for the residual safe gap. The initially suggested 7/(8u) constant
would be incorrect. Components are lifted to [0,1], so no circular wrap is
silently treated as one interval. Singleton W has zero duration and causes
no measure exception.

## Why an interval family has an exact tree certificate

For nonempty residual intervals `I_1,...,I_s`, order their left endpoints
nondecreasingly. For each j>1, attach j to a preceding interval p(j) whose
right endpoint is greatest. These edges form a tree because each parent
precedes its child.

Apart from possible endpoint membership differences of measure zero,

\[
I_j\cap\bigcup_{i<j}I_i=I_j\cap I_{p(j)}.
\]

Indeed, if the greatest preceding right endpoint is left of the new left
endpoint, both sides have zero length. Otherwise its interval starts no later
than the new interval, and covers precisely the portion of the new interval
that any preceding interval can cover. Summing union increments gives

\[
\left|\bigcup_{j=1}^s I_j\right|
=\sum_j|I_j|-\sum_{j>1}|I_j\cap I_{p(j)}|.
\]

Empty blockers can be attached by arbitrary zero-weight edges. Zero or one
blocker uses the protocol's separate convention. Consequently this tree gives
exactly

\[
|W|-\sum_i D_i+\sum_{ij\in T}O_{ij}
=\left|W\setminus\bigcup_i B_i\right|.
\]

Every tree expression is a lower bound on the uncovered duration: for an
active set with a>0 vertices, its induced forest has at most a-1 edges. Thus
no tree exceeds the actual duration, and the constructed tree proves that
the **maximum** tree bound is exact. Containment reduction is not needed for
this construction; a union-preserving reduction still leaves an interval
family and is exact as well.

This proof concerns duration. It does not equate an endpoint-insensitive
measure certificate with the complete allowed set: an exact zero bound can
coexist with isolated safe times.

## Consequence and its limitation

If a strict lonely time exists, continuity supplies positive lonely duration
inside a core-safe component for any fixed core containing a fastest runner.
The preceding argument then supplies a positive optimal tree certificate on
that component. In the six-case protocol, 15 of the 35 three-runner cores
contain the fastest speed, so a configuration-level strict failure would also
contradict this supplied argument. More strongly, the same conditional argument
uses a one-runner fastest core and a tree on the n-2 residual labels.

This is a proposed completeness result for a representation and selection
procedure. Exactness says that an opening, **if present**, can be certified
with these local pair durations. It gives no independent reason why one of
those exact values must be positive. The potentially many fastest safe laps
and their moment calculations remain; no speed-independent search bound or
runtime improvement has been established.

There is a separate endpoint observation. In a finite integer-speed instance,
an allowed isolated time has at least one constraint at threshold; otherwise
continuity would make it strict. A core containing that threshold runner has
the same time as one of its complete component endpoints, because the runner's
own safe lap ends or begins there. A fastest runner can also be placed in this
core. Thus the protocol's all-core endpoint fallback would find an equality-only
solution if one exists. This is another supplied elementary argument, not an
assertion that an equality point must exist. It does not change the distinction
between zero duration and no solution.

## Exact integer-lap encoding of the selected openings

For these positive integer speeds, fixing one lap m_i for each runner gives
the closed joint safe cell

\[
C(m)=\left[\max_i\frac{8m_i+1}{8v_i},
             \min_i\frac{8m_i+7}{8v_i}\right]\cap[0,1].
\]

It is feasible exactly when the maximum left endpoint does not exceed the
minimum right endpoint. It has strict interior exactly when the inequality is
strict. The same lap must work throughout the entire interval: circular
endpoint distances alone do not encode that condition.

Eliminating t gives a relation-only integer formulation for this fixed lap
vector:

\[
v_j(8m_i+1)\le v_i(8m_j+7)\qquad\text{for every }i,j.
\]

These 49 inequalities are equivalent to nonempty common-lap intersection; all
49 being strict is equivalent to positive length. `lattice.json` records the
integer matrix `S_ij=v_i(8m_j+7)-v_j(8m_i+1)` for each cell. It is a compact
way to check pairwise lap alignment without solving for a witness time. The
integers m_i are indispensable input, so this is not a conclusion from pair
durations or from a qualitative containment map.

More generally, any integer relation `w dot v=0` forces
`w dot (vt-m)=-w dot m` for the lifted phases. Such phase relations are valid,
but no claim that a single relation or a small-support Boolean-state summary
excludes the tree's discarded states was established here. The investigation
turned to the stronger fastest-core interval geometry instead. The exact lap
matrix supplies feasibility constraints; it does not itself improve a moment
bound or explain why a feasible lap vector must exist.

For an archived witness `t=a/b` in lowest terms, the checker records the
fourteen integer slacks

\[
L_i=8v_i a-b(8m_i+1),\qquad
R_i=b(8m_i+7)-8v_i a.
\]

All are nonnegative at a valid witness; all are positive at a strict witness.
For each surviving interval it separately checks the lower inequality at its
left endpoint and the upper inequality at its right endpoint, retaining a
single common lap. It also checks that taking max-left and min-right recovers
the complete archived interval exactly, and compares it with the global
allowed-component archive.

`lattice_check.py` imports no project code. It reads only the frozen protocol
and primary result archive, recomputes all lap bounds using `Fraction`, checks
the supplied witness distances directly, and writes `lattice.json` with source
hashes. These certificates are an equivalent exact encoding of the selected
openings, not a stronger lower bound or an unbounded lattice feasibility claim.

All **12 witnesses** (six selected and six global) have fourteen positive
integer slacks. All **20 selected surviving intervals** are recovered exactly
as common-lap cells and agree with components in the global archive. These are
**OBSERVED** exact certificate checks for the prescribed six inputs. They
directly certify each listed cell, rather than independently re-enumerating
the completeness of the entire global allowed set.

The lap-vector order is the seven positive speeds in protocol order. The
listed cell is the one containing the selected witness; some selected windows
contain several such cells.

| Case | Selected witness | Common lap vector | Witness cell | Cells in selected window |
| --- | --- | --- | --- | ---: |
| prime_mix | 1917/12728 | (1,1,2,3,4,5,6) | [49/344,47/296] | 2 |
| near_pairs | 11/840 | (0,0,0,0,0,0,0) | [1/120,1/56] | 4 |
| fibonacci | 19705/48416 | (3,5,8,13,22,36,58) | [289/712,111/272] | 4 |
| squares | 57/338 | (1,1,4,8,13,20,28) | [225/1352,231/1352] | 5 |
| prime_powers | 691/1500 | (7,11,12,22,29,37,57) | [11/24,463/1000] | 3 |
| perturbed_chain | 2527/11224 | (1,1,3,5,8,13,22) | [41/184,111/488] | 2 |

For a small fully explicit witness certificate, near_pairs has a=11, b=840
and every lap zero. In positive-speed order `(15,16,17,31,33,47,49)`, its lower
integer slacks are `(480,568,656,1888,2064,3296,3472)` and its upper integer
slacks are `(4560,4472,4384,3152,2976,1744,1568)`. Positivity certifies all seven
strict safety inequalities. Max-left/min-right gives `[1/120,1/56]`, with
width 1/105; the minimum circular distance at its midpoint is 11/56.

The selected witness uses the widest cell in its selected window. The global
witness uses a widest cell in the complete global allowed set, so these are
different optimizations. They agree in four cases. For fibonacci, the global
cell is `[121/712,199/1152]` of width 287/102528, whereas the selected witness
cell has width 53/24208. For perturbed_chain, the global cell is
`[361/800,223/488]` of width 279/48800, whereas the selected witness cell has
width 13/2806. Both distinctions are retained in the archive.

None of the six Q-selected cores contains the fastest runner. This does not
contradict the fastest-core candidate: Q maximizes the lower bound over all
cores, and a larger window outside that class can have a larger bound, even
with slack. The selected tree is exact in prime_mix, near_pairs, and
perturbed_chain; the other three selected windows have positive tree slack.

Reproduce the exact certificate checks with:

```bash
python -B reviews/2026-09-27-team/lattice_check.py --check
```
