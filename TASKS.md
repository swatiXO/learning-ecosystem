# Backend task breakdown (Phase 0–2)

Tracks and ownership are defined in `CONTRIBUTING.md`. This is the concrete first checklist per track — check items off (or move them into GitHub Issues) as you go.

**Day 0 shared foundation: done.** FastAPI skeleton, `docker-compose.yml`, Alembic wiring, shared event schema (`backend/app/schemas/events.py`), CI — all on `main`.

## Track A — Identity & Onboarding (@zurraizai)

1. [ ] `backend/app/models/identity.py`: `guardians`, `children`, `schools`, `consents` tables (columns in `PROJECT.md` §6)
2. [ ] Import those models in `backend/app/models/__init__.py`, generate first Alembic migration
3. [ ] `backend/app/onboarding/`: field validation + age-band-from-DOB helper
4. [ ] `backend/app/api/onboarding.py`: `POST /onboarding`, `GET /onboarding/options`; wire into `main.py`
5. [ ] `backend/app/api/children.py`: `PATCH /children/{id}`, `POST /children/{id}/consent`
6. [ ] Test proving onboarding never writes a `skill_scores` row (rule #10)

## Track B — Signals, Scoring & Plan Engine (@swatiXO)

1. [ ] `backend/app/models/events.py`: `signal_events` table (PK = `event_id`)
2. [ ] `backend/app/api/events.py`: `POST /events/batch`, de-duplicating on `event_id`; wire into `main.py`
3. [ ] `backend/app/models/scoring.py`: `skill_scores`, `plans`, `plan_modules` tables
4. [ ] `backend/app/scoring/stars_not_clouds.py`: first extractor, events → skill dimension scores
5. [ ] `backend/app/plan_engine/rules.py` + `engine.py` (shape sketched in `PROJECT.md` §6)
6. [ ] Fake-child fixtures + tests for the extractor and each rule (`backend/tests/fixtures/`)
7. [ ] `backend/app/api/profile.py`, `plans.py`: `GET /children/{id}/profile`, `GET`/`PUT /children/{id}/plan`

## Track C — Sessions, Week-1 & Safety (@kazimmehdi7)

1. [ ] `backend/app/models/sessions.py`: `sessions`, `activity_runs`, `week1_progress` tables
2. [ ] `backend/app/api/sessions.py`, `activity_runs.py`: start/end session, start/complete/skip/quit activity-run
3. [ ] `backend/app/week1/`: the 7-day schedule (PRD §6.2) + gate logic (rule #4: nothing unlocks before day 7)
4. [ ] `backend/app/api/today.py`: `GET /children/{id}/today`
5. [ ] `backend/app/models/safety.py`: `safety_flags`; `backend/app/safety/`: serious-signal rules
6. [ ] `media_objects` table + `POST /media/upload-url` (must check consent first — rule #6)

## Joint, once the first activity is wired end-to-end

- [ ] `docs/activity-signal-map.md` for `stars_not_clouds`: Track C defines the event types it emits, Track B defines what each feeds into scoring — fill in together, then hand to the Flutter dev (PROJECT.md §9).
