from pydantic import BaseModel

from app.schemas.plans import PlanOut
from app.schemas.profile import SkillScoreOut


class RecomputeResult(BaseModel):
    scores: list[SkillScoreOut]
    plan: PlanOut
