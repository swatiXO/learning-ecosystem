import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SignalEvent(Base):
    __tablename__ = "signal_events"

    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    child_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    activity_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    activity: Mapped[str] = mapped_column(String, index=True)
    activity_version: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)
    ts_client: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ts_server: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
