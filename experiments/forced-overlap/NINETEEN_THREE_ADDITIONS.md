# Nineteen runners with three freely chosen speeds

**November 24, 2026 · HYPOTHESIS (computer-assisted proof candidate).** Fix the sixteen integer speeds $Q=\{0,1,\ldots,14,105\}$. For **every** three distinct positive integers $u<v<w$ outside $Q$, every runner in $Q\cup\{u,v,w\}$ has a time at circular distance at least $1/19$ from all eighteen opponents. Times can differ by runner. This includes speeds between the fixed speeds, consecutive additions, and additions of unbounded size.

The [close-speed protocol](NINETEEN_CLOSE_PROTOCOL.md) originally asked about large additions with small gaps. Its [result and subsequent extension](NINETEEN_FAST_TRIPLES.md) settle any newcomer reference of speed at least 1680, regardless of the other two speeds. The reduction below was developed afterward. It handles every remaining reference and frees all three added speeds simultaneously.

## Why finitely many relative speeds suffice at each step

Fix the runner whose lonely time is sought. Write $C$ for the known positive absolute speed differences to its opponents and $k$ for the number of opponents whose speeds remain free. Suppose $I=[a,b]$ of length $L>0$ is safe against every member of $C$. If $k$ other opponents together spoil every time in $I$, at least one must block at least $L/k$ of its length. This observation lets us replace a search over all speeds by finitely many possibilities for **one** opponent.

For a relative speed $v>0$, the blocked phase is within $1/19$ of an integer. Write $B(v)$ for the time it blocks on $I$. The period estimate gives

$$B(v)\le\frac2{19}(L+1/v).$$

Counting closed blocking arcs in the calculation is conservative. Their endpoints are safe in the conjecture and have zero duration. If $B(v)\ge L/k$, rearrangement gives

$$vL\le\frac{2k}{19-2k}.$$

For the values $k=1,2,3$ this bound is at most $6/13<17/19$, the clear phase distance between successive blocking arcs. The interval $[va,vb]$ can therefore intersect at most one blocking arc. Such an arc can cover at least $vL/k$ of this image precisely when its full width is sufficient and its center is in the right place. Equivalently,

$$vL\le 2k/19,\qquad
v(a+L/k)-1/19\ \le m\le\ v(b-L/k)+1/19
\quad\hbox{for some integer }m.$$

Indeed, the intersection of $[va,vb]$ and $[m-1/19,m+1/19]$ has length at least $vL/k$ exactly when both intervals have that much length and each right endpoint is at least that far above the other left endpoint. The inequalities include equality. They give an exact finite list of the positive integers $v$ capable of blocking at least a $1/k$ share.

For each listed speed, move it into $C$ and seek a possibly different safe interval for the remaining $k-1$ opponents. When $k=1$, check an exact rational time for each listed speed against all known opponents and that speed. A hypothetical counterexample would follow at least one branch of this tree down to a failed terminal check. Repeated absolute differences are allowed, so the reasoning also covers opponents on opposite sides of the reference in speed.

The initial cutoff principle works more generally at clearance $1/n$ whenever $2k<n$. Its use still requires positive-width safe intervals for the known opponents at the internal nodes. The present calculation supplies them for the stated core.

## Exhausting the references

- For each of the sixteen references $r\in Q$, take $C=\{|s-r|:s\in Q,\ s\ne r\}$ and $k=3$.
- For each of the 1,664 speeds $1\le r<1680$ outside $Q$, take $C=\{|s-r|:s\in Q\}$ and $k=2$. Any two other new speeds give positive relative differences in the verified domain.
- For each newcomer reference $r\ge1680$, the [fast-reference argument](NINETEEN_FAST_TRIPLES.md) gives a witness against $Q$ and any two positive relative gaps. Its proof uses the size of the reference speed alone. The other two newcomers can be slower.

These cases exhaust all nineteen references, including configurations that straddle 1680. Sorting the three new physical speeds serves only to name the lineups.

| Opponents still free | Safe intervals checked | Candidate speeds across those intervals |
| ---: | ---: | ---: |
| 3 | 16 | 89 |
| 2 | 1,753 | 145,821 |
| 1 | 145,821 | 2,416,526 |

The final number counts terminal branches with multiplicity. Speeds outside each finite list are handled by the interval argument, including arbitrarily large speeds.

## Reproduction and counterchecks

From the repository root with Python 3.10 or later, run

```sh
python experiments/forced-overlap/verify_nineteen_fast_triples.py
python experiments/forced-overlap/verify_nineteen_three_additions.py --audit
```

The [finite verifier](verify_nineteen_three_additions.py) constructs its own intervals. It uses rational times with reduced denominator through 64 and also tries $1/(2\max C)$ when $2\min C>\max C$. The first twelve available times are considered when selecting an interval. All terminal witnesses are verified using exact integer residues. Each claimed internal interval is checked against its known speeds in audit mode.

The audit independently recalculates each finite list over the larger cutoff $2k/[(19-2k)L]$. It integrates the exact blocked portion of $[va,vb]$ by counting full laps and the two blocked pieces of a partial lap. This avoids the single-arc center formula. It compares the two lists for equality at every node and rechecks every terminal witness directly against every opponent. Both modes of computation are internal checks.

Two diagnostic controls test the limits of the reasoning. For $I=[(19-k)/38,(19+k)/38]$ centered at $1/2$, speed 2 blocks exactly a $1/k$ share and must appear in the list for each $k=1,2,3$. For the known relative speeds $1,\ldots,18$, valid $1/19$ times exist but are isolated: the nineteen points $0,t,\ldots,18t$ must all be equally spaced. The interval selector rejects that example as a starting point for this reduction. It requires genuinely positive width.

For a prior-work comparison, Ram Krishna Pandey's *On the lonely runner conjecture* (2010), Theorems 3.1–3.2, treats arithmetic progressions of relative speeds and a small-sumset condition. For reference zero with our additions 1000, 10000 and 100000, the eighteen positive relative speeds form a set $S$ with at least 55 distinct sums: $2,\ldots,28$, $106,\ldots,119$, and $1001,\ldots,1014$. This exceeds the bound $|S+S|<3|S|-3=51$ in Theorem 3.2. This check addresses those two theorem statements only. [Pandey, Mathematica Bohemica 135 (2010), 63–68](https://dml.cz/handle/10338.dmlcz/140683).

The fixed sixteen speeds are a hypothesis of the result. The argument leaves arbitrary nineteen-speed lineups and the conjecture for arbitrary runner counts open. AI assistance contributed the proof and code. Independent mathematical review and comparison with prior results are pending.
