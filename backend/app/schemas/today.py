from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class TodayOut(BaseModel):
    child_id: UUID
    phase: Literal["week1", "plan"]
    day_index: int | None
    activities: list[str]
    plan_id: UUID | None = None
