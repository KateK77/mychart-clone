# Feedback implemented in version 3

| Feedback | Implemented behavior | Verification |
| --- | --- | --- |
| Restore feels uncertain | Confirmation, destination Inbox, explicit success notice; only applicable folder action | Browser archive/cancel/restore workflow; backend per-user state |
| Text downloads feel informal | Website preview, PDF download and print for labs, documents, invoices and receipts | PDF extraction/access tests, browser download, rendered PDF inspection |
| Choose account type before registration | Patient, Family caregiver, Care team; role-specific form and landing | Browser onboarding and staff approval; backend role-denial tests |
| Family Access has no linking action | Invite/request with explicit scopes, incoming/outgoing status, acceptance/decline/cancel, revocation | Two-account browser workflow; backend consent, expiry, cross-account and revocation tests |
| Dependent access needs authorization | Guardian verification queue for administrators | Backend approval and no self-consent for minors |
| Earlier v1 feedback | All v2 fixes retained | Existing v1/v2 automated regressions |

The complete release requirements are specified in [the standalone v3 requirements document](../experiments/round-03/description.md). This feedback table is historical supporting evidence and is not needed to understand the requirements. Version 1 and 2 evidence remain in their original experiment directories.
