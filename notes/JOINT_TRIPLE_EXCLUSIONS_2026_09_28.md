# Two simultaneous triple bounds repair the collective-only window

September 28, 2026 UTC. Baseline `01c3ea2658a51e138f89837bf16ab44f16c81007`, draft PR #3. Material AI involvement: a coordinating agent and three complementary agents supplied the primary calculation, a separately structured exact verifier, and adversarial review. This is internal AI work, not independent human mathematical validation.

**Question.** On the archived collective-only window, what smallest subset of the four actual inclusive-triple upper bounds rules out every complete cover compatible with the total, single, and pair durations?

**Outcome.** Two bounds suffice, and exactly two pairs are inclusion-minimal within the frozen four-coordinate contract. With residual blockers `A=15`, `B=38`, `C=61`, and `D=100`, the two repairs are

| Simultaneous physical bounds | Exact minimum uncovered duration `U` |
| --- | ---: |
| `T_ABC<=0`, `T_ABD<=0` | `49/524400` |
| `T_ACD<=1/48800`, `T_BCD<=119/231800` | `13/22800` |

Every singleton and the other four pairs still admit an exact simultaneous complete-cover countermodel. The frozen cardinality/physical-lexicographic rule selects the first pair even though the second gives the stronger numerical lower bound. No post-result reranking occurred.

All four triple bounds together recover the physical duration `1/600`. A supplied collective bound `H<=99/185440`, where `H=sum T-Q`, also recovers `1/600`, but its present derivation uses all four physical triple durations and the four-way duration. This study does not produce a cheaper geometric route to `H`.

**Status.** OBSERVED/REPRODUCED in one frozen selected-reference window, its reflection check, and three existing controls. “Smallest” means least cardinality among subsets of these four supplied coordinate bounds at their exact physical values. It is not an unrestricted information-minimality, operation-count, selector, existence, or novelty theorem.

## 1. Frozen contract

The [protocol](../reviews/2026-09-28-joint-triple-exclusions/protocol.json), SHA256 `ad4746abe0a7b34ff0e4c63a1a3f1b18fab9ddbdb06a42da702e7a75b9f5db78`, was saved before calculation. It fixes:

- velocities `{0,7,8,15,23,38,61,100}`, reference `0`, threshold `1/8`;
- core `{7,8,23}`, residual blockers `{15,38,61,100}`;
- `J=[33/184,39/184]`, with physical `U=1/600`;
- pair constant `C_0=6121/2781600` and four-way duration `Q=0`;
- inclusive-triple upper bounds, in physical lexicographic order,
  `0, 0, 1/48800, 119/231800`;
- all sixteen subsets ordered first by cardinality and then by their lists of physical speed triples;
- exact primal/dual certificates for every optimization and an exact simultaneous cover countermodel for every zero optimum;
- separate controls `strict_16`, `doubling_112`, and `tight_13`, plus a read-only comparison with the earlier symmetric abstract model.

The charged scope is exactly 52 optimizations: sixteen target coordinate subsets, sixteen strict16 subsets, one doubling112 pair-only baseline, sixteen tight13 subsets, and three collective-bound comparisons. No new speed, core, window, reference, alternate-window search, broad scan, `+7/+9` work, or paid computation was added.

## 2. Complete target subset lattice

Write the four physical triple coordinates as

- `ABC={15,38,61}` with upper bound `0`;
- `ABD={15,38,100}` with upper bound `0`;
- `ACD={15,61,100}` with upper bound `1/48800`;
- `BCD={38,61,100}` with upper bound `119/231800`.

The exact minima are:

| Supplied subset | `min U` |
| --- | ---: |
| none | `0` |
| any singleton | `0` |
| `ABC, ABD` | `49/524400` |
| `ACD, BCD` | `13/22800` |
| any other pair | `0` |
| `ABC, ABD, ACD` | `49/524400` |
| `ABC, ABD, BCD` | `49/524400` |
| `ABC, ACD, BCD` | `13/22800` |
| `ABD, ACD, BCD` | `13/22800` |
| all four | `1/600` |

Thus the two displayed pairs are both inclusion-minimal and cardinality-minimal. Every three-coordinate success contains one of them and is not inclusion-minimal. Adding one remaining coordinate to a minimal pair does not improve its optimum; both remaining coordinates are needed to reach the full physical duration. The conclusion is stronger than the previous one-coordinate failure but narrower than a general geometric selection result.

The nine zero target cases retain compatible nonnegative mass tables satisfying all bounds in the subset simultaneously. These countermodels matter: separate covers witnessing individual failures would not settle the joint quantifier. They are abstract measurable-event distributions, not claims of alternative constant-speed runner realizations, and `U=0` does not rule out isolated safe points.

## 3. Why the pairs work

The optimal duals reduce to already-known five-edge `K_4`-minus-one-edge corrections. With `C_0=L-sum D_i+sum O_ij`, they are

`U >= C_0-O_CD-T_ABC-T_ABD`

and

`U >= C_0-O_AB-T_ACD-T_BCD`.

They follow from `U+H=C_0` and the elementary containments

`T_ACD+T_BCD-Q <= O_CD`,

`T_ABC+T_ABD-Q <= O_AB`.

Numerically they give `49/524400` and `13/22800`. This explains the consequential distinction: a complete cover can move higher-order burden away from any one queried triple, but it cannot do so after both triangles sharing the complementary pair are simultaneously capped.

The inequalities themselves are prior project work in [FOUR_BLOCKER_CYCLE_CORRECTIONS.md](FOUR_BLOCKER_CYCLE_CORRECTIONS.md), section 5. The contribution here is the exact subset-lattice minimality result and its countermodels on the preserved physical target, not a new graph inequality. The known sparse triple-exclusion selector and two-speed alternate-window dispatch also remain prior work and are not rediscovered here.

## 4. Full-coordinate and collective comparisons

The full coordinate result has a direct check:

`U=C_0-sum T+Q >= 6121/2781600-99/185440=1/600`.

The physical atom table attains equality. Therefore all four coordinate upper bounds recover exactly `1/600`; the exhaustive optimization independently agrees.

Supplying the one scalar `H<=99/185440` yields the same bound through `U+H=C_0`. It is one optimization input, but the current exact value of `H` was computed from all four triple durations and `Q`. Treating that scalar as a cheap practical query would hide its derivation cost. A compact speed-derived bound on `H`, or a cheap rule that selects one of the two successful coordinate pairs, remains open.

The reflected interval `[145/184,151/184]` has the exact reversed cell sequence and identical moments and atoms. It is a symmetry check, not a second independent configuration or another LP campaign.

## 5. Controls and abstract comparison

- `strict_16`: the only inclusion-minimal coordinate repair is its already-known `T_{6,11,16}=0`, giving `1/896`.
- `doubling_112`: the empty subset already gives the pair-only lower bound `761/32256`; no higher-order lattice is charged.
- `tight_13`: every coordinate subset and its collective bound have minimum `0`. The point `t=3/8` remains a valid isolated equality, with speed `11` blocking immediately to the left and speeds `5` and `13` immediately to the right.

The earlier symmetric abstract four-event model was rechecked read-only. Each of its fifteen proper zero-triple subsets is compatible with a cover. The present physical target behaves differently because its asymmetric pair moments permit two proper two-coordinate repairs. This comparison shows why zero individual minima alone do not determine joint sufficiency.

## 6. Exact verification

Artifacts are under [reviews/2026-09-28-joint-triple-exclusions/](../reviews/2026-09-28-joint-triple-exclusions/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-joint-triple-exclusions/primary.py --check
python -S -B reviews/2026-09-28-joint-triple-exclusions/verify.py --check
```

The primary archive contains exact rational primal/dual certificates for all 52 prescribed optimizations. The separately authored verifier imports neither primary functions nor its LP helper; it uses threshold-event reconstruction and its own exact two-phase Bland-rule simplex. It performed 883 exact pivots and matched every optimum.

The independent reconstruction checked 108 physical threshold cells: 17 target, 17 reflection, 9 strict16, 57 doubling112, and 8 tight13. It also checked all 33 zero-optimum coordinate countermodels, including 9 target, 8 strict16, and 16 tight13 cases, and all 195 proper-subset monotonicity comparisons in the three full lattices. Endpoint semantics, the physical lexicographic ranking, retained moments, all-order atoms, and the target reflection agree exactly.

The [adversarial review](../reviews/2026-09-28-joint-triple-exclusions/challenge.md) found no fatal defect within the frozen scope. It independently checked signs, quantifiers, monotonicity, the direct full-set calculation, controls, prior-work boundaries, and the difference between supplied-scalar and derivation cost.

## 7. Next bounded question

Freeze the selected zero-bound pair before calculation and seek one shared geometric certificate for

`B_15 intersect B_38 subset Safe_61 intersect Safe_100`

on the same target window. Count the exact lap/interval or arithmetic information needed to certify both exclusions together, then test the unchanged certificate format on strict16, doubling112, and tight13. Compare its cost with the already-known sparse two-test selector and preserve any failed control without retuning.

This asks whether the selected two-coordinate repair can be discovered and verified from a compact common occurrence statement rather than by reconstructing four complete triple durations or enumerating the subset lattice. It does not authorize new speeds, windows, references, broad scans, or a claim that such a selector exists generally.
