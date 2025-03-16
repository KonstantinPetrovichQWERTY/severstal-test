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

    @abstractmethod
    async def get_coil_by_id(
        self, session: AsyncSession, coil_id: uuid.UUID
    ) -> CoilSchema:
        """_summary_

        Args:
            session (AsyncSession): _description_
            coil_id (uuid.UUID): _description_

        Returns:
            CoilSchema: _description_
        """
        pass

    @abstractmethod
    async def register_new_coil(
        self, session: AsyncSession, coil_data: PartialCoilSchema
    ) -> CoilSchema:
        pass

    @abstractmethod
    async def update_coil(
        self,
        session: AsyncSession,
        coil_id: uuid.UUID,
        coil_data: UpdatePartialCoilSchema,
    ) -> CoilSchema:
        """_summary_

        Args:
            session (AsyncSession): _description_
            coil_id (uuid.UUID): _description_
            coil_data (UpdatePartialCoilSchema): _description_

        Returns:
            CoilSchema: _description_
        """ """_summary_

        Args:
            coil_id (uuid.UUID): _description_
            coil_data (UpdatePartialCoilSchema): _description_
            session (AsyncSession): _description_
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
        """_summary_

        Args:
            session (AsyncSession): _description_
            coil_id (Optional[uuid.UUID], optional): = None.
            weight_gte (Optional[float], optional): = None.
            weight_lte (Optional[float], optional): = None.
            length_gte (Optional[float], optional): = None.
            length_lte (Optional[float], optional): = None.
            created_at_gte (Optional[datetime], optional): = None.
            created_at_lte (Optional[datetime], optional): = None.
            deleted_at_gte (Optional[datetime], optional): = None.
            deleted_at_lte (Optional[datetime], optional): = None.

        Returns:
            list[CoilSchema]: _description_
        """
        pass

    @abstractmethod
    async def delete_coil(
        self,
        session: AsyncSession,
        coil_id: uuid.UUID,
    ) -> CoilSchema:
        """_summary_

        Args:
            session (AsyncSession): _description_
            coil_id (uuid.UUID): _description_

        Returns:
            CoilSchema: _description_
        """
        pass

    @abstractmethod
    async def get_coil_stats(
        self,
        session: AsyncSession,
        created_at_gte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
    ) -> CoilStatsSchema:
        """_summary_

        Args:
            session (AsyncSession): _description_
            created_at_gte (Optional[datetime], optional): = None.
            deleted_at_lte (Optional[datetime], optional): = None.

        Returns:
            CoilStatsSchema: _description_
        """
        pass
