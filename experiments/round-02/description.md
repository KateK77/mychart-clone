# CareConnect 2.0 scope

Date: 2026-11-14. The user authorized version 2 based on the original specification and completed manual-test feedback, with all interface content in English. This supersedes the original instruction to stop after Round 1.

The complete original specification remains in `../round-01/description.md`. Version 2 retains the functional React/TypeScript and Django/DRF application with SQLite, synthetic hospital operations, role/object permissions and audit events. It does not connect to a real hospital, payment processor or mail service.

Rebuild the visual interface and staff navigation. Replace below-list details with immediate drawers, preserve patient context, fix sign-out and technical errors, add password confirmation and recovery, and retain verified clinical, appointment, messaging, billing, document and family workflows. Use automated checks instead of another long manual test sequence. Keep v1 available and publish v2 source and a release tag to the existing private repository, verifying the remote commit.

See `../../docs/v2-feedback.md` for individual feedback decisions. Unrelated workspace files and v1 demo records are not part of this release.
