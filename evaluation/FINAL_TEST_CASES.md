# Final V3 specification-based native CUA test suite

Exactly 100 independent tests: Easy30 / Medium40 / Hard20 / Expert10.

Authority: `experiments/round-03/description.md` (3.0.0, Round3). No previous browser scores are reused.

Each test resets to an independent synthetic baseline; no test depends on an earlier test passing. F0 and named fixture contracts are defined in `FIXTURES.md`. Runtime accounts/secrets and URLs are provided privately.

## Requirement traceability

- **R01** — Current delivery instruction and precedence; §1; §21: All product copy and synthetic records are English; show the synthetic-only disclaimer; use fictional data.
- **R02** — §5 Design and Navigation: Eleven primary patient areas, consistent navigation, loading/empty/error/success states, confirmations, breadcrumbs, responsive accessible controls.
- **R03** — §6 Patient Dashboard: Personalized persisted overview: appointments, results, unread messages, medications, balance, visits, notifications and five quick actions.
- **R04** — §7 Authentication and Patient Accounts: Registration, login, hashed passwords, logout, profile editing, password change, sessions and role/object access control.
- **R05** — Retained feedback 3: Logout clears cached session/patient records, immediately returns to sign-in and permits account switching without refresh.
- **R06** — Retained feedback 4: Registration/change/recovery confirm password, validate strength/equality, provide accessible visibility controls and clear fields on success.
- **R07** — Retained feedback 4: Forgot password uses a clearly marked local simulated mailbox and expiring single-use reset links.
- **R08** — V2-MT-003 Account-type registration and landing pages: Mutually exclusive Patient, Family caregiver, Care team selection precedes role-specific form; allow choice changes; correct patient/caregiver landing.
- **R09** — V2-MT-003 Account-type registration and landing pages: Physician/Nurse/Front Desk/Billing Staff applications include organization, remain unprivileged pending review; administrator approval/decline needs verification note; no public Administrator.
- **R10** — §8 Appointment Management: Upcoming/past appointments, instructions, slot provider/type/date selection and six appointment types.
- **R11** — §8; §20 Workflow A: Booking persists to patient/dashboard/staff; availability validation, scheduling-conflict and double-booking prevention.
- **R12** — §8 Appointment Management: Cancellation records reason/history; previsit questionnaire and simulated eCheck-In persist; enforce status transitions.
- **R13** — §8; Retained feedback 7: Patients request rescheduling; staff replaces appointment, opens replacement, preserves separate cancellation histories; upcoming earliest first, consistent timezones.
- **R14** — §8; §18 Staff and Administrative Dashboard: Staff manage providers, departments/availability, appointments and statuses.
- **R15** — §9 Test Results: Results display test, collection/result dates, value, unit, reference range, status, flag, provider and comments; no inferred diagnoses.
- **R16** — §9 Test Results: Result name/date filtering, details, historical measurements/trend charts, Pending/Preliminary/Final/Corrected states.
- **R17** — §9; §20 Workflow B; V2-MT-002: Staff create initially unpublished results and publish; patient notification/visibility; withdrawal blocks details and direct exports.
- **R18** — §10 Secure Messaging: Inbox/Sent, new message, recipient/team, five categories, threaded replies, read/unread, staff inbox, persisted messages, non-emergency notice.
- **R19** — V2-MT-001 Message restoration: Archive/restore confirm, navigate to correct selected destination folder, specific success and visible thread; only applicable action, cancel unchanged, error retains detail; per-user state.
- **R20** — §11 Medication Management: Active/history/search and full medication details including strength, dosage, route, frequency, dates, provider, pharmacy, status, instructions.
- **R21** — §11; Retained feedback 6; §20 Workflow D: Simulated refill submission/staff review, Requested/Under Review/Approved/Denied/Completed; prevent duplicate pending requests with clear explanation; show progress/decision.
- **R22** — §11; §12 Health Summary: Medication and health corrections are requests/self-reported, not silent edits to official data; staff maintain official records.
- **R23** — §12 Health Summary: Demographics, conditions, allergies, medications, immunizations, medical/surgical/family/social history, care team, vitals, preventive care.
- **R24** — §13 Visits and Clinical Notes: Visit detail: date/provider/department/type/reason/diagnoses/summary/follow-up/shared notes/AVS; staff creates and publishes; private/unpublished notes hidden.
- **R25** — §14 Billing and Payments; §20 Workflow E: Invoices, insurance, outstanding balance/history, all specified invoice fields and statuses; staff creates; simulated payments update exact balances and transactions.
- **R26** — §14 Billing and Payments: Prevent duplicate processing of same payment request; input validation; no real card collection/live processing.
- **R27** — §15 Medical Documents: Seven document types, list/filter/open/download/date/linked encounter; generated synthetic content; authorization on every file access.
- **R28** — V2-MT-002 Document previews and PDF downloads: Web preview, Download PDF, Print for labs/documents/AVS/statements/receipts; real application/pdf and descriptive .pdf names from same authorized representation.
- **R29** — V2-MT-002 Document previews and PDF downloads: PDF branding, patient/available provider identifiers, reference/dates, values/units/ranges/status/exact amounts, disclaimer/page numbers; wrap and paginate long text.
- **R30** — V2-MT-002 Document previews and PDF downloads: Withdrawn labs, unpublished visits/documents, unrelated patients and disallowed/revoked proxy sections blocked at direct exports and UI.
- **R31** — V2-MT-004 Linking family accounts: Visible Link a family member; invite to own records or request another account; explicit section scopes and incoming/outgoing status, expiry, relationship/actions; local delivery disclosure.
- **R32** — V2-MT-004 Linking family accounts: Authenticated intended recipient explicitly accepts/declines; email/name match alone insufficient; bind invitations including registration, profile email edits cannot claim.
- **R33** — V2-MT-004 Linking family accounts: Cancel pending; block duplicates, expired/reused acceptance; owner revoke/proxy remove; old invitation cannot silently restore revoked access.
- **R34** — §16; §20 Workflow F; V2-MT-004: Linked profile switching exposes only granted sections; staff grants/revokes; enforce permission changes on subsequent requests and audit.
- **R35** — V2-MT-004 Linking family accounts: Dependent/guardian access requires administrator verification, never self-granted; synthetic verification limitations disclosed.
- **R36** — §17 Notifications: Results/messages/upcoming appointments/cancellations/refills/bills/payments notifications; read/unread/list/deep links/mark-read/preferences; local operation no external mail dependency.
- **R37** — Retained feedback 2: Staff categorized searchable/group-filtered work areas and compact selector; immediate focused detail drawer with close/back, patient/module preserved, keyboard/mobile no overflow.
- **R38** — Retained feedback 5; §22; §23: Readable permission/unavailable/validation errors and way back, no internal query/model errors; readable staff names/dates instead of raw IDs where possible.
- **R39** — §7; §22 Security and Auditability: Role/object authorization, sessions, CSRF, input validation, sensitive-data isolation and secure document access.
- **R40** — §22 Security and Auditability: Audit login, record access, appointment changes, lab publication, medication changes, refill decisions, proxy permission and billing changes.

## Easy

### Dashboard

#### T001 — Review the patient dashboard against the seeded record inventory.

Requirements: R01, R03

Preconditions:
- F0 patient P has appointments/results/messages/medications/invoice/visit/notification

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sign in as P.
2. Open Dashboard and inspect each overview card.

Expected result: Dashboard identifies P and accurately summarizes the seeded records.

Objective acceptance criteria:

- Name matches P.
- All seven overview data categories are present.
- Counts and balance match F0 rather than placeholders.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T003 — Find and open each of the five dashboard quick actions.

Requirements: R03

Preconditions:
- F0 P

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Dashboard.
2. Open Schedule Appointment, Send Message, View Test Results, Request Refill and Pay Bill one at a time, returning between actions.

Expected result: All quick actions lead to the relevant usable workflow.

Objective acceptance criteria:

- Five actions are visible and have correct destinations.
- No action falsely reports a completed mutation merely from navigation.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Navigation

#### T002 — Navigate all eleven patient areas and return to Dashboard.

Requirements: R02

Preconditions:
- F0 P

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sign in as P.
2. Use the primary navigation to open each of the eleven areas.
3. Return to Dashboard.

Expected result: Every required area is reachable through consistent navigation.

Objective acceptance criteria:

- Dashboard, Appointments, Messages, Test Results, Medications, Health Summary, Visits, Billing, Documents, Family Access and Account Settings load.
- No dead-end navigation or application error.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T029 — Inspect English copy and the synthetic disclaimer across patient and staff pages.

Requirements: R01, R02

Preconditions:
- F0 P and administrator

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Dashboard, appointment details, Billing and staff workspace.
2. Read headings, seeded values and disclaimer.

Expected result: English UI and synthetic-only disclosure are consistent.

Objective acceptance criteria:

- Inspected product text and new seeded records are English.
- Disclaimer is visible.
- No claim of Epic affiliation or clinical certification.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T030 — Use patient navigation on a narrow screen.

Requirements: R02

Preconditions:
- F0 P;390x844 browser content viewport

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open mobile navigation.
2. Visit Messages, Billing and Account Settings.
3. Close/reopen navigation.

Expected result: Primary areas remain reachable without clipped controls.

Objective acceptance criteria:

- Menu opens/closes.
- Main actions stay within the viewport.
- No horizontal page overflow is needed to read or act.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Authentication

#### T004 — Reject incorrect sign-in credentials and accept correct credentials.

Requirements: R04, R38

Preconditions:
- F0 P; private runtime password

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Enter P username with a wrong password and submit.
2. Read the error.
3. Enter the correct password and submit.

Expected result: Wrong password fails; correct password signs in.

Objective acceptance criteria:

- No authenticated records before valid login.
- Error is understandable and contains no internals.
- Correct login opens P portal.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T005 — Sign out and switch from one patient to another without refreshing.

Requirements: R04, R05

Preconditions:
- F0 P and Q have distinct names/records

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sign in as P and open a clinical record.
2. Sign out.
3. Without refreshing sign in as Q.

Expected result: Logout immediately returns to sign-in; Q sees only Q data.

Objective acceptance criteria:

- Logout navigation is immediate.
- P record is not cached visibly in Q session.
- No manual reload is needed.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Registration

#### T006 — Inspect the account-type selection and the care-team role choices.

Requirements: R08, R09

Preconditions:
- F0 signed out

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open registration.
2. Inspect Patient, Family caregiver and Care team.
3. Select Care team and inspect role choices and organization fields.

Expected result: Mutually exclusive account choices and only the four permitted applicant roles are offered.

Objective acceptance criteria:

- Three account types exist.
- Physician, Nurse, Front Desk and Billing Staff are available.
- Administrator is not a public choice.
- Organization information can be entered.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T007 — Register a family caregiver and inspect the first landing page.

Requirements: R08

Preconditions:
- F0; unused synthetic caregiver identity C_NEW

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open registration.
2. Choose Family caregiver and complete matching strong passwords.
3. Submit once.

Expected result: New caregiver lands in Family Access.

Objective acceptance criteria:

- Account is created exactly once.
- Family Access is the first authenticated landing page.
- No staff privileges appear.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T008 — Submit a care-team application and inspect its pending landing.

Requirements: R09

Preconditions:
- F0; unused synthetic applicant S_NEW

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Choose Care team and Physician.
2. Enter synthetic organization and valid account data.
3. Submit and inspect the destination.

Expected result: Applicant sees a clear pending application page.

Objective acceptance criteria:

- Pending state is explicit.
- Applicant does not receive active staff records or staff privileges before approval.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Appointments

#### T009 — Review upcoming and past appointment details and instructions.

Requirements: R10

Preconditions:
- F0 P has one upcoming and one completed appointment

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Appointments.
2. Open the upcoming appointment and review instructions.
3. Return and open the past appointment.

Expected result: Both groups and their relevant details are readable.

Objective acceptance criteria:

- Upcoming/past groups contain the correct records.
- Provider, appointment type, date/time and instructions are present.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T010 — Inspect all six appointment types when looking for a slot.

Requirements: R10

Preconditions:
- F0 contains available slots for all six specified types

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open scheduling from the patient portal.
2. Inspect appointment-type selection and available slots.

Expected result: All six specified visit types can be chosen.

Objective acceptance criteria:

- Primary Care, Follow-up, Annual Physical, Specialist Consultation, Telehealth and Laboratory Visit are selectable.
- Slot provider and date/time are readable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Laboratory

#### T011 — Browse the published laboratory result list.

Requirements: R15, R16

Preconditions:
- F0 P has published normal and abnormal results and one unpublished result

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Test Results.
2. Inspect the list and open a published result.

Expected result: Published records are discoverable with clear flags.

Objective acceptance criteria:

- Published results appear.
- Unpublished fixture does not appear.
- Normal/abnormal labels are distinguishable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T012 — Read every specified field of a laboratory result.

Requirements: R15

Preconditions:
- F0 fully populated published result LAB_FULL

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open LAB_FULL from Test Results.
2. Inspect all result information.

Expected result: All required fields match the record.

Objective acceptance criteria:

- Name, collection/result dates, value, unit, range, status, flag, ordering provider and comments are present and correct.
- No unsupported medical diagnosis is inferred.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T013 — Inspect historical measurements and a trend chart.

Requirements: R16

Preconditions:
- F0 LAB_TREND has three dated measurements of the same test/unit

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open LAB_TREND.
2. Scroll to historical measurements and chart.

Expected result: The history and chart reflect the three stored values over time.

Objective acceptance criteria:

- All three measurements can be identified.
- Chronological direction and displayed values match fixtures.
- Chart is visible and intelligible.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Medications

#### T014 — Review active medications and medication history.

Requirements: R20

Preconditions:
- F0 P has ACTIVE_MED and ENDED_MED

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Medications.
2. Inspect active medicines.
3. Open the history view.

Expected result: Active and historical medications are correctly distinguishable.

Objective acceptance criteria:

- ACTIVE_MED appears as active.
- ENDED_MED appears as history/ended and is not represented as currently active.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T015 — Read a complete prescription detail.

Requirements: R20

Preconditions:
- F0 fully populated ACTIVE_MED

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open ACTIVE_MED.
2. Review prescription details.

Expected result: Details show the complete medication information.

Objective acceptance criteria:

- Name, strength, dosage, route, frequency, start/end if applicable, provider, pharmacy, status and instructions match fixture.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Health summary

#### T016 — Review the complete health summary.

Requirements: R23

Preconditions:
- F0 P has all twelve health-summary sections populated

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Health Summary.
2. Scroll through all sections.

Expected result: Required health categories are readable.

Objective acceptance criteria:

- Demographics, conditions, allergies, medications, immunizations, medical/surgical/family/social histories, care team, vitals and preventive care are present.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Visits

#### T017 — Review a published encounter with shared notes and AVS.

Requirements: R24

Preconditions:
- F0 published VISIT_FULL with diagnosis/shared note/AVS

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Visits.
2. Open VISIT_FULL.
3. Inspect the summary and associated AVS.

Expected result: Visit detail is complete and links its AVS.

Objective acceptance criteria:

- Date, provider, department, visit type, reason, diagnoses, summary, follow-up and shared notes match fixture.
- AVS is reachable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Documents

#### T018 — Browse the available document-type choices.

Requirements: R27

Preconditions:
- F0 seven published synthetic document types

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Documents.
2. Inspect document-type filter and list.

Expected result: All seven document types are represented.

Objective acceptance criteria:

- AVS, Laboratory Report, Clinical Letter, Visit Instructions, Medication List, Billing Statement and Care Plan can be distinguished.
- Creation date and associated encounter are displayed when present.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Billing

#### T019 — Read a full unpaid invoice.

Requirements: R25

Preconditions:
- F0 INVOICE_FULL: charge180.00, adjustment115.50, responsibility64.50, paid0.00

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Billing.
2. Open INVOICE_FULL.

Expected result: Invoice fields and arithmetic are correct.

Objective acceptance criteria:

- Invoice number, service date, description, charge, adjustment, responsibility, paid, remaining, due date and status are present.
- Remaining is64.50 and status Unpaid.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T020 — Review insurance information and prior payment history.

Requirements: R25

Preconditions:
- F0 synthetic insurance and a historical paid invoice with transaction

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Billing.
2. Review insurance.
3. Open historical payment history.

Expected result: Patient can review insurance and transaction records.

Objective acceptance criteria:

- Insurance matches fixture.
- Payment date/amount and associated invoice are recognizable.
- No real card fields are required.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Messaging

#### T021 — Find received and sent conversations.

Requirements: R18

Preconditions:
- F0 P has incoming MSG_IN and outgoing MSG_OUT

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Messages.
2. Inspect Inbox and Sent.
3. Open one conversation from each.

Expected result: Both folders expose the corresponding messages.

Objective acceptance criteria:

- MSG_IN is accessible from Inbox.
- MSG_OUT is accessible from Sent.
- Thread contents match their records.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T022 — Read a conversation and its non-emergency notice.

Requirements: R18

Preconditions:
- F0 thread with P and Physician replies

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open the conversation.
2. Read messages, sender names and notice.

Expected result: Threaded messages have the correct authors and a clear non-emergency notice.

Objective acceptance criteria:

- Both authors and ordered messages are distinguishable.
- Non-emergency notice is visible near messaging controls.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Notifications

#### T023 — Browse notifications and follow one to its record.

Requirements: R36

Preconditions:
- F0 notification for a published P laboratory result

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open notifications.
2. Open the laboratory notification.

Expected result: Notification opens the associated record.

Objective acceptance criteria:

- Notification list includes event/date/read state.
- Destination is the exact linked lab result.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T024 — Inspect category-specific notification preferences.

Requirements: R36

Preconditions:
- F0 P

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Account Settings.
2. Inspect Notification preferences.

Expected result: Patient can configure event categories individually.

Objective acceptance criteria:

- Preferences exist for results, messages, appointments, cancellations, refill updates, billing and payments.
- Current state is understandable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Family access

#### T025 — Find the family-linking entry point and both consent directions.

Requirements: R31

Preconditions:
- F0 P; no pending links

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Family Access.
2. Open Link a family member.
3. Inspect invite-to-my-records and request-their-records paths.

Expected result: Both consent directions and scope selection are available.

Objective acceptance criteria:

- Visible linking action exists.
- Relationship and section scopes can be specified.
- Local delivery/no external email is disclosed.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T026 — Open an already authorized linked family profile.

Requirements: R34

Preconditions:
- F0 P proxy has Q appointments/results/visits only

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Family Access.
2. Select Q and inspect permitted section links.
3. Open Q results.

Expected result: Linked-profile context and permitted records are clear.

Objective acceptance criteria:

- Q records appear rather than P records.
- Only granted sections are offered on the family card.
- User can return to own profile.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Staff navigation

#### T027 — Find a patient and a staff work area using search and grouping.

Requirements: R37

Preconditions:
- F0 administrator

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sign in as administrator.
2. Search P.
3. Use work-area search/group filter to locate laboratory management.

Expected result: Compact searchable navigation preserves patient context.

Objective acceptance criteria:

- Search identifies P.
- Work-area search/filter narrows choices.
- Selected module visibly retains P context.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T028 — Open and close a staff record without hunting below a list.

Requirements: R37, R38

Preconditions:
- F0 administrator; P has at least12 lab results

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open P laboratory list.
2. Select a record near the start.
3. Close its detail view.

Expected result: Focused detail appears immediately and returns to the same list/context.

Objective acceptance criteria:

- Detail is not appended out of view below the list.
- Close/back action works.
- Patient/module remain selected.
- Provider/date are human readable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.


## Medium

### Registration

#### T031 — Register a patient and confirm the account persists after a fresh sign-in.

Requirements: R04, R06, R08

Preconditions:
- F0;unused synthetic P_NEW

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Choose Patient and fill valid account data plus matching strong passwords.
2. Use a password visibility control.
3. Register, sign out and sign in again.

Expected result: A durable patient account with its own portal is created.

Objective acceptance criteria:

- Matching-password registration succeeds once.
- Visibility control works accessibly.
- Re-login succeeds and identifies P_NEW.
- No pre-existing patient data is assigned.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T032 — Change the registration account type before submitting.

Requirements: R08

Preconditions:
- F0;unused synthetic identity

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Choose Care team and begin its form.
2. Change choice to Patient.
3. Complete valid patient registration.

Expected result: Final choice governs the account and landing.

Objective acceptance criteria:

- Patient account is created.
- No pending staff application or privileged role is created from abandoned choice.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T033 — Exercise required, mismatched and weak-password registration validation.

Requirements: R06, R39

Preconditions:
- F0;unused identity

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Submit an empty patient registration.
2. Enter valid identity but mismatched passwords.
3. Enter matching weak passwords.
4. Correct to a strong matching password and submit.

Expected result: Invalid submissions do not create accounts; correction works.

Objective acceptance criteria:

- Each invalid condition produces understandable feedback.
- Only final valid submission creates one account.
- Invalid values do not grant access.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Account settings

#### T034 — Edit and persist contact information.

Requirements: R04

Preconditions:
- F0 P;new synthetic email/phone/address

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Change contact fields in Account Settings and save.
2. Navigate away and return.
3. Sign out/in and inspect the profile.

Expected result: All accepted contact changes persist.

Objective acceptance criteria:

- Saved email, phone and address exactly match input after re-login.
- No unintended identity/role change.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T035 — Change a password with validation and verify old/new sign-in behavior.

Requirements: R04, R06

Preconditions:
- F0 P;private old/new strong passwords

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Try incorrect current password, then mismatched confirmation.
2. Submit correct current and strong matching new password.
3. Sign out; try old then new password.

Expected result: Invalid changes fail; valid change takes effect.

Objective acceptance criteria:

- Invalid attempts preserve old credential.
- Successful change clears sensitive fields.
- Old password is rejected and new password succeeds.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Password recovery

#### T036 — Recover a local demo password using the simulated mailbox.

Requirements: R06, R07

Preconditions:
- F0 P;local simulated delivery enabled

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Forgot password and request reset.
2. Open the clearly marked demo mailbox and its link.
3. Try mismatched new passwords then correct matching strong passwords.
4. Sign in with new password.

Expected result: Local recovery is fully operable without external email.

Objective acceptance criteria:

- Mailbox is explicitly simulated.
- Mismatch is rejected.
- Valid reset succeeds and new login works.
- Password fields clear on success.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Appointments

#### T037 — Combine provider, appointment-type and date filters.

Requirements: R10

Preconditions:
- F0 slots with different providers/types/dates plus a known match

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open scheduling.
2. Select the known provider/type/date and search.
3. Choose a date with no matching slots.

Expected result: Combined filters return only matching slots and handle empty results.

Objective acceptance criteria:

- Every returned slot matches all criteria.
- Known match appears.
- Empty case is readable and reversible.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T038 — Book a slot and verify list/dashboard persistence.

Requirements: R03, R11

Preconditions:
- F0 P;one available Primary Care slot

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Find the slot and book once.
2. Open appointment details.
3. Reload and inspect appointments and Dashboard.

Expected result: One scheduled record persists and is reflected on Dashboard.

Objective acceptance criteria:

- Exact provider/time/type match.
- One booking exists.
- Slot is no longer offered to book.
- Dashboard reflects it.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T039 — Cancel an appointment with a reason and preserve history.

Requirements: R12

Preconditions:
- F0 P;scheduled cancellable appointment

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open appointment and cancel with a unique reason.
2. Confirm.
3. Reopen history after reload.

Expected result: Cancellation is persisted with its reason.

Objective acceptance criteria:

- Appointment is absent from upcoming and present in cancellation history.
- Correct reason survives reload.
- No unrelated record changes.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T040 — Save and reopen a pre-visit questionnaire.

Requirements: R12

Preconditions:
- F0 P;future appointment

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Enter a distinctive synthetic discussion note in questionnaire.
2. Save and navigate away.
3. Reopen after reload.

Expected result: Questionnaire text persists on the same appointment.

Objective acceptance criteria:

- Exact note is visible after reload.
- Other appointments do not receive the note.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T041 — Complete simulated eCheck-In for a prepared appointment.

Requirements: R12

Preconditions:
- F0 P;confirmed appointment with completed questionnaire

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open the appointment.
2. Start eCheck-In and follow confirmations.
3. Reopen list/detail after reload.

Expected result: The appointment becomes Checked In.

Objective acceptance criteria:

- Checked In is shown consistently in detail and list.
- Persistence is verified.
- No real clinical check-in is claimed.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T042 — Submit a patient rescheduling request and inspect staff visibility.

Requirements: R13

Preconditions:
- F0 P;future scheduled appointment

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Request a new preferred date/time with a distinctive note.
2. Sign in as authorized scheduling staff.
3. Open the same appointment.

Expected result: Staff sees the request without silent date reassignment.

Objective acceptance criteria:

- Request/note persist.
- Original time remains until staff reschedules.
- Staff can identify the requested change.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Staff scheduling

#### T043 — Create a provider and available slot then find it as a patient.

Requirements: R14, R11

Preconditions:
- F0 administrator;unique provider;existing department

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Create provider and configure a future availability slot through staff UI.
2. Sign in as P and search that provider/date.

Expected result: Staff configuration makes a real bookable slot discoverable.

Objective acceptance criteria:

- Provider and availability persist.
- Exact slot appears to P.
- Invalid incomplete availability cannot silently save.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Laboratory

#### T044 — Search laboratory results by name and date range, including an empty result.

Requirements: R16

Preconditions:
- F0 multiple labs inside/outside range

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Set test name and collection interval.
2. Apply filters.
3. Change to a nonexistent test name.
4. Clear filters.

Expected result: Filtering and recovery from empty results work.

Objective acceptance criteria:

- Only matching records appear initially.
- Empty state is explicit.
- Clearing restores the full published list.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T045 — Compare normal/abnormal values and supported result statuses.

Requirements: R15, R16

Preconditions:
- F0 published Pending/Preliminary/Final/Corrected tests;values below/inside/above their ranges

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open each fixture result.
2. Compare its status, units, range and flag to the fixture inventory.

Expected result: Statuses and normal/abnormal semantics are accurate.

Objective acceptance criteria:

- All four statuses render correctly.
- In-range/below/above classifications match each test-specific range.
- No diagnosis is invented.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Messaging

#### T046 — Compose a categorized message to a care team and find it in Sent.

Requirements: R18

Preconditions:
- F0 P;eligible care team;unique subject/body

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Start a new message.
2. Inspect the five category choices, select Medication Question and recipient/team.
3. Send once and open Sent.

Expected result: A single correctly addressed persisted thread is created.

Objective acceptance criteria:

- Five specified categories are available.
- Subject/body/category/recipient match.
- One thread appears in Sent after reload.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T047 — Read an unread thread and reply without losing conversation history.

Requirements: R18, R36

Preconditions:
- F0 P;unread incoming thread

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Record unread count.
2. Open thread and reply once.
3. Return to list/dashboard then reopen.

Expected result: Reading updates unread state and reply extends the same thread.

Objective acceptance criteria:

- Unread count decreases appropriately.
- Original and new reply remain in the same thread with correct sender.
- Reload preserves them.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T048 — Archive a conversation with confirmation and destination feedback.

Requirements: R19

Preconditions:
- F0 P;unarchived thread

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open thread and choose Archive.
2. Confirm.
3. Inspect destination folder and reopen archived thread.

Expected result: User lands in Archive with explicit success.

Objective acceptance criteria:

- Confirmation exists.
- Archive tab is selected and thread visible.
- Specific archived success feedback appears.
- Archived detail offers Restore rather than Archive.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T049 — Restore an archived conversation with confirmation and Inbox navigation.

Requirements: R19

Preconditions:
- F0 P;archived thread with multiple messages

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open archived thread and choose Restore to inbox.
2. Confirm.
3. Inspect Inbox and reopen thread.

Expected result: User lands in Inbox with visible restored conversation and specific success.

Objective acceptance criteria:

- Confirmation and selected Inbox are present.
- Restored thread is visible.
- Messages/participants preserved.
- Only applicable Archive action remains.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T050 — Cancel Archive and Restore confirmation without changing state.

Requirements: R19

Preconditions:
- F0 P;one archived and one unarchived thread

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Start Archive on unarchived thread and cancel.
2. Start Restore on archived thread and cancel.
3. Reload both folders.

Expected result: Both cancellations leave state unchanged.

Objective acceptance criteria:

- Original folders and messages remain unchanged.
- No success mutation is reported.
- Detail remains usable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Medications

#### T051 — Search active and historical medications and recover from no matches.

Requirements: R20

Preconditions:
- F0 multiple active/ended medicines

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Search a known medicine.
2. Search nonexistent text.
3. Clear search and inspect history.

Expected result: Search limits results accurately with a usable empty state.

Objective acceptance criteria:

- Known result matches query.
- Nonmatch displays no unrelated medicines.
- Clearing restores records/history.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Refills

#### T052 — Request a simulated refill with a care-team note.

Requirements: R21

Preconditions:
- F0 ACTIVE_MED;no pending refill

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open active medicine, enter unique note and request refill.
2. Reload detail.

Expected result: A persistent Requested refill is created.

Objective acceptance criteria:

- Exactly one request exists for the correct medication/patient.
- Submitted note is retained.
- Status is Requested and no real dispensing occurs.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T053 — Review, approve and complete an existing refill with a decision note.

Requirements: R21

Preconditions:
- F0 requested refill;authorized clinical staff

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As staff mark Under Review.
2. Mark Approved then Completed with decision note.
3. Sign in as P and inspect medicine.

Expected result: Patient sees staff progress and final decision.

Objective acceptance criteria:

- Transitions persist in order.
- Completed and exact final note appear for the same request.
- No duplicated refill record.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Corrections

#### T054 — Report a medication information discrepancy and review it as staff.

Requirements: R22

Preconditions:
- F0 ACTIVE_MED with known pharmacy

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P request pharmacy correction with unique text.
2. As staff open correction request and mark reviewed.
3. Reopen patient medicine.

Expected result: Correction is tracked without silently altering verified medication.

Objective acceptance criteria:

- Staff receives exact request for P.
- Reviewed state persists.
- Original pharmacy remains unless explicitly changed by staff.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T055 — Submit a health-summary correction without directly altering official history.

Requirements: R22, R23

Preconditions:
- F0 P with a known allergy/history entry

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open Health Summary and request a correction.
2. Reload summary.
3. As staff inspect and review request.

Expected result: Patient request and official data remain distinguishable.

Objective acceptance criteria:

- Request persists with correct patient/topic.
- Original clinical value is unchanged by submission.
- Review is visible in staff workflow.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Health summary

#### T056 — Maintain an official synthetic clinical-history entry from staff UI.

Requirements: R22, R23

Preconditions:
- F0 authorized clinical staff;P history fixture

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Locate P clinical history.
2. Edit a clearly identified history entry.
3. Sign in as P and inspect Health Summary.

Expected result: Authorized staff edits persist into patient summary.

Objective acceptance criteria:

- Exact edited content appears in correct section.
- Patient identity/context preserved.
- Unrelated patient history unchanged.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Visits

#### T057 — Create and publish a synthetic encounter with shared information.

Requirements: R24

Preconditions:
- F0 authorized staff;P;unique encounter content

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Create encounter, diagnosis and shared note with follow-up.
2. Publish through available staff controls.
3. As P open Visits and the new encounter.

Expected result: Published encounter information becomes patient-visible.

Objective acceptance criteria:

- Correct patient/provider/date/type/reason/diagnosis/summary/follow-up/shared note appear.
- Record persists after reload.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Documents

#### T058 — Filter documents by type and follow its associated encounter.

Requirements: R27

Preconditions:
- F0 document set includes multiple types and one linked AVS

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Filter Documents to AVS.
2. Open the linked AVS and associated visit.
3. Clear filter.

Expected result: Filtering and document-encounter navigation are accurate.

Objective acceptance criteria:

- Only AVS appears while filtered.
- Linked encounter matches fixture.
- Clearing restores all published documents.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### PDF exports

#### T059 — Preview, print and download a laboratory report PDF.

Requirements: R28, R29

Preconditions:
- F0 LAB_FULL

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open lab website preview.
2. Use Print and dismiss the print dialog.
3. Download PDF and inspect file.

Expected result: Readable preview and a real authorized PDF represent the same lab.

Objective acceptance criteria:

- Print opens.
- File MIME is application/pdf and name is descriptive .pdf.
- Values/units/range/status/patient/provider/reference/dates/branding/disclaimer/page number agree with preview.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T060 — Preview, print and download an After Visit Summary PDF.

Requirements: R28, R29

Preconditions:
- F0 VISIT_FULL linked AVS

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open AVS website preview from visit.
2. Use Print then dismiss.
3. Download and inspect PDF.

Expected result: AVS has a professional web preview and matching PDF.

Objective acceptance criteria:

- Print works.
- PDF format/MIME/name correct.
- Patient/provider/reference/dates/summary/follow-up/disclaimer/page number match preview.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T061 — Preview and download an exact-amount billing statement.

Requirements: R25, R28, R29

Preconditions:
- F0 INVOICE_FULL

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open invoice statement preview.
2. Use Print then dismiss.
3. Download statement PDF.

Expected result: Statement preview and PDF preserve exact financial values.

Objective acceptance criteria:

- Real PDF and descriptive filename.
- Charge180.00, adjustment115.50, responsibility64.50, paid0.00, remaining64.50 agree.
- Branding/reference/date/patient/disclaimer/page numbering present.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T062 — Preview and download a simulated payment receipt.

Requirements: R25, R28, R29

Preconditions:
- F0 receipt for payment20.25 against INVOICE_FULL

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open payment from history and receipt preview.
2. Use Print then dismiss.
3. Download receipt PDF.

Expected result: Receipt is readable, identified and accurate.

Objective acceptance criteria:

- Real PDF/MIME/descriptive filename.
- Invoice reference, transaction reference, date, patient and amount20.25 match preview.
- Simulated disclaimer and page number present.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Billing

#### T063 — Make a partial simulated payment and reconcile balances.

Requirements: R25, R26, R03

Preconditions:
- F0 INVOICE_FULL remaining64.50

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Pay20.25 once.
2. Open invoice/history and Dashboard after reload.

Expected result: Payment persists and balance becomes44.25.

Objective acceptance criteria:

- Exactly one20.25 transaction.
- Paid20.25/remaining44.25/Partially Paid on invoice.
- Dashboard reflects correct total.
- No card information required.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T064 — Pay the exact remaining balance and inspect paid state.

Requirements: R25

Preconditions:
- F0 invoice with20.25 already paid and44.25 remaining

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Submit one44.25 simulated payment.
2. Reload invoice and payment history.

Expected result: Invoice becomes fully paid with zero remaining.

Objective acceptance criteria:

- Paid64.50, remaining0.00, Paid status.
- Both distinct transactions remain.
- Receipt for44.25 is available.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T065 — Create a synthetic invoice as authorized billing staff.

Requirements: R25, R36

Preconditions:
- F0 billing staff and P;new invoice responsibility37.80

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Create invoice with explicit service/due dates, charges and adjustment.
2. As P open Billing and notifications.

Expected result: New invoice and outstanding balance are reflected in patient portal.

Objective acceptance criteria:

- Exact invoice values persist.
- Total increases by37.80.
- New statement notification points to this invoice.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Notifications

#### T066 — Mark one notification read, then mark the remaining notifications read.

Requirements: R36

Preconditions:
- F0 P has at least3 unread notifications

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Mark one read.
2. Reload.
3. Mark remaining/all read using available controls and reload.

Expected result: Read states persist without deleting notifications.

Objective acceptance criteria:

- First operation changes only selected notification.
- Final unread count is zero.
- All original notification records remain accessible.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T067 — Mute one category, generate a matching event, then restore that preference.

Requirements: R36

Preconditions:
- F0 P;notification preferences enabled;staff can publish lab

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Mute Test result and save.
2. Staff publishes a new P lab.
3. Inspect patient notifications and existing notices.
4. Re-enable Test result and publish a second lab.

Expected result: Category preference governs new notifications and preserves existing ones.

Objective acceptance criteria:

- Muted event creates no new patient result notification.
- Existing notices remain.
- Other categories unchanged.
- Re-enabled event creates a result notification.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Family access

#### T068 — Invite an existing family account to selected own-record sections.

Requirements: R31, R32, R34

Preconditions:
- F0 P and Q;no relationship

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P invite Q with relationship and results/visits scopes.
2. Inspect pending outgoing request.
3. As Q explicitly accept incoming request.
4. Open linked P profile.

Expected result: Explicit consent creates only selected scoped access.

Objective acceptance criteria:

- Before acceptance no access.
- Incoming/outgoing status/expiry/relationship/scopes visible.
- After acceptance Q sees P results/visits only.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T069 — Request access to another adult and obtain that owner consent.

Requirements: R31, R32, R34

Preconditions:
- F0 P requester,Q owner;no relationship

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P request Q records with appointments scope.
2. As Q inspect incoming request and accept.
3. As P open Q appointments.

Expected result: Owner acceptance grants the requested scope.

Objective acceptance criteria:

- No access before Q acceptance.
- Correct direction ownerQ/proxyP.
- Only appointments scope granted.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T070 — Decline one invitation and cancel a different pending invitation.

Requirements: R31, R33

Preconditions:
- F0 two distinct pending invitations for different synthetic recipients

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Intended recipient declines first request.
2. Sender cancels second pending request.
3. Reload both sides.

Expected result: Decline and cancellation persist without granting access.

Objective acceptance criteria:

- Both statuses are clear.
- No proxy links are created.
- Neither request remains actionable for acceptance.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.


## Hard

### Authorization

#### T071 — Attempt another unrelated patient record and direct PDF access.

Requirements: R04, R30, R39

Preconditions:
- F0 P and unrelatedQ;private manifest includes Q detail/export URLs

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sign in as P.
2. Enter Q lab, visit, invoice and document URLs supplied in task data.
3. Attempt their PDF URLs.

Expected result: Object authorization denies every unrelated resource.

Objective acceptance criteria:

- No Q protected content/file returned.
- Readable denial/unavailable state with recovery path.
- P own records remain usable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T072 — Verify protected links after logout and through browser Back.

Requirements: R04, R05, R30, R39

Preconditions:
- F0 P;own lab/document/export URLs

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sign in, open protected record, then sign out.
2. Use Back and refresh.
3. Open direct detail/export URLs without signing in.

Expected result: Signed-out access never reveals authenticated record data.

Objective acceptance criteria:

- No stale protected display after logout/back.
- Requests require authentication.
- Direct exports cannot be downloaded anonymously.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Staff onboarding

#### T073 — Approve a care-team applicant only after a required verification note.

Requirements: R09, R39

Preconditions:
- F0 pending Physician applicant and administrator

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As applicant try staff workspace.
2. As administrator try approval with empty note.
3. Provide synthetic verification note and approve.
4. Re-login applicant.

Expected result: Only reviewed approval activates staff access.

Objective acceptance criteria:

- Pending access denied.
- Empty-note approval rejected.
- Approved applicant gains Physician workspace only.
- Administrator role was never publicly assignable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T074 — Decline a care-team application and verify continued access denial.

Requirements: R09, R39

Preconditions:
- F0 pending Nurse applicant and administrator

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Decline with required synthetic decision note.
2. As applicant reload/re-login and try staff record URLs.

Expected result: Declined account is clearly informed and unprivileged.

Objective acceptance criteria:

- Decline persists.
- Staff records remain unavailable.
- No role escalation or cached pending/approved state grants access.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Family access

#### T075 — Try claiming an invitation by changing another account email.

Requirements: R32, R39

Preconditions:
- F0 invitation to Q original registered identity;unrelatedR

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As R edit profile email to the invitation email if permitted.
2. Inspect incoming requests and attempt supplied invitation accept URL.
3. As Q inspect genuine invitation.

Expected result: Profile email editing cannot steal recipient-bound consent.

Objective acceptance criteria:

- R never gains acceptance authority or record access.
- Q remains intended recipient.
- Invalid attempt leaves invitation state unchanged.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T076 — Invite a not-yet-registered synthetic family member and accept after signup.

Requirements: R31, R32

Preconditions:
- F0 P;unused recipient identityN

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P invite N email with chosen scope.
2. Register N using intended synthetic email.
3. Open incoming invitation and explicitly accept.

Expected result: Invitation binds to the intended newly created account.

Objective acceptance criteria:

- Registration alone grants no access.
- Correct invitation appears for N.
- Explicit consent creates correct scoped link.
- Other account cannot claim it.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T077 — Reject duplicate pending requests and an expired acceptance.

Requirements: R33

Preconditions:
- F0 active pending invitation and separate expired invitation fixture

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Sender attempts duplicate of pending request.
2. Recipient opens expired invitation and attempts acceptance.
3. Inspect status/links.

Expected result: Duplicate and expired requests cannot grant unintended access.

Objective acceptance criteria:

- Only one original pending request remains.
- Expired request cannot accept.
- Feedback is readable and no proxy link created.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T078 — Prevent reused or old invitations from restoring revoked access.

Requirements: R33

Preconditions:
- F0 accepted invitation plus link subsequently revoked by owner

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As former proxy revisit old acceptance link and try accepting again.
2. Refresh linked profiles and attempt old protected URL.

Expected result: Consumed consent cannot silently re-enable access.

Objective acceptance criteria:

- No active link restored.
- Old invitation rejected as used/unavailable.
- Formerly shared record remains denied.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T079 — Enforce section scopes on visible navigation and direct exports.

Requirements: R30, R34

Preconditions:
- F0 Q permits P results only;Q also has billing/documents/visits

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P open Q family profile and allowed lab.
2. Attempt supplied Q billing, visits, document and export URLs.

Expected result: Results permission does not imply access to other sections.

Objective acceptance criteria:

- Allowed result works.
- Disallowed section controls are absent from linked card.
- All disallowed direct pages/files denied.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T080 — Revoke a live proxy grant and check already-open record access.

Requirements: R30, R33, R34

Preconditions:
- F0 active Q-to-P results grant;two separate authenticated browser profiles

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P open Q result and record export link.
2. In Q profile revoke grant.
3. Return P, refresh detail and try export/linked profile.

Expected result: Revocation takes effect on subsequent requests.

Objective acceptance criteria:

- Refreshed data/export denied.
- Link no longer active.
- Readable recovery path; no internal model/query error.
- Revocation audit recorded.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Appointments

#### T081 — Attempt to book the same slot from two patients with stale availability.

Requirements: R11

Preconditions:
- F0 one free slot;two isolated P/Q sessions both opened to slot before booking

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P book slot.
2. Switch Q stale page and try booking same slot.
3. Inspect both appointment lists.

Expected result: Exactly one booking wins and the other receives a conflict.

Objective acceptance criteria:

- One active booking for slot in persisted state.
- Losing patient has no duplicate appointment.
- Error readable and other available slots remain searchable.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T082 — Reject unavailable scheduling and invalid appointment state changes.

Requirements: R11, R12, R14

Preconditions:
- F0 unavailable slot and cancelled appointment;authorized scheduling staff

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Try booking unavailable slot via supplied stale UI.
2. As staff inspect cancelled appointment and try an invalid check-in/completion transition if offered.
3. Reload records.

Expected result: Availability and transition rules prevent inconsistent records.

Objective acceptance criteria:

- Unavailable slot not bookable.
- Cancelled record cannot silently become Checked In or Completed without a legitimate new scheduling workflow.
- Invalid controls absent or rejected; records unchanged.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

#### T083 — Check earliest-first ordering and timezone consistency across views.

Requirements: R10, R13

Preconditions:
- F0 three future appointments deliberately created out of chronological order;one crosses UTC/local date boundary

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Inspect Dashboard and upcoming list.
2. Open each detail and staff record.
3. Compare displayed instants and zone labels.

Expected result: Ordering follows time and date/timezone presentation is consistent.

Objective acceptance criteria:

- Earliest appointment first in upcoming views.
- All views describe same instant for each appointment.
- Zone is explicit or consistently documented; no day/time shift error.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Password recovery

#### T084 — Reject expired and reused local reset links.

Requirements: R06, R07

Preconditions:
- F0 separate expired reset fixture and unused valid reset link in private simulated mailbox

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open expired link and attempt reset.
2. Use valid link to reset once.
3. Reopen used link and try another reset.

Expected result: Expired/used links cannot reset credentials.

Objective acceptance criteria:

- Expired attempt fails.
- Valid link works once only.
- Reuse fails; password from successful reset remains valid.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Refills

#### T085 — Reject a second pending refill with patient-friendly feedback.

Requirements: R21

Preconditions:
- F0 ACTIVE_MED with Requested refill

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open medication and attempt another refill.
2. Repeat while original is Under Review using separate reset fixture stage.

Expected result: No duplicate pending request is created.

Objective acceptance criteria:

- One request remains in each stage.
- Feedback explains existing request/status, not generic conflict internals.
- Patient can still see original progress.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Billing

#### T086 — Validate payment boundaries and prevent double processing.

Requirements: R25, R26, R39

Preconditions:
- F0 remaining64.50;isolated simulation

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Attempt empty, zero, negative and amount64.51.
2. Correct to20.25 and trigger rapid double-click on submit.
3. Reload history.

Expected result: Invalid amounts are rejected and one intended payment posts once.

Objective acceptance criteria:

- No transaction for invalid attempts.
- Exactly one20.25 transaction after double submit.
- Remaining44.25.
- No real card or payment provider involved.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Laboratory

#### T087 — Withdraw a previously published result and test saved detail/PDF links.

Requirements: R17, R30

Preconditions:
- F0 published LAB_FULL;patient has opened detail and saved export link

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As staff unpublish LAB_FULL.
2. As patient refresh detail, search list and try saved PDF URL.

Expected result: Withdrawn data is inaccessible at every surface.

Objective acceptance criteria:

- Not in published list.
- Direct detail/PDF denied.
- Friendly unavailable message and route back.
- Other published results still work.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Visits and documents

#### T088 — Hide private notes and unpublished visits/documents including direct exports.

Requirements: R24, R27, R30

Preconditions:
- F0 public encounter with shared/private notes plus unpublished encounter/document

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. As P inspect public encounter.
2. Try private/unpublished item URLs and PDF exports supplied in manifest.

Expected result: Only explicitly shared published information is exposed.

Objective acceptance criteria:

- Shared note visible, private note absent.
- Unpublished encounter/document denied through direct page and export.
- Files reveal no private text.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### PDF exports

#### T089 — Read and export a long multi-page clinical document.

Requirements: R28, R29

Preconditions:
- F0 LONG_DOC with long paragraphs, long words and end marker;at least3 PDF pages expected

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Open web preview.
2. Download PDF.
3. Inspect first/middle/last pages and print preview.

Expected result: Long content wraps and paginates without loss.

Objective acceptance criteria:

- Real PDF has at least3 pages and page numbers.
- No clipped/overlapping text.
- First/middle/end markers retained.
- Branding/disclaimer/identification present; preview and PDF content agree.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Staff navigation

#### T090 — Use staff module search and a record drawer on a narrow screen with keyboard.

Requirements: R02, R37

Preconditions:
- F0 staff;390x844;P multiple records

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Use keyboard to reach module selector/search.
2. Choose P lab module and open a record.
3. Navigate focused controls and close drawer using available keyboard action.
4. Return to list.

Expected result: Staff navigation is accessible without horizontal overflow or lost context.

Objective acceptance criteria:

- Controls reachable by keyboard with visible focus.
- Drawer opens in viewport and closes.
- Patient/module preserved.
- No clipped essential action or horizontal page overflow.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.


## Expert

### Scheduling end-to-end

#### T091 — Complete booking, staff rescheduling and cancellation with consistent history.

Requirements: R03, R11, R12, R13, R14, R36

Preconditions:
- F0 P;two valid future slots;independent older cancelled appointment

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Book first slot as P and inspect Dashboard.
2. Request reschedule.
3. As staff move to second slot.
4. Verify replacement opens immediately.
5. As P inspect replacement then cancel with new reason.
6. Inspect history and notifications.

Expected result: Whole scheduling lifecycle remains consistent across roles.

Objective acceptance criteria:

- Original booking becomes cancelled due to reschedule; replacement has correct slot.
- Independent old cancellation is retained.
- Replacement opens after staff action.
- Final upcoming excludes cancelled replacement.
- Reasons, history, dashboard and relevant notifications agree.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Laboratory end-to-end

#### T092 — Create, publish, correct and withdraw a result across staff and patient views.

Requirements: R15, R16, R17, R28, R30, R36

Preconditions:
- F0 P with same-test history;authorized staff;unique new test record

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Staff creates unpublished result.
2. Patient verifies absence.
3. Staff publishes.
4. Patient follows notification, checks details/trend and downloads PDF.
5. Staff corrects result value/status then patient reopens.
6. Staff withdraws; patient retries saved links.

Expected result: Publication/correction/withdrawal consistently governs all representations.

Objective acceptance criteria:

- Unpublished absent; published notified.
- Patient/trend/PDF use current corrected value and status after correction.
- Withdrawal blocks list/detail/export.
- No unsupported diagnosis; unrelated tests unchanged.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Messaging end-to-end

#### T093 — Exchange messages across roles and verify per-user archive independence.

Requirements: R18, R19, R36

Preconditions:
- F0 P and Physician;unique subject

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Patient composes Medical Question.
2. Physician reads and replies.
3. Patient follows notification and reads reply.
4. Patient archives thread.
5. Physician confirms thread remains accessible.
6. Patient restores it to Inbox and reopens.

Expected result: Communication and folder/read states are persistent and user-specific.

Objective acceptance criteria:

- Correct recipients/authors/thread history.
- Notification and unread transition accurate.
- Patient archive does not archive physician view.
- Archive/restore confirmations and destination navigation work.
- No message lost/duplicated.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Refills end-to-end

#### T094 — Resolve a denied refill then process a separate new request to completion.

Requirements: R20, R21, R36, R40

Preconditions:
- F0 active medicine;no pending refill;authorized staff

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Patient requests refill with note.
2. Staff reviews and denies with reason.
3. Patient reads denial.
4. Patient submits a distinct new request.
5. Staff reviews, approves and completes it with final note.
6. Patient inspects history and notifications.

Expected result: Distinct decisions/history are preserved through the full simulated lifecycle.

Objective acceptance criteria:

- Denied request stays denied with reason.
- New request is separately tracked.
- Final request Completed with correct note.
- Progress/notifications and refill decision audit match.
- No real prescription transmission.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Billing end-to-end

#### T095 — Create an invoice, partially pay, finish paying and reconcile both receipts.

Requirements: R03, R25, R26, R28, R36, R40

Preconditions:
- F0 billing staff and P;unique invoice responsibility64.50

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Staff creates invoice.
2. Patient follows statement notification and previews bill.
3. Pay20.25, inspect partial balance and receipt.
4. Pay44.25, inspect final balance and second receipt.
5. Reopen Dashboard and history.

Expected result: Ledger, UI, PDFs and notifications reconcile to64.50.

Objective acceptance criteria:

- Exactly two transactions20.25/44.25.
- Intermediate44.25 and final0.00 balances.
- Two correct receipt PDFs.
- Dashboard/notifications reflect changes.
- Billing audit entries exist; no duplicate processing.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Family access end-to-end

#### T096 — Complete scoped invitation, owner revocation and a new consent after revocation.

Requirements: R30, R31, R32, R33, R34, R40

Preconditions:
- F0 adult P owner,Q proxy;no links

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. P invites Q results only.
2. Q accepts and views allowed result but cannot billing export.
3. P revokes.
4. Q retries old link/old invitation.
5. P sends a genuinely new invitation with visits only.
6. Q accepts and checks new scopes.

Expected result: Revocation cannot be bypassed; only fresh consent establishes new access.

Objective acceptance criteria:

- Old invite cannot restore access.
- Fresh invitation requires new explicit acceptance.
- New access permits visits only, not prior results/billing.
- Proxy-change audit reflects grants/revocation accurately.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Guardian verification

#### T097 — Request dependent access, deny self-approval, then verify an administrator decision.

Requirements: R31, R34, R35, R39, R40

Preconditions:
- F0 minor D;requesterG;administrator;no grant

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. G requests guardian/dependent access.
2. Inspect pending state and attempt dependent record access.
3. Administrator tries decision without note, then enters synthetic verification and approves specific scopes.
4. G opens permitted dependent section.
5. Administrator revokes; G retries.

Expected result: Guardian access is gated by recorded administrator verification.

Objective acceptance criteria:

- No self-grant before decision.
- Required verification note enforced.
- Granted scopes honored; revocation denies next access.
- Synthetic identity/guardian limitations disclosed.
- Audit records decision and revocation.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Account recovery end-to-end

#### T098 — Recover access after a failed reset, then validate session/account isolation.

Requirements: R04, R05, R06, R07, R39

Preconditions:
- F0 P and Q;local mailbox;P authenticated in separate isolated browser profile;expired and valid reset fixtures

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Attempt expired link then request valid recovery through UI.
2. Correct mismatch and complete reset from local mailbox.
3. Try old/new password.
4. Check already-open P authenticated page after refresh.
5. Sign out and sign in as Q without reload.

Expected result: Recovery yields one valid new credential without stale cross-account access.

Objective acceptance criteria:

- Expired/mismatched attempts do not alter password.
- New credential works, old fails.
- Existing sessions do not expose unauthorized post-reset content if invalidated; no cross-account leakage.
- Q sees only Q data.
- No external mail dependency.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Care-team onboarding end-to-end

#### T099 — Onboard all four permitted staff roles and verify their appropriate workspaces.

Requirements: R08, R09, R14, R18, R21, R25, R39

Preconditions:
- F0 administrator;four unused applicants with synthetic organizations

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Register Physician, Nurse, Front Desk and Billing Staff separately.
2. Verify each pending restriction.
3. Administrator reviews each with verification note and approves.
4. Re-login each and perform one role-appropriate action: clinical reply, refill review, scheduling update, invoice creation.

Expected result: Approved roles enter appropriate workspaces and execute authorized workflows.

Objective acceptance criteria:

- All pending users denied staff records.
- Four recorded approvals with notes.
- Each final role equals approved role, not Administrator.
- Role-appropriate changes persist and appear for relevant patient; no privilege from public selection alone.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.

### Audit and error recovery

#### T100 — Verify an audited cross-module staff session and recover from a missing record.

Requirements: R14, R17, R21, R25, R34, R38, R39, R40

Preconditions:
- F0 authorized administrator and clinical/billing fixtures;read-only audit verifier enabled

Test data: Independent reset of F0 plus the named fixture; substitute TEST_ID and RUN_ID in all new labels. Credentials are injected privately at runtime, never stored in this suite.

Expected workflow:

1. Log in and open P record.
2. Update appointment, publish a result, edit medication, decide refill, change proxy permission and record simulated billing change.
3. Open supplied nonexistent record URL.
4. Use recovery navigation and reopen P.

Expected result: Important events are auditable and missing-record errors do not strand the user.

Objective acceptance criteria:

- Read-only audit inspection finds actor/time/target/action for login, access and all six mutations.
- Error contains no internal model/query message and has usable return path.
- P context and durable changes remain correct.
- No real medical/payment operation.

Review the screenshots/action trace against EVERY criterion; inspect read-only persisted state or downloaded files where required. Agent self-report alone cannot establish PASS.
