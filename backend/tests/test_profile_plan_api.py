import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.db import SessionLocal
from app.main import app
from app.models import Plan, PlanModule, SkillScore

client = TestClient(app)


def test_profile_empty_for_new_child() -> None:
    child_id = uuid.uuid4()
    response = client.get(f"/children/{child_id}/profile")
    assert response.status_code == 200
    assert response.json() == {"child_id": str(child_id), "scores": []}


def test_profile_returns_scores_newest_first() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        older = SkillScore(
            child_id=child_id,
            dimension="impulse_control",
            score=60,
            confidence=0.6,
            is_baseline=True,
            evidence={},
            computed_at=datetime.now(UTC) - timedelta(days=1),
        )
        newer = SkillScore(
            child_id=child_id,
            dimension="impulse_control",
            score=70,
            confidence=0.7,
            is_baseline=False,
            evidence={},
            computed_at=datetime.now(UTC),
        )
        db.add_all([older, newer])
        db.commit()

        response = client.get(f"/children/{child_id}/profile")
        assert response.status_code == 200
        scores = response.json()["scores"]
        assert [s["score"] for s in scores] == [70, 60]
    finally:
        db.execute(delete(SkillScore).where(SkillScore.child_id == child_id))
        db.commit()
        db.close()


def test_plan_not_found_returns_404() -> None:
    child_id = uuid.uuid4()
    response = client.get(f"/children/{child_id}/plan")
    assert response.status_code == 404


def test_plan_override_creates_and_supersedes() -> None:
    child_id = uuid.uuid4()
    try:
        first = client.put(
            f"/children/{child_id}/plan",
            json={
                "modules": [{"module": "focus_attention", "weight": 1.0}],
                "rationale": {"note": "initial"},
            },
        )
        assert first.status_code == 200
        assert first.json()["version"] == 1
        assert first.json()["created_by"] == "therapist"

        second = client.put(
            f"/children/{child_id}/plan",
            json={
                "modules": [{"module": "speech_language", "weight": 1.0}],
                "rationale": {"note": "revised"},
            },
        )
        assert second.status_code == 200
        assert second.json()["version"] == 2

        current = client.get(f"/children/{child_id}/plan")
        assert current.status_code == 200
        assert current.json()["version"] == 2
        assert current.json()["modules"] == [{"module": "speech_language", "weight": 1.0}]
    finally:
        db = SessionLocal()
        try:
            plan_ids = [p.id for p in db.query(Plan).filter_by(child_id=child_id).all()]
            db.query(PlanModule).filter(PlanModule.plan_id.in_(plan_ids)).delete(
                synchronize_session=False
            )
            db.query(Plan).filter_by(child_id=child_id).delete()
            db.commit()
        finally:
            db.close()


def test_plan_override_requires_at_least_one_module() -> None:
    child_id = uuid.uuid4()
    response = client.put(f"/children/{child_id}/plan", json={"modules": []})
    assert response.status_code == 422
