from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import SkillScore
from app.schemas.profile import ProfileOut, SkillScoreOut

router = APIRouter(tags=["profile"])


@router.get("/children/{child_id}/profile", response_model=ProfileOut)
def get_profile(child_id: UUID, db: Session = Depends(get_db)) -> ProfileOut:
    scores = db.scalars(
        select(SkillScore)
        .where(SkillScore.child_id == child_id)
        .order_by(SkillScore.computed_at.desc())
    ).all()
    return ProfileOut(
        child_id=child_id,
        scores=[SkillScoreOut.model_validate(score) for score in scores],
    )
