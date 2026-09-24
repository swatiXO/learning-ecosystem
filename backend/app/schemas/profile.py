from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SkillScoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dimension: str
    score: float
    confidence: float
    is_baseline: bool
    computed_at: datetime


class ProfileOut(BaseModel):
    child_id: UUID
    scores: list[SkillScoreOut]
