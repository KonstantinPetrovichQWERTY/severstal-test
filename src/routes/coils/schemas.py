from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class PartialCoilSchema(BaseModel):
    length: int
    weight: int
    created_at: datetime
    deleted_at: Optional[datetime]

class CoilSchema(PartialCoilSchema):
    coil_id: uuid.UUID
