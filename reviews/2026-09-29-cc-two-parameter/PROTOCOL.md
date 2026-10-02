# Two-parameter orbit and witness protocol — September 29, 2026

Frozen before new computation and separate review. Authorized continuation of
the proposed primitive orbit/recovery step, including assessment of the same
two segments' coverage. Source branch head: `1696035e73bb53764f431237794cfca342dad002`;
mathematical predecessor: `e37858ffd238a668682289280ee26c6c5e8a0646`.

## Scope and proposed claims

Positive integer p,q, seven native coefficient rows
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2), stationary selected reference,
common start, closed threshold 1/8. Eight distinct speeds require p != q.
The p=q case may be checked as a labelled repeated-speed auxiliary only.
One witness is the output; no optimum, full safe set, other reference runner,
arbitrary seven speeds, or novelty claim is proposed.

1. For coprime p,q, prove orbit equivalence h=qx-py integral and recover
   t={r*x+s*y}, where r*p+s*q=1, with all physical lap labels.
2. For d=gcd(p,q), use P=p/d,Q=q/d and primitive orbit condition
   Qx-Py integral, equivalently qx-py in dZ. Recover primitive time tau
   and actual time t=tau/d. Check independence of the Bezout pair.
3. Test P3 first: x in [3/8,1/2], y=9/8-2x,
   full labels (0,0,0,1,1,1,2). Its projected interval is
   [3(Q-P)/8,(4Q-P)/8]. Width (Q+2P)/8 proves coverage for Q+2P>=8.
4. Exhaust the positive primitive exceptional triangle Q+2P<8 analytically.
   Proposed only misses: (P,Q)=(1,2),(1,4). Use P1:
   x in [1/8,5/24], y=7/8-3x, labels (0,0,0,0,0,1,1),
   interval [(Q-4P)/8,(5Q-6P)/24]. Retain both endpoints.
5. Revise cost honestly: at most two segment tests after gcd reduction,
   plus extended Euclid/Bezout recovery, whose iteration count is not constant.

## Fixed exact controls and failure tests

The complete primitive exceptional triangle has eight pairs including the
repeated-speed auxiliary (1,1): (1,1),(1,2),(1,3),(1,4),(1,5),(2,1),(2,3),(3,1).
Additional physical controls, fixed now: (1,6),(2,5),(3,2),(3,4),(4,3),(5,2),
(5,7),(3,5), and scaled controls (4,6),(6,10). Total 18 pairs, 17 distinct-speed
configurations. For each, check all seven phases and laps, reflection, and
alternative Bezout pair. Do not add a broad parameter scan or optimizer.

Negative control fixed now: p=2,q=4, native P3 point (x,y)=(7/16,1/4).
It is ambient-safe and qx-py=5/4? This proposed value must be calculated,
not presumed; if it does not give an integer outside dZ, preserve the failed
attempt and derive an explicitly marked replacement analytically.
Also check the tempting clocks t=x and t=y on the declared physical controls,
recording failures without treating success of a wrong clock as equivalence.
Check that removing closed endpoints loses the P1 fallback at primitive (1,4).

## Evidence and work division

Coordinator derives selector and writes a self-contained note. Separate AI
reviewers inspect (a) orbit/gcd/recovery and signs, (b) affine safety and full
parameter coverage, (c) direct physical witnesses using a separately structured
implementation. Reviewers own isolated files in this directory. Exact Fraction
arithmetic only. No finite controls are substituted for the infinite argument.
All general results remain internally reviewed proof candidates; no human or
formal verification is claimed. Preserve corrections and model-adequacy findings.

## Representation/source boundary

The fixed two edges and row labels come from the preserved parent-only discovery
and B-ray transfer packages. The original discovery rule is unchanged; this is
a new analytic coverage argument for its existing edges, not a new frozen-rule
discovery run. The full cell atlas remains the recovery source for stronger
questions. Standard affine convexity, integer rounding, gcd and Bezout identities
are sufficient complementary mathematics here; none is claimed as a CC invention.
No external theorem is imported. Novelty and broader family comparison remain OPEN.
