# Ultra review — summary for the team

September 27, 2026. This preserves the complete reader-facing summary accompanying the six-reviewer assessment. The findings are developed in greater detail in the [main Ultra review](ULTRA_REVIEW_2026_09_27.md), which links all six reports, derivations, verification artifacts, and research priorities. Material AI involvement and claim-status limits are recorded there.

**The Ultra review points toward a shift: we now understand several ways information gets lost. The next challenge is selecting where a useful witness can be found.**

Six reviewers examined arithmetic, geometry, optimization, rigor, literature, and strategy. The central calculations survived their scoped checks. All six executable verification groups passed. The general arguments remain proof candidates.

The most useful findings:

1. **Our strongest local failure still has plenty of global lonely time.** Throughout the `1680h` family, every joint-duration statistic agrees—even over the full cycle. Yet the chosen window alternates between an isolated lonely instant and nothing. Meanwhile, every member has the same positive global lonely duration, `45/448`, and an explicit strict witness elsewhere. Losing local detail does not necessarily prevent proving global existence.

2. **Knowing where boundaries meet is still insufficient.** The 1680/3360 examples share the same opposing-contact schedule and equality controllers. Another runner determines whether the candidate survives. We derived a complete contact selector **conditional on zero clear duration**; each selected point must then pass every runner's constraints.

3. **“Higher-order information” contains another distinction.** The 266/532 pair has identical pair statistics and identical lists of possible overlap states, but different clear durations. Knowing that a triple overlap is possible is insufficient—we need its amount. Separately, exact optimization found pair-only inequalities stronger than our best tree bounds.

4. **Changing the threshold reveals what a fixed-threshold summary hides.** This is the most productive additional “dimension” found in the review. An isolated lonely instant expands into an interval immediately when we lower the required separation. A near miss needs a positive relaxation first. We derived the exact distinction across the family:

   \[
   \max_{t\in J}\min_i\|v_it\|=
   \begin{cases}
   1/8,&h\text{ odd},\\
   y/[8(y+3)],&h\text{ even},
   \end{cases}
   \qquad y=1680h.
   \]

   The argument received a separate mathematical check and exact component checks.

5. **Dimension alone misses the clock.** A thought experiment produces rational runner systems with the same orbit dimension but different maximum separation. The improved alignment requires an increasingly long observation period. We need to distinguish dimension, winding, target geometry, and time required to reach it.

Vance's idea that information lives **in the relationships** now has a precise interpretation: the runners occupy a shared phase space constrained by one clock and integer relations. The promising LTCMs—**Languages That Carry Models**—are lattice geometry, modular arithmetic, piecewise-linear geometry, optimization, and dynamics with quantitative time bounds. The literature also supplies relevant machinery connecting rational contacts, slopes, and residue errors: Jain and Kravitz, [*Relative Lonely Runner spectra*, arXiv:2411.12684v2](https://arxiv.org/html/2411.12684v2), especially Lemmas 2.4–2.5. The main review and its literature report state the reading scope and limits.

**Recommended next investigation:** take our existing difficult configurations and examine every eligible three-runner core and its complete openings. Determine whether our certificate succeeds *somewhere*. One strict configuration where every such certificate fails would justify richer certificate information; successful cases would focus attention on finding the right opening efficiently.

The complete findings, derivations, limits, and three prioritized investigations are in [ULTRA_REVIEW_2026_09_27.md](ULTRA_REVIEW_2026_09_27.md), with all six reports and reproducible checks linked inside.

## Scope needed to read the summary on its own

The `1680h` family consists of eight common-start runners with speeds `{0,1,3,4,5,10,28,1680h}`, positive integer h, selected reference 0, and threshold `1/8`. Its chosen window is `J=[9/32,3/8]`. Equality at the threshold is allowed. The separate 266/532 comparison uses `{0,1,4,5,6,7,11,y}` on the same J and threshold. These are scoped examples; they are not counterexamples to Lonely Runner or claims that the full conjecture has been proved. The recommended all-core investigation is proposed work, not a completed experiment.
