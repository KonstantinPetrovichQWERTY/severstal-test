from typing import Optional
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy database models."""
    pass


class Coil(Base):
    """Database model representing coils.

    Attributes:
        coil_id: Universally unique identifier (primary key)
        length: Coil length in meters (must be positive)
        weight: Coil weight in kilograms (must be positive)
        created_at: Timestamp of coil creation (timezone-aware)
        deleted_at: Timestamp of soft deletion (timezone-aware, nullable)

    Table Constraints:
        - Length and weight values must be greater than 0
    """
    __tablename__ = "Coil"

    coil_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    length: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint("length > 0", name="check_length_positive"),
        CheckConstraint("weight > 0", name="check_weight_positive"),
    )
