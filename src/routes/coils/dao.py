from datetime import datetime
from typing import Optional, List
import uuid

from sqlalchemy import and_, case, func, select
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
        """Retrieve multiple coils with optional range filters.

        Args:
            session: Async database session
            coil_id: Exact coil ID filter
            weight_gte: Minimum weight filter (>=)
            weight_lte: Maximum weight filter (<=)
            length_gte: Minimum length filter (>=)
            length_lte: Maximum length filter (<=)
            created_at_gte: Earliest creation timestamp filter
            created_at_lte: Latest creation timestamp filter
            deleted_at_gte: Earliest deletion timestamp filter
            deleted_at_lte: Latest deletion timestamp filter

        Returns:
            List of CoilSchema representations matching filters

        Raises:
            CoilNotFoundException: If no coils match the criteria
        """
        query = select(Coil)

        # It's weird, but filtering IDs by range is even weirder :)
        # So I created `get_coil_by_id`
        if coil_id is not None:
            query = query.filter(Coil.coil_id == coil_id)

        filters_ranges = {
            "weight": (weight_gte, weight_lte),
            "length": (length_gte, length_lte),
            "created_at": (created_at_gte, created_at_lte),
            "deleted_at": (deleted_at_gte, deleted_at_lte),
        }

        for field, (gte, lte) in filters_ranges.items():
            if gte is not None:
                query = query.filter(getattr(Coil, field) >= gte)
            if lte is not None:
                query = query.filter(getattr(Coil, field) <= lte)

        tmp_result = await session.execute(query)
        coils = tmp_result.scalars().all()

        if not coils:
            raise CoilNotFoundException()

        result = [
            CoilSchema(
                length=coil.length,
                weight=coil.weight,
                created_at=coil.created_at,
                deleted_at=coil.deleted_at,
                coil_id=coil.coil_id,
            )
            for coil in coils
        ]

        return result

    async def get_coil_by_id(
        self, session: AsyncSession, coil_id: uuid.UUID
    ) -> CoilSchema:
        """Retrieve a single coil by its unique identifier.

        Args:
            session: Async database session
            coil_id: UUID of coil to retrieve

        Returns:
            CoilSchema representation of found coil

        Raises:
            CoilNotFoundException: If no coil exists with specified ID
        """
        tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
        coil = tmp_result.scalars().first()

        if coil is None:
            raise CoilNotFoundException()

        result = CoilSchema(
            length=coil.length,
            weight=coil.weight,
            created_at=coil.created_at,
            deleted_at=coil.deleted_at,
            coil_id=coil.coil_id,
        )
        return result

    async def register_new_coil(
        self, session: AsyncSession, coil_data: PartialCoilSchema
    ) -> CoilSchema:
        """Create and persist a new coil record.

        Args:
            session: Async database session
            coil_data:
                length: Coil length in meters (must be greater than 0)
                weight: Coil weight in kilograms (must be greater than 0)
                created_at: Timestamp of coil creation
                deleted_at: Optional timestamp of coil deletion/removal

        Returns:
            CoilSchema of newly created coil with generated UUID
        """
        new_coil = Coil(
            length=coil_data.length,
            weight=coil_data.weight,
            created_at=coil_data.created_at,
            deleted_at=coil_data.deleted_at,
        )

        session.add(new_coil)
        await session.commit()
        await session.refresh(new_coil)

        result = CoilSchema(
            length=new_coil.length,
            weight=new_coil.weight,
            created_at=new_coil.created_at,
            deleted_at=new_coil.deleted_at,
            coil_id=new_coil.coil_id,
        )
        return result

    async def delete_coil(
        self, session: AsyncSession, coil_id: uuid.UUID
    ) -> CoilSchema:
        """Permanently delete a coil from the database.

        Args:
            session: Async database session
            coil_id: UUID of coil to delete

        Returns:
            CoilSchema representation of deleted coil

        Raises:
            CoilNotFoundException: If specified coil doesn't exist
        """
        tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
        coil = tmp_result.scalars().first()

        if coil is None:
            raise CoilNotFoundException()

        await session.delete(coil)
        await session.commit()

        result = CoilSchema(
            length=coil.length,
            weight=coil.weight,
            created_at=coil.created_at,
            deleted_at=coil.deleted_at,
            coil_id=coil.coil_id,
        )
        return result

    async def update_coil(
        self,
        session: AsyncSession,
        coil_id: uuid.UUID,
        coil_data: UpdatePartialCoilSchema,
    ) -> CoilSchema:
        """Update specific fields of an existing coil.

        Args:
            session: Async database session
            coil_id: UUID of coil to update
            coil_data: Schema containing fields to update

        Returns:
            Updated CoilSchema representation

        Raises:
            CoilNotFoundException: If specified coil doesn't exist
        """
        tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
        coil = tmp_result.scalars().first()

        if coil is None:
            raise CoilNotFoundException()

        for field, value in coil_data.model_dump(exclude_unset=True).items():
            setattr(coil, field, value)

        if coil.deleted_at is not None and coil.created_at is not None:
            if coil.deleted_at < coil.created_at:
                raise ValueError("deleted_at must be later than created_at")

        await session.commit()
        await session.refresh(coil)

        result = CoilSchema(
            length=coil.length,
            weight=coil.weight,
            created_at=coil.created_at,
            deleted_at=coil.deleted_at,
            coil_id=coil.coil_id,
        )
        return result

    async def get_coil_stats(
        self,
        session: AsyncSession,
        created_at_gte: Optional[datetime] = None,
        deleted_at_lte: Optional[datetime] = None,
    ) -> CoilStatsSchema:
        """Generate comprehensive statistics for coils within time window.

        Calculates:
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

        Args:
            session: Async database session
            created_at_gte: Include coils created after this timestamp
            deleted_at_lte: Include coils deleted before this timestamp

        Returns:
            CoilStatsSchema with aggregated statistics

        Raises:
            CoilNotFoundException: If no data exists in time window
        """
        filters = []

        if created_at_gte:
            filters.append(Coil.created_at >= created_at_gte)
        if deleted_at_lte:
            filters.append(Coil.deleted_at <= deleted_at_lte)

        stats_query = select(
            func.count(Coil.coil_id).label("total_added"),
            func.sum(case((Coil.deleted_at.isnot(None), 1), else_=0)).label(
                "total_removed"
            ),
            func.avg(Coil.length).label("avg_length"),
            func.avg(Coil.weight).label("avg_weight"),
            func.max(Coil.length).label("max_length"),
            func.min(Coil.length).label("min_length"),
            func.max(Coil.weight).label("max_weight"),
            func.min(Coil.weight).label("min_weight"),
            func.sum(Coil.weight).label("total_weight"),
            func.max(func.extract("epoch", Coil.deleted_at - Coil.created_at)).label(
                "max_duration"
            ),
            func.min(func.extract("epoch", Coil.deleted_at - Coil.created_at)).label(
                "min_duration"
            ),
        ).where(and_(*filters))

        tmp_result = await session.execute(stats_query)
        stats = tmp_result.fetchone()

        if stats is None or stats.total_added == 0:
            raise CoilNotFoundException("No coils found for the given period")

        count_day_query = (
            select(
                func.date(Coil.created_at).label("day"),
                func.count(Coil.coil_id).label("count"),
            )
            .where(and_(*filters))
            .group_by(func.date(Coil.created_at))
            .order_by(func.count(Coil.coil_id).desc())
        )

        weight_day_query = (
            select(
                func.date(Coil.created_at).label("day"),
                func.sum(Coil.weight).label("total_weight"),
            )
            .where(and_(*filters))
            .group_by(func.date(Coil.created_at))
            .order_by(func.sum(Coil.weight).desc())
        )

        tmp_count_day_result = await session.execute(count_day_query)
        count_days = tmp_count_day_result.fetchall()

        tmp_weight_day_result = await session.execute(weight_day_query)
        weight_days = tmp_weight_day_result.fetchall()

        result = CoilStatsSchema(
            total_added=stats.total_added,
            total_removed=stats.total_removed,
            avg_length=stats.avg_length,
            avg_weight=stats.avg_weight,
            max_length=stats.max_length,
            min_length=stats.min_length,
            max_weight=stats.max_weight,
            min_weight=stats.min_weight,
            total_weight=stats.total_weight,
            max_duration=stats.max_duration,
            min_duration=stats.min_duration,
            max_count_day=count_days[0].day if count_days else None,
            min_count_day=count_days[-1].day if count_days else None,
            max_weight_day=weight_days[0].day if weight_days else None,
            min_weight_day=weight_days[-1].day if weight_days else None,
        )

        return result


dao = CoilPostgreDAO()
