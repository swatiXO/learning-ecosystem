from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.sessions import WEEK1_DAYS
from app.schemas.events import REGISTERED_ACTIVITIES

# Rule #5: no fail states. The only states an activity run can be closed with are these
# three — "failed" is not a representable value, so a bad client can't even try it.
ActivityRunTerminalStatus = Literal["completed", "skipped", "quit"]


class ActivityRunCreateIn(BaseModel):
    session_id: UUID
    activity: str
    activity_version: str
    day_index: int | None = None

    @field_validator("activity")
    @classmethod
    def activity_must_be_registered(cls, value: str) -> str:
        if value not in REGISTERED_ACTIVITIES:
            raise ValueError(f"unregistered activity: {value!r}")
        return value

    @field_validator("day_index")
    @classmethod
    def day_index_in_range(cls, value: int | None) -> int | None:
        if value is not None and not (1 <= value <= WEEK1_DAYS):
            raise ValueError(f"day_index must be between 1 and {WEEK1_DAYS}")
        return value


class ActivityRunUpdateIn(BaseModel):
    status: ActivityRunTerminalStatus


class ActivityRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    activity: str
    activity_version: str
    day_index: int | None
    status: str
    started_at: datetime
    ended_at: datetime | None
