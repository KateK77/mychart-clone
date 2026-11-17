# Manual-test feedback addressed in 2.0

The complete release requirements are specified in [the standalone v2 requirements document](../experiments/round-02/description.md). This table records historical verification decisions; it is not the requirements document.

| Feedback | Version 2 behavior | Evidence |
| --- | --- | --- |
| Long staff navigation | Categorized work-area cards, search, group filters and compact module selector | Visual review and browser test |
| Details appear below the long list | Immediate right-side drawer with sticky title and close control; Escape closes it | Browser test, reload and mobile |
| Sign-out needs refresh | Replaces session cache, clears records and shows sign-in immediately | Admin-to-patient browser test |
| Enter new password twice | Confirmation in registration, password change and recovery; visibility controls; clears after success | Backend and browser tests |
| Forgot password | Local simulated inbox, 30-minute single-use reset links | Expiry, reuse, isolation, CSRF and browser tests |
| All English | English UI, validation, documentation and clean seed records | Source and screenshot review |
| Technical unavailable errors | Readable unavailable/shared-access messages with navigation back | Backend and browser tests |
| Generic refill conflict | Explains pending request, blocks duplicate submission, shows staff decisions | Backend guard and browser workflow |
| Inconsistent upcoming order | Earliest appointment first | Source review and booking regression |
| Raw IDs and timestamps | Names and readable dates in staff drawers | Visual review |
| Reschedule leaves cancelled record open | Opens replacement immediately, retains old record in history | Staff-to-patient browser test |

The sender-name report was withdrawn after the user corrected the signed-in account; it is not a defect. The Notepad missing-file message was not established as a portal defect.

Previously successful patient and staff flows are retained. Automated checks replace repetitive manual testing; there is no requirement to restore a password solely for testing.
