# Compatibility Calculus visual presentation — executable plan

September 29, 2026.

**Status:** implementation plan only. No new mathematical claim is made here.

**Purpose:** build a code-generated visual research companion for the current Lonely Runner / Compatibility Calculus work. The presentation should help Vance, collaborators, and eventual public readers see the model changes, compatibility relations, information loss, witness recovery, and query-specific compression that are difficult to hold in prose alone.

The presentation is not a proof certificate. Every mathematical scene must be generated from or checked against the repository's exact sources and must carry the claim status of the result it depicts.

---

## 1. Why build this

The current work combines several structures that are individually understandable but difficult to hold simultaneously:

- runners moving on a circle;
- selected-reference relative motion;
- safe and blocking intervals;
- lap/occurrence identity;
- torus coordinates;
- three-dimensional safe polytopes;
- integer-orbit compatibility;
- contact geometry;
- projections to arithmetic intervals;
- isolated equality witnesses;
- parent/child constraint transfer;
- query-specific compression;
- explicit recovery of physical time and lap labels.

A visual system may help in three separate ways.

### Research insight

A picture can reveal whether two objects that look algebraically similar are geometrically or temporally different. It may expose a hidden conflation, a missing contact, a false marginal combination, or a useful smaller representation.

### Communication

The work can be explained without forcing a reader to reconstruct every layer from equations first.

### Audit

A generated visual can act as a representation check: source data, geometry, projection, and recovered physical witness should agree. Disagreement is a signal to inspect the model, not an invitation to smooth the picture.

---

## 2. Governing visual principles

Follow CC_REPRESENTATION_RULES.md and the repository evidence rules.

1. **Visuals are generated from exact state where possible.** Use Fraction / integer arithmetic in generation. Convert to floats only at rendering boundaries.
2. **A visual states which question it answers.** Existence, optimum value, one witness, every maximizer, complete safe set, and transfer remain distinct.
3. **Never merge marginal facts into joint compatibility.** If two conditions must hold at one physical point, the visual must preserve the shared state or explicitly label the view as a marginal projection.
4. **Preserve equality.** Singleton cells and isolated witness times are first-class objects, not zero-width noise.
5. **Keep ambient and physical geometry distinct.** An ambient safe point is not a runner witness until the actual-orbit condition and recovery map are satisfied.
6. **Show compression together with its limits.** If a smaller visual model answers only one question, display that scope.
7. **Keep the richer source reachable.** Every scene should identify the note/certificate that can reconstruct the detail omitted by the scene.
8. **Do not imply novelty or generality from visual elegance.** The presentation demonstrates what the current human/AI collaboration found useful.

---

## 3. Primary mathematical sources

The first implementation should use the existing research branch and avoid rederiving claims from prose when exact artifacts are available.

### Core CC sources

- notes/CC_REPRESENTATION_RULES.md
- notes/CC_BOUNDED_SELECTOR_2026_09_29.md
- notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md
- notes/CC_OTHER_RAY_REVIEW_2026_09_29.md
- notes/LTCM_EXACT_SPECTRUM_2026_09_29.md
- notes/LTCM_OTHER_RAY_UPPER_BOUND_2026_09_29.md
- notes/LAP_LABELLED_CONSTRAINTS.md
- notes/DISTINCTION_AUDIT_2026_09_25.md

### Exact review/certificate sources

- reviews/2026-09-29-ltcm-spectrum/
- reviews/2026-09-29-cc-other-ray-review/
- reviews/2026-09-29-cc-six-seven-transfer/
- reviews/2026-09-29-cc-bounded-selector/

Prefer saved JSON/certificate data when it already carries vertices, edges, phases, labels, projections, or witness records. Use the notes as semantic and claim-status sources.

---

## 4. Proposed output structure

Create a self-contained visual package under:

~~~text
visuals/compatibility-calculus/
├── README.md
├── index.html
├── presentation.html
├── explorer.html
├── css/
│   └── cc.css
├── js/
│   ├── cc-core.js
│   ├── cc-deck.js
│   ├── cc-geometry.js
│   ├── cc-orbit.js
│   ├── cc-runners.js
│   └── cc-explorer.js
├── data/
│   ├── build_visual_data.py
│   ├── visual_manifest.json
│   ├── cc_geometry.json
│   ├── cc_examples.json
│   └── source_hashes.json
├── figures/
│   ├── generated SVG files
│   └── generated PNG exports if desired
└── checks/
    ├── check_visual_data.py
    └── expected_controls.json
~~~

The first version should require only a local static web server and standard browser features. Avoid making the core presentation depend on a hosted service.

Use SVG for most diagrams because it is inspectable, crisp, and easy to label. Use HTML canvas only where animation materially helps. For the 3D geometry, begin with a deterministic 3D-to-2D projection implemented locally rather than introducing a large external visualization framework. A later optional interactive 3D viewer can be added if the static projection proves insufficient.

---

## 5. Two complementary products

Do not force one interface to serve every need.

### A. Guided visual presentation

presentation.html

A slide/scene sequence with short explanations. It should be usable by a person who does not know the repository.

Purpose:

- explain the problem;
- show why previous summaries lost information;
- introduce CC visually;
- demonstrate the fixed geometry, top caps, orbit projection, parent-child transfer, false marginal compatibility, equality preservation, and bounded selector.

### B. Research explorer

explorer.html

Interactive controls for Vance and collaborators.

Initial controls:

- choose A_q or B_q;
- integer q;
- show/hide full cells;
- show/hide z>=1/7 caps;
- select a cell/cap;
- show orbit functional;
- show projected interval;
- show integer lattice;
- show first integer hit;
- show physical time recovery;
- show runner phases;
- switch question:
  - one witness;
  - optimum;
  - every maximizer;
  - complete threshold-safe set;
- toggle parent/child six-to-seven transfer;
- toggle equality points.

The explorer should display a **representation scope panel** telling the user what the currently displayed compression can and cannot answer.

---

## 6. Guided presentation — proposed scenes

### Scene 1 — The ordinary Lonely Runner problem

Visual:

- circular track;
- selected runner highlighted;
- other runners moving;
- threshold arcs showing what "at least 1/n away" means.

Purpose:

- make the physical problem visible before abstraction.

Interaction/animation:

- scrub time;
- show nearest distance to selected reference;
- mark lonely times.

Use a small exact example first, not the hardest family.

---

### Scene 2 — Change viewpoint: selected reference and relative motion

Visual:

- freeze the selected reference at zero;
- convert the other runners to relative speeds;
- show phases around the unit circle.

Purpose:

- make clear that the later geometry is still carrying the original runner problem.

Caption distinction:

> changing representation is not changing the physical question when the translation is exact.

---

### Scene 3 — Blocking and safe intervals on one shared clock

Visual:

- horizontal time axis;
- colored blocking intervals for several runners;
- safe complement;
- one lonely witness.

Purpose:

- show the coverage formulation;
- introduce the idea that all runner claims must refer to the **same time**.

---

### Scene 4 — Why pairwise overlap summaries can lie by omission

Use the archived 6 / 11 / 16 occurrence example.

Visual:

- runner 16's lap-5 blocking occurrence;
- runner 16's lap-6 blocking occurrence;
- overlap with runner 6 highlighted on one occurrence;
- overlap with runner 11 highlighted on the other;
- attempted triple shown as impossible because it requires two different occurrences of runner 16.

Message:

> both pairwise statements are true; they are not true together.

This should be the first explicit visual definition of the CC problem.

---

### Scene 5 — Lap-labelled safe cells

Visual:

- a single safe lap vector;
- lower/upper inequalities;
- shared interval [L_m,R_m];
- positive interval, singleton, and empty cases side by side.

Purpose:

- show how CC carries occurrence identity, shared time, and equality status.

---

### Scene 6 — Lift to a geometric model

For the current fixed coefficient forms, introduce:

- x;
- y;
- z = achieved separation.

Visual:

- axes labeled x, y, z;
- show one polytope cell as the intersection of closed bands;
- animate clipping by constraints one at a time.

Purpose:

- explain why the geometry is genuinely 3D;
- show that a cell is a set of compatible states, not a decorative object.

---

### Scene 7 — The complete fixed geometry

Visual:

- the 10 seven-form cells;
- vertices and edges available by toggle;
- singleton cells rendered as prominent points rather than disappearing.

Display factual counts:

- 10 nonempty cells;
- 33 vertex occurrences;
- 45 edge occurrences;
- 3 singleton cells.

Source these counts and coordinates from the frozen certificate, not hand transcription.

Purpose:

- give the viewer the "whole object" before compression.

---

### Scene 8 — The seven top caps

This is the main answer to the current visualization question.

Visual:

- full geometry faint;
- horizontal plane z=1/7;
- the seven nonsingleton cells' portions above the plane highlighted;
- each top cap shown as a tetrahedron:
  conv(P, P+r1/42, P+r2/42, P+r3/42).

Purpose:

- show a **question-specific compression** of the full model.

Caption:

> For the current B_q optimum proof candidate, the supplied lower witnesses are strictly above 1/7. The geometry below this cut cannot beat them, so the upper-bound question can be carried by seven top caps. This smaller representation does not preserve the complete 1/8-safe set.

This scene should have a toggle:

full cells ↔ top caps only.

---

### Scene 9 — Horizontal cap section becomes a triangle

Pick one cap and a loss

e = 1/6-z.

Visual:

- horizontal cut through the tetrahedral cap;
- resulting triangle;
- the three directional vertices;
- label the orbit functional, for the B ray:
  H_q=x-qy.

Purpose:

- make the later projection visually obvious.

---

### Scene 10 — Project the triangle to one interval

Visual:

- triangle on left;
- arrows through H_q;
- one-dimensional interval
  I_P(e)=[h_P+e d_-(q), h_P+e d_+(q)]
  on the right;
- integer lattice ticks drawn across the number line.

As e increases, animate the interval expanding from its peak value.

Purpose:

- show geometry becoming arithmetic.

---

### Scene 11 — The first integer hit

Continue Scene 10.

Animate increasing e until the projected interval first touches an integer.

Display:

e_P=min(rho/(-d_-(q)), (1-rho)/d_+(q)).

Then show:

z=1/6-e_P.

Purpose:

- visually explain "first integer hit determines the loss from 1/6."

For one residue class, identify the winning cap/direction. Then allow a control to change q mod 6 and watch the winning cap/contact change.

---

### Scene 12 — Recover the actual runner witness

From the integer hit:

- identify the compatible point in the cap;
- apply the physical clock map;
- reconstruct the physical time;
- show the seven runner phases at that time;
- return to the circular track and show that all distances satisfy the claimed separation.

Purpose:

- close the loop:
  geometry → arithmetic → actual runners.

This scene is essential. It prevents the visual geometry from floating free of the physical problem.

---

### Scene 13 — Why full geometry must remain available

Use the A-ray q=4 control.

Visual sequence:

1. six-coordinate model has positive safe intervals plus isolated points;
2. add the seventh constraint;
3. the positive intervals disappear;
4. four isolated witnesses remain:
   1/8, 3/8, 5/8, 7/8.

Purpose:

- show why a duration-only or z>1/7 representation cannot be treated as universally sufficient;
- illustrate reversible compression.

---

### Scene 14 — Parent to child: adding the seventh constraint

Use the six-to-seven atlas.

Visual:

- one six-form parent tetrahedron;
- animate a seventh band plane cutting it;
- show outcomes:
  - survives unchanged;
  - clipped;
  - collapses to singleton;
  - splits into multiple children.

Then show the aggregate counts:

- 8 parent tetrahedra;
- 10 nonempty children;
- 9 child edges created inside old parent faces.

Purpose:

- show that adding a constraint can create new contacts that did not live on the old optimal structure.

---

### Scene 15 — A new optimum can appear inside an old face

Use q=10, t=17/35.

Visual:

- highlight parent P7;
- show old face;
- show point (17/35,6/7,1/7) in the **interior of that old face**;
- add seventh band;
- show new child edge through the point.

Purpose:

- make concrete why "keep the old edges" loses some new maximizing witnesses.

Scope caption:

> This refutes complete maximizer recovery from the old edge set. It does not by itself refute a smaller record that happens to select some other optimizer.

---

### Scene 16 — Separate marginals manufacture a false witness

Use A-ray q=4, parent P2 at z=1/8.

Panel A:

H_4=4x-y in [5/8,11/8]

with integer 1 highlighted.

Panel B:

S=5x+2y in [23/12,17/8]

with the safe endpoint 17/8 highlighted.

Then visually show that the two highlighted facts occur at different points in the triangle.

Next, cut by the **same** orbit slice H_4=1 and show the conditional S interval:

[109/56,33/16],

which lies between the relevant safe bands.

Message:

> marginal compatibility is not joint compatibility.

This should be one of the signature CC visuals.

---

### Scene 17 — Conditional interval repair

Visual:

- parent;
- same integer orbit slice;
- conditional interval J_(m,h)(z);
- intersect with seventh safe band;
- if nonempty, use the inverse map:
  x=(S+2h)/(2q+5),
  y=(qS-5h)/(2q+5).

Purpose:

- show the exact repair to the false marginal representation.

---

### Scene 18 — Compress further: the two-segment selector

Use CC_BOUNDED_SELECTOR_2026_09_29.md.

Visual:

- show only segments E1 and E2 in the parent geometry;
- project E1 through the orbit map to
  I1(q)=[(q-4)/8,(5q-6)/24];
- show the first integer chosen by the ceiling;
- show that E1 works for every integer q>=2 except q=5;
- then show E2 recovering q=5.

Purpose:

- demonstrate another query-specific compression:
  full atlas → conditional intervals → **two segments** for the narrower question "find one 1/8-safe witness."

Important scope label:

> This does not recover the optimum, all maximizers, or the complete safe set.

---

### Scene 19 — The representation ladder

A single diagram summarizing the current CC architecture:

~~~text
FULL CELL ATLAS
  answers: complete fixed geometry / rich transfer
        |
        | question-specific compression
        v
SEVEN TOP CAPS
  answers: B-ray optimum / maximizer proof candidate above 1/7
        |
        | different operation
        v
CONDITIONAL INTERVALS
  answers: exact same-slice six-to-seven compatibility
        |
        | narrower output request
        v
TWO COMPATIBLE SEGMENTS
  answers: one A-ray 1/8 witness for every integer q>=2
~~~

Beside each layer, show:

- what it retains;
- what it omits;
- what query it supports;
- what failure triggers return to the richer layer.

Purpose:

- visually teach **reversible, consequence-aware compression**.

---

### Scene 20 — Compatibility Calculus

Final conceptual scene.

Display:

> **Compatibility Calculus carries not only what is true, but what can be true together.**

Then show the recurring operations:

~~~text
state
  ↓
constraints
  ↓
contacts
  ↓
joint compatibility
  ↓
question-specific compression
  ↓
selection / optimization / enumeration
  ↓
recovery to physical model
  ↓
certificate
~~~

Add the correction loop:

counterexample / information loss → recover richer model → preserve missing relation → test again.

Purpose:

- present CC as a useful working language developed in partnership with AI, without making a novelty or disciplinary claim.

---

## 7. Research explorer — exact controls

The explorer should begin with a small set of canonical controls rather than an unrestricted parameter box.

### Required A-ray controls

- q=4
  - isolated equality case;
  - marginal-range false positive;
  - positive intervals removed by added speed;
- q=10
  - new maximizers inside an old parent face;
- q=3
  - transfer boundary control;
- q=5
  - two-segment selector fallback;
- q=6
  - selector endpoint equality.

### Required B-ray controls

Choose at least one from each residue behavior:

- residue 0;
- residue 2;
- residue 5;
- one constant 1/6 branch.

The first implementation may use the smallest valid q in each branch so the fractions remain readable.

---

## 8. Visual data builder

data/build_visual_data.py should create a stable JSON layer for the browser.

It should not parse prose when exact data already exist.

### Data groups

#### full_cells

For each cell:

- lap label;
- vertices;
- edges;
- dimension;
- singleton flag;
- peak;
- source certificate.

#### top_caps

For each of the seven caps:

- peak;
- three rays;
- cap cut e0=1/42;
- four tetrahedron vertices;
- projected extremal directions;
- valid question scope.

#### parameter_families

- A-ray speed formulas;
- B-ray speed formulas;
- coordinate ordering;
- orbit equation;
- physical clock;
- lap recovery map;
- reflection rule.

#### examples

Exact records for q=3,4,5,6,10 and selected B-ray residues:

- physical speed vector;
- selected time;
- minimum distance;
- phases;
- laps;
- active contacts;
- safe components where relevant.

#### parent_child

- eight parents;
- child list/lap;
- child vertices/edges;
- relation: unchanged / clipped / singleton / split;
- new face-cut edges.

#### selectors

- B-ray first-integer-hit formulas;
- A-ray E1/E2 segment formulas;
- residue/small-case scope.

### Serialization

Fractions should serialize as both exact and rendering values:

~~~json
{
  "num": 17,
  "den": 35,
  "text": "17/35",
  "float": 0.4857142857142857
}
~~~

The exact numerator/denominator is authoritative. The float is rendering convenience only.

---

## 9. Rendering conventions

Use consistent semantics rather than arbitrary color decoration.

The implementation may choose colors later, but the roles should remain fixed:

- safe object;
- blocking object;
- selected physical orbit;
- ambient-only object;
- equality/singleton;
- active contact;
- omitted/inactive geometry;
- false marginal combination;
- recovered witness.

Every visual should have a legend when more than three roles appear.

Accessibility:

- do not rely on color alone;
- use line style, fill pattern, labels, and markers;
- support reduced motion;
- keep fractions readable;
- allow pause/scrub on all animations.

---

## 10. 3D representation

Yes, part of the present model has a real 3D representation.

The three coordinates are:

- x;
- y;
- z = achieved separation.

The safe cells are bounded convex polytopes cut out by linear inequalities.

The seven top caps are literal tetrahedral subregions above z=1/7 of the seven nonsingleton cells.

### First implementation

Use a fixed oblique or perspective projection from 3D to SVG.

Required controls:

- rotate left/right;
- tilt;
- reset;
- toggle axes;
- toggle vertices/edges/faces;
- toggle z=1/7 plane;
- toggle full cells versus caps.

Do not begin with photorealistic rendering. Mathematical readability is the priority.

### Later option

If useful, add true interactive 3D with mouse orbiting. Do this only after the exact static diagrams are validated.

---

## 11. Animation candidates

Animation should be used only when change over time or transformation is the subject.

High-value animations:

1. runners moving around the circle;
2. time-axis blockers appearing/disappearing;
3. clipping a parent polytope by the seventh band;
4. lowering a horizontal plane through a top cap;
5. projected interval expanding until first integer contact;
6. mapping integer contact back to physical runner time;
7. positive intervals disappearing while equality points remain.

Avoid decorative continuous motion.

---

## 12. Verification requirements

A generated visual is accepted only after the data layer passes exact checks.

### Geometry controls

- 10 seven-form cells;
- 33 vertex occurrences;
- 45 edge occurrences;
- 3 singleton cells;
- 7 top caps;
- each cap reconstructed from the stored peak/rays;
- cap cut agrees with z>=1/7.

### A-ray transfer controls

- 8 parents;
- 10 nonempty children;
- 46 empty parent/lap branches;
- 27 inherited child vertices;
- 6 new child vertices;
- 5 parent vertices removed;
- 9 child edges lie inside old parent faces.

### q=4 controls

- full final safe set includes exactly four isolated witnesses at
  1/8, 3/8, 5/8, 7/8;
- the declared positive six-form intervals are removed by the seventh constraint;
- the P2 marginal-range picture shows the false product compatibility;
- the conditional H_4=1 section produces the stated blocked S interval.

### q=10 controls

- 17/35 and 18/35 are final maximizing times;
- 17/35 is interior to a two-dimensional parent face before the seventh cut;
- the added band creates the relevant child edge.

### bounded-selector controls

- E1 works for every declared small case except q=5;
- E2 recovers q=5;
- q=4 and q=6 closed endpoint cases remain accepted;
- direct physical phase checks agree with the saved certificate.

### B-ray controls

- selected cap/contact for chosen residue examples agrees with current proof candidate;
- projected interval reaches the declared first integer at the declared loss;
- recovered physical time gives the displayed minimum separation.

### Source integrity

source_hashes.json should record the hashes of every source JSON/script/note used to generate the visual data.

The page should display a small "generated from" panel with the current visual-data build hash.

---

## 13. Claim-status display

Every scene that depicts a non-established mathematical result should carry a compact status badge.

Examples:

- REPRODUCED — exact finite geometry
- HYPOTHESIS / proof candidate — internal AI review
- KNOWN / literature
- ILLUSTRATION — does not establish generality

Do not force the audience to infer epistemic status from prose at the bottom of a page.

---

## 14. Implementation phases

### Phase 0 — freeze sources and build manifest

Deliverables:

- visuals/compatibility-calculus/README.md;
- source-path list;
- source hashes;
- exact control table.

Success:

- every mathematical object planned for visualization has an owning source and claim status.

### Phase 1 — exact data layer

Build:

- fractions serializer;
- full-cell data;
- cap data;
- A/B family maps;
- canonical example records;
- parent-child atlas;
- two-segment selector records.

Success:

- check_visual_data.py passes every control in Section 12 without browser rendering.

### Phase 2 — static figures

Generate SVGs for:

1. one-runner-circle explanation;
2. shared-clock blocking intervals;
3. incompatible occurrence example;
4. one safe cell;
5. full 10-cell geometry;
6. seven top caps;
7. one cap section and projection;
8. q=4 false marginal compatibility;
9. q=10 new-face contact;
10. two-segment selector;
11. representation ladder.

Success:

- each figure can stand alone with a caption and source/status.

### Phase 3 — guided presentation

Implement the 20-scene deck.

Success:

- a reader can follow from physical runners to CC without reading the research notes first;
- every advanced scene provides a pointer to the richer source.

### Phase 4 — research explorer

Implement the controls in Section 5.

Success:

- changing q changes the rendered geometry/projection/witness from the exact data model;
- scope panel updates with the selected representation;
- q=4/q=10/q=5 controls remain correct.

### Phase 5 — animated transformations

Add only the high-value animations in Section 11.

Success:

- animation clarifies a transformation that is harder to see statically;
- reduced-motion mode preserves all information.

### Phase 6 — visual audit

Run two reviews:

1. **mathematical audit:** generated objects versus certificates;
2. **communication audit:** identify any visual that could imply a stronger claim than the source supports.

Success:

- no unresolved source mismatch;
- no visual silently merges ambient/physical, interval/point, one/all, or marginal/joint distinctions.

### Phase 7 — optional public explainer

Only after the research version is useful to Vance.

Create a shorter path, perhaps 8–10 scenes, that demonstrates what human/AI partnership can do without requiring a claim of mathematical novelty.

---

## 15. First build target

Do not start with the entire deck.

Build one vertical slice that tests the whole architecture:

### **Top cap → projection interval → first integer hit → physical witness**

Use one B-ray residue example.

It should show:

1. the relevant 3D cap;
2. a horizontal triangle section;
3. projection through H=x-qy;
4. the interval and integer lattice;
5. first contact;
6. the corresponding loss from 1/6;
7. recovered physical time;
8. phases of the actual runners at that time.

Why this first:

- it answers Vance's immediate visualization question;
- it exercises 3D geometry, exact arithmetic, projection, and recovery;
- it tests whether the visual language actually improves understanding before building the full presentation.

**First-build acceptance criterion:** after viewing it, a reader should be able to explain in ordinary language why an integer hit represents actual-orbit compatibility and why the hit's loss from the cap peak controls the candidate optimum.

---

## 16. Second build target

After the cap slice works, build the strongest CC information-loss demonstration:

### **Separate marginals versus joint compatibility**

Use A-ray q=4, parent P2.

Show:

- H range contains an integer;
- S range reaches a safe value;
- the two facts cannot occur at the same point;
- conditional same-orbit S interval removes the false witness.

**Acceptance criterion:** the viewer should be able to state:

> "Both conditions can be true somewhere without being true together."

This is the cleanest visual demonstration of why Compatibility Calculus preserves relationships rather than merely facts.

---

## 17. Third build target

Build the query-specific compression ladder:

full cells → B caps → A conditional intervals → A two-segment selector.

**Acceptance criterion:** the viewer should understand that none of these representations is "the final true model." Each is adequate for a declared question and can fail when the requested output changes.

---

## 18. What not to do

- Do not turn a sampled animation into evidence.
- Do not hide exact fractions behind only decimal values.
- Do not infer a 3D picture from an approximate point cloud when exact cell data exist.
- Do not show an ambient safe point as if it were an actual runner witness.
- Do not show positive-duration regions without separately rendering singleton equality witnesses when the question includes them.
- Do not flatten disconnected unions into one interval unless the operation proves that is valid.
- Do not reuse A-ray clock/orbit/lap maps for B-ray visuals.
- Do not imply the two-segment selector finds the optimum.
- Do not imply the seven top caps replace the full model for every question.
- Do not describe internally reviewed proof candidates as established external mathematics.
- Do not broaden the work into a general CC software platform before the first three visual targets demonstrate value.

---

## 19. New-thread execution instruction

When starting the implementation thread, begin with this file:

**notes/CC_VISUAL_PRESENTATION_PLAN_2026_09_29.md**

Then read, in order, only as needed:

1. notes/CC_REPRESENTATION_RULES.md
2. notes/CC_OTHER_RAY_REVIEW_2026_09_29.md
3. notes/CC_SIX_SEVEN_TRANSFER_2026_09_29.md
4. notes/CC_BOUNDED_SELECTOR_2026_09_29.md
5. the exact certificate directories listed in Section 3.

The implementation thread's first task should be **Phase 0 + Phase 1**, followed by the **Top cap → first integer hit → physical witness** vertical slice. Do not start by hand-drawing the entire deck.

---

## 20. Success definition

The project succeeds if the visual system helps a person answer questions that are currently difficult to hold in prose:

- What is the actual geometric object?
- Why do the seven top caps suffice for the B-ray upper-bound question but not for every threshold question?
- How does a cap become an arithmetic interval?
- Why does an integer hit correspond to a physical runner state?
- How is the physical witness reconstructed?
- Why can two true marginal statements fail to be true together?
- How can adding a constraint create a new relevant contact inside an old face?
- Why do isolated equality witnesses matter?
- Why can two segments be enough for one-witness selection while being inadequate for optimization?
- What information must a CC representation preserve for the question being asked?

If the visuals do not make those distinctions easier to see, revise the representation rather than polishing the presentation.
