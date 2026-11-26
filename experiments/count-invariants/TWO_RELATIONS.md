# Two independent short relations at sixteen runners

November 25, 2026. Proof candidate for independent mathematical and priority review.

Use the fifteen distinct positive absolute speed differences $a=(a_1,\ldots,a_{15})$ from one designated runner. A strict lonely time means $\|ta_j\|>1/16$ for every $j$. Equality gives a valid lonely time for the original conjecture. The distinctness hypothesis is imposed throughout. With fewer distinct positive gaps, the corresponding smaller-runner case supplies strict clearance at the 16-runner threshold.

**Candidate.** If there is no strict lonely time, there are two linearly independent integer relations $a\cdot m=a\cdot u=0$. We may choose $m$ primitive with odd coefficient sum, $\|m\|_2^2\le73$ and $\|m\|_1\le31$. The second relation satisfies $\|u\|_2^2\le98$. Only the first is required to have odd sum. These bounds are independent of the speed magnitudes.

Beck and Everett provide the first relation. The second bound below comes from moving their Fourier window to a point where the first relation has integral phase. Their November 24 revision and other work already use short relations, subspaces, and lattice flags. The estimate does not establish priority or improve an existing computational speed ceiling. [Beck and Everett, Theorem 2 and Lemma 3](https://arxiv.org/html/2609.06259v3) · [Allikvere, Section 3](https://arxiv.org/html/2609.02604v2#S3) · [Earlier rank-dependent bounds on projected lattice flags](https://www.munimtech.com/research/dual-cap-lonely-runner-flag-bound).

## Choosing a window for which the first relation cannot account for cancellation

Theorem 2 of Beck and Everett gives an odd-sum integer relation of squared norm at most $1024/14$ and absolute coefficient sum at most 33. Its coordinate gcd is odd. Divide by that gcd to get $m$ primitive. Put $L=\|m\|_1$. This positive integer is odd. A relation of length one is impossible since $a_j>0$. An integer vector of length 33 has squared norm at least $12\cdot2^2+3\cdot3^2=75$ by balancing absolute values among fifteen coordinates. Thus $3\le L\le31$.

For each coordinate choose $x_j=1/2-\operatorname{sgn}(m_j)/(2L)$, with $\operatorname{sgn}(0)=0$. Then $m\cdot x=(\sum_jm_j-1)/2$ is integral. Let $b=7/16$. Set $h_j=b-1/(2L)$ on the support of $m$ and $h_j=b$ off it. The open arc of radius $h_j$ about $x_j$ lies in $(1/16,15/16)$.

For $0<h<1/2$, take the unshifted autocorrelation $D_h$ of Beck and Everett's normalized truncated cosine. It is positive exactly at $\|z\|<h$. Its absolutely summable Fourier coefficients $A_h(k)$ give a symmetric probability distribution on the integers with second moment $1/(4h^2)$. These are the assertions of their Lemma 3 after undoing its half-turn translation.

Let $Z$ have independent integer coordinates with laws $A_{h_j}$. Under the no-strict-time hypothesis, $\prod_j D_{h_j}(a_jt-x_j)=0$ at every $t$. Grouping its absolutely convergent Fourier expansion at frequency $q$ gives

$$
\mathbb E\!\left[e^{-2\pi i Z\cdot x}\mid Z\cdot a=q\right]=0
$$

for each $q$ of positive probability. No atom of this conditional phase distribution can have mass exceeding $1/2$ by the triangle inequality.

Draw $q$ from its actual frequency distribution, then independently draw $Z,Z'$ from the conditional law at $q$. Their phases are different with probability at least $1/2$. Their difference $u=Z-Z'$ is always an integer relation. On the event that the phases differ, $u$ is outside the real span of $m$. Indeed, primitiveness gives $\mathbb Z^{15}\cap\mathbb R m=\mathbb Zm$, and all integer multiples of $m$ have integral phase against $x$.

## Bounding the second relation

Let $P$ be orthogonal projection onto $a^\perp$. The difference $u$ equals $P(Z-Z')$. Conditional independence and the law of total variance give

$$
\mathbb E\|u\|_2^2
=2\,\mathbb E\bigl[\operatorname{tr}\operatorname{Cov}(PZ\mid q)\bigr]
\le \frac12\sum_{j=1}^{15}
\frac{1-a_j^2/\|a\|_2^2}{h_j^2}.
$$

Since the phases differ with probability at least $1/2$, some pair with differing phases has squared distance at most the sum on the right without its factor $1/2$. The diagonal entries of $P$ total 14, each is at most one, and the support of $m$ has size at most $L$. This bounds that sum by

$$
14b^{-2}+L\big[(b-1/(2L))^{-2}-b^{-2}\big].
$$

The term with $L$ decreases with $L$. It is half the secant slope from zero to $1/(2L)$ of the convex function $z\mapsto(b-z)^{-2}$. At $L=3$ the bound becomes $11(16/7)^2+3(48/13)^2=814592/8281<99$. The squared distance is integral, giving the claimed 98.

### A refinement by subtracting a multiple of the first relation

The same argument gives $\|u\|_2^2\le85$ for a suitable second relation. Write $s=|\operatorname{supp}(m)|$, $S=\|m\|_2^2$, $A=b^{-2}$ and $B=(b-1/(2L))^{-2}$. The preceding projection bound is at most $V=14A+s(B-A)$. Project instead onto the complement of both $a$ and $m$. Since $a\perp m$, this removes the additional unit direction $m/\sqrt S$. All its nonzero components are on coordinates of weight $B$, so the upper bound for the squared projected distance on some unequal-phase pair drops to $V-B$. Subtract the nearest integer multiple of $m$ from this pair's difference $u$. The result remains an integer relation outside the span of $m$. The squared length added back along $m$ is at most $S/4$.

We can use whichever bound is smaller, giving $\min(V,V-B+S/4)$. For $L$ and $s$ fixed, $S\le\min(73,(L-s+1)^2+s-1)$ by putting all excess absolute coefficient mass on one coordinate. Over odd $3\le L\le31$ and $1\le s\le\min(15,L)$, substituting this upper estimate gives maximum $2831627/33124<86$. The checker evaluates these rational bounds. Integrality gives 85. Neither 85 nor the earlier 98 is asserted optimal.

## What the controls say

- **A case that the second relation distinguishes.** Use the fifteen speeds $1,B,B+1,B^2,\ldots,B^{13}$ with $B=32$. Every relation of squared norm at most 98 is a multiple of $(1,1,-1,0,\ldots,0)$. In the expansion in powers of $B$, the coefficients of $1$ and $B$ have absolute value at most 18 and the others at most 9. Reducing modulo $B$ and dividing repeatedly forces all these coefficients to vanish. Thus the second relation criterion guarantees strict clearance even though the first short relation exists. A direct check gives clearance $1/5$ at $t=1/5$.
- **Two identical equations, two different outcomes.** Start both lineups with relative speeds $1,2,3,4$. They share $1+2=3$ and $1+3=4$, including the identities of the participating runners. Complete the first lineup to $1,\ldots,15$. At any time at least two of $0,t,\ldots,15t$ are within $1/16$, and every pair gap is tested by the reference. The maximum is exactly $1/16$. Complete the second lineup with $6,7,8,9,11,12,13,14,16,17,18$. All fifteen clear at least $1/5$ at $t=1/5$. This shows why further information on the other runners must enter a proof using these particular equations.
- **Earlier residual panel.** On all 135 lineups from the archived neutral panel, comparing sums of up to three speeds on each side already finds two independent relations, including one with odd coefficient sum. Their squared norms are at most 36. Thus existence of the two relations eliminates zero of those 135. All already have witnesses by earlier exact checks. [Panel and controls](relation_rank.py) · [Original panel](RELATIONSHIPS.md).

## How a smaller solved case could enter

Allikvere's Lemma 3.3, attributed there to Giri and Kravitz, supplies the following extension. If $W\subseteq a^\perp$ is spanned by $d$ independent integer relations, then $W^\perp$ is rational of dimension $15-d$ and contains $a$. No coordinate vanishes identically on it. Assuming the Lonely Runner cases through $d+2$ total runners, the lemma gives $x\in W^\perp$ with every coordinate at circular distance at least $1/(d+2)$ from zero. When $d\le13$, this leaves a positive margin $h=1/(d+2)-1/16$.

Run the same fiber calculation with the common window radius $h$. Every integer vector in $W$ has integral phase against $x$, so unequal phases now produce a relation outside $W$ of squared norm at most $14/h^2$. Iterating, conditional on the smaller cases, gives bounds up to 14 independent relations. The last bound is $14\cdot240^2=806400$. Full rank restricts a primitive 15-speed vector to finitely many possibilities. Finite reductions are established in the literature and this loose bound does not make their enumeration feasible. The numerical test worth pursuing is whether retaining the actual coefficient vectors and their shared runner labels excludes a modular class that survives earlier tests. [Allikvere, Lemma 3.3](https://arxiv.org/html/2609.02604v2#S3.SS2) · [Blanco, Criado and Santos on finiteness](https://arxiv.org/abs/2603.24784).

