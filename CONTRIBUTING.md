# Contributing (backend, Phase 0–2)

Three backend devs working in parallel on one repo. This is the workflow so that doesn't turn into merge hell.

## The three tracks

| Track | Owns | Key folders |
|---|---|---|
| **A — Identity & Onboarding** | guardians/children/schools/consents, onboarding flow, age-band logic | `backend/app/onboarding/`, `backend/app/models/identity.py`, onboarding routes in `backend/app/api/` |
| **B — Signals, Scoring & Plan Engine** | event ingest, scoring extractors, plan engine, profile/plan endpoints | `backend/app/scoring/`, `backend/app/plan_engine/`, `backend/app/schemas/events.py` |
| **C — Sessions, Week-1 & Safety** | sessions/activity-runs, week-1 schedule + gate, safety flags, media upload | `backend/app/week1/`, `backend/app/safety/`, session/activity-run models and routes |

Full task breakdown per track is in the repo's project board / issues (label `track-a`, `track-b`, `track-c`).

## Branching

- `main` is protected — no direct pushes.
- Branch names: `track-a/<short-description>`, `track-b/<short-description>`, `track-c/<short-description>`.
- Open a PR against `main`. At least one review from a dev on a different track before merging (the whole point is a second set of eyes on the shared contracts).

## Alembic migrations (the one thing that WILL conflict if we're not careful)

- **Rebase onto latest `main` before generating a new revision.** Alembic revisions form a linked list (`down_revision`); two people generating a revision off the same head at the same time creates a fork.
- One revision per PR that touches the schema. Never edit a revision that's already been merged — write a new one.
- If you hit a migration conflict on rebase: regenerate your revision (`alembic revision --autogenerate`) against the new head rather than hand-editing the `down_revision` pointer, unless you're sure what you're doing.
- Before opening a PR with a migration: `alembic upgrade head` locally against a clean DB (`docker compose down -v && docker compose up -d`) to confirm it applies cleanly.

## Shared contracts — coordinate before changing

These files are read by all three tracks. Changing their shape needs a heads-up in the team chat before you open the PR, not after:

- `backend/app/schemas/events.py` (event schema v0)
- `backend/app/models/base.py`
- `docs/activity-signal-map.md`
- `PROJECT.md` §6 (domain model / API table) — update this file whenever a table or endpoint changes shape, per its own instructions.

## Conventions (from PROJECT.md §7)

- Type hints everywhere, `ruff` + `black`, Pydantic schemas for all I/O.
- No business logic in routers — it lives in `scoring/`, `plan_engine/`, `week1/`, `onboarding/`.
- Activity keys are `snake_case` and versioned (`activity_version`); bump the version when a payload shape changes.
- Every scoring extractor and plan-engine rule needs a fake-child test (`backend/tests/fixtures/`). Scoring must be deterministic.
- Commit prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `test:`.
- Never commit real child data, audio, or `.env`.
- Wording: "skill", "area to practise", "strength" — never "disorder", "symptom", "diagnosis" (PROJECT.md rule #1).

## Local setup

See `PROJECT.md` §8.

## CI

Every PR touching `backend/` runs ruff, black --check, an `alembic upgrade head` against a fresh Postgres, and pytest (`.github/workflows/ci.yml`). Green CI is required before merge.
