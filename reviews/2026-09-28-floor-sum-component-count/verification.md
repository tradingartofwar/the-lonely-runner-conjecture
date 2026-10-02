# Independent floor-sum component-count verification

**Status:** PASS

The verifier does not import `primary.py`. It enumerates every integer
point in each inherited lap rectangle, independently evaluates both
half-planes by fixed-`n` column prefixes, and rebuilds positive pair
components by an exact blocker-endpoint event sweep.

| case | exact pair counts | selected eligible pair | archive match |
| --- | --- | --- | --- |
| `collective_target` | 15/38=1, 15/61=1, 15/100=1, 38/61=2, 38/100=2, 61/100=3 | 15/38 | yes |
| `strict_16` | 6/7=0, 6/11=1, 6/16=1, 7/11=1, 7/16=0, 11/16=1 | 6/11 | yes |
| `doubling_112` | 56/64=2, 56/72=3, 56/112=6, 64/72=3, 64/112=5, 72/112=4 | 56/64 | yes |
| `tight_13` | 6/7=0, 6/11=1, 6/13=1, 7/11=1, 7/13=1, 11/13=0 | none | yes |

Primary comparison: compared 173 critical fields.

Strictness controls exclude both `D=-S` at `t=3/8` and `D=+S` at
`t=5/8` for `(a,b)=(3,5)`: each is a zero-length contact, not a
positive component.

Scope: 24 pairs, 410 rectangle points, 287 open event cells, and 41 positive components. This is separately structured internal AI verification, not independent
human mathematical validation.
