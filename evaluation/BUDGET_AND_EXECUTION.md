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

## Current budget review (supersedes the former $120 proposal)

Target $5; maximum acceptable ceiling $10. **No paid run is authorized.** The $15 feasibility question is not approval for $15. Full comparison, assumptions, per-difficulty forecasts and coverage estimates are in [OPTIMIZED_BUDGET.md](OPTIMIZED_BUDGET.md).

The central offline estimate is $15.60 for all 100 unchanged tasks (optimistic $9.45; cautious $29.04). This is not observed native performance. At $5/$10, central forecasts cover 32/64 complete attempts in the precommitted stratified order, conditional on no early infrastructure/API stop. See [execution order](EXECUTION_ORDER.md); all four difficulties appear in the first four tasks. Completion and PASS are different measurements.

The frozen `config.json` records the old plan and is unchanged. The runner loads `optimized_config.json`; approval must match the model, frozen suite hash and **execution fingerprint (including the fixed order)**, include an explicit user statement and timestamp, and specify at most $10. Historical approval cannot activate this executor. No approval file exists.

Before each approved generation, count input tokens and reserve uncached input plus maximum output cost. Persist the reservation before dispatch. Retain unresolved reservations on timeout/unknown usage and stop without retry. Record reported input, cached input and output usage separately. The local ledger estimates token charges; provider invoice/taxes are not available here.

The optimized protocol preserves every frozen requirement and all literal action history, while sending only the latest native call/output screenshot pair. All raw screenshots remain private review evidence. Local offline checks never invoke the provider endpoints and never score the 100 tasks.

Current free validation: 14/14 harness checks passed; frozen artifacts unchanged. Latest desktop browser check passed, but narrow-window foreground acquisition failed. Paid readiness is blocked until a new successful browser preflight matches the final fingerprint. See [validation](logs/stratified-plan-validation.json).

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

An ignored `approval.local.json` is created only after explicit user approval of the concrete budget. It records approved model, suite hash, executor fingerprint, dollar ceiling, timestamp and the user's approval text; it never contains the API key.
