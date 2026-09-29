# Compatibility Calculus visual companion

**Six connected sections:** **from cap to clock**, **true somewhere versus true together**, **what the model remembers**, **what survives the cut**, **one safe time**, and **one shared clock**.

Open [presentation.html](presentation.html) in a modern browser. It is a
self-contained offline file: no backend, network dependencies, font download,
or build tooling is required to view it. A static server also works:

```bash
python3 -m http.server 8000 --directory visuals/compatibility-calculus
```

Then open `http://localhost:8000/presentation.html`.
Choose **02 · True together** for the q=4 section. The URL fragment `#joint`
opens that chapter directly when serving or opening the local file.
Choose **03 · What the model remembers**, or open `#representation`, for six
question-specific representation records and their information-loss controls.
Choose **04 · What survives the cut**, or open `#transfer`, for the parent–child
geometry and physical recovery scenes.
Choose **05 · One safe time**, or open `#selector`, to run the two-segment
selector one test at a time.
Choose **06 · One shared clock**, or open `#clock`, to compare merged runner
rows with labelled blocking occurrences at the same exact physical time.

## What this version does

Select one of six B-ray controls, lower a triangular section from a cap peak,
and follow the exact interval under `H=x-qy`. At the first integer contact,
recover `t=y`, all seven phases, physical laps, and limiting distances. The
reflection switch uses `1-t`. Constant branches are already compatible at
the peak and explicitly have zero loss. The residue-3 control keeps both
winning folded caps without counting their reflected times twice.

Rotate/tilt the cap or reveal the complete ten-cell atlas. Three singleton
cells remain visible as hollow points. The coordinate picture exaggerates z
by a declared factor of four; fractions, not screen lengths, are authoritative.

The second chapter follows three steps: separate H/S ranges, the false
combined pair, and the conditional S interval on the same H=1 slice. An exact
inverse map and physical phase table expose which original constraint fails
when the marginals are combined. A slider then moves along the valid parent
slice, including its closed endpoints and the collision at t=4/13.

This is A-ray q=4 with its own clock t=x, explicitly distinct from the first
chapter's B ray. The scene rejects only parent P2 at height 1/8; the four
isolated full-system witnesses remain displayed and verified.

The third chapter lets the reader select six questions: B-ray optimal value
or every maximizing time; A-ray one witness, the entire safe set, same-slice
survival after a new constraint, or every optimizer after transfer. Each has
a matching representation record: retained information, deliberate omissions,
recovery trigger and pinned source. A branch map keeps A/B clocks distinct.

Each question also has an explicit reduced-record comparison. Removing an
upper bound leaves attainment without optimality; removing contact identity
leaves a value without its time set; opening the two q=4 selector segments
loses their only integer contact; keeping only positive-duration components
loses all four final q=4 witnesses; separate marginals create the preserved
false positive; keeping old q=10 edges loses 17/35 and 18/35 while retaining
six other maximizers. These are distinct failures of distinct requested outputs.

The fourth chapter shows three exact parent-to-child transformations, each
with before, after and recovery stages:

- **P2 at q=4, H=1:** a full physical triangle, including the positive floor
  interval [17/56,5/16], disappears. The ambient singleton C3 still exists but
  has H=11/8, so it supplies no actual-orbit point.
- **P4 at q=4, H=1:** the physical slice is already a closed singleton. Child C5
  preserves t=3/8 at separation 1/8, while the other child C6 misses this slice.
- **P7 at q=10, H=4:** the old slice optimum at t=16/33, z=5/33 fails the added
  runner. The new contact t=17/35, z=1/7 lies in an old parent face and on a new
  child edge. The table also checks its reflected time 18/35.

Rotatable 3D parent/child geometry and a 2D physical-time/separation plot share
the same exact points. New edges in old faces are highlighted. The 3D view
uses a declared height factor of two; the 2D view uses independent labelled
axes. No interpolated band is presented as a physical runner system. The full
q=4 safe set and complete q=10 maximizing set remain separate from the local
parent-slice conclusions. At the rejected q=4 time, the recovery panel clearly
checks the failed old time rather than displaying a child witness.

The fifth chapter makes the pinned E1-then-E2 selector operable. Start at q=5:
E1's interval [1/8,19/24] misses the integer 1, so the second test uses E2's
[3/2,19/8], accepts 2, and recovers t=25/56. No witness is displayed after the
failed first test. The other controls show negative-lower-bound rounding
(q=3), closed lower/upper equality (q=4/q=6), and width greater than one
(q=10). The reader can step, run directly, reset, and reflect physical time.

Both safe segments, their exact projected intervals and the tested orbit
remain linked. Every accepted point recovers its original laps and all seven
physical phases. The width argument and complete q=2,...,8 arithmetic table
explain the source candidate's all-q reduction. Five interactive examples are
finite reproductions, not a substitute for that argument. At q=4, the one
selected time and its reflection omit two safe times; at q=10, its minimum
1/8 is below the optimum 1/7. This is a one-witness selector.

The original selector order and mathematical sources remain pinned to the
frozen snapshot. Later discovery and coverage-compiler research are separate
versions. The 20-scene deck and full research explorer remain pending.

The sixth chapter returns to physical time with the archived configuration
0,1,4,5,6,7,11,16 and J=[9/32,3/8]. This is explicitly separate from the A/B
families. Runners 1,4,5 are safe throughout the window; the other four have
six strict blocking occurrences. Merging by runner creates a triangle among
6,11,16. Keeping (speed, meeting) labels restores the path (16,5)—(6,2)—
(11,4)—(16,6), plus the separate (11,3)—(7,2) edge.

The 6/16 overlap needs meeting 5 of runner 16; the 11/16 overlap needs meeting
6. No common time in J can use both disjoint occurrences. All three block at
t=0, so this is a local exclusion, not a consequence of their speed relation
alone. Every graph edge means overlap somewhere; current highlights mean
active now. The physical-time cursor and all seven phases remain unchanged
when switching representation.

Nineteen ordered exact stops cover every blocking boundary and every open
cell between boundaries. Pair buttons visit each edge of the triangle. A
magnified view preserves the full local safe interval [17/56,39/128], duration
1/896, and both closed endpoints. Open threshold endpoints and included window
clipping endpoints are drawn distinctly. Completed laps floor(vt) and nearby
blocking meeting m are separate fields, with the latter shown only when active.
The source's general forest argument and synthetic altered distribution are
not promoted into new physical or universal claims.

## Evidence and scope

Source snapshot: `6b2b9316dbc87499a1cb5184aadbd6614d4d6c32`, on
`research/near-doubling-overlap-2026-09-24`.

- **REPRODUCED:** finite geometry, exact serialization and declared controls.
- **HYPOTHESIS:** the pinned internally reviewed all-q spectrum and selection
  proof candidates. This implementation does not promote their status.
- **ILLUSTRATION:** the browser picture and animation. They are not evidence
  from sampling and do not establish a general Lonely Runner theorem.

The starting specification is
[the visual plan](../../notes/CC_VISUAL_PRESENTATION_PLAN_2026_09_29.md).
All mathematical source paths and SHA-256 hashes are recorded in
[source_hashes.json](data/source_hashes.json); scene ownership and supported
questions are in [visual_manifest.json](data/visual_manifest.json).

This is AI-assisted implementation with same-author verification. The exact
checker uses physical closed-band intersections and opposing contacts to
crosscheck the cap-derived examples; it is not independent human review.
There is no new literature/novelty claim or extension of the parameter family.

## Rebuild and verify

Python 3.10+ standard library and Git; run in a repository checkout containing
the pinned source commit:

```bash
python3 visuals/compatibility-calculus/data/build_visual_data.py
python3 visuals/compatibility-calculus/data/build_visual_data.py --check
python3 visuals/compatibility-calculus/checks/check_visual_data.py
```

An optional Playwright/Chromium audit exercises the real page. It needs those
development dependencies separately; the visual itself does not:

```bash
CC_CHROMIUM_PATH=/path/to/chromium node visuals/compatibility-calculus/checks/check_browser.cjs
```

Set `CC_SCREENSHOT_DIR` to a scratch directory to save review images. Saved
results and the communication audit are in `checks/verification.json`,
`checks/browser_check.json`, and `checks/VISUAL_AUDIT.md`.

The builder reads saved JSON certificates from the pinned Git commit, never
scrapes equations from notes, and does not silently substitute newer research
files. The generated presentation needs neither Python nor Git to view.
It uses exact rational arithmetic and serializes each fraction as `num`, `den`,
`text`, and a rendering-only `float`. It generates two data files, source hashes,
the manifest (including implementation hashes), expected controls, and the standalone presentation. Edit
`presentation.template.html`, `joint.template.html`, `representation.template.html`,
`transfer.template.html`, `selector.template.html`, `clock.template.html`,
`css/cc.css`, and the files in `js/`, then rebuild;
do not hand-edit generated outputs.

The browser uses BigInt rational arithmetic even while scrubbing. Conversion
to floating point occurs only when drawing SVG. No physical witness is shown
for an ambient section before its integer contact. The complete source lap
labels and B-ray permutation survive in the data rather than being inferred
from a drawing.

### Exact acceptance controls

| Object / operation | Checked scope |
| --- | --- |
| Full geometry | 10 cells, 33 vertices, 45 edges, 3 singletons |
| Top caps | All 7 exactly equal the corresponding cell cut at z≥1/7 |
| Transfer | 8 parents, 10 children, 46 empty branches; 27 inherited, 6 new, 5 removed vertices; 9 edges inside old parent faces |
| A-ray examples | q=3,4,5,6,10; correct selector times and physical laps |
| q=4 | All four isolated times survive; all four positive six-form intervals vanish |
| Marginal counterexample | Recomputed H/S ranges and the blocked conditional interval on H=1 |
| Combined marginal candidate | t=33/104 gives runner 6 distance 5/52<1/8 while runner 13 reaches 1/8 |
| Conditional slice | All 14 displayed exact points retain six-runner safety and fail only runner 13; collision t=4/13; the entire closed S interval is strictly blocked |
| q=10 | 17/35 and 18/35 are maximizers; the old face has dimension 2 and the child face dimension 1 |
| Selector | 56 endpoint inequalities; primary small cases, q=5 fallback, q=4/q=6 equality endpoints; ten projected intervals and five selected/reflected physical controls |
| Shared clock | Six exact blocking occurrences, four pair edges, no 6/11/16 triple in J; direct seven-band intersection reproduces the closed safe interval; 19 physical time stops |
| Parent–child scenes | Three parents and four children: seven exact orbit slices reconstructed independently from 2D inequalities; before/after phases, laps and reflections |
| Representation controls | q=4 closed/open segment integer contacts; all eight q=10 maximizers partitioned into six old-edge and two face-interior recoveries |
| B-ray examples | q=2,3,4,5,6,7; all 42 cap-contact tests, direct physical maxima and complete maximizing sets |

The all-q reasoning and unbounded comparisons remain in the pinned source
certificates. These finite checks verify the visual's data and examples;
they do not extrapolate a theorem from six screen choices.

## Representation checkpoint

Retained: closed geometry, singleton identity, shared point, orbit functional,
clock, lap map, reflection, extremal direction identities, status and recovery
sources. Omitted by the cap view: low geometry, complete threshold-safe sets,
and richer transfer operations. The full atlas is reachable but this does not
make the cap representation lossless.

The seven-cap reduction uses the B-ray lower witnesses strictly above 1/7.
Changing that premise requires restoring the full model. In particular the
A-ray q=4 control lives at 1/8 and cannot be represented by these caps.

The third section shows A and B as different question/ray branches. It does
not imply a lossless chain from B caps to A conditional intervals. Their
actual-orbit equations and physical clocks differ, and source availability is
a recovery route rather than intrinsic losslessness.

The q=4 scene retains the full joint triangle and same-H conditional interval.
Its separate-range rectangle is explicitly the inadequate representation; the
false candidate fails the original parent constraints under direct physical
checking. The 14 slider controls illustrate, rather than establish, the
continuous exclusion: 15/8 < 109/56 ≤ S ≤ 33/16 < 17/8 certifies the full slice.

The browser audit checks all 12 representation states at widths 1440, 390 and
320, exact values, ray/clock selection, restoration, and direct
chapter links. The original two sections remain covered after the shared
router change. Mathematical source data stay at the original frozen commit;
later discovery and two-parameter research are not silently imported.

The fourth-section audit adds nine exact stage states across 27 layouts,
physical/reflected phase tables, camera controls, orbit visibility and four
chapter direct links. The builder intersects certified edges with H=qx-y;
the checker independently intersects pairs of sliced halfspace boundaries,
covering empty, singleton and triangular results.

The fifth-section audit adds eleven exact states across 33 layouts, including
withheld witnesses after failure, closed endpoints, negative rounding, exact
physical/reflected tables, reset/direct execution and five-chapter navigation.
The interval checker projects endpoints directly and enumerates integer
contacts, independently of the builder's slope/intercept calculation.

The sixth-section audit checks all 38 time/representation states at three
widths (114 layouts), exact phases and completed/meeting labels, strict
blocking, both safe endpoints, graph structure, jump/step controls and
six-chapter navigation. Four archived source files were added to the manifest
at the same frozen commit; the existing A/B controls are unchanged.

Next visual target: connect the physical safe-lap inequalities to construction
of a geometric cell, then introduce the full atlas before its question-specific
compressions. The guided opening/relative-motion introduction, concluding CC
story, standalone figure exports and research explorer remain unfinished.
