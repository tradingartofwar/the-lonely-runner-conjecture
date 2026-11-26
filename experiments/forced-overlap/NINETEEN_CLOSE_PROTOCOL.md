# Protocol for three close fast speeds over the second core

**November 24, 2026.** The [preceding result](NINETEEN_TWO_ADDITIONS.md) covers three arbitrary additions to $Q=\{0,1,\ldots,14,105\}$ when the slowest is at least 1680 and both successive gaps are at least 420. Test the complementary family with slowest speed at least 1680 and both successive gaps in $[1,420]$. Keep the boundary 420 in both tests. All nineteen reference runners count.

Use the previously checked intervals for the sixteen fixed references. For a newcomer of speed $R$, the two other newcomers have absolute speed differences $d,e\le840$. Seek a rational center time $t_0$ where the fixed phases leave a circular gap of length at least $2/19+105/1680$, and where each difference $j\in\{d,e\}$ has distance from an integer at least $1/19+j/(2\cdot1680)$. Move time by at most $1/(2R)$ so that the phase of $R$ reaches the midpoint of that circular gap. Check all inequalities with integers or exact fractions.

First test all unordered pairs $1\le d\le e\le840$ using reduced center times in $[0,1/2]$ of denominator at most 128. This stronger domain covers the gap pairs for all three roles. If pairs remain, try the centers $k/4093$ on the same half-circle. Record the number left after each attempted stage. A missing center leaves the rule inconclusive for that pair. Neither a bounded speed scan nor the absence of an observed collision establishes the infinite-speed claim.

Direct controls use slowest speed 1680 and successive gaps $(1,1),(419,419),(420,420),(1,419),(419,1),(60,360)$. Test all nineteen roles separately with exact distances. Also test $(1,1)$ after raising the slowest speed by one and after a large translation of the three newcomers. Gap 420 defeats every unshifted center of denominator 2 through 7 for that difference. Report remaining speed ranges and preserve the shared manuscript as its review baseline.

AI assistance contributed the proposed test. This protocol precedes the center search.
