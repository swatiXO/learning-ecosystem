import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# schooling is a fixed two-value field (PROJECT.md §6), so it gets a DB CHECK. Other
# option lists (relationship, area, languages, gender, avatar, grade) are placeholders
# pending open decision D7 and are validated in Pydantic against app/onboarding/options.py
# instead, so extending them never needs a migration.
SCHOOLING_VALUES = ("school", "home_school")


class Guardian(Base):
    __tablename__ = "guardians"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    relationship: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, unique=True, index=True)
    locale: Mapped[str] = mapped_column(String, default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class School(Base):
    __tablename__ = "schools"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    area: Mapped[str] = mapped_column(String)


class Child(Base):
    __tablename__ = "children"
    __table_args__ = (
        CheckConstraint(
            "schooling IN (" + ", ".join(f"'{s}'" for s in SCHOOLING_VALUES) + ")",
            name="ck_children_schooling",
        ),
        CheckConstraint(
            "schooling != 'school' OR school_id IS NOT NULL",
            name="ck_children_school_requires_school_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guardian_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("guardians.id"), index=True
    )
    name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    area: Mapped[str] = mapped_column(String)
    schooling: Mapped[str] = mapped_column(String)
    school_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("schools.id"), nullable=True
    )
    grade: Mapped[str | None] = mapped_column(String, nullable=True)
    home_languages: Mapped[list[str]] = mapped_column(ARRAY(String))
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    onboarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Consent(Base):
    """One row per consent grant. A new consent (e.g. from POST /children/{id}/consent)
    never overwrites an old row — it revokes the previous active row and inserts a new
    one, keeping full history."""

    __tablename__ = "consents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), index=True
    )
    guardian_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("guardians.id"))
    version: Mapped[str] = mapped_column(String)
    audio: Mapped[bool] = mapped_column(Boolean)
    video: Mapped[bool] = mapped_column(Boolean)
    teacher_share: Mapped[bool] = mapped_column(Boolean, default=False)
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
