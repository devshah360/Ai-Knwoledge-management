from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logger import logger

async def global_exception_handler(
    request: Request,
    exe: Exception
):

    logger.error(
        f"Error on {request.method} {request.url}: {str(exe)}"
    )

    return JSONResponse(
        status_code=500,
        content={"message": str(exe)}
    )