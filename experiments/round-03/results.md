# Round 3 results — CareConnect 3.0

Date: 2026-11-15 (America/Chicago). Baseline: `acd53e8bd1243038c324fe89028c3f49233d2764` / `v2.0.0`.

## Delivered behavior

- English patient portal and role-scoped synthetic hospital workspace, retaining all v1/v2 modules.
- Restore/Archive confirmation, correct destination folder, specific completion notice, and only the applicable folder action.
- Website previews, printing, and genuine PDF downloads for laboratory reports, clinical documents/after-visit summaries, invoices and receipts. One permission-checked representation feeds preview and PDF content.
- Dedicated account-type choice, patient/caregiver landing pages, care-team application form, pending/declined status, and administrator approval with a decision note. Public users cannot select Administrator or grant themselves a staff role.
- Family invitations and access requests, explicit scopes, incoming/outgoing history, consent, decline/cancel, expiry, revocation and guardian review. Existing restricted proxy permissions remain enforced.
- Consolidated full master prompt, feedback mapping, short manual checklist, reproducible tests and release documentation.

## Verification

| Check | Result |
| --- | --- |
| `python -m pytest -q` | 23 passed |
| `python backend/manage.py check` | No issues |
| `python backend/manage.py makemigrations --check --dry-run` | No migration drift |
| `pnpm test` | 3 passed |
| `pnpm build` | TypeScript and Vite passed |
| `pnpm e2e` | 16 passed on a fresh, disposable SQLite database |
| Final preview-error regression | 1 focused browser test passed; TypeScript rechecked |
| Desktop/tablet/mobile captures | 15 captures; no measured horizontal overflow or page errors |
| PDF inspection | Four document types plus a seven-page summary rendered; all 11 pages inspected |

Browser: Microsoft Edge (Chromium), headless, Windows. Viewports include 1440, 768 and 390 pixels. PDF rendering used PyMuPDF; pypdf checks actual PDF content, page numbers, and multi-page completeness. Build warnings about ignored dependency `use client` directives were non-fatal.

Backend tests include unauthorized role approval, denied staff access before approval, family consent and cross-account protection, guardian authorization, invitation expiry/cancellation/decline, revocation, invitation binding after registration, prevention of invitation claiming by profile-email changes, PDF scoping/publication and prior account workflows. Browser tests exercise full patient/staff workflows and the newly introduced UI paths.

The first browser pass caught a caregiver landing-route race and an ambiguous accessible select label. Both were corrected. The final full browser run passed all 16 tests. A final focused preview test also confirms a readable unavailable message and a working return-to-results link.

Screenshots: `docs/screenshots-v3/`. Their `checks.json` records overflow and page-error measurements. PDF samples and page counts: `docs/pdf-samples/`. Samples contain synthetic records from a disposable test database, not the clean delivery database.

## Delivery and limitations

The website runs locally at http://127.0.0.1:15270 with Django on port 18270. Its dedicated cookies and fresh seeded delivery database are separate from v1/v2 and automated-test databases. Source is published to the existing private repository on branch `version-3`, with release tag `v3.0.0`; use the tag to resolve the final release SHA. Implementation SHA is recorded in metadata.json. No public hosted deployment is claimed.

All clinical records, payments, staff/guardian verification decisions and invitations are simulated. Family invitations appear in-app; no email is sent and the demo does not verify email ownership or real-world identity. Password recovery retains the explicitly local simulated mailbox. Real enrollment, verified email delivery, hospital integration, external prescriptions, payment processing, live telehealth, message attachments and production security/compliance certification remain outside this prototype. PostgreSQL production configuration is retained, but this round was tested on SQLite. The GitHub workflow is provided; local results above do not claim a completed remote CI run.

Stop after release and await the user's review. The short manual checklist avoids repeating the prior comprehensive test sequence.
