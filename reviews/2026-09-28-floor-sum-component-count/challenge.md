# Adversarial review: Euclidean floor-sum component counter

September 28, 2026 UTC. Reviewed against the frozen protocol (SHA256
`a398539b747b9510259e5a134090f3eb6430370588d735bdec12f67260ec5724`), the
prior lap-band artifact, the cached interval selector artifact, and the current
primary and independent verifier. This is internal AI review, not independent
human mathematical validation.

## Verdict

**PASS after preserving the qualifications and one prior-note correction
below.** I found no algebraic, strict-boundary, signed-offset, or recurrence
defect in the frozen counter. The primary's 24 counts follow from an exact
half-plane difference, and its Euclidean recurrence terminates with the
standard decreasing-modulus structure. The separate verifier agrees on all 24
pairs after scanning 410 lattice points and reconstructing 287 open event
cells; it compares 173 primary fields and checks both signs of equality
contact.

The cost outcome is mixed and mildly negative at the present scale. Across all
24 pairs the floor-sum implementation uses 65 Euclidean rounds versus 63 lap
rows. On the four active selector-charged pairs it uses 12 rounds versus 7
rows. Only the six `doubling_112` diagnostics show the intended loop-count
reduction, 28 rounds versus 39 rows. These are unlike primitives, so even the
last comparison is not a runtime result. The new representation removes the
speed-dependent *lap-row loop* but does not establish lower runtime, a cheaper
selector on these small active cases, or a uniformly better operation count.

## 1. Open-strip algebra and strict endpoints

For integer

`D = 8*b*m - 8*a*n` and `S = a+b`,

the inherited strict band

`|b*m-a*n| < (a+b)/8`

is exactly `-S < D < S`. Since `D` is integral, this is

`-S+1 <= D <= S-1`.

If `H(K)` counts points in the already-derived inclusive lap rectangle with
`D<=K`, then

`H(S-1)-H(-S)`

keeps precisely `-S<D<=S-1`. The apparent asymmetry is mandatory: subtracting
`H(-S)` removes equality at the negative boundary. Using `H(S)-H(-S-1)` would
incorrectly include both equality contacts.

The two exact attacks at `(a,b)=(3,5)` cover both signs:

- `(m,n)=(1,2)` gives `D=-8=-S` and contact only at `t=3/8`;
- `(m,n)=(2,3)` gives `D=+8=+S` and contact only at `t=5/8`.

Both have zero length and are correctly excluded. The transformation therefore
does not turn an isolated equality point into a positive component. In
particular, it does not absorb the separate `tight_13` equality at `3/8`.

The lap rectangle also keeps the earlier strict participation conversion:
integers in `lower<q<upper` are
`floor(lower)+1 <= q <= ceil(upper)-1`. No boundary is relaxed when the strip
count is introduced.

## 2. Clipping identity and signed offsets

For a fixed `m`, `D<=K` is

`n >= ceil((8*b*m-K)/(8*a))`.

Writing `A=8*b`, `Q=8*a`, and `B=-K+Q-1` gives the integer-valued below-threshold
count before clipping as

`x(m) = floor((A*m+B)/Q)-n_min`.

The `+Q-1` is valid for signed numerators because Python's `//` is mathematical
floor division. Since `x` is nondecreasing and integral, `clamp(x,0,N_n)` must
be split at the first `x>=1`, not at the first `x>=0`, and at the first
`x>=N_n`. The primary uses exactly

`first_ge(z)=ceil((Q*(n_min+z)-B)/A)`

for `z=1,N_n`, clipped to the half-open `m` range. This handles empty middle
ranges and immediate saturation without a hidden lap scan.

For a nonempty middle range beginning at `m_0`, the shift
`A*m_0+B` may be negative. The code applies one mathematical quotient/remainder
normalization before entering the nonnegative recurrence, so the normalized
offset lies in `[0,Q)`, while the possibly negative quotient is restored in the
range sum. Exhaustive direct checks of the recurrence on signed shifted offsets
also agreed with literal sums; the repository verifier independently checks
the resulting half-plane totals by the transposed, fixed-`n` identity.

## 3. Euclidean recurrence and termination

Each recurrence round first removes any coefficient and offset quotients. It
then has `0<=coefficient<modulus` and `0<=offset<modulus`. If
`coefficient*n+offset<modulus`, it terminates. Otherwise the reciprocal step
sets the next modulus to the old reduced coefficient, which is strictly smaller
than the old modulus. A zero reduced coefficient cannot reach that reciprocal
step, because then the reduced offset is already below the modulus. Thus there
is no division-by-zero path, and termination is the ordinary Euclidean descent.

The primary has no per-`m` or per-`n` loop in the count. This should be stated
as removal of coordinate iteration, not as removal of geometry: the rectangle,
strip, saturation thresholds, and half-planes are the overlap geometry in
arithmetic form. Bit complexity and the cost of transformations on large
integers are not measured here.

## 4. Exact cost reading

The frozen ledgers give:

| Scope | half-plane calls | threshold ceil divisions | range calls | Euclidean rounds | recurrence quotients/remainders | prior lap rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all 24 pairs | 48 | 96 | 29 | 65 | 107 / 107 | 63 |
| four active selector pairs | 8 | 16 | 5 | 12 | 20 / 20 | 7 |
| six `doubling_112` diagnostics | 12 | 24 | 12 | 28 | 49 / 49 | 39 |
| fourteen ineligible audits | 28 | 56 | 12 | 25 | 38 / 38 | 17 |

There are also 24 strip subtractions overall, 29 signed normalizations, and one
terminal comparison per Euclidean round. The ledger deliberately does not add
these unlike operations into a score. It also omits a wall-clock benchmark and
does not charge every fixed multiplication, addition, clipping comparison, or
fixed division by two. It is therefore an inspectable recurrence ledger, not a
complete machine-operation or runtime model.

The archived interval ledger is likewise only a side-by-side comparison. For
the four active pairs it records 38 lap candidates, 17 blocking pieces, and 13
join steps; for the doubling diagnostics it records 126, 93, and 87. Those
objects and comparisons are not commensurate with Euclidean rounds or integer
divisions. Moreover, the archived implementation caches each completed pair
intersection for later containment use, but reconstructs runner blocking lists
inside each eligible-pair call; its totals are not the cost of an optimized
runner-level shared cache. No winner should be inferred from either ledger.

## 5. Information barrier and interpretation limits

The primary initially parses the prior lap-band result only to project speeds,
windows, and inherited eligibility, then deletes that object. It fixes all 24
counts and all four branch records before reloading archived counts, decisions,
outcomes, and costs. This is a meaningful code-dependency barrier, not literal
epistemic blindness: the cases and their development history were already
known, and eligibility itself is inherited rather than rederived from a new
minimal source.

The exact matches are bounded observations on four frozen windows. The general
half-plane/floor-sum derivation is an AI-assisted elementary proof candidate
conditional on the prior lap-band component bijection. It is a classical
floor-sum transformation of the repository's existing arithmetic lap
compatibility, not a novelty claim. It adds no Lonely Runner coverage and no
held-out evidence for the fewest-components selector.

Use “four archived branch records,” not “four selections”: target and
`strict_16` are active selections, `doubling_112` is diagnostic after an
independent pair-only-positive exit, and `tight_13` has no eligible pair and
returns `None`.

## 6. Correction to inherited prose

During this review, section 4 of
`notes/LAP_BAND_COMPONENT_COUNT_2026_09_28.md` was found to say that the four
active selector pairs contain four compatible lap pairs. The archived data and
its own tables show six:

- target: counts `1+3=4`;
- `strict_16`: counts `1+1=2`;
- total: `4+2=6`.

The seven active `m` rows are correct. This was a prose transcription error,
not a change to any pair count, selection, or certificate. The prior note now
records the correction explicitly rather than propagating the value four.

## Required before finalization

- Preserve the mixed cost outcome: `12>7` on active pairs, `65>63` overall,
  and `28<39` only on doubling diagnostics, with the unlike-unit warning.
- Do not describe `tight_13` as a selection or `doubling_112` as an active
  selector success; use branch-record language.
- Preserve the recorded correction of the inherited active compatible-lap
  total from four to six.
- Keep both `D=-S` and `D=+S` equality controls and the strict lap-window
  conversion in the note.
- Describe the information barrier as a dependency/order barrier and the
  interval cost as the archived implementation's exact ledger, not an
  optimized runner-level cache.
- Make no runtime, asymptotic bit-complexity, novelty, held-out validation, or
  whole-configuration claim.
