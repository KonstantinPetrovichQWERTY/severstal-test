from datetime import datetime
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.routes.coils.schemas import CoilSchema, PartialCoilSchema, UpdatePartialCoilSchema
from src.database.models import Coil
from src.routes.coils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["coils"])


@router.post(
    "/api/v1/coils/register_new_coil/",
    response_model=CoilSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_coil(
    coil_data: PartialCoilSchema,
    session: AsyncSession = Depends(get_db),
):

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


@router.get(
    "/api/v1/coils/{coil_id}/",
    response_model=CoilSchema,
    status_code=status.HTTP_200_OK,
)
async def get_coil_by_id(coil_id: uuid.UUID, session: AsyncSession = Depends(get_db)):

    tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
    coil = tmp_result.scalars().first()

    if coil is None:
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

    tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
    coil = tmp_result.scalars().first()

    if coil is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    for field, value in coil_data.model_dump(exclude_unset=True).items():
        setattr(coil, field, value)

    await session.commit()
    await session.refresh(coil)

    return coil


@router.get("/api/v1/coils/", response_model=list[CoilSchema])
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

    result = await session.execute(query)
    return result.scalars().all()


@router.delete("/api/v1/coils/{coil_id}")
async def delete_coil(
    coil_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):

    tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
    coil = tmp_result.scalars().first()

    if coil is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coil with ID {coil_id} not found",
        )

    await session.delete(coil)
    await session.commit()

    return coil
