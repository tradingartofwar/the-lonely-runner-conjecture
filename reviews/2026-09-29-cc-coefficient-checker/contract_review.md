# Coefficient checker: contract and implementation review

September 29, 2026. Separately tasked AI review. This is internal review,
not external human review or formal verification. The reviewer first read
the frozen protocol and the prior selector-support argument and derived
the branch obligations before the runtime module existed. Later code and
declared validation results are reviewed separately below. No additional
coefficient or physical search is authorized by this review.

## Contract derivation before reading implementation

The acceptance predicate is a shared-lap assertion on the whole leading
segment plus the fallback point C. With u=2A+3B, v=3A+B and w=A+2B, let
m=floor(min(u,v)/8). Acceptance is equivalent to

```
8m+1 <= min(u,v) <= max(u,v) <= 8m+7 and w mod 8 != 0.
```

The common m is essential: safe endpoint residues in different laps do not
imply safety of every intermediate point. The first six phases are already
safe at every fixed-selector output. The prior proof candidate identifies
this predicate with uniform success of that selector for all positive
integer p,q. It does not identify the complete lonely-time set or say that
a rejected coefficient configuration has no other lonely time.

For the rejection algorithm, put delta=A-2B, D=abs(delta),
a=(2A+3B) mod 8. The precedence has the following totality argument.

1. If w mod 8=0, the selector uses C at (1,2), where the seventh phase is
   zero. If a=0, its left leader endpoint at (2,3) has seventh phase zero.
2. After these branches, a belongs to 1,...,7. At an outward boundary
   (delta>0,a=7 or delta<0,a=1),
   j=max(2,floor(7D/8)+1) satisfies j>7D/8 and j>=2. The selected sequence
   (1,4j-2) has positive drift magnitude 7D/(32j)<1/4. Thus its phase is
   strictly inside the open unsafe interval surrounding the adjacent integer.
   The strict rounding matters even if 7D/8 is an integer.
3. In the remaining D>=14 branch, c=7-a for positive delta and c=a-1 for
   negative delta satisfies 1<=c<=6. The open forbidden interval for j is
   (7D/[4(c+2)], 7D/[4c]). Its length is 7D/[2c(c+2)]>=7D/96>1.
   Its lower endpoint is at least 98/32>3. Consequently floor(lower)+1 is
   strictly inside the interval and is at least 4. This is valid for both
   slope signs and for integer lower endpoints.
4. All remaining cases have D<=13. Membership and each fixed-direction
   phase depend only on delta and B modulo 8: shifting (A,B) by (16,8)
   changes the seventh raw value by 7 on L and by 4 at C. This identity also
   works for a negative integral shift when both compared coefficient rows
   are positive. The prior exhaustive 216-cell reduction and its extracted
   first-failure directions therefore justify testing the declared 11
   directions in their preserved order. This small menu is not a universal
   finite menu for unbounded D. If the implementation reaches its end
   without a failure after rejecting the acceptance predicate, it has an
   internal inconsistency, not a mathematical rejection certificate.

Every chosen direction has p!=q. Direct physical verification must establish
that the six core phases are safe and the seventh distance is strictly less
than 1/8. These facts also prove that the seventh speed cannot coincide with
a core speed at that time. Thus every rejection is applicable to eight
distinct total speeds, including reference 0. Equality distance 1/8 is safe
and must never be emitted as a rejection.

## Domain and interface obligations

For positive integer p,q, core-speed distinctness is equivalent to p!=q.
The seventh speed is automatically greater than p and q. Its remaining
noncollision conditions are (A-a)p+(B-b)q!=0 for
(a,b)=(1,1),(2,1),(3,1),(3,2). Exactly these four identically repeated
coefficient rows have an empty eight-distinct-speed domain. For every other
row, finitely many nonidentity linear collision equations exclude finitely
many slopes, so positive integer pairs remain available. Accepted guarantees
may include the four repeated rows; their empty distinct-speed domain must
remain explicit rather than presented as an eight-distinct-speed example.

The Python API must reject bool, nonintegers, zero and negative values before
performing mathematical operations. Optional p,q must be supplied together
and independently checked. A requested-pair evaluation is an auxiliary
evaluation of the same fixed selector: success at that one pair cannot
override a global REJECTED result, and repeated speeds at that one pair do
not invalidate an otherwise valid ACCEPTED coefficient guarantee.

Invalid input, missing implementation resources and failed internal checks
are operational outcomes, not mathematical REJECTED results. Production
validation and invariant checks must use explicit conditionals/exceptions
that survive Python -O. Reflection is the declared unit-period time 1-t,
including when gcd(p,q)>1; changing to 1/d-t would preserve phases but would
alter the requested reflected time and lap certificate.

The constant bound concerns at most 11 menu contact checks and the fixed
number of arithmetic branches. Input bit length, integer arithmetic,
gcd/Bezout work and output size are not constant-cost claims. The module is
an implementation of a reviewed proof candidate with explanatory outputs,
not a formal prover or a general validator for arbitrary untrusted
certificates. A pinned mathematical source identifies the proof being
implemented; a runtime source identifier/hash identifies the actual code
executed. Neither proves the other correct.

## Runtime and declared validation review

The delivered runtime `lonely_runner/cc_coefficients.py` was then read in
full. Its SHA-256 at code review was
`ad42e998e49d9fc82f6dc002737c4e8105dab23d09041a4ce6f47340e9ffcde6`.
No contract defect was found by this static review.

- `_positive_integer` requires `type(value) is int` and positivity, excluding
  booleans, floats and coercions. The API raises `ValueError` for invalid
  input; the CLI catches parse/input errors and emits `INVALID_INPUT` with
  exit code 2. Valid ACCEPTED and REJECTED results both exit 0. Unexpected
  computation failures are not caught as mathematical rejection.
- The shared-lap predicate, closed endpoints, all branch signs, strict
  rounding and eleven-direction traversal match the frozen contract. The
  implementation uses exact `Fraction` arithmetic and Python integers.
- `_require` uses an explicit conditional and raises `ArithmeticError`.
  No production gate uses `assert`, so Python optimization cannot strip
  these checks. This conclusion follows from code inspection, separately
  from the declared optimized CLI executions.
- `evaluate_selector` normalizes p,q, checks Bezout and the orbit identity,
  recovers physical time and recomputes every torus lap. It compares derived
  physical laps and phases with direct multiplication. Reflection uses 1-t,
  direct floors and an explicit zero-aware phase/lap relation, including
  a rejected seventh phase equal to zero.
- Distinctness is checked both by the actual speed set including 0 and by
  the stated collision conditions. Rejections require core safety, seventh
  failure, exactly failed runner 7 and eight distinct speeds before return.
- The CLI adds `requested_evaluation` after the coefficient decision. It
  does not change the global status based on a requested-pair success or
  repeated-speed auxiliary. The domain flags remain attached to the global
  result.
- The code imports only the standard library and does not load an archived
  classification, output or proof file. `PROOF_COMMIT` and `PROOF_NOTE`
  identify the earlier mathematical source, not this newly written runtime.
  Runtime provenance is the code hash above and the package manifest.

The reviewer then read `tests/test_cc_coefficients.py`, `validate.py` and
the completed `validation.json`. The test inputs match the frozen protocol:
216 archived coefficient representatives, their 216 specified periodic
shifts, 48 analytic-branch inputs, 54 archived physical configurations,
eight named physical/domain controls, 15 invalid API calls and nine CLI
commands each in normal and optimized mode. No new coefficient or physical
trial was introduced by this reviewer. The reviewer inspected the stored
records and confirmed that every recorded input/procedure provenance hash
matches its current file, including the runtime hash above.

The recorded five unittest methods pass. There are 84 accepted and 396
rejected coefficient decisions among the 480 cases. The rejection counts
are 200 bounded-direction, 56 fallback-collision, 54 leader-start-collision,
50 outward-boundary and 36 large-slope certificates. Every declared branch
is therefore exercised. The accepted and rejected counts include the
specified periodic repetitions and must not be described as 480 new
coefficient classes.

The tests verify accepted endpoint values against their common lap, actual
fallback phases, direct physical multiplications, strict rejection and
distinctness, all declared archived physical fields, changed exact laps
under the large periodic shift, and the strict large-slope integer interval.
The named domains preserve all four repeated-core rows and the closed
boundary controls. The stored CLI results show (5,2) globally REJECTED while
its requested (1,3) output is safe; (1,1) is globally ACCEPTED with an empty
distinct-speed domain and its requested (2,3) output explicitly repeats a
speed. These are different outcomes and are serialized without conflation.
All nine CLI outputs and exit codes agree between normal and Python -O
execution, including invalid inputs. The independent coordinate-congruence
reconstruction belongs to the separate `audit.py` review, not to this
contract review's test execution claim.

**Conclusion:** no contract or implementation defect was found within this
review. The mathematical totality argument is inherited from the earlier
proof candidate and the branch derivation above; passing finite software
controls does not promote it to an established theorem. The implementation
keeps global scope, physical applicability, requested-pair behavior and
operational errors separate. The existing representation is adequate for
this fixed-selector decision. A changed contact rule or geometry requires
a new adequacy check and is outside this package.
