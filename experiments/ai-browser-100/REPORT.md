# CareConnect public browser evaluation

Target: https://careconnect-demo-rc0t.onrender.com
Generated: 2026-11-16T04:20:46.159Z

AI-authored Playwright browser agents using visible UI controls, DOM assertions and browser downloads. Not screenshot-only desktop computer-use.

## Results

- Planned: **100**; passed: **99**; failed: **1**; blocked: **0**.
- Overall pass rate: **99.0%** (passed / 100; blocked tasks remain in the denominator).
- Executed-task pass rate: **99.0%** (passed / (passed + failed)).

| Difficulty | Passed | Failed | Blocked | Total |
| --- | ---: | ---: | ---: | ---: |
| simple | 23 | 0 | 0 | 23 |
| medium | 47 | 0 | 0 | 47 |
| hard | 29 | 1 | 0 | 30 |

## Per-task evidence

| ID | Task | Difficulty | Outcome | Evidence |
| --- | --- | --- | --- | --- |
| A001 | Signed-out access to a protected record requires sign-in | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A001.png) |
| A002 | Empty sign-in cannot submit | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A002.png) |
| A003 | Incorrect credentials produce readable feedback | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A003.png) |
| A004 | Password visibility control preserves the entered value | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A004.png) |
| A005 | Registration offers three distinct account routes | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A005.png) |
| A006 | Care-team registration explains approval and limits requested roles | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A006.png) |
| A007 | Registration account choice can be changed before submission | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A007.png) |
| A008 | Blank registration identifies required information | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A008.png) |
| A009 | Malformed registration email is rejected | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A009.png) |
| A010 | Mismatched registration passwords are rejected | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A010.png) |
| A011 | Weak numeric registration password is rejected | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A011.png) |
| A012 | New patient can register and reach their own dashboard | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A012.png) |
| A013 | Authenticated session survives a page refresh | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A013.png) |
| A014 | Duplicate username cannot register a second account | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A014.png) |
| A015 | Patient contact information can be updated | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A015.png) |
| A016 | Saved profile persists across a new sign-in session | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A016.png) |
| A017 | Muting one notification category persists without muting others | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A017.png) |
| A018 | A muted category can be re-enabled and stays enabled | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A018.png) |
| A019 | Password change requires matching confirmation | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A019.png) |
| A020 | Password change rejects incorrect current password | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A020.png) |
| A021 | Valid password change clears sensitive fields and confirms success | hard | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A021.png) |
| A022 | Old password no longer grants access after a change | hard | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A022.png) |
| A023 | New password signs the patient in successfully | hard | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A023.png) |
| A024 | Sign-out removes identity and protects browser-back access | hard | passed | [Screenshot](auth-navigation-followup-2026-11-16T04-17-31-914Z/A024.png) |
| A025 | Mobile sign-in fits a narrow viewport | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A025.png) |
| A026 | Mobile navigation opens, navigates, and closes correctly | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A026.png) |
| A027 | Sign-in can be completed with keyboard navigation | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A027.png) |
| A028 | Registration provides a usable route back to sign-in | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A028.png) |
| A029 | Forgot-password form validates a missing email | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A029.png) |
| A030 | Public forgotten-password recovery can deliver a reset request | hard | failed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A030.png) |
| A031 | Incomplete reset URL offers recovery without exposing a form | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A031.png) |
| A032 | Unavailable record gives understandable feedback and a way back | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A032.png) |
| A033 | Unknown portal route offers a working home link | medium | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A033.png) |
| A034 | New patient sees a clear empty notification state | simple | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A034.png) |
| A035 | Switching administrator to patient removes privileged workspace state | hard | passed | [Screenshot](auth-navigation-2026-11-16T04-14-14-459Z/A035.png) |
| B036 | New patient has no inherited appointments or medications | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B036.png) |
| B037 | Filter appointment slots by provider and visit type | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B037.png) |
| B038 | An unavailable appointment date has a clear empty state | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B038.png) |
| B039 | Dismiss booking confirmation without creating a booking | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B039.png) |
| B040 | Book a slot and preserve the new appointment after refresh | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B040.png) |
| B041 | Save a pre-visit questionnaire and reload it | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B041.png) |
| B042 | Submit a patient reschedule request without changing the booking time | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B042.png) |
| B043 | Staff reschedules the requested booking and patient sees replacement | hard | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B043.png) |
| B044 | Cancel the replacement booking and preserve its reason | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B044.png) |
| B045 | Complete simulated eCheck-In on a new booking | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B045.png) |
| B046 | Empty message submission is blocked by required fields | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B046.png) |
| B047 | Send a new patient message to the care team | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B047.png) |
| B048 | Physician replies to the correct patient conversation | hard | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B048.png) |
| B049 | New-reply notification opens the matching conversation | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B049.png) |
| B050 | Mark all test-patient notifications read and persist | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B050.png) |
| B051 | Empty conversation reply is blocked | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B051.png) |
| B052 | Patient reply persists and the composer clears | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B052.png) |
| B053 | Cancel archiving without moving the conversation | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B053.png) |
| B054 | Archive a conversation with explicit list feedback | medium | passed | [Screenshot](clinical-focused-2026-11-16T04-18-55-322Z/B054.png) |
| B055 | Restore archived conversation with confirmation and inbox redirect | hard | passed | [Screenshot](clinical-focused-2026-11-16T04-18-55-322Z/B055.png) |
| B056 | Filter seeded laboratory results by test name | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B056.png) |
| B057 | Filter laboratory results to their visible collection date | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B057.png) |
| B058 | Unmatched laboratory search shows an empty result | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B058.png) |
| B059 | Lab detail shows reference range and keyboard-readable history | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B059.png) |
| B060 | Download a laboratory PDF through the browser | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B060.png) |
| B061 | Clear an empty result search and recover laboratory results | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B061.png) |
| B062 | Health summary identifies the patient and clinical sections | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B062.png) |
| B063 | Medication-name filter narrows current prescriptions | simple | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B063.png) |
| B064 | Physician creates a medication for the test patient | hard | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B064.png) |
| B065 | Patient sees the newly created prescription details | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B065.png) |
| B066 | Cancel refill confirmation without submitting a request | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B066.png) |
| B067 | Submit a refill request and prevent duplicates while pending | medium | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B067.png) |
| B068 | Physician approves refill and patient receives the decision | hard | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B068.png) |
| B069 | Complete refill and allow a future request | hard | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B069.png) |
| B070 | Medication correction request reaches staff and can be reviewed | hard | passed | [Screenshot](clinical-2026-11-16T04-16-19-250Z/B070.png) |
| C071 | Register an independent synthetic patient | simple | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C071.png) |
| C072 | Register a family caregiver into the correct workspace | simple | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C072.png) |
| C073 | Billing staff creates a patient-specific invoice | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C073.png) |
| C074 | Patient sees invoice calculations and unpaid status | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C074.png) |
| C075 | Cancelling a payment confirmation leaves balance unchanged | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C075.png) |
| C076 | Partial simulated payment persists after refresh | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C076.png) |
| C077 | Overpayment is rejected without changing the balance | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C077.png) |
| C078 | Paying the exact remaining balance closes the invoice | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C078.png) |
| C079 | Download a genuine payment receipt PDF | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C079.png) |
| C080 | Download a complete paid statement PDF | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C080.png) |
| C081 | Unpublished clinical document stays out of patient list | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C081.png) |
| C082 | Published document becomes readable and downloadable | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C082.png) |
| C083 | Draft lab result is visible only to staff | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C083.png) |
| C084 | Publish lab and verify patient values and reference range | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C084.png) |
| C085 | Withdrawing a lab blocks its already-open patient detail | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C085.png) |
| C086 | Republishing restores the original report URL | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C086.png) |
| C087 | Fresh patient has no unconsented family access | simple | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C087.png) |
| C088 | Family invitation requires at least one shared section | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C088.png) |
| C089 | Results-only invitation stays pending before consent | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C089.png) |
| C090 | Cancelling consent leaves family access pending | medium | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C090.png) |
| C091 | Accepting consent activates only selected sections | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C091.png) |
| C092 | Family access cannot open an unshared billing section | hard | passed | [Screenshot](crossrole-2026-11-16T04-13-51-163Z/C092.png) |
| C093 | Consenting caregiver can open shared patient lab | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C093.png) |
| C094 | Revocation removes access from a stale family detail link | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C094.png) |
| C095 | Care-team signup creates a pending application | medium | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C095.png) |
| C096 | Pending staff cannot bypass review with a direct workspace URL | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C096.png) |
| C097 | Administrator approves only the selected synthetic staff application | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C097.png) |
| C098 | Approved applicant enters physician workspace without a new signup | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C098.png) |
| C099 | Physician role does not gain billing or administrator privileges | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C099.png) |
| C100 | Mobile staff record drawer remains usable and closes with Escape | hard | passed | [Screenshot](crossrole-2026-11-16T04-18-26-054Z/C100.png) |

## Attempt history

First scripted attempts: **69.0%** (69 passed, 9 failed checks, 22 blocked).

The final score uses the latest complete run per group, plus explicitly documented focused retests after test-only corrections. It is not the first-attempt agent success rate. All raw attempts remain available. Two passing clinical scenarios were refined to avoid duplicate coverage; see the clinical notes.

| Group | Attempt | Completed | Passed | Failed | Blocked |
| --- | --- | ---: | ---: | ---: | ---: |
| auth-navigation | [2026-11-16T04:12:09.712Z](auth-navigation-2026-11-16T04-12-09-710Z/results.json) | 35 | 22 | 3 | 10 |
| auth-navigation | [2026-11-16T04:14:14.460Z](auth-navigation-2026-11-16T04-14-14-459Z/results.json) | 35 | 33 | 2 | 0 |
| auth-navigation | [2026-11-16T04:17:31.915Z](auth-navigation-followup-2026-11-16T04-17-31-914Z/results.json) | 1 | 1 | 0 | 0 |
| clinical | [2026-11-16T04:12:34.159Z](clinical-2026-11-16T04-12-34-157Z/results.json) | 35 | 31 | 3 | 1 |
| clinical | [2026-11-16T04:16:19.252Z](clinical-2026-11-16T04-16-19-250Z/results.json) | 35 | 33 | 1 | 1 |
| clinical | [2026-11-16T04:18:55.323Z](clinical-focused-2026-11-16T04-18-55-322Z/results.json) | 2 | 2 | 0 | 0 |
| crossrole | [2026-11-16T04:12:14.800Z](crossrole-2026-11-16T04-12-14-798Z/results.json) | 30 | 16 | 3 | 11 |
| crossrole | [2026-11-16T04:13:51.164Z](crossrole-2026-11-16T04-13-51-163Z/results.json) | 30 | 22 | 2 | 6 |
| crossrole | [2026-11-16T04:18:26.055Z](crossrole-2026-11-16T04-18-26-054Z/results.json) | 11 | 11 | 0 | 0 |

## Failures and blocked tasks

### A030 — Public forgotten-password recovery can deliver a reset request

Outcome: failed

```text
Error: expect(locator).toBeVisible() failed

Locator: getByRole('heading', { name: 'Check your email', exact: true })
Expected: visible
Timeout: 20000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByRole('heading', { name: 'Check your email', exact: true }) with timeout 20000ms
  - waiting for getByRole('heading', { name: 'Check your email', exact: true })

    at captureRawStack (C:\Users\jiawe\Documents\Codex\2026-11-13\mychart-https-www-mychart-org-utm\outputs\CareConnect-v3\frontend\node_modules\playwright-core\lib\coreBundle.js:9551:17)
    at callMatcherAsStep (C:\Users\jiawe\Documents\Codex\2026-11-13\mychart-https-www-mychart-org-utm\outputs\CareConnect-v3\frontend\node_modules\playwright\lib\matchers\expect.js:13342:57)
    at Object.toBeVisible (C:\Users\jiawe\Documents\Codex\2026-11-13\mychart-https-www-mychart-org-utm\outputs\CareConnect-v3\frontend\node_modules\playwright\lib\matchers\expect.js:13334:23)
    at Object.run (C:\Users\jiawe\Documents\Codex\2026-11-13\mychart-https-www-mychart-org-utm\outputs\CareConnect-v3\frontend\ai-tests\auth-navigation.cjs:42:567)
    at async runSuite (C:\Users\jiawe\Documents\Codex\2026-11-13\mychart-https-www-mychart-org-utm\outputs\CareConnect-v3\frontend\ai-tests\harness.cjs:45:8)
    at async C:\Users\jiawe\Documents\Codex\2026-11-13\mychart-https-www-mychart-org-utm\outputs\CareConnect-v3\frontend\ai-tests\auth-navigation.cjs:48:32
```

## Scope and limitations

- No application code was modified during this evaluation. The target is a shared public synthetic-data demonstration.
- These results measure the defined tasks on one browser family and selected desktop/mobile viewports, not all possible behavior or security.
- Browser automation uses semantic selectors and DOM inspection; it does not measure a vision-only agent's ability to find controls from pixels.
- No backend API or database assertions are used for scoring. Browser downloads may be inspected as files.
- First attempts and any corrected harness attempts are retained in their timestamped folders. Read AGENT-NOTES.md for test-only corrections and defect interpretation.
- Real email delivery, actual payments, external hospital integration and load testing are outside this demo evaluation.
