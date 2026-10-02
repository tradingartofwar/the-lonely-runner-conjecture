#!/usr/bin/env python3
"""Deterministic preparation and prompt assembly. No model or network calls.

This is not an execution recorder. Frozen schemas are checked on raw JSON;
invalid participant text is never repaired or trimmed into a valid response.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent


def read(name):
    return (HERE / name).read_text()


def load(name):
    return json.loads(read(name))


def write(name, obj):
    path = HERE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def history(hid):
    return read(f"histories/{hid}.md")


def author_prompt(hid, method):
    return (read("author_common.txt").strip() + "\n\nAUTHORING PROCEDURE\n" +
            read(f"method_{method}.txt").strip() + "\n\nCOMPLETE HISTORY\n" +
            history(hid))


def _unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def decode(raw):
    return json.loads(raw, object_pairs_hook=_unique_object)


def validate_author(raw):
    obj = decode(raw)
    if not isinstance(obj, dict) or list(obj) != ["status", "evidence", "next"]:
        raise ValueError("author schema or key order")
    if any(not isinstance(v, str) for v in obj.values()):
        raise ValueError("author values must be strings")
    if any(not v.strip() for v in obj.values()):
        raise ValueError("author fields must be nonempty")
    words = sum(len(v.split()) for v in obj.values())
    if words > load("CONFIG.json")["author_word_cap"]:
        raise ValueError("author word cap")
    return {"object": obj, "words": words, "raw_sha256": digest(raw)}


def render_handoff(raw):
    obj = validate_author(raw)["object"]
    return "\n\n".join(f"{key.upper()}\n{obj[key]}" for key in ["status", "evidence", "next"])


def validate_recipient(raw, mode="handoff"):
    if mode not in {"handoff", "full_source", "recovery"}:
        raise ValueError("unknown recipient mode")
    obj = decode(raw)
    if not isinstance(obj, dict) or set(obj) != {"answer", "recover"}:
        raise ValueError("recipient schema")
    if not isinstance(obj["answer"], str) or not obj["answer"].strip() or type(obj["recover"]) is not bool:
        raise ValueError("recipient field types or missing answer")
    words = len(obj["answer"].split())
    if words > load("CONFIG.json")["recipient_answer_word_cap"]:
        raise ValueError("recipient answer word cap")
    if mode != "handoff" and obj["recover"]:
        raise ValueError("no further recovery allowed")
    return {"object": obj, "words": words, "raw_sha256": digest(raw)}


def recipient_prompt(query, mode, evidence):
    if mode == "handoff":
        instruction = ("Evidence mode: handoff only. Give a supported first answer now. "
                       "Set recover to true only if seeing the complete history would help "
                       "resolve missing evidence; otherwise false. At most one source "
                       "followup will be served after this answer is saved.")
    elif mode == "full_source":
        instruction = ("Evidence mode: complete source history. Answer from this source "
                       "and the query. Set recover to false; no additional source is available.")
    else:
        raise ValueError("use recovery_prompt for a followup")
    return (read("recipient_common.txt").strip() + "\n\n" + instruction +
            "\n\nQUESTION\n" + query + "\n\nEVIDENCE\n" + evidence)


def recovery_prompt(hid):
    return ("COMPLETE SOURCE RECOVERY\nYour first answer is already recorded. Answer the "
            "same question again using this complete history and its explicit hypothetical, "
            "preserving uncertainty where the source itself leaves it. Return the same JSON "
            "schema and word limit, with recover false. Do not use tools or other sources.\n\n" +
            history(hid))


def build():
    config = load("CONFIG.json")
    questions = load("evaluator/QUESTIONS_AND_KEY.json")["questions"]
    hids = sorted({q["history"] for q in questions})
    rng = random.Random(config["seed"])
    order = list(hids)
    rng.shuffle(order)
    authors, author_map = [], {}
    # Three histories CC-first, three conventional-first, with shuffled history order.
    for i, hid in enumerate(order):
        methods = ["cc", "conventional"] if i % 2 == 0 else ["conventional", "cc"]
        for method in methods:
            aid = f"A{len(authors)+1:03}"
            prompt = author_prompt(hid, method)
            authors.append({"id": aid, "history": hid, "method": method,
                            "prompt": prompt, "prompt_sha256": digest(prompt), "status": "UNRUN"})
            author_map[(hid, method)] = aid
    readers = []
    for q in questions:
        for method in ["cc", "conventional", "full_source"]:
            readers.append({"question": q["id"], "history": q["history"], "method": method,
                            "author": author_map.get((q["history"], method)), "status": "UNRUN"})
    rng.shuffle(readers)
    for i, rec in enumerate(readers, 1):
        rec["id"] = f"Q{i:03}"
    # Runtime prompt assembly can use this file without reading the proposed answer key.
    public_questions = {q["id"]: {"history": q["history"], "query": q["query"]}
                        for q in questions}
    write("prepared/AUTHOR_INPUTS.json", authors)
    write("prepared/RECIPIENT_SCHEDULE.json", readers)
    write("prepared/QUESTION_PROMPTS.json", public_questions)
    print(json.dumps({"authors_prepared": len(authors), "recipient_cells_prepared": len(readers),
                      "model_calls": 0, "status": config["status"]}))


def files():
    return sorted(p for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                  and p.name != "PREPARATION_MANIFEST.json")


def pin():
    write("PREPARATION_MANIFEST.json", {
        "scope": "Reviewable preparation only; not execution authorization or execution freeze",
        "source_checkpoint": load("CONFIG.json")["source_checkpoint"],
        "sha256": {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files()}})
    print(json.dumps({"preparation_files_pinned": len(files()), "execution_frozen": False}))


def verify():
    manifest = load("PREPARATION_MANIFEST.json")["sha256"]
    actual = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files()}
    if manifest != actual:
        raise ValueError("preparation file set or hashes changed")
    print(json.dumps({"preparation_integrity": "PASS", "files": len(actual)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "pin", "verify"])
    args = parser.parse_args()
    globals()[args.command]()
