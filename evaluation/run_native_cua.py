"""Paid native Responses/computer runner. Refuses execution without explicit local approval.

The only UI motor is NativeBrowser.execute(model_action). No task-specific click scripts.
Raw evidence is private until independently reviewed and redacted for publication.
"""
import argparse
import base64
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from efficient_context import SYSTEM,make_input,evidence_request,screenshot_output,token_cost,reserve_request,TotalBudgetExhausted
from execution_order import load_order,require_next

HERE=Path(__file__).resolve().parent; REPO=HERE.parent
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');tmp.replace(path)
def stamp():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def execution_fingerprint():
    names=['optimized_config.json','run_native_cua.py','efficient_context.py','native_driver.py','browser_environment.mjs','execution_order.py','execution_order.json']
    return hashlib.sha256(b'\n'.join(name.encode()+b'\0'+(HERE/name).read_bytes().replace(b'\r\n',b'\n') for name in names)).hexdigest()

def validate_approval(approval,frozen,cfg):
    if approval.get('approved') is not True or approval.get('model')!=cfg['model'] or approval.get('suite_sha256')!=frozen['files']['evaluation/final_test_cases_100.json']:
        raise RuntimeError('Approval does not match frozen suite and model')
    if approval.get('execution_fingerprint')!=execution_fingerprint():
        raise RuntimeError('New explicit approval must match this optimized executor and configuration')
    if type(approval.get('budget_usd')) not in (int,float) or not 0<approval['budget_usd']<=min(10,cfg['proposed_total_budget_usd']):
        raise RuntimeError('Approved budget must be greater than zero and no more than $10')
    if not approval.get('approved_at') or not approval.get('user_approval_text'):
        raise RuntimeError('Explicit approval timestamp and user statement required')

def validate_local_readiness():
    fixture=read(HERE/'logs/offline-fixture-preflight.json')
    browser=read(HERE/'logs/infrastructure-check.json')
    if fixture.get('fixtures_ok')!=100:raise RuntimeError('All isolated database prerequisites must pass offline preflight')
    if browser.get('error') or browser.get('server_health')!='ok' or browser.get('native_browser_foreground_verified') is not True:
        raise RuntimeError('Local browser preflight is incomplete; no paid execution permitted')
    if browser.get('execution_fingerprint')!=execution_fingerprint():
        raise RuntimeError('Browser preflight must match the current executor')

def key():
    value=os.environ.get('OPENAI_API_KEY')
    if not value and os.name=='nt':
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,'Environment') as reg:value=winreg.QueryValueEx(reg,'OPENAI_API_KEY')[0]
        except FileNotFoundError:pass
    return value

def api(path,body=None,timeout=90):
    token=key()
    if not token:raise RuntimeError('OPENAI_API_KEY unavailable; configure it locally, never in chat/repository')
    req=Request('https://api.openai.com/v1/'+path,data=json.dumps(body).encode() if body is not None else None,
                headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
    try:
        with urlopen(req,timeout=timeout) as response:return json.load(response)
    except HTTPError as exc:
        # No provider payloads/headers are printed; credentials never enter public exceptions.
        raise RuntimeError(f'OpenAI HTTP {exc.code}; no automatic retry') from None

def verify_freeze():
    f=read(HERE/'freeze.json')
    for name,digest in f['files'].items():
        canonical=hashlib.sha256((REPO/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        if sha(REPO/name)!=digest and canonical!=f.get('canonical_lf_files',{}).get(name):
            raise RuntimeError('Frozen artifact changed: '+name)
    diff=subprocess.run(['git','diff','--quiet',f['application_commit'],'--','backend','frontend'],cwd=REPO)
    if diff.returncode:raise RuntimeError('Application/frontend tree differs from the frozen baseline')
    return f

def preflight(remote=False):
    f=verify_freeze();cfg=read(HERE/'optimized_config.json')
    import importlib.util
    report={'checked_at':stamp(),'freeze_valid':True,'api_key_available':bool(key()),
            'model':cfg['model'],'native_model_entitlement':'not verified',
            'dependencies':{x:bool(importlib.util.find_spec(x)) for x in ['django','PIL','pyautogui']},
            'frontend_build_present':(REPO/'frontend/dist/index.html').exists(),'paid_model_requests':0,
            'execution_fingerprint':execution_fingerprint(),'approval_present':(HERE/'approval.local.json').exists(),
            'profile':cfg['profile'],'proposed_ceiling_usd':cfg['proposed_total_budget_usd']}
    if remote and key():
        info=api('models/'+cfg['model'])
        report['native_model_entitlement']='model metadata accessible; native request compatibility still requires first approved attempt'
        report['model_metadata_id']=info['id']
    write(HERE/'preflight.json',report)
    print(json.dumps(report,indent=2))

def snapshot(db,target):
    """Read-only independent verification evidence; never available to the solving model."""
    data={}
    with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True) as con:
        con.row_factory=sqlite3.Row
        names=[r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        for name in names:
            if not name.startswith('portal_') or name=='portal_passwordreset':continue
            data[name]=[dict(r) for r in con.execute('SELECT * FROM "'+name+'"')]
    write(target,data)

def start_server(folder):
    env=os.environ.copy()
    for k in list(env):
        if k.startswith('CC_DB_'):env.pop(k)
    env.update(read(folder/'environment.json'))
    log=open(folder/'server.log','w',encoding='utf-8')
    server=subprocess.Popen([sys.executable,str(REPO/'backend/manage.py'),'runserver','127.0.0.1:18380','--noreload'],cwd=REPO,env=env,stdout=log,stderr=log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    for _ in range(100):
        if server.poll() is not None:break
        try:
            with urlopen('http://127.0.0.1:18380/api/healthcheck/',timeout=1) as response:
                if json.load(response).get('status')=='ok':return server,log
        except Exception:time.sleep(.1)
    server.terminate();server.wait(timeout=10);log.close()
    raise RuntimeError('Isolated evaluation server failed health check')

def run_one(test,cfg,approval,ledger_path):
    tid=test['id'];limits=cfg['limits'][test['difficulty']]
    ledger=read(ledger_path) if ledger_path.exists() else {'estimated_cost_usd':0,'reserved_unknown_usd':0,'attempts':[]}
    if any(x['test_id']==tid for x in ledger['attempts']):raise RuntimeError(tid+' already has an attempt; no silent retries')
    attempt_id=tid+'-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder=HERE/'.private'/attempt_id
    result={'test_id':tid,'attempt_id':attempt_id,'started_at':stamp(),'status':'NOT_RUN','actual_outcome':'Not started',
            'model':cfg['model'],'execution_fingerprint':execution_fingerprint(),'model_requests':0,'token_count_requests':0,'actions':0,'input_tokens':0,'output_tokens':0,'cached_input_tokens':0,'estimated_cost_usd':0,'reserved_unknown_usd':0,'execution_seconds':0,'evidence':[]}
    ledger['attempts'].append({'test_id':tid,'attempt_id':attempt_id,'status':'starting'})
    write(ledger_path,ledger)
    started=time.monotonic();server=browser=server_log=None
    # Results remain ERROR/pending review unless independent evidence establishes a final classification.
    try:
        setup=subprocess.run([sys.executable,str(HERE/'prepare_environment.py'),tid,str(folder)],capture_output=True,text=True)
        if setup.returncode:
            result.update(status='BLOCKED',actual_outcome='Independent fixture preparation failed; no valid task attempt',failure_reason='See private setup-error.log')
            folder.mkdir(parents=True,exist_ok=True);(folder/'setup-error.log').write_text(setup.stdout+setup.stderr,encoding='utf-8');return result
        server,server_log=start_server(folder)
        snapshot(folder/'test.sqlite3',folder/'before-state.json')
        from native_driver import NativeBrowser
        browser=NativeBrowser(folder,cfg['target_origin'],narrow=tid in {'T030','T090'})
        manifest=read(folder/'manifest.json')
        shot=browser.screenshot();(folder/'0000.png').write_bytes(shot)
        executed=[];observations=[];last_output=last_results=None
        while True:
            if time.monotonic()-started>limits['runtime_seconds']:raise RuntimeError('Per-test runtime limit reached')
            if result['model_requests']>=limits['model_requests']:raise RuntimeError('Per-test model-request limit reached')
            history=make_input(test,manifest,executed,observations,shot,last_output,last_results)
            body={'model':cfg['model'],'tools':[{'type':'computer'}],'instructions':SYSTEM,'input':history,
                  'reasoning':{'effort':cfg['reasoning_effort']},'text':{'verbosity':cfg['text_verbosity']}}
            count=api('responses/input_tokens',body,timeout=cfg['api_timeout_seconds']);result['token_count_requests']+=1
            n=count['input_tokens'];maxout=cfg['max_output_tokens_per_request']
            if n>cfg['max_input_tokens_per_request']:raise RuntimeError('Input-token limit would be exceeded')
            reserve=reserve_request(n,maxout,result,limits,ledger,approval['budget_usd'])
            # Persist reservation before dispatch; retain it if outcome/charge is ambiguous.
            ledger['reserved_unknown_usd']+=reserve;write(ledger_path,ledger)
            body.update(max_output_tokens=maxout,store=False,service_tier=cfg['service_tier'])
            write(folder/f'request-{result["model_requests"]+1:04}.json',{'request':evidence_request(body),'counted_input_tokens':n,'reserved_usd':reserve})
            result['model_requests']+=1
            try:response=api('responses',body,timeout=min(cfg['api_timeout_seconds'],max(1,int(limits['runtime_seconds']-(time.monotonic()-started)))))
            except Exception:
                result['reserved_unknown_usd']+=reserve
                raise
            seq=result['model_requests'];write(folder/f'response-{seq:04}.json',response)
            usage=response.get('usage')
            if not usage:
                result['reserved_unknown_usd']+=reserve
                raise RuntimeError('Missing usage; reserved cost retained and execution stopped')
            inp=usage['input_tokens'];out=usage['output_tokens'];cached=usage.get('input_tokens_details',{}).get('cached_tokens',0)
            cost=token_cost(inp,out,cached)
            result['input_tokens']+=inp;result['output_tokens']+=out;result['cached_input_tokens']+=cached
            result['estimated_cost_usd']+=cost;ledger['estimated_cost_usd']+=cost;ledger['reserved_unknown_usd']-=reserve
            write(ledger_path,ledger)
            write(folder/f'usage-{seq:04}.json',{'response_id':response['id'],'usage':usage,'cost_usd':cost,'reservation_usd':reserve,'service_tier':response.get('service_tier'),'model':response.get('model')})
            if cost>reserve+1e-9:raise RuntimeError('Provider usage exceeded reservation; stop for billing reconciliation')
            if response.get('status')!='completed':raise RuntimeError('Incomplete native response; no automatic paid retry')
            calls=[x for x in response['output'] if x['type']=='computer_call']
            for item in response['output']:
                if item['type']=='message':
                    observations.extend(c['text'] for c in item.get('content',[]) if c.get('type')=='output_text')
            if not calls:
                result.update(status='ERROR',actual_outcome='Native CUA stopped; independent review required before scoring',failure_reason='PENDING_INDEPENDENT_REVIEW')
                result['agent_final_text']='\n'.join(c.get('text','') for x in response['output'] if x['type']=='message' for c in x.get('content',[]) if c['type']=='output_text')
                break
            last_output=response['output'];last_results=[]
            for call in calls:
                if call.get('pending_safety_checks'):
                    result.update(status='BLOCKED',actual_outcome='Native model safety check needs operator review',failure_reason='No safety acknowledgement was automatically granted')
                    return result
                actions=call.get('actions')
                if actions is None:raise RuntimeError('Native actions array absent; stop rather than substitute a scripted solver')
                for action in actions:
                    if result['actions']>=limits['actions']:raise RuntimeError('Per-test native-action limit reached')
                    if time.monotonic()-started>limits['runtime_seconds']:raise RuntimeError('Runtime limit reached during action batch')
                    event={'at':stamp(),'response_id':response['id'],'call_id':call['call_id'],'action':action}
                    with (folder/'actions.jsonl').open('a',encoding='utf-8') as stream:stream.write(json.dumps(event)+'\n')
                    result['actions']+=1
                    browser.execute(action)
                    executed.append(action)
                    evidence_name=f'action-{result["actions"]:04}.png'
                    shot=browser.screenshot()
                    (folder/evidence_name).write_bytes(shot)
                    result['evidence'].append(evidence_name)
                if not actions:shot=browser.screenshot()
                # The final action frame is already current; no duplicate batch screenshot.
                last_results.append({'type':'computer_call_output','call_id':call['call_id'],'output':screenshot_output(shot)})
    except TotalBudgetExhausted as exc:
        result.update(status='ERROR' if result['model_requests'] else 'NOT_RUN',actual_outcome='Stopped at approved budget; no skipped steps or inferred success',failure_reason=str(exc))
        ledger['stop_reason']='TOTAL_BUDGET_EXHAUSTED'
        ledger['stopped_at_test']=tid
    except Exception as exc:
        result.update(status='ERROR',actual_outcome='Execution stopped without automatic retry',failure_reason=str(exc))
    finally:
        if browser:
            try:(folder/'final.png').write_bytes(browser.screenshot())
            except Exception:pass
            browser.close()
        if server:
            server.terminate()
            try:server.wait(timeout=10)
            except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
            server_log.close()
            snapshot(folder/'test.sqlite3',folder/'after-state.json')
        result['execution_seconds']=round(time.monotonic()-started,3);result['finished_at']=stamp()
        folder.mkdir(parents=True,exist_ok=True);write(folder/'attempt.json',result)
        ledger['attempts'][-1]['status']=result['status'];write(ledger_path,ledger)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preflight',action='store_true');parser.add_argument('--check-model',action='store_true')
    parser.add_argument('--test');parser.add_argument('--all',action='store_true')
    args=parser.parse_args()
    if args.preflight or args.check_model:return preflight(remote=args.check_model)
    frozen=verify_freeze();suite=read(HERE/'final_test_cases_100.json');cfg=read(HERE/'optimized_config.json')
    approved=HERE/'approval.local.json'
    if not approved.exists():raise SystemExit('STOP: explicit user budget approval is required; no paid calls made')
    approval=read(approved)
    validate_approval(approval,frozen,cfg)
    validate_local_readiness()
    if not key():raise SystemExit('STOP: API key not configured')
    if not args.all and args.test not in [x['id'] for x in suite['tests']]:raise SystemExit('Choose --test T001 or --all')
    private=HERE/'.private';private.mkdir(exist_ok=True)
    lock=private/'run.lock'
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    try:
        ordered=load_order(suite)
        initial=read(private/'ledger.json') if (private/'ledger.json').exists() else {'attempts':[]}
        if initial.get('stop_reason'):raise RuntimeError('Run stopped: '+initial['stop_reason']+'; no automatic continuation')
        require_next(ordered,initial['attempts'],None if args.all else args.test)
        reviews=read(HERE/'review.local.json') if (HERE/'review.local.json').exists() else {}
        if any(a['test_id'] not in reviews for a in initial['attempts']):
            raise RuntimeError('Every previous attempt requires independent review before continuation')
        for test in ordered:
            if not args.all and test['id']!=args.test:continue
            ledger_path=private/'ledger.json'
            prior=read(ledger_path) if ledger_path.exists() else {'attempts':[],'reserved_unknown_usd':0}
            if prior['reserved_unknown_usd']>0:
                raise RuntimeError('Unresolved API cost reservation; reconcile it before further paid calls')
            if any(a['test_id']==test['id'] for a in prior['attempts']):
                if not args.all:raise RuntimeError('Already attempted; no silent retry')
                reviews=read(HERE/'review.local.json') if (HERE/'review.local.json').exists() else {}
                if test['id'] not in reviews:
                    raise RuntimeError(test['id']+' requires independent review before batch continuation')
                continue
            result=run_one(test,cfg,approval,private/'ledger.json')
            print(json.dumps({k:result[k] for k in ['test_id','status','model_requests','actions','estimated_cost_usd']}),flush=True)
            if result['status'] in {'ERROR','BLOCKED','NOT_RUN'} or result['reserved_unknown_usd']:
                print('Stopped for independent review/infrastructure triage; no batch continuation or hidden retry.');break
    finally:os.close(fd);lock.unlink()

if __name__=='__main__':main()
