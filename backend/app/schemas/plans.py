from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator


class PlanModuleOut(BaseModel):
    module: str
    weight: float


class PlanOut(BaseModel):
    id: UUID
    child_id: UUID
    version: int
    status: str
    rationale: dict[str, Any]
    created_by: str
    created_at: datetime
    modules: list[PlanModuleOut]


class PlanModuleIn(BaseModel):
    module: str
    weight: float


class PlanOverrideIn(BaseModel):
    modules: list[PlanModuleIn]
    rationale: dict[str, Any] = {}

    @field_validator("modules")
    @classmethod
    def modules_not_empty(cls, value: list[PlanModuleIn]) -> list[PlanModuleIn]:
        if not value:
            raise ValueError("at least one module is required")
        return value
