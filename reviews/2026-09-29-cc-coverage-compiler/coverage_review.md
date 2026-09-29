# Coverage certificate review — September 29, 2026

Status: PASS for the frozen geometry/coverage scope and four failure controls.
No result-level defect was found; no production correction was requested.
This is a separately tasked AI review. It is not external, human, or formal
verification, and it does not establish novelty or upgrade the proof status.

## Method and exact scope

The numerical reconstruction in `coverage_review.py` imports neither the
compiler nor the preserved discovery implementation. It reads
`PARENT_INPUT.json` and reconstructs the clipped
records by intersecting each old floor edge's supporting line with all seven
forms' upper/lower boundaries, retaining feasible intersections and original
endpoints. This differs from production's affine parameter clipping. The
seventh lap range 0 through 4 follows from the preserved folded box:
7/8 <= 5x+2y <= 17/4. It is not inferred from the desired certificate.

The reconstruction checks all 27 records against the archived records and
rebuilds the descending ranking, strict finite domain, full contact matrix,
and greedy selection. In each projected interval it enumerates the exact
integer set and picks the first integer. No physical parameter scan, optimizer,
new speed family, or new reference runner is used. The separate physical
review owns the declared 18 physical controls.

All emitted geometry fields, including source-edge parameters and lap labels,
match the separate reconstruction. All ranking entries, leader fields, residual
pairs, 216 complete contact records, greedy steps, selected IDs, uncovered list
and counts also match. Input, protocol, compiler and certificate hashes verify.
The parent input is additionally checked against its own pinned richer source.

Only after those numerical comparisons, an isolated subprocess loads the
compiler to exercise the four specified same-input failure controls. It does
not supply any computed geometry or coverage result to the reconstruction.

## Independently reconstructed data

All 24 floor edges yield exactly the same 27 labelled records as the archive.
The checker makes 1,440 supporting-line/band-boundary intersections and checks
378 endpoint phase-band memberships, equivalent to 756 scalar inequalities.
Point records retain their repeated endpoint and closed safety.

There are ten descending candidates. Their ranked rectangle pair counts are
21, 33, 35, 77, 77, 121, 161, 161, 345, and 529, with numerical provenance
breaking ties. The first is `P3:E0-1:K2`, with alpha=1/8 and beta=1/4. The strict
rectangle has 1<=P<=3 and 1<=Q<=7, hence 21 lattice pairs before primitive and
width filtering. It lies within the frozen 400-pair budget.

The exact primitive domain with Q+2P<8 is
(1,1), (1,2), (1,3), (1,4), (1,5), (2,1), (2,3), (3,1).
The first pair is a repeated-speed auxiliary; it is not a distinct-speed
eight-runner configuration.

The 27-by-8 matrix has 216 entries and 50 contacts. Of its entries, 72 have
constant projection and nine of those have integer contact. The leader misses
exactly (1,2) and (1,4). The prescribed greedy rule adds `P1:E1-3:K1`, which
covers both. No pair remains uncovered. This menu agrees with the previously
known construction, but agreement with that answer is comparison evidence,
not a premise in this reconstruction or a minimality result.

## Conditional infinite argument

Let a supplied closed jointly safe segment be oriented with increments
(alpha,-beta), where alpha,beta>0. Along it H=Qx-Py increases by
alpha Q+beta P. If this width is at least 1, the integer ceil(H_min) belongs to
the closed interval, including equality. Affine interpolation locates a point
on the segment, whose seven labelled phases all remain in [1/8,7/8] by
convexity of each closed affine band.

If the width is less than 1, positivity implies P<1/beta and Q<1/alpha. Thus
the integer bounds are exactly ceil(1/beta)-1 and ceil(1/alpha)-1, including
the reciprocal-integer boundary case. Filtering that rectangle by gcd(P,Q)=1
and the strict width inequality enumerates every primitive direction not
covered by the width argument. Width below 1 alone does not mean failure:
the exact projection contact matrix is required.

For primitive (P,Q), an integer H is sufficient for actual torus-orbit
compatibility. If rP+sQ=1, tau={rx+sy} satisfies P tau=x-sh and
Q tau=y+rh modulo integers. For p=dP,q=dQ, t=tau/d is the physical time.
Thus the finite contacts plus the width argument support every positive
direction for this supplied menu. They do not guarantee that an arbitrary
family or candidate class contains a suitable descending segment.

## Failure semantics and limits

`INVALID_CANDIDATE` concerns invalid supplied geometry/labels;
`NO_DESCENDING_SEGMENT` concerns this finite-reduction strategy;
`SCOPE_LIMIT` concerns the declared computation budget;
`UNCOVERED_PRIMITIVE_PAIRS` concerns the menu available to this procedure.
None says that the Lonely Runner assertion fails. The last must list all
missed residual pairs; the width proof already covers the complement.

| Fixed ablation | Separately observed production result |
| --- | --- |
| Supply only non-descending records | `NO_DESCENDING_SEGMENT` |
| Supply only the selected leader | `UNCOVERED_PRIMITIVE_PAIRS`, exactly (1,2) and (1,4) |
| Set rectangle budget to zero | `SCOPE_LIMIT`, zero enumerated pairs and no contact matrix |
| Add one to the leader's first lap | `INVALID_CANDIDATE`, labelled endpoint safety violation |

All four reproduce the archived `run.json` failure summaries. The scope limit
occurs before enumeration. The lap corruption is rejected before ranking.
The evaluator is a consumer of the generated certificate, not a full validator
for arbitrary untrusted certificate files. It checks selected-segment safety
and physical identities when evaluating a time; full global certificate
integrity is checked by this separate reconstruction. Generic schema hardening
or adversarial arbitrary-input testing is outside the frozen task.

Deleting endpoints from the successful menu is a consequential change. At
(1,4), P3's projection is [9/8,15/8], with no integer; P1's is [0,7/12], whose
only integer is the first endpoint. Both open interiors therefore fail even
though the closed menu succeeds. This is loss of a particular sufficient
certificate, not evidence against physical loneliness.

The argument uses the credited threshold adaptation of the Jain–Kravitz
segment-contact mechanism recorded in the literature comparison. Its
optimal-locus and finite-spectrum conclusions are not inherited. Rosenfeld
already covers existence for these seven positive speeds. The present work
concerns assembly and checking of a compact explicit certificate.

Full cells, all safe times and optimization data are omitted from this carrier.
Those omissions are adequate for its one-witness question only. Candidate
failure or a stronger question triggers recovery of the preserved parent/child
atlas; it does not license a negative mathematical conclusion.

### Final interpretation review

Final prose review caught an understatement of `UNCOVERED_PRIMITIVE_PAIRS`:
after a complete contact matrix, each reported pair is missed by every
supplied candidate. No different leader or rearrangement of the same records
can repair that exact candidate-class obstruction. `NO_DESCENDING_SEGMENT`
and `SCOPE_LIMIT` do not establish such insufficiency. The coordinator revised
Section 4 of the synthesis and Section 11 of the representation rules and
preserved the correction in `CORRECTIONS.md`. I re-read those passages: the
distinction is now accurate. This interpretation repair changed no code,
certificate, parameter domain, numerical result, or proof status; no new run
was needed.

## Reproduction and inspected version

Run from the repository root:

```sh
python3 reviews/2026-09-29-cc-coverage-compiler/coverage_review.py
```

The JSON output preserves the full reconstructed contact matrix and source
digests. The reviewed compiler SHA-256 is
`f998170868ebb261f5a9ae431caba3ace3ecd837438246571a591bfc4e616d92`;
the emitted certificate SHA-256 is
`88142d4442d65cb50e8e6068cd1826b5957015ffd2d0742cb6867ab5ab452aa1`.
Rerun the review if either changes. This check uses standard-library rational
arithmetic and assertions; run Python normally, without disabling assertions.
