# Compatibility Calculus visual companion

**First build:** exact data plus **top cap → section → first integer hit → physical witness**.

Open [presentation.html](presentation.html) in a modern browser. It is a
self-contained offline file: no backend, network dependencies, font download,
or build tooling is required to view it. A static server also works:

```bash
python3 -m http.server 8000 --directory visuals/compatibility-calculus
```

Then open `http://localhost:8000/presentation.html`.

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

The exact data layer also preserves the five planned A-ray controls, the
six-to-seven atlas, the q=4 false marginal example, q=10 face contact, and both
A-ray selector segments. Those scenes are not yet interactive. The 20-scene
deck, full research explorer, second and third visual targets remain pending.

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
`presentation.template.html`, `css/cc.css`, and the files in `js/`, then rebuild;
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
| q=10 | 17/35 and 18/35 are maximizers; the old face has dimension 2 and the child face dimension 1 |
| Selector | 56 endpoint inequalities; primary small cases, q=5 fallback, q=4/q=6 equality endpoints |
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

For the eventual representation ladder, show the A and B uses as different
question/ray branches. Do not draw an unqualified lossless chain from B caps
to A conditional intervals. Their actual-orbit equations and physical clocks
differ.

Next visual target: the q=4 separate-marginals versus joint-compatibility
demonstration, using the exact data already preserved here.
