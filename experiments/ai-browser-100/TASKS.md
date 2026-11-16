# CareConnect: 100 browser tasks

Target: https://careconnect-demo-rc0t.onrender.com

Each task has an explicit user action and pass criterion. Synthetic accounts and records only. Task dependencies are reported as blocked when their prerequisites fail.

## simple

### A001 — Signed-out access to a protected record requires sign-in

Steps:

1. Open /results/1 in a fresh browser context.

Expected: Sign-in form is visible and patient record content is absent.

### A002 — Empty sign-in cannot submit

Steps:

1. Open sign-in.
2. Click Sign in without credentials.

Expected: Username receives native required-field validation.

### A003 — Incorrect credentials produce readable feedback

Steps:

1. Enter a nonexistent username and wrong password.
2. Submit sign-in.

Expected: An invalid-credentials alert appears without authenticated navigation.

### A004 — Password visibility control preserves the entered value

Steps:

1. Enter a sample password.
2. Click Show password, then Hide password.

Expected: Input switches password → text → password without changing its value.

### A005 — Registration offers three distinct account routes

Steps:

1. Click Create an account from sign-in.

Expected: Patient, Family caregiver, and Care team options are separate navigable choices.

### A007 — Registration account choice can be changed before submission

Steps:

1. Open Patient registration.
2. Click Change account type.
3. Choose Family caregiver.

Expected: Family caregiver account form replaces the patient form.

### A008 — Blank registration identifies required information

Steps:

1. Open Patient registration.
2. Submit an empty form.

Expected: Username validation blocks account creation.

### A009 — Malformed registration email is rejected

Steps:

1. Fill registration fields.
2. Replace email with not-an-email and submit.

Expected: Browser validation identifies invalid email and keeps the user on registration.

### A025 — Mobile sign-in fits a narrow viewport

Steps:

1. Open sign-in at 390 by 844 pixels.

Expected: Credentials and submit are visible without horizontal page overflow.

### A028 — Registration provides a usable route back to sign-in

Steps:

1. Open patient registration.
2. Click Back to sign in.

Expected: Sign-in page opens with its credentials form.

### A029 — Forgot-password form validates a missing email

Steps:

1. Open Forgot password from sign-in.
2. Submit without email.

Expected: Required email validation prevents submission.

### A034 — New patient sees a clear empty notification state

Steps:

1. Sign in to the synthetic account.
2. Click Notifications.

Expected: Notification heading and empty-record message appear without an error.

Prerequisites: A023

### B036 — New patient has no inherited appointments or medications

Steps:

1. Register a synthetic patient as fixture
2. Open Appointments and Medications

Expected: Both appointment groups and current medications are empty; seeded patient records do not leak into the new profile.

### B038 — An unavailable appointment date has a clear empty state

Steps:

1. Set Date to 2030-01-01
2. Find appointments

Expected: No matching appointments is shown and no Book button remains.

Prerequisites: B037

### B046 — Empty message submission is blocked by required fields

Steps:

1. Open New message
2. Click Send message with empty fields

Expected: Browser validation blocks submission and no conversation opens.

Prerequisites: B036

### B051 — Empty conversation reply is blocked

Steps:

1. Open test conversation
2. Click Send reply without text

Expected: Required validation blocks the reply and message count stays unchanged.

Prerequisites: B047

### B056 — Filter seeded laboratory results by test name

Steps:

1. Read-only patient opens Test Results
2. Search Hemoglobin A1c

Expected: Every displayed result matches the test name.

### B058 — Unmatched laboratory search shows an empty result

Steps:

1. Search a nonexistent synthetic test name
2. Apply filters

Expected: No result links are displayed and an empty-state message appears.

### B062 — Health summary identifies the patient and clinical sections

Steps:

1. Open Health Summary as seeded patient
2. Inspect demographics, allergies, and current medications

Expected: Jordan Vale identity, allergy record, medication and correction form are visible.

### B063 — Medication-name filter narrows current prescriptions

Steps:

1. Open Medications as seeded patient
2. Search Cetirizine
3. Apply filters

Expected: Cetirizine remains and Vitamin D3 is not listed.

### C071 — Register an independent synthetic patient

Steps:

1. Open patient registration
2. Enter unique invented identity and matching password
3. Create account

Expected: Casey reaches their own patient dashboard.

### C072 — Register a family caregiver into the correct workspace

Steps:

1. Choose Family caregiver registration
2. Create a separate invented account

Expected: Caregiver is routed to Family Access with no inherited patient data.

### C087 — Fresh patient has no unconsented family access

Steps:

1. Open Casey Family Access

Expected: Both incoming access and outgoing sharing show empty states.

Prerequisites: C071

## medium

### A006 — Care-team registration explains approval and limits requested roles

Steps:

1. Choose Care team registration.
2. Inspect requested-role options and approval notice.

Expected: Role choice includes clinical/office roles but not Administrator; approval requirement is visible.

### A010 — Mismatched registration passwords are rejected

Steps:

1. Fill a valid Patient registration with different password confirmation.
2. Submit.

Expected: A do-not-match error is shown; no account is created.

### A011 — Weak numeric registration password is rejected

Steps:

1. Fill Patient registration with matching password 12345678.
2. Submit.

Expected: A password-strength error is visible and registration remains open.

### A012 — New patient can register and reach their own dashboard

Steps:

1. Fill a valid unique synthetic Patient registration.
2. Submit.

Expected: Dashboard welcomes Atlas and shows personal account navigation.

### A013 — Authenticated session survives a page refresh

Steps:

1. Refresh the newly registered patient dashboard.

Expected: Atlas remains signed in and is not returned to sign-in.

Prerequisites: A012

### A014 — Duplicate username cannot register a second account

Steps:

1. Use a separate signed-out browser context.
2. Submit registration with the existing synthetic username.

Expected: An already-in-use error prevents duplicate creation.

Prerequisites: A012

### A015 — Patient contact information can be updated

Steps:

1. Sign in as the synthetic patient.
2. Open Account Settings.
3. Set phone and address; save profile.

Expected: Save confirmation is visible and entered values remain displayed.

Prerequisites: A012

### A016 — Saved profile persists across a new sign-in session

Steps:

1. Open a new browser context.
2. Sign in to the synthetic account and open Account Settings.

Expected: Previously saved phone and address are prefilled.

Prerequisites: A015

### A017 — Muting one notification category persists without muting others

Steps:

1. Mute Test result in synthetic account settings.
2. Refresh settings.

Expected: Test result shows Unmute while Message still shows Mute.

Prerequisites: A012

### A018 — A muted category can be re-enabled and stays enabled

Steps:

1. Click Unmute for Test result.
2. Refresh settings.

Expected: Test result returns to the Mute action after reload.

Prerequisites: A017

### A019 — Password change requires matching confirmation

Steps:

1. Open synthetic account settings.
2. Enter current password and different new-password confirmations.
3. Submit.

Expected: A mismatch alert appears without changing the password.

Prerequisites: A012

### A020 — Password change rejects incorrect current password

Steps:

1. Enter a wrong current password and valid matching new passwords.
2. Submit.

Expected: Current-password-incorrect alert appears.

Prerequisites: A012

### A026 — Mobile navigation opens, navigates, and closes correctly

Steps:

1. Sign in at mobile size.
2. Open menu and select Account Settings.
3. Open menu again and press Escape.

Expected: Settings opens; navigation closes on route selection and Escape; no horizontal overflow.

Prerequisites: A023

### A027 — Sign-in can be completed with keyboard navigation

Steps:

1. Focus Username and type username.
2. Press Tab to Password and type password.
3. Press Enter.

Expected: Keyboard-only form submission opens Atlas dashboard.

Prerequisites: A023

### A031 — Incomplete reset URL offers recovery without exposing a form

Steps:

1. Open /reset-password without a token.
2. Follow Request a new reset link.

Expected: Readable incomplete-link notice appears, then Forgot password opens.

### A032 — Unavailable record gives understandable feedback and a way back

Steps:

1. Sign in as the synthetic patient.
2. Open a nonexistent test-result detail.
3. Click Back to list.

Expected: Readable unavailable alert appears with no raw model error, and Test Results list opens.

Prerequisites: A023

### A033 — Unknown portal route offers a working home link

Steps:

1. Sign in.
2. Open /not-a-careconnect-page.
3. Use Home.

Expected: Page unavailable appears, and Home returns to the correct dashboard.

Prerequisites: A023

### B037 — Filter appointment slots by provider and visit type

Steps:

1. Open scheduling
2. Select Dr. Maya Rowan and Primary Care
3. Find appointments

Expected: Every returned slot matches both selected filters.

Prerequisites: B036

### B039 — Dismiss booking confirmation without creating a booking

Steps:

1. Open available slots
2. Click first Book
3. Choose Keep unchanged

Expected: Scheduling page and selected slot remain; no booking details are opened.

Prerequisites: B036

### B040 — Book a slot and preserve the new appointment after refresh

Steps:

1. Book first available appointment
2. Confirm
3. Refresh appointment details

Expected: Scheduled status and appointment details remain after refresh.

Prerequisites: B036

### B041 — Save a pre-visit questionnaire and reload it

Steps:

1. Enter a synthetic discussion topic
2. Save questionnaire
3. Refresh

Expected: Saved questionnaire text remains in appointment details.

Prerequisites: B040

### B042 — Submit a patient reschedule request without changing the booking time

Steps:

1. Enter preferred time
2. Request rescheduling
3. Refresh

Expected: The request is saved and the appointment remains Scheduled pending staff action.

Prerequisites: B040

### B044 — Cancel the replacement booking and preserve its reason

Steps:

1. Patient opens replacement
2. Enter cancellation reason
3. Confirm cancellation and reload

Expected: Cancelled status and the supplied reason persist.

Prerequisites: B043

### B045 — Complete simulated eCheck-In on a new booking

Steps:

1. Book a free slot
2. Save the required pre-visit questionnaire
3. Complete eCheck-In
4. Confirm and refresh

Expected: Checked In status persists and check-in action is no longer available.

Prerequisites: B036

### B047 — Send a new patient message to the care team

Steps:

1. Choose Care team and Medical Question
2. Fill unique subject and message
3. Send message

Expected: Conversation shows the exact subject, patient sender and supplied body.

Prerequisites: B036

### B049 — New-reply notification opens the matching conversation

Steps:

1. Patient opens Notifications
2. Click new care-team reply notification

Expected: Notification destination opens the test conversation with the physician reply.

Prerequisites: B048

### B050 — Mark all test-patient notifications read and persist

Steps:

1. Open Notifications
2. Mark all as read
3. Refresh

Expected: Read labels remain and Unread labels disappear.

Prerequisites: B049

### B052 — Patient reply persists and the composer clears

Steps:

1. Reply to test conversation
2. Send reply
3. Reload

Expected: Reply appears once, composer is empty, and saved reply survives reload.

Prerequisites: B047

### B053 — Cancel archiving without moving the conversation

Steps:

1. Click Archive
2. Choose Keep unchanged

Expected: Conversation stays open with Archive available and Restore absent.

Prerequisites: B047

### B054 — Archive a conversation with explicit list feedback

Steps:

1. Archive test conversation
2. Confirm

Expected: Archive tab is selected, saved notice is specific, and conversation is listed.

Prerequisites: B047

### B057 — Filter laboratory results to their visible collection date

Steps:

1. Read a result date from the list
2. Set collection date range to that date
3. Apply filters

Expected: Returned rows share the selected collection date.

### B059 — Lab detail shows reference range and keyboard-readable history

Steps:

1. Open a Hemoglobin A1c result
2. Inspect result and focus a historical data point

Expected: Value/reference range are present and historical point focus reveals its measurement.

### B060 — Download a laboratory PDF through the browser

Steps:

1. Click Download PDF on lab detail
2. Read the browser-downloaded file

Expected: Download has .pdf extension and PDF file signature.

Prerequisites: B059

### B061 — Clear an empty result search and recover laboratory results

Steps:

1. Search a nonexistent test name
2. Confirm empty results
3. Clear the name and apply filters

Expected: The empty-state message disappears and published result rows are restored.

### B065 — Patient sees the newly created prescription details

Steps:

1. Patient opens Medications
2. Open the new prescription

Expected: Strength, synthetic pharmacy, instructions and empty refill state match staff entry.

Prerequisites: B064

### B066 — Cancel refill confirmation without submitting a request

Steps:

1. Click Request refill
2. Choose Keep unchanged

Expected: Refill list stays empty and Request refill remains available.

Prerequisites: B065

### B067 — Submit a refill request and prevent duplicates while pending

Steps:

1. Enter refill note
2. Confirm Request refill
3. Refresh

Expected: One Requested refill is shown; duplicate request button is hidden.

Prerequisites: B065

### C073 — Billing staff creates a patient-specific invoice

Steps:

1. Sign in as billing staff
2. Choose Casey as patient context
3. Create invoice for $80 with $30 adjustment

Expected: Invoice drawer identifies Casey and $50 patient responsibility.

Prerequisites: C071

### C074 — Patient sees invoice calculations and unpaid status

Steps:

1. Open Billing as Casey
2. Open the new invoice

Expected: Charges $80, adjustment $30, responsibility and remaining $50; unpaid.

Prerequisites: C073

### C075 — Cancelling a payment confirmation leaves balance unchanged

Steps:

1. Enter $15 payment
2. Open confirmation
3. Choose Keep unchanged

Expected: Invoice remains unpaid with no $15 payment history.

Prerequisites: C074

### C076 — Partial simulated payment persists after refresh

Steps:

1. Pay $15 and confirm
2. Refresh invoice

Expected: Partially Paid with $15 paid and $35 remaining.

Prerequisites: C074

### C078 — Paying the exact remaining balance closes the invoice

Steps:

1. Pay $35 and confirm

Expected: Invoice is Paid, remaining $0, and payment form is removed.

Prerequisites: C076

### C079 — Download a genuine payment receipt PDF

Steps:

1. Open the $35 payment in history
2. Inspect receipt preview
3. Download PDF

Expected: Receipt identifies Casey and $35; downloaded file has a PDF signature.

Prerequisites: C078

### C080 — Download a complete paid statement PDF

Steps:

1. Return to invoice
2. Open View statement
3. Download PDF

Expected: Statement preview contains the invoice number and a genuine PDF is downloaded.

Prerequisites: C078

### C088 — Family invitation requires at least one shared section

Steps:

1. Open Link a family member
2. Enter caregiver email
3. Clear every section
4. Send invitation

Expected: Validation says choose at least one section and keeps the form open.

Prerequisites: C071, C072

### C090 — Cancelling consent leaves family access pending

Steps:

1. Choose Accept request
2. Choose Keep unchanged

Expected: Invitation remains Pending and no shared profile appears.

Prerequisites: C089

### C095 — Care-team signup creates a pending application

Steps:

1. Register a Physician with organization and invented identity

Expected: Applicant sees Pending application rather than staff records.

## hard

### A021 — Valid password change clears sensitive fields and confirms success

Steps:

1. Enter the correct current password and matching new passwords on the synthetic account.
2. Submit.

Expected: Password-changed confirmation appears and all three password fields are empty.

Prerequisites: A012

### A022 — Old password no longer grants access after a change

Steps:

1. Start a fresh browser session.
2. Attempt sign-in with the old password.

Expected: Invalid-credentials alert prevents dashboard access.

Prerequisites: A021

### A023 — New password signs the patient in successfully

Steps:

1. Sign in in a fresh session using the new password.

Expected: Atlas dashboard appears.

Prerequisites: A021

### A024 — Sign-out removes identity and protects browser-back access

Steps:

1. Sign in, then open Account Settings to create protected-page browser history.
2. Sign out, use browser Back and reload.

Expected: Sign-in remains required and Atlas identity is absent.

Prerequisites: A023

### A030 — Public forgotten-password recovery can deliver a reset request

Steps:

1. Open Forgot password.
2. Enter the synthetic registered email.
3. Click Send reset link.

Expected: A recovery request is accepted and Check your email is shown. Known deployment limitation: external recovery delivery is not configured.

Prerequisites: A012

### A035 — Switching administrator to patient removes privileged workspace state

Steps:

1. Sign in as demo admin.
2. Open Laboratory results and sign out.
3. Sign in as the synthetic patient without refreshing.
4. Try /staff.

Expected: Patient dashboard replaces staff shell; staff controls and administrator identity are absent; /staff cannot expose management UI.

Prerequisites: A023

### B043 — Staff reschedules the requested booking and patient sees replacement

Steps:

1. Staff selects the test patient and booking
2. Choose another slot and confirm reschedule
3. Patient opens replacement and previous booking

Expected: New appointment is Scheduled; previous appointment is Cancelled with reschedule reason.

Prerequisites: B042

### B048 — Physician replies to the correct patient conversation

Steps:

1. Physician opens Messages
2. Find unique test conversation
3. Send acknowledgement
4. Patient reloads conversation

Expected: Patient sees the physician sender and acknowledgement once.

Prerequisites: B047

### B055 — Restore archived conversation with confirmation and inbox redirect

Steps:

1. Open archived test conversation
2. Restore to inbox and confirm

Expected: Inbox is selected, exact restoration notice is visible, conversation remains in inbox after refresh.

Prerequisites: B054

### B064 — Physician creates a medication for the test patient

Steps:

1. Select test patient in staff workspace
2. Create medication with synthetic instructions
3. Save record

Expected: Medication drawer identifies Blair Test and the saved prescription.

Prerequisites: B036

### B068 — Physician approves refill and patient receives the decision

Steps:

1. Staff opens this patient refill
2. Select Approved and enter note
3. Save decision
4. Patient refreshes prescription

Expected: Approved and the physician decision note appear on the patient page.

Prerequisites: B067

### B069 — Complete refill and allow a future request

Steps:

1. Staff changes approved refill to Completed with note
2. Patient refreshes

Expected: Completed and decision text are visible; a future refill can be requested again.

Prerequisites: B068

### B070 — Medication correction request reaches staff and can be reviewed

Steps:

1. Patient submits a synthetic pharmacy correction
2. Staff opens Patient correction requests for Blair Test
3. Mark reviewed and refresh

Expected: Staff sees exact correction text and review state persists.

Prerequisites: B065

### C077 — Overpayment is rejected without changing the balance

Steps:

1. Attempt $99 against the $35 balance
2. Confirm the attempted payment

Expected: Visible validation rejects overpayment and balance stays $35.

Prerequisites: C076

### C081 — Unpublished clinical document stays out of patient list

Steps:

1. Sign in as physician
2. Create private clinical letter for Casey
3. Check patient Documents

Expected: Staff sees an unpublished document; patient cannot find it.

Prerequisites: C071

### C082 — Published document becomes readable and downloadable

Steps:

1. Publish the clinical letter and confirm
2. Refresh patient Documents
3. Open letter and download PDF

Expected: Patient sees correct content and a valid PDF.

Prerequisites: C081

### C083 — Draft lab result is visible only to staff

Steps:

1. Create Final lab value 100 with range 80–120
2. Do not publish
3. Check patient Test Results

Expected: Staff displays private result; patient list does not expose it.

Prerequisites: C071

### C084 — Publish lab and verify patient values and reference range

Steps:

1. Publish the private lab
2. Reload patient Test Results
3. Open new result

Expected: Patient sees 100 demo-unit, reference 80–120, In range.

Prerequisites: C083

### C085 — Withdrawing a lab blocks its already-open patient detail

Steps:

1. Unpublish from staff drawer
2. Refresh the patient detail URL

Expected: Patient sees readable unavailable message, no result value, and Back to list.

Prerequisites: C084

### C086 — Republishing restores the original report URL

Steps:

1. Republish the same lab
2. Refresh original patient detail

Expected: Original result URL works again without creating a second record.

Prerequisites: C085

### C089 — Results-only invitation stays pending before consent

Steps:

1. Select only Test Results
2. Send invitation
3. Inspect both accounts

Expected: Pending invitation is shown without granting linked-profile access.

Prerequisites: C088

### C091 — Accepting consent activates only selected sections

Steps:

1. Accept and confirm invitation
2. Inspect Casey profile card

Expected: Casey becomes linked, with Test Results link but no Billing link in that card.

Prerequisites: C090

### C092 — Family access cannot open an unshared billing section

Steps:

1. Navigate to Billing with Casey family-profile context

Expected: Visible permission denial; invoice details are not exposed.

Prerequisites: C091, C073

### C093 — Consenting caregiver can open shared patient lab

Steps:

1. Open Casey shared Test Results
2. Open the published lab

Expected: Correct family banner and 100 demo-unit result are displayed.

Prerequisites: C091, C086

### C094 — Revocation removes access from a stale family detail link

Steps:

1. Patient revokes Cameron access
2. Caregiver refreshes their existing lab detail

Expected: Caregiver sees unavailable/permission error and cannot read result.

Prerequisites: C093

### C096 — Pending staff cannot bypass review with a direct workspace URL

Steps:

1. Open /staff?area=results while pending

Expected: Pending review remains visible and laboratory records are absent.

Prerequisites: C095

### C097 — Administrator approves only the selected synthetic staff application

Steps:

1. Sign in as admin
2. Open Access reviews
3. Approve Cory with decision note and confirmation

Expected: Cory application changes to Approved with verification note.

Prerequisites: C095

### C098 — Approved applicant enters physician workspace without a new signup

Steps:

1. Click Check application status as Cory

Expected: Staff workspace and clinical work areas appear.

Prerequisites: C097, C096

### C099 — Physician role does not gain billing or administrator privileges

Steps:

1. Inspect approved physician work areas
2. Try direct billing area and access reviews routes

Expected: No invoice-management or access-review controls become available.

Prerequisites: C098

### C100 — Mobile staff record drawer remains usable and closes with Escape

Steps:

1. Open Casey lab as approved physician at 390px viewport
2. Inspect immediate drawer
3. Press Escape

Expected: Drawer is on screen, page has no horizontal overflow, Escape closes it.

Prerequisites: C098, C083
