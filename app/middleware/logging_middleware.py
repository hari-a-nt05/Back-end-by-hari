import time
from collections.abc import Awaitable
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.utils.logging_utils import setup_logger

logger = setup_logger("uvicorn_access")


class LoggingMiddleware(BaseHTTPMiddleware):  # type: ignore[misc]
    # Annotate `call_next` as a callable function that returns an Awaitable[Response]
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()

        # Await the call_next function to get the response
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        # Log the request details and processing time
        logger.info(
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} "
            f"({process_time:.2f} ms)"
        )

        # Return the response
        return response
