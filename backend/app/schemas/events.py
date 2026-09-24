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
