from datetime import datetime
import uuid
from pydantic import BaseModel


class PartialCoilSchema(BaseModel):
    length: int
    weight: int
    created_at: datetime
    deleted_at: datetime

class CoilSchema(PartialCoilSchema):
    coil_id: uuid.UUID
