from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field, field_validator, model_validator


class PartialCoilSchema(BaseModel):
    """Base schema for coil creation.

    Attributes:
        length: Coil length in meters (must be greater than 0)
        weight: Coil weight in kilograms (must be greater than 0)
        created_at: Timestamp of coil creation
        deleted_at: Optional timestamp of coil deletion/removal

    Validates:
        deleted_at must be later than created_at if both are provided
    """

    length: float = Field(gt=0)
    weight: float = Field(gt=0)
    created_at: datetime
    deleted_at: Optional[datetime] = None

    @model_validator(mode="after")
    def check_dates(self):
        """Ensure logical relationship between creation and deletion timestamps."""
        if self.created_at and self.deleted_at and self.deleted_at < self.created_at:
            raise ValueError("deleted_at must be > than created_at")
        return self


class CoilSchema(PartialCoilSchema):
    """Complete coil representation including system-generated ID.

    Extends PartialCoilSchema with:
        coil_id: Universally unique identifier for the coil
    """

    coil_id: uuid.UUID


class UpdatePartialCoilSchema(BaseModel):
    """Schema for partial updates of coil properties with validation constraints.

    Fields:
        length: Optional new length in meters (if provided, must be > 0)
        weight: Optional new weight in kilograms (if provided, must be > 0)
        created_at: Optional creation timestamp update
        deleted_at: Optional deletion timestamp update

    Validates:
        - created_at cannot be set to None if provided
        - deleted_at must be later than created_at when both are provided
    """

    length: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    @field_validator("created_at")
    def check_created_at(cls, value):
        """Prevent nullification of creation timestamp."""
        if value is None:
            raise ValueError("created_at cannot be null")
        return value

    @model_validator(mode="after")
    def check_dates(self):
        """Maintain temporal consistency between timestamps."""
        if self.created_at and self.deleted_at and self.deleted_at < self.created_at:
            raise ValueError("deleted_at must be > than created_at")
        return self


class CoilStatsSchema(BaseModel):
    """Comprehensive statistics summary for coil inventory analysis.

    Attributes:
        total_added: Total number of coils created in timeframe
        total_removed: Total number of coils deleted in timeframe
        avg_length: Mean length of all coils
        avg_weight: Mean weight of all coils
        max_length: Maximum coil length observed
        min_length: Minimum coil length observed
        max_weight: Maximum coil weight observed
        min_weight: Minimum coil weight observed
        total_weight: Combined weight of all coils
        max_duration: Longest lifetime (creation to deletion) in days
        min_duration: Shortest lifetime (creation to deletion) in days
        max_count_day: Date with highest number of coil operations
        min_count_day: Date with lowest number of coil operations
        max_weight_day: Date with largest total weight change
        min_weight_day: Date with smallest total weight change
    """

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
    max_count_day: Optional[datetime]
    min_count_day: Optional[datetime]
    max_weight_day: Optional[datetime]
    min_weight_day: Optional[datetime]
