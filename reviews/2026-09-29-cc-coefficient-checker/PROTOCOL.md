# Reusable coefficient checker — September 29, 2026

Frozen before new implementation or validation runs. Mathematical input head:
57997d4220226b44b9a89d8d8139926f15cca90c. The prior exact classification,
174 finite rejection certificates and large-slope proof remain unchanged.

## Intended interface and guarantee

Add a standard-library module lonely_runner/cc_coefficients.py with a Python
API and `python3 -m lonely_runner.cc_coefficients A B [--p p --q q]` JSON CLI.
Use exact Python integers and rational arithmetic. Accept only positive
integers; bool, float and implicit numeric-string coercion are invalid at
the Python API boundary. CLI decimal integer text is parsed explicitly.
Both optional physical parameters must be supplied together.

Coefficient outcomes are ACCEPTED, REJECTED, or INVALID_INPUT. ACCEPTED means
the fixed first-integer L/C construction meets the closed threshold 1/8 for
all positive integer p,q, with eight-distinct-speed applicability separately
reported. REJECTED supplies a concrete p!=q with eight distinct speeds where
this selector fails. It does not mean absence of another lonely time. Invalid
input, missing resource and internal inconsistency must never become a
mathematical REJECTED verdict. The CLI exits 0 for valid mathematical results,
2 for invalid input, and nonzero for unexpected internal failures.

Acceptance includes shared leader lap/band evidence, C evidence, proof source
and proof-candidate status, the physical recovery recipe and exact distinctness
conditions. Four identically repeated core rows carry an empty distinct-speed
domain flag. Optional p,q evaluation returns the actual selected time, point,
phases, torus/physical laps, unit-period reflection 1-t and domain flags,
even if a rejected coefficient happens to work at that requested pair.

Do not call this a formal prover or a generic untrusted-certificate validator.
Do not introduce discovery, clipping, optimization or a changed contact rule.

## Frozen rejection algorithm

Test the proved whole-L-plus-C inequalities first. If they accept, return
the guarantee. Otherwise use this deterministic precedence, with
delta=A-2B, D=|delta|, a=(2A+3B) mod8 and w=A+2B:

1. w mod8=0: return the C collision at (p,q)=(1,2).
2. a=0: return the left-leader collision at (2,3).
3. Outward boundary (delta>0,a=7 or delta<0,a=1):
   j=max(2,floor(7D/8)+1), (p,q)=(1,4j-2).
4. D>=14: c=7-a for delta>0 or a-1 for delta<0;
   j=floor(7D/[4(c+2)])+1, (p,q)=(1,4j-2).
   Retain the strict forbidden j interval and verify the chosen integer.
5. Remaining D<=13: evaluate the 11 previously extracted directions in the
   original increasing-M/P order:
   (1,2),(1,3),(2,1),(1,4),(1,5),(2,3),(1,6),(3,2),(2,5),(4,1),(1,8).
   Return the first unsafe seventh phase. Completeness is supplied by the
   prior full 216-cell reduction; this is not a new universal fixed menu.

Each returned rejection is checked by direct physical multiplication: all
six core phases safe, seventh distance <1/8, p!=q and eight distinct speeds.
Recompute actual laps for the supplied coefficients. No archived table or
proof-output file is required at runtime. At most 11 bounded contact checks
are used, plus one physical recovery; integer bit cost and gcd/Bezout work
are not constant-time claims. Production checks must survive Python -O.

## Frozen validation scope

1. All 216 old representatives (delta=-13..13, B=b+8, b=0..7) must match
   the archived acceptance verdict. Each accepted certificate is checked;
   every returned rejection is independently recovered and verified. Failure
   directions can differ from the archive because the new precedence is explicit.
2. Repeat those 216 decisions after adding (16K,8K), K=10^20. Verify phase
   invariance, the same decision and rejection direction, and changed exact laps.
   This is an algebraic-periodicity implementation control, not a coefficient scan.
3. Test all b=0..7 for each delta in {-15,-14,14,15,-(10^40+14),10^40+14}.
   Set B=8*(|delta|//8+2)+b, A=2B+delta. These 48 positive rows are all
   outside the accepted range and exercise the analytic branches, both signs,
   strict integer rounding and large exact inputs. Boundary D=13 is in step1.
4. Reproduce exactly the 54 archived progression physical configurations.
   Additional named domain/equality controls use only p,q=(2,3) with rows
   (1,1),(2,1),(3,1),(3,2),(4,5),(23,12), plus the old failure pairs
   (4,2;1,2) and (5,2;2,3).
5. API invalid coefficient pairs: (0,2),(-1,2),(6,0),(6,-2),(True,2),
   (6,False),(6.0,2),(6,"2"),(None,2). Invalid p,q for accepted row (6,2):
   (0,3),(2,0),(-1,3),(2,-3),(True,3),(2,3.0).
6. CLI controls: accepted6,2; rejected5,2; accepted6,2 with4,6; repeated
   core row1,1 with2,3; rejected5,2 with a requested old pair(1,3);
   missing optional q; noninteger 'two'; decimal '6.0'; negative -1.
   Repeat those same CLI cases under -O to check production validation.

No extra physical/coefficient trials unless a concrete bug requires a minimal
regression case, in which case preserve the correction and added scope.

## Review, persistence and claim limits

Coordinator implements the runtime and declared validation. Separate AI review
reconstructs verdicts/physical outputs with coordinate congruences and checks
the serialized records. A second reviewer audits branch totality, rounding,
invalid-input semantics, optimization mode, repeated-speed flags and scope.
Reviewers may read code after independent derivation; record timing accurately.

Save the module, tests and review package on the existing research branch,
preserving prior proofs and concurrent visual work. The classification remains
an internally reviewed proof candidate. No new existence result, novelty claim,
external contact, main merge or unattended work. A changed-rule/geometry
experiment remains a later, separately frozen task.
