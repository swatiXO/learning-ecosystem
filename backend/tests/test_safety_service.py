from datetime import date

from app.db import SessionLocal
from app.models import Child, Guardian, SafetyFlag, SkillScore
from app.safety.service import flag_serious_signals


def _make_child(db, phone: str) -> Child:
    guardian = Guardian(name="Test Guardian", relationship="mother", phone=phone)
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


def _cleanup(child_id) -> None:
    db = SessionLocal()
    try:
        db.query(SafetyFlag).filter_by(child_id=child_id).delete()
        db.query(SkillScore).filter_by(child_id=child_id).delete()
        db.commit()
        child = db.get(Child, child_id)
        if child is not None:
            guardian_id = child.guardian_id
            db.delete(child)
            db.commit()
            guardian = db.get(Guardian, guardian_id)
            if guardian is not None:
                db.delete(guardian)
                db.commit()
    finally:
        db.close()


def test_flag_serious_signals_creates_a_flag_with_evidence() -> None:
    db = SessionLocal()
    child = _make_child(db, "+923001110001")
    db.add(
        SkillScore(
            child_id=child.id,
            dimension="self_confidence",
            score=5,
            confidence=0.8,
            is_baseline=False,
        )
    )
    db.commit()
    child_id = child.id
    db.close()

    try:
        db = SessionLocal()
        try:
            flags = flag_serious_signals(db, child_id)
        finally:
            db.close()

        assert len(flags) == 1
        assert flags[0].rule == "very_low_self_confidence"
        assert flags[0].status == "open"
        assert flags[0].evidence == {
            "dimension": "self_confidence",
            "score": 5.0,
            "confidence": 0.8,
        }
    finally:
        _cleanup(child_id)


def test_flag_serious_signals_does_not_duplicate_an_open_flag() -> None:
    db = SessionLocal()
    child = _make_child(db, "+923001110002")
    db.add(
        SkillScore(
            child_id=child.id,
            dimension="self_confidence",
            score=5,
            confidence=0.8,
            is_baseline=False,
        )
    )
    db.commit()
    child_id = child.id
    db.close()

    try:
        db = SessionLocal()
        try:
            first = flag_serious_signals(db, child_id)
            second = flag_serious_signals(db, child_id)
        finally:
            db.close()

        assert len(first) == 1
        assert second == []
    finally:
        _cleanup(child_id)


def test_flag_serious_signals_reflags_after_the_open_flag_is_resolved() -> None:
    # A dismissed/reviewed flag from a past evaluation must not suppress a genuinely new
    # one - only a currently *open* flag for the same rule does.
    db = SessionLocal()
    child = _make_child(db, "+923001110003")
    db.add(
        SkillScore(
            child_id=child.id,
            dimension="self_confidence",
            score=5,
            confidence=0.8,
            is_baseline=False,
        )
    )
    db.commit()
    child_id = child.id
    db.close()

    try:
        db = SessionLocal()
        try:
            first = flag_serious_signals(db, child_id)
            first_id = first[0].id
            db.query(SafetyFlag).filter_by(id=first_id).update({"status": "dismissed"})
            db.commit()

            second = flag_serious_signals(db, child_id)
            second_id = second[0].id
        finally:
            db.close()

        assert len(second) == 1
        assert second_id != first_id
    finally:
        _cleanup(child_id)


def test_flag_serious_signals_returns_nothing_for_a_healthy_profile() -> None:
    db = SessionLocal()
    child = _make_child(db, "+923001110004")
    db.add(
        SkillScore(
            child_id=child.id,
            dimension="self_confidence",
            score=80,
            confidence=0.8,
            is_baseline=False,
        )
    )
    db.commit()
    child_id = child.id
    db.close()

    try:
        db = SessionLocal()
        try:
            flags = flag_serious_signals(db, child_id)
        finally:
            db.close()
        assert flags == []
    finally:
        _cleanup(child_id)
