from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from src.routes.coils.schemas import CoilSchema, PartialCoilSchema
from src.database.models import Coil
from src.routes.coils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["bags"])


@router.post(
    "/api/v1/coils/register_new_coil/",
    response_model=CoilSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_bag(
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
async def get_coil_by_id(coil_id: str, session: AsyncSession = Depends(get_db)):

    tmp_result = await session.execute(select(Coil).where(Coil.coil_id == coil_id))
    coil = tmp_result.scalars().first()

    if coil is None:
        raise HTTPException(status_code=404, detail="Coil not found")

    return coil
