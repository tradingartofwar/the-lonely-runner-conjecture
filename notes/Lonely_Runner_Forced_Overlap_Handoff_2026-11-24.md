# Lonely Runner handoff — forced overlap on candidate times

**November 24, 2026 · Research owner: Lonely Runner · Status: OPEN.**  
**Resume here.** If the other runners blocked every possible lonely moment, what would they have to do *at the same physical times*? Test whether the speed relations force them to duplicate so much blocking on a suitable finite grid that at least one time must survive. An uncovered grid point gives a rational witness, even when it is the only safe instant in its neighborhood.

This continues the November 21 project review's question about simultaneous failure on all pair-sum grids. The proposed change is to count forced duplication *on those grids*. The first counting rule below succeeds on a previously problematic example. A second example defeats it on every grid, and shows exactly what information it discarded. The general conjecture and the choice of a useful grid from the speeds remain open.

## Why take this direction?

In his Riemann hypothesis announcement, Levent Alpöge describes looking for something that could do the job multiplicity had done in a simpler setting. The transferable question is “What does one hypothetical exception force us to count more than once?” Here the object counted twice is a blocked numerator on a clock shared by all the runners. All the arithmetic below stands on its own. [Alpöge’s account, first page](https://alpo.ge/remark.pdf)

Three pieces of the project's existing work narrow the assignment.

- **September, blocking windows.** If $M(t)$ is the number of blockers and $U$ the duration with none, then, at the conjectured threshold, $\int_0^1(M(t)-1)_+\,dt=(n-2)/n+U$. This explains where redundant duration goes. A tight example with four isolated witnesses has $U=0$. Local overlap also has to beat local concentration. The doubled-speed study already obtained a restricted-family argument using this idea. Repeating the total duration calculation would miss the question of *which instant survives*. [Global overlap](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/c8a287f52ef0066d2ba6247094bdeba023825081/notes/BLOCKING_OVERLAPS.md) · [Local overlap](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/c8a287f52ef0066d2ba6247094bdeba023825081/notes/LOCAL_OVERLAP.md)
- **October, runner addition.** The center-selection study found a blocker for each of 1,199 components across twelve challenge cores. Different components can have different blockers. The new calculation must keep a common numerator for *all* speeds and allow the chosen grid to depend on the complete tuple. [October handoff](https://github.com/tradingartofwar/the-lonely-runner-conjecture/blob/35e426bb200f49fa742165b9e279b13d7524e0b6/notes/MISSION_CONTROL_HANDOFF_2026_10_17_CENTER_SELECTION.md)
- **November, where to search.** Section 4 of the project-folder file **Lonely_Runner_Proof_Review_2026-11-21.md** gives a complete family of pair-sum grids for a fixed tuple. Its shortest-relation filter misses viable grids, including for $(1,2,5,9)$. It asks whether pairs joining a speed inside a short relation to one outside it can help. Its bounds on a first counterexample remain candidates for review. The following experiment is independent of those bounds.

Overlap is an established approach. Perarnau and Serra studied correlations of blocking events. Hu and Jing's October 2026 preprint reports a uniform improvement on the elementary bound using interval multiplicities. Compare their continuous estimates with this discrete test before considering any novelty claim. Their $n$ counts moving speeds, our $n$ includes the reference. [Perarnau and Serra](https://doi.org/10.37236/5123) · [Hu and Jing, v1](https://arxiv.org/abs/2610.23790v1)

## The clock and the counting rule

Use the project's convention of $n$ total runners with a common start, one selected stationary reference, and $k=n-1$ moving constraints. For this experiment use $k\ge2$ distinct positive integer relative speeds $V$. Time is modulo one. Write $\|x\|$ for distance to the nearest integer. A runner blocks if $\|vt\|<1/n$. Equality is safe.

1. For distinct $u,v\in V$, take $d=u+v$. Its grid is $t=a/d$ for $a=0,\ldots,d-1$. Keep unreduced numerators, including those sharing a factor with $d$. Over the union of these grids a maximum of $\min_v\|vt\|$ is attained. Below $1/2$, a positive maximum needs active branches of opposite slope, so two phases are opposites and $(u+v)t$ is integral. At a maximum of $1/2$ all phases are half-integers, which gives the same conclusion. A particular grid may be completely blocked.
2. Replace each speed on this grid by $c=\min(v\bmod d,(-v)\bmod d)$. Speeds in the same class have identical distance to the reference at **every** numerator. In particular the two speeds that generated $d$ always collapse to one class. Keep the class-to-speed labels for reconstructing a witness. A zero class blocks every numerator.
3. For each distinct class $c$ let $g=\gcd(c,d)$ and $h=d/g$. Its number of blocked numerators is
   $$b_c=g\bigl(2\lceil h/n\rceil-1\bigr).$$
   Multiplication by $c$ visits each residue on a reduced grid of size $h$ exactly $g$ times. On that grid the blocking residues have distance strictly less than $h/n$ from zero, in numerator units. The ceiling keeps exact threshold contacts safe.
4. All classes block numerator zero. Let $C$ be the set of classes. Their union can cover at most $1+\sum_{c\in C}(b_c-1)$ distinct numerators. Thus the following integer is a **lower bound on the number of safe times on this grid**:
   $$L_0(d)=\max\left(0,\ d-1-\sum_{c\in C}(b_c-1)\right).$$
   A positive value proves existence on that grid before constructing its safe set. Zero leaves the grid undecided. This elementary bound counts each class once and credits only one shared numerator. The complete grid scan is the comparison for testing what it loses.

## Exact controls already checked

Each row fixes the indicated reference. The last column lists *all* safe numerators on that grid. Each list was independently cross-checked against the repository's closed-interval calculation by a second procedure using exact fractions. Both procedures were run by the same AI collaborator.

| Moving speeds | $n$ | $d$ | Counts $b_c$ in increasing class order | $L_0$ | Safe numerators |
|---|---:|---:|---|---:|---|
| $1,2$ | 3 | 3 | 1 | 2 | 1, 2 |
| $1,2,5,9$ | 5 | 3 | 3, 1 | 0 | none |
| $1,2,5,9$ | 5 | 10 | 3, 2, 5 | 2 | 3, 7 |
| $1,4,5,6,7,11,13$ | 8 | 8 | 1, 2, 1, 4 | 3 | 1, 3, 5, 7 |
| $1,4,5,6,7,11,13$ | 8 | 24 | 5, 4, 5, 6, 5, 5 | 0 | 3, 9, 15, 21 |
| $1,3,12$ | 4 | 4 | 4, 1 | 0 | none |
| $1,3,12$ | 4 | 13 | 7, 7 | 0 | 6, 7 |
| $1,3,12$ | 4 | 15 | 7, 9 | 0 | 7, 8 |

**What works.** In $(1,2,5,9)$ the short relation $2\cdot1=2$ suggests $d=3$, where speed 9 blocks everything. On $d=1+9=10$, speeds 1 and 9 have identical blocking behavior. The three class counts sum to ten. Since all three include zero, at most eight distinct numerators can be blocked. At $t=3/10$ the physical distances are $(3,4,5,3)/10$. This time can be verified directly against the original four speeds.

**What fails.** For $(1,3,12)$ every pair-sum grid has $L_0=0$. Two have witnesses. On $d=13$, the two classes 1 and 3 each block seven numerators. Their intersection contains $0,1,12$: both $1/13$ and $3/13$ are below $1/4$, and reflection supplies numerator 12. The union therefore covers at most $7+7-3=11$ numerators. Two must survive. The exact survivors are 6 and 7. The weak rule lost the locations at which *different* classes block together. In the tight eight-runner control even a zero-duration set has four distinct physical witnesses, all recovered on $d=8$.

## First experiment for the receiving project

**Freeze one small extension before looking at fresh results.** On each grid, in addition to numerator zero, credit only the two specified residues $+1,-1$. For a tested residue $a$, let $m(a)$ count blocking **classes** there, using the strict integer test $n\min(ac\bmod d,(-ac)\bmod d)<d$. Define
$$L_{\pm1}(d)=\max\left(0,\ d-\sum_{c\in C}b_c+
  \sum_{a\in\{0,1,d-1\}}(m(a)-1)_+\right).$$
Use a set of distinct residues. Apply the zero truncation after summing the corrections. At a tested residue with $m$ blocking classes the individual counts overstate coverage by exactly $m-1$. Ignoring duplication elsewhere gives a valid lower bound. The calculation needs the class sizes and three locations, regardless of $d$. It gives at least two survivors on the $d=13$ example. It still returns only a count until a physical numerator is recovered.

1. **Compare with an exact answer.** For the controls, then for primitive increasing four-speed tuples with speeds at most 15, compute both lower bounds and the exact survivor count on every distinct pair-sum grid. The November review reports 1,325 tuples in this box. Keep its shortest-relation failures identifiable. Separately keep the eight-runner equality control. Check recovered times in the repository interval checker. For a scaled tuple $sV$, carry $t$ back as $t/s$ if using the original clock.
2. **Ask two different questions.** How often does the correction certify a previously inconclusive *grid*? How often does it certify a tuple on which the original rule failed on *every* grid? Track weighted cost separately: number of moduli, classes, and residues inspected. For tuples with a distinguished short relation, mark internal and crossing pairs and retain all pairs as the baseline. Record ties in the choice of relation explicitly.
3. **Seek a failure that teaches something.** Return one tuple where all candidate bounds vanish although an exact witness exists, if found. Identify the smallest piece of omitted information that would repair the count on one successful grid. If even the three-residue correction exhausts the chosen box, report the finite scope and design a harder control. If inspecting more locations approaches a full scan, record that cost.
4. **Return one verified witness and one limitation.** Report tuple, reference, threshold, generating pair, denominator, class partition, predicted lower count, actual surviving numerators, and one physical time with all distances. A uniform argument would have to force a positive bound on *some* admissible grid for *every* tuple in its stated class. Selecting a working grid after seeing its full survivor list leaves that selection question open.

### What to return to Representation Science

Keep the mathematical result with Lonely Runner. Return a comparison of what each representation permits us to infer. The continuous duration loses isolated contacts. The signed residue classes preserve every runner's distance on a specified grid. Class sizes alone lose where distinct blockers coincide. Adding two named coincidences restores an existence inference on the 13-point example. The resulting lower bound still does not say *which* numerators survive. The experiment should report the information and work needed to go from a count to a recoverable physical witness. That is a testable contribution even if the proposed rule fails on a larger family.

### Reproduce the table

Run the following Python from the repository root. Its two checks use integer residues and the existing interval implementation. No external packages are needed.

~~~python
from fractions import Fraction
from math import gcd
from lonely_runner.checker import feasible_intervals

cases = [
    ((1, 2), [3]),
    ((1, 2, 5, 9), [3, 10]),
    ((1, 4, 5, 6, 7, 11, 13), [8, 24]),
    ((1, 3, 12), [4, 13, 15]),
]
for speeds, grids in cases:
    n = len(speeds) + 1
    allowed = feasible_intervals(speeds, Fraction(1, n))
    for d in grids:
        classes = sorted({min(v % d, (-v) % d) for v in speeds})
        def blocks(c, a):
            return n * min((a*c) % d, (-a*c) % d) < d

        counts = []
        for c in classes:
            g = gcd(c, d)
            h = d // g
            count = g * (2 * ((h + n - 1) // n) - 1)
            assert count == sum(blocks(c, a) for a in range(d))
            counts.append(count)

        lower = max(0, d - 1 - sum(b - 1 for b in counts))
        credit = sum(max(0, sum(blocks(c, a) for c in classes) - 1)
                     for a in {0, 1, d - 1})
        improved = max(0, d - sum(counts) + credit)
        safe = [a for a in range(d) if all(not blocks(v, a) for v in speeds)]
        interval_safe = [a for a in range(d)
                         if any(l <= Fraction(a, d) <= r for l, r in allowed)]
        assert safe == interval_safe and lower <= improved <= len(safe)
        print(speeds, d, counts, lower, improved, safe)
~~~

**Provenance and scope.** Vance selected the research direction and its connection to representation science. The AI collaborator drafted the finite counting argument, checked the displayed controls, and proposed the follow-up. These checks cover the listed controls. The four-speed comparison is work for the receiving project. No novelty or general solution is claimed.
