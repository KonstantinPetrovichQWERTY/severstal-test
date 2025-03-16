from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field, model_validator


class PartialCoilSchema(BaseModel):
    length: float = Field(gt=0)
    weight: float = Field(gt=0)
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @model_validator(mode='after')
    def check_dates(self):
        if self.created_at and self.deleted_at and self.deleted_at < self.created_at:
            raise ValueError('deleted_at must be > than created_at')
        return self

class CoilSchema(PartialCoilSchema):
    coil_id: uuid.UUID


class UpdatePartialCoilSchema(BaseModel):
    length: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    @model_validator(mode='after')
    def check_dates(self):
        if self.created_at and self.deleted_at and self.deleted_at < self.created_at:
            raise ValueError('deleted_at must be > than created_at')
        return self


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
