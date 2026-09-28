from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel

EventType = Literal[
    "stimulus_shown",
    "tap",
    "response",
    "audio_captured",
    "skip",
    "quit",
    "retry",
    "hint",
    "mood",
    "setting_changed",
    "complete",
]

# Every activity key documented in docs/activity-signal-map.md. This is broader than
# scoring's extractor registry (app/scoring/service.py) on purpose — an activity can be
# logged as soon as it's documented, before a scoring extractor for it exists.
REGISTERED_ACTIVITIES = frozenset(
    {
        "stars_not_clouds",
        "watch_the_pond",
        "wait_for_the_bell",
        "distraction_garden",
        "follow_instructions",
        "copy_the_pattern",
        "story_and_questions",
        "read_and_answer",
        "speak_this_line",
        "name_the_picture",
        "which_word",
        "retell_the_story",
        "chat_with_a_character",
        "how_does_she_feel",
        "what_would_you_do",
        "about_me",
        "oops_try_again",
        "level_choice",
        "mood_check_in",
        "sensory_setup",
    }
)


class EventIn(BaseModel):
    """Event schema v0 — see PROJECT.md §6. This is the shared contract; changing
    a field here affects onboarding/events, scoring and week1 tracks alike."""

    event_id: UUID
    child_id: UUID
    session_id: UUID
    activity_run_id: UUID
    activity: str
    activity_version: str
    event_type: EventType
    ts_client: datetime
    payload: dict[str, Any] = {}


class EventBatchIn(BaseModel):
    events: list[EventIn]


class EventBatchResult(BaseModel):
    accepted: int
    duplicates: int
    rejected: int = 0
