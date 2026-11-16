"""Prepare all 100 isolated prerequisites and inspect SQLite, without an API or UI task.

The output is infrastructure evidence, never PASS/FAIL for the native CUA suite.
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from run_native_cua import HERE,verify_freeze,write

def check(tid,root):
    folder=root/tid
    proc=subprocess.run([sys.executable,str(HERE/'prepare_environment.py'),tid,str(folder)],capture_output=True,text=True,timeout=180)
    if proc.returncode:return {'test_id':tid,'fixture_ok':False,'reason':'Fixture preparation failed; inspect private setup logs'}
    with sqlite3.connect((folder/'test.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
        integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
        foreign_keys=db.execute('PRAGMA foreign_key_check').fetchall()
        users=db.execute('SELECT COUNT(*) FROM auth_user').fetchone()[0]
        tables=db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'portal_%'").fetchone()[0]
    manifest=json.loads((folder/'manifest.json').read_text())
    environment=json.loads((folder/'environment.json').read_text())
    isolated=Path(environment['CC_SQLITE']).resolve()==(folder/'test.sqlite3').resolve()
    ok=integrity=='ok' and not foreign_keys and users>=10 and tables>=20 and isolated and manifest['test_id']==tid
    return {'test_id':tid,'fixture_ok':ok,'integrity':integrity,'foreign_key_violations':len(foreign_keys),'user_count':users,'portal_tables':tables,'isolated_database':isolated}

def main():
    verify_freeze()
    if (HERE/'approval.local.json').exists():raise SystemExit('Offline preflight expected before paid approval')
    root=HERE/'.private'/('offline-fixtures-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
    root.mkdir(parents=True)
    started=time.monotonic();rows=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(check,f'T{i:03}',root):f'T{i:03}' for i in range(1,101)}
        for f in as_completed(futures):
            try:row=f.result()
            except Exception as exc:row={'test_id':futures[f],'fixture_ok':False,'reason':type(exc).__name__}
            rows.append(row)
            if len(rows)%10==0:print(json.dumps({'fixtures_checked':len(rows),'ok':sum(x['fixture_ok'] for x in rows)}),flush=True)
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Infrastructure prerequisites only; no native CUA tasks executed',
            'paid_requests':0,'token_count_api_requests':0,'scored_tests':0,'seconds':round(time.monotonic()-started,2),
            'fixtures_ok':sum(x['fixture_ok'] for x in rows),'total':100,'results':sorted(rows,key=lambda r:r['test_id'])}
    write(HERE/'logs/offline-fixture-preflight.json',report)
    write(HERE/'.private/latest-offline-fixtures.json',{'path':str(root)})
    print(json.dumps({k:v for k,v in report.items() if k!='results'}))
    if report['fixtures_ok']!=100:raise SystemExit(1)

if __name__=='__main__':main()
