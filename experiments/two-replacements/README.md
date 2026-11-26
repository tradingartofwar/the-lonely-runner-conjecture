# How fast can two replacement runners be in a tight lineup?

November 25, 2026. Proof candidate for independent review. Yuhan Zhang's Question 8.2 asks for a speed bound on tight modifications of the consecutive lineup. The argument here treats exactly two replacements, at every count $n\ge5$. It uses Zhang's one-entry classification, the Goddyn–Wong criterion and interval coverage. We also give complete computations at selected counts. Equivalent earlier bounds and priority have not been ruled out. [Zhang, *Tight instances of the Lonely Runner Conjecture*, v3](https://arxiv.org/html/2608.13599v3) · [Goddyn and Wong](https://www.sfu.ca/~goddyn/Papers/063tight_lonely_runner.pdf).

## Statement

The runner at zero is the reference. Begin with its $n-1$ positive relative speeds $1,\ldots,n-1$, delete $r<s$, and insert integers $n\le x<y$. Write $D(V)=\max_t\min_{v\in V}\|vt\|$. A tight set has $D(V)=1/n$. A strict witness has clearance greater than $1/n$.

**If the modified speeds admit no strict witness, then**

$$
x<\frac{4n(n-1)^2}{n-4},\qquad
y\le 2(n-1)x<\frac{8n(n-1)^3}{n-4}.
$$

In particular the larger replacement in a tight set is $O(n^3)$. Using Zhang's more precise window lengths gives $x=O(n\log n)$ and $y=O(n^2\log n)$ below. The sharper proposed bound $O(n\log n)$ for the larger speed, and the general case of three or more changes, remain open here. The displayed bounds concern a designated reference.

## Why the first replacement always leaves an opening

Let $U_j$ be the open set of times when all original speeds except $j$ strictly clear $1/n$. The original set is tight, so $U_r$ and $U_s$ are disjoint. Each lies inside the strict-safe set after both deletions. If speed $x$ destroyed every strict witness there, it would suppress both $U_r$ and $U_s$. Thus replacing $r$ alone by $x$, and replacing $s$ alone by that same $x$, would both lack a strict witness.

We use the following detail of Zhang's one-entry proof. Theorem 1.2 states a classification for equality. Its proof also shows that every one-entry configuration outside the listed types has a strict witness. For $r=1$ the Goddyn–Wong lower bound and equality criterion apply directly. For $2r>n-1$, a failure of strictness at $t=1/r$ forces $r\mid x$, and the same theorem applies. In the middle range $3\le r\le(n-1)/2$, Proposition 3.4 uses coverage of the open windows to derive incompatible inequalities. Lemma 2.2 gives that coverage whenever the maximum is at most $1/n$. For $r=2$, Proposition 3.5 uses the same coverage followed by explicit strict witnesses for the two residual alternatives. These steps avoid assuming the unrestricted Lonely Runner Conjecture. [Zhang, Theorems 1.1–1.2, Lemmas 2.2–2.4, and Section 3](https://arxiv.org/html/2608.13599v3).

For the Goddyn–Wong type, a failure for deletion $r$ requires $r\mid x$ and every integer in
$$
[n-r,\ (x/r)(n-r)-1]
$$
to have a common factor greater than one with $r$. Suppose $s$ also has a Goddyn–Wong failure. Put $g=\gcd(r,s)$. Both $r$ and $s$ divide $x$, hence $x/r\ge s/g$. Since $s>r$, $s/g-1\ge r/g$, and $n-r\ge s-r+1\ge g+1$. The interval has at least $(r/g)(g+1)>r$ integers. It therefore contains an integer congruent to one modulo $r$, a contradiction.

The sporadic cases are $(n,r,x)=(5,2,7)$ and $(6,2,9)$. For 7 the only possible other divisor below 5 is 1, which cannot satisfy the criterion. For 9 the other nontrivial possibility is 3, and $[3,8]$ contains 4, coprime to 3. Thus **one inserted speed can suppress the opening for at most one individual deletion**. The twice-deleted core plus $x$ always has a nonempty strict-safe interval.

## Bounding the speeds

Let $J$ be a strict-safe component of the twice-deleted core and $L$ its length. Such a component exists by the preceding argument. An endpoint set by speed $u$ has the form $(nk\pm1)/(nu)$. Distinct endpoints set by $u,v\le n-1$ therefore differ by at least $1/(nuv)\ge1/[n(n-1)^2]$. The lower bound also holds if one speed sets both endpoints.

A speed $z$ blocks a fraction $2/n$ of each period. On an interval of length $L$, complete periods and the remaining partial period contribute at most $(2/n)(L+1/z)$ in total. Complete coverage of $J$ by the two inserted speeds gives
$$
(n-4)L\le2(1/x+1/y)<4/x.
$$
Substitution gives the stated bound on $x$. This step uses the same component-measure principle as Zhang's Lemma 6.1.

Now take a strict-safe component of the core **including** $x$. When different speeds set its ends, their product is at most $(n-1)x$, so its width is at least $1/[n(n-1)x]$. If the same speed $z$ sets both ends, their difference is a nonzero integer multiple of $1/(nz)$, which is also sufficient. One closed blocking interval of $y$ must cover the entire component. Such an interval has width $2/(ny)$. Comparing widths gives $y\le2(n-1)x$.

### Using Zhang's component lengths to improve the growth rate

Choose an omitted speed $j\ge2$ and set $s_0=n-j$, $I=\min\{i\ge s_0:\gcd(i,j)=1\}$. Every component of $U_j$ lies within the twice-deleted safe set. For $2j\le n-1$, Corollary 2.7 gives longest length $(2s_0-I)/(2jnI)$. The Jacobsthal estimate used in the proof of Zhang's Lemma 3.3 gives $I-s_0\le j/2$ when $j$ has two or more prime factors. For a prime power the difference is at most one. Consequently $I\le3s_0/2$, and this length is at least $1/(6jn)$.

For $2j>n-1$, Corollary 2.7 and the identity $\min F=I$ give length at least $s_0/(jnI)$. To bound $I$, take $X=\max(101,s_0,\log n)$. The Chebyshev estimates used in Zhang's Section 4 imply $\theta(4X)-\theta(X)>2X>\log j$, where $\theta$ sums the logarithms of the primes. Some prime in $(X,4X]$ therefore does not divide $j$, giving $I\le4X$. Since $s_0\ge1$, this length is at least $1/[4n^2\max(101,\log n)]$. Combining the two ranges gives $L\gg1/[n^2(1+\log n)]$. The preceding estimates now imply $x=O(n\log n)$ and $y=O(n^2\log n)$. These are upper bounds. The $n\log n$ limit superior for the largest speed in tight **one-entry** changes is Zhang's result. [Corollary 2.7, Lemma 3.3 and Section 4](https://arxiv.org/html/2608.13599v3).

## Unbounded checks for the designated runner

The checker uses actual rational interval lengths to reduce the search much further than the general bound. For each deletion pair the measure estimate handles all $x$ with $(n-4)Lx\ge4$ because $y>x$. For each remaining $x$, the enlarged core has a strict-safe component of width $L_x$. Every $y>2/(nL_x)$ is covered by the one-blocker width argument. For the remaining pairs the checker intersects open rational safe arcs, directly evaluates each positive witness, and checks strict witnesses again with an integer numerator-and-denominator scan. Equality-only cases get a separate endpoint check.

| Total runners | Deletion pairs | Smaller speeds needing their own interval check, summed across pairs | Finite pairs checked | Equality-only cases | Below $1/n$ |
|---:|---:|---:|---:|---:|---:|
| 8 | 21 | 279 | 119 | 1 | 0 |
| 15 | 91 | 1,374 | 731 | 0 | 0 |
| 16 | 105 | 1,533 | 706 | 0 | 0 |
| 17 | 120 | 1,699 | 584 | 0 | 0 |
| 18 | 136 | 2,179 | 1,025 | 0 | 0 |

Zhang's Theorem 6.10 already covers the finite window $y\le8n$ for these counts and many others. The interval arguments above cover all larger replacements at the five displayed counts. The known eight-runner control deletes 2 and 3 and adds 11 and 13. It attains equality at $1/8$. We also checked the single known 74-runner example, deleting 70 and 72 and adding 140 and 144. It attains equality at $1/74$.

## All sixteen physical runners in the 16-runner family

For this count the full lineup is $0,\ldots,15$ with two nonzero speeds replaced by $16\le x<y$. Every physical runner reaches $1/16$. The argument for zero above always gives a strict witness. A different runner can be tight.

For any retained runner $r$, take its positive absolute differences to the other retained runners, with repetitions removed. Both newcomers are faster than $r$. Apply the same two interval bounds to $x-r$ and $y-r$, then test the remaining finite cases including endpoints. The checker verifies the required nonempty windows for each finite row.

For a newcomer $R\ge61$ write $d=y-x$. When $d\ge60$, take times in $[0,1/30]$. The retained phases lie in $[0,1/2]$, so a newcomer phase in $(9/16,15/16)$ clears them. This phase arc occupies at least $(3/8)(1/30-1/R)$ time. The other newcomer blocks at most $(1/8)(1/30+1/d)$. The difference is positive since $1/15>3/61+1/60$. For $d\le59$, choose $q\in\{2,3,4,5\}$ that does not divide $d$, using their least common multiple 60. At $t=1/q+1/(2qR)$ each gap from $R$ to a retained speed is displaced from its original $q$-grid point by between $(1-15/R)/(2q)$ and $1/(2q)$. This gives clearance greater than $1/16$. The other newcomer is at least $(1-d/(2R))/q>1/16$ away.

For $17\le R\le60$, the open interval $(1/[16(R-15)],15/[16R])$ clears all speeds $0,\ldots,15$ before the deletions. Use its width to handle all sufficiently large $d$, and intersect the full core's safe intervals for the smaller $d$. Only $(R,d)=(17,1)$ requires the specific two deletions. For $R=16$ apply the one-blocker interval test to each retained set directly.

The complete test yields 121 combinations of omitted speeds, inserted speeds and designated runner with exact best clearance $1/16$. Every one has absolute relative speeds $\{1,\ldots,15\}$. For example, replace 5 and 6 by 24 and 25. Runner 0 gets strict clearance, while runner 15 sees exactly the original fifteen gaps. This control shows why the reference must travel with the statement. All other runner roles in this family clear strictly.

As an independent check, scanning rational clocks directly for all replacements up to 30 gave 176,279 strict roles and 121 equality roles. Each of the equality roles had consecutive absolute gaps.

### A control for what pair relationships can detect

Aaronson highlighted two papers in which lower and upper bounds meet. The Fourier paper counts linear gates for computing the entire transform. Its discussion of which intermediate computations can be shared suggested a narrower runner test. If we know how many clocks each outsider blocks and how many each labelled pair blocks together, can we tell whether any clock survives? [Aaronson's November 25 post](https://scottaaronson.blog/?p=10379) · [Fourier-transform paper](https://github.com/openai/math/blob/main/preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/paper.pdf).

On the grid $h/73$, the relative speeds $1,\ldots,12$ leave exactly five candidate numerators up to reflection. They are $5,17,26,28,34$. Add three outsiders as shown below. Each blocks 2, 2 and 3 candidates respectively. In both rows each labelled pair shares exactly one blocked time.

| Outsiders | First blocks | Second blocks | Third blocks | What survives |
|---|---|---|---|---|
| 15, 28, 13 | 5, 34 | 26, 34 | 17, 28, 34 | None on this grid |
| 17, 28, 13 | 17, 26 | 26, 34 | 17, 28, 34 | $5/73$ |

In the first lineup all three meet at numerator 34. In the second their pairwise overlaps occur at three different numerators, leaving numerator 5 untouched. The first lineup still has a lonely time at $1/16$. Across all 2,024 outsider triples of distinct unsigned classes from 13 through 36, six fell into a pair-count pattern with both outcomes. Applying the same test on four other primes (79, 83, 89 and 97) found no ambiguous pattern among 18,679 additional triples. This control concerns a fixed grid and a designated runner.

Run with standard Python 3.11 or later.

    python lr_two_swap.py
    python lr_changed_roles.py
    python lr_one_swap.py
    python overlap_control.py

The one-swap script also compares the one-entry classification for counts 6 through 20 with the four lowest speeds retained. It recovers the equality pattern at 8, 14 and 20 from the [earlier project test](../loneliness-spectrum/README.md).

