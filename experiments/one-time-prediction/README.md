# Does the representation predict a time on unseen inputs?

We froze one rule before seeing 240 test lineups. It picks a denominator from divisibility information and returns **one** physical time for the stationary runner. It inspects up to fifteen denominators in preprocessing. It makes no scans through time, retries or comparisons of final candidate clearances. The four sampling distributions were known to the rule designer. A separate team member chose the seed and generated the actual lineups without testing for witnesses. The original protocol records SHA-256 commitments to the panel and generator. [Frozen protocol and predictor](https://github.com/tradingartofwar/the-lonely-runner-conjecture/tree/43c53db25b707f8053f2f8f2175ff264bafab050/experiments/one-time-prediction).

| Panel, 60 each | Selected anchor alone | Always shift forward if needed | Choose direction from the speeds | Any reduced time with denominator at most 32 |
|---|---:|---:|---:|---:|
| Progression with two to four outliers | 30 | 41 | 41 | 60 |
| Three residue classes | 59 | 59 | 59 | 60 |
| Uniform speed samples | 52 | 55 | 57 | 60 |
| Ten slower and five faster opponents | 53 | 58 | 58 | 60 |
| **Total** | **194** | **213** | **215** | **240** |

The anchor is $1/q$, for one denominator chosen using only which speeds are divisible by each candidate $q$. For $q\le16$, it is automatically safe if no speed is divisible by $q$. The 194 such successes require no directional prediction. In the 46 remaining lineups both shift rules use distance $1/(16b)$, where $b$ is the slowest speed colliding at the anchor. The relational rule chooses the direction in which the other runners have more time before leaving their safe arcs. It found a witness in **21 of 46**, versus **19 of 46** for always forward. Three cases favored the directional choice and one favored always forward. Neither rule retries a miss. An exhaustive exact interval calculation subsequently found a witness in every lineup.

For example, one held-out lineup had stationary reference zero and moving speeds $20,30,50,60,70,80,90,100,110,120,130,140,150,232,344$. The chosen anchor was $1/13$ and the colliding speed was 130. The predicted backward shift to $159/2080$ gives exact minimum clearance $1/16$ across all fifteen opponents. The forward shift fails. The small-denominator comparator also solves this lineup at another time.

The result demonstrates prospective witness selection. Two net hits compared with the same-distance forward rule on this finite panel leave the advantage of directional information uncertain. The larger grid solved all 240. A stronger claim would require an independently selected class and a proof that the rule succeeds throughout that class, or an advantage that persists against a comparably budgeted alternative. The disclosed input distributions, fixed number of candidates, comparison with the successful grid and retained misses are essential when interpreting the figures.

Run from the repository root with Python 3.11 or later. The panel is regenerated from its committed seed; the scoring script checks its digest. It constructs the entire prediction list before running verification.

    python experiments/one-time-prediction/generate.py /tmp/lr_panel.json
    PYTHONPATH=. python experiments/one-time-prediction/score.py /tmp/lr_panel.json

