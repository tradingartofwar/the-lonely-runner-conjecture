# Does one short speed relation survive several prime grids?

For a fixed reference, a lineup with no time strictly above $1/n$ must have a short integer relation among its $k=n-1$ positive relative speeds. Beck and Everett give a coefficient vector $h$ with odd coordinate sum, $h\cdot v=0$, $\|h\|_1\le2k+3$ and $(k-1)\|h\|_2^2\le4(k+1)^2$. The same $h$ must therefore work modulo every prime, with coordinates matched to the same physical runners. Excluding all such $h$ certifies strict clearance. Finding one modular relation leaves the question open. [Beck and Everett, Theorem 2.1](https://arxiv.org/html/2609.06259v2).

## Keeping the labels can matter

Write $r=(1,\ldots,n-1)$. Start with the same unsigned consecutive speed set on two distinct prime grids of denominators $p,q>(n-1)(2n+1)$. Each grid misses the target. Indeed the $n$ points $0,t,\ldots,(n-1)t$ have to be equally spaced for all consecutive relative speeds to clear $1/n$. Such a time has reduced denominator $n$. Reordering or individually reversing speeds leaves the single-grid result unchanged.

Now specify which runner gets which residues. If $v_i\equiv i\pmod p$ and $v_i\equiv n-i\pmod q$, the two dot products of $h$ with the small rows must vanish as integers: their absolute values are at most $(n-1)(2n+1)$. Adding gives $n\sum h_i=0$, impossible for an odd coordinate sum. Every positive integer lift of this **labelled** pair has strict clearance for the reference. This argument works for any total count $n\ge3$ with the stated prime bounds.

There is an explicit time as well. Set $a,b$ to the nearest integers to $p/(2n),q/(2n)$ and take $t=a/p+b/q$. Each runner's phase differs from half a lap modulo one by at most $i/(2p)+(n-i)/(2q)$. For $n=16$, $p=503$, $q=509$, the time $16192/256027$ gives minimum distance exactly $125819/256027$. This time works for the whole labelled residue class.

For the identical row at both primes, $2v_1-v_2\equiv0$ on both grids. The literal speeds $1,\ldots,15$ just attain $1/16$. Replacing each even speed $i$ by $i+503\cdot509$ produces an all-odd lineup at identical residues, with clearance $1/2$ at $t=1/2$. Even the product grid cannot distinguish these two lineups.

## Fixed panels

All input pairs below are individually blocked on each prime grid. A product-grid success means an actual witness for every integer lift of the prescribed pairing. The five-runner panel includes sign-related duplicates by design.

| Total runners and panel | Pairings | Excluded by common-relation test | Retain a short relation | Combined grid has a witness |
|---|---:|---:|---:|---:|
| 5, all signed permutations at 47 and 53 | 384 | 124 | 260 | 382 |
| 16, identical and reversed controls at 503 and 509 | 2 | 1 | 1 | 1 |
| 16, fixed-seed signed permutations at 503 and 509 | 256 | 0 | 256 | 256 |

For five runners we enumerated both coefficient bounds in full. An independent four-coordinate box enumeration agreed on all 384 decisions. For every sampled 16-runner row an explicit relation of 1-norm at most 5 sufficed, so the positive compatibility decisions also hold for the full bound 33. This sample varies the pairing of one residue pattern. It supplies no population estimate for all lineups. [Fixed panel protocol](PROTOCOL.md).

## What disappears when the clocks forget runner identities

In the common modular representation, each prime groups together coordinate permutations, individual sign changes and multiplication of all speeds by one unit. An unordered pair can be rejected only if **every** permitted alignment fails. For first-level 16-runner grids at the seven primes studied previously, **every** surviving unsigned support contains three distinct classes that admit some signed equation $a+b=c$. The same coefficient shape $(1,1,-1,0,\ldots,0)$ can consequently be aligned across any combination of these seven primes. It meets both bounds. This covers all first-level survivors with speeds nonzero modulo each respective prime, including repeated classes.

| Prime | 37 | 41 | 43 | 47 | 53 | 59 | 61 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Smallest support that blocks the full grid | 9 | 10 | 12 | 12 | 11 | 12 | 12 |
| Largest support without a signed triple of distinct classes | 7 | 8 | 8 | 9 | 10 | 11 | 11 |

We directly enumerated triple-free supports up to 15 and checked their blocked grid times. The upper row also has two independent counts in the [previous study](../shift-coverage/README.md).

**Reason for the gap.** At any odd prime greater than 3 let $T$ be the full signed set associated to a nonempty unsigned support with no such triple. For every $d\in T$, at most three $x\in T$ satisfy $x+d\in T$: unless $x$, $d$, and $x+d$ have a coincident unsigned class they form a forbidden triple. The only possible $x$ are $d,-2d,-d/2$. If $d,2d\in T$, the translates $T,T+d,T+2d$ therefore each intersect one another in at most three elements. Their union has size at least $3|T|-9$ and at most $p$. If no such $d$ exists, $T$ is sum-free, since a sum in $T$ would require a signed triple or a doubling. Cauchy–Davenport then gives $3|T|\le p+1$. In either case the unsigned support has size at most $\lfloor(p+9)/6\rfloor$. This bound alone suffices with the seven covering minima above. [Cauchy–Davenport inequality](https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/PolynomialMethodClassNotes.pdf).

The triple can represent one exact integer equation as well: align the three residues at each prime, choose positive simultaneous lifts of the first two and use their sum as the third. Choose all other lifts distinct by adding multiples of the product of the primes. If primitivity is required, choose the second lift coprime to the first by also specifying its residues at the prime divisors of the first; those divisors are coprime to the grid moduli. This gives potential candidates for a relation filter, without implying that the physical lineup is tight.

## A deeper-grid control with a shared denominator

The fourth binary refinements at 97 and 101 produce 64 surviving consecutive-seed lifts apiece before the established divisor-shift test. The two grids share a factor of 16, which partially restores runner identities: speeds paired across these grids must agree modulo 16 after the allowed symmetries. Both sets have thirteen zero residues and two odd ones modulo 16. The signed unordered odd pair, up to a common odd multiplier, has types $(1,1),(1,3),(1,7)$ with frequencies 16, 32, 16 on either side.

Of 4,096 pairs, 2,560 already fail this shared-modulus check. All 1,536 remaining pairs preserve a signed triple across both grids. In each lifted row the first three speeds are multiples of 16 and satisfy the triple on the prime grid. They can be matched in the same order while aligning the exceptional odd coordinates separately. We constructed the compatible combined residues and checked the triple for every pair. The short-relation test removes zero additional pairs here. The standard four-shift test already clears the individual survivors; this is a diagnostic panel. [Follow-up test scope](UNLABELLED_TEST.md).

## Reproduce

Run `python check.py`, `python unlabelled.py`, and `python shared_level.py` in this directory with Python 3.11 or later. The last command imports the previously verified binary lift routine from the adjacent proof-survivors directory. The work gives a strict-clearance certificate for prescribed pairings and a proof of redundancy on the specified unordered grids. General 16-runner coverage and usefulness on harder prime families remain open.
