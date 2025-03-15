from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class PartialCoilSchema(BaseModel):
    length: float
    weight: float
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class CoilSchema(PartialCoilSchema):
    coil_id: uuid.UUID


class UpdatePartialCoilSchema(BaseModel):
    length: Optional[float] = None
    weight: Optional[float] = None
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class CoilStatsSchema(BaseModel):
    total_added: int
    total_removed: int
    avg_length: float
    avg_weight: float
    max_length: float
    min_length: float
    max_weight: float
    min_weight: float
    total_weight: float
    max_duration: Optional[float]
    min_duration: Optional[float]
