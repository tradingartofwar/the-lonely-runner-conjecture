# Three freely chosen fast speeds with no gap condition

**November 24, 2026 · HYPOTHESIS (computer-assisted proof candidate).** Let $Q=\{0,1,\ldots,14,105\}$ and let $1680\le u<v<w$ be integers. Every runner in $Q\cup\{u,v,w\}$ has a time at distance at least $1/19$ from its eighteen opponents. The bound on the smallest speed is sufficient. The evidence comes from a [prespecified close-speed test](NINETEEN_CLOSE_PROTOCOL.md), followed by a separate argument for an arbitrarily distant third newcomer.

Write $K=1680$, $\delta=1/19$, and $\|a\|$ for distance to the nearest integer. All runners start together. Times can differ by reference. An arc of length $\beta$ on the unit circle is occupied by a speed $z>0$ for between $\beta(L-1/z)$ and $\beta(L+1/z)$ during any time interval of length $L$. Split the time into full periods and one remainder to obtain these bounds.

## Fixed references

All sixteen fixed runners clear each other at $1/19$ throughout the same interval

$$I=[96/1729,113/1995],\qquad |I|=29/25935.$$

The verifier checks the image of $I$ under every positive fixed speed difference against a single closed safe arc. These endpoints come from the component containing $1/18$, with speed differences 91 and 105 setting its two ends. For a fixed reference $r$, each added speed $z$ blocks at most $2(|I|+1/(z-r))/19$ units of time. The sum for three additions is less than $|I|$, since $13(K-105)|I|=435/19>6$.

## Newcomer reference with two bounded relative gaps

In fact this part of the proof and the next work for **any reference $R\ge K$ outside $Q$**, with any two other speeds distinct from each other, from $R$ and from $Q$. Only their positive absolute speed differences $d\le e$ from $R$ matter.

Suppose $e\le840$. At a rational time $t_0=p/q$, let $H$ be the width of a largest circular gap between successive phases of the sixteen fixed speeds. Choose its midpoint $\theta$. It suffices that

$$H\ge 2\delta+105/K,\qquad
\|j t_0\|\ge\delta+j/(2K)\quad(j=d,e).$$

Choose the nearest time $t$ to $t_0$ at which $Rt=\theta\pmod 1$. Then $|t-t_0|\le1/(2R)$. Each fixed phase can move by at most $105/(2R)$, so its distance from $\theta$ stays at least $\delta$. The two relative gaps drift by at most $j/(2R)$, leaving each at least $\delta$ from an integer.

Among reduced center times of denominator at most 128, the search covered every pair by denominator 47. It kept 46 centers. For each center, the [verifier](verify_nineteen_fast_triples.py) computes the largest circular gap from $Q$, and for each $j=1,\ldots,840$ records which centers meet the gap-distance bound. The two lists intersect for all **353,220** unordered pairs with repetition. Through denominator 40 the sole outstanding pair in this stronger test domain was $(786,800)$, which $16/47$ covers. There were zero remaining pairs at the first protocol stage. The optional denominator 4093 was unnecessary.

## An unbounded relative gap

This extension was derived after the close-speed test. Suppose $e>840$.

**If $d\ge45$**, restrict time to $[0,1/28]$. The speeds $0,\ldots,14$ have phases in $[0,1/2]$. The phase of $R$ clears them in the arc $[1/2+\delta,1-\delta]$ of length $15/38$. Subtract the time blocked by speed 105 and by the two other newcomers. Their relative speeds are $R-105,d,e$, each with blocking arc length $4/38$. The surviving duration is at least

$$\frac1{38}\left(\frac3{28}-\frac{15}{R}-\frac4{R-105}-\frac4d-\frac4e\right)
\ \ge\ \frac{17}{319200}>0.$$

**If $d\le44$**, choose $2\le q\le5$ with $q\nmid d$. Such a $q$ exists because the least common multiple is 60. Work on an interval of length $L=1/200$ centered at $1/q$. Throughout it the small gap is safe, since $\|dt\|\ge1/5-44L/2=9/100>\delta$.

Subtract speed 7 from the speeds $0,\ldots,14$ and from $R$ to compare phases. At $1/q$ the fifteen fixed phases lie on the $1/q$ grid. Each moves at most $7L/2$ from its starting grid point. Thus a phase of $(R-7)t$ at distance at least $\delta+7L/2$ from that grid clears all fifteen. These favorable phases occupy a fraction $\beta=1-q(2\delta+7L)\ge227/760$. They repeat with period $1/[q(R-7)]$ in time. Subtract the blocked durations for the outlier 105 and the other gap $e$. The duration left is at least

$$\frac{227}{760}\left(L-\frac1{2(K-7)}\right)
-\frac2{19}\left(2L+\frac1{K-105}+\frac1{840}\right)
=\frac{364759}{2288664000}>0.$$

These two cases and the bounded-gap certificate cover all positive $d,e$. Together with the fixed-reference estimate they prove the claimed implication, subject to independent review.

## Reproduction and scope

Run from the repository root with Python 3.10 or later:

```sh
python experiments/forced-overlap/verify_nineteen_fast_triples.py
```

Expected output:

```text
46 centers cover 353,220 gap pairs.
247 direct role checks and 27 constructed-time checks passed.
```

The 13 full-lineup controls include every frozen case, an adjacent-speed trio translated by a trillion, both orders of a small and a large gap, and the split at 44/45. Direct controls search for an exact rational time independently of the center construction. The checker also constructs the prescribed shifted times in the bounded-gap controls and rechecks all opponents. At gap 420 all center denominators 2 through 7 divide the gap, so testing only those unshifted times misses this case.

The proof keeps sixteen prescribed speeds. For three arbitrary additions over $Q$, its newcomer argument already covers each individual reference of speed at least 1680 even if one of its fellow newcomers is slower. The fixed references and the slower newcomer references still require coverage in that case. AI assistance contributed the derivation and verification. Independent review and priority assessment remain open.
