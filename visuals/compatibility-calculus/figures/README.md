# Compatibility Calculus — eleven standalone figures

Open [the offline gallery](index.html) to browse or download all eleven SVGs.
Every preview and download is embedded in that HTML file. Each SVG contains
vector shapes and selectable text, a caption, exact selected values, evidence
status, pinned source links and machine-readable JSON in its `<metadata>`.
There are no scripts, raster images, downloaded fonts or external rendering
dependencies. Source links require a connection when followed.

| Figure | Subject | Retained distinction |
|---|---|---|
| [01](01-runner-circle.svg) | Runner circle and reference change | Coincident identities and invariant distances |
| [02](02-shared-clock.svg) | Blocking intervals on one clock | Strict blocking, closed safe endpoints and the narrow gap |
| [03](03-occurrence-identity.svg) | Incompatible occurrences | Runner identity versus meeting identity |
| [04](04-safe-cell.svg) | One completed closed cell | Ambient geometry versus a physical orbit |
| [05](05-ten-cell-atlas.svg) | Complete ten-cell atlas | Three singleton cells and all vertex/edge occurrences |
| [06](06-seven-top-caps.svg) | Seven top caps | Cap identity, declared cut and independently fitted panels |
| [07](07-cap-to-clock.svg) | B-ray q=6 contact | Same section, integer contact, clock t=y and recovery |
| [08](08-false-marginals.svg) | A-ray q=4 false pair | Marginals versus the joint H=1 slice |
| [09](09-new-face-contact.svg) | A-ray q=10 face contact | New child edges versus old parent edges; every maximizer |
| [10](10-two-segment-selector.svg) | A-ray q=5 selector | One witness versus optimum or complete safe set |
| [11](11-representation-branches.svg) | Representation branches | Different questions, A/B clocks and recovery obligations |

Figure 11 implements the plan's “representation ladder” as parallel branches,
consistent with the representation rules and the guided presentation. It does
not suggest a universal lossless B-cap → A-slice → selector chain.

## Rebuild and check

From the repository root, first verify the unchanged presentation/data inputs:

```bash
python3 visuals/compatibility-calculus/data/build_visual_data.py --check
python3 visuals/compatibility-calculus/checks/check_visual_data.py
```

The exporter requires Node, Playwright and Chromium. It uses `playwright` from
the normal module search path, or `CODEX_PRIMARY_RUNTIME_NODE_MODULES` when
available. Set `CC_CHROMIUM_PATH` if using a separately installed browser;
otherwise Playwright's installed Chromium is used.

```bash
CC_CHROMIUM_PATH=/path/to/chromium \
  node visuals/compatibility-calculus/figures/export_figures.cjs
CC_CHROMIUM_PATH=/path/to/chromium \
  node visuals/compatibility-calculus/figures/export_figures.cjs --check
CC_CHROMIUM_PATH=/path/to/chromium \
  node visuals/compatibility-calculus/checks/check_figures.cjs --write
```

The exporter selects exact controls in `presentation.html`, asserts their
states, and serializes the existing SVG renderers with resolved presentation
attributes. The seven-cap sheet reuses the same geometry renderer; the atlas
adds cell-name annotations to its existing vertex markers. The final branch
map is authored SVG tied to the same source records. Captions deliberately
carry scope that normally lives beside the interactive diagrams.

`--check` regenerates in memory and requires byte-for-byte equality. Rendering
is pinned in [manifest.json](manifest.json) to Chromium 153.0.8010.0, a fixed
viewport, light mode, reduced motion and `Arial, sans-serif`. Browser/font
changes can alter vector layout bytes; use the same rendering environment for
an exact byte comparison. Rational states and source hashes remain the
mathematical authority. No timestamps or local machine paths enter the exports.

The figure checker compares metadata to exact data, independently checks five
physical recoveries with integer arithmetic, verifies the three singleton rings
and seven cap meshes, checks text against figure/panel boundaries, and opens
the gallery at widths 1440, 390 and 320. It verifies an actual downloaded SVG
against its hash and requires no network requests or page errors. Its report
is [figure_check.json](../checks/figure_check.json). Set `CC_SCREENSHOT_DIR` to
a directory outside the repository to save review PNGs. All eleven exports
also received a visual inspection; this is an AI-assisted same-author audit.

## Provenance and limits

All mathematical and semantic records stay frozen at
`6b2b9316dbc87499a1cb5184aadbd6614d4d6c32`. This collection does not import later
research, promote proof candidates, or establish a new LRC result. Captions
distinguish finite reproductions from the source's all-q arguments.

The figure manifest records input hashes, selected states, captions, sources,
rendering environment and output hashes. The presentation's earlier embedded
implementation-scope note describes its own build; the separate figure
manifest and this README track the completed export collection. The original
data and presentation bytes are unchanged.

Static figures omit interaction, alternative controls and most derivations.
Restore the matching presentation chapter and pinned richer source before
changing the parameter, threshold, representation or requested output. An
available source is a recovery route, not an assertion of losslessness.

Next visual target: the separate research explorer, with coordinated exact
parameter, geometry, projection, witness and representation-scope controls.
