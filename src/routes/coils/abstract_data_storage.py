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

    @staticmethod
    @abstractmethod
    async def get_coil_by_id(session: AsyncSession, coil_id: uuid.UUID) -> CoilSchema:
        """_summary_

        Args:
            session (AsyncSession): _description_
            coil_id (uuid.UUID): _description_

        Returns:
            CoilSchema: _description_
        """
        pass

    @staticmethod
    @abstractmethod
    async def register_new_coil(
        session: AsyncSession, coil_data: PartialCoilSchema
    ) -> CoilSchema:
        pass

    @staticmethod
    @abstractmethod
    async def update_coil(
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

    @staticmethod
    @abstractmethod
    async def get_all_coils(
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
            coil_id (Optional[uuid.UUID], optional): _description_. Defaults to None.
            weight_gte (Optional[float], optional): _description_. Defaults to None.
            weight_lte (Optional[float], optional): _description_. Defaults to None.
            length_gte (Optional[float], optional): _description_. Defaults to None.
            length_lte (Optional[float], optional): _description_. Defaults to None.
            created_at_gte (Optional[datetime], optional): _description_. Defaults to None.
            created_at_lte (Optional[datetime], optional): _description_. Defaults to None.
            deleted_at_gte (Optional[datetime], optional): _description_. Defaults to None.
            deleted_at_lte (Optional[datetime], optional): _description_. Defaults to None.

        Returns:
            list[CoilSchema]: _description_
        """
        pass

    @staticmethod
    @abstractmethod
    async def delete_coil(
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

    @staticmethod
    @abstractmethod
    async def get_coil_stats(
        session: AsyncSession,
        created_at_gte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
    ) -> CoilStatsSchema:
        """_summary_

        Args:
            session (AsyncSession): _description_
            created_at_gte (Optional[datetime], optional): _description_. Defaults to None.
            deleted_at_lte (Optional[datetime], optional): _description_. Defaults to None.

        Returns:
            CoilStatsSchema: _description_
        """
        pass
