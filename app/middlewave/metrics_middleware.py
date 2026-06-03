import time

from starlette.middleware.base import (
    BaseHTTPMiddleware
)


class MetricsMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start = time.time()

        response = await call_next(
            request
        )

        end = time.time()

        duration = end - start

        print(
            request.url.path,
            duration
        )

        return response