# Authentication and navigation browser-agent notes

Method: AI-authored and executed Playwright browser UI automation using Edge. This is not a native screenshot-only desktop computer-use evaluation. Actions use visible form controls, keyboard input, browser navigation, DOM accessibility locators, and rendered-document checks. No direct application API or database assertions are used.

## Original run

- Evidence: `auth-navigation-2026-11-16T04-12-09-710Z/results.json`.
- 35 planned tasks: 22 passed, 3 failed, 10 blocked.
- A017 and A021 stopped during their sign-in prerequisite, before testing notification muting or password updates. The inherited Playwright assertion timeout was 5 seconds, while the screenshot and rendered text showed `Please wait…`. Other sign-ins succeeded. These outcomes do not establish product failures for muting or changing passwords.
- A030 reached the recovery page and submitted a valid synthetic email. The website displayed `Password recovery is not configured. Please contact support.` This is a known production feature limitation, not successful recovery.
- Dependencies on A017/A021 account for the 10 blocked tasks. Original JSON, text, and screenshots remain unchanged.

## Test-only corrections

- The shared runner's assertion timeout was corrected from Playwright's implicit 5 seconds to an explicit 20 seconds by the coordinating agent. This accommodates the free hosting tier's asynchronous sign-in completion; no website behavior or assertion expectation was changed.
- This suite now derives its unique username from `CC_AI_RUN` (`ai-a-<run key>`) so a full rerun can use fresh synthetic data instead of colliding with the first run's account.
- Corrected runs used an explicit 20-second assertion bound. Light overlap with other browser-agent groups remained; this is not a load test and no performance-capacity claim is made. No application code was modified by this agent.

## Corrected execution

- Full rerun: `auth-navigation-2026-11-16T04-14-14-459Z/results.json`, using synthetic patient `ai-a-20261115-r2`. Raw result: 33 passed, 2 failed, 0 blocked.
- A017 and A021 passed with the corrected 20-second assertion timeout. The notification preference screenshot was also visually inspected: Test result showed Unmute, while other categories showed Mute.
- A024 exposed a test setup error: login and logout intentionally replace browser history, so a fresh context with no intermediate protected-page visit went Back to `about:blank`. The original assertion expected sign-in there. This did not establish unauthorized access or stale patient information.
- Corrected A024 setup explicitly visits Account Settings after sign-in to create a protected-page history entry, then signs out, goes Back and refreshes. The same requirement remains: sign-in is required and the Atlas identity is absent. Isolated rerun **passed**: `auth-navigation-followup-2026-11-16T04-17-31-914Z/results.json`. The original blank screenshot remains preserved; final task catalog steps reflect the corrected setup.
- A030 failed again as expected from the live deployment limitation. Its screenshot was visually inspected and displays: `Password recovery is not configured. Please contact support.` The test is not relabeled as a pass merely because that limitation was known.
- Final task-level result after documented test-only corrections: **34 / 35 passed (97.14%)**, **1 failed**, **0 blocked**. Count A024 once using its focused corrected evidence, and retain the original run summaries separately.
- Shared demo accounts were not modified. Both Atlas synthetic accounts remain on the public demo. The first account retains the original demo password; the corrected-run account uses the test-specific changed password documented in the executable suite. Profile changes and notification preference tests only affected the synthetic accounts created by this agent.
