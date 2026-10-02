#!/usr/bin/env python3
"""Post-collection descriptive sensitivity; never rewrites frozen or graded data."""
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def main():
    grades = read("grading/FINAL_GRADES.json")["grades"]
    mapping = read("grading/PRIVATE_MASK_MAP.json")["answers"]
    changed = copy.deepcopy(grades)
    affected = [g for g in changed if g["id"] == "R040"]
    assert {g["stage"] for g in affected} == {"first", "final"}
    for grade in affected:
        assert grade["primary"] == grade["requested_outputs_correct"] == 1
        grade.update(supported_by_exposure=0, source_faithful=0,
                     primary=0, unsupported_assertion=1)

    def counts(rows):
        return {method: {stage: {
            "observed": sum(g["stage"] == stage and mapping[g["id"]]["method"] == method for g in rows),
            **{field: sum(g[field] == 1 for g in rows
                          if g["stage"] == stage and mapping[g["id"]]["method"] == method)
               for field in ("primary", "requested_outputs_correct", "unsupported_assertion", "unsupported_approval")}
        } for stage in ("first", "final")}
            for method in ("cc", "conventional", "full_source")}

    retention = read("grading/RETENTION_AUDIT.json")
    authors = read("run/AUTHORS_TRANSCRIPTS.json")
    summary_map = read("grading/PRIVATE_MASK_MAP.json")["summaries"]
    author_map = {a["id"]: a for a in authors}
    output = {
        "status": "POST_COLLECTION_DESCRIPTIVE_SENSITIVITY",
        "basis": "grading/ADJUDICATION.md; contextual decision and alternative fixed before method unmasking",
        "preferred": counts(grades),
        "broad_R040_planned_work_reading": counts(changed),
        "affected_answer": {"masked_id": "R040", **mapping["R040"]},
        "requested_outputs_change": 0,
        "retention_by_method": {method: {
            "queries": sum(author_map[summary_map[r["summary_id"]]]["method"] == method for r in retention["records"]),
            "adequate": sum(r["supports_every_requested_output"] and r["source_true_support"]
                            for r in retention["records"]
                            if author_map[summary_map[r["summary_id"]]]["method"] == method)
        } for method in ("cc", "conventional")},
        "S12_optional_booking_clause": {
            "author": summary_map["S12"], "method": author_map[summary_map["S12"]]["method"],
            "supported_reading": "No completed station-selection booking",
            "unsupported_reading": "No completed room booking",
            "recipient_repetitions": 0, "recipient_grade_changes": 0
        },
        "author_decoded_words": {method: {
            "values": [a["handoff_words"] for a in authors if a["method"] == method],
            "mean": sum(a["handoff_words"] for a in authors if a["method"] == method) / 6
        } for method in ("cc", "conventional")},
        "limits": "Alternative semantic reading, not extra observations. Six paired histories; no inferential test or causal attribution to information selection."
    }
    (HERE / "SENSITIVITY.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "preferred": output["preferred"],
                      "broad_reading": output["broad_R040_planned_work_reading"]}, indent=2))


if __name__ == "__main__":
    main()
