"""Offline harness tests only: never count these as the 100 native CUA tests."""
import copy
import json
import unittest
import tempfile
from pathlib import Path
from types import SimpleNamespace
from contextlib import ExitStack
from unittest.mock import Mock
from unittest.mock import patch
import efficient_context as ctx
import run_native_cua as runner

class Guards(unittest.TestCase):
    def setUp(self):
        self.cfg=runner.read(runner.HERE/'optimized_config.json')
        self.frozen=runner.read(runner.HERE/'freeze.json')
        self.zero={'input_tokens':0,'output_tokens':0,'estimated_cost_usd':0,'reserved_unknown_usd':0}

    def test_suite_unchanged(self):
        runner.verify_freeze()
        suite=runner.read(runner.HERE/'final_test_cases_100.json')
        self.assertEqual(len(suite['tests']),100)
        self.assertEqual(suite['distribution'],{'Easy':30,'Medium':40,'Hard':20,'Expert':10})

    def test_fixture_factoring_is_lossless(self):
        fixture={'accounts':{'P':{'password':'synthetic','id':1},'Q':{'password':'synthetic','id':2}},
                 'records':{'hidden':{'id':3,'published':False}},'new_accounts':{'N':{'name':'New'}}}
        before=copy.deepcopy(fixture)
        self.assertEqual(ctx.expanded_fixture(ctx.compact_fixture(fixture)),before)
        self.assertEqual(fixture,before)

    def test_complete_task_preserved_and_only_latest_frame_sent(self):
        test={'task':'Inspect all','workflow':['one','two','three'],'pass_fail_criteria':['A','B','C']}
        actions=[{'type':'click','x':12,'y':40},{'type':'type','text':'Synthetic'}]
        outputs=[{'type':'computer_call','call_id':'call_1','actions':actions}]
        results=[{'type':'computer_call_output','call_id':'call_1','output':ctx.screenshot_output(b'new image')}]
        inp=ctx.make_input(test,{},actions,['Observed screen'],b'OLD IMAGE',outputs,results)
        payload=json.loads(inp[0]['content'][0]['text'])
        self.assertEqual(payload['frozen_test'],test)
        self.assertEqual(payload.get('prior_executed_actions',[])+inp[1]['actions'],actions)
        self.assertEqual(json.dumps(inp).count('data:image/png;base64,'),1)
        self.assertEqual(inp[1:],outputs+results)
        with self.assertRaises(ValueError):ctx.make_input(test,{},[],[],b'',outputs,[])

    def test_requests_evidence_hashes_images_not_task_text(self):
        body={'input':ctx.make_input({'task':'unchanged'},{},[],[],b'PNG')}
        record=ctx.evidence_request(body)
        self.assertNotIn('data:image/png',json.dumps(record))
        self.assertIn('unchanged',json.dumps(record))
        self.assertIn('data:image/png',json.dumps(body))

    def test_latest_text_dedup_is_exact_and_lossless(self):
        old=[{'type':'click','x':1,'y':2}];new=[{'type':'type','text':'test'}]
        output=[{'type':'computer_call','call_id':'c','actions':new},{'type':'message','content':[{'type':'output_text','text':'latest'}]}]
        returned=[{'type':'computer_call_output','call_id':'c','output':ctx.screenshot_output(b'new')}]
        inp=ctx.make_input({}, {},old+new,['earlier','latest'],b'old',output,returned)
        payload=json.loads(inp[0]['content'][0]['text'])
        self.assertEqual(payload['prior_executed_actions']+inp[1]['actions'],old+new)
        self.assertEqual(payload['prior_model_text_observations']+[inp[2]['content'][0]['text']],['earlier','latest'])
        unmatched=ctx.make_input({}, {},old,['different'],b'old',output,returned)
        self.assertEqual(json.loads(unmatched[0]['content'][0]['text'])['prior_executed_actions'],old)

    def test_fixed_strata_and_no_skipping(self):
        suite=runner.read(runner.HERE/'final_test_cases_100.json')
        ordered=runner.load_order(suite)
        self.assertEqual([t['id'] for t in ordered[:4]],['T001','T031','T071','T091'])
        self.assertEqual(len({t['id'] for t in ordered}),100)
        for start in range(0,100,10):
            self.assertEqual(dict(runner.Counter(t['difficulty'] for t in ordered[start:start+10])),{'Easy':3,'Medium':4,'Hard':2,'Expert':1})
        self.assertEqual(runner.require_next(ordered,[{'test_id':'T001'}]),'T031')
        with self.assertRaises(RuntimeError):runner.require_next(ordered,[],'T091')
        with self.assertRaises(RuntimeError):runner.require_next(ordered,[{'test_id':'T031'}])

    def test_ten_dollar_stop_includes_unknown_charges(self):
        ledger={**self.zero,'estimated_cost_usd':9.97,'reserved_unknown_usd':.01}
        with self.assertRaises(ctx.TotalBudgetExhausted):ctx.reserve_request(3000,1024,self.zero,self.cfg['limits']['Easy'],ledger,10)

    def test_pricing_and_image_math(self):
        self.assertAlmostEqual(ctx.token_cost(1279839,12025),3.3799725)
        self.assertEqual(ctx.image_tokens(1280,800),1200)
        self.assertEqual(ctx.image_tokens(1280,880),1344)
        self.assertAlmostEqual(ctx.token_cost(1000000,0,1000000),.25)
        with self.assertRaises(ValueError):ctx.token_cost(1,1,2)

    def test_budget_reserves_maximum_output(self):
        limit=self.cfg['limits']['Easy']
        amount=ctx.reserve_request(3000,1024,self.zero,limit,self.zero,5)
        self.assertAlmostEqual(amount,.02286)
        ledger={**self.zero,'estimated_cost_usd':4.98}
        with self.assertRaises(RuntimeError):ctx.reserve_request(3000,1024,self.zero,limit,ledger,5)
        ledger={**self.zero,'reserved_unknown_usd':4.99}
        with self.assertRaises(RuntimeError):ctx.reserve_request(3000,1024,self.zero,limit,ledger,5)

    def test_old_or_excessive_approval_is_rejected(self):
        approval={'approved':True,'model':self.cfg['model'],'suite_sha256':self.frozen['files']['evaluation/final_test_cases_100.json'],
                  'execution_fingerprint':runner.execution_fingerprint(),'budget_usd':5,
                  'approved_at':'UNIT TEST ONLY','user_approval_text':'UNIT TEST ONLY; never saved'}
        runner.validate_approval(approval,self.frozen,self.cfg)
        runner.validate_approval({**approval,'budget_usd':10},self.frozen,self.cfg)
        for change in [{'budget_usd':120},{'budget_usd':15},{'budget_usd':0},{'approved':False},{'execution_fingerprint':'old'}]:
            with self.assertRaises(RuntimeError):runner.validate_approval({**approval,**change},self.frozen,self.cfg)

    def test_missing_approval_prevents_any_api(self):
        self.assertFalse((runner.HERE/'approval.local.json').exists(),'This offline check must precede approval')
        with patch.object(runner,'api',side_effect=AssertionError('NO NETWORK')),patch('sys.argv',['runner','--test','T001']):
            with self.assertRaises(SystemExit) as stop:runner.main()
            self.assertIn('no paid calls made',str(stop.exception))

    def rehearsal(self,timeout=False,exhausted=False):
        """Fake transport/native motor exercises accounting; makes zero real calls."""
        class Browser:
            def __init__(self,*args,**kwargs):pass
            def screenshot(self):return b'OFFLINE FAKE IMAGE'
            def execute(self,action):pass
            def close(self):pass
        def setup(args,**kwargs):
            folder=Path(args[-1]);folder.mkdir(parents=True)
            runner.write(folder/'manifest.json',{})
            return SimpleNamespace(returncode=0)
        responses=[]
        def transport(path,body,**kwargs):
            if path=='responses/input_tokens':return {'input_tokens':3000}
            responses.append(copy.deepcopy(body))
            # The reservation must already be durable before dispatch.
            stored=runner.read(ledger)
            self.assertGreater(stored['reserved_unknown_usd'],0)
            if timeout:raise TimeoutError('Offline simulated timeout')
            n=len(responses)
            output=([{'type':'computer_call','call_id':f'call_{n}','actions':[{'type':'click','x':1,'y':2}]}]
                    if n<=2 else [{'type':'message','role':'assistant','content':[{'type':'output_text','text':'Observation only'}]}])
            return {'id':f'offline_{n}','status':'completed','output':output,
                    'usage':{'input_tokens':3000,'output_tokens':40,'input_tokens_details':{'cached_tokens':0}}}
        with tempfile.TemporaryDirectory(prefix='harness-unit-') as tmp,ExitStack() as stack:
            root=Path(tmp);ledger=root/'ledger.json'
            if exhausted:runner.write(ledger,{'attempts':[],'estimated_cost_usd':9.99,'reserved_unknown_usd':0})
            stack.enter_context(patch.object(runner,'HERE',root))
            stack.enter_context(patch.object(runner,'execution_fingerprint',return_value='OFFLINE'))
            stack.enter_context(patch.object(runner.subprocess,'run',side_effect=setup))
            stack.enter_context(patch.object(runner,'start_server',return_value=(Mock(),Mock())))
            stack.enter_context(patch.object(runner,'snapshot'))
            stack.enter_context(patch.object(runner,'api',side_effect=transport))
            stack.enter_context(patch.dict('sys.modules',{'native_driver':SimpleNamespace(NativeBrowser=Browser)}))
            result=runner.run_one({'id':'T001','difficulty':'Easy','expected_workflow':['unchanged']},self.cfg,{'budget_usd':10 if exhausted else 5},ledger)
            persisted=runner.read(ledger)
            if exhausted:
                self.assertEqual(len(responses),0)
                self.assertEqual(result['status'],'NOT_RUN')
                self.assertEqual(persisted['stop_reason'],'TOTAL_BUDGET_EXHAUSTED')
                self.assertAlmostEqual(persisted['estimated_cost_usd'],9.99)
                return
            if timeout:
                self.assertEqual(len(responses),1)
                self.assertGreater(persisted['reserved_unknown_usd'],0)
                self.assertGreater(result['reserved_unknown_usd'],0)
            else:
                self.assertEqual(len(responses),3)
                self.assertAlmostEqual(persisted['estimated_cost_usd'],ctx.token_cost(9000,120))
                self.assertAlmostEqual(persisted['reserved_unknown_usd'],0)
                third=responses[2]['input']
                self.assertEqual(json.dumps(third).count('data:image/png;base64,'),1)
                self.assertEqual([x['call_id'] for x in third if x.get('type')=='computer_call'],['call_2'])
                self.assertEqual(result['failure_reason'],'PENDING_INDEPENDENT_REVIEW')
            self.assertEqual(result['status'],'ERROR')

    def test_native_loop_accounting_and_pairing_with_fake_transport(self):self.rehearsal()
    def test_ambiguous_charge_is_reserved_without_retry(self):self.rehearsal(timeout=True)
    def test_exhausted_run_dispatches_no_generation(self):self.rehearsal(exhausted=True)

if __name__=='__main__':unittest.main()
