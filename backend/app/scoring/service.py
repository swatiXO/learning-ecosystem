import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SignalEvent, SkillScore
from app.scoring.stars_not_clouds import ACTIVITY as STARS_NOT_CLOUDS_ACTIVITY
from app.scoring.stars_not_clouds import score_stars_not_clouds

# Hardcoded for now (only one extractor exists). Formalize into a real registry
# once a second activity's extractor lands — see issue #29.
EXTRACTORS = [(STARS_NOT_CLOUDS_ACTIVITY, score_stars_not_clouds)]


def recompute_scores(
    db: Session, child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    new_scores: list[SkillScore] = []
    for activity, extractor in EXTRACTORS:
        events = db.scalars(
            select(SignalEvent).where(
                SignalEvent.child_id == child_id, SignalEvent.activity == activity
            )
        ).all()
        new_scores.extend(extractor(list(events), child_id, is_baseline=is_baseline))

    db.add_all(new_scores)
    db.flush()
    return new_scores
