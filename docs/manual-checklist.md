# Short v2 review

Automated checks cover the repeated workflows. This is an optional design review, not another exhaustive test session.

1. Open http://127.0.0.1:15260 and sign in as `patient`. Review the dashboard and menu, then use the visible **Sign out** button.
2. Sign in as `admin`. Select Jordan Vale in **Patient context**, search for **Laboratory results**, and open a record. Its drawer appears immediately. Close it with **X** or Escape.
3. Narrow the window and check that navigation and record actions remain readable without horizontal scrolling.
4. To try recovery, sign out, choose **Forgot password?**, enter a synthetic demo email, then open **Demo mailbox** and use the reset link. Choose a password you will remember; you do not need to change it back.

Default seeded password: `CareConnect-Demo-2026!`. Use separate browser profiles or a private window for simultaneous patient and staff sessions. Tabs in one browser profile share the same login.
