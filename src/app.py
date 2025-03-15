from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.utils import get_service_name
from src.version import __version__
from src.settings import settings
from src.routes.healthchecks.views import router as health_router
from src.routes.coils.views import router as coils_router
from src.routes.coils.database import sessionmanager


def create_app(init_db: bool = True) -> FastAPI:
    lifespan = None

    if init_db:
        sessionmanager.init(settings.db_connection_url)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(
        title=get_service_name(),
        version=__version__,
        middleware=[],
        lifespan=lifespan,
    )

    app.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    app.include_router(health_router)
    app.include_router(coils_router)

    return app
