# Interpretation and execution notes

## Result meaning

The evaluation contains 100 scored task IDs: 23 simple, 47 medium, and 30 hard. After documented test-harness corrections, **99 passed, 1 failed, and 0 remained blocked**. These are functional results for the specified scenarios, not a claim that the entire application is 99% correct or that security is fully verified.

The first scripted attempts produced **69 passed, 9 failed checks, and 22 blocked: 69% overall**. The original screenshots and outcomes have not been overwritten. Several checks failed because of test implementation assumptions: an implicit 5-second assertion timeout, ambiguous text selectors, reading a URL before asynchronous navigation, missing required questionnaire setup, and a browser-history setup that went back to a blank tab. Corrections changed test code only. The application remained at deployment commit `bc2dea78f0e9715b96c0cb4587a8d0112b9152f4` throughout the evaluation.

The final 99% is a **corrected functional-test pass rate**, not first-attempt autonomous-agent performance. Full corrected runs and explicitly identified focused retests are combined once per task ID. `report.json` records exact evidence provenance and all raw attempt counts. Two clinical tasks were refined before the corrected run to avoid duplicating another group's registration/missing-record cases; both versions remain documented.

## Confirmed limitation: A030

**Public password recovery cannot be completed.**

1. Open the live sign-in page and choose **Forgot password?**.
2. Enter a registered synthetic account email.
3. Click **Send reset link**.

Expected: the request is accepted and the user can proceed with password recovery.

Observed: **Password recovery is not configured. Please contact support.** No recovery workflow can be completed on this deployment. This is an already known missing production configuration, still counted as a failed user task. The public page describes sending a link even though no delivery service is configured. Follow-up work would require configuring a delivery provider and testing the delivered link; no such implementation was performed during this assessment.

[Failure screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A030.png)

## Agent-specific notes

- [Authentication/navigation: 34/35](auth-navigation-notes.md)
- [Clinical workflows: 35/35](clinical-test-corrections.md)
- [Cross-role workflows: 30/30](crossrole-notes.md)

## Limits and data footprint

- The agents used Playwright to operate real Edge browser contexts, with semantic DOM selectors and downloaded-file checks. This was **not** a screenshot-only desktop computer-use benchmark, a human usability study, penetration test, or load test.
- No API/database calls were used to establish passing test outcomes. Source inspection helped identify controls and distinguish script mistakes from observed application behavior.
- The agents created clearly labelled synthetic accounts and workflow records. They remain on the shared demonstration service to preserve reproducibility and evidence; existing shared demo passwords were not changed.
- Changed passwords, contact settings and preferences belonged only to synthetic accounts created for this evaluation.
- There was light overlap between agents. Some login requests exceeded the initial 5-second assertion limit; corrected tests allowed up to 20 seconds. This does not establish a latency guarantee or rule out performance issues.
- Coverage includes selected desktop/mobile viewports in one browser family. A passing UI role check does not prove all backend authorization combinations are secure.
- Real medical, email, payment and hospital integrations are outside this synthetic demonstration.

## Report reproduction

`node frontend/ai-tests/report.cjs` validates exactly 100 distinct final IDs. It chooses the latest complete run for each group, overlays any later focused retests by ID, and writes the Markdown, HTML, CSV and JSON reports. It does not convert failed or blocked statuses to passed without a new recorded result. Run the stateful full suites against fresh synthetic fixtures when testing again.
