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

## Public deployment verification

Verified November 16, 2026 (UTC), November 15 in America/Chicago.

- Render Blueprint `exs-dbt7uf3bc2fs73dchqv0` deployed the reviewed plan in the owner's confirmed My Workspace. Both web service and database use free plans in Oregon; no paid resources provisioned.
- Deploy `dep-dbt7v6oae00c739ue1ig` reached `live` at 04:01:04 UTC, running commit `bc2dea78f0e9715b96c0cb4587a8d0112b9152f4`.
- Public URL: https://careconnect-demo-rc0t.onrender.com. Its HTTPS health endpoint returned 200 with `status: ok`.
- Browser smoke against the actual HTTPS website passed: new synthetic patient registration; patient, physician, administrator and caregiver demo logins; report preview and PDF signature/content type; deep-link refresh; secure session cookie; CSRF-less login rejected; public demo mailbox disabled; unknown API/assets return 404. No browser JavaScript errors observed.
- The new test account is `public-smoke-20261115`, with invented contact information. This public check did not restart the service; restart persistence was verified separately in the local Docker/PostgreSQL test above.
- GitHub Actions completed successfully for the deployed commit on both pushed branches.
- Added the verified public website, sign-in and registration links to the README and deployment guide.

## Deployment limitations

The Render deployment uses PostgreSQL 18; the earlier disposable-container regression suite used PostgreSQL 17. Public deployment checks exercise the live database through the application. GitHub hosts the source and presentation; Render runs the interactive website and database.

The free database expires December 16, 2026 at 03:58 UTC unless upgraded. Free web instances sleep when idle. A paid web instance and database should be selected for an ongoing showcase. The public deployment keeps the existing simulated reset mailbox disabled; external email recovery remains unconfigured.
