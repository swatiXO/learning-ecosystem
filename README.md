# Learning Ecosystem

Product context: [`PRD.md`](PRD.md). Build context, architecture and current status: [`PROJECT.md`](PROJECT.md) (also loaded as `CLAUDE.md` for AI coding assistants).

Working on this with 3 backend devs in parallel? Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first — it covers the branching model, migration conventions and which track owns which folder.

## Quickstart

```bash
cp .env.example .env
docker compose up -d            # postgres + minio
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload   # http://localhost:8000/docs
pytest
```

## Repo layout

See `PROJECT.md` §5 for the full target layout.
