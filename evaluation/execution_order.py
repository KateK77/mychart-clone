"""Precommitted, outcome-independent stratification; never rewrites frozen tasks."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PATTERN=['Easy','Medium','Hard','Expert','Medium','Easy','Hard','Medium','Easy','Medium']

def planned_rows(suite):
    pools={d:iter(sorted((t for t in suite['tests'] if t['difficulty']==d),key=lambda t:t['id'])) for d in set(PATTERN)}
    return [{'rank':block*10+i+1,'block':block+1,'test_id':next(pools[d])['id'],'difficulty':d}
            for block in range(10) for i,d in enumerate(PATTERN)]

def load_order(suite):
    plan=json.loads((HERE/'execution_order.json').read_text(encoding='utf-8'))
    frozen=json.loads((HERE/'freeze.json').read_text(encoding='utf-8'))
    if plan['suite_sha256']!=frozen['files']['evaluation/final_test_cases_100.json'] or plan['tests']!=planned_rows(suite):
        raise RuntimeError('Precommitted execution order or suite binding changed')
    by_id={t['id']:t for t in suite['tests']}
    if len(by_id)!=100 or set(by_id)!={r['test_id'] for r in plan['tests']}:
        raise RuntimeError('Order must contain all 100 tests exactly once')
    return [by_id[r['test_id']] for r in plan['tests']]

def require_next(ordered,attempts,requested=None):
    ids=[t['id'] for t in ordered]
    attempted=[a['test_id'] for a in attempts]
    if attempted!=ids[:len(attempted)]:raise RuntimeError('Attempt ledger is not a prefix of the fixed order')
    next_id=ids[len(attempted)] if len(attempted)<len(ids) else None
    if requested is not None and requested!=next_id:
        raise RuntimeError(f'Next precommitted test is {next_id}; no reorder, skip or automatic retry')
    return next_id

if __name__=='__main__':
    suite=json.loads((HERE/'final_test_cases_100.json').read_text(encoding='utf-8'))
    frozen=json.loads((HERE/'freeze.json').read_text(encoding='utf-8'))
    target=HERE/'execution_order.json'
    if (HERE/'.private/ledger.json').exists():raise SystemExit('Cannot author order after a ledger exists')
    plan={'version':1,'state':'PRECOMMITTED_BEFORE_PAID_EXECUTION','suite_sha256':frozen['files']['evaluation/final_test_cases_100.json'],
          'rule':'Ten identical difficulty blocks, ascending original ID within each difficulty. No outcome/cost-based selection.',
          'block_pattern':PATTERN,'tests':planned_rows(suite)}
    if target.exists() and json.loads(target.read_text(encoding='utf-8'))!=plan:raise SystemExit('Existing order differs; explicit protocol revision required')
    target.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    print('Fixed order validated: 100 unique tasks, 30/40/20/10 difficulty totals')
