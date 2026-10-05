# PROJECT.md: Learning Ecosystem

> The living context file for this repo. Read this first, whether you are a human or an AI coding assistant (Claude Code, Copilot, Cursor).
> Product requirements are in `PRD.md`. **This file covers how it is built and where it currently stands.** Update the Status, Decisions and Build Log sections every time something is built or changed.
> Tip: if you use Claude Code, copy or symlink this file as `CLAUDE.md` so it loads automatically.

---

## 1. What we are building (one paragraph)

A learning app for children with ADHD, autism and low self-esteem. **It is not a diagnostic tool** — it never outputs diagnosis labels. Setup is a 2–3 minute **onboarding** of simple context questions (name, date of birth, area, school or home school). There is **no intake survey**. A 7-day game-based first week logs behavioural signals. These become a **needs profile** (skill scores + confidence, **never diagnosis labels**). A rules-based **plan engine** assigns 1–3 weighted modules (Focus & attention, Speech & language, Social-emotional, Confidence builder, Routine & sensory) — this five-module set is, and has always been, the actual intervention. Once week 1 is complete, delivery of that intervention is via an AI **tutor agent** that adapts content live within the plan's module weights (see §12); week 1 itself stays fully scripted and agent-free so every child's baseline is measured under the same conditions. The app re-evaluates every 6–8 weeks against the child's own baseline. Parents, teachers and therapists have dashboards, and serious signals go to a human for referral.

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

- [x] D1 Language: resolved 2026-10-05 — both Urdu and English; Urdu means both Urdu script and Roman Urdu (see decision log)
- [x] D2 Target age range: resolved 2026-10-05 — 5–12 (briefly logged as 5–18 earlier the same day; revised)
- [x] D3 Platform first: resolved 2026-10-05 — Android tablet
- [x] D4 Conversation partner: resolved 2026-09-29 — mixed per activity (see decision log)
- [x] D5 Dashboards: resolved 2026-10-05 — Flutter (web)
- [ ] D6 Hosting and data residency — access model resolved 2026-10-05 (see decision log); server country still open
- [x] D7 Final onboarding field list: resolved 2026-10-05 — keep gender; every option list kept to the minimum actually needed
- [ ] D8 LLM hosting for the tutor: hybrid (small on-device model for a very limited offline mode + cloud model online) is the working direction; Urdu/Roman-Urdu model choice pending owner's own research — architecture must keep the model layer swappable

## 11. Decision log

Record every decision here with its date and reason.

| Date | Decision | Why |
|---|---|---|
| 2026-09-23 | Backend = Python / FastAPI / Postgres | ML/speech is in Python; owner knows Python; OpenAPI contract for Flutter |
| 2026-09-23 | Rules-based plan engine before ML | Explainable, no training data yet |
| 2026-09-23 | First vertical: Stars not clouds, then Speak this line | No ML/mic needed to prove the loop; speech is Phase 3 |
| 2026-09-24 | Intake survey replaced by 2–3 min onboarding (name, DOB, area, school/home school, etc.) | Lower setup friction; needs info comes from week-1 play only; the week-1 order is the same for every child |
| 2026-09-29 | Product direction: the app is a tutoring application — an AI agent-based tutor whose profile comes from week-1 play, using the games/API as tools, adapting delivery to the child's weak areas. Rule #8 (referrals and plan overrides require a human action) stays as-is under this direction. | Owner's original intent, only now made explicit; rule #8 is a written safety boundary for a vulnerable population, not a delivery-capability question, so agent capability doesn't change it — confirmed explicitly rather than assumed |
| 2026-09-29 | Interest-based content personalization uses a curated template library (~15–20 pre-authored, pre-reviewed themes the agent matches/fills), not open per-child generation | Research found reskinning isn't automatically score-neutral even with mechanics held fixed (stimulus salience/preference independently moves RT/accuracy in autism and ADHD specifically); a small reviewed set is what bounds hallucination, stereotyping, and makes per-template validation tractable — matches the only pattern industry precedent (Khanmigo, Duolingo Max) actually uses |
| 2026-09-29 | No item wording, question structure, or scoring formula from any established clinical screening instrument (M-CHAT-R/F, SCQ, CAST, AQ-Child/Adolescent, SRS-2) may be used as a template for our own onboarding, activities, or scoring — even loosely | 3 of 5 are fully commercial/publisher-controlled (SCQ, SRS-2, AQ-family for commercial use — WPS, Mapi/ePROVIDE); the 2 "free" ones (M-CHAT-R/F, CAST) still forbid modification. Infringement risk aside, also consistent with rule #1 — this app is deliberately not a diagnostic instrument |
| 2026-09-29 | `signal_events` gets a `source` field (`game`/`agent`, plus `model` and `prompt_version` when agent-sourced); scoring extractors treat agent-sourced events as provisional until validated against therapist/teacher ratings, never as immediate ground truth | Team review caught a real gap: nothing distinguished a game-produced event from an agent-produced one, so an agent emitting e.g. a dialogue outcome would become a permanent `skill_score` with no trace an LLM judged it — contradicting §12's own rule that agent social-emotional judgment must not silently become a score |
| 2026-09-29 | Week 1 stays fully scripted and agent-free; the tutor agent's activity-selection/adaptation role begins only once week 1 is complete | Baseline comparability (rule #3) requires every child to be measured under the same conditions; letting the agent influence week 1 would make day-7 baselines incomparable across children |
| 2026-09-29 | Tutor architecture adds an explicit Learner State layer (skill estimate + confidence + evidence_count + engagement/persistence, tracked separately from skill) and an Adaptive Policy layer between it and the agent: `Events → Scoring → Learner State → Adaptive Policy → Tutor Agent`. The agent picks only within the set of activities/actions the Adaptive Policy allows, and every pick is logged with a rationale | Proposed in a teammate's architecture review; makes "the agent stays within the plan's module weights" true by construction rather than by prompt instruction — same enforcement principle as rule #8's tool-omission, applied one layer up |
| 2026-09-29 | Safety spec for live tutor dialogue expanded beyond a denylist: pre-publication output check (not just banned words), a disclosure path routing revealed harm/distress to a human under rule #8, handling of children pushing the agent off-topic or attempting to manipulate it, session time limits, explicit mitigation for emotional dependence on the tutor (a specific risk for this app's low-self-esteem population), clear AI disclosure to both child and parent, and a check of the LLM provider's terms and data-retention policy for a product used by minors | None of this was in the original tutor-agent design; a denylist alone is not an adequate safety layer for live AI talking to vulnerable children |
| 2026-09-29 | Adopted sequencing: first tutor-agent work is a `confidence_builder`-only spike behind a feature flag, tested with adults before any child — run in parallel with, not blocking on, closing existing blockers (API auth/roles are stubbed open; no FKs yet from `signal_events`/`skill_scores`/`plans`/`sessions`/`week1_progress` to `children`; nothing calls `flag_serious_signals()`; Phase 0 interviews haven't started) | Team review's recommendation: the tutor is a large new system layered on a backend that doesn't yet enforce its own existing safety/auth guarantees; de-risk with the smallest slice before committing further |
| 2026-09-29 | Corrected: earlier design discussion implicitly assumed live open-mic conversation for the tutor without resolving open decision D4 (conversation partner). Reverted to unresolved — D4 stays open in §10. Default until decided: tutor dialogue activities are text/tap-choice only; voice stays scoped to its original Phase 3 plan | A silent reversal of an open decision was caught by team review; a call with real cost/privacy/offline/minors-ToS consequences needs an explicit owner decision, not an inherited assumption |
| 2026-09-29 | "Tutor" scope, pending confirmation: default is the five skill modules only (coaching on focus/speech/social/confidence/sensory-regulation) — not school-subject/curriculum teaching, which would be a materially larger, unresearched scope change | Flagged by team review; needs a one-sentence resolution from the owner, logged here once given |
| 2026-09-29 | **D4 resolved: mixed, per activity.** Most tutor dialogue activities (`what_would_you_do`, `about_me`, `story_and_questions`, etc.) are text/tap-choice only — no live voice understanding, no new consent, stays offline-tolerant. The activities already scoped for audio capture before the tutor-agent direction existed (`speak_this_line`, `chat_with_a_character`) keep that original Phase 3 plan, scored once the speech pipeline lands — not a new decision for those. | Owner's call. Avoids a blanket voice-vs-text choice: most of the tutor's new dialogue surface stays low-risk, while the activities that already needed audio keep the scope they always had |
| 2026-10-05 | **Tutor scope resolved: skill modules + school subjects + open learning.** The tutor covers the five skill modules, the 12 primary subjects taught on the owner's LMS (template-supported, same curated-template principle as the 2026-09-29 personalization decision), and anything else the student wants to learn via open chatbot-style conversation (non-template). Conditions: (a) open chat gets the full safety layer (pre-publication output check, age-banded topic limits for 5–12) — "like a regular chatbot" never means unfiltered; (b) learning difficulties the agent identifies in conversation may be added to the profile, but only as agent-sourced, provisional evidence (`source="agent"`), worded as skills/areas to practise (rule #1), and never touching the week-1 baseline (rule #3); (c) subject learning needs its own per-subject/per-concept mastery tracking alongside — not inside — the 12 skill dimensions | Owner's call. Supersedes the 2026-09-29 "five modules only" default. Open topics remove the bounded-content guarantee the template library gave, so the output check becomes the primary safety layer rather than a backstop; subject concepts ("fractions") are a different construct from skill dimensions ("working memory") and would corrupt `skill_scores` if mixed in. Pending from owner: the 12 subject names and whether lesson content can be sourced from the LMS |
| 2026-10-05 | **LMS is the lesson-content source.** Subject content comes straight from the owner's LMS. The 12 subjects = Pakistan's core school subjects (maths, science, English, Urdu, etc. — exact list to be confirmed) + four custom subjects: **AI Mind**, **Media Mind**, **Social and Emotional Learning**, **Environmental Literacy**. Open question: how the SEL *subject* relates to the existing `social_emotional` skill *module* (likely: SEL lessons are content the module draws on, with one source of truth for `social_communication`/`emotion_recognition` scores — never tracked twice) | Owner's call; avoids authoring subject content twice. LMS integration (API/export format, how lessons map to concepts for per-concept mastery tracking) is new engineering work |
| 2026-10-05 | D1: Urdu and English, where Urdu means **both Urdu script and Roman Urdu** (and code-mixed English). D2: ages 5–18 (revised later the same day to **5–12**, see below). D3: **Android tablet** first. D5: dashboards in **Flutter**. D7: keep gender, minimal option lists | Owner's calls. Superseded for D2 by the 5–12 row below |
| 2026-10-05 | D6 (access model): not "no human can ever read it" (contradicts rule #7/#8 — safety review, referrals and therapist overrides need a human to read data, and operators can technically access it anyway). Instead: encryption at rest, least-privilege access per role, audit log of every human access to a child's data, raw audio/video kept on-device where possible. Server country still open | Owner accepted the realistic version of the privacy goal |
| 2026-10-05 | Notifications split in two. **Learning-struggle notices** ("finding fractions tricky, here's how to help") go to the parent/guardian, but only after the tutor has tried other approaches first. **Serious safety flags** (`flag_serious_signals()`, disclosure of harm/distress) go to the owner's own team, who review and decide whether to contact the family — never auto-sent to the parent. `flag_serious_signals()` runs after every score recompute | If a child discloses harm, the person responsible may be at home — auto-notifying the guardian could endanger the child; safeguarding practice routes to a trained human first, consistent with rule #8 |
| 2026-10-05 | "Extreme" struggle signal, two tiers (thresholds are placeholders): tier 1 — e.g. ≥3 quits/retries on the same activity in one session → tutor adapts (eases off, switches approach); tier 2 — e.g. frustrated/stuck across ≥3 sessions in 7 days → opens a flag for human review | Owner defined "extreme" as repeatedly annoyed or stuck; two tiers keep rule #5 (quits are comfort signals, not failures) — the tutor responds first, a human only sees persistent patterns |
| 2026-10-05 | Full re-evaluation scheduled every **6 weeks**; skill scores still recompute continuously as events arrive | Owner's call; resolves PRD's "6–8 weeks" range |
| 2026-10-05 | **D2 revised: ages 5–12** (replaces 5–18 logged earlier the same day). Age bands: **5–7, 8–10, 11–12**. Onboarding accepts ages 5–12 only; a child who turns 13 while using the app stays in the 11–12 band rather than being locked out | Owner's call. Brings the product back to the population the activities, research and PRD were designed around; removes the need for teen-specific content, art and wording. Every activity still needs per-band content for 5–7 / 8–10 / 11–12 (#57) |
| 2026-10-05 | LLM hosting direction: hybrid — very limited offline mode on-device, real tutoring via a cloud model (zero data retention, terms that permit minors' products) when online. Urdu-script + Roman-Urdu model choice is **deferred to the owner's own research**; no fine-tuning until an eval shows a gap. Architecture must keep the model behind a swappable interface and treat offline as a reduced-capability mode (pre-written lines may suffice there) | Small models are weak at Urdu, factual teaching and safety; fine-tuning first needs data that doesn't exist yet and can degrade safety behaviour. Deferred, but must not be designed out |

## 12. Tutor-agent delivery model (per module)

Corrects a framing mistake in `docs/activity-signal-map.md`'s "blocked on content design" / "blocked on Phase 3" labels: those meant *the deterministic scoring extractor needs a pre-authored rubric*, not *a human must be in this interaction*. Under the tutor-agent direction (§1, decision log 2026-09-29), the question per item is:

1. **Agent-buildable now** — the agent can read the child's response in context and use its own judgment instead of a fixed rubric, or a known tool (ASR, etc.) closes the gap. No human rubric-author needed.
2. **Needs pilot validation** — the *technique* is evidence-backed, but "an LLM delivering it to this population" is untested. Treat the agent's output here as a hypothesis to check against real therapist/teacher judgment before it becomes ground truth in the profile, not as an established fact from day one.
3. **Stays human** — only rule #8 (referrals and plan overrides). Not a delivery-capability gap; a safety boundary, confirmed to hold as-is.

### `focus_attention` (sustained_attention, impulse_control, distractibility)
- Agent-buildable: `stars_not_clouds`, `watch_the_pond`, `wait_for_the_bell`, `distraction_garden` stay as diagnostic/practice tools the agent calls.
- Needs pilot validation: near-transfer from repeated play is real, far-transfer to real-world attention is mostly unproven (the cross-cutting finding from the 2026-09-29 research pass) — so the agent's job isn't "more reps," it's explicit *generalization coaching* in dialogue ("where at school could this skill help you?"), which a fixed game can't do but a conversational agent can. Whether that dialogue actually produces far-transfer still needs a pilot check.

### `speech_language` (articulation, expressive_language, auditory_comprehension, reading_comprehension)
- Agent-buildable: `speak_this_line`/`retell_the_story`/`chat_with_a_character` were only "blocked on Phase 3" for lack of a speech pipeline, not lack of a human — ASR (Whisper/wav2vec2) as a tool plus an LLM layer judging pragmatics/topic-maintenance is the clean agent-with-tools case. Reading comprehension suits Socratic follow-up questioning over a fixed multiple-choice check.
- Needs pilot validation: articulation scoring from ASR output, for this age range and accent variety, should be checked against a human SLP's rating before it drives plan weighting.

### `social_emotional` (social_communication, emotion_recognition)
- Agent-buildable technically: `what_would_you_do`/`about_me` can become live dialogue instead of a fixed-choice rubric.
- Needs pilot validation — the most caution of any module: LLM social/emotional judgment for autistic/ADHD children specifically is the least-validated area in the research pass. The agent's qualitative read of a social interaction should not silently become a `skill_score` without comparing it against real teacher/therapist ratings first.

### `confidence_builder` (self_confidence)
- Agent-buildable, the strongest fit: Bandura self-efficacy theory and the Mueller & Dweck effort-vs-ability praise finding are both about *exact wording*, applied consistently and adaptively — what an LLM does better than a fixed game script. `oops_try_again`, `about_me`, `level_choice` become places the agent actively chooses effort-praise language instead of passively logging a choice.

### `routine_sensory` (sensory_regulation)
- Most limited role for the agent: least-explored module in the research pass, and `sensory_setup`'s signal (calm-mode toggle rate) is mechanical, not something dialogue improves on directly. Agent's job is closer to noticing a pattern and surfacing it to the guardian than delivering an intervention to the child directly.

The `working_memory`/broader `auditory_comprehension`/`reading_comprehension` dimensions not yet wired to a plan-engine rule (see §6, open item) get the same agent-buildable / needs-validation split once that wiring lands — no separate treatment needed.

### Interest-based personalization (added 2026-09-29, research-backed)

New construct: `child_interests` (id, child_id, label, source [agent_inferred/guardian_reported/child_stated], confidence, evidence jsonb, created_at) — same explainability pattern as `skill_scores`. Not sourced from onboarding (rule #10 keeps onboarding context-only); sourced from the tutor agent's own dialogue activities and optional guardian input. **Prefer explicit (child/guardian-stated) interests over agent-inferred ones** for anything used to personalize content — inferring demographic/interest profiles from behavior alone is a documented stereotyping exposure path (see below).

Evidence for the underlying idea:
- **Autism**: solid, direct evidence that embedding a child's circumscribed/special interest into instruction increases engagement and on-task behavior, and at least one pilot found real reading-comprehension gains from a rewritten-vs-neutral version of the same passage — closest published analogue to this app's reskin design (Gunn & Delafield-Butt 2016; Harrop et al. 2019; Developmental Neurorehabilitation 2014 pilot). Caveat: practitioners distinguish genuine flexible interest from rigid perseveration — leaning on a fixation can reinforce rigidity instead of building skill; unquantified for a digital product.
- **ADHD**: much thinner evidence. A 2024 pilot found enjoyment/preference and raw performance metrics did **not** move together in lockstep — explicit caution against assuming "more preferred theme = better score."
- **General personalization theory** (Walkington, algebra tutoring): a hard split between "surface" personalization (swap a name/object — reliably raises interest, does **not** reliably raise performance) and "deep" personalization (match the theme to how the child actually reasons in that domain — the version that improves learning). Reskinning a timing-based attention game's art is surface personalization by this definition.
- **Cognitive-load risk**: the "seductive details" literature shows task-irrelevant flavor/narrative content imposes extraneous cognitive load and measurably *hurts* performance, worse when the base task already demands sustained attention — directly relevant to this app's population.

**This overturns an initial framing from this same session** ("mechanics fixed, theme purely cosmetic = automatically score-neutral"). Dedicated measurement-validity research found that even holding every timing/trial parameter constant, a personally-preferred or unfamiliar stimulus set can independently shift reaction time and accuracy — documented in autism specifically (attentional bias toward circumscribed-interest stimuli) and separately in ADHD (novel/salient stimuli change attentional performance). The two populations this app serves are exactly the ones where "just reskin the art" is least safe to assume is score-neutral.

Revised constraints:
1. **Curated template library, not open generation.** The agent matches a child's recorded interest to the closest of a small, pre-authored, pre-reviewed set of theme templates (~15–20) and fills child-specific slots inside it, rather than generating an arbitrary new theme per child. Matches the only pattern every safety-conscious precedent (Khanmigo, Duolingo Max) actually uses: generation constrained inside a fixed structure, never open-ended for child-facing output. Bounds hallucination, bounds stereotyping risk (each template human-reviewed once), and makes validation (#4) tractable — validate a template once, reuse across children.
2. **Normalize low-level stimulus properties across templates** (image size, contrast/luminance, animation complexity, audio-cue timing), not just category labels — no template should be inherently more/less salient than another.
3. **Never let personalization pick which entity is the target vs. non-target based on preference.** The preferred item becoming "the one you tap" is the exact attentional-bias confound the research flags. Target/non-target role assignment stays fixed per template regardless of theme.
4. **Pilot each template before trusting it**: same task parameters, compare RT/accuracy distributions across a couple of themes on a small sample — the way parallel test forms get equated, not a formality.
5. **Pin a child's theme for as long as their scores are being trended; a theme change is a logged baseline-reset event** — extends rule #3 ("baseline, not norms") to cover this.
6. **Track theme/template id as a first-class field** in scoring evidence so any future between-theme discrepancy is analyzable, not silently absorbed into `skill_scores`.
7. **Content safety, independent of validity**: pre-publication schema/allowlist filter on any generated slot content before it reaches a child (stricter than industry's post-hoc-report norm, appropriate for this population); log every generated instance with its source template + prompt for bias audit (rule #7).
8. **"Deep" personalization only where content has real structure to match it to** — dialogue/social-scenario activities and reading passages can plausibly get real outcome gains from matching an interest's internal logic (Walkington's "deep" case); a timing-based attention game mostly can't, so keep expectations calibrated per activity: reskinning `stars_not_clouds` buys engagement, not necessarily better attention scores.

### Scope review (2026-09-29) — corrections from team review

A teammate review of the tutor-agent direction above found real gaps, now corrected here (short version; full detail in the decision log):

1. **Framing.** This project was never a "screening tool" — PRD.md is explicit: "It is not a diagnostic tool... gives skill scores." The five modules were always the intervention. What the tutor-agent direction changes is the *delivery mechanism* (pre-designed games/scripts → an LLM agent), not the product's fundamental nature. §1 corrected to say this directly.
2. **Event provenance was a real bug, not a style note.** `signal_events` had no field distinguishing a game-produced event from an agent-produced one. An agent emitting a dialogue outcome would become a permanent `skill_score` with no trace an LLM judged it — directly contradicting this same section's own rule that agent social-emotional judgment must not silently become a score. **Fix**: `signal_events` gets a `source` field (`game`/`agent`, + `model`/`prompt_version` when agent-sourced); scoring extractors treat agent-sourced events as provisional until validated against a therapist/teacher rating.
3. **Week 1 must stay agent-free.** Baseline comparability (rule #3) only holds if every child is measured under the same conditions. The agent's role in picking/adapting activities now explicitly begins only after week 1 completes.
4. **Learner State + Adaptive Policy layers** (proposed by a teammate's architecture review, adopted): the pipeline becomes `Events → Scoring → Learner State → Adaptive Policy → Tutor Agent`. Learner State holds skill estimate + confidence + evidence_count + engagement/persistence, tracked separately from skill itself (low engagement ≠ low ability). Adaptive Policy is a rules layer (same spirit as `plan_engine`, one level down) that computes the *allowed* set of activities/actions from Learner State + the active plan's module weights; the tutor agent picks only within that allowed set and logs why (`tutor_turns`). This is what makes "the agent stays within the plan's module weights" true by construction instead of by prompt instruction — same enforcement principle as rule #8's tool-omission, applied one layer up. Low-confidence estimates should favor more observation, not more personalization. Recent evidence should be weighted more than old evidence as the child develops (temporal weighting) — not yet implemented, logged for when `scoring/common.py`'s confidence function is next revisited.
5. **Safety spec, expanded.** A denylist filter alone is not adequate for live AI talking to vulnerable children. Required before any child session: an output check before a message reaches a child (a real check, not just banned words), a disclosure path that routes revealed harm/distress to a human under rule #8, handling of a child trying to push the agent off-topic or manipulate it, session time limits, explicit design against emotional dependence on the tutor (a specific risk given this app's low-self-esteem population), clear AI disclosure to both child and parent, and a check of the LLM provider's terms and data-retention policy for a product used by minors.
6. **Sequencing, adopted.** First tutor-agent work is a `confidence_builder`-only spike behind a feature flag, tested with adults before any child — in parallel with, not blocking on, closing existing blockers (API auth/roles are stubbed open; no FKs yet from `signal_events`/`skill_scores`/`plans`/`sessions`/`week1_progress` to `children`; nothing calls `flag_serious_signals()`; Phase 0 interviews haven't started).
7. **Two items reverted to genuinely open, then one resolved.** D4 (conversation partner) had been implicitly assumed rather than decided — flagged back to the owner and **resolved 2026-09-29: mixed per activity** (text/tap-choice for most tutor dialogue; the activities already scoped for audio before the tutor-agent direction existed keep that original plan — see decision log). "Tutor" scope was **resolved 2026-10-05**: skill modules + the 12 LMS subjects (template-supported) + open chat for anything else (see decision log).

Cost/latency per tutor turn also isn't estimated yet — flagged, not blocking the spike (a single-module, adults-only spike is cheap enough to measure directly rather than estimate first).

## 13. Current status

**Phase:** 0 (research) + 1 (backend foundation), in parallel
**Next up:**
1. [x] Scaffold repo + docker-compose (Postgres, MinIO)
2. [x] FastAPI skeleton + config + health check
3. [x] Event schema (Pydantic) + `signal_events` table + `POST /events/batch` (idempotent)
4. [x] Core tables (guardians, children with onboarding fields, schools, consents) + Alembic migration
5. [x] `POST /onboarding` + `GET /onboarding/options` + age-band helper (test that onboarding sets no scores)
6. [x] Week-1 schedule + `GET /children/{id}/today`
7. [x] Scoring extractor for `stars_not_clouds`
8. [x] Plan engine v0 + fake-child tests
9. [ ] Write `docs/activity-signal-map.md` for the first 3 activities and hand it to the Flutter dev

## 14. Build log

Add a newest-first entry after each work session: what was built, files touched, what's left, any gotchas.

```
### YYYY-MM-DD
- Built:
- Files:
- Next:
- Notes/gotchas:
```

### 2026-10-05 (owner decisions)
- Built: no code — owner answered the open-questions round. Resolved D1 (Urdu script + Roman Urdu + English), D2 (5–12; briefly 5–18, revised same day), D3 (Android tablet), D5 (Flutter), D7 (keep gender, minimal lists), tutor scope (skill modules + 12 LMS subjects with templates + open chat for anything else), D6's access model (encryption + least privilege + audit log; country still open), notification split (learning-struggle → parent after the tutor tries first; safety flags → owner's team), two-tier "extreme struggle" definition, 6-week scheduled re-evaluation, `flag_serious_signals()` runs after every recompute. LLM hosting direction set (hybrid), Urdu model research taken on by the owner — logged as D8. Added `.claude/launch.json` (`backend` config) for one-click dev server.
- Files: `PROJECT.md`, `CLAUDE.md`, `.claude/launch.json`.
- Next: (a) confirm the exact core-subject list (custom four known: AI Mind, Media Mind, SEL, Environmental Literacy) and how the LMS exposes content; settle SEL-subject vs `social_emotional`-module overlap; (b) design per-concept subject mastery tracking (separate from `skill_scores`); (c) wire `flag_serious_signals()` after every recompute; (d) 6-week re-evaluation scheduler; (e) age-banded content for 5–12 (bands 5–7, 8–10, 11–12) across all activities; (f) still-pending content work: rubrics for `what_would_you_do`/`about_me`/`level_choice`, mood-to-valence scale, Phase 0 interview guide; (g) fix `docs/activity-signal-map.md` (built count is 14 incl. partials not 13, "blocked" wording per §12).
- Notes/gotchas: these doc changes (and all the 2026-09-29 ones) are uncommitted on `demo/frontend-test-harness`, which never merges — move them to a docs branch off `main`. §12's "Interest-based personalization" and "five modules only" text predates the scope decision; the decision log is authoritative where they differ.

### 2026-09-29 (scope review)
- Built: no code — incorporated a team review of the tutor-agent direction (Zurraiz's agent, written up as a PDF; Kazim's architecture recommendations). Fixed a real bug the review caught: `signal_events` had no way to tell a game-produced event from an agent-produced one, so an agent's dialogue judgment could become a permanent, unflagged `skill_score` — contradicting §12's own stated rule about agent judgment not silently becoming a score. Adopted the fix (`source`/`model`/`prompt_version` fields, provisional scoring for agent-sourced events), the week-1-agent-free constraint, Kazim's Learner State + Adaptive Policy layering, and an expanded safety spec. Corrected §1's framing (never a "screening tool" — PRD.md already said "not a diagnostic tool"; the tutor changes delivery, not the product). Reverted two implicitly-assumed points back to genuinely open rather than silently deciding them: D4 (conversation partner) and "tutor" scope (5 modules vs. also school subjects) — both flagged back to the owner instead.
- Files: `PROJECT.md`, `CLAUDE.md`.
- Next: get the owner's call on D4 and tutor scope; then start the `confidence_builder`-only spike (feature-flagged, adults first) in parallel with closing the listed blockers (auth/roles, missing FKs to `children`, `flag_serious_signals()` wiring, Phase 0 interviews).
- Notes/gotchas: the review's citations to "Voice Play Library", "Learning Ecosystem Blueprint", "Implementation & Team Plan", and two intern briefs aren't in this repo — couldn't independently verify those specific documents, but everything checkable against `PRD.md` (D4 open, offline-tolerant requirement, "not a diagnostic tool", "process audio/video on the device where possible") matched. Worth getting those docs into `research/` or `docs/` if they're going to keep being cited as decision history — right now this file is the only source of truth other sessions can actually read.

### 2026-09-29 (later still)
- Built: no code — researched 5 established clinical autism screening instruments (M-CHAT-R/F, SCQ, CAST, AQ-Child/AQ-Adolescent, SRS-2) at the team's request, to check whether their construct lists, age-banding practice, or norming approach should change anything about our own 12-dimension skill model or `age_band` design.
- Files: `PROJECT.md`, `CLAUDE.md`.
- Next: (a) legal/IP — do not reference these instruments' item wording, ordering, or scoring formulas as a starting point for anything, logged in the decision log; keep activities/scoring independently derived. (b) two candidate future skill dimensions logged for later, not urgent: restricted/repetitive behavior & rigidity (distinct from `sensory_regulation`), attention-switching/cognitive flexibility (distinct from `impulse_control`/`distractibility`). (c) sanity-check activity content across the full 5–12 age range — AQ/SRS-2 reword items per age band rather than rescale a single item; worth a lighter version of the same check on our own activities.
- Notes/gotchas: no change needed to baseline-referencing (rule #3) or the single continuous `age_band` approach — the two instruments whose age range most overlaps ours (SCQ: 4+, CAST: 4–11) don't age-band within that range either, and the reason instruments like AQ/SRS-2 do split (differing population norms per age) doesn't apply to a baseline-referenced design in the first place.

### 2026-09-29 (later)
- Built: no code — ran 4 parallel deep-research passes (autism/ADHD special-interest evidence, general interest-personalization theory, LLM-generated child content safety precedent, measurement-validity of reskinned cognitive tasks) after the owner asked to record each child's interests/strengths and use an LLM to generate JSON that customizes the games and dialogue activities per child. Added §12 "Interest-based personalization" reclassifying the idea with that research and **correcting an assumption made earlier in this same design pass** ("mechanics fixed, theme purely cosmetic = automatically score-neutral") — dedicated research found stimulus salience/preference can independently move reaction time and accuracy in autism and ADHD specifically, even with every timing/trial parameter held constant. Revised the architecture from "LLM generates a theme per child" to "LLM matches/fills a small curated, pre-validated template library" and added concrete validity safeguards (fixed target/non-target role assignment, per-template piloting, theme pinned during score-trending, theme-change-as-baseline-reset).
- Files: `PROJECT.md`, `CLAUDE.md`.
- Next: author the first template library (~15–20 themes) and the `child_interests` table + tutor-agent tool to populate it; pilot at least two templates against each other on the same task before trusting cross-theme score comparability, per the validity constraints above.
- Notes/gotchas: this is the second time in one design pass that a "should be safe by construction" assumption didn't survive actually researching it (first was "needs a human" vs. "needs a rubric" two turns ago) — worth remembering as a pattern for this project specifically: check evidence before treating an engineering-clean split (mechanics vs. content, human vs. agent) as a safety guarantee.

### 2026-09-29
- Built: no code — ran deep research (parallel agents) on evidence-based interventions per skill dimension after the owner clarified the product is actually a tutoring application (AI agent-based tutor, profile from week-1 play, games/API as tools). Corrected an initial framing mistake once the owner pushed back ("we are replacing the human with an agent, that's the whole point"): "blocked on content design"/"blocked on Phase 3" in `docs/activity-signal-map.md` meant the deterministic scoring extractor needed a pre-authored rubric, not that a human had to be in the interaction. Added §12 "Tutor-agent delivery model" reclassifying every item as agent-buildable-now / needs-pilot-validation / stays-human, and logged the decision that rule #8 (human-in-the-loop for referrals/plan overrides) stays as-is under this direction.
- Files: `PROJECT.md`, `CLAUDE.md`.
- Next: pick one module (confidence_builder is the strongest evidence fit — Bandura self-efficacy + Mueller & Dweck effort-praise) and design the actual agent architecture (tools, system prompt, profile-as-context) as a follow-up, once the owner wants to resume prototyping. `docs/activity-signal-map.md`'s "blocked on content design"/"blocked on Phase 3" wording should get updated too so it stops re-triggering the same misreading for the next person who reads it.
- Notes/gotchas: rule #8 is unchanged and was explicitly confirmed, not assumed — watch that it doesn't quietly erode as the tutor-agent design gets built out (e.g. an agent that "drafts a referral for review" is a different, larger scope change than what was confirmed here).

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

### 2026-09-28 (Track A, #1-6)
- Built: `guardians`, `children`, `schools`, `consents` tables + migration `c9dae9fdbc8f` (revises `0d07cdd64f6b`); onboarding pure functions (`age_in_years`/`age_band`, DOB/schooling/home-language/consent validation, phone normalisation, option constants); `POST /onboarding` (guardian + child + consent in one transaction) and `GET /onboarding/options`; `PATCH /children/{id}` and `POST /children/{id}/consent`. `children.schooling` is DB-CHECKed to `school`/`home_school` plus "school implies school_id" (rule #6-adjacent data integrity); every other option list (relationship, area, grade, language, gender, avatar) is a placeholder pending D7 and is validated in Pydantic against `onboarding/options.py`, not the DB, so extending them needs no migration. `POST /onboarding` looks guardians up by normalised phone before creating one, so a second sibling reuses the existing guardian instead of hitting the phone-unique constraint (existing name/relationship are never overwritten) — there's a TODO in `api/onboarding.py` that this needs OTP/phone verification before production. When `schooling == "school"`, the API accepts either an existing `school_id` or a new `school_name` (created in the same transaction); the DB CHECK still requires `school_id` to end up set. `POST /children/{id}/consent` inserts a new consent row and revokes the previous one — never overwrites history. Verified upgrade → downgrade → upgrade and `alembic check` show no drift; 85 tests pass (34 pre-existing + 51 new), including a test that `POST /onboarding` writes zero `skill_scores`/`plans` rows (rule #10).
- Files: `backend/app/models/identity.py`, `backend/app/models/__init__.py`, `backend/app/onboarding/{options,age,validation}.py`, `backend/app/schemas/{onboarding,children}.py`, `backend/app/api/{onboarding,children}.py`, `backend/app/main.py`, `backend/alembic/versions/c9dae9fdbc8f_create_identity_tables.py`, `backend/tests/{test_age,test_onboarding_validation,test_identity_model,test_onboarding_api,test_children_api}.py`.
- Next: no FK yet from `signal_events`/`skill_scores`/`sessions`/`activity_runs` to `children` — those tracks' `child_id` columns are still bare indexed UUIDs (see Track C's 2026-09-24 note); add the FKs in a follow-up migration now that `children` exists on `main`. Also still open: OTP/phone verification on `POST /onboarding` (see TODO in `api/onboarding.py`), and D7 (final onboarding field list) is still unresolved so the option lists in `onboarding/options.py` should be expected to change.
- Notes/gotchas: SQLAlchemy's `expire_on_commit=True` default bit a test — reading an ORM attribute after `db.commit()` *and* `db.close()` (as opposed to just commit) raises `DetachedInstanceError`; capture the plain value before closing the session instead of reading it off the object afterward. Also: a pure validator raising `ValueError` only becomes an HTTP 422 automatically when it runs inside a Pydantic validator; the same function called directly from a router body (as `PATCH /children/{id}` does, since a partial update needs to validate against the merged row, not just the request) needs an explicit `try/except ValueError -> HTTPException(422, ...)`.

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
