import datetime
from fastapi import APIRouter, Depends, status

from src.routes.coils.schemas import CoilSchema, PartialCoilSchema
from src.database.models import Coil
from src.routes.coils.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["bags"])

@router.get("/")
async def read_root():
    return {"hi": "q"}


@router.post(
    "/api/v1/bags/register_new_coil/",
    response_model=CoilSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_bag(
    coil_data: PartialCoilSchema, session: AsyncSession = Depends(get_db)
):

    new_coil = Coil(
        length = coil_data.length,
        weight = coil_data.weight,
        created_at = coil_data.created_at,
        deleted_at = None,
    )

    session.add(new_coil)
    await session.commit()
    await session.refresh(new_coil)

    return new_coil
