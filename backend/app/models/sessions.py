import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# Skips and quits are comfort signals, not failures (PROJECT.md rule #5), so there is no
# "failed" status.
ACTIVITY_RUN_STATUSES = ("started", "completed", "skipped", "quit")
WEEK1_DAYS = 7


class ChildSession(Base):
    """A play session. Named ChildSession so it never shadows sqlalchemy.orm.Session."""

    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    device_info: Mapped[dict] = mapped_column(JSONB, default=dict)
    mood_before: Mapped[str | None] = mapped_column(String, nullable=True)
    mood_after: Mapped[str | None] = mapped_column(String, nullable=True)


class ActivityRun(Base):
    __tablename__ = "activity_runs"
    __table_args__ = (
        CheckConstraint(
            "status IN (" + ", ".join(f"'{s}'" for s in ACTIVITY_RUN_STATUSES) + ")",
            name="ck_activity_runs_status",
        ),
        CheckConstraint(
            f"day_index IS NULL OR day_index BETWEEN 1 AND {WEEK1_DAYS}",
            name="ck_activity_runs_day_index",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), index=True
    )
    activity: Mapped[str] = mapped_column(String, index=True)
    activity_version: Mapped[str] = mapped_column(String)
    day_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String, default="started")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Week1Progress(Base):
    """One row per completed week-1 day. Missed calendar days add no row, so they never
    count against the child (PRD FR-7)."""

    __tablename__ = "week1_progress"
    __table_args__ = (
        CheckConstraint(
            f"day_index BETWEEN 1 AND {WEEK1_DAYS}", name="ck_week1_progress_day_index"
        ),
    )

    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    day_index: Mapped[int] = mapped_column(Integer, primary_key=True)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
