# Marginal ceiling and signed-residual overlap arithmetic

**Date:** September 28, 2026. **Status:** HYPOTHESIS/proof-candidate review of the general arithmetic; no novelty claim. This materially AI-generated audit does not establish arbitrary-speed existence or independently certify an unbounded theorem. Its input is the frozen protocol, not benchmark outcomes.

Protocol: `protocol.json`, SHA256 `36ef24405de801a114e11325d30fe0b5f2d855e71441e5c4478047aa15b82d8e`. Baseline recorded by that protocol: `539dd899ac8ceea5b50d46b72c0fa28cec7a354e`. Only this report is owned by the arithmetic reviewer; no new cases, implementation, cutoffs, or full allowed sets are supplied here.

The fixed setting is eight common-start runners, selected reference zero, threshold \(\delta=1/8\), and distinct positive integer nonreference speeds. The core is supplied. The protocol selects its widest positive closed safe component \(J=[\alpha,\beta]\), with the stated earliest-left-endpoint tie rule, before inspecting residual blocking. Let \(L=\beta-\alpha>0\).

## 1. What the marginal ceiling proves

For the four residual speeds, let \(B_i\subset J\) be their strict blocking sets, \(D_i=|B_i|\), \(O_{ij}=|B_i\cap B_j|\), and

\[
E=\sum_i D_i-L.
\]

The single-pair grouping inequality is

\[
U_J=L-\left|\bigcup_i B_i\right|
\ge L-\sum_iD_i+O_{ij}=O_{ij}-E.
\tag{1}
\]

It follows by grouping \(B_i\cup B_j\) first and applying the union bound to that union and the other two sets. It does not sum several pair overlaps and therefore does not overcount triple or quadruple intersections.

Every pair satisfies the universal marginal upper bound

\[
O_{ij}\le C_{ij}:=\min(D_i,D_j).
\]

Consequently, on this fixed window,

\[
\max_{i<j}(O_{ij}-E)
\le C_*-E,
\qquad C_*:=\max_{i<j}C_{ij}.
\tag{2}
\]

If the durations in descending order are \(d_1\ge d_2\ge d_3\ge d_4\), then \(C_*=d_2\): no pair has a smaller member greater than \(d_2\), and the pair attaining \(d_1,d_2\) attains that cap. The protocol's six scalar caps and numerical tie rule specify a deterministic pair even when several durations agree.

This justifies the three branches before any overlap query:

- If \(E<0\), singles already give \(U_J\ge-E>0\); querying a pair is unnecessary.
- If \(E\ge0\) and \(C_*\le E\), every single-pair bound in (1) is nonpositive. No overlap query could produce a positive certificate of that form on this \(J\).
- If \(E\ge0\) and \(C_*>E\), a positive single-pair bound is possible according to the marginals. It is not guaranteed for the selected pair, or for any pair.

For the selected cap-maximizing pair, define its cap surplus and cap loss by

\[
S=C_*-E>0,\qquad Q=C_*-O_{ij}\ge0.
\]

Then its actual certificate value is exactly

\[
O_{ij}-E=S-Q.
\tag{3}
\]

The surplus is the overlap loss that the selected pair can tolerate, not a predicted clear duration. Success requires \(Q<S\); equality gives a zero lower bound. Ranking by cap maximizes an upper bound on the queried score, not the score itself. Even the largest feasible cap can lose too much through placement.

The inequality \(O_{ij}\le\min(D_i,D_j)\) can be attained by arbitrary measurable sets when the smaller is contained in the larger. That explains the cap's marginal meaning; it does not assert such containment for these runners. Conversely, \(C_*\le E\) says nothing by itself about whether \(U_J\) is positive or whether a valid equality time exists. Redundancy can be distributed among several relationships. The existing [core-transfer study](../../notes/CORE_TRANSFER.md), Sections 6–8, already separates these possibilities. No actual-duration claim follows from a failed cap test or a failed chosen-pair query.

Individual durations require only endpoint primitives. For \(z\ge0\), set

\[
\mathcal C(z)=\frac{\lfloor z\rfloor}{4}
 +\min(\{z\},1/8)+\max(0,\{z\}-7/8).
\]

Then

\[
D_w=\frac{\mathcal C(w\beta)-\mathcal C(w\alpha)}{w}.
\tag{4}
\]

Thus the cap test uses four exact single-duration calculations, eight endpoint evaluations, and six scalar minima. It does not require any pair overlap or the full seven-runner allowed set.

## 2. Signed residual strips for the chosen pair

Only after the pair \(a<b\) is selected, choose \(h\in\{1,2\}\) minimizing

\[
(|b-ha|,h)
\]

lexicographically, and put \(r=b-ha\). This chooses an evaluation representation. Neither \(h\), \(r\), nor a model phase area participates in the frozen pair ranking.

If runner \(a\) blocks, there is a unique integer \(j\) with

\[
x=at-j\in(-\delta,\delta).
\]

Because \(bt=h(at)+rt\), simultaneous blocking is equivalent to an integer \(m\) such that

\[
|x|<\delta,\qquad |hx+rt-m|<\delta.
\tag{5}
\]

For fixed \(t\), the permissible fast phase is

\[
\ell(t)<x<u(t),\qquad
\ell(t)=\max\left(-\delta,\frac{m-\delta-rt}{h}\right),
\quad
u(t)=\min\left(\delta,\frac{m+\delta-rt}{h}\right).
\tag{6}
\]

Positive width requires \(|rt-m|<(h+1)\delta\). Since \((h+1)\delta\le3/8<1/2\), at most one integer \(m\) can have positive width at a given time. Where none does, simultaneous strict blocking is impossible. Thus no extra summation over competing phase strips at a single time is omitted.

Temporarily allowing \(x\) to vary, the width is

\[
K_{h,r}(t)=
\max\left(0,\min\left(\frac{2\delta}{h},
 \frac{(h+1)\delta-\|rt\|}{h}\right)\right).
\tag{7}
\]

For \(h=1\), this is \((1/4-\|rt\|)_+\). For \(h=2\), it is the existing clipped trapezoid
\(\min(1/8,\max(0,(3/8-\|rt\|)/2))\).
Its integral is a model phase area, not actual overlap duration: the common-start trajectory has the specific fast phase \(x=at-j\). In particular, changing \(r\) to \(-r\) preserves (7), while the endpoint correction below need not be preserved.

For \(r\ne0\), split \(J\) at the relevant events

\[
rt=m\pm(h+1)\delta,
\qquad
rt=m\pm(h-1)\delta.
\tag{8}
\]

The first pair enters or leaves positive support; the second pair switches a maximum or minimum in (6). For \(h=1\), the two inner events coincide at \(rt=m\) and must be deduplicated. Add \(\alpha,\beta\), sort chronologically even when \(r<0\), and discard zero-width or zero-length pieces. On every surviving piece, both endpoints in (6) are affine, with slopes drawn from

\[
0,\quad -r/h.
\tag{9}
\]

No event division by \(r\) is used when \(r=0\). That case has one constant positive strip, \(m=0\), with

\[
\ell=-\delta/h,\qquad u=\delta/h.
\tag{10}
\]

Distinct \(a<b\) excludes \(h=1,r=0\), so the actual zero-residual branch is exact doubling \(h=2,b=2a\). It must not be skipped as an empty event list.

## 3. Exact periodic endpoint correction

This extends the endpoint primitive already used in [OVERLAP_PLACEMENT.md](../../notes/OVERLAP_PLACEMENT.md), Section 7. On one positive affine piece \([A,B]\), the simultaneous-blocking indicator, except at threshold boundaries, is

\[
\lfloor at-\ell(t)\rfloor-\lfloor at-u(t)\rfloor
=(u(t)-\ell(t))+
\{at-u(t)\}-\{at-\ell(t)\}.
\tag{11}
\]

The strip width is less than one, so this integer count is zero or one. Let

\[
P(z)=\tfrac12\{z\}(\{z\}-1).
\]

The periodic extension is continuous, has range \([-1/8,0]\), and has derivative \(\{z\}-1/2\) away from integers. For an affine endpoint \(f(t)=st+d\), define

\[
W_a(f;A,B)=
\frac{P((a-s)B-d)-P((a-s)A-d)}{a-s}.
\tag{12}
\]

The denominator is always positive:

\[
a-s\in\{a,a+r/h\}=\{a,b/h\}\subset(0,\infty).
\tag{13}
\]

This is the necessary signed-residual check. When \(r<0\), the moving phase endpoints have positive slope, but that slope is still less than \(a\), since the other physical speed \(b\) is positive. An implementation must not assume that all endpoint slopes are nonpositive or replace \(r\) by \(|r|\) inside (6) or (12).

Integrating (11), with the two \((B-A)/2\) terms cancelling, gives the exact selected-pair duration

\[
\boxed{
O_J(a,b)=
\sum_{[A,B]}
\left[
\int_A^B(u(t)-\ell(t))\,dt
+W_a(u;A,B)-W_a(\ell;A,B)
\right].
}
\tag{14}
\]

The integral on each piece is an exact trapezoid area. Its sum alone is \(\int_JK_{h,r}\), whereas the \(P\)-terms recover actual common-start alignment. Formula (14) handles both signs of \(r\) and the constant strip (10). It need not construct any individual fast blocking interval.

Threshold exceptions to (11) occur only at finitely many times: the affine arguments have strictly positive slopes (13), and \(J\) is bounded. They therefore do not change duration. This measure-zero convention does not discard valid threshold times from the protocol's separate closed endpoint test. At a support boundary, \(u=\ell\) and the strip contributes zero duration.

## 4. What the evaluation cost means

The coordinate \(rt\) ranges over an interval of length \(|r|L\). Only integers within \((h+1)\delta\) of that interval can contribute a positive strip. Their number is \(O(1+|r|L)\), and each contributes at most four event values in (8). Thus the number of affine pieces and primitive evaluations in (14) is

\[
O(1+|r|L).
\tag{15}
\]

For \(r=0\), it is constant. Each positive piece needs two endpoint corrections, hence four uncached evaluations of \(P\), plus constant rational arithmetic for its area. Shared endpoints may be cached, but the reported count must follow what the implementation actually does.

Equation (15) is an operation/count statement, not a bit-complexity or measured runtime claim. The rational operands still contain \(a,b\), the core endpoints, and residual event denominators. A generic sort of all events adds its usual sorting cost; linear event ordering is possible by merging the fixed number of arithmetic progressions in (8). The full policy also pays for constructing the supplied core's complete closed safe set and for any endpoint fallback. Those costs are not included in (15).

A small residual can make a selected pair inexpensive to evaluate even when its gcd is small. A large residual can leave many pieces, and choosing \(h\) by smallest \(|r|\) does not prove that it minimizes every cost or makes the pair useful. No uniform runtime advantage or success guarantee follows merely from making one overlap query.

## 5. Review conclusions and finite scope

The marginal rejection test \(C_*\le E\) is valid before any overlap query and rejects only the possibility of a positive bound of form (1) on the selected window. Positive cap surplus is necessary for such a bound, but is not sufficient. The canonical residual representation affects evaluation only. Formula (14) preserves placement that model phase area omits, with no sign or zero-residual obstruction under the stated positive-speed assumptions.

The existing core-transfer zero-area window illustrates why model feasibility must not be confused with actual overlap or final clearance; it is background counterpressure, not a selector input. The frozen protocol may terminate with a failed policy despite actual lonely times elsewhere or even inside its selected window. Endpoint fallback is separately needed to distinguish an equality witness from a duration certificate. These distinctions are part of the claim, not exceptions to it.

This report reviews the symbolic evaluator and cap argument only. Exact values for the ordered six controls, stop position, event counts, and primitive counts belong to the primary output and its separately structured verifier. No additional speed cases, alternative pair ranking, fallback search, or cutoff derivation was performed for this audit.
