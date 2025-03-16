import time
from typing import Callable

import structlog
from fastapi import Request


logger = structlog.get_logger(__name__)


async def logging_middleware(request: Request, call_next: Callable):
    start_time = time.time()

    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        headers=dict(request.headers),
        query_params=dict(request.query_params),
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(
            "Request failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
        )
        raise

    process_time = (time.time() - start_time) * 1000
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=f"{process_time:.2f}ms",
    )

    return response
