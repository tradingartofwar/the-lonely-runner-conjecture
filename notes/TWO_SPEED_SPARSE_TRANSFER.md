# Two variable speeds: lap constraints and a two-window selector

September 25, 2026. Baseline `249de490b2881622ee44c7191691e11f67771b8d`.

**Question:** Does the compact overlap model survive when two runners can share the blocking duty, and can it identify when a different window is necessary?

**Outcome:** the two-triple graph structure survives. The shared-clock tests become integer-point questions in a two-dimensional region of lap labels. Combining these with a prescribed choice between two windows gives a certificate for every admissible pair in the already-studied family

$$\{0,1,4,5,6,7,x,y\},\qquad 0<x<y,\quad x,y\in\mathbb Z\setminus\{1,4,5,6,7\}.$$

**Status:** exact finite checks are OBSERVED/REPRODUCED. The unbounded synthesis below is an AI-assisted proof candidate awaiting independent review. Eight total runners, common start, selected stationary reference 0, threshold `delta=1/8`. No novelty, other-reference, arbitrary-speed, or full Lonely Runner claim is made.

Existence for this family was already covered in [TWO_VARIABLE_SPEEDS.md](TWO_VARIABLE_SPEEDS.md). This continuation tests the LTCM/certificate mechanism, supplies an explicit two-window dispatch, and preserves its limits. It does not add a new family to the project's coverage.

## 1. Two different kinds of failed window

Keep three intervals distinct:

$$I=[17/56,5/16],\qquad J=[9/32,3/8],\qquad H=[25/56,15/32].$$

I is the small opening from the earlier one-variable study. J is the larger window used by the recent sparse graph. H is the alternate window already used by the earlier two-variable argument.

The known pair `(16,23)` closes I completely, including its endpoints. But it does **not** close J. In J its complete allowed interval is

$$[17/48,47/128],\qquad\text{length }5/384.$$

The sparse graph detects that full duration. The entire H also survives, with length `5/224`. Thus closing the earlier small opening does not itself force us out of the current larger window.

A genuine empty-window family is `(x,y)=(3,8m)`, m>=1. With speeds `{1,4,5,6,7,3}`, the only valid time in J is `3/8`. Speed `8m` collides there. Hence J is empty for every member of this infinite family, regardless of how much information the certificate retains. H handles it, as shown below. This separates a weak certificate from the absence of a witness in the chosen window.

For a direct check, the five fixed runners are clear in J exactly on `I union [17/48,3/8]`. On I, runner 3's phase ranges from `51/56` to `15/16`, entirely within the blocked zone. On the second interval its phase ranges from `1/16` to `1/8`, reaching safety only at the last endpoint. Multiplication by `8m` sends that endpoint to the integer `3m`.

## 2. The shared-clock constraint as a lap lattice

On J, the fixed blockers 6 and 7 have disjoint intervals

$$I_6=(5/16,17/48),\qquad I_7=[9/32,17/56).$$

The only possible triple types are `{6,x,y}` and `{7,x,y}`. Four-way blocking cannot occur. Determining those two possibilities requires checking whether the x/y blockers overlap inside I_6 or I_7.

For a positive-length interval with endpoint values a,b, let m,n be the nearby meeting labels of runners x,y. A positive common blocking interval exists exactly when some integers m,n satisfy

$$xa-\delta<m<xb+\delta,\qquad ya-\delta<n<yb+\delta,$$
$$|ym-xn|<\delta(x+y).$$

The first two inequalities make each blocking interval meet `[a,b]` with positive length. The last makes the two blocking intervals overlap each other. Three single intervals with positive pair overlaps have positive common intersection: their greatest left endpoint is less than their smallest right endpoint. Thus the conditions are sufficient as well as necessary for positive duration.

This is an explicit local lattice model: integer points in a rectangle intersected with a narrow strip. It does not assume independent clocks; the strip expresses their common-time compatibility. It is not the full polyhedral Lonely Runner formulation from S10.

For each candidate m, the test reduces to finding an integer n strictly between

$$\max\left(ya-\delta,\frac{ym-\delta(x+y)}x\right)
\quad\text{and}\quad
\min\left(yb+\delta,\frac{ym+\delta(x+y)}x\right).$$

A floor operation finds the first possible n, without enumerating y's laps. For `(16,23)` on I_6, the only individual lap candidates are m=5,n=8. But `|23*5-16*8|=13>39/8`, so they cannot overlap. On I_7 runner 16 has no candidate meeting at all. Both triple tests therefore return false.

## 3. The graph still needs just two compatibility answers

Use edge order

`e0=(6,x), e1=(6,y), e2=(7,x), e3=(7,y), e4=(x,y)`.

Retain any subset of the five edges, except that a possible triple forbids retaining all three of its triangle edges. Every four-cycle requires both 6 and 7 active and is therefore harmless. As in [SPARSE_OVERLAP_SELECTION.md](SPARSE_OVERLAP_SELECTION.md), at most 32 masks select the largest valid pair weight.

There is also a direct expression for the optimum. Write the five edge weights as a,b,c,d,e in that order. The smallest necessary omitted weight is

| Triple possibilities | Omitted weight C |
| --- | --- |
| Neither | 0 |
| Only `{6,x,y}` | `min(a,b,e)` |
| Only `{7,x,y}` | `min(c,d,e)` |
| Both | `min(e, min(a,b)+min(c,d))` |

The selected graph gives

$$U_J\ge |J|-D_6-D_7-D_x-D_y+a+b+c+d+e-C.$$

Counting the possible active subsets supplies the same forest inequality as before. The code checks the direct expression against all admissible masks and verifies the pointwise counting bound.

If T_6,T_7 are the actual triple durations, full inclusion-exclusion gives the exact duration by replacing C with `T_6+T_7`. Consequently the bound's deficit is exactly `C-T_6-T_7`. The two yes/no answers can certify an opening without recovering its whole duration.

## 4. Compact data can still cost more to obtain

For the periodic primitive A from SPARSE_OVERLAP_SELECTION.md,

$$D_v([a,b])=\frac{A(vb)-A(va)}v.$$

The only new pair duration is O_xy. Compute it by summing D_y over the separate x-blocking intervals in J. The number of such intervals grows with x; unrestricted two-variable evaluation is therefore **not** automatically constant-cost merely because the output contains two bits.

The following window rule restores a bounded number of arithmetic operations for this specific family:

| Smaller speed x | Window and certificate |
| --- | --- |
| `x>=34` | H; use the already-established individual-duration bound |
| `x=3` | H; only runner y remains to be handled |
| Otherwise | J; use the sparse graph, retaining `t=3/8` for four finite equality cases |

In the last branch x<=33. There are at most four x-blocking occurrences in J, at most two in I_6, and at most one in I_7. The y-laps are never enumerated. Rational/integer bit costs still grow with the size of the speeds.

## 5. Why the H branches work

All five fixed runners are safe on H. Its length is `5/224`. The existing periodic discrepancy estimate gives

$$U_H\ge\frac5{448}-\frac3{16}\left(\frac1x+\frac1y\right)
\ge\frac1{7616}>0\quad(x,y\ge34).$$

This is the earlier two-variable fast bound, not a newly discovered estimate.

Runner 3 is also safe throughout H: its phase ranges from `19/56` to `13/32`. For x=3, only y can block it, so

$$U_H\ge\frac{15}{896}-\frac3{16y}>0\quad(y\ge12).$$

The only smaller admissible y are 8,9,10,11. Direct periodic integration gives respectively `5/224,1/96,5/224,1/352`, all positive. These four exact controls complete the x=3 branch. They include the genuine empty-J family `(3,8m)`.

## 6. A finite reduction for the sparse J branch

For each of the 27 remaining possible x<34, choose a fixed conservative graph G_x: whenever `O_6x>0`, break the 6/x/y triangle for every y; likewise for `O_7x>0`. This graph is valid even when the actual triple tests would permit more edges.

Let k_x count the x-blocking occurrences in J. Then

$$O_{xy}=D_x/4+\epsilon_{xy},\quad |\epsilon_{xy}|\le\frac{3k_x}{16y}.$$

The other y-dependent terms obey the one-interval estimate `3/(16y)`. Therefore the fixed graph has an explicit bound

$$U_J\ge L_x-C_x/y.$$

Its limit L_x is obtained by replacing `D_y(J)` with `|J|/4`, `O_6y` with `D_6/4`, `O_7y` with `D_7/4`, and `O_xy` with `D_x/4`. Its error coefficient is

$$C_x=\frac3{16}\left(1+\mathbf1_{e1\in G_x}+\mathbf1_{e3\in G_x}
+k_x\mathbf1_{e4\in G_x}\right).$$

All selected L_x are positive. Put `Y_x=floor(C_x/L_x)+1`; every y>=Y_x has positive slack. The table records all constants. The mask is `sum(2^i for retained e_i)` using the edge order in Section 3.

| x | L_x | C_x | Y_x | Mask |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 15/896 | 3/8 | 23 | 2 |
| 8 | 19/1792 | 3/4 | 71 | 26 |
| 9 | 15/896 | 3/8 | 23 | 3 |
| 10 | 9/640 | 9/16 | 41 | 22 |
| 11 | 31/9856 | 15/16 | 299 | 26 |
| 12 | 15/896 | 3/8 | 23 | 3 |
| 13 | 3/224 | 9/16 | 43 | 15 |
| 14 | 1/96 | 9/16 | 55 | 15 |
| 15 | 15/896 | 3/8 | 23 | 3 |
| 16 | 3/448 | 9/16 | 85 | 11 |
| 17 | 185/11424 | 9/16 | 35 | 15 |
| 18 | 15/896 | 3/8 | 23 | 7 |
| 19 | 25/4256 | 9/16 | 96 | 11 |
| 20 | 23/1920 | 3/8 | 32 | 7 |
| 21 | 15/896 | 3/8 | 23 | 7 |
| 22 | 27/2464 | 9/16 | 52 | 11 |
| 23 | 83/5152 | 9/16 | 35 | 15 |
| 24 | 23/1344 | 9/16 | 33 | 15 |
| 25 | 69/5600 | 9/16 | 46 | 15 |
| 26 | 3/224 | 9/16 | 43 | 15 |
| 27 | 79/6048 | 9/16 | 44 | 15 |
| 28 | 5/336 | 9/16 | 38 | 15 |
| 29 | 103/6496 | 9/16 | 36 | 11 |
| 30 | 3/224 | 9/16 | 43 | 15 |
| 31 | 367/20832 | 9/16 | 32 | 15 |
| 32 | 13/896 | 9/16 | 39 | 15 |
| 33 | 85/7392 | 9/16 | 49 | 15 |

For `x<y<Y_x`, excluding fixed speeds, exactly 819 pairs remain. Exact checks give 815 positive graph bounds. The four zero cases are `(2,3),(10,11),(11,13),(11,26)`; each retains `t=3/8`. The two cases `(10,11)` and `(11,26)` additionally retain `t=5/16` in J. No positive-duration claim is substituted for these contacts.

The selected adaptive graph is at least as strong as each fixed G_x. The analytic tails, finite remainder, and H branches therefore cover every pair under the stated integer/fixed-core assumptions. The table and written error bounds, not a guessed cutoff, justify exhaustiveness.

## 7. Verification and what remains open

```bash
python -B reviews/2026-09-25-lr2/check_two_speed_transfer.py --check
```

[Script](../reviews/2026-09-25-lr2/check_two_speed_transfer.py) and [exact results](../reviews/2026-09-25-lr2/two_speed_transfer.json). Standard-library rational arithmetic; no project imports. The archive includes the script hash, every reduced finite row, all 27 tail profiles, graph/lattice controls, and large-speed formula checks. Direct time partitions separately verify finite pair integrals, both triple tests, and clear durations. Large formula examples do not enumerate a complete schedule.

An additional session check used the existing safe-interval checker on `(2,3),(10,11),(11,13),(11,26),(3,8),(16,23),(19,95)`. It confirmed the equality, empty-J, cooperative, and near-cutoff controls. All 27 constants in the written table were compared with the archived exact results.

A separate diagnostic box `x<y<=80`, excluding the five fixed speeds, contains 2,775 pairs. Of these, 2,698 have positive duration in J and every one receives a positive sparse certificate; 67 have only valid isolated times; ten have empty J, exactly `(3,8m)` for m=1..10. The earlier box through 32 is contained in this box and is not an additional replication. The archive preserves the diagnostic domain, exception lists, and a digest of all regenerated rows. This box overlaps the reduced finite cases and is not the justification of the unbounded result.

The investigation distinguishes three matters: information retained by a model, work required to obtain that information, and whether the chosen window contains a solution. Refining the first cannot repair a genuinely empty window. Here arithmetic supplies both a compact model and a justified window choice, with all fixed-core assumptions visible.

The restriction still matters: disjointness of the two fixed blocker sets and a five-runner-safe alternate window supply the structure. The earlier affine/four-fast-runner work addresses settings where a coarse sum of four quarter-duty blockers has no positive leading term. **Next useful test:** compare these sparse compatibility checks with the already-preserved four-blocker examples, especially `{56,113,64,72}` on J, and identify which disjointness or triple exclusions survive. Do not restart already-covered one- or two-variable existence arguments as new results. General selection for arbitrary speed configurations remains OPEN.

**Continuation completed:** [Four-blocker cycle corrections](FOUR_BLOCKER_CYCLE_CORRECTIONS.md) compares eight existing inputs. Positive four-way overlap makes the uncorrected active-forest method revert to trees, but subtracting one selected cycle-intersection duration improves seven of eight tree bounds. The 113 case retains a lap-derived triple exclusion; the 112 case requires a quantitative four-way correction. Computing these moments still uses speed-dependent interval lists, so this does not inherit the bounded occurrence count proved above.
