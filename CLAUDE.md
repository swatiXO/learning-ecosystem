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

### 2026-09-28 (Track C, #16)
- Built: `media_objects` table (`app/models/media.py` — real FKs to `children.id`, `activity_runs.id`, `consents.id`; `kind` CHECK-constrained to audio/video) and `POST /media/upload-url`. Checks, in order: child exists (404) → `activity_run_id` actually belongs to a session for *this* child, not just that it exists (404 — otherwise a client could attach media to another child's activity run by guessing its id) → the child's current active consent (`revoked_at IS NULL`, same lookup `POST /children/{id}/consent` already uses) has the `audio`/`video` flag matching `kind` (403 if not — rule #6, checked server-side, never trusted from the client). Presigned PUT URL is generated with boto3 against MinIO (`app/storage.py`) — signing is local/HMAC, no network call, so it's computed *before* the DB insert rather than after (a signing failure can't leave an orphan row with no usable URL).
- Also fixed a real gap this issue exposed: nothing provisioned the MinIO bucket the app is configured to use (`docker-compose.yml` only starts the MinIO *server*). Tried a `minio/mc` one-shot bootstrap container first (the standard pattern) - neither `minio/mc` nor `quay.io/minio/mc` pull in this environment (same Docker Hub distribution problem the 2026-09-24 build log entry already hit for `minio/minio` itself, apparently now hitting `mc` too). Went with `ensure_bucket_exists()` in `app/storage.py` instead, called from `app/main.py`'s FastAPI `lifespan` on every startup (idempotent - swallows `BucketAlreadyOwnedByYou`/`BucketAlreadyExists`, re-raises anything else) - no extra container needed.
- Verified end-to-end, not just via mocks: fresh Postgres *and* fresh MinIO volumes, `alembic upgrade head` → `downgrade -1` → `upgrade head`, then a real `uvicorn` process, a real `POST /media/upload-url` call, an actual `PUT` of bytes to the returned presigned URL (200), and `list_objects_v2` confirming the object landed in MinIO under the exact `storage_key`. 152 tests pass (6 new); ruff/black/mypy clean.
- Files: `backend/app/models/media.py`, `backend/app/api/media.py`, `backend/app/schemas/media.py`, `backend/app/storage.py`, `backend/app/main.py`, `backend/app/models/__init__.py`, `backend/pyproject.toml` (added `boto3`), `backend/alembic/versions/35d78e387717_create_media_objects_table.py`, `backend/tests/test_media_api.py`, `docker-compose.yml` (net no-op — added then removed the `mc` service once it proved unpullable).
- Next: this was the last of the 6 originally-scoped Track C issues (#11-#16). Remaining open cross-track gaps this track's build log has flagged along the way, for whoever picks them up: no module→activity catalog (#14), nothing auto-triggers plan regeneration when week 1 completes (#14), nothing calls `flag_serious_signals()` yet (#15).
- Notes/gotchas: `Consent`→`Child` has no cascade delete (`children.guardian_id` FK has none either) - deleting a `Guardian`/`Child` in a script or test needs to delete `Child` before `Guardian` explicitly; found this the manual way while cleaning up the end-to-end verification's own test data.

### 2026-09-28 (Track C, #15)
- Built: `safety_flags` table (`app/models/safety.py` — status CHECK-constrained to open/reviewed/referred/dismissed; `child_id` has a real FK to `children.id` now that Track A's identity tables are on `main`, unlike sessions/activity_runs/signal_events/skill_scores which predate it and still don't) and serious-signal rule definitions (`app/safety/rules.py`, `service.py`). Rules reuse Track B's `plan_engine.rules.Profile` directly (latest skill score per dimension) rather than re-deriving it — same shape, no reason to duplicate it. Threshold is deliberately much stricter than plan_engine's "low" (score < 15 vs < 40, same confidence ≥ 0.5 gate): plan_engine's threshold is expected to fire often (it drives normal module selection), a safety signal needs to be rare. PLACEHOLDER pending Phase 0 clinical input, same caveat PROJECT.md already puts on plan_engine's thresholds. `flag_serious_signals()` is idempotent per rule — won't open a duplicate flag while one's already `open` for the same child+rule, but does re-flag if a prior flag was resolved (dismissed/reviewed) and the condition still holds. Rule #8/FR-27: firing a rule only ever inserts a row for a human to look at later — nothing here contacts anyone or changes a score/plan.
- Files: `backend/app/models/safety.py`, `backend/app/safety/rules.py`, `backend/app/safety/service.py`, `backend/app/models/__init__.py`, `backend/alembic/versions/313935531bb7_create_safety_flags_table.py`, `backend/tests/test_safety_model.py`, `backend/tests/test_safety_rules.py`, `backend/tests/test_safety_service.py`.
- Next: #16 media upload (depends on Track A's `consents` table, which is on `main` now — unblocked).
- Notes/gotchas: **nothing calls `flag_serious_signals()` anywhere yet** — no endpoint owns this per the API v0 table (there's no `/safety` route listed), and the natural trigger point (after every score recompute? after every session? a scheduled sweep?) is a cross-track/product call, not something to guess at here. Same class of gap as #14's plan-generation trigger. Also: only skill-score-based rules exist for now; session-level signals (extreme quit rates, mood) would need a defined mood vocabulary and a decision about what counts as "extreme" — deliberately not invented here, same reasoning as #14's missing module→activity catalog.

### 2026-09-28 (Track C, #14)
- Built: `GET /children/{id}/today`. While `current_day_index()` (#13) is not `None`, returns that day's scheduled activities (`phase: "week1"`). Once week 1 is complete, looks up the active plan (`plan_engine.service.current_plan`, from Track B) and returns `phase: "plan"` with the `plan_id`. 404s (not a 500 or a misleadingly-empty 200) if week 1 is done but no active plan exists yet.
- Files: `backend/app/api/today.py`, `backend/app/schemas/today.py`, `backend/app/main.py`, `backend/tests/test_today_api.py`.
- Next: #15 safety flags, #16 media upload (both unblocked, independent of this).
- Notes/gotchas — two real gaps this issue surfaced but does not fix, both flagged rather than papered over:
  1. **No module → activity catalog exists.** PRD FR-18 ("each module a set of activities tagged by skill and difficulty") isn't built by any track yet — so once `phase: "plan"`, `activities` is always `[]`. This needs a product/content decision (which activities belong to which module), not an engineering guess, before anyone can fill it in.
  2. **Nothing auto-generates a plan when week 1 finishes.** `regenerate_plan()` (Track B) exists but nothing calls it automatically — today a plan only exists if `PUT /plan` (therapist override) was used. Until something wires "week1 complete -> recompute scores -> regenerate plan", every child will hit the 404 branch here the moment they finish day 7. Same underlying gap Track B's own 2026-09-24 build log entry already flagged from the other side (scores -> plan wiring); this is the missing "week1 done -> trigger it" half.
- Depends on #13 (branched from `track-c/week1-schedule-gate`, not `main`) — PR is stacked and should be reviewed/merged after #36.

### 2026-09-28 (Track C, #13)
- Built: the 7-day week-1 schedule (`app/week1/schedule.py`, matching PRD §6.2's table exactly — day 7 repeats `stars_not_clouds`/`speak_this_line` per FR-9) and gate logic (`app/week1/gate.py`): `current_day_index` (next unfinished day, or `None` once week 1 is done), `is_week1_complete`, and `try_complete_day` (marks a day done once every scheduled activity has a terminal — completed/skipped/**or quit**, rule #5 — run against it). Wired `try_complete_day` into `PATCH /activity-runs/{id}` (#12) so a day actually gets marked complete as its activities finish, rather than leaving `week1_progress` a table nothing ever writes to. No calendar/date logic anywhere — completion is purely "which days have all their activities logged", so a missed day never costs the child anything (FR-7).
- Files: `backend/app/week1/schedule.py`, `backend/app/week1/gate.py`, `backend/app/api/activity_runs.py`, `backend/tests/test_week1_schedule.py`, `backend/tests/test_week1_gate.py`, `backend/tests/test_activity_runs_api.py` (added an end-to-end gate-wiring test).
- Next: #14 `GET /children/{id}/today` (depends on this — will call `current_day_index`/`activities_for_day` for week-1, fall back to the active plan once `is_week1_complete`), #15 safety flags (unblocked), #16 media upload (depends on Track A's `consents` table).
- Notes/gotchas: `try_complete_day` is idempotent (`ON CONFLICT DO NOTHING` against the `week1_progress` PK) and safe to call on every activity-run status change, not just the one that happens to finish the day — simpler than trying to detect "was this the last one" and it self-heals if a call site is ever missed. No day-ordering is enforced on `POST /activity-runs` itself (out of #12's scope); `try_complete_day` only checks "are this day's activities done", not "was the previous day done first".

### 2026-09-28 (Track C, #12)
- Built: `POST /sessions`, `PATCH /sessions/{id}` (ends session, records mood after), `POST /activity-runs`, `PATCH /activity-runs/{id}` (complete/skip/quit — status is a closed `Literal`, so a "failed" status 422s before it ever reaches the DB constraint from #11; rule #5). `POST /activity-runs` 404s on an unknown `session_id` instead of surfacing the FK violation as a 500. `activity` is validated against the same `REGISTERED_ACTIVITIES` set events already use. Both PATCH endpoints are first-write-wins/idempotent for a retried request with the same value; `PATCH /activity-runs/{id}` uses a conditional `UPDATE ... WHERE status = 'started'` (checked via rowcount) rather than a plain ORM read-then-write, so two concurrent PATCHes with different terminal statuses can't race past the check-then-set gap — the loser gets a clean 409 instead of silently overwriting the winner's status. Verified end-to-end: fresh-DB `alembic upgrade head`, `downgrade -3` → `upgrade head` round-trip, ruff/black/mypy clean, all 74 tests pass (57 existing + 17 new).
- Files: `backend/app/api/sessions.py`, `backend/app/api/activity_runs.py`, `backend/app/schemas/sessions.py`, `backend/app/schemas/activity_runs.py`, `backend/app/main.py`, `backend/tests/test_sessions_api.py`, `backend/tests/test_activity_runs_api.py`.
- Next: #13 week-1 schedule + gate logic, #15 safety flags (both unblocked), then #14 (`GET /today`, depends on #13) and #16 (media upload, depends on Track A's `consents` table).
- Notes/gotchas: no migration needed — #11 already created `sessions`/`activity_runs`; this issue was API-only. `child_id`/`session_id` still have no FK to a `children` table (Track A isn't merged yet), so a session can be created for any UUID — same tradeoff `signal_events` already made.

### 2026-09-24 (Track C, #11)
- Built: `sessions`, `activity_runs`, `week1_progress` tables + migration `0d07cdd64f6b` (revises `c1236465921b`). `activity_runs.status` is DB-constrained to started/completed/skipped/quit (rule #5, no fail state). `day_index` is constrained to 1–7. `week1_progress` has one row per completed day (PK child_id + day_index), so missed calendar days add nothing (FR-7). Verified upgrade → downgrade → upgrade, and a from-scratch `upgrade head` on an empty DB; 30 tests pass.
- Files: `backend/app/models/sessions.py`, `backend/app/models/__init__.py`, `backend/alembic/versions/0d07cdd64f6b_create_session_tables.py`, `backend/tests/test_sessions_model.py`.
- Next: #12 sessions + activity-runs API, #13 week-1 schedule + gate.
- Notes/gotchas: the ORM class is `ChildSession` (table `sessions`) so it never shadows `sqlalchemy.orm.Session` in routers. `child_id` is an indexed UUID with **no FK** yet, the same as `signal_events`/`skill_scores`, because Track A's `children` table isn't on `main`; add the FK in a follow-up migration once it lands.

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
