# Separate condition-masked semantic grading review

I recommend retaining the initial numerical grades at both stages: **53/54 primary successes for first answers and 53/54 for final answers**. R010 is the one clear failure. R040 receives primary credit under the contextual reading, with the initial broad-reading sensitivity preserved. There are no recommended numerical disagreements with `INITIAL_GRADES.json`; there is one additional handoff wording observation for S12, recorded separately in the retention audit.

This recommendation follows a semantic review of **all 54 preserved answers**, not just flagged rows. All first/final pairs are identical. The packet contains 108 initial stage-grade rows, whose paired fields are identical apart from stage. Every delivered handoff exactly matches its masked summary; every delivered full source exactly matches its authorized history; every query matches the key’s exact query. No recovery was requested or served and no followup source was supplied. Both stages remain recorded; their duplicate values are not 108 independent observations.

The six histories establish truth. Only each query’s named hypothetical replaces source assumptions. I used `review/ORACLE_COMPARISON.md` as the controlling item-level optionality instruction. Correct conclusions may rely on adequate source-true cached decisions. I did not require old packet numerators, a recited acceptance threshold, extra explanation of other alternatives, or unchanged timing details unless the exact query requests them. Volunteered assertions were still checked.

## History-level comparison before aggregation

The summaries remain identified only by opaque packet IDs. A cell lists primary successes out of the three questions for that summary or source control; both stages have the same scores.

| History | Masked handoff 1 | Masked handoff 2 | Full-source answers | All preserved answers |
|---|---|---|---:|---:|
| H01 | S04: 3/3 | S12: 3/3 | 3/3 | 9/9 |
| H02 | S02: 3/3 | S10: 3/3 | 3/3 | 9/9 |
| H03 | S01: 3/3 | S08: 3/3 | 3/3 | 9/9 |
| H04 | S09: 2/3 | S11: 3/3 | 3/3 | 8/9 |
| H05 | S05: 3/3 | S06: 3/3 | 3/3 | 9/9 |
| H06 | S03: 3/3 | S07: 3/3 | 3/3 | 9/9 |

Across question kinds, current decision is 18/18, evidence scope 17/18 and changed use 18/18. Handoff answers total 35/36 and full-source answers 18/18. All cells are observed and completed. Under R040’s broader reading, only changed use drops to 17/18, S09 to 1/3, H04 to 7/9 and the aggregate to 52/54 per stage (handoffs 34/36). This is wording sensitivity, not missingness or an additional run.

## Contested cases and adjudication

**R010 — retain failure.** The exact requested second output asks whether the stored backup content includes the two post-M0 changes. The response says: “Inclusion of the post-M0 addition K97 revision 1 and the change to K12 revision 2 is not established” and “Their actual presence is unresolved, rather than proven absent.” It correctly gives one object, but substitutes a destination-audit question for fixed backup content.

The delivered S09 passage is: “H02–H03: M0 contains K1–K96 revision 1; backup-east and archive-copy alias one stored object, object-amber, not independent copies.” Its delta ledger names K97 revision 1 and K12 revision 2. Source H02–H03 fixes object-amber as M0; H08–H09 places both changes after M0; H12 preserves the backup identity and contents. Missing destination ingestion/verification does not leave the contents of this fixed backup unknown. The response’s stated rationale therefore does not support its answer to the actual query.

I challenged whether S09 failed to state the object-to-snapshot relation explicitly enough. It does not use S11’s clearer “containing only M0,” but the shared H02–H03 sentence’s snapshot and alias clauses support that ordinary contextual relation. Semantic scoring does not require a formal database edge or repeated “contains” verb. The recommended retention assessment is adequate, and the downstream error is a recipient object/scope confusion. An unusually literal reading can regard that compressed relation as an exposure gap; even then it cannot make the full-source backup answer unknown or supply the requested exclusion answer. A generous reading that treats the uncertainty sentence as an aside solely about the destination likewise leaves the requested backup-inclusion output unanswered. Neither defense restores primary credit. The preferred flags remain requested=0, exposed=0, faithful=0, primary=0, unsupported assertion=1, unsupported approval=0, unnecessary abstention and recipient_error. The alternative scope interpretations are preserved here rather than silently used to erase the failure.

**R040 — retain contextual pass and sensitivity.** The response begins: “The two successful comparisons raise verification to 96 M0 snapshot matches, but only 95 of 97 current key/revisions are verified.” It then correctly names both delta gaps and says they must be synchronized and verified. Its final sentence is: “The planned work remains unexecuted.”

The preferred reading refers to the immediately discussed remaining delta synchronization/verification, so it is consistent with the hypothetical. This fits both the correct opening and the supplied requirement that only two comparisons have now completed. The broader reading refers to all H11 planned work, including those two comparisons; that is false under the hypothetical. Preserve this as a genuine wording sensitivity. On that broader reading requested outputs stay correct, but exposure support and source faithfulness fall to 0, primary falls to 0 and unsupported assertion becomes 1. Unsupported approval stays 0: retirement is refused under either reading. The subsequent-writes sentence is conditional and does not invent an actual extra source change.

**S12 — added retention observation, no recipient regrade.** The summary says “no booking completion is recorded” after mentioning C’s afternoon transport and room availability. R11 already refers to “the room booking” while also asking the successor to report readiness before a booking choice. A narrow station-booking interpretation is supportable; a broad denial of any room booking is not. The audit records both. R041, R046 and R053 do not repeat this clause, and they correctly distinguish technical eligibility from logistics. This ambiguity does not remove any requested technical support and supplies no basis for penalizing those answers.

## Complete answer-level recommendations

The table records both recommended primary stage scores. Requested, exposed and faithful are the three separate semantic fields. The initial values are retained in every row. All protocol-valid flags remain true based on the packet’s successful parse/schema/cap checks and visible response records; this does not certify unseen execution procedures. Unsupported approval is 0 throughout. Unsupported assertion is 0 except R010=1. Error mechanism is `none` except R010=`recipient_error` (object/stage scope confusion). Under the initial reporting convention, R014, R020, R025, R027, R034 and R046 retain `source_itself_underdetermined`; this describes the correct limited-performance/classification answer, not a failure to respond. R010 retains `unnecessary`; all other abstention fields remain `none`.

| Answer | Query | Exposure | Requested | Exposed | Faithful | First / final primary | Review rationale |
|---|---|---|---:|---:|---:|---:|---|
| R001 | H05-Q1 | S06 | 1 | 1 | 1 | 1 / 1 | BC output 16 and resource totals (8,9,8) match; its sole-feasible status is retained in S06. |
| R002 | H05-Q2 | S05 | 1 | 1 | 1 | 1 / 1 | Rental changes only staff; AB uses (9,11,9), giving staff spare 1, memory excess 2 and power excess 1. |
| R003 | H06-Q1 | S03 | 1 | 1 | 1 | 1 / 1 | Capacity, ninety-minute booked interval, full leader coverage and headphone exemption are complete; no-setup and no-extra-approval claims are also supported. |
| R004 | H02-Q1 | S02 | 1 | 1 | 1 | 1 / 1 | One late unique sample U out of three, with calibrated delays 1,1,3 and the retry identity preserved. |
| R005 | H01-Q1 | Full source | 1 | 1 | 1 | 1 / 1 | C alone; A has both missing current tests and disabled buffering; B has only the runtime deficit. All volunteered measurements agree with R03–R12. |
| R006 | H05-Q3 | S06 | 1 | 1 | 1 | 1 / 1 | AC output 14 and (7,10,7) fit (8,10,8); the optional AB excess of one in every resource is correct. |
| R007 | H05-Q2 | Full source | 1 | 1 | 1 | 1 / 1 | Correct staff-only hypothetical, quantified remaining memory and power violations, and rejection. |
| R008 | H04-Q1 | S09 | 1 | 1 | 1 | 1 / 1 | 93 current matches, four correctly identified revision-specific gaps and no retirement; old K12 and missing-audit explanation are supported. |
| R009 | H03-Q3 | S01 | 1 | 1 | 1 | 1 / 1 | C2 has 1/0/11, with the correct eleven missing IDs and exact-version acceptance rejection; no C1 outcome transfer. |
| R010 | H04-Q2 | S09 | 0 | 0 | 0 | 0 / 0 | One object is correct, but backup inclusion is wrongly called unresolved by importing destination-stage uncertainty; see contested-case analysis. |
| R011 | H04-Q2 | S11 | 1 | 1 | 1 | 1 / 1 | One shared M0 object and exclusion of both later changes are expressly retained by S11. |
| R012 | H02-Q1 | Full source | 1 | 1 | 1 | 1 / 1 | One late U among three; exact calibration and retry treatment support every volunteered assertion. |
| R013 | H04-Q1 | Full source | 1 | 1 | 1 | 1 / 1 | Correct 93/97 count and four gaps. Excluding K12 from K1–K94 gives 93; labels, ingestion, preview and plans do not add verification. |
| R014 | H02-Q3 | S02 | 1 | 1 | 1 | 1 / 1 | Common-offset formulas, closed endpoints, classifications and simultaneous all-pass witness are all correct. |
| R015 | H04-Q2 | Full source | 1 | 1 | 1 | 1 / 1 | One fixed M0 object includes K1–K96 r1 and neither later change; retaining K12 r1 is correctly scoped. |
| R016 | H06-Q1 | Full source | 1 | 1 | 1 | 1 / 1 | All requested workshop explanations and volunteered capacity, booking-history and reservation assertions follow from O01–O12. |
| R017 | H03-Q1 | S08 | 1 | 1 | 1 | 1 / 1 | C1 rejects with 9/2/1 and required failure/untested names; even a B4 pass only reaches ten. |
| R018 | H03-Q3 | S08 | 1 | 1 | 1 | 1 / 1 | C2 has 1/0/11 and does not pass; listed untested IDs and unchanged X exclusions are correct. |
| R019 | H05-Q1 | S05 | 1 | 1 | 1 | 1 / 1 | BC is the unique feasible optimum, with all requested output/resource totals correct. |
| R020 | H01-Q2 | Full source | 1 | 1 | 1 | 1 / 1 | Unknown current packet performance and invalidated old-firmware result are correctly distinguished from observed failure or deterioration. |
| R021 | H06-Q3 | Full source | 1 | 1 | 1 | 1 / 1 | 24 participants exactly meet all three capacities. Timing/headphone restatement is optional and need not be demanded. |
| R022 | H05-Q2 | S06 | 1 | 1 | 1 | 1 / 1 | AB remains infeasible after rental with excess memory 2 and power 1; BC remains sole feasible pair under those caps. |
| R023 | H02-Q1 | S10 | 1 | 1 | 1 | 1 / 1 | One late U among three with delay 3; “delivery time” means elapsed delay in the sentence, not absolute gateway time. Retry adds no sample. |
| R024 | H06-Q2 | S03 | 1 | 1 | 1 | 1 / 1 | Each independent capacity has spare 2 and overall spare is 2; the maximum total is 24. |
| R025 | H02-Q3 | S10 | 1 | 1 | 1 | 1 / 1 | Offset interval classifications, [2,4) failure subset for U and common endpoint all-pass are exact; retry identity remains correct. |
| R026 | H06-Q3 | S03 | 1 | 1 | 1 | 1 / 1 | 24 meets all three limits and leaves no places or spare kits; unchanged plan remains feasible. |
| R027 | H01-Q2 | S04 | 1 | 1 | 1 | 1 / 1 | The old 99% meets the numerical threshold but is expressly invalid as firmware-8 evidence; no claim of preserved current performance is made. |
| R028 | H06-Q3 | S07 | 1 | 1 | 1 | 1 / 1 | 24 meets room, kit and two-leader limits exactly; no spare participant capacity remains. |
| R029 | H05-Q1 | Full source | 1 | 1 | 1 | 1 / 1 | BC and requested totals correct; optional AC memory-only and AB all-resource violations match the final caps. |
| R030 | H02-Q2 | S10 | 1 | 1 | 1 | 1 / 1 | Neither stage simultaneous; arrivals 101/101.5 and half-second order correct. Shared insertion does not establish arrival simultaneity. |
| R031 | H01-Q1 | S04 | 1 | 1 | 1 | 1 / 1 | C alone and both other stations’ reasons correct. Old badge is not current evidence, and B’s order is still unfulfilled/unmeasured. |
| R032 | H02-Q2 | Full source | 1 | 1 | 1 | 1 / 1 | Acquisition values, signed conversion, reference arrivals and database distinction all agree with source. |
| R033 | H06-Q1 | S07 | 1 | 1 | 1 | 1 / 1 | Every requested feasibility explanation is present, including booked timing and exemption; capacities and leader exclusions are accurate. |
| R034 | H02-Q3 | Full source | 1 | 1 | 1 | 1 / 1 | Correct common-offset classifications and endpoint witness, with no invented separate offsets or fourth sample. |
| R035 | H03-Q2 | S08 | 1 | 1 | 1 | 1 / 1 | 9/11 and 9/12 with authorized prior exclusions; B4 is untested and difficult cases stay included. |
| R036 | H01-Q3 | S04 | 1 | 1 | 1 | 1 / 1 | BC become ready under the explicit valid-pack hypothetical. Current seven-second limit, C equality and A evidence gaps are all respected. |
| R037 | H03-Q3 | Full source | 1 | 1 | 1 | 1 / 1 | C2 1/0/11 and rejection correct; no inheritance and the listed cohort/exclusions agree with source. |
| R038 | H03-Q2 | Full source | 1 | 1 | 1 | 1 / 1 | Both fractions and distinct denominators correct; exclusions precede outcomes and untested B4 is not made a failure. |
| R039 | H05-Q3 | Full source | 1 | 1 | 1 | 1 / 1 | AC output/resource totals and changed caps correct; optional AB rejection correctly identifies all three violations. |
| R040 | H04-Q3 | S09 | 1 | 1 | 1 | 1 / 1 | Requested decision, 95 current matches and remaining delta blockers are correct; contextual final sentence refers to remaining delta work. Preserve broad-reading sensitivity. |
| R041 | H01-Q1 | S12 | 1 | 1 | 1 | 1 / 1 | C alone; A and B exclusion reasons correct. Separating technical eligibility from booking/signoff is source-true; S12’s no-booking-completion clause is not repeated. |
| R042 | H04-Q3 | S11 | 1 | 1 | 1 | 1 / 1 | Two new audits yield 95 current matches and 96 M0 matches; both delta revisions remain gaps. Checking possible future writes is conditional. |
| R043 | H03-Q2 | S01 | 1 | 1 | 1 | 1 / 1 | Fractions 9/11 and 9/12 and prior X exclusions correct; inclusion of B4 in only the authorized denominator is supported. |
| R044 | H02-Q2 | S02 | 1 | 1 | 1 | 1 / 1 | Neither acquisition nor arrival simultaneous; reference arrivals 101/101.5 and insertion explanation are correct. |
| R045 | H04-Q3 | Full source | 1 | 1 | 1 | 1 / 1 | No retirement; 95 current matches, 96 M0 matches and K12 r2/K97 r1 gaps. Missing verification is not asserted to be mismatch. |
| R046 | H01-Q2 | S12 | 1 | 1 | 1 | 1 / 1 | Unknown upgraded performance and invalidation are fully answered. Omission of the old 99/100 value is explicitly permitted. |
| R047 | H03-Q1 | Full source | 1 | 1 | 1 | 1 / 1 | C1 9/2/1 and required case names correct; optional exclusions and C2 version distinction remain accurate. |
| R048 | H05-Q3 | S05 | 1 | 1 | 1 | 1 / 1 | AC output 14 and (7,10,7) correct under memory-only change; AB exceeds all three revised caps. |
| R049 | H03-Q1 | S01 | 1 | 1 | 1 | 1 / 1 | C1 counts, failure/untested IDs and rejection correct; B4-only completion cannot satisfy the threshold and C2 does not replace C1 evidence. |
| R050 | H06-Q2 | Full source | 1 | 1 | 1 | 1 / 1 | Separate spare capacities and simultaneous overall limit are all 2, yielding attendance 24. |
| R051 | H01-Q3 | Full source | 1 | 1 | 1 | 1 / 1 | BC new ready set and why B changes are correct; v2 latency replaces v1, C equality remains valid and A still lacks tests/buffering. |
| R052 | H06-Q2 | S07 | 1 | 1 | 1 | 1 / 1 | Room, kits, staffing and overall spare all 2; leader exclusions from participant cap and kit needs are supported. |
| R053 | H01-Q3 | S12 | 1 | 1 | 1 | 1 / 1 | BC ready after the valid 8.5-hour test, with all other facts unchanged; A remains excluded. Logistics separation is true and the ambiguous booking clause is not repeated. |
| R054 | H04-Q1 | S11 | 1 | 1 | 1 | 1 / 1 | No retirement; 93 current matches and the four gaps are correct. In this current-cutoff question the planned work is indeed unexecuted. |

## Source checks and limits

The independent semantic checks covered the firmware/version and proposal/adoption relations (R01, R03–R12); the signed clock relation, common-offset endpoints and acquisition identity (C01, C03–C12); prespecified exclusions, denominators and candidate-specific results (J01–J02, J04–J12); backup identity versus destination stages and snapshot versus current revisions (H01–H12); additive resource requirements and independent hypothetical options (D01–D12); and simultaneous capacities, complete booking/leader confirmation and headphone exemption (O01–O12). Optional explanations were checked where offered, not added as new output requirements.

This is a separate internal AI review conducted after collection closed. I read only the authorized masked packet, initial grades, scoring instructions, key, optionality comparison and six histories. I did not read a condition map, method prompts, schedules, configuration, run records, broader repository or earlier results, and made no network or participant calls. The review is condition-masked only to that extent: prose style can reveal a method, and initial grades were visible, so it is neither secure blinding nor independent human certification.

The packet permits verification of the answers and their supplied evidence, not an independent reconstruction of collection, assignment or hidden protocol execution. No numerical method effect can be assigned from opaque summary IDs. The retention audit identifies plausible interpretation mechanisms; it does not causally isolate wording effects. The final recommendation preserves the original packet and initial grade file unchanged and adds no optional trial expansion.
