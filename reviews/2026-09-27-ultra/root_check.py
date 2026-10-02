"""Root crosschecks of global measure and threshold profiles, pinned review scope."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from lonely_runner.checker import feasible_intervals, circular_distance

FIXED = (1,3,4,5,10,28)
J = (F(9,32), F(3,8))
D = F(1,8)

def clip(intervals):
    return [(max(a,J[0]),min(b,J[1])) for a,b in intervals if max(a,J[0])<=min(b,J[1])]

def length(intervals):
    return sum((b-a for a,b in intervals),F(0))

def main():
    base = feasible_intervals(FIXED,D)
    assert length(base)==F(15,112)
    records=[]
    for h in (1,2,3,4):
        y=1680*h
        full=feasible_intervals((*FIXED,y),D)
        assert length(full)==F(45,448)
        assert clip(full)==([(J[0],J[0])] if h%2 else [])
        critical=F(3,8*(y+3))
        tstar=J[1]-F(1,8*(y+3))
        beta=F(y,8*(y+3))
        profile=[]
        for factor in (F(0),F(1,2),F(1),F(2)):
            eps=factor*critical
            alpha=D-eps
            got=clip(feasible_intervals((*FIXED,y),alpha))
            expected=[]
            if h%2:
                expected.append((J[0],J[0]+eps/28))
            if factor>=1:
                expected.append((J[1]-eps/3,J[1]-alpha/y))
            assert got==expected,(h,factor,got,expected)
            profile.append({'epsilon':eps,'threshold':alpha,'components':got,'duration':length(got)})
        assert clip(feasible_intervals((*FIXED,y),D+critical/2))==[]
        if not h%2:
            assert min(circular_distance(v*tstar) for v in (*FIXED,y))==beta
            assert clip(feasible_intervals((*FIXED,y),beta+critical/100))==[]
        # Direct certificate for the strict GLOBAL adaptive witness.
        target=y*F(11,64)-F(1,2)
        nearest=(target+F(1,2)).numerator//(target+F(1,2)).denominator
        witness=(F(nearest)+F(1,2))/y
        assert abs(witness-F(11,64))<=F(1,2*y)
        margin=min(circular_distance(v*witness) for v in (*FIXED,y))-D
        assert margin>=F(1,64)-F(14,y)>0
        records.append({'h':h,'y':y,'global_duration':length(full),
                        'global_positive_components':sum(a<b for a,b in full),
                        'global_isolated_components':sum(a==b for a,b in full),
                        'local_maximum':D if h%2 else beta,
                        'local_maximizer':J[0] if h%2 else tstar,
                        'threshold_profile':profile,'adaptive_global_witness':witness,
                        'actual_witness_margin':margin,'certified_margin':F(1,64)-F(14,y)})
    out={'baseline_commit':'e94a87f650264826569cae63412c43a5175f5ae4',
         'fixed_speeds':FIXED,'fixed_allowed_set':base,'fixed_allowed_duration':length(base),
         'window':J,'threshold':D,'cases':records,
         'scope':'Four exact checker controls. The accompanying synthesis gives the all-h proof, rather than extrapolating these cases.',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'checker_sha256':hashlib.sha256((ROOT/'lonely_runner/checker.py').read_bytes()).hexdigest()}
    encoded=json.dumps(out,indent=2,default=str)+'\n'
    dest=Path(__file__).with_name('root_checks.json')
    if sys.argv[1:]==['--check']:
        assert json.loads(encoded)==json.loads(dest.read_text())
        print('PASS: four full-period controls; exact near-threshold component lists; adaptive global witnesses.')
    else:
        assert not sys.argv[1:]
        print(encoded,end='')

if __name__=='__main__':main()
