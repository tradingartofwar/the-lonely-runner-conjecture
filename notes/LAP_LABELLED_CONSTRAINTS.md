# Shared-clock constraints: retain which lap produced the overlap

September 25, 2026. Baseline `3817153be1a6bd892c33a5b9019deb9ae6571ec4`.

**Question:** Which shared-clock information rules out Ultra's artificial zero-clear arrangement with the same individual and pairwise blocking totals?

**Result:** the pair summaries merge different blocking occurrences of the same runner. Labelling an occurrence by `(speed, lap)` makes the incompatibility explicit. A forest on these individual intervals recovers the exact clear duration in all five previously selected local controls, including the two where the fixed runner graph was inconclusive.

**Status:** OBSERVED exact facts for five fixed local cases, with a self-contained elementary interval argument proposed below. The general argument is an AI-assisted reconstruction awaiting independent review; no originality or general Lonely Runner theorem is claimed. This reuses the interval objects from [BLOCKING_CHAINS.md](BLOCKING_CHAINS.md) and graph bounds from [LR2_REVIEW_PRIORITIES.md](LR2_REVIEW_PRIORITIES.md). AI materially supplied derivation, code, checks, and writing.

## 1. Keep the occurrence label

Use eight total runners, stationary reference 0, core `{1,4,5}`, extras `{6,7,11,w}`, threshold `delta=1/8`, and the unchanged core-safe window

$$J=[9/32,3/8].$$

A positive speed v blocks the reference around its m-th completed lap during

$$I_{v,m}=J\cap\left(\frac{m-\delta}{v},\frac{m+\delta}{v}\right).$$

These are single intervals. The full blocked set for runner v is their union. The integer m identifies the nearby meeting with the reference, not necessarily the floor of vt throughout the interval. Threshold endpoints are excluded; clipping endpoints of J are included when the strict blocking inequality holds there.

At w=16 there are exactly six positive-length intervals. The table gives endpoint values; open/closed distinctions are handled separately from duration.

| Speed | Lap m | Left endpoint | Right endpoint |
| --- | ---: | ---: | ---: |
| 11 | 3 | 9/32 | 25/88 |
| 7 | 2 | 9/32 | 17/56 |
| 16 | 5 | 39/128 | 41/128 |
| 6 | 2 | 5/16 | 17/48 |
| 11 | 4 | 31/88 | 3/8 |
| 16 | 6 | 47/128 | 3/8 |

Their only positive-length pair intersections are:

| First occurrence | Second occurrence | Duration |
| --- | --- | ---: |
| (11,3) | (7,2) | 1/352 |
| (16,5) | (6,2) | 1/128 |
| (6,2) | (11,4) | 1/528 |
| (11,4) | (16,6) | 1/128 |

The occurrence graph consists of one four-vertex path and one separate edge. Merging occurrences that belong to the same runner creates the earlier triangle with an attached edge. Thus a cycle in the runner graph need not represent simultaneous overlap.

## 2. The artificial triple has no consistent lap assignment

In J, any overlap of runners 6 and 16 uses speed 16's lap 5 occurrence. Any overlap of 11 and 16 uses speed 16's lap 6 occurrence. If 6,11,16 all blocked at one time, the same occurrence of speed 16 would have to participate in both pairs. The required lap sets `{5}` and `{6}` are disjoint.

Ultra's modified distribution assigns mass `1/896` to exactly this triple. It therefore cannot be realized by the specified speeds on this window. The script reconstructs the alteration and verifies that total mass, all four individual durations, and all six pair durations are nevertheless unchanged.

Equivalently, the 6/11 pair only overlaps on `(31/88,17/48)`, where speed 16's phase lies between `7/11` and `2/3`. This recovers the earlier exclusion in a different representation, rather than claiming a newly found opening.

The relation `6+16=2*11` alone does not exclude simultaneous blocking: all three block at t=0. It must be combined with the local window and compatible phase/lap information. A necessary phase identity is not the full orbit restricted to J.

## 3. An elementary interval-forest identity

Let finitely many intervals I_i lie in a bounded window J. Ignore endpoint choices only for the duration calculation. Give each vertex weight `d_i=|I_i|` and each positive-overlap edge weight `o_ij=|I_i intersect I_j|`. Let W be the maximum total weight of a forest in this graph. The proposed reconstruction is

$$\left|J\setminus\bigcup_i I_i\right|=|J|-\sum_i d_i+W.$$

**First direction, valid for arbitrary measurable events:** for any forest F and any nonempty active set of vertices, its induced edges number at most the number of active vertices minus one. Integration gives

$$\sum_{ij\in F}o_{ij}\leq\sum_i d_i-\left|\bigcup_i I_i\right|.$$

**Reverse direction, using single intervals:** sort intervals by nondecreasing left endpoint. For each interval, select as parent an earlier interval with the greatest right endpoint, if it overlaps; otherwise start a new component. Edges point to earlier vertices, with at most one parent per vertex, so they form a forest. Within the new interval, the union of all earlier intervals has exactly the same duration as its overlap with that parent: earlier intervals start no later, and none ends later than the parent's right endpoint. Each selected edge therefore accounts for the full duration counted twice when this interval is added. Summing proves that this forest attains the upper bound on W.

This covers containment, tied endpoints, disconnected groups, and real endpoints. The construction is a restatement of elementary interval-union geometry, not a proposed novel graph theorem. S18 provides the broader graph-bound context; S20 records standard interval-graph terminology. The script computes a maximum-weight forest from pair durations using Kruskal's algorithm and separately constructs the parent forest from endpoint order.

Pairwise intersection of finitely many single intervals also implies common intersection: choose the greatest left endpoint and smallest right endpoint. Positive pair overlaps make the former strictly smaller than the latter. Unions of disjoint intervals do not share this property. This explains why changing the unit represented by a vertex matters.

## 4. Exact controls

| Replacement w | Occurrences | Positive pair edges | Three-occurrence intersections | Clear duration from occurrence forest | Direct phase check |
| --- | ---: | ---: | ---: | ---: | ---: |
| 13 | 5 | 4 | 0 | 0 | 0 |
| 14 | 6 | 6 | 2 | 1/112 | 1/112 |
| 15 | 5 | 3 | 0 | 1/112 | 1/112 |
| 16 | 6 | 4 | 0 | 1/896 | 1/896 |
| 17 | 6 | 5 | 1 | 1/112 | 1/112 |

For w=14 and 17 actual triple intersections exist. The forest still gives exact duration; adding every pair indiscriminately would overcount. For w=16 every positive edge already belongs to a forest, so all four overlaps can be retained. Its clear interval is `[17/56,39/128]`.

The w=13 duration is zero but the valid time `t=3/8` survives. Direct evaluation of threshold boundaries preserves this distinction. Endpoint inclusion is not recoverable from durations alone.

Reproduce without altering archived results:

```bash
python -B reviews/2026-09-25-lr2/check_lap_constraints.py --check
```

[Script](../reviews/2026-09-25-lr2/check_lap_constraints.py) and [exact results](../reviews/2026-09-25-lr2/lap_constraints.json). Standard-library rational arithmetic; no project imports. The JSON pins the script hash. Checks compare two forest constructions with a direct threshold partition and phase evaluation. Scope is precisely these five selected-reference configurations and this one window; no new speed scan or independent reviewer is involved.

As a separate session crosscheck, the existing `lonely_runner.checker.feasible_intervals` routine was evaluated for all five complete speed lists and clipped to J. It agreed on every duration and on the singleton `[3/8,3/8]` for w=13. The previous LR 2 priority verifier also still passes. No original Ultra artifact was modified.

## 5. What this changes, and the remaining obstacle

The previous information barrier concerns **runner-level** single/pair totals. It remains valid. Pair totals for **individual interval occurrences**, together with their interval interpretation, carry enough extra structure to recover duration. Lap labels alone are insufficient without knowing which occurrences overlap or their endpoint constraints.

This puts Vance's LTCM question to work: inspect the distinctions lost when translating an actual trajectory into a smaller graph. A more expressive representation can repair a certificate without introducing a physical interaction or assigning a formal information-theoretic synergy value.

There is still no guarantee of positive slack. Constructing every occurrence and overlap re-expresses exact interval coverage; its size can grow with the speeds. It neither selects a successful core/window in advance nor proves an opening for all configurations. Isolated equality continues to need separate treatment.

**Next bounded question:** can speed arithmetic retain only selected occurrence labels and incompatibilities, enough to certify a useful graph without reconstructing the entire schedule? In this example one local disjoint-lap constraint for runner 16 suffices to exclude the problematic triple. Test a stated rule for selecting such constraints against w=14 and 17 before proposing a family statement. A general successful-window selection theorem remains OPEN.
