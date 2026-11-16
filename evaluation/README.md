# Final V3 evaluation

**Status: NOT_STARTED. Paid generation requests: 0. New explicit approval required.**

Offline readiness: database prerequisites **100/100**, harness checks **10/10**, and both desktop/narrow browser preflights passed. The narrow viewport remains active after setup. These are infrastructure checks, not portal test scores; live OpenAI compatibility still requires a separately approved first native attempt.

Current budget review: target **$4**, maximum **$5**; all 100 original tests unchanged. The offline central forecast is **$15.60** for the full suite, so $5 completion is not promised. [Read the comparison, per-difficulty estimates and coverage projections](OPTIMIZED_BUDGET.md).

This is the user's replacement evaluation protocol: exactly100 specification-derived tests executed by native OpenAI computer-use, not the previous Playwright scripts.

- [Frozen test suite](FINAL_TEST_CASES.md) / [JSON](final_test_cases_100.json)
- [Specification identification](PROVENANCE.md)
- [Independent synthetic prerequisites](FIXTURES.md)
- [Model, limits, estimate and approval](BUDGET_AND_EXECUTION.md)
- [Current report](FINAL_EVALUATION_REPORT.md) / [JSON](final_results_100.json) / [CSV](summary.csv)

## Preparation and execution

Use the existing project Python environment with backend requirements and `pyautogui==0.9.54` installed. Build frontend from the frozen application (`node node_modules/vite/bin/vite.js build` with cwd `frontend`). On this workstation, the existing Python environment is `../../work/venv/Scripts/python.exe` relative to the repository. `python evaluation/check_infrastructure.py` performs a no-cost localhost/browser/screenshot check; it executes and scores no test. The network sandbox must allow localhost connections.

1. `python evaluation/build_suite.py` is authoring only; refuses after freeze exists.
2. `python evaluation/freeze_suite.py` saves hashes once. Do not regenerate expectations after seeing results.
3. `python evaluation/run_native_cua.py --preflight` checks local configuration without a paid request.
4. `python evaluation/offline_fixture_preflight.py` checks all 100 isolated prerequisite databases; `python -m unittest discover -s evaluation -p test_execution_guards.py -v` tests the harness with fake transports. Neither executes native CUA tasks. Model metadata and live compatibility remain unverified in this offline review.
5. After explicit user approval, record model/suite hash/execution fingerprint/budget/approval timestamp/approval text in ignored `evaluation/approval.local.json`. Do not create this from inferred consent or mere API-key availability.
6. `python evaluation/run_native_cua.py --test T001` starts one native attempt. `--all` progresses in suite order, stopping for review or errors; it never silently retries an existing attempt.
7. Inspect private screenshots, action logs, read-only before/after state and downloaded PDFs. Review every frozen criterion. Publish redacted evidence to `screenshots/` and `logs/`.
8. Record independent review decisions in ignored `review.local.json`, keyed by test ID, with `status`, `actual_outcome`, `failure_reason`, `evidence` relative paths and one `criteria` item per frozen criterion (`met`, evidence/reason, and `application_failure` where relevant). PASS requires every criterion met. FAIL requires a demonstrated application failure.
9. `python evaluation/generate_report.py` writes the requested100-row artifacts. It never treats agent self-report as PASS.

Raw screenshots can contain test passwords when testing visibility controls and reset tokens in address bars. They are private until reviewed. The browser adapter refuses to operate when a different application owns the foreground window. Use a dedicated uninterrupted desktop session. Native model availability/protocol and the full UI execution loop are not considered verified until a user-approved native attempt succeeds; local setup checks are not scored tests.

The specification/application remain unchanged. This branch must not be merged into main without approval.

## Budget artifacts

- [Original 100 tasks](FINAL_TEST_CASES.md)
- [Optimized budget and CareFlow comparison](OPTIMIZED_BUDGET.md)
- [Machine-readable projections](budget_estimate.json) / [reproducible inputs](budget_inputs.json)
- [100 isolated database preflight checks](logs/offline-fixture-preflight.json)
- [Latest browser preflight](logs/infrastructure-check.json)
- [Optimized runtime configuration](optimized_config.json)

A preflight or unit-test success is not a portal PASS. Real native calls, screenshots, traces and independent scores will be published after a separately approved run and evidence redaction.
