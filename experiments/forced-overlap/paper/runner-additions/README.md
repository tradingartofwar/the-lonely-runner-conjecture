# Fast-runner extensions for two families of lonely runners

Vance Williams, Lonely Runner Project. Working paper for independent mathematical review, November 24, 2026.

## Read or edit

Open `main.tex` as the main document in Overleaf. Select pdfLaTeX and recompile. The manuscript uses standard TeX Live packages and its bibliography is embedded. The Python programs are for checking the mathematics separately.

## Reproduce

Extract the complete project into an empty directory. From its top level use Python 3.11 or later with assertions enabled. The programs use the standard library and run offline.

```sh
python reproduce.py
python reproduce.py --panels --regenerate
```

The default command verifies all finite witnesses and the inequalities for the infinite ranges. It checks the archived mathematical evidence against `SHA256SUMS`. The extended command also repeats the two endpoint studies, compares their complete outputs, and regenerates the three certificates. The code uses a temporary directory for regenerated files.

| Experiment | Exact finite cases | Archive |
| --- | ---: | --- |
| 17 runners, core P and any one addition | 948 speeds, 16,116 role checks | `seventeen_family_results.json` and `seventeen_family_witnesses.csv` |
| 18 runners, core P and any two additions | 16,566 pairs, 298,188 role checks | `eighteen_family.json.xz` |
| 18 runners, core Q and any two additions | 30,386 pairs, 546,948 role checks | `eighteen_transfer.json.xz` |

All three rows refer to every physical runner as a separate reference. The separate selected-reference panels contain 53,805 configurations for 17 runners and 21,760 for 18. The transfer verifier also checks the failed time and its repair at added speeds 420 and 480. All file paths in the table are relative to `experiments/forced-overlap/`, which also contains the frozen protocols.

[Underlying research, immutable snapshot](https://github.com/tradingartofwar/the-lonely-runner-conjecture/tree/b693d00938d0f320eab9c8c0349c08e8bb8b10cb/experiments/forced-overlap). Repository terms accompany the archive in `LICENSE`, `LICENSE-CODE` and `LICENSE-CONTENT.md`.
