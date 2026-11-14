# Version 2 verification

Date: 2026-11-14, America/Chicago. Implementation commit: `dc97a9a5a8cd18b8c662c820c7a312bb20ce4257`. Release tag: `v2.0.0`. The tag includes this verification record in a following documentation commit.

## Delivered

Rebuilt sign-in, patient navigation, dashboard styling and staff workspace. Staff work areas are grouped and searchable; records open in a focused drawer with persistent URL context. Added password confirmation, visibility controls and a simulated recovery mailbox. Fixed sign-out state, unavailable-record messages, pending refill feedback, notification freshness and rescheduling navigation. Preserved all original functional modules and role/object permissions.

## Executed checks

| Command/check | Result |
| --- | --- |
| `python -m pytest -q` | 16 passed in 16.60 seconds |
| `python backend/manage.py check` | No issues |
| `python backend/manage.py makemigrations --check --dry-run` | No migration drift |
| `pnpm test` | 3 component tests passed |
| `pnpm build` | TypeScript and production Vite bundle passed |
| `playwright test --timeout 25000` using installed Microsoft Edge | 12 passed in 20.9 seconds |
| Desktop/mobile visual review | 11 captures, widths 390/768/1440; no horizontal document overflow |
| Browser runtime inspection during visual review | No JavaScript page errors |
| English source review | No Chinese characters in frontend source or portal backend |
| `git diff --check` | Passed |

The full browser suite uses a disposable SQLite database and distinct browser contexts. It covers appointment booking/rescheduling/cancellation, care team replies and notifications, mobile family navigation, lab publication, refill approval/completion, invoice/payment/receipt download, sign-out and account switching, registration/password confirmation/change, password recovery and token reuse, staff drawer/reload/Escape, and friendly unavailable-record navigation.

Backend recovery checks cover hashed token storage, expiry, single use, reissue, password-change invalidation, session revocation, CSRF, rate limiting, mailbox isolation, production-disabled simulation and duplicate email validation. The original backend workflow and permission checks remain included.

Browser testing found and fixed late form resets, lost demo-mailbox configuration after sign-out and a notification cache freshness issue. The complete suite passed after those corrections. Final typography spacing was checked visually and rebuilt afterward.

## Running demo

Frontend: http://127.0.0.1:15260. Backend: http://127.0.0.1:18260. A separate clean SQLite database was migrated and seeded for delivery. The v1 source and demo database were left independent. Sessions use a different cookie name from v1.

Screenshots and viewport checks are in `../../docs/screenshots/`. Password recovery is demonstrated without changing the seeded delivery account passwords.

## Limits

All records are synthetic. The mailbox is a deliberately local simulation, not verified external email delivery, and is disabled in production. PostgreSQL configuration is retained but was not exercised in this Windows/SQLite run. Reports and receipts remain plain text. Existing limits on external email/SMS, attachments, telehealth, real payments and prescription transmission remain. Visual review is not a comprehensive accessibility or clinical certification.

Vite emits benign upstream `use client` directive warnings; the build succeeds. GitHub Actions is configured for the dedicated v2 ports; its remote run is separate from the local results above.
