import uuid

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models import Plan, Week1Progress
from app.week1.schedule import activities_for_day

client = TestClient(app)


def _mark_days_complete(child_id: uuid.UUID, days: range) -> None:
    db = SessionLocal()
    try:
        db.add_all([Week1Progress(child_id=child_id, day_index=day) for day in days])
        db.commit()
    finally:
        db.close()


def _cleanup(child_id: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        db.query(Week1Progress).filter_by(child_id=child_id).delete()
        db.query(Plan).filter_by(child_id=child_id).delete()
        db.commit()
    finally:
        db.close()


def test_today_returns_week1_day_one_for_a_new_child() -> None:
    child_id = uuid.uuid4()
    response = client.get(f"/children/{child_id}/today")
    assert response.status_code == 200
    body = response.json()
    assert body["phase"] == "week1"
    assert body["day_index"] == 1
    assert body["activities"] == list(activities_for_day(1))
    assert body["plan_id"] is None


def test_today_advances_to_day_two_after_day_one_completes() -> None:
    child_id = uuid.uuid4()
    _mark_days_complete(child_id, range(1, 2))
    try:
        response = client.get(f"/children/{child_id}/today")
        assert response.status_code == 200
        body = response.json()
        assert body["phase"] == "week1"
        assert body["day_index"] == 2
        assert body["activities"] == list(activities_for_day(2))
    finally:
        _cleanup(child_id)


def test_today_404s_when_week1_done_and_no_plan_exists_yet() -> None:
    child_id = uuid.uuid4()
    _mark_days_complete(child_id, range(1, 8))
    try:
        response = client.get(f"/children/{child_id}/today")
        assert response.status_code == 404
    finally:
        _cleanup(child_id)


def test_today_returns_plan_phase_once_week1_done_and_plan_exists() -> None:
    child_id = uuid.uuid4()
    _mark_days_complete(child_id, range(1, 8))
    db = SessionLocal()
    try:
        plan = Plan(child_id=child_id, version=1, status="active", created_by="engine")
        db.add(plan)
        db.commit()
        plan_id = plan.id
    finally:
        db.close()

    try:
        response = client.get(f"/children/{child_id}/today")
        assert response.status_code == 200
        body = response.json()
        assert body["phase"] == "plan"
        assert body["day_index"] is None
        assert body["activities"] == []
        assert body["plan_id"] == str(plan_id)
    finally:
        _cleanup(child_id)
