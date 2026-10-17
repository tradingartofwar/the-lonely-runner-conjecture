# Runner addition: exact opportunities and sufficient explanations

Started October 17, 2026. Branch: `research/runner-addition-2026-10-17`.
Base: `f2126bfe929aae4eda77b4ea3418a4c38b47f0f5`.

## Purpose

Use code to investigate which exact safe opportunities survive an added runner,
and turn a finite calculation plus a justified tail bound into an inspectable
argument for a specified family. The measure of advancement is what can now be
reliably represented, understood, or done. Solving the general conjecture is not
the success condition of this bounded study.

The October 17 framing adds three requirements to the October 2 pending work:

- Do not require a single formula or a fixed small explanation. Permit multiple
  components and case distinctions, recording the complexity actually used.
- Compare the historical stronger threshold 1/8 with the actual ten-runner
  threshold 1/10. Failure at 1/8 is not failure of Lonely Runner.
- Remain open to another LTCM (Languages That Carry Models), an adaptation, or
  a missing operation. A proposed language earns its place through a concrete
  checkable capability. CC is one experimental approach, not a mandatory format.

Necessary structure may be extensive; a better representation may also simplify
it. Neither incompressibility nor a general advantage of AI is assumed. The
human-facing account may be short while exact models and evidence retain detail.
AI agents' agreement is not a proof certificate.

## First bounded study

Common-start speeds are

`(0,p,q,p+q,2p+q,3p+q,3p+2q,6p+2q,3p+8q,r)`.

Use only `(p,q)=(1,2)` as an exposed control and `(1,4),(1,6)` as the two
previously proposed follow-ups; r is a positive integer distinct from the eight
core speeds. Only the stationary reference is investigated. This is not an
all-reference result or arbitrary three-parameter coverage.

The source class consists of connected components of the complete core-safe set.
Fix its widest positive component (earliest start breaks ties), then find the
minimum sufficient menu **containing that leader**, within a declared budget.
This removes the earlier success requirement of at most two sources while still
answering that historical question. It does not compute an unrestricted minimum
over all leaders or an intrinsic information/algorithmic lower bound.

Read [PROTOCOL.md](PROTOCOL.md), [protocol.json](protocol.json), and
[DERIVATION.md](DERIVATION.md). `inputs.json` freezes complete cores and the exact
matched finite inputs before any new r evaluation. Code and dependency hashes
will be published before evaluation. Results and later interpretations will be
separate files; the protocol will remain unchanged.

## Prior evidence and provenance

- [Pending decisions and limits](../../reviews/2026-10-02-ultra-value-review/math_audit.md)
- [Existing all-r control and value review](../../notes/ULTRA_VALUE_REVIEW_2026_10_02.md)
- [Orbit interval derivation](../../reviews/2026-10-02-cc-orbit-intervals/DERIVATION.md)
- [Exact checker](../../lonely_runner/checker.py)
- [CC representation contract](../../notes/CC_REPRESENTATION_RULES.md)
- [Internal reconstruction correction, October 3](https://github.com/tradingartofwar/representation-science/blob/main/records/RR-LR-005-internal-reconstruction.md)

The mathematical arguments remain proof candidates pending independent review;
novelty is unassessed. Implementation and alternate verification in this study
are by the same AI author using different algorithms. No external application,
speed advantage, general complexity law, or breakthrough is presumed.
