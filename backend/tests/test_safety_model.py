import uuid
from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import Child, Guardian, SafetyFlag


def _make_child(db) -> Child:
    guardian = Guardian(
        name="Test Guardian", relationship="mother", phone=f"+92300{uuid.uuid4().int % 10**7:07d}"
    )
    db.add(guardian)
    db.flush()
    child = Child(
        guardian_id=guardian.id,
        name="Test Child",
        date_of_birth=date(2020, 1, 1),
        area="karachi",
        schooling="home_school",
        home_languages=["urdu"],
    )
    db.add(child)
    db.flush()
    return child


def _cleanup(db, child_id: uuid.UUID) -> None:
    db.rollback()
    child = db.get(Child, child_id)
    if child is not None:
        guardian_id = child.guardian_id
        db.delete(child)
        db.commit()
        guardian = db.get(Guardian, guardian_id)
        if guardian is not None:
            db.delete(guardian)
            db.commit()


def test_safety_flag_defaults_to_open_status() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    child_id = child.id
    try:
        flag = SafetyFlag(child_id=child.id, rule="very_low_self_confidence", evidence={"score": 5})
        db.add(flag)
        db.commit()

        fetched = db.get(SafetyFlag, flag.id)
        assert fetched is not None
        assert fetched.status == "open"
        assert fetched.reviewer_id is None
        assert fetched.created_at is not None
    finally:
        _cleanup(db, child_id)
        db.close()


def test_safety_flag_rejects_invalid_status() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    child_id = child.id
    try:
        db.add(SafetyFlag(child_id=child.id, rule="very_low_self_confidence", status="ignored"))
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        _cleanup(db, child_id)
        db.close()


def test_safety_flag_requires_an_existing_child() -> None:
    db = SessionLocal()
    try:
        db.add(SafetyFlag(child_id=uuid.uuid4(), rule="very_low_self_confidence"))
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.close()


def test_deleting_child_cascades_to_safety_flags() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    child_id = child.id
    try:
        flag = SafetyFlag(child_id=child.id, rule="very_low_self_confidence")
        db.add(flag)
        db.commit()
        flag_id = flag.id

        db.delete(db.get(Child, child_id))
        db.commit()
        db.expire_all()
        assert db.get(SafetyFlag, flag_id) is None
    finally:
        _cleanup(db, child_id)
        db.close()
