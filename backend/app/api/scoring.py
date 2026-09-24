from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.plan_engine.service import regenerate_plan, serialize_plan
from app.schemas.profile import SkillScoreOut
from app.schemas.scoring import RecomputeResult
from app.scoring.service import recompute_scores

router = APIRouter(tags=["scoring"])


@router.post("/children/{child_id}/score", response_model=RecomputeResult)
def recompute_and_replan(
    child_id: UUID, is_baseline: bool = False, db: Session = Depends(get_db)
) -> RecomputeResult:
    new_scores = recompute_scores(db, child_id, is_baseline=is_baseline)
    plan = regenerate_plan(db, child_id)
    db.commit()
    db.refresh(plan)
    return RecomputeResult(
        scores=[SkillScoreOut.model_validate(score) for score in new_scores],
        plan=serialize_plan(db, plan),
    )
