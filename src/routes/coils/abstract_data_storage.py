from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes.coils.schemas import (
    CoilSchema,
    CoilStatsSchema,
    PartialCoilSchema,
    UpdatePartialCoilSchema,
)


class DataStorage(ABC):
    """Abstract base class defining operations for coil data storage management."""

    @abstractmethod
    async def get_coil_by_id(
        self, session: AsyncSession, coil_id: uuid.UUID
    ) -> CoilSchema:
        """Retrieve a single coil by its unique identifier.

        Args:
            session (AsyncSession): Asynchronous database session
            coil_id (uuid.UUID): Unique identifier of the coil to retrieve

        Returns:
            CoilSchema: Complete pydantic coil schema
        """
        pass

    @abstractmethod
    async def register_new_coil(
        self, session: AsyncSession, coil_data: PartialCoilSchema
    ) -> CoilSchema:
        """Create a new coil record in the database.

        Args:
            session (AsyncSession): Asynchronous database session
            coil_data (PartialCoilSchema): Required data for coil creation

        Returns:
            CoilSchema: Newly created coil with generated ID field
        """
        pass

    @abstractmethod
    async def update_coil(
        self,
        session: AsyncSession,
        coil_id: uuid.UUID,
        coil_data: UpdatePartialCoilSchema,
    ) -> CoilSchema:
        """Update specified fields of an existing coil.

        Args:
            session (AsyncSession): Asynchronous database session
            coil_id (uuid.UUID): Unique identifier of the coil to update
            coil_data (UpdatePartialCoilSchema): Fields to update with new values

        Returns:
            CoilSchema: Updated coil data representation
        """
        pass

    @abstractmethod
    async def get_all_coils(
        self,
        session: AsyncSession,
        coil_id: Optional[uuid.UUID] = None,
        weight_gte: Optional[float] = None,
        weight_lte: Optional[float] = None,
        length_gte: Optional[float] = None,
        length_lte: Optional[float] = None,
        created_at_gte: Optional[datetime] = None,
        created_at_lte: Optional[datetime] = None,
        deleted_at_gte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
    ) -> list[CoilSchema]:
        """Retrieve coils with optional filtering parameters.

        Args:
            session (AsyncSession): Asynchronous database session
            coil_id (Optional[uuid.UUID]): Filter by specific coil ID
            weight_gte (Optional[float]): Minimum weight filter (>= value)
            weight_lte (Optional[float]): Maximum weight filter (<= value)
            length_gte (Optional[float]): Minimum length filter (>= value)
            length_lte (Optional[float]): Maximum length filter (<= value)
            created_at_gte (Optional[datetime]): Minimum creation timestamp filter
            created_at_lte (Optional[datetime]): Maximum creation timestamp filter
            deleted_at_gte (Optional[datetime]): Minimum deletion timestamp filter
            deleted_at_lte (Optional[datetime]): Maximum deletion timestamp filter

        Returns:
            list[CoilSchema]: List of coils matching filter criteria
        """
        pass

    @abstractmethod
    async def delete_coil(
        self,
        session: AsyncSession,
        coil_id: uuid.UUID,
    ) -> CoilSchema:
        """Perform deletion of a coil from database.

        Args:
            session (AsyncSession): Asynchronous database session
            coil_id (uuid.UUID): Unique identifier of the coil to delete

        Returns:
            CoilSchema: Representation of the deleted coil
        """
        pass

    @abstractmethod
    async def get_coil_stats(
        self,
        session: AsyncSession,
        created_at_gte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
    ) -> CoilStatsSchema:
        """Calculate aggregate statistics for coils within specified time window.

        Args:
            session (AsyncSession): Asynchronous database session
            created_at_gte (Optional[datetime]): Coils created after this timestamp
            deleted_at_lte (Optional[datetime]): Coils deleted before this timestamp

        Returns:
            CoilStatsSchema: Aggregated statistics
        """
        pass
