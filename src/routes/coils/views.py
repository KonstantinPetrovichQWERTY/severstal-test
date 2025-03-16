from datetime import datetime
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.routes.coils.dao import CoilPostgreDAO
from src.routes.coils.exceptions import CoilNotFoundException
from src.routes.coils.schemas import (
    CoilSchema,
    CoilStatsSchema,
    PartialCoilSchema,
    UpdatePartialCoilSchema,
)
from src.database.models import Coil
from src.routes.coils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["coils"])

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
    new_coil = await dao.register_new_coil(session=session, coil_data=coil_data)
    return new_coil


@router.get(
    "/api/v1/coils/{coil_id}/",
    response_model=CoilSchema,
    status_code=status.HTTP_200_OK,
)
async def get_coil_by_id(coil_id: uuid.UUID, session: AsyncSession = Depends(get_db)):

    try:
        coil = await dao.get_coil_by_id(session=session, coil_id=coil_id)
    except CoilNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    return coil


@router.patch("/api/v1/coils/{coil_id}/", response_model=CoilSchema)
async def update_coil(
    coil_id: uuid.UUID,
    coil_data: UpdatePartialCoilSchema,
    session: AsyncSession = Depends(get_db),
):

    try:
        coil = await dao.update_coil(
            session=session, coil_id=coil_id, coil_data=coil_data
        )
    except CoilNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coils not found",
        )

    return coils


@router.delete("/api/v1/coils/{coil_id}", response_model=CoilSchema)
async def delete_coil(
    coil_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):

    try:
        coil = await dao.delete_coil(session=session, coil_id=coil_id)
    except CoilNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    return coil


@router.get("/api/v1/coils/stats/", response_model=CoilStatsSchema)
async def get_coil_stats(
    created_at_gte: Optional[datetime] = None,
    deleted_at_lte: Optional[datetime] = None,
    session: AsyncSession = Depends(get_db),
):

    query = select(Coil)

    if created_at_gte:
        query = query.where(Coil.created_at >= created_at_gte)
    if deleted_at_lte:
        query = query.where(Coil.deleted_at <= deleted_at_lte)

    tmp_result = await session.execute(query)
    coils = tmp_result.scalars().all()

    if not coils:
        raise HTTPException(
            status_code=404, detail="No rolls found for the given period"
        )

    total_added = len(coils)
    total_removed = len([coil for coil in coils if coil.deleted_at is not None])
    lengths = [coil.length for coil in coils]
    weights = [coil.weight for coil in coils]
    durations = [
        (
            (coil.deleted_at - coil.created_at).total_seconds()
            if coil.deleted_at and coil.created_at
            else None
        )
        for coil in coils
    ]

    stats = CoilStatsSchema(
        total_added=total_added,
        total_removed=total_removed,
        avg_length=sum(lengths) / total_added,
        avg_weight=sum(weights) / total_added,
        max_length=max(lengths),
        min_length=min(lengths),
        max_weight=max(weights),
        min_weight=min(weights),
        total_weight=sum(weights),
        max_duration=max(d for d in durations if d is not None),
        min_duration=min(d for d in durations if d is not None),
    )
    return stats
