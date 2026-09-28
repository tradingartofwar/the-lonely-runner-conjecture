# Adversarial construction: repeated critical tilings are obstructed

September 28, 2026. Pinned baseline:
`5871f2b6c57552b5bd55fd4caa82d0c61307b10e`.

**Outcome:** no unbounded advancing-move or round family was constructed.
An attempted perturbation of the critical tiling with speed ratios
`1,1,2,2` instead yields a general no-double-repeat lemma. A local
perturbation of any exact periodic tiling also cannot strictly cover two
complete tiling periods plus margins. These statements are
**HYPOTHESIS / proof candidates**, materially derived with AI and internally
challenged by the affine, occurrence, geometry, and challenge agents. They
are not externally reviewed results or novelty claims.

All statements below allow auxiliary arbitrary phases and positive real
speeds. No additional physical configuration or broad parameter scan was
created. No proposed long chain was transferred to common-start integer
speeds, because no such family was obtained.

## 1. Notation and the attempted construction

For runner `i`, write `p_i=1/v_i` for its period. Its blocked occurrences
are open intervals of length `p_i/4`, and the right endpoints of successive
occurrences differ by `p_i`. Equality remains safe.

There is an exact critical tiling at periods `(1,1,1/2,1/2)`: within each
unit interval, take blocked tiles

```
a: (0,1/4)
c: (1/4,3/8)
d: (3/8,1/2)
b: (1/2,3/4)
c: (3/4,7/8)
d: (7/8,1)
```

and repeat by translation by 1. Explicit speeds and phases are
`v=(1,1,2,2)` and `alpha=(7/8,3/8,3/8,1/8)` for colors `(a,b,c,d)`.
This is an auxiliary shifted-phase tiling, not a common-start physical input. The open
tiles leave each contact as an equality witness. The tempting construction
is to perturb periods and phases so that the word `a,c,d,b,c,d` develops
strict overlaps and repeats for many cycles. The following lemma excludes
even two complete strictly overlapping copies with the same occurrence
translation pattern.

## 2. No-double-repeat lemma

Let `I_0,...,I_{2s}` be occurrences of at most four runners. Write their
left and right endpoints as `L_j,R_j`, and their runner colors as `i_j`.
Assume:

1. `R_0<R_1<...<R_{2s}`.
2. `R_j>L_{j+1}` for every `0<=j<2s`.
3. There are positive integers `h_i` such that, for `0<=j<=s`,
   `i_{s+j}=i_j` and `R_{s+j}=R_j+c_{i_j}`, where `c_i=h_i p_i`.

Thus there are two complete copies of a closed color word, and the final
anchor occurrence `I_{2s}` is present. Each runner uses the same occurrence
label translation between the copies. Internal skipped occurrence labels
are allowed.

**Claim:** these three assumptions are inconsistent.

Let `r=i_0=i_s=i_{2s}`. For each used color, let `n_i` be its number of
occurrences among destinations `I_1,...,I_s`. Strictly increasing right
endpoints imply strictly increasing occurrence labels within each color.
The first occurrence of the next copy comes after the last occurrence of
the previous copy, so `h_i>=n_i`. Define

`g_j=R_j-L_{j+1}` for `0<=j<s`.

Since `L_{j+1}=R_{j+1}-p_{i_{j+1}}/4`, telescoping gives

`S := sum_j g_j = (1/4) sum_i n_i p_i - c_r`.

Consequently,

`S <= (1/4) sum_i c_i - c_r <= max_i c_i - c_r`,

because at most four colors occur. The corresponding overlap in the
second copy is

`g_{s+j}=g_j+c_{i_j}-c_{i_{j+1}}`.

Strict positivity in both copies therefore requires

`g_j > max(0,c_{i_{j+1}}-c_{i_j})`.

Summing these inequalities, the total positive variation of `c` around
the closed word is at least the rise from its anchor value `c_r` to its
largest value. Thus

`S > sum_j max(0,c_{i_{j+1}}-c_{i_j}) >= max_i c_i-c_r`,

contradicting the preceding upper bound. This includes the constant-`c`
case: it would require `S>0` and `S<=0` simultaneously.

The lemma concerns any such strict increasing-endpoint chain. It does not
assume or prove that the chain is the actual selector itinerary. Conversely,
an arbitrary long color word need not contain this exact translated
double block, so the lemma alone is not a universal iteration bound.

## 3. A simpler local obstruction near a periodic tiling

The occurrence and geometry agents supplied a shorter argument for the
specific compactness application. It is recorded here to keep the
construction obstruction and its required local premise explicit.

Suppose a limiting occurrence family exactly tiles the real line: interiors
of different tiles are disjoint, their closed intervals cover the line,
and contacts occur only between the two adjacent tiles. Suppose its common
period is `P`. Runner `i` contributes `q_i=P/p_i` tiles per period, where
`q_i` is a positive integer.

Perturb its positive periods and phases slightly, to periods `p_i'`.
Keep the occurrence indices from the limiting tiling, and put

`c_i=q_i p_i'`.

Choose a runner `r` maximizing `c_i`. Start at one of its limiting tiles,
and follow all consecutive limiting tiles through its translate by `P`.
This cycle has exactly `q_i` destination tiles of runner `i`. Its perturbed
right-endpoint displacement is `c_r`. If every adjacent pair in that
cycle strictly overlapped after perturbation, telescoping would give

`0 < sum_adjacent (R_left'-L_right')`

`  = (1/4) sum_i q_i p_i' - q_r p_r'`

`  = (1/4) sum_i c_i - max_i c_i <= 0`,

a contradiction. Two periods of the limiting tiling, with small outer
margins, contain such a complete cycle regardless of which runner
maximizes `c_i` after perturbation.

This weighted maximum argument requires all the neighboring inequalities
in that cycle. An arbitrary chosen subchain can skip tiles, so this premise
must be obtained from an actual open cover of the whole segment, as below.

### Why a nearby open cover forces those adjacent overlaps

Fix the finite collection of limiting contacts in two periods. At any one
contact `x`, exactly two tiles have `x` in their closure. A third tile
would have positive interior length immediately to the left or right of
`x`, creating overlap with one of those two tiles. Because every period
is positive and only finitely many runners occur, the endpoint families
are locally finite.

Choose a small closed neighborhood of `x` that meets no other limiting
occurrence and lies inside the segment under consideration. Under
sufficiently small changes of periods and phases, only these same two
occurrences can meet a still smaller neighborhood; their relevant endpoints
remain inside it. There are only finitely many contacts, so one parameter
neighborhood can satisfy all these conditions.

If the perturbed left tile has `R_left'<=L_right'`, a point between these
two endpoints is uncovered. If they are equal, that common point is
uncovered because all blocking intervals are open. Therefore an open cover
of the entire smaller neighborhood forces `R_left'>L_right'`.

Applying this at every contact supplies all the strict inequalities needed
by the maximum-displacement contradiction. Right-endpoint order also
persists, because the limiting right endpoints are distinct and this is a
finite collection. The perturbation need not have a common period: only
the limiting occurrence-label translations `q_i` are used.

This proves a **local exclusion**: each exact periodic tiling has a
neighborhood of its speed/phase parameters in which an open covered segment
cannot include the selected two-period segment with margins. It does not,
by itself, supply a numerical uniform bound across all speed ratios.

## 4. Periodicity of an exact tiling need not use a classification

If two positive-speed occurrence families have incommensurable periods,
their meeting-center differences

`m p_i - n p_j + constant`,

with integer labels, are dense in the real line. A difference of absolute
value less than `(p_i+p_j)/8` makes their blocked intervals overlap
strictly. Thus an exact multiplicity-one tiling has rational period ratios
for every pair of runners. With finitely many runners there is then a
common period `P` that is an integer multiple of every `p_i`.

If tiling has initially been established only on a forward half-line,
the same incompatibility holds there: for an irrational period ratio,
positive-label multiples have dense residues, and the overlapping pair can
be chosen arbitrarily far forward. A common period therefore exists, and
one may choose the finite two-period test segment sufficiently far inside
that half-line.

This supplies the periodicity needed in Section 3 without relying on a
complete classification of critical tiling ratios. It still needs a
separate argument that a proposed long-chain limit really is a
multiplicity-one tiling.

## 5. Necessary structure of many actual selector rounds

For the specified repeated round

`a,b,c,d,c,d,b,c,d,c,d`,

the first call is `P_a` and the remaining ten calls form the prior exact
triple selector for `b,c,d`. Hence an unsafe round-end time can be blocked
only by `a`.

After a moving `P_a` lands at the right endpoint `R_{a,m}` of occurrence
`m`, the triple selector advances by less than

`W3=1/(4b)+1/(2c)+1/d <= 7/(4a)`.

The left endpoint of occurrence `m+2` is exactly

`R_{a,m}+7/(4a)`.

It follows that, if the next round is still necessary, the next moving
`P_a` visits occurrence `m+1`. It cannot skip an `a` occurrence. Thus many
continued rounds would require strict continuous blocking across many
consecutive `a` periods. This observation uses the prior triple-selector
waiting bound and applies after the first moving `P_a`; a stationary
initial `P_a` requires the usual separate first-round bookkeeping.

For a geometric obstruction away from bounded ratios, if `d>3a`, every
whole `a`-blocked interval must have positive overlap with a `d`-blocked
interval: its length `1/(4a)` exceeds the largest `d`-safe gap `3/(4d)`.
A uniform quantitative estimate requires a fixed margin such as `d>=4a`;
the qualitative statement alone degenerates when `d` decreases to `3a`.
The geometry agent handles that estimate separately.

## 6. What has and has not been established here

- The attempted near-critical repeated-word construction fails for an
  explicit, exact inequality reason, not because a finite search missed it.
- A local strict-cover obstruction applies to every exact periodic tiling,
  including tilings with unequal speeds.
- The obstruction is about continuous open coverage. An actual continuing
  projection trace supplies such a cover, but a generic covering family
  need not be its selected trace.
- No example here forces more advances than the archived seven-move
  counterexample, and that counterexample is not challenged.
- A full speed-independent bound still needs the coordinator's separate
  compactness/limit and large-ratio arguments. Even if those arguments
  establish a finite bound, these local lemmas give no numerical value.
- No literature or novelty claim was investigated, and no external
  correctness review is represented by the internal crosschecks.

No executable experiment was needed for these symbolic inequalities.
