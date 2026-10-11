# Financial Management System (backend skeleton)

AI-Enabled Financial Management and Accounting System.
Stack follows the proposal: Python, FastAPI, SQLAlchemy 2, PostgreSQL (SQLite for local dev and tests).

What exists so far:

- Chart of accounts (`Account`): create, list, get.
- Journal entries (`JournalEntry` + `JournalLine`): create as draft, list, get.

Not implemented yet: posting, double-entry balance enforcement, periods, AP/AR, budgeting, tax,
reporting, auth/RBAC, audit trail, migrations, AI components.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --reload      # http://127.0.0.1:8000/docs
pytest
```

### PostgreSQL

```bash
docker compose up -d db
pip install -e ".[dev,postgres]"
export FMS_DATABASE_URL=postgresql+psycopg://fms:fms@localhost:5432/fms
uvicorn app.main:app --reload
```

## Layout

```
app/
  main.py        app factory, router wiring
  config.py      settings (env prefix FMS_)
  db.py          engine / session helpers, declarative Base
  models/        SQLAlchemy models
  schemas/       Pydantic request/response models
  api/           route handlers
tests/           pytest suite (SQLite per test)
```
