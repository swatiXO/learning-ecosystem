# PROJECT.md: Learning Ecosystem

> The living context file for this repo. Read this first, whether you are a human or an AI coding assistant (Claude Code, Copilot, Cursor).
> Product requirements are in `PRD.md`. **This file covers how it is built and where it currently stands.** Update the Status, Decisions and Build Log sections every time something is built or changed.
> Tip: if you use Claude Code, copy or symlink this file as `CLAUDE.md` so it loads automatically.

---

## 1. What we are building (one paragraph)

A learning app for children with ADHD, autism and low self-esteem. Setup is a 2–3 minute **onboarding** of simple context questions (name, date of birth, area, school or home school). There is **no intake survey**. A 7-day game-based first week logs behavioural signals. These become a **needs profile** (skill scores + confidence, **never diagnosis labels**). A rules-based **plan engine** assigns 1–3 weighted modules (Focus & attention, Speech & language, Social-emotional, Confidence builder, Routine & sensory). The app adapts live and re-evaluates every 6–8 weeks against the child's own baseline. Parents, teachers and therapists have dashboards, and serious signals go to a human for referral.

## 2. Non-negotiable rules (apply to all code)

1. **Scores, not labels.** No field, API response or UI string may contain a diagnosis (ADHD, autism, etc.) as a child attribute.
2. **No activity without evidence.** Every activity must emit events mapped to at least one skill dimension.
3. **Baseline, not norms.** Progress = change from the child's own baseline. Never rank children against each other.
4. **Week 1 is the gate.** Program modules stay locked until week 1 is complete.
5. **No fail states.** Skips and quits are comfort signals, not errors. Rewards are for effort.
6. **Consent first.** Check consent before storing audio/video. Raw media lives in object storage, linked by ID, never inside profile tables.
7. **Explainable.** Every score and plan stores which events and rules produced it.
8. **Humans in the loop.** Referrals and plan overrides require a human action. Log them.
9. **Idempotent events.** Clients generate `event_id` (UUID). The server de-duplicates.
10. **Onboarding is context, not assessment.** Onboarding answers never set skill scores or priors. They only set age band, language, reading level and school link. Keep it at 2–3 minutes: no new onboarding question without a reason written in the Decision log.

## 3. Architecture

```
┌──────────────────────┐        HTTPS/JSON         ┌───────────────────────────┐
│  Flutter app         │  ───────────────────────▶ │  FastAPI backend          │
│  (child + parent)    │   /events/batch, /today   │  ├─ api/  (routers)       │
│  Flame games, Rive   │                           │  ├─ scoring/ (events→skills)
│  offline event queue │  ◀─────────────────────── │  ├─ plan_engine/ (rules)  │
└──────────────────────┘      plans, profile       │  ├─ speech/ (Whisper etc.)│
                                                   │  └─ safety/ (flags)       │
┌──────────────────────┐                           └─────┬──────────────┬──────┘
│  Dashboards          │  ◀──── /profile, /plans ────────┘              │
│  parent/teacher/     │                           ┌─────▼─────┐  ┌─────▼──────┐
│  therapist           │                           │ Postgres  │  │ MinIO / S3 │
└──────────────────────┘                           │ (profile  │  │ (raw audio │
                                                   │  store)   │  │  & video)  │
                                                   └───────────┘  └────────────┘
```

**Data flow:** onboarding (context only) → week-1 default schedule → activity → events → `signal_events` → scoring → `skill_scores` → plan engine → `plans` → app shows today's activities → repeat.

## 4. Tech stack

| Layer | Choice | Notes |
|---|---|---|
| Backend | Python 3.12, FastAPI, Pydantic v2 | OpenAPI at `/docs` is the contract with the Flutter team |
| DB | PostgreSQL 16, SQLAlchemy 2, Alembic | JSONB for event payloads |
| Storage | MinIO (dev) / S3 (prod) | audio, video |
| Speech | openai-whisper or faster-whisper; wav2vec2 | Phase 3 |
| Tests | pytest, httpx | fake-child fixtures for rules |
| Lint/format | ruff, black, mypy | |
| App | Flutter 3.x, Dart, Flame, Rive/Lottie, dio, drift/sqflite (offline queue) | owned by the Flutter developer |
| Dev infra | Docker Compose | api + postgres + minio |

## 5. Repo layout (target)

```
learning-ecosystem/
├── PRD.md
├── PROJECT.md              ← this file (also CLAUDE.md)
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── pyproject.toml
│   ├── alembic/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── models/         # SQLAlchemy tables
│   │   ├── schemas/        # Pydantic request/response + event schema
│   │   ├── api/            # routers: onboarding, children, consent, sessions, events, plans, profile
│   │   ├── onboarding/     # field list, validation, age-band logic
│   │   ├── scoring/        # per-activity extractors → skill dimension scores
│   │   ├── plan_engine/    # rules.py, engine.py
│   │   ├── week1/          # schedule, gate logic
│   │   ├── speech/         # Phase 3
│   │   └── safety/         # serious-signal flags
│   └── tests/
│       ├── fixtures/       # fake children + event streams
│       ├── test_events.py
│       ├── test_scoring.py
│       └── test_plan_engine.py
├── app/                    # Flutter project (Flutter developer)
├── docs/
│   ├── skill-dimensions.md # from Phase 0
│   ├── activity-signal-map.md
│   └── api-contract.md     # notes on top of OpenAPI
└── research/               # Phase 0 interview notes (no personal data)
```

## 6. Core domain model

### Skill dimensions (draft; finalise in Phase 0)

| key | Name | Main activities |
|---|---|---|
| `sustained_attention` | Sustained attention | Watch the pond |
| `impulse_control` | Impulse control | Stars not clouds, Wait for the bell |
| `distractibility` | Resistance to distraction | Distraction garden |
| `working_memory` | Working memory | Copy the pattern, Follow instructions |
| `auditory_comprehension` | Listening comprehension | Story and questions, Follow instructions |
| `reading_comprehension` | Reading comprehension | Read and answer |
| `articulation` | Articulation / phonology | Speak this line, Name the picture, Which word? |
| `expressive_language` | Expressive language | Retell the story, Name the picture |
| `social_communication` | Conversation & turn-taking | Chat with a character, What would you do? |
| `emotion_recognition` | Emotion recognition | How does she feel? |
| `self_confidence` | Confidence & persistence | About me, Oops try again, Level choice |
| `sensory_regulation` | Sensory comfort | Sensory setup, Mood check-in |

### Modules

`focus_attention`, `speech_language`, `social_emotional`, `confidence_builder`, `routine_sensory`

### Event schema (v0; the most important contract)

```json
{
  "event_id": "uuid (client-generated)",
  "child_id": "uuid",
  "session_id": "uuid",
  "activity_run_id": "uuid",
  "activity": "stars_not_clouds",
  "activity_version": "1.0.0",
  "event_type": "stimulus_shown | tap | response | audio_captured | skip | quit | retry | hint | mood | setting_changed | complete",
  "ts_client": "ISO-8601",
  "payload": { "target": "cloud", "correct": false, "reaction_ms": 412 }
}
```

- `payload` is free-form JSON per activity. Its shape is documented in `docs/activity-signal-map.md`.
- The server adds `ts_server`. Reject events whose `activity` is not registered.

### Onboarding (replaces the intake survey; 2–3 minutes)

One question per screen, Urdu or English, phone-friendly. Draft field list (final list is open decision D7):

| Field | Type | Required |
|---|---|---|
| consent (terms + audio + video toggles) | bool ×3 | yes |
| guardian name, relationship (mother/father/guardian/teacher) | text, enum | yes |
| guardian phone (login/OTP) | phone | yes |
| child name / nickname | text | yes |
| child date of birth | date | yes |
| area / city | enum + "other" | yes |
| schooling: `school` or `home_school` | enum | yes |
| school name, class/grade | text/fk, enum | if `school` |
| home languages | enum[] | yes |
| gender | enum | no |
| avatar | enum | no (child can pick on Day 1) |

What onboarding drives: `age_band` (from DOB) → content + starting difficulty; `home_languages` → UI language and voice lines; `schooling` → whether a teacher link/dashboard is offered. It drives **nothing** in scoring or activity order.

### Tables (v0)

| Table | Key columns |
|---|---|
| `guardians` | id, name, relationship, phone, locale, created_at |
| `children` | id, guardian_id, name, date_of_birth, gender?, area, schooling (school/home_school), school_id?, grade?, home_languages[], avatar?, onboarded_at, created_at |
| `schools` | id, name, area |
| `consents` | id, child_id, guardian_id, version, audio bool, video bool, teacher_share bool, granted_at, revoked_at? |
| `teacher_inputs` (optional, later) | id, child_id, teacher_id, notes jsonb, submitted_at |
| `sessions` | id, child_id, started_at, ended_at, device_info jsonb, mood_before?, mood_after? |
| `activity_runs` | id, session_id, activity, activity_version, day_index?, status (started/completed/skipped/quit), started_at, ended_at |
| `signal_events` | event_id PK, activity_run_id, child_id, event_type, ts_client, ts_server, payload jsonb |
| `media_objects` | id, child_id, activity_run_id, kind (audio/video), storage_key, consent_id, created_at |
| `skill_scores` | id, child_id, dimension, score 0–100, confidence 0–1, is_baseline bool, evidence jsonb, computed_at |
| `plans` | id, child_id, version, status (active/superseded), rationale jsonb, created_by (engine/therapist), created_at |
| `plan_modules` | plan_id, module, weight |
| `week1_progress` | child_id, day_index, completed_at |
| `safety_flags` | id, child_id, rule, evidence jsonb, status (open/reviewed/referred/dismissed), reviewer_id?, updated_at |

### API (v0)

| Method | Path | Purpose |
|---|---|---|
| POST | `/onboarding` | one call: guardian + child + consent (the whole 2–3 min flow) |
| GET | `/onboarding/options` | area list, school search, grades, languages |
| PATCH | `/children/{id}` | edit onboarding answers later |
| POST | `/children/{id}/consent` | update consent |
| POST | `/children/{id}/teacher-input` | optional, later |
| POST | `/sessions` | start session |
| PATCH | `/sessions/{id}` | end session, mood after |
| POST | `/activity-runs` | start activity |
| PATCH | `/activity-runs/{id}` | complete/skip/quit |
| POST | `/events/batch` | ingest events (idempotent) |
| GET | `/children/{id}/today` | activities for today (week-1 schedule or plan) |
| GET | `/children/{id}/profile` | skill scores + confidence + history |
| POST | `/children/{id}/score` | (internal/dev) recompute scores |
| GET | `/children/{id}/plan` | current plan + rationale |
| PUT | `/children/{id}/plan` | therapist override |
| POST | `/media/upload-url` | pre-signed URL (checks consent) |

Auth: JWT with roles `guardian`, `teacher`, `therapist`, `admin`. Can be stubbed until Phase 2.

### Plan engine (v0 rules; example shape)

```python
# plan_engine/rules.py
RULES = [
    Rule("low_attention",   when=lambda p: p.low("sustained_attention") or p.low("impulse_control"), add={"focus_attention": 1.0}),
    Rule("speech_need",     when=lambda p: p.low("articulation") or p.low("expressive_language"),   add={"speech_language": 1.0}),
    Rule("social_need",     when=lambda p: p.low("social_communication") or p.low("emotion_recognition"), add={"social_emotional": 1.0}),
    Rule("confidence_need", when=lambda p: p.low("self_confidence"), add={"confidence_builder": 1.0}),
    Rule("sensory_need",    when=lambda p: p.sensory_sensitive(),    add={"routine_sensory": 0.5}),
]
# p.low(dim) = score < 40 AND confidence >= 0.5
# Normalise → keep top 3 → weights sum to 1 → store the rules that fired as the rationale.
# Fallback when nothing fires: confidence_builder 0.5 + focus_attention 0.5.
```

The thresholds are placeholders. Tune them with Phase 0 input and pilot data.

## 7. Conventions

- Python: type hints everywhere, ruff + black, Pydantic schemas for all I/O, no business logic in routers (keep it in `scoring/`, `plan_engine/`, `week1/`).
- Activity keys: `snake_case`, versioned (`activity_version`). Changing a payload shape means bumping the version.
- Migrations: one Alembic migration per schema change, never edit an applied one.
- Tests: every scoring extractor and rule needs a fake-child test. Scoring must be deterministic.
- Commits: `feat:`, `fix:`, `chore:`, `docs:`, `test:`.
- Never commit real child data, audio or `.env`.
- Wording: UI and API text says "skill", "area to practise", "strength". Never "disorder", "symptom" or "diagnosis".

## 8. Local setup (fill in as it's built)

```bash
cp .env.example .env
docker compose up -d            # postgres + minio
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload   # http://localhost:8000/docs
pytest
```

## 9. Working with the Flutter developer

- Contract = OpenAPI at `/docs` + `docs/activity-signal-map.md` (event payload per activity).
- They can build against mock JSON before the API is live.
- Acceptance for each activity: the events it emits match the signal map exactly. Check it in `signal_events`.
- App responsibilities: games, animation, character, mic recording, sensory settings, offline queue with retry, locale.

## 10. Open decisions (mirror of PRD §11)

- [ ] D1 Language: Urdu / English / both
- [ ] D2 Target age range
- [ ] D3 Platform first (Android tablet likely)
- [ ] D4 Conversation partner: scripted character vs AI voice
- [ ] D5 Dashboards: Flutter web vs React
- [ ] D6 Hosting and data residency
- [ ] D7 Final onboarding field list (keep/drop gender, area list granularity)

## 11. Decision log

Record every decision here with its date and reason.

| Date | Decision | Why |
|---|---|---|
| 2026-09-23 | Backend = Python / FastAPI / Postgres | ML/speech is in Python; owner knows Python; OpenAPI contract for Flutter |
| 2026-09-23 | Rules-based plan engine before ML | Explainable, no training data yet |
| 2026-09-23 | First vertical: Stars not clouds, then Speak this line | No ML/mic needed to prove the loop; speech is Phase 3 |
| 2026-09-24 | Intake survey replaced by 2–3 min onboarding (name, DOB, area, school/home school, etc.) | Lower setup friction; needs info comes from week-1 play only; the week-1 order is the same for every child |

## 12. Current status

**Phase:** 0 (research) + 1 (backend foundation), in parallel
**Next up:**
1. [x] Scaffold repo + docker-compose (Postgres, MinIO)
2. [x] FastAPI skeleton + config + health check
3. [x] Event schema (Pydantic) + `signal_events` table + `POST /events/batch` (idempotent)
4. [ ] Core tables (guardians, children with onboarding fields, schools, consents) + Alembic migration
5. [ ] `POST /onboarding` + `GET /onboarding/options` + age-band helper (test that onboarding sets no scores)
6. [ ] Week-1 schedule + `GET /children/{id}/today`
7. [x] Scoring extractor for `stars_not_clouds`
8. [x] Plan engine v0 + fake-child tests
9. [ ] Write `docs/activity-signal-map.md` for the first 3 activities and hand it to the Flutter dev

## 13. Build log

Add a newest-first entry after each work session: what was built, files touched, what's left, any gotchas.

```
### YYYY-MM-DD
- Built:
- Files:
- Next:
- Notes/gotchas:
```

### 2026-09-24
- Built: repo scaffold (FastAPI skeleton, docker-compose, Alembic wiring, shared event schema, CI), pushed to GitHub; 17 tracking issues + branch protection on `main`; installed Docker Desktop + GitHub CLI locally and verified the full loop (`docker compose up -d` → `alembic upgrade head` → `pytest` → live `uvicorn` hitting `/health` and `/openapi.json`, plus MinIO health/console).
- Files: repo root (`README.md`, `CONTRIBUTING.md`, `TASKS.md`, `.github/`), `backend/app/{main,config,db}.py`, `backend/app/models/base.py`, `backend/app/schemas/events.py`, `backend/app/api/health.py`, `backend/alembic/`, `docker-compose.yml`.
- Next: Track A/B/C pick up their first issues (see `TASKS.md` / GitHub issues #1–#17).

### 2026-09-24 (later)
- Built: Track B complete for this pass — `signal_events` table, idempotent `POST /events/batch`, `skill_scores`/`plans`/`plan_modules` tables, the `stars_not_clouds` scoring extractor (impulse_control + sustained_attention, server-derived correctness, confidence scales with trial count), plan engine v0 (`rules.py`/`engine.py` matching PROJECT.md §6's example exactly), and `GET /children/{id}/profile` + `GET`/`PUT /children/{id}/plan`. Migrations verified upgrade/downgrade/upgrade against real Postgres at each step; 22 tests pass on `main`.
- Files: `backend/app/models/{events,scoring}.py`, `backend/app/api/{events,profile,plans}.py`, `backend/app/schemas/{profile,plans}.py`, `backend/app/scoring/stars_not_clouds.py`, `backend/app/plan_engine/{rules,engine}.py`, two new Alembic migrations, `backend/tests/` (11 new test files/fixtures).
- Next: Track A (identity/onboarding) and Track C (sessions/week-1/safety) are the remaining unclosed issues (#1–4, #11–16). Real gap to ticket: nothing yet wires "events land → scores recompute → engine generates a new plan" together — right now scoring and plan creation both exist as standalone pieces (extractor is a pure function nothing calls yet; `PUT /plan` only supports therapist override, not engine-generated plans). Needs an owner and an issue before Track B is *actually* done end to end, not just its listed checklist.
- Notes/gotchas: two migration/PR-process incidents this session, both recovered cleanly — (1) a PR accidentally merged into its stacked-parent branch instead of `main` (harmless, just meant one PR carried two issues' worth of changes); (2) real near-miss on two people generating an Alembic migration with `down_revision = None` at the same time (caught before it hit CI) — reinforces: always rebase onto latest `main` before `alembic revision --autogenerate`.
- Notes/gotchas: `minio/minio` was pulled entirely off Docker Hub — `docker-compose.yml` now points at `quay.io/minio/minio` instead. On a fresh Windows machine, Docker Desktop's "virtualization support not detected" error was fixed by `wsl --install --no-distribution` (elevated) + reboot, not a BIOS change.
