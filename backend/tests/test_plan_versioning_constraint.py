import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import Plan


def test_only_one_active_plan_per_child_at_db_level() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        db.add(Plan(child_id=child_id, version=1, status="active", created_by="engine"))
        db.commit()

        # A fresh session (not the one that inserted the first row) attempting a second
        # active plan for the same child — a clean test of the DB constraint itself,
        # not an ORM identity-map artifact.
        second_db = SessionLocal()
        try:
            second_db.add(Plan(child_id=child_id, version=2, status="active", created_by="engine"))
            with pytest.raises(IntegrityError):
                second_db.commit()
        finally:
            second_db.rollback()
            second_db.close()
    finally:
        db.query(Plan).filter_by(child_id=child_id).delete()
        db.commit()
        db.close()


def test_superseding_then_inserting_active_is_allowed() -> None:
    child_id = uuid.uuid4()
    db = SessionLocal()
    try:
        first = Plan(child_id=child_id, version=1, status="active", created_by="engine")
        db.add(first)
        db.commit()

        first.status = "superseded"
        db.add(Plan(child_id=child_id, version=2, status="active", created_by="engine"))
        db.commit()  # must not raise — only one row has status="active" at a time
    finally:
        db.query(Plan).filter_by(child_id=child_id).delete()
        db.commit()
        db.close()
