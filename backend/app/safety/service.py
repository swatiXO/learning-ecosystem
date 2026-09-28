import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SafetyFlag, SkillScore
from app.plan_engine.rules import Profile
from app.safety.rules import evaluate


def flag_serious_signals(db: Session, child_id: uuid.UUID) -> list[SafetyFlag]:
    """Evaluates the safety rules against the child's current skill scores and opens a new
    SafetyFlag for each rule that fires and doesn't already have an open flag for this
    child. Rule #8/FR-27: this only ever creates a flag for a human to review later - it
    never notifies or refers anyone by itself.
    """
    scores = db.scalars(
        select(SkillScore)
        .distinct(SkillScore.dimension)
        .where(SkillScore.child_id == child_id)
        .order_by(SkillScore.dimension, SkillScore.computed_at.desc())
    ).all()
    profile = Profile.from_scores(list(scores))
    fired = evaluate(profile)

    already_open = set(
        db.scalars(
            select(SafetyFlag.rule).where(
                SafetyFlag.child_id == child_id, SafetyFlag.status == "open"
            )
        ).all()
    )

    new_flags = []
    for rule in fired:
        if rule.name in already_open:
            continue
        score = profile.scores[rule.dimension]
        flag = SafetyFlag(
            child_id=child_id,
            rule=rule.name,
            evidence={
                "dimension": rule.dimension,
                "score": score.score,
                "confidence": score.confidence,
            },
        )
        db.add(flag)
        new_flags.append(flag)

    if new_flags:
        db.commit()
        for flag in new_flags:
            db.refresh(flag)
    return new_flags
