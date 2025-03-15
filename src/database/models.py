import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Coil(Base):
    __tablename__ = "Coil"

    coil_id: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )

    length: int = Column(BigInteger)
    weight: int = Column(BigInteger)
    created_at: datetime = Column(DateTime)
    deleted_at: datetime = Column(DateTime, nullable=True)
