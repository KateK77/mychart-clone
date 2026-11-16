"""Aggregate native attempts plus independently reviewed decisions. Never infer PASS."""
import csv
from collections import Counter
import json
from pathlib import Path
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
suite=read(HERE/'final_test_cases_100.json'); frozen=read(HERE/'freeze.json')
reviews=read(HERE/'review.local.json') if (HERE/'review.local.json').exists() else {}
results=[]
for t in suite['tests']:
    attempts=sorted((HERE/'.private').glob(t['id']+'-*/attempt.json'))
    if len(attempts)>1:raise SystemExit('Multiple attempts require explicit disclosed selection: '+t['id'])
    raw=read(attempts[0]) if attempts else None
    r={'test_id':t['id'],'description':t['task'],'difficulty':t['difficulty'],'functional_category':t['functional_category'],
       'requirement_ids':t['requirement_ids'],'expected_outcome':t['expected_result'],
       'status':'NOT_RUN','actual_outcome':'No native CUA attempt yet. Awaiting matching API configuration and explicit budget approval.',
       'failure_reason':None,'evidence':[],'model_requests':0,'token_count_requests':0,'actions':0,'execution_seconds':0,
       'input_tokens':0,'output_tokens':0,'cached_input_tokens':0,'estimated_cost_usd':0,'actual_api_cost_usd':None}
    if raw:
        for k in ['status','actual_outcome','failure_reason','model_requests','token_count_requests','actions','execution_seconds','input_tokens','output_tokens','cached_input_tokens','estimated_cost_usd']:
            if k in raw:r[k]=raw[k]
        r['attempt_id']=raw['attempt_id']
    review=reviews.get(t['id'])
    if review:
        if not raw:raise SystemExit('Cannot review an unexecuted task: '+t['id'])
        if review['status'] not in {'PASS','FAIL','BLOCKED','ERROR'}:raise SystemExit('Invalid review status')
        checks=review.get('criteria',[])
        if review['status'] in {'PASS','FAIL'}:
            if len(checks)!=len(t['pass_fail_criteria']):raise SystemExit('Review must cover every criterion: '+t['id'])
            if review['status']=='PASS' and not all(x.get('met') is True for x in checks):raise SystemExit('PASS lacks criterion evidence')
            if review['status']=='FAIL' and not any(x.get('met') is False and x.get('application_failure') is True for x in checks):raise SystemExit('FAIL needs an application failure, not CUA navigation error')
        for ref in review['evidence']:
            p=(HERE/ref).resolve()
            if not p.is_relative_to(HERE.resolve()) or '.private' in p.parts or not p.exists():raise SystemExit('Evidence must be sanitized and published: '+ref)
        if review['status'] in {'PASS','FAIL'} and not review['evidence']:raise SystemExit('Scored task has no public evidence')
        r.update({k:review[k] for k in ['status','actual_outcome','failure_reason','evidence']})
        r['criterion_review']=checks
    results.append(r)

counts=Counter(r['status'] for r in results)
for status in ['PASS','FAIL','BLOCKED','ERROR','NOT_RUN']:counts.setdefault(status,0)
valid=counts['PASS']+counts['FAIL'];all_valid=valid==100
def grouped(field):
    out=[]
    for k in dict.fromkeys(t[field] for t in results):
        rows=[r for r in results if r[field]==k];c=Counter(r['status'] for r in rows)
        out.append({'name':k,'total':len(rows),**{s:c[s] for s in counts},'primary_pass_rate_percent':100*c['PASS']/len(rows)})
    return out
totals={k:sum(r[k] for r in results) for k in ['model_requests','token_count_requests','actions','execution_seconds','input_tokens','output_tokens','cached_input_tokens','estimated_cost_usd']}
report={'evaluation_complete':all_valid,'execution_state':'NOT_STARTED' if not totals['model_requests'] else ('COMPLETE' if all_valid else 'INCOMPLETE'),
    'specification':suite['description'],'application_commit':suite['application_commit'],'suite_frozen_at':frozen['frozen_at'],
    'cua_model_used':read(HERE/'optimized_config.json')['model'] if totals['model_requests'] else None,
    'total':100,'counts':dict(counts),'primary_overall_pass_rate_percent':counts['PASS'],
    'validly_evaluated_pass_rate_percent':100*counts['PASS']/valid if valid else None,'difficulty_results':grouped('difficulty'),
    'category_results':grouped('functional_category'),'usage':totals,'actual_api_cost_usd':None,'results':results}
(HERE/'final_results_100.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
with (HERE/'summary.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=['test_id','difficulty','functional_category','status','description','expected_outcome','actual_outcome','failure_reason','model_requests','actions','execution_seconds','input_tokens','output_tokens','estimated_cost_usd','evidence'])
    writer.writeheader()
    for r in results:writer.writerow({k:'; '.join(r[k]) if k=='evidence' else r[k] for k in writer.fieldnames})
lines=['# Final native CUA evaluation — '+report['execution_state'],'',
       '**This is incomplete until all100 tasks have valid native CUA evidence and independent decisions.**',
       'No result from the previous Playwright evaluation is included. Before execution,0% is denominator bookkeeping, not an observed application-quality score.','',
       '## A. Overall results','',f"Total:100 | PASS:{counts['PASS']} | FAIL:{counts['FAIL']} | BLOCKED:{counts['BLOCKED']} | ERROR:{counts['ERROR']} | NOT_RUN:{counts['NOT_RUN']}",'',
       f"Primary overall pass rate (PASS/100): **{counts['PASS']}%**.",
       f"Validly evaluated pass rate: **{report['validly_evaluated_pass_rate_percent'] if valid else 'N/A — no validly evaluated tests'}**.",'',
       '## B. Difficulty results','','| Difficulty | Total | PASS | FAIL | BLOCKED | ERROR | NOT_RUN | Pass rate |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
for g in report['difficulty_results']:lines.append(f"| {g['name']} | {g['total']} | {g['PASS']} | {g['FAIL']} | {g['BLOCKED']} | {g['ERROR']} | {g['NOT_RUN']} | {g['primary_pass_rate_percent']:.1f}% |")
lines.extend(['','### Functional categories','','| Category | Total | PASS | FAIL | BLOCKED | ERROR | NOT_RUN | Pass rate |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |'])
for g in report['category_results']:lines.append(f"| {g['name']} | {g['total']} | {g['PASS']} | {g['FAIL']} | {g['BLOCKED']} | {g['ERROR']} | {g['NOT_RUN']} | {g['primary_pass_rate_percent']:.1f}% |")
lines.extend(['','## C. Detailed results',''])
for r in results:
    lines.extend([f"### {r['test_id']} — {r['description']}",'',f"Difficulty: {r['difficulty']} | Category: {r['functional_category']} | Status: **{r['status']}**",'',
       f"Expected: {r['expected_outcome']}",'',f"Actual: {r['actual_outcome']}",'',f"Reason: {r['failure_reason'] or 'None recorded.'}",'',
       'Evidence: '+(', '.join(f'[{Path(p).name}]({p})' for p in r['evidence']) or 'None — do not infer execution.'),''])
lines.extend(['## D. Failure analysis','',
       'Application failures are established only by criterion-specific evidence from a valid native attempt. CUA navigation mistakes, limits, model/API errors and adapter failures are ERROR; missing prerequisites are BLOCKED.',
       'Before execution there are no findings about missing features, incorrect functionality, UI/UX, permissions or validation. None should be inferred from NOT_RUN.',
       'Pending independent review is explicitly marked ERROR with PENDING_INDEPENDENT_REVIEW; it is not an application failure and must be resolved before claiming completion.','',
       '## E. Evaluation metadata','',f"- Description: {suite['description']['version']} ({suite['description']['sha256']}).",f"- Application commit: `{suite['application_commit']}`.",
       f"- CUA model used: {report['cua_model_used'] or 'None — no paid execution yet'}.",f"- Model requests: {totals['model_requests']}; token-count requests: {totals['token_count_requests']}; native actions: {totals['actions']}.",
       f"- Summed attempt execution time: {totals['execution_seconds']} seconds.",f"- Input/output/cache tokens: {totals['input_tokens']}/{totals['output_tokens']}/{totals['cached_input_tokens']}.",
       f"- Token-rate cost estimate: ${totals['estimated_cost_usd']:.6f}; actual invoice cost: not available.",
       '- Planned model and cost ceilings: see [budget plan](BUDGET_AND_EXECUTION.md).',
       '- No application or Description changes. No merge to main.',''])
(HERE/'FINAL_EVALUATION_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'state':report['execution_state'],'counts':counts,'overall_percent':counts['PASS'],'valid_percent':report['validly_evaluated_pass_rate_percent']}))
