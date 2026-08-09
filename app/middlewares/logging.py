import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

logger = logging.getLogger("app.access")

class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        logger.info(
            f"Method: {request.method} Path: {request.url.path}"
            f"Status Code: {response.status_code} Process Time: {process_time:.4f}s"
        )

        return response
