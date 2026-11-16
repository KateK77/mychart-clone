"""Offline planning arithmetic, not a native test run or a tokenizer measurement.

Use --measure-local-fixtures only after offline_fixture_preflight.py. Public output
contains character counts and assumptions, never credentials or raw fixture data.
"""
import argparse
import json
import math
from pathlib import Path
from collections import Counter
from efficient_context import SYSTEM,prompt_text,image_tokens,token_cost
from run_native_cua import HERE,read,write,verify_freeze

# Human forecasts of screenshot-observation rounds for the unchanged workflows.
# They include UI login, navigation, role switches, validation and final inspection.
# These values do not generate actions and are never passed to the solving model.
CENTRAL=[
    6,15,12,5,7,6,6,7,7,7,4,5,5,5,5,6,6,6,5,7,5,5,5,5,5,6,6,7,9,7,
    12,9,12,9,15,17,9,12,10,8,9,16,20,11,12,12,11,11,11,12,9,10,15,16,16,12,20,10,12,12,11,11,11,10,13,10,19,18,18,18,
    14,10,16,15,18,20,18,18,18,20,22,22,16,18,12,18,22,20,16,18,
    34,55,40,40,28,42,36,30,65,32
]
OUTPUT={'Easy':60,'Medium':90,'Hard':110,'Expert':130}
SCENARIOS={
    'optimistic':{'request_factor':.7,'chars_per_token':4.5,'output_factor':.75,'history_tokens_per_round':45,'protocol_tokens_per_request':120},
    'central':{'request_factor':1,'chars_per_token':4,'output_factor':1,'history_tokens_per_round':65,'protocol_tokens_per_request':180},
    'cautious':{'request_factor':1.4,'chars_per_token':3.5,'output_factor':1.5,'history_tokens_per_round':95,'protocol_tokens_per_request':250}
}

def measure(suite):
    root=Path(read(HERE/'.private/latest-offline-fixtures.json')['path'])
    rows=[]
    for t,forecast in zip(suite['tests'],CENTRAL,strict=True):
        manifest=read(root/t['id']/'manifest.json')
        rows.append({'test_id':t['id'],'difficulty':t['difficulty'],'central_requests':forecast,
                     'initial_prompt_characters':len(SYSTEM)+len(prompt_text(t,manifest,[],[])),
                     'central_output_tokens_per_request':OUTPUT[t['difficulty']]})
    write(HERE/'budget_inputs.json',{'method':'Character lengths of full frozen test plus losslessly compacted actual fixture and system instructions. Token lengths and request counts are forecasts, not API measurements.',
        'suite_sha256':verify_freeze()['files']['evaluation/final_test_cases_100.json'],'tests':rows})

def calculate(inputs,cfg):
    scenarios={};frame=image_tokens(*cfg['desktop_window'])
    for name,p in SCENARIOS.items():
        rows=[]
        for row in inputs['tests']:
            n=math.ceil(row['central_requests']*p['request_factor'])
            initial=math.ceil(row['initial_prompt_characters']/p['chars_per_token'])+p['protocol_tokens_per_request']
            # Full text history is retained: average input increases as actions accumulate.
            text=n*initial+p['history_tokens_per_round']*n*(n-1)//2
            imgs=n*frame
            out=n*math.ceil(row['central_output_tokens_per_request']*p['output_factor'])
            rows.append({'test_id':row['test_id'],'difficulty':row['difficulty'],'requests':n,
                         'text_input_tokens':text,'image_input_tokens':imgs,'input_tokens':text+imgs,
                         'output_tokens':out,'cost_usd':token_cost(text+imgs,out),
                         'exceeds_request_guard':n>cfg['limits'][row['difficulty']]['model_requests']})
        groups=[]
        for difficulty in OUTPUT:
            group=[r for r in rows if r['difficulty']==difficulty]
            groups.append({'difficulty':difficulty,'tests':len(group),
                           **{k:sum(r[k] for r in group) for k in ['requests','text_input_tokens','image_input_tokens','input_tokens','output_tokens','cost_usd']},
                           'request_range_per_test':[min(r['requests'] for r in group),max(r['requests'] for r in group)]})
        budgets={}
        for budget in [4,5,15]:
            spent=0;count=0;dist=Counter()
            # Small unspent reserve for the last request's max-output guard.
            # Conservative: use each test's average actual cost plus maximum guard reserve.
            for r in rows:
                guard=token_cost(math.ceil(r['input_tokens']/r['requests']),cfg['max_output_tokens_per_request'])
                if spent+r['cost_usd']+guard>budget or r['exceeds_request_guard']:break
                spent+=r['cost_usd'];count+=1;dist[r['difficulty']]+=1
            budgets[str(budget)]={'estimated_fully_executed_in_suite_order':count,'difficulty_distribution':dict(dist),
                                 'cost_of_completed_forecasts_usd':spent,
                                 'caveat':'Conditional planning only: assumes no early stop for infrastructure/API error or unresolved review; not predicted PASS count.'}
        scenarios[name]={'assumptions':p,'totals':{k:sum(r[k] for r in rows) for k in ['requests','text_input_tokens','image_input_tokens','input_tokens','output_tokens','cost_usd']},
                         'difficulty':groups,'budget_coverage':budgets,'tests_exceeding_request_guard':[r['test_id'] for r in rows if r['exceeds_request_guard']],
                         'tests':rows}
    return {'state':'ESTIMATE_ONLY_NO_PAID_RUN','suite_sha256':inputs['suite_sha256'],'model':cfg['model'],
            'pricing_usd_per_million':cfg['pricing_usd_per_million'],'screenshot_budget_pixels':cfg['desktop_window'],
            'image_tokens_per_frame':frame,'cached_tokens_assumed':0,'extra_tool_cost_modeled_usd':0,
            'extra_tool_cost_note':'Local browser, no paid hosted container/search. Official pricing lists no separate computer-action fee. Provider invoice/tax and any unlisted account-specific charges are not measured.',
            'request_count_note':'Generation requests only. One additional input-token-count endpoint request is planned before each paid generation. No such endpoint was called for this estimate.',
            'uncertainty':'Scenario range is not a confidence interval. Token estimates use measured character lengths, not an exact tokenizer. Native model compatibility, account entitlement, visual navigation and cache hits remain unmeasured.',
            'scenarios':scenarios}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--measure-local-fixtures',action='store_true');args=ap.parse_args()
    verify_freeze();suite=read(HERE/'final_test_cases_100.json');cfg=read(HERE/'optimized_config.json')
    if args.measure_local_fixtures:measure(suite)
    result=calculate(read(HERE/'budget_inputs.json'),cfg)
    write(HERE/'budget_estimate.json',result)
    for name,s in result['scenarios'].items():print(json.dumps({'scenario':name,'totals':s['totals'],'coverage':s['budget_coverage'],'request_guard_exceedances':s['tests_exceeding_request_guard']}))

if __name__=='__main__':main()
