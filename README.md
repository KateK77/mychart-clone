# CareConnect Patient Portal

**DEMO — SYNTHETIC DATA ONLY — NOT FOR CLINICAL USE.**

CareConnect is an independent research prototype inspired by patient portal workflows. It has no affiliation with Epic Systems or MyChart. Synthetic billing, prescriptions, and communications are stored locally.

## Features

Patients can manage appointments, check in, send messages, review published laboratory trends, request medication refills, review their health summary and visits, pay synthetic bills, download documents and receipts, switch to authorized family records, and manage notification preferences. Employees use the same portal sign-in and see a role-based workspace for scheduling, clinical records, publication, billing and proxy administration.

## Architecture

React, TypeScript, Vite, Tailwind CSS, React Router and TanStack Query power the interface. Django and Django REST Framework handle authenticated sessions, CSRF, role checks, patient and proxy scoping, validation and persisted audit events. Local development uses SQLite. Production settings support PostgreSQL. Vite proxies API calls to Django, keeping browser requests same-origin during local development.

## Run locally

Use Python 3.12 or later, Node.js 22 or later and pnpm 11. Run from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py seed_demo
python backend/manage.py runserver 127.0.0.1:8000
```

On macOS and Linux, activate with `source .venv/bin/activate`. In a second terminal, run the frontend.

```sh
cd frontend
pnpm install --frozen-lockfile
pnpm dev --host 127.0.0.1
```

Open [CareConnect locally](http://127.0.0.1:5173). The second patient demonstrates scoped proxy access. Rerunning the seed command preserves edits and uses the current date when creating demo availability. To start with a fresh database, set `CC_SQLITE` to a new writable SQLite path before migrating and seeding.

| Username | Role |
| --- | --- |
| patient | Patient, Jordan Vale |
| dependent | Patient, Avery Vale |
| physician | Physician |
| nurse | Nurse |
| frontdesk | Front Desk |
| billing | Billing Staff |
| admin | Administrator |

The default local password is `CareConnect-Demo-2026!`. Set `CC_DEMO_PASSWORD` before first seeding to use another password. Production mode disables the seed command.

## Configuration

See `.env.example` for process environment variables. For a production-style deployment configure PostgreSQL and set `CC_PRODUCTION=1`, `CC_SECRET_KEY`, database credentials, allowed hosts and the HTTPS trusted origin. Build the frontend and serve its output with SPA fallback for browser navigation and an HTTPS same-origin reverse proxy to Django for `/api/`. This repository provides local startup and production configuration, with hosting and infrastructure left to the deployer.

## Verification

```sh
python -m pytest -q
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
cd frontend
pnpm test
pnpm build
pnpm exec playwright install chromium
pnpm e2e
```

Playwright expects the two local services running with default seeded credentials. Use a disposable seeded database because browser tests write synthetic records. Optionally set `CC_BROWSER_BIN` to an installed Chromium binary.

See [the Round 1 results](experiments/round-01/results.md) for execution evidence and [the manual checklist](docs/manual-checklist.md) for walkthroughs.

## Known limits

Plain-text reports and receipts are generated in the application. Message attachments, external email and SMS, scheduled appointment reminders, live telehealth, live payment processing and electronic prescription transmission are outside this implementation. Appointment slots represent exact start times. Staff permissions apply by department function or message team and use the synthetic patient directory. This prototype has not undergone clinical, production security, accessibility or compliance certification.

## Versioning

Round 1 uses the Git tag `v0.1.0-r1`. The original brief and experiment record are under `experiments/round-01/`.
