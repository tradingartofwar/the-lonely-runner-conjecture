# Powers of two and one arbitrary speed

November 24, 2026. **Proof candidate** for the common-start, stationary-reference problem. This arose after the frozen overlap experiment. The proof uses a time depending on the added runner. The finite checks supplement the argument.

Let $\|x\|$ denote distance to the nearest integer and let $r$ be any positive integer. Take all the moving speeds $1,2,4,8,\ldots$ together with $r$. Even for this infinite core the best simultaneous distance is exactly
$$
\max_{t\in[0,1]}\min\bigl(\|rt\|,\inf_{i\ge0}\|2^it\|\bigr)
=\begin{cases}1/3 & 3\nmid r,\\ 1/5 & 3\mid r.\end{cases}
$$
Every finite subset of the powers inherits the lower bound. For $n\ge5$ total runners this supplies the Lonely Runner threshold $1/n$ for the designated reference when the other speeds have this form. The upper bound in the second row need not hold for a short or sparse finite subset.

## Constructing the physical time

If $3\nmid r$, take $t=1/3$. The doubled phases alternate between $1/3$ and $2/3$, and the added runner also lands at one of these two positions.

Suppose $3\mid r$. Take the least $j\ge0$ with $r\le12\cdot4^j$ and set
$$
t=\frac13+\frac1{15\cdot4^j}.
$$
Then $1/5\le r/(15\cdot4^j)\le4/5$. For $j>0$ the left inequality follows from minimality. For $j=0$ it follows from $r\ge3$. Since $r/3$ is an integer, the added runner is safe.

For $i<2j$, the shift from $2^i/3$ is at most $1/30$. Those base phases have distance $1/3$ from an integer, so the perturbed distance is at least $3/10$. At $i=2j$ we have $4^j\equiv1\bmod3$, giving phase $2/5$. All further doublings follow the cycle $2/5,4/5,3/5,1/5$. This single time protects every dyadic speed, whatever the largest exponent.

For example, $r=15$ defeats both $1/3$ and $1/5$. The rule chooses $j=1$ and $t=7/20$. The added runner reaches distance $1/4$. The first dyadic phases are $7/20,7/10,2/5$, and the four-cycle takes over.

## Why the distances are optimal

The speeds 1 and 2 alone preclude a distance strictly above $1/3$. For the uniform $1/5$ bound over all $r$, speed $r=3$ gives the short obstruction $1,2,3,4$. Among $0,t,2t,3t,4t$ on the circle some cyclic gap is at most $1/5$, and its endpoints differ by one of these four speeds times $t$.

For the stronger claim about **each** multiple of 3, suppose all dyadic phases have distance strictly greater than $1/5$. No phase $y$ in $[0,1)$ can lie in $(1/5,1/4]$, since $4y$ is then at distance less than $1/5$ from an integer. Reflection excludes $[3/4,4/5)$ too. Thus every successive doubling lies strictly between $1/4$ and $3/4$. In a binary expansion this forces every pair of consecutive digits to differ. Hence the only possible starting times are $1/3$ and $2/3$. Both give distance zero for the added multiple of 3. The explicit witness above attains $1/5$.

**Finite-prefix consequence.** If $3\mid r$ and the core contains every speed from $2^0$ through $2^m$ with $2^m\ge5r$, its exact optimum is already $1/5$, assuming all other core speeds are also powers of two. Indeed, if all the first $m+1$ dyadic distances exceed $1/5$, the first $m-1$ doubled phases ($i=0,\ldots,m-2$) must lie strictly between $1/4$ and $3/4$ by the same two-step argument. The first $m$ binary digits alternate, placing $t$ within $2^{-m}$ of $1/3$ or $2/3$. The added runner is therefore within $r2^{-m}\le1/5$ of an integer. Dyadic endpoints cause no ambiguity in the forcing step, since exactly $1/4$ and $3/4$ were excluded.

## A boundary for the next question

For two arbitrary added speeds the single-extra conclusion already changes. Add 3 and 5. The included speeds $1,2,3,4,5$ give the pigeonhole upper bound $1/6$. The time $1/6$ attains it even with every power of two present. The witness family $1/3$ and $1/3+1/(15\cdot4^j)$ cannot handle 3 and 5 together even at this weaker threshold. At $j=0$, speed 5 lands at an integer. For $j\ge1$, speed 3 is within $1/20$ of an integer, and it also blocks $1/3$. Whether **every** pair of added positive integer speeds permits $1/6$ for the entire dyadic core is a question for investigation. The example supplies a necessary change of witness family.

## Evidence and attribution

The reproducible checks exercise the scale decision, both exact endpoints, transitions for very large integers, and exact optima for ten finite prefixes. The proof above supplies the quantifiers over all added speeds and all exponents. Vance's question about blocking at the same physical times motivated the experiment. AI collaborators developed and checked this argument. Independent specialist review and publication priority remain open. The doubled phases lie in the setting of established doubling-map dynamics. Related lacunary Lonely Runner results impose ratio conditions on successive speeds, which an arbitrary additional speed can violate. [Bonanno, Carminati, Isola and Tiozzo](https://users.math.yale.edu/users/tiozzo/docs/confrackneaseq_DCDS3.pdf) · [Dubickas, 2011](https://web.math.pmf.unizg.hr/glasnik/vol_46/no1_05.html) · [Experiment and replay](RESULTS.md)

