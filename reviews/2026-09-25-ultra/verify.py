"""Read-only reproduction of bounded Ultra-review certificate checks.

Run from any directory: python /path/to/reviews/2026-09-25-ultra/verify.py
Optional positional arguments select checks: early affine overlap tilings
perturbations package root. Default: all seven.

The reviewers' standalone scripts import no project modules. The two that
normally write JSON have writes captured in memory and compared to the archived
review outputs. Assertions remain enabled. This is not a theorem prover.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECKS = {
    "early": ("early_check.py", None),
    "affine": ("affine_checks.py", None),
    "overlap": ("overlap_check.py", "overlap_check.json"),
    "tilings": ("test_tilings.py", None),
    "perturbations": ("check_perturbations.py", "check_perturbations_results.json"),
    "package": ("audit_package.py", None),
    "root": ("verify_review_findings.py", "root_checks.json"),
}

# Child isolation avoids accumulated module/global state. All writes made by
# these scripts use Path.write_text; unexpected destinations are rejected.
BOOTSTRAP = r'''
import json, runpy, sys
from pathlib import Path
script=Path(sys.argv[1]).resolve()
root=Path(sys.argv[2]).resolve()
captured={}
def capture(self,data,*args,**kwargs):
    path=self.resolve()
    if path.parent != script.parent or path.name not in ("affine_checks.json","test_tilings_results.json"):
        raise RuntimeError("Unexpected write destination: "+str(path))
    captured[path]=data
    return len(data)
Path.write_text=capture
sys.argv=[str(script),str(root)]
runpy.run_path(str(script),run_name="__main__")
for path,data in captured.items():
    assert json.loads(data)==json.loads(path.read_text()), "Review output drift: "+path.name
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checks", nargs="*")
    args=parser.parse_args()
    names=args.checks or list(CHECKS)
    for name in names:
        if name not in CHECKS:
            parser.error("Unknown check: "+name)
        script,expected=CHECKS[name]
        print("Checking "+name+"...",flush=True)
        result=subprocess.run([sys.executable,"-B","-c",BOOTSTRAP,str(HERE/script),str(ROOT)],
                              cwd=ROOT,text=True,capture_output=True)
        if result.returncode:
            print(result.stdout,end="")
            print(result.stderr,file=sys.stderr,end="")
            return result.returncode
        if expected:
            assert json.loads(result.stdout)==json.loads((HERE/expected).read_text()), name+" output drift"
        if name=="package":
            summary=json.loads(result.stdout)
            print("  "+str(summary["recorded_hashes_checked"])+" hashes; "+
                  str(summary["validated_endpoint_certificate_groups"])+" endpoint groups.")
        print("PASS "+name,flush=True)
    print("All selected bounded checks passed; no archived output was rewritten.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
