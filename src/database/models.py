import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Coil(Base):
    __tablename__ = "Coil"

    coil_id: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )

    length: int = Column(Float)
    weight: int = Column(Float)
    created_at: datetime = Column(DateTime(timezone=True), nullable=True)
    deleted_at: datetime = Column(DateTime(timezone=True), nullable=True)
