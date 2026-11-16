# Native CUA execution plan — approval required

This plan does not authorize API expenditure. No paid model call has been made during preparation.

## Model and protocol

Proposed model: `gpt-5.4-2026-03-05`, documented as supporting the native `computer` tool on the Responses API. Use model-issued `computer_call.actions` for screenshot-based clicks, typing, scrolling, keypresses and dragging. Return native `computer_call_output` screenshots. Do not request generated Playwright scripts or use DOM selectors as task execution.

The local adapter uses native Windows mouse/keyboard input (PyAutoGUI) and screenshots of the dedicated browser window. It is an action executor, not a scripted test solver. The model receives the frozen task plus synthetic fixture information and screenshots; it must choose every test action. Playwright is not the solver. A visible dedicated browser window is necessary during paid execution; do not use the same desktop concurrently. A foreground-window guard stops rather than operating on another application.

Official sources checked during preparation:

- [Native computer-use protocol](https://developers.openai.com/api/docs/guides/tools-computer-use)
- [GPT-5.4 supported tools and pricing](https://developers.openai.com/api/docs/models/gpt-5.4)
- [Input-token counting endpoint](https://developers.openai.com/api/docs/guides/token-counting)
- [API pricing](https://developers.openai.com/api/docs/pricing)

Documentation confirms model/tool compatibility, **not this account's model entitlement**. An API key is required; after local configuration, a metadata-only model availability request can verify access. A paid first native call is permitted only after explicit budget approval and remains part of the recorded attempt, with no invisible retry. If the selected snapshot is unavailable, stop and propose a documented compatible model; never silently switch.

## Cost estimate (USD)

Standard model rate used for planning: input$2.50/million, output$15/million; cached input$0.25/million, but estimate assumes no cache discount. Image inputs contribute input tokens. No paid hosted computer/container is used; the browser runs locally.

Illustrative100-test total:10–35million cumulative input tokens plus0.5–1.5million output tokens gives **$32.50–$110.00**. This is a planning range, not observed usage or a completion guarantee. Multi-turn context is counted again as billed; the estimate is not just the number of screenshot files.

**Proposed total ceiling:$120.** Difficulty-specific token budgets sum to28.5million input and2.85million output tokens, or$114 without cache savings. Remaining headroom does not grant permission for unrecorded retries or unrelated calls. Limits may leave complex tests ERROR/NOT_RUN rather than complete the whole suite.

| Difficulty | Tests | Requests/test | Native actions/test | Cumulative input/output tokens/test | Runtime/test | Cost guard/test |
| --- | ---: | ---: | ---: | --- | --- | ---: |
| Easy |30|30|80|150k /15k|10min|$0.60|
| Medium |40|50|140|250k /25k|15min|$1.00|
| Hard |20|80|220|400k /40k|25min|$1.60|
| Expert |10|120|350|600k /60k|40min|$2.40|

Before each generation, count input tokens using `/responses/input_tokens`, reserve the counted input plus the configured maximum output cost, and refuse calls that exceed remaining per-test or global allowance. Count each model response's reported usage. Stop on timeout/ambiguous billing; do not retry a request whose charge/outcome is unknown. Monetary figures computed from tokens are **estimates** until reconciled with the provider bill. Local guards are not a replacement for project billing controls.

## Isolation and scoring

1. Verify frozen hashes and unchanged application tree.
2. Create new synthetic per-test DB and fresh browser profile; reset before each task, never mutate shared demo data.
3. Let native CUA complete task within limits, recording actions/screenshots/timing/usage. No silent retries.
4. Independently review every frozen criterion using evidence and read-only state/file inspection. Agent claims are not final scores.
5. Record PASS/FAIL/BLOCKED/ERROR/NOT_RUN. Navigation mistakes and infrastructure faults are not application failures.
6. Primary rate is PASS/100. Validly evaluated rate is PASS/(PASS+FAIL), undefined when denominator is zero. Also report per-difficulty/category rates with all scheduled tests in each denominator.
7. Review/redact secrets before committing evidence; publish only to evaluation branch. Do not merge main.

## Key configuration

Provide `OPENAI_API_KEY` through the operating system's user environment-variable interface, then restart Codex so the process inherits it (the runner can also read the named user variable directly on Windows). Do not paste the key into chat, a tracked file or a command containing its literal value. The runner does not read Codex login tokens and does not treat a ChatGPT subscription as API authorization.

An ignored `approval.local.json` is created only after explicit user approval of the concrete budget. It records approved model, suite hash, dollar ceiling, timestamp and the user's approval text; it never contains the API key.
