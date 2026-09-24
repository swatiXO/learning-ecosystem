import uuid

from app.db import SessionLocal
from app.models import Plan, PlanModule, SkillScore


def test_skill_score_round_trip() -> None:
    db = SessionLocal()
    try:
        child_id = uuid.uuid4()
        score = SkillScore(
            child_id=child_id,
            dimension="sustained_attention",
            score=35.0,
            confidence=0.6,
            is_baseline=True,
            evidence={"events": ["e1", "e2"]},
        )
        db.add(score)
        db.commit()

        fetched = db.get(SkillScore, score.id)
        assert fetched is not None
        assert fetched.dimension == "sustained_attention"
        assert fetched.is_baseline is True

        db.delete(fetched)
        db.commit()
    finally:
        db.close()


def test_plan_with_modules_round_trip() -> None:
    db = SessionLocal()
    try:
        child_id = uuid.uuid4()
        plan = Plan(
            child_id=child_id,
            version=1,
            status="active",
            rationale={"rules_fired": ["low_attention"]},
            created_by="engine",
        )
        db.add(plan)
        db.flush()

        module = PlanModule(plan_id=plan.id, module="focus_attention", weight=1.0)
        db.add(module)
        db.commit()

        fetched_modules = db.query(PlanModule).filter_by(plan_id=plan.id).all()
        assert len(fetched_modules) == 1
        assert fetched_modules[0].weight == 1.0

        db.query(PlanModule).filter_by(plan_id=plan.id).delete()
        db.delete(db.get(Plan, plan.id))
        db.commit()
    finally:
        db.close()
