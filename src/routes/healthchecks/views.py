from http import HTTPStatus

from fastapi import APIRouter
from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    create_async_engine
)


from src.routes.healthchecks.schema import HealthCheckReadinessOutScheme
from src.routes.healthchecks.spec import API
from src.settings import settings

router = APIRouter(tags=["health-checks"])


@router.get(API.LIVENESS, status_code=HTTPStatus.OK)
async def liveness() -> None:
    return


@router.get(
    API.READINESS,
    status_code=HTTPStatus.OK,
    response_model=HealthCheckReadinessOutScheme,
)
async def readiness():
    items = []
    msg = ""

    is_alive_database = False
    try:
        engine = create_async_engine(url=settings.db_connection_url)
        async with engine.connect() as connect:
            await connect.execute(select(1))
        msg = "Have is connection to database"
        is_alive_database = True
    except ConnectionError:
        msg = "No connection to database"
    finally:
        items.append({"service": "database", "is_alive": is_alive_database, "msg": msg})
    response = {"items": items}
    return response
