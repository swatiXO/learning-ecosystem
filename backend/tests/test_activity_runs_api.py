import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.db import SessionLocal
from app.main import app
from app.models import ChildSession, Plan, PlanModule, SignalEvent, SkillScore, Week1Progress
from app.models.sessions import WEEK1_DAYS
from app.week1.gate import current_day_index
from app.week1.schedule import activities_for_day

client = TestClient(app)


def _create_session(child_id: uuid.UUID | None = None) -> uuid.UUID:
    db = SessionLocal()
    try:
        session = ChildSession(child_id=child_id or uuid.uuid4())
        db.add(session)
        db.commit()
        db.refresh(session)
        return session.id
    finally:
        db.close()


def _delete_session(session_id: uuid.UUID) -> None:
    # Cascades to any activity_runs created against it.
    db = SessionLocal()
    try:
        session = db.get(ChildSession, session_id)
        if session is not None:
            db.delete(session)
            db.commit()
    finally:
        db.close()


def test_create_activity_run_requires_existing_session() -> None:
    response = client.post(
        "/activity-runs",
        json={
            "session_id": str(uuid.uuid4()),
            "activity": "stars_not_clouds",
            "activity_version": "1.0.0",
        },
    )
    assert response.status_code == 404


def test_create_activity_run_starts_open() -> None:
    session_id = _create_session()
    try:
        response = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "stars_not_clouds",
                "activity_version": "1.0.0",
                "day_index": 1,
            },
        )
        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "started"
        assert body["ended_at"] is None
        assert body["day_index"] == 1
    finally:
        _delete_session(session_id)


def test_create_activity_run_rejects_unregistered_activity() -> None:
    session_id = _create_session()
    try:
        response = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "not_a_real_activity",
                "activity_version": "1.0.0",
            },
        )
        assert response.status_code == 422
    finally:
        _delete_session(session_id)


@pytest.mark.parametrize("day_index", [0, 8])
def test_create_activity_run_rejects_out_of_range_day_index(day_index: int) -> None:
    session_id = _create_session()
    try:
        response = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "stars_not_clouds",
                "activity_version": "1.0.0",
                "day_index": day_index,
            },
        )
        assert response.status_code == 422
    finally:
        _delete_session(session_id)


@pytest.mark.parametrize("status", ["completed", "skipped", "quit"])
def test_update_activity_run_accepts_non_fail_statuses(status: str) -> None:
    session_id = _create_session()
    try:
        created = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "stars_not_clouds",
                "activity_version": "1.0.0",
            },
        )
        run_id = created.json()["id"]

        response = client.patch(f"/activity-runs/{run_id}", json={"status": status})
        assert response.status_code == 200
        assert response.json()["status"] == status
        assert response.json()["ended_at"] is not None
    finally:
        _delete_session(session_id)


def test_update_activity_run_rejects_fail_status() -> None:
    session_id = _create_session()
    try:
        created = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "stars_not_clouds",
                "activity_version": "1.0.0",
            },
        )
        run_id = created.json()["id"]

        response = client.patch(f"/activity-runs/{run_id}", json={"status": "failed"})
        assert response.status_code == 422
    finally:
        _delete_session(session_id)


def test_update_activity_run_same_status_is_idempotent() -> None:
    session_id = _create_session()
    try:
        created = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "stars_not_clouds",
                "activity_version": "1.0.0",
            },
        )
        run_id = created.json()["id"]

        first = client.patch(f"/activity-runs/{run_id}", json={"status": "completed"})
        second = client.patch(f"/activity-runs/{run_id}", json={"status": "completed"})
        assert second.status_code == 200
        assert second.json()["ended_at"] == first.json()["ended_at"]
    finally:
        _delete_session(session_id)


def test_update_activity_run_conflicting_transition_returns_409() -> None:
    session_id = _create_session()
    try:
        created = client.post(
            "/activity-runs",
            json={
                "session_id": str(session_id),
                "activity": "stars_not_clouds",
                "activity_version": "1.0.0",
            },
        )
        run_id = created.json()["id"]

        client.patch(f"/activity-runs/{run_id}", json={"status": "completed"})
        response = client.patch(f"/activity-runs/{run_id}", json={"status": "skipped"})
        assert response.status_code == 409
    finally:
        _delete_session(session_id)


def test_update_activity_run_not_found_returns_404() -> None:
    response = client.patch(f"/activity-runs/{uuid.uuid4()}", json={"status": "completed"})
    assert response.status_code == 404


def test_completing_days_activities_advances_the_week1_gate() -> None:
    # End-to-end wiring check: PATCH /activity-runs/{id} is what actually feeds the
    # week1_progress table (app/week1/gate.py), not just a status field in isolation.
    child_id = uuid.uuid4()
    session_id = _create_session(child_id)
    try:
        assert current_day_index_for(child_id) == 1

        activities = activities_for_day(1)
        for i, activity in enumerate(activities):
            created = client.post(
                "/activity-runs",
                json={
                    "session_id": str(session_id),
                    "activity": activity,
                    "activity_version": "1.0.0",
                    "day_index": 1,
                },
            )
            run_id = created.json()["id"]
            # Rule #5: a skip still finishes the day, same as a completion.
            status = "skipped" if i == 0 else "completed"
            response = client.patch(f"/activity-runs/{run_id}", json={"status": status})
            assert response.status_code == 200

        assert current_day_index_for(child_id) == 2
    finally:
        _delete_session(session_id)
        db = SessionLocal()
        try:
            db.query(Week1Progress).filter_by(child_id=child_id).delete()
            db.commit()
        finally:
            db.close()


def current_day_index_for(child_id: uuid.UUID) -> int | None:
    db = SessionLocal()
    try:
        return current_day_index(db, child_id)
    finally:
        db.close()


def test_finishing_day_seven_triggers_scoring_and_a_generated_plan() -> None:
    # Issue #39: nothing used to call recompute_scores/regenerate_plan when week 1
    # finished. Drive a child through all 7 days for real, via the actual API, and
    # confirm a plan now exists afterward instead of the 404 GET /today used to hit.
    child_id = uuid.uuid4()
    session_id = _create_session(child_id)
    try:
        for day in range(1, WEEK1_DAYS + 1):
            for activity in activities_for_day(day):
                created = client.post(
                    "/activity-runs",
                    json={
                        "session_id": str(session_id),
                        "activity": activity,
                        "activity_version": "1.0.0",
                        "day_index": day,
                    },
                )
                run_id = created.json()["id"]

                if activity == "stars_not_clouds":
                    # The only registered extractor needs real events to score anything —
                    # an activity-run alone carries no signal_events.
                    client.post(
                        "/events/batch",
                        json={
                            "events": [
                                {
                                    "event_id": str(uuid.uuid4()),
                                    "child_id": str(child_id),
                                    "session_id": str(session_id),
                                    "activity_run_id": run_id,
                                    "activity": "stars_not_clouds",
                                    "activity_version": "1.0.0",
                                    "event_type": "tap",
                                    "ts_client": datetime.now(UTC).isoformat(),
                                    "payload": {
                                        "target": "star",
                                        "correct": True,
                                        "reaction_ms": 400,
                                    },
                                }
                                for _ in range(5)
                            ]
                        },
                    )

                response = client.patch(f"/activity-runs/{run_id}", json={"status": "completed"})
                assert response.status_code == 200

        assert current_day_index_for(child_id) is None  # week 1 fully complete

        plan_response = client.get(f"/children/{child_id}/plan")
        assert plan_response.status_code == 200
        assert plan_response.json()["created_by"] == "engine"

        db = SessionLocal()
        try:
            scores = db.query(SkillScore).filter_by(child_id=child_id).all()
            assert len(scores) > 0
            assert all(s.is_baseline for s in scores)
        finally:
            db.close()
    finally:
        _delete_session(session_id)
        db = SessionLocal()
        try:
            db.query(Week1Progress).filter_by(child_id=child_id).delete()
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
