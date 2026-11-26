# Same collision summary, opposite answers at 11/32

**Coordinator handoff · November 26, 2026 · Opened development control.** Use this pair when evaluating a cheaper endpoint test. The existing residue-membership checker already distinguishes the lineups. A proposed replacement should explain which observation lets it do the same.

**DISPROVEN for this endpoint.** At anchor 1/3, the identities of every collider together with the count, minimum and maximum in *each* residue class modulo 3 suffice to decide whether the stationary reference is safe after the first forward escape of the slowest collider. The following pair refutes that sufficiency claim.

**OBSERVED.** All 16 runners start together. The 15 moving speeds are the nonempty subset sums of the four weights. The two inputs produce exactly the same summaries:

| Residue modulo 3 | Number of speeds | Smallest | Largest |
|---|---:|---:|---:|
| 0 | 5 | 6 | 48 |
| 1 | 5 | 1 | 43 |
| 2 | 5 | 5 | 47 |

The colliders in both are 6, 18, 30, 42 and 48. Speed 6 needs 1/96 time to move 1/16 of a lap. The proposed endpoint is therefore 1/3 + 1/96 = 11/32 for both lineups.

| Four weights | Minimum clearance at 11/32 | All limiting speeds | Reference meets 1/16? |
|---|---:|---|---|
| (1, 5, 13, 29) | 1/32 | 29, 35 | No |
| (1, 5, 17, 25) | 1/16 | 6, 26 | Yes, at equality |

An exact modular check exposes the missing distinction. At 11/32 a speed *v* is unsafe exactly when 11*v* has residue 0, 1 or 31 modulo 32. Multiplying by 3, the inverse of 11 modulo 32, gives forbidden **speed** residues 0, 3 and 29. The first lineup has speeds 35 and 29 in those classes. The second has none. For this particular endpoint a single yes/no membership query suffices. How to cheaply choose endpoints that will pass remains open. This pair concerns one fixed candidate and one reference. It does not rule out sound sufficient tests that sometimes abstain.

**Replay from the repository root**

```sh
python3 -m observatory.escape_trial.check_collision_summary
```

The replay compares the actual [extrema representation](rule.py) and [membership checker](reentry_membership.py) with exact distances computed directly from the 15 speeds in each lineup. Expected output: the first lineup fails with minimum 1/32 and the second passes at exactly 1/16.

**Research origin.** An AI-assisted comparison of the November 25 Cogentic papers suggested looking for two inputs that agree under a proposed summary and give opposite answers to the same query. The edge-reconstruction paper makes the allowed relabellings explicit. The log-rank paper uses an exact identity retained by Boolean inputs. The [Cogentic system paper, §§2.1–2.3](https://arxiv.org/html/2609.40324v2) describes retaining verified intermediate claims separately from attempted explanations. The calculation above uses elementary modular arithmetic and is independent of those papers' proof claims. [Six-manuscript release](https://github.com/google-research/google-research/tree/3f540f420bfae7e6ce48365a68d0ae003feb2f87/cogentic_research_papers)

**Pickup for the Observatory.** Treat the inputs as exposed controls. For any candidate summary of the noncolliders, specify its inputs, compare the summaries on both lineups, and record whether the rule decides or abstains. To test generalization, freeze the proposed rule before drawing further matched pairs. Keep the live last-anchor comparison's held-out score separate.
