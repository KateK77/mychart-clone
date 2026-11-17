# CareConnect 3.0 — Complete Requirements Specification

**Release:** 3.0.0 · **Development round:** 3 · **Requirements edition:** November 16, 2026 · **Repository:** KateK77/mychart-clone

This document defines the complete requirements for CareConnect 3.0. It can be read and implemented independently; no earlier prompt, feedback log, or conversation is required. It specifies expected behavior, not a claim that every requirement has passed verification.

## 1. Product purpose and scope

CareConnect is a standalone patient portal and simulated hospital workspace inspired by MyChart workflows. Patients and staff use the same persistent database, so a request made in the patient portal becomes an actionable record in the staff workspace, and staff decisions appear in the patient portal.

Deliver a complete working application covering appointments, laboratory results, messages, medications, refills, health history, visits, documents, billing, family access, notifications, and account settings. Buttons must perform validated operations and persist their results; a success message alone is insufficient. The application must run locally without an existing EHR, hospital API, or paid third-party service.

CareConnect is an independent synthetic-data research prototype, not an Epic Systems or MyChart product. Use original branding and assets. Display **“DEMO — SYNTHETIC DATA ONLY — NOT FOR CLINICAL USE.”** throughout the application. Do not use real patient information, transmit real prescriptions, process real payments, or claim clinical certification or HIPAA compliance.

## 2. Architecture and technology

| Layer | Required technology and responsibility |
| --- | --- |
| Frontend | React, TypeScript, Vite, Tailwind CSS, React Router, and TanStack Query; responsive routing, forms, and server-state presentation |
| Backend | Python, Django, and Django REST Framework; authentication, validation, permissions, transactions, and audit events |
| Persistence | SQLite for local development; PostgreSQL-compatible deployment configuration; migrations and a repeatable synthetic seed command |
| Automated verification | pytest/pytest-django, Vitest, React Testing Library, and Playwright for unit, integration, and browser workflows |

Use a modular architecture with a shared data model between patient and staff interfaces. Persist business state on the server. Refresh or invalidate affected frontend queries after mutations so dashboards, lists, details, and counters remain consistent. Local frontend requests must reach the matching backend through a same-origin development proxy. Configuration and secrets belong in environment variables, with documented examples and safe defaults.

## 3. Interface, navigation, and accessibility

All product copy, validation messages, documentation, and newly seeded records must be in English. Use clear typography, white backgrounds, blue/teal accents, and readable labels. Support desktop, tablet, and narrow mobile layouts without horizontal clipping.

Patient navigation must provide Dashboard, Appointments, Messages, Test Results, Medications, Health Summary, Visits, Billing, Documents, Family Access, and Account Settings. Include a notification entry point, a discoverable sign-out control, and breadcrumbs or equivalent return navigation.

Staff navigation must use categorized work areas, search, group filters, and a compact module selector. Selecting a record must immediately open a focused detail drawer with a visible title and close/back control. Preserve the selected patient and work area while inspecting or closing records. Do not insert the selected detail below a long list where it is difficult to discover. Support keyboard navigation, Escape-to-close behavior, accessible labels, visible focus, and usable mobile drawers.

Provide loading, empty, validation, success, and error states. Explain unavailable records and missing permissions in plain English with a way back. Do not expose internal model names, query exceptions, or raw server tracebacks. Display patient/provider names and readable dates instead of bare database IDs or raw ISO timestamps. Financial amounts, laboratory units, reference ranges, and status labels must remain legible.

Confirm destructive or consequential changes where appropriate. Canceling a confirmation must leave data unchanged. A failed operation must not display success or discard information needed to retry manually.

## 4. Accounts, registration, and authentication

Provide a dedicated registration route that first asks the visitor to choose exactly one account type: **Patient**, **Family caregiver**, or **Care team**. Show the appropriate form after selection and allow the visitor to change the selection before submitting. All forms require validated identity/contact fields and confirmed passwords.

| Account type | Registration requirements | Landing and access |
| --- | --- | --- |
| Patient | Patient account details and confirmed password | Patient portal with the account's own records |
| Family caregiver | Caregiver account details and confirmed password | Family Access; other patients' records require a separate authorized relationship |
| Care team | Choose Physician, Nurse, Front Desk, or Billing Staff; supply organization details and confirmed password | Pending-application page until administrator approval |

Administrator must not be an option in public registration. Selecting a staff role must create an application, not immediately grant privileges. Pending and declined applicants must not access staff records or APIs.

Provide an administrator Access reviews area for care-team applications. Review must include a required verification/decision note and an approve or decline action. Approval grants only the approved role and sends the account to the corresponding workspace on subsequent access. Preserve application status and audit the decision. This is simulated verification of synthetic identities, not proof of professional credentials.

Provide deterministic demo accounts for patients, a caregiver, Physician, Nurse, Front Desk, Billing Staff, and Administrator. Seeded staff accounts may be preauthorized for local demonstration.

### Sessions, profiles, and passwords

Implement login, logout, secure password hashing, profile editing, password change, and session management. Profile editing covers contact information such as email, phone, and address. Validate current credentials before a password change.

Registration, password change, and password recovery must require the new password twice, enforce matching values and password-strength validation, provide accessible visibility controls, and clear password fields after success. Incorrect current passwords and invalid forms must be rejected with readable feedback.

Sign-out must invalidate the session, clear cached identity and patient data, and return immediately to sign-in. Switching accounts must work without reloading the browser and must not briefly expose the previous account's records.

Provide a discoverable Forgot password flow using expiring, single-use reset links in a clearly labeled local simulated mailbox. Isolate the mailbox to the requesting browser session; do not send external email. Reject expired, reused, and superseded links, and invalidate prior authenticated sessions after a successful reset. Protect recovery operations with CSRF validation and abuse controls. Clearly disclose that the mailbox is a local synthetic-data facility.

## 5. Patient dashboard

Show the current patient's name, upcoming appointments, recent test results, unread messages, current medications, outstanding balance, recent visits, and important notifications. Provide working shortcuts for Schedule Appointment, Send Message, View Test Results, Request Refill, and Pay Bill.

All counts, balances, and summaries must derive from persisted records and current access permissions. Upcoming appointments are ordered earliest first. Each dashboard entry must lead to the corresponding authorized list or record. Account/profile changes must not leave another patient's information in the dashboard cache.

## 6. Appointments and scheduling

Patients must be able to view upcoming and past appointments, search available slots, filter by provider, appointment type, and date, select a time, book, inspect instructions, save a pre-visit questionnaire, complete simulated eCheck-In, request rescheduling, and cancel with a reason.

Supported appointment types are Primary Care, Follow-up, Annual Physical, Specialist Consultation, Telehealth, and Laboratory Visit. Represent slot availability and appointment states clearly: Available, Scheduled, Confirmed, Checked In, Completed, Cancelled, and No Show, as applicable to the record.

Authorized scheduling staff must manage providers, departments, availability, appointments, and valid status changes. The backend must validate provider availability, prevent double booking transactionally, reject scheduling conflicts, enforce state transitions, and apply consistent timezone handling.

Questionnaire answers, check-in status, rescheduling requests, and cancellation reasons must survive reload. A staff reschedule must reserve the replacement slot, preserve the original appointment as a historical cancellation with its reason, and open the replacement appointment immediately. Retain separate cancellation events as separate history records. Upcoming lists and the dashboard must show the current appointment in chronological order.

## 7. Laboratory results

Provide a result list with test-name search and collection-date filtering, a dedicated detail view, historical measurements, a trend chart, and a downloadable summary. Each result must include its name, collection date, result date, value, unit, reference interval, status, abnormal flag, ordering provider, and comments.

Support Pending, Preliminary, Final, and Corrected result statuses. Associate reference intervals with the relevant test and units; show in-range and abnormal values clearly without inferring a diagnosis. Charts must correspond to the displayed test's historical measurements and expose understandable dates and values.

Authorized staff must create, edit, publish, correct, and withdraw synthetic results. Newly created unpublished results must not be visible to patients. Publication makes the authorized result available and creates an appropriate notification. Withdrawal must remove access from lists, saved detail links, and downloads. Result status and publication visibility are distinct fields.

## 8. Secure messaging

Provide Inbox, Sent, and Archive folders, message details, threaded conversations, composition, recipient/care-team selection, replies, and read/unread state. Support Medical Question, Appointment Question, Medication Question, Billing Question, and General Request categories.

Persist messages, participants, authors, timestamps, and per-user folder state. Authorized clinical or billing staff must receive the applicable threads and reply within the same conversation. Patient views must show staff replies with the correct sender and update unread indicators. Restrict threads to authorized participants and staff scope. Display a clear non-emergency communication notice; no messages are sent to outside healthcare organizations.

Archive and Restore to inbox must follow the same interaction pattern: request confirmation, perform the state change, and navigate to the destination folder with the correct tab selected. The moved conversation must be visible there. Show a specific success notice such as “Conversation restored to inbox.” Only present the action applicable to the current archive state.

Canceling confirmation leaves the thread unchanged. A failed operation keeps the detail page available with an error. Moving a thread must preserve its messages, participants, other users' folder states, and correct unread behavior. A generic success notice on an unchanged detail page is insufficient.

## 9. Medications and refill requests

Display active medications and medication history, with search and prescription details. Each record includes medication name, strength, dosage, route, frequency, start date, optional end date, prescriber, pharmacy, status, and instructions.

Patients must be able to request a refill for an eligible medication, include a note, and track Requested, Under Review, Approved, Denied, and Completed states. Authorized staff must review requests, make valid state changes, and record a decision note. Patient views must show the updated status and final decision note.

Prevent duplicate pending requests for the same medication. Explain that a request is already awaiting review instead of showing a generic database-conflict error. Keep completed and denied requests available as history.

Provide a medication-information discrepancy form that creates a staff-review request. It must not directly overwrite clinician-maintained information. All refill and prescription actions are simulated; no dispensing or external prescription transmission is permitted.

## 10. Health summary and correction requests

Provide demographics, active conditions, allergies, current medications, immunizations, medical history, surgical history, family history, social history, care team, recent vital signs, and preventive care information.

Patients can inspect the summary and request a correction. Patient-entered clinical changes must be represented as requests or clearly identified self-reported information, not silently applied to official clinical records. Authorized staff must be able to maintain synthetic clinical records and inspect correction requests, mark them reviewed, and reopen them when appropriate. Preserve the request text, patient association, creation time, and review state.

## 11. Visits and clinical notes

Provide past-visit lists and dedicated encounter details containing visit date, provider, department, visit type, reason, diagnoses, encounter summary, follow-up instructions, shared clinical notes, and an After Visit Summary.

Authorized staff must create encounters, diagnoses, and notes, and control publication of patient-visible information. Private or unpublished notes must never appear in patient responses. Link the visit to its associated authorized documents. Display consistent information between the encounter summary and its downloadable After Visit Summary.

## 12. Billing and simulated payments

Patients must be able to view outstanding balances, invoice lists and details, insurance information, payment history, and downloadable receipts. An invoice includes invoice number, service date, description, charges, insurance adjustment, patient responsibility, paid amount, remaining balance, due date, and status.

Support Unpaid, Partially Paid, Paid, Overdue, and Voided states as appropriate. Authorized billing staff must create and manage invoices, maintain insurance records, and record simulated payments.

Use exact decimal amounts. A successful payment must atomically create a transaction and update the invoice, remaining balance, status, and dashboard total. Support partial payment and payment of the remaining amount. Validate invalid amounts and prevent duplicate processing of the same payment request. A settled or voided invoice must not continue to accept an ordinary payment.

Receipts must identify the payment, invoice, date, and amount. Never collect real card details or connect to a live payment processor.

## 13. Website previews, medical documents, and PDF exports

Provide a document list with type filtering, creation date, associated encounter, and an open action. Support After Visit Summary, Laboratory Report, Clinical Letter, Visit Instructions, Medication List, Billing Statement, and Care Plan document types with synthetic content.

Laboratory reports, clinical documents including After Visit Summaries, invoice statements, and simulated payment receipts must open a readable website preview. Each preview provides **Download PDF** and **Print** controls. Print must invoke the browser's print flow.

Generate genuine PDF files with `application/pdf` responses and descriptive `.pdf` filenames; a text file renamed to PDF is not acceptable. Use the same permission-checked data representation for preview and export so dates, laboratory values, reference intervals, and financial amounts agree.

Include CareConnect branding, the patient identity, available provider identifiers, document reference, relevant dates, content-specific details, the synthetic-data disclaimer, and PDF page numbers. Laboratory reports include values, units, ranges, status, and comments; statements and receipts include exact charges, adjustments, balances or transaction amounts as relevant. Wrap long content and paginate multiple pages without clipping.

Every preview and export must enforce authentication, ownership, staff permissions, publication state, and active proxy-section permissions. Withdrawn results, unpublished documents or visits, another patient's records, and disallowed or revoked proxy sections must remain inaccessible even through saved direct export links. Associated documents must be discoverable from their encounter. Staff must be able to create and publish patient-visible documents.

Render and visually inspect representative PDFs, including a multi-page document, in addition to verifying file structure, text, and authorization.

## 14. Family linking, consent, and proxy access

Family Access must provide a visible **Link a family member** action, linked profiles, profile switching, and clear active-patient context. A caregiver account alone does not authorize access to another person's records.

Support two adult-account linking directions: inviting someone to access the current patient's records, and requesting access to another family member's records. Capture the intended recipient, relationship, and explicitly selected sections. Available sections include appointments, results, medications, health summary, visits, billing, and documents.

Show incoming and outgoing requests with sender/recipient context, relationship, requested scopes, status, expiry, and applicable actions. The authenticated intended recipient must explicitly accept or decline before a relationship becomes active. The sender can cancel a pending request. Block duplicate pending requests, expired requests, repeated acceptance, and acceptance by an unintended account.

Bind invitations to the intended account identity, including an invitation addressed to a person who registers afterward. An email/name match alone must not grant record access, and editing an existing profile email must not allow that account to claim another user's invitation. In-app invitation delivery must be labeled as local simulation; no external email is sent.

After consent, display the linked profile and only permitted sections. The owner can revoke access and the proxy can remove their access. Enforce changes on subsequent API and export requests. Do not allow an old accepted invitation to silently reactivate a revoked relationship; renewed access requires a fresh valid authorization.

Dependent/guardian access must use an administrator verification queue with a required verification decision/note. A requester cannot grant themselves dependent access or substitute self-consent for guardian review. Administrative grant management must enforce the same section restrictions and audit requirements.

Record invitations, decisions, grants, scope changes, revocations, and removals. Do not claim verified real-world identity or guardianship; this workflow uses fictional accounts and simulated administrative review.

## 15. Notifications and preferences

Provide an in-app notification center for published test results, new messages, appointments, cancellations, refill updates, billing statements, and payment confirmations. Notifications must belong to the correct account and link to the corresponding authorized record.

Support individual read/unread state, marking one notification read, and marking all read. Dashboard counters and notification indicators must reflect stored state. Notification-read state and conversation-read state must be handled consistently without treating unrelated items as read.

Account Settings must allow individual categories to be muted or unmuted and persist preferences. Muting affects future notification delivery; existing notifications remain visible. Explain this behavior in the interface. Local operation must not require external email or SMS services.

## 16. Simulated hospital workspace

Provide a functional staff interface backed by the same database as the patient portal. Authorized staff must be able to search patients, retain patient context, and access the work areas permitted by their role.

Work areas must cover appointments, provider availability, providers, departments, laboratory results and publication, medications, refill requests, clinical history, patient correction requests, encounters, diagnoses, clinical notes, documents, invoices/payments, insurance policies, and family proxy administration. Staff must also receive and respond to patient message threads.

Enforce the distinction between clinical, scheduling, billing, and administrative responsibilities on the backend. Hiding an interface item alone is not an authorization control. Staff updates must become visible in the permitted patient view without manual database editing.

## 17. Data model, API, and security

Use normalized relational entities for users, patients, patient/staff profiles, providers, departments, availability, appointments, encounters, diagnoses, clinical notes, laboratory orders/results, medications/prescriptions, refill requests, allergies, immunizations, vital signs, medical history, message threads/messages, invoices, billing transactions, insurance policies, documents, notifications, proxy relationships, and audit events. Additional entities may support recovery and other workflows. Use foreign keys, appropriate uniqueness constraints, indexes, and transactions; create and apply migrations.

Expose consistent REST APIs for authentication, profiles, dashboard, scheduling/providers, results, medications/refills, health summary, visits, messaging, billing, documents, notifications, proxy access, staff administration, and health checks. Validate inputs on the server and return predictable, readable errors.

Enforce authenticated sessions, password hashing, CSRF protection, role permissions, object-level patient isolation, and document access checks. Patients cannot access another patient's records without an active scoped proxy grant. Staff access is restricted by role and applicable record scope. API requests and direct download URLs must enforce the same rules as navigation.

Audit significant logins, record access, appointment changes, result publication/withdrawal, medication updates, refill decisions, proxy changes, and billing mutations. Audit records must identify the actor, affected record, action, and time without exposing credentials.

Seed deterministic fictional accounts for each supported role, multiple patients and providers, departments, past/upcoming appointments, lab history, medications, diagnoses, messages, invoices, notes, documents, and notifications. Provide repeatable setup and isolate disposable automated-test data from the clean manual-review database.

## 18. Acceptance and verification

Verify the following complete workflows against persisted server state and the rendered interface. A visible success notice without the expected state change does not satisfy acceptance.

| Workflow | Required observable outcome |
| --- | --- |
| Account and session | Register/sign in, edit profile, and sign out; state survives reload where appropriate, sign-out is immediate, and another account sees only its own records |
| Password management | Reject incorrect current passwords, mismatched confirmation, and weak passwords; accept a valid change and authenticate with it; reject expired or reused recovery links |
| Scheduling | Patient searches and books; dashboard and staff workspace show the booking; duplicate/conflicting booking is rejected; questionnaire and check-in persist |
| Cancellation and rescheduling | Patient cancellation records its reason; staff rescheduling creates/opens a replacement, preserves historical cancellation, and updates patient views |
| Laboratory publication | Staff creates an unpublished result; patient cannot see it; publication makes details/trends available and creates a notification; correction updates the record and withdrawal denies saved links |
| Messaging | Patient sends, staff replies in the same thread, patient sees the correct sender; unread indicators and per-user archive state remain correct |
| Refill | Patient requests once, duplicate pending submission is rejected clearly, staff progresses/reviews the request, and the patient sees the final status and decision note |
| Health corrections | A patient correction creates a separate review request; staff review state persists without silently changing official clinical data |
| Visits and documents | Patient opens a published visit, shared notes, and associated summary; private/unpublished information remains inaccessible |
| Billing | Staff creates an invoice; partial and remaining simulated payments produce transactions/receipts, correct statuses, and a zero remaining balance after settlement; duplicate processing is prevented |
| Proxy permissions | A valid grant permits only its sections; another patient and disallowed sections are denied; revocation prevents subsequent detail and download access |
| Notifications | Authorized events produce the intended notifications; read states and category preferences persist; muting does not remove existing notifications |
| Staff usability | Search/filter locates work areas; selecting a record immediately opens its drawer; closing returns to the preserved patient/module context |
| Responsive interface | Desktop, tablet, and mobile views remain readable and operable; keyboard controls, drawers, loading/empty/error states, and navigation work without horizontal overflow |

Use deterministic synthetic fixtures for backend unit/integration tests and browser workflows. Cover role escalation, object isolation, invalid requests, appointment transitions/conflicts, result publication, billing arithmetic/idempotency, document permissions, proxy access, audit events, database integrity, and frontend interactions.

Run TypeScript checks, the frontend production build, frontend unit tests, backend tests, Django system checks, and migration-drift checks. Inspect representative desktop/tablet/mobile screenshots. Record the exact commands, results, test environment, and limitations. Do not turn an untested feature into a claimed success. Keep independent benchmark scoring separate from development validation.

Provide a short manual checklist that samples each distinct capability once. Do not require repetitive account resets or replay of already verified workflows solely to extend the checklist.

Additional acceptance requirements for onboarding, sharing, and exports:

| Workflow | Required observable outcome |
| --- | --- |
| Registration routes | Patient and caregiver registrations open their corresponding destinations; each care-team role remains pending until approved; a crafted request cannot obtain Administrator or staff privileges |
| Staff review | An administrator approves or declines with the required note; pending/declined accounts cannot read staff records and approved accounts receive only the authorized role |
| Archive/restore navigation | Canceling confirmation does nothing; confirmed archive or restore opens the correct folder/tab and shows the moved thread with specific success feedback |
| Adult family consent | Test both invite and request directions with separate accounts; only the intended recipient can accept; duplicate, canceled, expired, reused, and email-reassignment attempts cannot create access |
| Dependent access | A guardian request requires administrative verification; no self-granted relationship appears before approval |
| Revocation | Owner revocation/proxy removal blocks subsequent reads and exports; an older invitation cannot restore access |
| PDF consistency | Lab, document, statement, and receipt previews match genuine downloaded PDFs; amounts, identities, units, dates, references, disclaimer, and page numbering are present as applicable |
| Export denial | Direct PDF/preview URLs deny another patient, an unpublished/withdrawn record, and a revoked or out-of-scope proxy |
| Pagination | A long multi-page PDF wraps and paginates correctly when rendered, with no clipped text or missing content |
| Role changes and navigation | Browser route changes and sign-out clear prior role/patient state; subsequent login and proxy navigation use the new authorized context |

Apply frontend, backend, and browser regression checks across the complete application as well as these scenarios.

## 19. Release deliverables and reproducibility

Deliver version **3.0.0** in repository **KateK77/mychart-clone** with frontend, backend, tests, docs, experiments, CI configuration, README, AGENTS.md, CHANGELOG, an environment example, and a gitignore that excludes secrets and local data.

The release must include applied migrations, a repeatable synthetic seed command, documented role-based demo accounts, and a clean database for manual review separate from automated-test mutations. Use an isolated version-3 checkout and version-specific session/CSRF configuration so other local releases and their databases remain usable. Local frontend port is **15270**; backend port is **18270**. Port conflicts must fail visibly rather than redirect users to another running application.

The README must enable a developer to clone and run the application without conversation context. Document purpose, synthetic-data boundaries, stack, architecture, module overview, prerequisites, installation, environment variables, migrations, seeding, demo credentials, startup, test commands, version identifiers, and known limits.

Store this complete requirements document at `experiments/round-03/description.md`. Keep implementation/validation findings in `results.md` and machine-readable release facts in `metadata.json` beside it. Results must record completed modules, verified workflows, exact checks, environment, date, commit identity, available model identifier, and unresolved issues; they must not be mixed into the requirements as claims of acceptance.

Publish source and documentation to GitHub using normal commits and verify the remote commit. The release identifier is `v3.0.0` on development branch `version-3`. Preserve existing release tags and history; an editorial documentation correction must not move a release tag or rewrite historical test evidence.

Provide the local URL, documented demo credentials, repository and requirements links, release commit/tag, migration status, concise verification results, known limitations, and the non-repetitive manual checklist. Leave the local release available for review and wait for feedback before another implementation version.

## 20. Operational boundaries

All records, organizations, identities, prescriptions, and payments are synthetic. A Telehealth appointment type does not require live video consultation. Real hospital integration, electronic prescribing, live payment processing, external mail/SMS, and production clinical use are outside this release's required local behavior. Message attachments are optional and may be omitted if clearly documented.

A local demonstration mailbox does not prove control of an email address. A deployment without configured real recovery delivery must clearly report that limitation and must not expose the local mailbox as a public password-reset mechanism. Do not claim that a hosted website, automated test result, or visual review establishes clinical, accessibility, security, or compliance certification. Document unimplemented features and environmental dependencies factually.
