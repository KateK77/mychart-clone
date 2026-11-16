import hashlib
import json
from pathlib import Path
from datetime import datetime,timezone

here=Path(__file__).resolve().parent
target=here/'freeze.json'
if target.exists():raise SystemExit('Already frozen; refusing to overwrite')
suite=json.loads((here/'final_test_cases_100.json').read_text(encoding='utf-8'))
assert len(suite['tests'])==100
assert [x['id'] for x in suite['tests']]==[f'T{i:03}' for i in range(1,101)]
assert {d:sum(t['difficulty']==d for t in suite['tests']) for d in suite['distribution']}==suite['distribution']
files=['experiments/round-03/description.md','evaluation/final_test_cases_100.json','evaluation/FINAL_TEST_CASES.md','evaluation/FIXTURES.md','evaluation/config.json']
f={'frozen_at':datetime.now(timezone.utc).isoformat(),'application_commit':suite['application_commit'],
   'native_execution_started':False,'files':{p:hashlib.sha256((here.parent/p).read_bytes()).hexdigest() for p in files}}
f['canonical_lf_files']={p:hashlib.sha256((here.parent/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in files}
target.write_text(json.dumps(f,indent=2)+'\n',encoding='utf-8')
print('Frozen100 tests; SHA256='+f['files']['evaluation/final_test_cases_100.json'])
