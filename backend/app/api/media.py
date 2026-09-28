import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ActivityRun, Child, ChildSession, Consent, MediaObject
from app.schemas.media import MediaUploadUrlIn, MediaUploadUrlOut
from app.storage import presigned_upload_url

router = APIRouter(tags=["media"])


@router.post("/media/upload-url", response_model=MediaUploadUrlOut, status_code=201)
def create_media_upload_url(
    payload: MediaUploadUrlIn, db: Session = Depends(get_db)
) -> MediaUploadUrlOut:
    if db.get(Child, payload.child_id) is None:
        raise HTTPException(status_code=404, detail="Child not found")

    # The activity_run must actually belong to a session for THIS child - otherwise a
    # client could attach media to another child's activity run just by guessing its id.
    run = db.scalar(
        select(ActivityRun)
        .join(ChildSession, ActivityRun.session_id == ChildSession.id)
        .where(
            ActivityRun.id == payload.activity_run_id,
            ChildSession.child_id == payload.child_id,
        )
    )
    if run is None:
        raise HTTPException(status_code=404, detail="Activity run not found for this child")

    # Rule #6: consent is checked server-side against the child's active grant, never
    # trusted from the client.
    consent = db.scalar(
        select(Consent)
        .where(Consent.child_id == payload.child_id, Consent.revoked_at.is_(None))
        .order_by(Consent.granted_at.desc())
    )
    if consent is None or not (consent.audio if payload.kind == "audio" else consent.video):
        raise HTTPException(
            status_code=403, detail=f"No active {payload.kind} consent for this child"
        )

    media_id = uuid.uuid4()
    storage_key = f"{payload.kind}/{media_id}"
    # Signed locally (no network call) - computed before the insert so a signing failure
    # never leaves behind a media_objects row with no usable URL.
    upload_url = presigned_upload_url(storage_key)

    db.add(
        MediaObject(
            id=media_id,
            child_id=payload.child_id,
            activity_run_id=payload.activity_run_id,
            kind=payload.kind,
            storage_key=storage_key,
            consent_id=consent.id,
        )
    )
    db.commit()

    return MediaUploadUrlOut(
        media_object_id=media_id, upload_url=upload_url, storage_key=storage_key
    )
