# PRD: Learning Ecosystem (working name)

**Owner:** Zurraiz Ahmed, Mediatiz Foundation
**Status:** Draft v2 (intake survey replaced by quick onboarding)
**Last updated:** 2026-09-24

---

## 1. Summary

A learning app that helps children with ADHD, autism and low self-esteem regulate their learning and work through common difficulties. It uses animations, games and speech-therapy exercises. Setup is a 2–3 minute onboarding of simple questions (name, date of birth, area, school or home school). There is no intake survey. A required first week of game-based activities builds a **needs profile** (skill scores with confidence levels). A rules-based plan engine then assigns a weighted mix of modules. The app adapts as the child uses it and re-evaluates every 6–8 weeks against the child's own baseline.

**It is not a diagnostic tool.** It never outputs diagnosis labels. It gives skill scores and suggests referral to a specialist when signals are serious.

## 2. Problem

- Children with attention, communication and confidence difficulties rarely get individual support at the pace they need, especially in Pakistani schools.
- Therapy and specialist time is scarce and expensive. Parents and teachers lack tools to see where a child is struggling and what helps.
- Existing apps are usually one-size-fits-all, test-like, or built only for English speakers.

## 3. Goals

1. Build a reliable, explainable needs profile from 7 days of play, without it feeling like a test.
2. Assign each child a personalised, weighted plan across 5 modules.
3. Show measurable progress against the child's own baseline after 6–8 weeks.
4. Keep parents, teachers and therapists informed, and in control of important decisions.
5. Handle children's data safely: consent first, minimal collection, raw media kept apart from the profile.

### Non-goals

- Diagnosing ADHD, autism or any condition.
- Replacing therapists or teachers.
- Comparing children against population norms or against each other.
- Open-ended AI chat with children in v1 (see Open Decisions).

## 4. Users

| User | Needs |
|---|---|
| **Child** (primary; age range TBD) | Fun, calm, no failure, short sessions, sensory control |
| **Parent** | Setup in 2–3 minutes, consent control, simple progress view, clear next steps |
| **Teacher** | Classroom-relevant insights, optional input when invited |
| **Therapist / specialist** | Detailed signals, ability to adjust plans, referral path |
| **Admin (Mediatiz / school)** | Manage schools, accounts, pilots, data exports |

## 5. User flow

1. **Onboarding (required, 2–3 minutes):** consent plus a few simple questions: child's name, date of birth, area, school or home school, and a few more (see 6.1). No survey.
   **Optional extras (any time later):** teacher input, speech sample, video.
   Every child starts week 1 on the same default schedule. Date of birth sets the age band, which sets content and starting difficulty.
2. **Week 1 (7 days, required gate):** assessment through games, presented as an adventure. No program unlocks until it is complete.
3. **Signal extraction:** every activity logs events tied to a skill area.
4. **Needs profile:** skill scores + confidence. Never labels.
5. **Plan engine:** rules first (ML later). Assigns 1–3 weighted modules.
6. **Modules:** Focus & attention · Speech & language · Social-emotional · Confidence builder · Routine & sensory.
7. **Adaptive layer:** adjusts difficulty, pacing, rewards and sensory load live.
8. **Session tracking:** passive, every session.
9. **Re-evaluation:** every 6–8 weeks, updating the profile against the child's own baseline.

**Central:** Profile store (single source of truth).
**Side systems:** parent/teacher/therapist dashboards; safety net (referral to a specialist).

## 6. Functional requirements

### 6.1 Onboarding (replaces the intake survey)
- FR-1 Onboarding takes 2–3 minutes on a phone. It is one question per screen, big buttons, and can be answered in Urdu or English. No free-text essays and no behaviour questions.
- FR-2 Onboarding questions:

| # | Question | Input | Required |
|---|---|---|---|
| 1 | Consent (terms, plus separate audio and video toggles) | checkboxes | yes |
| 2 | Your name and relationship to the child (mother, father, guardian, teacher) | text + pick | yes |
| 3 | Phone number (for login and OTP) | phone | yes |
| 4 | Child's name or nickname | text | yes |
| 5 | Child's date of birth | date picker | yes |
| 6 | Area / city | pick from list + "other" | yes |
| 7 | School or home school? | two buttons | yes |
| 8 | If school: school name and class/grade | search/pick + pick | yes if school |
| 9 | Languages spoken at home | multi-pick (Urdu, English, Punjabi, Pashto, Sindhi, other) | yes |
| 10 | Child's gender | pick (optional) | no |
| 11 | Child's avatar / character | pick | no (the child can do it on Day 1) |

- FR-3 Onboarding answers **do not** score the child and do not set skill priors. They only set context: age band (from date of birth), app language and voice lines, reading level, and whether a school/teacher link is possible.
- FR-4 Parent can edit onboarding answers later from settings.
- FR-5 Optional, later and not part of onboarding: invite a teacher to add input; speech sample and video upload, only when the matching consent is on.

### 6.2 Week-1 assessment
- FR-6 7-day schedule, 10–15 min/day, 2–4 activities per day, always ending on a success. The order is the same for every child. The age band adjusts content and starting difficulty only.
- FR-7 Missed days extend the week and never count against the child.
- FR-8 Skipping an activity is logged as a comfort signal, not a failure.
- FR-9 Day 7 repeats two activities (consistency check) and then unlocks the program.

**Activity library (each must log the listed signals):**

| Skill area | Activity | Signals |
|---|---|---|
| Attention & impulse | Stars, not clouds (go/no-go) | wrong taps, missed stars, reaction-time spread |
| | Watch the pond (3-min sustained) | accuracy drop over time, longest steady stretch |
| | Wait for the bell | early taps, wait tolerance |
| | Distraction garden (optional) | off-task taps, time to return |
| Listening & memory | Follow instructions | followed, repetitions, response time, errors |
| | Copy the pattern | longest sequence, order errors |
| | Story and questions | correct answers, replays requested |
| | Read and answer | accuracy, time on task, re-reads |
| Speech & language | Speak this line | phoneme errors, speech rate, retries |
| | Name the picture | word-finding time, articulation |
| | Which word? (ship/chip) | sound-discrimination errors |
| | Retell the story | sentence length, event order |
| Conversation & feelings | Chat with a character | latency, interruptions, turn-taking, speech rate, staying on topic |
| | How does she feel? | emotion-recognition accuracy, response time |
| | What would you do? | choices, response time |
| Confidence & comfort | About me | self-image choices |
| | Oops, try again | retry vs quit, time to retry |
| | Level choice | risk-taking, persistence |
| | Mood check-in | mood shift, skip rate |
| | Sensory setup | sensory preferences, calm-mode use |

**7-day schedule:**

| Day | Theme | Activities |
|---|---|---|
| 1 | Welcome | Sensory setup, Mood check-in, easy Stars not clouds |
| 2 | Sounds and words | Speak this line, Name the picture, Which word? |
| 3 | Focus | Watch the pond, Wait for the bell, Read and answer |
| 4 | Listening | Follow instructions, Copy the pattern, Story and questions |
| 5 | Talking and feelings | Chat with a character, How does she feel?, What would you do? |
| 6 | Confidence | About me, Oops try again, Level choice, Retell the story |
| 7 | Replay and unlock | Stars not clouds + Speak this line (repeat), Distraction garden, unlock |

### 6.3 Signals and scoring
- FR-10 All activities send events in one shared event schema (see PROJECT.md).
- FR-11 The app queues events offline and syncs them in batches.
- FR-12 Scoring turns events into 8–12 skill dimensions (to be finalised in Phase 0), each with a score (0–100) and a confidence (0–1).
- FR-13 A score moves only when several activities agree. Confidence stays low until they do. With no survey, every score starts neutral with zero confidence and is built only from activity signals.
- FR-14 Scoring accounts for confounders (e.g. a slow reply could mean shyness, processing time or poor audio).

### 6.4 Plan engine
- FR-15 Rules-based v1: needs profile + onboarding context (age band, languages) → 1–3 modules with weights that add up to 1.
- FR-16 Every plan stores the reason it was chosen (which rules fired). Explainability is required.
- FR-17 A therapist can override or adjust a plan. Overrides are logged.

### 6.5 Modules and adaptive layer
- FR-18 Five modules, each a set of activities tagged by skill and difficulty.
- FR-19 The adaptive layer adjusts difficulty, pacing, rewards and sensory load based on in-session performance.
- FR-20 No fail states. Rewards are for effort. Calm mode is always available.

### 6.6 Re-evaluation
- FR-21 Every 6–8 weeks, a short re-run of key activities updates the profile.
- FR-22 Progress is shown as change from the child's own baseline.

### 6.7 Dashboards
- FR-23 Parent: simple progress, streaks, what the child is working on, tips.
- FR-24 Teacher: class overview and individual child cards (with parent consent only; only for children marked "school" in onboarding).
- FR-25 Therapist: detailed signals, score history, plan editing, notes.

### 6.8 Safety net
- FR-26 Defined serious-signal rules flag a child for human review.
- FR-27 A human (therapist or admin) decides on referral. The system never contacts anyone automatically without human approval.

## 7. Non-functional requirements

- **Privacy:** consent first; data minimisation (onboarding asks only context questions; store date of birth but show an age band everywhere except settings); process audio/video on the device where possible; raw media in separate object storage, linked by ID only; encryption at rest and in transit; parent can export or delete data.
- **Accessibility:** large touch targets, minimal text for young children, voice-over instructions, adjustable volume, motion and colours.
- **Performance:** works on low-end Android tablets; offline-tolerant; event sync under 2 s on 3G.
- **Localisation:** Urdu and/or English (TBD); right-to-left support if Urdu.
- **Explainability:** every score and plan can be traced back to events and rules.
- **Reliability:** no lost events (idempotent batch ingest with client-generated event IDs).

## 8. Tech stack (proposed)

| Layer | Choice |
|---|---|
| Child/parent app | Flutter (Dart), Flame for games, Rive/Lottie for animation |
| Backend API | Python 3.12, FastAPI, Pydantic v2 |
| Database | PostgreSQL 16, SQLAlchemy 2 + Alembic |
| Media storage | S3-compatible (MinIO locally) |
| Speech | Whisper / wav2vec2 for transcription and pronunciation features |
| Dashboards | Flutter web or a separate React app (TBD) |
| Infra (dev) | Docker Compose |

## 9. Success metrics

- Onboarding: median time ≤ 3 minutes; ≥ 90% of parents who start it finish it.
- Week-1 completion rate ≥ 70% of children who start.
- Average session length within the 10–15 min target; skip rate under 20%.
- Test-retest consistency of Day 1 vs Day 7 repeated activities (target correlation ≥ 0.6).
- Therapist agreement with the auto-generated plan ≥ 70% in the pilot.
- Measurable gain from baseline on the targeted skills at the first re-evaluation, for most pilot children.
- Parent satisfaction ≥ 4/5.

## 10. Phases / roadmap

| Phase | Scope | Exit criteria |
|---|---|---|
| 0 | Interview 5–10 parents, teachers, speech therapists; define 8–12 skill dimensions; validate the activity list | Signed-off skill dimension list and activity→signal→skill map |
| 1 | Profile store + event API + rules-based plan engine | API live, unit-tested rules with fake children |
| 2 | 2–3 minute onboarding + week-1 activities with signal logging (starting with Stars not clouds) | A parent onboards in ≤ 3 min; the child completes week 1 and gets a profile |
| 3 | Speech module end to end (vertical slice) | Speak this line → features → score → plan → speech activities |
| 4 | Remaining modules, dashboards, re-evaluation | All 5 modules and 3 dashboards usable |
| 5 | Small school/clinic pilot, then ML in routing | Pilot report; metrics above |

## 11. Open decisions

| # | Decision | Options | Blocks |
|---|---|---|---|
| D1 | Language scope | Urdu / English / both | Speech models, content, UI |
| D2 | Target age range | e.g. 5–8, 6–12 | UI, reading level, activity design |
| D3 | Platform first | Android tablet / web / iOS | Flutter build targets, testing |
| D4 | Conversation partner | Scripted animated character vs open AI voice | Chat activity, safety review |
| D5 | Dashboard technology | Flutter web vs React | Front-end staffing |
| D6 | Hosting and data residency | Local (Pakistan) vs cloud region | Privacy, cost |
| D7 | Final onboarding field list | Draft in 6.1 (e.g. keep or drop gender; area list granularity) | Onboarding screens, `children` table |

**Decided (2026-09-24):** the intake survey is replaced by a 2–3 minute onboarding of simple context questions. With no parent survey, needs information comes only from week-1 play.

## 12. Risks

- **Misreading signals** (shyness vs difficulty): mitigated by combining signals, tracking confidence and keeping humans in the loop.
- **Being seen as a diagnosis:** clear wording in the UI, no labels, and a consent text that explains this.
- **Speech models weak on Urdu or children's voices:** start with simple features; collect consented data; allow manual review.
- **No parent view at start** (survey removed): week 1 must carry all the evidence, so confidence is lower after week 1 for some skills. Mitigated by the Day-7 consistency check, re-evaluation, and optional teacher input later.
- **Children disengaging:** short sessions, adventure framing, always ending on a success.
- **Data breach involving minors:** strict access control, encryption, minimal storage, audit logs.
