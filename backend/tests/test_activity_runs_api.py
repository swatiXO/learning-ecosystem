import uuid

import pytest
from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models import ChildSession

client = TestClient(app)


def _create_session() -> uuid.UUID:
    db = SessionLocal()
    try:
        session = ChildSession(child_id=uuid.uuid4())
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
