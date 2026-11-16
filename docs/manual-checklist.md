# CareConnect 3.0 — short manual review

Open http://127.0.0.1:15270. All seeded accounts use `CareConnect-Demo-2026!`.
Use separate browser profiles or a private window for the second account. Tabs in the same browser share one signed-in account.

1. **Messages:** sign in as `patient`, open a conversation, Archive and confirm, reopen it from Archive, then Restore to inbox and confirm. The Inbox should open with the restored item and a specific success notice.
2. **PDFs:** open any Test Result → View report → Download PDF. The preview and PDF should agree. Documents, Billing → View statement, and payment receipts use the same preview controls.
3. **Registration:** sign out → Create an account → choose a role. Care-team registration should show Pending. In the `admin` account, open Access reviews, select a decision and add a verification note. Check application status in the applicant's window.
4. **Family linking:** as `patient`, open Family Access → Link a family member → invite `caregiver@careconnect.example`. Sign in as `caregiver` in a separate browser profile, accept the incoming invitation, and open the shared records. Revoke from the patient account to remove access.
5. **General usability:** browse any area you want at desktop or mobile width. Existing workflows have already been regression-tested; report anything confusing without repeating the full previous checklist.

No real email, payment, prescription, or hospital connection is used. Stop after these checks and share feedback; no password-reset round trip is necessary.
