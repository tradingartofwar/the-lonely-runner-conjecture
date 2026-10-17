"""Exact finite leader-containing cover; no full nonexception contact matrix."""
from fractions import Fraction as F
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load("exception_parent_primary", HERE.parent / "study.py")
gap = load("exception_optional_gap", HERE.parent / "gap-selection/run.py")
require = base.require


class ContactBudget(Exception):
    pass


def residual_dp(masks, target, leader, cfg):
    """Parent mask recurrence with strict pre-operation budgets."""
    states, transitions, peak = {0: ()}, 0, 1
    if cfg["max_dp_states"] < 1:
        return {"status":"UNKNOWN_BUDGET","ids":None,"states":0,"transitions":0,"reason":"states"}
    for i, component_mask in sorted(masks.items()):
        if not component_mask:
            continue
        updated = dict(states)
        for mask, subset in states.items():
            if transitions >= cfg["max_dp_transitions"]:
                return {"status":"UNKNOWN_BUDGET","ids":None,"states":peak,"transitions":transitions,"reason":"transitions"}
            transitions += 1
            union, candidate = mask | component_mask, subset+(i,)
            old = updated.get(union)
            if old is None or (len(candidate), candidate) < (len(old), old):
                if old is None and len(updated) >= cfg["max_dp_states"]:
                    return {"status":"UNKNOWN_BUDGET","ids":None,"states":peak,"transitions":transitions,"reason":"states"}
                updated[union] = candidate
                peak = max(peak, len(updated))
        states = updated
    require(target in states, "covered residual target absent from DP")
    return {"status":"EXACT","ids":sorted((leader,)+states[target]),"states":peak,"transitions":transitions}


def construct(core, leader, domain, d, cfg):
    core = [tuple(map(F, row)) for row in core]
    d = F(d)
    require(bool(core) and 0 <= leader < len(core), "invalid source/leader")
    require(all(F(0) <= a <= b <= F(1) for a,b in core), "invalid source interval")
    require(all(core[i][1] < core[i+1][0] for i in range(len(core)-1)), "sources must be sorted/disjoint")
    require(domain == sorted(set(domain)) and all(type(r) is int and r > 0 for r in domain), "invalid domain")
    require(0 < d < F(1,2), "invalid threshold")
    cache, queries, failures = {}, [], []
    costs = {"leader":0,"lazy":0,"residual":0,"cache_reuses":0}
    stage, complete = "LEADER", False

    def query(i, r, label):
        key = (i,r)
        if key in cache:
            costs["cache_reuses"] += 1
            return cache[key]
        if len(cache) >= cfg["max_contact_queries"]:
            raise ContactBudget()
        value = base.first_contact(core[i],r,d)
        cache[key] = value
        queries.append({"component":i,"r":r,"stage":label,**value})
        costs[label] += 1
        return value

    def finish(status, ids, route, missing=None, masks=None, dp=None):
        optional = {"status":"NOT_ATTEMPTED","component":None,"search":None}
        certificate = None
        if status == "EXACT":
            table = []
            for r in failures:
                i = next(i for i in ids if (i,r) in cache and cache[i,r]["hit"])
                table.append({"r":r,"component":i,"time":cache[i,r]["candidate"]})
            if len(ids) == 2:
                j = next(i for i in ids if i != leader)
                search = gap.gap_search([core[j]],failures,d,cfg["max_gap_probes"])
                optional = {"status":search["status"],"component":j,"search":search}
            common = ({"time":optional["search"]["time"],"component":optional["component"]}
                      if optional["status"] == "FOUND" else None)
            certificate = {"threshold":d,"domain":domain,"leader":{"component":leader,"interval":core[leader]},
                           "menu":[{"component":i,"interval":core[i]} for i in ids],
                           "exception_table":table,"common_repair":common,"family_context":None}
        return {"status":status,"ids":ids,"route":route,"failures":failures,
                "classification_complete":complete,"queries":queries,"query_costs":{**costs,"unique":len(cache)},
                "uncovered_speeds":missing or [],"residual_masks":masks,"dp":dp,
                "optional_common":optional,"certificate":certificate}

    try:
        for r in domain:
            if not query(leader,r,"leader")["hit"]:
                failures.append(r)
        complete = True
        if not failures:
            return finish("EXACT",[leader],"LEADER_ONLY")
        stage = "LAZY"
        for i in range(len(core)):
            if i == leader:
                continue
            if all(query(i,r,"lazy")["hit"] for r in failures):
                return finish("EXACT",sorted([leader,i]),"LAZY_TWO")
        stage = "RESIDUAL_FILL"
        masks = {}
        for i in range(len(core)):
            if i != leader:
                masks[i] = sum(1 << j for j,r in enumerate(failures) if query(i,r,"residual")["hit"])
        target = (1 << len(failures))-1
        combined = 0
        for mask in masks.values():
            combined |= mask
        missing = [r for j,r in enumerate(failures) if not combined & (1 << j)]
        saved_masks = [{"component":i,"mask":mask} for i,mask in sorted(masks.items())]
        if missing:
            return finish("NO_SUFFICIENT_MENU",None,"RESIDUAL_NO_COVER",missing=missing,masks=saved_masks)
        stage = "RESIDUAL_DP"
        dp = residual_dp(masks,target,leader,cfg)
        return finish(dp["status"],dp["ids"],stage,masks=saved_masks,dp=dp)
    except ContactBudget:
        return finish("UNKNOWN_BUDGET",None,stage)


def dispatch(certificate, r):
    """Return t, component ID, fresh first-contact call count; guard scope."""
    require(certificate is not None, "no certified menu")
    require(type(r) is int and r > 0, "speed must be a positive integer")
    family = certificate["family_context"]
    if family:
        require(r not in family["core_speeds"], "added speed repeats core")
    require(r in certificate["domain"] or (family is not None and r >= family["tail_from"]), "query outside certified scope")
    saved = next((x for x in certificate["exception_table"] if x["r"] == r), None)
    if saved:
        point = certificate["common_repair"] or saved
        return F(point["time"]), point["component"], 0
    leader = certificate["leader"]
    contact = base.first_contact(tuple(map(F,leader["interval"])),r,F(certificate["threshold"]))
    require(contact["hit"], "certificate leader failed a covered query")
    return contact["candidate"], leader["component"], 1
