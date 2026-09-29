# LTCM one-parameter spectrum protocol
Date: 2026-09-29. Base research commit: 4c4d370d0bb9b97e47eca9e9260d64beac1502ef.
User authorized the proposed bounded analytical test. No hourly resumption.

## Fixed question and family
Eight total common-start runners, selected reference 0.
Moving speeds V(q)=(1,q,q+1,q+2,q+3,2q+3,2q+5), integer q>=2.
M(q)=max_{0<=t<=1} min_{v in V(q)} ||vt||.
Target: exact witness selection and matching global upper bound on an infinite branch, preferably the whole ray. General deductions remain proof candidates pending independent review; no novelty claim.

## Method declared before running any family calculations
Use two coordinates x=t mod1,y=qt mod1. The seven fixed integer linear forms have rows
(1,0),(0,1),(1,1),(2,1),(3,1),(3,2),(5,2).
Keep the actual-orbit condition qx-y=h with h integer.
By reflection restrict x to [0,1/2]. Use closed safe inequalities at a baseline 1/8; retaining equality is mandatory. A fixed coefficient arrangement can be explored exactly, independently of q, by clipping finitely many lap cells in (x,y). Within each, attach separation z with inequalities z<=linear_form-lap<=1-z.
Proposed selector: intersect the actual-orbit planes with the fixed three-dimensional cell polytopes. The maximum z on any such plane lies at a polytope vertex or on an edge. Along an edge z is affine; only an extremal admissible integer value of qx-y can maximize z. Thus floor/ceiling choices at fixed edge endpoints should give a finite candidate list whose size is independent of q.
This assertion must be proved, including constant projections, horizontal edges, cell boundaries, and isolated equality. It must not silently replace actual-orbit intersection by ambient feasibility.

## Bounded computations allowed in this cycle
1. Exact construction of this ONE fixed ambient arrangement; no variation of coefficient rows.
2. Once a symbolic formula/selector is derived, exact validation only for q=2,...,25 (four cycles modulo6) and q=100003,100004 as large-parameter witness checks. Whole-period exhaustive maxima for the large parameters are excluded.
3. Independent validation structure: direct one-dimensional tent-breakpoint envelope or opposing-contact enumeration for q=2,...,25, distinct from the ambient construction.
4. No other speed families, phases, references, broad q scan, automated research, or paid compute.
Analytical parameter deductions are unrestricted within this declared family. Any additional exact computation must be justified by a concrete remaining risk and recorded separately before execution.

## Success / stop criteria
Success: explicit formula or finite floor/residue selector with proof of exact optimality on an unbounded declared domain, original common-time witnesses, equality-safe semantics, and a q-independent symbolic branch budget. Existing polyhedral/relative-spectrum precedents must be credited.
Also useful: a precise mathematical failure of the declared selector, preserved as a limitation.
Finite agreement alone, ambient safe points, another supplied witness, or ordinary known eight-runner existence do not pass.

## Tiny language
A cell carries integer lap labels, closed constraints, and endpoint status.
A transfer carries a reconstruction of physical time.
A selector carries a coverage proof and a bound on its number of branches.

