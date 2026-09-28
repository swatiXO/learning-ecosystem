from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SessionCreateIn(BaseModel):
    child_id: UUID
    device_info: dict[str, Any] = {}
    mood_before: str | None = None


class SessionUpdateIn(BaseModel):
    """PATCH /sessions/{id}: ends the session and/or records mood after.

    Ending is first-write-wins (a retried PATCH after a dropped response must not push
    ended_at forward again), but mood_after can be updated on every call since it is just
    metadata, not a state transition.
    """

    mood_after: str | None = None


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    child_id: UUID
    started_at: datetime
    ended_at: datetime | None
    device_info: dict[str, Any]
    mood_before: str | None
    mood_after: str | None
