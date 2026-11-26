# Two-endpoint experiment fixed before execution

November 24, 2026. Work at distance 1/16 for the stationary reference. Delete the largest integer speed V. Each core contains 14 distinct positive speeds. Compare the Two-Endpoint Fast-Runner Lemma with the following arithmetic refinement before consulting the full tuple's safe times.

For distinct retained speeds u,w let g=gcd(u,w) and S=u+w. For a component containing a 1/15 witness with left endpoint set by u and right endpoint set by w, the scaled width D=16uw(b-a) obeys D+S = 0 modulo 16g and D >= S/15. Use the least such integer D, giving a sufficient cutoff V >= max(2uw/D) over pairs. Compare with 30LM/(L+M), where L and M are the two largest retained speeds. A surviving pair in this test is a possibility. Measurements count a tuple once whenever its V reaches the indicated cutoff.

- Dense panel: all 14-element subsets of the integers 1 through 16.
- Fixed controls, reported separately: 1 through 13 together with 17, 1 through 13 together with 26, and the odds 1 through 27. Check the known component [1/16,15/224] of the consecutive core and the controls V=15 and 210.
- Sparse panel: for seeds j=0 through 7 choose one speed from each of 14 consecutive blocks of length 6. For i=0 through 13 the speed is 6i+1 plus the first byte of SHA-256 of the ASCII string endpoint/j/i modulo 6, substituting the decimal integers for j and i.
- For each core test all integers M < V <= 15M. Record coverage under both rules, additional certifications, and unresolved predictions. Retain cases with no improvement as well as improvements.
- As a separate check, compute the exact 1/16 core components containing a 1/15 witness. For every V certified by the arithmetic rule, each of these components must yield an exact full witness. Verify physical distances. For V=M+1, 2M, 5M, 10M, 15M also compare component survival with the full interval solver. Any discrepancy invalidates the run. All scores are descriptive of these panels.
