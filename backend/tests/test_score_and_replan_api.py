import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.db import SessionLocal
from app.main import app
from app.models import Plan, PlanModule, SignalEvent, SkillScore
from tests.fixtures.stars_not_clouds_events import make_tap

client = TestClient(app)


def _cleanup(child_id: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        plan_ids = [p.id for p in db.query(Plan).filter_by(child_id=child_id).all()]
        db.query(PlanModule).filter(PlanModule.plan_id.in_(plan_ids)).delete(
            synchronize_session=False
        )
        db.query(Plan).filter_by(child_id=child_id).delete()
        db.query(SkillScore).filter_by(child_id=child_id).delete()
        db.execute(delete(SignalEvent).where(SignalEvent.child_id == child_id))
        db.commit()
    finally:
        db.close()


def test_score_with_no_events_returns_fallback_plan() -> None:
    child_id = uuid.uuid4()
    try:
        response = client.post(f"/children/{child_id}/score")
        assert response.status_code == 200
        body = response.json()
        assert body["scores"] == []
        modules = {m["module"]: m["weight"] for m in body["plan"]["modules"]}
        assert modules == {"confidence_builder": 0.5, "focus_attention": 0.5}
        assert body["plan"]["created_by"] == "engine"
    finally:
        _cleanup(child_id)


def test_score_computes_scores_and_regenerates_plan() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        # 12 impulsive taps on "cloud" -> low, confident impulse_control -> low_attention rule fires
        db.add_all([make_tap(child_id, "cloud", 350) for _ in range(12)])
        db.commit()
    finally:
        db.close()

    try:
        response = client.post(f"/children/{child_id}/score")
        assert response.status_code == 200
        body = response.json()

        impulse = next(s for s in body["scores"] if s["dimension"] == "impulse_control")
        assert impulse["score"] == 0.0

        modules = {m["module"]: m["weight"] for m in body["plan"]["modules"]}
        assert modules == {"focus_attention": 1.0}
        assert body["plan"]["rationale"]["rules_fired"] == ["low_attention"]
        assert body["plan"]["version"] == 1
    finally:
        _cleanup(child_id)


def test_calling_score_twice_supersedes_previous_plan() -> None:
    child_id = uuid.uuid4()
    try:
        first = client.post(f"/children/{child_id}/score")
        assert first.json()["plan"]["version"] == 1

        second = client.post(f"/children/{child_id}/score")
        assert second.json()["plan"]["version"] == 2

        current = client.get(f"/children/{child_id}/plan")
        assert current.json()["version"] == 2
    finally:
        _cleanup(child_id)


def test_is_baseline_flag_propagates_to_new_scores() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        db.add_all([make_tap(child_id, "star", 400) for _ in range(3)])
        db.commit()
    finally:
        db.close()

    try:
        response = client.post(f"/children/{child_id}/score", params={"is_baseline": True})
        assert response.status_code == 200
        assert all(s["is_baseline"] for s in response.json()["scores"])
    finally:
        _cleanup(child_id)
