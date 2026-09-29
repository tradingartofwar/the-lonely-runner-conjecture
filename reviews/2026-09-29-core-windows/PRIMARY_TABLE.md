# Exact primary core-window table

**OBSERVED** exact arithmetic on the frozen 31-value domain. The all-fast-residual
implication is a **HYPOTHESIS / proof candidate**, conditional on the three-train
span argument. Equality is safe. The selected window is the earliest widest
positive closed component; all ties and isolated points are retained in JSON.

| a | Selected closed window | Width w_a | Sufficient b >= B_a | Widest ties | Isolated points |
| ---: | --- | --- | ---: | ---: | ---: |
| 2 | [9/32, 3/8] | 3/32 | 19 | 2 | 0 |
| 3 | [1/8, 7/40] | 1/20 | 35 | 2 | 2 |
| 6 | [17/40, 15/32] | 7/160 | 40 | 2 | 0 |
| 7 | [17/56, 3/8] | 1/14 | 25 | 2 | 2 |
| 8 | [9/32, 23/64] | 5/64 | 23 | 2 | 0 |
| 9 | [1/8, 7/40] | 1/20 | 35 | 2 | 0 |
| 10 | [5/16, 3/8] | 1/16 | 28 | 2 | 0 |
| 11 | [25/88, 31/88] | 3/44 | 26 | 2 | 2 |
| 12 | [9/32, 31/96] | 1/24 | 42 | 4 | 0 |
| 13 | [33/104, 3/8] | 3/52 | 31 | 2 | 0 |
| 14 | [33/112, 39/112] | 3/56 | 33 | 2 | 0 |
| 15 | [9/32, 13/40] | 7/160 | 40 | 2 | 2 |
| 16 | [41/128, 47/128] | 3/64 | 38 | 2 | 0 |
| 17 | [1/8, 23/136] | 3/68 | 40 | 4 | 0 |
| 18 | [41/144, 47/144] | 1/24 | 42 | 2 | 0 |
| 19 | [49/152, 55/152] | 3/76 | 45 | 4 | 2 |
| 20 | [49/160, 11/32] | 3/80 | 47 | 2 | 0 |
| 21 | [7/24, 55/168] | 1/28 | 49 | 4 | 0 |
| 22 | [57/176, 63/176] | 3/88 | 52 | 2 | 0 |
| 23 | [25/184, 31/184] | 3/92 | 54 | 4 | 2 |
| 24 | [25/192, 31/192] | 1/32 | 56 | 6 | 0 |
| 25 | [1/8, 31/200] | 3/100 | 59 | 6 | 0 |
| 26 | [5/16, 71/208] | 3/104 | 61 | 4 | 0 |
| 27 | [65/216, 71/216] | 1/36 | 63 | 4 | 2 |
| 28 | [33/224, 39/224] | 3/112 | 66 | 8 | 4 |
| 29 | [33/232, 39/232] | 3/116 | 68 | 6 | 0 |
| 30 | [11/80, 13/80] | 1/40 | 70 | 8 | 0 |
| 31 | [33/248, 39/248] | 3/124 | 73 | 6 | 2 |
| 32 | [33/256, 39/256] | 3/128 | 75 | 10 | 0 |
| 33 | [1/8, 13/88] | 1/44 | 77 | 8 | 0 |
| 34 | [41/272, 47/272] | 3/136 | 80 | 8 | 0 |

For a < b < c < d, the bound is obtained from
`T3 = 1/(4b)+1/(2c)+1/d <= 7/(4b) <= w_a`.
This table does not enumerate b,c,d or establish the remaining cases below B_a.
No all-reference, full-conjecture, or novelty claim is made. This calculation
was materially AI-assisted and awaits the stated independent comparison.

Reproduce from the repository root with:
`python reviews/2026-09-29-core-windows/primary_core_windows.py`.
