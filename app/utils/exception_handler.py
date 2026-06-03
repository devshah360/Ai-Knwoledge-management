from fastapi import Request
from fastapi.responses import JSONResponse

async def global_exception_handler(request:Request,exe:Exception):
        return JSONResponse(status_code=500,content={"message":str(exe)})