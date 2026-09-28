from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class MediaUploadUrlIn(BaseModel):
    child_id: UUID
    activity_run_id: UUID
    kind: Literal["audio", "video"]


class MediaUploadUrlOut(BaseModel):
    media_object_id: UUID
    upload_url: str
    storage_key: str
