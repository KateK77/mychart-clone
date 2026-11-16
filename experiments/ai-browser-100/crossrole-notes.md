# Cross-role browser evaluation notes

Target: https://careconnect-demo-rc0t.onrender.com

Agent group C owns C071–C100 (30 tasks). It uses separate browser contexts for the synthetic patient, caregiver, existing demonstration staff, and a new physician applicant. All business setup and assertions use visible browser UI. PDF checks inspect the actual browser download's file signature. No direct API or database requests are used by this suite.

## Initial attempt and test harness correction

Raw evidence: `crossrole-2026-11-16T04-12-14-798Z/results.json` and per-task screenshots/text.

The initial attempt produced 16 passed, 3 failed, and 11 blocked results. C071–C080 passed, including invoice calculations, confirmation cancellation, partial and full simulated payments, overpayment rejection, and receipt/statement PDF downloads.

C081 and C095 timed out in the browser assertion after 5 seconds while the captured UI still said **Please wait…** during staff login and staff registration respectively. The harness's page timeout of 15 seconds did not change Playwright's separate assertion timeout. C083 then encountered the unauthenticated state after the preceding login was interrupted; subsequent workflow cases were blocked by their explicit prerequisites. These results do not establish that the application rejected valid credentials or registration.

The shared harness was corrected to use a 20-second assertion timeout. The original evidence is retained. A fresh run uses `CC_AI_RUN=20261115b` to avoid duplicate registration and to preserve separate synthetic records. No application implementation, expected user outcome, or permission requirement was changed for the rerun.

## Known evaluation boundaries

- This is AI-authored Playwright browser automation, not a screenshot-only visual desktop agent.
- It tests the deployed English interface and real browser downloads, not every underlying API authorization combination.
- Only synthetic users and uniquely named test invoices, documents, and labs are created. Payments are simulated. Shared demonstration credentials are not changed.
- A task's evidence screenshot is its final visible page; some multi-account tasks also act in another context before the final screenshot.

## Corrected full attempt and focused recovery

The full 20-second-assertion attempt is `crossrole-2026-11-16T04-13-51-163Z/results.json`: **22 passed, 2 test-script errors, 6 blocked**.

- **C084:** the exact text `In range` appeared in both the result detail and historical measurement. Playwright correctly reported a strict-mode ambiguity. The existing screenshot and page text showed the expected result and reference range. The selector was scoped to the first (detail) badge; the value, range, status, and publication criteria were unchanged.
- **C098:** C096 intentionally navigated the pending applicant to `/staff?area=results`. After administrator approval, checking application status correctly revealed that remembered laboratory module, rather than the all-work-areas chooser. The script had incorrectly looked for a work-area button. It now checks the Staff workspace heading, Laboratory results heading, `Work area=results`, visible `Create record`, and absence of the pending-application heading.

Only the affected chains were rerun: C084–C086 and C093–C100. The recovery used the existing `20261115b` patient, caregiver, lab and consent; fixture state was established through the UI. A new synthetic applicant `ai-cdoc-20261115b-recovery` enabled the complete application approval chain. One recovery setup attempt stopped before any case because it inspected publication-button count before the drawer loaded; a wait for the visible lab heading corrected that setup race. This setup error is not counted as a product result.

Focused recovery evidence is `crossrole-2026-11-16T04-18-26-054Z/results.json`: **11 passed, 0 failed, 0 blocked**, each with a screenshot. The full 30-task catalog was restored after the focused run.

**Final assessed C071–C100 outcome: 30/30 passed (100%)**, combining the corrected full run with the 11 explicitly identified recovery results. This is not a claim that the first script run passed. All raw attempts remain available, no application code changed, and no observed product failure was suppressed.

Run commands (from repository root):

```powershell
# Full suite with fresh identities; use a new run key on subsequent runs.
$env:CC_AI_RUN='20261115b'
node frontend/ai-tests/crossrole.cjs

# Recorded focused recovery, relying on that full run's UI-created fixtures.
$env:CC_AI_C_RECOVERY='1'
$env:CC_AI_C_APPLICANT_SUFFIX='-recovery'
node frontend/ai-tests/crossrole.cjs
```
