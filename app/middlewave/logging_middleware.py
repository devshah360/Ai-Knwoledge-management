from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger
import time


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        logger.info(f"{request.method} {request.url}")

        response = await call_next(request)

        end = time.time()

        logger.info(
            f"Execution Time: {end - start:.2f} seconds"
        )

        return response