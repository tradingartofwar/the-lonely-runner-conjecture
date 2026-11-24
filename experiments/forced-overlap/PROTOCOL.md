# Six 16-runner tests of pairwise overlap

Frozen before evaluation on this panel, November 24, 2026. The first-stage four-moving-speed rules and domain were already fixed in PR #4 at 7236871. Results for that first stage and exploratory tree checks in four moving speeds were known when this panel was chosen.

**Inputs.** The reference has speed zero. Use fifteen moving speeds f(j)+s for j=1,...,15, f(j) equal to j², j²+3j, or j³, and s equal to 1 or 5. Treat the six configurations as a structured challenge, with no statistical inference to arbitrary inputs. Preserve physical speeds as specified. The threshold is 1/16.

**Predictions to test.** Does keeping pairwise overlap certify at least one grid on each of the six inputs? Does it certify an input that the three-residue count leaves undecided on every grid? A single miss refutes panel-wide coverage. A grid certificate with lower count exceeding the true count invalidates the implementation.

**Procedure.** Test every distinct pair-sum denominator. Keep the original count, the three-residue count, and the direct witness at numerator 1. Independently evaluate the Hunter lower bound on a maximum-weight spanning tree of the signed classes, using exact sizes of all two-class intersections. Compare each bound with the full grid on the original speeds. Count tuples and grids separately. Recover a physical numerator when one exists and directly check its distances. Log empty and inconclusive grids. Different tuples sharing a denominator count separately. No retuning or substitution of a family after the run.

**Verification and cost.** Validate the arithmetic intersection algorithm exhaustively against a direct count for every modulus 2 through 60, every pair of folded residues including zero, and thresholds 1/5 and 1/16. Use integer operations and record the number of pair-size queries and exact-grid locations. Arithmetic query counts and brute-force verification costs have different units. Failure of a bound to certify a tuple leaves the Lonely Runner question for that tuple to the exact baseline.

