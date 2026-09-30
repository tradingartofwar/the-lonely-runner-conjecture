# Compatibility Calculus research explorer

Open [explorer.html](../explorer.html). It is one self-contained offline file;
no server, installation, network request or external library is needed to view
it. The guided presentation and static figures remain separate products.

The explorer supports **A and B, integer q=2…60, six or seven required forms**,
and four different requested outputs:

- one 1/8-safe witness;
- the optimal separation;
- every maximizing time in one period [0,1];
- the complete closed safe set at threshold 1/8, 1/7 or 1/6.

All runners start together, with reference speed 0. The six-form comparison
retains the same 1/8 atlas floor; that is not the seven-total-runner nominal
1/7 loneliness threshold. The runner count and actual speed vector update.
Later coefficient/compiler and nine/ten-runner research are not imported.

## How to use it

Choose the ray, q, question and required forms. The answer panel gives the
complete requested output. The inspector below selects one cell, cap or
selector segment and can explore a different, locally compatible point.
**Inspect the answer** restores a point supporting the output above.

The height slider interpolates exact rational sections between the object's
peak and floor. **First integer hit** jumps directly to its highest integer
orbit contact, without a sampled search. Choose H and scrub the resulting
common slice. The projection, physical time, phases, distances and laps all
refer to that same point. If the section misses the selected H, physical
recovery is withheld. Reflection checks 1−t while keeping the folded diagram.

The complete-set view retains all closed endpoints and singleton times. Its
exact list and controls remain available when equality markers are hidden.
Display toggles change visibility only. A hidden point never becomes an empty
mathematical set. Dense points may overlap on screen; exact fractions are
authoritative.

The parent/child comparison uses the same ray, q and integer H. It shows the
entire vertical orbit section of the selected object's six-form parent and
all its children. Its before/after optima are local to that parent and H.
They do not replace the global answer across all cells and orbits. An empty
child has no witness; an unchecked seventh runner in the six-form table is
explicitly labelled. **Inspect surviving child** applies the seventh form and
recovers its point.

The five shortcuts open:

| Control | Exact result to inspect |
|---|---|
| B6 · first contact | H=-2, point (4/25,9/25,4/25), t=9/25, minimum 4/25 |
| A4 · four isolated times | Complete 1/8-safe set {1/8,3/8,5/8,7/8}; empty at 1/7 |
| A5 · selector fallback | E1 [1/8,19/24] misses 1; E2 [3/2,19/8] hits 2; t=25/56 |
| A10 · new face contact | P7/H=4 → C9, point (17/35,6/7,1/7); eight global maximizers |
| A4 · failed transfer | P2/H=1 loses its entire child slice; the preserved false marginal pair fails speed 6 |

The URL fragment records exact inspector state, including rational height and
slice position, for reload/bookmark use. **Download exact state JSON** saves
the controls, question, complete answer, selected point, physical check,
transfer state, scope and source commit. Unsupported q values retain the last
valid state and show an input message.

## Representation contract

| View | Retained | Scope / recovery |
|---|---|---|
| Full cells / parents | Labels, closed geometry, facets, orbit sections and reflection | Answers at/above the 1/8 atlas floor require all cells and all compatible integers, not one selected drawing |
| Seven top caps | Upper geometry, cap identity and integer contact | B optimum/every-maximizer reduction requires a witness strictly above 1/7; recover the full atlas for complete lower safe sets or transfer |
| E1 / E2 selector | Closed endpoints, ordered integer tests and one recovery | A-ray one 1/8 witness only; recover full geometry for optimum, all maximizers or complete safe sets |

The scope panel updates with the selected view and requested output. If an
inadequate compression is selected for a broader question, it says so; the
answer panel retains its explicitly identified richer source. A and B keep
different H maps and physical clocks. Source availability supplies a recovery
route rather than a claim of intrinsic losslessness.

## Exact computation and countercheck

`model.js` uses the existing BigInt rational core. The full answer comes from
edge-plane intersections in the pinned certified atlas. Every compatible
integer H is enumerated within exact vertex bounds. Highest section vertices
give optimal contacts; horizontal sections at the selected threshold yield
closed time intervals. Reflection, union and duplicate-time removal preserve
equality. The A one-witness question instead uses the pinned E1-then-E2 order.

No pixels, camera settings, time samples or slider steps determine feasibility
or the complete outputs. Floating-point conversion occurs only when drawing.

The independently structured Python checker works in physical time: it
intersects each runner's closed safe bands and enumerates tent tops and
opposing-slope contacts to optimize the distance lower envelope. All **236**
ray/q/form-count configurations agree for the optimum, complete optimizer set
and physical witness. All **708** threshold-safe sets agree. The **59** B-ray
seven-form controls also match the cap-only optimum, strictly above 1/7.
These are finite, same-author counterchecks, not independent human proof review.

The browser audit covers 312 question/control layouts at 1440, 390 and 320 px,
plus canonical interaction and screenshot states. It checks before-contact
withholding, rational depth/slice scrubbing, reflection, closed endpoints,
selector failure/fallback, empty/singleton/new-face transfer, display-only
toggles, invalid q, exact permalink reload and a downloaded state JSON. It
requires no page errors, network requests, page overflow or clipped SVG text.

## Rebuild and verify

From the repository root:

```bash
python3 visuals/compatibility-calculus/explorer/build_explorer.py
python3 visuals/compatibility-calculus/explorer/build_explorer.py --check
python3 visuals/compatibility-calculus/explorer/checks/check_model.py --write
CC_CHROMIUM_PATH=/path/to/chromium \
  node visuals/compatibility-calculus/explorer/checks/check_browser.cjs --write
```

The model checker requires Python and Node. Browser checking additionally
requires Playwright and Chromium; `CODEX_PRIMARY_RUNTIME_NODE_MODULES` is an
optional Playwright lookup path. Set `CC_SCREENSHOT_DIR` outside the repository
for review PNGs. Reports are [model_check.json](checks/model_check.json) and
[browser_check.json](checks/browser_check.json). Canonical expected outputs are
generated only after the independent physical comparison passes.

[manifest.json](manifest.json) records source/data hashes, implementation input
hashes, domain, method and the generated HTML hash. All mathematical and
semantic sources stay at `6b2b9316dbc87499a1cb5184aadbd6614d4d6c32`. The original
presentation, figure exports and exact data files are unchanged; this separate
manifest owns the new explorer build. Implementation is AI-assisted.

Next visual target: the coordinated transformation pass, with reduced-motion
equivalents, followed by the package-wide final visual audit.
