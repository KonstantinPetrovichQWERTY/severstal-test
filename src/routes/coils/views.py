from datetime import datetime
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
import structlog

from src.routes.coils.dao import CoilPostgreDAO
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
dao = CoilPostgreDAO()


@router.post(
    "/api/v1/coils/register_new_coil/",
    response_model=CoilSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_coil(
    coil_data: PartialCoilSchema,
    session: AsyncSession = Depends(get_db),
):
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
            detail=f"No coils found for the given period {created_at_gte, deleted_at_lte}",
        )

    logger.info("get_coil_stats: completed")
    return stats
