# Publish the CareConnect demo

GitHub hosts the project, screenshots, and source. Render runs the React app, Django API, and PostgreSQL database. Visitors follow the online-demo link in the README and can register or use the shared demo accounts without installing anything.

## Current status

The deployment package is prepared. No public application URL is claimed until the owner connects Render and deployment succeeds. The `v3.0.0` tag preserves the reviewed local release; subsequent `main` commits add the showcase and hosting package.

## Owner setup on Render

1. Open [Render](https://dashboard.render.com/) and sign in or create an account. Connect GitHub and allow access to `KateK77/mychart-clone`.
2. Choose **New → Blueprint**, select this repository, and use branch **main** with **render.yaml**.
3. Review the web service and PostgreSQL database. The supplied Blueprint uses **Free** for both; do not select a paid plan unless you intend to pay for it.
4. Create the Blueprint and wait for `careconnect-demo` to become **Live**. The first build installs dependencies, builds React, runs database migrations, and seeds a new demo database.
5. Open the service's assigned **HTTPS URL**. Sign in as `patient` with `CareConnect-Demo-2026!`, then try **Create an account** in a separate browser session.
6. Copy the exact working HTTPS URL back to the project owner/maintainer. Replace the README's `LIVE_DEMO_START` block with **Open website**, **Sign in** (`/login`), and **Create an account** (`/register`) links. Set GitHub's **About → Website** to that same URL.

[Open the Render Blueprint setup](https://dashboard.render.com/select-repo?type=blueprint) · [Render documentation](https://render.com/docs/infrastructure-as-code)

No hosting account password or API token belongs in this repository or in a chat message. Use the platform's normal GitHub connection flow.

## Free trial or lasting showcase

The free web service sleeps after 15 idle minutes, and restarting it can take about a minute. Free PostgreSQL expires 30 days after creation and is deleted after the subsequent grace period if not upgraded. The app uses PostgreSQL because files written to the free web service are not durable. Review [Render's current free-instance limits](https://render.com/docs/free).

For a lasting demo, choose a paid web-service instance and a paid PostgreSQL instance before the free database expires. Review both charges and storage on [Render's pricing page](https://render.com/pricing); the web service and database are separate resources. Choosing a paid workspace subscription alone does not upgrade their compute plans. Update `render.yaml` to match your selected plans so later Blueprint syncs retain the intended configuration.

## What is deployed

- One Docker web service serves the compiled React assets and Django API from the same origin. Browser routes such as `/register` and `/results/1` work when opened directly or refreshed.
- One PostgreSQL database stores registrations, sessions, synthetic records, requests, and audit events.
- A generated `CC_SECRET_KEY` stays in Render's environment. Database credentials are supplied through Blueprint references, not committed values.
- `CC_PRODUCTION=1` disables debug responses and enables HTTPS cookies. `CC_PUBLIC_DEMO=1` explicitly permits synthetic accounts. The initial demo is seeded only when the `patient` account is absent; service restarts do not reset visitor accounts or edits.
- `RENDER_EXTERNAL_HOSTNAME` supplies the service's allowed host and HTTPS CSRF origin. For a custom domain, add it to `CC_HOSTS` and its `https://` origin to `CC_TRUSTED_ORIGINS`.
- Automatic deploys wait for GitHub checks to pass. Migrations run before Gunicorn starts; this package is for one web-service instance.

## Visitor expectations

Demo accounts share data with everyone using those accounts. Staff demo accounts can manage synthetic patient records. Use invented information only, including when registering a personal test account. New patients and caregivers can register immediately; care-team applications still require an administrator's approval.

The public deployment disables the local simulated password-reset mailbox. Without an external delivery service, **Forgot password** reports that recovery is not configured. No real email, payment, prescription, or hospital integration is activated by deploying this demo.

## After deployment

Check the assigned URL from a browser that is not signed into Render: sign-in page, registration, a demo-account dashboard, and a PDF download. Confirm that a newly registered account can sign in again after a service restart. Only then advertise the URL as a working live demo.

For diagnostics, `/api/healthcheck/` checks database connectivity. Inspect Render's deployment and runtime logs if a build or startup fails. Keep secret values out of screenshots and issue reports.
