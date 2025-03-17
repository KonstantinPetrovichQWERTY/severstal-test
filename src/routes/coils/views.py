from datetime import datetime
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
import structlog

from src.routes.coils.dao import dao
from src.routes.coils.exceptions import CoilNotFoundException
from src.routes.coils.schemas import (
    CoilSchema,
    CoilStatsSchema,
    PartialCoilSchema,
    UpdatePartialCoilSchema,
)
from src.routes.coils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["coils"])
logger = structlog.get_logger()


@router.post(
    "/api/v1/coils/register_new_coil/",
    response_model=CoilSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_coil(
    coil_data: PartialCoilSchema,
    session: AsyncSession = Depends(get_db),
):
    """Register a new coil in the system.

    Creates a new coil record.

    Args:
        coil_data (PartialCoilSchema):
            - length: Initial length in meters (must be > 0)
            - weight: Initial weight in kilograms (must be > 0)
            - created_at: Creation timestamp
        session (AsyncSession): Database session dependency

    Returns:
        CoilSchema: Created coil data with system-generated UUID

    Raises:
        HTTPException: 422 if input validation fails
    """

    logger.info("register_new_coil: started", coil_data=coil_data.model_dump())

    new_coil = await dao.register_new_coil(session=session, coil_data=coil_data)

    logger.info("register_new_coil: completed", coil_id=new_coil.coil_id)
    return new_coil


@router.get(
    "/api/v1/coils/{coil_id}/",
    response_model=CoilSchema,
    status_code=status.HTTP_200_OK,
)
async def get_coil_by_id(coil_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    """Retrieve coil by ID.

    Args:
        coil_id (uuid.UUID): ID of the coil to retrieve
        session (AsyncSession): Database session dependency

    Returns:
        CoilSchema: Complete coil data including deletion timestamp if available

    Raises:
        HTTPException: 404 if no coil exists with the specified ID
    """

    logger.info("get_coil_by_id: started", coil_id=coil_id)

    try:
        coil = await dao.get_coil_by_id(session=session, coil_id=coil_id)
    except CoilNotFoundException:
        logger.warning("get_coil_by_id: coil not found", coil_id=coil_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    logger.info("get_coil_by_id: completed", coil_id=coil_id)
    return coil


@router.patch("/api/v1/coils/{coil_id}/", response_model=CoilSchema)
async def update_coil(
    coil_id: uuid.UUID,
    coil_data: UpdatePartialCoilSchema,
    session: AsyncSession = Depends(get_db),
):
    """Update partial information of an existing coil.

    Allows partial updates of coil properties.

    Args:
        coil_id (uuid.UUID): ID of the coil to update
        coil_data (UpdatePartialCoilSchema):
            - length: New length in meters (optional, must be > 0 if provided)
            - weight: New weight in kilograms (optional, must be > 0 if provided)
            - created_at: New creation timestamp to update (optional)
            - deleted_at: New deletion timestamp to update (optional)
        session (AsyncSession): Database session dependency

    Returns:
        CoilSchema: Updated coil data

    Raises:
        HTTPException:
            404 if no coil exists with the specified ID
            422 if timestamp validation fails
    """
    logger.info(
        "update_coil: started", coil_id=coil_id, coil_data=coil_data.model_dump()
    )

    try:
        coil = await dao.update_coil(
            session=session, coil_id=coil_id, coil_data=coil_data
        )
    except CoilNotFoundException:
        logger.warning("update_coil: coil not found", coil_id=coil_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    logger.info("update_coil: completed", coil_id=coil_id)
    return coil


@router.get("/api/v1/coils/", response_model=List[CoilSchema])
async def get_all_coils(
    coil_id: Optional[uuid.UUID] = None,
    weight_gte: Optional[float] = None,
    weight_lte: Optional[float] = None,
    length_gte: Optional[float] = None,
    length_lte: Optional[float] = None,
    created_at_gte: Optional[datetime] = None,
    created_at_lte: Optional[datetime] = None,
    deleted_at_gte: Optional[datetime] = None,
    deleted_at_lte: Optional[datetime] = None,
    session: AsyncSession = Depends(get_db),
):
    """Retrieve filtered list of coils with optional query parameters.

    Supports filtering by:
    - Exact coil ID
    - Weight range (greater/less than or equal)
    - Length range (greater/less than or equal)
    - Creation timestamp range
    - Deletion timestamp range

    Args:
        coil_id (Optional[uuid.UUID]): Filter by exact coil ID
        weight_gte (Optional[float]): Minimum weight in kilograms
        weight_lte (Optional[float]): Maximum weight in kilograms
        length_gte (Optional[float]): Minimum length in meters
        length_lte (Optional[float]): Maximum length in meters
        created_at_gte (Optional[datetime]): Earliest creation timestamp
        created_at_lte (Optional[datetime]): Latest creation timestamp
        deleted_at_gte (Optional[datetime]): Earliest deletion timestamp
        deleted_at_lte (Optional[datetime]): Latest deletion timestamp
        session (AsyncSession): Database session dependency

    Returns:
        List[CoilSchema]: Matching coils

    Raises:
        HTTPException: 404 if no coils match the filters
    """
    logger.info(
        "get_all_coils: started",
        filters={
            "coil_id": coil_id,
            "weight_gte": weight_gte,
            "weight_lte": weight_lte,
            "length_gte": length_gte,
            "length_lte": length_lte,
            "created_at_gte": created_at_gte,
            "created_at_lte": created_at_lte,
            "deleted_at_gte": deleted_at_gte,
            "deleted_at_lte": deleted_at_lte,
        },
    )

    try:
        coils = await dao.get_all_coils(
            session=session,
            coil_id=coil_id,
            weight_gte=weight_gte,
            weight_lte=weight_lte,
            length_gte=length_gte,
            length_lte=length_lte,
            created_at_gte=created_at_gte,
            created_at_lte=created_at_lte,
            deleted_at_gte=deleted_at_gte,
            deleted_at_lte=deleted_at_lte,
        )
    except CoilNotFoundException:
        logger.warning("Coils not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coils not found",
        )

    logger.info("get_all_coils: completed", number_of_coils=len(coils))
    return coils


@router.delete("/api/v1/coils/{coil_id}", response_model=CoilSchema)
async def delete_coil(
    coil_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    """Delete a coil.

    Args:
        coil_id (uuid.UUID): Unique identifier of the coil to delete
        session (AsyncSession): Database session dependency

    Returns:
        CoilSchema: Deleted coil data

    Raises:
        HTTPException: 404 if no coil exists with the specified ID
    """
    logger.info("delete_coil: started", coil_id=coil_id)

    try:
        coil = await dao.delete_coil(session=session, coil_id=coil_id)
    except CoilNotFoundException:
        logger.warning("delete_coil: coil not found", coil_id=coil_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    logger.info("delete_coil: completed", coil_id=coil_id)
    return coil


@router.get("/api/v1/statistics/coils/", response_model=CoilStatsSchema)
async def get_coil_stats(
    created_at_gte: Optional[datetime] = None,
    deleted_at_lte: Optional[datetime] = None,
    session: AsyncSession = Depends(get_db),
):
    """Comprehensive statistics for coils within a time window.

    Statistics include:
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
        created_at_gte (Optional[datetime]): Include coils created after this timestamp
        deleted_at_lte (Optional[datetime]): Include coils deleted before this timestamp
        session (AsyncSession): Database session dependency

    Returns:
        CoilStatsSchema: Complete statistical summary

    Raises:
        HTTPException: 404 if no data exists in specified time window
    """
    logger.info(
        "get_coil_stats: started", dates_period=[created_at_gte, deleted_at_lte]
    )

    try:
        stats = await dao.get_coil_stats(
            session=session,
            created_at_gte=created_at_gte,
            deleted_at_lte=deleted_at_lte,
        )
    except CoilNotFoundException:
        logger.warning(
            "get_coil_stats: No coils found for the given period",
            dates_period=[created_at_gte, deleted_at_lte],
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No coils found for given period {created_at_gte, deleted_at_lte}",
        )

    logger.info("get_coil_stats: completed")
    return stats
