import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import ActivityRun, ChildSession, Week1Progress


def test_session_with_activity_run_round_trip() -> None:
    db = SessionLocal()
    try:
        session = ChildSession(child_id=uuid.uuid4(), device_info={"os": "android"})
        db.add(session)
        db.flush()

        run = ActivityRun(
            session_id=session.id,
            activity="stars_not_clouds",
            activity_version="1.0.0",
            day_index=1,
        )
        db.add(run)
        db.commit()
        run_id = run.id

        fetched = db.get(ActivityRun, run_id)
        assert fetched is not None
        assert fetched.status == "started"
        assert fetched.started_at is not None
        assert fetched.ended_at is None

        # Deleting the session cascades to its activity runs.
        db.delete(db.get(ChildSession, session.id))
        db.commit()
        db.expire_all()
        assert db.get(ActivityRun, run_id) is None
    finally:
        db.close()


@pytest.mark.parametrize("status", ["completed", "skipped", "quit"])
def test_activity_run_accepts_non_fail_statuses(status: str) -> None:
    db = SessionLocal()
    try:
        session = ChildSession(child_id=uuid.uuid4())
        db.add(session)
        db.flush()
        db.add(
            ActivityRun(
                session_id=session.id,
                activity="stars_not_clouds",
                activity_version="1.0.0",
                status=status,
            )
        )
        db.commit()

        db.delete(session)
        db.commit()
    finally:
        db.close()


def test_activity_run_rejects_failed_status() -> None:
    # Rule #5: there is no fail state.
    db = SessionLocal()
    try:
        session = ChildSession(child_id=uuid.uuid4())
        db.add(session)
        db.flush()
        db.add(
            ActivityRun(
                session_id=session.id,
                activity="stars_not_clouds",
                activity_version="1.0.0",
                status="failed",
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.close()


def test_week1_progress_one_row_per_day() -> None:
    db = SessionLocal()
    child_id = uuid.uuid4()
    try:
        db.add(Week1Progress(child_id=child_id, day_index=1))
        db.commit()

        fetched = db.get(Week1Progress, (child_id, 1))
        assert fetched is not None
        assert fetched.completed_at is not None

        db.add(Week1Progress(child_id=child_id, day_index=1))
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.query(Week1Progress).filter_by(child_id=child_id).delete()
        db.commit()
        db.close()


@pytest.mark.parametrize("day_index", [0, 8])
def test_week1_progress_rejects_out_of_range_day(day_index: int) -> None:
    db = SessionLocal()
    try:
        db.add(Week1Progress(child_id=uuid.uuid4(), day_index=day_index))
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.close()
