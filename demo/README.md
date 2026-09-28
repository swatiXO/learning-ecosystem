# Backend test harness (not the real app)

This is **not** the Flutter app. It's a barebones, single-page HTML/JS harness that hits the real backend API end to end, so the team can click through the whole loop — onboard a child, play through week 1, watch scoring and a plan get generated — without waiting for real Flutter/Flame games to exist.

Lives on an isolated branch (`demo/frontend-test-harness`) that is never meant to merge into `main`. When real Flutter work starts, this gets thrown away, not adapted.

## Running it

```bash
# from repo root, with the backend already set up (see main README.md)
cd backend
uvicorn app.main:app --reload
```

Then open **http://localhost:8000/demo/** — served by the backend itself (same origin, no CORS setup needed).

## What it does

1. Onboard a fake guardian + child.
2. Starts a session automatically.
3. Shows "today's" activities (the real `GET /today`, backed by the real week-1 schedule and gate logic).
4. For each activity: either **play a real tiny interactive game** (available for `stars_not_clouds`, `wait_for_the_bell`, `distraction_garden` — real timing, real clicks, real events sent to `POST /events/batch`), or **quick-simulate** a "good" or "poor" performance with one click (available for all 20 activities, generating events matching the exact shape in `docs/activity-signal-map.md`) — or just **skip** it (rule #5: skips are a comfort signal, not a failure).
5. Completing an activity's real event batch, then marks the activity-run complete and refreshes the "today" view — which will advance through the 7 days exactly like the real gate logic does, and switch to plan phase once week 1 finishes.
6. Profile and Plan panels show the real `GET /profile` and `GET /plan` responses, so you can watch scores and the plan actually change as you play.
7. A raw request/response log at the bottom shows exactly what's being sent and received, for debugging.
