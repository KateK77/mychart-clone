# Showcase and deployment verification

Date: 2026-11-15

## Delivered

- English GitHub presentation: product purpose, workflow table, screenshots, PDF samples, shared demonstration accounts, registration instructions, and setup links.
- Existing repository visibility changed from private to public at the owner's explicit request; confirmed through GitHub repository metadata.
- Multi-stage Docker build for React and Django, served together by Gunicorn and WhiteNoise, with PostgreSQL, HTTPS settings, and deep-link support.
- Render Blueprint for an explicitly enabled public synthetic demo, plus owner setup instructions. No paid resources provisioned.
- New demonstration database initialization preserves visitor accounts and existing records on service restart.
- Updated the pnpm 11 dependency-build allowlist and browser title to CareConnect 3.0.

## Checks completed

- Docker image built successfully from the repository with frozen frontend dependencies.
- 25 backend tests passed using a disposable PostgreSQL 17 database in a Linux container. This test process used the suite's normal local HTTP configuration; the separately running service retained production HTTPS settings.
- SQLite regression run passed 24 tests; the new frontend-shell test initially needed a Django database-test marker for response cleanup. After that test-only correction, both hosting tests passed.
- Django system and production deployment checks: no issues. Migration drift: none.
- Browser smoke against the built image, using Edge and the expected TLS-terminating proxy header: new-patient registration; patient, administrator, and caregiver logins; deep-link refresh; real PDF download; secure session cookie; rejection of a CSRF-less login; disabled public demo mailbox; 404s for unknown API and asset routes. No browser JavaScript errors observed.
- Restarted the disposable application container and logged back into the newly registered account, confirming PostgreSQL persistence.
- Git whitespace check passed.

## Deployment boundary

The Docker service was validated locally, bound only to loopback. Render has not issued a public application URL in this task. The README deliberately marks the live demo as pending until the owner connects the hosting account and the actual deployment succeeds. GitHub source visibility is public; this alone does not deploy the application.

The free Blueprint is a short trial because Render's free PostgreSQL database expires after 30 days. A paid web instance and database should be selected for an ongoing showcase. The public deployment keeps the existing simulated reset mailbox disabled; external email recovery remains unconfigured.
