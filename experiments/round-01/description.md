# CODEX MASTER INSTRUCTION — MYCHART-INSPIRED PATIENT PORTAL

## 0. Read This First

You are an autonomous senior full-stack software engineer, healthcare software architect, database engineer, and QA engineer.

Build a complete, functional, end-to-end patient portal inspired by Epic MyChart.

This is a standalone healthcare software engineering experiment.

You have no previous conversation context.

Do not assume that an EHR system, hospital database, clinical API, or existing repository is available.

Build everything required for the application to function independently.

**Implement the entire specified application during Round 1.**

Do not deliver only a scaffold, static interface, or limited MVP.

You may organize implementation internally, but do not divide delivery into multiple development phases.

## 1. Project Identity

Project name: CareConnect Patient Portal

Reference product:
https://www.mychart.org/

GitHub owner:
KateK77

Target repository:
KateK77/mychart-clone

Preferred local directory:
D:\AI-Workspace\Personal\mychart-clone

Repository visibility:
PRIVATE

This is an independent synthetic-data research prototype inspired by patient portal workflows.

It is not affiliated with Epic Systems or MyChart.

Do not copy protected logos, branding, proprietary code, or restricted material.

Display:

"DEMO — SYNTHETIC DATA ONLY — NOT FOR CLINICAL USE."

## 2. Experiment Context

This application is part of a three-project AI software generation benchmark.

The experiment evaluates the ability of an AI coding agent to generate complete healthcare software from detailed requirements.

There may be up to five development rounds.

This instruction initiates Round 1 only.

Round 1 objectives:

- Generate the complete application.
- Implement all required modules.
- Create and apply database migrations.
- Seed realistic synthetic data.
- Execute automated tests.
- Verify core user workflows.
- Commit and push code to GitHub.
- Save the complete requirements and test results.
- Stop and wait for feedback.

Do not automatically begin Round 2.

The final independent benchmark test suite will be introduced after development is complete.

## 3. Product Objective

Build a complete web-based patient portal that enables patients to access their health information, communicate with healthcare staff, manage appointments, review test results, request medication refills, and manage healthcare billing.

The system must function as a standalone application.

Because no hospital EHR is available, implement a simulated clinical backend and administrative interface.

The patient-facing features and clinical backend must use the same persistent database.

Actions performed by patients must create real application records or state transitions.

Do not implement buttons that only display success messages without changing application state.

## 4. Technology Stack

Frontend:

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- TanStack Query

Backend:

- Python
- Django
- Django REST Framework

Database:

- PostgreSQL for production
- SQLite for local development

Testing:

- pytest / pytest-django
- Vitest
- React Testing Library
- Playwright

Use a modular architecture.

The application should be fully usable locally without any paid third-party services.

## 5. Design and Navigation

Design a clean, modern, patient-friendly healthcare interface.

Primary style:

- White backgrounds
- Blue and teal accents
- Clear typography
- Accessible controls
- Patient-friendly language
- Responsive layout
- Desktop and mobile support

Primary patient navigation:

1. Dashboard
2. Appointments
3. Messages
4. Test Results
5. Medications
6. Health Summary
7. Visits
8. Billing
9. Documents
10. Family Access
11. Account Settings

Provide consistent sidebar or top navigation.

Include:

- Loading states
- Empty states
- Validation messages
- Success notifications
- Error handling
- Confirmation dialogs
- Breadcrumbs where appropriate

## 6. Patient Dashboard

The dashboard must show a personalized overview.

Include:

- Patient name
- Upcoming appointments
- Recent test results
- Unread messages
- Current medications
- Outstanding balances
- Recent visits
- Important notifications
- Quick action buttons

Quick actions:

- Schedule Appointment
- Send Message
- View Test Results
- Request Refill
- Pay Bill

Dashboard values must come from actual persisted records.

Do not hardcode counts or balances in the UI.

## 7. Authentication and Patient Accounts

Implement:

- Patient registration
- Login
- Logout
- Password hashing
- Profile editing
- Password change
- Session management
- Access control

Roles:

- Patient
- Physician
- Nurse
- Front Desk
- Billing Staff
- Administrator

Users must only access information permitted by their roles.

Patients must not access other patients' records.

Staff actions must be appropriately restricted.

Provide deterministic synthetic demo accounts for each role.

Document demo credentials in local development instructions, not in publicly deployed production interfaces.

## 8. Appointment Management

Implement a complete appointment workflow.

Patient features:

- View upcoming appointments
- View past appointments
- Search available appointment slots
- Filter by provider
- Filter by appointment type
- Select date and time
- Book an appointment
- Request rescheduling
- Cancel appointments
- View appointment instructions
- Complete pre-visit questionnaires
- Perform simulated eCheck-In

Appointment types:

- Primary Care
- Follow-up
- Annual Physical
- Specialist Consultation
- Telehealth
- Laboratory Visit

Appointment statuses:

- Available
- Scheduled
- Confirmed
- Checked In
- Completed
- Cancelled
- No Show

Backend requirements:

- Prevent double booking.
- Enforce appointment state transitions.
- Validate provider availability.
- Handle scheduling conflicts.
- Record cancellation reasons.
- Preserve appointment history.
- Apply consistent timezone handling.

Build an administrative scheduling interface so staff can create providers, configure availability, manage appointments, and update appointment statuses.

## 9. Test Results

Patients must be able to view laboratory test results.

Display:

- Test name
- Collection date
- Result date
- Result value
- Unit
- Reference range
- Result status
- Abnormal flag
- Ordering provider
- Related comments

Features:

- View results list
- Filter by date
- Search by test name
- Open result details
- View historical measurements
- Display trends in charts
- Download a result summary

Support:

- Pending
- Preliminary
- Final
- Corrected

Show normal and abnormal values clearly.

Reference ranges must be associated with the relevant laboratory test and units.

Do not infer medical diagnoses from abnormal results.

Administrative users should be able to create and publish synthetic laboratory results.

Unpublished results must not appear in the patient portal.

## 10. Secure Messaging

Build an internal patient-provider messaging system.

Features:

- Inbox
- Sent messages
- Message details
- Threaded conversations
- Compose new message
- Select recipient or care team
- Reply to messages
- Read/unread states
- Archive messages
- Attachment support, if feasible

Message categories:

- Medical Question
- Appointment Question
- Medication Question
- Billing Question
- General Request

Messages must persist in the database.

Clinical staff must have a corresponding inbox and be able to reply.

Patients must see replies in the same thread.

Provide clear notices that messaging is for non-emergency communication.

Do not send messages to external healthcare organizations.

## 11. Medication Management

Display the patient's medication information.

Each medication record should contain:

- Medication name
- Strength
- Dosage
- Route
- Frequency
- Start date
- End date, if applicable
- Prescribing provider
- Pharmacy
- Status
- Instructions

Features:

- View active medications
- View medication history
- Search medications
- View prescription details
- Request a refill
- Track refill request status
- Report medication information discrepancies

Refill statuses:

- Requested
- Under Review
- Approved
- Denied
- Completed

Create a staff workflow to review and update refill requests.

**No real prescriptions may be transmitted or dispensed.**

All medication activity must be simulated.

## 12. Health Summary

Create a comprehensive patient health summary.

Sections:

- Demographics
- Active medical conditions
- Allergies
- Current medications
- Immunizations
- Medical history
- Surgical history
- Family history
- Social history
- Care team
- Recent vital signs
- Preventive care information

Allow patients to review this information.

Appropriate patient-entered updates should be treated as requests or self-reported information, rather than silently changing clinician-verified data.

Authorized staff should be able to maintain official synthetic clinical records.

## 13. Visits and Clinical Notes

Allow patients to review past encounters.

Display:

- Visit date
- Provider
- Department
- Visit type
- Reason for visit
- Diagnoses
- Encounter summary
- Follow-up instructions
- Shared clinical notes
- After Visit Summary

Create a dedicated visit detail page.

Staff should be able to create synthetic encounters and publish appropriate information to the patient portal.

Notes marked private or unpublished must not be shown.

## 14. Billing and Payments

Implement a simulated medical billing system.

Features:

- View outstanding balances
- View invoices
- View payment history
- View billing details
- View insurance information
- Make simulated payments
- Download payment receipts

Each invoice should contain:

- Invoice number
- Service date
- Description
- Amount
- Insurance adjustment
- Patient responsibility
- Paid amount
- Remaining balance
- Due date
- Status

Support:

- Unpaid
- Partially Paid
- Paid
- Overdue
- Voided

A simulated payment must update balances accurately and create a transaction record.

Prevent duplicate processing of the same payment request.

Do not collect or process real credit card information.

Do not integrate live payment processing.

## 15. Medical Documents

Create a document management module.

Document types:

- After Visit Summary
- Laboratory Report
- Clinical Letter
- Visit Instructions
- Medication List
- Billing Statement
- Care Plan

Features:

- View document list
- Filter by type
- Open document
- Download document
- Display creation date
- Display associated encounter

Use generated synthetic documents.

Implement authorization checks for every file access.

## 16. Family and Proxy Access

Implement basic family account management.

Allow authorized users to:

- View linked dependent profiles
- Switch between permitted patient accounts
- Access permitted records
- Manage proxy relationships

Use explicit permission rules.

Do not assume that a family relationship automatically provides access to all medical records.

Administrators should be able to create and revoke synthetic proxy access.

Record proxy access changes in the audit log.

## 17. Notifications

Create an in-app notification center.

Events:

- New test result
- New message
- Upcoming appointment
- Appointment cancellation
- Refill request update
- New billing statement
- Payment confirmation

Features:

- Read/unread state
- Notification list
- Navigate to associated record
- Mark notification as read
- Notification preferences

Use internal notifications by default.

External email and SMS providers are optional and must not be required for local operation.

## 18. Staff and Administrative Dashboard

Because no real EHR integration exists, implement a functional simulated hospital backend.

Authorized staff must be able to:

- Search patients
- View permitted patient records
- Manage appointments
- Configure provider availability
- Create encounters
- Maintain clinical history
- Enter laboratory results
- Publish results
- Manage medication records
- Review refill requests
- Reply to messages
- Create invoices
- Record simulated payments
- Publish documents

This functionality is essential.

The patient portal must not be a collection of disconnected frontend screens.

Patient-facing features must reflect staff-side changes.

## 19. Database Models

Design normalized relational models.

Suggested entities:

- User
- Patient
- PatientProfile
- StaffProfile
- Provider
- Department
- Appointment
- ProviderAvailability
- Encounter
- Diagnosis
- ClinicalNote
- LaboratoryOrder
- LaboratoryResult
- Medication
- Prescription
- RefillRequest
- Allergy
- Immunization
- VitalSign
- MedicalHistory
- MessageThread
- Message
- Invoice
- BillingTransaction
- InsurancePolicy
- MedicalDocument
- Notification
- ProxyAccess
- AuditEvent

Use appropriate foreign keys, unique constraints, indexes, and transactional updates.

Create and apply database migrations.

## 20. Workflow Requirements

The following workflows must function end-to-end.

### Workflow A: Scheduling

Patient logs in → searches appointments → selects provider and slot → books appointment → appointment appears on dashboard → staff can view it → patient can cancel or request rescheduling.

### Workflow B: Laboratory Results

Staff creates a lab result → result is initially unpublished → authorized staff publishes the result → patient receives a notification → patient opens the result → patient can view details and historical trends.

### Workflow C: Messaging

Patient creates a message → staff receives it → staff replies → patient receives a notification → patient opens the thread and reads the response.

### Workflow D: Medication Refill

Patient opens an active medication → submits refill request → staff reviews request → status changes → patient sees the updated status.

### Workflow E: Billing

Staff creates invoice → patient sees outstanding balance → patient makes simulated payment → transaction is recorded → outstanding balance is updated → receipt becomes available.

### Workflow F: Proxy Access

Administrator grants access → proxy user switches to permitted patient profile → authorized records are visible → access is revoked → further access is denied.

These workflows must have automated tests.

## 21. Synthetic Data

Seed the database with realistic synthetic records.

Include:

- Multiple patients
- Multiple providers
- Several departments
- Past and upcoming appointments
- Laboratory results
- Medications
- Diagnoses
- Messages
- Billing records
- Clinical notes
- Documents
- Notifications

Use clearly fictional identities.

Do not use real patient records or protected health information.

Provide a repeatable seed command.

## 22. Security and Auditability

Implement:

- Role-based access control
- Object-level authorization
- Secure authentication
- CSRF protection
- Input validation
- Secure document access
- Audit logs
- Transactional state changes
- Sensitive data isolation
- Safe error messages

Audit important events:

- Login
- Record access
- Appointment changes
- Result publication
- Medication updates
- Refill decisions
- Proxy permission changes
- Billing changes

Do not claim that this demonstration application is HIPAA compliant.

## 23. REST API

Implement endpoints for:

- Authentication
- Patient profile
- Dashboard
- Appointments
- Providers
- Laboratory results
- Medications
- Refill requests
- Health summary
- Visits
- Messages
- Billing
- Documents
- Notifications
- Proxy access
- Staff administration
- Health checks

Use consistent validation and error responses.

## 24. Automated Testing

Implement unit, integration, and end-to-end tests.

Test:

- Authentication
- Authorization
- Patient data isolation
- Appointment conflicts
- Appointment transitions
- Lab publication visibility
- Messaging
- Refill workflow
- Billing calculations
- Duplicate payment prevention
- Document authorization
- Proxy access
- Audit events
- Database integrity
- Invalid requests
- Frontend interactions

Tests must use deterministic synthetic data.

Do not use live medical services.

The final independent benchmark evaluation will be conducted after development iterations.

## 25. GitHub and Experiment Tracking

Target repository:

KateK77/mychart-clone

Create as PRIVATE if it does not exist.

Inspect existing contents before changing anything.

Required structure:

- frontend/
- backend/
- tests/
- docs/
- experiments/
- .github/workflows/
- README.md
- AGENTS.md
- CHANGELOG.md
- .env.example
- .gitignore

Create:

experiments/round-01/description.md
experiments/round-01/results.md
experiments/round-01/metadata.json

Save this complete original instruction as description.md.

Record:

- Model identifier, if available
- Date
- Git commit SHA
- Completed modules
- Test commands
- Test results
- Known limitations

Create Git tag:

v0.1.0-r1

Push source code, documentation, and tag.

Verify the remote commit.

Do not overwrite unrelated repository history.

If GitHub access is unavailable, explain the blocker instead of claiming the push succeeded.

## 26. README Requirements

The README must explain:

- Project purpose
- Independent prototype disclaimer
- Technology stack
- Feature list
- Architecture
- Installation
- Environment configuration
- Database migrations
- Synthetic data setup
- Demo accounts
- Startup commands
- Test commands
- Known limitations
- GitHub versioning

A developer should be able to clone the repository and run the application using only the README.

## 27. Final Deliverables

After Round 1, report:

1. Completed modules
2. Working workflows
3. Application architecture
4. GitHub repository URL
5. Git commit SHA
6. Git tag
7. Database migration status
8. Demo accounts
9. Local startup instructions
10. Automated test results
11. Manual test checklist
12. Known issues and incomplete features

Be honest about incomplete functionality.

Do not claim a feature is working unless it has been implemented and appropriately checked.

## 28. Execution Instructions

Begin implementation immediately.

Build the complete patient portal and supporting synthetic clinical backend.

Prioritize real end-to-end behavior over superficial UI completeness.

Do not ask for repeated confirmation of ordinary engineering choices.

Do not begin Round 2.

After completing and verifying Round 1, stop and wait for feedback.

**BEGIN ROUND 1: BUILD THE COMPLETE CARECONNECT PATIENT PORTAL.**