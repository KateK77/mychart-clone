# Independent fixture contract

No test relies on a previous test. Before each T001–T100 attempt, stop the evaluation-only server, create a new SQLite database, migrate and seed the unchanged application, add the synthetic prerequisites, and start a new evaluation browser profile. Restarting the process also clears process-local rate limits. Never reset the public demo or delivery database.

Use `127.0.0.1:18380` for the evaluation server with the already built frontend served by the application's supported `CC_SERVE_FRONTEND` mode. Local DEBUG and `CC_DEMO_MAILBOX=1` preserve the V3-required simulated recovery workflow. Production/public-demo limitations are not the oracle for local V3 requirements. Use a dedicated session-cookie name and private browser profile. Bind only loopback.

## F0

- P: adult patient with populated dashboard and all health-summary categories. Q: unrelated adult patient with visibly distinct records. R: unrelated third adult. D: synthetic dependent under18. G: adult caregiver. Physician, Nurse, Front Desk, Billing Staff and Administrator accounts are seeded independently.
- Each run generates random local-only passwords, stored only below ignored `.private/`; accounts and password changes do not affect shared demo identities. Test inputs and new labels include the task ID and run marker.
- Appointments: future confirmed/prepared and past completed records, an independent cancelled history item, all six types, available/unavailable slots, providers and departments. Dates use a single recorded setup UTC time with future offsets. Conflict tests receive one known common slot.
- Labs: full populated published normal result, test-specific high/low examples and status variants; three historical measurements with identical units; one unpublished result; more than12 records for staff navigation. Distinct Q record URLs are exposed only as test data for intentional denial checks.
- Medication: complete active and discontinued records. No pending refill by default; requested/review states are supplied only for tasks requiring them. No real medicine or external prescription endpoint.
- Encounters: published full visit with shared and private notes, linked AVS; unpublished visit/document. Seven published document kinds. LONG_DOC contains first/middle/end markers and enough content for at least3 pages.
- Billing: unpaid invoice charge180.00 less adjustment115.50 equals64.50; insurance; a separate paid historical invoice and receipt. T062/T064 get the specified20.25 partial payment on the target invoice; ordinary billing tasks start unpaid. Exact total dashboard balance is recorded in the private manifest.
- Messages: incoming unread and outgoing threads with distinct content and authors. Archive fixtures are per-user only. No external messaging.
- Notifications: at least3 unread internal notices and their destinations. Preferences start enabled unless a task states otherwise.
- Family: no adult links by default. T026/T079/T080 get only the explicitly scoped grant. Expired, accepted, revoked or pending invitations are set up only for the corresponding tasks; fixture setup does not count as demonstrated consent.
- Staff applications: pending applicants have no staff groups. Four new identities for the long onboarding scenario. Guardian approval is never pre-granted for the guardian scenario.
- Reset expiry: insert only a synthetic expired link prerequisite when required; the valid reset request and mailbox recovery must be performed by native CUA through UI. Never expose reset tokens in committed evidence.

## Reset, verification and privacy

`prepare_environment.py TEST_ID` materializes the baseline plus case prerequisites and writes a private manifest with roles, labels, dates, URLs and expected inventory. It is setup, not a scored task. Missing business capability is FAIL if valid prerequisites and an attempted workflow demonstrate it; inability to construct valid prerequisites is BLOCKED, not a manufactured PASS.

During execution, only native `computer_call` actions from the model may interact with the UI. Setup cannot perform any task's acceptance action. No selector-driven fallback, hidden API mutation or database write is allowed during a scored attempt.

Afterward, use screenshots and action logs plus read-only database snapshots/PDF inspection to grade each frozen criterion independently. Private data snapshots remain ignored. Public evidence must be reviewed for passwords, reset/invitation tokens, session cookies and personal desktop content before staging. The runtime uses only generated synthetic identities; no real patient information is allowed.

Some requirements (technology stack, migrations, indexes, password hashing, CSRF internals and production Postgres configuration) are not fully provable through screenshot-driven E2E tasks. They are listed as verification boundaries, not implicitly certified by a high UI pass rate. Optional attachments and external mail/SMS integrations are not required PASS conditions.
