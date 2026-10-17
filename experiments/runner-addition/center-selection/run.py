"""Frozen primary decisions and separately labelled heuristic diagnostics."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import ceil, gcd
from pathlib import Path
import subprocess
from selector import select, required, norm, witness

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def dump(x):
    return json.dumps(x, sort_keys=True, indent=2,
                      default=lambda z: str(z) if isinstance(z, F) else z)+'\n'


def check_freeze(freeze):
    rel = 'experiments/runner-addition/center-selection/'
    path = HERE/'manifest.json'
    assert path.read_bytes() == subprocess.check_output(['git','show',freeze+':'+rel+'manifest.json'],cwd=ROOT)
    for name, digest in json.loads(path.read_text())['sha256'].items():
        raw = (ROOT/name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest, name
        assert raw == subprocess.check_output(['git','show',freeze+':'+name],cwd=ROOT), name


def grid_diagnostic(speeds, d, caps):
    # A deliberately capped heuristic, not part of the complete selector.
    checks, terms, unknowns = 0, 0, 0
    for v in range(2, len(speeds)+3):
        for u in range(1, v):
            if gcd(u,v) != 1:
                continue
            checks += 1
            c = F(u,v)
            G = min((norm(s*c)-d)/s for s in speeds)
            if G <= 0:
                continue
            h = required(c,d,caps['H_terms'])
            terms += h['terms']
            if h['status'] != 'EXACT':
                unknowns += 1
            elif h['H'] <= G:
                return dict(status='FOUND',center=c,H=h['H'],G=G,
                            predicates=checks*len(speeds),H_terms=terms)
    return dict(status='UNKNOWN' if unknowns else 'NO_GRID_CENTER',
                predicates=checks*len(speeds),H_terms=terms)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--freeze',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--checkpoint-dir',required=True)
    a=p.parse_args()
    check_freeze(a.freeze)
    cfg=json.loads((HERE/'config.json').read_text())
    checkpoint=Path(a.checkpoint_dir); checkpoint.mkdir(parents=True,exist_ok=True)
    result=dict(freeze=a.freeze,rule_freeze=cfg['rule_freeze'],cases=[])
    for case in cfg['cases']:
        S,d=case['speeds'],F(case['d'])
        decision=select(S,d,cfg['caps'])
        row=dict(case=case,primary=decision,heuristic=grid_diagnostic(S,d,cfg['caps']))
        row['witnesses']=[]
        if decision['status']=='YES':
            interval=decision['selected']['interval']
            cutoff=ceil(2*d/(interval[1]-interval[0]))
            row['cutoff']=cutoff
            if cutoff-1 > cfg['caps']['contacts']:
                row['recovery_status']='UNKNOWN_RECOVERY'
            else:
                tests=set(r for r in range(1,cutoff) if r not in S)
                for raw in [cutoff,cutoff+1,10**6+1,10**18+1]:
                    while raw in S: raw+=1
                    tests.add(raw)
                row['witnesses']=[witness(interval,r,S,d) for r in sorted(tests)]
                row['recovery_status']='COMPLETE_FINITE_PLUS_TAIL_CONTROLS'
        result['cases'].append(row)
        (checkpoint/(case['id']+'.json')).write_text(dump(row))
    # Deliberate resource stops; never counted as mathematical NO.
    S=[1,2,3,4,5,7,10,19]; d=F(1,10)
    result['budget_controls']={}
    for key in ['events','candidates','speed_sum','H_terms']:
        cap=dict(cfg['caps']); cap[key]=0
        result['budget_controls'][key]=select(S,d,cap)
    result['budget_controls']['specified_center']=required(F(159,1330),d,1)
    Path(a.output).write_text(dump(result))
    print(dump({'cases':len(result['cases']),'statuses':{s:sum(x['primary']['status']==s for x in result['cases']) for s in sorted({x['primary']['status'] for x in result['cases']})}}))

if __name__=='__main__': main()
