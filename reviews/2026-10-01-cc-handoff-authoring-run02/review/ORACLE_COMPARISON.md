# Source-first answer-key comparison

The independent source-first review was completed before receipt of the proposed key. It was then saved verbatim to `review/ORACLE_SOURCE_FIRST.md` and hashed before opening either `evaluator/QUESTIONS_AND_KEY.json` or `SCORING.md`.

Source-first SHA-256:

`d5654b914164b7e5a9f6ee70db6df16bd2043da5bebbd39cc902ffea707afb71`

All eighteen proposed substantive answers agree with the sealed derivations. The proposed key has no incorrect decision, count, fraction, resource sum, clock conversion, interval classification, identity relation, or version/current-revision treatment. No question requires a factual correction or has two materially different reasonable answers under the supplied assumptions.

The remaining concern is grading scope. Several strings in the key's `required` arrays combine requested outputs with optional explanations. SCORING.md correctly says those arrays are not permission to impose unasked details, and it explicitly exempts H01-Q2's old 99/100 value and H03-Q1's “at least eleven” wording. Read under that controlling instruction, the key and scoring can be applied consistently. Read as literal all-clause checklists, some key entries would reject sufficient answers. This report identifies those clauses before execution.

## Exact substantive agreements and scope qualifications

| Item | Agreement with the sealed derivation | Details that must not become independent requirements merely because the key includes them |
|---|---|---|
| H01-Q1 | C alone is ready. A has disabled buffering and no qualifying firmware-8 packet/latency evidence. B's 7.5-hour pack is below eight hours. | No issue with the listed reasons: the query asks why each other station is not ready. It does not additionally require reproducing every qualifying C measurement or logistics. |
| H01-Q2 | Packet performance after A's upgrade is unknown, with the old firmware-7 result invalid as current evidence. | The old 99/100 numerator and denominator are optional; SCORING.md already says this explicitly. |
| H01-Q3 | The new set is B and C; B's verified 8.5-hour pack resolves its only unmet condition. | The explanation can say B now meets the runtime requirement and its other qualifying attributes are unchanged. A separate recitation of packet rate, six-second latency, and buffer status is optional. Listing the eligible set already excludes A. |
| H02-Q1 | One late unique sample out of three, namely U. | The additional `required` sentence about using calibrated gateway arrival and merging U-retry describes the correct derivation. Explicitly narrating either step is not requested when the count, denominator, and identity are correct. |
| H02-Q2 | Neither acquisition nor arrival was simultaneous; reference arrivals are S=101 and T=101.5. | The clause about common database insertion is explanatory context, not a requested output. Acquisition timestamps and insertion timestamps need not be recited. |
| H02-Q3 | S/T are guaranteed passes, none is a guaranteed failure, U is unresolved, and simultaneous all-pass is possible at the common offset 4. Delay intervals [0,2], [0,2], and [2,4] agree exactly. | Numerical intervals and the offset-4 witness are sufficient supporting explanations, not separately requested outputs. Correct classifications and “yes, all three can pass” suffice. A separate “not guaranteed” sentence is unnecessary because the classifications already express it. If a witness or formula is supplied, it must respect one common offset and endpoint equality. |
| H03-Q1 | C1 does not pass: 9 passes, failures A8/B3, and untested B4. | A separate recitation of the 11-pass threshold is unnecessary; SCORING.md already explicitly exempts it. The query requires the failed and untested names, but not the nine passing names. |
| H03-Q2 | Evaluated fraction 9/11 and authorized-cohort fraction 9/12=3/4; two pre-evaluation exclusions explain why fourteen is not a denominator. | Naming X1/X2 is not necessary if the two authorized prior exclusions are accurately described. Naming B4 is useful but not separately requested; equivalent explanations distinguishing evaluated versus authorized cases suffice. Exact fractions do not need percentages as well. |
| H03-Q3 | C2 has 1 pass, 0 observed failures, 11 untested, and does not satisfy acceptance. | The passing case name B3 and a separate explanation forbidding C1 outcome transfer are not requested. Correct version-specific counts and acceptance status suffice. “Does not pass the finite rule” and “acceptance is not established” are equivalent here; neither asserts failures on the untested cases. |
| H04-Q1 | Retirement is not permitted. There are 93 verified current revisions among 97 current keys. Blockers are K95/K96's missing audits, added K97 revision 1, and changed K12 revision 2. | The standalone `required` sentence “Missing verification is not an observed mismatch” must not demand a disclaimer from an answer that already accurately describes missing verification. An answer asserting observed mismatches would be false. The query asks for the verified count; the total-current-key denominator 97 is helpful but not a separate requested number. |
| H04-Q2 | The two labels establish one object containing M0; it omits K97 and K12 revision 2 and retains K12 revision 1. | The object identifier `object-amber`, explicit key/revision identifiers, and the parenthetical old K12 revision are explanatory specifics, not separately requested outputs. One shared M0 object containing neither subsequent change answers both questions. |
| H04-Q3 | Retirement remains impermissible; 95 current revisions are verified, with K97 revision 1 and K12 revision 2 remaining unverified/unsynchronized. | The current-key denominator 97 is not independently requested. Describing the two remaining current-revision gaps need not additionally recite every ingestion-stage fact. |
| H05-Q1 | B/C maximizes feasible output: 16 output, staff 8, memory 9, power 8. | The second required sentence's rejection of the higher-output A/B proposal is optional explanation. Neither the other pairs' calculations nor a complete enumeration is requested. |
| H05-Q2 | Staff-only rental does not make A/B feasible: memory 11 exceeds 9, power 9 exceeds 8; staff 9 fits the new cap 10. | The remaining violations are requested and must be quantified. The extra explicit explanation that staff alone was resolved is optional when the correct memory/power violations and decision are supplied. |
| H05-Q3 | With caps (8,10,8) and required A inclusion, A/C gives output 14 and resources (7,10,7). | The query asks for the pair, output, and resource totals. Separately stating the changed cap tuple or explaining that B/C lacks A is optional. Choosing A/C already respects the inclusion requirement. |
| H06-Q1 | The 22-person workshop is feasible: room/kits/leader capacity 24, confirmed 10:00–11:30 inside 09:00–17:00, both leaders confirmed, headphones exempt before 11:00. | No material scope issue: the query explicitly asks for timing, headphones, and capacity. No hidden requirement should be added. |
| H06-Q2 | Each of room, kits, and leader ratio permits 2 more participants; overall capacity is 2. | An explicit sentence saying the spare counts are not added is optional when the four requested answers are correct. Claiming six overall would be wrong. |
| H06-Q3 | Yes: attendance becomes 24 and exactly meets all three capacity limits. | The second required sentence, “The booked time and headphone exemption remain valid,” is not requested. Nothing changed in those facts, and Q3 expressly asks for the new count and relation to the three capacities. Their omission must not lose credit. |

The source-first arithmetic checks also agree with every numerical key field: 119/120 exceeds 99%; the calibrated delays are 1, 1, and 3; all-pass under the common uncertain offset occurs at the included endpoint 4; current verification counts are 94-1=93 and 93+2=95; A/B requires (9,11,9); and every workshop spare capacity is 24-22=2. The key's rational representation `203/2` is exactly 101.5, and `3/4` is exactly 9/12.

## Required pre-execution clarification

No change is required to a history, a query, or a substantive answer. Before freezing execution materials, resolve the literal-checklist ambiguity in one of these equivalent ways:

1. Separate requested-output requirements from optional explanatory rationale in the key; or
2. Retain the current key but add explicit item-level scoring notes adopting the optionality distinctions in the table above.

This is a clarification of SCORING.md's existing rule, not a new obligation imposed on recipients. In particular, do not score an omission as an unsupported assertion. The strongest clean examples are H02-Q2's insertion-time explanation, H05-Q1's rejected A/B explanation, H05-Q3's rejected B/C explanation, and H06-Q3's unchanged timing/headphone explanation. Each is true, but each may be omitted from a complete answer to its query.

For illustration, these short answers satisfy the requested-output dimension, assuming sufficient delivered evidence supports them:

- H02-Q1: “One of three unique samples is late: U.”
- H02-Q2: “They were simultaneous at neither acquisition nor gateway arrival. Reference arrivals are S=101 and T=101.5.”
- H02-Q3: “S and T are guaranteed passes; none is a guaranteed failure; U is unresolved. Yes, all three can pass.”
- H03-Q3: “C2 has one pass, zero observed failures, and eleven untested cases. It does not pass the acceptance rule.”
- H04-Q1: “No. There are 93 verified current revisions. K95 and K96 lack audits, and K97's addition and K12's changed revision still lack current verification.”
- H04-Q2: “One shared object containing M0; it contains neither subsequent source change.”
- H05-Q1: “B/C, output 16; staff 8, memory 9, power 8.”
- H05-Q3: “A/C, output 14; staff 7, memory 10, power 7.”
- H06-Q2: “Room: 2; kits: 2; leaders: 2; overall: 2.”
- H06-Q3: “Yes. There would be 24 participants, exactly meeting the room cap, kit inventory, and two-leader capacity.”

These examples do not override the separate exposure-support, source-faithfulness, or protocol dimensions. A correct but unsupported guess need not earn strict primary credit. Conversely, when a source-true cached conclusion is actually supplied, SCORING.md correctly permits its use without demanding reconstructed primitives.

Optional assertions remain checkable when volunteered. For example, claiming all hypothetical timing offsets make U pass, describing unaudited keys as observed corruptions, or claiming C2 inherited C1 outcomes is false, even alongside a correct requested decision. If a phrase genuinely permits a supported reading and an unsupported reading, retain both and report sensitivity rather than silently assuming the harsher reading. This is consistent with SCORING.md.

## Limits and preservation

This comparison used only the previously authorized source inputs and, after sealing, the proposed key and SCORING.md. I did not inspect authoring methods, broader protocol files, grading examples, trial outputs, git history, or the internet. Accordingly, I cannot certify collection execution, masking, adherence to an unseen protocol, or method effects. Scoring text about those matters was read but is not execution evidence.

The sealed derivation and this comparison come from the same separate internal reviewer in sequential phases. They do not establish independent human review or formal certification. There are no material source ambiguities requiring sensitivity across different scenario answers; the identified sensitivity concerns only whether optional explanatory details are mistakenly treated as mandatory.

`review/ORACLE_SOURCE_FIRST.md` must remain unchanged. No history, query, key, or scoring file was modified by this review.
