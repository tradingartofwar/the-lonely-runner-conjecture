import sys,json,time,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
S=P.parent/'run_support.py'
def rec(*args):
 r=subprocess.run([sys.executable,str(S),*args],check=True,capture_output=True,text=True)
 obj=json.loads(r.stdout);print(r.stdout,end='');return obj
def clock():
 s=json.loads((P/'STATUS.json').read_text()); elapsed=time.time()-s['started_epoch'];assert elapsed<s['deadline_seconds'],f'DEADLINE {elapsed}';return elapsed
def log(operation,tid,agent):
 t=json.loads((P/'trials'/f'{tid}.json').read_text());msg=t['messages'][-1]['content'] if operation=='followup_task' else t['messages'][0]['content']
 with (P/'INVOCATIONS.jsonl').open('a') as f:f.write(json.dumps({'operation':operation,'trial_id':tid,'task_name':tid.lower(),'fork_turns':'none' if operation=='spawn_agent' else None,'model_override':None,'reasoning_override':None,'agent_path':agent,'message_sha256':hashlib.sha256(msg.encode()).hexdigest(),'recorded_at':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':clock()},ensure_ascii=False)+'\n')
a=sys.argv[1:]
if a[0]=='start':rec('init',a[1]);rec('begin','R001');print('CLOCK_SECONDS',clock())
elif a[0]=='register':
 rec('register',a[1],a[2]);log('spawn_agent',a[1],a[2]);
 if len(a)>3:rec('begin',a[3]);print('CLOCK_SECONDS',clock())
elif a[0]=='reply':
 tid=a[1];raw=sys.stdin.read();raw=raw[:-1] if raw.endswith('\n') else raw;i=len(list((P/'incoming').glob(tid+'-*.txt')))+1;p=P/'incoming'/f'{tid}-{i:02d}.txt';p.write_text(raw);rec('reply',tid,str(p));print('CLOCK_SECONDS',clock())
elif a[0]=='delivered':
 rec('delivered',a[1]);t=json.loads((P/'trials'/f'{a[1]}.json').read_text());log('followup_task',a[1],t['agent'])
elif a[0]=='begin':rec('begin',a[1]);print('CLOCK_SECONDS',clock())
elif a[0]=='clock':print('CLOCK_SECONDS',clock())
elif a[0]=='close':rec('close')
