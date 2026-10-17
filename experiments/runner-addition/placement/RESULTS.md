# Placement results — a short rule and an exact boundary

October 17, 2026. **Completed bounded study.** The rational-anchor rule explains
all three earlier single-interval 1/10 certificates. The two additional pairs
have no universally sufficient individual core component: every component has
an explicit blocking added speed. All 13 complete-core checks at those blocking
speeds still have witnesses. The distinction between source failure and physical
nonexistence is therefore visible in the saved data.

Exact finite records pass alternate verification and one byte-identical replay.
The symbolic rule, family extensions and universal implications remain **proof
candidates**, with same-author verification and no novelty claim.

## 1. What placement means exactly

For a closed interval I=[a,b], let c=(a+b)/2 and h=(b-a)/2. At threshold d, an
added positive integer speed r leaves a safe opportunity in I exactly when

`distance(r*c, nearest integer) + r*h >= d`.

If this fails, the entire interval fits inside one open unsafe band centered
on an integer. The saved blocking integer m satisfies the strict inequalities
`r*b-d < m < r*a+d`. Equality remains safe.

This separates center placement from width while expressing the same exact
contact decision as the prior algorithm. It does not establish a new complexity
bound or speed advantage. All 1,888 prior saved contacts agree with the predicate.

## 2. A constructive explanation for the earlier three families

Choose a reduced rational anchor u/v with v*d<=1. Suppose the interval from
u/v to u/v+e*d/v, for fixed direction e=-1 or +1, is safe for the fixed core.
Then a physical witness after adding any positive integer speed r is

```
v does not divide r:  t = u/v
v divides r:          t = u/v + e*d/r
```

In the first case the added runner is at least 1/v>=d from an integer. In the
second it is exactly distance d away, and the adjustment stays inside the safe
interval because r>=v. The same common interval keeps all core runners safe.

At d=1/10 the predictions from the frozen rule all pass:

| Original pair | Anchor | Direction | Core-safe adjustment interval | Eligible individual core speeds |
| --- | --- | ---: | --- | ---: |
| (1,2) | 1/8 | -1 | [9/80,1/8] | 28 |
| (1,4) | 1/9 | -1 | [1/10,1/9] | 36 |
| (1,6) | 3/10 | +1 | [3/10,31/100] | 36 |

Each adjustment interval lies in its original widest component. All 108 declared
physical witness controls pass, including very large speeds both divisible and
not divisible by the anchor denominator.

**A broader sufficient family follows from the same proof.** The rule's integer
residue inequalities identify all individual speeds safe throughout each common
adjustment interval. Those sets have sizes 28, 36 and 36, respectively, and are
listed in the machine-readable results. Any eight distinct speeds chosen from
one such set, with reference 0 and any distinct positive integer ninth moving
speed r, satisfy the same reference-0 1/10 argument. These are combinations
certified by a shared interval, not separately chosen incompatible witnesses.
We did not enumerate the combinations or claim a general ten-runner theorem.

The full proof and residue conditions are in [THEORY.md](THEORY.md). A formula
is useful here because its hypotheses are checkable. Its failure must retain
the possibility of another formula, another interval, or several intervals.

## 3. Where the simple pattern stops

The added cases keep the earlier coefficient family
`(0,1,q,1+q,2+q,3+q,3+2q,6+2q,3+8q,r)` and threshold 1/10.
We chose q=8 and q=10 after the rule was committed, before constructing their
cores. Their selection intentionally tests the rule's limitations:

- For q=10, speed 83 exceeds the rational-anchor class's proved maximum 80.
- For q=8, speed 67 requires denominator at least 9, but core speeds 9 and 10
  exclude the only allowed denominators 9 and 10 by making the anchor unsafe.

Those facts predict no certificate of this restricted kind. They do not predict
failure of every connected component. The full interval calculation adds that
stronger, class-specific finding:

| Pair | Complete core components | Components with a blocker | Components without a resolved decision | Distinct recorded blocking speeds | Full core succeeds at those speeds |
| --- | ---: | ---: | ---: | --- | ---: |
| (1,8) | 26 | 26 | 0 | 2,3,4,5,6,7 | 6/6 |
| (1,10) | 34 | 34 | 0 | 2,3,4,5,7,8,9 | 7/7 |

All 60 components have positive width. For each one, an exact admissible added
speed blocks that entire component. Because every connected core-safe interval
is contained in a complete component, its component's blocker defeats it too.
Thus changing the chosen interval cannot rescue the universal single-interval
strategy for either core. Integer speeds give period 1, so another integer
translate of an interval does not change the conclusion.

This is a limit of the fixed connected-interval representation. It does not
establish an intrinsic lower bound for arbitrary encodings or algorithms. It
does not exclude input-dependent choices among intervals.

Two concrete examples show where the answer survives:

| Pair | Widest component | Added speed that blocks it | Safe time recovered elsewhere |
| --- | --- | ---: | --- |
| (1,8) | [231/670,39/110] | 3 | 31/220 |
| (1,10) | [41/130,269/830] | 3 | 11/100 |

The quantifiers matter: **each component has some blocker**. This is not the
claim that one speed blocks all components. All recorded blocking-speed inputs
have a safe time elsewhere in the complete core.

Complete all-r coverage and minimum multi-component menus for these two new
cores were not evaluated in this protocol. The 13 recovered witnesses do not
establish those stronger statements. The previous three families retain their
separately recorded all-r candidates.

## 4. Evidence and reproduction

Rule commit, before validation selection:
`8ecfaae521f80eca72fb137549d67f019452fbd2`.
Execution freeze, before any new evaluation:
`bf1c84c84bad2a0b1afd2172b9c71a6acd25c854`.

- Exact Fraction primary evaluation: midpoint obstruction, modular residue
  palettes, and the unchanged repository complete-core checker.
- Alternate verification: safe-band intersection, complete threshold-event
  decomposition, and constant-lap endpoint checks; no primary/checker imports.
- Matched: 1,888 old contacts, 108 anchor witnesses, 216 palette candidate-speed
  decisions, 60 new components, 270 new contact decisions, 13 complete child
  sets and their witnesses. Event reconstruction used 4,978 event positions.
- Five predeclared equality, placement, singleton and lap-wrap controls pass.
- All new component decisions resolve below budget. One primary replay is
  byte-identical. No execution defect or post-execution source change occurred.

Same AI author for both algorithms; no independent human or formal proof review.
The added pairs may have appeared in historical repository scans; this study
does not label them globally held out. A limited literature discovery search
did not complete a full-text comparison, so novelty remains unassessed.
No minimum menu search, wider parameter scan or performance benchmark was run.

From the repository root, with Python 3.12 and a checkout containing the freeze:

```bash
placement_run=$(mktemp -d)
timeout 60s python experiments/runner-addition/placement/run.py \
  --freeze bf1c84c84bad2a0b1afd2172b9c71a6acd25c854 \
  --output "$placement_run/RESULTS.json"
timeout 60s python experiments/runner-addition/placement/verify.py \
  --input "$placement_run/RESULTS.json" --output "$placement_run/VERIFICATION.json"
cmp experiments/runner-addition/placement/results/RESULTS.json "$placement_run/RESULTS.json"
```

Saved [results](results/RESULTS.json), [verification](results/VERIFICATION.json),
[replay](results/REPLAY.json), [protocol](PROTOCOL.md), and [manifest](manifest.json).
Primary result SHA-256:
`898718248bf12c68795a494a134b5c54ba8eeefb493a68834b6fc68f63273a44`.

## 5. Next question

Determine the smallest sufficient component menu containing each core's fixed
widest interval for q=8 and q=10, using that interval for the infinite tail and exact coverage of its complete finite
remainder. The earlier set-cover implementation supplies a starting point;
freeze the new cases and scope before execution. Preserve failure if the full
core misses a required speed rather than forcing a successful menu.

This would answer whether a small collection repairs the demonstrated limit,
and make the choice of representation follow evidence. It would not require
assuming either that every explanation is simple or that complexity is intrinsic.
