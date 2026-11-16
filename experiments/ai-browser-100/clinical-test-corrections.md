# Clinical browser test corrections

No application code was changed. The original attempt is retained at `clinical-2026-11-16T04-12-34-157Z/results.json` with screenshots and text evidence.

Original attempt: **31 passed, 3 failed checks, 1 blocked** out of 35.

- **B039:** The assertion compared browser `innerText` (line breaks) to Playwright's default text-content matcher (no line breaks between inline DOM nodes). The screenshot and page text showed the slot unchanged after dismissing the confirmation. Corrected to compare `innerText` with `innerText`; the expected behavior remains unchanged.
- **B043:** After confirmation, the test immediately matched the old appointment's still-visible `Scheduled` label, then read the old record URL before the asynchronous reschedule navigation finished. The patient page correctly showed the old record cancelled. Corrected to wait until the visible browser URL changes to a new record before checking its status. **B044** was blocked by this test prerequisite.
- **B045:** The test omitted a required pre-visit questionnaire. The application displayed `Complete the pre-visit questionnaire before checking in.` Corrected the test steps to save that required questionnaire first, then exercise successful check-in. The original rejection is evidence that the prerequisite is enforced, not evidence of a successful check-in.

The shared harness was also updated by the coordinator to allow 20-second assertions on the free hosted instance. The corrected full attempt uses a fresh synthetic test patient so it does not reuse mutated workflow records. The original attempt is not overwritten or silently counted as passing.

The corrected full attempt `clinical-2026-11-16T04-16-19-250Z` completed with **33 passed, 1 failed test selector, 1 blocked**. B054's broad `getByRole('status')` matched both the correct `Conversation archived.` notice and a transient `Loading…` panel. The archived success notice was present in the saved screenshot/text. The selector now explicitly identifies the success notice by its expected text. B054 and its dependent B055 were rerun as a focused pair on a new UI-created synthetic conversation; their outcomes are stored separately under `clinical-focused-*`. No application behavior or assertions were weakened.

For future reproducibility, medication creation now selects the patient by the value already selected in the visible `Patient context` dropdown, avoiding ambiguity if display names repeat. Both medication workflows in the executed full attempts passed before this selector hardening.

Coordinator scenario refinements before corrected execution: B036 uses registration only as a fixture and verifies appointment/medication isolation for a fresh patient. B061 now verifies recovery after clearing an empty laboratory search, avoiding duplication with another agent's missing-record navigation task. The originally executed B036 and B061 results remain in the original run artifact.
