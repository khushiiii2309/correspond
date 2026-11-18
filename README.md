# Correspond

An AI-powered email intelligence and productivity app. Correspond helps you understand
what's in your inbox, surface what needs attention, extract action items, and draft
replies — without ever sending anything on your behalf without approval.

This repository is being built incrementally, phase by phase (see `PROJECT SPEC` in the
original planning conversation). **This is Phase 1: working foundation.**

## Current status (Phase 1 — complete)

- FastAPI backend with the full Phase 1 data model (`users`, `email_accounts`, `emails`,
  `email_analyses`, `tasks`, `reply_drafts`, `activity_logs`) migrated via Alembic.
- A single seeded "demo" user stands in for authentication — there is no login yet.
  Every row is already scoped by `user_id`, so real auth can be layered in later without
  reshaping the schema.
- 12 synthetic sample emails (ordinary mail, deadlines, newsletters, meeting requests,
  multi-task requests, phishing attempts, and a prompt-injection attempt) seedable via
  one API call.
- React + Vite frontend: unified inbox with search, category/priority filters, unread
  filter, sort, read/unread toggling, and a reading pane. AI category/priority badges
  are wired up in the UI but show "Not analyzed yet" until Phase 2 adds the AI service.
- 11 passing backend tests covering seeding, listing, filtering, detail fetch, read-status
  updates, and per-user data isolation.

**Not implemented yet** (by design — later phases): AI classification/summarization,
task extraction, reply drafting, Gmail OAuth, activity log UI, authentication.

## Architecture

```
backend/   FastAPI + SQLAlchemy 2.x + Alembic + PostgreSQL
  app/
    core/      settings, DB engine/session
    models/    SQLAlchemy ORM models (one file per entity) + shared enums
    schemas/   Pydantic request/response models
    api/       routers + dependencies (api/routes/*.py, api/deps.py)
    services/  business logic (demo seeding, sample data)
  alembic/     migrations
  tests/       pytest suite (spins up a real Postgres test DB)

frontend/  React + Vite + React Router + Axios
  src/
    api/         API client
    components/  Sidebar, Layout, EmailList, EmailDetailPanel, Badge
    pages/       Inbox, ComingSoon (Tasks/Activity/Settings placeholders)
```

### Why a "demo user" instead of login?

Phase 1's goal is just: load sample emails, see them in an inbox, open one. Building a
full auth system before there's anything worth protecting would be premature. Every
table already has `user_id` columns and queries already filter by it (verified by a
data-isolation test), so swapping the demo user for real sessions later is additive, not
a rewrite.

### Port conflicts with other local projects

This machine already runs an unrelated project (`kitchenverse`) using the default
Postgres (`5432`) and backend (`8000`) ports. To avoid touching those containers,
Correspond uses:

- Postgres: **5433** (host) → 5432 (container)
- Backend API: **8001**
- Frontend dev server: **5173** (Vite default, proxies `/api` to `:8001`)

If you don't have a port conflict on your machine, feel free to change these back in
`docker-compose.yml`, `backend/.env`, and `frontend/vite.config.js`.

## Setup (Windows)

Prerequisites confirmed on this machine: Python 3.14, Node 26, Docker Desktop, Git.
(Python 3.15 was also present but too new for prebuilt wheels of several dependencies —
use 3.14 or earlier.)

```powershell
# 1. Start Postgres
docker compose up -d postgres

# 2. Backend
cd backend
py -3.14 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --port 8001 --reload

# 3. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173, click **Load sample emails**, and browse the inbox.

### Running backend tests

```powershell
cd backend
.venv\Scripts\activate
pytest
```

Tests create and migrate a separate `correspond_test` database automatically (same
Postgres server, different database) and truncate tables between tests.

## API

| Method | Path                              | Description                          |
|--------|-----------------------------------|---------------------------------------|
| GET    | `/api/health`                     | Health check                          |
| POST   | `/api/emails/demo/seed`           | Seed the 12 sample emails (idempotent)|
| GET    | `/api/emails`                     | List emails (filters: `category`, `priority`, `unread_only`, `search`, `sort`) |
| GET    | `/api/emails/{email_id}`          | Email detail, including AI analysis if present |
| PATCH  | `/api/emails/{email_id}/read-status` | Mark read/unread                  |

Full interactive docs: http://localhost:8001/docs

## Next: Phase 2

AI email intelligence — an LLM provider layer, classification, summarization, task
extraction, structured-output validation, and persisting `EmailAnalysis` rows so the
badges and insights panel already in the UI start showing real data.
