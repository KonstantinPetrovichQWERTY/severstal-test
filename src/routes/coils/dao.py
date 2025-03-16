from datetime import datetime
from typing import Optional, List
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Coil
from src.routes.coils.abstract_data_storage import DataStorage
from src.routes.coils.exceptions import CoilNotFoundException
from src.routes.coils.schemas import (
    CoilSchema,
    CoilStatsSchema,
    PartialCoilSchema,
    UpdatePartialCoilSchema,
)


class CoilPostgreDAO(DataStorage):

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
    ) -> List[CoilSchema]:
        pass

    async def get_coil_by_id(self, session: AsyncSession, coil_id: uuid.UUID) -> CoilSchema:

        tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
        coil = tmp_result.scalars().first()

        if coil is None:
            raise CoilNotFoundException()

        return coil

    async def register_new_coil(
        self, session: AsyncSession, coil_data: PartialCoilSchema
    ) -> CoilSchema:

        new_coil = Coil(
            length=coil_data.length,
            weight=coil_data.weight,
            created_at=coil_data.created_at,
            deleted_at=coil_data.deleted_at,
        )

        session.add(new_coil)
        await session.commit()
        await session.refresh(new_coil)

        return new_coil

    async def delete_coil(self, session: AsyncSession, coil_id: uuid.UUID) -> CoilSchema:
        tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
        coil = tmp_result.scalars().first()

        if coil is None:
            raise CoilNotFoundException()

        await session.delete(coil)
        await session.commit()

        return coil

    async def update_coil(
        self,
        session: AsyncSession,
        coil_id: uuid.UUID,
        coil_data: UpdatePartialCoilSchema,
    ) -> CoilSchema:
        tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
        coil = tmp_result.scalars().first()

        if coil is None:
            raise CoilNotFoundException()

        for field, value in coil_data.model_dump(exclude_unset=True).items():
            setattr(coil, field, value)

        await session.commit()
        await session.refresh(coil)

        return coil

    async def get_coil_stats(
        self,
        session: AsyncSession,
        created_at_gte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
    ) -> CoilStatsSchema:
        pass
