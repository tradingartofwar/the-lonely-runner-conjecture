# Development record

All ten cases and the implementation were written before the first full run;
`FREEZE.json` records that boundary. Selected SymPy API probes had already been
seen, so the demonstration was always labelled exposed development regression.
One exploratory API-probe command had a parenthesis syntax typo, corrected before
it ran. That did not generate or change a candidate result.

The frozen first implementation passed all ten cases and 120 exact substitution
checks. A second execution produced identical report bytes. Those records are
preserved as `INITIAL_REPORT.json` and `INITIAL_REPRODUCTION.json`.
The exact initial source is preserved as `INITIAL_DEMO.py`, checked against the
`FREEZE.json` SHA256. For an initial-version replay, copy the package to a temporary
directory and restore that source as `demo.py`; the source has a literal `demo.py`
provenance filename, so running the archival filename directly is not an accurate
source-binding replay.

Subsequent AI static review found an unexecuted-path discrepancy: the protocol
said to stop on unsupported input/result, whereas `main` recorded an error and
continued. The implementation now stops after an `UNSUPPORTED` or `ERROR`
record, and the summary checks all ten requested cases rather than just completed
records. No input, adapter algorithm, oracle, or successful-case output changed.
This is a control-flow correction after the freeze, not a pristine first-run claim
about the final source hash. The updated report and reproduction record carry the
final source hash. The ten-case run does not exercise these error branches.

The two-minute execution limit is enforced by the recorded external `timeout 120`
command, not by an internal alarm. Removing that wrapper removes the time limit.
