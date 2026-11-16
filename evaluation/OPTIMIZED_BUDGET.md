# GPT-5.4 native CUA — budget review, not execution

**No paid OpenAI request has been made. New explicit approval is required.** The current research target is **$5**, with a **$10 maximum**. These planning ceilings do not authorize any paid run. $15 figures are feasibility analysis only. No approval file has been created.

All 100 frozen tests remain unchanged: Easy 30, Medium 40, Hard 20, Expert 10. The original difficulty, workflow, expected result and every criterion remain authoritative. The application and specification are unchanged. The frozen `config.json` preserves the former plan; the executor now loads the separate [optimized configuration](optimized_config.json).

## Recommendation and uncertainty

The current offline forecast is **$15.60 central**, with an **optimistic $9.45 / cautious $29.04** scenario range for executing all 100 unchanged tasks. These are explicit planning assumptions, **not measured CUA performance, a quote, or a confidence interval**. There has been no paid pilot. Request counts were estimated per task from its workflow; text tokens use measured prompt character lengths and a sensitivity range, not an exact tokenizer.

It is not responsible to promise all 100 within $10; only the optimistic scenario fits. Nor can this preparation establish reliable completion within $15: the central estimate already exceeds it, and long cross-role tasks have substantial navigation uncertainty. A favorable run or actual cache hits might bring the total below $15; that possibility is not a commitment. Tests will not be simplified to force a lower number.

## Why CareFlow cost $3.38

The comparison is now based on the original [CareFlow results](https://github.com/KateK77/careflow-ehr/blob/3ae015ec5155ccbb9ca44766f0d13e2a3a8d2070/docs/testing/cua100-v1/results.json), [benchmark](https://github.com/KateK77/careflow-ehr/blob/3ae015ec5155ccbb9ca44766f0d13e2a3a8d2070/tools/cua/benchmark.py), and [native driver](https://github.com/KateK77/careflow-ehr/blob/3ae015ec5155ccbb9ca44766f0d13e2a3a8d2070/tools/cua/driver.py), pinned to commit `3ae015ec5155ccbb9ca44766f0d13e2a3a8d2070`. Extracted figures are in [careflow_comparison.json](careflow_comparison.json).

| Dimension | CareFlow recorded run | Former CareConnect proposal | Optimized CareConnect forecast |
| --- | --- | --- | --- |
| Evidence | Actual 100 native tasks; 85 PASS / 15 FAIL | No paid run; rough planning range | No paid run; per-task scenarios |
| Task shape | First 70 are entry/read/authorization probes; remaining 30 validation/write workflows | More complete patient/staff workflows | Same frozen 100 workflows, unchanged |
| Login | Harness preauthenticates non-login tasks through UI | Model performs required login/role changes | Required login/role changes remain model-driven |
| Generation requests | 336; 3.36/test | Loose guards of 30/50/80/120 per difficulty | Central 1,454; 14.54/test |
| Input tokens | 1,279,839 | Assumed 10–35 million | Central 5,351,415, including images |
| Output tokens | 12,025; 35.8/request | Assumed 0.5–1.5 million | Central 148,200; about 102/request |
| Model | `gpt-5.4` alias | `gpt-5.4-2026-03-05` | Same GPT-5.4 snapshot, reasoning `none`, low verbosity |
| Screenshot sizing | 1280×800 viewport, original detail | Actual launch size not reliably enforced | 1280×880 whole window; native pixels; narrow CSS viewport 390×844 |
| Context | Shorter tasks and bounded native loop | Every previous screenshot replayed each round | Complete task and action text, only latest native call/output image pair |
| Output limit | 1,024/request | 3,000/request | 1,024/request; stop on incomplete response, no paid retry |
| Token-rate cost | Reported $3.379979 | $32.50–110 | $15.6015375 central |

The old $32.50–110 was simply `10–35M input × $2.50 + 0.5–1.5M output × $15`. It was too coarse to compare directly with an observed $3.38 run and should not have been presented as a calibrated estimate. It was not evidence that native CUA has a large flat tool fee.

CareFlow aggregate tokens recompute to **$3.3799725**; the reported $3.379979 differs by less than $0.00001, consistent with summing rounded task costs. Neither is a provider invoice. CareFlow's Playwright-backed motor executes native model actions and supports verification; this does not make its native requests fictitious.

For a concrete complexity comparison, CareConnect T092 includes creating an unpublished result, checking patient absence, publishing, following a notification and PDF, correcting and rechecking, then withdrawing and testing saved links. T099 registers and approves **four** staff roles and executes a role-specific action for each. Those cannot be replaced with one prepared-record button click. See the [unchanged suite](FINAL_TEST_CASES.md).

## Optimizations implemented

- Keep the full frozen test in every model input. Factor repeated fixture fields losslessly and use compact JSON; no grading criterion is summarized away.
- Retain literal executed actions and model observations. Remove an exactly matching latest-turn suffix from the older text history because the native response already carries it; unmatched text is retained. This saves input text, not model requests. Remove old raster images from subsequent requests, retaining the latest complete native call/output pairing. Raw calls, intermediate screenshots and traces remain in private evidence for review.
- Reuse the final action screenshot as the batch response instead of capturing it again. The old per-action local screenshots were not all API inputs; **replaying old batch screenshots** was the principal image-token problem.
- Permit the native model to batch already-understood actions; require observation after navigation or a state change. The harness does not prescribe clicks or solve tasks with DOM/SQL/Playwright.
- Use native-pixel, original-detail screenshots with controlled window dimensions. Do not shrink text until unreadable. Narrow-screen setup uses CDP only to establish/measure viewport size, never to inspect DOM or choose task actions.
- Use GPT-5.4 standard service, reasoning `none`, brief prose, and a 1,024-output-token cap. No model substitution, paid judge, automatic retry, or retry after truncation/timeout. Lower output/reasoning settings may increase navigation errors; their effect is unmeasured and must be reported honestly.
- Reserve counted input plus maximum output cost before every paid generation. Persist the reservation before dispatch; retain it on ambiguous failure. Stop at the approved global limit, even if tests remain unexecuted. Old approvals do not match the new executor fingerprint.

### Limits are stop guards, not reduced tests

| Difficulty | Requests/test maximum | Actions/test maximum | Runtime/test | Input/output token guards | Per-test dollar guard |
| --- | ---: | ---: | --- | --- | ---: |
| Easy | 22 | 80 | 10 minutes | 96k / 8k | $0.30 |
| Medium | 30 | 140 | 15 minutes | 192k / 16k | $0.60 |
| Hard | 45 | 220 | 25 minutes | 320k / 28k | $1.00 |
| Expert | 95 | 350 | 40 minutes | 560k / 50k | $2.50 |

Action and runtime ceilings are unchanged from the original plan. Request limits allow complex exceptions such as T002's eleven-area navigation and T099's four-role onboarding. The **global $10 maximum overrides all per-test allowances**. Hitting a guard never lowers a PASS criterion: a partially executed task is incomplete/ERROR; a budget-stopped task with zero generations remains NOT_RUN. The cautious all-suite scenario could exceed other per-test guards even when its request count fits.

## Forecast by difficulty

Standard rates: **$2.50/M uncached input, $0.25/M cached input, $15/M output**, with no assumed cache discount. These rates and GPT-5.4 support are documented in [OpenAI pricing](https://developers.openai.com/api/docs/pricing) and the [model reference](https://developers.openai.com/api/docs/models/gpt-5.4). All planned requests are far below the long-context pricing boundary.

| Difficulty | Tests | Central requests/test range | Central requests total | Central input tokens | Central output tokens | Central cost |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Easy | 30 | 4–15 | 192 | 607,177 | 11,520 | $1.69 |
| Medium | 40 | 8–20 | 509 | 1,721,072 | 45,810 | $4.99 |
| Hard | 20 | 10–22 | 351 | 1,243,832 | 38,610 | $3.69 |
| Expert | 10 | 28–65 | 402 | 1,779,334 | 52,260 | $5.23 |
| **Total** | **100** | | **1,454** | **5,351,415** | **148,200** | **$15.60** |

Central breakdown: text input **$8.49**, screenshot input **$4.89**, output **$2.22**. Images are included in the 5.35M input tokens, not charged twice. A 1280×880 original-detail GPT-5.4 image is estimated at `ceil(1280/32) × ceil(880/32) × 1.2 = 1,344` tokens, about **$0.00336** uncached. A 1280×800 frame is 1,200 tokens, about $0.003. This follows the current [image-token documentation](https://developers.openai.com/api/docs/guides/images-vision); the old “85 tokens for low detail” rule must not be assumed for this GPT-5.4 configuration.

| Scenario | Generation requests | Input tokens | Output tokens | Token cost for all 100 |
| --- | ---: | ---: | ---: | ---: |
| Optimistic | 1,062 | 3,293,980 | 81,149 | $9.45 |
| Central | 1,454 | 5,351,415 | 148,200 | $15.60 |
| Cautious | 2,068 | 9,722,025 | 315,660 | $29.04 |

The forecasts do not include automatic paid retries. They allow different amounts of navigation/observation within a single attempt. Reproduce every row with `python evaluation/estimate_budget.py`; [budget_inputs.json](budget_inputs.json) contains measured character lengths and per-test request assumptions, and [budget_estimate.json](budget_estimate.json) contains all scenario arithmetic. This forecast is separate from `final_results_100.json`.

Text-token sensitivity uses 4.5 / 4 / 3.5 characters per token; protocol overhead 120 / 180 / 250 tokens per request; retained text history grows by 45 / 65 / 95 tokens per round. Central output assumptions are 60 / 90 / 110 / 130 tokens per request by difficulty. Those assumptions are deliberately disclosed because no exact API count or paid pilot is authorized. More screenshots per native response, longer text, failed navigation or environment interruptions can increase cost or stop execution.

### Possible extra costs

Modeled extra tool/hosting expense is **$0**: computer actions execute on the existing local machine, with no OpenAI hosted container, web search, file search or paid external browser service. The current official pricing page lists no separate `computer` action fee; built-in tool tokens are charged at model rates. This is a planning assumption, not verification of the account's eventual invoice. Tax, currency conversion and any account-specific charge are outside the token estimate and cannot be guaranteed by a local token guard.

One additional `/responses/input_tokens` request is planned before each generation to make the runtime reservation accurate. It does not generate a model response; no separate token-count price is listed in the cited pricing page. **Neither counting nor generation endpoints were called in this offline review.** The [token-counting guide](https://developers.openai.com/api/docs/guides/token-counting) explains why local character/image calculations are estimates. Interactive calls use standard pricing, not an assumed Batch discount. No cache hit is counted in advance; actual cached usage will be recorded if it occurs.

## Fixed stratified order and coverage

The precommitted [execution_order.json](execution_order.json) contains all 100 original IDs exactly once. Every 10-task block follows **Easy, Medium, Hard, Expert, Medium, Easy, Hard, Medium, Easy, Medium**. Within each difficulty, IDs ascend. This gives 3/4/2/1 tasks per block, matching the full 30/40/20/10 distribution. First four: **T001, T031, T071, T091**. The [complete readable order](EXECUTION_ORDER.md) is fixed before any paid call.

No results, cheap tasks, observed success rates or remaining balance may change this order. Both `--all` and single-task continuation enforce its prefix. No skipped hard task, automatic paid retry or replacement test is allowed. The order and loader are included in the approval fingerprint. Each test retains its independent fresh fixture and complete original workflow.

| Budget | Central complete attempts | Easy / 30 | Medium / 40 | Hard / 20 | Expert / 10 | Optimistic / cautious totals |
| --- | ---: | --- | --- | --- | --- | --- |
| $5 target | 32 | 10 (33.3%) | 13 (32.5%) | 6 (30%) | 3 (30%) | 53 / 14 |
| $10 maximum | 64 | 19 (63.3%) | 25 (62.5%) | 13 (65%) | 7 (70%) | 100 / 33 |

These are projected fully executed attempts, **not PASS predictions**. Forecasts assume no early API/desktop fault and timely independent review. Actual completion can be lower. All scenario distributions are in [budget_estimate.json](budget_estimate.json). Coverage follows the fixed order, reserves one request's maximum output headroom, and never selects a cheaper later task to fill the remaining balance.

At $10, optimistic coverage is 30/40/20/10; cautious coverage is 10/13/7/3. At $5, optimistic coverage is 16/21/11/5; cautious coverage is 4/5/3/2. The first four planned attempts cover all difficulty levels, conditional on progressing that far. The order is proportional, not a claim of random or statistically representative sampling.

The full-suite scenario totals describe hypothetical full workflows. In the cautious scenario, T099 also exceeds its 560k input-token guard; it would stop incomplete rather than receive a relaxed criterion. No scenario exceeds the request-count guards. Action/time requirements cannot be verified without a real run.

### Audit of the 1,454 generation requests

The 1,454 is the sum of pre-run task forecasts, not 1,454 observed requests with redundant calls that can be identified empirically. The executor has no extra paid planning, grading, login-helper or retry request. Existing safe batching of known visible actions is already permitted. Each generated native turn must be followed by its required observation; unchanged pixels alone are not grounds for skipping a model turn or declaring success. The terminal observation/verification remains required.

Historical raster frames are absent from later API inputs. The newest native call/output pair remains; if the provider emits multiple calls, each matching output is retained rather than violating the protocol. Intermediate local screenshots are evidence, not repeated API inputs. The final action frame is reused for its batch result. The new exact-suffix text deduplication removes repeated latest actions/observations without deleting history. Unit tests check the full task, reconstruction of action/text history, call IDs and one-image normal-turn behavior.

No additional deterministic reduction in generation count was established, so the central **1,454** forecast remains. Text-dedup savings are deliberately not credited to the heuristic cost forecast before real token measurements. Initial fixture character counts remain valid. One additional token-count endpoint call per generation remains necessary for the spend reservation; it is not a paid model generation. There were zero such calls during this review.

### Budget stop and reporting

The $5 target is a planning milestone, not authorization. A later explicit approval must state the allowed ceiling (at most $10); approving $5 does not permit spending $10. Before each paid generation, reserve counted uncached input plus maximum output against that actual approved ceiling, including any unknown charge reservation. Stop before a request that cannot fit; never auto-retry a timeout.

Persist `TOTAL_BUDGET_EXHAUSTED` in the ledger. A task with no generation remains NOT_RUN; a task interrupted after paid work is ERROR/incomplete, not PASS or an application FAIL. All remaining unstarted tasks are NOT_RUN. The fixed order is not reshuffled after exhaustion. A stopped run cannot automatically resume. Preserve raw calls, screenshots, action trace, per-task tokens/cost and independently reviewed criteria; no pooled success score substitutes for individual results.

## Evidence, preflight and publication

See [offline fixture checks](logs/offline-fixture-preflight.json), [browser check](logs/infrastructure-check.json), and [local configuration preflight](preflight.json). Harness unit tests exercise approval rejection, lossless task context, native call pairing, durable spend reservations and timeout-without-retry through fake transports; they are **not native CUA task results**.

Current free validation: **14/14 harness checks passed; frozen suite and application unchanged.** Existing 100/100 isolated database checks are retained because fixture code is unchanged; they were not rerun in this budget-only revision. In the new browser preflight the desktop frame passed at 1280×880, but the narrow window failed to acquire a verifiable foreground window. This is an infrastructure failure, not a portal FAIL. **Readiness is blocked until a fresh successful desktop/narrow check matches the final executor fingerprint.** No paid call was made or retried.

The [prior successful browser check](logs/infrastructure-check-prior-success.json) is preserved as historical evidence, not substituted for the current failed check. It measured a 516×950 narrow frame, requested 390×844 CSS viewport and 375-pixel content width excluding a 15-pixel scrollbar. The forecast still conservatively uses the larger desktop image cost for both narrow tasks. See the [current free-validation record](logs/stratified-plan-validation.json).

Formal execution remains NOT_STARTED. Account entitlement, live native protocol compatibility and real model navigation remain unverified. Before paid execution, resolve any browser-preflight error, obtain a new explicit approval matching the frozen suite and executor fingerprint, and recheck local readiness. No approval file is supplied by this change.

Future attempts preserve raw native responses and response/call IDs, request manifests with screenshot hashes, screenshots per action, action JSONL, usage/cache/cost, timing, independent state/file evidence and criterion-by-criterion review. Public copies must be redacted before GitHub upload; private originals remain intact. The eventual report will distinguish PASS, FAIL, BLOCKED, ERROR and NOT_RUN and will not reuse the earlier Playwright score.
