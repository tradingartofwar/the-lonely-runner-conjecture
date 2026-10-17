# One exact model, several question-specific views

October 17, 2026. Incorporates the maintainer's proposal to investigate
representation choice alongside the runner-addition work. Source state:
`a74bf46a4d96e554b50e71ea191cc8223253beb5`.

The objective is to discover checkable explanatory relationships by organizing
the same exact facts differently. Binary is an encoding. Its interpretation
requires named objects, relationships, assumptions, operations, and recovery
links. We use existing interval, Boolean, modular, and event representations;
a new LTCM is an option only if a demonstrated operation requires one.

## Shared objects and meaning

Every record identifies the ordered integer speeds, reference 0, common start,
threshold, physical period [0,1], exact rational arithmetic, input identity and
source commit. Component IDs index the complete ordered closed core-safe set.
Each component stores endpoints and constant core laps; a singleton remains an
object. Added-speed IDs are actual integer r values, not arbitrary array labels.

For each finite r, complete child-safe sets and per-component intersections
retain all possible witnesses. A stored time has its original speed ordering,
phases and laps. These links connect derived views to physical motion.

| View | Supported question/operation | What is omitted | Recovery |
| --- | --- | --- | --- |
| Complete interval geometry | All safe times; intersect another constraint | Per-runner reasons outside the safe set | Original predicates and event states |
| Center and half-width | Does r block this entire component, and in which unsafe gap? | Other components unless included | a=c-h, b=c+h; exact reversible coordinates |
| Component/speed Boolean incidence | Does this component supply some time for r? Select a cover | Location of that time, surviving subintervals, phase detail | Keyed component intersections and full child set |
| Ordered per-runner event states | Which conditions hold simultaneously at a time or throughout an open cell? | Detailed phase values between events | Speeds and exact clock; recompute phase and lap |
| Selected menu and dispatcher | Produce one witness for each admissible r | Most safe times and optimum | Complete components and intersections |

The incidence bit at (I,r) means `exists t in I: every fixed-core condition and
the r condition hold at t`. A per-runner time bit has a different meaning:
`the specified runner's condition holds at this same time`. All runner bits
must be conjoined before eliminating time. Separate existential bits cannot be
conjoined to justify simultaneous satisfaction of two added constraints.

Bit ordering is explicit: bit i in a numeric component mask represents component
i; a displayed bit string lists IDs 0,1,... from left to right (least significant
bit first). Component case masks use the saved ordered list of finite r values.
Time masks use the saved ordered speeds, including the added runner last.

## Operations and guards

- Core construction and child intersection preserve closed boundaries and
  isolated points. A failed component is not an empty complete safe set.
- Endpoint-to-center conversion is lossless. Thresholding the placement
  predicate or existentially eliminating time is a question-specific summary;
  an inverse is not assumed.
- For I=[a,b], c=(a+b)/2 and h=(b-a)/2, the exact contact test is
  `distance(r*c, integers)+r*h >= d`. Failure has integer certificate
  `r*b-d < m < r*a+d`, hence I lies strictly inside ((m-d)/r,(m+d)/r).
  This quantity decides existence; it is not generally maximum loneliness.
- For a selected menu, all its finite failure sets must have empty intersection.
  The required widest component handles the infinite tail by its width bound.
  A complete finite domain and verified tail hypotheses are prerequisites for
  the family-wide conclusion.
- Event times and open cells are separate records. Boolean states are constant
  on each open cell; lap labels need not be constant on a cell where a runner
  remains unsafe while passing an integer. Recover phases/laps from time.
- A new threshold, core, reference, added constraint, or requested output changes
  the obligation. Recover the rich source and recheck before composition.

## What this study can add

Use coverage to select sufficient collections. Use placement to expose their
complementary failures, and event states to identify the constraints opening or
closing one saved opportunity. Attempt a simple dispatcher when an exact common
repair point exists; retain the ordinary exact contact dispatcher otherwise.

Evaluate demonstrated operations and counterexamples, not naming, apparent
simplicity, or raw bit count. This is not a human-readability experiment, a
runtime comparison, a general semantic platform, or a novelty claim. Both code
paths are by the same AI author; proof candidates await independent review.
