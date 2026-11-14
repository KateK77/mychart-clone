# Changelog

## v2.0.0 · 2026-11-14

- Rebuilt the interface with English copy, grouped navigation, responsive layouts and a visible sign-out control.
- Replaced long staff navigation and below-list details with searchable work-area groups, patient context and a focused record drawer. Selection survives refresh; Escape closes the drawer.
- Added password confirmation and visibility controls, plus a browser-scoped simulated mailbox with expiring, single-use reset links.
- Fixed stale account UI after sign-out, late form resets, notification freshness, appointment ordering and technical unavailable-record errors.
- Improved refill feedback, readable staff names and dates, publication status and proxy controls. Rescheduling opens the new appointment immediately.
- Added account and navigation regression tests while retaining existing patient and staff workflows.
- Isolated v2 ports and cookies from v1 and retained the v1 release tag.

## v0.1.0-r1 · 2026-11-13

- Added the CareConnect patient portal and staff workspace with a shared relational database.
- Added SQLite migrations, synthetic seed command, role-based access, audit events, and workflow tests.
