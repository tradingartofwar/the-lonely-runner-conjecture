# One containment query: capacity versus occurrence complexity

September 28, 2026 UTC. Baseline `65f0148c15ed08248250198107b60c9d961569eb`, draft PR #3. Material AI involvement: one coordinating agent, one exact-calculation agent, one separately structured exact-verification agent, and one adversarial-review agent. This is internal AI work, not independent human mathematical validation.

**Question.** Among base pairs with positive potential five-edge slack `C_0-O_cd`, can a predeclared cheap rule select the useful shared containment with only one compound complement query?

**Outcome.** The two frozen rules separate sharply on the archived target:

| Rule | Selected base pair | Potential slack | Positive base components | Containment | Outcome |
| --- | --- | ---: | ---: | --- | --- |
| largest potential slack | `{61,100}` | `3071/2781600` | 3 | fails | no certificate; no retuning |
| fewest positive occurrence components | `{15,38}` | `49/524400` | 1 | holds | `U>=49/524400` |

The larger conditional bound chooses the false containment. Its first exact positive violation is speed 38 on `(55/304,29/160)`, with midpoint `1101/6080`. The failed rule is retained without querying another pair. The component rule chooses the previously known one-component table `(63/304,5/24)` and reproduces the two zero triples and positive five-edge bound.

**Status.** OBSERVED for four supplied selected-reference windows under the frozen contract. This is a useful finite distinction, not held-out selector validation, a general rule, new existence coverage, or a runtime theorem. The successful target pair and its component table were visible in the preceding study.

## 1. Frozen information and computation contract

The [protocol](../reviews/2026-09-28-one-containment-selector/protocol.json), SHA256 `42c3fe75734e7fc137b3ffc9de805172661acb988b3d39162517adb50028a607`, was saved before selector calculation. For a base pair `{a,b}` with complement `{c,d}` it defines

`potential slack = C_0-O_cd`.

Only strictly positive slacks are eligible. The two rules are:

1. maximize potential slack, physical-speed lexicographic ties;
2. minimize the number of maximal positive-length components of `B_a intersect B_b` among eligible pairs, physical-speed lexicographic ties directly.

Each rule receives at most one compound query

`B_a intersect B_b subset Safe_c intersect Safe_d`.

There is no fallback pair. If both rules select the same pair, they may reuse one physical calculation. Strict blockers use distance `<1/8`; equality belongs to the closed safe set. Tight13's isolated endpoint and doubling112's pair-only exit remain separate branches.

The component rule has the explicitly larger information contract. It counts every eligible candidate before selection, not only the selected table. Across the batch this means ten pair intersections containing 29 positive components. On the target its two eligible candidates are complementary pairs, so it reads occurrence complexity from both sides even though it does not inspect either candidate jointly with its complement.

## 2. Exact target distinction

The six exact target slacks leave only two eligible pairs:

| Eligible base | Complement | Slack | Components |
| --- | --- | ---: | ---: |
| `{15,38}` | `{61,100}` | `49/524400` | 1 |
| `{61,100}` | `{15,38}` | `3071/2781600` | 3 |

Maximizing capacity therefore selects `{61,100}`. Containment fails before any reinterpretation: both a base occurrence and speed 38 block throughout `(55/304,29/160)`. This is a local certificate failure, not a failure of loneliness; the archived actual clear duration is `1/600`.

The fewest-components rule selects `{15,38}`. Its one shared occurrence lies in both complementary safe sets, so

`T_(15,38,61)=T_(15,38,100)=0`

and the prior five-edge correction yields `49/524400>0`. This reproduces an already known geometric repair; the increment is the frozen comparison of selection rules.

## 3. Controls

| Case | Largest-slack rule | Fewest-components rule | Correct interpretation |
| --- | --- | --- | --- |
| strict16 | `{6,11}`, certifies `1/896` | `{6,11}`, certifies `1/896` | exact tie with unused `{11,16}` is broken lexicographically; one physical query reused |
| doubling112 | diagnostic `{56,112}`, fails | diagnostic `{56,64}`, fails | pair-only optimum `761/32256>0` exits before selection |
| tight13 | no eligible pair; no query | no eligible pair; no query | duration remains zero on the window; valid isolated equality `t=3/8` retained |

The two doubling failures have exact positive witnesses: speed 72 blocks the `{56,112}` base on `(175/576,39/128)`, and speed 112 blocks the `{56,64}` base on `(183/512,321/896)`. They do not weaken the independent pair-only certificate. Tight13's zero slack is not eligible; lack of a duration query does not invalidate its endpoint.

No eligible empty base pair occurs in this batch. The frozen rule would select one by a zero component count and its containment would be vacuous, but that specified branch remains untested.

## 4. What was learned—and what was not

Potential slack measures the size of a five-edge lower bound *conditional* on a geometric containment. It does not measure whether that containment is true. The target gives an exact counterexample to conflating those questions.

Occurrence complexity carries relevant placement information here: the one-component target pair succeeds while the three-component alternative fails. But this is a development case, not a held-out prediction. Counting components also enumerates speed-dependent pair geometry. The study does not show that the rule is cheaper than the repository's known sparse arithmetic tests, scalable, or successful on arbitrary windows.

The sparse triple-exclusion selector, its alternate-window dispatch, the strict16 repair, and the five-edge inequality are prior repository results. No novelty claim is made for them. The present result is selected-reference only and says nothing about every reference runner or whole-configuration coverage.

## 5. Verification and delegation

Artifacts are under [reviews/2026-09-28-one-containment-selector/](../reviews/2026-09-28-one-containment-selector/). Reproduce read-only with:

```bash
python -S -B reviews/2026-09-28-one-containment-selector/primary.py --check
python -S -B reviews/2026-09-28-one-containment-selector/verify.py --check
```

The primary calculation evaluates 24 slacks, ten eligible pair tables, six logical queries, and five unique physical containments; three logical queries succeed, three fail, and none issues a second query. The independent implementation reconstructs all interval geometry from speeds and windows, imports no primary code, and compares 142 critical fields with zero disagreement. Adversarial review found no fatal mathematical defect after catching and requiring repair of an initial verifier-schema mismatch.

The calculation, independent reconstruction, and hostile review were performed by three complementary AI agents. Agreement among them is useful error control, not independent mathematical validation.

## 6. Next bounded question

The promising information is the *ordering* of eligible pair occurrence counts, but the present rule obtains it by enumeration. Freeze a new investigation on these same archived cases: derive a speed-and-window arithmetic formula or certified upper/lower ordering for positive components of `B_a intersect B_b` without constructing all pair intervals, then test whether it reproduces the frozen component selector. Preserve ties and failures; do not add speeds, windows, references, complement queries, broad scans, or revive the parked `+7/+9` campaigns.

This next step asks whether the observed placement signal can be made genuinely cheaper. It does not presume that the component rule generalizes.
