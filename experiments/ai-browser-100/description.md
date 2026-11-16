# AI browser evaluation request

The owner requested approximately 100 AI-designed tasks, from simple to difficult, executed by a computer-use agent, with the written tests and final pass rate.

## Execution design

- Target: the deployed CareConnect 3.0 site at https://careconnect-demo-rc0t.onrender.com.
- Three delegated browser agents own 35 authentication/navigation tasks, 35 clinical workflow tasks, and 30 cross-role tasks.
- Available capability: real Edge browser automation via Playwright. No native vision-only desktop computer-use tool is available. This distinction was disclosed before execution.
- All scored actions use browser UI interaction, visible page assertions, browser navigation or downloaded files. No direct API/database shortcuts for test outcomes.
- Application code is frozen during the evaluation. Failed product behavior is reported, not fixed to improve the score.
- New synthetic identities and labelled records isolate state-changing tasks from ordinary shared demo workflows. No shared demo passwords are changed.
- Each task has steps, an expected outcome, difficulty, and evidence. A dependency failure blocks subsequent tasks rather than treating them as passed.
- Overall pass rate is passed / 100. Executed-task rate is passed / (passed + failed). Both are reported, with blocked counts.
- Test-only locator/fixture corrections must be documented; first-attempt artifacts remain available. They are not application repairs.

## Files

- `TASKS.md`: full English task catalog, generated from the suite definitions.
- `REPORT.md`, `report.json`, `report.html`: detailed results and evidence links.
- Timestamped group folders: per-task screenshots, failed-page text and raw outcomes.
- `AGENT-NOTES.md`: execution caveats, fixture corrections and defect interpretation.
- `frontend/ai-tests/`: runnable browser task suites, harness and report generator.

## Reproduction

Install frontend dependencies as documented in the project README. Set `CC_BROWSER_BIN` to a compatible Chromium/Edge executable and `CC_AI_URL` to the test deployment. `CC_AI_RUN` identifies fixture names where used; create a fresh test data set when repeating stateful scenarios.

Run each of `node frontend/ai-tests/auth-navigation.cjs`, `node frontend/ai-tests/clinical.cjs`, and `node frontend/ai-tests/crossrole.cjs`. Then run `node frontend/ai-tests/report.cjs` to generate reports only when all 100 tasks have results. Use a synthetic-data deployment. These suites intentionally create accounts and workflow records.
