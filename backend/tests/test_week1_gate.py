import uuid
from collections.abc import Sequence

from app.db import SessionLocal
from app.models import ActivityRun, ChildSession, Week1Progress
from app.week1.gate import completed_days, current_day_index, is_week1_complete, try_complete_day
from app.week1.schedule import activities_for_day


def _log_runs(db, child_id: uuid.UUID, day_index: int, statuses: Sequence[str]) -> None:
    """One ActivityRun per (activity, status) pair against day_index's scheduled activities."""
    session = ChildSession(child_id=child_id)
    db.add(session)
    db.flush()
    # Not zip(..., strict=True): some tests intentionally log fewer statuses than
    # activities, to simulate the day being only partially done.
    for activity, status in zip(activities_for_day(day_index), statuses):
        db.add(
            ActivityRun(
                session_id=session.id,
                activity=activity,
                activity_version="1.0.0",
                day_index=day_index,
                status=status,
            )
        )
    db.commit()


def _cleanup(db, child_id: uuid.UUID) -> None:
    # Deleting each session cascades to its activity_runs.
    for session in db.query(ChildSession).filter_by(child_id=child_id).all():
        db.delete(session)
    db.query(Week1Progress).filter_by(child_id=child_id).delete()
    db.commit()


def test_current_day_index_starts_at_one_for_a_new_child() -> None:
    db = SessionLocal()
    try:
        assert current_day_index(db, uuid.uuid4()) == 1
        assert is_week1_complete(db, uuid.uuid4()) is False
    finally:
        db.close()


def test_try_complete_day_false_when_activities_incomplete() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        activities = activities_for_day(1)
        _log_runs(db, child_id, 1, ["completed"] * (len(activities) - 1))
        assert try_complete_day(db, child_id, 1) is False
        assert completed_days(db, child_id) == set()
    finally:
        _cleanup(db, child_id)
        db.close()


def test_try_complete_day_counts_skip_and_quit_as_done() -> None:
    # Rule #5: skips and quits are comfort signals, not failures — they finish a day just
    # like completing does. Day 1 has exactly 3 activities.
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        _log_runs(db, child_id, 1, ["completed", "skipped", "quit"])
        assert try_complete_day(db, child_id, 1) is True
        assert completed_days(db, child_id) == {1}
    finally:
        _cleanup(db, child_id)
        db.close()


def test_try_complete_day_is_idempotent() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        _log_runs(db, child_id, 1, ["completed", "skipped", "quit"])
        assert try_complete_day(db, child_id, 1) is True
        # Calling again (e.g. a second activity in the day finishing afterwards) must not
        # error on the week1_progress primary key, and correctly reports "not newly done".
        assert try_complete_day(db, child_id, 1) is False
        assert completed_days(db, child_id) == {1}
    finally:
        _cleanup(db, child_id)
        db.close()


def test_current_day_index_advances_after_day_complete() -> None:
    # FR-7: nothing here is calendar-based — day 2 becomes current the instant day 1's
    # activities are logged, no matter how much real time passes either side of that.
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        activities = activities_for_day(1)
        _log_runs(db, child_id, 1, ["completed"] * len(activities))
        try_complete_day(db, child_id, 1)
        assert current_day_index(db, child_id) == 2
    finally:
        _cleanup(db, child_id)
        db.close()


def test_is_week1_complete_true_only_once_day_seven_is_done() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        for day in range(1, 7):
            db.add(Week1Progress(child_id=child_id, day_index=day))
        db.commit()
        assert is_week1_complete(db, child_id) is False
        assert current_day_index(db, child_id) == 7

        db.add(Week1Progress(child_id=child_id, day_index=7))
        db.commit()
        assert is_week1_complete(db, child_id) is True
        assert current_day_index(db, child_id) is None
    finally:
        _cleanup(db, child_id)
        db.close()
