#!/usr/bin/env python3
"""Build equal-content arms after oracle review. Does not invoke respondents."""
from pathlib import Path
import json
import hashlib

HERE = Path(__file__).resolve().parent


def main():
    review=(HERE/"ORACLE_REVIEW.md").read_text()
    assert "review complete; all ten" in review
    cards=json.loads((HERE/"SOURCE_CARDS.json").read_text())["cards"]
    atoms={
      "K": ["Which checks have passed somewhere.",
            "The summary omits which results belong to the same build.",
            "Before deciding joint eligibility, retrieve the build-level record."],
      "T": ["Individual availability durations.",
            "Locations, joint availability and endpoint membership are omitted.",
            "Retrieve the interval record before deciding either joint feasibility question."],
      "M": ["Training coverage and coverage by the entire source class.",
            "The unchanged policy's held-out outcomes and evaluation completion are omitted.",
            "Retrieve the evaluation record before declaring a held-out pass, failure or incomplete result."],
      "V": ["Observed failure status in the day1 report.",
            "A day2 report exists; its contents and current availability are not carried here.",
            "Retrieve the latest report before judging the current state; retain uncertainty if it is unavailable."],
      "S1": ["Existence of a build with both required checks.",
             "The summary identifies one joint witness; other builds' results are omitted.",
             "Answer the existence question from the summary; retrieve only if another build's details are required."],
      "S2": ["Shared availability throughout a specified closed interval.",
             "The complete stated interval and its endpoints are retained; no further source detail is needed for this query.",
             "Check that the proposed task fits inside the stated interval."],
    }
    handoffs={}
    for c in cards:
        cid=c["id"]
        supported,limits,recovery=atoms[cid if cid.startswith("S") else cid[0]]
        summary=c["neutral_summary"]
        sources="; ".join(s["alias"]+", "+s["date"] for s in c["sources"])+"."
        conventional=(f"Facts and scope: {summary} {supported}\n"
                      f"Assumptions and limits: {limits}\n"
                      f"Dated source links: {sources}\n"
                      f"Recommended next action: {recovery}")
        cc=(f"Supported query: {supported}\n"
            f"Retained facts: {summary}\n"
            f"Scope and omissions: {limits}\n"
            f"Relevant dated source: {sources}\n"
            f"Recovery trigger: {recovery}")
        words={"conventional":len(conventional.split()),"cc_informed":len(cc.split())}
        assert len(set(words.values()))==1 and max(words.values())<=120
        handoffs[cid]={"conventional":conventional,"cc_informed":cc,"word_counts":words,
                       "shared_atoms":{"summary":summary,"supported":supported,"limits":limits,"sources":sources,"recovery":recovery}}
        assert all(atom in conventional and atom in cc for atom in [summary,supported,limits,sources,recovery])
    for pair in [("K1","K2"),("T1","T2"),("M1","M2"),("V1","V2")]:
        for arm in ["conventional","cc_informed"]:assert handoffs[pair[0]][arm]==handoffs[pair[1]][arm]
    (HERE/"HANDOFFS.json").write_text(json.dumps({"treatment":"Shared factual atoms; field labels, grouping and order differ.","cards":handoffs},indent=2,ensure_ascii=False)+"\n")
    instructions=(HERE/"RESPONDENT_INSTRUCTIONS.md").read_text().strip()
    by={c["id"]:c for c in cards}
    schedule=json.loads((HERE/"TRIAL_SCHEDULE.json").read_text())["trials"]
    stimuli={}
    for trial in schedule:
        c=by[trial["card_id"]]
        catalog="\n".join(s["alias"]+" — "+s["date"] for s in c["sources"])
        prompt=(instructions+"\n\nSUMMARY\n"+c["neutral_summary"]+"\n\nHANDOFF\n"+handoffs[c["id"]][trial["arm"]]+
                "\n\nSOURCE CATALOG\n"+catalog+"\n\nQUESTION\n"+c["query"])
        stimuli[trial["trial_id"]]={"prompt":prompt,"sha256":hashlib.sha256(prompt.encode()).hexdigest()}
    (HERE/"STIMULI.json").write_text(json.dumps(stimuli,indent=2,ensure_ascii=False)+"\n")
    key=json.loads((HERE/"ANSWER_KEY_DRAFT.json").read_text())
    key["status"]="INTERNAL_SOURCE_FIRST_ORACLE_REVIEW_COMPLETE"
    key["review"]="ORACLE_REVIEW.md"
    key["grading"]="SCORING.md; semantic scope and exposed evidence govern, not literal decision labels."
    (HERE/"ANSWER_KEY.json").write_text(json.dumps(key,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"word_counts":{k:v["word_counts"] for k,v in handoffs.items()},"stimuli":len(stimuli),"model_trials":0}))


if __name__=="__main__":main()
