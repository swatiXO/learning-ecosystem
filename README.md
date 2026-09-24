# Learning Ecosystem

Product context: [`PRD.md`](PRD.md). Build context, architecture and current status: [`PROJECT.md`](PROJECT.md) (also loaded as `CLAUDE.md` for AI coding assistants).

Working on this with 3 backend devs in parallel? Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first — it covers the branching model, migration conventions and which track owns which folder.

## Quickstart

**Prerequisites:** Docker (Desktop on Windows/Mac, Engine on Linux) and Python 3.12.

> **Windows:** if Docker Desktop shows "virtualization support not detected" on first launch, it almost always means WSL2 isn't enabled yet (not a BIOS issue). Fix: open PowerShell **as Administrator** and run `wsl --install --no-distribution`, then restart your machine. If it still fails after that, check Task Manager → Performance → CPU for "Virtualization: Enabled" — if it says Disabled, you'll need to enable Intel VT-x/AMD-V in your BIOS/UEFI setup.

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
