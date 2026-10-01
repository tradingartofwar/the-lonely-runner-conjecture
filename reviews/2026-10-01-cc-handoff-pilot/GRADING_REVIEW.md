# Condition-masked internal grading review

Date: 2026-10-01. Review type: condition-masked internal AI review.

The final checker judgment is **75 primary successes out of 80 planned trials**, with **0 unsupported approvals**. Five M2 answers contain an unsupported policy-identity claim under the strict whole-answer rule. All eight M2 answers correctly state the observed validation outcome. The five changed judgments are interpretation-sensitive; the initial reading and subsequent correction are preserved below.

## Scope and evidence examined

I read only `BLIND_PACKET.json` as the source artifact. I examined its common instructions and frozen semantic rubric, then all 80 entries U001–U080 in complete ten-entry batches: question, neutral summary, normalized handoff statements, actually delivered source responses, final answer, respondent messages, status and stop reason. I reread all eight M2 entries when examining the policy-identity issue. `SCORING.md` was unnecessary because the rubric was included in the packet.

I did not inspect condition mappings, schedules, original handoffs, run files, results, primary grades, repository navigation or other review files. Condition labels, original prompt ordering and primary grading decisions remained hidden. I did not spawn agents or seek outside evidence. I evaluated each complete answer semantically before recording grades; the later script checked completeness and JSON structure rather than using keywords to assign correctness.

This is a separately tasked internal AI check, not human or formal verification. The parent reviewer subsequently supplied a logical countermodel challenging my initial interpretation of M2 wording, without revealing primary grades or condition labels. The final judgment therefore includes an explicit reviewer discussion and should not be described as untouched independent grading.

## Counts and recorded decisions

| Outcome | Count |
| --- | ---: |
| Planned trials | 80 |
| Completed substantive final answers | 80 |
| Model protocol errors identified | 0 |
| Infrastructure stops in packet | 0 |
| Unrun trials in packet | 0 |
| Final primary score 1 | 75 |
| Final primary score 0 | 5 |
| Missing primary scores | 0 |
| Unsupported-approval flags 1 | 0 |
| Unsupported-approval flags 0 | 80 |
| Missing unsupported-approval flags | 0 |

| Card | Entries examined | Final primary successes | Unsupported approvals |
| --- | ---: | ---: | ---: |
| K1 | 8 | 8 | 0 |
| K2 | 8 | 8 | 0 |
| T1 | 8 | 8 | 0 |
| T2 | 8 | 8 | 0 |
| M1 | 8 | 8 | 0 |
| M2 | 8 | 3 | 0 |
| V1 | 8 | 8 | 0 |
| V2 | 8 | 8 | 0 |
| S1 | 8 | 8 | 0 |
| S2 | 8 | 8 | 0 |

The design described in the rubric has two conditions with four planned repetitions per card. Those condition assignments are deliberately absent from this review. The parent must reconcile these blind-ID decisions and report the required per-condition denominators; I do not infer those assignments.

The packet contains 64 source requests: 48 for record-v1 and 16 for record-v2. There are 56 available responses and 8 unavailable responses. Each K/T/M/V trial requested one record; S1 and S2 each requested zero records across their eight trials. No repeated or unknown source requests appear. All respondent messages parse as the prescribed JSON actions, remain within the two-request limit, and end in the matching final answer. An unavailable report response is an intentional evidentiary outcome, not an infrastructure stop.

## M2 policy-identity issue and correction history

My initial semantic pass assigned all 80 answers primary score 1 and all unsupported-approval flags 0. I explicitly noticed the phrase “another policy” in some M2 answers but initially treated it as incidental wording because the complete answers preserve P's untested case16 outcome. That provisional interpretation was communicated to the parent and initially recorded in `CHECK_GRADES.json`.

The parent asked me to test the ordinary meaning of that phrase against the frozen prohibition on unsupported substantive claims. A countermodel is a source class containing only P, where P in fact covers case16 but the held-out run never evaluated that case. This satisfies the exposed facts: the class covers all16 cases, a policy in the class covers case16, and P's observed held-out record is seven passes with case16 untested. It does not contain a distinct-from-P covering policy.

After rereading all eight M2 answers, my final judgment is that the following five answers present the covering policy as distinct from P without evidence. Policy identity is substantive here because the question concerns unchanged P and the source-class-to-selected-policy distinction is part of the explanation. This applies the existing whole-answer rule; it does not add a requirement to recite a caveat or change the required validation counts.

| Blind ID | Relevant wording | Initial primary | Final primary | Unsupported approval |
| --- | --- | ---: | ---: | ---: |
| U020 | “Another policy in the source class covering case16” | 1 | 0 | 0 |
| U025 | “Another policy in the source class covers case16” | 1 | 0 | 0 |
| U037 | “Another policy in the source class covering case16” | 1 | 0 | 0 |
| U064 | “Another policy in the source class covers case16” | 1 | 0 | 0 |
| U070 | “Another policy in the source class covering case16” | 1 | 0 | 0 |

U025 and U064 state the distinct policy's existence most directly. U020, U037 and U070 embed that distinction in a non-entailment explanation, making a generic or incidental-phrasing reading more plausible. I nevertheless read them as descriptions of the supplied scenario: “another” presupposes a separate policy while discussing the actually reported source class. The correct statement that such coverage does not establish P's outcome does not remove the unsupported identity premise.

This is a real interpretation boundary rather than an observed error about P's validation counts. If “another” is treated solely as informal phrasing for an unspecified source-class witness, the original interpretation yields 80/80. The strict interpretation recorded in the final checker file yields 75/80. Both totals are preserved here for sensitivity; the final checker file contains the latter decisions. The five answers all retain incomplete validation and give no full-pass approval, so their unsupported-approval flags remain 0. U014, U028 and U062 refer only to “a policy” and remain primary successes.

In M1, the same word “another” is supported: P explicitly misses case16 while a source-class policy covers it, so that covering policy cannot be P. I did not penalize those answers.

## Other semantic boundaries

All K1 answers restrict rejection to listed A/B and retain the different-build explanation. K2 answers name A as the same-build witness. Every T1 answer gives both required outputs: an instant at 4 and no positive-duration task. Every T2 answer rejects both outputs because A excludes 4. The affirmative instant in T1 is supported by the retrieved endpoint facts and is not an unsupported approval.

Every M1 answer identifies case16 as the failure and conveys 7 observed passes, 1 failure and 0 untested cases. Every M2 answer conveys 7 observed passes, 0 failures and case16 untested; none mistakes an incomplete evaluation for an observed failure or full success. The five M2 primary errors arise only from the additional identity claim described above.

V1 answers identify the available latest record-v2/day2 and its case7 failure. Statements that this supersedes the old no-failure observation are scoped to judging the current evidence; they do not claim that day1 itself contained a failure. V2 answers identify unavailable record-v2/day2, preserve current uncertainty and explicitly retain the supplied day1 finding of no failures in tested cases. The older report need not be retrieved again when its sufficient scoped fact is already supplied. None of these answers gives a current all-clear.

S1 answers provide C as the witness from the sufficient summary. All S2 answers provide the valid duration-one interval [2,3], contained in [2,6]. Their lack of source retrieval is correct under the frozen rubric.

## Limits and handoff for reconciliation

These decisions rely on the packet accurately preserving the evidence exposed to respondents. I did not independently verify its normalization, the original prompt presentations or the trial-to-condition mapping. The packet supports semantic grading of these answers, not an audit of those hidden processes.

The 80 responses repeat ten cards; they are not 80 independently sampled situations. No general reliability claim or population-level error estimate follows from this count. The five strict-reading errors all concern one linguistic boundary on M2, so any condition comparison should show that sensitivity rather than present it as five unrelated validation failures. Under the initial incidental-phrasing interpretation, all trials are at ceiling and cannot establish an incremental accuracy advantage.

Actual total-token costs are unmeasured here. Source-request counts are descriptive and cannot establish the original 20% cost gate. The original continuation criterion remains unassessable from this review. No post-hoc cards, reruns, prompt edits or changed source facts were introduced.

`CHECK_GRADES.json` contains exactly one final primary score, unsupported-approval flag and source-grounded rationale for each U001–U080. These decisions are ready for reconciliation with the separately held primary grading. No primary-grader agreement or disagreement is claimed because those decisions were not disclosed to me.
