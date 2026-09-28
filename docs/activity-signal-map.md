# Activity → signal → skill map

For each activity: the event types it emits, the shape of `payload` for each, and which skill dimension(s) each signal feeds. This is the contract between the Flutter app, the events API, and scoring — see PROJECT.md §6 and §9.

**Status: mostly built.** 13 of 20 activities have a real extractor under `app/scoring/`, registered in `app/scoring/service.py`'s `EXTRACTORS`. The scoring approach for each is engineering's best grounded translation of the signals PRD.md §6.2 already describes — not the Phase 0 sign-off PROJECT.md's roadmap calls for (interviews with parents/teachers/therapists validating the skill dimensions and activity list). Treat every score/confidence scaling constant below as a placeholder to be checked against real pilot data, same caveat PROJECT.md already puts on the plan engine's thresholds.

3 activities are marked **blocked on Phase 3** — their signals require the speech pipeline (Whisper/wav2vec2) that doesn't exist yet, so raw audio can be captured and stored now, but no score can be computed from it until that pipeline lands. 3 more are marked **blocked on content design** — the game presents choices (or a mood value) that isn't objectively right/wrong or isn't on a defined scale, so scoring needs someone to define a rubric first, which is a product decision, not an engineering one.

## `stars_not_clouds` (v1.0.0) — built, `app/scoring/stars_not_clouds.py`

| event_type | payload shape | feeds |
|---|---|---|
| `tap` | `{"target": "star"\|"cloud", "correct": bool, "reaction_ms": int}` | `impulse_control`, `sustained_attention` |

Scoring: false-alarm rate on `target=="cloud"` taps → `impulse_control`; reaction-time variability on `target=="star"` taps → `sustained_attention`. Correctness is derived from `target` server-side, not trusted from the client's `correct` field.

## `watch_the_pond` — built, `app/scoring/watch_the_pond.py`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"time_bucket": int, "correct": bool}` | `sustained_attention` |

Scoring: sorted by `time_bucket`; score is accuracy over the second half of the run (sustained attention is about holding up through the *end*, not the average). `overall_accuracy` and `longest_correct_streak` are stored as evidence, not folded into the score formula itself.

## `wait_for_the_bell` — built, `app/scoring/wait_for_the_bell.py`

| event_type | payload shape | feeds |
|---|---|---|
| `tap` | `{"phase": "waiting"\|"bell", "early": bool, "wait_ms": int}` | `impulse_control` |

Scoring: false-alarm rate = early taps / total trials (same pattern as `stars_not_clouds`); average `wait_ms` on non-early taps stored as evidence.

## `distraction_garden` (optional) — built, `app/scoring/distraction_garden.py`

| event_type | payload shape | feeds |
|---|---|---|
| `tap` | `{"target": "on_task"\|"distractor"}` | `distractibility` |
| `response` | `{"return_ms": int}` (logged after a distraction) | `distractibility` |

Scoring: off-task tap rate = distractor taps / total taps; average `return_ms` after a distraction stored as evidence.

## `follow_instructions` — built, `app/scoring/follow_instructions.py`

| event_type | payload shape | feeds |
|---|---|---|
| `hint` | `{}` (repetition requested) | `working_memory` |
| `response` | `{"n_steps": int, "steps_followed": int, "correct": bool, "reaction_ms": int}` | `working_memory`, `auditory_comprehension` |

Scoring: `steps_followed / n_steps` → `auditory_comprehension`. **Correction from the original draft:** `n_steps` must be on the `response` event itself, not only on a separate `stimulus_shown` — the extractor scores each trial standalone rather than correlating two events by timing, which is a fragile pattern to build on. `hint` (repeat-request) rate → `working_memory` (more repeats needed = lower score).

## `copy_the_pattern` — built, `app/scoring/copy_the_pattern.py`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"sequence_length": int, "correct_order": bool}` | `working_memory` |

Scoring: longest `sequence_length` achieved with `correct_order=true`, scaled so a length of 10 is a perfect score (placeholder cap). Order-error rate stored as evidence.

## `story_and_questions` — built, `app/scoring/story_and_questions.py`

| event_type | payload shape | feeds |
|---|---|---|
| `hint` | `{}` (replay requested) | `auditory_comprehension` |
| `response` | `{"correct": bool}` | `auditory_comprehension` |

Scoring: accuracy rate on questions; replay count stored as evidence.

## `read_and_answer` — built, `app/scoring/read_and_answer.py`

| event_type | payload shape | feeds |
|---|---|---|
| `hint` | `{}` (re-read triggered) | `reading_comprehension` |
| `response` | `{"correct": bool, "time_on_task_ms": int}` | `reading_comprehension` |

Scoring: accuracy rate; average `time_on_task_ms` and re-read count stored as evidence.

## `speak_this_line` — **blocked on Phase 3**

| event_type | payload shape | feeds |
|---|---|---|
| `audio_captured` | `{"storage_key": str, "duration_ms": int}` | `articulation` |
| `retry` | `{}` | `articulation` |

Scoring: phoneme-error rate and speech rate both require running the speech pipeline against the captured audio — not computable from `signal_events` alone yet.

## `name_the_picture` — partially built, `app/scoring/name_the_picture.py`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"reaction_ms": int}` (word-finding time, before speech starts) | `expressive_language` |
| `audio_captured` | `{"storage_key": str}` | `articulation` (blocked on Phase 3) |

Scoring: word-finding time → `expressive_language`, built now. Articulation itself still needs Phase 3 speech analysis on the captured audio.

## `which_word` (ship/chip) — built, `app/scoring/which_word.py`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"target": str, "selected": str, "correct": bool, "reaction_ms": int}` | `articulation` |

Scoring: correctness is derived from `target == selected` server-side (not trusted from the client's own `correct` field, same principle as `stars_not_clouds`). Accuracy rate → score.

## `retell_the_story` — **blocked on Phase 3**

| event_type | payload shape | feeds |
|---|---|---|
| `audio_captured` | `{"storage_key": str, "duration_ms": int}` | `expressive_language` |

Scoring: sentence length and event-order correctness both require speech-to-text + NLP analysis on the captured audio.

## `chat_with_a_character` — **blocked on Phase 3**

| event_type | payload shape | feeds |
|---|---|---|
| `audio_captured` | `{"storage_key": str, "turn_index": int, "latency_ms": int, "interrupted": bool}` | `social_communication` |

Scoring: turn-taking latency and interruption rate are mechanically computable from the payload fields directly, but "staying on topic" (the more important half of this signal per PRD §6.2) needs Phase 3 NLP — no extractor built yet rather than shipping a partial one that undersells the dimension.

## `how_does_she_feel` — built, `app/scoring/how_does_she_feel.py`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"correct": bool, "reaction_ms": int}` | `emotion_recognition` |

Scoring: accuracy rate, same pattern as `stars_not_clouds`'s impulse control.

## `what_would_you_do` — **blocked on content design**

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"choice": str, "reaction_ms": int}` | `social_communication` |

Scoring: choices aren't objectively right/wrong, so there's no accuracy rate to compute. Needs a rubric — someone maps each specific choice option to a social-appropriateness rating — before this can produce a score. Not an engineering gap.

## `about_me` — **blocked on content design**

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"choice": str}` | `self_confidence` |

Scoring: same issue as `what_would_you_do` — needs a rubric mapping self-image choices to a confidence signal before scoring is possible.

## `oops_try_again` — built, `app/scoring/oops_try_again.py`

| event_type | payload shape | feeds |
|---|---|---|
| `retry` | `{"time_to_retry_ms": int}` | `self_confidence` |
| `quit` | `{}` | `self_confidence` |

Scoring: retry rate = retries / (retries + quits); average `time_to_retry_ms` stored as evidence.

## `level_choice` — **blocked on content design + cross-referencing**

| event_type | payload shape | feeds |
|---|---|---|
| `setting_changed` | `{"chosen_level": str}` | `self_confidence` |

Scoring: risk-taking = chosen difficulty relative to the child's demonstrated skill level — needs cross-referencing against existing `skill_scores`, which doesn't fit the extractor registry's uniform `(events, child_id, is_baseline)` signature every other extractor uses. Also needs a rubric for what "chosen difficulty vs. demonstrated skill" actually means numerically. Not built.

## `mood_check_in` — partially built, `app/scoring/mood_check_in.py`

| event_type | payload shape | feeds |
|---|---|---|
| `mood` | `{"mood": str, "phase": "before"\|"after"}` | — (not scored; see below) |
| `skip` | `{}` | `sensory_regulation` |

Scoring: only skip rate is built. "Mood shift" (comparing `before` vs. `after` mood values) needs a defined mood-to-valence scale that doesn't exist anywhere in the project yet — same class of content-design gap as `what_would_you_do`/`about_me`, not something to invent in the extractor.

## `sensory_setup` — built, `app/scoring/sensory_setup.py`

| event_type | payload shape | feeds |
|---|---|---|
| `setting_changed` | `{"setting": str, "value": str}` (`setting="calm_mode"`, `value="on"\|"off"` for calm-mode toggles) | `sensory_regulation` |

Scoring: calm-mode activation frequency as an inverse regulation signal (frequent use suggests higher sensory sensitivity), placeholder-scaled so 10 activations floors the score at 0.
