# Activity → signal → skill map

For each activity: the event types it emits, the shape of `payload` for each, and which skill dimension(s) each signal feeds. This is the contract between the Flutter app, the events API, and scoring — see PROJECT.md §6 and §9.

**Status: draft.** This is engineering's best translation of the signals PRD.md §6.2 already describes into concrete event types and payload fields, plus a scoring approach for each — done so that whoever picks up an extractor next isn't guessing at data shapes. It is **not** the Phase 0 sign-off PROJECT.md's roadmap calls for (interviews with parents/teachers/therapists validating the skill dimensions and activity list). Treat every "scoring approach" note below as a placeholder to be checked against real pilot data, same caveat PROJECT.md already puts on the plan engine's thresholds.

Three activities are marked **blocked on Phase 3** — their signals require the speech pipeline (Whisper/wav2vec2) that doesn't exist yet, so raw audio can be captured and stored now, but no score can be computed from it until that pipeline lands. Two more are marked **blocked on content design** — the game presents choices that aren't objectively right/wrong, so scoring them needs someone to define a rubric (which choice indicates what), which is a product decision, not an engineering one.

## `stars_not_clouds` (v1.0.0) — built, see `app/scoring/stars_not_clouds.py`

| event_type | payload shape | feeds |
|---|---|---|
| `tap` | `{"target": "star"\|"cloud", "correct": bool, "reaction_ms": int}` | `impulse_control`, `sustained_attention` |

Scoring: false-alarm rate on `target=="cloud"` taps → `impulse_control`; reaction-time variability on `target=="star"` taps → `sustained_attention`. Correctness is derived from `target` server-side, not trusted from the client's `correct` field.

## `watch_the_pond`

| event_type | payload shape | feeds |
|---|---|---|
| `stimulus_shown` | `{"time_bucket": int}` | `sustained_attention` |
| `response` | `{"time_bucket": int, "correct": bool, "reaction_ms": int}` | `sustained_attention` |

Scoring: split the run into fixed time buckets; accuracy drop-off = accuracy in later buckets vs. earlier ones; longest steady stretch = longest consecutive run of correct responses.

## `wait_for_the_bell`

| event_type | payload shape | feeds |
|---|---|---|
| `tap` | `{"phase": "waiting"\|"bell", "early": bool, "wait_ms": int}` | `impulse_control` |

Scoring: false-alarm rate = early taps / total trials (same pattern as `stars_not_clouds`); wait tolerance = average `wait_ms` achieved before the bell.

## `distraction_garden` (optional)

| event_type | payload shape | feeds |
|---|---|---|
| `tap` | `{"target": "on_task"\|"distractor"}` | `distractibility` |
| `response` | `{"return_ms": int}` (logged after a distraction) | `distractibility` |

Scoring: off-task tap rate = distractor taps / total taps; average `return_ms` after a distraction (lower is better).

## `follow_instructions`

| event_type | payload shape | feeds |
|---|---|---|
| `stimulus_shown` | `{"n_steps": int}` | — |
| `hint` | `{}` (repetition requested) | `working_memory` |
| `response` | `{"steps_followed": int, "correct": bool, "reaction_ms": int}` | `working_memory`, `auditory_comprehension` |

Scoring: `steps_followed / n_steps` → `auditory_comprehension`; `hint` (repeat-request) rate → `working_memory` (more repeats needed = lower score).

## `copy_the_pattern`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"sequence_length": int, "correct_order": bool}` | `working_memory` |

Scoring: longest `sequence_length` achieved with `correct_order=true` is the primary signal; order-error rate as a secondary.

## `story_and_questions`

| event_type | payload shape | feeds |
|---|---|---|
| `hint` | `{}` (replay requested) | `auditory_comprehension` |
| `response` | `{"correct": bool}` | `auditory_comprehension` |

Scoring: accuracy rate on questions; replay count as a secondary (inverse) signal.

## `read_and_answer`

| event_type | payload shape | feeds |
|---|---|---|
| `hint` | `{}` (re-read triggered) | `reading_comprehension` |
| `response` | `{"correct": bool, "time_on_task_ms": int}` | `reading_comprehension` |

Scoring: accuracy rate; average `time_on_task_ms`; re-read count as a secondary signal.

## `speak_this_line` — **blocked on Phase 3**

| event_type | payload shape | feeds |
|---|---|---|
| `audio_captured` | `{"storage_key": str, "duration_ms": int}` | `articulation` |
| `retry` | `{}` | `articulation` |

Scoring: phoneme-error rate and speech rate both require running the speech pipeline against the captured audio — not computable from `signal_events` alone yet. Retry count alone is a weak proxy in the meantime (more retries suggests difficulty), usable at low confidence only.

## `name_the_picture` — partially blocked on Phase 3

| event_type | payload shape | feeds |
|---|---|---|
| `stimulus_shown` | `{"item": str}` | — |
| `response` | `{"reaction_ms": int}` (before speech starts) | `expressive_language` |
| `audio_captured` | `{"storage_key": str}` | `articulation` |

Scoring: word-finding time (`reaction_ms`) → `expressive_language`, computable now. Articulation itself needs Phase 3 speech analysis on the captured audio.

## `which_word` (ship/chip)

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"target": str, "selected": str, "correct": bool, "reaction_ms": int}` | `articulation` |

Scoring: sound-discrimination error rate = incorrect / total, same false-alarm-style pattern as `stars_not_clouds`.

## `retell_the_story` — **blocked on Phase 3**

| event_type | payload shape | feeds |
|---|---|---|
| `audio_captured` | `{"storage_key": str, "duration_ms": int}` | `expressive_language` |

Scoring: sentence length and event-order correctness both require speech-to-text + NLP analysis on the captured audio. Not computable from `signal_events` alone.

## `chat_with_a_character` — partially blocked on Phase 3

| event_type | payload shape | feeds |
|---|---|---|
| `audio_captured` | `{"storage_key": str, "turn_index": int, "latency_ms": int, "interrupted": bool}` | `social_communication` |

Scoring: turn-taking latency average and interruption rate are computable now from the payload fields directly. "Staying on topic" needs Phase 3 NLP on the captured audio.

## `how_does_she_feel`

| event_type | payload shape | feeds |
|---|---|---|
| `response` | `{"correct": bool, "reaction_ms": int}` | `emotion_recognition` |

Scoring: accuracy rate, same pattern as `stars_not_clouds`'s impulse control; `reaction_ms` as a secondary signal.

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

## `oops_try_again`

| event_type | payload shape | feeds |
|---|---|---|
| `retry` | `{"time_to_retry_ms": int}` | `self_confidence` |
| `quit` | `{}` | `self_confidence` |

Scoring: retry rate = retries / (retries + quits); average `time_to_retry_ms` (faster suggests more resilience).

## `level_choice`

| event_type | payload shape | feeds |
|---|---|---|
| `setting_changed` | `{"chosen_level": str}` | `self_confidence` |

Scoring: risk-taking = chosen difficulty relative to the child's demonstrated skill level — needs cross-referencing against existing `skill_scores`, more involved than the other extractors. Persistence = repeated attempts logged at the chosen level.

## `mood_check_in`

| event_type | payload shape | feeds |
|---|---|---|
| `mood` | `{"mood": str, "phase": "before"\|"after"}` | `sensory_regulation` |
| `skip` | `{}` | `sensory_regulation` |

Scoring: mood shift = compare `before` vs. `after` mood values; skip rate = skips / total prompts.

## `sensory_setup`

| event_type | payload shape | feeds |
|---|---|---|
| `setting_changed` | `{"setting": str, "value": str}` (includes calm-mode toggles) | `sensory_regulation` |

Scoring: calm-mode activation frequency as an inverse regulation signal (frequent use suggests higher sensory sensitivity).
