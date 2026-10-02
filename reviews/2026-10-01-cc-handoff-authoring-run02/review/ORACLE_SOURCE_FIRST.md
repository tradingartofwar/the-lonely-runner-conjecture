This review was derived only from the supplied review prompt, six histories, and eighteen question prompts, before receiving any proposed key. All eighteen questions are answerable under the stated fictional rules. I found no material ambiguity or missing premise that changes an answer.

**H01-Q1.** The bench-ready set is **{C}**. Current rule v2 requires firmware 8, packet success ≥99%, latency ≤7 seconds, buffering enabled, and runtime ≥8 hours on the same station. C satisfies all five: 198/200 = 99%, seven seconds, buffering enabled, firmware 8, and eight hours; equality is accepted. A has no qualifying post-upgrade packet or latency measurements and buffering remains disabled, although its unchanged nine-hour pack qualifies. B satisfies the other requirements—119/120 ≈99.17%, six seconds, firmware 8, buffering enabled—but its 7.5-hour runtime is insufficient. Sources: R01, R04, R06–R08, R10, R12.

**H01-Q2.** A’s packet performance after the upgrade is **unknown**, not an observed failure of the current packet-success criterion. Its earlier 99/100 result was obtained on firmware 7; upgrading to firmware 8 invalidated that result as current readiness evidence. No new packet measurement followed. Sources: R01, R03, R06, R12.

**H01-Q3.** The new bench-ready set is **{B, C}**. The hypothetical valid 8.5-hour pack result resolves B’s only unmet v2 condition; its unchanged packet success, latency, firmware, and buffering already qualify. C remains ready and A remains unready. Sources: R04, R06–R08, R10, R12, plus the question’s explicit pack change.

Grading scope: These questions concern technical readiness. Transport bookings, photographs, dashboard appearance, and administrative choices should not be required. Q2 does not require a latency or buffering discussion. Q3 does not require an actual booking or an additional unmentioned approval.

**H02-Q1.** **One of three unique samples is late: U.** Subtract three seconds from each gateway timestamp, then subtract acquisition time:

| Sample | Reference-clock arrival | Delay |
|---|---:|---:|
| S | 104 − 3 = 101 | 101 − 100 = 1 second |
| T | 104.5 − 3 = 101.5 | 101.5 − 100.5 = 1 second |
| U | 108 − 3 = 105 | 105 − 102 = 3 seconds |

The requirement is delay ≤2 seconds. U-retry is the same acquired sample as U and adds no sample to the denominator. Sources: C01, C03–C05, C07–C08, C12.

**H02-Q2.** S and T were **not simultaneous at acquisition or gateway arrival**. Their acquisitions were 100 and 100.5; their reference-clock gateway arrivals were **101 and 101.5**, respectively. T follows S by 0.5 seconds at both stages. Their shared database insertion time does not establish simultaneous acquisition or gateway arrival. Sources: C03–C04, C07.

**H02-Q3.** With one common unknown offset \(o \in [2,4]\):

- S and T each have delay \(4-o \in [0,2]\), so both are **guaranteed to pass**.
- U has delay \(6-o \in [2,4]\), so it is **unresolved**: it passes at \(o=4\), and fails at every allowed \(o<4\).
- **No sample is guaranteed to fail.**
- **All three can pass simultaneously**, precisely when the common offset is four seconds. Their delays are then 0, 0, and 2 seconds.

Sources: C01, C03–C05, C08, C10, C12; the hypothetical replaces the exact calibration only.

Grading scope: Q1 asks for the late count, denominator, and identities; a full timing table or percentage should not be separately required. Q2 does not ask for insertion times. Q3 requires the classifications and joint possibility; exact delay formulas support them but equivalent correct reasoning should suffice. No reliability estimate for unseen samples is requested.

**H03-Q1.** C1 **does not pass**. It has **nine passes, two failures, and one untested case**. The failures are **A8 and B3**; **B4** is untested. Group A contributes seven passes and one failure; group B contributes two passes, one failure, and one untested case. The rule requires at least eleven passes and all twelve cohort cases evaluated, so both requirements are unmet. Sources: J02, J04–J05, J12.

**H03-Q2.** The pass fraction among evaluated cohort cases is **9/11**, approximately **81.82%**. The fraction among all authorized cohort cases is **9/12 = 75%**. The first denominator excludes untested B4; the second includes it. Neither denominator is fourteen because X1 and X2 were removed by the prespecified exclusion rule before outcome inspection, leaving a twelve-case authorized cohort. Sources: J01, J04–J05, J09, J12.

**H03-Q3.** If C2 is selected without additional evaluation, it has **one pass, zero observed failures, and eleven untested cases**. Its sole evaluated case is B3, which passed. It **does not pass** the acceptance rule: eleven cases remain untested and it has only one established pass. Selection does not transfer C1’s outcomes to C2. Sources: J02, J08, J10–J12.

For completeness, C2’s eleven untested cases are A1–A8, B1, B2, and B4; identifying each is not requested by Q3.

Grading scope: Q1 requires naming failed and untested cases, but not all nine passing cases. Q2 asks for fractions; correct exact fractions need not also be converted to percentages. Q3 does not require the eleven untested names, a testing plan, or a statistical confidence calculation. Untested cases must not be classified as observed failures.

**H04-Q1.** The live source **may not be retired**. **93 of 97 current source keys** have verified matching current revisions. The audit verified 94 M0 revisions, but K12’s verification covers revision 1 while its current source revision is 2. Thus \(94-1=93\) verifications apply to current revisions.

Four keys prevent establishing complete current coverage:

- **K95 revision 1:** ingested as part of M0 but unaudited.
- **K96 revision 1:** ingested as part of M0 but unaudited.
- **K97 revision 1:** added after M0; no destination ingestion or verification recorded.
- **K12 revision 2:** changed after M0; no ingestion or verification of the current revision recorded.

These are verification gaps, not observed checksum mismatches. Sources within H04: H01, H04–H06, H08–H09, H12.

**H04-Q2.** The labels establish **one distinct stored backup object**, object-amber, containing immutable snapshot M0. They are aliases for that same object. Its stored content includes **neither the K97 addition nor the K12 revision-2 change**: M0 contains K1–K96 at revision 1. Sources within H04: H02–H03, H08–H09, H12.

**H04-Q3.** The source **still may not be retired**. Completing the two specified comparisons raises the current-revision verification count to **95 of 97**: \(93+2=95\). K95 and K96 now have verified revision-1 matches. The remaining blockers are **K97 revision 1 and K12 revision 2**, neither of which has destination ingestion or current-revision verification in the unchanged record. Equivalently, all 96 M0 revisions would be verified, but one of those revisions—K12 revision 1—is outdated, giving \(96-1=95\) current matches. Sources within H04: H01–H02, H06, H08–H09, H11–H12, plus the hypothetical comparisons.

Grading scope: Q1 and Q3 concern verified **current revisions**, not merely verified M0 entries or ingestion acknowledgments. Q2 asks about the objects established by the two backup labels, not a count including the live source and destination. No external retention, redundancy, legal, or hardware requirements should be introduced.

**H05-Q1.** **B/C** is the feasible pair maximizing output. It produces **16 output units** and uses **8 staff, 9 memory, and 8 power**, exactly fitting the final caps.

The complete pair calculation is:

| Pair | Output | Staff | Memory | Power | Feasible under (8, 9, 8)? |
|---|---:|---:|---:|---:|---|
| A/B | 18 | 9 | 11 | 9 | No |
| A/C | 14 | 7 | 10 | 7 | No: memory |
| B/C | 16 | 8 | 9 | 8 | Yes |

Sources: D01–D04, D07, D12.

**H05-Q2.** **No.** Adopting only the staff rental gives caps **(10, 9, 8)**. A/B requires **(9, 11, 9)**. Its staff requirement now fits, but **memory exceeds its cap by two units** and **power exceeds its cap by one unit**. Sources: D02–D03, D08, D12.

**H05-Q3.** Choose **A/C**. With only one additional memory unit, the caps are **(8, 10, 8)**. A/C uses **(7, 10, 7)** and produces **14 output units**, so it fits, including equality at the memory cap. It contains A and consists of two distinct jobs. The only other pair containing A, A/B, requires (9, 11, 9), exceeding all three changed caps. Sources: D01–D04, D10, D12, plus the question’s A-inclusion requirement.

Grading scope: Q1 requires the chosen pair, output, and three resource totals; displaying the entire enumeration should not be an additional requirement. Q2 requires the remaining violations; explaining unrelated pairs is unnecessary. Q3 does not require recounting the chronology, adopting the staff rental, or discussing sequential execution.

**H06-Q1.** **Yes, the current workshop is feasible under every supplied rule.** Twenty-two participants fit the room’s 24-participant cap and the 24 functioning reserved kits. Two confirmed leaders support up to \(2 \times 12=24\) participants. Leaders do not count toward the participant room cap or use participant kits. The confirmed **10:00–11:30** booking lasts ninety minutes, fits entirely inside **09:00–17:00**, and is covered by both leaders’ confirmations. Listening uses headphones throughout, which are explicitly exempt from the restriction on amplified room sound before 11:00. Required reservations and confirmations are complete. Sources: O01–O04, O06–O08, O11–O12.

**H06-Q2.** The plan can accommodate **two additional participants under each limit**:

- Room: \(24-22=2\).
- Kits: \(24-22=2\).
- Leaders: \(2 \times 12-22=2\).

The overall remaining participant capacity is **two**, the minimum of the three separate allowances. Sources: O02–O04, O08, O11–O12.

**H06-Q3.** **Yes.** Two additional registrations raise attendance to **24**. That exactly meets the **24-participant room cap**, uses all **24 kits**, and reaches the **24-participant capacity of two leaders**. The unchanged timing, confirmations, and headphone arrangement continue to qualify. Sources: O02–O04, O06–O07, O10–O12, plus the hypothetical attendance increase.

Grading scope: Q1 expressly requests timing, headphones, and capacity. Q2 requires spare capacities, not a reconstruction of discarded plans. Q3 requires the new attendance and its relationship to the three capacity limits; a detailed repetition of booking history or headphone reasoning should not be necessary. No hidden setup time, extra leader requirement, waiting-list rule, or additional approval is supplied.

This is a source-first internal answerability review, not independent human or formal certification.
