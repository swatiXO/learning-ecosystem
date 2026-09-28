"""Week-1 gate logic (rule #4: nothing unlocks before day 7 completes).

Completion is purely event-driven — there is no calendar-day tracking anywhere here, so a
missed day never counts against the child (PRD FR-7): a child who disappears for two weeks
resumes on exactly the day they left off.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import ActivityRun, ChildSession, Week1Progress
from app.models.sessions import WEEK1_DAYS
from app.week1.schedule import activities_for_day

# Rule #5: skips and quits are comfort signals, not failures — they count as "done with
# this activity for now" exactly like completing it, so none of them can block the gate.
TERMINAL_STATUSES = ("completed", "skipped", "quit")


def completed_days(db: Session, child_id: uuid.UUID) -> set[int]:
    return set(
        db.scalars(select(Week1Progress.day_index).where(Week1Progress.child_id == child_id)).all()
    )


def current_day_index(db: Session, child_id: uuid.UUID) -> int | None:
    """The next week-1 day this child hasn't finished, or None once week 1 is complete."""
    done = completed_days(db, child_id)
    for day in range(1, WEEK1_DAYS + 1):
        if day not in done:
            return day
    return None


def is_week1_complete(db: Session, child_id: uuid.UUID) -> bool:
    return current_day_index(db, child_id) is None


def try_complete_day(db: Session, child_id: uuid.UUID, day_index: int) -> bool:
    """Marks `day_index` complete for `child_id` if every activity scheduled for that day
    has at least one terminal run logged against it. Safe to call repeatedly (idempotent)
    — e.g. after every activity-run status change, not just the one that finishes the day.

    Returns True only if this call is what completed the day.
    """
    required = set(activities_for_day(day_index))

    done_activities = set(
        db.scalars(
            select(ActivityRun.activity)
            .join(ChildSession, ActivityRun.session_id == ChildSession.id)
            .where(
                ChildSession.child_id == child_id,
                ActivityRun.day_index == day_index,
                ActivityRun.status.in_(TERMINAL_STATUSES),
            )
            .distinct()
        ).all()
    )

    if not required.issubset(done_activities):
        return False

    result = db.execute(
        insert(Week1Progress)
        .values(child_id=child_id, day_index=day_index)
        .on_conflict_do_nothing(index_elements=["child_id", "day_index"])
        .returning(Week1Progress.day_index)
    )
    newly_completed = result.first() is not None
    db.commit()
    return newly_completed
